# Publication automatique de la boutique Nervina.
# Lancé par GitHub Actions à chaque modification de store.json (depuis la page /admin/) :
# remet les produits dans le site, régénère les pages produit / collection / info, le sitemap
# et les aperçus de partage. Les photos sont déjà converties en WebP par l'admin.
import json, os, re, importlib.util

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sp = importlib.util.spec_from_file_location('seo', os.path.join(R, 'tools', 'seo.py'))
seo = importlib.util.module_from_spec(sp); sp.loader.exec_module(seo)

s = json.load(open(os.path.join(R, 'store.json'), encoding='utf-8'))
# garde-fous : jamais de produit sans identifiant, prix toujours entier
for p in s['products']:
    p['price'] = int(float(p.get('price') or 0))
    p['old'] = int(float(p.get('old') or 0))
    p.setdefault('hidden', False)
    p.setdefault('imgs', [])
json.dump(s, open(os.path.join(R, 'store.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

SEED = re.compile(r'(<script type="application/json" id="seed">)(.*?)(</script>)', re.S)
payload = json.dumps(s, ensure_ascii=False).replace('</', '<\\/')


def with_seed(path):
    g = open(path, encoding='utf-8').read()
    g2, n = SEED.subn(lambda m: m.group(1) + payload + m.group(3), g, count=1)
    assert n == 1, 'balise seed introuvable dans ' + path
    return g2


g = with_seed(os.path.join(R, 'tools', 'base.html'))
print('pages:', seo.run(R, g, s, assets=False))
bc = os.path.join(R, 'tools', 'base-carre.html')
if os.path.exists(bc):
    open(os.path.join(R, 'carre.html'), 'w', encoding='utf-8').write(with_seed(bc))
    seo.noindex(os.path.join(R, 'carre.html'))
print('produits visibles:', sum(1 for p in s['products'] if not p.get('hidden')))
