<script context="module" lang="ts">
  import { fetchFates } from '$lib/request';
  export const prerender = false;
  /** @type {import('@sveltejs/kit@next').Load} */
  export async function load({ url, session, fetch }) {
    let tag = url.searchParams.get('tag');
    let targetType = url.searchParams.get('target_type');
    const searchUrl = `/search-tags?q=${tag}`;
    const res = await fetchFates(searchUrl, '', fetch, false, true);

    if (res.ok) {
      let data = await res.json();
      return {
        props: {
          data: data,
          targetType: targetType,
          tag: tag
        }
      };
    }

    return {
      status: res.status,
      error: new Error(`Tag Search Error`)
    };
  }
</script>

<script lang="ts">
  import CardContainer from '$lib/cards/CardContainer.svelte';
  import BotCard from '$lib/cards/BotCard.svelte';
  import SearchBar from '$lib/base/SearchBar.svelte';
  import Section from '$lib/base/Section.svelte';
  import Tag from '$lib/base/Tag.svelte';
  import BristlefrostMeta from '$lib/base/BristlefrostMeta.svelte';
  export let data: any;
  export let targetType: string;
  export let tag: string;
</script>

<BristlefrostMeta
  url="https://fateslist.xyz/frostpaw/search/tags?q={tag}&target_type={targetType}"
  title="Search results for {targetType}s tagged with {tag}"
  description="Find, invite and discover the best {tag} {targetType}s"
  thumbnail="https://fateslist.xyz/static/botlisticon.webp"
/>

<section>
  <h1>Fates List</h1>
  <h2 class="best-bots">Find the best bots for your servers!</h2>
</section>
<SearchBar type={targetType} query="" />

<Section title="Bots" icon="fa-solid:search" id="bots-res-tags">
  <Tag targetType={'bot'} tags={data.tags.bots} />
  <CardContainer>
    {#each data.bots as bot}
      <BotCard data={bot} type={'bot'} rand={false} />
    {/each}
  </CardContainer>
</Section>
<Section title="Servers" icon="fa-solid:search" id="servers-res-tags">
  <Tag targetType={'server'} tags={data.tags.servers} />
  <CardContainer>
    {#each data.servers as server}
      <BotCard data={server} type={'server'} rand={false} />
    {/each}
  </CardContainer>
</Section>

<style lang="scss">
  h1 {
    font-size: 50px;
    margin: 0px;
  }

  h2 {
    font-size: 40px;
    margin: 0px;
  }

  .best-bots {
    opacity: 0.6;
  }
  section {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    flex: 1;
    overflow: hidden;
  }
</style>
