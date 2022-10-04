import { api } from '$lib/config';
import * as logger from '$lib/logger';
import { request } from '$lib/request';
import { error } from '@sveltejs/kit';

/** @type {import('./$types').PageLoad} */
export async function load({ parent, fetch }) {
  let session = await parent();
  logger.info('Page', session);
  const url = `/index?target_type=0`;
  let res = null;
  res = await request(`${api}${url}`, {
    method: 'GET',
    session: session,
    endpointType: 'user',
    fetch: fetch,
    auth: false
  });

  let data = await res.json();

  // Fetch metadata
  const metadata = await request(`${api}/meta`, {
    method: 'GET',
    session: session,
    endpointType: 'user',
    fetch: fetch,
    auth: false
  });

  let metaJson = null;

  if (metadata.ok) {
    metaJson = await metadata.json();
  } else {
    throw error(500, 'Failed to fetch list metadata');
  }

  // Fetch random bot
  let randomJson = null;
  const random = await request(`${api}/random?target_type=0`, {
    method: 'GET',
    session: session,
    endpointType: 'user',
    fetch: fetch,
    auth: false
  });

  if (random.ok) {
    randomJson = await random.json();
  } else {
    throw error(404, 'Random bot not found');
  }

  if (res.ok) {
    return {
      index: data,
      meta: metaJson,
      random: randomJson
    };
  }

  throw error(res.status, `Could not load ${url}`);
}
