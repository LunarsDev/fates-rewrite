<script context="module" lang="ts">
  import { fetchFates } from '$lib/request';
  export const prerender = false;
  /** @type {import('@sveltejs/kit@next').Load} */
  export async function load({ url, session, fetch }) {
    let search = {
      query: url.searchParams.get('q'),
      targetType: url.searchParams.get('f'), // f stands for first display
      gc_from: parseInt(url.searchParams.get('gcf')) || 0,
      gc_to: parseInt(url.searchParams.get('gct')) || -1
    };

    const res = await fetchFates(
      `/search?q=${search.query}&gc_from=${search.gc_from}&gc_to=${search.gc_to}`,
      '',
      fetch,
      false,
      true
    );

    if (res.ok) {
      let data = await res.json();
      return {
        props: {
          data: data,
          targetType: search.targetType,
          query: search.query,
          gc_from: search.gc_from,
          gc_to: search.gc_to
        }
      };
    }

    return {
      status: res.status,
      error: new Error(`Search Error`)
    };
  }
</script>

<script lang="ts">
  import SearchBar from '$lib/base/SearchBar.svelte';
  import BristlefrostMeta from '$lib/base/BristlefrostMeta.svelte';
  import Intl from '$lib/base/Intl.svelte';
  export let data: any;
  export let targetType: string;
  export let query: string;
  export let gc_from: number;
  export let gc_to: number;
</script>

<BristlefrostMeta
  url="https://fateslist.xyz/frostpaw/search?q={query}"
  title="Search results matching {query}!"
  description="Find, invite and discover the best bots and servers matching {query}"
  thumbnail="https://fateslist.xyz/static/botlisticon.webp"
/>

<section>
  <h1 class="best-bots">Fates List</h1>
  <h2 class="best-bots"><Intl key="index.search" /></h2>
</section>

<SearchBar type={targetType} query={query} gc_from={gc_from} gc_to={gc_to} data={data} />

<style lang="scss">
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
