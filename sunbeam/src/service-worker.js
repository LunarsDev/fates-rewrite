import * as logger from '$lib/logger';

let CACHE_NAME = 'cache-' + Date.now();

self.addEventListener('install', (event) => {
  logger.info('Service Worker', 'Installed');
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.add('https://api.fateslist.xyz/static/offline.html');
    })
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  logger.info('Service Worker', 'Activated');
  event.waitUntil(
    // Loop through the cache
    caches.keys().then((keys) => {
      // We must return a promise so it gets awaited
      return Promise.all(
        keys.map((k) => {
          // If the key doesn't match the name of the current cache, delete it
          if (k !== CACHE_NAME) return caches.delete(k);
        })
      );
    })
  );
});

self.addEventListener('fetch', (event) => {
  // We only want to send /offline.html when the user is navigating pages,
  // not when they're requesting something else like CSS files or API requests.
  if (event.request.mode !== 'navigate') return;

  event.respondWith(
    fetch(event.request).catch(() => {
      return caches.open(CACHE_NAME).then((cache) => {
        return cache.match('offline.html');
      });
    })
  );
});

self.addEventListener('push', (event) => {
  logger.info('Service Worker', `Push Recieved ${event.data.json()}`);
  console.log('Push received of', event.data.json());
});
