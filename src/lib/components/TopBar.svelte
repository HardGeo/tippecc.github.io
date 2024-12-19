<script>
    export let activeView; // Receive the writable store

    const switchView = (view) => {
        activeView.set(view); // Update the store directly
        console.log("Switched to:", view);
    };
</script>

<div class="top-bar">
    <button class="top-bar-button" 
            on:click={() => switchView("View 1")}
            class:active={$activeView === "View 1"}>
        Minimal View
    </button>
    <button class="top-bar-button" 
            on:click={() => switchView("View 2")}
            class:active={$activeView === "View 2"}>
        Detail View
    </button>
    <button class="top-bar-button" 
            on:click={() => switchView("View 3")}
            class:active={$activeView === "View 3"}>
        Collection View
    </button>
</div>

<style>
    .top-bar {
        display: flex;
        justify-content: flex-start; /* Align items to the left */
        align-items: center; /* Vertically center items */
        background-color: #f8f9fa; /* Light gray background */
        padding: 10px;
        border-bottom: 2px solid #ddd; /* Optional bottom border */
        gap: 10px; /* Space between buttons */
        z-index: 10;
    }

    .top-bar-button {
        padding: 10px 20px;
        font-size: 16px;
        background-color: rgb(194, 194, 194);
        border: 1px solid #ccc;
        border-radius: 5px;
        cursor: pointer !important;;
        transition: background-color 0.2s, color 0.2s;
        color: black;
        pointer-events: auto;
        z-index: 20;
    }

    .top-bar-button:hover {
        background-color: #203c74;
        color: white;
        cursor: pointer !important;
    }

    .top-bar-button.active {
        background-color: #203c74 !important; /* Keep the active button blue */
        color: white;
    }
</style>
