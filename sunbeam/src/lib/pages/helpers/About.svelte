<script lang="ts">
  import AuditLogs from '$lib/base/AuditLogs.svelte';

  import Tag from '$lib/base/Tag.svelte';

  import Icon from '@iconify/svelte';
  import Owner from '$lib/base/Owner.svelte';
  import { enums, type TargetType } from '$lib/enums/enums';

  // https://stackoverflow.com/a/46959528
  function title(str: string) {
    return str.replaceAll('_', ' ').replace(/(^|\s)\S/g, function (t) {
      return t.toUpperCase();
    });
  }

  export let data: any;
  export let type: TargetType;

  if (data.shards !== undefined && data.shards.length < 1) {
    data.shards = ["No shards set. Try checking it's website or support server (if it has one)!"];
  }
</script>

{#if type == enums.TargetType.Bot}
  <h2>Owners</h2>
  <Icon icon="mdi-crown" inline={false} height="1.2em" style="margin-right: 1px" />
  {#each data.owners as owner}
    <Owner user={owner.user} />
  {/each}
{:else}
  <h2>Server Owner</h2>
  <Icon icon="mdi-crown" inline={false} height="1.2em" style="margin-right: 1px" />
  <Owner user={data.owner} />
{/if}

{#if type == enums.TargetType.Bot}
  <h2>Admin Actions</h2>
  <a href="/bot/{data.user.id}/settings">Settings</a>
{/if}

<h2>Tags</h2>
<Tag type={type} redirectUser={true} tags={data.tags} modWidth={false} />

{#if type == enums.TargetType.Bot}
  <h2>Uptime</h2>
  <p>Uptime Checks (Total): {data.uptime_checks_total}</p>
  <p>Uptime Checks (Failed): {data.uptime_checks_failed}</p>
  <p>Uptime Checks (Success): {data.uptime_checks_total - data.uptime_checks_failed}</p>
  <p>
    Uptime Checks (Score):
    {#if data.uptime_checks_total}
      {(data.uptime_checks_total - data.uptime_checks_failed) / data.uptime_checks_total}
    {:else}
      Not Available
    {/if}
  </p>

  <h2>Bot Features</h2>
  {#each data.features as feature}
    <p>
      {feature.name}:
      <span class="opaque"
        >{feature.description}.
        <em>According to our community, this feature is {feature.viewed_as}.</em></span
      >
    </p>
  {/each}
{/if}

<h2>Statistics</h2>
<p>Guild Count: {data.guild_count}</p>
<p>User Count (according to {enums.helpers.targetTypeString(type)}): {data.user_count}</p>
{#if type == enums.TargetType.Bot}
  <p>Shard Count: {data.shard_count}</p>
  <p>
    Shards:
    {#each data.shards as shard}
      <span class="white">{shard}</span>,
    {/each}
  </p>
{/if}

<h2>Nerdville</h2>
{#if type == enums.TargetType.Bot}
  <p>Last posted statistics on: {data.last_stats_post}</p>
{/if}
<p>Added to the list on: {data.created_at}</p>
<p>{title(enums.helpers.targetTypeString(type))} Flags: {data.flags}</p>

{#if type == enums.TargetType.Bot}
  <AuditLogs logs={data.action_logs} />
{/if}
