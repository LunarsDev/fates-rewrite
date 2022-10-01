export const prerender = false;
import { request } from '$lib/request';
import { api } from '$lib/config';
import * as logger from '$lib/logger';
import { enums } from '$lib/enums/enums';
import { redirect, error } from '@sveltejs/kit';

/** @type {import('./$types').PageLoad} */
export async function load({ params, fetch, parent }) {
  if (params.vanity == 'servers') {
    throw redirect(307, '/frostpaw/servers/');
  }

  let session = await parent();

  const res = await request(`${api}/code/${params.vanity}`, {
    method: 'GET',
    fetch: fetch,
    session: session,
    endpointType: 'user'
  });

  if (res.ok) {
    let data = await res.json();
    let id = data.target_id;
    let type = enums.TargetType[data.target_type];

    throw redirect(307, `/${type}/${id}/invite`);
  }

  throw error(404, 'Invalid Vanity');
}
