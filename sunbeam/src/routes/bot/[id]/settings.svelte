<script lang="ts" context="module">
  import { fetchFates } from '$lib/request';
  import { genError } from '$lib/strings';
  /** @type {import('@sveltejs/kit@next').Load} */
  export async function load({ params, fetch, session, stuff }) {
    if (!session.session.token) {
      return {
        props: {
          failed: true,
          data: {},
          context: {}
        }
      };
    }
    let url = `/users//${session.session.user.id}/bots/${params.id}/settings`;
    let res = await fetchFates(url, 'User ' + session.session.token, fetch, false, true);
    if (!res.ok) {
      let json = await res.json();
      return {
        status: res.status,
        error: new Error(genError(json))
      };
    }
    let json = await res.json();
    return {
      props: {
        failed: false,
        data: json.bot,
        context: json.context
      }
    };
  }
</script>

<script lang="ts">
  import { browser } from '$app/env';
  import BotSettings from '$lib/pages/BotSettings.svelte';
  import { loginUser } from '$lib/request';
  export let failed: boolean;
  export let data: any;
  export let context: any;
  if (failed) {
    if (browser) {
      loginUser(false);
    }
  }
</script>

{#if !failed}
  <BotSettings mode="edit" data={data} context={context} />
{:else}
  <p>Logging you in, please wait...</p>
{/if}
