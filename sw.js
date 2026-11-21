// Avisos de vídeo novo (OneSignal). Se falhar (sem internet), o app continua funcionando.
try { importScripts("https://cdn.onesignal.com/sdks/web/v16/OneSignalSDK.sw.js"); } catch (e) {}
// Rede primeiro (sempre a versão mais nova do app e dos vídeos); sem internet, usa a cópia guardada.
const CACHE = "reforma-v3";
const BASE = ["./", "index.html", "estilo.css", "app.js", "manifest.webmanifest",
  "icones/icone-192.png", "icones/icone-512.png", "dados/videos.json"];

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(BASE)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", (e) => {
  e.waitUntil(caches.keys().then((ks) => Promise.all(ks.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
    .then(() => self.clients.claim()));
});
self.addEventListener("fetch", (e) => {
  if (e.request.method !== "GET" || new URL(e.request.url).origin !== location.origin) return;
  e.respondWith(fetch(e.request).then((r) => {
    if (r.ok) { const c = r.clone(); caches.open(CACHE).then((k) => k.put(e.request, c)); }
    return r;
  }).catch(() => caches.match(e.request)));
});
