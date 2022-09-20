import { api } from '$lib/config';
import * as logger from '$lib/logger';
  import { request } from '$lib/request';
import { error } from '@sveltejs/kit';

/** @type {import('../../../$types').PageLoad} */
export async function load({ params, fetch, parent }) {
  let session = await parent();

  if(!session.token) {
    return {}
  }

  let botObj = await request(`${api}/bots/${params.id}`, {
    method: 'GET',
    endpointType: 'user',
    headers: {
        'Frostpaw-Cache': '0'
    },
    session: session,
    fetch: fetch,
    auth: false
  });
  let data = await botObj.json();

  let meta = null;

    // Fetch metadata
    try {
        const metadata = await request(`${api}/meta`, {
          method: "GET",
          session: session,
          endpointType: "user",
          fetch: fetch,
          auth: false
        });

        if (metadata.ok) {
          meta = await metadata.json();
        }
    } catch (err) {
        throw error(500, err)
    }

    return {
        bot: data,
        meta: meta.bot,
    }

}