# i18n/i18n.py
import json, os
from pathlib import Path
from PySide6.QtCore import QObject, Signal

APP_DIR = Path(__file__).resolve().parents[1] if (Path(__file__).parent.name == "i18n") else Path(__file__).resolve().parent
I18N_DIR = APP_DIR / "i18n"

class _I18N(QObject):
    changed = Signal()

    def __init__(self):
        super().__init__()
        self.lang = os.getenv("TV_LANG", "es")
        self._dict = {}
        self._fallback = {}
        self._load_fallback()
        self.set_language(self.lang)

    def _load_fallback(self):
        try:
            self._fallback = json.loads((I18N_DIR / "es.json").read_text(encoding="utf-8"))
        except Exception:
            self._fallback = {}

    def set_language(self, lang: str):
        lang = (lang or "es").strip()
        self.lang = lang
        try:
            p = I18N_DIR / f"{lang}.json"
            self._dict = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
        except Exception:
            self._dict = {}
        self.changed.emit()

    def t(self, key: str, default: str | None = None, **fmt):
        # lookup: selected -> fallback -> default -> key
        val = self._dict
        for part in key.split("."):
            val = val.get(part) if isinstance(val, dict) else None
            if val is None: break
        if val is None:
            val = self._fallback
            for part in key.split("."):
                val = val.get(part) if isinstance(val, dict) else None
                if val is None: break
        if val is None:
            val = default if default is not None else key
        if fmt:
            try:
                val = val.format(**fmt)
            except Exception:
                pass
        return val

I18N = _I18N()
tr = I18N.t
