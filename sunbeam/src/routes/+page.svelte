<script lang="ts">
  import SearchBar from '$lib/base/SearchBar.svelte';
  import Tag from '$lib/base/Tag.svelte';
  import BotCard from '$lib/cards/BotCard.svelte';
  import CardContainer from '$lib/cards/CardContainer.svelte';
  import BristlefrostMeta from '$lib/base/BristlefrostMeta.svelte';
  import Section from '$lib/base/Section.svelte';
  import Intl from '$lib/base/Intl.svelte';
  import RandomCard from '$lib/base/RandomCard.svelte';
    import { enums } from '$lib/enums/enums';
  export let data: { index: any; random: any; meta: any };

  let searchData: any = null;
</script>

<BristlefrostMeta
  url="https://fateslist.xyz"
  title="Fates List | Discord Bot List"
  description="Find, invite and discover the best bots &amp; servers now on Fates List"
  thumbnail="https://fateslist.xyz/static/botlisticon.webp"
/>

<section>
  <h1 class="best-bots">Fates List</h1>
  <h2 class="best-bots"><Intl key="index.best_bots" /></h2>
</section>

<SearchBar bind:data={searchData} meta={data.meta} />

{#if !searchData}
  <Tag tags={data.meta.tags} />

  {#if data.random}
    <RandomCard type={enums.TargetType.Bot} randomBot={data.random} />
  {/if}

  <Section icon="fa-solid:certificate" title="Certified" id="certified-index">
    <CardContainer>
      {#each data.index.certified as bot}
        <BotCard data={bot} type={enums.TargetType.Bot} rand={false} />
      {/each}
    </CardContainer>
  </Section>

  <Section icon="fa-solid:sort-amount-up" title="Top Voted" id="top-voted-index">
    <CardContainer>
      {#each data.index.top_voted as bot}
        <BotCard data={bot} type={enums.TargetType.Bot} rand={false} />
      {/each}
    </CardContainer>
  </Section>

  <Section icon="fa-solid:plus" title="New Bots" id="new-bots">
    <CardContainer>
      {#each data.index.new as bot}
        <BotCard data={bot} type={enums.TargetType.Bot} rand={false} />
      {/each}
    </CardContainer>
  </Section>
{/if}

<style>
  h1 {
    font-size: 50px;
    margin: 0px;
  }

  h2 {
    font-size: 40px;
    margin: 0px;
    opacity: 0.6;
  }

  .best-bots {
    width: 90%;
  }

  section {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    flex: 1;
    overflow: hidden;
    margin-top: 35px;
  }
</style>
