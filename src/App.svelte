<script>
  import { onMount } from "svelte";
  let data;
  let idInput;
  let loading = false;
  let error = null;
  let selectedFormat = null;
  $: {
    let url = new URL(window.location.href);
    const params = {};
    if (data?.id) {
      params.v = data.id;
    }
    if (typeof selectedFormat == "number") {
      params.fmt = selectedFormat;
    }
    if (Object.keys(params).length) {
      url.search = new URLSearchParams(params).toString();
      history.pushState(null, null, url);
    }
  }
  $: embedLink = `${window.location.origin}/watch?v=${data?.id}&fmt=${selectedFormat}`;
  async function update(identifier) {
    console.log(identifier);
    loading = true;
    let returnedData = await fetch(`/api`, { method: "post", body: JSON.stringify({ identifier }), type: "application/json" }).then((r) => r.json());
    if (returnedData.status === "success") {
      selectedFormat = null;
      data = returnedData.data;
      error = null;
    } else {
      error = returnedData.error;
    }
    loading = false;
  }
  onMount(async (_) => {
    let searchParamIdenfier = new URLSearchParams(window.location.search).get("v");
    let searchParamFormat = new URLSearchParams(window.location.search).get("fmt");
    if (searchParamIdenfier) {
      update(searchParamIdenfier);
    }
    if (searchParamFormat) {
      selectedFormat = parseInt(searchParamFormat);
    }
  });
</script>

<main>
  <!-- <h1>youtube download tool</h1> -->
  <div class="horizPanel" style="margin-bottom: 16px;">
    {#if data}
      <h1>{data.id}</h1>
    {/if}
    <input
      type="text"
      placeholder="enter video id or link"
      bind:this={idInput}
      on:keypress={(e) => {
        if (e.key == "Enter") update(idInput.value);
      }}
    />
    <button on:click={(_) => update(idInput.value)}>Go</button>
    {#if loading}
      <p style="color: gold;">Loading...</p>
    {/if}
    {#if error}
      <p style="color: red;">{error}</p>
    {/if}
  </div>
  {#if data}
    <div class="horizPanel" style="gap: 32px;  flex-wrap: wrap;">
      <img src={data.thumbnails[data.thumbnails.length - 1].url} style="width: 35%;" alt="" />
      <div class="vertiPanel" style="gap: 8px; flex: 1;">
        <h2>{data.title}</h2>
        <p>by <a href={data.uploader_url}>{data.uploader}</a></p>
      </div>
    </div>
    <h2>Selected Format</h2>
    {#if typeof selectedFormat == "number"}
      <div class="horizPanel" style="width: 100%; gap: 32px;">
        <video src={data.formats[selectedFormat].url} style="width: 35%; background: #222;" alt="" controls />
        <div class="vertiPanel" style="gap: 12px; flex: 1;">
          <details>
            <summary style="font-size: 1.2em; font-weight: bold;">{data.formats[selectedFormat].format_note} ({data.formats[selectedFormat].ext}, fmt index {selectedFormat})</summary>
            <div class="vertiPanel" style="gap: 8px; padding: 8px">
              {#if data.formats[selectedFormat].vcodec !== "none"}
                <h4>Video</h4>
                <p>
                  {data.formats[selectedFormat].width}x{data.formats[selectedFormat].height} @ {data.formats[selectedFormat].fps}fps ({data.formats[selectedFormat].vcodec})
                </p>
              {/if}
              {#if data.formats[selectedFormat].acodec !== "none"}
                <h4>Audio</h4>
                <p>
                  {data.formats[selectedFormat].asr / 1000}khz @ {data.formats[selectedFormat].abr}kbps ({data.formats[selectedFormat].acodec})
                </p>
              {/if}
            </div>
          </details>
          <!-- <h4>Link</h4> -->
          <div class="horizPanel" style="gap: 8px;">
            <!-- <a href={data.formats[selectedFormat].url} class="button" target="_blank">View</a> -->
            <span>To download, press ⋮ &rarr; Download</span>
            <!-- <a href={data.formats[selectedFormat].url} class="button" download={data.title + "." + data.formats[selectedFormat].ext}>Download</a> -->
          </div>
          <h4>Embed</h4>
          <code>{'<video src="'}<a href={embedLink}>{embedLink}</a>{'"> </video>'}</code>
        </div>
      </div>
    {:else}
      <p>Select an available format below</p>
    {/if}
    <h2>Available Formats</h2>
    <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(min(200px, 100%), 1fr)); width: 100%; gap: 16px;">
      {#each data.formats as format, i}
        <div class={`card button ${selectedFormat === i && "card_selected"}`} style="user-select: none; cursor: pointer;" on:click={(_) => (selectedFormat = i)}>
          <div>
            <div class="vertiPanel" style="gap: 8px">
              <h3>{format.format_note} ({format.ext})</h3>
              {#if format.vcodec !== "none"}
                <h4>Video</h4>
                <p>
                  {format.width}x{format.height} @ {format.fps}fps ({format.vcodec})
                </p>
              {/if}
              {#if format.acodec !== "none"}
                <h4>Audio</h4>
                <p>
                  {format.asr / 1000}khz @ {format.abr}kbps ({format.acodec})
                </p>
              {/if}
            </div>
          </div>
          <!-- <div>
            <div class="horizPanel" style="gap: 8px;">
              <a href={format.url} class="button" target="_blank">View</a>
              <a href={format.url} class="button" download={data.title + "." + format.ext}>Download</a>
            </div>
          </div> -->
        </div>
      {/each}
    </div>
  {/if}
</main>

<style lang="scss">
  main {
    width: 100%;
    max-width: 900px;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
    > * {
      margin: 0;
    }
    > h2 {
      margin-top: 8px;
    }
  }
  .horizPanel {
    display: flex;
    gap: 16px;
    > * {
      margin: 0;
    }
    align-items: center;
  }
  .vertiPanel {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    gap: 16px;
    > * {
      margin: 0;
    }
  }
  .card {
    padding: 16px;
    border-radius: 8px;
    // background-color: #fff2;
    gap: 16px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    > * {
      display: flex;
      width: 100%;
    }
    > *:nth-child(1) {
      justify-content: flex-start;
    }
    > *:nth-child(2) {
      justify-content: flex-end;
    }
  }
  .card_selected {
    background-color: #fff;
    color: black;
  }
  img,
  video {
    border-radius: 6px;
  }
</style>
