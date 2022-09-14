  import { apiUrl, origin } from '$lib/config';
  import { enums } from '$lib/enums/enums';
  import Base64 from "$lib/b64";
  import { error } from '@sveltejs/kit';

  export const prerender = false;

  interface CustomClients {
    clientId?: string;
    currentTime?: number;
    hmacTime?: string;
    cliInfo?: any;
    code: string;
    state: string;
  }

/** @type {import('../../$types').PageLoad} */
export async function load({ parent, fetch }) {

    try {
      let session = await parent();
      let url = new URL(session.url);
      let searchParams = url.searchParams;

      let retry = "<br/><br/><a href='https://fateslist.xyz'>Try Again?</a>";

      let error = searchParams.get('error');

      if (error) {
        return {
          error: error
        };
      }

      let code = searchParams.get('code');
      let state = searchParams.get('state');
      if (!code || !state) {
        return {
          error: 'Invalid code/state' + retry
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
            error: 'Invalid custom client information'
          };
        }
        if (
          new Date().getTime() / 1000 - customClientInfo.currentTime > 60 ||
          customClientInfo.currentTime > new Date().getTime() / 1000 ||
          customClientInfo.currentTime <= 0
        ) {
          return {
            error: `Current time nonce is too old! (${new Date().getTime() / 1000})`
          };
        }

        // Fetch baypaw client info
        let res = await fetch(`${apiUrl}/frostpaw/clients/${customClientInfo.clientId}`, {
          headers: {
            origin: origin
          }
        });

        if (!res.ok) {
          return {
            error: `Could not fetch custom client information: ${res.statusText}`
          };
        }

        customClientInfo.cliInfo = await res.json();

        return {
          customClient: customClientInfo
        };
      }

      if (stateSplit.length != 2) {
        return {
          error: 'Invalid state'
        };
      }

      let nonce = stateSplit[0];
      let modifier = stateSplit[1];

      let modifierInfo = {};

      console.log(Base64.decode(modifier))

      try {
        modifierInfo = JSON.parse(Base64.decode(modifier));
      } catch (e) {
        return {
          error: 'Invalid modifier info'
        };
      }

      if (modifierInfo['state'] != nonce) {
        return {
          error: 'Invalid nonce'
        };
      }

      if (modifierInfo['version'] != 11) {
        return {
          error: 'Invalid login request, please try logging in again!!!'
        };
      }

      console.log('ORIGIN:', url.origin);

      let res = await fetch(`${apiUrl}/oauth2`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Frostpaw: '0.1.0',
          'Frostpaw-Server': url.origin,
          origin: origin
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
          error: `Invalid login request, please try logging in again (${e})`
        };
      }

      if (json['state'] == enums.UserState.global_ban) {
        return {
          error: `<h1>You are global banned</h1><br/><h2>This is a global ban and as such, you may not login/use our API.</h2><br/>You can try to appeal this ban at <a href="https://fateslist.xyz/staffserver">our ban appeal server</a>`
        };
      } else if (!json['token']) {
        return {
          error: `Got error: ${JSON.stringify(json)}.`
        };
      }

      return {
        cookie: Base64.encode(JSON.stringify(json)),
        href: modifierInfo['href'] || '/',
        modifier: modifierInfo
      };
    } catch (err) {
      throw error(404, err)
    }
  }