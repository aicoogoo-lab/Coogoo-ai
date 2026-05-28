/**
 * SAMA Service Worker
 * تخزين مؤقت ذكي للملفات الأساسية
 */

const CACHE_NAME = 'sama-cache-v10.5';
const ASSETS_TO_CACHE = [
    '/',
    '/static/css/core.css',
    '/static/js/sama-api.js',
    '/static/js/sama-ui.js',
    '/static/manifest.json'
];

// التثبيت
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(ASSETS_TO_CACHE);
        })
    );
    self.skipWaiting();
});

// التفعيل
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((keys) => {
            return Promise.all(
                keys.filter(key => key !== CACHE_NAME)
                    .map(key => caches.delete(key))
            );
        })
    );
    self.clients.claim();
});

// الجلب
self.addEventListener('fetch', (event) => {
    // لا نخزن طلبات API
    if (event.request.url.includes('/command') ||
        event.request.url.includes('/status') ||
        event.request.url.includes('/master') ||
        event.request.url.includes('/awaken') ||
        event.request.url.includes('/shutdown')) {
        return;
    }

    event.respondWith(
        caches.match(event.request).then((cached) => {
            const fetchPromise = fetch(event.request).then((response) => {
                if (response && response.status === 200) {
                    const responseClone = response.clone();
                    caches.open(CACHE_NAME).then((cache) => {
                        cache.put(event.request, responseClone);
                    });
                }
                return response;
            });
            return cached || fetchPromise;
        })
    );
});
