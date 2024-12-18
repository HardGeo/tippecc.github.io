<script lang="ts">
    import { SvelteFlow, Controls, Background, BackgroundVariant, MarkerType} from '@xyflow/svelte';
    import { SvelteComponent, onMount } from 'svelte';
    import '@xyflow/svelte/dist/style.css';


    import EntityNode from '$lib/components/entityNode1.svelte';
    import ActivityNode from '$lib/components/ActivityNode.svelte';
    import PersonNode from '$lib/components/PersonNode.svelte';
    import OrgaNode from '$lib/components/OrgaNode.svelte';
    import SoftwareNode from '$lib/components/SoftwareNode.svelte';
    import Sidebar from '$lib/components/Sidebar.svelte'; // Import the Sidebar
    import { nodes, edges } from '$lib/store';

    import data from '$lib/generate_rdfjson/article-prov.json'

    import { createActionFlow, createPeople, addOrga, addSoftware, addEdgesOnly, createEntityFlow } from '$lib/components//dataProcessing'; // Adjust path as necessary
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
        orgaNode: OrgaNode as unknown as typeof SvelteComponent,
        softwareNode: SoftwareNode as unknown as typeof SvelteComponent,
    };

    onMount(() => {
        //const hadMember = data.hadMember;


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
        )


        // create all Collection edges and nodes
        createPeople({
            dataset: data, 
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


        adjustPositions({
            nodes: nodes,
            edges: edges,
            edgeToSelect: "wasAttributedTo",
            nodeTypeToAdjust: 'personNode',
            minSpace: 400

        });

        // create Organisations
        addOrga({
            dataset: data, 
            nodes: nodes,  
            edges: edges, 
            color: '#e28743',
            border_radius: '',
            height: '',
            EdgeLabel: "actedOnBehalfOf",
            IdName: 'prov:responsible',
            EntityName: 'prov:delegate',
            swapArrow: false,
            edgeStyle: "stroke: #e28743"
        });
        adjustPositions({
            nodes: nodes,
            edges: edges,
            edgeToSelect: "actedOnBehalfOf",
            nodeTypeToAdjust: 'orgaNode',
            minSpace: 400

        });


        //Add Software Nodes
        addSoftware({
            dataset: data,  
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


        // Process all starting actions
        createActionFlow(
            data, 
            nodes, 
            edges, 
            '#3399bf',
            '',
            '',
            "wasInformedBy",
            false
        );


        //Add Edges for Used
        addEdgesOnly({
            dataset: data.used,  
            edges: edges, 
            EdgeLabel: "used",
            IdName: 'prov:activity',
            EntityName: 'prov:entity',
            swapArrow: false,
            style: "stroke: red;",
            labelStyle: "color: red;",
            handle1: "right",
            handle2: "left"
        });


        adjustPositionsNotOrder({
            nodes: nodes,
            edges: edges,
            edgeToSelect: "used",
            nodeTypeToAdjust: 'activityNode',
            minSpace: 200

        });
        adjustPositions({
            nodes: nodes,
            edges: edges,
            edgeToSelect: "wasAssociatedWith",
            nodeTypeToAdjust: 'softwareNode',
            minSpace: 400

        });


        // Add Edges for wasGeneratedBy
        addEdgesOnly({
            dataset: data.wasGeneratedBy,  
            edges: edges, 
            EdgeLabel: "wasGeneratedBy",
            IdName: 'prov:entity',
            EntityName: 'prov:activity',
            swapArrow: true,
            style: "stroke: green;",
            labelStyle: "color: green;",
            handle1: "left",
            handle2: "right"
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
