<script>
    import { Handle, Position } from '@xyflow/svelte';
    
    export let id;

</script>



<div class="p-4 bg-green-50 rounded-lg shadow-lg mx-auto relative space-y-3 inline-block max-w">

    <!-- Right Handle -->
    <Handle
        type="source"
        position={Position.Right}
        id={`${id}-right`}
        style="background-color: black; width: 10px; height: 10px; border-radius: 50%; position: absolute; right: -10px; top: 50%; transform: translateY(-50%);"
    />


    <!-- Label -->
    <div class="text-center text-lg font-semibold text-black px-2 py-1">{id}</div>
</div>