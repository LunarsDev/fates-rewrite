<script lang="ts">
  import BotServerPage from '$lib/pages/BotServerPage.svelte';
  import BotServerPageTabs from '$lib/pages/BotServerPageTabs.svelte';
  import { enums } from '$lib/enums/enums';
  export let data: any;
</script>

{#if data.bot.page_style == enums.PageStyle.tabs}
  <BotServerPageTabs data={data.bot} type={enums.TargetType.Bot} />
{:else}
  <BotServerPage data={data.bot} type={enums.TargetType.Bot} />
{/if}
