// Версия сервис воркера
const CACHE_NAME = 'passout-pwa-v1.0.0';
const urlsToCache = [
  '/',
  '/app',
  '/static/js/bundle.js',
  '/static/css/main.css',
  '/assets/index.js',
  '/manifest.json',
  '/favicon.ico'
];

// Установка сервис воркера
self.addEventListener('install', (event) => {
  console.log('Service Worker: Installing...');
  
  // Пропускаем ожидание и активируем сразу
  self.skipWaiting();
  
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('Service Worker: Caching app shell');
        return cache.addAll(urlsToCache);
      })
      .then(() => {
        console.log('Service Worker: Install completed');
      })
  );
});

// Активация сервис воркера
self.addEventListener('activate', (event) => {
  console.log('Service Worker: Activating...');
  
  // Удаляем старые кэши
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cache) => {
          if (cache !== CACHE_NAME) {
            console.log('Service Worker: Removing old cache:', cache);
            return caches.delete(cache);
          }
        })
      );
    })
  );
  
  // Захватываем контроль над клиентами сразу
  event.waitUntil(self.clients.claim());
  console.log('Service Worker: Activated');
});

// Перехват сетевых запросов
self.addEventListener('fetch', (event) => {
  // Пропускаем не-GET запросы и chrome-extension
  if (event.request.method !== 'GET' || 
      event.request.url.startsWith('chrome-extension://')) {
    return;
  }

  event.respondWith(
    caches.match(event.request)
      .then((response) => {
        // Возвращаем кэшированный response если есть
        if (response) {
          return response;
        }

        // Иначе делаем сетевой запрос
        return fetch(event.request)
          .then((response) => {
            // Проверяем валидный ли response
            if (!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }

            // Клонируем response для кэширования
            const responseToCache = response.clone();

            caches.open(CACHE_NAME)
              .then((cache) => {
                // Кэшируем только важные ресурсы
                const shouldCache = [
                  '/static/',
                  '/assets/',
                  '.js',
                  '.css',
                  '.json',
                  '.ico',
                  '.png',
                  '.jpg',
                  '.webp',
                  '.svg'
                ].some(ext => event.request.url.includes(ext));

                if (shouldCache) {
                  cache.put(event.request, responseToCache);
                }
              });

            return response;
          })
          .catch(() => {
            // Fallback для страниц
            if (event.request.destination === 'document') {
              return caches.match('/');
            }
          });
      })
  );
});

// Фоновая синхронизация (опционально)
self.addEventListener('sync', (event) => {
  if (event.tag === 'background-sync') {
    console.log('Service Worker: Background sync');
    event.waitUntil(doBackgroundSync());
  }
});

async function doBackgroundSync() {
  // Ваша фоновая логика
  console.log('Background sync in progress...');
}

// Получение push-уведомлений
self.addEventListener('push', (event) => {
  if (event.data) {
    const data = event.data.json();
    const options = {
      body: data.body || 'Новое уведомление',
      icon: '/icons/icon-192x192.png',
      badge: '/icons/icon-72x72.png',
      vibrate: [200, 100, 200],
      tag: 'pwa-notification'
    };

    event.waitUntil(
      self.registration.showNotification(data.title || 'PassOut', options)
    );
  }
});

// Обработка кликов по уведомлениям
self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  
  event.waitUntil(
    clients.openWindow('/app')
  );
});