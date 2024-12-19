<script>
    import Timeline from '$lib/components/timeline.svelte';
    import { Handle, Position } from '@xyflow/svelte';
    
    export let id;
    export let selected;
    export let selectable;
    export let deletable;
    export let zIndex;
    export let dragging;
    export let draggable;
    export let dragHandle;
    export let parentId;
    export let type;
	export let isConnectable;
	export let positionAbsoluteX;
	export let positionAbsoluteY;
	export let width;
	export let height;

	export let data = {
		parameter: '',
		zeitspranne: [{ start: 1950, end: 2010 }],
		regionalmodell: '',
		globalmodell: '',
		einheit: '',
		szenario: '',
		format: '',
		resolutionZeitlich: '',
		resolutionRaeumlich: 0,
		spatialExtent: [0, 0, 0, 0],
        spatialExtent_orig: [0,0,0,0],
		dateigroesse: '',
        timestamp: '2019-12-09-T14:52:55Z',
        project: 'CORDEX',
        experiment: 'historic',
        standard: 'CF-1.4',
        bias: 'yes',
        source: 'Climate Limited-area Modelling Community (CLM-Community)',
        institution: 'IMK-TRO/KIT, Karlsruhe, Germany in collaboration with the CLM community',
        domain: 'AFR-22',
        contact: 'hendrik.feldmann@kit.edu',
        tracking_id: 'hdl:21.14103/0f700e74-9c64-4638-9fab-e7a2f3d26b26',
        doi: 'www.exampleDOI.com'
	}
    
    import { detailInfo } from '$lib/store';  // Import the store
    let showBubble = false;

    const showDetails = () => {
        showBubble = !showBubble;
        // Update the store with the current entity's details
        if (showBubble) {
            detailInfo.set(data);
        } else {
            detailInfo.set(null);  // Clear the details when the bubble is hidden
        }
    };

</script>



<div class="p-4 bg-green-50 rounded-lg shadow-lg space-y-3 mx-auto relative" style="z-index: 1;">
    <!-- Top Handle -->
    <Handle
    type="target"
    position={Position.Top}
    id={`${id}-top`}
    style="background-color: black; width: 10px; height: 10px; border-radius: 50%; position: absolute; margin-top: -5px"
    />

    <!-- Bottom Handle -->
    <Handle
        type="source"
        position={Position.Bottom}
        id={`${id}-bottom`}
        style="background-color: black; width: 10px; height: 10px; border-radius: 50%; position: absolute; margin-bottom: -2px;"
    />

    <!-- Left Handle -->
    <Handle
    type="target"
    position={Position.Left}
    id={`${id}-left`}
    style="background-color: black; width: 10px; height: 10px; border-radius: 50%; transform: translateX(0px); margin-top: -5px; margin-left: -8px;"
    />

    <!-- Right Handle -->
    <Handle
        type="target"
        position={Position.Right}
        id={`${id}-right`}
        style="background-color: black; width: 10px; height: 10px; border-radius: 50%; transform: translateX(0px); margin-top: -5px; margin-right: -7px;"
    />

    <div class="flex space-x-4 w-full justify-between">
        <!-- Parameter Chip -->
        <div class="bg-green-700 text-gray-100 rounded-md h-8 leading-tight inline-flex items-center justify-center text-lg font-bold flex-grow">
            {data.parameter}
        </div>

        <!-- Unit Chip -->
        <div class="bg-white text-green-700 border border-green-700 rounded-md h-8 leading-tight inline-flex items-center justify-center text-xs flex-grow font-bold">
            {data.einheit}
        </div>

        <!-- Details Button -->
        <div class="relative group w-auto flex-grow">
            <!-- Copy Icon -->
            <button
                on:click={showDetails}
                class="absolute -top-2 right-0 bg-gray-200 p-2 rounded-md shadow-md hover:bg-gray-200"
                title="Show Details"
            >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-600 hover:text-gray-800" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd"/>
                </svg>
            </button>
        </div>
    </div>

    <!-- Time Span with Graphical Timeline -->
    <div class="space-y-1 w-full justify-evenly">
        <div class="flex items-center space-x-2">
            <Timeline
                step={25}
                activeRanges={data.zeitspranne}
            />
        </div>
    </div>

    <div class="flex space-x-4 w-full justify-between">
        <!-- Temporal Resolution Chip -->
        <div class="bg-green-700 text-gray-100 font-bold px-4 py-2 rounded-md inline-flex items-center justify-center inline-block text-sm flex-grow">
            {data.resolutionZeitlich}
        </div>

		<div class="relative group flex flex-col items-center space-y-2 bg-white border border-green-700 rounded-md p-2 overflow-hidden flex-grow">
            <!-- SVG map visualization -->
            <svg class="w-14 h-14" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                <!-- Black outline for original extent -->
                <rect 
                    x=0
                    y=0 
                    width=100
                    height=100
                    fill="#fee2e2" 
                    stroke="none" 
                    stroke-width="3"
                />

                {#if data.spatialExtent && data.spatialExtent.length === 4 && data.spatialExtent_orig && data.spatialExtent_orig.length === 4}
                    <!-- Calculate the red outline for the current extent -->
                    <rect 
                        x={(data.spatialExtent[0] - data.spatialExtent_orig[0]) / (data.spatialExtent_orig[1] - data.spatialExtent_orig[0]) * 100}
                        y={(data.spatialExtent[2] - data.spatialExtent_orig[2]) / (data.spatialExtent_orig[3] - data.spatialExtent_orig[2]) * 100}
                        width={(data.spatialExtent[1] - data.spatialExtent[0]) / (data.spatialExtent_orig[1] - data.spatialExtent_orig[0]) * 100}
                        height={(data.spatialExtent[3] - data.spatialExtent[2]) / (data.spatialExtent_orig[3] - data.spatialExtent_orig[2]) * 100}
                        fill="none" 
                        stroke="red" 
                        stroke-width="2"
                    />
                {/if}
            </svg>

			<!-- Hover Text -->
			<div class="absolute inset-0 flex items-center justify-center bg-gray-600 bg-opacity-75 text-white text-xs rounded-md opacity-0 group-hover:opacity-100 transition-opacity duration-300 p-2">
				<!-- First line for xmin and xmax -->
				<div>{data.spatialExtent[0]}, {data.spatialExtent[1]}</div>
				<!-- Second line for ymin and ymax -->
				<div>{data.spatialExtent[2]}, {data.spatialExtent[3]}</div>
			</div>
		</div>

        <!-- Spatial Resolution with Map -->
        <div class="bg-gray-200 text-green-700 font-bold px-4 py-2 rounded-md inline-flex items-center justify-center inline-block text-sm flex-grow">
            {data.resolutionRaeumlich}
        </div>
    </div>

    <!-- Scenario and Format Chips -->
    <div class="flex space-x-4 w-full justify-between">
        <div class="bg-green-700 text-gray-100 font-bold px-4 py-2 inline-flex items-center justify-center rounded-md text-xs flex-grow">
            {data.szenario}
        </div>
        <div class="bg-white text-green-700 font-bold border border-green-700 px-4 py-2 inline-flex items-center justify-center rounded-md text-xs flex-grow">
            {data.format}
        </div>
        <!-- File Size -->
        <div class="bg-gray-200 text-green-700 font-bold px-4 py-2 inline-flex items-center justify-center rounded-md inline-block text-xs flex-grow">
            {data.dateigroesse}
        </div>
    </div>

    <div class="flex space-x-4 w-full justify-between">
        <!-- Regional Model Chip -->
        <div class="bg-green-700 text-gray-100 font-bold px-4 py-2 inline-flex items-center justify-center rounded-md inline-block text-xs flex-grow">
            {data.regionalmodell}
        </div>

        <!-- Global Model Chip -->
        <div class="bg-white text-green-700 font-bold border border-green-700 px-4 py-2 inline-flex items-center justify-center rounded-md inline-block text-xs flex-grow">
            {data.globalmodell}
        </div>
    </div>
</div>