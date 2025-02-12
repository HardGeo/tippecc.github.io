<script lang="ts">
    
    //import '../app.css';
    import { onMount } from "svelte";
    import { writable } from 'svelte/store';
    import {
        SvelteFlow,
        Background,
        MarkerType
    } from '@xyflow/svelte';
    //import { SvelteFlow } from '@xyflow/svelte/dist/lib/container/SvelteFlow.js';
    import '@xyflow/svelte/dist/style.css';
    import data from '$lib/tippecc-prov.json';
    
    import { 
        createEntityFlowCore, 
        addSoftware, 
        addEdgesOnly,
        createEntityFlow,
        createFlow } from './dataProcessing'; // Adjust path as necessary

    import * as d3 from 'd3'; // Import D3.js

    const defaultEdgeOptions = {
    style: 'stroke-width: 1; stroke: black;',
    type: 'floating',
    markerStart: { // Change this to markerStart for arrows pointing to the source
        type: MarkerType.ArrowClosed,
        color: 'black'
    },
    markerEnd: { // This will keep the original arrow at the end if needed
        type: MarkerType.None, // Change to None if you don't want an arrow at the end
    }
    };

    interface Node {
        id: string;
        data: { label: string };
        position: { x: number; y: number };
        style: string;
    }

    const connectionLineStyle = 'stroke: black; stroke-width: 3;';

    // Create writable stores for nodes and edges
    const nodes = writable([]);
    const edges = writable([]);

    // Function to initialize D3 force layout
    function initializeD3Layout(nodeData, edgeData) {
        const simulation = d3.forceSimulation(nodeData)
            .force('charge', d3.forceManyBody().strength(-3000)) // Adjust for node spacing
            .force('link', d3.forceLink(edgeData).id(d => d.id).distance(1))
            .force('center', d3.forceCenter(500, 300)) // Center on screen

        // Update the Svelte store on each simulation tick
        simulation.on('tick', () => {
            nodes.set(nodeData.map(node => ({
                ...node,
                position: { x: node.x, y: node.y }
            })));
        });
    }

    onMount(() => {
        const wasDerivedFrom = data.wasDerivedFrom;
        const wasInformedBy = data.wasInformedBy;
        const hadMember = data.hadMember;
        const People = data.wasAttributedTo;
        const Organisations = data.actedOnBehalfOf;
        const Software = data.wasAssociatedWith
        const used = data.used
        const wasGeneratedBy = data.wasGeneratedBy


        //Create Entities
        const { startEntities, generatedToUsedMap } = createEntityFlowCore(wasDerivedFrom, 'prov:generatedEntity', 'prov:usedEntity');
        console.log(startEntities);
        console.log(generatedToUsedMap);
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
        }


        // Create Actions (renaming for consistency)
        const { startEntities: startActions, generatedToUsedMap: generatedToUsedMapAction } = createEntityFlowCore(wasInformedBy, 'prov:informed', 'prov:informant');

        // Process all starting actions
        for (let startAction of startActions) {
            createEntityFlow(
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
        }
        
        // create all Collection edges and nodes
        createFlow({
            dataset: hadMember, 
            nodes: nodes,  
            edges:edges,
            color: '#6ec13c',
            border_radius: 'border-radius: 50%',
            height: 'height: 40px',
            EdgeLabel: "hadMember",
            IdName: 'prov:collection',
            EntityName: 'prov:entity',
            swapArrow: true,
            edgeStyle: "stroke: black"
        });

        //Create all People (Agents) Nodes and Edges
        createFlow({
            dataset: People, 
            nodes: nodes,  
            edges:edges, 
            color: '#e28743',
            border_radius: '',
            height: '',
            EdgeLabel: "wasAttributedTo",
            IdName: 'prov:agent',
            EntityName: 'prov:entity',
            swapArrow: false,
            edgeStyle: "stroke: #e28743"
        });

        //Create all Organisations (Agents) Nodes and Edges
        createFlow({
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

        // Fetch node and edge data to use in the D3 simulation
        let nodeArray;
        let edgeArray;
        nodes.subscribe(n => nodeArray = n);
        edges.subscribe(e => edgeArray = e);

        // Initialize D3 layout
        initializeD3Layout(nodeArray, edgeArray);   
    });

</script>



<div id="flow-container" style="height: 100vh; width: 100%; background-color: #f0f0f0;">
    <SvelteFlow {nodes} {edges} {defaultEdgeOptions} {connectionLineStyle} fitView>
        <Background />
    </SvelteFlow>
</div>
