<script lang="ts">
    // Import necessary libraries
    import { SvelteComponent } from "svelte";
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
        createFlow 
    } from './dataProcessing_minimalView';
    import { adjustPositions, adjustPositionsNotOrder } from "$lib/components/adjustPositions";
    import EntityNode from '$lib/components/entityNode_mini.svelte';
    import ActivityNode from "./ActivityNode.svelte";
    import SoftwareNode from "./SoftwareNode_mini.svelte";
    import PersonNode from "./PersonNode_mini.svelte";
    import OrgaNode from "./OrgaNode_mini.svelte";
    import Sidebar from '$lib/components/Sidebar.svelte'; // Import the Sidebar
    import { 
        isSwitchOn, 
        updateLabels, 
        wasDerivedFrom_lb, 
        wasInformedBy_lb, 
        wasAttributedTo_lb, 
        actedOnBehalfOf_lb, 
        wasAssociatedWith_lb, 
        wasGeneratedBy_lb, 
        used_lb,
        nodes,
        edges } from "$lib/store"; // Import the store

    // Default edge options
    const defaultEdgeOptions = {
        style: 'stroke-width: 1; stroke: black;',
        type: 'floating',
        markerStart: {
            type: MarkerType.ArrowClosed,
            color: 'black'
        },
        markerEnd: {
            type: MarkerType.None,
        }
    };

    let minZoom = 0.04;
    const connectionLineStyle = 'stroke: black; stroke-width: 3;';
    
    // Define node types
    const nodeTypes: Record<string, typeof SvelteComponent> = {
        entityNode: EntityNode as unknown as typeof SvelteComponent,
        activityNode: ActivityNode as unknown as typeof SvelteComponent,
        softwareNode: SoftwareNode as unknown as typeof SvelteComponent,
        personNode: PersonNode as unknown as typeof SvelteComponent,
        orgaNode: OrgaNode as unknown as typeof SvelteComponent,
    };

    // Watch for changes in the switch state
    $: {
        // Adjust labels based on switch state
        updateLabels($isSwitchOn);

        // Reset nodes and edges
        nodes.set([]);
        edges.set([]);

        // Create Entities
        const { startEntities, generatedToUsedMap } = createEntityFlowCore(
            data.wasDerivedFrom, 
            'prov:generatedEntity', 
            'prov:usedEntity'
        );

        for (let startEntity of startEntities) {
            createEntityFlow(
                startEntity, 
                nodes, 
                edges, 
                $wasDerivedFrom_lb,
                true, 
                generatedToUsedMap, 
                'entityNode', 
                0
            );
        }

        // Create Actions (renaming for consistency)
        const { startEntities: startActions, generatedToUsedMap: generatedToUsedMapAction } = createEntityFlowCore(
            data.wasInformedBy, 
            'prov:informed', 
            'prov:informant'
        );

        for (let startAction of startActions) {
            createEntityFlow(
                startAction, 
                nodes, 
                edges, 
                $wasInformedBy_lb, 
                true, 
                generatedToUsedMapAction, 
                'activityNode', 
                1000
            );
        }

        // Create People (Agents) Nodes and Edges
        createFlow({
            dataset: data.wasAttributedTo,
            nodes: nodes,
            edges: edges,
            EdgeLabel: $wasAttributedTo_lb,
            IdName: 'prov:agent',
            EntityName: 'prov:entity',
            swapArrow: false,
            edgeStyle: "stroke: #424242",
            nodeType: 'personNode',
            xPos: -400
        });

        adjustPositions({
            nodes: nodes,
            edges: edges,
            edgeToSelect: $wasAttributedTo_lb,
            nodeTypeToAdjust: 'personNode',
            minSpace: 400
        });

        // Create Organisations (Agents) Nodes and Edges
        createFlow({
            dataset: data.actedOnBehalfOf,
            nodes: nodes,
            edges: edges,
            EdgeLabel: $actedOnBehalfOf_lb,
            IdName: 'prov:responsible',
            EntityName: 'prov:delegate',
            swapArrow: false,
            edgeStyle: "stroke: #424242",
            nodeType: 'orgaNode',
            xPos: -800
        });

        adjustPositions({
            nodes: nodes,
            edges: edges,
            edgeToSelect: $actedOnBehalfOf_lb,
            nodeTypeToAdjust: 'orgaNode',
            minSpace: 400
        });

        // Add Software Nodes
        addSoftware({
            dataset: data.wasAssociatedWith,
            nodes: nodes,
            edges: edges,
            EdgeLabel: $wasAssociatedWith_lb,
            IdName: 'prov:activity',
            EntityName: 'prov:agent',
            swapArrow: true,
            edgestyle: "stroke: #424242;",
            nodeType: 'softwareNode',
            xPos: 1400
        });

        // Add Edges for Used
        addEdgesOnly({
            dataset: data.used,
            edges: edges,
            EdgeLabel: $used_lb,
            IdName: 'prov:activity',
            EntityName: 'prov:entity',
            swapArrow: false,
            style: "stroke: #424242;",
            labelStyle: "color: black; font-size: 16px;",
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
            style: "stroke: #424242;",
            labelStyle: "color: black; font-size: 16px;",
            handle1: "left",
            handle2: "right"
        });
    }


</script>

<!-- Flow container -->
<div id="flow-container" style="height: 100vh; width: 100%; background-color: #f0f0f0;">
    <SvelteFlow {nodes} {edges} {defaultEdgeOptions} {connectionLineStyle} nodeTypes={nodeTypes} {minZoom} fitView>
        <Background />
    </SvelteFlow>
    <Sidebar title="Details" />
</div>
