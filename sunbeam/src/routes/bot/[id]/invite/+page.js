import { api } from '$lib/config';
import * as logger from '$lib/logger';
  import { request } from '$lib/request';

/** @type {import('../../../$types').PageLoad} */
export async function load({ params, fetch, parent }) {
  let session = await parent();
  let inviteUrl = await request(`${api}/bots/${params.id}`, {
    method: 'GET',
    headers: {
      'Frostpaw-Target': 'invite'
    },
    endpointType: 'user',
    session: session,
    fetch: fetch,
    auth: true
  });
  let inviteJson = await inviteUrl.json();

  if (!inviteUrl.ok) {
    return {
      status: 400,
      error: new Error(`${inviteJson.reason}`)
    };
  }

  // JS and URLS do not go well together
  logger.info(
    'BotInvite',
    'Parsed invite info',
    inviteJson,
    decodeURIComponent(inviteJson.invite_link)
  );
  return {
    status: 307,
    redirect: decodeURIComponent(inviteJson.invite_link)
  };
}