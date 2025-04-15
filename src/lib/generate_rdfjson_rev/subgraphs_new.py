import time
import json
import os.path as path
from rdflib import Graph, Namespace
import networkx as nx
#import matplotlib.pyplot as plt
import prov


# Load PROV RDF Data
g = Graph()
# load RDF data
dir = path.dirname(path.abspath(__file__))

graph_dir = path.join( dir, "GRAPH.ttl" )

g.parse(graph_dir, format="ttl")

# Check if the graph is loaded correctly
if len(g) == 0:
    print("The graph is empty. Please check the input file.")
    import sys
    sys.exit()
else:
    print(f"The graph contains {len(g)} triples.")

# Define PROV Namespace
PROV = Namespace("http://www.w3.org/ns/prov#")
TIPPECC = Namespace("http://www.provbook.org/tippecc/data/")
SCHEMA = Namespace("http://schema.org/")
WIKIDATA = Namespace("http://www.wikidata.org/entity/")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")
EXE = Namespace("http://www.provbook.org/tippecc/exe/")
ORGS = Namespace("http://www.provbook.org/tippecc/orgs/")
PEOPLE = Namespace("http://www.provbook.org/tippecc/people/")
SOFTWARE = Namespace("http://www.provbook.org/tippecc/software/")
TIPPECC_DATA = Namespace("http://www.provbook.org/tippecc/data/")


sparql_entities = """
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX tippecc_data: <http://www.provbook.org/tippecc/data/>

SELECT ?entity WHERE {
  ?entity a prov:Entity .
}
"""
# Execute the query
results = g.query(sparql_entities)
print([str(row[0]).split("/")[-1] for row in results])
# Extract all the entity URIs into a list
entity_list = [str(row[0]).split("/")[-1] for row in results if not str(row[0]).split("/")[-1].startswith("COLLECTION")]
#print(len(entity_list))
import sys
sys.exit()
for entity in entity_list:
  start = time.perf_counter()
  # Define the entity to extract the subgraph for
  target_entity = TIPPECC[entity]

  sparql_query1 = f"""
      PREFIX prov: <http://www.w3.org/ns/prov#>
      PREFIX tippecc_data: <http://www.provbook.org/tippecc/data/>
      CONSTRUCT {{
        ?activity ?p ?o .
        ?entity ?p2 ?o2 .
        ?entity prov:qualifiedGeneration ?gen .
        ?gen ?p3 ?o3 .
        ?entity prov:wasAttributedTo ?agent .
        ?agent ?p4 ?o4 .
        ?activity prov:wasAssociatedWith ?software .
        ?software ?p5 ?o5 .
        ?collection prov:hadMember ?entity .
      }}
      WHERE {{
        <{target_entity}> prov:qualifiedGeneration/prov:activity ?baseActivity .
        ?baseActivity prov:wasInformedBy* ?activity .
        OPTIONAL {{
          ?activity ?p ?o .
          ?activity prov:used ?entity .
          ?entity ?p2 ?o2 .
          ?entity prov:qualifiedGeneration ?gen .
          ?gen ?p3 ?o3 .
          ?entity prov:wasAttributedTo ?agent .
          ?agent ?p4 ?o4 .
          ?activity prov:wasAssociatedWith ?software .
          ?software ?p5 ?o5 .
          ?collection prov:hadMember ?entity .
        }}
      }}"""

  # Execute SPARQL Query
  subgraph_rdf = g.query(sparql_query1)

  # Create a new graph for the subgraph
  subgraph = Graph()
  for stmt in subgraph_rdf:
      subgraph.add(stmt)

  # Save the subgraph to a new TTL file

  subgraph.bind("prov", PROV) 
  subgraph.bind("tippecc", TIPPECC)
  subgraph.bind("wd", WIKIDATA)
  subgraph.bind("sdo", SCHEMA)
  subgraph.bind("rdfs", RDFS)
  subgraph.bind("xsd", XSD)
  subgraph.bind("foaf", FOAF)
  subgraph.bind("exe", EXE)
  subgraph.bind("orgs", ORGS)
  subgraph.bind("people", PEOPLE)
  subgraph.bind("software", SOFTWARE)
  subgraph.bind("tippecc_data", TIPPECC_DATA)

  subgraph.serialize(path.join(dir, "subgraphs", entity + ".ttl"), format="ttl")

  graph = prov.read(path.join(dir, "subgraphs", entity + ".ttl"), format="rdf")
  graph.serialize(path.join(dir, "subgraphs", entity + ".json"), format="json")
  end = time.perf_counter()
  print(f"\n✅ {entity} finished in {end - start:.2f} seconds")

# Print the results



"""
for row in subgraph_rdf:
    print( row )


activities = set( x for x in subgraph_rdf if x.activity )
print( len(activities) )

# Convert RDF results to a NetworkX graph
G = nx.DiGraph()
for row in subgraph_rdf:
    G.add_edge(target_entity, row.activity, label="used")

# Print the extracted subgraph
# print("Nodes in subgraph:", G.nodes)
# print("Edges in subgraph:", G.edges)

# Optional: Visualize with Graphviz
pos = nx.spring_layout(G)
labels = {node: node.split("/")[-1] for node in G.nodes}  # Simplify labels
nx.draw(G, pos, labels=labels, with_labels=True, node_size=3000, node_color="lightblue")

# Optional: Save the graph as an image
# plt.savefig("subgraph.png")
"""