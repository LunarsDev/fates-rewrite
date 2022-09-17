<script lang="ts">
  interface CustomClients {
    clientId?: string;
    currentTime?: number;
    hmacTime?: string;
    cliInfo?: any;
    code: string;
    state: string;
  }

    import { goto } from '$app/navigation';
  
    export let data: { cookie: string, customClient: CustomClients, error: string, href: string, modifier: any };

    if(!data.href) {
      data.href = "/"
    }

    error('Login', `Got login error: ${data.error}\nGot href: ${data.href}\nGot modifier: ${data.modifier}`)
  
    import Button from '$lib/base/Button.svelte';
    import { enums } from '$lib/enums/enums';
    import { browser } from '$app/environment';
    import { apiUrl } from '$lib/config';
    import Base64 from "$lib/b64";
    import { error, info } from '$lib/logger';
  
    const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));
  
    async function setLoginCookie() {
      if (data.cookie) {
        if (browser) {
          setCookie();
          info("Login", "Set cookie");
          document.cookie = `sunbeam-session=${data.cookie};Path=/;secure;max-age=28800;samesite=lax;priority=High`;
          await sleep(1000);
          window.location.href = data.href;
        }
      }
    }
  
    function setCookie() {
      document.cookie = `sunbeam-session=${data.cookie};Path=/;secure;max-age=28800;samesite=lax;priority=High`;
    }
  
    function setCookieReload() {
      setCookie();
      window.location.href = data.href;
    }
  
    if (data.cookie) {
      setLoginCookie();
    }
  </script>
  
  <div style="margin: 20px;">
    {#if data.error}
      <p style="font-size: bold;">{@html data.error}</p>
      <footer>
        <p>Try logging in again?</p>
      </footer>
    {/if}
  
    {#if data.cookie}
      <p style="font-size: bold;">
        Successfully logged in and will be redirecting to {data.href}! If you do not get redirected, click
        <a href={'#'} on:click={() => setCookieReload()}>here</a>
      </p>
      <footer>Modifier (for debugging): {JSON.stringify(data.modifier)}</footer>
    {/if}
    {#if data.customClient}
      <h1>Custom Client Alert!</h1>
      <h2>
        Custom clients can add, edit and delete bots on your behalf and can also vote for bots and
        servers.
      </h2>
      <p>
        You are about to login to <span
          style="opacity: 0.8; text-decoration: underline; font-weight: bolder;"
          >{data.customClient.cliInfo.name}</span
        >!
        <br /><br />
        Fates List cannot validate the authenticity of this client.
        <br /><br />
        You will be redirected to
        <span style="opacity: 0.8; text-decoration: underline; font-weight: bolder;"
          >{data.customClient.cliInfo.domain}</span
        >
        which has a privacy policy of
        <span style="opacity: 0.8; text-decoration: underline; font-weight: bolder;"
          >{data.customClient.cliInfo.privacy_policy}</span
        >
        and is owned by
        <span style="opacity: 0.8; text-decoration: underline; font-weight: bolder;"
          >{data.customClient.cliInfo.owner.username}</span
        >
        <br /><br />
        If you are not sure, <em>exit this page now</em>.
        <br /><br />
      </p>
      <small
        >Client ID: <span style="text-decoration: underline; font-weight: bolder;"
          >{data.customClient.cliInfo.id}</span
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
              code: data.customClient.code,
              state: data.customClient.state,
              // We are a custom client
              frostpaw: true,
              frostpaw_blood: data.customClient.clientId,
              frostpaw_claw: data.customClient.hmacTime,
              frostpaw_claw_unseathe_time: data.customClient.currentTime
            })
          });
          let json = await res.json();
          if (res.ok) {
            window.location.href = `${data.customClient.cliInfo.domain}/frostpaw?data=${Base64.encode(
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
  