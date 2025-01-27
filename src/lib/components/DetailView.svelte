<script lang="ts">
    import { SvelteFlow, Controls, Background, BackgroundVariant, MarkerType} from '@xyflow/svelte';
    import { SvelteComponent } from 'svelte';
    import '@xyflow/svelte/dist/style.css';


    import EntityNode from '$lib/components/entityNode1.svelte';
    import ActivityNode from '$lib/components/ActivityNode.svelte';
    import PersonNode from '$lib/components/PersonNode.svelte';
    import SoftwareNode from '$lib/components/SoftwareNode.svelte';
    import Sidebar from '$lib/components/Sidebar.svelte'; // Import the Sidebar
    //import TopBar from '$lib/components/TopBar.svelte';

    import { 
        isSwitchOn, 
        updateLabels, 
        wasDerivedFrom_lb, 
        wasInformedBy_lb, 
        wasAttributedTo_lb, 
        wasAssociatedWith_lb, 
        wasGeneratedBy_lb, 
        used_lb,
        nodes,
        edges } from "$lib/store"; // Import the store

    import data from '$lib/generate_rdfjson/article-prov.json'
    //import data from '$lib/generate_rdfjson/test.json'

    import { createActionFlow, createPeople, addSoftware, addEdgesOnly, createEntityFlow } from '$lib/components//dataProcessing'; // Adjust path as necessary
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
        activityNode: ActivityNode as unknown as typeof SvelteComponent,
        personNode: PersonNode as unknown as typeof SvelteComponent,
        softwareNode: SoftwareNode as unknown as typeof SvelteComponent,
    };
    $: {
        // Adjust labels based on switch state
        updateLabels($isSwitchOn);

        // Clear the nodes and edges stores before repopulating them
        nodes.set([]);
        edges.set([]);

        //const hadMember = data.hadMember;


        // create all entity nodes and edges
        createEntityFlow(
            data,
            nodes, 
            edges, 
            $wasDerivedFrom_lb,
            false,
        )


        createPeople({
            dataset: data, 
            nodes: nodes,  
            edges: edges, 
            EdgeLabel: $wasAttributedTo_lb,
            //IdName: 'prov:agent',
            //EntityName: 'prov:entity',
            swapArrow: false,
            edgeStyle: "stroke: #e28743"
        });


        adjustPositions({
            nodes: nodes,
            edges: edges,
            edgeToSelect: $wasAttributedTo_lb,
            nodeTypeToAdjust: 'personNode',
            minSpace: 400

        });

        // create Organisations
        /*
        addOrga({
            dataset: data, 
            nodes: nodes,  
            edges: edges, 
            EdgeLabel: $actedOnBehalfOf_lb,
            IdName: 'prov:responsible',
            EntityName: 'prov:delegate',
            swapArrow: false,
            edgeStyle: "stroke: #e28743"
        });
        adjustPositions({
            nodes: nodes,
            edges: edges,
            edgeToSelect: $actedOnBehalfOf_lb,
            nodeTypeToAdjust: 'orgaNode',
            minSpace: 400

        });*/


        //Add Software Nodes
        addSoftware({
            dataset: data,  
            nodes: nodes, 
            edges: edges, 
            EdgeLabel: $wasAssociatedWith_lb,
            IdName: 'prov:activity',
            EntityName: 'prov:agent',
            swapArrow: true,
            edgestyle: "stroke: #e28743;"
        });


        // Process all starting actions
        createActionFlow(
            data, 
            nodes, 
            edges, 
            $wasInformedBy_lb,
            false
        );


        //Add Edges for Used
        addEdgesOnly({
            dataset: data.used,  
            edges: edges, 
            EdgeLabel: $used_lb,
            IdName: 'prov:activity',
            EntityName: 'prov:entity',
            swapArrow: false,
            style: "stroke: red;",
            labelStyle: "color: red; font-size: 16px",
            handle1: "right",
            handle2: "left"
        });


        adjustPositionsNotOrder({
            nodes: nodes,
            edges: edges,
            edgeToSelect: $used_lb,
            nodeTypeToAdjust: 'activityNode',
            minSpace: 200

        });
        adjustPositions({
            nodes: nodes,
            edges: edges,
            edgeToSelect: $wasAssociatedWith_lb,
            nodeTypeToAdjust: 'softwareNode',
            minSpace: 400

        });


        // Add Edges for wasGeneratedBy
        addEdgesOnly({
            dataset: data.wasGeneratedBy,  
            edges: edges, 
            EdgeLabel: $wasGeneratedBy_lb,
            IdName: 'prov:entity',
            EntityName: 'prov:activity',
            swapArrow: true,
            style: "stroke: green;",
            labelStyle: "color: green; font-size: 16px",
            handle1: "left",
            handle2: "right"
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
