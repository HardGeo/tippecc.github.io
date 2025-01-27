<script>
    import { Handle, Position } from '@xyflow/svelte';

    export let id;

    export let data = {
        person: 'Franziska',
        orcid: '0000-0001-6892-7046',
        orga: 'Uni Jena',
        rorid: 'XXX-XXX-XXX-XXX'
    };

    import { detailInfo } from '$lib/store';
    let showBubble = false;

    const showDetails = () => {
        showBubble = !showBubble;
        // Update the store with the current entity's details
        if (showBubble) {
            detailInfo.set(data);
        } else {
            detailInfo.set(null); // Clear the details when the bubble is hidden
        }
    };

    const handleKeyDown = (event) => {
        // Trigger showDetails on Enter or Space key press
        if (event.key === 'Enter' || event.key === ' ') {
            event.preventDefault();
            showDetails();
        }
    };
</script>

<!-- Updated with role and keyboard event handling -->
<div
    class="bg-yellow-200 rounded-lg shadow-lg relative inline-block p-4 cursor-pointer"
    style="z-index: 1;"
    role="button"
    tabindex="0"
    aria-label="Show details"
    on:click={showDetails}
    on:keydown={handleKeyDown}
>
    <!-- Right Handle -->
    <Handle
        type="source"
        position={Position.Right}
        id={`${id}-right`}
        style="background-color: black; width: 10px; height: 10px; border-radius: 50%; position: absolute; right: -10px; top: 50%; transform: translateY(-50%);"
    />

    <!-- Person and ORCID Information -->
    <div class="flex flex-col space-y-3 w-full">
        <!-- Person and Organisation -->
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
    </div>
</div>
