<script>
const dict = {
  es: {
    hero_title: "TokenLens — Señales multi-exchange con IA",
    cta_download: "Descargar",
    cta_buy: "Comprar licencia",
    features_title: "¿Qué hace TokenVision?",
    footer_rights: "Todos los derechos reservados."
  },
  en: {
    hero_title: "TokenLens — Multi-exchange AI signals",
    cta_download: "Download",
    cta_buy: "Buy license",
    features_title: "What does TokenLens do?",
    footer_rights: "All rights reserved."
  }
};

function setLang(l) {
  const lang = dict[l] ? l : "es";
  document.documentElement.lang = lang;
  document.querySelectorAll("[data-i18n]").forEach(el => {
    const key = el.getAttribute("data-i18n");
    if (dict[lang][key]) el.textContent = dict[lang][key];
  });
  localStorage.setItem("lang", lang);
}

document.addEventListener("DOMContentLoaded", () => {
  const saved = localStorage.getItem("lang") || (navigator.language || "es").slice(0,2);
  setLang(saved);
  document.getElementById("lang-select").addEventListener("change", (e)=> setLang(e.target.value));
});
</script>
