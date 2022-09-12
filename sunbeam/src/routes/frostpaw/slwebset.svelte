<script lang="ts" context="module">
  export const prerender = false;
  /** @type {import('@sveltejs/kit@next').Load} */
  export async function load({ session }) {
    return {
      props: {
        token: new URL(session.url).searchParams.get('token')
      }
    };
  }
</script>

<script lang="ts">
  import { browser } from '$app/env';

  import FormInput from '$lib/base/FormInput.svelte';
  import SelectOption from '$lib/base/SelectOption.svelte';
  import { apiUrl } from '$lib/config';
  import Button from '$lib/base/Button.svelte';
  import * as logger from '$lib/logger';

  export let token: string;

  async function setValue() {
    if (!token) {
      return;
    }
    let res = await fetch(`${apiUrl}/slwebset`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `${token}`
      },
      body: JSON.stringify({
        value: (document.querySelector('#value') as HTMLInputElement).value
      })
    });

    if (res.status == 200) {
      alert('Success!');
    } else {
      alert('Error!');
    }
  }

  let previewHtml = '<h3>Start typing to generate a preview!</h3>';

  let charsTyped = 0;

  let wsUp = false;
  let previewWs: WebSocket = null;

  function setupWs() {
    if (!browser) {
      return;
    }
    previewWs = new WebSocket('wss://api.fateslist.xyz/ws/_preview');
    previewWs.onmessage = (e) => {
      let json = JSON.parse(e.data);
      if (json.preview === undefined || !json.preview) return;
      previewHtml = json.preview.replaceAll('long-description', 'preview-tab');
    };

    previewWs.onopen = () => {
      setInterval(() => {
        previewWs.send('PING');
      }, 20 * 1000);
    };

    previewWs.onclose = () => {
      logger.info('Settings', 'PreviewWs closed');
      wsUp = false;
    };

    wsUp = true;
  }

  async function preview() {
    /* if(charsTyped % 4 == 0) {
        await previewInput()
    }
    charsTyped++ */
    previewInput();
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
        long_description_type: parseInt(
          (document.querySelector('#long_description_type') as HTMLInputElement).value
        ),
        text: (document.querySelector('#value') as HTMLInputElement).value
      })
    );
  }
</script>

<div id="slwebdiv">
  <h2>Web Field Setter</h2>
  {#if token}
    <p>Note that this url will expire in 15 minutes from when you ran <code>/webset</code>.</p>
  {/if}

  <label for="site-lang">Text Format</label>
  <select name="long_description_type" id="long_description_type">
    <SelectOption value="1" masterValue={'1'}>Markdown (pulldown-cmark)</SelectOption>
    <SelectOption value="0" masterValue={'1'}>HTML</SelectOption>
  </select>

  <FormInput
    name="Value"
    required={true}
    id="value"
    type="text"
    textarea={true}
    placeholder={'Enter a value'}
    oninput={() => preview()}
  />

  <div id="preview-tab" class="prose prose-zinc dark:prose-invert">
    {@html previewHtml}
  </div>

  {#if !token}
    <p>
      You will not be able to update anything as there is no token however you can still use this
      interface to preview your descriptions
    </p>
  {:else}
    <Button onclick={() => setValue()}>Set Value</Button>
  {/if}
</div>

<style>
  #slwebdiv {
    margin-left: 30px;
  }
</style>
