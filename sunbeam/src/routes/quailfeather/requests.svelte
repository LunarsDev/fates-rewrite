<script lang="ts" context="module">
  import { lynxUrl } from '$lib/config';
  export const prerender = false;
  export async function load({ params, url, fetch, session, stuff }) {
    let res = await fetch(`${lynxUrl}/requests`);
    if (!res.ok) {
      let data = await res.json();
      return {
        status: res.status,
        error: new Error(`{JSON.stringify(data)}`)
      };
    }
    return {
      props: {
        data: await res.json()
      }
    };
  }
</script>

<script lang="ts">
  export let data: any;
</script>

{#each data as request}
  <p>
    {request.user_id} - {request.method} - {request.url} - {request.status_code} - {request.request_time}
  </p>
{/each}
