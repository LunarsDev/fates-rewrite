<script lang="ts">
    import Section from "./Section.svelte";
    import CardContainer from "../cards/CardContainer.svelte";
    import BotCard from "../cards/BotCard.svelte";
    import BotPack from "../base/BotPack.svelte";
    import Tag from "../base/Tag.svelte";

    export let targetType: string;
    export let data: any;
</script>

<!--First Display-->
{#if targetType == 'bot'}
  <Section title="Bots" icon="fa-solid:search" id="search-res-bots">
    <Tag targetType={targetType} tags={data.tags.bots} />
    <CardContainer>
      {#each data.bots as bot}
        <BotCard data={bot} type="bot" rand={false} />
      {/each}
    </CardContainer>
  </Section>

  <Section title="Bot Packs" icon="bx:bx-package" id="search-res-packs">
    {#each data.packs as pack}
      <BotPack pack={pack} />
    {/each}
  </Section>

  <Section title="Servers" icon="fa-solid:search" id="search-res-servers">
    <Tag targetType={targetType} tags={data.tags.servers} />
    <CardContainer>
      {#each data.servers as server}
        <BotCard data={server} type="server" rand={false} />
      {/each}
    </CardContainer>
  </Section>

  <Section title="Profiles" icon="fa-solid:search" id="search-res-profiles">
    <CardContainer>
      {#each data.profiles as profile}
        <BotCard data={profile} type="profile" rand={false} />
      {/each}
    </CardContainer>
  </Section>
{:else if targetType == 'pack'}
  <Section title="Bot Packs" icon="bx:bx-package" id="search-res-packs">
    {#each data.packs as pack}
      <BotPack pack={pack} />
    {/each}
  </Section>

  <Section title="Bots" icon="fa-solid:search" id="search-res-bots">
    <Tag targetType={targetType} tags={data.tags.bots} />
    <CardContainer>
      {#each data.bots as bot}
        <BotCard data={bot} type="bot" rand={false} />
      {/each}
    </CardContainer>
  </Section>

  <Section title="Servers" icon="fa-solid:search" id="search-res-servers">
    <Tag targetType={targetType} tags={data.tags.servers} />
    <CardContainer>
      {#each data.servers as server}
        <BotCard data={server} type="server" rand={false} />
      {/each}
    </CardContainer>
  </Section>

  <Section title="Profiles" icon="fa-solid:search" id="search-res-profiles">
    <CardContainer>
      {#each data.profiles as profile}
        <BotCard data={profile} type="profile" rand={false} />
      {/each}
    </CardContainer>
  </Section>
{:else if targetType == 'server'}
  <Section title="Servers" icon="fa-solid:search" id="search-res-servers">
    <Tag targetType={targetType} tags={data.tags.servers} />
    <CardContainer>
      {#each data.servers as server}
        <BotCard data={server} type="server" rand={false} />
      {/each}
    </CardContainer>
  </Section>

  <Section title="Profiles" icon="fa-solid:search" id="search-res-profiles">
    <CardContainer>
      {#each data.profiles as profile}
        <BotCard data={profile} type="profile" rand={false} />
      {/each}
    </CardContainer>
  </Section>

  <Section title="Bots" icon="fa-solid:search" id="search-res-bots">
    <Tag targetType={targetType} tags={data.tags.bots} />
    <CardContainer>
      {#each data.bots as bot}
        <BotCard data={bot} type="bot" rand={false} />
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
        <BotCard data={profile} type="profile" rand={false} />
      {/each}
    </CardContainer>
  </Section>

  <Section title="Servers" icon="fa-solid:search" id="search-res-servers">
    <Tag targetType={targetType} tags={data.tags.servers} />
    <CardContainer>
      {#each data.servers as server}
        <BotCard data={server} type="server" rand={false} />
      {/each}
    </CardContainer>
  </Section>

  <Section title="Bot Packs" icon="bx:bx-package" id="search-res-packs">
    {#each data.packs as pack}
      <BotPack pack={pack} />
    {/each}
  </Section>

  <Section title="Bots" icon="fa-solid:search" id="search-res-bots">
    <Tag targetType={targetType} tags={data.tags.bots} />
    <CardContainer>
      {#each data.bots as bot}
        <BotCard data={bot} type="bot" rand={false} />
      {/each}
    </CardContainer>
  </Section>
{/if}
