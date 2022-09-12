<script lang="ts">
  import BristlefrostMeta from '$lib/base/BristlefrostMeta.svelte';
  export let data: any;
  export let type: string;
  import Warns from './helpers/Warns.svelte';
  import Actions from './helpers/Actions.svelte';
</script>

<BristlefrostMeta
  url="https://fateslist.xyz/{type}/{data.user.id}"
  pageTitle={data.user.username}
  title="Vote For {data.user.username} on Fates List!"
  description={data.description}
  thumbnail={data.user.avatar}
/>

{#if data.banner && data.keep_banner_decor}
  <style lang="scss">
    .banner-decor {
      opacity: 0.7;
      background-color: black;
      border-radius: 15px 15px 15px 15px;
    }
  </style>
{/if}

{@html data.css}

<div id="long-description" class="lozad bot-page-banner" data-background-image={data.banner}>
  <img
    class="bot-avatar"
    loading="lazy"
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
        Vote for {data.user.username}! {#if type == 'bot'}<span class="prefix"
            >({data.prefix || '/'})</span
          >{/if}
      </h2>
    </a>
    <div class="bot-page-content">
      <div class="accordion-container">
        <Warns data={data} />
      </div>
      <p class="banner-decor white" id="bot-description">
        {@html data.description.replace('p>', 'span>')}
      </p>
      <Actions data={data} type={type} limited={true} />
      <p id="vote-warning">
        <span class="red">Warning:</span> You can only vote for one bot every 8 hours, so vote wisely
      </p>
    </div>
  </article>
</div>

<style lang="scss">
  :global(.buttons-all) {
    background-color: black !important;
  }
  :global(.codehilite) {
    background-color: white;
  }

  .prefix {
    opacity: 0.65;
  }

  .bot-page-banner {
    background-size: cover;
    width: 100%;
    height: 100%;
    min-height: 1000px;
    background-repeat: no-repeat;
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

  :global(.buttons-all) {
    color: white !important;
    border: solid thin !important;
    opacity: 1 !important;
    margin-right: 10px;
  }

  :global(.disabled) {
    opacity: 0.63 !important;
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

  .red {
    color: red;
  }
  #vote-warning {
    text-align: center;
  }
</style>
