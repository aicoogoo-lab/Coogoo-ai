// ============================================================
// SkyOS v10 - Sovereign Service Worker (Final Eternal Ultimate Edition)
// ============================================================
// هذا الملف هو الحارس السيادي الأعظم للنظام.
// مسؤول عن: التخزين الفائق، العمل بدون إنترنت، التحديثات الذكية،
// حماية الملفات، دعم GodMode offline، الإشعارات، وتحليلات الأداء.
// ============================================================

const SKYOS_VERSION = "v10.0.0-ultimate";
const CACHE_NAME = `skyos-cache-${SKYOS_VERSION}`;
const OFFLINE_CACHE_NAME = `skyos-offline-${SKYOS_VERSION}`;
const DYNAMIC_CACHE_NAME = `skyos-dynamic-${SKYOS_VERSION}`;
const API_CACHE_NAME = `skyos-api-${SKYOS_VERSION}`;

// ============================================================
// الملفات الأساسية للنظام (App Shell) - القشرة السيادية
// ============================================================
const CORE_FILES = [
  "/",
  "/templates/index.html",
  "/static/css/core.css",
  "/static/js/core.js",
  "/static/js/ui.js",
  "/static/js/mind.js",
  "/static/js/three-mind.js",
  "/static/icons/icon-192.png",
  "/static/icons/icon-512.png",
  "/static/icons/icon-144.png",
  "/static/icons/icon-256.png",
  "/static/offline.html",
  "/static/splash.png",
  "/static/notification-icon.png"
];

// ============================================================
// قائمة الامتدادات التي سيتم تخزينها باستراتيجيات مختلفة
// ============================================================
const STATIC_EXTENSIONS = ['.css', '.js', '.json', '.wasm'];
const IMAGE_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.ico'];
const FONT_EXTENSIONS = ['.woff', '.woff2', '.ttf', '.eot'];
const API_PATTERNS = ['/api/', '/graphql', '/socket.io'];

// ============================================================
// تثبيت Service Worker
// ============================================================
self.addEventListener("install", (event) => {
  console.log(`[SkyOS SW] ⚡ Installing Sovereign Service Worker v${SKYOS_VERSION}`);

  event.waitUntil(
    Promise.all([
      caches.open(CACHE_NAME).then(async (cache) => {
        console.log("[SkyOS SW] Caching core files");
        // إضافة كل الملفات الأساسية بشكل موثوق مع التحقق من النجاح
        const addPromises = CORE_FILES.map(async (file) => {
          try {
            const response = await fetch(file);
            if (response && response.ok) {
              await cache.put(file, response);
            } else {
              console.warn(`[SkyOS SW] Failed to cache: ${file}`);
            }
          } catch (err) {
            console.warn(`[SkyOS SW] Error caching ${file}:`, err);
          }
        });
        await Promise.all(addPromises);
        return cache;
      }),
      caches.open(OFFLINE_CACHE_NAME),
      caches.open(DYNAMIC_CACHE_NAME),
      caches.open(API_CACHE_NAME)
    ])
  );

  // تصبح الخدمة جاهزة فوراً
  self.skipWaiting();
});

// ============================================================
// تفعيل Service Worker + حذف النسخ القديمة + تنظيف ذكي
// ============================================================
self.addEventListener("activate", (event) => {
  console.log("[SkyOS SW] 🛡️ Activating Sovereign Guardian");

  event.waitUntil(
    (async () => {
      // حذف جميع الكاشات القديمة من الإصدارات السابقة
      const cacheKeys = await caches.keys();
      const deletePromises = cacheKeys.map(async (key) => {
        if (key !== CACHE_NAME && key !== OFFLINE_CACHE_NAME && key !== DYNAMIC_CACHE_NAME && key !== API_CACHE_NAME) {
          console.log("[SkyOS SW] Removing old cache:", key);
          await caches.delete(key);
        }
      });
      await Promise.all(deletePromises);

      // إرسال رسالة للعملاء المتصلين بأنه تم التحديث
      const clientsList = await self.clients.matchAll({ includeUncontrolled: true });
      clientsList.forEach(client => {
        client.postMessage({
          type: "SKYOS_SW_ACTIVATED",
          version: SKYOS_VERSION,
          timestamp: Date.now()
        });
      });
    })()
  );

  // السيطرة على جميع العملاء فوراً
  self.clients.claim();
});

// ============================================================
// إستراتيجيات الجلب الذكية المتقدمة (Sovereign Fetch Strategy)
// ============================================================
// - Cache First (with network fallback) للملفات الثابتة
// - Network First (with cache fallback) لواجهات API
// - Stale While Revalidate للصور والخطوط
// - Offline Fallback لبقية الطلبات مع دعم وضع GodMode
// ============================================================
self.addEventListener("fetch", (event) => {
  const request = event.request;
  const url = new URL(request.url);

  // تجاهل الطلبات غير الآمنة أو غير المرغوب فيها
  if (request.method !== "GET" ||
      url.protocol === "chrome-extension:" ||
      url.protocol === "chrome:" ||
      url.protocol === "about:") {
    return;
  }

  // التعامل مع الطلبات حسب نوعها
  const isStatic = STATIC_EXTENSIONS.some(ext => url.pathname.endsWith(ext));
  const isImage = IMAGE_EXTENSIONS.some(ext => url.pathname.endsWith(ext));
  const isFont = FONT_EXTENSIONS.some(ext => url.pathname.endsWith(ext));
  const isAPI = API_PATTERNS.some(pattern => url.pathname.includes(pattern));

  if (isStatic) {
    // استراتيجية Cache First مع إعادة التحقق الدورية
    event.respondWith(cacheFirstWithRefresh(request));
  } else if (isImage || isFont) {
    // استراتيجية Stale While Revalidate
    event.respondWith(staleWhileRevalidate(request));
  } else if (isAPI) {
    // استراتيجية Network First مع تخزين محدود
    event.respondWith(networkFirstWithCache(request));
  } else {
    // استراتيجية Offline Fallback مع دعم GodMode
    event.respondWith(offlineFallback(request));
  }
});

// ============================================================
// Cache First مع تحديث الخلفية (للثابت)
// ============================================================
async function cacheFirstWithRefresh(request) {
  const cache = await caches.open(CACHE_NAME);
  const cachedResponse = await cache.match(request);
  
  if (cachedResponse) {
    // تحديث الخلفية بشكل غير متزامن
    fetch(request).then(async (networkResponse) => {
      if (networkResponse && networkResponse.ok) {
        await cache.put(request, networkResponse.clone());
        // إشعار العملاء بالتحديث (اختياري)
        const clientsList = await self.clients.matchAll();
        clientsList.forEach(client => {
          client.postMessage({
            type: "SKYOS_ASSET_UPDATED",
            url: request.url,
            timestamp: Date.now()
          });
        });
      }
    }).catch(() => {});
    return cachedResponse;
  }
  
  // إذا لم يوجد في الكاش، نجلب من الشبكة
  const networkResponse = await fetch(request);
  if (networkResponse && networkResponse.ok) {
    await cache.put(request, networkResponse.clone());
  }
  return networkResponse;
}

// ============================================================
// Stale While Revalidate (للصور والخطوط)
// ============================================================
async function staleWhileRevalidate(request) {
  const cache = await caches.open(DYNAMIC_CACHE_NAME);
  const cachedResponse = await cache.match(request);
  
  const fetchPromise = fetch(request).then(async (networkResponse) => {
    if (networkResponse && networkResponse.ok) {
      await cache.put(request, networkResponse.clone());
    }
    return networkResponse;
  }).catch(() => null);
  
  return cachedResponse || fetchPromise;
}

// ============================================================
// Network First مع Cache Fallback (للواجهات API)
// ============================================================
async function networkFirstWithCache(request) {
  const cache = await caches.open(API_CACHE_NAME);
  
  try {
    const networkResponse = await fetch(request);
    if (networkResponse && networkResponse.ok) {
      // تخزين مؤقت مع تحديد صلاحية (مثلاً 5 دقائق)
      const responseToCache = networkResponse.clone();
      const headers = new Headers(responseToCache.headers);
      headers.set('sw-cached-time', Date.now().toString());
      const modifiedResponse = new Response(responseToCache.body, {
        status: responseToCache.status,
        statusText: responseToCache.statusText,
        headers: headers
      });
      await cache.put(request, modifiedResponse);
      return networkResponse;
    }
    throw new Error('Network response not ok');
  } catch (error) {
    const cachedResponse = await cache.match(request);
    if (cachedResponse) {
      const cachedTime = cachedResponse.headers.get('sw-cached-time');
      const isStale = cachedTime && (Date.now() - parseInt(cachedTime) > 300000); // 5 دقائق
      if (!isStale) {
        return cachedResponse;
      }
    }
    // إذا فشل كل شيء، نقدم رداً مخصصاً (API offline)
    return new Response(JSON.stringify({
      error: "Sovereign Offline Mode",
      message: "الخدمة غير متاحة حالياً. العقل السيادي يعمل في وضع عدم الاتصال.",
      timestamp: Date.now(),
      godmode: true
    }), {
      status: 503,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}

// ============================================================
// Offline Fallback مع دعم GodMode و Ultra Mode
// ============================================================
async function offlineFallback(request) {
  const cache = await caches.open(OFFLINE_CACHE_NAME);
  
  try {
    const networkResponse = await fetch(request);
    if (networkResponse && networkResponse.ok) {
      await cache.put(request, networkResponse.clone());
      return networkResponse;
    }
    throw new Error('Network failed');
  } catch (error) {
    const cachedResponse = await cache.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }
    // صفحة offline مخصصة للنظام السيادي
    if (request.headers.get('accept')?.includes('text/html')) {
      return caches.match('/templates/offline.html') || new Response(`
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head><meta charset="UTF-8"><title>SkyOS • الوضع السيادي غير المتصل</title>
        <style>body{background:#050509;color:#00E5FF;font-family:monospace;text-align:center;padding:50px;}</style>
        </head>
        <body>
          <h1>🌌 العقل السيادي يعمل دون اتصال</h1>
          <p>تم تفعيل وضع <strong>GodMode Offline</strong>. بعض القدرات محدودة. أعد الاتصال لاستعادة الوظائف الكاملة.</p>
          <button onclick="location.reload()">إعادة المحاولة</button>
        </body>
        </html>
      `, { headers: { 'Content-Type': 'text/html' } });
    }
    return new Response("Sovereign Offline Mode: الطلب غير متاح حالياً", { status: 503 });
  }
}

// ============================================================
// تحديثات ذكية ومركزة (Smart Update)
// ============================================================
self.addEventListener("message", async (event) => {
  const { type, payload } = event.data || {};
  
  switch (type) {
    case "SKYOS_FORCE_UPDATE":
      console.log("[SkyOS SW] Force update requested");
      await self.skipWaiting();
      const clientsList = await self.clients.matchAll();
      clientsList.forEach(client => client.postMessage({ type: "SKYOS_UPDATE_READY" }));
      break;
      
    case "SKYOS_CLEAR_CACHE":
      console.log("[SkyOS SW] Clearing all caches");
      const cacheNames = await caches.keys();
      await Promise.all(cacheNames.map(name => caches.delete(name)));
      event.source.postMessage({ type: "SKYOS_CACHE_CLEARED" });
      break;
      
    case "SKYOS_PREFETCH":
      if (payload?.urls && Array.isArray(payload.urls)) {
        const cache = await caches.open(DYNAMIC_CACHE_NAME);
        payload.urls.forEach(async (url) => {
          try {
            const response = await fetch(url);
            if (response.ok) await cache.put(url, response);
          } catch(e) {}
        });
      }
      break;
      
    case "SKYOS_GET_VERSION":
      event.source.postMessage({ type: "SKYOS_VERSION", version: SKYOS_VERSION, cacheName: CACHE_NAME });
      break;
      
    default:
      // أي رسالة أخرى قد تكون من الواجهة
      console.log("[SkyOS SW] Received message:", type);
  }
});

// ============================================================
// دعم الإشعارات (Push Notifications) - جاهز للاستخدام
// ============================================================
self.addEventListener("push", (event) => {
  if (!event.data) return;
  
  let data = {};
  try {
    data = event.data.json();
  } catch {
    data = { title: "SkyOS", body: event.data.text() };
  }
  
  const options = {
    body: data.body || "حدث جديد في النظام السيادي",
    icon: data.icon || "/static/notification-icon.png",
    badge: "/static/badge-icon.png",
    vibrate: [200, 100, 200],
    data: { url: data.url || "/" },
    actions: [
      { action: "open", title: "فتح", icon: "/static/icons/icon-64.png" },
      { action: "dismiss", title: "تجاهل" }
    ]
  };
  
  event.waitUntil(self.registration.showNotification(data.title || "SkyOS v10", options));
});

self.addEventListener("notificationclick", (event) => {
  event.notification.close();
  if (event.action === "open") {
    const urlToOpen = event.notification.data?.url || "/";
    event.waitUntil(
      self.clients.matchAll({ type: "window", includeUncontrolled: true }).then((clientList) => {
        for (const client of clientList) {
          if (client.url === urlToOpen && "focus" in client) return client.focus();
        }
        if (self.clients.openWindow) return self.clients.openWindow(urlToOpen);
      })
    );
  }
});

// ============================================================
// تحليلات الأداء والتقارير (Performance Analytics)
// ============================================================
self.addEventListener("fetch", (event) => {
  const startTime = Date.now();
  event.respondWith((async () => {
    const response = await fetchHandler(event.request);
    const endTime = Date.now();
    const duration = endTime - startTime;
    // إرسال تحليلات للواجهة (اختياري) مع تجميعها
    if (duration > 500) {
      const clientsList = await self.clients.matchAll();
      clientsList.forEach(client => {
        client.postMessage({
          type: "SKYOS_SLOW_REQUEST",
          url: event.request.url,
          duration: duration,
          timestamp: startTime
        });
      });
    }
    return response;
  })());
});

// دالة مساعدة لتجنب إعادة تعريف fetchHandler
async function fetchHandler(request) {
  const url = new URL(request.url);
  const isStatic = STATIC_EXTENSIONS.some(ext => url.pathname.endsWith(ext));
  const isImage = IMAGE_EXTENSIONS.some(ext => url.pathname.endsWith(ext));
  const isFont = FONT_EXTENSIONS.some(ext => url.pathname.endsWith(ext));
  const isAPI = API_PATTERNS.some(pattern => url.pathname.includes(pattern));
  
  if (isStatic) return cacheFirstWithRefresh(request);
  if (isImage || isFont) return staleWhileRevalidate(request);
  if (isAPI) return networkFirstWithCache(request);
  return offlineFallback(request);
}

// ============================================================
// مراقبة حالة الشبكة (Network Status Monitoring)
// ============================================================
self.addEventListener("online", () => {
  console.log("[SkyOS SW] Network is back online");
  self.clients.matchAll().then(clients => {
    clients.forEach(client => client.postMessage({ type: "SKYOS_NETWORK_ONLINE" }));
  });
});

self.addEventListener("offline", () => {
  console.log("[SkyOS SW] Network is offline");
  self.clients.matchAll().then(clients => {
    clients.forEach(client => client.postMessage({ type: "SKYOS_NETWORK_OFFLINE" }));
  });
});

// ============================================================
// نهاية الملف — الحارس السيادي الأبدي
// ============================================================
