import csv,json,os,re,urllib.parse,sys,importlib.util
_sp=importlib.util.spec_from_file_location('banner',os.path.join(os.path.dirname(os.path.abspath(__file__)),'banner.py'));banner=importlib.util.module_from_spec(_sp);_sp.loader.exec_module(banner)
from PIL import Image, ImageOps
SCR='/tmp/claude-0/-home-claude/ff2ae7a3-8d31-5e47-be59-c1e595b976e6/scratchpad'
SRC='/mnt/user-data/uploads/jgus0t-ph-files-2026-10-21-102141'
REPO='/home/claude/nervina-maroccc'
BT=SCR+'/zip/Nervina-projet/boutique'
s=json.load(open(BT+'/store.json'))
rows=list(csv.DictReader(open('/root/.claude/uploads/ff2ae7a3-8d31-5e47-be59-c1e595b976e6/883f1328-products_export_1.csv',encoding='utf-8')))
csvimgs={}
for r in rows:
    if r['Image Src']: csvimgs.setdefault(r['Handle'],[]).append((int(r['Image Position']),r['Image Src']))
# 1. Arrondis: take full Shopify photo list
P={p['id']:p for p in s['products']}
P['meuble-tv-arrondis']['imgs']=[u for _,u in sorted(csvimgs['meuble-tv-arrondis'])]
# 2. Duo Curve
if 'table-de-chevet-duo-curve' not in P:
    s['products'].append({"id":"table-de-chevet-duo-curve","title":"Table de Chevet Duo Curve","price":3500,"old":0,"col":"chambres",
      "desc":"Table de chevet aux bords arrondis, deux tiroirs, finition vert sauge et effet noyer. Fabriquée sur mesure, livrée montée. Couleur au choix.",
      "imgs":[u for _,u in sorted(csvimgs['table-de-chevet-duo-curve'])],"hidden":False,"star":False})
# 3. local images
os.makedirs(REPO+'/images',exist_ok=True)
fallback={}
done={}
for p in s['products']:
    new=[]
    for i,u in enumerate(p['imgs'],1):
        if not u.startswith('http'): new.append(u);continue
        if u in done: new.append(done[u]);continue
        fn=urllib.parse.unquote(u.split('?')[0].rsplit('/',1)[1])
        out=f"images/{p['id']}-{i}.webp"
        im=Image.open(os.path.join(SRC,fn)); im=ImageOps.exif_transpose(im)
        im=im.convert('RGBA') if im.mode in('RGBA','LA','P') else im.convert('RGB')
        im.thumbnail((1600,1600),Image.LANCZOS)
        im.save(REPO+'/'+out,'WEBP',quality=82,method=6)
        done[u]=out; fallback[out]=u; new.append(out)
    p['imgs']=new
s['shopify']=fallback
os.makedirs(REPO+'/images/sm',exist_ok=True)
for out in done.values():
    im=Image.open(REPO+'/'+out); im.thumbnail((640,640),Image.LANCZOS)
    im.save(REPO+'/'+out.replace('images/','images/sm/'),'WEBP',quality=80,method=6)
json.dump(s,open(REPO+'/store.json','w'),ensure_ascii=False,indent=1)
# 4. rebuild page; add a safety net: if a local photo is missing, show the Shopify copy
m=open(BT+'/modele.html').read()
FB="const IMGURL=id=>'/_blob/'+id;"
assert FB in m
m=m.replace(FB,FB+"\nconst IMGSM=id=>/^images\\//.test(id)?id.replace('images/','images/sm/'):IMGURL(id);\ndocument.addEventListener('error',e=>{const t=e.target;if(!t||t.tagName!=='IMG')return;const s=t.getAttribute('src')||'';if(s.includes('images/sm/')){t.src=s.replace('images/sm/','images/');return}if(!t.dataset.fb){const u=(S.shopify||{})[s];if(u){t.dataset.fb=1;t.src=u}}},true);")
for a,b in [('<img src="${IMGURL(im)}" alt="${esc(p.title)}" loading="lazy">','<img src="${IMGSM(im)}" alt="${esc(p.title)}" loading="lazy" decoding="async">'),
            ('<button data-gi="${i}" aria-label="Photo ${i+1}" aria-current="${i===0}"><img src="${IMGURL(m)}" alt=""></button>','<button data-gi="${i}" aria-label="Photo ${i+1}" aria-current="${i===0}"><img src="${IMGSM(m)}" alt="" loading="lazy" decoding="async"></button>'),
            ('const th=p=>`<div class="th">${p.imgs&&p.imgs[0]?`<img src="${IMGURL(p.imgs[0])}" alt="">`','const th=p=>`<div class="th">${p.imgs&&p.imgs[0]?`<img src="${IMGSM(p.imgs[0])}" alt="">`')]:
    assert a in m,a; m=m.replace(a,b)
m=m.replace('src="${IMGURL(cp','src="${IMGSM(cp')
assert m.count('IMGSM(')>=4, m.count('IMGSM(')
open(SCR+'/modele.html','w').write(m)
c=open(BT+'/styles.css').read()+'''
/* UI/UX Pro Max : cibles tactiles de 44 px sur mobile et écrans tactiles */
@media (pointer:coarse),(max-width:700px){
  .ib{height:44px;min-width:44px}
  .chip,.pc .add,.sf input,.sf select,input,select{min-height:44px}
  .qty button,.li .qty button{height:44px;width:44px}
  .rm{min-height:44px;padding:0 6px}
  .chips{gap:8px}
}
.li .price{display:block}.li .qty{display:flex;width:max-content;margin-top:8px}
/* la notification ne doit pas masquer le bouton de commande */
@media (max-width:700px){.toast{bottom:auto;top:calc(76px + env(safe-area-inset-top,0px))}}
'''
banner.make_assets(REPO)
m,c,s=banner.patch(m,c,s)
open(SCR+'/styles.css','w').write(c)
open(SCR+'/modele.html','w').write(m)
g=m.replace('@@CSS@@',c).replace('@@SEED@@',json.dumps(s,ensure_ascii=False).replace('</','<\\/')).replace(FB,"const IMGURL=id=>/[./]/.test(id)?id:'/_blob/'+id;")
HEAD='<!doctype html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<meta name="description" content="Nervina Maroc : tables, meubles TV, consoles et tables de chevet sur mesure. Livraison partout au Maroc, commande par WhatsApp.">\n'
g=HEAD+g.replace('<meta name="claude:viewport-fit-sides" content="cover">\n','',1)
open(REPO+'/index.html','w',encoding='utf-8').write(g)
print(len(s['products']),len(done),sum(os.path.getsize(REPO+'/'+x) for x in done.values())//1024,'KB')
