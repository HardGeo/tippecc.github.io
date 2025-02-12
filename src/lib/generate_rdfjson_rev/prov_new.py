import os
import json

import prov
import xmltodict as xmltodict
from prov.model import ProvDocument
from prov.dot import prov_to_dot

def flatten_meta_data(meta_data, parent_key=""):
    """
    Flattens a nested dictionary:
    - Brings all keys to the top level, prefixed by their parent key path.
    - Adds 'tippecc_data:' as a prefix to every key **only if it does not already contain a colon (":")**.
    - Replaces empty dictionaries {} with an empty string ''.
    - Converts lists to a comma-separated string of their content.
    """
    items = []
    
    for key, value in meta_data.items():
        # Add "tippecc_data:" only if the key does not already contain ":"
        new_key = key if ":" in key else f"tippecc_data:{key}"
        
        if isinstance(value, dict):
            if not value:  # Replace empty dictionaries with ''
                items.append((new_key, ''))
            else:
                items.extend(flatten_meta_data(value, parent_key=new_key).items())  # Recursive call
        elif isinstance(value, list):
            items.append((new_key, ', '.join(map(str, value))))  # Convert list to comma-separated string
        else:
            items.append((new_key, value))
    
    return dict(items)


def get_prov_metadata(key, prov_path, namespace="tippecc_data:"):
    prov_metadata_path = os.path.join(prov_path, "prov_metadata_template.json")
    with open(prov_metadata_path, 'r', encoding='utf-8') as file:
        prov_metadata = json.load(file)
    
    # Extract the metadata for the given key
    metadata = prov_metadata.get(key, {})
    
    # Process the metadata
    updated_metadata = {}
    for k, v in metadata.items():
        # Add namespace if the key does not already contain ':'
        if ':' not in k:
            k = f"{namespace}{k}"
        
        # If the value is a nested dict with "@key" or "@id", extract its value
        if isinstance(v, dict) and "@key" in v:
            v = v["@key"]
        if isinstance(v, dict) and "@id" in v:
            v = v["@id"]
        
        updated_metadata[k] = v
    
    return f"{namespace}{key}", updated_metadata





base_dir = r"C:\Users\jonas\svelte_scripts\tippecc.github.io\src\lib\generate_rdfjson_rev"
# Ensure the directory exists
os.makedirs(base_dir, exist_ok=True)

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
d1.add_namespace(exe_namespace, 'http://www.provbook.org/tippecc/exe/#')
d1.add_namespace('foaf', 'http://xmlns.com/foaf/0.1/')

# Specify the directory path
prov_path = r"C:\Users\jonas\svelte_scripts\tippecc.github.io\src\lib\prov_meta_revised\prov"
meta_path = r"C:\Users\jonas\svelte_scripts\tippecc.github.io\src\lib\prov_meta_revised\meta"


added_agents = set()
activities = []
# Iterate over all files in the directory
for filename in os.listdir(prov_path):
    if filename.endswith('.json') and filename.startswith("TIPPECC"):  # Check if the file has a .json extension
        if filename.endswith("prov_metadata.json"):
            continue

        prov_file = os.path.join(prov_path, "_".join(filename.split("_")[:-1]) + "_prov.json")
        meta_file = os.path.join(meta_path, "_".join(filename.split("_")[:-1]) + "_metadata.json")
        
        try:
            # Try to read the provenance file
            with open(prov_file, 'r', encoding='utf-8') as file:
                prov_data = json.load(file)
            
            # Try to read the metadata file
            with open(meta_file, 'r', encoding='utf-8') as file:
                meta_data = json.load(file)

            #print(f"{filename} processed")
        except FileNotFoundError as e:
            print(f"Skipping {filename} due to missing file: {e}")
            continue  # Skip to the next file
        
        
        # Create an entity
        entity_id = f"{entity_namespace}:{filename}".replace('.json', '.nc')
        meta_data = flatten_meta_data(meta_data)

        #prov_data = flatten_meta_data(prov_data)
        entity = d1.entity(entity_id, meta_data)

        #TODO Add Metadata from prov to entity
        prov_sec_meta_content = flatten_meta_data(prov_data['metadata']['content'][1])
        #prov_sec_meta = flatten_meta_data(prov_data['metadata'])
        #print(prov_sec_meta)
        for key, value in prov_sec_meta_content.items():
            #print(key, value)
            entity.add_attributes({key: value})

        
        # Add person
        person_id = prov_data['processing'][0]['executed_by']
        person_id, person_metadata = get_prov_metadata (person_id, "\\".join(prov_path.split("\\")[:-1]), f"{people_namespace}:")
        #print(person_id, person_metadata)
        if person_id not in added_agents:
            d1.agent(person_id, person_metadata)
            added_agents.add(person_id)



        # Add orga only if not already added
        orga_id = prov_data['processing'][0]['on_behalf_of']
        orga_id, orga_metadata = get_prov_metadata (orga_id, "\\".join(prov_path.split("\\")[:-1]), f"{orgs_namespace}:")
        #print(orga_id, orga_metadata)
        if orga_id not in added_agents:
            d1.agent(orga_id, orga_metadata)
            added_agents.add(orga_id)



        # Add software
        software_id = prov_data['processing'][0]['software'][0]
        software_id, software_metadata = get_prov_metadata (software_id, "\\".join(prov_path.split("\\")[:-1]), f"{software_namespace}:")
        #print(software_id, software_metadata)
        if software_id not in added_agents:
            d1.agent(software_id, software_metadata)
            added_agents.add(software_id)



        # Add collections
        for collection_id in prov_data['collection']:
            raw_collection_id, collection_metadata = get_prov_metadata(
                collection_id, "\\".join(prov_path.split("\\")[:-1]), f"{collection_namespace}:"
            )
        
            # Ensure the namespace is not duplicated
            if ":" in raw_collection_id:
                collection_id = raw_collection_id  # Keep original if already namespaced
            else:
                collection_id = f"{collection_namespace}:{raw_collection_id}"
        
            if collection_id not in added_agents:
                d1.collection(collection_id)
                #print(collection_id)
                added_agents.add(collection_id)
        
            if (collection_id, entity_id) not in added_agents:
                d1.hadMember(collection_id, entity)
                added_agents.add((collection_id, entity_id))



        #print(person_id, orga_id)
        # Add actedOnBehalfOf only if not already added
        if (person_id, orga_id) not in added_agents:
            d1.actedOnBehalfOf(person_id, orga_id)
            added_agents.add((person_id, orga_id))

        

        # add wasAttributedTo
        d1.wasAttributedTo(entity, person_id)




        #ADD wasDerivedFrom
        for derivation in prov_data['input_files']:
            derivation = f"{entity_namespace}:{derivation.split('/')[-1]}".replace(".nc","_prov.nc")
            #json_file = derivation.split(":")[1].replace(".nc", ".json")
            #if json_file in os.listdir(prov_path):
            d1.wasDerivedFrom(entity_id, derivation)





        #add activities and wasAssociatedWith and generation
        activity_id = prov_data['processing'][0]['function']
        activity_id, activity_metadata = get_prov_metadata (activity_id, "\\".join(prov_path.split("\\")[:-1]), f"{exe_namespace}:")
        time = prov_data['processing'][0]['execution_time']

        #print(activity_id, activity_metadata, time)
        if activity_id not in added_agents:
            activity  = d1.activity(activity_id, time)
            # Add metadata to the activity
            for key, value in activity_metadata.items():
                activity.add_attributes({key: value})
            d1.wasAssociatedWith(activity_id, software_id)
            d1.generation(entity_id, activity_id, time)
            added_agents.add(activity_id)
            activities.append({'id': activity_id, 'start_time': time, 'metadata': activity_metadata})



        # Add USED information
        d1.used(activity_id, entity_id)


activities.sort(key=lambda x: x['start_time'])  # Sort by earliest start time
# Add `wasInformedBy` relationships
for i in range(1, len(activities)):
    source = activities[i - 1]['id']
    destination = activities[i]['id']
    d1.wasInformedBy(destination, source)  # Create wasInformedBy relationship

# visualize and export the graph
dot = prov_to_dot(d1)
#dot.write_png(os.path.join(base_dir, 'test.png'))
d1.serialize(os.path.join(base_dir, 'test.json'), format='json')