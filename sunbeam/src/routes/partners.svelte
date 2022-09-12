<script context="module" lang="ts">
  import { fetchFates } from '$lib/request';
  export const prerender = false;
  /** @type {import('@sveltejs/kit@next').Load} */
  export async function load({ params, fetch, stuff }) {
    const url = `/partners`;
    const res = await fetchFates(url, '', fetch, false, true);

    if (res.ok) {
      return {
        props: {
          partners: await res.json()
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
  import Partner from '$lib/base/Partner.svelte';
  import BristlefrostMeta from '$lib/base/BristlefrostMeta.svelte';
  export let partners: any;
</script>

<BristlefrostMeta
  url="https://fateslist.xyz/partners"
  title="Fates List | Our Partners"
  description="See our partners and supporters!"
  thumbnail="https://fateslist.xyz/static/botlisticon.webp"
/>

<div class="content">
  <h1>Our Partners</h1>

  <p>
    Note that Fates List is not responsible for any activities taking place on the below servers!
  </p>
</div>

{#each partners.partners as partner}
  <Partner partner={partner} icons={partners.icons} />
{/each}

<style>
  .content {
    width: 100%;
    max-width: var(--column-width);
    margin: var(--column-margin-top) auto 0 auto;
    padding: 3px;
  }
</style>
