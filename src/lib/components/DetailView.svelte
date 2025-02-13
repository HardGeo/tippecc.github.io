<script lang="ts">
    import { SvelteFlow, Controls, Background, BackgroundVariant, MarkerType} from '@xyflow/svelte';
    import { SvelteComponent, onMount } from 'svelte';
    import * as d3 from 'd3'; // Import D3.js
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
        nodes_det,
        edges_det } from "$lib/store"; // Import the store

    //import data from '$lib/generate_rdfjson/article-prov.json';
    import data from '$lib/generate_rdfjson_rev/AWI.json'

    import { AddActions, createPeople, addSoftware, addEdgesOnly, AddEntities } from '$lib/components//dataProcessing'; // Adjust path as necessary
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
        activityNode: ActivityNode as unknown as typeof SvelteComponent,
        personNode: PersonNode as unknown as typeof SvelteComponent,
        softwareNode: SoftwareNode as unknown as typeof SvelteComponent,
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
            nodes_det.set(nodeData.map((node:any) => ({
                ...node,
                position: { x: node.x, y: node.y }
            })));

            edges_det.set(edgeData.map((edge:any) => ({
                ...edge,
                source: edge.source.id ?? edge.source,  // Ensure the source ID is correctly mapped
                target: edge.target.id ?? edge.target,  // Ensure the target ID is correctly mapped
            })));
            

            // OPTIONAL: TRANSFER People and Organisation to Entity
            createPeople({
                dataset: data, 
                nodes: nodes_det,  
                edges: edges_det, 
                EdgeLabel: $wasAttributedTo_lb,
                swapArrow: false,
                edgeStyle: "stroke: #CC8400"
            });
            
            adjustPositions({
                edges: edges_det,
                nodes: nodes_det,
                edgeToSelect: $wasAttributedTo_lb,
                nodeTypeToAdjust: "personNode",
                minSpace: 400
            });
            /*
            AddActions(
                data,
                nodes_det, 
                edges_det, 
                $wasInformedBy_lb
            );
            */
            //Add Edges for Used
            addEdgesOnly({
                dataset: data.used,  
                edges: edges_det, 
                EdgeLabel: $used_lb,
                IdName: 'prov:activity',
                EntityName: 'prov:entity',
                swapArrow: false,
                style: "stroke: #88BCE4;",
                labelStyle: "color: black; font-size: 16px",
                handle1: "right",
                handle2: "left",
                IdAppendix: "used"
            });

            // Add Edges for wasGeneratedBy
            addEdgesOnly({
                dataset: data.wasGeneratedBy,  
                edges: edges_det, 
                EdgeLabel: $wasGeneratedBy_lb,
                IdName: 'prov:entity',
                EntityName: 'prov:activity',
                swapArrow: true,
                style: "stroke: #6BAF74;",
                labelStyle: "color: black; font-size: 16px",
                handle1: "right",
                handle2: "left",
                IdAppendix: "wasGeneratedBy",
            });
            /*
            adjustPositions({
                edges: edges_det,
                nodes: nodes_det,
                edgeToSelect: $used_lb,
                nodeTypeToAdjust: "activityNode",
                minSpace: 400
            });*/

            //Add Software Nodes
            addSoftware({
                dataset: data,  
                nodes: nodes_det, 
                edges: edges_det, 
                EdgeLabel: $wasAssociatedWith_lb,
                IdName: 'prov:activity',
                EntityName: 'prov:agent',
                swapArrow: true,
                edgestyle: "stroke: #CE93D8;"
            });

            adjustPositions({
                edges: edges_det,
                nodes: nodes_det,
                edgeToSelect: $wasAssociatedWith_lb,
                nodeTypeToAdjust: "softwareNode",
                minSpace: 400
            });
        
        });

        return simulation;
    }

    $: {
        updateLabels($isSwitchOn);
    }

    // Update edges with new labels whenever the label changes
    $: {
        edges_det.update((edges) => {
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
                    case 'followed by':
                        label = $wasInformedBy_lb;
                        break;
                    case 'wasInformedBy':
                        label = $wasInformedBy_lb;
                        break;
                    case 'resp. person':
                        label = $wasAttributedTo_lb;
                        break;
                    case 'wasAttributedTo':
                        label = $wasAttributedTo_lb;
                        break;
                    case 'part of software':
                        label = $wasAssociatedWith_lb;
                        break;
                    case 'wasAssociatedWith':
                        label = $wasAssociatedWith_lb;
                        break;
                    case 'generated by':
                        label = $wasGeneratedBy_lb;
                        break;
                    case 'wasGeneratedBy':
                        label = $wasGeneratedBy_lb;
                        break;
                    case 'used dataset':
                        label = $used_lb;
                        break;
                    case 'used':
                        label = $used_lb;
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
        nodes_det.set([]);
        edges_det.set([]);

        //const hadMember = data.hadMember;
        AddEntities(data, nodes_det, edges_det, $wasDerivedFrom_lb, "entityNode");
        AddActions(
                data,
                nodes_det, 
                edges_det, 
                $wasInformedBy_lb
        );


        // Fetch node and edge data to use in the D3 simulation
        let nodeArray;
        let edgeArray;
        nodes_det.subscribe(n => nodeArray = n);
        edges_det.subscribe(e => edgeArray = e);

        // Initialize D3 layout
        initializeD3Layout(nodeArray, edgeArray);

    }) 

</script>

<div style="height: 1000px;">
    <SvelteFlow 
        {minZoom}
        nodes={nodes_det}
        edges={edges_det}
        {defaultEdgeOptions}
        nodeTypes={nodeTypes}
        fitView
    >

    <Controls/>
    <Background variant={BackgroundVariant.Dots} />
    </SvelteFlow>
    <Sidebar />
    
</div>
