import { browser } from '$app/environment';
import { api, origin } from './config';
import { genError } from './strings';
import * as logger from './logger';
import Base64 from "./b64"
import type { LayoutData } from '.svelte-kit/types/src/routes/$types';
import { page } from '$app/stores';
import { get } from 'svelte/store';

function getTargetType(type: number | string) {
  let targetType = 0;
  if (type == 'server') {
    targetType = 1;
  }
  return targetType;
}

/** Defines an auth for an entity (bot or server) */
interface EntityAuth {
  id: string;
  apiToken: string;
}

type Headers = {
  [key: string]: any;
}

interface AuthOptions {
  method: string;
  headers?: Headers;
  body?: any;
  fetch: any;
  session: LayoutData;
  endpointType: "bot" | "server" | "user";
  entityAuth?: EntityAuth;
  /** Does this request need auth, defaults to false if unset */
  auth?: boolean;
  errorOnFail?: boolean;
}

// Authenticated fetch (should always be preferred to fetch)
export async function request(url: string, options: AuthOptions): Promise<Response> {
  if(options.auth === undefined) options.auth = false;

  if(!options.headers) {
    options.headers = {}
  }

  if(!options.fetch) {
    throw new Error("No fetch function provided");
  }

  logger.info("RequestHandler", `Fetching ${url} with method ${options.method} (auth: ${options.auth})`);

  if (!options.session) {
    throw new Error("Session is undefined");
  }

  if (options.auth) {
    if(options.endpointType == "bot" || options.endpointType == "server") {
      if(!options.entityAuth) {
        throw new Error(`entityAuth must be included for bot endpoint ${url}`);
      }
      options.headers["Frostpaw-Auth"] = `${options.endpointType}|${options.entityAuth.id}|${options.entityAuth.apiToken}`;
    } else {
      if(options.session.token) {
        options.headers["Frostpaw-Auth"] = `${options.endpointType}|${options.session.user.id}|${options.session.token}`
      } else {
        throw new Error("No token found in session");
      }
    }
  }
  
  options.headers["Origin"] = origin;
  options.headers["Content-Type"] = "application/json";

  try {
    let res: Response = await options.fetch(url, {
      method: options.method,
      headers: options.headers,
      body: options.body,
    });

    if(options.errorOnFail && !res.ok) {
      let err = await res.text();
      throw new Error(err);
    }

    return res
  } catch (err) {
    logger.error(err);
    throw new Error(`${err} (url: ${url})`);
  }
}

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

export async function roll(type: string | number, session: any) {
  let targetType = getTargetType(type);
  let res = await request(`${api}/random?target_type=${targetType}&reroll=true`, {
    method: 'GET',
    session: session,
    endpointType: "user",
    auth: false,
    fetch: fetch
  })

  if(res.ok) {
    return await res.json()
  }

  alert("Error: " + res.status + " " + res.statusText + " " + res.url)
  return null
}

export async function loginUser() {
  let modifier = {};

  modifier['href'] = window.location.href;

  const res = await request(`${api}/oauth2`, {
    method: 'GET',
    headers: {
      'Frostpaw-Server': window.location.origin
    },
    session: get(page).data,
    auth: false,
    endpointType: "user",
    fetch: fetch
  });
  const json = await res.json();

  modifier['state'] = json.state;

  modifier['version'] = 11;

  window.location.href = `${json.url}&state=${json.state}.${Base64.encode(JSON.stringify(modifier))}`;
}

export function logoutUser() {
  document.cookie = `sunbeam-session=;Path=/;secure;expires=${new Date(
    0
  ).toUTCString()};samesite=lax;priority=High`;
}

export async function voteHandler(
  id: string,
  test: boolean,
  type: string
) {
  if (!browser) {
    return;
  }

  let targetType = getTargetType(type);

  const res = await request(`${api}/votes/${id}?target_type=${targetType}&test=${test}`, {
    method: 'PATCH',
    session: get(page).data,
    auth: true,
    endpointType: "user",
    fetch: fetch
  });
  return res;
}

export async function addReviewHandler(
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

  let targetType = getTargetType(type);

  let json = {
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
  };

  if (review_id) {
    json["id"] = review_id;
  }

  return await request(
    `${api}/reviews/${target_id}?target_type=${targetType}`, {
      method: method,
      body: JSON.stringify(json),
      session: get(page).data,
      auth: true,
      endpointType: "user",
      fetch: fetch
    }
  );
}

export async function subNotifs(user_id: string, token: string) {
  if (!('PushManager' in window)) {
    alert('Push notifications are not supported on your browser.');
    return;
  }

  if (!token) {
    loginUser();
    return;
  }

  const status = await Notification.requestPermission();

  if (status !== 'granted') {
    alert(
      'Permission not granted. Consider unblocking notifications from Fates List in your browsers settings?'
    );
    return;
  }

  const resp = await request(`${api}/notifications/info`, {
    method: 'GET',
    fetch: fetch,
    session: get(page).data,
    auth: true,
    endpointType: "user"
  });

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

  const res = await request(`${api}/notifications/${user_id}/sub`, {
    method: 'POST',
    headers: {
      Authorization: token,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(subscriptionObject),
    fetch: fetch,
    session: get(page).data,
    auth: true,
    endpointType: "user"
  });

  if (!res.ok) {
    alert(genError(await res.json()));
    return;
  }
}