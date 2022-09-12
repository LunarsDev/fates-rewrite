<script lang="ts">
  import { browser } from '$app/env';

  import FormInput from '$lib/base/FormInput.svelte';
  import Button from '$lib/base/Button.svelte';

  let saveTxt = 'fetch';

  let appURL = '';

  let appData;

  async function getAppFromJSON(url: string) {
    let response = await fetch(url);
    let data = await response.json();
    return await getApplication(data);
  }

  async function getApplication(data: any) {
    appData = data;
  }

  function getAppEl(): HTMLInputElement {
    return document.querySelector('#app-url');
  }

  function getAppJsonEl(): HTMLInputElement {
    return document.querySelector('#app-json');
  }
</script>

<h1>Qibli Staff App Viewer</h1>
<div class="staff-app">
  <FormInput
    id="app-url"
    data={appURL}
    required={true}
    name="Application Qibli Data URL"
    placeholder="Enter the URL for qibli data"
  />
</div>
<div class="center">
  <Button
    href={'#'}
    onclick={() => {
      let url = getAppEl().value;
      getAppFromJSON('https://fateslist.xyz/frostpaw/qibli-fetch?url=' + url);
    }}
    class="button"
    id="post-app-btn"
    touch
    >{saveTxt}</Button
  >
</div>
<div class="staff-app">
  <FormInput
    id="app-json"
    data={''}
    required={true}
    name="Fallback: Paste JSON here"
    placeholder="Enter the staff application json"
    textarea={true}
  />
</div>
<div class="center">
  <Button
    href={'#'}
    onclick={() => {
      let data = getAppJsonEl().value;
      getApplication(JSON.parse(data));
    }}
    class="button"
    id="post-app-btn"
    touch
    >{saveTxt}</Button
  >
</div>
{#if appData}
  <h2>App Format: {appData.app_version}</h2>
  <h2>User</h2>
  <img
    class="user-avatar"
    src="https://cdn.discordapp.com/avatars/{appData.user.id}/{appData.user.avatar}.png"
    alt="user avatar"
    on:error={function () {
      this.src = 'https://api.fateslist.xyz/static/botlisticon.webp';
    }}
  />
  <h3>{appData.user.username}<span class="disc">#{appData.user.discriminator}</span></h3>
  <h4>User ID: {appData.user.id}</h4>
  <h2>Application</h2>
  {#each appData.questions as pane}
    <h3>{pane.title}</h3>
    {#each pane.questions as question}
      <h3>{question.title}</h3>
      <h4>Question: <span class="disc">{question.question}</span></h4>
      <h4>Answer: <span class="disc">{appData.app[question.id]}</span></h4>
    {/each}
  {/each}
{/if}

<style lang="scss">
  .user-avatar {
    border-radius: 50%;
    width: 50px;
  }

  .disc {
    opacity: 0.7;
  }

  h1 {
    text-align: center;
  }
  .staff-app {
    width: 80%;
    margin-left: auto;
    margin-right: auto;
  }

  :global(.button) {
    opacity: 1 !important;
    border: solid thin !important;
  }

  .center {
    text-align: center;
  }
</style>
