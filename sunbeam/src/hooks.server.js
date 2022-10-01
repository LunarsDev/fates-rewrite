/** @type {import('@sveltejs/kit').HandleServerError} */
export function handleError({ error, event }) {
  return {
    message: error.toString()
  };
}
