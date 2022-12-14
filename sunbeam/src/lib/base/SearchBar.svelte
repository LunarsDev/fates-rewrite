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
  import Button from './Button.svelte';
  import { goto } from '$app/navigation';

  export let type: TargetType = enums.TargetType.Bot;
  let query: string;
  let gc_from = 0;
  let gc_to = -1;
  let vc_from = 0;
  let vc_to = -1;
  let bot_op = 'and';
  let server_op = 'and';
  export let data: any = null;

  export let meta;

  let serverTags = [];
  let botTags = [];

  // Used by tags
  function botTagsSelect(s: string[]) {
    botTags = s;
    searchBot();
  }

  function serverTagsSelect(s: string[]) {
    serverTags = s;
    searchBot();
  }

  let sTagAction = {
    func: () => searchBot(),
    text: 'Search'
  };

  onMount(() => {
    if (browser) {
      let url = new URL(window.location.href);

      if (url.searchParams.get('t')) {
        type = enums.helpers.strToTargetType(url.searchParams.get('t') || 'bot');
      }

      query = url.searchParams.get('q') || '';
      gc_from = parseInt(url.searchParams.get('gcf') || '0');
      gc_to = parseInt(url.searchParams.get('gct') || '-1');
      vc_from = parseInt(url.searchParams.get('vcf') || '0');
      vc_to = parseInt(url.searchParams.get('vct') || '-1');

      if (url.searchParams.get('bot_op') == 'and' || url.searchParams.get('bot_op') == 'or') {
        bot_op = url.searchParams.get('bot_op');
      }

      if (url.searchParams.get('server_op') == 'and' || url.searchParams.get('server_op') == 'or') {
        server_op = url.searchParams.get('server_op');
      }

      let bt = url.searchParams.get('bt') || '';
      botTags = bt.split('.').filter((x) => x != '');

      let st = url.searchParams.get('st') || '';
      serverTags = st.split('.').filter((x) => x != '');

      info('SearchBar', type, query, gc_from, gc_to, vc_from, vc_to, botTags, serverTags);

      if (query || botTags.length > 0 || serverTags.length > 0) {
        searchBot();
      } else {
        data = null;
      }
    }
  });

  let searching = false;

  function keyHandle(event) {
    event.preventDefault();
    if (event.keyCode === 13) {
      searchBot();
    }
  }

  async function searchBot() {
    // update location silently to include new query params
    let url = new URL(window.location.href);

    let searchDat = new Map();

    if (query) {
      searchDat.set('query', query);
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
      searchDat.set('gc_from', gc_from);
      url.searchParams.set('gcf', gc_from.toString());
    } else {
      url.searchParams.delete('gcf');
    }

    if (gc_to && gc_to != -1) {
      searchDat.set('gc_to', gc_to);
      url.searchParams.set('gct', gc_to.toString());
    } else {
      url.searchParams.delete('gct');
    }

    if (vc_from) {
      searchDat.set('vc_from', vc_from);
      url.searchParams.set('vcf', vc_from.toString());
    } else {
      url.searchParams.delete('vcf');
    }

    if (vc_to && vc_to != -1) {
      searchDat.set('vc_to', vc_to);
      url.searchParams.set('vct', vc_to.toString());
    } else {
      url.searchParams.delete('vct');
    }

    if (bot_op) {
      url.searchParams.set('bot_op', bot_op);
    } else {
      url.searchParams.delete('bot_op');
    }

    if (server_op) {
      url.searchParams.set('server_op', server_op);
    } else {
      url.searchParams.delete('server_op');
    }

    if (botTags.length > 0) {
      searchDat.set('botTags', botTags);
      url.searchParams.set('bt', botTags.join('.'));
    } else {
      url.searchParams.delete('bt');
    }

    if (serverTags.length > 0) {
      searchDat.set('serverTags', serverTags);
      url.searchParams.set('st', serverTags.join('.'));
    } else {
      url.searchParams.delete('st');
    }

    window.history.replaceState({}, '', url.href);

    if (searchDat.size == 0) {
      data = null;
      searching = false;
      setTimeout(() => window.llhandler(), 300);
      return;
    }

    let bopStr = '&&';

    if (bot_op == 'and') {
      bopStr = '@>';
    }

    let sopStr = '&&';

    if (server_op == 'and') {
      sopStr = '@>';
    }

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
        votes: {
          filter_from: vc_from,
          filter_to: vc_to
        },
        tags: {
          bot: botTags,
          server: serverTags,
          bot_op: bopStr,
          server_op: sopStr
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
    on:keyup={keyHandle}
    on:input={(event) => {
      query = castToEl(event.target).value;
      searchBot();
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
      onkeyup={keyHandle}
      oninput={(event) => {
        gc_from = parseInt(castToEl(event.target).value) || 0;
        searchBot();
      }}
      id="gcf"
      name="From:"
      placeholder="From..."
      type="number"
      data={gc_from}
    />
    <FormInput
      formclass="filter-inp filter-inp-right"
      onkeyup={keyHandle}
      oninput={(event) => {
        gc_to = parseInt(castToEl(event.target).value) || -1;
        searchBot();
      }}
      id="gct"
      name="To:"
      placeholder="To... (-1 means no limit)"
      type="number"
      data={gc_to}
    />

    <h3>Votes Filter</h3>
    <FormInput
      formclass="filter-inp filter-inp-left"
      onkeyup={keyHandle}
      oninput={(event) => {
        vc_from = parseInt(castToEl(event.target).value) || 0;
        searchBot();
      }}
      id="vcf"
      name="From:"
      placeholder="From..."
      type="number"
      data={vc_from}
    />

    <FormInput
      formclass="filter-inp filter-inp-right"
      onkeyup={keyHandle}
      oninput={(event) => {
        vc_to = parseInt(castToEl(event.target).value) || -1;
        searchBot();
      }}
      id="vct"
      name="To:"
      placeholder="To... (-1 means no limit)"
      type="number"
      data={vc_to}
    />

    <h3>Tag Operation Modes</h3>

    <label for="btm">Bot Tag Mode</label>
    <select
      name="btm"
      on:change={(e) => {
        bot_op = castToEl(e.target).value;
        searchBot();
      }}
    >
      <option value="and" selected={bot_op == 'and'}>AND</option>
      <option value="or" selected={bot_op == 'or'}>OR</option>
    </select>

    <label for="stm">Server Tag Mode</label>
    <select
      name="stm"
      on:change={(e) => {
        server_op = castToEl(e.target).value;
        searchBot();
      }}
    >
      <option value="and" selected={server_op == 'and'}>AND</option>
      <option value="or" selected={server_op == 'or'}>OR</option>

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
          searchBot();
        }}
      >
        <option value="#" disabled>Choose a display order</option>
        <option value="bot" selected={type == enums.TargetType.Bot}>Bots First</option>
        <option value="server" selected={type == enums.TargetType.Server}>Servers First</option>
        <option value="pack" selected={type == enums.TargetType.Pack}>Packs First</option>
        <option value="user" selected={type == enums.TargetType.User}>Users First</option>
      </select>
    </select>
  </details>
</div>

{#if data}
  <Button
    onclick={() => {
      query = '';
      botTags = [];
      serverTags = [];
      searchBot();
      goto('/');
    }}>Leave Search</Button
  >
  <!--First Display-->
  {#if type == enums.TargetType.Bot}
    <Section title="Bots" icon="fa-solid:search" id="search-res-bots">
      <Tag
        tagAction={sTagAction}
        onclick={botTagsSelect}
        type={enums.TargetType.Bot}
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
        type={enums.TargetType.Server}
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
        type={enums.TargetType.Bot}
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
        type={enums.TargetType.Server}
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
        type={enums.TargetType.Server}
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
        type={enums.TargetType.Bot}
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
        type={enums.TargetType.Server}
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
        type={enums.TargetType.Bot}
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
    type={enums.TargetType.Bot}
    initialSelected={botTags}
    tags={meta.bot.tags}
  />
{:else}
  <Tag
    tagAction={sTagAction}
    onclick={serverTagsSelect}
    type={enums.TargetType.Server}
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
