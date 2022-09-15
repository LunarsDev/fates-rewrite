import { api, origin } from '$lib/config';
import * as logger from '$lib/logger';
import { error } from '@sveltejs/kit';

/** @type {import('./$types').PageLoad} */
export async function load({ parent, fetch }) {
    let session = await parent();
    logger.info('Page', session);
    const url = `/index?target_type=0`;
    let res = null
    try {
        res = await fetch(`${api}${url}`, {
            headers: {
                origin: origin
            }
        });
    } catch (err) {
        throw error(404, err)
    }

    let data = await res.json();

    // Fetch metadata
    try {
        const metadata = await fetch(`${api}/meta`, {
          headers: {
            origin: origin
          }
        });

        if (metadata.ok) {
          let metaJson = await metadata.json();
          data.tags = metaJson.bot.tags;
        }
    } catch (err) {
        throw error(404, err)
    }

    // Fetch random bot
    let randomJson = null;
    try {
        const random = await fetch(`${api}/random?target_type=0`, {
          headers: {
            origin: origin
          }
        });

        if (random.ok) {
          randomJson = await random.json();
        } else {
          throw error(404, 'Random bot not found')
        }
    } catch (err) {
      throw error(404, err)
    }

    console.log(data, "is data")

    if (res.ok) {
      return {
        index: data,
        random: randomJson
      };
    }

    throw error(res.status, `Could not load ${url}`)
  }