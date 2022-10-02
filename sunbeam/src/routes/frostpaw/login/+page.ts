import { request } from '$lib/request';
import { enums } from '$lib/enums/enums';
import Base64 from '$lib/b64';
import { error } from '@sveltejs/kit';
import { info } from '$lib/logger';
import { api } from '$lib/config';

export const prerender = false;

/** @type {import('./$types').PageLoad} */
export async function load({ parent, fetch }) {
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

  let modifierInfo = {};

  let stateSplit = state.split('.');

  if (stateSplit.length != 2) {
    return {
      error: 'Invalid state'
    };
  }

  let nonce = stateSplit[0];
  let modifier = stateSplit[1];

  info('Login', Base64.decode(modifier));

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

  let res = await request(`${api}/oauth2`, {
    method: 'POST',
    headers: {
      'Frostpaw-Server': url.origin
    },
    json: {
      code: code,
    },
    session: session,
    fetch: fetch,
    endpointType: 'user'
  });

  let json = {};

  try {
    json = await res.json();
  } catch (e) {
    return {
      error: `Invalid login request, please try logging in again (${e})`
    };
  }

  if (json['state'] == enums.UserState.global_ban && !modifierInfo["allowBanned"]) {
    return {
      error: `<h1>You are global banned</h1><br/><h2>This is a global ban and as such, you may not login/use our API.</h2><br/>You can try to appeal this ban at <a href="https://fateslist.xyz/staffserver">our ban appeal server</a>`
    };
  } else if (!json['token']) {
    return {
      error: `Got error: ${JSON.stringify(json)}.`
    };
  }

  json["allowBanned"] = modifierInfo["allowBanned"];

  return {
    cookie: Base64.encode(JSON.stringify(json)),
    href: modifierInfo['href'] || '/',
    state: state,
    modifier: modifierInfo
  };
}
