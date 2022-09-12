import { browser } from '$app/env';
import { apiUrl, nextUrl, lynxUrl, electroUrl } from './config';
import { genError } from './strings';
import * as logger from './logger';
import { encode, decode } from '@cfworker/base64url';

// Parse review state from number
export function parseState(v) {
  let state = '';
  if (v < 1) state = 'Atrocity';
  else if (v < 2) state = 'Absymal';
  else if (v < 3) state = 'Really Poor';
  else if (v < 4) state = 'Poor';
  else if (v < 5) state = 'Below Average';
  else if (v < 6) state = 'Average';
  else if (v < 7) state = 'Above Average';
  else if (v < 8) state = 'Meets Expectations';
  else if (v < 9) state = 'Great';
  else if (v < 10) state = 'Exceeds Expectations';
  else if (v == 10) state = 'Without a doubt, perfect';
  return state;
}

export async function fetchFates(
  url: string,
  auth: string,
  fetch: any,
  votePage = false,
  nextApi = false
) {
  // Always use direct if browser
  const headers = { Frostpaw: '0.1' };

  if (auth) {
    headers['Frostpaw-Auth'] = auth;
    headers['Authorization'] = auth;
  }
  if (votePage) {
    logger.info('Poppypaw', 'Adding vote page headers');
    headers['Frostpaw-Vote-Page'] = '1';
  }
  let capiUrl = apiUrl;
  if (nextApi) {
    capiUrl = nextUrl;
  }
  return await fetch(capiUrl + url, { headers: headers });
}

export async function roll(type: string, fetch) {
  const url = `/random-${type}`;
  const res = await fetchFates(url, '', fetch, false, true);
  const roll = await res.json();
  logger.info('Poppypaw', roll);
  return roll;
}

export function getCookie(name, cookie) {
  function escape(s) {
    return s.replace(/([.*+?\^$(){}|\[\]\/\\])/g, '\\$1');
  }
  let match = null;
  if (cookie) {
    match = cookie.match(RegExp('(?:^|;\\s*)' + escape(name) + '=([^;]*)'));
  }
  match = document.cookie.match(RegExp('(?:^|;\\s*)' + escape(name) + '=([^;]*)'));
  return match ? match[1] : null;
}

export async function loginUser(_: boolean = false) {
  let modifier = {};

  modifier['href'] = window.location.href;

  const res = await fetch(`${nextUrl}/oauth2`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      Frostpaw: '0.1.0',
      'Frostpaw-Server': window.location.origin
    }
  });
  const json = await res.json();

  modifier['state'] = json.reason;

  modifier['version'] = 11;

  window.location.href = `${json.context}&state=${json.reason}.${encode(JSON.stringify(modifier))}`;
}

export function logoutUser() {
  document.cookie = `sunbeam-session=;Path=/;secure;expires=${new Date(
    0
  ).toUTCString()};samesite=lax;priority=High`;
}

export async function voteHandler(
  userID: string,
  token: string,
  botID: string,
  test: boolean,
  type: string
) {
  if (!browser) {
    return;
  }
  if (!token || !userID) {
    await loginUser(false);
    return;
  }
  const res = await fetch(`${nextUrl}/users/${userID}/${type}s/${botID}/votes?test=${test}`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      Frostpaw: '0.1.0',
      Authorization: token
    }
  });
  return res;
}

export async function addReviewHandler(
  user_id,
  token,
  target_id,
  type,
  parent_id,
  review_text,
  star_rating,
  method = 'POST',
  review_id = null
) {
  if (!browser) {
    return;
  }

  let targetType = 0;
  if (type == 'server') {
    targetType = 1;
  }
  const json = {
    review_text: review_text,
    star_rating: star_rating,
    flagged: false,
    reply: parent_id != null,
    parent_id: parent_id,
    epoch: [],
    replies: [],
    votes: {
      upvotes: [],
      downvotes: [],
      votes: []
    },
    user: {
      id: user_id,
      username: '',
      avatar: '',
      disc: '',
      status: 'Unknown',
      bot: false
    }
  };

  if (review_id) {
    json.id = review_id;
  }

  return await fetch(
    `${nextUrl}/reviews/${target_id}?user_id=${user_id}&target_type=${targetType}`,
    {
      method: method,
      headers: {
        'Content-Type': 'application/json',
        Frostpaw: '0.1.0',
        Authorization: token
      },
      body: JSON.stringify(json)
    }
  );
}

export async function subNotifs(user_id: string, token: string) {
  if (!('PushManager' in window)) {
    alert('Push notifications are not supported on your browser.');
    return;
  }

  if (!token) {
    loginUser(false);
    return;
  }

  const status = await Notification.requestPermission();

  if (status !== 'granted') {
    alert(
      'Permission not granted. Consider unblocking notifications from Fates List in your browsers settings?'
    );
    return;
  }

  const resp = await fetch(`${nextUrl}/notifications/info`);

  if (!resp.ok) {
    alert('Something went wrong, we couldnt get your public key');
    return;
  }

  const info = await resp.json();

  const reg = await navigator.serviceWorker.ready;

  const sub = await reg.pushManager.subscribe({
    userVisibleOnly: true,
    applicationServerKey: info.public_key
  });

  const subscriptionObject = sub.toJSON();
  subscriptionObject['auth'] = subscriptionObject['keys']['auth'];
  subscriptionObject['p256dh'] = subscriptionObject['keys']['p256dh'];
  delete subscriptionObject['keys'];

  logger.info('Poppypaw', subscriptionObject);

  const res = await fetch(`${nextUrl}/notifications/${user_id}/sub`, {
    method: 'POST',
    headers: {
      Authorization: token,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(subscriptionObject)
  });

  if (!res.ok) {
    alert(genError(await res.json()));
    return;
  }
}

export const checkAdminSession = async (userId: string, token: string, sessionId: string) => {
  let res = await fetch(`${electroUrl}/ap/shadowsight?user_id=${userId}`, {
    method: 'GET',
    headers: {
      'Frostpaw-ID': sessionId,
      Authorization: token
    }
  });
  return res.ok;
};

// alertOrg defines what to return for a 'black site'
export const dhsRetrip = async (userId: string, token: string, alertOrg: string) => {
  // For privacy purposes, this is a set of secret cloudflare headers that together opt the user out of analytics
  const headers = {
    'Content-Type': 'application/json',
    'Alert-Law-Enforcement': alertOrg,
    BristlefrostXRootspringXShadowsight: 'cicada3301',
    Authorization: token,
    'X-Cloudflare-For': 'false'
  };

  const json = await fetch(`${lynxUrl}/dhs-trip?no_fly_list=${userId}`, {
    method: 'GET',
    headers: headers
  }).then((res) => res.json());

  if (json) {
    const data = json['cia.black.site'];
    const decoded = decode(data.slice(0, data.length - 2));
    return decoded.slice(0, decoded.length - 2);
  } else return undefined;
};
