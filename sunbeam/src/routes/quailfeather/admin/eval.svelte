<script context="module">
  /** @type {import('@sveltejs/kit').ErrorLoad} */
  import { apiUrl, lynxUrl } from '$lib/config';
  import { checkAdminSession } from '$lib/request';
  export const prerender = false;
  export async function load({ session }) {
    let id = '0';
    if (session.session.token) {
      id = session.session.user.id;
    }
    let perms = await fetch(`${apiUrl}/baypaw/perms/${id}`);

    let permsResp = await perms.json();

    if (permsResp.perm < 2) {
      return {
        status: 401,
        error: new Error('You are not a developer.')
      };
    }

    if (!session.adminData) {
      return {
        status: 307,
        redirect: `/quailfeather/admin/login?redirect=/quailfeather/admin/eval`
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
        redirect: `/quailfeather/admin/login?redirect=/quailfeather/admin/eval`
      };
    }

    return {
      props: {
        perms: perms
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
  import { enums } from '$lib/enums/enums';
  import * as logger from '$lib/logger';
  import Button from '$lib/base/Button.svelte';

  import FormInput from '$lib/base/FormInput.svelte';
  import { session } from '$app/stores';

  interface Args {
    type?: string;
    array?: boolean;
    value?: string;
    values?: any[]; // Ignored if not array
  }

  let args: Args[] = [];

  function waitForTask(id: string) {
    setInterval(async () => {
      let task = await fetch(`${lynxUrl}/long-running/${id}`);
      if (task.ok) {
        let taskResp = await task.json();
        if (taskResp.error) {
          alert(taskResp.error);
        } else {
          alert(taskResp.output);
        }
      }
    }, 500);
  }

  function addArgument() {
    alert({
      title: 'Login',
      message: 'Enter your Admin credentials here.',
      type: enums.AlertType.Prompt,
      inputs: [
        {
          id: 'arg-type',
          label:
            'Argument Type (boolean/number/integer/text/uuid/timestamptz/add [] to signify array)',
          placeholder: 'Password',
          required: true,
          type: enums.AlertInputType.Text
        }
      ],
      submit: (v) => {
        let value = v.toLines('arg-type');
        logger.info('Eval', { value });
        let array = false;
        if (value.includes('[]')) {
          array = true;
        }

        let type = value.replace('[]', '');

        args.push({
          type: type,
          array: array,
          value: '',
          values: [] // Ignored if not array
        });

        args = args;
      }
    });
  }

  function getSql(): HTMLInputElement {
    return document.querySelector('#sql');
  }
</script>

<QuailTree perms={perms.perm}>
  <FormInput id="sql" name="SQL Statement" placeholder="Must be explicitly approved. DEV+ only!" />
  <a href={'javascript:void(0)'} on:click={addArgument}>Add Argument</a>

  {#each args as arg, i}
    {#if arg.array}
      {#each arg.values as value, j}
        <div class="arg">
          <FormInput
            id="arg-{i}-{j}"
            name="Argument ${i + 1}"
            placeholder="ABC"
            data={value}
            oninput={(e) => {
              logger.debug('Eval', 'New input', e.target.value);
              args[i].values[j].value = e.target.value;
            }}
          />
          <a
            href={'javascript:void(0)'}
            on:click={() => {
              args[i].values.splice(j, 1);
              args = args;
            }}>Remove</a
          >
        </div>
      {/each}
      <a
        href={'javascript:void(0)'}
        on:click={() => {
          args[i].values.push('');
          args = args;
        }}>Add</a
      >
    {:else}
      <FormInput
        id="arg-{i}"
        name="Argument ${i}"
        placeholder="ABC"
        data={arg.value}
        oninput={(e) => {
          logger.debug('Eval', 'New input', e.target.value);
          args[i].value = e.target.value;
        }}
      />
      <a
        href={'javascript:void(0)'}
        on:click={() => {
          args.splice(i, 1);
          args = args;
        }}>Remove</a
      >
    {/if}
  {/each}
  <Button
    onclick={() => {
      let sql = getSql().value;

      logger.info('Eval', { sql, args });
      alert({
        title: `Evaluate}`,
        message: `Going to run ${sql}`,
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

          let res = await fetch(`${lynxUrl}/ap/evalsql?user_id=${$session.session.user.id}`, {
            method: 'POST',
            headers: {
              'Frostpaw-ID': $session.adminData,
              Authorization: $session.session.token,
              'Content-Type': 'application/json',
              'Frostpaw-MFA': mfa
            },
            body: JSON.stringify({
              sql: sql,
              args: args
            })
          });

          if (res.ok) {
            alert('Waiting for approval.');

            let json = await res.json();

            waitForTask(json.task_id);
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
    }}>Eval</Button
  >
</QuailTree>
