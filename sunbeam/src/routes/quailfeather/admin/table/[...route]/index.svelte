<script context="module">
  /** @type {import('@sveltejs/kit').ErrorLoad} */
  import { apiUrl, lynxUrl, electroUrl } from '$lib/config';
  import { checkAdminSession } from '$lib/request';
  import { browser } from '$app/env';
  export const prerender = false;
  export async function load({ params, session }) {
    let id = '0';
    if (session.session.token) {
      id = session.session.user.id;
    }
    let perms = await fetch(`${apiUrl}/baypaw/perms/${id}`);

    let permsResp = await perms.json();

    if (permsResp.perm < 2) {
      return {
        status: 401,
        error: new Error('You are not a staff member.')
      };
    }

    if (!session.adminData) {
      return {
        status: 307,
        redirect: `/quailfeather/admin/login?redirect=/quailfeather/admin/table/${params.route}`
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
        redirect: `/quailfeather/admin/login?redirect=/quailfeather/admin/table/${params.route}`
      };
    }

    let schema = await fetch(`${electroUrl}/ap/schema?table_name=${params.route}`);

    if (!schema.ok) {
      let json = await schema.json();
      return {
        status: 401,
        error: new Error(JSON.stringify(json))
      };
    }

    let schemaResp = await schema.json();

    // Get order from schema
    let schemaOrder = [];

    let secrets = [];

    for (let i = 0; i < schemaResp.length; i++) {
      if (schemaResp[i].secret) {
        secrets.push(schemaResp[i].column_name); // Do not show secret data
        continue;
      }
      schemaOrder.push(schemaResp[i].column_name);
    }

    logger.info('AdminPanel', schemaOrder);

    // Get cols
    let cols = await fetch(
      `${electroUrl}/ap/tables/${params.route}?user_id=${session.session.user.id}`,
      {
        method: 'GET',
        headers: {
          'Frostpaw-ID': session.adminData,
          Authorization: session.session.token
        }
      }
    );

    if (!cols.ok) {
      let json = await cols.json();
      return {
        status: 401,
        error: new Error(JSON.stringify(json))
      };
    }

    let colsResp = await cols.json();

    let count = await fetch(
      `${electroUrl}/ap/tables/${params.route}?user_id=${session.session.user.id}&count=true`,
      {
        method: 'GET',
        headers: {
          'Frostpaw-ID': session.adminData,
          Authorization: session.session.token
        }
      }
    );

    if (!count.ok) {
      let json = await count.json();
      return {
        status: 401,
        error: new Error(JSON.stringify(json))
      };
    }

    let countResp = await count.json();

    return {
      props: {
        perms: perms,
        tableName: params.route,
        rows: colsResp,
        count: countResp,
        schemaOrder: schemaOrder,
        secrets: secrets
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

  import QuailTree from '../../../_helpers/QuailTree.svelte';
  export let perms: any;
  export let tableName: any;
  export let rows: any;
  export let schemaOrder: any[];
  export let secrets: any[];
  export let count: number;
  import * as logger from '$lib/logger';
  import Button from '$lib/base/Button.svelte';
  import { session } from '$app/stores';
  import FormInput from '$lib/base/FormInput.svelte';
  import Tip from '$lib/base/Tip.svelte';
  import { goto } from '$app/navigation';

  let page = 1;
  let limit = 50;

  let extQuery = '';

  const getPage = async (nextPage) => {
    // Get cols
    if (extQuery) {
      // Get new total count expected for this query
      let countReq = await fetch(
        `${electroUrl}/ap/tables/${tableName}?user_id=${
          $session.session.user.id
        }&limit=${limit}&offset=${(nextPage - 1) * limit}&${extQuery}&count=true`,
        {
          method: 'GET',
          headers: {
            'Frostpaw-ID': $session.adminData,
            Authorization: $session.session.token
          }
        }
      );
      if (countReq.ok) {
        count = await countReq.json();
      } else {
        let json = await countReq.json();
        logger.error(json);
        alert(json.reason);
      }
    }
    let cols = await fetch(
      `${electroUrl}/ap/tables/${tableName}?user_id=${
        $session.session.user.id
      }&limit=${limit}&offset=${(nextPage - 1) * limit}&${extQuery}`,
      {
        method: 'GET',
        headers: {
          'Frostpaw-ID': $session.adminData,
          Authorization: $session.session.token
        }
      }
    );

    if (!cols.ok) {
      let json = await cols.json();
      alert(json.reason);
      return;
    }
    rows = await cols.json();
    page = nextPage;
  };

  function getSearchBy(): HTMLInputElement {
    return document.querySelector('#search-by');
  }

  function getSearchVal(): HTMLInputElement {
    return document.querySelector('#search-val');
  }
</script>

<QuailTree perms={perms.perm}>
  <div class="mx-2">
    <h1 id={tableName}>{title(tableName)}</h1>
    <h2>Columns</h2>
    <ul>
      {#each schemaOrder as column}
        <li>{column}</li>
      {/each}
      {#each secrets as secret}
        <li>{secret} (secret)</li>
      {/each}
    </ul>

    <h3>Search</h3>
    <label for="search-by">Search By</label>
    <select name="search-by" id="search-by">
      {#each schemaOrder as column}
        <option value={column}>{title(column)} ({column})</option>
      {/each}
    </select>
    <div class="width-80">
      <FormInput
        required={true}
        name="Value to search by"
        id="search-val"
        textarea={false}
        placeholder={'Mew...'}
      />
    </div>
    <Tip>
      When searching, here are some useful special-cases implemented in the API:
      <ul>
        <li>null => Select all rows such that the specified column is NULL</li>
        <li>
          (&lt / &gt)QUERY =&gt Performs a <em>character</em> based search by converting fields to text
          and searching by string comparison
        </li>
        <li>@QUERY => Do not parse the query for special cases</li>
      </ul>
    </Tip>
    <Button
      class="button"
      onclick={() => {
        extQuery = `search_by=${getSearchBy().value}&search_val=${getSearchVal().value}`;
        getPage(1);
      }}>Search</Button
    >

    <!--Insert schema-->
    <p>Showing {(page - 1) * limit} to [max] {page * limit} of {count} elements</p>
    <div class="scroll">
      <table class="rules-all">
        <thead>
          <tr>
            <th>Actions</th>
            {#each schemaOrder as table}
              <th>{title(table)}</th>
            {/each}
          </tr>
        </thead>

        {#each rows as row}
          <tr class="link" role="link">
            <td>
              <a
                class="edit"
                href={'javascript:void(0)'}
                on:click={() => {
                  goto(`/quailfeather/admin/table/${tableName}/edit/${row._lynxtag}`);
                }}>Edit</a
              >
            </td>

            {#each schemaOrder as column}
              {#if `${row[column]}`.length > 70}
                <td>{`${row[column]}`.slice(0, 70) + '...'}</td>
              {:else}
                <td>{`${row[column]}`}</td>
              {/if}
            {/each}
          </tr>
        {/each}
      </table>
    </div>

    <div class="seperate" />

    {#if page > 0}
      <Button
        class="next-page button"
        
        onclick={() => {
          getPage(page - 1);
        }}>Previous Page</Button
      >
    {/if}

    {#if rows.length > 0}
      <Button
        class="next-page button"
        
        onclick={() => {
          getPage(page + 1);
        }}>Next Page</Button
      >
    {/if}

    <div class="seperate-bottom" />
  </div>
</QuailTree>

<style>
  ul,
  table,
  thead,
  td,
  tr {
    color: white !important;
  }

  table {
    width: 100%;
    white-space: nowrap;
    padding: 3px !important;
    border-collapse: collapse !important;
    min-width: 400px !important;
    margin: 25px 0 !important;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.15) !important;
    overflow: scroll !important;
  }

  th,
  td {
    padding: 12px 15px !important;
  }

  th {
    text-transform: uppercase !important;
  }

  tr:hover {
    background-color: rgba(255, 255, 255, 0.1) !important;
  }

  .scroll {
    overflow-x: scroll !important;
  }

  .width-80 {
    width: 80% !important;
  }

  .seperate {
    padding: 5px;
  }

  .seperate-bottom {
    margin-bottom: 20px;
  }

  :global(.button:hover) {
    animation: none !important;
    background-color: rgba(255, 255, 255, 0.1) !important;
  }

  .edit:hover {
    color: white !important;
  }
</style>
