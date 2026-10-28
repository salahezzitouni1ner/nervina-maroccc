# Vignettes produit uniformes : chaque produit détouré (ISNet) sur le même fond beige, centré,
# même taille, ombre douce. La vignette devient la 1re photo ; les photos en situation suivent.
import os, json, urllib.parse
import numpy as np
from PIL import Image, ImageFilter
import importlib.util

SCR = '/tmp/claude-0/-home-claude/ff2ae7a3-8d31-5e47-be59-c1e595b976e6/scratchpad'
ORIG = '/mnt/user-data/uploads/jgus0t-ph-files-2026-10-21-102141/'
CACHE = SCR + '/cards_cache'
BG = (236, 230, 217)
_sp = importlib.util.spec_from_file_location('isnet', SCR + '/tools/isnet.py'); isnet = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(isnet)

# photo source (index dans p['imgs'], 0 = première) ; None = choix automatique (photo studio sinon la 1re)
SOURCE = {
    'table-de-chevet-canne': 5, 'table-de-chevet-cloud-noyer': 1, 'table-a-manger-ronde-travertin-4-chaises': 1,
    'table-de-chevet-mdf-arrondie': 5, 'console-arche-miroirs-organiques': 2, 'table-basse-ronde-marbre-bois': 4,
    'table-de-chevet-arrondie-luxe': 2, 'meuble-tv-arrondis': 6,
    'table-de-chevet-design-noyer-blanc-laiton': 2, 'meuble-tv-suspendu-design': 2, 'table-basse-ovale-noire-mdf': 0,
}
# recadrage préalable de la photo source (fraction l,t,r,b) quand elle contient du texte ou d'autres éléments
PRECROP = {'meuble-tv-arrondis': (0.02, 0.30, 0.99, 0.66),
           'table-de-chevet-design-noyer-blanc-laiton': (0.27, 0.15, 0.97, 0.88),
           'meuble-tv-suspendu-design': (0.04, 0.22, 0.99, 0.86),
           'table-basse-ovale-noire-mdf': (0.0, 0.565, 1.0, 0.97)}


def studio_score(path):
    a = np.asarray(Image.open(path).convert('RGB').resize((200, 200))).astype(float)
    b = np.concatenate([a[:6].reshape(-1, 3), a[-6:].reshape(-1, 3), a[:, :6].reshape(-1, 3), a[:, -6:].reshape(-1, 3)])
    return ((b.mean(1) > 200) & ((b.max(1) - b.min(1)) < 25)).mean()


def cutout(src_path, pid):
    os.makedirs(CACHE, exist_ok=True)
    cp = f'{CACHE}/{pid}.png'
    if os.path.exists(cp) and os.path.getmtime(cp) > os.path.getmtime(__file__) - 1e9 and os.path.getsize(cp) > 0:
        return Image.open(cp)
    im = Image.open(src_path).convert('RGB')
    if pid in PRECROP:
        l, t, r, b = PRECROP[pid]; W, H = im.size
        im = im.crop((int(l * W), int(t * H), int(r * W), int(b * H)))
    m = isnet.mask(im)
    a = np.asarray(m).astype(float)
    a = np.clip((a - 25) / (235 - 25), 0, 1) * 255          # nettoyer les bords flous
    m = Image.fromarray(a.astype('uint8')).filter(ImageFilter.GaussianBlur(0.6))
    o = im.convert('RGBA'); o.putalpha(m)
    bb = m.point(lambda v: 255 if v > 40 else 0).getbbox()
    o = o.crop(bb)
    o.save(cp)
    return o


def compose(cut, size=1000):
    c = Image.new('RGB', (size, size), BG)
    maxw, maxh = int(size * .80), int(size * .66)
    r = min(maxw / cut.width, maxh / cut.height)
    t = cut.resize((max(1, int(cut.width * r)), max(1, int(cut.height * r))), Image.LANCZOS)
    x = (size - t.width) // 2
    base = int(size * .80)                                   # même ligne de sol pour tous
    y = base - t.height
    # ombre au sol
    sh = Image.new('L', (size, size), 0)
    sw, shh = int(t.width * .9), int(size * .045)
    ell = Image.new('L', (sw, shh), 0)
    from PIL import ImageDraw
    ImageDraw.Draw(ell).ellipse((0, 0, sw - 1, shh - 1), fill=90)
    sh.paste(ell, ((size - sw) // 2, base - shh // 2))
    sh = sh.filter(ImageFilter.GaussianBlur(size * .018))
    dark = Image.new('RGB', (size, size), (90, 70, 50))
    c = Image.composite(dark, c, sh)
    c.paste(t, (x, y), t)
    return c


def run(repo, s):
    os.makedirs(repo + '/images/card', exist_ok=True); os.makedirs(repo + '/images/sm/card', exist_ok=True)
    fb = s.get('shopify', {})
    for p in s['products']:
        imgs = [x for x in p['imgs'] if not x.startswith('images/card/')]
        if not imgs: continue
        idx = SOURCE.get(p['id'])
        if idx is None:
            scores = [studio_score(repo + '/' + x) for x in imgs]
            idx = next((i for i, sc in enumerate(scores) if sc >= .95), 0)
        idx = min(idx, len(imgs) - 1)
        local = imgs[idx]
        u = fb.get(local)
        src = ORIG + urllib.parse.unquote(u.split('?')[0].rsplit('/', 1)[1]) if u else repo + '/' + local
        if not os.path.exists(src): src = repo + '/' + local
        card = compose(cutout(src, p['id']))
        out = f"images/card/{p['id']}.webp"
        card.save(repo + '/' + out, 'WEBP', quality=86, method=6)
        sm = card.resize((640, 640), Image.LANCZOS); sm.save(repo + '/images/sm/card/' + p['id'] + '.webp', 'WEBP', quality=84, method=6)
        # ordre : vignette, puis photos en situation, puis photos studio
        rest = sorted(imgs, key=lambda x: studio_score(repo + '/' + x) >= .95)
        p['imgs'] = [out] + rest
    return s
