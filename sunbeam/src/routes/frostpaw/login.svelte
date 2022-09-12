<script context="module" lang="ts">
  import { encode, decode } from '@cfworker/base64url';
  import { apiUrl } from '$lib/config';

  export const prerender = false;

  interface CustomClients {
    clientId?: string;
    currentTime?: number;
    hmacTime?: string;
    cliInfo?: any;
    code: string;
    state: string;
  }

  export async function load({ session, fetch }) {
    let url = new URL(session.url);
    let searchParams = url.searchParams;

    let retry = "<br/><br/><a href='https://fateslist.xyz'>Try Again?</a>";

    let error = searchParams.get('error');

    if (error) {
      return {
        props: {
          error: error
        }
      };
    }

    let code = searchParams.get('code');
    let state = searchParams.get('state');
    if (!code || !state) {
      return {
        props: {
          error: 'Invalid code/state' + retry
        }
      };
    }

    let stateSplit = state.split('.');
    let customClientInfo: CustomClients = { code: code, state: stateSplit[3] };

    if (state.startsWith('Bayshine.')) {
      // Bayshine custom client login
      customClientInfo.clientId = stateSplit[1];
      customClientInfo.currentTime = parseInt(stateSplit[2]);
      customClientInfo.hmacTime = stateSplit[3];
      if (
        !customClientInfo.clientId ||
        !customClientInfo.currentTime ||
        !customClientInfo.hmacTime
      ) {
        return {
          props: {
            error: 'Invalid custom client information'
          }
        };
      }
      if (
        new Date().getTime() / 1000 - customClientInfo.currentTime > 60 ||
        customClientInfo.currentTime > new Date().getTime() / 1000 ||
        customClientInfo.currentTime <= 0
      ) {
        return {
          props: {
            error: `Current time nonce is too old! (${new Date().getTime() / 1000})`
          }
        };
      }

      // Fetch baypaw client info
      let res = await fetch(`${apiUrl}/frostpaw/clients/${customClientInfo.clientId}`);

      if (!res.ok) {
        return {
          props: {
            error: `Could not fetch custom client information: ${res.statusText}`
          }
        };
      }

      customClientInfo.cliInfo = await res.json();

      return {
        props: {
          customClient: customClientInfo
        }
      };
    }

    if (stateSplit.length != 2) {
      return {
        props: {
          error: 'Invalid state'
        }
      };
    }

    let nonce = stateSplit[0];
    let modifier = stateSplit[1];

    let modifierInfo = {};

    try {
      modifierInfo = JSON.parse(decode(modifier));
    } catch (e) {
      return {
        props: {
          error: 'Invalid modifier info'
        }
      };
    }

    if (modifierInfo['state'] != nonce) {
      return {
        props: {
          error: 'Invalid nonce'
        }
      };
    }

    if (modifierInfo['version'] != 11) {
      return {
        props: {
          error: 'Invalid login request, please try logging in again!!!'
        }
      };
    }

    console.log('ORIGIN:', url.origin);

    let res = await fetch(`${apiUrl}/oauth2`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Frostpaw: '0.1.0',
        'Frostpaw-Server': url.origin
      },
      body: JSON.stringify({
        code: code,
        state: nonce,
        // We are not a custom client
        frostpaw: false
      })
    });

    let json = {};

    try {
      json = await res.json();
    } catch (e) {
      return {
        props: {
          error: `Invalid login request, please try logging in again (${e})`
        }
      };
    }

    if (json['state'] == enums.UserState.global_ban) {
      return {
        props: {
          error: `<h1>You are global banned</h1><br/><h2>This is a global ban and as such, you may not login/use our API.</h2><br/>You can try to appeal this ban at <a href="https://fateslist.xyz/staffserver">our ban appeal server</a>`
        }
      };
    } else if (!json['token']) {
      return {
        props: {
          error: `Got error: ${JSON.stringify(json)}.`
        }
      };
    }

    return {
      props: {
        cookie: encode(JSON.stringify(json)),
        href: modifierInfo['href'] || '/',
        modifier: modifierInfo
      }
    };
  }
</script>

<script lang="ts">
  import { goto } from '$app/navigation';

  export let cookie: string;
  export let customClient: CustomClients;
  export let error: string;
  export let href: string;
  export let modifier: any;

  import Button from '$lib/base/Button.svelte';
  import { enums } from '$lib/enums/enums';
  import { browser } from '$app/env';

  const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

  async function setLoginCookie() {
    if (cookie) {
      if (browser) {
        setCookie();
        document.cookie = `sunbeam-session=${cookie};Path=/;secure;max-age=28800;samesite=lax;priority=High`;
        await sleep(1000);
        window.location.href = href;
      }
    }
  }

  function setCookie() {
    document.cookie = `sunbeam-session=${cookie};Path=/;secure;max-age=28800;samesite=lax;priority=High`;
  }

  function setCookieReload() {
    setCookie();
    window.location.href = href;
  }

  if (cookie) {
    setLoginCookie();
  }
</script>

<div style="margin: 20px;">
  {#if error}
    <p style="font-size: bold;">{@html error}</p>
    <footer>
      <p>Try logging in again?</p>
    </footer>
  {/if}

  {#if cookie}
    <p style="font-size: bold;">
      Successfully logged in and will be redirecting to {href}! If you do not get redirected, click
      <a href={'#'} on:click={() => setCookieReload()}>here</a>
    </p>
    <footer>Modifier (for debugging): {JSON.stringify(modifier)}</footer>
  {/if}

  {#if customClient}
    <h1>Custom Client Alert!</h1>
    <h2>
      Custom clients can add, edit and delete bots on your behalf and can also vote for bots and
      servers.
    </h2>
    <p>
      You are about to login to <span
        style="opacity: 0.8; text-decoration: underline; font-weight: bolder;"
        >{customClient.cliInfo.name}</span
      >!
      <br /><br />
      Fates List cannot validate the authenticity of this client.
      <br /><br />
      You will be redirected to
      <span style="opacity: 0.8; text-decoration: underline; font-weight: bolder;"
        >{customClient.cliInfo.domain}</span
      >
      which has a privacy policy of
      <span style="opacity: 0.8; text-decoration: underline; font-weight: bolder;"
        >{customClient.cliInfo.privacy_policy}</span
      >
      and is owned by
      <span style="opacity: 0.8; text-decoration: underline; font-weight: bolder;"
        >{customClient.cliInfo.owner.username}</span
      >
      <br /><br />
      If you are not sure, <em>exit this page now</em>.
      <br /><br />
    </p>
    <small
      >Client ID: <span style="text-decoration: underline; font-weight: bolder;"
        >{customClient.cliInfo.id}</span
      ></small
    >
    <br /><br />
    <Button
      onclick={() => {
        goto('/');
      }}
      style="background-color: #90EE90; color: black;">Back To Safety</Button
    >
    <Button
      onclick={async () => {
        let res = await fetch(`${apiUrl}/oauth2`, {
          credentials: 'include',
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Frostpaw: '0.1.0',
            'Frostpaw-Server': window.location.origin
          },
          body: JSON.stringify({
            code: customClient.code,
            state: customClient.state,
            // We are a custom client
            frostpaw: true,
            frostpaw_blood: customClient.clientId,
            frostpaw_claw: customClient.hmacTime,
            frostpaw_claw_unseathe_time: customClient.currentTime
          })
        });
        let json = await res.json();
        if (res.ok) {
          window.location.href = `${customClient.cliInfo.domain}/frostpaw?data=${encode(
            JSON.stringify(json)
          )}`;
        } else {
          alert({
            title: 'Error',
            id: 'frostpaw-cli-error',
            message: `Error: ${json.error}`,
            type: enums.AlertType.Error
          });
        }
      }}
      style="background-color: red; color: white;">Authorize</Button
    >
    <style>
      small {
        color: white;
      }
    </style>
  {/if}
</div>
