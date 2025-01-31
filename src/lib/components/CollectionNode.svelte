<script>
    import { Handle, Position } from '@xyflow/svelte';
    
    export let id;

</script>



<div class="p-4 bg-[#EAF6EA] border-4 border-[#9CCEA0] rounded-lg shadow-lg mx-auto relative inline-block max-w">

    <!-- Right Handle -->
    <Handle
        type="source"
        position={Position.Right}
        id={`${id}-right`}
        style="background-color: black; width: 10px; height: 10px; border-radius: 50%; position: absolute; right: -10px; top: 50%; transform: translateY(-50%);"
    />

    <!-- Label -->
    <div class="text-center text-lg font-bold text-[#424242] px-2 py-1">{id}</div>
</div>