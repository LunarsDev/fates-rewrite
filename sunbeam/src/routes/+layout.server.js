import cookie from 'cookie';
import * as logger from '$lib/logger';


/** @type {import('./$types').LayoutServerLoad} */
export async function load({ request, setHeaders }) {
    logger.info('Auth', 'getSession called');

    const cookies = cookie.parse(
      request.headers.get('cookie') || request.headers.get('Cookie') || ''
    );
  
    let sessionData = {
      user: {
        id: '',
        username: '',
        disc: '0000',
        avatar: 'https://cdn.discordapp.com/embed/avatars/0.png'
      },
      token: '',
      css: '',
      refresh_token: '',
      user_experiments: [2, 5, 6],
      site_lang: 'en',
      admin_ticket: "",
      url: request.url
    };
  
    let adminData = '';
  
    if (cookies['_adminsession']) {
      adminData = cookies['_adminsession'];
    }
  
    if (cookies['sunbeam-session']) {
      const newJwt = cookies['sunbeam-session'];
  
      try {
        sessionData = JSON.parse(newJwt);
        sessionData.admin_ticket = adminData;
        sessionData.url = request.url
      } catch (e) {
        logger.error('Auth', e);
      }
    }
  
    return sessionData;  
}
  