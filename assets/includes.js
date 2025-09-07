<script>
/* Carga elementos con data-include="archivo.html", inicializa i18n y marca nav activo */
(async function includePartials() {
  async function injectOnce() {
    const nodes = Array.from(document.querySelectorAll('[data-include]'));
    if (!nodes.length) return false;
    for (const el of nodes) {
      const url = el.getAttribute('data-include');
      try {
        const res = await fetch(url, { cache: 'no-cache' });
        const html = await res.text();
        el.insertAdjacentHTML('afterend', html);
        el.remove();
      } catch (e) {
        el.outerHTML = `<!-- include failed: ${url} -->`;
        console.warn('Include failed:', url, e);
      }
    }
    return true;
  }

  // Permite includes anidados (header dentro de algo, etc.)
  while (await injectOnce()) {}

  // === Helpers post-include ===
  function getLang() {
    const qs = new URLSearchParams(location.search).get('lang');
    const st = localStorage.getItem('lang');
    const nv = (navigator.language || 'es').slice(0,2).toLowerCase();
    const v = (qs || st || nv);
    return v.startsWith('pt') ? 'pt' : v.startsWith('en') ? 'en' : 'es';
  }

  function markActiveNav() {
    const here = location.pathname.split('/').pop() || 'index.html';
    document.querySelectorAll('header.nav nav a').forEach(a => {
      const href = a.getAttribute('href') || '';
      // Coincidencia por archivo (precios.html, descarga.html) o por hash para index
      const isActive =
        (href && href.split('#')[0] === here) ||
        (here === 'index.html' && href.startsWith('index.html#'));
      a.classList.toggle('active', !!isActive);
    });
  }

  // i18n: si la página ya definió applyI18n(lang), la ejecutamos
  const lang = getLang();
  try {
    if (window.applyI18n) window.applyI18n(lang);
  } catch {}

  // Sincroniza selector <select id="lang"> del header
  const sel = document.getElementById('lang');
  if (sel) {
    sel.value = lang;
    sel.addEventListener('change', e => {
      const l = e.target.value;
      localStorage.setItem('lang', l);
      if (window.applyI18n) window.applyI18n(l);
      const u = new URL(location.href);
      u.searchParams.set('lang', l);
      history.replaceState({}, '', u);
    });
  }

  markActiveNav();

  // Hook opcional por página
  if (typeof window.afterIncludes === 'function') window.afterIncludes();
})();
</script>
