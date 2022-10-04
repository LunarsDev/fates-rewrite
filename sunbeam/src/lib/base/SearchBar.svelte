<script lang="ts">
  import { browser } from '$app/environment';

  import { api } from '$lib/config';
  import { request } from '$lib/request';
  import { page } from '$app/stores';

  import FormInput from './FormInput.svelte';
  import Tip from './Tip.svelte';
  import Tag from './Tag.svelte';
  import { onMount } from 'svelte';
  import Section from './Section.svelte';
  import CardContainer from '../cards/CardContainer.svelte';
  import BotCard from '../cards/BotCard.svelte';
  import BotPack from './BotPack.svelte';
  import { enums, type TargetType } from '$lib/enums/enums';
  import { info } from '$lib/logger';

  export let type: TargetType = enums.TargetType.Bot;
  let query: string;
  let gc_from = 1;
  let gc_to = -1;
  export let data: any = null;

  export let meta;

  let serverTags = [];
  let botTags = [];

  // Used by tags
  function botTagsSelect(s: string[]) {
    botTags = s;
  }

  function serverTagsSelect(s: string[]) {
    serverTags = s;
  }

  let sTagAction = {
    func: () => searchBot(true),
    text: 'Search'
  };

  onMount(() => {
    if (browser) {
      let url = new URL(window.location.href);

      type = enums.helpers.strToTargetType(url.searchParams.get('t') || 'bot');

      query = url.searchParams.get('q') || '';
      gc_from = parseInt(url.searchParams.get('gcf') || '0');
      gc_to = parseInt(url.searchParams.get('gct') || '-1');

      let bt = url.searchParams.get('bt') || '';
      botTags = bt.split('.').filter((x) => x != '');

      let st = url.searchParams.get('st') || '';
      serverTags = st.split('.').filter((x) => x != '');

      info('SearchBar', type, query, gc_from, gc_to, botTags, serverTags);

      if (query || botTags.length > 0 || serverTags.length > 0) {
        searchBot(true);
      } else {
        data = null;
      }
    }
  });

  let searching = false;

  function keyHandle(event) {
    event.preventDefault();
    if (event.keyCode === 13) {
      searchBot(true);
    }
  }

  async function searchBot(tagsSearch = false) {
    // update location silently to include new query params
    let url = new URL(window.location.href);

    if (query) {
      url.searchParams.set('q', query);
    } else {
      url.searchParams.delete('q');
    }

    if (type || type == enums.TargetType.Bot) {
      url.searchParams.set('t', enums.helpers.targetTypeString(type));
    } else {
      url.searchParams.delete('t');
    }

    if (gc_from) {
      url.searchParams.set('gcf', gc_from.toString());
    } else {
      url.searchParams.delete('gcf');
    }

    if (gc_to && gc_to != -1) {
      url.searchParams.set('gct', gc_to.toString());
    } else {
      url.searchParams.delete('gct');
    }

    if (botTags.length > 0) {
      url.searchParams.set('bt', botTags.join('.'));
    } else {
      url.searchParams.delete('bt');
    }

    if (serverTags.length > 0) {
      url.searchParams.set('st', serverTags.join('.'));
    } else {
      url.searchParams.delete('st');
    }

    window.history.replaceState({}, '', url.href);

    if (!query && !tagsSearch) {
      data = null;
      setTimeout(() => window.llhandler(), 300);
      return;
    } // Don't search if query is empty

    searching = true;
    let res = await request(`${api}/search`, {
      method: 'POST',
      endpointType: 'user',
      auth: false,
      session: $page.data,
      json: {
        query: query,
        guild_count: {
          filter_from: gc_from,
          filter_to: gc_to
        },
        tags: {
          bot: botTags,
          server: serverTags
        }
      },
      fetch: fetch
    });

    data = await res.json();
    searching = false;
    setTimeout(() => window.llhandler(), 300);
  }

  function castToEl(a: any): HTMLInputElement {
    return a;
  }
</script>

<p>
  {#if searching}Searching...{:else}&nbsp{/if}
</p>

<div class="search">
  <input
    type="text"
    on:input={(event) => {
      query = castToEl(event.target).value;
      searchBot(false);
    }}
    id="search-bar"
    class="form-control fform search"
    placeholder="Search for {enums.helpers.targetTypeString(type)}s (ENTER to search)"
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
        gc_from = parseInt(castToEl(event.target).value) || 0;
        searchBot(false);
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
        gc_to = parseInt(castToEl(event.target).value) || -1;
        searchBot(false);
      }}
      id="gct"
      name="To:"
      placeholder="To... (-1 means no limit)"
      type="number"
      data={gc_to}
    />

    <h3>Display Order</h3>
    <Tip>
      First display is either 'bot', 'server', 'pack' or 'user' and chooses whether you want bots
      first or servers first!
    </Tip>
    <select
      on:change={(event) => {
        if (castToEl(event).value == '#') {
          return;
        }

        type = enums.helpers.strToTargetType(castToEl(event.target).value || 'bot');
        searchBot(false);
      }}
    >
      <option value="#" disabled>Choose a display order</option>
      <option value="bot" selected={type == enums.TargetType.Bot}>Bots First</option>
      <option value="server" selected={type == enums.TargetType.Server}>Servers First</option>
      <option value="pack" selected={type == enums.TargetType.Pack}>Packs First</option>
      <option value="user" selected={type == enums.TargetType.User}>Users First</option>
    </select>
  </details>
</div>

{#if data}
  <!--First Display-->
  {#if type == enums.TargetType.Bot}
    <Section title="Bots" icon="fa-solid:search" id="search-res-bots">
      <Tag
        tagAction={sTagAction}
        onclick={botTagsSelect}
        initialSelected={botTags}
        tags={meta.bot.tags}
      />
      <CardContainer>
        {#each data.bots as bot}
          <BotCard data={bot} type={enums.TargetType.Bot} rand={false} />
        {/each}
      </CardContainer>
    </Section>

    <Section title="Bot Packs" icon="bx:bx-package" id="search-res-packs">
      {#each data.packs as pack}
        <BotPack pack={pack} />
      {/each}
    </Section>

    <Section title="Servers" icon="fa-solid:search" id="search-res-servers">
      <Tag
        tagAction={sTagAction}
        onclick={serverTagsSelect}
        initialSelected={serverTags}
        tags={meta.server.tags}
      />
      <CardContainer>
        {#each data.servers as server}
          <BotCard data={server} type={enums.TargetType.Server} rand={false} />
        {/each}
      </CardContainer>
    </Section>

    <Section title="Profiles" icon="fa-solid:search" id="search-res-profiles">
      <CardContainer>
        {#each data.profiles as profile}
          <BotCard data={profile} type={enums.TargetType.User} rand={false} />
        {/each}
      </CardContainer>
    </Section>
  {:else if type == enums.TargetType.Pack}
    <Section title="Bot Packs" icon="bx:bx-package" id="search-res-packs">
      {#each data.packs as pack}
        <BotPack pack={pack} />
      {/each}
    </Section>

    <Section title="Bots" icon="fa-solid:search" id="search-res-bots">
      <Tag
        tagAction={sTagAction}
        onclick={botTagsSelect}
        initialSelected={botTags}
        tags={meta.bot.tags}
      />
      <CardContainer>
        {#each data.bots as bot}
          <BotCard data={bot} type={enums.TargetType.Bot} rand={false} />
        {/each}
      </CardContainer>
    </Section>

    <Section title="Servers" icon="fa-solid:search" id="search-res-servers">
      <Tag
        tagAction={sTagAction}
        onclick={serverTagsSelect}
        initialSelected={serverTags}
        tags={meta.server.tags}
      />
      <CardContainer>
        {#each data.servers as server}
          <BotCard data={server} type={enums.TargetType.Server} rand={false} />
        {/each}
      </CardContainer>
    </Section>

    <Section title="Profiles" icon="fa-solid:search" id="search-res-profiles">
      <CardContainer>
        {#each data.profiles as profile}
          <BotCard data={profile} type={enums.TargetType.User} rand={false} />
        {/each}
      </CardContainer>
    </Section>
  {:else if type == enums.TargetType.Server}
    <Section title="Servers" icon="fa-solid:search" id="search-res-servers">
      <Tag
        tagAction={sTagAction}
        onclick={serverTagsSelect}
        initialSelected={serverTags}
        tags={meta.server.tags}
      />
      <CardContainer>
        {#each data.servers as server}
          <BotCard data={server} type={enums.TargetType.Server} rand={false} />
        {/each}
      </CardContainer>
    </Section>

    <Section title="Profiles" icon="fa-solid:search" id="search-res-profiles">
      <CardContainer>
        {#each data.profiles as profile}
          <BotCard data={profile} type={enums.TargetType.User} rand={false} />
        {/each}
      </CardContainer>
    </Section>

    <Section title="Bots" icon="fa-solid:search" id="search-res-bots">
      <Tag
        tagAction={sTagAction}
        onclick={botTagsSelect}
        initialSelected={botTags}
        tags={meta.bot.tags}
      />
      <CardContainer>
        {#each data.bots as bot}
          <BotCard data={bot} type={enums.TargetType.Bot} rand={false} />
        {/each}
      </CardContainer>
    </Section>

    <Section title="Bot Packs" icon="bx:bx-package" id="search-res-packs">
      {#each data.packs as pack}
        <BotPack pack={pack} />
      {/each}
    </Section>
  {:else}
    <Section title="Profiles" icon="fa-solid:search" id="search-res-profiles">
      <CardContainer>
        {#each data.profiles as profile}
          <BotCard data={profile} type={enums.TargetType.User} rand={false} />
        {/each}
      </CardContainer>
    </Section>

    <Section title="Servers" icon="fa-solid:search" id="search-res-servers">
      <Tag
        tagAction={sTagAction}
        onclick={serverTagsSelect}
        initialSelected={serverTags}
        tags={meta.server.tags}
      />
      <CardContainer>
        {#each data.servers as server}
          <BotCard data={server} type={enums.TargetType.Server} rand={false} />
        {/each}
      </CardContainer>
    </Section>

    <Section title="Bot Packs" icon="bx:bx-package" id="search-res-packs">
      {#each data.packs as pack}
        <BotPack pack={pack} />
      {/each}
    </Section>

    <Section title="Bots" icon="fa-solid:search" id="search-res-bots">
      <Tag
        tagAction={sTagAction}
        onclick={botTagsSelect}
        initialSelected={botTags}
        tags={meta.bot.tags}
      />
      <CardContainer>
        {#each data.bots as bot}
          <BotCard data={bot} type={enums.TargetType.Bot} rand={false} />
        {/each}
      </CardContainer>
    </Section>
  {/if}
{:else if type == enums.TargetType.Bot}
  <Tag
    tagAction={sTagAction}
    onclick={botTagsSelect}
    initialSelected={botTags}
    tags={meta.bot.tags}
  />
{:else}
  <Tag
    tagAction={sTagAction}
    onclick={serverTagsSelect}
    initialSelected={serverTags}
    tags={meta.server.tags}
  />
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
