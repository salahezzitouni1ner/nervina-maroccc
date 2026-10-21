# Bannière « motion graphic » de l'accueil (GSAP + ScrollTrigger + SplitText + DrawSVG, Lenis)
# Effets inspirés de React Bits (BlurText, ShinyText, CircularText, Noise), réécrits en GSAP sans React.
import os, shutil
import numpy as np
from PIL import Image, ImageFilter

VEND = '/tmp/claude-0/-home-claude/ff2ae7a3-8d31-5e47-be59-c1e595b976e6/scratchpad/vend'
ROOM = 'images/meuble-tv-sur-pieds-noyer-creme-3.webp'
CUT_SRC = 'images/table-basse-amazonica-1.webp'
CUT = 'images/hero/amazonica.webp'
FEAT = 'table-basse-amazonica'

ARCH = 'M6 262V102a94 94 0 0 1 188 0v160'

OLD_HERO_START = '  return `<section class="hero">'

HERO = r'''  const fp=prod('__FEAT__');
  const mq=['Tables','Meubles TV',"Meubles d'entrée",'Tables de chevet','Sur mesure','Fait main au Maroc'];
  const mqh=mq.map(x=>`<span>${esc(x)}</span><svg viewBox="0 0 24 30"><path d="M3 29V12a9 9 0 0 1 18 0v17"/></svg>`).join('');
  return `<section class="mg" id="mg" aria-label="Nervina Maroc">
  <div class="mg-bg" aria-hidden="true"><div class="mg-glow"></div><div class="mg-grain"></div></div>
  <div class="mg-scene" aria-hidden="true">
    <div class="mg-archwrap">
      <svg class="mg-ripples" viewBox="0 0 200 264" preserveAspectRatio="none"><path class="mg-rip" d="__ARCH__"/><path class="mg-rip" d="__ARCH__"/><path class="mg-rip" d="__ARCH__"/></svg>
      <div class="mg-win"><div class="mg-par"><img src="__ROOM__" alt="" fetchpriority="high" decoding="async"></div></div>
      <svg class="mg-line" viewBox="0 0 200 264" preserveAspectRatio="none"><path d="__ARCH__"/></svg>
      <div class="mg-badge"><svg class="mg-ring" viewBox="0 0 100 100"><defs><path id="mgc" d="M50,50 m-38,0 a38,38 0 1,1 76,0 a38,38 0 1,1 -76,0"/></defs><text><textPath href="#mgc" textLength="236">FAIT MAIN AU MAROC · SUR MESURE ·</textPath></text></svg><svg class="mg-bi" viewBox="0 0 24 30"><path d="M3 29V12a9 9 0 0 1 18 0v17"/></svg></div>
    </div>
    <div class="mg-obj"><div class="mg-shadow"></div><img class="mg-table" src="__CUT__" alt="" decoding="async"></div>
    <span class="mg-chip c1"><i style="background:linear-gradient(135deg,#7a4b2c,#4a2b17)"></i>Noyer massif</span>
    <span class="mg-chip c2"><i style="background:linear-gradient(135deg,#efdcc2,#c9a983)"></i>Verre champagne</span>
    <span class="mg-chip c3"><i style="background:#D9B88F"></i>Sur mesure</span>
  </div>
  <div class="mg-txt">
    <p class="eyebrow mg-eye">Mobilier · Décoration · Menuiserie</p>
    <h1 class="mg-h"><span class="mg-h1">${esc(st.heroTitle1)}</span> <em class="mg-em">${esc(st.heroTitle2)}</em></h1>
    <p class="lead mg-lead">${esc(st.heroLead)}</p>
    <div class="mg-cta"><a class="btn mg-b1" href="#catalogue">Voir le catalogue</a><a class="btn mg-b2" href="#contact">Nous contacter</a></div>
    ${fp&&!fp.hidden?`<a class="mg-tag" href="#p-${esc(fp.id)}"><span class="mg-k">En vedette</span><b>${esc(fp.title)}</b><span class="mg-p">${MAD(fp.price)} <svg viewBox="0 0 16 10" aria-hidden="true"><path d="M0 5h14M10 1l4 4-4 4"/></svg></span></a>`:''}
  </div>
  <div class="mg-mq" aria-hidden="true"><div class="mg-track"><div>${mqh}${mqh}</div><div>${mqh}${mqh}</div></div></div>
  <button class="mg-pp" id="mgpp" aria-label="Mettre l'animation en pause"><svg viewBox="0 0 20 20" aria-hidden="true"><path class="ic-pause" d="M6 4h3v12H6zM11 4h3v12h-3z"/><path class="ic-play" d="M6 4l10 6-10 6z"/></svg></button>
</section>`+`'''.replace('__ARCH__', ARCH).replace('__ROOM__', ROOM).replace('__CUT__', CUT).replace('__FEAT__', FEAT)

HELPERS = r'''
/* ---------- défilement doux (Lenis) + bannière animée (GSAP) ---------- */
const RM=matchMedia('(prefers-reduced-motion: reduce)');
let LEN=null;
(function(){
  if(!window.Lenis||RM.matches)return;
  LEN=new Lenis({autoRaf:!window.gsap,anchors:false,lerp:.1,smoothWheel:true});
  if(window.gsap){if(window.ScrollTrigger){gsap.registerPlugin(ScrollTrigger);LEN.on('scroll',ScrollTrigger.update)}gsap.ticker.add(t=>LEN.raf(t*1000));gsap.ticker.lagSmoothing(0)}
})();
const toY=y=>{if(LEN)LEN.scrollTo(y,{immediate:true,force:true});else scrollTo(0,y)};
let MG=null;
function mgKill(){if(MG){try{MG.ctx&&MG.ctx.revert()}catch(e){}MG=null}}
function mgGrain(){
  if(mgGrain.u)return mgGrain.u;
  try{const c=document.createElement('canvas');c.width=c.height=160;const x=c.getContext('2d'),d=x.createImageData(160,160);
    for(let i=0;i<d.data.length;i+=4){const v=Math.random()*255|0;d.data[i]=d.data[i+1]=d.data[i+2]=v;d.data[i+3]=Math.random()*70|0}
    x.putImageData(d,0,0);mgGrain.u=c.toDataURL()}catch(e){mgGrain.u=''}
  return mgGrain.u}
function mgSync(){
  if(!MG)return;const on=MG.vis!==false&&!MG.user&&!document.hidden,root=$('#mg');
  MG.L.forEach(t=>on?t.resume():t.pause());
  if(root){root.classList.toggle('mg-paused',!on);const pp=$('#mgpp');if(pp){pp.classList.toggle('is-paused',!!MG.user);pp.setAttribute('aria-label',MG.user?"Lancer l'animation":"Mettre l'animation en pause")}}
}
document.addEventListener('visibilitychange',mgSync);
function mgInit(){
  const root=$('#mg');if(!root)return;
  const g=root.querySelector('.mg-grain');if(g){const u=mgGrain();if(u)g.style.backgroundImage=`url(${u})`}
  const pp=$('#mgpp');
  if(!window.gsap||!window.ScrollTrigger||!window.SplitText||RM.matches){root.classList.add('mg-static');if(pp)pp.hidden=true;return}
  gsap.registerPlugin(ScrollTrigger,SplitText,...(window.DrawSVGPlugin?[DrawSVGPlugin]:[]));
  MG={L:[],vis:true,user:false};
  const st=MG;
  MG.ctx=gsap.context(()=>{
    const q1=s=>root.querySelector(s),qa=s=>[...root.querySelectorAll(s)];
    const split=SplitText.create(q1('.mg-h1'),{type:'words',wordsClass:'mg-w'});
    const tl=gsap.timeline({paused:true,defaults:{ease:'power3.out'}});
    tl.from('.mg-glow',{opacity:0,scale:.5,duration:1.8},0)
      .from('.mg-grain',{opacity:0,duration:1},0)
      .from('.mg-line path',window.DrawSVGPlugin?{drawSVG:'50% 50%',duration:1.4,ease:'power2.inOut'}:{opacity:0,duration:1},.1)
      .from('.mg-win',{clipPath:'inset(100% 0% 0% 0%)',duration:1.3,ease:'power4.inOut'},.45)
      .from('.mg-win img',{scale:1.4,duration:2,ease:'power3.out'},.45)
      .from('.mg-eye',{opacity:0,y:10,duration:.6},.5)
      .from(split.words,{opacity:0,y:24,filter:'blur(12px)',stagger:.07,duration:.95},.65)
      .from('.mg-em',{clipPath:'inset(0% 100% 0% 0%)',duration:1.1,ease:'power4.inOut'},1.05)
      .from('.mg-table',{y:-170,opacity:0,rotation:-7,filter:'blur(10px)',duration:1.15,ease:'power4.out'},1.05)
      .from('.mg-shadow',{scaleX:.15,opacity:0,duration:1.15},1.05)
      .from('.mg-badge',{scale:0,rotation:-140,opacity:0,duration:1,ease:'back.out(1.6)'},1.3)
      .from('.mg-chip',{y:16,scale:.7,opacity:0,stagger:.13,duration:.75,ease:'back.out(2)'},1.45)
      .from('.mg-lead,.mg-cta,.mg-tag',{opacity:0,y:16,stagger:.1,duration:.7},1.35)
      .from('.mg-mq',{opacity:0,y:12,duration:.8},1.6)
      .from('.mg-pp',{opacity:0,duration:.6},1.8);
    const imgs=qa('.mg-win img,.mg-table').map(i=>i.decode?i.decode().catch(()=>{}):Promise.resolve());
    Promise.race([Promise.all(imgs),new Promise(r=>setTimeout(r,1400))]).then(()=>tl.play());
    const L=st.L,loop=v=>(L.push(v),v);
    loop(gsap.to('.mg-table',{y:-10,duration:2.7,ease:'sine.inOut',yoyo:true,repeat:-1,delay:2.3}));
    loop(gsap.to('.mg-shadow',{scaleX:.84,opacity:.5,duration:2.7,ease:'sine.inOut',yoyo:true,repeat:-1,delay:2.3}));
    const ring=loop(gsap.to('.mg-ring',{rotation:360,duration:20,ease:'none',repeat:-1,transformOrigin:'50% 50%'}));
    qa('.mg-chip').forEach((c,i)=>loop(gsap.to(c,{y:i%2?8:-8,x:i%2?-5:5,duration:3+i*.7,ease:'sine.inOut',yoyo:true,repeat:-1,delay:2.2})));
    loop(gsap.timeline({repeat:-1,delay:1.7}).fromTo('.mg-rip',{scale:1,opacity:.5},{scale:1.34,opacity:0,duration:3.3,ease:'power1.out',stagger:1.1,transformOrigin:'50% 100%'}));
    loop(gsap.to('.mg-glow',{xPercent:14,yPercent:-10,scale:1.15,duration:7,ease:'sine.inOut',yoyo:true,repeat:-1}));
    loop(gsap.fromTo('.mg-em',{backgroundPosition:'100% 0'},{backgroundPosition:'0% 0',duration:2.4,ease:'power2.inOut',repeat:-1,repeatDelay:3.2,delay:2.6}));
    loop(gsap.to('.mg-track',{xPercent:-50,duration:30,ease:'none',repeat:-1}));
    gsap.timeline({scrollTrigger:{trigger:root,start:'top top',end:'bottom top',scrub:.6}})
      .to('.mg-par',{yPercent:12,scale:1.06,ease:'none'},0)
      .to('.mg-obj',{y:-60,ease:'none'},0)
      .to('.mg-archwrap',{y:36,ease:'none'},0)
      .to('.mg-txt',{y:-28,ease:'none'},0);
    ScrollTrigger.create({trigger:root,start:'top bottom',end:'bottom top',
      onToggle:s=>{st.vis=s.isActive;mgSync()},
      onUpdate:s=>{const v=Math.abs(s.getVelocity());if(v>60&&!st.user)gsap.to(ring,{timeScale:1+Math.min(v/250,7),duration:.15,overwrite:true,onComplete:()=>gsap.to(ring,{timeScale:1,duration:1.4})})}});
  },root);
  if(pp)pp.onclick=()=>{st.user=!st.user;mgSync()};
  mgSync();
}
'''

CSS = r'''
/* ===== Bannière animée (motion graphic) ===== */
html.lenis{scroll-behavior:auto}
html.lenis,html.lenis body{height:auto}
.lenis:not(.lenis-autoToggle).lenis-stopped{overflow:clip}
.lenis [data-lenis-prevent]{overscroll-behavior:contain}
.mg{--ink:#F3F0E6;--sand:#D9B88F;--copper:#B07F52;position:relative;overflow:hidden;isolation:isolate;color:var(--ink);background:#111213;
  display:flex;flex-direction:column;min-height:calc(100svh - 128px);margin-inline:calc(-1*max(16px,env(safe-area-inset-left,0px)));padding:14px 20px 0}
.mg-bg{position:absolute;inset:0;z-index:-1;overflow:hidden;pointer-events:none}
.mg-glow{position:absolute;left:50%;top:30%;width:120vw;max-width:900px;aspect-ratio:1;translate:-50% -50%;
  background:radial-gradient(closest-side,rgba(217,184,143,.30),rgba(176,127,82,.14) 45%,rgba(17,18,19,0) 75%)}
.mg-grain{position:absolute;inset:-60%;background-size:160px;opacity:.5;mix-blend-mode:overlay;animation:mg-grain .9s steps(6) infinite}
@keyframes mg-grain{0%{transform:translate(0,0)}20%{transform:translate(-6%,4%)}40%{transform:translate(5%,-3%)}60%{transform:translate(-3%,-6%)}80%{transform:translate(6%,5%)}100%{transform:translate(0,0)}}
.mg-paused .mg-grain{animation-play-state:paused}
/* scène */
.mg-scene{position:relative;height:clamp(290px,44svh,430px);display:grid;place-items:center;flex:none}
.mg-archwrap{position:relative;height:90%;aspect-ratio:200/264}
.mg-win,.mg-ripples,.mg-line{position:absolute;inset:0;width:100%;height:100%}
.mg-win{overflow:hidden;border-radius:47% 47% 0 0/35.6% 35.6% 0 0;clip-path:inset(0% 0% 0% 0%);inset:0 3% 0 3%;width:94%}
.mg-par{position:absolute;inset:-8% 0;will-change:transform}
.mg-par img{width:100%;height:100%;object-fit:cover;object-position:50% 60%}
.mg-win::after{content:"";position:absolute;inset:0;background:linear-gradient(0deg,rgba(17,18,19,.55),rgba(17,18,19,0) 45%)}
.mg-line,.mg-ripples{overflow:visible;fill:none;pointer-events:none}
.mg-line path{stroke:var(--sand);stroke-width:1.4;vector-effect:non-scaling-stroke}
.mg-rip{stroke:rgba(217,184,143,.55);stroke-width:1;vector-effect:non-scaling-stroke;opacity:0}
.mg-badge{position:absolute;right:-9%;top:-2%;width:34%;aspect-ratio:1;display:grid;place-items:center}
.mg-ring{position:absolute;inset:0;width:100%;height:100%;overflow:visible}
.mg-ring text{font:500 8.6px var(--font);letter-spacing:.14em;fill:var(--sand)}
.mg-bi{width:18%;fill:none;stroke:var(--sand);stroke-width:1.8}
.mg-obj{position:absolute;left:50%;bottom:-1%;width:min(94%,470px);translate:-50% 0;will-change:transform}
.mg-table{position:relative;width:100%;height:auto;display:block;filter:drop-shadow(0 18px 22px rgba(0,0,0,.45))}
.mg-shadow{position:absolute;left:18%;right:18%;bottom:2%;height:16%;border-radius:50%;background:radial-gradient(closest-side,rgba(0,0,0,.75),rgba(0,0,0,0));filter:blur(4px)}
.mg-chip{position:absolute;display:inline-flex;align-items:center;gap:7px;padding:6px 10px;font-size:.7rem;font-weight:500;letter-spacing:.02em;white-space:nowrap;
  color:var(--ink);background:rgba(17,18,19,.45);border:1px solid rgba(243,240,230,.2);border-radius:2px;-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px)}
.mg-chip i{width:10px;height:10px;border-radius:50%;flex:none;box-shadow:inset 0 0 0 1px rgba(255,255,255,.2)}
.mg-chip.c1{left:0;top:26%}.mg-chip.c2{right:0;top:54%}.mg-chip.c3{left:2%;top:64%}
/* texte */
.mg-txt{position:relative;padding:14px 0 18px;will-change:transform}
.mg .eyebrow{color:var(--sand);margin:0 0 10px}
.mg-h{font-size:clamp(1.85rem,8.2vw,2.5rem);line-height:1.08;color:var(--ink);font-weight:300}
.mg-h .mg-w{display:inline-block}
.mg-em{display:block;font-style:normal;font-weight:500;color:transparent;
  background:linear-gradient(100deg,var(--sand) 0%,var(--sand) 40%,#FFF4E0 50%,var(--sand) 60%,var(--sand) 100%);background-size:250% 100%;background-position:100% 0;
  -webkit-background-clip:text;background-clip:text;clip-path:inset(0% 0% 0% 0%);padding-bottom:.06em}
.mg-lead{display:none}
.mg-cta{display:flex;gap:10px;margin-top:18px}
.mg-cta .btn{flex:1;min-height:48px;padding-inline:14px}
.mg .mg-b1{background:var(--ink);color:#111213}
.mg .mg-b2{background:transparent;color:var(--ink);border:1px solid rgba(243,240,230,.5)}
.mg .mg-b2:hover{border-color:var(--ink);background:rgba(243,240,230,.08)}
.mg :focus-visible{outline-color:var(--sand)}
.mg-tag{display:none}
/* défilant */
.mg-mq{margin:auto -20px 0;border-top:1px solid rgba(243,240,230,.14);overflow:hidden;padding:12px 0;flex:none}
.mg-track{display:flex;width:max-content;will-change:transform}
.mg-track>div{display:flex;align-items:center;gap:18px;padding-right:18px}
.mg-track span{font-size:.74rem;letter-spacing:.22em;text-transform:uppercase;color:rgba(243,240,230,.72);white-space:nowrap}
.mg-track svg{width:10px;height:13px;fill:none;stroke:var(--sand);stroke-width:2;flex:none}
.mg-pp{position:absolute;top:8px;left:8px;z-index:4;width:44px;height:44px;display:grid;place-items:center;background:transparent;border:0;color:rgba(243,240,230,.8);cursor:pointer}
.mg-pp svg{width:15px;height:15px;fill:currentColor}.mg-pp .ic-play{display:none}
.mg-pp.is-paused .ic-play{display:block}.mg-pp.is-paused .ic-pause{display:none}
.mg-pp:hover{color:var(--ink)}
.mg-pp[hidden]{display:none}
@media (min-width:430px) and (max-width:899px){.mg-scene{height:clamp(320px,48svh,480px)}.mg-cta .btn{flex:0 1 auto;padding-inline:24px}}
@media (min-width:900px){
  .mg{display:grid;grid-template-columns:1.05fr 1fr;grid-template-rows:1fr auto;margin:24px 0 0;border-radius:2px;padding:0 0 0 56px;
    min-height:clamp(560px,calc(100svh - 190px),700px)}
  .mg-txt{grid-column:1;grid-row:1;align-self:center;padding:40px 0}
  .mg-scene{grid-column:2;grid-row:1;height:100%;min-height:480px}
  .mg-archwrap{height:78%}
  .mg-obj{bottom:6%;width:min(96%,520px)}
  .mg-chip{font-size:.76rem;padding:8px 12px}.mg-chip.c1{left:4%;top:24%}.mg-chip.c2{right:3%;top:50%}.mg-chip.c3{left:2%;top:62%}
  .mg-h{font-size:clamp(2.3rem,4.2vw,3.5rem)}
  .mg-lead{display:block;color:rgba(243,240,230,.82);max-width:44ch;margin:20px 0 0;font-size:1.05rem}
  .mg-cta{margin-top:26px}.mg-cta .btn{flex:0 0 auto;padding-inline:26px}
  .mg-tag{display:grid;gap:2px;margin-top:30px;padding-top:18px;border-top:1px solid rgba(243,240,230,.18);max-width:420px;text-decoration:none;color:var(--ink)}
  .mg-tag .mg-k{font-size:.7rem;letter-spacing:.2em;text-transform:uppercase;color:var(--sand)}
  .mg-tag b{font-weight:500}
  .mg-tag .mg-p{display:inline-flex;gap:10px;align-items:center;color:rgba(243,240,230,.8);font-size:.9rem}
  .mg-tag svg{width:16px;height:10px;fill:none;stroke:currentColor;stroke-width:1.4;transition:transform .25s}
  .mg-tag:hover svg{transform:translateX(4px)}
  .mg-mq{grid-column:1/-1;grid-row:2;margin:0}
  .mg-pp{top:14px;left:auto;right:14px}
  .mg-badge{right:-16%;top:-4%;width:38%}
}
@media (prefers-reduced-motion:reduce){.mg-grain{animation:none}}
'''

SLIDES = []  # plus de diaporama


def make_assets(repo):
    os.makedirs(repo + '/vendor', exist_ok=True)
    for f in ['gsap.min.js', 'ScrollTrigger.min.js', 'SplitText.min.js', 'DrawSVGPlugin.min.js']:
        shutil.copy(f'{VEND}/GSAP/dist/{f}', f'{repo}/vendor/{f}')
    shutil.copy(f'{VEND}/out/lenis.min.js', f'{repo}/vendor/lenis.min.js')
    # détourage de la table Amazonica (fond blanc -> transparent, ombre douce conservée)
    from scipy import ndimage
    im = Image.open(os.path.join(repo, CUT_SRC)).convert('RGB'); a = np.asarray(im).astype(float)
    br = a.mean(2); sat = a.max(2) - a.min(2)
    lab, n = ndimage.label((sat < 22) & (br > 168))
    edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    obj = ndimage.binary_fill_holes(ndimage.binary_opening(~np.isin(lab, list(edge)), iterations=1))
    obj = ndimage.binary_erosion(obj, iterations=2)
    m = 10; obj[:m] = obj[-m:] = False; obj[:, :m] = obj[:, -m:] = False
    ao = np.asarray(Image.fromarray((obj * 255).astype('uint8')).filter(ImageFilter.GaussianBlur(1.6))).astype(float) / 255
    sh = np.clip((250 - br) / 90, 0, 1) * 0.55 * (1 - ao); sh[:m] = sh[-m:] = 0; sh[:, :m] = sh[:, -m:] = 0
    alpha = np.clip(ao + sh, 0, 1)
    rgba = np.dstack([np.where(ao[..., None] > .02, a, 0), alpha * 255]).astype('uint8')
    o = Image.fromarray(rgba, 'RGBA'); o = o.crop(Image.fromarray(((alpha * 255) > 14).astype('uint8') * 255).getbbox())
    o.thumbnail((1100, 1100), Image.LANCZOS)
    os.makedirs(os.path.join(repo, 'images/hero'), exist_ok=True)
    o.save(os.path.join(repo, CUT), 'WEBP', quality=86, method=6)


SCRIPTS = ('<script src="vendor/gsap.min.js"></script>\n<script src="vendor/ScrollTrigger.min.js"></script>\n'
           '<script src="vendor/SplitText.min.js"></script>\n<script src="vendor/DrawSVGPlugin.min.js"></script>\n'
           '<script src="vendor/lenis.min.js"></script>\n')


def patch(m, c, s):
    i = m.index(OLD_HERO_START); j = m.index('</section>', i) + len('</section>')
    m = m[:i] + HERO + m[j:]
    for a, b in [('scrollTo(0,0)', 'toY(0)'), ('scrollTo(0,k)', 'toY(k)'), ('scrollTo(0,y)', 'toY(y)')]:
        assert a in m, a; m = m.replace(a, b)
    k = m.index('function perks(')
    m = m[:k] + HELPERS.lstrip('\n') + m[k:]
    m = m.replace("function bind(h){\n", "function bind(h){\n  if(h==='accueil')mgInit();\n", 1)
    m = m.replace("function route(){\n", "function route(){\n  mgKill();\n", 1)
    m = m.replace('<div id="layer"></div>', '<div id="layer" data-lenis-prevent></div>', 1)
    m = m.replace('<script type="application/json" id="seed">', SCRIPTS + '<script type="application/json" id="seed">', 1)
    for t in ["mgInit();", "mgKill();", "data-lenis-prevent", "vendor/gsap.min.js"]:
        assert t in m, t
    return m, c + CSS, s
