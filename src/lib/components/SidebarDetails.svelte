<script lang="ts">

    import { detailInfo } from '$lib/store';
    import { onDestroy } from 'svelte';

    let detailedData;
    const unsubscribe = detailInfo.subscribe((data) => {
        detailedData = data;
    });

    onDestroy(() => {
        unsubscribe();  // Clean up the subscription when the component is destroyed
    });

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

    function copyPersonData() {
        // Format data to copy, you can adjust this string based on what you need
        let dataToCopy = `
Person:;${detailedData.person}
ORCID;${detailedData.orcid}
Organisation;${detailedData.orga}
RORID;${detailedData.rorid}
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

    function copySoftwareData() {
        // Format data to copy, you can adjust this string based on what you need
        let dataToCopy = `
Software:;${detailedData.software}
Version;${detailedData.version}
License;${detailedData.license}
Source;${detailedData.source}
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
    .sidebar h2 {
        font-size: 1.24rem;
        margin-bottom: 1rem;
        margin-top: 1rem;
    }

    .table-container {
        display: grid;
        grid-template-columns: auto 2fr;
        gap: 6rem; /* Adjust this gap for more space between columns */
    }

    .table-container td {
        padding: 0.3rem; /* Uniform padding */
    }

    .table-container strong {
        font-weight: bold;
    }
</style>

<div class="sidebar">

    {#if detailedData?.parameter}
        <div class="relative"> <!-- Ensure relative positioning -->
            <button
                on:click={copyData}
                class="bg-gray-200 p-2 rounded-md shadow-md hover:bg-gray-200 mt-4"
                title="Copy to Clipboard"
            >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-600 hover:text-gray-800" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M14 2H9a2 2 0 00-2 2v12a2 2 0 002 2h6a2 2 0 002-2V4a2 2 0 00-2-2zM9 4h6v12H9V4z" />
                    <path d="M4 6a1 1 0 011-1h3a1 1 0 011 1v3a1 1 0 11-2 0V7H6v2a1 1 0 01-2 0V6z" />
                </svg>
            </button>
            <h2>{"Entity Details"}</h2>
            <div class="triangle absolute left-1/2 -top-2 transform -translate-x-1/2"></div>
            
            <div class="table-container">
                <!-- Table layout with bigger column spacing -->
                <table class="w-full">
                    <tbody>
                        <tr>
                            <td><strong>Parameter:</strong></td>
                            <td >{detailedData.parameter}</td>
                        </tr>
                        <tr>
                            <td ><strong>Unit:</strong></td>
                            <td >{detailedData.einheit}</td>
                        </tr>
                        <tr>
                            <td ><strong>Timespan:</strong></td>
                            <td >
                                {#each detailedData.zeitspranne as timespan}
                                    <div>{timespan.start} - {timespan.end}</div>
                                {/each}
                            </td>
                        </tr>
                        <tr>
                            <td ><strong>Model (R):</strong></td>
                            <td >{detailedData.regionalmodell}</td>
                        </tr>
                        <tr>
                            <td ><strong>Model (G):</strong></td>
                            <td >{detailedData.globalmodell}</td>
                        </tr>
                        <tr>
                            <td ><strong>Format:</strong></td>
                            <td >{detailedData.format}</td>
                        </tr>
                        <tr>
                            <td ><strong>Scenario:</strong></td>
                            <td >{detailedData.szenario}</td>
                        </tr>
                        <tr>
                            <td ><strong>Temp Res:</strong></td>
                            <td >{detailedData.resolutionZeitlich}</td>
                        </tr>
                        <tr>
                            <td ><strong>Spat Res:</strong></td>
                            <td >{detailedData.resolutionRaeumlich}</td>
                        </tr>
                        <tr>
                            <td ><strong>Sp. Extent:</strong></td>
                            <td >{detailedData.spatialExtent.join(', ')}</td>
                        </tr>
                        <tr>
                            <td ><strong>Sp. Ext Or.:</strong></td>
                            <td >{detailedData.spatialExtent_orig.join(', ')}</td>
                        </tr>
                        <tr>
                            <td ><strong>File Size:</strong></td>
                            <td >{detailedData.dateigroesse}</td>
                        </tr>
                        <tr>
                            <td ><strong>Timestamp:</strong></td>
                            <td >{detailedData.timestamp}</td>
                        </tr>
                        <tr>
                            <td ><strong>Project:</strong></td>
                            <td >{detailedData.project}</td>
                        </tr>
                        <tr>
                            <td ><strong>Experiment:</strong></td>
                            <td >{detailedData.experiment}</td>
                        </tr>
                        <tr>
                            <td ><strong>Standard:</strong></td>
                            <td >{detailedData.standard}</td>
                        </tr>
                        <tr>
                            <td ><strong>Bias:</strong></td>
                            <td >{detailedData.bias}</td>
                        </tr>
                        <tr>
                            <td ><strong>Source:</strong></td>
                            <td >{detailedData.source}</td>
                        </tr>
                        <tr>
                            <td ><strong>Institution:</strong></td>
                            <td >{detailedData.institution}</td>
                        </tr>
                        <tr>
                            <td ><strong>Tracking ID:</strong></td>
                            <td >{detailedData.tracking_id}</td>
                        </tr>
                        <tr>
                            <td ><strong>Contact:</strong></td>
                            <td >{detailedData.contact}</td>
                        </tr>
                        <tr>
                            <td ><strong>Domain:</strong></td>
                            <td >{detailedData.domain}</td>
                        </tr>
                        <tr>
                            <td ><strong>DOI:</strong></td>
                            <td >{detailedData.doi}</td>
                        </tr>
                        <tr>
                            <td ><strong>Collection:</strong></td>
                            <td >{detailedData.collection}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    {/if}

    {#if detailedData?.person}
        <div class="relative"> <!-- Ensure relative positioning -->
            
            <button
                on:click={copyPersonData}
                class="bg-gray-200 p-2 rounded-md shadow-md hover:bg-gray-200 mt-4"
                title="Copy to Clipboard"
            >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-600 hover:text-gray-800" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M14 2H9a2 2 0 00-2 2v12a2 2 0 002 2h6a2 2 0 002-2V4a2 2 0 00-2-2zM9 4h6v12H9V4z" />
                    <path d="M4 6a1 1 0 011-1h3a1 1 0 011 1v3a1 1 0 11-2 0V7H6v2a1 1 0 01-2 0V6z" />
                </svg>
            </button>
            <h2>{"Agent Details"}</h2>
            <div class="triangle absolute left-1/2 -top-2 transform -translate-x-1/2"></div>
            
            <div class="table-container">
                <!-- Table layout with adjusted column spacing -->
                <table class="w-full">
                    <tbody>
                        <tr>
                            <td ><strong>Person:</strong></td> 
                            <td >{detailedData.person}</td>
                        </tr>
                        <tr>
                            <td ><strong>ORCID:</strong></td>
                            <td >{detailedData.orcid}</td>
                        </tr>
                        <tr>
                            <td ><strong>Organisat.:</strong></td>
                            <td >{detailedData.orga}</td>
                        </tr>
                        <tr>
                            <td ><strong>RORID:</strong></td>
                            <td >{detailedData.rorid}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    {/if}


    {#if detailedData?.software}
        <div class="relative"> <!-- Ensure relative positioning -->
            
            <button
                on:click={copySoftwareData}
                class="bg-gray-200 p-2 rounded-md shadow-md hover:bg-gray-200 mt-4"
                title="Copy to Clipboard"
            >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-600 hover:text-gray-800" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M14 2H9a2 2 0 00-2 2v12a2 2 0 002 2h6a2 2 0 002-2V4a2 2 0 00-2-2zM9 4h6v12H9V4z" />
                    <path d="M4 6a1 1 0 011-1h3a1 1 0 011 1v3a1 1 0 11-2 0V7H6v2a1 1 0 01-2 0V6z" />
                </svg>
            </button>
            <h2>{"Software Details"}</h2>
            <div class="triangle absolute left-1/2 -top-2 transform -translate-x-1/2"></div>
            
            <div class="table-container">
                <!-- Table layout with adjusted column spacing -->
                <table class="w-full">
                    <tbody>
                        <tr>
                            <td ><strong>Software:</strong></td> 
                            <td >{detailedData.software}</td>
                        </tr>
                        <tr>
                            <td ><strong>Version:</strong></td>
                            <td >{detailedData.version}</td>
                        </tr>
                        <tr>
                            <td ><strong>License.:</strong></td>
                            <td >{detailedData.license}</td>
                        </tr>
                        <tr>
                            <td ><strong>Source:</strong></td>
                            <td >{detailedData.source}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    {/if}


</div>