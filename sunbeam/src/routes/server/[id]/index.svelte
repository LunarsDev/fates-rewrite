<script context="module" lang="ts">
  import { fetchFates } from '$lib/request';
  export const prerender = false;
  /** @type {import('@sveltejs/kit@next').Load} */
  export async function load({ params, fetch, session, stuff }) {
    const url = `/servers/${params.id}`;
    const res = await fetchFates(url, '', fetch, false, true);

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
      error: new Error(`Server Not Found`)
    };
  }
</script>

<script lang="ts">
  import BotServerPage from '$lib/pages/BotServerPage.svelte';
  export let data: any;
</script>

<BotServerPage data={data} type="server" />
