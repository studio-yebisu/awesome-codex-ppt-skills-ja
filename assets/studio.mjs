import {renderSlide,validateDeck,xml} from './slide-renderer.mjs';
const $=selector=>document.querySelector(selector);
const labels={business:'社内提案',pitch:'企画・ピッチ',education:'教材',research:'技術・登壇',product:'製品説明',motion:'動くスライド'};
let decks=[],skills=[],current=null,index=0,playing=false,raf=0,elapsed=0,last=0,trigger=null,toastTimer;
const dialog=$('#deck-dialog');
function toast(message){$('#toast').textContent=message;$('#toast').classList.add('visible');clearTimeout(toastTimer);toastTimer=setTimeout(()=>$('#toast').classList.remove('visible'),2600)}
function gallery(filter='all'){
  const visible=decks.filter(d=>filter==='all'||d.category===filter);
  $('#deck-grid').innerHTML=visible.map((d,i)=>`<article class="deck-card" style="animation-delay:${i*35}ms"><button type="button" class="deck-open" data-open-deck="${xml(d.id)}" aria-label="${xml(d.title)}の作例を再生">${renderSlide(d,0,{label:false})}<span class="open-affordance">▶ <span>作例を再生</span> ↗</span></button><div class="deck-meta"><span>${xml(labels[d.category])} / ${xml(d.style)}</span><span>4 SLIDES · ${d.slides.reduce((sum,s)=>sum+(s.duration||6),0)} SEC</span></div><h3><button type="button" data-open-deck="${xml(d.id)}">${xml(d.title)}</button></h3><p class="deck-description">${xml(d.description)}</p><div class="deck-info"><span>SVG + PPTX</span><span>${xml(d.font)}</span><span>CC0</span></div></article>`).join('');
  $('#filter-status').textContent=`${filter==='all'?'すべて':labels[filter]}：${visible.length}件の作例`;
}
function showSkills(){
  $('#skill-grid').innerHTML=skills.filter(s=>s.upstream).map(s=>`<article class="skill-card"><div class="skill-card-head"><span class="skill-symbol" aria-hidden="true">${xml(s.symbol)}</span><span class="license-chip">${xml(s.license)}</span></div><h3>${xml(s.title)}</h3><p>${xml(s.description)}</p><p class="skill-origin">派生元：<a href="${xml(s.upstream.url)}" target="_blank" rel="noopener noreferrer">${xml(s.upstream.repository)}</a><br>日本語改修：Studio Yebisu / ${xml(s.id)}</p><div class="skill-bottom"><a href="downloads/${xml(s.id)}.zip" download>スキルを入手 ↓</a><a href="skills/${xml(s.id)}/CHANGES.md">改修内容 ↗</a></div></article>`).join('');
}
function showEngines(upstreams){
  const choices=[['slidevjs/slidev','Slidev','コードと図解に強い、Web発表','MarkdownとVueで組み立てる、開発者向けのプレゼンテーション環境。テーマや発表者モードを使いたいときに。','https://sli.dev/guide/'],['marp-team/marp','Marp','Markdownから、配れる資料へ','文章中心の原稿を、PDFやスライドへ。形式を揃えた技術資料や定期的な報告を、テキストで管理できます。','https://marp.app/'],['hakimel/reveal.js','reveal.js','ブラウザで、発表を組み立てる','HTMLのスライドに、ページ移動や発表者ノートを追加。Webの表現を活かした発表の制作基盤です。','https://revealjs.com/'],['gitbrent/PptxGenJS','PptxGenJS','文字と図形を、PowerPointへ','JavaScriptからPPTXを作るライブラリ。配布スキルの簡易exporterでも、ネイティブな文字と図形の出力に使っています。','https://gitbrent.github.io/PptxGenJS/']];
  $('#engine-grid').innerHTML=choices.map(([repo,title,lead,description,guide])=>{const u=upstreams.find(u=>u.repository===repo);return `<article class="skill-card"><div class="skill-card-head"><span>${xml(title)}</span><span class="license-chip">${xml(u.github_license)} · ★ ${u.stars.toLocaleString('ja-JP')}</span></div><h3>${xml(lead)}</h3><p>${xml(description)}</p><div class="skill-bottom"><a href="${guide}" target="_blank" rel="noopener noreferrer">公式の導入案内 ↗</a><a href="${u.url}" target="_blank" rel="noopener noreferrer">GitHub ↗</a><a href="licenses.html">利用条件 ↗</a></div></article>`}).join('');
}
function stop(){playing=false;cancelAnimationFrame(raf);raf=0;$('#player-play').innerHTML='▶ <span>再生</span>';$('#player-play').setAttribute('aria-label','自動再生する')}
function updateSlide(animate=true){
  $('#player-stage').innerHTML=renderSlide(current,index,{animate:animate&&!matchMedia('(prefers-reduced-motion: reduce)').matches});
  $('#player-counter').textContent=`${index+1} / ${current.slides.length}`;
  $('#player-prev').disabled=index===0;$('#player-next').disabled=index===current.slides.length-1;
  $('#note-title').textContent=`${index+1}. ${current.slides[index].title}`;
  $('#note-content').textContent=current.slides[index].notes||'';
  $('#player-progress').style.width='0%';
  for(const button of $('#slide-selector').querySelectorAll('button'))button.setAttribute('aria-current',String(Number(button.dataset.slide)===index));
}
function move(target){stop();index=Math.max(0,Math.min(target,current.slides.length-1));elapsed=0;updateSlide()}
function tick(now){
  if(!playing)return;
  elapsed+=now-last;last=now;
  const duration=(current.slides[index].duration||6)*1000;
  $('#player-progress').style.width=`${Math.min(100,elapsed/duration*100)}%`;
  if(elapsed>=duration){
    if(index===current.slides.length-1){stop();return;}
    index++;elapsed=0;updateSlide();
  }
  raf=requestAnimationFrame(tick);
}
function play(){
  if(playing){stop();return;}
  if(index===current.slides.length-1 && elapsed>=(current.slides[index].duration||6)*1000){index=0;elapsed=0;updateSlide();}
  playing=true;last=performance.now();$('#player-play').innerHTML='Ⅱ <span>停止</span>';$('#player-play').setAttribute('aria-label','自動再生を停止する');raf=requestAnimationFrame(tick);
}
function openDeck(id,button){
  const deck=decks.find(d=>d.id===id);if(!deck)return;
  stop();current=deck;index=0;elapsed=0;trigger=button;
  $('#player-title').textContent=deck.title;$('#player-category').textContent=`${labels[deck.category]} / ${deck.style}`;
  $('#player-description').textContent=`${deck.description} 制作：Studio Yebisu。SVG・HTMLの動きと、編集用PPTXの静止スライドを収録。`;
  $('#player-pptx').href=`downloads/${deck.id}.pptx`;$('#player-html').href=`examples/${deck.id}/index.html`;$('#player-source').href=`downloads/${deck.id}-source.zip`;$('#player-skill').href=`downloads/${deck.skill}.zip`;
  $('#slide-selector').innerHTML=deck.slides.map((s,i)=>`<button type="button" data-slide="${i}" aria-label="${i+1}枚目：${xml(s.title)}" aria-current="${i===0}">${renderSlide(deck,i,{label:false})}</button>`).join('');
  $('#player-notes').hidden=true;$('#notes-toggle').setAttribute('aria-expanded','false');dialog.querySelector('.copy-fallback')?.remove();
  updateSlide();dialog.showModal();document.body.classList.add('body-lock');dialog.scrollTop=0;$('#player-play').focus();
}
async function copyPrompt(){
  try{await navigator.clipboard.writeText(current.prompt);toast('制作プロンプトをコピーしました');}
  catch{
    let textarea=dialog.querySelector('.copy-fallback');
    if(!textarea){textarea=document.createElement('textarea');textarea.className='copy-fallback';textarea.readOnly=true;textarea.setAttribute('aria-label','コピー用の制作プロンプト');$('.player-footer').append(textarea);}
    textarea.value=current.prompt;textarea.focus();textarea.select();toast('表示されたプロンプトを選択してコピーしてください');
  }
}
if(dialog){
  document.addEventListener('click',event=>{
    const open=event.target.closest('[data-open-deck]');if(open){openDeck(open.dataset.openDeck,open);return;}
    const filter=event.target.closest('[data-filter]');if(filter){for(const b of document.querySelectorAll('[data-filter]'))b.setAttribute('aria-pressed',String(b===filter));gallery(filter.dataset.filter);return;}
    const slide=event.target.closest('[data-slide]');if(slide)move(Number(slide.dataset.slide));
  });
  $('#player-close').addEventListener('click',()=>dialog.close());
  dialog.addEventListener('click',event=>{if(event.target===dialog){const bounds=dialog.getBoundingClientRect();if(event.clientX<bounds.left||event.clientX>bounds.right||event.clientY<bounds.top||event.clientY>bounds.bottom)dialog.close();}});
  dialog.addEventListener('close',()=>{stop();document.body.classList.remove('body-lock');trigger?.focus()});
  $('#player-prev').addEventListener('click',()=>move(index-1));$('#player-next').addEventListener('click',()=>move(index+1));$('#player-restart').addEventListener('click',()=>move(0));$('#player-play').addEventListener('click',play);
  $('#notes-toggle').addEventListener('click',()=>{const visible=$('#player-notes').hidden;$('#player-notes').hidden=!visible;$('#notes-toggle').setAttribute('aria-expanded',String(visible))});
  $('#copy-prompt').addEventListener('click',copyPrompt);
  dialog.addEventListener('keydown',event=>{
    if(['INPUT','TEXTAREA','SELECT'].includes(event.target.tagName))return;
    if(event.key==='ArrowRight'){event.preventDefault();move(index+1)}if(event.key==='ArrowLeft'){event.preventDefault();move(index-1)}
    if(event.code==='Space' && event.target.tagName!=='BUTTON'){event.preventDefault();play()}
    if(event.key==='Home'){event.preventDefault();move(0)}if(event.key==='End'){event.preventDefault();move(current.slides.length-1)}
  });
  document.addEventListener('visibilitychange',()=>{if(document.hidden)stop()});
  try{
    const responses=await Promise.all([fetch('data/decks.json'),fetch('data/refined-skills.json'),fetch('data/upstreams.json')]);
    if(responses.some(r=>!r.ok))throw new Error('制作データを読み込めません');
    const [deckData,skillData,upstreams]=await Promise.all(responses.map(r=>r.json()));decks=deckData;skills=skillData;decks.forEach(validateDeck);
    $('#hero-stage').innerHTML=renderSlide(decks.find(d=>d.id==='motion-manifesto'),0,{label:false});gallery();showSkills();showEngines(upstreams);
  }catch(error){console.error(error);$('#deck-grid').innerHTML='<p>作例を読み込めませんでした。ページを再読み込みするか、<a href="examples/team-report/index.html">HTML作例を直接開いてください。</a></p>';}
}
