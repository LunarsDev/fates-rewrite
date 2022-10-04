export const prerender = false;
import { request } from '$lib/request';
import { api } from '$lib/config';
import * as logger from '$lib/logger';
import { enums } from '$lib/enums/enums';
import { redirect, error } from '@sveltejs/kit';

/** @type {import('./$types').PageLoad} */
export async function load({ url, fetch, parent }) {
  let session = await parent();

  if (!session.token) {
    return {};
  }

  let allPerms = await request(`${api}/permissions`, {
    method: 'GET',
    session: session,
    endpointType: 'user',
    fetch: fetch
  });

  if (!allPerms.ok) {
    throw error(500, 'Failed to get permissions');
  }

  return {
    all_permissions: (await allPerms.json())['perms'],
    action: url.searchParams.get('act')
  };
}
