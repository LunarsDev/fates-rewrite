import { api } from '$lib/config';
import * as logger from '$lib/logger';
import { request } from '$lib/request';
import { error } from '@sveltejs/kit';

/** @type {import('./$types').PageLoad} */
export async function load({ params, fetch, parent }) {
  let session = await parent();

  if (!session.token) {
    return {};
  }

  let botObj = await request(`${api}/bots/${params.id}`, {
    method: 'GET',
    endpointType: 'user',
    headers: {
      'Frostpaw-Cache': '0'
    },
    session: session,
    fetch: fetch,
    auth: false,
    errorOnFail: true
  });

  let data = await botObj.json();

  // Fetch metadata
  const metadata = await request(`${api}/meta`, {
    method: 'GET',
    session: session,
    endpointType: 'user',
    fetch: fetch,
    auth: false,
    errorOnFail: true
  });

  let meta = null;
  if (metadata.ok) {
    meta = await metadata.json();
  } else {
    throw error(404, 'Metadata could not be loaded');
  }

  // Fetch bot secrets
  const secret = await request(`${api}/bots/${params.id}/secrets`, {
    method: 'GET',
    session: session,
    endpointType: 'user',
    fetch: fetch,
    auth: true
  });

  let secrets = null;
  if (secret.ok) {
    secrets = await secret.json();
  } else if (secret.status == 403 || secret.status == 401) {
    throw error(401, "Hmmm... you aren't allowed to edit this bot ");
  } else {
    secrets = await secret.text();
    throw error(404, `Secrets load error: ${secrets}`);
  }

  data.api_token = secrets.api_token;
  data.webhook = secrets.webhook;
  data.webhook_secret = secrets.webhook_secret;

  return {
    bot: data,
    meta: meta.bot
  };
}
