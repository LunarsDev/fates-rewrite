/** @type {import('./$types').PageLoad} */
export async function load() {
  return {
    status: 307,
    redirect: 'https://fateslist.xyz/frostpaw/add-bot'
  };
}