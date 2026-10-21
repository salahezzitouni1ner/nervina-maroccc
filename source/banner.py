# Bannière animée de l'accueil : patch appliqué à modele.html / styles.css / store.json par build.py
OLD_HERO_START='  return `<section class="hero">'

HERO='''  const sl=heroSlides(),c0=sl[0];
  return `<section class="mb" id="mb" aria-roledescription="carrousel" aria-label="Nos pièces en situation">
  <div class="mb-media" aria-hidden="true">${sl.map((s,i)=>`<div class="mb-slide${i?'':' on'}"><img src="${IMGURL(s.img)}" alt="" decoding="async"${i?' loading="lazy"':' fetchpriority="high"'} style="object-position:${esc(s.pos||'50% 50%')}"></div>`).join('')}<div class="mb-shade"></div></div>
  <div class="mb-in">
    <div class="mb-txt">
      <p class="eyebrow mb-r" style="--d:0"><svg class="mb-arch" viewBox="0 0 24 30" aria-hidden="true"><path d="M3 29V12a9 9 0 0 1 18 0v17"/></svg>Mobilier · Décoration · Menuiserie</p>
      <h1><span class="mb-l"><span class="mb-r" style="--d:1">${esc(st.heroTitle1)}</span></span> <span class="mb-l"><em class="mb-r" style="--d:2">${esc(st.heroTitle2)}</em></span></h1>
      <p class="lead mb-r" style="--d:3">${esc(st.heroLead)}</p>
      <div class="mb-cta mb-r" style="--d:4"><a class="btn mb-b1" href="#catalogue">Voir le catalogue</a><a class="btn mb-b2" href="#contact">Nous contacter</a></div>
    </div>
    ${c0?`<div class="mb-foot mb-r" style="--d:5">
      <a class="mb-cap" id="mbcap" href="#p-${esc(c0.p.id)}">${mbCap(c0)}</a>
    </div>`:''}
      ${sl.length>1?`<div class="mb-ctl mb-r" style="--d:6"><div class="mb-bars">${sl.map((s,i)=>`<button class="mb-bar" data-go="${i}" aria-label="Photo ${i+1} sur ${sl.length} : ${esc(s.p.title)}"${i?'':' aria-current="true"'}><i></i></button>`).join('')}</div>
      <button class="mb-pp" id="mbpp" aria-label="Mettre l'animation en pause"><svg viewBox="0 0 20 20" aria-hidden="true"><path class="ic-pause" d="M6 4h3v12H6zM11 4h3v12h-3z"/><path class="ic-play" d="M6 4l10 6-10 6z"/></svg></button></div>`:''}
  </div></section>`+`'''

HELPERS=r'''
function heroSlides(){
  const L=(S.settings.heroSlides||[]).map(s=>{const p=prod(s.p);return p&&!p.hidden&&p.imgs&&p.imgs.length?{p,img:p.imgs[Math.min(s.i||0,p.imgs.length-1)],pos:s.pos}:null}).filter(Boolean);
  if(L.length)return L;
  const f=prod(S.settings.featured)||vis()[0];return f&&f.imgs&&f.imgs[0]?[{p:f,img:f.imgs[0]}]:[]}
const mbCap=s=>`<span class="mb-k">${esc(colName(s.p.col))}</span><span class="mb-n">${esc(s.p.title)}</span><span class="mb-p">${MAD(s.p.price)} <span class="mb-go">Voir la pièce <svg viewBox="0 0 16 10" aria-hidden="true"><path d="M0 5h14M10 1l4 4-4 4"/></svg></span></span>`;
let MB=null;
function mbInit(){
  const root=$('#mb');if(!root)return;
  const sl=heroSlides(),slides=[...root.querySelectorAll('.mb-slide')],bars=[...root.querySelectorAll('.mb-bar')],cap=$('#mbcap'),pp=$('#mbpp');
  const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  const st={i:0,user:reduce,hover:false,hidden:document.hidden};
  MB=st;
  const paused=()=>st.user||st.hover||st.hidden;
  const sync=()=>{root.classList.toggle('paused',paused());if(pp){pp.setAttribute('aria-label',st.user?"Lancer l'animation":"Mettre l'animation en pause");pp.classList.toggle('is-paused',st.user)}};
  const go=n=>{
    if(!slides.length)return;n=(n+slides.length)%slides.length;if(n===st.i&&slides[n].classList.contains('on'))return;
    const prev=st.i;st.i=n;
    slides.forEach((s,k)=>{s.classList.toggle('on',k===n);s.classList.toggle('was',k===prev&&k!==n)});
    const im=slides[n].querySelector('img');im.loading='eager';
    const nx=slides[(n+1)%slides.length];if(nx){nx.querySelector('img').loading='eager'}
    bars.forEach((b,k)=>{b.classList.toggle('done',k<n);b.classList.remove('run');k===n?b.setAttribute('aria-current','true'):b.removeAttribute('aria-current')});
    void root.offsetWidth;if(bars[n])bars[n].classList.add('run');
    if(cap){cap.classList.add('out');setTimeout(()=>{cap.href='#p-'+sl[n].p.id;cap.innerHTML=mbCap(sl[n]);cap.classList.remove('out')},reduce?0:260)}
  };
  bars.forEach(b=>{b.onclick=()=>go(+b.dataset.go);b.addEventListener('animationend',e=>{if(e.animationName==='mb-tick'&&b.classList.contains('run'))go(st.i+1)})});
  if(pp)pp.onclick=()=>{st.user=!st.user;sync()};
  root.addEventListener('mouseenter',()=>{st.hover=true;sync()});root.addEventListener('mouseleave',()=>{st.hover=false;sync()});
  root.addEventListener('focusin',()=>{st.hover=true;sync()});root.addEventListener('focusout',e=>{if(!root.contains(e.relatedTarget)){st.hover=false;sync()}});
  let x0=null;root.addEventListener('touchstart',e=>{x0=e.touches[0].clientX},{passive:true});
  root.addEventListener('touchend',e=>{if(x0==null)return;const dx=e.changedTouches[0].clientX-x0;x0=null;if(Math.abs(dx)>45)go(st.i+(dx<0?1:-1))},{passive:true});
  root.addEventListener('keydown',e=>{if(e.target.closest('.mb-bars')&&(e.key==='ArrowRight'||e.key==='ArrowLeft')){e.preventDefault();go(st.i+(e.key==='ArrowRight'?1:-1));bars[st.i]&&bars[st.i].focus()}});
  if(bars[0])bars[0].classList.add('run');
  sync();
}
document.addEventListener('visibilitychange',()=>{if(MB&&$('#mb')){MB.hidden=document.hidden;$('#mb').classList.toggle('paused',MB.user||MB.hover||MB.hidden)}});
'''

CSS=r'''
/* ===== Bannière animée de l'accueil ===== */
.mb{--mb-dur:6.5s;--mb-ink:#F3F0E6;--mb-sand:#D9B88F;position:relative;overflow:hidden;margin-top:24px;min-height:clamp(520px,calc(100svh - 200px),660px);
  display:grid;color:var(--mb-ink);background:#111213;border-radius:2px;isolation:isolate}
.mb-media,.mb-slide,.mb-shade{position:absolute;inset:0}
.mb-slide{opacity:0;transition:opacity 1.3s cubic-bezier(.4,0,.2,1);z-index:0}
.mb-slide.on{opacity:1;z-index:1}.mb-slide.was{z-index:0;opacity:0}
.mb-slide img{width:100%;height:100%;object-fit:cover;transform:scale(1.02);will-change:transform}
.mb-slide.on img{animation:mb-kb calc(var(--mb-dur) + 1.6s) linear forwards}
@keyframes mb-kb{from{transform:scale(1.02) translate3d(0,0,0)}to{transform:scale(1.11) translate3d(-1.2%,-.8%,0)}}
.mb-shade{z-index:2;background:linear-gradient(90deg,rgba(17,18,19,.86) 0%,rgba(17,18,19,.62) 38%,rgba(17,18,19,.12) 72%,rgba(17,18,19,0) 100%),
  linear-gradient(0deg,rgba(17,18,19,.7) 0%,rgba(17,18,19,0) 34%)}
.mb-in{position:relative;z-index:3;display:grid;grid-template-rows:1fr auto;gap:28px;padding:clamp(28px,4.2vw,56px)}
.mb-txt{align-self:center;max-width:640px}
.mb h1{font-size:clamp(2.1rem,4.3vw,3.4rem)}
.mb .eyebrow{color:var(--mb-sand);display:flex;align-items:center;gap:12px}
.mb-arch{width:18px;height:23px;flex:none;fill:none;stroke:var(--mb-sand);stroke-width:1.6;stroke-dasharray:60;stroke-dashoffset:60;animation:mb-draw 1.4s .35s cubic-bezier(.6,0,.2,1) forwards}
@keyframes mb-draw{to{stroke-dashoffset:0}}
.mb h1{color:var(--mb-ink)}.mb h1 em{font-style:normal;font-weight:500;color:var(--mb-sand)}
.mb-l{display:inline-block;overflow:hidden;vertical-align:top;padding-bottom:.08em;margin-bottom:-.08em}
.mb-l>.mb-r{display:inline-block}
.mb .lead{color:rgba(243,240,230,.86);max-width:46ch;margin:18px 0 26px;font-size:1.05rem}
.mb-cta{display:flex;gap:12px;flex-wrap:wrap}
.mb .mb-b1{background:var(--mb-ink);color:#111213}
.mb .mb-b2{background:transparent;color:var(--mb-ink);border:1px solid rgba(243,240,230,.55)}
.mb .mb-b2:hover{border-color:var(--mb-ink);background:rgba(243,240,230,.08)}
.mb :focus-visible{outline-color:var(--mb-sand)}
/* entrée du texte, une seule fois au chargement */
.mb-r{opacity:0;transform:translateY(22px);animation:mb-rise .95s cubic-bezier(.2,.7,.2,1) forwards;animation-delay:calc(var(--d,0)*110ms + 120ms)}
.mb-l>.mb-r{transform:translateY(105%);opacity:1}
@keyframes mb-rise{to{opacity:1;transform:none}}
/* légende + contrôles */
.mb-foot{display:flex;align-items:flex-end;justify-content:space-between;gap:20px 32px;flex-wrap:wrap;border-top:1px solid rgba(243,240,230,.22);padding-top:20px}
.mb-cap{display:grid;gap:2px;text-decoration:none;color:var(--mb-ink);min-width:0;transition:opacity .26s,transform .26s}
.mb-cap.out{opacity:0;transform:translateY(8px)}
.mb-k{font-size:.72rem;letter-spacing:.2em;text-transform:uppercase;color:var(--mb-sand)}
.mb-n{font-size:1.05rem;font-weight:500;line-height:1.35}
.mb-p{font-size:.9rem;color:rgba(243,240,230,.8);display:flex;gap:14px;align-items:center;flex-wrap:wrap}
.mb-go{display:inline-flex;align-items:center;gap:8px;color:var(--mb-ink);border-bottom:1px solid rgba(243,240,230,.4);padding-bottom:1px}
.mb-go svg{width:16px;height:10px;fill:none;stroke:currentColor;stroke-width:1.4;transition:transform .25s}
.mb-cap:hover .mb-go svg{transform:translateX(4px)}
.mb-ctl{display:flex;align-items:center;gap:14px;position:absolute;right:clamp(28px,4.2vw,56px);bottom:clamp(28px,4.2vw,56px)}
.mb-foot{padding-right:420px}
.mb-bars{display:flex;gap:6px}
.mb-bar{width:44px;height:44px;padding:0;background:none;border:0;cursor:pointer;display:grid;align-items:center}
.mb-bar i{display:block;height:2px;background:rgba(243,240,230,.28);position:relative;overflow:hidden}
.mb-bar i::after{content:"";position:absolute;inset:0;background:var(--mb-ink);transform:scaleX(0);transform-origin:left}
.mb-bar.done i::after{transform:scaleX(1)}
.mb-bar.run i::after{animation:mb-fill var(--mb-dur) linear forwards}
.mb-bar.run i{animation:mb-tick var(--mb-dur) linear forwards}
@keyframes mb-fill{to{transform:scaleX(1)}}@keyframes mb-tick{to{opacity:1}}
.mb-bar:hover i{background:rgba(243,240,230,.5)}
.mb-pp{width:44px;height:44px;display:grid;place-items:center;background:transparent;border:1px solid rgba(243,240,230,.4);color:var(--mb-ink);cursor:pointer;border-radius:2px}
.mb-pp:hover{border-color:var(--mb-ink)}
.mb-pp svg{width:16px;height:16px;fill:currentColor}.mb-pp .ic-play{display:none}
.mb-pp.is-paused .ic-play{display:block}.mb-pp.is-paused .ic-pause{display:none}
.mb.paused .mb-slide.on img,.mb.paused .mb-bar.run i,.mb.paused .mb-bar.run i::after{animation-play-state:paused}
@media(max-width:700px){
  .mb{min-height:clamp(560px,calc(100svh - 150px),720px);margin-top:16px;margin-inline:-16px;border-radius:0}
  .mb-in{padding:64px 20px 24px;gap:22px}
  .mb-txt{align-self:end}
  .mb-shade{background:linear-gradient(0deg,rgba(17,18,19,.95) 0%,rgba(17,18,19,.86) 50%,rgba(17,18,19,.5) 76%,rgba(17,18,19,.35) 100%)}
  .mb .lead{font-size:.98rem;margin:16px 0 22px}
  .mb-foot{padding-top:14px;padding-right:0}
  .mb-ctl{top:8px;left:20px;right:12px;bottom:auto;gap:8px}
  .mb-bars{flex:1;gap:4px}.mb-bar{width:auto;flex:1}
  .mb-pp{border-color:transparent}
}
@media(prefers-reduced-motion:reduce){
  .mb-r,.mb-l>.mb-r{animation:none;opacity:1;transform:none}
  .mb-arch{animation:none;stroke-dashoffset:0}
  .mb-slide.on img,.mb-bar.run i,.mb-bar.run i::after{animation:none}
  .mb-slide{transition:opacity .2s}
}
'''

SLIDES=[
 {"p":"table-basse-amazonica","i":1,"pos":"60% 55%"},
 {"p":"table-basse-ronde-luxe","i":1,"pos":"55% 60%"},
 {"p":"table-a-manger-ronde-4-chaises-mdf-noyer","i":1,"pos":"60% 55%"},
 {"p":"table-de-chevet-cloud-noyer","i":3,"pos":"62% 50%"},
 {"p":"console-arche-miroirs-organiques","i":0,"pos":"50% 88%"},
 {"p":"meuble-tv-sur-pieds-noyer-creme","i":2,"pos":"55% 55%"},
]

def patch(m,c,s):
    i=m.index(OLD_HERO_START); j=m.index('</section>',i)+len('</section>')
    m=m[:i]+HERO+m[j:]
    k=m.index('function perks(')
    m=m[:k]+HELPERS.lstrip('\n')+m[k:]
    m=m.replace("function bind(h){\n","function bind(h){\n  if(h==='accueil')mbInit();\n",1)
    assert "mbInit();" in m
    s['settings'].setdefault('heroSlides',SLIDES)
    return m,c+CSS,s
