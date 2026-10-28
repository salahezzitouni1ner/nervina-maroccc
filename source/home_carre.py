# Variante « photos carrées » de l'accueil : mêmes sections que home_pro, mais toutes les photos
# au format carré (1:1), montrées en entier. Mobile d'abord.
import importlib.util, os, json
_sp = importlib.util.spec_from_file_location('home_pro', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'home_pro.py'))
hp = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(hp)

hp.ASSETS = [
    ('sq-promo-signature', 'meuble-tv-arrondis-1', (0, 362, 1086, 1448), 1086),
    ('sq-banner', 'set-2-tables-basses-organiques-3', (208, 0, 1040, 832), 1100),
] + [a for a in hp.ASSETS if a[0].startswith('ig-')]


A = hp.ACCUEIL
for a, b in [
    ('images/home/promo-signature.webp', 'images/home/sq-promo-signature.webp'),
    ('<section class="big bleed"><img class="big-img" src="images/home/banner-sur-mesure.webp"',
     '<section class="big bleed"><img class="big-img" src="images/home/sq-banner.webp"'),
]:
    assert a in A, a; A = A.replace(a, b)
hp.ACCUEIL = A
H = hp.HELPERS
a = "const big=document.querySelector('.big-img');if(big)"
assert a in H; hp.HELPERS = H.replace(a, "const big=null;if(big)")

hp.CSS += r'''
/* ================= VARIANTE PHOTOS CARRÉES ================= */
.hs{background:#111213}
.hs-slide::after{display:none}
.hs-slide picture{position:absolute;top:0;bottom:0;right:max(0px,calc((100vw - 1200px)/2));aspect-ratio:1/1;height:100%;overflow:hidden;display:block}
.hs-slide picture .hs-img{object-position:50% 50%}
.hs-cap .hs-in>*{max-width:min(500px,calc(100vw - 100vh - 140px))}
.hs-t{font-size:clamp(2.1rem,3.6vw,3.4rem)}
.hs-ui .hs-dots{max-width:min(500px,calc(100vw - 100vh - 140px))}
.cat{aspect-ratio:1/1}
.promo-img{aspect-ratio:1/1}
.promo-in{grid-template-columns:1fr 1fr}
.big{display:grid;grid-template-columns:1fr 1fr;align-items:stretch;min-height:0;padding:0}
.big::after{display:none}
.big-img{position:relative;top:auto;left:auto;right:auto;height:auto;width:100%;aspect-ratio:1/1;grid-column:2;grid-row:1;object-fit:cover}
.big-in{grid-column:1;grid-row:1;align-self:center;padding:clamp(32px,5vw,72px) clamp(24px,4vw,64px) clamp(32px,5vw,72px) max(20px,calc((100vw - 1200px)/2))}
.big-in>*{max-width:520px}
@media(max-width:1000px) and (min-width:761px){.hs-slide picture{height:auto;width:50%;top:50%;translate:0 -50%}.hs-cap .hs-in>*{max-width:44vw}}
@media(max-width:760px){
  /* téléphone : photo carrée pleine largeur, texte en dessous */
  .hs{height:calc(100vw + 300px);min-height:0;max-height:none}
  .mban+.hs{height:calc(100vw + 300px)!important}
  .hs-slide picture{left:0;right:0;top:0;bottom:auto;width:100%;height:auto;aspect-ratio:1/1}
  .hs-cap{top:100vw;padding:18px 0 80px}
  .hs-cap .hs-in>*{max-width:none}
  .hs-cap .hs-in{padding-inline:20px}
  .hs-t{font-size:clamp(1.85rem,8.4vw,2.4rem)}
  .hs-ui .hs-dots{max-width:none}
  .hs-d{-webkit-line-clamp:2}
  .promo-in{grid-template-columns:1fr}
  .big{grid-template-columns:1fr}
  .big-img{grid-column:1;grid-row:1}
  .big-in{grid-row:2;padding:28px 20px 40px}
  .big .big-b1{width:100%}
}
'''

ASSETS, HOME, ICONS, ACCUEIL, CARD, HELPERS, CSS, TB = hp.ASSETS, hp.HOME, hp.ICONS, hp.ACCUEIL, hp.CARD, hp.HELPERS, hp.CSS, hp.TB
make_assets, patch = hp.make_assets, hp.patch
