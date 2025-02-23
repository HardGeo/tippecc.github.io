import { get } from 'svelte/store';
import type { Edge, Node } from '@xyflow/svelte';


export function adjustPositionSoftware({
    edges,
    nodes,
    EdgeLabel
}: {
    edges: import('svelte/store').Readable<Edge[]>;
    nodes: import('svelte/store').Readable<Node[]>;
    EdgeLabel: string;
}): void {
    const currentNodes = get(nodes);
    const currentEdges = get(edges);

    // Get all activity edges matching the given label
    const activityEdges = currentEdges.filter(edge => edge.label === EdgeLabel);

    if (activityEdges.length === 0) {
        console.warn("No matching activity edges found, skipping adjustment.");
        return;
    }

    // Group edges by source
    const groupedBySource = activityEdges.reduce((acc, edge) => {
        (acc[edge.source] = acc[edge.source] || []).push(edge);
        return acc;
    }, {} as Record<string, Edge[]>);

    // Calculate average y-position for each group and ensure minimum spacing of 200
    const adjustedYPositions = new Map<string, number>();

    Object.entries(groupedBySource).forEach(([sourceId, edges]) => {
        const targetNodes = edges.map(edge => currentNodes.find(node => node.id === edge.target)).filter(Boolean) as Node[];
        if (targetNodes.length === 0) return;

        let avgY = targetNodes.reduce((sum, node) => sum + node.position.y, 0) / targetNodes.length;

        // Ensure a minimum spacing of 200 between nodes
        while ([...adjustedYPositions.values()].some(y => Math.abs(y - avgY) < 200)) {
            avgY += 200;
        }
        adjustedYPositions.set(sourceId, avgY);

        // Update source node with the new y position
        const sourceNode = currentNodes.find(node => node.id === sourceId);
        if (sourceNode) {
            sourceNode.position = { x: sourceNode.position.x, y: avgY };
        }
    });
}




export function adjustPositionPersons({
    edges,
    nodes,
    EdgeLabel
}: {
    edges: import('svelte/store').Readable<Edge[]>;
    nodes: import('svelte/store').Readable<Node[]>;
    EdgeLabel: string;
}): void {
    const currentNodes = get(nodes);
    const currentEdges = get(edges);

    // Get all activity edges matching the given label
    const activityEdges = currentEdges.filter(edge => edge.label === EdgeLabel);

    if (activityEdges.length === 0) {
        console.warn("No matching activity edges found, skipping adjustment.");
        return;
    }

    // Group edges by target
    const groupedBySource = activityEdges.reduce((acc, edge) => {
        (acc[edge.source] = acc[edge.source] || []).push(edge);
        return acc;
    }, {} as Record<string, Edge[]>);

    // Calculate average y-position for each group and ensure minimum spacing of 200
    const adjustedYPositions = new Map<string, number>();

    Object.entries(groupedBySource).forEach(([sourceId, edges]) => {
        const targetNodes = edges.map(edge => currentNodes.find(node => node.id === edge.target)).filter(Boolean) as Node[];
        if (targetNodes.length === 0) return;

        let avgY = targetNodes.reduce((sum, node) => sum + node.position.y, 0) / targetNodes.length;

        // Ensure a minimum spacing of 200 between nodes
        while ([...adjustedYPositions.values()].some(y => Math.abs(y - avgY) < 200)) {
            avgY += 200;
        }
        adjustedYPositions.set(sourceId, avgY);

        // Update source node with the new y position
        const sourceNode = currentNodes.find(node => node.id === sourceId);
        if (sourceNode) {
            sourceNode.position = { x: sourceNode.position.x, y: avgY };
        }
    });

    // Adjust x position for personNodes based on entityNodes
    const personNodes = currentNodes.filter(node => node.type === "personNode");
    personNodes.forEach(personNode => {
        const relatedEdges = currentEdges.filter(edge => edge.source === personNode.id || edge.target === personNode.id);
        const entityNodes = relatedEdges.map(edge => currentNodes.find(node => node.id === (edge.source === personNode.id ? edge.target : edge.source)))
                                       .filter(node => node && node.type === "entityNode") as Node[];
        if (entityNodes.length === 0) return;

        const minX = Math.min(...entityNodes.map(node => node.position.x));
        personNode.position = { x: minX - 1000, y: personNode.position.y };
    });
}

