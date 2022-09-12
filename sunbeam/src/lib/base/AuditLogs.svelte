<script lang="ts">
  import { enums } from '$lib/enums/enums';
  export let logs: any;

  // https://stackoverflow.com/a/46959528
  function title(str: string) {
    return str.replaceAll('_', ' ').replace(/(^|\s)\S/g, function (t) {
      return t.toUpperCase();
    });
  }
</script>

<details>
  <summary>View Public Audit Logs</summary>
  <p class="opaque">
    Warning Agent P! You probably shouldn't be here unless you're solving a crisis!
  </p>
  {#each logs as log}
    <p>
      <span class="opaque">Action</span> <em>{title(enums.UserBotAction[log.action])}</em>
      <span class="opaque">by user (ID)</span> <em>{log.user_id}</em>
      <span class="opaque">at time</span> <em> {log.action_time} </em> <br />
      {#if log.context}
        Context: <span class="opaque">{log.context}</span>
      {/if}
      <details>
        <summary>Raw JSON (for machines and robots!)</summary>
        <code>{JSON.stringify(log)}</code>
      </details>
    </p>
  {/each}
</details>
