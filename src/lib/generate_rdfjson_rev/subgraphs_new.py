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

# Define the entity to extract the subgraph for
target_entity = TIPPECC["TIPPECC_ACCESS-ESM1-5_day_r1i1p1f1__ai__mm_1950_2100__yearsum_mean_1981_2000-2080_2099"]

# SPARQL Query to extract all entities used to create the target entity
sparql_query = f"""
    PREFIX prov: <http://www.w3.org/ns/prov#>
    PREFIX tippecc_data: <http://www.provbook.org/tippecc/data/>

    SELECT DISTINCT *
    WHERE {{

      <{target_entity}> prov:wasGeneratedBy ?baseActivity .
      ?baseActivity prov:wasInformedBy* ?activity .

      OPTIONAL {{
        ?activity prov:wasInformedBy ?parent ;
                  ?rel ?att ;
      }}

    }}
 """


sparql_query12 = f"""
    PREFIX prov: <http://www.w3.org/ns/prov#>
    PREFIX tippecc_data: <http://www.provbook.org/tippecc/data/>

    SELECT DISTINCT  ?activity ?entity
    WHERE {{

      <{target_entity}> prov:qualifiedGeneration/prov:activity ?baseActivity .
      ?baseActivity prov:wasInformedBy* ?activity .
      OPTIONAL {{
      ?activity prov:used ?entity .
      }}


    }}
 """
# TODO add missing entites
sparql_query1 = f"""
    PREFIX prov: <http://www.w3.org/ns/prov#>
    PREFIX tippecc_data: <http://www.provbook.org/tippecc/data/>

    CONSTRUCT {{
      ?activity ?p ?o .
      ?entity ?p2 ?o2 .
      ?entity prov:qualifiedGeneration ?gen .
      ?gen ?p3 ?o3 .
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
      }}
    }}
"""


# Execute SPARQL Query
subgraph_rdf = g.query(sparql_query1)

# Create a new graph for the subgraph
subgraph = Graph()
for stmt in subgraph_rdf:
    subgraph.add(stmt)

# Save the subgraph to a new TTL file

subgraph.serialize(path.join(dir, "subgraph.ttl"), format="ttl")


graph = prov.read(path.join(dir, "subgraph.ttl"), format="rdf")
graph.serialize(path.join(dir, "subgraph.json"), format="json")



# Print the results
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
