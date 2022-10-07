import { api } from '$lib/config';
import { request } from '$lib/request';
import { error } from '@sveltejs/kit';

/** @type {import('./$types').PageLoad} */
export async function load({ fetch, parent }) {
  let session = await parent();
  if (!session.token) {
    return {};
  }

  let metaJson = await request(`${api}/meta`, {
    method: 'GET',
    session: session,
    endpointType: 'user',
    fetch: fetch
  });
  if (!metaJson.ok) {
    throw error(500, 'Could not fetch tags and features');
  }

  let data = await metaJson.json();
  return data;
}
