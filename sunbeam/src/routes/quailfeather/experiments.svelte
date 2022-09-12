<script lang="ts" context="module">
  import { fetchFates } from '$lib/request';
  import { lynxUrl } from '$lib/config';
  export const prerender = false;
  export async function load({ params, url, fetch, session, stuff }) {
    let res = await fetchFates(`/${lynxUrl}/experiments`, '', fetch, false, true);
    if (res.ok) {
      return {
        props: {
          data: await res.json()
        }
      };
    } else {
      let data = await res.json();
      return {
        status: res.status,
        error: new Error(`{JSON.stringify(data)}`)
      };
    }
  }
</script>

<script lang="ts">
  export let data: any;
</script>

{JSON.stringify(data)}
