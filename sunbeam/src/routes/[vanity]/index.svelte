<script context="module" lang="ts">
  export const prerender = false;
  import { fetchFates } from '$lib/request';
  import * as logger from '$lib/logger';
  /** @type {import('@sveltejs/kit@next').Load} */
  export async function load({ params, fetch, session, stuff }) {
    if (params.vanity == 'servers') {
      return {
        status: 307,
        redirect: '/frostpaw/servers/'
      };
    }

    let auth = '';

    if (session.session.user) {
      auth = `${session.session.user.id}|${session.session.token}`;
    }

    const url = `/code/${params.vanity}`;
    const res = await fetchFates(url, auth, fetch, false, true);

    if (res.ok) {
      let data = await res.json();
      let id: string = data.target_id;
      let type: string = data.target_type;

      let useNextApi = false;

      if (type == 'bot') {
        useNextApi = true;
      }

      const pageUrl = `/${type}s/${id}`;
      const pageRes = await fetchFates(pageUrl, auth, fetch, false, useNextApi);
      if (pageRes.ok) {
        let pageData = await pageRes.json();
        logger.info('Index', 'Index page data is: ', pageData);
        return {
          props: {
            data: pageData,
            type: type
          }
        };
      }

      return {
        status: res.status,
        error: new Error(`Invalid Vanity`)
      };
    }

    return {
      status: res.status,
      error: new Error(`Invalid Vanity`)
    };
  }
</script>

<script lang="ts">
  import BotServerPage from '$lib/pages/BotServerPage.svelte';
  import BotServerPageTabs from '$lib/pages/BotServerPageTabs.svelte';
  import { enums } from '$lib/enums/enums';
  export let data: any;
  export let type: string;

  if (type == 'guild') {
    type = 'server';
  }
</script>

{#if data.page_style == enums.PageStyle.tabs}
  <BotServerPageTabs data={data} type={type} />
{:else}
  <BotServerPage data={data} type={type} />
{/if}
