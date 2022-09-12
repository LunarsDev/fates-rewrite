<script lang="ts">
  import { session } from '$app/stores';
  import { apiUrl } from '$lib/config';
  import Icon from '@iconify/svelte';
  import Button from '$lib/base/Button.svelte';
  import { enums } from '../enums/enums';
  export let data: any;
  export let type: string;
  export let rand: boolean;

  // Do some processing
  if (data.id && !data.user) {
    data.user = { id: data.id };
  }
  data.banner = data.banner || `${apiUrl}/static/assets/prod/banner.webp?v=2`;

  if(data.description && data.description.length > 150) {
	data.description = data.description.substring(0, 150) + '...';
  }
</script>

<section class="bot-card">
  <div class="bot-card-banner lazy" style="--background: url('{data.banner}');">
    {#if (type == 'bot' || type == 'server') && data.state == enums.BotState.certified}
      <Icon class="bot-card-cert" icon="fa-solid:certificate" inline={false} height="3em" />
    {/if}
    <a href="/{type}/{data.user.id}" class="bot-card-view-link bot-card-avatar-container">
      <img
        alt="Bot Avatar"
        class="bot-card-avatar"
        src={data.user.avatar.replace('.png', '.webp')}
        loading="lazy"
        on:error={function () {
          this.src = 'https://api.fateslist.xyz/static/botlisticon.webp';
        }}
      />
    </a>
    <div>
      <a href="/{type}/{data.user.id}" class="bot-card-view-link">
        <div class="bot-card-username">
          <p class="bot-card-username-txt white-bold">
            {#if rand}Fetching random bot...{:else}{data.user.username}{/if}
          </p>
        </div>
      </a>
    </div>

    <p class="bot-card-description">
      <span class="bot-card-description-txt" style="overflow-wrap: anywhere;"
        >{#if rand}Try out your luck!{:else}{data.description}{/if}</span
      >
    </p>

    {#if type == 'bot' || type == 'server'}
      <div class="d-flex bot-card-footer">
        <div class="bot-card-footer-stats">
          <p class="text-center white-bold">
            <Icon icon="fa-solid:server" inline={false} />
            <span style="margin-left: 3px;" class="bot-servers"
              >{#if rand}N/A{:else}{data.guild_count}{/if}</span
            >
          </p>
        </div>
        <div class="bot-card-footer-stats">
          <p class="text-center white-bold">
            <Icon icon="fa-solid:thumbs-up" inline={false} />
            <span style="margin-left: 3px;" class="bot-votes"
              >{#if rand}N/A{:else}{data.votes}{/if}</span
            >
          </p>
        </div>
      </div>
    {/if}
    <div class="bot-card-actions">
      <Button
        ariaLabel="View"
        href="/{type}/{data.user.id}"
        class="bot-card-actions-link button"
        onclick={() => {}}>View</Button
      >
      {#if type != 'profile'}
        <Button
          ariaLabel="Invite"
          href="/{type}/{data.user.id}/invite"
          class="bot-card-actions-link button"
          target="_blank"
          onclick={() => {}}
          >{#if type == 'server'}Join{:else}Invite{/if}</Button
        >
      {:else if $session.session.token && data.user.id == $session.session.user.id}
        <Button
          id="bot-card-action-settings-{data.user.id}"
          ariaLabel="Settings"
          href="/{type}/{data.user.id}/settings"
          onclick={() => {}}
          class="bot-card-actions-link profile-settings-btn button">Settings</Button
        >
      {:else}
        <Button
          id="bot-card-action-settings-{data.user.id}"
          onclick={() => {}}
          ariaLabel="Settings"
          ariaDisabled={true}
          class="bot-card-actions-link disabled-profile-btn">Settings</Button
        >
      {/if}
    </div>
    <slot />
  </div>
</section>

<style lang="scss">
  :global(.disabled-profile-btn) {
    opacity: 0.8 !important;
    color: white !important;
  }

  :global(.profile-settings-btn) {
    font-size: 12px !important;
  }

  a {
    opacity: 1 !important;
  }

  $card-scale: 1.025;
  $form-radius: 4px;
  $link-opacity: 0.63;

  .text-center {
    text-align: center;
  }
  .d-flex {
    display: flex;
  }

  .bot-card:hover {
    transform: scale($card-scale, $card-scale) perspective(1px) translateZ(0);
    filter: blur;
    -webkit-filter: blur(0);
  }

  .bot-card-username {
    margin-right: auto;
    margin-left: auto;
    margin-top: 30px;
  }

  .bot-card-username-txt {
    white-space: nowrap;
    text-overflow: ellipsis;
    overflow: hidden;
    font-size: 21px;
    margin-top: 35px;
    text-align: center;
  }

  .bot-card {
    width: 310px;
    height: 520px;
    background: #111112;
    -moz-box-shadow: 0px 0px 20px 5px #000;
    -webkit-box-shadow: 0px 0px 20px 5px #000;
    box-shadow: 0px 0px 20px 5px #000;
    border-top-style: none;
    margin: 25px 25px;
    border-radius: 10px 10px 10px 10px;
  }

  .bot-card-banner {
    width: 100%;
    height: 35%;
    background: center / cover no-repeat;
    border-radius: 10px 10px 0px 0px !important;
  }

  .bot-card-avatar {
    border-radius: 50%;
    background-color: black !important;
    width: 100px;
    min-width: 100px;
    height: 100px;
    min-height: 100px;
    margin: 5% auto;
    margin-top: 17%;
    margin-right: 35%;
    margin-left: 35%;
    margin-bottom: 0px;
  }

  .bot-card-description {
    color: white;
    opacity: $link-opacity;
    width: 90%;
    min-width: 90%;
    max-width: 90%;
    margin: 0 5%;
    height: 105px;
    text-overflow: ellipsis;
    min-height: 105px;
    max-height: 105px;
  }

  :global(.bot-card-cert) {
    color: #7289da;
    position: absoulute;
    margin-top: -15px;
    margin-left: 90%;
    z-index: 10 !important;
  }
  .bot-card-footer {
    width: 80%;
    margin: 0 10%;
    height: 10%;
    margin-top: 20px;
    margin-bottom: 20px;
  }

  .bot-card-footer-stats {
    height: 30px !important;
    width: 55% !important;
  }

  .bot-card-actions {
    width: 80%;
    margin: 0 15%;
  }

  .bot-card-banner {
    background: var(--background) no-repeat;
    background-size: 100% 100%;
    height: 190px;
    width: 100%;
    z-index: 10;
  }

  .bot-card-banner.lazy {
    background-image: none;
    background-color: #f1f1fa;
  }
</style>
