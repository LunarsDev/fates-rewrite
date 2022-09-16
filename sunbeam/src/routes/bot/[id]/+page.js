import { api, origin } from '$lib/config';
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

    if (session.user) {
      auth = `${session.user.id}|${session.token}`;
    }

    let headers = {
      origin: origin
    }

    if (auth) {
      headers['authorization'] = auth;
    }

    res = await fetch(`${api}${url}`, {
      headers: headers
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