<script lang="ts">
    import { SvelteFlow, Controls, Background, BackgroundVariant, MarkerType} from '@xyflow/svelte';
    import { SvelteComponent, onMount } from 'svelte';
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
        nodes,
        edges } from "$lib/store"; // Import the store

    import data from '$lib/generate_rdfjson/article-prov.json'

    import { createEntityFlow } from '$lib/components//dataProcessing'; // Adjust path as necessary
    import { createFlow } from './dataProcessing_minimalView';
    import {adjustPositions, adjustPositionsNotOrder} from "$lib/components/adjustPositions";

    const defaultEdgeOptions = {
        style: 'stroke-width: 3; stroke: black; z-index: 1;',
        type: 'floating',
        markerEnd: {
            type: MarkerType.ArrowClosed,
            color: 'black'
        }
    };
    
    
    let minZoom = 0.04;

    const nodeTypes: Record<string, typeof SvelteComponent> = {
        entityNode: EntityNode as unknown as typeof SvelteComponent,
        collectionNode: CollectionNode as unknown as typeof SvelteComponent
    };
    
    $: {
        // Adjust labels based on switch state
        updateLabels($isSwitchOn);
        // Clear the nodes and edges stores before repopulating them
        nodes.set([]);
        edges.set([]);
        const hadMember = data.hadMember;


        // create all entity nodes and edges
        createEntityFlow(
            data,
            nodes, 
            edges, 
            $wasDerivedFrom_lb,
            false,
        );


        // create all Collection edges and nodes
        createFlow({
            dataset: hadMember, 
            nodes: nodes,  
            edges:edges,
            EdgeLabel: $hadMember_lb,
            IdName: 'prov:collection',
            EntityName: 'prov:entity',
            swapArrow: false,
            edgeStyle: "stroke: #424242",
            nodeType: 'collectionNode',
            xPos: -800
        });

        adjustPositions({
            nodes: nodes,
            edges: edges,
            edgeToSelect: $hadMember_lb,
            nodeTypeToAdjust: 'collectionNode',
            minSpace: 400

        });
    }

</script>

<div style="height: 2000px;">
    <SvelteFlow 
        {minZoom}
        {nodes}
        {edges}
        {defaultEdgeOptions}
        nodeTypes={nodeTypes}
        fitView
    >

    <Controls/>
    <Background variant={BackgroundVariant.Dots} />
    </SvelteFlow>
    <Sidebar title="Details" />
    
</div>