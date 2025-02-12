import { get } from 'svelte/store';

import type { Node, Edge } from '@xyflow/svelte';


export function adjustPositions ({
    edges,
    nodes,
    edgeToSelect,
    nodeTypeToAdjust,
    minSpace
}:  {
    edges:import('svelte/store').Writable<Edge[]>,
    nodes:import('svelte/store').Writable<Node[]>,
    edgeToSelect:string,
    nodeTypeToAdjust:string,
    minSpace: number
}):void

    {

    const currentEdges = get(edges); // Current edges in the flow
    const currentNodes = get(nodes); // Current edges in the flow
    const attributedEdges = currentEdges.filter(edge => edge.label === edgeToSelect);
    //console.log(attributedEdges);
    // Group the filtered edges by the source
    const groupedBySource: Record<string, Edge[]> = attributedEdges.reduce((acc: Record<string, Edge[]>, edge) => {
    // If the source doesn't exist in the accumulator, create an empty array for it
    if (!acc[edge.source]) {
        acc[edge.source] = [];
    }
    // Add the edge to the array for the corresponding source
    acc[edge.source].push(edge);
    return acc;
    }, {});
    //console.log(groupedBySource);

    const yPositionsBySource: Record<string, number> = {};
    const xPositionsBySource: Record<string, number> = {};
    // Now iterate through each group
    Object.keys(groupedBySource).forEach(source => {
        const group = groupedBySource[source];
        
        // Create a list to store y positions for this group
        const yPositions: number[] = [];
        const xPositions: number[] = [];
        // Iterate through each edge in the group
        group.forEach(edge => {
            const targetId = edge.target;

            // Search for the node in currentNodes that matches the targetId
            const targetNode = currentNodes.find(node => node.id === targetId) as Node;

            // If targetNode is found, get its y position and add to the list
            if (targetNode) {
                const yPosition = targetNode.position?.y; // Assuming `position` contains `y`
                const xPosition = targetNode.position?.x; // Assuming `position` contains `y`
                if (yPosition !== undefined && xPosition !== undefined) {
                    yPositions.push(yPosition);
                    xPositions.push(xPosition);
                } else {
                    yPositions.push(NaN);
                    xPositions.push(NaN);
                }
            } else {
                //do nothing
            }

        });
        
        const calculateMean = (positions: number[]) => {
            if (!positions.length) {
                return NaN; // Return NaN if the array is empty
            }
            // Filter valid numbers
            const validPositions = positions.filter(pos => typeof pos === 'number' && !isNaN(pos));
            if (!validPositions.length) {
                return NaN; // Return NaN if no valid positions
            }

            // Calculate the mean
            const sum = validPositions.reduce((acc, curr) => acc + curr, 0);
            return sum / validPositions.length;
        };

        const yPositionsMean = calculateMean(yPositions);
        const xPositionsMean = calculateMean(xPositions);
        // Store the y positions list for this source
        
        yPositionsBySource[source] = yPositionsMean;
        xPositionsBySource[source] = xPositionsMean;
    });

    // Adjust y positions of personNodes based on yPositionsBySource
    currentNodes.forEach(node => {
        // Check if the node is a personNode and exists in yPositionsBySource
        if (yPositionsBySource.hasOwnProperty(node.id) && xPositionsBySource.hasOwnProperty(node.id)) {
            const newYPosition = yPositionsBySource[node.id];
            const newXPosition = xPositionsBySource[node.id];

            if (newYPosition !== null && !isNaN(newYPosition) && (newXPosition !== null && !isNaN(newXPosition)) ) {
                // Update the node's y position
                node.position.y = newYPosition;
                node.position.x = newXPosition;
            } else {
                // Handle nodes with null or NaN y positions (optional)
                console.warn(`Skipping node with id ${node.id} due to invalid y position`);
            }
        }
    });

    
    // Adjust y positions of personNodes ensuring minimum spacing and no duplication
    const adjustYPositions = (nodes: any, minSpacing: number) => {
        // Filter the nodes to adjust based on personNode type
        const personNodes = nodes; // Alle Nodes berücksichtigen

        // Map nodes to include yPosition from yPositionsBySource and sort by it
        const sortedNodes = personNodes
            .map((node:Node) => ({
                ...node,
                targetY: node.position?.y, // Fallback to current position if undefined
                targetX: node.position?.x, // X position
            }))
            .sort((a:any, b:any) => (a.targetY || 0) - (b.targetY || 0)); // Sort by targetY

        // Track adjusted Y positions to ensure no duplication
        const adjustedPositions: Set<string> = new Set();

        sortedNodes.forEach((node:any, index:number) => {
            let adjustedX = node.targetX;
            let adjustedY = node.targetY;

            // Ensure no duplicates and maintain minimum spacing
            while (
                adjustedPositions .has((`${adjustedX},${adjustedY}`)) || // Prevent duplicate y positions
                (index > 0 && (() => {
                    const lastEntry = [...adjustedPositions].values().next().value;
                    if (!lastEntry) return false; // Skip if no previous positions
                    const lastY = parseFloat(lastEntry.split(',')[1]);
                    return adjustedY - lastY < minSpacing;
                })())                

            ) {
                adjustedY += minSpacing; // Increase y by minSpacing to avoid conflicts
                adjustedX += minSpacing / 2;  // Slight shift in X to separate horizontally as well
            }

            // Update node position with adjusted Y and X
            node.position.y = adjustedY;
            node.position.x = adjustedX;

            // Add the adjusted xy position to the set
            adjustedPositions.add(`${adjustedX},${adjustedY}`);
        });

        // Iterate through all person nodes again to check for duplicate Y positions
        let hasDuplicates = true;
        while (hasDuplicates) {
            const seenPositions  = new Set();
            hasDuplicates = false;

            sortedNodes.forEach((node:Node) => {
                const positionKey = `${node.position.x},${node.position.y}`; // Key combining both X and Y
                if (seenPositions.has(positionKey)) {
                    // Increment the y position if duplicate is found
                    node.position.y += minSpacing;
                    node.position.x += minSpacing / 2; // Adjust X position as well, to prevent overlap horizontally
                    hasDuplicates = true;
                } else {
                    seenPositions.add(positionKey);
                }
            });
        }

        return nodes; // Return the updated nodes
    };

    // Call the function with minimum spacing of 400
    const minSpacing = minSpace;
    const updatedNodes = adjustYPositions(currentNodes, minSpacing);

    // Log updated nodes
    //console.log('Updated Nodes with Minimum Spacing: ', nodeTypeToAdjust, updatedNodes);
    

}