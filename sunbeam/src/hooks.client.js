import { error as errorFunc } from '$lib/logger';

/** @type {import('@sveltejs/kit').HandleClientError} */
export function handleError({ error, event }) {
  errorFunc('ErrorHandler:Client', event);
  return {
    message: error.toString()
  };
}
