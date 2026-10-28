# Partage + référencement : aperçus de liens (Open Graph), icônes, une page par produit,
# sitemap, robots, données structurées. Appelé par build.py après la génération d'index.html.
import os, json, html, re
from PIL import Image

SITE = 'https://nervina.ma'
SCR = '/tmp/claude-0/-home-claude/ff2ae7a3-8d31-5e47-be59-c1e595b976e6/scratchpad'
LOGO = SCR + '/zip/Nervina-projet/logos/logo-fonce.png'
BEIGE = (243, 240, 230)


def esc(s):
    return html.escape(str(s or ''), quote=True)


def icons(repo):
    os.makedirs(repo + '/icons', exist_ok=True)
    lg = Image.open(LOGO).convert('RGBA')
    # garder l'arche (partie haute du logo), sans le texte
    a = lg.getchannel('A').point(lambda v: 255 if v > 30 else 0)
    w, h = lg.size
    arch = lg.crop((0, 0, w, int(h * 0.62)))
    arch = arch.crop(arch.getchannel('A').point(lambda v: 255 if v > 30 else 0).getbbox())
    for size, name, pad in [(512, 'icon-512.png', .16), (192, 'icon-192.png', .16), (180, 'apple-touch-icon.png', .16), (48, 'favicon-48.png', .08), (32, 'favicon-32.png', .06)]:
        c = Image.new('RGBA', (size, size), BEIGE + (255,))
        inner = int(size * (1 - 2 * pad))
        t = arch.copy(); t.thumbnail((inner, inner), Image.LANCZOS)
        c.alpha_composite(t, ((size - t.width) // 2, (size - t.height) // 2))
        c.convert('RGB').save(f'{repo}/icons/{name}', optimize=True)
    Image.open(f'{repo}/icons/favicon-48.png').save(f'{repo}/favicon.ico', sizes=[(16, 16), (32, 32), (48, 48)])


def og_home(repo):
    os.makedirs(repo + '/images/og', exist_ok=True)
    b = Image.open(repo + '/images/home/banniere-6-ordinateur.webp').convert('RGB')
    c = Image.new('RGB', (1200, 630), BEIGE)
    t = b.copy(); t.thumbnail((1200, 630), Image.LANCZOS)
    c.paste(t, ((1200 - t.width) // 2, (630 - t.height) // 2))
    c.save(repo + '/images/og/nervina.jpg', quality=86, optimize=True, progressive=True)


def og_product(repo, p):
    src = os.path.join(repo, p['imgs'][0]) if p.get('imgs') else None
    if not src or not os.path.exists(src):
        return '/images/og/nervina.jpg'
    im = Image.open(src).convert('RGB')
    s = min(im.size); l, t = (im.width - s) // 2, (im.height - s) // 2
    im = im.crop((l, t, l + s, t + s)).resize((900, 900), Image.LANCZOS)
    out = f'/images/og/{p["id"]}.jpg'
    im.save(repo + out, quality=84, optimize=True, progressive=True)
    return out


def head_tags(title, desc, url, image, img_w, img_h, kind='website', extra=''):
    return f'''<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{kind}">
<meta property="og:site_name" content="Nervina Maroc">
<meta property="og:locale" content="fr_MA">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}{image}">
<meta property="og:image:width" content="{img_w}">
<meta property="og:image:height" content="{img_h}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#F3F0E6">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" href="/icons/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="/icons/apple-touch-icon.png">
<link rel="manifest" href="/manifest.webmanifest">
{extra}'''


def jsonld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False).replace('</', '<\\/') + '</script>'


def strip_head(g):
    g = re.sub(r'<meta name="description"[^>]*>\n?', '', g, count=1)
    g = re.sub(r'<title>[^<]*</title>\n?', '', g, count=1)
    return g


def run(repo, g, s):
    icons(repo); og_home(repo)
    st = s['settings']
    store = {
        '@context': 'https://schema.org', '@type': 'FurnitureStore', 'name': 'Nervina Maroc', 'url': SITE + '/',
        'logo': SITE + '/icons/icon-512.png', 'image': SITE + '/images/og/nervina.jpg',
        'description': 'Mobilier fait main et sur mesure au Maroc : tables, meubles TV, consoles et tables de chevet. Livraison partout au Maroc.',
        'telephone': '+212' + re.sub(r'\D', '', st.get('whatsapp', ''))[1:], 'email': st.get('email', ''),
        'address': {'@type': 'PostalAddress', 'addressLocality': 'Casablanca', 'addressCountry': 'MA'},
        'areaServed': 'MA', 'priceRange': 'MAD', 'currenciesAccepted': 'MAD',
        'sameAs': [f"https://www.instagram.com/{st.get('instagram','').lstrip('@')}/"] if st.get('instagram') else [],
    }
    vis = [p for p in s['products'] if not p.get('hidden')]
    title = 'Nervina Maroc · Mobilier fait main et sur mesure'
    desc = 'Tables basses, meubles TV, consoles et tables de chevet fabriqués au Maroc, à vos dimensions. Livraison partout au Maroc, commande simple sur WhatsApp.'
    base = strip_head(g)
    index = base.replace('<meta name="viewport" content="width=device-width, initial-scale=1">',
                         '<meta name="viewport" content="width=device-width, initial-scale=1">\n' + head_tags(title, desc, SITE + '/', '/images/og/nervina.jpg', 1200, 630, extra=jsonld(store)), 1)
    open(repo + '/index.html', 'w', encoding='utf-8').write(index)
    # page 404 : la boutique elle-même (adresse inconnue -> accueil), non indexée
    open(repo + '/404.html', 'w', encoding='utf-8').write(index.replace('<link rel="canonical"', '<meta name="robots" content="noindex">\n<base href="/">\n<link rel="canonical"', 1))
    # une page par produit : même boutique, ouverte directement sur la fiche, avec son propre aperçu
    urls = [SITE + '/']
    for p in vis:
        img = og_product(repo, p)
        col = next((c['name'] for c in s['collections'] if c['id'] == p['col']), '')
        pt = f"{p['title']} · Nervina Maroc"
        pd = (p.get('desc') or st.get('productDesc', ''))[:155]
        pd = f"{pd} {format(p['price'], ',').replace(',', ' ')} dh, sur mesure, livraison partout au Maroc."[:200]
        url = f"{SITE}/p/{p['id']}/"
        prod = {
            '@context': 'https://schema.org', '@type': 'Product', 'name': p['title'], 'description': p.get('desc') or st.get('productDesc', ''),
            'image': [SITE + '/' + x for x in p.get('imgs', [])[:4]], 'sku': p['id'], 'category': col,
            'brand': {'@type': 'Brand', 'name': 'Nervina Maroc'},
            'offers': {'@type': 'Offer', 'url': url, 'priceCurrency': 'MAD', 'price': p['price'], 'availability': 'https://schema.org/InStock',
                       'itemCondition': 'https://schema.org/NewCondition', 'seller': {'@type': 'Organization', 'name': 'Nervina Maroc'}},
        }
        start = f'<base href="/">\n<script>window.NV_START="p-{p["id"]}"</script>\n'
        page = base.replace('<meta name="viewport" content="width=device-width, initial-scale=1">',
                            '<meta name="viewport" content="width=device-width, initial-scale=1">\n' + start + head_tags(pt, pd, url, img, 900, 900, kind='product', extra=jsonld(prod)), 1)
        os.makedirs(f"{repo}/p/{p['id']}", exist_ok=True)
        open(f"{repo}/p/{p['id']}/index.html", 'w', encoding='utf-8').write(page)
        urls.append(url)
    # nettoyer les pages de produits supprimés ou masqués
    keep = {p['id'] for p in vis}
    if os.path.isdir(repo + '/p'):
        import shutil
        for d in os.listdir(repo + '/p'):
            if d not in keep: shutil.rmtree(f'{repo}/p/{d}')
    for c in s['collections']:
        pass
    open(repo + '/sitemap.xml', 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        ''.join(f'  <url><loc>{u}</loc></url>\n' for u in urls) + '</urlset>\n')
    open(repo + '/robots.txt', 'w').write(f'User-agent: *\nAllow: /\nDisallow: /carre.html\nDisallow: /source/\n\nSitemap: {SITE}/sitemap.xml\n')
    json.dump({'name': 'Nervina Maroc', 'short_name': 'Nervina', 'start_url': '/', 'display': 'standalone', 'background_color': '#F3F0E6',
               'theme_color': '#F3F0E6', 'lang': 'fr', 'icons': [{'src': '/icons/icon-192.png', 'sizes': '192x192', 'type': 'image/png'},
                                                                   {'src': '/icons/icon-512.png', 'sizes': '512x512', 'type': 'image/png'}]},
              open(repo + '/manifest.webmanifest', 'w'), ensure_ascii=False, indent=1)
    return len(vis)


def noindex(path):
    g = open(path, encoding='utf-8').read()
    if 'name="robots"' not in g:
        g = g.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n<meta name="robots" content="noindex">', 1)
        open(path, 'w', encoding='utf-8').write(g)
