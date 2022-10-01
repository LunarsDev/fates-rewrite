import { api } from '$lib/config';
import * as logger from '$lib/logger';
import { request } from '$lib/request';
import { redirect, error } from '@sveltejs/kit';

/** @type {import('./$types').PageLoad} */
export async function load({ params, fetch, parent }) {
  let session = await parent();
  let inviteUrl = await request(`${api}/bots/${params.id}/invite`, {
    method: 'GET',
    headers: {
      'Frostpaw-Target': 'invite'
    },
    endpointType: 'user',
    session: session,
    fetch: fetch
  });
  let inviteJson = await inviteUrl.json();

  if (!inviteUrl.ok) {
    throw error(500, 'Could not fetch invite');
  }

  // JS and URLS do not go well together
  logger.info('BotInvite', 'Parsed invite info', inviteJson, decodeURIComponent(inviteJson.invite));
  throw redirect(307, decodeURIComponent(inviteJson.invite));
}
