
/* === FRONTEND-SLIDES / SLIDEPRESENTATION CONTROLLER ADAPTATION === */
class SlidePresentation{
 constructor(){this.slides=document.querySelectorAll('.slide');this.currentSlide=0;this.stage=document.getElementById('deckStage');this.setupStageScale();this.setupKeyboardNav();this.setupTouchNav();this.setupWheelNav();this.slides.forEach(s=>s.querySelectorAll('.reveal').forEach((e,i)=>e.style.transitionDelay=`${.08+i*.12}s`));this.showSlide(Number(location.hash.slice(1)||1)-1);}
 setupStageScale(){const scale=()=>{const factor=Math.min(innerWidth/1920,innerHeight/1080);this.stage.style.transform=`translate(${(innerWidth-1920*factor)/2}px,${(innerHeight-1080*factor)/2}px) scale(${factor})`};scale();addEventListener('resize',scale)}
 setupKeyboardNav(){addEventListener('keydown',e=>{if(e.target.closest('button,a,[contenteditable="plaintext-only"],[contenteditable="true"],input,textarea'))return;if(['ArrowRight','ArrowDown','PageDown',' '].includes(e.key)){e.preventDefault();this.showSlide(this.currentSlide+1)}if(['ArrowLeft','ArrowUp','PageUp'].includes(e.key)){e.preventDefault();this.showSlide(this.currentSlide-1)}if(e.key==='Home')this.showSlide(0);if(e.key==='End')this.showSlide(this.slides.length-1)})}
 setupTouchNav(){let start=null;addEventListener('touchstart',e=>{start=e.target.closest('[contenteditable]')?null:e.changedTouches[0].clientX},{passive:true});addEventListener('touchend',e=>{if(start===null)return;const delta=e.changedTouches[0].clientX-start;if(Math.abs(delta)>60)this.showSlide(this.currentSlide+(delta<0?1:-1))},{passive:true})}
 setupWheelNav(){let last=0;addEventListener('wheel',e=>{if(e.target.closest('[contenteditable]'))return;if(Date.now()-last>700&&Math.abs(e.deltaY)>25){this.showSlide(this.currentSlide+(e.deltaY>0?1:-1));last=Date.now()}},{passive:true})}
 showSlide(index){this.currentSlide=Math.max(0,Math.min(index,this.slides.length-1));this.slides.forEach((s,i)=>{s.classList.toggle('active',i===this.currentSlide);s.classList.toggle('visible',i===this.currentSlide);s.setAttribute('aria-hidden',i!==this.currentSlide)});document.getElementById('count').textContent=`${String(this.currentSlide+1).padStart(2,'0')} / 06`;history.replaceState(null,'',`#${this.currentSlide+1}`)}
}
window.deck=new SlidePresentation();
/* === SAME-ORIGIN YEBISU VIEWER BRIDGE === */
const nativeShow=deck.showSlide.bind(deck);deck.showSlide=function(index){nativeShow(index);if(parent!==window)parent.postMessage({type:'yebisu-page',index:this.currentSlide,total:this.slides.length},location.origin)};
addEventListener('message',e=>{if(e.source===parent&&e.origin===location.origin&&e.data?.type==='yebisu-slide'&&Number.isInteger(e.data.index))deck.showSlide(e.data.index)});deck.showSlide(deck.currentSlide);
document.getElementById('prev').onclick=()=>deck.showSlide(deck.currentSlide-1);document.getElementById('next').onclick=()=>deck.showSlide(deck.currentSlide+1);
const moods=[['答えを出さない、<br>読書もある。','詩や短いエッセイから。<br>ひとつの段落に、少し長くとどまる。'],['帰り道から、<br>知らない街へ。','旅の記録や物語から。<br>いつもの景色に、新しい窓をひらく。'],['知らなかったことが、<br>明日の種になる。','暮らしや自然、ものづくりの本から。<br>小さな「やってみたい」を見つける。']];
let editor;
document.querySelectorAll('[data-mood]').forEach(b=>b.onclick=()=>{document.querySelectorAll('[data-mood]').forEach(x=>{x.classList.toggle('selected',x===b);x.setAttribute('aria-selected',x===b)});document.querySelectorAll('[data-book]').forEach(x=>x.classList.toggle('chosen',x.dataset.book===b.dataset.mood));const m=moods[Number(b.dataset.mood)],t=document.getElementById('mood-text');t.innerHTML=`<h3>${m[0]}</h3><p>${m[1]}</p>`;editor?.decorate(t,`mood-${b.dataset.mood}`);t.classList.remove('swap');void t.offsetWidth;t.classList.add('swap')});
/* === POST-DRAFT TEXT EDITING / ORIGINAL DEFAULT AFFORDANCE ===
   Text-only edits keep the authored line breaks, SVGs and CSS intact.
   Text is restored with textContent, never interpreted as saved HTML. */
class InlineEditor {
 constructor(){
  this.isActive=false;this.storageKey=`frontend-slides:night-library:v1:${location.pathname}`;
  this.status=document.getElementById('editStatus');
  try{this.saved={...JSON.parse(document.getElementById('savedEdits').textContent||'{}'),...JSON.parse(localStorage.getItem(this.storageKey)||'{}')}}catch{this.saved={}}
  document.querySelectorAll('.slide').forEach((s,i)=>this.decorate(s,`slide-${i+1}`));
  this.decorate(document.getElementById('mood-text'),`mood-${document.querySelector('[data-mood][aria-selected="true"]').dataset.mood}`);
  const hot=document.querySelector('.edit-hotzone'),toggle=document.getElementById('editToggle');let hide;
  const show=()=>{clearTimeout(hide);toggle.classList.add('show')};
  const later=()=>{hide=setTimeout(()=>toggle.classList.remove('show'),400)};
  hot.addEventListener('mouseenter',show);hot.addEventListener('mouseleave',later);hot.addEventListener('click',()=>this.toggleEditMode());
  toggle.addEventListener('mouseenter',show);toggle.addEventListener('mouseleave',later);toggle.onclick=()=>this.toggleEditMode();
  document.getElementById('exportDeck').onclick=()=>this.exportFile();
  addEventListener('keydown',e=>{if(e.target.closest('[contenteditable],input,textarea')){if(e.key==='Escape'){e.target.blur();this.toggleEditMode(false)}else if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='s'){e.preventDefault();this.exportFile()}return}if(e.key.toLowerCase()==='e'&&!e.ctrlKey&&!e.metaKey&&!e.altKey){e.preventDefault();this.toggleEditMode()}if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='s'){e.preventDefault();this.exportFile()}});
 }
 decorate(root,prefix){
  let n=0;const walk=document.createTreeWalker(root,NodeFilter.SHOW_TEXT),nodes=[];
  while(walk.nextNode()){const t=walk.currentNode;if(!t.textContent.trim()||t.parentElement.closest('svg,button,a,[data-edit-id]'))continue;if(!prefix.startsWith('mood-')&&t.parentElement.closest('#mood-text'))continue;nodes.push(t)}
  for(const t of nodes){const span=document.createElement('span');span.className='edit-run';span.dataset.editId=`${prefix}-${n++}`;span.textContent=t.textContent;t.replaceWith(span)}
  root.querySelectorAll('[data-edit-id]').forEach(el=>{const id=el.dataset.editId;if(Object.hasOwn(this.saved,id))el.textContent=this.saved[id];el.setAttribute('spellcheck','false');if(this.isActive)el.setAttribute('contenteditable','plaintext-only');else el.removeAttribute('contenteditable');if(el.dataset.editBound)return;el.dataset.editBound='true';el.addEventListener('input',()=>{this.saved[id]=el.textContent;try{localStorage.setItem(this.storageKey,JSON.stringify(this.saved));this.status.textContent='このブラウザーに保存済み'}catch{this.status.textContent='自動保存不可：HTMLを保存してください'}})})
 }
 toggleEditMode(force){this.isActive=typeof force==='boolean'?force:!this.isActive;document.body.classList.toggle('editing',this.isActive);document.getElementById('editToggle').classList.toggle('active',this.isActive);document.getElementById('editToggle').setAttribute('aria-pressed',this.isActive);document.querySelectorAll('[data-edit-id]').forEach(el=>{if(this.isActive)el.setAttribute('contenteditable','plaintext-only');else el.removeAttribute('contenteditable')});this.status.textContent=this.isActive?'本文をクリックして編集。Escで終了。':''}
 exportFile(){const copy=document.documentElement.cloneNode(true);copy.querySelector('body').classList.remove('editing');copy.querySelectorAll('[contenteditable]').forEach(el=>el.removeAttribute('contenteditable'));copy.querySelectorAll('[data-edit-bound]').forEach(el=>el.removeAttribute('data-edit-bound'));copy.querySelector('#editToggle').classList.remove('active','show');copy.querySelector('#editToggle').setAttribute('aria-pressed','false');copy.querySelector('#editStatus').textContent='';copy.querySelector('#savedEdits').textContent=JSON.stringify(this.saved).replaceAll('<','\\u003c');const a=document.createElement('a');a.href=URL.createObjectURL(new Blob(['<!doctype html>\n'+copy.outerHTML],{type:'text/html;charset=utf-8'}));a.download='night-library-edited.html';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000);this.status.textContent='HTMLの保存を開始しました'}
}
editor=new InlineEditor();
