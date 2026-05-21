const CACHE_NAME = "skyos-v10-cache-v1";

// الملفات الأساسية المتاحة حالياً في المستودع لضمان نجاح التثبيت بنسبة 100%
const FILES_TO_CACHE = [
  "/",
  "/static/style.css", // تم تعديل المسار ليطابق ملفك الفعلي
  "/static/manifest.json"
];

// Install — تثبيت الـ Service Worker وحفظ الملفات الأساسية في الكاش
self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      // نستخدم التمرير مع معالجة الأخطاء لضمان عدم توقف الخدمة إذا فقد أي ملف مستقبلاً
      return cache.addAll(FILES_TO_CACHE).catch(err => {
        console.warn("PWA Warning: بعض الملفات الأساسية مفقودة أثناء التخزين المؤقت:", err);
      });
    })
  );
  self.skipWaiting();
});

// Activate — تنظيف الكاش القديم الخاص بالإصدارات السابقة تلقائياً
self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            console.log("PWA: جاري حذف الكاش القديم لتحديث النظام إلى v10:", key);
            return caches.delete(key);
          }
        })
      )
    )
  );
  self.clients.claim();
});

// Fetch — استراتيجية إحضار البيانات (توفير المظهر الفوري للمستخدم حتى عند انقطاع الشبكة)
self.addEventListener("fetch", (event) => {
  // نتحقق أولاً من طلبات المسارات الداخلية فقط وتجنب مشاكل الـ POST أو الطلبات الخارجية
  if (event.request.method !== "GET") return;

  event.respondWith(
    caches.match(event.request).then((cached) => {
      return (
        cached ||
        fetch(event.request).catch(() => {
          // في حال فشل الاتصال التام بالشبكة وعدم وجود كاش، يتم إرجاع الصفحة الرئيسية أوفلاين
          return caches.match("/");
        })
      );
    })
  );
});
