<script context="module">
  /** @type {import('@sveltejs/kit').ErrorLoad} */
  import { apiUrl, lynxUrl, electroUrl } from '$lib/config';
  import Button from '$lib/base/Button.svelte';
  export const prerender = false;
  export async function load({ session }) {
    let id = '0';
    if (session.session.token) {
      id = session.session.user.id;
    }
    let permsResp = await fetch(`${apiUrl}/baypaw/perms/${id}`);

    let perms = await permsResp.json();

    if (perms.perm < 2) {
      return {
        status: 401,
        error: new Error('You are not a staff member.')
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
  import { enums } from '$lib/enums/enums';
  import QuailTree from '../_helpers/QuailTree.svelte';
  import { session } from '$app/stores';
  export let perms: any;
  import * as logger from '$lib/logger';
</script>

<QuailTree perms={perms.perm}>
  <h2>Login</h2>
  <Button
    onclick={() => {
      alert({
        title: 'Login',
        message: 'Enter your Admin credentials here.',
        type: enums.AlertType.Prompt,
        submit: async (v) => {
          let pwd = v.toSingleLine('passwd');
          let mfa = v.toSingleLine('mfa-key');
          logger.info('AdminPanel', { pwd, mfa });
          let loginSession = await fetch(
            `${electroUrl}/ap/pouncecat?user_id=${$session.session.user.id}`,
            {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'Frostpaw-Pass': pwd,
                'Frostpaw-MFA': mfa.padStart(6, 0),
                Authorization: $session.session.token
              }
            }
          );

          if (!loginSession.ok) {
            let loginSessionResp = await loginSession.text();
            alert(loginSessionResp);
          }

          let loginSessionStr = await loginSession.text();

          document.cookie = `_adminsession=${loginSessionStr};Path=/quailfeather/admin;secure;max-age=28800;samesite=strict;priority=High`;

          let searchParams = new URLSearchParams(window.location.search);

          let redirect = searchParams.get('redirect') || '/quailfeather/admin';

          window.location.href = redirect;
        },
        inputs: [
          {
            id: 'passwd',
            label: 'Password',
            placeholder: 'Password',
            required: true,
            type: enums.AlertInputType.Text
          },
          {
            id: 'mfa-key',
            label: '2FA Code',
            placeholder: '2FA Code',
            required: true,
            type: enums.AlertInputType.Number
          }
        ],
        buttons: [
          {
            name: 'Forgot Credentials',
            function: () => {
              alert({
                title: 'Forgot Credentials',
                message: 'Please DM @Rootspring#6701 on Discord for assistance.',
                type: enums.AlertType.Info,
                buttons: [
                  {
                    name: 'Open Discord',
                    function: () => {
                      window.open('https://discord.com/channels/@me/955459763519500368');
                    }
                  }
                ]
              });
            }
          }
        ]
      });
    }}
    class="button"
    >Login</Button
  >
</QuailTree>
