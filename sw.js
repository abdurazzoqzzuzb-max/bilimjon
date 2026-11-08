/* Bilimjon — offline kesh. 0.5.0: Firebase SDK ham keshlanadi. Har yangilanishda V ni oshiring. Natija hech qachon keshda emas — u localStorage'da (bj_state_v1). */
/* 🧪 0.7.0: …/beta/sw.js (sinov rejimi) — alohida kesh (bj-beta-…); har SW faqat o'z prefiksidagi eski keshlarni o'chiradi */
const BETA = self.location.pathname.indexOf('/beta/') >= 0, P = BETA ? 'bj-beta-' : 'bj-v';
const V = P + '0.8.0';
const OV = 'bj-ovoz-1';
const SHELL = ['./', 'index.html', 'manifest.webmanifest', 'icon.svg', 'icon-192.png', 'icon-512.png'];
/* 0.7.1 (07.11): GitHub Pages fayllarni 10 daqiqa keshlaydi (max-age=600) — oddiy fetch() eski index.html ni brauzer keshidan berib, yangilanish 10 daqiqagacha kechikardi.
   Endi o'z fayllarimiz tarmoqdan har safar tekshiriladi (no-cache → 304 yoki yangi fayl), install ham brauzer keshini chetlab o'tadi (reload). Yo'naltirish bo'lsa — eski usul. */
const tarmoq = req => fetch(req.url, { cache: 'no-cache', credentials: 'same-origin' }).then(r => r.redirected ? fetch(req) : r).catch(() => fetch(req));
self.addEventListener('install', e => { e.waitUntil(caches.open(V).then(c => c.addAll(SHELL.map(u => new Request(u, { cache: 'reload' })))).then(() => self.skipWaiting())); });
self.addEventListener('activate', e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k.indexOf(P) === 0 && k !== V).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener('fetch', e => {
  const req = e.request; if (req.method !== 'GET') return; const url = new URL(req.url);
  /* 🔄 0.8.0: version.json (yangilanish tekshiruvi) keshlanmaydi — har safar tarmoqdan, ilova o'zi ?t= va no-store bilan so'raydi */
  if (url.origin === location.origin && /\/version\.json$/.test(url.pathname)) return;
  if (url.origin === location.origin && /\/ovoz\/.+\.mp3$/.test(url.pathname)) {
    /* 🔊 0.7.1: ovoz fayllari o'zgarmaydi (matn o'zgarsa — id ham o'zgaradi) — avval kesh, alohida «bj-ovoz-1» (versiya almashganda o'chmaydi) */
    e.respondWith(caches.open(OV).then(c => c.match(req).then(r => r || fetch(req).then(res => { if (res.ok) c.put(req, res.clone()); return res; }))));
  } else if (url.origin === location.origin) {
    /* avval tarmoq (yangi versiya tez yetib borsin), bo'lmasa kesh — internetsiz ham ishlaydi */
    e.respondWith(tarmoq(req).then(r => { if (r.ok) { const cp = r.clone(); caches.open(V).then(c => c.put(req, cp)); } return r; }).catch(() => caches.match(req, { ignoreSearch: true }).then(r => r || caches.match('index.html'))));
  } else if (/fonts\.(googleapis|gstatic)\.com$/.test(url.hostname) || (url.hostname === 'www.gstatic.com' && url.pathname.indexOf('/firebasejs/') === 0)) {
    /* shriftlar va Firebase SDK (versiyali, o'zgarmaydi) — keshdan; Firestore/Auth so'rovlariga tegilmaydi */
    e.respondWith(caches.match(req).then(r => r || fetch(req).then(res => { const cp = res.clone(); caches.open(V).then(c => c.put(req, cp)); return res; }).catch(() => r)));
  }
});
