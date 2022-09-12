<script context="module">
  /** @type {import('@sveltejs/kit').ErrorLoad} */
  export function load({ error, status }) {
    if (status == 408 || status == 502) {
      return {
        props: {
          title: 'Server Maintenance',
          message:
            "The Fates List API is currently under maintenance.<br/>Dont worry this won't take long!",
          serverMaint: true
        }
      };
    }
    return {
      props: {
        status: status,
        error: error.message,
        serverMaint: false
      }
    };
  }
</script>

<script>
  export let status;
  export let error;
  export let title = '';
  export let message = '';
  export let serverMaint = false;
  import { getIntlString } from '$lib/strings';
</script>

{#if serverMaint}
  <h1>{title}</h1>
  <h2>{@html message}</h2>
{:else}
  <h1 style="text-align: center">{status}</h1>
  <h2>{@html getIntlString(error)}</h2>

  <p>
    Please visit our <a href="https://fateslist.xyz/server/789934742128558080/invite"
      >support server</a
    > if you have any queries or concerns or just for fun!
  </p>
{/if}
