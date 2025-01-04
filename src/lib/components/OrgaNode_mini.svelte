<script>
    import { Handle, Position } from '@xyflow/svelte';

    export let id;

</script>

<div class="bg-white rounded-lg shadow-lg relative inline-block" style="z-index: 1;">


    <!-- Right Handle -->
    <Handle
        type="source"
        position={Position.Right}
        id={`${id}-right`}
        style="background-color: black; width: 10px; height: 10px; border-radius: 50%; position: absolute; right: -10px; top: 50%; transform: translateY(-50%);"
    />

    <!-- Left Side: Person and Organisation -->
    <div class="bg-white text-orange-800 border-4 border-orange-700 font-bold px-4 py-4 rounded-md text-lg inline-block">{id}</div>
    

    
</div>
