<script lang="ts">
  import BotServerPage from '$lib/pages/BotServerPage.svelte';
  import BotServerPageTabs from '$lib/pages/BotServerPageTabs.svelte';
  import { enums } from '$lib/enums/enums';
  export let data: any;
</script>

{#if data.data.page_style == enums.PageStyle.tabs}
  <BotServerPageTabs data={data.data} type={data.type} />
{:else}
  <BotServerPage data={data.data} type={data.type} />
{/if}
