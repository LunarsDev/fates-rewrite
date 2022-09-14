import { apiUrl, origin } from '$lib/config';
import * as logger from '$lib/logger';
import { error } from '@sveltejs/kit';

/** @type {import('./$types').PageLoad} */
export async function load({ parent, fetch }) {
    let session = await parent();
    logger.info('Page', session);
    const url = `/index?target_type=0`;
    let res = null
    try {
        res = await fetch(`${apiUrl}${url}`, {
            headers: {
                origin: origin
            }
        });
    } catch (err) {
        throw error(404, err)
    }

    let data = await res.json();

    console.log(data, "is data")

    if (res.ok) {
      return {
        index: data,
        randomBot: data.random
      };
    }

    throw error(res.status, `Could not load ${url}`)
  }