import { fetchFates } from '$lib/request';
export const prerender = false;

/** @type {import('../../$types').PageLoad} */
export async function load({ params, fetch }) {
  const url = `/bots/${params.id}`;

  let auth = '';

  if (session.session.user) {
    auth = `${session.session.user.id}|${session.session.token}`;
  }

  const res = await fetchFates(url, auth, fetch, false, true);

  if (res.ok) {
    let data = await res.json();
    return {
      props: {
        data: data
      }
    };
  }

  return {
    status: res.status,
    error: new Error(`Bot Not Found`)
  };
}