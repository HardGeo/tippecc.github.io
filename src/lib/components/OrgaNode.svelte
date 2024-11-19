<script>
    import { Handle, Position } from '@xyflow/svelte';

    export let id;

    export let data = {
        orga: 'Uni Jena',
        rorid: 'XXX-XXX-XXX-XXX'
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

    <!-- Organization and RORID Information -->
    <div class="flex-col space-y-2">
        <!-- Person Chip -->
        <div class="bg-white text-orange-700 border border-orange-700 text-center font-bold px-4 py-2 rounded-md text-lg items-center justify-center flex-grow">
            {data.orga}
        </div>

        <!-- ORCID Chip -->
        <div class="bg-orange-700 text-white text-center font-bold px-4 py-2 rounded-md text-lg items-center justify-center flex-grow whitespace-nowrap">
            {data.rorid}
        </div>
    </div>
</div>
