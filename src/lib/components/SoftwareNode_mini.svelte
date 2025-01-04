<script>
    import { Handle, Position } from '@xyflow/svelte';

    export let id;

</script>

<div class="bg-purple-100 rounded-lg shadow-lg relative inline-block" style="z-index: 1;">


    <!-- Left Handle -->
    <Handle
        type="source"
        position={Position.Left}
        id={`${id}-left`}
        style="background-color: black; width: 10px; height: 10px; border-radius: 50%; position: absolute; left: -10px; top: 50%; transform: translateY(-50%);"
    />


    <!-- Display Main Information with exact background size -->
    <div class="bg-white text-purple-700 border-4 border-purple-700 font-bold px-4 py-2 rounded-md text-lg inline-block">
        {id}
    </div>
</div>
