<script lang="ts">
  import { enums } from '../../enums/enums';
  import Section from '$lib/base/Section.svelte';
  import * as logger from '$lib/logger';

  export let data: any;

  // https://stackoverflow.com/a/46959528
  function title(str: string) {
    return str.replaceAll('_', ' ').replace(/(^|\s)\S/g, function (t) {
      return t.toUpperCase();
    });
  }

  let groupedCmds = new Map();
  let groups = new Map();

  data.commands.forEach((el) => {
    // Insert each command into the correct group
    el.groups.forEach((group) => {
      if (!group) {
        return;
      }

      if (group == 'default') {
        group = 'Uncategorized';
      }

      let groupId = group.replaceAll(',', '').replaceAll(' ', '').toLowerCase();
      groups.set(groupId, title(group));
      if (groupedCmds.has(groupId)) {
        groupedCmds.get(groupId).push(el);
      } else {
        groupedCmds.set(groupId, [el]);
      }
    });
  });

  logger.info('Commands', 'Parsed commands', { groupedCmds });
</script>

{#if groupedCmds.size == 0}
  <h3>This bot does not have any commands</h3>
  {#if !data.prefix}
    <h4>This bot uses slash commands, try typing / to see a list of commands</h4>
  {/if}
{/if}
{#each [...groupedCmds] as [cmd_group, cmds]}
  <Section icon={'bx:command'} id={cmd_group} title={title(groups.get(cmd_group))}>
    <table id="{cmd_group}-table" class="commands-table rules-all">
      <tr>
        <th class="commands-header">Command</th>
        <th class="commands-header">Type</th>
        <th class="commands-header">Description</th>
        <th class="commands-header">Notes</th>
        <th class="commands-header">Groups</th>
      </tr>
      {#each cmds as cmd}
        <tr>
          <td class="commands-item"
            >{data.prefix || '/'}{cmd['name']}
            <span class="opaque">{cmd['args'].join(' | ')}</span></td
          >
          <td class="commands-item">{enums.CommandType[cmd['cmd_type']]}</td>
          <td class="commands-item">{cmd['description']}</td>
          <td class="commands-item">
            <ul class="command-group-list">
              {#if cmd['vote_locked']}
                <li>Requires Voting (vote-locked)</li>
              {/if}
              {#if cmd['premium_only']}
                <li>Premium Only</li>
              {/if}
              {#each cmd['notes'] as note}
                <li>{note}</li>
              {/each}
            </ul>
          </td>
          <td class="commands-item">
            <ul class="command-group-list">
              {#each cmd['groups'] as group}
                <li>{title(group)}</li>
              {/each}
            </ul>
          </td>
        </tr>
      {/each}
    </table>
  </Section>
{/each}

<style>
  .commands-table,
  .commands-item,
  .commands-header {
    padding: 1rem;
  }
  .command-group-list {
    padding: 0;
    margin: 0;
    list-style-type: none !important;
  }
</style>
