<script context="module" lang="ts">
  import { fetchFates } from '$lib/request';
  import { roll } from '$lib/request';
  export const prerender = false;
  /** @type {import('@sveltejs/kit@next').Load} */
  export async function load({ params, fetch, stuff }) {
    const url = `/index?target_type=0`;
    const res = await fetchFates(url, '', fetch, false, true);

    let data = await res.json();

    if (res.ok) {
      return {
        props: {
          data: data,
          randomBot: data.random
        }
      };
    }

    return {
      status: res.status,
      error: new Error(`Could not load ${url}`)
    };
  }
</script>

<script lang="ts">
  import SearchBar from '$lib/base/SearchBar.svelte';
  import Tag from '$lib/base/Tag.svelte';
  import BotCard from '$lib/cards/BotCard.svelte';
  import CardContainer from '$lib/cards/CardContainer.svelte';
  import type { BotIndex } from '$lib/apiTypes';
  import RandomBot from '$lib/base/RandomBot.svelte';
  import BristlefrostMeta from '$lib/base/BristlefrostMeta.svelte';
  import Section from '$lib/base/Section.svelte';
  import Intl from '$lib/base/Intl.svelte';
  export let data: BotIndex;
  export let randomBot: any;
  //
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

<SearchBar type="bot" query="" />
<Tag targetType="bot" tags={data.tags} />
<RandomBot type="bot" randomBot={randomBot} />

<Section icon="fa-solid:certificate" title="Certified" id="certified-index">
  <CardContainer>
    {#each data.certified as bot}
      <BotCard data={bot} type="bot" rand={false} />
    {/each}
  </CardContainer>
</Section>

<Section icon="fa-solid:sort-amount-up" title="Top Voted" id="top-voted-index">
  <CardContainer>
    {#each data.top_voted as bot}
      <BotCard data={bot} type="bot" rand={false} />
    {/each}
  </CardContainer>
</Section>

<Section icon="fa-solid:plus" title="New Bots" id="new-bots">
  <CardContainer>
    {#each data.new as bot}
      <BotCard data={bot} type="bot" rand={false} />
    {/each}
  </CardContainer>
</Section>

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
