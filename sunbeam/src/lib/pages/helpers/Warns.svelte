<script lang="ts">
  export let data: any;
  import { enums } from '$lib/enums/enums';
</script>

<div class="accordion-container">
  <div class="accordian">
    {#if enums.helpers.flagCheck(enums.Flags.system, data.flags)}
      <div class="panel" color="secondary" open>
        <h3 class="header">System Bot</h3>
        <p class="content accordian-container">
          This bot is a system bot and was added as a placeholder to avoid malicious use of your
          bot. If you are the bots owner, please either edit your bot setting System to False if
          available or contact Fates List Support to claim the bot. To avoid misinformation and
          false advertising, the actual owner of the bot is listed in About who may edit their bot
          if they wish to change anything on it.

          <em>System gots cannot be voted for until claimed</em>
        </p>
      </div>
    {/if}
    {#if data.state == enums.BotState.denied}
      <div class="panel" color="primary" open>
        <h3 class="header">Bot Denied</h3>
        <p class="content accordian-container">
          This bot has been DENIED from this list for being a low-quality bot. Please do not invite
          it.
        </p>
      </div>
    {:else if data.state == enums.BotState.banned}
      <div class="panel" color="primary" open>
        <h3 class="header">Bot Banned</h3>
        <p class="content accordian-container">
          This bot has been BANNED from this bot list for violating our rules or being a low-quality
          bot. Please do not invite it until further notice!
        </p>
      </div>
    {:else if data.state == enums.BotState.pending}
      <div class="panel" color="secondary" open>
        <h3 class="header">Bot Pending Review</h3>
        <p class="content accordian-container">
          This bot has not yet been tested and may be low quality or malicious. Please do not invite
          it yet
        </p>
      </div>
    {:else if data.state == enums.BotState.under_review}
      <div class="panel" color="secondary" open>
        <h3 class="header">Bot Under Review</h3>
        <p class="content accordian-container">
          This bot is currently being tested, Expect to hear from us soon!
        </p>
      </div>
    {/if}
  </div>
</div>
