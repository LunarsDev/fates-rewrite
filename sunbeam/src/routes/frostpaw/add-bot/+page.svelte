<script lang="ts">
  import { browser } from '$app/environment';
  import BotSettings from '$lib/pages/BotSettings.svelte';
  import { loginUser } from '$lib/request';
  import { page } from '$app/stores';
  import { apiUrl } from '$lib/config';
  export let data: any;

  let context = data.context;
  data = data.data;

  let user = {
    username: 'Fates List',
    avatar: `${apiUrl}/static/botlisticon.webp`
  };
  data.user = user;

  // Set needed fields
  data.flags = [];
  data.owners = [];

  if (!$page.data.token) {
    if (browser) {
      loginUser();
    }
  }
</script>

{#if $page.data.token}
  <BotSettings mode="add" data={data} context={context} />
{:else}
  <p>Logging you in, please wait...</p>
{/if}
