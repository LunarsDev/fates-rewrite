<script>
  import { getIntlString } from '$lib/strings';
  import { page } from "$app/stores";

  if(!$page.error) {
    $page.error = {
      message: "Not Found"
    };
  }
</script>

{#if $page.status == 400 || $page.status == 502}
  <h1>Server Maintenance</h1>
  <h2>The Fates List API is currently under maintenance.<br/>Dont worry this won't take long!</h2>
{:else}
  <h1 style="text-align: center">{$page.status}</h1>
  <h2>{@html getIntlString($page.error.message)}</h2>

  <p>
    Please visit our <a href="https://fateslist.xyz/server/789934742128558080/invite"
      >support server</a
    > if you have any queries or concerns or just for fun!
  </p>
{/if}
