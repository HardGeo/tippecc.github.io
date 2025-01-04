<script>
    import { Handle, Position } from '@xyflow/svelte';

    export let id;

</script>

<div class="bg-blue-100 rounded-lg shadow-lg relative inline-block" style="z-index: 1;">
    <!-- Top Handle -->
    <Handle
        type="target"
        position={Position.Top}
        id={`${id}-top`}
        style="background-color: black; width: 10px; height: 10px; border-radius: 50%; position: absolute; top: -10px; left: 50%; transform: translateX(-50%);"
    />

    <!-- Bottom Handle -->
    <Handle
        type="source"
        position={Position.Bottom}
        id={`${id}-bottom`}
        style="background-color: black; width: 10px; height: 10px; border-radius: 50%; position: absolute; bottom: -10px; left: 50%; transform: translateX(-50%);"
    />

    <!-- Left Handle -->
    <Handle
        type="source"
        position={Position.Left}
        id={`${id}-left`}
        style="background-color: black; width: 10px; height: 10px; border-radius: 50%; position: absolute; left: -10px; top: 50%; transform: translateY(-50%);"
    />

    <!-- Right Handle -->
    <Handle
        type="target"
        position={Position.Right}
        id={`${id}-right`}
        style="background-color: black; width: 10px; height: 10px; border-radius: 50%; position: absolute; right: -10px; top: 50%; transform: translateY(-50%);"
    />

    <!-- Display Main Information with exact background size -->
    <div class="bg-white text-blue-700 border-4 border-blue-700 font-bold px-4 py-2 rounded-md text-lg inline-block">
        {id}
    </div>
</div>
