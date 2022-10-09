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
  import { enums, type ListMeta } from '$lib/enums/enums';
  import RedStar from '$lib/base/RedStar.svelte';
  import PreviewBox from '$lib/base/PreviewBox.svelte';
  export let data: ListMeta;

  if (!$page.data.token) {
    if (browser) {
      loginUser();
    }
  }

  console.log(data);

  let tagOptions: Option[] = getMsOptions(data.bot.tags);
  let featureOptions: Option[] = getMsOptions(data.bot.features);

  let selectedTags = [];
  let selectedFeatures = [];

  let botId: string;
  let clientId: string;
  let prefix: string;
  let description: string;
  let vanity: string;
  let invite: string;

  // Internal vars
  let verifyData;
  let verifyTicket: string;
  let verifiedBotClientSide: boolean;
  let nextButtonText = 'Next';

  async function finalizeBot() {
    let res = await request(`${api}/bots/add/finalize`, {
      method: 'POST',
      fetch: fetch,
      session: $page.data,
      endpointType: 'user',
      auth: true,
      json: {
        tags: selectedTags.map((t) => t.value),
        features: selectedFeatures.map((t) => t.value),
        ticket: verifyTicket,
        prefix: prefix,
        invite: invite,
        vanity: vanity,
        description: description,
        long_description_type: longDescType,
        long_description: longDesc
      }
    });

    if (res.ok) {
      alert({
        title: 'Success',
        message:
          'Your bot has been added to the list! You can set more information such as extra owners and webhook information in Bot Settings now!',
        type: enums.AlertType.Success,
        close: () => {
          window.location.href = '/bots/' + botId + '/settings';
        }
      });
    } else {
      let json = await res.json();
      alert(genError(json));
    }
  }

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

  let previewHtml = '';
  let longDescType = enums.LongDescriptionType.Markdown;
  let longDesc = '';
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
      <label for="bot-prefix">Bot Prefix</label>
      <input
        id="bot-prefix"
        name="bot-prefix"
        class="fform"
        bind:value={prefix}
        placeholder="Bot Prefix. Leave blank for 'slash command' bots."
        type="text"
      />
      <label for="bot-vanity">Vanity <RedStar /></label>
      <input
        id="bot-vanity"
        name="bot-vanity"
        class="fform"
        bind:value={vanity}
        placeholder="mybot, fateslist etc. Prefix with _ to disable"
        type="text"
      />
      <Tip>
        Custom Invite Links are supported<br /><br />

        Support for P:PERM_NUMBER was removed. You can use the URL generator in Discord Developer
        Portal instead.<br /><br />
      </Tip>
      <label for="invite">Bot Invite</label>
      <input
        name="invite"
        id="invite"
        class="fform"
        placeholder="https://..."
        bind:value={invite}
      />
      <label for="bot-description">Description <RedStar /></label>
      <input
        id="bot-description"
        name="bot-description"
        class="fform"
        bind:value={description}
        placeholder="Bot Description"
        type="text"
      />
      <PreviewBox bind:textAreaVal={longDesc} bind:longDescType bind:value={previewHtml} />

      <div id="preview-tab" class="prose prose-zinc dark:prose-invert">
        {#if !previewHtml}
          <h3>Start typing to generate a preview!</h3>
        {:else}
          {@html previewHtml}
        {/if}
      </div>

      <div class="spacer" />

      <Button onclick={() => finalizeBot()}>Lets Go!</Button>
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
