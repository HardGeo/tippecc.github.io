<script>
    import { Handle, Position } from '@xyflow/svelte';

    export let id;

    export let data = {
        software: 'software:cdo',
        source: 'www.example.com',
        version: '1.7',
        repository: 'https://github.com/rue-a/provo?tab=readme-ov-file',
        license: 'MIT'
    };
</script>

<div class="bg-gray-300 p-6 rounded-lg shadow-lg relative inline-block" style="z-index: 1;">

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

    <!-- Software Information with Flex Layout -->
    <div class="flex flex-col space-y-3">
        <!-- Row with Software, Version, and License Chips -->
        <div class="flex space-x-3 w-full">
            <!-- Software Chip -->
            <div class="bg-white border border-purple-500 text-purple-500 font-bold px-4 py-2 rounded-md text-lg flex-shrink-0 text-center">
                {data.software}
            </div>

            <!-- Version Chip -->
            <div class="bg-white text-purple-500 border border-purple-500 font-bold px-4 py-2 rounded-md text-lg flex-grow text-center">
                {data.version}
            </div>

            <!-- License Chip -->
            <div class="bg-white text-purple-500 border border-purple-500 font-bold px-4 py-2 rounded-md text-lg flex-grow text-center">
                {data.license}
            </div>
        </div>

        <!-- Source URL Chip -->
        <div class="bg-purple-500 text-white font-bold px-4 py-2 rounded-md text-lg w-full text-center">
            {data.source}
        </div>

        <!-- Repository URL Chip, allows for max 2 lines -->
        <div class="bg-purple-500 text-white font-bold px-4 py-2 rounded-md text-lg w-full break-words text-center">
            {data.repository}
        </div>
    </div>
</div>
