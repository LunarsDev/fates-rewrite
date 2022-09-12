<script lang="ts">
  export let pack: any;
  export let centered = true;
</script>

<div class="pack-container">
  <h3>{pack.name}</h3>
  <h4 class="opaque">{pack.description}</h4>
  {#each pack.resolved_bots as bot}
    <div class="pack-bot">
      <a href="/bot/{bot.id || bot.user.id}">
        <img
          class="pack-user-avatar"
          alt="{bot.username || bot.user.username}s avatar"
          src={bot.avatar || bot.user.avatar}
          loading="lazy"
          on:error={function () {
            this.src = 'https://api.fateslist.xyz/static/botlisticon.webp';
          }}
        />
      </a>
      <span class="pack-data">
        <a href="/bot/{bot.id || bot.user.id}">
          {bot.username || bot.user.username}<br />
        </a>
        <span class="indent">{bot.description}</span>
      </span>
    </div>
  {/each}
</div>

{#if centered}
  <style lang="scss">
    .pack-container {
      margin-left: auto;
      margin-right: auto;
    }
  </style>
{/if}

<style lang="scss">
  $img-width: 30px;

  a {
    opacity: 1 !important;
  }

  .pack-container {
    background: #111112;
    width: 80%;
    -moz-box-shadow: 0px 0px 20px 5px #000;
    -webkit-box-shadow: 0px 0px 20px 5px #000;
    box-shadow: 0px 0px 20px 5px #000;
    padding: 3px;
    border-radius: 5px;
    border: solid 1px;
    margin-bottom: 3px;
  }

  .pack-bot {
    margin-bottom: 20px;
  }

  .opaque {
    opacity: 0.8;
  }

  .indent {
    margin-left: $img-width + 3px;
    opacity: 0.8;
  }

  .pack-data {
    color: white;
    clear: both;
  }

  .pack-user-avatar {
    border-radius: 50%;
    width: $img-width;
    vertical-align: middle;
  }
</style>
