<script lang="ts">
    
    //import '../app.css';
    import { onMount, SvelteComponent } from "svelte";
    import { writable } from 'svelte/store';
    import {
        SvelteFlow,
        Background,
        MarkerType
    } from '@xyflow/svelte';
    import '@xyflow/svelte/dist/style.css';
    import data from '$lib/generate_rdfjson/article-prov.json';
    import { 
        createEntityFlowCore, 
        addSoftware, 
        addEdgesOnly,
        createEntityFlow,
        createFlow } from './dataProcessing_minimalView'; // Adjust path as necessary
    
    import {adjustPositions, adjustPositionsNotOrder} from "$lib/components/adjustPositions";

    import EntityNode from '$lib/components/entityNode_mini.svelte';
	import ActivityNode from "./ActivityNode.svelte";
    import SoftwareNode from "./SoftwareNode_mini.svelte";
    import PersonNode from "./PersonNode_mini.svelte";
    import OrgaNode from "./OrgaNode_mini.svelte";

    const defaultEdgeOptions = {
    style: 'stroke-width: 1; stroke: black;',
    type: 'floating',
    markerStart: { // Change this to markerStart for arrows pointing to the source
        type: MarkerType.ArrowClosed,
        color: 'black'
    },
    markerEnd: { // This will keep the original arrow at the end if needed
        type: MarkerType.None   ,
    }
    };

    let minZoom = 0.04;

    const connectionLineStyle = 'stroke: black; stroke-width: 3;';

    const nodeTypes: Record<string, typeof SvelteComponent> = {
        entityNode: EntityNode as unknown as typeof SvelteComponent,
        activityNode: ActivityNode as unknown as typeof SvelteComponent,
        softwareNode: SoftwareNode as unknown as typeof SvelteComponent,
        personNode: PersonNode as unknown as typeof SvelteComponent,
        orgaNode: OrgaNode as unknown as typeof SvelteComponent,
    };

    // Create writable stores for nodes and edges
    const nodes = writable([]);
    const edges = writable([]);

    onMount(() => {
        nodes.set([]);
        edges.set([]);

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
        // Process all starting entities
        for (let startEntity of startEntities) {
            // create all entity nodes and edges
            createEntityFlow(
                startEntity, 
                nodes, 
                edges, 
                "was derived from",
                false,
                generatedToUsedMap,
                'entityNode',
                0);   
        }


        // Create Actions (renaming for consistency)
        const { startEntities: startActions, generatedToUsedMap: generatedToUsedMapAction } = createEntityFlowCore(wasInformedBy, 'prov:informed', 'prov:informant');

        // Process all starting actions
        for (let startAction of startActions) {
            createEntityFlow(
                startAction, 
                nodes, 
                edges, 
                "wasInformedBy",
                false,
                generatedToUsedMapAction,
                'activityNode',
                1000
            );   
        }
        /*
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
            edgeStyle: "stroke: black",
            xPos: -400
        });*/

        //Create all People (Agents) Nodes and Edges
        createFlow({
            dataset: People, 
            nodes: nodes,  
            edges: edges, 
            EdgeLabel: "wasAttributedTo",
            IdName: 'prov:agent',
            EntityName: 'prov:entity',
            swapArrow: false,
            edgeStyle: "stroke: #e28743",
            nodeType: 'personNode',
            xPos: -400
        });
        
        
        adjustPositions({
            nodes: nodes,
            edges: edges,
            edgeToSelect: "wasAttributedTo",
            nodeTypeToAdjust: 'default',
            minSpace: 400

        });

        //Create all Organisations (Agents) Nodes and Edges
        createFlow({
            dataset: Organisations, 
            nodes: nodes,  
            edges:edges, 
            EdgeLabel: "actedOnBehalfOf",
            IdName: 'prov:responsible',
            EntityName: 'prov:delegate',
            swapArrow: false,
            edgeStyle: "stroke: #e28743",
            nodeType: 'orgaNode',
            xPos: -800
        });
      
        adjustPositions({
            nodes: nodes,
            edges: edges,
            edgeToSelect: "actedOnBehalfOf",
            nodeTypeToAdjust: 'default',
            minSpace: 400

        });


        //Add Software Nodes
        addSoftware({
            dataset: Software,  
            nodes: nodes, 
            edges: edges, 
            EdgeLabel: "wasAssociatedWith",
            IdName: 'prov:activity',
            EntityName: 'prov:agent',
            swapArrow: true,
            edgestyle: "stroke: #e28743;",
            nodeType: 'softwareNode',
            xPos: 1400
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
            labelStyle: "color: red; font-size: 16px;",
            handle1: "right",
            handle2: "left"
        });

        adjustPositionsNotOrder({
            nodes: nodes,
            edges: edges,
            edgeToSelect: "used",
            nodeTypeToAdjust: 'default',
            minSpace: 200

        });
        adjustPositions({
            nodes: nodes,
            edges: edges,
            edgeToSelect: "wasAssociatedWith",
            nodeTypeToAdjust: 'default',
            minSpace: 400

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
            labelStyle: "color: green; font-size: 16px;",
            handle1: "left",
            handle2: "right"
        });

        // Fetch node and edge data to use in the D3 simulation
        let nodeArray;
        let edgeArray;
        nodes.subscribe(n => nodeArray = n);
        edges.subscribe(e => edgeArray = e);

    });


</script>



<div id="flow-container" style="height: 100vh; width: 100%; background-color: #f0f0f0;">
    <SvelteFlow {nodes} {edges} {defaultEdgeOptions} {connectionLineStyle} nodeTypes={nodeTypes} {minZoom} fitView>
        <Background />
    </SvelteFlow>
</div>
