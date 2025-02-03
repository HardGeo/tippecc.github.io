<script>
    import { Handle, Position } from '@xyflow/svelte';

    import { showDetails, handleKeyDown } from '$lib/store';

    export let id;


    export let data = {
        software: 'software:cdo',
        source: 'www.example.com',
        version: '1.7',
        repository: 'https://github.com/rue-a/provo?tab=readme-ov-file',
        license: 'MIT'
    };
</script>

<div 
    class="rounded-lg shadow-lg relative inline-block" 
    style="z-index: 1;"
    role="button"
    tabindex="0"
    aria-label="Show details"
    on:click={() => showDetails(data)}
    on:keydown={(event) => handleKeyDown(event, data)}
>


    <!-- Left Handle -->
    <Handle
        type="source"
        position={Position.Left}
        id={`${id}-left`}
        style="background-color: black; width: 10px; height: 10px; border-radius: 50%; position: absolute; left: -10px; top: 50%; transform: translateY(-50%);"
    />


    <!-- Display Main Information with exact background size -->
    <div class="bg-[#F8F2F9] text-[#424242] border-4 border-[#C28DB8] font-bold px-4 py-2 rounded-md text-lg inline-block">
        {id}
    </div>
</div>
