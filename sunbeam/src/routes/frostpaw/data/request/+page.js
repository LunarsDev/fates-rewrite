export const prerender = false;
import { request } from '$lib/request';
import { api } from '$lib/config';
import * as logger from '$lib/logger';
import { enums } from '$lib/enums/enums';
import { redirect, error } from '@sveltejs/kit';

/** @type {import('./$types').PageLoad} */
export async function load({ params, fetch, parent }) {
  let session = await parent();

  if(!session.token) {
    return {}
  }
}