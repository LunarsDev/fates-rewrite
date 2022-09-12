<script lang="ts">
  import BristlefrostMeta from '$lib/base/BristlefrostMeta.svelte';
  import { enums } from '../enums/enums';
  import Tab from '$lib/base/TabV2.svelte';
  import Commands from './helpers/Commands.svelte';
  import About from './helpers/About.svelte';
  import Actions from './helpers/Actions.svelte';
  import Warns from './helpers/Warns.svelte';
  import ReviewAdd from './helpers/ReviewAdd.svelte';
  import ReviewList from './helpers/ReviewList.svelte';

  export let data: any;
  export let type: string;

  let extra_links = data.extra_links as Map<string, string>;
</script>

<BristlefrostMeta
  url="https://fateslist.xyz/{type}/{data.user.id}"
  pageTitle={data.user.username}
  title={data.user.username}
  description={data.description}
  thumbnail={data.user.avatar}
/>

{#if data.banner && data.flags.includes(enums.Flags.keep_banner_decor)}
  <style lang="scss">
    .opaque {
      opacity: 0.83;
    }

    .banner-decor {
      opacity: 0.7;
      background-color: black;
      border-radius: 15px 15px 15px 15px;
    }
  </style>
{/if}

<div id="long-description" class="lazy bot-page-banner" style="--background: url('{data.banner}');">
  <img
    class="bot-avatar"
    src={data.user.avatar.replace('.png', '.webp').replace('width=', 'width=120px')}
    id="bot-avatar"
    alt="{data.user.username}'s avatar"
    on:error={function () {
      this.src = 'https://api.fateslist.xyz/static/botlisticon.webp';
    }}
  />
  <article class="bot-page">
    <a href="/{type}/{data.user.id}/invite" class="banner-decor bot-username bot-username-link">
      <h2 class="white" id="bot-name">
        {data.user.username}
        {#if type == 'bot'}<span class="prefix">({data.prefix || '/'})</span>{/if}
      </h2>
    </a>
    <div class="bot-page-content">
      <Warns data={data} />
      <p class="banner-decor white" id="bot-description">
        {@html data.description.replace('p>', 'span>')}
      </p>
      <Actions data={data} type={type} />
      <Tab>
        <section id="long-description-real" class="tabs-v2 prose prose-zinc dark:prose-invert">
          {@html data.css}
          {@html data.long_description}
        </section>
        <section id="commands-tab" class="tabs-v2">
          <h2>Commands</h2>
          {#if type == 'bot'}
            <Commands data={data} />
          {:else}
            <span>Servers do not have commands</span>
          {/if}
        </section>
        <hr />
        <section id="reviews-tab" class="tabs-v2">
          <ReviewAdd data={data} type={type} />
          <ReviewList data={data} type={type} />
        </section>
        <hr />
        <section id="resources-tab" class="tabs-v2">
          <h2>Some cool resources!</h2>
          <h3>Basics</h3>
          <a href="/bot/{data.user.id}/invite">Invite</a><br />
          {#each Object.entries(extra_links) as link}
            {#if !link[0].startsWith('_')}
              <a href={link[1]}>{link[0]}</a><br />
            {/if}
          {/each}
        </section>
        <hr />
        <section id="about-tab" class="tabs-v2">
          <!--First main owner is guaranteed to be first in HTML-->
          <About data={data} type={type} />
        </section>
      </Tab>
    </div>
  </article>
</div>

<style lang="scss" global>
  #reviews-tab {
    overflow: visible !important;
  }
  #review-add {
    opacity: 1 !important;
    border: solid thin;
    width: 250px;
    max-width: 250px;
    margin-bottom: 10px;
  }
  :global(.codehilite) {
    background-color: white;
  }
  .prefix {
    opacity: 0.65;
  }

  .bot-page-banner {
    background: var(--background) no-repeat;
    background-size: 100% 100%;
    width: 100%;
    height: 100%;
    min-height: 1000px;
    background-repeat: no-repeat;
    z-index: 10;
  }

  .bot-page-banner.lazy {
    background-image: none;
    background-color: #f1f1fa;
  }

  .bot-page {
    display: flex;
    flex-wrap: wrap;
  }
  .bot-username,
  .bot-avatar {
    display: flex;
    opacity: 1 !important;
    justify-content: center;
    align-items: center;
    margin: 0 auto;
  }
  .bot-username,
  span {
    margin-bottom: 0px;
    padding-bottom: 0px;
  }
  .bot-avatar {
    border-radius: 50%;
    width: 120px;
  }
  .bot-page-content {
    display: block;
    margin: 10px;
    width: 100%;
  }
  .accordion-container {
    display: block;
    cursor: text !important;
  }
  #bot-description {
    font-size: 18px;
    text-align: center;
    margin: 0px;
    padding: 0px;
  }

  @media screen and (max-width: 768px) {
    #long-description-real {
      padding: 3px !important;
      border: none !important;
    }
  }

  :global(.review-user) {
    opacity: 1;
    margin-top: 5px;
    padding-left: 3px;
    box-sizing: border-box;
    /*border-left: 1px solid white !important; */
    margin-bottom: 2px;
  }
  :global(.review-left) {
    display: inline-block;
  }
  #long-description img {
    max-width: 100% !important;
  }
  :global(.page-item) {
    display: inline-block;
    margin-right: 5px !important;
    list-style: none;
  }
  .bot-username-link,
  #bot-name {
    margin-top: 0px !important;
    margin-bottom: 1px !important;
  }
  .opaque {
    opacity: 0.7;
  }

  #long-description-real {
    padding: 45px;
    border: solid 1px;
    width: 100%;
    height: 100%;
  }
</style>
