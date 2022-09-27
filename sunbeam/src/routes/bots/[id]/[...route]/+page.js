/** @type {import('./$types').PageLoad} */
export async function load({ params }) {
  return {
    status: 307,
    redirect: `/bot/${params.id}/${params.route}`
  };
}