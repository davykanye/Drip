self.addEventListener('install', e => {
  e.waitUntil(
    caches.open('staticfiles').then(cache => {
      return cache.addAll([])
    })
  )
});

self.addEventListener('fetch',() => console.log("fetch"));
