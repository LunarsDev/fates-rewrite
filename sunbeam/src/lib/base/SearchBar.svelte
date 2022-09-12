<script lang="ts">
import { browser } from '$app/env';

import { goto } from '$app/navigation';

import { apiUrl } from '$lib/config';

  import FormInput from './FormInput.svelte';
import SearchRes from './SearchRes.svelte';
  import Tip from './Tip.svelte';

  export let type: string;
  export let query: string;
  export let gc_from = 1;
  export let gc_to = -1;
  export let data: any = null;

  let searching = false;

  function keyHandle(event) {
    event.preventDefault();
    if (event.keyCode === 13) {
      let form = document.querySelector('#search') as HTMLFormElement;
      form.submit();
    }
  }

  async function searchBot() {
    if(window.location.pathname != "/frostpaw/search") {
      goto(`/frostpaw/search?f=${type}&q=${query}&gcf=${gc_from}&gct=${gc_to}#focus`);
      return;
    }
    searching = true;
    let res = await fetch(`${apiUrl}/search?q=${query}&gc_from=${gc_from}&gc_to=${gc_to}`);
    data = await res.json();
    // update location silently to include new query params
    let url = new URL(window.location.href);
    url.searchParams.set('q', query);
    url.searchParams.set('f', type);
    url.searchParams.set('gcf', gc_from.toString());
    url.searchParams.set('gct', gc_to.toString());
    window.history.replaceState({}, '', url.href);
    searching = false
    window.llhandler()
  }

  function castToEl(a: any): HTMLInputElement {
    return a;
  }

  if(browser) {
    if(window.location.hash == "#focus") {
      function focus() {
        let el = (document.querySelector("#search-bar") as HTMLInputElement)

        if(!el) {
          setTimeout(focus, 100);
        } else {
          el.focus()
        }
      }
      focus()
    }
  }

</script>

<p>{#if searching}Searching...{:else}&nbsp{/if}</p>

<form id="search" method="GET" action="/frostpaw/search">
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
</form>

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