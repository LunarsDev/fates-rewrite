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
  </div>
  