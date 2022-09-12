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

    const res = await fetchFates(url, auth, fetch, true, true);

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
  import BotServerVotePage from '$lib/pages/BotServerVotePage.svelte';
  export let data: any;
</script>

<BotServerVotePage data={data} type="bot" />
