<script lang="ts">
  import { browser } from '$app/environment';
  import BotSettings from '$lib/pages/BotSettings.svelte';
  import { loginUser } from '$lib/request';
  import { page } from '$app/stores';
  export let data: any;

  if (browser && !$page.data.token) {
    loginUser();
  }
</script>

{#if $page.data.token}
  <BotSettings mode="edit" data={data.bot} context={data.meta} />
{:else}
  <p>Logging you in, please wait...</p>
{/if}
