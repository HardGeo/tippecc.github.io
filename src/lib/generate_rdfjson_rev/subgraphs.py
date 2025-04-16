## PREPARATIONS

import os
import json
from collections import Counter, defaultdict

# Funktion zur rekursiven Rückverfolgung der Provenance eines Datensatzes
"""
# suche nach ids in wasDerivedFrom, in denen die Zielid "tippecc_data:TIPPECC_AWI-ESM-1-REcoM_day_r1i1p1f1__ai__mm_1850_2100__yearsum_mean_1981_2000-2080_2099_prov.nc" in ["prov:generatedEntity"] vorkommt
# für die beiden gefundenen  IDs nimm jeweils die ["prov:usedEntity"] und suche wiederum in welcher ID diese in ["prov:generatedEntity"] vorkommt
# wiederhole bis sich kein neues ["prov:generatedEntity"] mehr findet

# aus entity nimm nur die in wasDerivedFrom vorhandenen entities

# entity
# hadMember
# agent
# activity

sollen live gesucht werden
"""
def find_derivation_chain(target_id):
    new_was_derived_from = {}
    queue = [target_id]
    visited = set()

    while queue:
        current_target = queue.pop(0)
        if current_target in visited:
            continue
        visited.add(current_target)

        matching_ids = [
            key for key, entry in was_derived_from.items()
            if entry.get("prov:generatedEntity") == current_target
        ]

        for _id in matching_ids:
            used_entity = was_derived_from[_id].get("prov:usedEntity")
            new_was_derived_from[_id] = {
                "prov:generatedEntity": current_target,
                "prov:usedEntity": used_entity,
            }


            if used_entity:
                queue.append(used_entity)

    return new_was_derived_from

# Gesuchte Ziel-ID
#target_id = "tippecc_data:TIPPECC_AWI-ESM-1-REcoM_day_r1i1p1f1__ai__mm_1850_2100__yearsum_mean_1981_2000-2080_2099_prov.nc"

base_dir = r"C:\Users\jonas\svelte_scripts\tippecc.github.io\src\lib\generate_rdfjson_rev"
input_file = os.path.join(base_dir, "GRAPH_new.json")

# JSON-LD Datei laden
with open(input_file, "r") as f:
    data_load = json.load(f)

# Ermittle alle Targets
was_derived_from = data_load.get("wasDerivedFrom", {})
entity_list = data_load.get("entity", {})

targets = set()


for entry in entity_list.keys():
    targets.add(entry)
    #targets.add(entry["prov:usedEntity"])
#print(targets)   
#targets = [target.split(":")[1] for target in targets]

import sys
#sys.exit()
#---------------------------------------------------------------------------------------------------------



#----------------------------------------------------------------------------------------------------------
# for every entity create a subgraph
for target_id in targets:
    #target_id = "TIPPECC_AWI-ESM-1-REcoM_day_r1i1p1f1__ai__mm_1850_2100__yearsum_mean_1981_2000-2080_2099.json"
    data = data_load.copy()
    target_id = target_id.replace("tippecc_data:", "")
    output_file = os.path.join(base_dir, "subgraphs_old", target_id+".json")

    target = "tippecc_data:" + target_id.replace(".json", "")


    # Starte die Suche und ersetze die Daten
    chain = find_derivation_chain(target)
    data["wasDerivedFrom"] = chain

    #________________________________________________________
    # Die gesamte "Entity"-Struktur
    entities = data.get("entity", {})

    # Extract unique values from chain
    unique_values = set()

    for entry in chain.values():
        unique_values.add(entry["prov:generatedEntity"])
        unique_values.add(entry["prov:usedEntity"])


    # Filter entities based on unique_values_list
    filtered_entities = {
        entity_id: entity_data
        for entity_id, entity_data in entities.items()
        if entity_id in unique_values
    }
    data["entity"] = filtered_entities

    #______________________________________________________
    # Die gesamte "hadMember"-Struktur
    collections = data.get("hadMember", {})


    filtered_collections = {
        key: value for key, value in collections.items()
        if value.get("prov:entity") in unique_values
    }

    data["hadMember"] = filtered_collections


    #_________________________________________________________
    # Die gesamte "wasAttributedTo"-Struktur
    wasAttributedTo = data.get("wasAttributedTo", {})

    filtered_wasAttributedTo = {
        key: value for key, value in wasAttributedTo.items()
        if value.get("prov:entity") in unique_values
    }

    data["wasAttributedTo"] = filtered_wasAttributedTo


    #___________________________________________________________
    # Die gesamte "used"-Struktur
    used = data.get("used", {})

    filtered_used = {
        key: value for key, value in used.items()
        if value.get("prov:entity") in unique_values
    }

    # Gruppiere nach "prov:activity"
    grouped_by_activity = defaultdict(list)
    for key, value in filtered_used.items():
        grouped_by_activity[value["prov:activity"]].append((key, value["prov:entity"]))

    # Behalte nur die IDs, bei denen es mehrere verschiedene "prov:entity" innerhalb einer Activity gibt
    selected_ids_used = {}
    for activity, entries in grouped_by_activity.items():
        unique_entities = {entity for _, entity in entries}  # Einzigartige Entities in der Gruppe
        if len(unique_entities) > 1:  # Prüfe, ob es mehr als eine einzigartige Entity gibt
            for key, entity in entries:
                selected_ids_used[key] = used[key]

    # Speichere das gefilterte Dictionary zurück in data
    data["used"] = selected_ids_used

    #_______________________________________________________________
    #get new activities unique values
    unique_exe = set()

    for entry in selected_ids_used.values():
        unique_exe.add(entry["prov:activity"])

    #_________________________________________________________
    # Die gesamte "wasGeneratedBy"-Struktur
    wasGeneratedBy = data.get("wasGeneratedBy", {})
    #print(wasGeneratedBy)

    filtered_wasGeneratedBy = {
        key: value for key, value in wasGeneratedBy.items()
        if value.get("prov:entity") in unique_values
        and value.get("prov:activity") in unique_exe
    }

    # Speichere das gefilterte Dictionary zurück in data
    data["wasGeneratedBy"] = filtered_wasGeneratedBy

    #_________________________________________________________________
    # FRAGE: and oder or ??? Wie soll wasInformedBy gebaut werden?
    # AKtuell spielt es für die Visualisierung keine Rolle mehr 
    # Die gesamte "wasInformedBy"-Struktur
    wasInformedBy = data.get("wasInformedBy", {})
    #print(wasInformedBy)

    filtered_wasInformedBy = {}

    for key, value in wasInformedBy.items():
        # Normalize to a list of dicts
        items = value if isinstance(value, list) else [value]

        for item in items:
            if (
                item.get("prov:informed") in unique_exe
                and item.get("prov:informant") in unique_exe
            ):
                #print(item)  # 👈 print each matching value
                filtered_wasInformedBy[key] = item

    data["wasInformedBy"] = filtered_wasInformedBy
    #_________________________________________________________________
    # Die gesamte "wasAssociatedWith"-Struktur
    wasAssociatedWith = data.get("wasAssociatedWith", {})

    filtered_wasAssociatedWith = {
        key: value for key, value in wasAssociatedWith.items()
        if value.get("prov:activity") in unique_exe
    }

    data["wasAssociatedWith"] = filtered_wasAssociatedWith

    #________________________________________________________
    #get new agents unique values
    unique_persons = set()

    for entry in filtered_wasAttributedTo.values():
        unique_persons.add(entry["prov:agent"])

    # Die gesamte "actedOnBehalfOf"-Struktur

    actedOnBehalfOf = data.get("actedOnBehalfOf", {})

    filtered_actedOnBehalfOf = {
        key: value for key, value in actedOnBehalfOf.items()
        if value.get("prov:delegate") in unique_persons
    }

    data["actedOnBehalfOf"] = filtered_actedOnBehalfOf

    #_______________________________________________________
    #get new software unique values
    unique_software = set()
    for entry in filtered_wasAssociatedWith.values():
        unique_software.add(entry["prov:agent"])

    #get new orgs unique values
    unique_orgs = set()
    for entry in filtered_actedOnBehalfOf.values():
        unique_orgs.add(entry["prov:responsible"])


    # Die gesamte "agent"-Struktur
    agent = data.get("agent", {})

    filtered_agent = {
        key: value for key, value in agent.items()
        if key in unique_persons
        or key in unique_exe
        or key in unique_software
        or key in unique_orgs
    }

    data["agent"] = filtered_agent

    #_______________________________________________
    # Die gesamte "agent"-Struktur
    activity = data.get("activity", {})

    filtered_activity = {
        key: value for key, value in activity.items()
        if key in unique_exe
    }

    data["activity"] = filtered_activity
    #if target_id == "tippecc_data:TIPPECC_AWI-ESM-1-REcoM_day_r1i1p1f1__ai__mm_1850_2100__yearsum_mean_1981_2000-2080_2099":
        #print(len(filtered_activity))

    # Aktualisierte JSON-Datei speichern
    with open(output_file, "w") as f:
        json.dump(data, f, indent=4)

    print(f"File {target_id} written succesfully to: {base_dir}")