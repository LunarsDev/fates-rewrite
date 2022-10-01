import { redirect } from '@sveltejs/kit';

/** @type {import('./$types').PageLoad} */
export async function load({ params }) {
  throw redirect(307, `/bot/${params.id}/${params.route}`);
}
