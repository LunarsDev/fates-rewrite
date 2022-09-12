<script context="module">
  import { nextUrl } from '$lib/config';

  import { genError } from '$lib/strings';

  export const prerender = false;
  export async function load({ params, fetch, session, stuff }) {
    let auth = '';
    if (session.session.user) {
      auth = `${session.session.user.id}|${session.session.token}`;
    }
    let inviteUrl = await fetch(`${nextUrl}/servers/${params.id}`, {
      method: 'GET',
      headers: {
        Frostpaw: '0.1.0',
        'Frostpaw-Auth': auth,
        'Frostpaw-Invite': '1'
      }
    });

    let inviteJson = await inviteUrl.json();

    if (!inviteUrl.ok) {
      return {
        status: 400,
        error: new Error(genError(inviteJson))
      };
    }

    if (!inviteJson.invite_link.startsWith('https://')) {
      inviteJson.invite_link = `https://discord.gg/${inviteJson.invite_link}`;
    }

    return {
      status: 307,
      redirect: inviteJson.invite_link
    };
  }
</script>
