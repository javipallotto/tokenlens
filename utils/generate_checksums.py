# utils/generate_checksums.py
import hashlib, json, sys, pathlib


ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'manifest.json'


# Editá estas rutas a tus binarios construidos
BINARIES = {
'Windows': ROOT / 'dist' / 'TokenLens-1.0.0-Setup.exe',
'macOS': ROOT / 'dist' / 'TokenLens-1.0.0.dmg',
}


def sha256(path: pathlib.Path) -> str:
h = hashlib.sha256()
with open(path, 'rb') as f:
for chunk in iter(lambda: f.read(1<<20), b''):
h.update(chunk)
return h.hexdigest()


def main():
m = json.loads(MANIFEST.read_text('utf-8'))
for item in m['trial']:
p = BINARIES.get(item['os'])
if not p or not p.exists():
print(f"No encontrado: {item['os']} -> {p}")
continue
item['sha256'] = sha256(p)
print(f"{item['os']}: {item['sha256']}")
MANIFEST.write_text(json.dumps(m, indent=2), encoding='utf-8')
print('manifest.json actualizado')


if __name__ == '__main__':
sys.exit(main())