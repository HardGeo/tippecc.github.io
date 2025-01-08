import urllib
from urllib.parse import urlencode

import prov
import requests
import xmltodict as xmltodict
from prov.model import ProvDocument
from prov.dot import prov_to_dot

import os
import json

os.environ["PATH"] += os.pathsep + 'C:/Users/c1zafr/Downloads/windows_10_cmake_Release_Graphviz-12.0.0-win64/Graphviz-12.0.0-win64/bin'

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

# Load the JSON data from a file
with open(os.path.join(base_dir, 'meta.json')) as file:
    metadata = json.load(file)
#print(metadata)
#exit()

# Creating an entity
# add cf_standard_name to the entity; add tracking_id to the entity, add format to the entity, add resolution to the entity,
# add spatial coverage to the entity, add temporal resolution to the entity, add max min?, add units, doi....
# (merge file infos later via ontop from DB or retrieve on demand?
e1ds = 'tippecc_data:CLMcom-KIT-CCLM5-0-15_v1_NCC-NorESM1-M_pr_Afr_day_b_1950_2100_kariba_2080-2099_monthsum.nc'
e2ds = 'tippecc_data:CLMcom-KIT-CCLM5-0-15_v1_NCC-NorESM1-M_pr_Afr_day_b_1950_2100_kariba_2080-2099.nc'
e3ds = 'tippecc_data:CLMcom-KIT-CCLM5-0-15_v1_NCC-NorESM1-M_pr_Afr_day_b_1950_2100_kariba.nc'
e4ds = 'tippecc_data:TIPPECC_CLMcom-KIT-CCLM5-0-15_v1_NCC-NorESM1-M_pr_Afr_day_b_1950_2100_.nc'
e5ds = 'tippecc_data:TIPPECC_CLMcom-KIT-CCLM5-0-15_v1_NCC-NorESM1-M_pr_Afr_day_1950_2100.nc'
e6ds = 'tippecc_data:Kariba.shp'
e7ds = 'esgf_portal:CLMcom-KIT-CCLM5-0-15_v1_NCC-NorESM1-M_pr_Afr_day_rcp85.nc'
e8ds = 'esgf_portal:CLMcom-KIT-CCLM5-0-15_v1_NCC-NorESM1-M_pr_Afr_day_historicl.nc'
print(metadata[e1ds])

e1 = d1.entity(e1ds, metadata[e1ds])
e2 = d1.entity(e2ds, metadata[e2ds])
e3 = d1.entity(e3ds, metadata[e3ds])
e4 = d1.entity(e4ds, metadata[e4ds])
e5 = d1.entity(e5ds, metadata[e5ds])
e6 = d1.entity(e6ds, metadata[e6ds])
e7 = d1.collection(e7ds, metadata[e7ds])
e8 = d1.collection(e8ds, metadata[e8ds])


# maybe use ORCID / ROR as IRI for identification -> only artificial identifiers id no ror or orcid available
# person infos theoretically stored in the tippecc database -> use as source ?
# FAOF or schema.org as source for more information about the person
# wd:P496 -> ORCID (explicit ORCID -> schema.org only implicit
# wd:P6782 -> ROR
d1.agent('people:Franzi', metadata['people:Franzi'])  # given Name and Surname # email address
d1.agent('people:Kawawa', metadata['people:Kawawa'])
d1.agent('people:Jessica', metadata['people:Jessica'])
d1.agent('people:Francios', metadata['people:Francios'])
d1.agent('orgs:UniJena', metadata['orgs:UniJena'])
d1.agent('orgs:UNZA', metadata['orgs:UNZA'])
d1.agent('orgs:WITS', metadata['orgs:WITS'])

# collections as way also to hide complexity of the data and/or group data
d1.collection('tippecc_data:Kariba_2080_2099_monthly')
d1.wasAttributedTo('tippecc_data:Kariba_2080_2099_monthly', 'people:Kawawa')
d1.actedOnBehalfOf('people:Kawawa', 'orgs:UNZA')

d1.collection('tippecc_data:bias_adjusted_datasets')
d1.wasAttributedTo('tippecc_data:bias_adjusted_datasets', 'people:Jessica')
d1.actedOnBehalfOf('people:Jessica', 'orgs:WITS')
d1.wasAttributedTo('tippecc_data:bias_adjusted_datasets', 'people:Francios')
d1.actedOnBehalfOf('people:Francios', 'orgs:WITS')

d1.collection('tippecc_data:raw_datasets')
d1.wasAttributedTo('tippecc_data:raw_datasets', 'people:Jessica')
d1.actedOnBehalfOf('people:Jessica', 'orgs:WITS')
d1.wasAttributedTo('tippecc_data:raw_datasets', 'people:Francios')
d1.actedOnBehalfOf('people:Francios', 'orgs:WITS')

d1.hadMember('tippecc_data:Kariba_2080_2099_monthly', e1)
d1.hadMember('tippecc_data:Kariba_2080_2099_monthly', e2)
d1.hadMember('tippecc_data:Kariba_2080_2099_monthly', e3)

d1.hadMember('tippecc_data:bias_adjusted_datasets', e4)
d1.hadMember('tippecc_data:raw_datasets', e5)

# schema.org as source for more possible properties
d1.agent('software:xclim', metadata['software:xclim'])
d1.agent('software:cdo', metadata['software:cdo'])
d1.agent('software:wits_fortran_magic_tool', metadata['software:wits_fortran_magic_tool'])

d1.actedOnBehalfOf('people:Franzi', 'orgs:UniJena')
# https://www.wikidata.org/wiki/Property:P6782 ROR ID
# ORCID iD  https://www.wikidata.org/wiki/Property:P496

# Attributing the article to the agent
d1.wasAttributedTo(e1, 'people:Franzi')
d1.wasAttributedTo(e2, 'people:Franzi')
d1.wasAttributedTo(e3, 'people:Franzi')
d1.wasAttributedTo(e4, 'people:Jessica')
d1.wasAttributedTo(e5, 'people:Jessica')
d1.wasAttributedTo(e6, 'people:Kawawa')


d1.wasDerivedFrom('tippecc_data:CLMcom-KIT-CCLM5-0-15_v1_NCC-NorESM1-M_pr_Afr_day_b_1950_2100_kariba_2080-2099.nc',
                  'tippecc_data:CLMcom-KIT-CCLM5-0-15_v1_NCC-NorESM1-M_pr_Afr_day_b_1950_2100_kariba.nc')
d1.wasDerivedFrom('tippecc_data:CLMcom-KIT-CCLM5-0-15_v1_NCC-NorESM1-M_pr_Afr_day_b_1950_2100_kariba_2080-2099_monthsum.nc',
                  'tippecc_data:CLMcom-KIT-CCLM5-0-15_v1_NCC-NorESM1-M_pr_Afr_day_b_1950_2100_kariba_2080-2099.nc')
d1.wasDerivedFrom(e4, e5)
d1.wasDerivedFrom(e3, e6)
d1.wasDerivedFrom(e5, e7)
d1.wasDerivedFrom(e5, e8)

# Adding an activity
d1.add_namespace('exe', 'http://www.provbook.org/tippecc/exe/#')
d1.activity('exe:aggregateMonthlySum')
d1.activity('exe:sliceByTime')
d1.activity('exe:sliceByArea')
d1.activity('exe:sliceByProjectArea')
d1.activity('exe:regrid')
d1.activity('exe:combineDatasetsHistoricalRCP')
d1.activity('exe:bias_adjustment')

d1.wasInformedBy('exe:aggregateMonthlySum', 'exe:sliceByTime')
d1.wasInformedBy('exe:sliceByTime', 'exe:sliceByArea')
d1.wasInformedBy('exe:sliceByArea', 'exe:bias_adjustment')
d1.wasInformedBy('exe:bias_adjustment', 'exe:sliceByProjectArea')
d1.wasInformedBy('exe:sliceByProjectArea', 'exe:regrid')
d1.wasInformedBy('exe:regrid', 'exe:combineDatasetsHistoricalRCP')

d1.wasAssociatedWith('exe:bias_adjustment', 'software:wits_fortran_magic_tool')
d1.wasAssociatedWith('exe:sliceByTime', 'software:cdo')
d1.wasAssociatedWith('exe:aggregateMonthlySum', 'software:cdo')

d1.used('exe:aggregateMonthlySum', 'tippecc_data:CLMcom-KIT-CCLM5-0-15_v1_NCC-NorESM1-M_pr_Afr_day_b_1950_2100_kariba_2080-2099.nc')
d1.used('exe:sliceByTime', 'tippecc_data:CLMcom-KIT-CCLM5-0-15_v1_NCC-NorESM1-M_pr_Afr_day_b_1950_2100_kariba.nc')
d1.used('exe:sliceByArea', e4)
d1.used('exe:sliceByArea', e6)
d1.used('exe:bias_adjustment', e5)
d1.used('exe:combineDatasetsHistoricalRCP', e8)
d1.used('exe:combineDatasetsHistoricalRCP', e7)

d1.generation('tippecc_data:CLMcom-KIT-CCLM5-0-15_v1_NCC-NorESM1-M_pr_Afr_day_b_1950_2100_kariba_2080-2099_monthsum.nc', 'exe:aggregateMonthlySum',
              '2012-04-03T13:35:23Z')
d1.generation('tippecc_data:CLMcom-KIT-CCLM5-0-15_v1_NCC-NorESM1-M_pr_Afr_day_b_1950_2100_kariba_2080-2099.nc', 'exe:sliceByTime', '2012-04-03T13:35:23Z')
d1.generation(e3, 'exe:sliceByArea', '2012-04-03T13:35:23Z')
d1.generation(e4, 'exe:bias_adjustment', '2012-04-03T13:35:23Z')
d1.generation(e5, 'exe:sliceByProjectArea', '2012-04-03T13:35:23Z')


# visualize and export the graph
dot = prov_to_dot(d1)
dot.write_png(os.path.join(base_dir, 'article-prov.png'))


d1.serialize(os.path.join(base_dir, 'article-prov.json'), format='json')
d1.serialize(os.path.join(base_dir, 'article-prov.ttl'), format='rdf', rdf_format='ttl')
d1.serialize(os.path.join(base_dir, 'article-prov.xml'), format='xml')


# test to manipulate the graph with rdflib

from rdflib import Graph, Literal, RDF, URIRef
# rdflib knows about quite a few popular namespaces, like W3C ontologies, schema.org etc.
from rdflib.namespace import FOAF, XSD, RDF, SDO, RDFS, Namespace

g = Graph()
g.parse(os.path.join(base_dir, 'article-prov.ttl'), format="ttl")

print(len(g))

# add example -> works, but created a different prefix -> schema: instead of sdo: as used in the example above
#g.bind("schema", "http://schema.org/")
g.add((URIRef("http://www.provbook.org/tippecc/software/cdo"), SDO.version, Literal("1.7")))




import pprint
#for stmt in g:
    #pprint.pprint(stmt)


g.serialize(destination=os.path.join(base_dir, "tbl.ttl"))

d1 = prov.read(os.path.join(base_dir, "tbl.ttl"))
dot = prov_to_dot(d1)
dot.write_png(os.path.join(base_dir, 'article-prov.png'))
d1.serialize(os.path.join(base_dir, 'article-prov.json'), format='json')
d1.serialize(os.path.join(base_dir, 'article-prov.ttl'), format='rdf', rdf_format='ttl')
d1.serialize(os.path.join(base_dir, 'article-prov.xml'), format='xml')



import json

def replace_tippecc_data(obj):
    """Recursively replace 'tippecc:data/' with 'tippecc_data:' in all strings."""
    if isinstance(obj, dict):
        return {replace_tippecc_data(key): replace_tippecc_data(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [replace_tippecc_data(item) for item in obj]
    elif isinstance(obj, str):
        return obj.replace("tippecc:data/", "tippecc_data:")
    else:
        return obj

# Load and reformat the JSON
json_file_path = os.path.join(base_dir, 'article-prov.json')
with open(json_file_path, 'r') as file:
    data = json.load(file)

# Replace the string in the JSON data
updated_data = replace_tippecc_data(data)

# Write formatted JSON
with open(json_file_path, 'w') as file:
    json.dump(updated_data, file, indent=4)
# stop script
# 

