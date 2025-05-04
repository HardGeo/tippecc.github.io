import requests
from io import BytesIO
from rdflib import Graph, Namespace
import prov
import os.path as path

# Accept header / different response for SPARQL queries
headers = {
        "Accept": "application/sparql-results+json, application/sparql-results+xml, text/turtle"
    }

repo_name = "repo"
# Set the repository name and the URL of the GraphDB server
graphdb_url = "http://localhost:7200"


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

def send_request(query):
    response = requests.post(
        graphdb_url + "/repositories/" + repo_name,
        data={"query": query},
        headers=headers
    )

    if response.status_code == 200:
        print("Query executed successfully.")
    else:
        print("Error executing query:", response.status_code)
    print("Response:", response.text)
    return response

def create_repo(repo_name):
    repo_config_ttl = """
   #
# RDF4J configuration template for a GraphDB repository
# This template is intended as an example only
#
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.
@prefix rep: <http://www.openrdf.org/config/repository#>.
@prefix sr: <http://www.openrdf.org/config/repository/sail#>.
@prefix sail: <http://www.openrdf.org/config/sail#>.
@prefix graphdb: <http://www.ontotext.com/config/graphdb#>.

[] a rep:Repository ;
    rep:repositoryID "repo" ;
    rdfs:label "Sample repository TTL file." ;
    rep:repositoryImpl [
        rep:repositoryType "graphdb:SailRepository" ;
        sr:sailImpl [
            sail:sailType "graphdb:Sail" ;

            graphdb:read-only "false" ;

            # Inference and Validation
            graphdb:ruleset "rdfsplus-optimized" ;
            graphdb:disable-sameAs "true" ;
            graphdb:check-for-inconsistencies "false" ;

            # Indexing
            graphdb:entity-id-size "32" ;
            graphdb:enable-context-index "false" ;
            graphdb:enablePredicateList "true" ;
            graphdb:enable-fts-index "false" ;
            graphdb:fts-indexes ("default" "iri") ;
            graphdb:fts-string-literals-index "default" ;
            graphdb:fts-iris-index "none" ;

            # Queries and Updates
            graphdb:query-timeout "0" ;
            graphdb:throw-QueryEvaluationException-on-timeout "false" ;
            graphdb:query-limit-results "0" ;

            # Settable in the file but otherwise hidden in the UI and in the RDF4J console
            graphdb:base-URL "http://example.org/owlim#" ;
            graphdb:defaultNS "" ;
            graphdb:imports "" ;
            graphdb:repository-type "file-repository" ;
            graphdb:storage-folder "storage" ;
            graphdb:entity-index-size "10000000" ;
            graphdb:in-memory-literal-properties "true" ;
            graphdb:enable-literal-index "true" ;
        ]
    ].

    """
    # Fake a file upload using BytesIO
    files = {
        'config': ('repo-config.ttl', BytesIO(repo_config_ttl.encode('utf-8')), 'application/x-turtle')
    }

    url = "http://localhost:7200/rest/repositories"

# POST request
    response = requests.post(url, files=files)

    print("Status:", response.status_code)
    print("Response:", response.text)

def delete_repo(repo_name):
    url = f"{graphdb_url}/rest/repositories/{repo_name}"
    response = requests.delete(url)

    if response.status_code == 204:
        print(f"Repository '{repo_name}' deleted successfully.")
    else:
        print(f"Failed to delete repository '{repo_name}'. Status code: {response.status_code}")

def delete_all_repos():
    url = f"{graphdb_url}/rest/repositories"
    response = requests.get(url)

    if response.status_code == 200:
        repos = response.json()
        for repo in repos:
            repo_name = repo['id']
            delete_repo(repo_name)
    else:
        print(f"Failed to retrieve repositories. Status code: {response.status_code}")

def import_data(file, repo_name):
    with open(file, "rb") as ttl_file:
        response = requests.post(
            f"http://localhost:7200/repositories/{repo_name}/statements",
            headers={"Content-Type": "application/x-turtle"},
            data=ttl_file
        )

    print("Import status:", response.status_code)
    print("Response:", response.text)
    


def test_repo(repo_name):
    query = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT ?s ?p ?o WHERE { ?s ?p ?o } LIMIT 100
    """

    response = send_request(query)

    print(response.json())


def subquery(entity):


    query = """
    PREFIX prov: <http://www.w3.org/ns/prov#>
    PREFIX tippecc_data: <http://www.provbook.org/tippecc/data/>
    CONSTRUCT {
        ?activity ?p ?o .

        ?entity prov:qualifiedGeneration ?gen .
        ?gen ?p3 ?o3 .
        ?entity prov:wasAttributedTo ?agent .
        ?agent ?p4 ?o4 .
        ?activity prov:wasAssociatedWith ?software .
        ?software ?p5 ?o5 .
        ?collection prov:hadMember ?entity .
    }
    WHERE { tippecc_data:""" + entity + """
        prov:qualifiedGeneration/prov:activity ?baseActivity .
        ?baseActivity prov:wasInformedBy* ?activity .

        OPTIONAL { ?activity ?p ?o .
            OPTIONAL {
      			?activity prov:wasAssociatedWith ?software .
      			?software ?p5 ?o5 .
    		}
    	}
  		OPTIONAL {
    		?activity prov:used ?entity .

    		OPTIONAL {
      			?entity prov:qualifiedGeneration ?gen .
      			?gen ?p3 ?o3 .
    		}
    		OPTIONAL {
      			?entity prov:wasAttributedTo ?agent .
      			?agent ?p4 ?o4 .
    		}
    		OPTIONAL {
      			?collection prov:hadMember ?entity .

    		}
  		}
    }

    """

    #send_request(query)
    response = send_request(query)
    return response.text if response.status_code == 200 else None




def subquery_entity_meta(entity):

    query = """
        PREFIX prov: <http://www.w3.org/ns/prov#>
        PREFIX tippecc_data: <http://www.provbook.org/tippecc/data/>
        CONSTRUCT {
            ?entity ?p8 ?o8 .
        }
        WHERE { tippecc_data:""" + entity + """
            prov:qualifiedGeneration/prov:activity ?baseActivity .
            ?baseActivity prov:wasInformedBy* ?activity .

  		    OPTIONAL {
    		    ?activity prov:used ?entity .
                ?entity ?p8 ?o8 .
  		    }
        }
    """

    response = send_request(query)
    return response.text if response.status_code == 200 else None


def subquery_collection_meta(entity):
    headers = {
        "Accept": "application/sparql-results+json, application/sparql-results+xml, text/turtle"
    }

    query = """
    PREFIX prov: <http://www.w3.org/ns/prov#>
      PREFIX tippecc_data: <http://www.provbook.org/tippecc/data/>
      CONSTRUCT {

    ?collection ?p7 ?o7 .

      }
      WHERE { tippecc_data:""" + entity + """
        prov:qualifiedGeneration/prov:activity ?baseActivity .
        ?baseActivity prov:wasInformedBy* ?activity .

          OPTIONAL {
               OPTIONAL {
      				?activity prov:wasAssociatedWith ?software .
    			}
    	  }
  		  OPTIONAL {
    		?activity prov:used ?entity .

    		OPTIONAL {
      			?entity prov:qualifiedGeneration ?gen .
    		}
    		OPTIONAL {
      			?entity prov:wasAttributedTo ?agent .
    		}
    		OPTIONAL {
      			?collection prov:hadMember ?entity .
                ?collection ?p7 ?o7 .
            FILTER(?p7 != prov:hadMember)  # Exclude 'hadMember' relations
    		}
  		}
    }

    """

    response = send_request( query)
    return response.text if response.status_code == 200 else None


def count_prov(entity):
    query = """
     PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX tippecc_data: <http://www.provbook.org/tippecc/data/>

SELECT   (COUNT(DISTINCT ?entity) AS ?entityCount)
  (COUNT(DISTINCT ?activity) AS ?activityCount)
  (COUNT(DISTINCT ?agent) AS ?agentCount)
 (COUNT(DISTINCT ?software) AS ?softwareCount)
 (COUNT(DISTINCT ?collection) AS ?collectionCount)
WHERE {
  tippecc_data:""" + entity + """
    prov:qualifiedGeneration/prov:activity ?baseActivity .

  ?baseActivity prov:wasInformedBy* ?activity .
  OPTIONAL {


    OPTIONAL {
      ?activity prov:wasAssociatedWith ?software .
      ?software ?p5 ?o5 .
    }
  }

  OPTIONAL {
    ?activity prov:used ?entity .

    OPTIONAL {
      ?entity prov:qualifiedGeneration ?gen .
      ?gen ?p3 ?o3 .
    }

    OPTIONAL {
      ?entity prov:wasAttributedTo ?agent .
      ?agent ?p4 ?o4 .
    }

    OPTIONAL {
      ?collection prov:hadMember ?entity .
    }
  }
}
    """

    response = send_request(query)
    #print(response.json())

def source_entities(entity):
    query = """
    PREFIX prov: <http://www.w3.org/ns/prov#>
    PREFIX tippecc_data: <http://www.provbook.org/tippecc/data/>
    SELECT  DISTINCT ?entity
    WHERE { tippecc_data:""" + entity + """
        prov:qualifiedGeneration/prov:activity ?baseActivity .

        ?baseActivity prov:wasInformedBy* ?activity .
        OPTIONAL {
            ?activity prov:used ?entity .
        }
        FILTER NOT EXISTS {
                ?entity prov:wasDerivedFrom [] .
        }
    }
    """

    response = send_request(query)
    #print(response.json())

def all_entities():
    query = """
    PREFIX prov: <http://www.w3.org/ns/prov#>
    SELECT ?entity WHERE {
      ?entity a prov:Entity .
    }
    """
    response = send_request(query)
    
    if response.status_code != 200:
        return None
    
    json_data = response.json()
    results = json_data.get("results", {}).get("bindings", [])
    
    # Extract only the URI strings
    entities = [binding["entity"]["value"] for binding in results]
    return entities




def activities(entity):
    query = """
    PREFIX prov: <http://www.w3.org/ns/prov#>
    PREFIX tippecc_data: <http://www.provbook.org/tippecc/data/>
    SELECT  DISTINCT ?activities ?p ?o
    WHERE { tippecc_data:""" + entity + """
        prov:qualifiedGeneration/prov:activity ?baseActivity .

        ?baseActivity prov:wasInformedBy* ?activity .
        ?activity ?p ?o .
    }
    """

    response = send_request(query)
    #print(response.json())




def export_combined_turtle(entity_id: str):
    g = Graph()
    dir = path.dirname(path.abspath(__file__))

    # Call all three functions and parse returned Turtle strings
    turtle_parts = [
        subquery(entity_id),
        subquery_entity_meta(entity_id),
        subquery_collection_meta(entity_id)
    ]

    for ttl in turtle_parts:
        if ttl:
            g.parse(data=ttl, format="turtle")

    g.bind("prov", PROV) 
    g.bind("tippecc", TIPPECC)
    g.bind("wd", WIKIDATA)
    g.bind("sdo", SCHEMA)
    g.bind("rdfs", RDFS)
    g.bind("xsd", XSD)
    g.bind("foaf", FOAF)
    g.bind("exe", EXE)
    g.bind("orgs", ORGS)
    g.bind("people", PEOPLE)
    g.bind("software", SOFTWARE)
    g.bind("tippecc_data", TIPPECC_DATA)

    # Serialize combined graph to Turtle
    g.serialize(path.join(dir, "subgraphs", entity_id + ".ttl"), format="ttl")

    graph = prov.read(path.join(dir, "subgraphs", entity_id + ".ttl"), format="rdf")
    graph.serialize(path.join(dir, "subgraphs", entity_id + ".json"), format="json")

    
    #print(f"File written to: {entity_id}")

ttl_file = r"C:\Users\jonas\svelte_scripts\tippecc.github.io\src\lib\generate_rdfjson_rev\GRAPH.ttl"
entity = "TIPPECC_ACCESS-CM2_day_r1i1p1f1__ai_1950_2100__yearsum_mean_1981_2000-2080_2099"
delete_all_repos()
create_repo(repo_name)
import_data(ttl_file,repo_name)

entity_list = all_entities()
#entity_list = [entry["entity"]["value"].split("/")[-1] for entry in entity_list]

#test_repo(repo_name)
#subquery(entity)
#subquery_entity_meta(entity)
#subquery_collection_meta(entity)
#count_prov(entity)
#source_entities(entity)  
#result_entities(entity)

#for entity in entity_list:
  #export_combined_turtle(entity)
#activities(entity)