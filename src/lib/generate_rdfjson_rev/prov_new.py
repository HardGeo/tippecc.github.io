import os
import json
import os.path as path

from collections import defaultdict
import prov
import xmltodict as xmltodict
from prov.model import ProvDocument
from rdflib import Namespace
import sys



# Specify the directory path
dir = os.path.dirname(os.path.abspath(__file__))
prov_base = path.join( dir, "..", "prov_meta_revised" )
prov_path = path.join( dir, "..", "prov_meta_revised", "prov" )
meta_path = path.join( dir, "..", "prov_meta_revised", "meta" )

prov_metadata_path = os.path.join(dir, "..", "prov_meta_revised", "prov_metadata_template.json")

with open(prov_metadata_path, 'r', encoding='utf-8') as file:
    prov_metadata = json.load(file)



def flatten_meta_data(meta_data, parent_key='', counter=None):
    """
    Flattens a nested dictionary:
    - Keys become 'parent.child' (e.g., citation_scenario_source.doi).
    - Adds 'tippecc_data:' if key doesn't already contain ':'.
    - Appends _1, _2, ... to avoid duplicates.
    - Lists are converted to comma-separated strings.
    - Empty dicts become empty strings.
    """
    if counter is None:
        counter = defaultdict(int)

    items = []

    for key, value in meta_data.items():
        full_key = f"{parent_key}.{key}" if parent_key else key
        base_key = full_key if ':' in full_key else f"tippecc_data:{full_key}"

        if isinstance(value, dict):
            if not value:
                items.append((make_unique_key(base_key, counter), ''))
            else:
                items.extend(flatten_meta_data(value, parent_key=full_key, counter=counter).items())
        elif isinstance(value, list):
            items.append((make_unique_key(base_key, counter), ', '.join(map(str, value))))
        else:
            items.append((make_unique_key(base_key, counter), value))

    return dict(items)


def make_unique_key(key, counter):
    count = counter[key]
    counter[key] += 1
    return key if count == 0 else f"{key}_{count}"



def qualify_metadata_values(metadata: dict, d1, people_namespace, orgs_namespace, software_namespace):
    qualified = {}
    for k, v in metadata.items():
        if isinstance(v, str):
            raw = v.strip()
            if raw.startswith("ORG__"):
                qualified[k] = d1.valid_qualified_name(f"{orgs_namespace}:{raw}")
            elif raw.startswith("SOFTWARE__"):
                qualified[k] = d1.valid_qualified_name(f"{software_namespace}:{raw}")
            elif raw.startswith("PERSON__"):
                qualified[k] = d1.valid_qualified_name(f"{people_namespace}:{raw}")
            else:
                qualified[k] = raw
        else:
            qualified[k] = v  # Optional: du kannst hier auch weiter rekursiv durch Dictionaries gehen
    return qualified

def get_prov_metadata(key, prov_path, namespace="tippecc_data:"):
    """
    Retrieves and processes provenance metadata for a given key.

    Args:
        key (str): The metadata key to look up in the provenance metadata file.
        prov_path (str): The path to the directory containing the "prov_metadata_template.json" file.
        namespace (str, optional): The namespace to prepend to keys that do not already contain a colon (':').
                                   Defaults to "tippecc_data:".

    Returns:
        tuple: A tuple containing:
            - str: The namespaced version of the input key.
            - dict: A dictionary of processed metadata where:
                - Keys are prefixed with the namespace if they did not contain a colon.
                - Values are extracted from nested dictionaries if they contain "@key" or "@id".

    Process:
        1. The function constructs the full path to the metadata JSON file.
        2. It opens and loads the JSON file into a dictionary.
        3. It extracts the metadata associated with the given key, defaulting to an empty dictionary if not found.
        4. It iterates over the extracted metadata:
            - If a key does not contain a colon, the provided namespace is prepended.
            - If a value is a dictionary and contains "@key", the function replaces the value with "@key"'s content.
            - If a value is a dictionary and contains "@id", the function replaces the value with "@id"'s content.
        5. The function returns the namespaced key and the processed metadata dictionary.
    """


    metadata = prov_metadata.get(key, {})

    # SOFTWARE-Verarbeitung
    if isinstance(key, str) and key.startswith("SOFTWARE__") and isinstance(metadata.get("sdo:targetProduct"), dict):
        target = metadata.get("sdo:targetProduct")
        version = metadata.get("sdo:softwareVersion")
        if "@id" in target:
            target_id = target["@id"]
            if isinstance(target_id, str) and target_id.startswith("SOFTWARE__"):
                metadata = prov_metadata.get(target_id, {})
                if version:
                    metadata["sdo:softwareVersion"] = version


    updated_metadata = {}

    for k, v in metadata.items():
        # Ergänze default namespace, falls kein Präfix vorhanden
        if ':' not in k:
            k = f"{namespace}{k}"

        # Spezialbehandlung für dict-Werte
        if isinstance(v, dict):
            if "@id" in v:
                raw_id = v["@id"]
                # Rate den passenden Namespace anhand des ID-Musters
                if raw_id.startswith("ORG__"):
                    v = d1.valid_qualified_name(f"{orgs_namespace}:{raw_id}")
                elif raw_id.startswith("SOFTWARE__"):
                    v = d1.valid_qualified_name(f"{software_namespace}:{raw_id}")
                elif raw_id.startswith("PERSON__"):
                    v = d1.valid_qualified_name(f"{people_namespace}:{raw_id}")
                else:
                    v = d1.valid_qualified_name(f"{namespace}{raw_id}")
            elif "@key" in v:
                v = v["@key"]

        # String-Präfixe erkennen und Namespaces zuweisen
        elif isinstance(v, str):
            if v.startswith("ORG__"):
                v = d1.valid_qualified_name(f"{orgs_namespace}:{v}")
            elif v.startswith("SOFTWARE__"):
                v = d1.valid_qualified_name(f"{software_namespace}:{v}")
            elif v.startswith("PERSON__"):
                v = d1.valid_qualified_name(f"{people_namespace}:{v}")

        # Korrigiere "@type"-Schlüssel zur richtigen Form
        if "@type" in k:
            if ':' in v:
                namespace_type = v.split(":")[0]
            else:
                namespace_type = "tippecc_data"
            k = namespace_type + ':type'

        # Vermeide "@id" direkt als Schlüssel
        if "@id" not in k:
            updated_metadata[k] = v

    return f"{namespace}{key}", updated_metadata

# Ensure the directory exists
os.makedirs(dir, exist_ok=True)

d1 = ProvDocument()

collection_namespace = "tippecc_data"
entity_namespace = "tippecc_data"
people_namespace = "people"
orgs_namespace = "orgs"
software_namespace = "software"
exe_namespace = "exe"


# Declaring namespaces for various prefixes used in the example
# todo replace provbook with the actual domain / our namespace
d1.add_namespace('tippecc', 'http://www.provbook.org/tippecc/')
d1.add_namespace(people_namespace, 'http://www.provbook.org/tippecc/people/')
d1.add_namespace(orgs_namespace, 'http://www.provbook.org/tippecc/orgs/')
d1.add_namespace(software_namespace, 'http://www.provbook.org/tippecc/software/')
d1.add_namespace(collection_namespace, 'http://www.provbook.org/tippecc/data/')
d1.add_namespace('esgf_portal', 'http://www.provbook.org/tippecc/esgf_portal/')

d1.add_namespace('dcterms', 'http://purl.org/dc/terms/')
d1.add_namespace('dcat','http://www.w3.org/ns/dcat#')
d1.add_namespace('datacite', 'https://datacite-metadata-schema.readthedocs.io/en/4.6/')
d1.add_namespace('wd', 'http://www.wikidata.org/entity/')
d1.add_namespace('sdo', 'http://schema.org/')
d1.add_namespace('cf', 'https://cfconventions.org/cf-conventions/cf-conventions.html')
d1.add_namespace('nerc', 'http://vocab.nerc.ac.uk/collection/P07/current/')
d1.add_namespace('orcid', 'http://www.orcid.org/')
d1.add_namespace('ror', 'https://ror.org/')
d1.add_namespace(exe_namespace, 'http://www.provbook.org/tippecc/exe/')
d1.add_namespace('foaf', 'http://xmlns.com/foaf/0.1/')



added_agents = set()
activities = []
activity_counter = 0
input_files_wasInformedBy = []
activities_added = []
excluded_activities = []
# Iterate over all files in the directory
for filename in os.listdir(prov_path):
    if filename.endswith('.json'):  # Check if the file has a .json extension
        if filename.endswith("prov_metadata.json"):
            continue
        prov_file = os.path.join(prov_path, "_".join(filename.split("_")[:-1]) + "_prov.json")
        meta_file = os.path.join(meta_path, "_".join(filename.split("_")[:-1]) + "_metadata.json")

        try:
            # Versuche, die prov-Datei zu lesen (obligatorisch)
            with open(prov_file, 'r', encoding='utf-8') as file:
                prov_data = json.load(file)
        except FileNotFoundError as e:
            #print(f"Skipping {filename} due to missing provenance file: {e}")
            continue  # prov fehlt → skip alles
    
        try:
            # Versuche, die metadata-Datei zu lesen (optional)
            with open(meta_file, 'r', encoding='utf-8') as file:
                meta_data = json.load(file)
        except FileNotFoundError:
            meta_data = {}
            #print(f"Metadata file missing for {filename}, using empty metadata.")


        # Create an entity
        entity_id = f"{entity_namespace}:{filename}".replace('_prov.json', '')
        meta_data = flatten_meta_data(meta_data)
        
        #prov_data = flatten_meta_data(prov_data)
        entity = d1.entity(entity_id, meta_data)
        #entity = d1.entity(entity_id)


        #TODO Add Metadata from prov to entity
        #prov_sec_meta_content = flatten_meta_data(prov_data['metadata']['content'][1])
        #prov_sec_meta = flatten_meta_data(prov_data['metadata'])
        #print(prov_sec_meta)
        #for key, value in prov_sec_meta_content.items():
            #print(key, value)
            #entity.add_attributes({key: value})

        # reset activities
        activities_ = []
        first = True
        for process in prov_data['processing']:

            # Add person
            person_id = process['executed_by']
            person_id, person_metadata = get_prov_metadata (person_id, prov_base, f"{people_namespace}:")
            # Qualifiziere alle relevanten Werte in den Metadaten
            person_metadata = qualify_metadata_values(person_metadata, d1, people_namespace, orgs_namespace, software_namespace)
            
            #print(json.dumps(person_metadata, indent=2, ensure_ascii=False))
            #print(person_id, person_metadata)
            if person_id not in added_agents:
                d1.agent(person_id, person_metadata)
                added_agents.add(person_id)

            # Add orga only if not already added
            orga_id = process['on_behalf_of']
            orga_id, orga_metadata = get_prov_metadata (orga_id, prov_base, f"{orgs_namespace}:")
            #print(orga_id, orga_metadata)
            if orga_id not in added_agents:
                d1.agent(orga_id, orga_metadata)
                added_agents.add(orga_id)

            software_id = process.get('software', None)
            function_id = process.get('function', None)

            if isinstance(software_id, list):
                software_id = software_id[0]
            if isinstance(function_id, list):
                function_id = function_id[0]

            if not software_id == None:
                software_id, software_metadata = get_prov_metadata (software_id, prov_base, f"{software_namespace}:")

            if not function_id == None:
                function_id, function_metadata = get_prov_metadata (function_id, prov_base, f"{software_namespace}:")


            if software_id not in added_agents and not software_id == None:
                d1.agent(software_id, software_metadata)
                added_agents.add(software_id)
            if function_id not in added_agents and not function_id == None:
                d1.agent(function_id, function_metadata)
                added_agents.add(function_id)

            #add activities and wasAssociatedWith and generation
            try:
                activity_id = process['label']
                label = process['label']
            except:
                activity_id = process['function']

            #append a number so every activity is unique
            #activity_id = urllib.parse.quote_plus( f"{activity_id}_{activity_counter}" )
            activity_id = f"{activity_id.replace(' ', '_')}_{activity_counter}"
            activity_counter += 1

            activity_id, __ = get_prov_metadata (activity_id, prov_base, f"{exe_namespace}:")

            try:
                time = process['execution_time']
            except:
                time = "N/A"

            try:
                function = process['function']
            except:
                function = None

            __, activity_metadata = get_prov_metadata (function, prov_base, f"{exe_namespace}:")


            try:
                description = process['description']
            except:
                description = "N/A"
            try:
                params = str(process['params'])
            except:
                params = "N/A"

            #print(params, type(params))

            #print(activity_id, activity_metadata, time)
            if activity_id not in added_agents:
                activity  = d1.activity(activity_id, time)

                activity.add_attributes({'prov:label': label})
                activity.add_attributes({'prov:description': description})
                # TODO: Add more activity metadata ???
                activity.add_attributes({'prov:function': function})
                activity.add_attributes({'prov:params': params})

                #'prov:function': function, 'prov:params': params


                if not software_id == None:
                    d1.wasAssociatedWith(activity_id, software_id)
                if not function_id == None:
                    d1.wasAssociatedWith(activity_id, function_id)

                added_agents.add(activity_id)


            if (activity_id, entity) not in added_agents:
                # Add USED information //
                #print(entity_id, activity_id)
                #d1.used(activity_id, entity_id) #-> Das hier hat dem used immer noch das Output File zugeordnet
               # print(entity_id, activity_id, time)
                d1.generation(entity_id, activity_id, time)
                added_agents.add((activity_id, entity_id))

            input_files = prov_data.get("input_files", [])

            # Prüfen, ob wir eine Liste von Listen oder eine flache Liste haben
            if input_files and isinstance(input_files[0], list):
                files_to_iterate = input_files[0]
            else:
                files_to_iterate = input_files


            #ADD wasDerivedFrom
            for derivation in files_to_iterate:
                #print(derivation)
                if derivation.endswith(".nc"):
                    derivation = f"{entity_namespace}:{derivation.split('/')[-1]}".replace(".nc","")
                else:
                    derivation = f"{entity_namespace}:{derivation.split('/')[-1]}"
                if (entity_id, derivation) not in added_agents:
                    d1.wasDerivedFrom(entity_id, derivation)
                    d1.entity(derivation, {})
                    added_agents.add((entity_id, derivation))
                if (activity_id, derivation) not in added_agents:
                    if first:
                        d1.used(activity_id, derivation)
                    else:
                        excluded_activities.append(activity_id)
                    #d1.generation(derivation, activity_id) #-> hier stehen am Ende immer Falsche Sachen drin
                    added_agents.add((activity_id, derivation))
                #if first:
                input_files_wasInformedBy.append({"result_id": entity_id, "entity_id":derivation, "activity_id":activity_id})


            first = False
            # Collect activities
            activities_.append({'id': activity_id})


        # Add wasInformedBy
        #print(activities_)
        if len(activities_) > 1:
            for i in range(1, len(activities_)):
                source = activities_[i - 1]['id']
                destination = activities_[i]['id']
                #print(source, destination)
                d1.wasInformedBy(destination, source)
                # remember source activity
                activities_added.append(source)
                #activities_added.append(destination)



        # Add collections
        try:
            for collection_id in prov_data['collection']:
                raw_collection_id, collection_metadata = get_prov_metadata(
                    collection_id, prov_base, f"{collection_namespace}:"
                )

                # Ensure the namespace is not duplicated
                if ":" in raw_collection_id:
                    collection_id = raw_collection_id  # Keep original if already namespaced
                else:
                    collection_id = f"{collection_namespace}:{raw_collection_id}"

                if collection_id not in added_agents:
                    d1.collection(collection_id, collection_metadata)
                    #print(collection_id)
                    added_agents.add(collection_id)

                if (collection_id, entity_id) not in added_agents:
                    d1.hadMember(collection_id, entity)
                    added_agents.add((collection_id, entity_id))
        except:
            pass



        #print(person_id, orga_id)
        # Add actedOnBehalfOf only if not already added
        if (person_id, orga_id) not in added_agents:
            d1.actedOnBehalfOf(person_id, orga_id)
            added_agents.add((person_id, orga_id))

        # add wasAttributedTo
        d1.wasAttributedTo(entity, person_id)

# Add wasInformedBy relationships
# search first for all activities relted to a entity_id (based on result_id) and then add the wasInformedBy relationships
#print(activities_added)

total = len(input_files_wasInformedBy)
informed_pairs_added = set()  # Set zum Tracken der Paare
for idx, input_file in enumerate(input_files_wasInformedBy, start=1):
    print(f"{idx}/{total}", end="\r")

    source = input_file['entity_id']
    source_activity = input_file['activity_id']

    for input_file2 in input_files_wasInformedBy:
        if input_file2['result_id'] == source:
            destination = input_file2['activity_id']
            pair = (source_activity, destination)

            if (
                pair not in informed_pairs_added
                and destination not in activities_added
                and source_activity not in excluded_activities
            ):
                d1.wasInformedBy(source_activity, destination)
                informed_pairs_added.add(pair)


#activities.sort(key=lambda x: x['start_time'])  # Sort by earliest start time

# export the graph
#d1.serialize(os.path.join(dir, 'GRAPH_new.json'), format='json')

# save as RDF
d1.serialize(os.path.join(dir, 'GRAPH.ttl'), format='rdf', rdf_format="turtle")