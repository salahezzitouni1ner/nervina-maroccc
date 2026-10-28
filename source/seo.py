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
<meta name="google-site-verification" content="C2QKTSXRmBoDAZWHZOLYi5kOMKuZIIbIhbf2dBbYhuw">
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


COLS = {
    'tables': ('Tables basses et tables à manger sur mesure au Maroc',
               'Tables basses en noyer, marbre et travertin, tables à manger rondes avec chaises : fabriquées à la main au Maroc, à vos dimensions. Livraison partout au Maroc.',
               'Nos tables basses et tables à manger sont fabriquées à la main dans notre atelier au Maroc : plateaux en noyer, marbre ou travertin, formes rondes, ovales ou organiques. Chaque table peut être adaptée à vos dimensions et à votre teinte.'),
    'tv': ('Meubles TV sur mesure en noyer au Maroc',
           'Meubles TV suspendus ou sur pieds, finition noyer, éclairage LED intégré, dimensions sur mesure. Fabriqués au Maroc, livrés dans tout le Maroc.',
           'Meubles TV suspendus ou sur pieds, en noyer ou en finition bicolore, avec ou sans éclairage LED. Longueur, hauteur et couleur sont adaptées à votre salon et à la taille de votre écran.'),
    'entree': ("Console d'entrée et miroirs sur mesure au Maroc",
               "Console d'entrée en arche avec miroirs organiques, fabriquée à la main au Maroc. Dimensions et finitions sur mesure, livraison partout au Maroc.",
               "Une entrée soignée commence par une belle console. Nos consoles d'entrée et miroirs aux formes organiques sont fabriqués à la main au Maroc, aux dimensions de votre espace."),
    'chambres': ('Tables de chevet sur mesure en noyer au Maroc',
                 'Tables de chevet arrondies en noyer, laquées ou bicolores, avec tiroirs. Fabriquées à la main au Maroc, couleurs au choix, livraison partout au Maroc.',
                 'Tables de chevet aux lignes douces : noyer, vert sauge, crème ou laque blanche, une ou deux tiroirs. Chaque modèle est fabriqué à la main au Maroc et peut être réalisé dans la couleur de votre choix.'),
}
PAGE_DESC = {
    'faq': 'Commande, paiement en deux fois (30 % / 70 %), délais, livraison partout au Maroc, sur mesure : toutes les réponses sur Nervina Maroc.',
    'a-propos': 'Nervina Maroc fabrique à la main des meubles sur mesure : meubles TV, tables basses, consoles et tables de chevet, livrés partout au Maroc.',
    'livraison': 'Livraison de nos meubles partout au Maroc : délais de 3 à 7 jours pour les produits standard, 7 à 21 jours pour le sur mesure.',
}


def dh(n):
    return format(int(n), ',').replace(',', ' ') + ' dh'


def crumbs(items):
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList',
            'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': u} for i, (n, u) in enumerate(items)]}


def plinks(ps):
    return '<ul>' + ''.join(f'<li><a href="/p/{p["id"]}/">{esc(p["title"])}</a> · {dh(p["price"])}</li>' for p in ps) + '</ul>'


def prerender(page, inner):
    # contenu lisible par Google dans le HTML ; la boutique le remplace dès son démarrage
    a = '<main class="wrap" id="app"></main>'
    assert a in page
    return page.replace(a, '<main class="wrap" id="app"><div class="seo-pre">' + inner + '</div></main>', 1)


def faq_ld(body):
    qs, blocks = [], [b.strip() for b in body.split('\n\n') if b.strip()]
    for b in blocks:
        q, _, a = b.partition('\n')
        if q.strip().endswith('?') and a.strip():
            qs.append({'@type': 'Question', 'name': q.strip(), 'acceptedAnswer': {'@type': 'Answer', 'text': a.strip()}})
    return {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': qs} if qs else None


def run(repo, g, s):
    icons(repo); og_home(repo)
    st = s['settings']
    store = {
        '@context': 'https://schema.org', '@type': 'FurnitureStore', 'name': 'Nervina Maroc', 'url': SITE + '/',
        'logo': SITE + '/icons/icon-512.png', 'image': SITE + '/images/og/nervina.jpg',
        'description': 'Mobilier fait main et sur mesure au Maroc : meubles TV, tables basses, tables à manger, consoles et tables de chevet. Livraison partout au Maroc.',
        'telephone': '+212' + re.sub(r'\D', '', st.get('whatsapp', ''))[1:], 'email': st.get('email', ''),
        'address': {'@type': 'PostalAddress', 'addressLocality': 'Casablanca', 'addressCountry': 'MA'},
        'areaServed': {'@type': 'Country', 'name': 'Maroc'}, 'priceRange': '2 300 – 13 500 MAD', 'currenciesAccepted': 'MAD',
        'paymentAccepted': 'Acompte de 30 % à la commande, solde à la livraison',
        'sameAs': [f"https://www.instagram.com/{st.get('instagram','').lstrip('@')}/"] if st.get('instagram') else [],
    }
    site_ld = {'@context': 'https://schema.org', '@type': 'WebSite', 'name': 'Nervina Maroc', 'url': SITE + '/', 'inLanguage': 'fr-MA'}
    vis = [p for p in s['products'] if not p.get('hidden')]
    if vis:
        prices = sorted(p['price'] for p in vis); store['priceRange'] = f"{dh(prices[0])} – {dh(prices[-1])}".replace(' dh', ' MAD')
    colname = {c['id']: c['name'] for c in s['collections']}
    title = 'Nervina Maroc | Meubles sur mesure : meubles TV, tables basses, chevets'
    desc = 'Meubles faits main au Maroc : meubles TV en noyer, tables basses, tables à manger, consoles et tables de chevet, à vos dimensions. Livraison partout au Maroc, paiement en deux fois.'
    base = strip_head(g)
    VP = '<meta name="viewport" content="width=device-width, initial-scale=1">'

    def write(path, start, head, pre):
        page = base.replace(VP, VP + '\n' + start + head, 1)
        page = prerender(page, pre)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, 'w', encoding='utf-8').write(page)
        return page

    col_links = '<ul>' + ''.join(f'<li><a href="/c/{c["id"]}/">{esc(COLS.get(c["id"], (c["name"],))[0])}</a></li>' for c in s['collections']) + '</ul>'
    home_pre = (f'<h1>Nervina Maroc : meubles sur mesure fabriqués à la main au Maroc</h1>'
                f'<p>{esc(desc)}</p><h2>Nos collections</h2>{col_links}<h2>Nos meubles</h2>{plinks(vis)}'
                f'<p><a href="/faq/">Questions fréquentes</a> · <a href="/a-propos/">À propos de Nervina</a></p>')
    index = write(repo + '/index.html', '', head_tags(title, desc, SITE + '/', '/images/og/nervina.jpg', 1200, 630, extra=jsonld(store) + '\n' + jsonld(site_ld)), home_pre)
    # page 404 : la boutique elle-même (adresse inconnue -> accueil), non indexée
    open(repo + '/404.html', 'w', encoding='utf-8').write(index.replace('<link rel="canonical"', '<meta name="robots" content="noindex">\n<base href="/">\n<link rel="canonical"', 1))
    urls = [(SITE + '/', '/images/og/nervina.jpg')]
    keep = {'p': set(), 'c': set(), 'pg': set()}
    # une page par produit
    for p in vis:
        img = og_product(repo, p)
        col = colname.get(p['col'], '')
        pt = f"{p['title']} sur mesure – {dh(p['price'])} | Nervina Maroc"
        pd = (p.get('desc') or st.get('productDesc', ''))[:150].rstrip()
        pd = f"{pd} {dh(p['price'])}, fait main au Maroc, sur mesure, livraison partout au Maroc."[:200]
        url = f"{SITE}/p/{p['id']}/"
        prod = {
            '@context': 'https://schema.org', '@type': 'Product', 'name': p['title'], 'description': p.get('desc') or st.get('productDesc', ''),
            'image': [SITE + '/' + x for x in p.get('imgs', [])[:4]], 'sku': p['id'], 'category': col,
            'brand': {'@type': 'Brand', 'name': 'Nervina Maroc'},
            'offers': {'@type': 'Offer', 'url': url, 'priceCurrency': 'MAD', 'price': p['price'], 'availability': 'https://schema.org/InStock',
                       'itemCondition': 'https://schema.org/NewCondition', 'seller': {'@type': 'Organization', 'name': 'Nervina Maroc'}},
        }
        bc = crumbs([('Accueil', SITE + '/'), (col, f"{SITE}/c/{p['col']}/"), (p['title'], url)])
        rel = [q for q in vis if q['col'] == p['col'] and q['id'] != p['id']][:8]
        pre = (f'<nav><a href="/">Accueil</a> / <a href="/c/{p["col"]}/">{esc(col)}</a></nav><h1>{esc(p["title"])}</h1>'
               f'<p>{dh(p["price"])}</p><p>{esc(p.get("desc") or st.get("productDesc", ""))}</p>'
               f'<p>Fabriqué à la main au Maroc, dimensions et teinte sur mesure. Livraison partout au Maroc. Paiement en deux fois : 30 % à la commande, 70 % à la livraison.</p>'
               + (f'<h2>Dans la même collection</h2>{plinks(rel)}' if rel else ''))
        write(f"{repo}/p/{p['id']}/index.html", f'<base href="/">\n<script>window.NV_START="p-{p["id"]}"</script>\n',
              head_tags(pt, pd, url, img, 900, 900, kind='product', extra=jsonld(prod) + '\n' + jsonld(bc)), pre)
        urls.append((url, '/' + p['imgs'][0] if p.get('imgs') else None)); keep['p'].add(p['id'])
    # une page par collection
    for c in s['collections']:
        ps = [p for p in vis if p['col'] == c['id']]
        if not ps: continue
        h1, cd, intro = COLS.get(c['id'], (c['name'] + ' sur mesure au Maroc', f"{c['name']} fabriqués à la main au Maroc, sur mesure.", ''))
        url = f"{SITE}/c/{c['id']}/"
        lst = {'@context': 'https://schema.org', '@type': 'ItemList', 'name': h1,
               'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'url': f"{SITE}/p/{p['id']}/", 'name': p['title']} for i, p in enumerate(ps)]}
        bc = crumbs([('Accueil', SITE + '/'), (c['name'], url)])
        img = og_product(repo, ps[0])
        pre = f'<nav><a href="/">Accueil</a> / {esc(c["name"])}</nav><h1>{esc(h1)}</h1><p>{esc(intro)}</p>{plinks(ps)}<h2>Autres collections</h2>{col_links}'
        write(f"{repo}/c/{c['id']}/index.html", f'<base href="/">\n<script>window.NV_START="c-{c["id"]}"</script>\n',
              head_tags(f'{h1} | Nervina Maroc', cd, url, img, 900, 900, extra=jsonld(lst) + '\n' + jsonld(bc)), pre)
        urls.append((url, None)); keep['c'].add(c['id'])
    # pages d'information (FAQ, livraison, à propos…)
    for k, pg in s.get('pages', {}).items():
        url = f"{SITE}/{k}/"
        body = pg.get('body', '')
        pdsc = PAGE_DESC.get(k) or re.sub(r'\s+', ' ', body)[:155]
        extra = ''
        if k == 'faq':
            f = faq_ld(body)
            if f: extra = jsonld(f)
        pre = f'<h1>{esc(pg["title"])}</h1>' + ''.join(f'<p>{esc(b)}</p>' for b in body.split('\n') if b.strip())
        write(f"{repo}/{k}/index.html", f'<base href="/">\n<script>window.NV_START="{k}"</script>\n',
              head_tags(f'{pg["title"]} | Nervina Maroc', pdsc, url, '/images/og/nervina.jpg', 1200, 630, extra=extra), pre)
        urls.append((url, None)); keep['pg'].add(k)
    # nettoyer les pages supprimées ou masquées
    import shutil
    for d, ks in (('p', keep['p']), ('c', keep['c'])):
        if os.path.isdir(f'{repo}/{d}'):
            for x in os.listdir(f'{repo}/{d}'):
                if x not in ks: shutil.rmtree(f'{repo}/{d}/{x}')
    import datetime
    today = datetime.date.today().isoformat()
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
    for u, im in urls:
        sm.append(f'  <url><loc>{u}</loc><lastmod>{today}</lastmod>' + (f'<image:image><image:loc>{SITE}{im}</image:loc></image:image>' if im else '') + '</url>')
    open(repo + '/sitemap.xml', 'w').write('\n'.join(sm + ['</urlset>']) + '\n')
    open(repo + '/robots.txt', 'w').write(f'User-agent: *\nAllow: /\nDisallow: /carre.html\nDisallow: /source/\n\nSitemap: {SITE}/sitemap.xml\n')
    json.dump({'name': 'Nervina Maroc', 'short_name': 'Nervina', 'start_url': '/', 'display': 'standalone', 'background_color': '#F3F0E6',
               'theme_color': '#F3F0E6', 'lang': 'fr', 'icons': [{'src': '/icons/icon-192.png', 'sizes': '192x192', 'type': 'image/png'},
                                                                   {'src': '/icons/icon-512.png', 'sizes': '512x512', 'type': 'image/png'}]},
              open(repo + '/manifest.webmanifest', 'w'), ensure_ascii=False, indent=1)
    return len(urls)


def noindex(path):
    g = open(path, encoding='utf-8').read()
    if 'name="robots"' not in g:
        g = g.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n<meta name="robots" content="noindex">', 1)
        open(path, 'w', encoding='utf-8').write(g)
