import { get } from 'svelte/store';

export function adjustPositions ({
    edges,
    nodes,
    edgeToSelect,
    nodeTypeToAdjust,
    minSpace
}:  {
    edges:import('svelte/store').Readable<Edge[]>,
    nodes:import('svelte/store').Readable<Edge[]>,
    edgeToSelect:string,
    nodeTypeToAdjust:string,
    minSpace: number
}):void

    {

    const currentEdges = get(edges); // Current edges in the flow
    const currentNodes = get(nodes); // Current edges in the flow
    const attributedEdges = currentEdges.filter(edge => edge.label === edgeToSelect);
    // Group the filtered edges by the source
    const groupedBySource: Record<string, Edge[]> = attributedEdges.reduce((acc, edge) => {
    // If the source doesn't exist in the accumulator, create an empty array for it
    if (!acc[edge.source]) {
        acc[edge.source] = [];
    }
    // Add the edge to the array for the corresponding source
    acc[edge.source].push(edge);
    return acc;
    }, {});

    const yPositionsBySource = {};
    // Now iterate through each group
    Object.keys(groupedBySource).forEach(source => {
        const group = groupedBySource[source];
        
        // Create a list to store y positions for this group
        const yPositions: number[] = [];
        // Iterate through each edge in the group
        group.forEach(edge => {
            const targetId = edge.target;

            // Search for the node in currentNodes that matches the targetId
            const targetNode = currentNodes.find(node => node.id === targetId);

            // If targetNode is found, get its y position and add to the list
            if (targetNode) {
                const yPosition = targetNode.position?.y; // Assuming `position` contains `y`
                if (yPosition !== undefined) {
                    yPositions.push(yPosition);
                } else {
                    yPositions.push(NaN);
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
        // Store the y positions list for this source
        
        yPositionsBySource[source] = yPositionsMean;
    });

    // Adjust y positions of personNodes based on yPositionsBySource
    currentNodes.forEach(node => {
        // Check if the node is a personNode and exists in yPositionsBySource
        if (yPositionsBySource.hasOwnProperty(node.id)) {
            const newYPosition = yPositionsBySource[node.id];

            if (newYPosition !== null && !isNaN(newYPosition)) {
                // Update the node's y position
                node.position.y = newYPosition;
            } else {
                // Handle nodes with null or NaN y positions (optional)
                console.warn(`Skipping node with id ${node.id} due to invalid y position`);
            }
        }
    });

    // Adjust y positions of personNodes ensuring minimum spacing and no duplication
    const adjustYPositions = (nodes, minSpacing) => {
        // Filter the nodes to adjust based on personNode type
        const personNodes = nodes.filter(node => node.type === nodeTypeToAdjust);

        // Map nodes to include yPosition from yPositionsBySource and sort by it
        const sortedNodes = personNodes
            .map(node => ({
                ...node,
                targetY: node.position?.y // Fallback to current position if undefined
            }))
            .sort((a, b) => (a.targetY || 0) - (b.targetY || 0)); // Sort by targetY

        // Track adjusted Y positions to ensure no duplication
        const adjustedYPositions = new Set();

        sortedNodes.forEach((node, index) => {
            let adjustedY = node.targetY;

            // Ensure no duplicates and maintain minimum spacing
            while (
                adjustedYPositions.has(adjustedY) || // Prevent duplicate y positions
                (index > 0 && adjustedY - [...adjustedYPositions].pop() < minSpacing) // Ensure spacing between nodes
            ) {
                adjustedY += minSpacing; // Increase y by minSpacing to avoid conflicts
            }

            // Update node position with adjusted Y
            node.position.y = adjustedY;

            // Add the adjusted y position to the set
            adjustedYPositions.add(adjustedY);
        });

        // Iterate through all person nodes again to check for duplicate Y positions
        let hasDuplicates = true;
        while (hasDuplicates) {
            const seenYPositions = new Set();
            hasDuplicates = false;

            sortedNodes.forEach(node => {
                if (seenYPositions.has(node.position.y)) {
                    // Increment the y position if duplicate is found
                    node.position.y += minSpacing;
                    hasDuplicates = true;
                } else {
                    seenYPositions.add(node.position.y);
                }
            });
        }

        return nodes; // Return the updated nodes
    };

    // Call the function with minimum spacing of 400
    const minSpacing = minSpace;
    const updatedNodes = adjustYPositions(currentNodes, minSpacing);

    // Log updated nodes
    console.log('Updated Nodes with Minimum Spacing:', updatedNodes);

}


export function adjustPositionsNotOrder({
    edges,
    nodes,
    edgeToSelect,
    nodeTypeToAdjust,
    minSpace
}: {
    edges: import('svelte/store').Readable<Edge[]>,
    nodes: import('svelte/store').Readable<Node[]>,
    edgeToSelect: string,
    nodeTypeToAdjust: string,
    minSpace: number
}): void {
    const currentEdges = get(edges); // Current edges in the flow
    const currentNodes = get(nodes); // Current nodes in the flow

    const attributedEdges = currentEdges.filter(edge => edge.label === edgeToSelect);

    // Group the filtered edges by the source
    const groupedBySource: Record<string, Edge[]> = attributedEdges.reduce((acc, edge) => {
        if (!acc[edge.source]) {
            acc[edge.source] = [];
        }
        acc[edge.source].push(edge);
        return acc;
    }, {});

    const yPositionsBySource = {};

    // Iterate through each group to calculate mean Y positions
    Object.keys(groupedBySource).forEach(source => {
        const group = groupedBySource[source];

        // Collect y positions of target nodes
        const yPositions: number[] = [];
        group.forEach(edge => {
            const targetId = edge.target;
            const targetNode = currentNodes.find(node => node.id === targetId);

            if (targetNode?.position?.y !== undefined) {
                yPositions.push(targetNode.position.y);
            }
        });

        const calculateMean = (positions: number[]) => {
            const validPositions = positions.filter(pos => !isNaN(pos));
            if (!validPositions.length) return NaN;

            return validPositions.reduce((sum, pos) => sum + pos, 0) / validPositions.length;
        };

        const yMean = calculateMean(yPositions);
        yPositionsBySource[source] = yMean;
    });

    // Adjust y positions based on calculated means
    const adjustYPositionsPreservingOrder = (nodes, minSpacing) => {
        // Filter nodes by type
        const nodesToAdjust = nodes.filter(node => node.type === nodeTypeToAdjust);

        // Preserve original order
        const originalOrder = nodesToAdjust.map(node => node.id);

        // Map nodes to include target Y positions
        const mappedNodes = nodesToAdjust.map(node => ({
            ...node,
            targetY: yPositionsBySource[node.id] || node.position.y // Use yPositionsBySource if available
        }));

        // Adjust positions incrementally while preserving order
        const adjustedNodes = [];
        let lastAdjustedY = -Infinity;

        originalOrder.forEach(id => {
            const node = mappedNodes.find(n => n.id === id);
            if (!node) return;

            // Ensure minimum spacing and no overlaps
            let adjustedY = Math.max(node.targetY, lastAdjustedY + minSpacing);
            node.position.y = adjustedY;
            lastAdjustedY = adjustedY;

            adjustedNodes.push(node);
        });

        return nodes.map(node => {
            const adjustedNode = adjustedNodes.find(adjusted => adjusted.id === node.id);
            return adjustedNode ? adjustedNode : node;
        });
    };

    // Call adjustment logic with min spacing
    const updatedNodes = adjustYPositionsPreservingOrder(currentNodes, minSpace);

    // Log the updated nodes
    console.log('Updated Nodes Preserving Original Order:', updatedNodes);
}
