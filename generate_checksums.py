#!/usr/bin/env python3
if lower.endswith(".appimage") or lower.endswith(".deb") or lower.endswith(".tar.gz") or lower.endswith(".tar.xz"):
return "linux"
return None


def guess_arch(filename: str) -> str:
lower = filename.lower()
for arch, hints in ARCH_HINTS.items():
if any(h in lower for h in hints):
return arch
# default
return "x64"




def sha256_of(path: Path) -> str:
h = hashlib.sha256()
with open(path, 'rb') as f:
for chunk in iter(lambda: f.read(1024 * 1024), b''):
h.update(chunk)
return h.hexdigest()




def main():
ap = argparse.ArgumentParser(description="Genera manifest.json con SHA-256 de instaladores")
ap.add_argument("--dist", default="dist", help="Carpeta con instaladores (default: dist)")
ap.add_argument("--out", default="web/manifest.json", help="Salida manifest.json (default: web/manifest.json)")
ap.add_argument("--version", required=True, help="Versión a publicar (ej: 0.9.0)")
ap.add_argument("--app-name", default="TokenLens", help="Nombre de la app")
ap.add_argument("--cdn-prefix", default="", help="Prefijo absoluto para los URLs (ej: https://cdn.tu-dominio.com)")
args = ap.parse_args()


dist = Path(args.dist)
if not dist.exists():
print(f"[ERR] No existe carpeta: {dist}", file=sys.stderr)
return 2


builds = []
for p in sorted(dist.iterdir()):
if not p.is_file():
continue
plat = guess_platform(p.name)
if not plat:
continue
arch = guess_arch(p.name)
sha = sha256_of(p)
size = p.stat().st_size
url = f"{args.cdn_prefix.rstrip('/')}/{p.name}" if args.cdn_prefix else p.name
builds.append({
"platform": plat,
"arch": arch,
"filename": p.name,
"url": url,
"sha256": sha,
"size_bytes": size,
})


if not builds:
print("[ERR] No se detectaron instaladores válidos en la carpeta dist/", file=sys.stderr)
return 3


manifest = {
"app_name": args.app_name,
"version": args.version,
"released_utc": datetime.now(timezone.utc).isoformat(),
"notes": "",
"min_version_required": args.version,
"builds": builds,
}


out = Path(args.out)
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
print(f"[OK] Escrito manifest: {out} ({len(builds)} builds)")
for b in builds:
print(f" - {b['platform']:7s} {b['arch']:5s} {b['filename']} SHA256={b['sha256'][:12]}… size={b['size_bytes']}")
return 0


if __name__ == "__main__":
raise SystemExit(main())