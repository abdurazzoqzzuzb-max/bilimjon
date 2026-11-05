/* Bilimjon — offline kesh. 0.5.0: Firebase SDK ham keshlanadi. Har yangilanishda V ni oshiring. Natija hech qachon keshda emas — u localStorage'da (bj_state_v1). */
const V = 'bj-v0.6.0';
const SHELL = ['./', 'index.html', 'manifest.webmanifest', 'icon.svg', 'icon-192.png', 'icon-512.png'];
self.addEventListener('install', e => { e.waitUntil(caches.open(V).then(c => c.addAll(SHELL)).then(() => self.skipWaiting())); });
self.addEventListener('activate', e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== V).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener('fetch', e => {
  const req = e.request; if (req.method !== 'GET') return; const url = new URL(req.url);
  if (url.origin === location.origin) {
    /* avval tarmoq (yangi versiya tez yetib borsin), bo'lmasa kesh — internetsiz ham ishlaydi */
    e.respondWith(fetch(req).then(r => { if (r.ok) { const cp = r.clone(); caches.open(V).then(c => c.put(req, cp)); } return r; }).catch(() => caches.match(req, { ignoreSearch: true }).then(r => r || caches.match('index.html'))));
  } else if (/fonts\.(googleapis|gstatic)\.com$/.test(url.hostname) || (url.hostname === 'www.gstatic.com' && url.pathname.indexOf('/firebasejs/') === 0)) {
    /* shriftlar va Firebase SDK (versiyali, o'zgarmaydi) — keshdan; Firestore/Auth so'rovlariga tegilmaydi */
    e.respondWith(caches.match(req).then(r => r || fetch(req).then(res => { const cp = res.clone(); caches.open(V).then(c => c.put(req, cp)); return res; }).catch(() => r)));
  }
});
