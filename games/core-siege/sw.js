/* CORE SIEGE 서비스 워커 — 코어 파일 프리캐시 + 에셋 런타임 캐시(오프라인 플레이) */
const VERSION = 'cs-v2';
const CORE = [
  './',
  'index.html',
  'manifest.json',
  'js/core.js',
  'js/i18n.js',
  'js/entities.js',
  'js/game.js',
  'assets/icon.png',
  'assets/keyart.webp',
];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(VERSION).then(c => c.addAll(CORE)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== VERSION).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

// 코드(html/js/json)=네트워크 우선(항상 최신, 오프라인 시 캐시 폴백)
// 에셋(webp/mp4/png)=캐시 우선 + 백그라운드 갱신(즉시 로드)
self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  if (e.request.method !== 'GET' || url.origin !== location.origin) return;
  if (url.pathname.includes('/upload')) return; // 개발용 엔드포인트 제외
  const isCode = /\.(html|js|json)$/.test(url.pathname) || url.pathname === '/' || url.pathname.endsWith('/');
  e.respondWith(
    caches.open(VERSION).then(cache => {
      if (isCode) {
        return fetch(e.request)
          .then(res => {
            if (res && res.ok) cache.put(e.request, res.clone());
            return res;
          })
          .catch(() => cache.match(e.request));
      }
      return cache.match(e.request).then(hit => {
        const refresh = fetch(e.request)
          .then(res => {
            if (res && res.ok) cache.put(e.request, res.clone());
            return res;
          })
          .catch(() => hit);
        return hit || refresh;
      });
    })
  );
});
