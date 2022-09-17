import { api, origin } from '$lib/config';
import { request } from '$lib/request';
import { error } from '@sveltejs/kit';
export const prerender = false;

/** @type {import('../../$types').PageLoad} */
export async function load({ parent, params, fetch }) {
  const url = `/bots/${params.id}`;

  let auth = '';

  let session = null
  let res = null

  try {
    session = await parent();

    res = await request(`${api}${url}`, {
      method: "GET",
      session: session,
      endpointType: "user",
      fetch: fetch,
    })
  } catch (err) {
    throw error(404, err)
  }

  if (res.ok) {
    let data = await res.json();
    return {
      bot: data
    };
  }

  throw error(404, "Bot Not Found")
}