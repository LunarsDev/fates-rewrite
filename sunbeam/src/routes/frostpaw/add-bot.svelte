<script lang="ts" context="module">
  export const prerender = false;
  /** @type {import('@sveltejs/kit@next').Load} */
  export async function load({ params, fetch, session, stuff }) {
    if (!session.session.token) {
      return {
        props: {
          data: {},
          context: {}
        }
      };
    }
    let tagsRes = await fetch('/meta', {
      headers: {
        origin: origin,
      }
    });
    if (!tagsRes.ok) {
      return {
        status: tagsRes.status,
        error: new Error('Could not fetch tags and features')
      };
    }
    let data = await tagsRes.json();
    return {
      props: {
        data: { tags: [], features: [] },
        context: data
      }
    };
  }
</script>

<script lang="ts">
  import { browser } from '$app/environment';
  import BotSettings from '$lib/pages/BotSettings.svelte';
  import { loginUser } from '$lib/request';
  import { page } from '$app/stores';
  import { apiUrl } from '$lib/config';
  export let context: any;
  export let data: any;
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
      loginUser(false);
    }
  }
</script>

{#if $page.data.token}
  <BotSettings mode="add" data={data} context={context} />
{:else}
  <p>Logging you in, please wait...</p>
{/if}
