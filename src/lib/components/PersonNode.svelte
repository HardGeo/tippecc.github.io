<script>
    import { Handle, Position } from '@xyflow/svelte';

    export let id;

    export let data = {
        person: 'Franziska',
        orcid: '0000-0001-6892-7046',
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

    <!-- Person and ORCID Information -->
    <div class="flex flex-col space-y-3 w-full">
        <!-- Left Side: Person and Organisation -->
        <div class="flex space-x-2 w-full">
            <!-- Person Chip -->
            <div class="bg-orange-700 text-white border border-orange-800 font-bold px-4 py-2 rounded-md text-lg flex-grow text-center">
                {data.person}
            </div>
            <!-- Organisation Chip -->
            <div class="bg-orange-700 text-white border border-orange-800 font-bold px-4 py-2 rounded-md text-lg flex-grow text-center">
                {data.orga}
            </div>
        </div>
    
        <!-- Right Side: ORCID and ROR ID -->
        <div class="flex space-x-2 w-full min-w-0">
            <!-- ORCID Chip -->
            <div class="bg-white text-orange-800 border border-orange-800 font-bold px-4 py-2 rounded-md text-lg flex-grow text-center">
                {data.orcid}
            </div>
            <!-- ROR ID Chip -->
            <div class="bg-white text-orange-800 border border-orange-800 font-bold px-4 py-2 rounded-md text-lg flex-grow text-center">
                {data.rorid}
            </div>
        </div>
    </div>
    

    
</div>
