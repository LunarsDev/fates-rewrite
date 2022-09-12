<script context="module" lang="ts">
  import { fetchFates } from '$lib/request';
  export const prerender = false;
  /** @type {import('@sveltejs/kit@next').Load} */
  export async function load({ params, fetch, session, stuff }) {
    const url = `/bots/${params.id}`;

    let auth = '';

    if (session.session.user) {
      auth = `${session.session.user.id}|${session.session.token}`;
    }

    const res = await fetchFates(url, auth, fetch, false, true);

    if (res.ok) {
      let data = await res.json();
      return {
        props: {
          data: data
        }
      };
    }

    return {
      status: res.status,
      error: new Error(`Bot Not Found`)
    };
  }
</script>

<script lang="ts">
  import BotServerPage from '$lib/pages/BotServerPage.svelte';
  import BotServerPageTabs from '$lib/pages/BotServerPageTabs.svelte';
  import { enums } from '$lib/enums/enums';
  export let data: any;
</script>

{#if data.page_style == enums.PageStyle.tabs}
  <BotServerPageTabs data={data} type="bot" />
{:else}
  <BotServerPage data={data} type="bot" />
{/if}
