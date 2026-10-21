# Bannière plein écran « pièce signature » : Meuble TV Arrondis en noyer
# GSAP (ScrollTrigger, SplitText, DrawSVG) + Lenis. Effets inspirés de React Bits (SplitText, CountUp, ShinyText, Noise).
import os, shutil
import numpy as np
from PIL import Image, ImageFilter

VEND = '/tmp/claude-0/-home-claude/ff2ae7a3-8d31-5e47-be59-c1e595b976e6/scratchpad/vend'
SRC_ORIG = '/mnt/user-data/uploads/jgus0t-ph-files-2026-10-21-102141/ChatGPTImageJun1_2026_02_08_35PM.png'
CUT = 'images/hero/meuble-tv-arrondis.webp'
FEAT = 'meuble-tv-arrondis'
OLD_HERO_START = '  return `<section class="hero">'

HERO = r'''  const fp=prod('__FEAT__')||vis()[0];
  const mq=['Meuble TV Arrondis','Noyer naturel','LED intégrée','Fixation invisible','Sur mesure','Fait main au Maroc'];
  const mqh=mq.map(x=>`<span>${esc(x)}</span><svg viewBox="0 0 24 30"><path d="M3 29V12a9 9 0 0 1 18 0v17"/></svg>`).join('');
  const wa=WAU(`Bonjour Nervina, je suis intéressé(e) par le ${fp.title} (${MAD(fp.price)}).`);
  return `<section class="sg" id="mg" aria-label="${esc(fp.title)}, pièce signature">
  <div class="sg-bg" aria-hidden="true"><div class="sg-wash"></div><div class="mg-grain"></div><div class="sg-vig"></div></div>
  <div class="sg-head">
    <p class="sg-eye"><span class="sg-dot"></span>Pièce signature · ${esc(colName(fp.col))}</p>
    <h1 class="sg-h">${esc(fp.title)}</h1>
    <p class="sg-sub">Noyer naturel · LED intégrée · Suspendu</p>
  </div>
  <div class="sg-stage" aria-hidden="true">
    <div class="sg-rig">
      <div class="sg-unit">
        <svg class="sg-dim sg-dim-w" viewBox="0 0 1000 40" preserveAspectRatio="none"><path d="M500 20H4M4 8v24M500 20h492M996 8v24"/></svg>
        <span class="sg-dl sg-dl-w"><b data-n="200">200</b> cm</span>
        <svg class="sg-dim sg-dim-h" viewBox="0 0 40 1000" preserveAspectRatio="none"><path d="M20 500V4M8 4h24M20 500v492M8 996h24"/></svg>
        <span class="sg-dl sg-dl-h"><b data-n="30">30</b> cm</span>
        <div class="sg-led"><i></i></div>
        <img class="sg-img" src="__CUT__" alt="" fetchpriority="high" decoding="async">
        <div class="sg-sheen"></div>
        <div class="sg-hs up" style="--x:5%;--y:46%"><i></i><span>Angles arrondis</span></div>
        <div class="sg-hs up r" style="--x:62%;--y:40%"><i></i><span>Noyer naturel</span></div>
        <div class="sg-hs dn" style="--x:34%;--y:93%"><i></i><span>LED intégrée</span></div>
      </div>
    </div>
  </div>
  <div class="sg-foot">
    <dl class="sg-specs">
      <div><dt>Longueur</dt><dd><b data-n="200">200</b> cm</dd></div>
      <div><dt>Hauteur</dt><dd><b data-n="30">30</b> cm</dd></div>
      <div><dt>Profondeur</dt><dd><b data-n="30">30</b> cm</dd></div>
    </dl>
    <div class="sg-buy">
      <p class="sg-price"><span>À partir de</span><b>${MAD(fp.price)}</b><small>Dimensions et teinte sur mesure</small></p>
      <div class="sg-cta"><a class="btn sg-b1" href="#p-${esc(fp.id)}">Découvrir le meuble</a><a class="btn sg-b2" href="${wa}" target="_blank" rel="noopener">Commander sur WhatsApp</a></div>
    </div>
  </div>
  <div class="mg-mq" aria-hidden="true"><div class="mg-track"><div>${mqh}${mqh}</div><div>${mqh}${mqh}</div></div></div>
  <button class="mg-pp" id="mgpp" aria-label="Mettre l'animation en pause"><svg viewBox="0 0 20 20" aria-hidden="true"><path class="ic-pause" d="M6 4h3v12H6zM11 4h3v12h-3z"/><path class="ic-play" d="M6 4l10 6-10 6z"/></svg></button>
</section>`+`'''.replace('__CUT__', CUT).replace('__FEAT__', FEAT)

HELPERS = r'''
/* ---------- défilement doux (Lenis) + bannière plein écran (GSAP) ---------- */
const RM=matchMedia('(prefers-reduced-motion: reduce)');
let LEN=null;
(function(){
  if(!window.Lenis||RM.matches)return;
  LEN=new Lenis({autoRaf:!window.gsap,anchors:false,lerp:.1,smoothWheel:true});
  if(window.gsap){if(window.ScrollTrigger){gsap.registerPlugin(ScrollTrigger);LEN.on('scroll',ScrollTrigger.update)}gsap.ticker.add(t=>LEN.raf(t*1000));gsap.ticker.lagSmoothing(0)}
})();
const toY=y=>{if(LEN)LEN.scrollTo(y,{immediate:true,force:true});else scrollTo(0,y)};
let MG=null;
function mgKill(){document.body.classList.remove('sg-in');if(MG){try{MG.ctx&&MG.ctx.revert()}catch(e){}removeEventListener('resize',MG.fit);MG=null}}
function mgGrain(){
  if(mgGrain.u)return mgGrain.u;
  try{const c=document.createElement('canvas');c.width=c.height=160;const x=c.getContext('2d'),d=x.createImageData(160,160);
    for(let i=0;i<d.data.length;i+=4){const v=Math.random()*255|0;d.data[i]=d.data[i+1]=d.data[i+2]=v;d.data[i+3]=Math.random()*70|0}
    x.putImageData(d,0,0);mgGrain.u=c.toDataURL()}catch(e){mgGrain.u=''}
  return mgGrain.u}
function mgSync(){
  if(!MG||!MG.L)return;const on=MG.vis!==false&&!MG.user&&!document.hidden,root=$('#mg');
  MG.L.forEach(t=>on?t.resume():t.pause());
  if(root){root.classList.toggle('mg-paused',!on);const pp=$('#mgpp');if(pp){pp.classList.toggle('is-paused',!!MG.user);pp.setAttribute('aria-label',MG.user?"Lancer l'animation":"Mettre l'animation en pause")}}
}
document.addEventListener('visibilitychange',mgSync);
function mgInit(){
  const root=$('#mg');if(!root)return;
  const fit=()=>{const r=root.getBoundingClientRect();root.style.setProperty('--top',Math.max(0,r.top+scrollY)+'px')};
  fit();addEventListener('resize',fit);
  const g=root.querySelector('.mg-grain');if(g){const u=mgGrain();if(u)g.style.backgroundImage=`url(${u})`}
  const pp=$('#mgpp');
  if(!window.gsap||!window.ScrollTrigger||!window.SplitText||RM.matches){root.classList.add('sg-static');if(pp)pp.hidden=true;MG={fit};return}
  gsap.registerPlugin(ScrollTrigger,SplitText,...(window.DrawSVGPlugin?[DrawSVGPlugin]:[]));
  MG={L:[],vis:true,user:false,fit};
  const st=MG;
  MG.ctx=gsap.context(()=>{
    const q1=s=>root.querySelector(s),qa=s=>[...root.querySelectorAll(s)];
    const split=SplitText.create(q1('.sg-h'),{type:'lines,chars',linesClass:'sg-line',charsClass:'sg-ch',mask:'lines'});
    const nums=qa('[data-n]');nums.forEach(n=>n.textContent='0');
    const tl=gsap.timeline({paused:true,defaults:{ease:'power3.out'}});
    tl.from('.sg-bg',{opacity:0,duration:1.2,ease:'power1.out'},0)
      .from('.sg-img',{opacity:0,y:26,filter:'brightness(.12) blur(6px)',duration:1.3},.2)
      .to('.sg-img',{filter:'brightness(1) blur(0px)',duration:1.4,ease:'power2.out'},1.05)
      .fromTo('.sg-led',{opacity:0},{keyframes:[{opacity:.9,duration:.06},{opacity:.15,duration:.08},{opacity:1,duration:.05},{opacity:.35,duration:.12},{opacity:1,duration:.5}],ease:'none'},.95)
      .from('.sg-led i',{scaleX:.2,duration:1,ease:'power3.out'},.95)
      .from('.sg-wash',{opacity:0,scale:.7,duration:1.6},1.05)
      .from('.sg-eye',{opacity:0,y:10,duration:.6},.6)
      .from(split.chars,{yPercent:110,duration:.9,stagger:.025,ease:'power4.out'},.75)
      .from('.sg-sub',{opacity:0,y:12,duration:.7},1.15)
      .from('.sg-dim path',window.DrawSVGPlugin?{drawSVG:'0%',duration:1.1,ease:'power2.inOut'}:{opacity:0,duration:.8},1.6)
      .from('.sg-dl',{opacity:0,y:6,duration:.5,stagger:.1},2)
      .from('.sg-hs',{opacity:0,scale:.6,duration:.6,stagger:.15,ease:'back.out(2)'},2.1)
      .from('.sg-specs>div,.sg-price,.sg-cta',{opacity:0,y:18,duration:.7,stagger:.08},1.7)
      .from('.mg-mq,.mg-pp',{opacity:0,duration:.8},2.2);
    nums.forEach(n=>{const o={v:0},to=+n.dataset.n;tl.to(o,{v:to,duration:1.4,ease:'power2.out',onUpdate:()=>n.textContent=Math.round(o.v)},1.8)});
    const im=q1('.sg-img');
    Promise.race([im.decode?im.decode().catch(()=>{}):Promise.resolve(),new Promise(r=>setTimeout(r,1500))]).then(()=>tl.play());
    const L=st.L,loop=v=>(L.push(v),v);
    loop(gsap.to('.sg-led',{'--glow':.78,duration:2.8,ease:'sine.inOut',yoyo:true,repeat:-1,delay:2.6}));
    loop(gsap.fromTo('.sg-sheen',{backgroundPosition:'130% 0'},{backgroundPosition:'-30% 0',duration:2.6,ease:'power2.inOut',repeat:-1,repeatDelay:3.5,delay:3}));
    loop(gsap.to('.sg-wash',{scale:1.08,opacity:.8,duration:5,ease:'sine.inOut',yoyo:true,repeat:-1,delay:2.6}));
    loop(gsap.to('.mg-track',{xPercent:-50,duration:34,ease:'none',repeat:-1}));
    qa('.sg-hs i').forEach((d,i)=>loop(gsap.fromTo(d,{'--ring':0},{'--ring':1,duration:2,ease:'power1.out',repeat:-1,delay:2.8+i*.5})));
    const mm=gsap.matchMedia();
    mm.add('(max-width:899px)',()=>{
      const rig=q1('.sg-rig'),unit=q1('.sg-unit');const span=()=>Math.max(0,(unit.offsetWidth-root.clientWidth)/2+14);
      gsap.set(rig,{x:()=>span()});
      loop(gsap.to(rig,{x:()=>-span(),duration:11,ease:'sine.inOut',yoyo:true,repeat:-1,delay:2.4,invalidateOnRefresh:true}));
    });
    gsap.timeline({scrollTrigger:{trigger:root,start:'top top',end:'bottom top',scrub:.6}})
      .to('.sg-unit',{scale:1.1,y:-30,ease:'none'},0)
      .to('.sg-head',{y:-50,opacity:.25,ease:'none'},0)
      .to('.sg-wash',{yPercent:-12,ease:'none'},0);
    ScrollTrigger.create({trigger:root,start:'top bottom',end:'bottom top',onToggle:s=>{st.vis=s.isActive;mgSync()}});
    ScrollTrigger.create({trigger:root,start:'top bottom',end:'bottom 70%',onToggle:s=>document.body.classList.toggle('sg-in',s.isActive)});
  },root);
  if(pp)pp.onclick=()=>{st.user=!st.user;mgSync()};
  mgSync();
}
'''

CSS = r'''
/* ===== Bannière plein écran : pièce signature ===== */
html.lenis{scroll-behavior:auto}
html.lenis,html.lenis body{height:auto}
.lenis:not(.lenis-autoToggle).lenis-stopped{overflow:clip}
.lenis [data-lenis-prevent]{overscroll-behavior:contain}
@property --glow{syntax:'<number>';inherits:true;initial-value:1}
@property --ring{syntax:'<number>';inherits:true;initial-value:0}
.sg{--ink:#F3F0E6;--sand:#D9B88F;--led:255,200,135;position:relative;overflow:hidden;isolation:isolate;color:var(--ink);background:#0f0d0b;
  display:flex;flex-direction:column;min-height:calc(100svh - var(--top,128px));margin-inline:calc(-1*max(16px,env(safe-area-inset-left,0px)));padding:18px 20px 0}
.sg-bg{position:absolute;inset:0;z-index:-1;overflow:hidden;pointer-events:none;
  background:radial-gradient(120% 70% at 50% 52%,#2c231b 0%,#191410 50%,#0d0b09 100%)}
.sg-wash{position:absolute;left:50%;top:44%;width:150%;max-width:1500px;aspect-ratio:2.2;translate:-50% -50%;
  background:radial-gradient(closest-side,rgba(var(--led),.16),rgba(var(--led),.05) 55%,rgba(0,0,0,0) 80%)}
.sg-vig{position:absolute;inset:0;background:radial-gradient(130% 90% at 50% 50%,rgba(0,0,0,0) 55%,rgba(0,0,0,.55) 100%)}
.mg-grain{position:absolute;inset:-60%;background-size:160px;opacity:.45;mix-blend-mode:overlay;animation:mg-grain .9s steps(6) infinite}
@keyframes mg-grain{0%{transform:translate(0,0)}20%{transform:translate(-6%,4%)}40%{transform:translate(5%,-3%)}60%{transform:translate(-3%,-6%)}80%{transform:translate(6%,5%)}100%{transform:translate(0,0)}}
.mg-paused .mg-grain{animation-play-state:paused}
/* en-tête */
.sg-head{position:relative;z-index:2}
.sg-eye{display:flex;align-items:center;gap:10px;margin:0 0 12px;font-size:.72rem;letter-spacing:.24em;text-transform:uppercase;color:var(--sand);font-weight:500}
.sg-dot{width:6px;height:6px;border-radius:50%;background:rgb(var(--led));box-shadow:0 0 12px 2px rgba(var(--led),.7)}
.sg-h{font-size:clamp(2.3rem,11vw,3.1rem);font-weight:300;line-height:.98;letter-spacing:-.035em;color:var(--ink);margin:0}
.sg-line{padding-bottom:.06em}
.sg-sub{margin:8px 0 0;color:rgba(243,240,230,.72);font-size:.92rem;letter-spacing:.02em}
/* scène */
.sg-stage{position:relative;flex:1 1 auto;min-height:200px;display:grid;align-items:center;margin-inline:-20px;overflow:visible}
.sg-rig{width:max-content;margin-inline:auto;padding:46px 0 62px;will-change:transform}
.sg-unit{position:relative;width:150vw;max-width:1100px;transform-origin:50% 60%}
.sg-img{position:relative;z-index:2;display:block;width:100%;height:auto;filter:drop-shadow(0 30px 30px rgba(0,0,0,.55))}
.sg-sheen{position:absolute;inset:0;z-index:3;pointer-events:none;mix-blend-mode:soft-light;
  background:linear-gradient(105deg,rgba(255,255,255,0) 35%,rgba(255,240,215,.75) 50%,rgba(255,255,255,0) 65%) no-repeat;background-size:250% 100%;background-position:130% 0;
  -webkit-mask:url(__CUT__) center/100% 100% no-repeat;mask:url(__CUT__) center/100% 100% no-repeat}
.sg-led{position:absolute;z-index:1;left:7%;width:88%;top:98%;height:4px;opacity:var(--glow);transform-origin:0 50%;rotate:-4.56deg}
.sg-led i{position:absolute;inset:0;border-radius:4px;background:rgb(255,226,180);box-shadow:0 0 10px 2px rgba(var(--led),.9),0 0 34px 8px rgba(var(--led),.55)}
.sg-led::after{content:"";position:absolute;left:-6%;right:-6%;top:0;height:clamp(90px,28vw,260px);
  background:radial-gradient(60% 100% at 50% 0%,rgba(var(--led),.55),rgba(var(--led),.22) 38%,rgba(var(--led),0) 72%);filter:blur(6px)}
.sg-led::before{content:"";position:absolute;left:8%;right:8%;top:-18px;height:30px;background:radial-gradient(50% 50% at 50% 100%,rgba(var(--led),.35),rgba(var(--led),0));filter:blur(4px)}
/* cotes */
.sg-dim{position:absolute;z-index:3;overflow:visible;fill:none;stroke:var(--sand);stroke-width:1;vector-effect:non-scaling-stroke;pointer-events:none}
.sg-dim path{vector-effect:non-scaling-stroke}
.sg-dim-w{left:0;right:0;width:100%;top:-46px;height:22px}
.sg-dim-h{right:-30px;top:0;height:100%;width:16px}
.sg-dl{position:absolute;z-index:4;font-size:.7rem;letter-spacing:.14em;color:var(--sand);background:#16120f;padding:2px 8px;white-space:nowrap}
.sg-dl b{font-weight:500;font-variant-numeric:tabular-nums}
.sg-dl-w{left:50%;top:-46px;translate:-50% 0;line-height:22px;padding-block:0}
.sg-dl-h{right:-30px;top:50%;translate:50% -50%;rotate:90deg}
/* points d'intérêt */
.sg-hs{position:absolute;z-index:5;left:var(--x);top:var(--y);width:0;height:0}
.sg-hs i{position:absolute;left:-5px;top:-5px;width:10px;height:10px;border-radius:50%;background:var(--ink);box-shadow:0 0 0 3px rgba(243,240,230,.25)}
.sg-hs i::after{content:"";position:absolute;inset:-4px;border-radius:50%;border:1px solid var(--ink);opacity:calc(1 - var(--ring));transform:scale(calc(1 + var(--ring)*2.2))}
.sg-hs span{position:absolute;left:0;white-space:nowrap;font-size:.72rem;font-weight:500;letter-spacing:.04em;padding:6px 10px;color:var(--ink);
  background:rgba(15,13,11,.6);border:1px solid rgba(243,240,230,.22);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px)}
.sg-hs span::before{content:"";position:absolute;left:0;width:1px;height:34px;background:linear-gradient(rgba(243,240,230,.7),rgba(243,240,230,.15))}
.sg-hs.up span{bottom:44px}.sg-hs.up span::before{top:100%}
.sg-hs.dn span{top:32px}.sg-hs.dn span::before{bottom:100%;height:22px}
.sg-hs.r span{left:auto;right:0}.sg-hs.r span::before{left:auto;right:0}
/* pied */
.sg-foot{position:relative;z-index:2;display:grid;gap:12px;padding-bottom:14px}
.sg-specs{display:grid;grid-template-columns:repeat(3,1fr);margin:0;border-top:1px solid rgba(243,240,230,.16);border-bottom:1px solid rgba(243,240,230,.16)}
.sg-specs>div{padding:8px 0 8px 12px;border-left:1px solid rgba(243,240,230,.16)}
.sg-specs>div:first-child{border-left:0;padding-left:0}
.sg-specs dt{font-size:.62rem;letter-spacing:.2em;text-transform:uppercase;color:rgba(243,240,230,.6)}
.sg-specs dd{margin:2px 0 0;font-size:1.05rem;font-weight:300}.sg-specs dd b{font-weight:400;font-size:1.35rem;font-variant-numeric:tabular-nums}
.sg-price{margin:0 0 10px;display:flex;align-items:baseline;gap:10px;flex-wrap:wrap}
.sg-price span{font-size:.72rem;letter-spacing:.16em;text-transform:uppercase;color:rgba(243,240,230,.6)}
.sg-price b{font-size:1.5rem;font-weight:500;color:var(--ink)}
.sg-price small{display:none;font-size:.78rem;color:rgba(243,240,230,.6)}
.sg-cta{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.sg-cta .btn{min-height:48px;padding-inline:8px;font-size:.8rem;text-align:center;white-space:nowrap}
.sg .sg-b1{background:var(--ink);color:#111213}
.sg .sg-b2{background:transparent;color:var(--ink);border:1px solid rgba(243,240,230,.5)}
.sg .sg-b2:hover{border-color:var(--ink);background:rgba(243,240,230,.08)}
.sg :focus-visible{outline-color:var(--sand)}
/* défilant + pause */
.mg-mq{margin:0 -20px;border-top:1px solid rgba(243,240,230,.12);overflow:hidden;padding:10px 0;flex:none;position:relative;z-index:2}
.mg-track{display:flex;width:max-content;will-change:transform}
.mg-track>div{display:flex;align-items:center;gap:18px;padding-right:18px}
.mg-track span{font-size:.72rem;letter-spacing:.22em;text-transform:uppercase;color:rgba(243,240,230,.66);white-space:nowrap}
.mg-track svg{width:10px;height:13px;fill:none;stroke:var(--sand);stroke-width:2;flex:none}
.mg-pp{position:absolute;top:10px;right:8px;z-index:6;width:44px;height:44px;display:grid;place-items:center;background:transparent;border:0;color:rgba(243,240,230,.75);cursor:pointer}
.mg-pp svg{width:15px;height:15px;fill:currentColor}.mg-pp .ic-play{display:none}
.mg-pp.is-paused .ic-play{display:block}.mg-pp.is-paused .ic-pause{display:none}
.mg-pp:hover{color:var(--ink)}.mg-pp[hidden]{display:none}
#waf{transition:opacity .3s,visibility .3s}
body.sg-in #waf{opacity:0;visibility:hidden}
/* mouvement réduit / sans JS : tout visible, cadré au centre */
.sg-static .sg-unit{width:100vw;max-width:1100px}
@media (min-width:600px) and (max-width:899px){.sg-unit{width:130vw}.sg-h{font-size:clamp(3rem,9vw,4.4rem)}}
@media (min-width:900px){
  .sg{display:grid;grid-template-columns:1fr 1fr;grid-template-rows:auto 1fr auto auto;margin-inline:calc(-1*max(16px,env(safe-area-inset-left,0px)));padding:clamp(28px,4vw,56px) clamp(32px,5vw,80px) 0;
    min-height:calc(100svh - var(--top,104px))}
  .sg-head{grid-column:1/-1;grid-row:1;display:grid;grid-template-columns:1fr auto;align-items:end;gap:4px 40px}
  .sg-eye{grid-column:1/-1}
  .sg-h{font-size:clamp(3rem,6vw,5.6rem);white-space:nowrap}
  .sg-sub{margin:0 0 .6em;text-align:right}
  .sg-stage{grid-column:1/-1;grid-row:2;margin:0;min-height:300px}
  .sg-rig{padding:70px 40px 90px}
  .sg-unit{width:min(62vw,1000px,calc((100svh - var(--top,104px) - 380px)*3.4))}
  .sg-foot{grid-column:1/-1;grid-row:3;grid-template-columns:auto 1fr;align-items:end;gap:40px;padding-bottom:28px}
  .sg-specs{min-width:420px;border-bottom:0}
  .sg-buy{display:flex;align-items:end;justify-content:flex-end;gap:32px}
  .sg-price{margin:0;flex-direction:column;gap:2px;align-items:flex-end;text-align:right}
  .sg-price small{flex-basis:auto;display:block}
  .sg-cta{display:flex}.sg-cta .btn{padding-inline:26px;font-size:.9rem}
  .sg-hs.dn span{top:40px}.sg-hs.dn span::before{height:30px}
  .mg-mq{grid-column:1/-1;grid-row:4;margin:0 calc(-1*clamp(32px,5vw,80px))}
  .mg-pp{top:16px;right:16px}
  .sg-hs span{font-size:.78rem;padding:7px 12px}
}
@media (max-width:899px) and (max-height:790px){.sg{padding-top:12px}.sg-eye{margin-bottom:8px}.sg-h{font-size:2.05rem}.sg-sub{font-size:.85rem}.sg-rig{padding:38px 0 54px}.sg-unit{width:140vw}.sg-specs dd b{font-size:1.15rem}.sg-price{margin-bottom:8px}.sg-price b{font-size:1.3rem}.mg-mq{padding:8px 0}}
@media (max-width:380px){.sg-cta{grid-template-columns:auto 1fr;gap:8px}.sg-cta .btn{font-size:.74rem;padding-inline:10px}}
@media (prefers-reduced-motion:reduce){.mg-grain{animation:none}}
'''.replace('__CUT__', CUT)

SLIDES = []


def make_assets(repo):
    os.makedirs(repo + '/vendor', exist_ok=True)
    for f in ['gsap.min.js', 'ScrollTrigger.min.js', 'SplitText.min.js', 'DrawSVGPlugin.min.js']:
        shutil.copy(f'{VEND}/GSAP/dist/{f}', f'{repo}/vendor/{f}')
    shutil.copy(f'{VEND}/out/lenis.min.js', f'{repo}/vendor/lenis.min.js')
    from scipy import ndimage
    im = Image.open(SRC_ORIG).convert('RGB').crop((30, 400, 1230, 800))
    a = np.asarray(im).astype(float); br = a.mean(2); sat = a.max(2) - a.min(2)
    obj = (br < 150) & (sat / np.maximum(br, 1) > 0.42)
    lab, n = ndimage.label(obj); sizes = ndimage.sum(obj, lab, range(1, n + 1)); obj = lab == (np.argmax(sizes) + 1)
    obj = ndimage.binary_closing(obj, iterations=3); obj = ndimage.binary_fill_holes(obj)
    obj = ndimage.binary_opening(obj, iterations=3); obj = ndimage.binary_erosion(obj, iterations=1)
    al = np.asarray(Image.fromarray((obj * 255).astype('uint8')).filter(ImageFilter.GaussianBlur(1.1))).astype(float)
    o = Image.fromarray(np.dstack([a, al]).astype('uint8'), 'RGBA')
    o = o.crop(Image.fromarray((al > 10).astype('uint8') * 255).getbbox())
    o = o.resize((o.width * 2, o.height * 2), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
    os.makedirs(os.path.join(repo, 'images/hero'), exist_ok=True)
    o.save(os.path.join(repo, CUT), 'WEBP', quality=88, method=6)


SCRIPTS = ('<script src="vendor/gsap.min.js"></script>\n<script src="vendor/ScrollTrigger.min.js"></script>\n'
           '<script src="vendor/SplitText.min.js"></script>\n<script src="vendor/DrawSVGPlugin.min.js"></script>\n'
           '<script src="vendor/lenis.min.js"></script>\n')


def patch(m, c, s):
    for a, b in [('scrollTo(0,0)', 'toY(0)'), ('scrollTo(0,k)', 'toY(k)'), ('scrollTo(0,y)', 'toY(y)')]:
        assert a in m, a; m = m.replace(a, b)
    i = m.index(OLD_HERO_START); j = m.index('</section>', i) + len('</section>')
    m = m[:i] + HERO + m[j:]
    k = m.index('function perks(')
    m = m[:k] + HELPERS.lstrip('\n') + m[k:]
    m = m.replace("function bind(h){\n", "function bind(h){\n  if(h==='accueil')mgInit();\n", 1)
    m = m.replace("function route(){\n", "function route(){\n  mgKill();\n", 1)
    m = m.replace('<div id="layer"></div>', '<div id="layer" data-lenis-prevent></div>', 1)
    m = m.replace('<script type="application/json" id="seed">', SCRIPTS + '<script type="application/json" id="seed">', 1)
    for t in ["mgInit();", "mgKill();", "data-lenis-prevent", "vendor/gsap.min.js", "else scrollTo(0,y)"]:
        assert t in m, t
    return m, c + CSS, s
