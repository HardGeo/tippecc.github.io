<script>
    import { Handle, Position } from '@xyflow/svelte';

    export let id;

</script>

<div class="bg-orange-800 rounded-lg shadow-lg relative inline-block p-4" style="z-index: 1;">

    <!-- Left Handle -->
    <Handle
        type="target"
        position={Position.Left}
        id={`${id}-left`}
        style="background-color: black; width: 10px; height: 10px; border-radius: 50%; position: absolute; left: -10px; top: 50%; transform: translateY(-50%);"
    />

    <!-- Right Handle -->
    <Handle
        type="source"
        position={Position.Right}
        id={`${id}-right`}
        style="background-color: black; width: 10px; height: 10px; border-radius: 50%; position: absolute; right: -10px; top: 50%; transform: translateY(-50%);"
    />

    <!-- Left Side: Person and Organisation -->
    <div class="text-white text-center text-lg font-semibold text-black px-2 py-1">{id}</div>
    

    
</div>
