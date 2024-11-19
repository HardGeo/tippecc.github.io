<script>
    import { Handle, Position } from '@xyflow/svelte';

    export let id;

    export let data = {
        person: 'Franziska',
        orcid: '0000-0001-6892-7046'
    };
</script>

<div class="bg-yellow-200 rounded-lg shadow-lg relative inline-block p-4" style="z-index: 1;">

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

    <!-- Person and ORCID Information -->
    <div class="flex-col space-y-2">
        <!-- Person Chip -->
        <div class="bg-white text-orange-800 border border-orange-800 text-center font-bold px-4 py-2 rounded-md text-lg items-center justify-center flex-grow">
            {data.person}
        </div>

        <!-- ORCID Chip -->
        <div class="bg-orange-800 text-white text-center font-bold px-4 py-2 rounded-md text-lg items-center justify-center flex-grow whitespace-nowrap">
            {data.orcid}
        </div>
    </div>
</div>
