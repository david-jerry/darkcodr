import { precacheAndRoute } from "workbox-precaching/precacheAndRoute";
import { CacheableResponsePlugin } from "workbox-cacheable-response";
// import { setDefaultHandler, registerRoute } from "workbox-routing";
// import { registerRoute, setCatchHandler } from "workbox-routing";
import { setCatchHandler, setDefaultHandler, registerRoute } from "workbox-routing";
// import { NetworkOnly, StaleWhileRevalidate } from "workbox-strategies";
import { StaleWhileRevalidate } from "workbox-strategies";
import { ExpirationPlugin } from "workbox-expiration";

const manifest = self.__WB_MANIFEST;

const OFFLINE_URL = "{{offline_url}}";
const CACHE_NAME = "offline-html";
const LOGO_URL = "{{logo_url}}";

if (manifest) {
    console.log("precaching: ", manifest);
    precacheAndRoute(
        manifest,
        {url: "{{home_url}}", revision: "{{home_revision}}"},
        {url: "{{about_url}}", revision: "{{about_revision}}"},
        {url: "{{service_url}}", revision: "{{service_revision}}"},
        {url: "{{offline_url}}", revision: "{{offline_revision}}"},
    );
}

registerRoute(
    ({ url }) => url.origin === "https://unpkg.com" || url.origin === "https://api.userway.org" || url.origin === "https://cdn.userway.org" || url.origin === "https://cdnjs.cloudflare.com" || url.origin === "https://polyfill.io" || url.origin === "https://maps.googleapis.com" || url.origin === "https://fonts.googleapis.com" || url.origin === "https://fonts.gstatic.com",
    new StaleWhileRevalidate({
        cacheName: `google-fonts`,
        plugins: [
            new CacheableResponsePlugin({
                statuses: [0, 200],
            }),
            new ExpirationPlugin({ maxEntries: 20 }),
        ],
    })
);

registerRoute(
    ({ request }) => request.destination === 'audio',
    new StaleWhileRevalidate({
        cacheName: `audio-cache`,
        plugins: [
            new CacheableResponsePlugin({
                statuses: [0, 200],
            }),
            new ExpirationPlugin({ maxEntries: 60, maxAgeSeconds: 30 * 24 * 60 * 60, }),
        ],
    })
);


self.addEventListener("install", function (event) {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => cache.add(
            new Request(OFFLINE_URL, { cache: "reload"})
        ))
    );

    self.skipWaiting();
    console.log(`[SW] Service Worker Installed - ${event}`);
});

self.addEventListener("activate", function (event) {
    self.clients.claim();
    console.log(`[SW] Service Worker Activated - ${event.request.url}`);
});

setDefaultHandler(
    new StaleWhileRevalidate()
);

setCatchHandler(({ event }) => {
    console.log(`[SW] Catch Handler for - ${event}`);
    switch (event.request.destination) {
        case 'document':
            return caches.match(OFFLINE_URL);
        default:
            return Response.error();
    }
});

self.addEventListener('push', event => {
    let notificationTitle = 'Push Notification';
    let notificationOptions;
    try {
        const responseJson = event.data.json();
        notificationTitle = responseJson.title;
        notificationOptions = {
            body: responseJson.body,
            icon: LOGO_URL,
        };
    } catch (err) {
        notificationOptions = {
            body: event.data.text(),
        };
    }

    event.waitUntil(self.registration.showNotification(notificationTitle, notificationOptions));
    console.log(`[SW] [PUSH] Notification - ${event.request.url}`);
});

self.addEventListener('appinstalled', event => {
    console.log("[SW] App installed", event);
});

