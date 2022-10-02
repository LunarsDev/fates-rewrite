<script>
  import { loginUser } from '$lib/request';
  import { page } from '$app/stores';
  import { browser } from '$app/environment';

   if (!$page.data.token) {
    if (browser) {
      loginUser({
        allowBanned: true
      });
    }
  }
</script>

{#if $page.data.token}
  <p>{JSON.stringify($page.data.permissions)}</p>
{:else}
  <p>Logging you in, please wait...</p>
{/if}
