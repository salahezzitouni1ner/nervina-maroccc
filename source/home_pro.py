# Page d'accueil « boutique pro » : slider plein écran, bandeau défilant d'annonces, réassurance,
# univers, carrousels produits, bannière promo, bannière sur mesure, étapes, Instagram.
# GSAP + ScrollTrigger (apparitions), Lenis (défilement doux sur ordinateur).
import os, re, shutil, json, urllib.parse
from PIL import Image

VEND = '/tmp/claude-0/-home-claude/ff2ae7a3-8d31-5e47-be59-c1e595b976e6/scratchpad/vend'
ORIG = '/mnt/user-data/uploads/jgus0t-ph-files-2026-10-21-102141/'

# (nom, image produit locale, recadrage (l,t,r,b) ou None, largeur max)
ASSETS = [
    ('promo-duo', 'table-de-chevet-duo-curve-1', None, 1200),
    ('banner-sur-mesure', 'set-2-tables-basses-organiques-3', None, 1600),
    ('cat-tables', 'table-basse-ronde-marbre-bois-4', None, 900),
    ('cat-tv', 'meuble-tv-suspendu-design-3', None, 900),
    ('cat-entree', 'console-arche-miroirs-organiques-1', None, 900),
    ('cat-chambres', 'table-de-chevet-arrondie-luxe-4', None, 900),
    ('ig-1', 'table-de-chevet-canne-5', None, 700),
    ('ig-2', 'table-basse-ovale-noire-mdf-2', None, 700),
    ('ig-3', 'table-a-manger-ronde-travertin-4-chaises-2', None, 700),
    ('ig-4', 'table-de-chevet-duo-curve-1', None, 700),
    ('ig-5', 'table-basse-ovale-design-2', None, 700),
    ('ig-6', 'table-basse-ronde-noyer-metal-noir-2', None, 700),
]

HOME = {
  'slides': [
    {'img': 'images/home/slide-tables.webp', 'imgm': 'images/home/slide-tables-m.webp', 'pos': '50% 65%', 'posm': '50% 75%', 'k': 'Collection Tables', 't': 'Des tables basses sculpturales',
     'd': 'Noyer, marbre, verre et travertin, pour un salon qui a du caractère.', 'cta': 'Voir les tables', 'href': '#c-tables', 'cta2': 'Table Ronde Luxe', 'href2': '#p-table-basse-ronde-luxe', 'alt': 'Table basse ronde en noyer et verre fumé dans un salon, la nuit'},
    {'img': 'images/home/slide-chambres.webp', 'imgm': 'images/home/slide-chambres-m.webp', 'pos': '60% 55%', 'posm': '50% 70%', 'k': 'Collection Chambres', 't': 'Le calme, en noyer',
     'd': 'Tables de chevet aux lignes arrondies, fabriquées à la main au Maroc.', 'cta': 'Voir les chambres', 'href': '#c-chambres', 'alt': 'Table de chevet arrondie sous une arche marocaine'},
    {'img': 'images/home/slide-entree.webp', 'imgm': 'images/home/slide-entree-m.webp', 'pos': '50% 70%', 'posm': '40% 80%', 'k': "Meubles d'entrée", 't': 'Une entrée qui accueille',
     'd': 'Console en arche et miroirs organiques, pour soigner la première impression.', 'cta': 'Découvrir la console', 'href': '#p-console-arche-miroirs-organiques', 'alt': 'Console en arche avec miroirs organiques'},
    {'img': 'images/home/slide-sur-mesure.webp', 'imgm': 'images/home/slide-sur-mesure-m.webp', 'pos': '50% 65%', 'posm': '50% 75%', 'k': 'Fabrication sur mesure', 't': 'Vos dimensions. Votre teinte.',
     'd': 'Chaque pièce est adaptée à votre espace. Devis gratuit sur WhatsApp.', 'cta': 'Demander un devis', 'href': 'WA', 'alt': 'Table à manger ronde en noyer et quatre chaises'},
  ],
  'cats': {'tables': 'images/home/cat-tables.webp', 'tv': 'images/home/cat-tv.webp', 'entree': 'images/home/cat-entree.webp', 'chambres': 'images/home/cat-chambres.webp'},
  'ig': ['images/home/ig-%d.webp' % i for i in range(1, 7)],
}

ICONS = {
  'truck': '<path d="M2 6h12v10H2zM14 9h4.5L22 12.5V16h-8"/><circle cx="6.5" cy="17.5" r="1.8"/><circle cx="17.5" cy="17.5" r="1.8"/>',
  'hand': '<path d="M4 20l7-7M9 11l4 4M13 4l7 7-3 3-7-7z"/>',
  'ruler': '<path d="M3 16.5L16.5 3 21 7.5 7.5 21z"/><path d="M7 12.5l2 2M10 9.5l2 2M13 6.5l2 2"/>',
  'wallet': '<rect x="3" y="6" width="18" height="13" rx="1"/><path d="M3 10h18M15.5 14.5h2.5"/>',
  'chat': '<path d="M4 5h16v11H9l-5 4z"/><path d="M8 10h8"/>',
  'box': '<path d="M3 7l9-4 9 4v10l-9 4-9-4z"/><path d="M3 7l9 4 9-4M12 11v10"/>',
  'arrowl': '<path d="M15 5l-7 7 7 7"/>', 'arrowr': '<path d="M9 5l7 7-7 7"/>',
  'ig': '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/>',
}

ACCUEIL = r'''accueil(){
  const L=vis(),H=__HOME__,ICO2=__ICONS__,ic=(k,c='')=>`<svg class="ic ${c}" viewBox="0 0 24 24" aria-hidden="true">${ICO2[k]}</svg>`;
  const wa=WAU('Bonjour Nervina, je souhaite un devis pour un meuble sur mesure.');
  const sl=H.slides.filter(s=>!s.pid||prod(s.pid));const n=sl.length;
  const href=h=>h==='WA'?wa:h,ext=h=>h==='WA'?' target="_blank" rel="noopener"':'';
  const usp=[['truck','Livraison partout au Maroc','Frais confirmés avant commande'],['hand','Fabrication artisanale','Dans notre atelier au Maroc'],['ruler','Sur mesure','Dimensions et teintes au choix'],['wallet','Paiement en deux fois','30 % à la commande, 70 % à la livraison']];
  const sig=prod('table-de-chevet-duo-curve');
  const NOHOME=['table-basse-amazonica','meuble-tv-arrondis'];const byCol=c=>L.filter(p=>p.col===c&&!NOHOME.includes(p.id));
  const best=['table-de-chevet-duo-curve','table-basse-london','console-arche-miroirs-organiques','table-a-manger-ronde-travertin-4-chaises','table-de-chevet-cloud-noyer','table-basse-ronde-marbre-bois','table-de-chevet-canne'].map(prod).filter(p=>p&&!p.hidden);
  const rail=(id,k,t,list,all)=>list.length?`<section class="sec2"><div class="sh rv"><div><p class="eyebrow">${k}</p><h2>${t}</h2></div><div class="sh-r">${all?`<a class="lnk" href="${all}">Tout voir</a>`:''}<div class="rail-nav"><button class="rn" data-rail="${id}" data-d="-1" aria-label="Précédent">${ic('arrowl')}</button><button class="rn" data-rail="${id}" data-d="1" aria-label="Suivant">${ic('arrowr')}</button></div></div></div><div class="rail" id="${id}">${list.map(card).join('')}</div></section>`:'';
  const ig=String(S.settings.instagram||'').replace(/^@/,'');
  return `<h1 class="sr">Nervina Maroc : une pièce pour chaque pièce, mobilier fait main et sur mesure</h1>
<a class="mban bleed" href="#catalogue" aria-label="Découvrir la collection : meuble TV, tables basses, console d'entrée, table de chevet"><picture><source media="(min-width:761px)" srcset="images/home/banniere-6-ordinateur.webp" width="1920" height="820"><img src="images/home/banniere-6-mobile.webp" width="1080" height="1350" alt="Une pièce pour chaque pièce : meuble TV noyer et crème, table London, console Arche, chevet arrondi, set organique et table ovale en marbre" fetchpriority="high" decoding="async"></picture></a>
<section class="usp bleed" aria-label="Nos engagements"><div class="usp-in">${usp.map(u=>`<div class="usp-i">${ic(u[0])}<div><b>${u[1]}</b><span>${u[2]}</span></div></div>`).join('')}</div></section>
<section class="sec2"><div class="sh rv"><div><p class="eyebrow">Collections</p><h2>Explorez nos univers</h2></div><a class="lnk" href="#catalogue">Tout le catalogue</a></div>
  <div class="cats">${S.collections.map(c=>{const k=byCol(c.id).length;const im=H.cats[c.id]||(byCol(c.id)[0]||{}).imgs?.[0];return `<a class="cat rv" href="#c-${esc(c.id)}">${im?`<img src="${im}" alt="" loading="lazy" decoding="async">`:''}<span class="cat-cap"><b>${esc(c.name)}</b><small>${k} pièce${k>1?'s':''}</small><em>Découvrir ${ic('arrowr','sm')}</em></span></a>`}).join('')}</div></section>
${rail('r-best','Les plus demandées','Nos best-sellers',best,'#catalogue')}
${sig&&!sig.hidden?`<section class="promo bleed rv-wrap"><div class="promo-in">
  <div class="promo-img rv"><img src="images/home/promo-duo.webp" alt="Table de chevet Duo Curve vert sauge et noyer" loading="lazy" decoding="async"><span class="promo-badge">Nouveauté</span></div>
  <div class="promo-txt rv"><p class="eyebrow">Chambres</p><h2>${esc(sig.title)}</h2>
    <p class="promo-d">Deux tiroirs aux formes douces, le vert sauge associé au noyer : une table de chevet apaisante, fabriquée sur mesure.</p>
    <ul class="promo-l"><li>Vert sauge et noyer</li><li>Deux tiroirs</li><li>Livrée montée</li><li>Toutes les couleurs sur demande</li></ul>
    <p class="promo-p">${MAD(sig.price)}</p>
    <div class="promo-cta"><a class="btn" href="#p-${esc(sig.id)}">Découvrir</a><a class="btn ghost" href="${WAU('Bonjour Nervina, je suis intéressé(e) par le '+sig.title+'.')}" target="_blank" rel="noopener">Commander sur WhatsApp</a></div>
  </div></div></section>`:''}
${rail('r-tables','Collection Tables','Tables basses et à manger',byCol('tables'),'#c-tables')}
<section class="big bleed"><img class="big-img" src="images/home/banner-sur-mesure.webp" alt="" loading="lazy" decoding="async">
  <div class="big-in rv"><p class="eyebrow">Fabrication sur mesure</p><h2>Votre meuble, à vos dimensions.</h2>
  <p>Envoyez-nous une photo de votre espace et vos mesures : nous vous proposons un devis gratuit, la teinte et les finitions qui vous ressemblent.</p>
  <div class="big-cta"><a class="btn big-b1" href="${wa}" target="_blank" rel="noopener">${ic('chat')} Devis gratuit sur WhatsApp</a></div></div></section>
${rail('r-ch','Collection Chambres','Pour la chambre',byCol('chambres'),'#c-chambres')}
<section class="sec2 steps-s"><div class="sh rv"><div><p class="eyebrow">Comment commander</p><h2>Simple, depuis chez vous</h2></div></div>
  <ol class="steps">${[['chat','Choisissez','Ajoutez vos pièces au panier ou envoyez-nous votre projet.'],['ruler','Validez sur WhatsApp','Nous confirmons dimensions, teinte, délai et frais de livraison.'],['hand','Fabrication','Après un acompte de 30 %, votre meuble est fabriqué dans notre atelier.'],['box','Livraison','Livraison chez vous partout au Maroc. Vous réglez le solde de 70 %.']].map((s,i)=>`<li class="rv"><span class="st-n">${String(i+1).padStart(2,'0')}</span>${ic(s[0])}<b>${s[1]}</b><p>${s[2]}</p></li>`).join('')}</ol></section>
${ig?`<section class="sec2"><div class="sh rv"><div><p class="eyebrow">@${esc(ig)}</p><h2>Nos pièces chez vous</h2></div><a class="btn ghost" href="https://www.instagram.com/${encodeURIComponent(ig)}/" target="_blank" rel="noopener">${ic('ig')} Suivre sur Instagram</a></div>
  <div class="igg">${H.ig.map(u=>`<a class="igt rv" href="https://www.instagram.com/${encodeURIComponent(ig)}/" target="_blank" rel="noopener" aria-label="Voir sur Instagram"><img src="${u}" alt="" loading="lazy" decoding="async"><span>${ic('ig')}</span></a>`).join('')}</div></section>`:''}`},
'''

CARD = r'''function card(p){const i2=p.imgs&&p.imgs[1];return `<article class="pc"><a class="im" href="#p-${esc(p.id)}" aria-label="${esc(p.title)}">${ph(p)}${i2?`<img class="alt" src="${IMGSM(i2)}" alt="" loading="lazy" decoding="async">`:''}<span class="tag">Sur mesure</span></a><p class="pc-c">${esc(colName(p.col))}</p><h3><a href="#p-${esc(p.id)}">${esc(p.title)}</a></h3>${priceH(p)}<button class="btn ghost add" data-add="${esc(p.id)}">Ajouter au panier</button></article>`}'''

HELPERS = r'''
/* ---------- Lenis + GSAP + accueil pro ---------- */
const RM=matchMedia('(prefers-reduced-motion: reduce)');
let LEN=null;
(function(){
  if(!window.Lenis||RM.matches)return;
  LEN=new Lenis({autoRaf:!window.gsap,anchors:false,lerp:.1,smoothWheel:true});
  if(window.gsap){if(window.ScrollTrigger){gsap.registerPlugin(ScrollTrigger);LEN.on('scroll',ScrollTrigger.update)}gsap.ticker.add(t=>LEN.raf(t*1000));gsap.ticker.lagSmoothing(0)}
})();
const toY=y=>{if(LEN)LEN.scrollTo(y,{immediate:true,force:true});else scrollTo(0,y)};
/* bandeau d'annonces qui défile */
let ANN=null;
function annSet(){
  const el=$('#ann'),st=S.settings;if(!el)return;
  const msgs=[st.banner,...(st.annMsgs||['Paiement : 30 % à la commande, 70 % à la livraison','Fabrication artisanale et sur mesure au Maroc'])].filter(Boolean);
  el.hidden=!msgs.length;if(!msgs.length)return;
  el.innerHTML=`<span class="ann-t">${esc(msgs[0])}</span>`;
  clearInterval(ANN);if(msgs.length<2||RM.matches)return;
  let i=0,hold=false;el.onmouseenter=()=>hold=true;el.onmouseleave=()=>hold=false;
  ANN=setInterval(()=>{if(hold||document.hidden)return;const t=el.querySelector('.ann-t');t.classList.add('out');setTimeout(()=>{i=(i+1)%msgs.length;t.textContent=msgs[i];t.classList.remove('out')},350)},4200);
}
let MG=null;
function mgKill(){document.body.classList.remove('hs-in');if(MG&&MG.io)MG.io.disconnect();if(MG){try{MG.ctx&&MG.ctx.revert()}catch(e){}MG=null}}
document.addEventListener('visibilitychange',()=>{if(MG&&MG.sync)MG.sync()});
function mgInit(){
  const root=$('#hs');
  if(root){const fit=()=>root.style.setProperty('--top',Math.max(0,root.getBoundingClientRect().top+scrollY)+'px');fit();addEventListener('resize',fit)}
  MG={user:RM.matches,hover:false};
  const st=MG;
  /* carrousels produits */
  app.querySelectorAll('[data-rail]').forEach(b=>b.onclick=()=>{const r=$('#'+b.dataset.rail);if(r)r.scrollBy({left:(+b.dataset.d)*r.clientWidth*.9,behavior:RM.matches?'auto':'smooth'})});
  const railUpd=r=>{const nav=app.querySelectorAll(`[data-rail="${r.id}"]`);if(nav.length<2)return;nav[0].disabled=r.scrollLeft<8;nav[1].disabled=r.scrollLeft+r.clientWidth>=r.scrollWidth-8};
  app.querySelectorAll('.rail').forEach(r=>{railUpd(r);r.addEventListener('scroll',()=>railUpd(r),{passive:true})});
  /* slider */
  if(root){
    const slides=[...root.querySelectorAll('.hs-slide')],dots=[...root.querySelectorAll('.hs-dot')],pp=$('#hspp');let cur=0;
    st.sync=()=>{const p=st.user||st.hover||document.hidden;root.classList.toggle('paused',p);if(pp){pp.classList.toggle('is-paused',st.user);pp.setAttribute('aria-label',st.user?'Lancer le diaporama':'Mettre le diaporama en pause')}};
    const go=n=>{if(!slides.length)return;n=(n+slides.length)%slides.length;if(n===cur)return;
      slides.forEach((s,k)=>{const on=k===n;s.classList.toggle('on',on);s.classList.toggle('was',k===cur);if(on){s.removeAttribute('aria-hidden');s.inert=false;const im=s.querySelector('img');im.loading='eager'}else{s.setAttribute('aria-hidden','true');s.inert=true}});
      const nx=slides[(n+1)%slides.length];if(nx)nx.querySelector('img').loading='eager';
      dots.forEach((d,k)=>{d.classList.toggle('done',k<n);d.classList.remove('run');k===n?d.setAttribute('aria-current','true'):d.removeAttribute('aria-current')});
      void root.offsetWidth;if(dots[n])dots[n].classList.add('run');cur=n};
    dots.forEach(d=>{d.onclick=()=>go(+d.dataset.go);d.addEventListener('animationend',e=>{if(e.animationName==='hs-fill'&&d.classList.contains('run'))go(cur+1)})});
    root.querySelectorAll('[data-step]').forEach(b=>b.onclick=()=>go(cur+(+b.dataset.step)));
    if(pp)pp.onclick=()=>{st.user=!st.user;st.sync()};
    root.addEventListener('mouseenter',()=>{st.hover=true;st.sync()});root.addEventListener('mouseleave',()=>{st.hover=false;st.sync()});
    root.addEventListener('focusin',()=>{st.hover=true;st.sync()});root.addEventListener('focusout',e=>{if(!root.contains(e.relatedTarget)){st.hover=false;st.sync()}});
    let x0=null,y0=null;root.addEventListener('touchstart',e=>{x0=e.touches[0].clientX;y0=e.touches[0].clientY},{passive:true});
    root.addEventListener('touchend',e=>{if(x0==null)return;const dx=e.changedTouches[0].clientX-x0,dy=e.changedTouches[0].clientY-y0;x0=null;if(Math.abs(dx)>45&&Math.abs(dx)>Math.abs(dy))go(cur+(dx<0?1:-1))},{passive:true});
    root.addEventListener('keydown',e=>{if(e.key==='ArrowRight'||e.key==='ArrowLeft'){if(e.target.closest('.hs-ui')){e.preventDefault();go(cur+(e.key==='ArrowRight'?1:-1))}}});
    if(dots[0])dots[0].classList.add('run');
    st.sync();
    if('IntersectionObserver' in window){st.io=new IntersectionObserver(es=>document.body.classList.toggle('hs-in',es[0].isIntersecting&&es[0].intersectionRatio>.25),{threshold:[0,.25,.5]});st.io.observe(root)}
  }
  /* apparitions au défilement */
  if(window.gsap&&window.ScrollTrigger&&!RM.matches){
    gsap.registerPlugin(ScrollTrigger);
    st.ctx=gsap.context(()=>{
      gsap.set('.rv',{opacity:0,y:34});
      ScrollTrigger.batch('.rv',{start:'top 90%',once:true,onEnter:els=>gsap.to(els,{opacity:1,y:0,duration:.9,ease:'power3.out',stagger:.09,overwrite:true})});
      gsap.utils.toArray('.rail').forEach(r=>gsap.from(r.children,{opacity:0,x:40,duration:.8,ease:'power3.out',stagger:.07,scrollTrigger:{trigger:r,start:'top 88%',once:true}}));
      const big=document.querySelector('.big-img');if(big)gsap.fromTo(big,{yPercent:-10},{yPercent:10,ease:'none',scrollTrigger:{trigger:'.big',start:'top bottom',end:'bottom top',scrub:true}});
      const pimg=document.querySelector('.promo-img img');if(pimg)gsap.fromTo(pimg,{scale:1.12},{scale:1,ease:'none',scrollTrigger:{trigger:'.promo',start:'top bottom',end:'center center',scrub:true}});
      requestAnimationFrame(()=>ScrollTrigger.refresh());
    });
  }
}
'''

CSS = r'''
/* ================= Accueil pro ================= */
html.lenis{scroll-behavior:auto}
html.lenis,html.lenis body{height:auto}
.lenis:not(.lenis-autoToggle).lenis-stopped{overflow:clip}
.lenis [data-lenis-prevent]{overscroll-behavior:contain}
html,body{overflow-x:clip}
.ann{margin-inline:calc(50% - 50vw)!important}
.bleed{margin-inline:calc(50% - 50vw)}
#waf{transition:opacity .3s,visibility .3s}body.hs-in #waf{opacity:0;visibility:hidden}
.ic{width:22px;height:22px;fill:none;stroke:currentColor;stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round;flex:none}
.ic.sm{width:14px;height:14px}
/* bandeau annonces */
.ann{overflow:hidden;white-space:nowrap;text-overflow:ellipsis}
.ann-t{display:inline-block;transition:opacity .35s,transform .35s}
.ann-t.out{opacity:0;transform:translateY(-8px)}
@media(max-width:520px){.ann{font-size:.7rem;letter-spacing:.04em;padding:8px 12px}}
/* ---- slider ---- */
.hs{position:relative;overflow:hidden;background:#111213;color:#F3F0E6;height:clamp(560px,calc(100svh - 104px),860px)}
.hs-slide{position:absolute;inset:0;opacity:0;transition:opacity 1.1s cubic-bezier(.4,0,.2,1);z-index:0}
.hs-slide.on{opacity:1;z-index:2}.hs-slide.was{z-index:1}
.hs-img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:var(--pos);transform:scale(1.04)}
.hs-slide.on .hs-img{animation:hs-kb 9s ease-out forwards}
@keyframes hs-kb{from{transform:scale(1.12)}to{transform:scale(1.02)}}
.hs-slide::after{content:"";position:absolute;inset:0;z-index:1;background:linear-gradient(90deg,rgba(12,11,10,.78) 0%,rgba(12,11,10,.45) 42%,rgba(12,11,10,.05) 75%),linear-gradient(0deg,rgba(12,11,10,.55),rgba(12,11,10,0) 40%)}
.hs-cap{position:absolute;inset:0;z-index:2;display:flex;align-items:center}
.hs-in{width:100%;max-width:1200px;margin-inline:auto;padding-inline:max(16px,env(safe-area-inset-left,0px))}
.hs-cap .hs-in>*{max-width:600px}
.hs-k{font-size:.76rem;letter-spacing:.24em;text-transform:uppercase;color:#D9B88F;font-weight:500;margin:0 0 14px}
.hs-t{font-size:clamp(2.3rem,5.6vw,4.8rem);font-weight:300;line-height:1.02;letter-spacing:-.03em;margin:0;color:#F3F0E6}
.hs-d{font-size:clamp(.98rem,1.3vw,1.12rem);color:rgba(243,240,230,.86);margin:18px 0 28px;line-height:1.6;max-width:46ch}
.hs-d b{color:#F3F0E6;font-weight:500;white-space:nowrap}
.hs-cta{display:flex;gap:12px;flex-wrap:wrap}
.hs .hs-b1{background:#F3F0E6;color:#111213;min-height:50px;padding-inline:30px}
.hs .hs-b2{background:transparent;color:#F3F0E6;border:1px solid rgba(243,240,230,.6);min-height:50px;padding-inline:26px}
.hs .hs-b2:hover{background:rgba(243,240,230,.1);border-color:#F3F0E6}
.hs :focus-visible{outline-color:#D9B88F}
.hs-slide .hs-k,.hs-slide .hs-t,.hs-slide .hs-d,.hs-slide .hs-cta{opacity:0;transform:translateY(26px)}
.hs-slide.on .hs-k{animation:hs-up .8s .25s cubic-bezier(.2,.7,.2,1) forwards}
.hs-slide.on .hs-t{animation:hs-up .9s .38s cubic-bezier(.2,.7,.2,1) forwards}
.hs-slide.on .hs-d{animation:hs-up .9s .52s cubic-bezier(.2,.7,.2,1) forwards}
.hs-slide.on .hs-cta{animation:hs-up .9s .64s cubic-bezier(.2,.7,.2,1) forwards}
@keyframes hs-up{to{opacity:1;transform:none}}
.hs-ui{position:absolute;left:0;right:0;bottom:0;z-index:3;padding-bottom:26px}
.hs-row{display:flex;align-items:center;justify-content:space-between;gap:20px}
.hs-dots{display:flex;gap:18px;flex:1;max-width:620px}
.hs-dot{flex:1;min-width:44px;background:none;border:0;color:rgba(243,240,230,.6);padding:8px 0;cursor:pointer;text-align:left;font:500 .74rem var(--font);letter-spacing:.12em}
.hs-dot span{display:block;margin-bottom:8px}
.hs-dot[aria-current] {color:#F3F0E6}
.hs-dot i{display:block;height:2px;background:rgba(243,240,230,.25);position:relative;overflow:hidden}
.hs-dot i::after{content:"";position:absolute;inset:0;background:#F3F0E6;transform:scaleX(0);transform-origin:left}
.hs-dot.done i::after{transform:scaleX(1)}
.hs-dot.run i::after{animation:hs-fill 7s linear forwards}
@keyframes hs-fill{to{transform:scaleX(1)}}
.hs.paused .hs-dot.run i::after,.hs.paused .hs-slide.on .hs-img{animation-play-state:paused}
.hs-nav{display:flex;gap:8px}
.hs-btn{width:48px;height:48px;display:grid;place-items:center;background:rgba(17,18,19,.35);color:#F3F0E6;border:1px solid rgba(243,240,230,.35);cursor:pointer;border-radius:2px;-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px)}
.hs-btn:hover{background:rgba(243,240,230,.12);border-color:#F3F0E6}
.hs-btn .ic-play{display:none}.hs-btn.is-paused .ic-play{display:block}.hs-btn.is-paused .ic-pause{display:none}
@media(max-width:760px){
  .hs{height:clamp(540px,calc(100svh - 128px),760px)}
  .hs-slide::after{background:linear-gradient(0deg,rgba(12,11,10,.92) 0%,rgba(12,11,10,.72) 42%,rgba(12,11,10,.15) 72%,rgba(12,11,10,.1) 100%)}
  .hs-cap{align-items:flex-end;padding-bottom:104px}
  .hs-in{padding-inline:20px}
  .hs-t{font-size:clamp(2.1rem,9.6vw,2.8rem)}
  .hs-img{object-position:var(--posm)}
  .hs-d{margin:12px 0 20px;font-size:.95rem}
  .hs-cta .btn{flex:1;min-height:48px;padding-inline:14px}
  .hs-ui{padding-bottom:18px}
  .hs-dots{gap:8px}.hs-dot span{display:none}.hs-dot{padding:20px 0}
  .hs-btn{width:44px;height:44px}
  .hs-nav [data-step]{display:none}
}
/* ---- réassurance ---- */
.usp{background:var(--surface);border-bottom:1px solid var(--line)}
.usp-in{max-width:1200px;margin-inline:auto;padding:22px max(16px,env(safe-area-inset-left,0px));display:grid;grid-template-columns:repeat(4,1fr);gap:20px}
.usp-i{display:flex;align-items:center;gap:14px;color:var(--fg)}
.usp-i .ic{width:30px;height:30px;color:var(--accent-ink);stroke-width:1.3}
.usp-i b{display:block;font-weight:500;font-size:.92rem}.usp-i span{display:block;font-size:.8rem;color:var(--muted)}
@media(max-width:900px){.usp-in{grid-template-columns:1fr 1fr;gap:18px 14px;padding-block:20px}.usp-i{align-items:flex-start}.usp-i .ic{width:26px;height:26px}.usp-i b{font-size:.86rem}.usp-i span{font-size:.75rem}}
/* ---- sections ---- */
.sec2{padding-block:clamp(44px,6vw,80px)}
.sh{display:flex;justify-content:space-between;align-items:flex-end;gap:16px 24px;flex-wrap:wrap;margin-bottom:clamp(22px,3vw,36px)}
.sh h2{font-size:clamp(1.7rem,3.4vw,2.6rem)}
.sh-r{display:flex;align-items:center;gap:18px}
.lnk{font-size:.9rem;font-weight:500;text-decoration:none;border-bottom:1px solid currentColor;padding-bottom:2px}
.lnk:hover{color:var(--accent-ink)}
/* univers */
.cats{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.cat{position:relative;display:block;aspect-ratio:3/4;overflow:hidden;background:var(--surface);color:#F3F0E6;text-decoration:none;border-radius:2px}
.cat img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:transform .9s cubic-bezier(.2,.7,.2,1)}
.cat::after{content:"";position:absolute;inset:0;background:linear-gradient(0deg,rgba(12,11,10,.75),rgba(12,11,10,0) 55%)}
.cat:hover img{transform:scale(1.06)}
.cat-cap{position:absolute;left:0;right:0;bottom:0;z-index:1;padding:20px;display:grid;gap:2px}
.cat-cap b{font-size:1.25rem;font-weight:400;letter-spacing:-.01em}
.cat-cap small{font-size:.8rem;color:rgba(243,240,230,.75)}
.cat-cap em{font-style:normal;font-size:.82rem;font-weight:500;margin-top:8px;display:inline-flex;align-items:center;gap:6px}
.cat:hover .cat-cap em .ic{transform:translateX(4px)}.cat-cap em .ic{transition:transform .3s}
@media(max-width:900px){.cats{grid-template-columns:1fr 1fr;gap:10px}.cat-cap{padding:14px}.cat-cap b{font-size:1.05rem}}
/* carrousels */
.rail{display:grid;grid-auto-flow:column;grid-auto-columns:calc((100% - 3*20px)/4);gap:28px 20px;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none;overscroll-behavior-x:contain;padding-bottom:4px}
.rail::-webkit-scrollbar{display:none}
.rail>.pc{scroll-snap-align:start}
.rail-nav{display:flex;gap:8px}
.rn{width:44px;height:44px;display:grid;place-items:center;background:transparent;border:1px solid var(--line);color:var(--fg);cursor:pointer;border-radius:2px}
.rn:hover:not(:disabled){border-color:var(--fg)}.rn:disabled{opacity:.35;cursor:default}
@media(max-width:1000px){.rail{grid-auto-columns:calc((100% - 2*16px)/3);gap:24px 16px}}
@media(max-width:700px){.rail{grid-auto-columns:72%;gap:20px 12px;margin-inline:-16px;padding-inline:16px;scroll-padding-inline:16px}.rail-nav{display:none}}
/* cartes produit */
.pc .im{position:relative}
.pc .alt{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transition:opacity .5s ease;border-radius:2px;aspect-ratio:1/1}
@media(hover:hover){.pc:hover .alt{opacity:1}}
.pc .tag{position:absolute;left:10px;top:10px;z-index:2;font-size:.66rem;letter-spacing:.14em;text-transform:uppercase;font-weight:500;padding:5px 8px;background:var(--bg);color:var(--fg);border-radius:2px}
.pc .badge~.tag,.pc .ph:has(.badge)~.tag{top:44px}
.pc-c{margin:14px 0 0;font-size:.7rem;letter-spacing:.16em;text-transform:uppercase;color:var(--muted)}
.pc h3{margin-top:4px}
/* bannière promo */
.promo{background:var(--card);border-block:1px solid var(--line)}
.promo-in{max-width:1200px;margin-inline:auto;display:grid;grid-template-columns:1.15fr 1fr;align-items:center;gap:clamp(28px,5vw,72px);padding:clamp(40px,6vw,80px) max(16px,env(safe-area-inset-left,0px))}
.promo-img{position:relative;overflow:hidden;aspect-ratio:3/2;border-radius:2px;background:var(--surface)}
.promo-img img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.promo-badge{position:absolute;left:14px;top:14px;background:#111213;color:#F3F0E6;font-size:.7rem;letter-spacing:.16em;text-transform:uppercase;padding:7px 10px;font-weight:500}
.promo-txt h2{font-size:clamp(1.9rem,3.6vw,3rem);margin-bottom:14px}
.promo-d{color:var(--muted);margin:0 0 18px;max-width:46ch}
.promo-l{list-style:none;padding:0;margin:0 0 22px;display:grid;grid-template-columns:1fr 1fr;gap:10px 18px}
.promo-l li{display:flex;gap:10px;align-items:center;font-size:.92rem}
.promo-l li::before{content:"";width:6px;height:6px;background:var(--accent);flex:none}
.promo-p{font-size:1.6rem;font-weight:500;margin:0 0 20px}.promo-p span{font-size:.75rem;letter-spacing:.16em;text-transform:uppercase;color:var(--muted);font-weight:400;margin-right:6px}
.promo-cta{display:flex;gap:12px;flex-wrap:wrap}
@media(max-width:860px){.promo-in{grid-template-columns:1fr}.promo-l{grid-template-columns:1fr}.promo-cta .btn{flex:1}}
/* bannière sur mesure */
.big{position:relative;overflow:hidden;min-height:clamp(440px,70vh,640px);display:flex;align-items:center;color:#F3F0E6;background:#111213}
.big-img{position:absolute;left:0;right:0;top:-12%;height:124%;width:100%;object-fit:cover}
.big::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(12,11,10,.82),rgba(12,11,10,.35) 60%,rgba(12,11,10,.15))}
.big-in{position:relative;z-index:1;width:100%;max-width:1200px;margin-inline:auto;padding:56px max(16px,env(safe-area-inset-left,0px))}
.big-in>*{max-width:560px}
.big .eyebrow{color:#D9B88F}
.big h2{font-size:clamp(2rem,4.4vw,3.6rem);color:#F3F0E6;margin-bottom:16px}
.big p{color:rgba(243,240,230,.85);margin:0 0 26px}
.big .big-b1{background:#F3F0E6;color:#111213;min-height:52px;padding-inline:26px;gap:10px}
@media(max-width:700px){.big::after{background:linear-gradient(0deg,rgba(12,11,10,.9),rgba(12,11,10,.55) 60%,rgba(12,11,10,.3))}.big{align-items:flex-end}.big .big-b1{width:100%}}
/* étapes */
.steps{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(4,1fr);gap:20px;counter-reset:s}
.steps li{position:relative;padding:26px 22px;border:1px solid var(--line);background:var(--card);border-radius:2px}
.steps .ic{width:30px;height:30px;color:var(--accent-ink);stroke-width:1.3;margin-bottom:14px}
.steps b{display:block;font-weight:500;margin-bottom:6px}.steps p{margin:0;color:var(--muted);font-size:.9rem}
.st-n{position:absolute;right:18px;top:18px;font-size:.75rem;letter-spacing:.14em;color:var(--muted)}
@media(max-width:900px){.steps{grid-template-columns:1fr 1fr;gap:10px}.steps li{padding:18px 16px}}
@media(max-width:480px){.steps{grid-template-columns:1fr}}
/* instagram */
.igg{display:grid;grid-template-columns:repeat(6,1fr);gap:8px}
.igt{position:relative;display:block;aspect-ratio:1;overflow:hidden;background:var(--surface);border-radius:2px}
.igt img{width:100%;height:100%;object-fit:cover;transition:transform .7s}
.igt span{position:absolute;inset:0;display:grid;place-items:center;color:#fff;background:rgba(12,11,10,.35);opacity:0;transition:opacity .3s}
.igt:hover img{transform:scale(1.06)}.igt:hover span,.igt:focus-visible span{opacity:1}
@media(max-width:700px){.igg{grid-template-columns:repeat(3,1fr);gap:4px}}
.sh .btn.ghost{gap:8px}

/* ================= MOBILE D'ABORD ================= */
.tb{display:none}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.mban{display:block;background:#F3F0E6;line-height:0}.mban img{width:100%;height:auto;display:block}
@media(max-width:760px){
  /* barre d'onglets en bas, comme une appli */
  .tb{display:grid;grid-template-columns:repeat(4,1fr);position:fixed;left:0;right:0;bottom:0;z-index:60;background:var(--bg);border-top:1px solid var(--line);padding-bottom:env(safe-area-inset-bottom,0px)}
  .tb a,.tb button{position:relative;min-height:58px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3px;background:none;border:0;color:var(--muted);font:500 .66rem var(--font);letter-spacing:.04em;text-decoration:none;cursor:pointer}
  .tb .ic{width:22px;height:22px}
  .tb a[aria-current]{color:var(--fg)}.tb a[aria-current]::before{content:"";position:absolute;top:0;left:30%;right:30%;height:2px;background:var(--accent)}
  .tb .tb-wa{color:var(--fg)}
  .tb-cnt{position:absolute;top:7px;left:calc(50% + 6px);min-width:17px;height:17px;padding:0 4px;border-radius:9px;background:var(--btn-bg);color:var(--btn-fg);font-size:.62rem;display:grid;place-items:center}
  .tb-cnt[data-n="0"]{display:none}
  body{padding-bottom:calc(58px + env(safe-area-inset-bottom,0px))}
  #waf{display:none!important}
  /* slider : photo en haut, texte en dessous */
  .hs{height:calc(100svh - var(--top,104px) - 58px - env(safe-area-inset-bottom,0px));min-height:560px;max-height:820px}
  .hs-slide picture{position:absolute;left:0;right:0;top:0;height:54%;overflow:hidden;display:block}
  .hs-slide picture .hs-img{object-position:var(--posm)}
  .hs-slide::after{inset:0 0 auto 0;height:54%;background:linear-gradient(0deg,#111213 0%,rgba(17,18,19,0) 28%)}
  .hs-cap{top:54%;align-items:flex-start;padding:4px 0 84px}
  .hs-k{margin-bottom:8px;font-size:.7rem}
  .hs-t{font-size:clamp(1.85rem,8.4vw,2.4rem);line-height:1.05}
  .hs-d{margin:10px 0 16px;font-size:.92rem;line-height:1.5;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
  .hs-cta{flex-wrap:nowrap}
  .hs-ui{padding-bottom:14px}
  /* sections plus compactes */
  .sec2{padding-block:40px}
  .sh{margin-bottom:18px;align-items:center}.sh h2{font-size:1.6rem}
  /* réassurance : bande qui défile au doigt */
  .usp-in{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none;gap:24px;padding-block:16px}
  .usp-in::-webkit-scrollbar{display:none}
  .usp-i{flex:0 0 auto;scroll-snap-align:start;align-items:center}
  .usp-i span{white-space:nowrap}
  /* univers : carrousel horizontal */
  .cats{display:grid;grid-auto-flow:column;grid-template-columns:none;grid-auto-columns:46%;gap:10px;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none;margin-inline:-16px;padding-inline:16px;scroll-padding-inline:16px}
  .cats::-webkit-scrollbar{display:none}.cat{scroll-snap-align:start}
  .rail{grid-auto-columns:62%}
  .pc .add{width:100%;justify-content:center}
  /* étapes : carrousel */
  .steps{display:grid;grid-auto-flow:column;grid-template-columns:none;grid-auto-columns:78%;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none;margin-inline:-16px;padding-inline:16px;scroll-padding-inline:16px}
  .steps::-webkit-scrollbar{display:none}.steps li{scroll-snap-align:start}
  .promo-in{padding-block:36px;gap:22px}
  .promo-txt h2{font-size:1.8rem}
  .big{min-height:420px}.big-in{padding-block:40px}
  .big h2{font-size:1.9rem}
  .sh .btn.ghost{width:100%}
  footer{padding-bottom:20px}
}


.share-b{margin-top:10px;gap:10px}.share-b .ic{width:18px;height:18px}
/* ===== Page produit : Commander maintenant ===== */
.pd-bar{position:fixed;left:0;right:0;bottom:0;z-index:55;display:flex;align-items:center;gap:16px;
  padding:10px max(16px,calc((100vw - 1200px)/2)) calc(10px + env(safe-area-inset-bottom,0px));background:var(--bg);border-top:1px solid var(--line);
  box-shadow:0 -10px 30px rgba(0,0,0,.07);transform:translateY(110%);transition:transform .35s cubic-bezier(.2,.7,.2,1)}
.pd-bar.on{transform:none}
.pd-bar-i{flex:1;min-width:0}
.pd-bar-i b{display:block;font-weight:500;font-size:.92rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.pd-bar-i .price{font-size:.92rem;margin:0}
.pd-bar .btn{min-height:50px;padding-inline:30px;white-space:nowrap}
body.has-pdbar #waf{transform:translateY(-80px)}
.pd-rel .pc .add{display:none}
/* cartes produit uniformes : même fond beige, même hauteur, bouton aligné en bas */
.pc{display:flex;flex-direction:column}
.pc .ph{background:#ECE6D9}
.pc .ph img{object-fit:cover}
.pc h3{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;min-height:2.6em;line-height:1.3}
.pc .add{margin-top:auto}
.pc .pr,.pc .price{margin-bottom:10px}
#ad{min-height:52px}
@media(max-width:760px){
  .pd-bar{bottom:calc(58px + env(safe-area-inset-bottom,0px));padding:10px 16px;gap:12px;transform:none}
  .pd-bar-i{flex:0 1 auto;max-width:44%}
  .pd-bar .btn{flex:1 1 auto;padding-inline:14px}
  #ad{display:none}
  .buy{margin-bottom:10px}
  body.has-pdbar{padding-bottom:calc(58px + 72px + env(safe-area-inset-bottom,0px))}
}
@media (prefers-reduced-motion:reduce){.pd-bar{transition:none}}
/* aligne le contenu des sections pleine largeur sur la grille de la page */
.hs-in,.usp-in,.promo-in,.big-in{max-width:none;padding-inline:max(20px,calc((100vw - 1200px)/2))}
@media (prefers-reduced-motion:reduce){.hs-slide .hs-k,.hs-slide .hs-t,.hs-slide .hs-d,.hs-slide .hs-cta{opacity:1;transform:none;animation:none!important}.hs-slide.on .hs-img{animation:none}}
'''


def _src(name):
    s = json.load(open('/home/claude/nervina-maroccc/store.json'))
    u = s['shopify']['images/' + name + '.webp']
    return ORIG + urllib.parse.unquote(u.split('?')[0].rsplit('/', 1)[1])


def make_assets(repo):
    os.makedirs(repo + '/vendor', exist_ok=True)
    for f in ['gsap.min.js', 'ScrollTrigger.min.js']:
        shutil.copy(f'{VEND}/GSAP/dist/{f}', f'{repo}/vendor/{f}')
    shutil.copy(f'{VEND}/out/lenis.min.js', f'{repo}/vendor/lenis.min.js')
    os.makedirs(repo + '/images/home', exist_ok=True)
    for name, src, crop, w in ASSETS:
        im = Image.open(_src(src)).convert('RGB')
        if crop: im = im.crop(crop)
        if im.width > w: im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        im.save(f'{repo}/images/home/{name}.webp', 'WEBP', quality=80, method=6)


SCRIPTS = '<script src="vendor/gsap.min.js"></script>\n<script src="vendor/ScrollTrigger.min.js"></script>\n<script src="vendor/lenis.min.js"></script>\n'


TB = r'''<div class="tb" role="navigation" aria-label="Navigation rapide">
  <a href="#accueil" data-r="accueil"><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 11l8-7 8 7v9H4z"/><path d="M10 20v-5h4v5"/></svg>Accueil</a>
  <a href="#catalogue" data-r="catalogue"><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><rect x="4" y="4" width="7" height="7"/><rect x="13" y="4" width="7" height="7"/><rect x="4" y="13" width="7" height="7"/><rect x="13" y="13" width="7" height="7"/></svg>Catalogue</a>
  <a class="tb-wa" id="tbwa" href="#" target="_blank" rel="noopener"><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 20l1.3-4A8 8 0 1 1 8 18.7z"/><path d="M9 9.5c.3 2 2.2 4.2 5 5"/></svg>WhatsApp</a>
  <button type="button" id="tbcart" aria-label="Ouvrir le panier"><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 8h14l-1 12H6z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/></svg>Panier<span class="tb-cnt" data-n="0">0</span></button>
</div>
'''


def patch(m, c, s):
    for a, b in [('scrollTo(0,0)', 'toY(0)'), ('scrollTo(0,k)', 'toY(k)'), ('scrollTo(0,y)', 'toY(y)')]:
        assert a in m, a; m = m.replace(a, b)
    i = m.index('accueil(){'); j = m.index('catalogue(){', i)
    acc = ACCUEIL.replace('__HOME__', json.dumps(HOME, ensure_ascii=False)).replace('__ICONS__', json.dumps(ICONS))
    m = m[:i] + acc + m[j:]
    m2 = re.sub(r'function card\(p\)\{.*?</article>`\}', lambda _: CARD, m, count=1, flags=re.S)
    assert m2 != m; m = m2
    k = m.index('function perks(')
    m = m[:k] + HELPERS.lstrip('\n') + m[k:]
    a = "$('#ann').textContent=st.banner||'';$('#ann').hidden=!st.banner;"
    assert a in m; m = m.replace(a, 'annSet();')
    m = m.replace("function bind(h){\n", "function bind(h){\n  if(h==='accueil')mgInit();\n", 1)
    m = m.replace("function route(){\n", "function route(){\n  mgKill();\n", 1)
    m = m.replace('<div id="layer"></div>', '<div id="layer" data-lenis-prevent></div>', 1)


    # partage + pages produit : démarrage direct sur une fiche, bouton « Partager »
    a = "let h=(location.hash||'#accueil').slice(1),html;"
    assert a in m; m = m.replace(a, "let h=(location.hash||('#'+(window.NV_START||'accueil'))).slice(1),html;")
    a = 'target="_blank" rel="noopener">Poser une question sur WhatsApp</a>'
    assert a in m
    m = m.replace(a, a + '\n  <button class="btn ghost wide share-b" id="share" type="button" data-id="${esc(p.id)}" data-t="${esc(p.title)}" data-pr="${esc(MAD(p.price))}"><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 15V3M7 8l5-5 5 5"/><path d="M5 12v8h14v-8"/></svg>Partager cette pièce</button>')
    a = "$('#ad').onclick=()=>{add(id,n);openCart()};"
    assert a in m
    m = m.replace(a, "const sb=$('#share');if(sb)sb.onclick=async()=>{const u='https://nervina.ma/p/'+sb.dataset.id+'/',t=sb.dataset.t+' · '+sb.dataset.pr+' · Nervina Maroc';try{if(navigator.share){await navigator.share({title:sb.dataset.t,text:t,url:u});return}}catch(e){if(e&&e.name==='AbortError')return}window.open('https://wa.me/?text='+encodeURIComponent(t+'\\n'+u),'_blank','noopener')};" + a, 1)
    # page produit : « Commander maintenant » (bouton + barre collante), sans « Ajouter au panier »
    a = '<button class="btn" id="ad" style="flex:1;min-width:180px">Ajouter au panier</button>'
    assert a in m; m = m.replace(a, '<button class="btn" id="ad" style="flex:1;min-width:180px">Commander maintenant</button>')
    a = '<section class="sec"><div class="sechead"><h2>Dans la même collection</h2></div>'
    assert a in m
    m = m.replace(a, '<div class="pd-bar" id="pdbar"><div class="pd-bar-i"><b>${esc(p.title)}</b>${priceH(p)}</div><button class="btn" id="ad2" type="button">Commander maintenant</button></div>\n  ' + a.replace('<section class="sec">', '<section class="sec pd-rel">'))
    a = "$('#ad').onclick=()=>{add(id,n);openCart()};"
    assert a in m
    m = m.replace(a, "const buy=()=>{cart[id]=Math.min(20,(cart[id]||0)+n);saveCart();updCnt();openCart()};$('#ad').onclick=buy;$('#ad2').onclick=buy;document.body.classList.add('has-pdbar');"
      "if('IntersectionObserver' in window){PDIO=new IntersectionObserver(es=>{const bar=$('#pdbar');if(bar)bar.classList.toggle('on',!es[0].isIntersecting)});PDIO.observe($('#ad'))}else{$('#pdbar').classList.add('on')}")
    a = "function mgKill(){"
    assert a in m
    m = m.replace(a, "let PDIO=null;\nfunction mgKill(){document.body.classList.remove('has-pdbar');if(PDIO){PDIO.disconnect();PDIO=null}", 1)
    a = '<a class="btn wa-float" id="waf" href="#" target="_blank" rel="noopener">WhatsApp</a>'
    assert a in m; m = m.replace(a, a + '\n' + TB, 1)
    a = "function updCnt(){$('#cnt').textContent=Object.entries(cart).filter(([id])=>prod(id)).reduce((a,[,b])=>a+b,0)}"
    assert a in m
    m = m.replace(a, "function updCnt(){const n=Object.entries(cart).filter(([id])=>prod(id)).reduce((a,[,b])=>a+b,0);$('#cnt').textContent=n;const t=document.querySelector('.tb-cnt');if(t){t.textContent=n;t.dataset.n=n}}")
    a = "function setNav(h){document.querySelectorAll('nav a')"
    assert a in m; m = m.replace(a, "function setNav(h){document.querySelectorAll('nav a,.tb a[data-r]')")
    a = "$('#waf').href=WAU("
    assert a in m; m = m.replace(a, "$('#tbwa').href=$('#waf').href=WAU(")
    a = "chrome();updCnt();route();"
    assert a in m; m = m.replace(a, "chrome();updCnt();route();$('#tbcart').onclick=()=>openCart();")
    m = m.replace('<script type="application/json" id="seed">', SCRIPTS + '<script type="application/json" id="seed">', 1)
    for t in ["mgInit();", "mgKill();", "annSet();", "vendor/gsap.min.js", "else scrollTo(0,y)"]:
        assert t in m, t
    return m, c + CSS, s
