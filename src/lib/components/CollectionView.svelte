<script lang="ts">
    import { SvelteFlow, Controls, Background, BackgroundVariant, MarkerType} from '@xyflow/svelte';
    import { SvelteComponent, onMount } from 'svelte';
    import '@xyflow/svelte/dist/style.css';


    import EntityNode from '$lib/components/entityNode1.svelte';
    import CollectionNode from '$lib/components/CollectionNode.svelte';
    import Sidebar from '$lib/components/Sidebar.svelte'; // Import the Sidebar
    //import TopBar from '$lib/components/TopBar.svelte';
    import { nodes, edges } from '$lib/store';

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

    onMount(() => {
        // Clear the nodes and edges stores before repopulating them
        nodes.set([]);
        edges.set([]);
        const hadMember = data.hadMember;


        // create all entity nodes and edges
        createEntityFlow(
            data,
            nodes, 
            edges, 
            '#6ec13c',
            'border-radius: 50%',
            'height: 40px',
            "was derived from",
            false,
        );


        // create all Collection edges and nodes
        createFlow({
            dataset: hadMember, 
            nodes: nodes,  
            edges:edges,
            EdgeLabel: "hadMember",
            IdName: 'prov:collection',
            EntityName: 'prov:entity',
            swapArrow: false,
            edgeStyle: "stroke: black",
            nodeType: 'collectionNode',
            xPos: -800
        });

        adjustPositions({
            nodes: nodes,
            edges: edges,
            edgeToSelect: "hadMember",
            nodeTypeToAdjust: 'collectionNode',
            minSpace: 400

        });


    });

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