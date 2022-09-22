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
  let botObj = null

  try {
    botObj = await request(`${api}/bots/${params.id}`, {
        method: 'GET',
        endpointType: 'user',
        headers: {
            'Frostpaw-Cache': '0'
        },
        session: session,
        fetch: fetch,
        auth: false,
        errorOnFail: true,
    });
  } catch (err) {
    throw error(404, err)
  }
  let data = await botObj.json();

  let meta = null;

    // Fetch metadata
    try {
        const metadata = await request(`${api}/meta`, {
          method: "GET",
          session: session,
          endpointType: "user",
          fetch: fetch,
          auth: false,
          errorOnFail: true,
        });

        if (metadata.ok) {
          meta = await metadata.json();
        }
    } catch (err) {
        throw error(500, err)
    }

    // Fetch bot secrets
    let secrets = null;
    try {
        const secret = await request(`${api}/bots/${params.id}/secrets`, {
            method: "GET",
            session: session,
            endpointType: "user",
            fetch: fetch,
            auth: true,
            errorOnFail: true,
        });

        if (secret.ok) {
            secrets = await secret.json();
        }
    } catch (err) {
        throw error(500, err)
    }

    data.api_token = secrets.api_token;
    data.webhook = secrets.webhook;
    data.webhook_secret = secrets.webhook_secret;

    return {
        bot: data,
        meta: meta.bot,
    }

}