<script lang="ts">
    import { SvelteFlow, Controls, Background, BackgroundVariant, MarkerType} from '@xyflow/svelte';
    import { SvelteComponent, onMount } from 'svelte';
    import * as d3 from 'd3'; // Import D3.js
    import '@xyflow/svelte/dist/style.css';


    import EntityNode from '$lib/components/entityNode1.svelte';
    import CollectionNode from '$lib/components/CollectionNode.svelte';
    import Sidebar from '$lib/components/Sidebar.svelte'; // Import the Sidebar
    //import TopBar from '$lib/components/TopBar.svelte';
    import { 
        isSwitchOn, 
        updateLabels, 
        wasDerivedFrom_lb, 
        hadMember_lb,
        nodes_col,
        edges_col } from "$lib/store"; // Import the store

    import data from '$lib/generate_rdfjson_rev/subgraphs/TIPPECC_AWI-ESM-1-REcoM_day_r1i1p1f1__ai__mm_1850_2100__yearsum_mean_1981_2000-2080_2099_prov.nc.json'

    import { AddEntities, createCollection } from './dataProcessing';
    import {adjustPositions} from "$lib/components/adjustPositions";

    const defaultEdgeOptions = {
        style: 'stroke-width: 3; stroke: black; z-index: 1;',
        type: 'floating',
        markerEnd: {
            type: MarkerType.ArrowClosed,
            color: 'black'
        }
    };
    
    
    let minZoom = 0.01;

    const nodeTypes: Record<string, typeof SvelteComponent> = {
        entityNode: EntityNode as unknown as typeof SvelteComponent,
        collectionNode: CollectionNode as unknown as typeof SvelteComponent
    };
    
    function initializeD3Layout(nodeData:any, edgeData:any) {
        const simulation = d3.forceSimulation(nodeData)
            .force('charge', d3.forceManyBody().strength(-5000))
            .force('link', d3.forceLink(edgeData).id((d:any) => d.id).distance(800))
            .force('center', d3.forceCenter(500, 300))
            .alpha(1)
            .alphaDecay(0.03); // Ensure smooth positioning over time

        simulation.on("end", () => {
            // Create a deep copy to trigger reactivity
            nodes_col.set(nodeData.map((node:any) => ({
                ...node,
                position: { x: node.x, y: node.y }
            })));

            edges_col.set(edgeData.map((edge:any) => ({
                ...edge,
                source: edge.source.id ?? edge.source,  // Ensure the source ID is correctly mapped
                target: edge.target.id ?? edge.target,  // Ensure the target ID is correctly mapped
            })));
            
            createCollection({
                dataset: data, 
                nodes: nodes_col, 
                edges: edges_col,
                EdgeLabel: $hadMember_lb,
                swapArrow: false,
                edgeStyle: "stroke: #FFA500"
            });

            adjustPositions({
                edges: edges_col,
                nodes: nodes_col,
                edgeToSelect: $hadMember_lb,
                nodeTypeToAdjust: "collectionNode",
                minSpace: 400
            });

            /*
            //Add Software Nodes
            addSoftware({
                dataset: data,  
                nodes: nodes_col, 
                edges: edges_col, 
                EdgeLabel: $wasAssociatedWith_lb,
                IdName: 'prov:activity',
                EntityName: 'prov:agent',
                swapArrow: true,
                edgestyle: "stroke: #CE93D8;"
            });

            adjustPositions({
                edges: edges_col,
                nodes: nodes_col,
                edgeToSelect: $wasAssociatedWith_lb,
                nodeTypeToAdjust: "softwareNode",
                minSpace: 400
            });
            */
        });

        return simulation;
    }

    $: {
        updateLabels($isSwitchOn);
    }

    // Update edges with new labels whenever the label changes
    $: {
        edges_col.update((edges) => {
            return edges.map((edge) => {
                // Update the label based on the edge's existing label (edge.label)
                let label;
                switch (edge.label) {
                    case 'derived from':
                        label = $wasDerivedFrom_lb;
                        break;
                    case 'wasDerivedFrom':
                        label = $wasDerivedFrom_lb;
                        break;
                    case 'part of collection':
                        label = $hadMember_lb;
                        break;
                    case 'hadMember':
                        label = $hadMember_lb;
                        break;
                }

                // Return the updated edge with the new label
                return { ...edge, label };
            });
        });
    }

    onMount(() => {
        // Adjust labels based on switch state

        // Clear the nodes and edges stores before repopulating them
        nodes_col.set([]);
        edges_col.set([]);

        //const hadMember = data.hadMember;
        AddEntities(data, nodes_col, edges_col, $wasDerivedFrom_lb, "entityNode");



        // Fetch node and edge data to use in the D3 simulation
        let nodeArray;
        let edgeArray;
        nodes_col.subscribe(n => nodeArray = n);
        edges_col.subscribe(e => edgeArray = e);

        // Initialize D3 layout
        initializeD3Layout(nodeArray, edgeArray);

    }) 

</script>

<div style="height: 2000px;">
    <SvelteFlow 
        {minZoom}
        nodes={nodes_col}
        edges={edges_col}
        {defaultEdgeOptions}
        nodeTypes={nodeTypes}
        fitView
    >

    <Controls/>
    <Background variant={BackgroundVariant.Dots} />
    </SvelteFlow>
    <Sidebar/>
    
</div>