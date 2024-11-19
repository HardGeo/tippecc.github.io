<script lang="ts">
    import { SvelteFlow, Controls, Background, BackgroundVariant, MarkerType, type Node, type Edge } from '@xyflow/svelte';
    import { writable } from 'svelte/store';
    import { SvelteComponent, onMount } from 'svelte';
    import '@xyflow/svelte/dist/style.css';



    import EntityNode from '$lib/components/entityNode1.svelte';
    import ActivityNode from '$lib/components/ActivityNode.svelte';
    import PersonNode from '$lib/components/PersonNode.svelte';
    import OrgaNode from '$lib/components/OrgaNode.svelte';
    import SoftwareNode from '$lib/components/SoftwareNode.svelte';

    import data from '$lib/tippecc-prov.json'

    import { createEntityFlowCore, createActionFlow, createPeople, addOrga, addSoftware, addEdgesOnly, createEntityFlow } from '$lib/components//dataProcessing'; // Adjust path as necessary

    const defaultEdgeOptions = {
        style: 'stroke-width: 3; stroke: black; z-index: 1;',
        type: 'floating',
        markerEnd: {
            type: MarkerType.ArrowClosed,
            color: 'black'
        }
    };

    const initialNodes: Node[] = [
        /*
        {
            id: '1',
            type: 'entityNode',
            data: { 
                parameter: 'Prec',
                zeitspranne: [{ start: 1910, end: 1950 }, { start: 1980, end: 2050 }],
                regionalmodell: 'CLMcom-KIT-CCLM5-0-15',
                globalmodell: 'NCC-NorESM1-M',
                einheit: 'kg m-2 s-1',
                szenario: 'SSP-100',
                format: 'netCDF',
                resolutionZeitlich: 'Mon',
                resolutionRaeumlich: 22,
                spatialExtent: [11.97, 12.156, 50.523, 51.058],
                spatialExtent_orig: [11.9, 12.3, 50.3, 51.2],
                dateigroesse: '200MB',
                timestamp: '2019-12-09-T14:52:55Z',
                project: 'CORDEX',
                experiment: 'historic',
                standard: 'CF-1.4',
                bias: 'yes',
                source: 'Climate Limited-area Modelling Community (CLM-Community)',
                institution: 'IMK-TRO/KIT, Karlsruhe, Germany in collaboration with the CLM community',
                domain: 'AFR-22',
                contact: 'hendrik.feldmann@kit.edu',
                tracking_id: 'hdl:21.14103/0f700e74-9c64-4638-9fab-e7a2f3d26b26',
                doi: 'www.exampleDOI.com'
            },
            position: { x: 300, y: 100 },
            style: 'border-radius: 12px; width: 250px; padding: 10px;',
            width: 455,
            height: 320
        },
        {
            id: '2',
            type: 'entityNode',
            data: { 
                parameter: 'Tass',
                zeitspranne: [{ start: 1950, end: 2020 }],
                regionalmodell: 'CLMcom-KIT-CCLM5-0-15',
                globalmodell: 'NCC-NorESM1-M',
                einheit: 'km/h',
                szenario: 'SSP-100',
                format: 'netCDF',
                resolutionZeitlich: 'Week',
                resolutionRaeumlich: 44,
                spatialExtent: [12.013, 12.156, 50.523, 51.058],
                spatialExtent_orig: [11.9, 12.3, 50.3, 51.3],
                dateigroesse: '526MB',
                timestamp: '2019-12-09-T14:52:55Z',
                project: 'CORDEX',
                experiment: 'historic',
                standard: 'CF-1.4',
                bias: 'yes',
                source: 'Climate Limited-area Modelling Community (CLM-Community)',
                institution: 'IMK-TRO/KIT, Karlsruhe, Germany in collaboration with the CLM community',
                domain: 'AFR-22',
                contact: 'hendrik.feldmann@kit.edu',
                tracking_id: 'hdl:21.14103/0f700e74-9c64-4638-9fab-e7a2f3d26b26',
                doi: 'www.exampleDOI.com'
            },
            position: { x: 300, y: 500 },
            style: 'border-radius: 12px; width: 250px; padding: 10px;',
            width: 455,
            height: 320
        },
        {
            id: '3',
            type: 'activityNode',
            data: { 
                aggregateInfo: 'exe:aggregateMonthlySum',
            },
            position: { x: 800, y: 250 },
            style: 'border-radius: 12px; width: 250px; padding: 10px;',
        },
        {
            id: '4',
            type: 'personNode',
            data: { 
                person: 'Franziska',
                orcid: '0000-0001-6892-7046'
            },
            position: { x: -70, y: 250 },
            style: 'border-radius: 12px; width: 250px; padding: 10px;',
        },
        {
            id: '5',
            type: 'orgaNode',
            data: { 
                orga: 'Uni Jena',
                rorid: 'XXX-XXXX-XX'
            },
            position: { x: -400, y: 250 },
            style: 'border-radius: 12px; width: 250px; padding: 10px;',
        },
        {
            id: '6',
            type: 'softwareNode',
            data: { 
                software: 'software:cdo',
                source: 'www.example.com',
                version: '1.7',
                repository: 'https://github.com/rue-a/provo?tab=readme-ov-file',
                license: 'MIT'
            },
            position: { x: 1100, y: 250 },
            style: 'border-radius: 12px; width: 250px; padding: 10px;',
        }
        // Additional nodes...
        */
    ];

    const initialEdges: Edge[] = [
        /*
    {   
        id: 'e1',
        source: '1',
        target: '2',
        label: "wasGeneratedBy",
        sourceHandle: '1-bottom',
        targetHandle: '2-top',
        type: "default",
        labelStyle: 'color: black; font-size: 12px; z-index: 2; pointer-events: none;'
    }

        // Additional edges...
        */
    ];
    
    const nodes = writable<Node[]>(initialNodes);
    const edges = writable<Edge[]>(initialEdges);

    const nodeTypes: Record<string, typeof SvelteComponent> = {
        entityNode: EntityNode as unknown as typeof SvelteComponent,
        activityNode: ActivityNode as unknown as typeof SvelteComponent,
        personNode: PersonNode as unknown as typeof SvelteComponent,
        orgaNode: OrgaNode as unknown as typeof SvelteComponent,
        softwareNode: SoftwareNode as unknown as typeof SvelteComponent,
    };

    onMount(() => {
        const wasDerivedFrom = data.wasDerivedFrom;
        const wasInformedBy = data.wasInformedBy;
        //const hadMember = data.hadMember;
        const People = data.wasAttributedTo;
        const Organisations = data.actedOnBehalfOf;
        const Software = data.wasAssociatedWith
        const used = data.used
        const wasGeneratedBy = data.wasGeneratedBy


        //Create Entities
        const { startEntities, generatedToUsedMap } = createEntityFlowCore(wasDerivedFrom, 'prov:generatedEntity', 'prov:usedEntity');

        // Process all starting entities
        for (let startEntity of startEntities) {
            // create all entity nodes and edges
            createEntityFlow(
                startEntity, 
                nodes, 
                edges, 
                '#6ec13c',
                'border-radius: 50%',
                'height: 40px',
                "was derived from",
                false,
                generatedToUsedMap);
        };

        // Create Actions (renaming for consistency)
        const { startEntities: startActions, generatedToUsedMap: generatedToUsedMapAction } = createEntityFlowCore(wasInformedBy, 'prov:informed', 'prov:informant');

        // Process all starting actions
        for (let startAction of startActions) {
            createActionFlow(
                startAction, 
                nodes, 
                edges, 
                '#3399bf',
                '',
                '',
                "wasInformedBy",
                false,
                generatedToUsedMapAction
            );   
        };

        // create all Collection edges and nodes
        createPeople({
            dataset: People, 
            nodes: nodes,  
            edges: edges, 
            color: '#e28743',
            border_radius: '',
            height: '',
            EdgeLabel: "wasAttributedTo",
            IdName: 'prov:agent',
            EntityName: 'prov:entity',
            swapArrow: false,
            edgeStyle: "stroke: #e28743"
        });

        // create Organisations
        addOrga({
            dataset: Organisations, 
            nodes: nodes,  
            edges:edges, 
            color: '#e28743',
            border_radius: '',
            height: '',
            EdgeLabel: "actedOnBehalfOf",
            IdName: 'prov:responsible',
            EntityName: 'prov:delegate',
            swapArrow: false,
            edgeStyle: "stroke: #e28743"
        });


        //Add Software Nodes
        addSoftware({
            dataset: Software,  
            nodes: nodes, 
            edges: edges, 
            color: '#e28743',
            border_radius: '',
            height: '',
            EdgeLabel: "wasAssociatedWith",
            IdName: 'prov:activity',
            EntityName: 'prov:agent',
            style: 'background: #e28743; border: 2px solid black; width: 150px', // Customize as needed
            swapArrow: true,
            edgestyle: "stroke: #e28743;"
        });


        //Add Edges for Used
        addEdgesOnly({
            dataset: used,  
            edges: edges, 
            EdgeLabel: "used",
            IdName: 'prov:activity',
            EntityName: 'prov:entity',
            swapArrow: false,
            style: "stroke: red;",
            labelStyle: "color: red;"
        });

        /* BRAUCHE ICH DIESES LABEL ??????? ODER REICHT USED
        // Add Edges for wasGeneratedBy
        addEdgesOnly({
            dataset: wasGeneratedBy,  
            edges: edges, 
            EdgeLabel: "wasGeneratedBy",
            IdName: 'prov:entity',
            EntityName: 'prov:activity',
            swapArrow: true,
            style: "stroke: green;",
            labelStyle: "color: green;"
        });
        */  

    });



</script>


<div style="height: 2000px;">
    <SvelteFlow
        {nodes}
        {edges}
        {defaultEdgeOptions}
        nodeTypes={nodeTypes}
        fitView
    >
        <Controls />
        <Background variant={BackgroundVariant.Dots} />
    </SvelteFlow>
</div>
