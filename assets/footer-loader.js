<!-- assets/footer-loader.js -->
(function () {
  const host = document.getElementById('app-footer');
  if (!host) return;

  const candidates = ['footer.html', '../footer.html', './footer.html', '../../footer.html'];

  (async () => {
    let found = null;
    for (const p of candidates) {
      try {
        const r = await fetch(p, { cache: 'no-cache' });
        if (r.ok) { found = { url: p, text: await r.text() }; break; }
      } catch (_) {}
    }
    if (!found) { host.innerHTML = '<div class="container muted small">Footer no encontrado.</div>'; return; }

    host.innerHTML = found.text;

    // Ejecutar <script> dentro del footer inyectado (por si lo usás)
    host.querySelectorAll('script').forEach((old) => {
      const s = document.createElement('script');
      if (old.src) s.src = new URL(old.getAttribute('src'), found.url).toString();
      else s.textContent = old.textContent;
      document.body.appendChild(s);
      old.remove();
    });
  })();
})();
