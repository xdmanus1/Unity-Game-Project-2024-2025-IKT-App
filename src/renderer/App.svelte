<script>
  import { onMount } from "svelte";
  import { db, storage } from "../firebase.js";
  import { collection, getDocs } from "firebase/firestore";
  import { ref, getBytes } from "firebase/storage";

  let versions = [];
  let error = null;
  let downloadStatus = "";

  onMount(async () => {
    try {
      const querySnapshot = await getDocs(collection(db, "versions"));
      versions = querySnapshot.docs.map((doc) => ({
        number: doc.data().number,
        fileName: doc.data().fileName, // Assume each version document has a fileName field
      }));
    } catch (e) {
      error = e.message;
      console.error("Error fetching versions:", e);
    }

    window.electronAPI.onSaveFileComplete((event, { path }) => {
      downloadStatus = `Download complete. File saved at: ${path}`;
      runFile(path);
    });

    window.electronAPI.onSaveFileError((event, errorMessage) => {
      error = `Save file error: ${errorMessage}`;
    });

    window.electronAPI.onRunFileComplete(() => {
      downloadStatus = "File executed successfully!";
    });

    window.electronAPI.onRunFileError((event, errorMessage) => {
      error = `Error running file: ${errorMessage}`;
    });
  });

  async function downloadAndRunFile(version) {
    try {
      downloadStatus = "Downloading...";
      const fileRef = ref(storage, version.fileName);
      const buffer = await getBytes(fileRef);
      window.electronAPI.saveFile(buffer, version.fileName);
    } catch (e) {
      error = `Download error: ${e.message}`;
    }
  }

  function runFile(filePath) {
    window.electronAPI.runFile(filePath);
  }
</script>

<main>
  <h1>Unity Game Launcher</h1>

  {#if error}
    <p class="error">Error: {error}</p>
  {:else if versions.length === 0}
    <p>Loading versions...</p>
  {:else}
    <ul>
      {#each versions as version}
        <li>
          Version {version.number}
          <button on:click={() => downloadAndRunFile(version)}
            >Download & Run</button
          >
        </li>
      {/each}
    </ul>
  {/if}

  {#if downloadStatus}
    <p>{downloadStatus}</p>
  {/if}
</main>

<style>
  /* Styles remain the same */
</style>
