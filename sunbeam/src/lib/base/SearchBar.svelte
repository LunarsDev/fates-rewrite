<script lang="ts">
import { browser } from '$app/environment';

import { apiUrl } from '$lib/config';
    import { request } from '$lib/request';
    import { page } from '$app/stores';

  import FormInput from './FormInput.svelte';
import SearchRes from './SearchRes.svelte';
  import Tip from './Tip.svelte';
    import { onMount } from 'svelte';

  let type: string;
  let query: string;
  let gc_from = 1;
  let gc_to = -1;
  export let data: any = null;

  onMount(() => {
    if (browser) {
      let url = new URL(window.location.href);

      type = url.searchParams.get('t') || 'bot';
      query = url.searchParams.get('q') || '';
      gc_from = parseInt(url.searchParams.get('gcf') || '1');
      gc_to = parseInt(url.searchParams.get('gct') || '-1');

      if(query) {
        searchBot()
      }
    }
  })

  let searching = false;

  function keyHandle(event) {
    event.preventDefault();
    if (event.keyCode === 13) {
      let form = document.querySelector('#search') as HTMLFormElement;
      form.submit();
    }
  }

  async function searchBot() {
    if(!query) {
      data = null
      let url = new URL(window.location.href);
      url.searchParams.delete('q');
      url.searchParams.delete('t');
      url.searchParams.delete('gcf');
      url.searchParams.delete('gct');
      window.history.replaceState({}, '', url.href);
      setTimeout(() => window.llhandler(), 300)
      return
    }; // Don't search if query is empty

    // update location silently to include new query params
    let url = new URL(window.location.href);
    url.searchParams.set('q', query);
    url.searchParams.set('t', type);
    url.searchParams.set('gcf', gc_from.toString());
    url.searchParams.set('gct', gc_to.toString());
    window.history.replaceState({}, '', url.href);

    searching = true;
    let res = await request(`${apiUrl}/search?q=${query}&gc_from=${gc_from}&gc_to=${gc_to}`, {
      method: 'GET',
      endpointType: 'user',
      auth: false,
      session: $page.data,
      fetch: fetch,
    });

    data = await res.json();
    searching = false
    setTimeout(() => window.llhandler(), 300)
  }

  function castToEl(a: any): HTMLInputElement {
    return a;
  }
</script>

<p>{#if searching}Searching...{:else}&nbsp{/if}</p>

<div class="search">
  <input
    type="text"
    on:input={(event) => {
      query = castToEl(event.target).value
      searchBot()
    }}
    id="search-bar"
    class="form-control fform search"
    placeholder="Search for {type}s (ENTER to search)"
    name="q"
    value={query}
    aria-label="Search for something.."
    style="width: 90%"
  />
  <details class="filters">
    <summary>Advanced Search Options</summary>
    <h3>Server Count Filter</h3>
    <FormInput
      formclass="filter-inp filter-inp-left"
      oninput={(event) => {
        gc_from = parseInt(castToEl(event.target).value) || -1
        searchBot()
      }}
      id="gcf"
      name="From:"
      placeholder="From..."
      type="number"
      data={gc_from}
    />
    <FormInput
      formclass="filter-inp filter-inp-right"
      oninput={(event) => {
        gc_to = parseInt(castToEl(event.target).value) || -1
        searchBot()
      }}
      id="gct"
      name="To:"
      placeholder="To... (-1 means no limit)"
      type="number"
      data={gc_to}
    />

    <h3>Display Order</h3>
    <Tip>
      First display is either 'bot', 'server', 'pack' or 'profile' and chooses whether you want
      bots first or servers first!
    </Tip>
    <FormInput
      onkeyup={keyHandle}
      id="f"
      name="First Display"
      data={type}
      placeholder="First display, see tip"
    />
  </details>
</div>

{#if data}
  <SearchRes targetType={type} data={data} />
{/if}

<style lang="scss">
  .search {
    display: block;
    padding: 12px !important;
    margin-top: 15px;
  }

  .filters {
    max-width: 94%;
    margin: 0 auto;
    color: white;
  }

  :global(.filter-inp) {
    min-width: 45% !important;
    max-width: 45% !important;
    display: inline-block !important;
    white-space: nowrap;
    overflow-x: nowrap;
  }

  @media only screen and (min-width: 763px) {
    :global(.filter-inp-left) {
      margin-right: 65px;
    }
  }
  @media only screen and (max-width: 763px) {
    :global(.filter-inp-left) {
      margin-right: 20px;
    }
  }
</style>