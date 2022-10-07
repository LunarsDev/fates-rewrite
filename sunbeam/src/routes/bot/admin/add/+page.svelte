<script lang="ts">
  import { browser } from '$app/environment';
  import type { Option } from 'svelte-multiselect';
  import { getMsOptions, loginUser, request } from '$lib/request';
  import { page } from '$app/stores';
  import MultiSelectInput from '$lib/base/MultiSelectInput.svelte';
  import Tip from '$lib/base/Tip.svelte';
  import Button from '$lib/base/Button.svelte';
  import { api } from '$lib/config';
  import { genError } from '$lib/strings';
  import Icon from '@iconify/svelte';
  export let data: any;

  if (!$page.data.token) {
    if (browser) {
      loginUser();
    }
  }

  console.log(data);

  let tagOptions: Option[] = getMsOptions(data.bot.tags);
  let featureOptions: Option[] = getMsOptions(data.bot.features);

  let selectedTags: Option[] = [];
  let selectedFeatures: Option[] = [];

  let botId: string;
  let clientId: string;

  let verifyData: any;

  let verifyTicket: string;

  let verifiedBotClientSide: boolean;

  let nextButtonText = 'Next';

  // Verify that Bot ID and Client ID are set correctly (which is typically a huge cause of concern and pain)
  async function verifyBot() {
    if (!clientId) {
      return;
    }

    nextButtonText = 'Verifying...';

    let res = await request(`${api}/bots/add/verify-client-id?client_id=${clientId}`, {
      method: 'POST',
      fetch: fetch,
      session: $page.data,
      endpointType: 'user',
      auth: true
    });

    let json = await res.json();

    if (res.ok) {
      nextButtonText = 'Reverify';
      botId = json.bot_id;
      verifyTicket = json.ticket;
      verifyData = json.data;
      verifiedBotClientSide = true;
    } else {
      nextButtonText = 'Next';
      verifiedBotClientSide = false;
      verifyTicket = null;
      botId = null;
      alert(genError(json));
    }
  }
</script>

{#if $page.data.token}
  <div class="page">
    <h1>Welcome To Fates List</h1>
    <Tip>
      To make this a bit simpler for newcomers, only the basic settings needed for adding your bot
      are shown here. Once you've added your bot, you can edit it to your hearts content in <em
        >Bot Settings</em
      >!<br /><br />

      Older bots have differing Client ID and Bot ID's. Make sure you are typing the Client ID and
      *not* the Bot ID (which we'll fetch for you anyways).
    </Tip>
    <label for="client-id">Client ID</label>
    <input
      id="client-id"
      name="client-id"
      class="fform"
      bind:value={clientId}
      placeholder="Client ID (older bots have differing Bot ID and Client ID)"
      type="text"
    />
    <Button onclick={() => verifyBot()}
      >{nextButtonText}
      {#if verifiedBotClientSide}<Icon
          class="white tag-icon"
          icon="mdi:check"
          inline={false}
          aria-hidden="true"
        />{/if}</Button
    >
    <div class="spacer" />
    {#if verifiedBotClientSide}
      <h3>Great! Next let's get some basic information about {verifyData.data.bot.username}</h3>

      <MultiSelectInput title="Tags" id="tags" options={tagOptions} bind:selected={selectedTags} />
      <MultiSelectInput
        title="Features"
        id="features"
        options={featureOptions}
        bind:selected={selectedFeatures}
      />
    {/if}
  </div>
{:else}
  <p>Logging you in, please wait...</p>
{/if}

<style>
  .page {
    color: white !important;
    overflow: visible !important;
    min-height: 700px !important;
    max-width: 90% !important;
    margin: 0 auto !important;
  }

  .spacer {
    margin-bottom: 15px;
  }
</style>
