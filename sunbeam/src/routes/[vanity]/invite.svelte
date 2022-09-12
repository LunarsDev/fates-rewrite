<script context="module" lang="ts">
  import { fetchFates } from '$lib/request';
  export const prerender = false;
  export async function load({ params, fetch, session, stuff }) {
    let auth = '';

    if (session.session.user) {
      auth = `${session.session.user.id}|${session.session.token}`;
    }

    const codeUrl = `/code/${params.vanity}`;
    const codeRes = await fetchFates(codeUrl, auth, fetch, false, true);

    if (codeRes.ok) {
      let data = await codeRes.json();
      let id: string = data.target_id;
      let type: string = data.target_type;

      if (type == 'bot') {
        return {
          status: 307,
          redirect: `/bot/${id}/invite`
        };
      } else {
        return {
          status: 307,
          redirect: `/server/${id}/invite`
        };
      }
    }
  }
</script>
