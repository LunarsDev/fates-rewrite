import { apiUrl, origin } from '$lib/config';
import * as logger from '$lib/logger';

/** @type {import('./$types').PageLoad} */
export async function load({ parent, fetch }) {
    let session = await parent();
    logger.info('Page', session);
    const url = `/index?target_type=0`;
    const res = await fetch(`${apiUrl}${url}`, {
        headers: {
            origin: origin
        }
    });

    let data = await res.json();

    console.log(data, "is data")

    if (res.ok) {
      return {
        index: data,
        randomBot: data.random
      };
    }

    return {
      status: res.status,
      error: new Error(`Could not load ${url}`)
    };
  }