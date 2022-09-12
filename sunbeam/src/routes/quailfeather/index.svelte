<script lang="ts" context="module">
  import { fetchFates } from '$lib/request';
  import { apiUrl, lynxUrl } from '$lib/config';
  export const prerender = false;
  export async function load({ params, url, fetch, session, stuff }) {
    const res = await fetchFates('/stats', '', fetch, false, true);
    if (res.ok) {
      let id = '0';
      if (session.session.token) {
        id = session.session.user.id;
      }
      let perms = await fetch(`${apiUrl}/baypaw/perms/${id}`);
      return {
        props: {
          data: await res.json(),
          perms: await perms.json()
        }
      };
    } else {
      return {
        status: res.status,
        error: new Error(`Could not load ${url}`)
      };
    }
  }
</script>

<script lang="ts">
  import BotCard from '$lib/cards/BotCard.svelte';
  import CardContainer from '$lib/cards/CardContainer.svelte';
  import Section from '$lib/base/Section.svelte';
  import { enums } from '$lib/enums/enums';
  import Button from '$lib/base/Button.svelte';
  import { session } from '$app/stores';
  import { genError } from '$lib/strings';
  import QuailTree from './_helpers/QuailTree.svelte';
  import Tip from '$lib/base/Tip.svelte';
  import FormInput from '$lib/base/FormInput.svelte';
  export let data: any;
  export let perms: any;

  let approvedBots = [];
  let bannedBots = [];
  let deniedBots = [];
  let pendingBots = [];
  let certifiedBots = [];
  let underReviewBots = [];
  let miscBots = [];

  for (let i = data.bots.length; i--; i >= 0) {
    let bot = data.bots[i];
    switch (bot.state) {
      case enums.BotState.denied:
        deniedBots.push(bot);
        break;
      case enums.BotState.banned:
        bannedBots.push(bot);
        break;
      case enums.BotState.certified:
        certifiedBots.push(bot);
        break;
      case enums.BotState.pending:
        pendingBots.push(bot);
        break;
      case enums.BotState.under_review:
        underReviewBots.push(bot);
        break;
      case enums.BotState.approved:
        approvedBots.push(bot);
        break;
      default:
        miscBots.push(bot);
        break;
    }
  }

  let cache = {
    approved: approvedBots,
    banned: bannedBots,
    denied: deniedBots,
    pending: pendingBots,
    certified: certifiedBots,
    underReview: underReviewBots
  };

  // Ensure browsers dont crash trying to render 500 bots
  const MAX_RENDER = 20;

  deniedBots = deniedBots.slice(0, MAX_RENDER);
  bannedBots = bannedBots.slice(0, MAX_RENDER);
  pendingBots = pendingBots.slice(0, MAX_RENDER);
  approvedBots = approvedBots.slice(0, MAX_RENDER);
  underReviewBots = underReviewBots.slice(0, MAX_RENDER);
  certifiedBots = certifiedBots.slice(0, MAX_RENDER);

  const searchSection = (e, dataSource) => {
    let search = e.target.value.toLowerCase();
    if (!search) {
      return dataSource.slice(0, MAX_RENDER);
    }
    let filtered = [];
    for (let i = dataSource.length; i--; i >= 0) {
      let bot = dataSource[i];
      if (bot.user.username.toLowerCase().includes(search) || bot.user.id.includes(search)) {
        filtered.push(bot);
      }
    }
    return filtered.slice(0, MAX_RENDER);
  };

  const secondsToDhms = (seconds) => {
    seconds = Number(seconds);
    const d = Math.floor(seconds / (3600 * 24));
    const h = Math.floor((seconds % (3600 * 24)) / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = Math.floor(seconds % 60);

    const dDisplay = d > 0 ? d + (d == 1 ? ' day, ' : ' days, ') : '';
    const hDisplay = h > 0 ? h + (h == 1 ? ' hour, ' : ' hours, ') : '';
    const mDisplay = m > 0 ? m + (m == 1 ? ' minute, ' : ' minutes, ') : '';
    const sDisplay = s > 0 ? s + (s == 1 ? ' second' : ' seconds') : '';
    return `${dDisplay} ${hDisplay} ${mDisplay} ${sDisplay}`;
  };

  const claimBot = async (id: string) => {
    handler(id, 'STUB_REASON', 'claim');
  };

  const unclaimBot = async (id: string) => {
    alert({
      title: 'Reason',
      id: 'feedback-msg',
      message: "Please always unclaim when you can't review them",
      type: enums.AlertType.Prompt,
      validate: (value) => {
        if (value.toSingleLine().length < 5) {
          return 'Reason must be at least 5 characters';
        }
      },
      input: {
        label: 'Reason',
        placeholder: 'Reason for unclaim',
        multiline: false,
        function: (value) => {
          handler(id, value.toString(), 'unclaim');
        }
      }
    });
  };

  const approveBot = async (id: string) => {
    alert({
      title: 'Feedback',
      id: 'feedback-msg',
      message: 'Please carefully review bots before approving them',
      type: enums.AlertType.Prompt,
      validate: (value) => {
        if (value.toSingleLine().length < 5) {
          return 'Reason must be at least 5 characters';
        }
      },
      input: {
        label: 'Feedback',
        placeholder: 'Why is this bot being approved',
        multiline: false,
        function: (value) => {
          handler(id, value.toString(), 'approve', null, (res) => {
            const url = `https://discord.com/api/oauth2/authorize?client_id=${id}&scope=bot%20applications.commands&guild_id=${res.guild_id}`;
            window.open(url, '_blank');
          });
        }
      }
    });
  };

  const denyBot = async (id: string) => {
    alert({
      title: 'Reason',
      id: 'reason-msg',
      message: 'Please do not deny for spurious reasons',
      type: enums.AlertType.Prompt,
      validate: (value) => {
        if (value.toSingleLine().length < 5) {
          return 'Reason must be at least 5 characters';
        }
      },
      input: {
        label: 'Reason',
        placeholder: 'Why is this bot being denied',
        multiline: false,
        function: (value) => {
          handler(id, value.toString(), 'deny');
        }
      }
    });
  };

  const banBot = async (id: string) => {
    alert({
      title: 'Reason',
      id: 'reason-msg',
      message: 'Please do not ban for spurious reasons',
      type: enums.AlertType.Prompt,
      validate: (value) => {
        if (value.toSingleLine().length < 5) {
          return 'Reason must be at least 5 characters';
        }
      },
      input: {
        label: 'Reason',
        placeholder: 'Why is this bot being banned?',
        multiline: false,
        function: (value) => {
          handler(id, value.toString(), 'ban');
        }
      }
    });
  };

  const unbanBot = async (id: string) => {
    alert({
      title: 'Reason',
      id: 'reason-msg',
      message: 'Please do not unban for spurious reasons',
      type: enums.AlertType.Prompt,
      validate: (value) => {
        if (value.toSingleLine().length < 5) {
          return 'Reason must be at least 5 characters';
        }
      },
      input: {
        label: 'Reason',
        placeholder: 'Why is this bot being unbanned?',
        multiline: false,
        function: (value) => {
          handler(id, value.toString(), 'unban');
        }
      }
    });
  };

  const unverifyBot = async (id: string) => {
    alert({
      title: 'Reason',
      id: 'reason-msg',
      message: 'Please do not unverify for spurious reasons',
      type: enums.AlertType.Prompt,
      validate: (value) => {
        if (value.toSingleLine().length < 5) {
          return 'Reason must be at least 5 characters';
        }
      },
      input: {
        label: 'Reason',
        placeholder: 'Why is this bot being unverify?',
        multiline: false,
        function: (value) => {
          handler(id, value.toString(), 'unverify');
        }
      }
    });
  };

  const requeueBot = async (id: string) => {
    alert({
      title: 'Reason',
      id: 'reason-msg',
      message: 'Please do not requeue for spurious reasons',
      type: enums.AlertType.Prompt,
      validate: (value) => {
        if (value.toSingleLine().length < 5) {
          return 'Reason must be at least 5 characters';
        }
      },
      input: {
        label: 'Reason',
        placeholder: 'Why is this bot being requeued?',
        multiline: false,
        function: (value) => {
          handler(id, value.toString(), 'requeue');
        }
      }
    });
  };

  const certifyBot = async (id: string) => {
    alert({
      title: 'Feedback',
      id: 'reason-msg',
      message: 'Before certifing, make sure you have reviewed the bot to meet the requirements',
      type: enums.AlertType.Prompt,
      validate: (value) => {
        if (value.toSingleLine().length < 5) {
          return 'Reason must be at least 5 characters';
        }
      },
      input: {
        label: 'Feedback',
        placeholder: 'Why is this bot being certified/Any feedback?',
        multiline: false,
        function: (value) => {
          handler(id, value.toString(), 'certify');
        }
      }
    });
  };

  const uncertifyBot = async (id: string) => {
    alert({
      title: 'Reason',
      id: 'reason-msg',
      message: 'Please do not uncertify for spurious reasons',
      type: enums.AlertType.Prompt,
      validate: (value) => {
        if (value.toSingleLine().length < 5) {
          return 'Reason must be at least 5 characters';
        }
      },
      input: {
        label: 'Reason',
        placeholder: 'Why is this bot being uncertified?',
        multiline: false,
        function: (value) => {
          handler(id, value.toString(), 'uncertify');
        }
      }
    });
  };

  const resetBotVotes = async (id: string) => {
    alert({
      title: 'Reason',
      id: 'reason-msg',
      message: 'Please do not reset bot votes for spurious reasons',
      type: enums.AlertType.Prompt,
      validate: (value) => {
        if (value.toSingleLine().length < 5) {
          return 'Reason must be at least 5 characters';
        }
      },
      input: {
        label: 'Reason',
        placeholder: 'Why are the votes of this bot being reset?',
        multiline: false,
        function: (value) => {
          handler(id, value.toString(), 'reset-votes');
        }
      }
    });
  };

  const resetAllVotes = async () => {
    alert({
      title: 'Reason',
      id: 'reason-msg',
      message: 'Please do not reset all bot votes for spurious reasons',
      type: enums.AlertType.Prompt,
      validate: (value) => {
        if (value.toSingleLine().length < 5) {
          return 'Reason must be at least 5 characters';
        }
      },
      input: {
        label: 'Reason',
        placeholder: 'Why are the votes of all bots being reset? Defaults to Monthly Votes Reset',
        multiline: false,
        required: false,
        function: (value) => {
          handler('0', value.toString() || '', 'reset-all-votes');
        }
      }
    });
  };

  const setBotFlag = async (id: string, flag: number) => {
    alert({
      title: 'Reason',
      id: 'reason-msg',
      message: 'Please do not set bot flags for spurious reasons',
      type: enums.AlertType.Prompt,
      validate: (value) => {
        if (value.toSingleLine().length < 5) {
          return 'Reason must be at least 5 characters';
        }
      },
      input: {
        label: 'Reason',
        placeholder: 'Why is this bot being modified?',
        multiline: false,
        function: (value) => {
          handler(id, value.toString(), 'set-flag', flag);
        }
      }
    });
  };

  const handler = async (
    id: string,
    reason: string,
    action: string,
    context: any = null,
    followup: (res) => void = null
  ) => {
    if (!reason) {
      return;
    }

    let res = await fetch(`${lynxUrl}/kitty`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: $session.session.token
      },
      body: JSON.stringify({
        id: id,
        reason: reason,
        action: action,
        user_id: $session.session.user.id,
        context: context
      })
    });

    if (res.ok) {
      alert({
        title: 'Success',
        id: 'success-msg',
        message: genError(await res.json()),
        type: enums.AlertType.Success,
        close: () => {
          window.location.reload();
        }
      });
      if (followup) {
        followup(await res.json());
      }
    } else {
      alert({
        title: 'Error',
        id: 'error-msg',
        message: genError(await res.json()),
        type: enums.AlertType.Error
      });
    }
  };

  enum permData {
    USER = 1,
    BOT_REVIEWER = 2,
    MODERATOR = 3,
    ADMIN = 4,
    DEVELOPER = 5,
    HEAD_ADMIN = 6,
    OVERSEER = 7
  }

  const minPerm = (perm: permData) => {
    return `${perm} (${permData[perm]})`;
  };

  function queryToInpEl(q: string): HTMLInputElement {
    return document.querySelector(q);
  }
</script>

<QuailTree perms={perms.perm}>
  <h1>Admin Statistics</h1>
  <ul class="white" style="font-size: 24px">
    <li>Server Uptime: {secondsToDhms(data.uptime)} ({data.uptime})</li>
    <li>Queue Length: {cache.pending.length}</li>
    <li>Under Review Length: {cache.underReview.length}</li>
    <li>Total Bot Length: {data.total_bots}</li>
    <li>Approved or Certified Bot Length: {cache.approved.length + cache.certified.length}</li>
    <li>Certified Bots Length: {cache.certified.length}</li>
    <li>Banned Bots Length: {cache.banned.length}</li>
    <li>Denied Bots Length: {cache.denied.length}</li>
  </ul>

  <div class="mx-2">
    <Tip>
      The list of bots rendered is currently limited to {MAX_RENDER} (to protect your browser from crashing
      due to too many rendered dom nodes).<br /><br />

      You can use the Search bar to look for a bot based on its ID or name. This works even if it is
      not rendered

      <br /><br /><br />
      Support for server rendering is coming soon (TM)
    </Tip>
  </div>

  <Section icon="fa-solid:plus" title="Queue" id="queue">
    <div class="mx-2">
      <div class="search-flex">
        <input
          class="search-bots"
          placeholder="Search..."
          on:input={(e) => {
            pendingBots = searchSection(e, cache.pending);
          }}
        />
      </div>
    </div>
    <CardContainer>
      {#each pendingBots as bot}
        <BotCard data={bot} type="bot" rand={false}>
          {#if perms.perm > permData.BOT_REVIEWER}
            <div class="flex justify-center">
              <Button
                onclick={() => claimBot(bot.user.id)}
                
                class="button self-center">Claim</Button
              >
            </div>
          {/if}
        </BotCard>
      {/each}
    </CardContainer>
  </Section>

  <div class="seperate" />

  <Section icon="fluent:thinking-24-regular" title="Under Review" id="under-review">
    <div class="mx-2">
      <div class="search-flex">
        <input
          class="search-bots"
          placeholder="Search..."
          on:input={(e) => {
            underReviewBots = searchSection(e, cache.underReview);
          }}
        />
      </div>
    </div>
    <CardContainer>
      {#each underReviewBots as bot}
        <BotCard data={bot} type="bot" rand={false}>
          {#if perms.perm > permData.BOT_REVIEWER}
            <div class="flex justify-center">
              <Button
                onclick={() => unclaimBot(bot.user.id)}
                
                class="button self-center lb">Unclaim</Button
              >
              <Button
                onclick={() => approveBot(bot.user.id)}
                
                class="button self-center lb">Approve</Button
              >
              <Button
                onclick={() => denyBot(bot.user.id)}
                
                class="button self-center lb">Deny</Button
              >
            </div>
          {/if}
        </BotCard>
      {/each}
    </CardContainer>
  </Section>

  <div class="seperate" />

  <Section icon="fa-solid:certificate" title="Certified" id="certified">
    <div class="mx-2">
      <div class="search-flex">
        <input
          class="search-bots"
          placeholder="Search..."
          on:input={(e) => {
            certifiedBots = searchSection(e, cache.certified);
          }}
        />
      </div>
    </div>
    <CardContainer>
      {#each certifiedBots as bot}
        <BotCard data={bot} type="bot" rand={false}>
          {#if perms.perm >= permData.HEAD_ADMIN}
            <div class="flex justify-center">
              <Button
                onclick={() => uncertifyBot(bot.user.id)}
                
                class="button self-center">Uncertify</Button
              >
            </div>
          {/if}
        </BotCard>
      {/each}
    </CardContainer>
  </Section>

  <div class="seperate" />

  <Section icon="bi:hammer" title="Banned Bots" id="banned">
    <div class="mx-2">
      <div class="search-flex">
        <input
          class="search-bots"
          placeholder="Search..."
          on:input={(e) => {
            bannedBots = searchSection(e, cache.banned);
          }}
        />
      </div>
    </div>
    <CardContainer>
      {#each bannedBots as bot}
        <BotCard data={bot} type="bot" rand={false}>
          <div class="flex justify-center">
            {#if perms.perm >= permData.ADMIN}
              <Button
                onclick={() => unbanBot(bot.user.id)}
                
                class="button self-center lb">Unban</Button
              >
            {/if}

            {#if perms.perm >= permData.MODERATOR}
              <Button
                onclick={() => requeueBot(bot.user.id)}
                
                class="button self-center lb">Requeue</Button
              >
            {/if}
          </div>
        </BotCard>
      {/each}
    </CardContainer>
  </Section>

  <div class="seperate" />

  <Section icon="akar-icons:cross" title="Denied Bots" id="denied">
    <div class="mx-2">
      <div class="search-flex">
        <input
          class="search-bots"
          placeholder="Search..."
          on:input={(e) => {
            deniedBots = searchSection(e, cache.denied);
          }}
        />
      </div>
    </div>
    <CardContainer>
      {#each deniedBots as bot}
        <BotCard data={bot} type="bot" rand={false}>
          {#if perms.perm >= permData.MODERATOR}
            <div class="flex justify-center">
              <Button
                onclick={() => requeueBot(bot.user.id)}
                
                class="button self-center">Requeue</Button
              >
            </div>
          {/if}
        </BotCard>
      {/each}
    </CardContainer>
  </Section>

  <div class="seperate" />

  <Section icon="fa:check" title="Approved Bots" id="approved">
    <div class="mx-2">
      <div class="search-flex">
        <input
          class="search-bots"
          placeholder="Search..."
          on:input={(e) => {
            approvedBots = searchSection(e, cache.approved);
          }}
        />
      </div>
    </div>
    <CardContainer>
      {#each approvedBots as bot}
        <BotCard data={bot} type="bot" rand={false}>
          <div class="flex justify-center">
            {#if perms.perm >= permData.MODERATOR}
              <Button
                onclick={() => unverifyBot(bot.user.id)}
                
                class="button self-center lb">Unverify</Button
              >
            {/if}

            {#if perms.perm >= permData.DEVELOPER}
              <Button
                onclick={() => certifyBot(bot.user.id)}
                
                class="button self-center lb">Certify</Button
              >
            {/if}

            {#if perms.perm >= permData.ADMIN}
              <Button
                onclick={() => banBot(bot.user.id)}
                
                class="button self-center lb">Ban</Button
              >
            {/if}
          </div>
        </BotCard>
      {/each}
    </CardContainer>
  </Section>

  <div class="seperate" />

  <Section icon="fa-solid:robot" title="Definitions" id="definitions">
    <h2>How to use</h2>
    <ol>
      <li>Find the initial state of the item you wish to handle</li>
      <li>
        From the initial state, trace out a route from said initial state to the final desired state
      </li>
      <li>???</li>
      <li>Profit!</li>
    </ol>
    <h2>Bot Actions</h2>
    <ul class="ba-defs">
      <li>
        Claim (claim): pending => under_review<br />
        <!--Impl-->
        <ul>
          <li>Minimum Perm: {minPerm(permData.BOT_REVIEWER)}</li>
        </ul>
      </li>
      <li>
        Unclaim (unclaim): under_review => pending<br />
        <!--Impl-->
        <ul>
          <li>Minimum Perm: {minPerm(permData.BOT_REVIEWER)}</li>
        </ul>
      </li>
      <li>
        Approve (approve): under_review => approved<br />
        <!--Impl-->
        <ul>
          <li>Minimum Perm: {minPerm(permData.BOT_REVIEWER)}</li>
        </ul>
      </li>
      <li>
        Deny (deny): under_review => denied<br />
        <!--Impl-->
        <ul>
          <li>Minimum Perm: {minPerm(permData.BOT_REVIEWER)}</li>
        </ul>
      </li>
      <li>
        Ban (ban): approved => banned<br />
        <!--Impl-->
        <ul>
          <li>Minimum Perm: {minPerm(permData.ADMIN)}</li>
        </ul>
      </li>
      <li>
        Unban (unban): banned => approved<br />
        <!--Impl-->
        <ul>
          <li>Minimum Perm: {minPerm(permData.ADMIN)}</li>
        </ul>
      </li>
      <li>
        Certify (certify): approved => certified<br />
        <!--Impl-->
        <ul>
          <li>Minimum Perm: {minPerm(permData.DEVELOPER)}</li>
        </ul>
      </li>
      <li>
        Uncertify (uncertify): certified => approved<br />
        <!--Impl-->
        <ul>
          <li>Minimum Perm: {minPerm(permData.DEVELOPER)}</li>
        </ul>
      </li>
      <li>
        Unverify (unverify): approved => under_review<br />
        <!--Impl-->
        <ul>
          <li>Minimum Perm: {minPerm(permData.MODERATOR)}</li>
        </ul>
      </li>
      <li>
        Requeue (requeue): denied | banned => under_review<br />
        <!--Impl-->
        <ul>
          <li>Minimum Perm: {minPerm(permData.MODERATOR)}</li>
        </ul>
      </li>
      <li>
        Reset Votes (reset-votes): votes => 0<br />
        <ul>
          <li>Minimum Perm: {minPerm(permData.MODERATOR)}</li>
        </ul>
      </li>
      <li>
        Reset All Votes (reset-all-votes): votes => 0 %all%<br />
        <ul>
          <li>Minimum Perm: {minPerm(permData.DEVELOPER)}</li>
        </ul>
      </li>
      <li>
        Set/Unset Bot Flag (setflag): flag => flags.intersection(flag)<br />
        <!---->
        <ul>
          <li>Minimum Perm: {minPerm(permData.MODERATOR)}</li>
        </ul>
      </li>
    </ul>

    {#if perms.perm >= permData.MODERATOR}
      <h2>Set/Unset Bot Flags</h2>
      <FormInput id="bot-id-setflag" name="Bot ID" placeholder="Enter Bot ID here" />
      <select id="bot-flag">
        <option value="" disabled aria-disabled="true">Select a flag</option>
        {#each Object.keys(enums.Flags).filter((k) => !parseInt(k) && parseInt(k) != 0) as flag, i}
          <option value={i}>{flag} ({i}, may be inaccurate, always check this number)</option>
        {/each}
      </select>
      <Button
        class="button"
        
        onclick={() => {
          let flag = parseInt(queryToInpEl('#bot-flag').value);
          let id = queryToInpEl('#bot-id-setflag').value;
          setBotFlag(id, flag);
        }}>Set Flag</Button
      >

      <h2>Reset Bot Votes</h2>
      <FormInput id="bot-id-rbv" name="Bot ID" placeholder="Enter Bot ID here" />
      <Button
        class="button"
        
        onclick={() => {
          let id = queryToInpEl('#bot-id-rbv').value;
          resetBotVotes(id);
        }}>Reset</Button
      >
    {/if}

    {#if perms.perm >= permData.HEAD_ADMIN}
      <h2>Reset All Bot Votes</h2>
      <Button
        class="button"
        
        onclick={() => {
          resetAllVotes();
        }}>Reset</Button
      >
    {/if}
  </Section>
</QuailTree>

<style>
  :global(.lb) {
    margin-left: 2px;
  }

  .ba-defs > li {
    margin-bottom: 5px;
  }

  ul {
    list-style: none;
  }

  li {
    color: white !important;
    padding-bottom: 5px;
  }

  .search-flex {
    display: flex;
    flex-wrap: wrap;
  }

  .seperate {
    padding: 20px;
  }

  .search-bots {
    background: #444;
    padding: 0 20px;
    border: none;
    border-radius: 4px;
    color: #ffffff;
    height: 30px;
    margin: 0 !important;
    width: 100% !important;
    overflow-x: hidden !important;
  }

  .search-bots::placeholder {
    color: #ffffff;
    font-weight: bold;
  }
</style>
