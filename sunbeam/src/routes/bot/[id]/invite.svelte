<script context="module">
  export const prerender = false;
  import { nextUrl } from '$lib/config';
  import * as logger from '$lib/logger';

  export async function load({ params, fetch, session, stuff }) {
    let auth = '';
    if (session.session.user) {
      auth = `${session.session.user.id}|${session.session.token}`;
    }
    let inviteUrl = await fetch(`${nextUrl}/bots/${params.id}`, {
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
        error: new Error(`${inviteUrl.reason}`)
      };
    }

    // JS and URLS do not go well together
    logger.info(
      'BotInvite',
      'Parsed invite info',
      inviteJson,
      decodeURIComponent(inviteJson.invite_link)
    );
    return {
      status: 307,
      redirect: decodeURIComponent(inviteJson.invite_link)
    };
  }
</script>
