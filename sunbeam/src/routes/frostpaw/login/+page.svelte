<script lang="ts">
  interface CustomClients {
    clientId?: string;
    currentTime?: number;
    hmacTime?: string;
    cliInfo?: any;
    code: string;
    state: string;
  }

  export let data: {
    cookie: string;
    customClient: CustomClients;
    error: string;
    href: string;
    modifier: any;
    state: string;
  };

  if (!data.href) {
    data.href = '/';
  }

  error(
    'Login',
    `Got login error: ${data.error}\nGot href: ${data.href}\nGot modifier: ${data.modifier}`
  );

  import { browser } from '$app/environment';
  import { error, info } from '$lib/logger';

  const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

  async function setLoginCookie() {
    if (data.cookie) {
      if (browser) {
        setCookie();
        info('Login', 'Set cookie');
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
    if (data.state === 'api') {
      if (browser) {
        if (!window.opener) {
          alert(
            'No window.opener provided... Please contact Fates List Support immediately and also regenerate your user token NOW to prevent any security issues.'
          );
        }

        window.opener.postMessage(data.cookie, '*');
        return;
      }
    }

    setCookie();
    window.location.href = data.href;
  }

  if (data.cookie) {
    if (data.state === 'api') {
      if (browser) {
        if (!window.opener) {
          alert(
            'No window.opener provided... Please contact Fates List Support immediately and also regenerate your user token NOW to prevent any security issues.'
          );
        }

        window.opener.postMessage(data.cookie, '*');
      }
    } else {
      setLoginCookie();
    }
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
      Successfully logged in and will be redirecting to {data.href}! If you do not get redirected,
      click
      <a href={'#'} on:click={() => setCookieReload()}>here</a>
    </p>
    <footer>Modifier (for debugging): {JSON.stringify(data.modifier)}</footer>
  {/if}
</div>
