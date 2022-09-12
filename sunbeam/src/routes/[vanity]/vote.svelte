<script context="module" lang="ts">
  export const prerender = false;
  import { fetchFates } from '$lib/request';
  import * as logger from '$lib/logger';
  /** @type {import('@sveltejs/kit@next').Load} */
  export async function load({ params, fetch, session, stuff }) {
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

      const pageUrl = `/${type}s/${id}`;
      // Votes via site are not supported outside of bots anyways...
      const pageRes = await fetchFates(pageUrl, auth, fetch, true, true);
      if (pageRes.ok) {
        let pageData = await pageRes.json();
        logger.info('Vote', 'Vote page data is: ', pageData);
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
  import BotServerVotePage from '$lib/pages/BotServerVotePage.svelte';
  export let data: any;
  export let type: string;

  if (type == 'guild') {
    type = 'server';
  }
</script>

<BotServerVotePage data={data} type={type} />
