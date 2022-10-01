import { api } from '$lib/config';
import { request } from '$lib/request';
import { error } from '@sveltejs/kit';

/** @type {import('../../$types').PageLoad} */
export async function load({ fetch, parent }) {
  let session = await parent();
  if (!session.token) {
    return {};
  }

  let tagsRes = await request(`${api}/meta`, {
    method: 'GET',
    session: session,
    endpointType: 'user',
    fetch: fetch
  });
  if (!tagsRes.ok) {
    throw error(500, 'Could not fetch tags and features');
  }

  let data = await tagsRes.json();
  return {
    data: { tags: [], features: [] },
    context: data.bot
  };
}
