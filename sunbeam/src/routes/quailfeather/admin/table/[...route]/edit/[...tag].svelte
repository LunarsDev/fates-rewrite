<script context="module">
  /** @type {import('@sveltejs/kit').ErrorLoad} */
  import { apiUrl, lynxUrl, electroUrl } from '$lib/config';
  import { checkAdminSession } from '$lib/request';
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
        redirect: `/quailfeather/admin/login?redirect=/quailfeather/admin/table/${params.route}/edit/${params.tag}`
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
        redirect: `/quailfeather/admin/login`
      };
    }

    // Get cols
    let cols = await fetch(
      `${electroUrl}/ap/tables/${params.route}?user_id=${session.session.user.id}&search_by=_lynxtag&search_val==${params.tag}`,
      {
        method: 'GET',
        headers: {
          'Frostpaw-ID': session.adminData,
          Authorization: session.session.token
        }
      }
    );

    if (!cols.ok) {
      let json = await cols.text();
      return {
        status: 401,
        error: new Error(json)
      };
    }

    let colsResp = await cols.json();

    let schema = await fetch(`${electroUrl}/ap/schema?table_name=${params.route}`);

    if (!schema.ok) {
      let json = await schema.json();
      return {
        status: 401,
        error: new Error(JSON.stringify(json))
      };
    }

    let schemaResp = await schema.json();

    let typeMap = {};

    cols = colsResp[0];

    schemaResp.forEach((t) => {
      typeMap[t.column_name] = {
        array: t.array,
        secret: t.secret
      };
    });

    let rows = [];

    Object.entries(cols).forEach((el) => {
      if (typeMap[el[0]].secret) {
        return;
      }

      if (typeMap[el[0]].array && !el[1]) {
        logger.info('Admin Panel', 'Got bad data column: ', typeMap[el[0]], el[1]);
        el[1] = [];
      }

      rows.push({
        name: el[0],
        array: typeMap[el[0]].array,
        value: el[1]
      });
    });

    logger.info('AdminPanel', 'Parsed data', rows);

    return {
      props: {
        perms: permsResp,
        tableName: params.route,
        lynxTag: params.tag,
        rows: rows
      }
    };
  }
</script>

<script lang="ts">
  // https://stackoverflow.com/a/46959528
  function title(str: string) {
    return str.replaceAll('_', ' ').replace(/(^|\s)\S/g, function (t) {
      return t.toUpperCase();
    });
  }

  import QuailTree from '../../../../_helpers/QuailTree.svelte';
  export let perms: any;
  export let tableName: any;
  export let lynxTag: any;
  export let rows: any;
  import * as logger from '$lib/logger';
  import { enums } from '$lib/enums/enums';
  import { session } from '$app/stores';
  import Button from '$lib/base/Button.svelte';

  /*
import FormInput from '$lib/base/FormInput.svelte';
import Tip from '$lib/base/Tip.svelte';
*/

  function editAlert(key, content) {
    alert({
      title: `Editting ${key}`,
      message: `Editting ${key}`,
      type: enums.AlertType.Prompt,
      submit: async (value) => {
        // First check their ratelimits
        let raven = await fetch(`${lynxUrl}/ap/raven?user_id=${$session.session.user.id}`, {
          method: 'GET',
          headers: {
            'Frostpaw-ID': $session.adminData,
            Authorization: $session.session.token
          }
        });

        if (!raven.ok) {
          let json = await raven.json();
          alert(json.reason);
          return;
        }

        let ravenResp = await raven.json();

        if (ravenResp.max == ravenResp.made) {
          alert(
            `You have reached your ratelimit. Please wait ${ravenResp.ttl} seconds before trying again.`
          );
          return;
        }

        let mfa = value.toSingleLine('mfa-key');

        logger.info('AdminPanel', 'Setting new content to:', { content });

        let res = await fetch(
          `${lynxUrl}/ap/tables/${tableName}/tag/${lynxTag}?user_id=${$session.session.user.id}`,
          {
            method: 'PATCH',
            headers: {
              'Frostpaw-ID': $session.adminData,
              Authorization: $session.session.token,
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              patch: {
                col: key,
                value: content
              },
              otp: mfa
            })
          }
        );

        if (res.ok) {
          alert('Successfully updated the column.');
        } else {
          let json = await res.json();
          alert(json.reason);
        }
      },
      inputs: [
        {
          id: 'mfa-key',
          type: enums.AlertInputType.Number,
          label: '2FA code',
          placeholder: '2FA code from your authenticator app'
        }
      ]
    });
  }

  function getInputElement(id: string): HTMLInputElement {
    return document.querySelector(id);
  }
</script>

<QuailTree perms={perms.perm}>
  <div class="mx-2">
    <h1 id={tableName}>{title(tableName)} - Editing entity</h1>
    <h2>Columns</h2>
    {#each rows as row}
      <h3>
        {title(row.name)}
      </h3>
      {#if row.array}
        {#each row.value as val, i}
          <textarea
            id="inp-{row.name}-{i}"
            class="fform inp"
            on:keyup={function () {
              this.scrollTop = this.scrollHeight;
            }}>{val}</textarea
          >
          <Button
            class="button"
            onclick={() => {
              let added = false;
              rows.forEach((e) => {
                if (added) {
                  return;
                }
                if (e.name == row.name) {
                  e.value.splice(i, 1);
                  added = true;
                }
              });
              row = row;
            }}>Remove Element</Button
          >
        {/each}
        <br />
        <br />
        <Button
          class="button"
          onclick={() => {
            let added = false;
            rows.forEach((e) => {
              if (added) {
                return;
              }
              if (e.name == row.name) {
                e.value.push('');
                added = true;
              }
            });
            row = row;
          }}>Add new element</Button
        >
        <br /><br />
        <Button
          class="button"
          onclick={() => {
            let els = [];
            let end = false;
            let i = 0;
            while (!end) {
              let el = getInputElement(`#inp-${row.name}-${i}`);
              if (el) {
                els.push(el.value);
                i++;
              } else {
                end = true;
              }
            }
            editAlert(row.name, els);
          }}>Edit</Button
        >
      {:else}
        <textarea
          id="inp-{row.name}"
          class="fform inp"
          on:keyup={() => {
            console.log('keyup');
            document.querySelector(`#inp-${row.name}`).scrollTop = document.querySelector(
              `#inp-${row.name}`
            ).scrollHeight;
          }}>{row.value}</textarea
        >
        <Button
          class="button"
          onclick={() => {
            editAlert(row.name, getInputElement(`#inp-${row.name}`).value);
          }}>Edit</Button
        >
      {/if}
    {/each}
  </div>
</QuailTree>

<style>
  .inp {
    height: 100px !important;
  }
</style>
