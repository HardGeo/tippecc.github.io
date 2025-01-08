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
    - Adds 'tippecc_data:' as a prefix to every key.
    - Replaces empty dictionaries {} with an empty string ''.
    - Converts lists to a comma-separated string of their content.
    """
    items = []
    for key, value in meta_data.items():
        new_key = f"tippecc_data:{parent_key}{key}" if parent_key else f"tippecc_data:{key}"
        
        if isinstance(value, dict):
            if not value:  # Check if the dictionary is empty
                items.append((new_key, ''))  # Replace {} with ''
            else:
                items.extend(flatten_meta_data(value, parent_key=new_key + ".").items())
        elif isinstance(value, list):
            # Convert list to a comma-separated string
            items.append((new_key, ', '.join(map(str, value))))
        else:
            items.append((new_key, value))
    
    return dict(items)




base_dir = r"C:\Users\jonas\svelte_scripts\tippecc.github.io\src\lib\generate_rdfjson"
# Ensure the directory exists
os.makedirs(base_dir, exist_ok=True)

d1 = ProvDocument()

# Declaring namespaces for various prefixes used in the example
# todo replace provbook with the actual domain / our namespace
d1.add_namespace('tippecc', 'http://www.provbook.org/tippecc/')
d1.add_namespace('people', 'http://www.provbook.org/tippecc/people/')
d1.add_namespace('orgs', 'http://www.provbook.org/tippecc/orgs/')
d1.add_namespace('software', 'http://www.provbook.org/tippecc/software/')
d1.add_namespace('tippecc_data', 'http://www.provbook.org/tippecc/data/')
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
d1.add_namespace('exe', 'http://www.provbook.org/tippecc/exe/#')

# Specify the directory path
prov_path = r"C:\Users\jonas\svelte_scripts\tippecc.github.io\src\lib\prov_meta_water_budget\prov"
meta_path = r"C:\Users\jonas\svelte_scripts\tippecc.github.io\src\lib\prov_meta_water_budget\meta"

added_agents = set()
# Iterate over all files in the directory
for filename in os.listdir(prov_path):
    if filename.endswith('.json'):  # Check if the file has a .json extension
        prov_file = os.path.join(prov_path, filename)
        meta_file = os.path.join(meta_path, filename).replace(".json", ".nc.json")
        

        with open(prov_file, 'r', encoding='utf-8') as file:
            prov_data = json.load(file)
        with open(meta_file, 'r', encoding='utf-8') as file:
            meta_data = json.load(file)
        # Create an entity
        entity_id = f"tippecc_data:{filename}".replace('.json', '.nc')
        meta_data = flatten_meta_data(meta_data)
        prov_data = flatten_meta_data(prov_data)
       
        entity = d1.entity(entity_id, meta_data)
        
        # Add person only if not already added
        person_id = f"people:{prov_data['tippecc_data:executed_by']}"
        orcid_id = f"{prov_data['tippecc_data:executed_by_orcid']}"
        if (person_id, orcid_id) not in added_agents:
            d1.agent(person_id, {'tippecc_data:executed_by_orcid': orcid_id})
            added_agents.add((person_id, orcid_id))

        # Add orga only if not already added
        orga_id = f"orgs:{prov_data['tippecc_data:executed_on_behalf_of']}"
        ror_id = f"{prov_data['tippecc_data:executed_on_behalf_of_ror']}"
        if (orga_id, ror_id) not in added_agents:
            d1.agent(orga_id, {'tippecc_data:executed_on_behalf_of_ror': ror_id})
            added_agents.add((orga_id, ror_id))

        
        # Add software only if not already added
        software_id = f"software:{prov_data['tippecc_data:library']}"
        name = f"{prov_data['tippecc_data:name']}"
        if (software_id, name) not in added_agents:
            d1.agent(software_id, 
                     {'tippecc_data:name': prov_data['tippecc_data:name'],
                      'tippecc_data:abbr': prov_data['tippecc_data:abbr'],
                      'tippecc_data:description': prov_data['tippecc_data:description'],
                      'tippecc_data:function': prov_data['tippecc_data:function'],
                      'tippecc_data:library_version': prov_data['tippecc_data:library_version']
                     }
                    )
            
            added_agents.add((software_id, name))

        # Add collections
        #d1.collection('tippecc_data:Kariba_2080_2099_monthly')
        # d1.wasAttributedTo('tippecc_data:Kariba_2080_2099_monthly', 'people:Kawawa')
        #d1.hadMember('tippecc_data:Kariba_2080_2099_monthly', e)
        
        
        # Add actedOnBehalfOf only if not already added
        delegate = f"people:{prov_data['tippecc_data:executed_by']}"
        responsible = f"orgs:{prov_data['tippecc_data:executed_on_behalf_of']}"
        if (delegate, responsible) not in added_agents:
            d1.actedOnBehalfOf(delegate, responsible)
            added_agents.add((delegate, responsible))

        d1.wasAttributedTo(entity, f"people:{prov_data['tippecc_data:executed_by']}")

        #ADD wasDerivedFrom
        for derivation in prov_data['tippecc_data:input_files'].split(','):
            derivation = f"tippecc_data:{derivation.split('/')[-1]}"
            d1.wasDerivedFrom(entity_id, derivation)
        
        
        #add activities and wasAssociatedWith if not exist yet
        activity = f"exe:{prov_data['tippecc_data:function']}"
        if activity not in added_agents:
            d1.activity(activity)
            d1.wasAssociatedWith(activity, software_id)
            d1.generation(entity_id, activity, prov_data['tippecc_data:date'])
            added_agents.add(activity)

        #TODO: wasInformedBy
        #for derivation in prov_data['tippecc_data:input_files'].split(','):
            #d1.wasInformedBy(destination, source)

        # Add USED information
        d1.used(activity, entity_id)
        

        # visualize and export the graph
        dot = prov_to_dot(d1)
        dot.write_png(os.path.join(base_dir, 'test.png'))
        d1.serialize(os.path.join(base_dir, 'test.json'), format='json')
        #d1.serialize(os.path.join(base_dir, 'tbl_test.ttl'), format='rdf', rdf_format='ttl')

        #from rdflib import Graph, Literal, RDF, URIRef
        # rdflib knows about quite a few popular namespaces, like W3C ontologies, schema.org etc.
        #from rdflib.namespace import FOAF, XSD, RDF, SDO, RDFS, Namespace
        
        #g = Graph()
        #g.parse(os.path.join(base_dir, 'tbl_test.ttl'), format="ttl")

        #g.serialize(destination=os.path.join(base_dir, "tbl_test.ttl"))

        #d1 = prov.read(os.path.join(base_dir, "tbl_test.ttl"))
        #dot = prov_to_dot(d1)
        #dot.write_png(os.path.join(base_dir, 'test.png'))
        #d1.serialize(os.path.join(base_dir, 'test.json'), format='json')
