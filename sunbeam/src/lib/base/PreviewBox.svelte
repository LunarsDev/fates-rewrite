<script lang="ts">
  import SelectOption from '$lib/base/SelectOption.svelte';
  import { browser } from '$app/environment';
  import { api } from '$lib/config';

  import { debug, error } from '$lib/logger';
  import type { LongDescriptionType } from '$lib/enums/enums';
  import { onMount } from 'svelte';

  export let value = '<h3>Start typing to generate a preview!</h3>';

  export let textAreaVal = "Whoa there! The developer hasn't set a value for this yet!";

  export let longDescType: LongDescriptionType;

  export let label = 'Long Description';
  export let selectLabel = 'Long Description Type';

  debug('PreviewBox', longDescType);

  let wsUp = false;
  let previewWs: WebSocket = null;

  function setupWs() {
    if (!browser) {
      return;
    }

    if (previewWs) {
      // Kill the old one
      previewWs.close(1001);
    }

    previewWs = new WebSocket(
      `${api.replace('http://', 'ws://').replace('https://', 'wss://')}/ws/preview`
    );

    previewWs.onmessage = (e) => {
      console.log(e.data);
      if (e.data.startsWith('PONG:')) {
        return;
      }

      value = JSON.parse(e.data).text.replaceAll('long-description', 'preview-tab');
    };

    previewWs.onopen = () => {
      setInterval(() => {
        previewWs.send('PING');
      }, 20 * 1000);
    };

    previewWs.onclose = () => {
      error('Settings', 'PreviewWs closed');
      wsUp = false;
    };

    wsUp = true;
  }

  async function previewInput() {
    if (!browser) {
      return;
    }

    if (!wsUp) {
      setupWs();
    }
    if (previewWs.readyState != WebSocket.OPEN) {
      setTimeout(previewInput, 500);
      return;
    }
    previewWs.send(
      JSON.stringify({
        type: longDescType,
        content: textAreaVal
      })
    );
  }

  onMount(() => {
    previewInput();
  });

  function castToInputEl(el) {
    return el as HTMLInputElement;
  }
</script>

<label for="long_description_type">{selectLabel}</label>
<select
  on:change={(e) => {
    let el = castToInputEl(e.target);
    longDescType = parseInt(el.value);
  }}
  name="long_description_type"
  id="long_description_type"
>
  <SelectOption value="1" masterValue={`${longDescType}`}>Markdown (pulldown-cmark)</SelectOption>
  <SelectOption value="0" masterValue={`${longDescType}`}>HTML</SelectOption>
</select>

<label for="long_description">{label}</label>
<textarea
  on:input={(e) => {
    let el = castToInputEl(e.target);
    textAreaVal = el.value;
    previewInput();
  }}
  name="long_description"
  id="long_description"
  class="fform"
  bind:value={textAreaVal}
/>
