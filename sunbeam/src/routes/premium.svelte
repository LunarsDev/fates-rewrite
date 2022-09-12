<script context="module" lang="ts">
  export const prerender = false;

  /** @type {import('@sveltejs/kit@next').Load} */
  export async function load({ params, fetch, stuff }) {
    return {};
  }
</script>

<script lang="ts">
  import BristlefrostMeta from '$lib/base/BristlefrostMeta.svelte';
</script>

<BristlefrostMeta
  url="https://fateslist.xyz"
  title="Fates List | Discord Bot List"
  description="Find, invite and discover the best bots &amp; servers now on Fates List"
  thumbnail="https://fateslist.xyz/static/botlisticon.webp"
/>

<div class="premium">
  <div class="premium-about">
    <img
      src="https://api.fateslist.xyz/static/assets/prod/premium.webp"
      class="premium-icon"
      height="25px"
      width="25px"
      alt="Fates List Premium Icon"
      on:error={function () {
        this.src = 'https://api.fateslist.xyz/static/botlisticon.webp';
      }}
    />
    <h2 class="premium-title">Fates List Premium</h2>
  </div>

  <p class="premium-description">Help your bot reach more servers with Fates List Premium!</p>
</div>

<style>
  .premium-about {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 25px;
  }

  .premium-title {
    text-align: center;
  }

  .premium-icon {
    height: 25px;
    width: 25px;
    padding: 5px;
    background: black;
    border-radius: 50%;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.5);
  }

  .premium-icon + .premium-title {
    margin-left: 10px;
  }

  .premium-description {
    text-align: center;
    margin-top: -5px;
  }
</style>
