

import { 
    changedPar, 
    changedUnit,  
    changedTempRes, 
    changedSpatRes, 
    changedScenario, 
    changedFormat, 
    changedSize, 
    changedGlobMod, 
    changedRegMod} from '$lib/store';

type WasDerivedFrom = {
    [key: string]: {
        "prov:generatedEntity": string;
        "prov:usedEntity": string;
    };
};

type WasInformedBy = {
    [key: string]: {
        "prov:informed": string;
        "prov:informant": string;
    };
};

type Entity = {
    [key: string]: {
        "tippecc_data:variable_id"?: string;
        "tippecc_data:units"?: string;
        "tippecc_data:upperLeft"?: string;
        "tippecc_data:lowerRight"?: string;
        "tippecc_data:lowerLeft"?: string;
        "tippecc_data:upperRight"?: string;
        "tippecc_data:size"?: string;
        "tippecc_data:source_id"?: string;
        "tippecc_data:scenario"?: string;
        "tippecc_data:format"?: string; 
        "tippecc_data:frequency"?: string;
        "tippecc_data:file_size"?: { "$": number};
        "tippecc_data:creation_date"?: string;
        "tippecc_data:activity_id"?: string;
        "tippecc_data:experiment_id"?: string;
        "tippecc_data:Conventions"?: string;
        "tippecc_data:institution"?: string;
        "tippecc_data:realm"?: string;
        "tippecc_data:contact"?: string;
        "tippecc_data:tracking_id"?: string;
        "tippecc_data:parent_variant_label"?: string;
        [key: string]: any;
    };
};

type Node = {
    id: string;
    type: string;
    data: {
        parameter: string;
        zeitspranne: any;
        regionalmodell: string;
        globalmodell: string;
        einheit: string;
        szenario: string;
        format: string;
        resolutionZeitlich: string;
        resolutionRaeumlich: string;
        spatialExtent: any;
        dateigroesse: number;
        timestamp: string;
        project: string;
        experiment: string;
        standard: string;
        bias: string;
        source: string;
        institution: string;
        domain: string;
        contact: string;
        tracking_id: string;
        doi: string;
        collection: string;
        variant: string;
        id: string;
    };
    position: { x: number; y: number };
};

type NodeActivity = {
    id: string;
    type: string;
    data: {
        id: string;
    };
    position: { x: number; y: number };
};

type Edge = {
    id: string, // Unique edge id using generated and used entities
    source: string, // Source is the generated entity
    target: string, // Target is the used entity
    animated: boolean, // Set animated to false
    label: string, // Add a label if necessary
    type: string, // Specify the edge type
    labelStyle: string // Styling for the label
};


type Dataset = {
    wasDerivedFrom: WasDerivedFrom;
    wasInformedBy: WasInformedBy;
    hadMember: HadMember;
    entity: Entity;
  };


type HadMember = {
    [key: string]: {
        "prov:entity": string;
        "prov:collection": string;
    };
};
    
// Funktion, die die eindeutigen Entitäten extrahiert
export function AddEntities(dataset: Dataset, nodes: any, edges: any, label: any): void {
    const uniqueEntities = new Set<string>();

    Object.values(dataset.wasDerivedFrom).forEach(({ "prov:generatedEntity": gen, "prov:usedEntity": used }) => {
        uniqueEntities.add(gen);
        uniqueEntities.add(used);
    });


    function findCollectionForEntity(currentEntity: string, hadMember: HadMember): string {
        // Iterate through the hadMember object to find the matching collection
        const entry = Object.values(hadMember).find(member => member["prov:entity"] === currentEntity);
        return entry ? entry["prov:collection"] : "No Collection defined";
    }

    function calculateSpatialResolution(
        gridSize: [number, number], 
        upperLeft: [number, number], 
        upperRight: [number, number], 
        lowerLeft: [number, number]
    ): string {
        
        const [width, height] = gridSize;

        const longitudeRange = upperRight[0] - upperLeft[0]; // 52.0 - 10.0
        const latitudeRange = upperLeft[1] - lowerLeft[1];   // -5.0 - (-36.0)

        const lonResolution = longitudeRange / width;  // 42.0 / 84 = 0.5°
        const latResolution = latitudeRange / height;  // 31.0 / 62 = 0.5°

        return `${lonResolution.toFixed(1)}° x ${latResolution.toFixed(1)}°`;
    }

    let name: string ;
    let unit: string ;
    let extent: any ;
    let collection: string ;
    let regionalmodel: string;
    let globalmodel: string ;
    let scenario: string ;
    let format: string ;
    let temporalResolution: string ;
    let spatialResolution: string ;
    let size: number ;
    let parsedTimespans: any ;
    let timestamp: string ;
    let project: string ;
    let experiment: string ;
    let standard: string ;
    let bias: string ;
    let source: string ;
    let institution: string ;
    let domain: string ;
    let contact: string ;
    let tracking_id: string ;
    let doi: string ;
    let variant: string ;
    let xPos: number;
    let yPos: number;
    

    uniqueEntities.forEach((currentEntity) => {
        if (dataset.entity[currentEntity]) {
            
            // EXTRACT PARAMTER NAME
            // Split the string at ", ", find the part starting with "name:", and extract the value
            name = dataset.entity[currentEntity]["tippecc_data:variable_id"] ?? "N/A";
            //EXTRACT UNIT
            unit = dataset.entity[currentEntity]["tippecc_data:units"] ?? "N/A";
            //EXTRACT BOUNDS
            const upperLeft = (dataset.entity[currentEntity]["tippecc_data:upperLeft"] ?? "0, 0").split(", ").map(Number) as [number, number];
            const lowerRight = (dataset.entity[currentEntity]["tippecc_data:lowerRight"] ?? "0, 0").split(", ").map(Number) as [number, number];
            const lowerLeft = (dataset.entity[currentEntity]["tippecc_data:lowerLeft"] ?? "0, 0").split(", ").map(Number) as [number, number];
            const upperRight = (dataset.entity[currentEntity]["tippecc_data:upperRight"] ?? "0, 0").split(", ").map(Number) as [number, number];
            const gridSize = (dataset.entity[currentEntity]["tippecc_data:size"] ?? "1, 1").split(", ").map(Number) as [number, number];
            extent = [upperLeft[0], lowerRight[0], lowerRight[1], upperLeft[1]]
            // EXTRACT COLLECTION
            collection = findCollectionForEntity(currentEntity, dataset.hadMember);
            // EXTRACT REGIONAL MODEL TODO
            regionalmodel =  "not defined";//dataset.entity[currentEntity]["tippecc_data:source"];
            // EXTRACT Global MODEL
            globalmodel =  dataset.entity[currentEntity]["tippecc_data:source_id"] ?? "N/A";
            // EXTRACT scenario TODO
            scenario =  dataset.entity[currentEntity]["tippecc_data:scenario"] ?? "N/A";
            //EXTRACT File Format TODO
            format =  dataset.entity[currentEntity]["tippecc_data:format"] ?? "N/A";
            //EXTRACT temp res
            temporalResolution =  dataset.entity[currentEntity]["tippecc_data:frequency"] ?? "N/A";
            //EXTRACT spat res
            spatialResolution = calculateSpatialResolution(gridSize, upperLeft, upperRight, lowerLeft);
            //EXTRACT File Size
            size = dataset.entity[currentEntity]["tippecc_data:file_size"]?.$ ?? 0 ;
            //TODO
            parsedTimespans = [ { start: 1910, end: 1960 }, { start: 1980, end: 2050 } ];
            //EXTRACT Timestamp
            timestamp = dataset.entity[currentEntity]["tippecc_data:creation_date"] ?? "N/A";
            // EXTRACT Project TODO
            project = dataset.entity[currentEntity]["tippecc_data:activity_id"] ?? "N/A";
            // EXTRACT experiment
            experiment = dataset.entity[currentEntity]["tippecc_data:experiment_id"] ?? "N/A";
            // EXTRACT Standard
            standard = dataset.entity[currentEntity]["tippecc_data:Conventions"] ?? "N/A";
            //EXTRACT Bias TODO
            bias = "Yes";
            //EXTRACT source TODO
            source = "Climate Limited-area Modelling Community (CLM-Community)";
            //EXTRACT institution
            institution = dataset.entity[currentEntity]["tippecc_data:institution"] ?? "N/A";
            //EXTRACT domain TODO
            domain = dataset.entity[currentEntity]["tippecc_data:realm"] ?? "N/A";
            //EXTRACT contact
            contact = dataset.entity[currentEntity]["tippecc_data:contact"] ?? "N/A";
            //EXTRACT tracking_id
            tracking_id = dataset.entity[currentEntity]["tippecc_data:tracking_id"] ?? "N/A";
            //EXTRACT doi
            doi = "doi:example"//dataset.entity[currentEntity]["tippecc_data:references"];
            //EXTRACT variant
            variant = dataset.entity[currentEntity]["tippecc_data:parent_variant_label"] ?? "N/A";

        } else {

            name =  "N/A";
            unit = "N/A";
            const upperLeft = [0, 0] as [number, number];
            const lowerRight = [0, 0] as [number, number];
            const lowerLeft = [0, 0] as [number, number];
            const upperRight = [0, 0] as [number, number];
            const gridSize = [0, 0] as [number, number];
            extent = [upperLeft[0], lowerRight[0], lowerRight[1], upperLeft[1]];
            try{
                collection = findCollectionForEntity(currentEntity, dataset.hadMember);
            }
            catch{
                collection = "unknown";
            }
            regionalmodel =  "not defined";
            globalmodel =  "N/A";
            scenario =  "N/A";
            format =  "N/A";
            temporalResolution =  "N/A";
            spatialResolution = calculateSpatialResolution(gridSize, upperLeft, upperRight, lowerLeft);
            size = 0;
            parsedTimespans = [];
            timestamp = "N/A";
            project = "N/A";
            experiment = "N/A";
            standard = "N/A";
            bias = "N/A";
            source = "N/A";
            institution = "N/A";
            domain = "N/A";
            contact = "N/A";
            tracking_id = "N/A";
            doi = "N/A";
            variant = "N/A";
        }
        function findUsedEntities(dataset:any, currentEntity:any) {
            let usedEntities = [];
        
            for (const key in dataset.wasDerivedFrom) {
                const entry = dataset.wasDerivedFrom[key];
                if (entry["prov:generatedEntity"] === currentEntity) {
                    usedEntities.push(entry["prov:usedEntity"]);
                }
            }
        
            return usedEntities;
        }
        const usedEntitiesList = findUsedEntities(dataset, currentEntity);
        
        
        let name_used: string ;
        let unit_used: string ;
        let regionalmodel_used: string ;
        let globalmodel_used: string ;
        let scenario_used: string ;
        let format_used: string ;
        let temporalResolution_used: string ;
        let spatialResolution_used: string ;
        let size_used: number ;

        // Loop over usedEntitiesList
        usedEntitiesList.forEach((usedEntity) => {

            if (dataset.entity[usedEntity]) {
                name_used = dataset.entity[usedEntity]["tippecc_data:variable_id"] ?? "N/A";
                unit_used = dataset.entity[usedEntity]["tippecc_data:units"] ?? "N/A";
                temporalResolution_used =  dataset.entity[usedEntity]["tippecc_data:frequency"] ?? "N/A";
                const upperLeft_used = (dataset.entity[usedEntity]["tippecc_data:upperLeft"] ?? "0, 0").split(", ").map(Number) as [number, number];
                const lowerLeft_used = (dataset.entity[usedEntity]["tippecc_data:lowerRight"] ?? "0, 0").split(", ").map(Number) as [number, number];
                const upperRight_used = (dataset.entity[usedEntity]["tippecc_data:upperRight"] ?? "0, 0").split(", ").map(Number) as [number, number];
                const gridSize_used = (dataset.entity[usedEntity]["tippecc_data:size"] ?? "1, 1").split(", ").map(Number) as [number, number];
                spatialResolution_used = calculateSpatialResolution(gridSize_used, upperLeft_used, upperRight_used, lowerLeft_used);
                scenario_used =  dataset.entity[usedEntity]["tippecc_data:scenario"] ?? "N/A";
                format_used =  dataset.entity[usedEntity]["tippecc_data:format"] ?? "N/A";
                size_used = dataset.entity[usedEntity]["tippecc_data:file_size"]?.$ ?? 0;
                globalmodel_used =  dataset.entity[usedEntity]["tippecc_data:source_id"] ?? "N/A";
                regionalmodel_used =  "not defined";//dataset.entity[usedEntity]["tippecc_data:source"];
            }
            else{
                name_used = "N/A";
                unit_used = "N/A";
                temporalResolution_used = "N/A";
                const upperLeft_used = [0, 0] as [number, number];
                const lowerLeft_used = [0, 0] as [number, number];
                const upperRight_used = [0, 0] as [number, number];
                const gridSize_used = [0, 0] as [number, number];
                spatialResolution_used = calculateSpatialResolution(gridSize_used, upperLeft_used, upperRight_used, lowerLeft_used);
                scenario_used =  "N/A";
                format_used =  "N/A";
                size_used = 0 ;
                globalmodel_used =  "N/A";
                regionalmodel_used =  "not defined";//dataset.entity[usedEntity]["tippecc_data:source"];
            }
    
            if (name !== name_used) {
                changedPar.update(set => {
                    set.add(usedEntity);
                    return new Set(set);
                });
            }
            if (unit !== unit_used) {
                changedUnit.update(set => {
                    set.add(usedEntity); // Add entity ID to the set
                    return new Set(set); // Return a new Set to trigger reactivity
                });
            }
            if (temporalResolution !== temporalResolution_used) {
                changedTempRes.update(set => {
                    set.add(usedEntity); // Add entity ID to the set
                    return new Set(set); // Return a new Set to trigger reactivity
                });
            }
            if (spatialResolution !== spatialResolution_used) {
                changedSpatRes.update(set => {
                    set.add(usedEntity); // Add entity ID to the set
                    return new Set(set); // Return a new Set to trigger reactivity
                });
            }
            if (scenario !== scenario_used) {
                changedScenario.update(set => {
                    set.add(usedEntity); // Add entity ID to the set
                    return new Set(set); // Return a new Set to trigger reactivity
                });
            }
            if (format !== format_used) {
                changedFormat.update(set => {
                    set.add(usedEntity); // Add entity ID to the set
                    return new Set(set); // Return a new Set to trigger reactivity
                });
            }
            if (size !== size_used) {
                changedSize.update(set => {
                    set.add(usedEntity); // Add entity ID to the set
                    return new Set(set); // Return a new Set to trigger reactivity
                });
            }
            if (globalmodel !== globalmodel_used) {
                changedGlobMod.update(set => {
                    set.add(usedEntity); // Add entity ID to the set
                    return new Set(set); // Return a new Set to trigger reactivity
                });
            }
            if (regionalmodel !== regionalmodel_used) {
                changedRegMod.update(set => {
                    set.add(usedEntity); // Add entity ID to the set
                    return new Set(set); // Return a new Set to trigger reactivity
                });
            }
    
        });


        xPos = Math.random() * 400;  // Zufälliger Wert zwischen 0 und 800
        yPos = Math.random() * 800;  // Zufälliger Wert zwischen 0 und 600

        // Add node for currentEntity
        nodes.update((n: Node[]) => {

            if (!n.some(node => node.id === currentEntity)) {
                //console.log(uniqueEntityId);
                
                n.push({
                    id: currentEntity,
                    type: 'entityNode', // Specify the custom node type
                    data: {
                        parameter: name || "N/A",
                        zeitspranne: parsedTimespans  || [],
                        regionalmodell: regionalmodel  || "not defined",
                        globalmodell: globalmodel  || "N/A",
                        einheit: unit  || "N/A",
                        szenario: scenario  || "N/A",
                        format: format  || "N/A",
                        resolutionZeitlich: temporalResolution  || "N/A",
                        resolutionRaeumlich: spatialResolution  || "N/A",
                        spatialExtent: extent  || "N/A",
                        //spatialExtent_orig: [0,0,0,0],
                        dateigroesse: size  || 0,
                        timestamp: timestamp || "N/A",
                        project: project  || "N/A",
                        experiment: experiment  || "N/A",
                        standard: standard || "N/A",
                        bias: bias  || "N/A",
                        source: source  || "N/A",
                        institution: institution || "N/A",
                        domain: domain || "N/A",
                        contact: contact || "N/A",
                        tracking_id: tracking_id || "N/A",
                        doi: doi || "N/A",
                        collection: collection  || "N/A",
                        variant: variant || "N/A",
                        id: currentEntity

                    },
                    position: { x: xPos, y: yPos },
                });
    
            }
            return n;
        });
    })

    edges.update((e: Edge[]) => {
        const newEdges = Object.keys(dataset.wasDerivedFrom).map(id => {
            const generatedEntity = dataset.wasDerivedFrom[id]["prov:generatedEntity"];
            const usedEntity = dataset.wasDerivedFrom[id]["prov:usedEntity"];

    
            // Create a new edge object
            return {
                id: `${generatedEntity}-${usedEntity}`, // Unique edge id using generated and used entities
                source: generatedEntity, // Source is the generated entity
                target: usedEntity, // Target is the used entity
                animated: false, // Set animated to false
                label: label, // Add a label if necessary
                type: 'default', // Specify the edge type
                labelStyle: 'color: black; font-size: 16px; z-index: 2; pointer-events: none;' // Styling for the label
            };
        });
    
        // Use push to add the new edges to the existing list
        newEdges.forEach(newEdge => {
            e.push(newEdge);
        });

        // Return the updated edges list
        return e;
    });

}





// Funktion, die die eindeutigen Entitäten extrahiert
export function AddActions(dataset: Dataset, nodes: any, edges: any, label: any): void {
    const uniqueEntities = new Set<string>();

    Object.values(dataset.wasInformedBy).forEach(({ "prov:informed": gen, "prov:informant": used }) => {
        uniqueEntities.add(gen);
        uniqueEntities.add(used);
    });

    let xPos: number;
    let yPos: number;
    

    uniqueEntities.forEach((currentEntity) => {

        xPos = Math.random() * 400;  // Zufälliger Wert zwischen 0 und 800
        yPos = Math.random() * 800;  // Zufälliger Wert zwischen 0 und 600

        // Add node for currentEntity
        nodes.update((n: NodeActivity[]) => {

            if (!n.some(node => node.id === currentEntity)) {
                //console.log(uniqueEntityId);
                
                n.push({
                    id: currentEntity,
                    type: 'activityNode', // Specify the custom node type
                    data: {
                        id: currentEntity
                    },
                    position: { x: xPos, y: yPos },
                });
    
            }
            return n;
        });
    })

    edges.update((e: Edge[]) => {
        const newEdges = Object.keys(dataset.wasInformedBy).map(id => {
            const generatedEntity = dataset.wasInformedBy[id]["prov:informed"];
            const usedEntity = dataset.wasInformedBy[id]["prov:informant"];

    
            // Create a new edge object
            return {
                id: `${generatedEntity}-${usedEntity}`, // Unique edge id using generated and used entities
                source: generatedEntity, // Source is the generated entity
                target: usedEntity, // Target is the used entity
                animated: false, // Set animated to false
                label: label, // Add a label if necessary
                type: 'default', // Specify the edge type
                labelStyle: 'color: black; font-size: 16px; z-index: 2; pointer-events: none;' // Styling for the label
            };
        });
    
        // Use push to add the new edges to the existing list
        newEdges.forEach(newEdge => {
            e.push(newEdge);
        });

        // Return the updated edges list
        return e;
    });

}



export function createPeople ({
    dataset,
    nodes,
    edges,
    EdgeLabel,
    swapArrow,
    edgeStyle
}: {
    dataset: any, 
    nodes: any, 
    edges: any,
    EdgeLabel: string,
    swapArrow: boolean,
    edgeStyle: string
}) {
    const entityNodes = new Set(); 
    let yPosition = 0;

    for (const [id, member] of Object.entries(dataset.wasAttributedTo)) {
        const personId = member["prov:agent"]; // Use full person identifier (e.g., people:Franzi)
        const entity = member["prov:entity"];

        // Find organization (orgaId) from actedOnBehalfOf
        const actedOnBehalfOfEntry = Object.values(dataset.actedOnBehalfOf).find(
            (entry: any) => entry["prov:delegate"] === personId
        );

        const orgaId = actedOnBehalfOfEntry?.["prov:responsible"] || null;
        const rorid = orgaId ? dataset.agent[orgaId]?.["wd:P6782"] : null;

        // Only add the person node if it hasn't been added yet
        if (!entityNodes.has(personId)) {
            nodes.update(n => {
                n.push({
                    id: personId,
                    type: 'personNode',
                    data: { 
                        person: personId  || "N/A",
                        orga: orgaId || "N/A",
                        orcid: dataset.agent?.[personId]?.["wd:P496"] || "N/A",
                        rorid: rorid || "N/A"
                    },
                    position: { x: -600, y: yPosition },
                });
                return n;
            });
            entityNodes.add(personId);
            yPosition += 400;
        }

        // Add edge between the person and the corresponding entity
        const source = swapArrow ? entity : personId;
        const target = swapArrow ? personId : entity;
        const sourceHandle = swapArrow ? `${entity}-left` : `${personId}-right`;
        const targetHandle = swapArrow ? `${personId}-right` : `${entity}-left`;

        edges.update(e => {
            e.push({
                id: `${personId}-${entity}`,
                source: source,
                target: target,
                sourceHandle: sourceHandle,
                targetHandle: targetHandle,
                animated: false,
                label: EdgeLabel,
                style: edgeStyle,
                labelStyle: 'color: black; font-size: 16px'
            });
            return e;
        });
    }
}
//-----------------------------------------------------------------------------------------
//---------------------------------------------------------------------------------------


//ADD Nodes and Edges for Software
export function addSoftware({
    dataset,
    nodes,
    edges,
    EdgeLabel,
    IdName,
    EntityName,
    swapArrow,
    edgestyle
}: {
    dataset: any, 
    nodes: any,
    edges: any,
    EdgeLabel: string,
    IdName: string,
    EntityName: string,
    swapArrow: boolean,
    edgestyle: string
}) {
    let yPosition = 0;
    for (const member of Object.values(dataset.wasAssociatedWith)) {
        const activityId = member[IdName];
        const agentId = member[EntityName];
        
        // Ensure agent node is added if not present
        nodes.update(n => {
            if (!n.some(node => node.id === agentId)) {
                n.push({
                    id: agentId,
                    type: 'softwareNode',
                    data: {
                        software: agentId  || "N/A",
                        source: dataset.agent[agentId]["dcterms:source"]  || "N/A",
                        version: dataset.agent[agentId]["sdo:version"]  || "N/A",
                        repository: dataset.agent[agentId]["sdo:codeRepository"]  || "N/A",
                        license: dataset.agent[agentId]["sdo:license"]  || "N/A"
                     },
                    position: { x: 1200, y: yPosition }, // Adjust as needed
                });
            }
            return n;
        });
        yPosition += 400;

        // Define edge direction based on swapArrow
        const source = swapArrow ? agentId : activityId;
        const target = swapArrow ? activityId : agentId;
        const sourceHandle = swapArrow ? `${agentId}-left` : `${activityId}-right`; // Use the correct handle
        const targetHandle = swapArrow ? `${activityId}-right` : `${agentId}-left`; // Use the correct handle
        
        // Add edge between the activity and agent
        edges.update(e => {
            e.push({
                id: `${activityId}-${agentId}`,
                source: source,
                target: target, 
                sourceHandle: sourceHandle, // Assign the correct source handle
                targetHandle: targetHandle, // Assign the correct target handle
                animated: false,
                label: EdgeLabel,
                style: edgestyle,
                labelStyle: 'color: black; font-size: 16px',
            });
            return e;
        });
    }
}


// ADD EDGES ONLY
export function addEdgesOnly({
    dataset,
    edges,
    EdgeLabel,
    IdName,
    EntityName,
    swapArrow,
    style,
    labelStyle,
    handle1,
    handle2,
    IdAppendix
    //edgeStyle = {} // Allow optional edge style customization
}: {
    dataset: any, 
    edges: any,
    EdgeLabel: string,
    IdName: string,
    EntityName: string,
    swapArrow: boolean,
    style: string,
    labelStyle: string,
    handle1: string,
    handle2: string,
    IdAppendix: string
}) {
    for (const member of Object.values(dataset)) {
        const activityId = member[IdName];
        const entityId = member[EntityName];

        
        // Define edge direction based on swapArrow
        const source = swapArrow ? entityId : activityId;
        const target = swapArrow ? activityId : entityId;
        //console.log("source and target:", source, target);
        

        // Specify the correct handles for source and target
        const sourceHandle = swapArrow ? `${entityId}-${handle1}` : `${activityId}-${handle2}`; // Use entityNode right or activityNode left
        const targetHandle = swapArrow ? `${activityId}-${handle2}` : `${entityId}-${handle1}`; // Use activityNode left or entityNode right
        //console.log(sourceHandle, targetHandle)
        
        // Add edge between activity and entity
        edges.update(e => {
            e.push({
                id: `${source}-${target}-${IdAppendix}`,
                source: source,
                target: target,
                sourceHandle: sourceHandle, // Assign the correct source handle
                targetHandle: targetHandle, // Assign the correct target handle
                animated: false,
                label: EdgeLabel,
                style: style,
                labelStyle: labelStyle
            });
            return e;
        });
    }
}

