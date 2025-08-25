// Версия кеша (меняйте при обновлении файлов)
const CACHE_NAME = 'pass-pwa-cache-v1'

// Список файлов для кеширования
const urlsToCache = []
const ASSETS = [
	'/', // главная страница
	'/app/home', // start_url из manifest.json
	'/static/icon-192x192.png', // иконка
	'/static/manifest.json', // манифест
]
// Установка Service Worker и кеширование файлов
self.addEventListener('install', event => {
	event.waitUntil(
		caches.open(CACHE_NAME).then(cache => {
			console.log('Кешируем файлы')
			return cache.addAll(urlsToCache)
		})
	)
})

// Активация и очистка старых кешей
self.addEventListener('activate', event => {
	event.waitUntil(
		caches.keys().then(cacheNames => {
			return Promise.all(
				cacheNames.map(cache => {
					if (cache !== CACHE_NAME) {
						console.log('Удаляем старый кеш:', cache)
						return caches.delete(cache)
					}
				})
			)
		})
	)
})

// Стратегия: "Сначала из кеша, потом сеть"
self.addEventListener('fetch', event => {
	event.respondWith(
		caches.match(event.request).then(response => {
			return response || fetch(event.request)
		})
	)
})

self.addEventListener('fetch', event => {
	event.respondWith(
		caches.match(event.request).then(response => {
			// Если файл есть в кеше — возвращаем его, но параллельно обновляем
			const fetchPromise = fetch(event.request).then(networkResponse => {
				caches.open(CACHE_NAME).then(cache => {
					cache.put(event.request, networkResponse.clone())
				})
				return networkResponse
			})
			return response || fetchPromise
		})
	)
})
