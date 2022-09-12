<script context="module">
  /** @type {import('@sveltejs/kit').ErrorLoad} */
  import { apiUrl, electroUrl } from '$lib/config';
  import { checkAdminSession } from '$lib/request';
  export const prerender = false;
  export async function load({ session }) {
    let id = '0';
    if (session.session.token) {
      id = session.session.user.id;
    }
    let permsRes = await fetch(`${apiUrl}/baypaw/perms/${id}`);

    let perms = await permsRes.json();

    if (perms.perm < 2) {
      return {
        status: 401,
        error: new Error('You are not a staff member.')
      };
    }

    if (!session.adminData) {
      return {
        status: 307,
        redirect: `/quailfeather/admin/login?redirect=/quailfeather/admin`
      };
    }

    let sessionCheck = await checkAdminSession(
      session.session.user.id,
      session.session.token,
      session.adminData
    );

    if (!sessionCheck) {
      return {
        status: 307,
        redirect: `/quailfeather/admin/login?redirect=/quailfeather/admin`
      };
    }

    let schema = await fetch(`${electroUrl}/ap/schema`);

    if (!schema.ok) {
      let json = await schema.json();
      return {
        status: 401,
        error: new Error(JSON.stringify(json))
      };
    }

    let schemaResp = await schema.json();

    let allowedTables = await fetch(
      `${electroUrl}/ap/schema/allowed-tables?user_id=${session.session.user.id}`,
      {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          Authorization: session.session.token
        }
      }
    );

    if (!allowedTables.ok) {
      let json = await allowedTables.json();
      return {
        status: 401,
        error: new Error(JSON.stringify(json))
      };
    }

    let allowedTablesResp = await allowedTables.json();

    // Get all tables
    let tables = new Map();
    let tableList = [];

    let pub = allowedTablesResp.length == 0;

    schemaResp.forEach((el) => {
      if (!tables.has(el.table_name)) {
        tables.set(el.table_name, []);
        if (pub) {
          allowedTablesResp.push(el.table_name);
        }
      }
      tables.get(el.table_name).push(el);
    });

    return {
      props: {
        perms: perms,
        allowedTables: allowedTablesResp,
        tables: tables
      }
    };
  }
</script>

<script lang="ts">
  // https://stackoverflow.com/a/46959528
  const title = (str: string) => {
    return str.replaceAll('_', ' ').replace(/(^|\s)\S/g, (t) => {
      return t.toUpperCase();
    });
  };

  import QuailTree from '../_helpers/QuailTree.svelte';
  export let perms: any;
  export let allowedTables: any;
  export let tables: any;
  import Button from '$lib/base/Button.svelte';
  import Section from '$lib/base/Section.svelte';
</script>

<QuailTree perms={perms.perm}>
  <Section id="Allowed Tables" title="Allowed Tables" icon="fluent:thinking-24-regular">
    <div class="mx-2">
      <h2>Here are the tables you are allowed to edit!</h2>
      {#each [...tables] as [tableName, _]}
        {#if allowedTables == null || allowedTables.includes(tableName)}
          <li><a href="#{tableName}">{title(tableName)}</a></li>
        {/if}
      {/each}
    </div>
  </Section>

  <div class="seperate" />

  <Section id="Tables" title="Tables" icon="fluent:thinking-24-regular">
    <div class="mx-2">
      {#each [...tables] as [tableName, table]}
        <fieldset>
          <legend id={tableName}>{title(tableName)}</legend>
          {#if allowedTables == null || allowedTables.includes(tableName)}
            <h3>You are allowed to edit this table</h3>
            <Button
              onclick={() => {}}
              id="edit-table-{tableName}"
              class="button"
              href={`/quailfeather/admin/table/${tableName}`}>Edit Table</Button
            >
          {:else}
            <h3>You are not allowed to edit this table</h3>
          {/if}
          <h4>Columns</h4>
          <ul>
            {#each table as column}
              <li>{column.column_name}</li>
            {/each}
          </ul>
        </fieldset>

        <div class="seperate" />
      {/each}
    </div>
  </Section>
</QuailTree>

<style>
  ul {
    color: white !important;
  }

  .seperate {
    padding: 15px;
  }

  fieldset {
    border-radius: 6px;
    overflow-y: scroll;
  }

  legend {
    font-family: 'Fira Code', monospace;
    color: white;
    font-weight: bold;
  }
</style>
