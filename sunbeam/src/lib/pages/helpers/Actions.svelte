<script lang="ts">
  import { session } from '$app/stores';
  import alertstore from '$lib/alertstore';
  import Tag from '$lib/base/Tag.svelte';

  import { nextUrl } from '$lib/config';

  import { enums } from '$lib/enums/enums';
  import loadstore from '$lib/loadstore';
  import navigationState from '$lib/navigationState';
  import { voteHandler } from '$lib/request';
  import { genError } from '$lib/strings';
  import Icon from '@iconify/svelte';
  import Button from '$lib/base/Button.svelte';

  export let data: any;
  export let type: string;
  export let limited = false;

  async function voteBot() {
    let token = $session.session.token;
    let userID = '';
    if (token) {
      userID = $session.session.user.id;
    }
    $loadstore = 'Voting...';
    $navigationState = 'loading';
    let res = await voteHandler(userID, token, data.user.id, false, type);
    let jsonDat = await res.json();
    if (res.ok) {
      alert({
        title: 'Successful Vote',
        message: `
Successfully voted for this ${type}!

<em>Pro Tip</em>: You can vote for ${type} directly on your server using Fates List Helper. Fates List Helper also supports vote reminders as well!

You can invite Fates List Helper to your server by <a style="color: blue !important" href="https://discord.com/api/oauth2/authorize?client_id=811073947382579200&permissions=2048&scope=bot%20applications.commands">clicking here</a>!

If you have previously invited Squirrelflight, please remove and add Fates List Helper instead.
`,
        id: 'alert',
        type: enums.AlertType.Success
      });
    } else {
      alert({
        show: true,
        title: 'Oops :(',
        message: genError(jsonDat),
        id: 'alert',
        type: enums.AlertType.Error
      });
    }
    $navigationState = 'loaded';
  }

  let extLinks = [];

  for (const [key, value] of Object.entries(data.extra_links)) {
    if (key.startsWith('_')) {
      // Field is meant for custom clients only
      continue;
    }
    extLinks.push({
      name: key,
      id: key,
      href: value
    });
  }
</script>

<span class="auxillary" />
<div class="buttons">
  <Button
    onclick={() => voteBot()}
    class="buttons-all button"
    id="buttons-vote"
    touch
    
  >
    <Icon icon="fa-solid:thumbs-up" inline={false} />
    <span style="margin-left: 3px;"><strong>{data.votes}</strong></span>
  </Button>
  <Button
    href="/{type}/{data.user.id}/invite"
    class="buttons-all button"
    id="buttons-invite"
    touch
    
    onclick={() => {}}
  >
    <span
      ><strong
        >{#if type == 'server'}Join{:else}Invite{/if}</strong
      ></span
    >
  </Button>
  {#if $session.session.token && $session.session.user_experiments.includes(enums.UserExperiments.BotReport)}
    <Button
      onclick={() => {
        alert({
          title: `Report this ${type}`,
          message: `
Oh, we're sorry you are having an issue with this ${type}. 
        
Before you report, have you tried contacting the owner of this ${type} if possible?

If you still wish to report, type the reason for reporting this ${type} below. Reports are <em>not</em> automated by Fates List and as such may take time to process.`,
          input: {
            label: 'Reason for reporting and proof',
            placeholder: `Be sure to have proof of why you're reporting!`,
            multiline: true,
            function: async (value) => {
              const res = await fetch(
                `${nextUrl}/users/${$session.session.user.id}/${type}s/${data.user.id}/appeal`,
                {
                  method: 'POST',
                  headers: {
                    'Content-Type': 'application/json',
                    Frostpaw: '0.1.0',
                    Authorization: $session.session.token
                  },
                  body: JSON.stringify({
                    request_type: 2, // 2 means report
                    appeal: value.toString()
                  })
                }
              );
              if (res.ok) {
                alert(`Successfully reported this ${type}`);
              } else {
                const err = await res.json();
                alert(genError(err));
              }
            }
          }
        });
      }}
      id="buttons-report"
      class="buttons-all button"
      touch
      
    >
      <span><strong>Report</strong></span>
    </Button>
  {/if}
  {#if !limited}
    {#if type == 'bot'}
      <Button
        href="/bot/{data.user.id}/settings"
        id="buttons-settings"
        class="buttons-all auxillary button"
        touch
        
        onclick={() => {}}
      >
        <span><strong>Settings</strong></span>
      </Button>
    {:else}
      <Button
        onclick={() => {}}
        class="buttons-all disabled auxillary"
        id="buttons-settings"
        touch
        
        disabled
      >
        <span><strong>Settings</strong></span>
      </Button>
    {/if}
  {/if}
</div>
{#if extLinks.length > 0 && !limited}
  <div class="links-pane">
    <Tag buttonTag={true} targetType={type} tags={extLinks} />
  </div>
{/if}

<style lang="scss" global>
  .buttons-all {
    background-color: black !important;
    margin-right: 10px;
    color: white !important;
    opacity: 1 !important;
    //min-width: 130px;
    //max-width: 150px;
    word-wrap: break-word !important;
    font-size: 15px !important;
    border: solid 0.1px !important;
  }

  .disabled {
    opacity: 0.63 !important;
  }

  @media screen and (max-width: 992px) {
    .buttons {
      overflow-x: scroll;
      overflow-y: hidden;
      overflow-wrap: break-word !important;
      font-size: 12px !important;
    }
  }

  .buttons {
    word-wrap: break-word;
    text-overflow: ellipsis;
  }

  .buttons {
    margin-bottom: 40px;
  }

  .buttons {
    display: flex;
    flex-flow: column-wrap;
    justify-content: center;
    align-items: center;
    min-width: 93%;
    height: 53px;
    margin: 0 auto;
    /*white-space: nowrap;*/
  }

  @media screen and (max-width: 768px) {
    .buttons {
      margin-left: 10px !important;
      width: 100% !important;
      overflow-wrap: break-word !important;
    }
    .auxillary {
      display: none;
    }
    .mobile-small {
      font-size: 11px !important;
    }
  }

  .links-pane {
    display: flex;
    flex-flow: column-wrap;
    justify-content: center;
    align-items: center;
    min-width: 93%;
  }
</style>
