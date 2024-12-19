<script lang="ts">
    import { nodes, edges } from '$lib/store'; // Import the nodes and edges stores

    import { detailInfo } from '$lib/store';
    import { onDestroy } from 'svelte';

    let detailedData;
    const unsubscribe = detailInfo.subscribe((data) => {
        detailedData = data;
    });

    onDestroy(() => {
        unsubscribe();  // Clean up the subscription when the component is destroyed
    });

    export let title = "Detail View";   

    function copyData() {
        // Format data to copy, you can adjust this string based on what you need
        let dataToCopy = `
Parameter;${detailedData.parameter}
Unit;${detailedData.einheit}
Timespan;${detailedData.zeitspranne.map(t => `${t.start} - ${t.end}`).join(',')}
Regional Model;${detailedData.regionalmodell}
Global Model;${detailedData.globalmodell}
Format;${detailedData.format}
Scenario;${detailedData.szenario}
Temporal Res.;${detailedData.resolutionZeitlich}
Spatial Res.;${detailedData.resolutionRaeumlich}
Spatial Extent;${detailedData.spatialExtent.join(',')}
spatialExtent_orig;${detailedData.spatialExtent_orig}
File Size;${detailedData.dateigroesse}
Timestamp;${detailedData.timestamp}
Project;${detailedData.project}
Experiment;${detailedData.experiment}
Standard;${detailedData.standard}
Bias;${detailedData.bias}
Source;${detailedData.source}
Institution;${detailedData.institution}
Tracking ID;${detailedData.tracking_id}
Contact;${detailedData.contact}
Domain;${detailedData.domain}
DOI;${detailedData.doi}
Collection;${detailedData.collection}
`.trim();

        // Use Clipboard API to copy the string
        navigator.clipboard.writeText(dataToCopy)
            .then(() => {
                console.log('Data copied to clipboard');
                alert('Data copied to clipboard!');
            })
            .catch(err => {
                console.error('Failed to copy: ', err);
                alert('Failed to copy data. Please try again.');
            });
    }
</script>

<style>
    .sidebar {
        width: 440px;
        background: #ffffff;
        border-left: 1px solid #ddd;
        padding: 16px;
        overflow-y: auto;
        box-shadow: -2px 0 4px rgba(0, 0, 0, 0.1);
        color: #000;
        font-size: 16px;
        position: fixed; /* Fix the sidebar on the right */
        right: 0; /* Attach to the right edge */
        top: 0; /* Align it to the top */
        bottom: 0; /* Extend it to the bottom */
        z-index: 1000; /* Ensure it stays above other elements */
    }

    .sidebar h2 {
        font-size: 1.24rem;
        margin-bottom: 1rem;
    }

    .sidebar ul {
        list-style: none;
        padding: 0;
    }

    .sidebar li {
        margin-bottom: 0.4rem;
    }
</style>

<div class="sidebar">

    {#if detailedData}
        <h2>{title}</h2>
        <button
            on:click={copyData}
            class="absolute right-4 bg-gray-200 p-2 rounded-md shadow-md hover:bg-gray-200"
            title="Copy to Clipboard"
        >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-600 hover:text-gray-800" viewBox="0 0 20 20" fill="currentColor">
                <path d="M14 2H9a2 2 0 00-2 2v12a2 2 0 002 2h6a2 2 0 002-2V4a2 2 0 00-2-2zM9 4h6v12H9V4z" />
                <path d="M4 6a1 1 0 011-1h3a1 1 0 011 1v3a1 1 0 11-2 0V7H6v2a1 1 0 01-2 0V6z" />
            </svg>
        </button>

        <div class="triangle absolute left-1/2 -top-2 transform -translate-x-1/2"></div>
        
        <!-- Table layout with bigger column spacing -->
        <table class="w-full table-auto">
            <tbody>
                <tr>
                    <td class="pr-4 align-top"><strong>Parameter:</strong></td>
                    <td class="pl-4">{detailedData.parameter}</td>
                </tr>
                <tr>
                    <td class="pr-4 align-top"><strong>Unit:</strong></td>
                    <td class="pl-4">{detailedData.einheit}</td>
                </tr>
                <tr>
                    <td class="pr-4 align-top"><strong>Timespan:</strong></td>
                    <td class="pl-4">
                        {#each detailedData.zeitspranne as timespan}
                            <div>{timespan.start} - {timespan.end}</div>
                        {/each}
                    </td>
                </tr>
                <tr>
                    <td class="pr-4 align-top"><strong>Model (R):</strong></td>
                    <td class="pl-4">{detailedData.regionalmodell}</td>
                </tr>
                <tr>
                    <td class="pr-4 align-top"><strong>Model (G):</strong></td>
                    <td class="pl-4">{detailedData.globalmodell}</td>
                </tr>
                <tr>
                    <td class="pr-4 align-top"><strong>Format:</strong></td>
                    <td class="pl-4">{detailedData.format}</td>
                </tr>
                <tr>
                    <td class="pr-4 align-top"><strong>Scenario:</strong></td>
                    <td class="pl-4">{detailedData.szenario}</td>
                </tr>
                <tr>
                    <td class="pr-4 align-top"><strong>Temp Res:</strong></td>
                    <td class="pl-4">{detailedData.resolutionZeitlich}</td>
                </tr>
                <tr>
                    <td class="pr-4 align-top"><strong>Spat Res:</strong></td>
                    <td class="pl-4">{detailedData.resolutionRaeumlich}</td>
                </tr>
                <tr>
                    <td class="pr-4 align-top"><strong>Sp. Extent:</strong></td>
                    <td class="pl-4">{detailedData.spatialExtent.join(', ')}</td>
                </tr>
                <tr>
                    <td class="pr-4 align-top"><strong>Sp. Ext Or.:</strong></td>
                    <td class="pl-4">{detailedData.spatialExtent_orig.join(', ')}</td>
                </tr>
                <tr>
                    <td class="pr-4 align-top"><strong>File Size:</strong></td>
                    <td class="pl-4">{detailedData.dateigroesse}</td>
                </tr>
                <tr>
                    <td class="pr-4 align-top"><strong>Timestamp:</strong></td>
                    <td class="pl-4">{detailedData.timestamp}</td>
                </tr>
                <tr>
                    <td class="pr-4 align-top"><strong>Project:</strong></td>
                    <td class="pl-4">{detailedData.project}</td>
                </tr>
                <tr>
                    <td class="pr-4 align-top"><strong>Experiment:</strong></td>
                    <td class="pl-4">{detailedData.experiment}</td>
                </tr>
                <tr>
                    <td class="pr-4 align-top"><strong>Standard:</strong></td>
                    <td class="pl-4">{detailedData.standard}</td>
                </tr>
                <tr>
                    <td class="pr-4 align-top"><strong>Bias:</strong></td>
                    <td class="pl-4">{detailedData.bias}</td>
                </tr>
                <tr>
                    <td class="pr-4 align-top"><strong>Source:</strong></td>
                    <td class="pl-4">{detailedData.source}</td>
                </tr>
                <tr>
                    <td class="pr-4 align-top"><strong>Institution:</strong></td>
                    <td class="pl-4">{detailedData.institution}</td>
                </tr>
                <tr>
                    <td class="pr-4 align-top"><strong>Tracking ID:</strong></td>
                    <td class="pl-4">{detailedData.tracking_id}</td>
                </tr>
                <tr>
                    <td class="pr-4 align-top"><strong>Contact:</strong></td>
                    <td class="pl-4">{detailedData.contact}</td>
                </tr>
                <tr>
                    <td class="pr-4 align-top"><strong>Domain:</strong></td>
                    <td class="pl-4">{detailedData.domain}</td>
                </tr>
                <tr>
                    <td class="pr-4 align-top"><strong>DOI:</strong></td>
                    <td class="pl-4">{detailedData.doi}</td>
                </tr>
                <tr>
                    <td class="pr-4 align-top"><strong>Collection:</strong></td>
                    <td class="pl-4">{detailedData.collection}</td>
                </tr>
            </tbody>
        </table>
    {/if}

</div>

