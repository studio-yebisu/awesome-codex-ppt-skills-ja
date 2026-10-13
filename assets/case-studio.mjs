const $=s=>document.querySelector(s);
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const [cases,collection,previews,pins]=await Promise.all(['data/case-studies.json','data/skills.json','data/previews.json','data/upstreams.json'].map(async url=>{const r=await fetch(url,{cache:'no-store'});if(!r.ok)throw Error(url);return r.json()}));
const skills=collection.skills,categories={general:'資料制作総合',pptx:'パワーポイント',html:'ウェブスライド',image:'画像スライド',business:'ビジネス資料',convert:'発表資料'};
for(const c of cases)c.compare=c.compare||c.compare_id;
let use='all',category='all',current=null,page=0,playing=false,timer=null,trigger=null;
function caseUse(c){if(/企画/.test(c.use_case))return '企画';if(/研修/.test(c.use_case))return '研修';if(/報告/.test(c.use_case))return '報告';if(/提案|改善/.test(c.use_case))return '提案';return c.use_case}
const dialog=$('#case-dialog');
function imagePath(c,i){return c.pages?.[i]||'examples/cases/'+c.id+'/render/slide-'+String(i+1).padStart(2,'0')+'.png'}
function caseCards(){
  if(!$('#case-grid'))return;
  const format=$('#case-format').value;
  const list=cases.filter(c=>(use==='all'||caseUse(c)===use)&&(format==='all'||c.format===format));
  $('#case-results').textContent=list.length+'冊 / '+list.reduce((n,c)=>n+c.page_count,0)+'枚';
  $('#case-grid').innerHTML=list.length?list.map(c=>'<article class="case-card"><button class="case-card-image" data-open-case="'+esc(c.id)+'" aria-label="'+esc(c.title)+' '+esc(c.style)+'のスライド事例を見る"><img src="'+esc(c.cover)+'" alt="'+esc(c.title)+'の表紙" loading="lazy"><img class="interior-thumb" src="'+esc(c.interior)+'" alt="本文の見本" loading="lazy"><span class="watch">▶ スライド事例を見る</span></button><div class="case-card-copy"><div class="case-tag"><span>'+esc(c.use_case)+'</span><span>'+(c.format==='pptx'?'PowerPoint':'Web')+' · '+c.page_count+'枚</span></div><h3>'+esc(c.title)+'</h3><p class="skill-name">'+esc(c.repository)+' / '+esc(c.style)+'</p><div class="case-card-actions"><button data-open-case="'+esc(c.id)+'">事例を見る ↗</button><a href="'+esc(c.guide)+'">このスキルで作る →</a></div></div></article>').join(''):'<p class="case-empty">この条件の制作事例はまだありません。別の用途・形式を選んでください。</p>';
}
function previewFor(repo){return Array.isArray(previews)?previews.find(p=>p.repository===repo||p.repo_full_name===repo):previews.images?.[repo]||previews[repo]}
function skillCards(){
  if(!$('#skill-grid'))return;
  const term=$('#skill-query').value.trim().normalize('NFKC').toLowerCase(),local=$('#skill-status').value==='local';
  const list=skills.filter(s=>(category==='all'||s.kind===category)&&(!term||(s.repo_full_name+' '+s.description_ja).normalize('NFKC').toLowerCase().includes(term))&&(!local||cases.some(c=>c.repository===s.repo_full_name))).sort((a,b)=>$('#skill-order').value==='stars'?b.stars-a.stars||a.repo_full_name.localeCompare(b.repo_full_name):a.repo_full_name.localeCompare(b.repo_full_name));
  $('#skill-results').textContent=skills.length+'件中 '+list.length+'件'+(term?' /「'+term+'」':'');
  $('#skill-grid').innerHTML=list.map(s=>{
    const repo=s.repo_full_name,works=cases.filter(c=>c.repository===repo),p=previewFor(repo),[owner,name]=repo.split('/');
    const cover=works[0]?.cover||(p?.kind==='project'?(p.src||p.image||p.local_path):null);
    const visual=cover?'<img class="skill-preview" src="'+esc(cover)+'" alt="'+esc(works.length?'このサイトで制作した日本語資料':'原作者の公開作例・紹介画像')+'" loading="lazy">':'';
    return '<article class="skill-item" id="skill-'+esc(repo.replace('/','--'))+'">'+visual+'<span class="owner">'+esc(owner)+' / '+esc(categories[s.kind])+'</span><h3>'+esc(name)+'</h3><p>'+esc(s.description_ja)+'</p><p class="skill-state">'+(works.length?'日本語の制作事例 '+works.length+'冊・派生版あり':'日本語の制作事例は未制作')+'</p><div class="skill-item-actions">'+works.map((c,i)=>'<button data-open-case="'+esc(c.id)+'">'+esc(c.use_case)+'の事例 '+(i+1)+' ↗</button>').join('')+'<a href="https://github.com/'+esc(repo)+'" target="_blank" rel="noopener noreferrer">原典 ↗</a></div><p class="case-sample-note">★ '+Number(s.stars).toLocaleString('ja-JP')+' / '+esc(s.license||'条件を原典で確認')+(visual&&!works.length?' / 原作者の公開画像':'')+'</p></article>';
  }).join('')||'<p class="case-empty">該当するスキルがありません。</p>';
}
function stop(){playing=false;clearTimeout(timer);timer=null;$('#case-play').textContent='▶ 再生'}
function fit(){
  const stage=$('#case-stage'),frame=stage?.querySelector('iframe');if(!frame)return;
  stage.style.setProperty('--case-scale',String(stage.clientWidth/1280));
}
function send(){const frame=$('#case-stage iframe');if(frame)frame.contentWindow.postMessage({type:'yebisu-slide',index:page},location.origin)}
function go(n){
  if(!current)return;page=Math.max(0,Math.min(n,current.page_count-1));
  if(current.preview_kind==='powerpoint-render')$('#case-stage').innerHTML='<img src="'+esc(current.pages[page])+'" alt="'+esc(current.titles[page])+'">';
  else send();
  $('#case-counter').textContent=(page+1)+' / '+current.page_count;
  $('#case-prev').disabled=page===0;$('#case-next').disabled=page===current.page_count-1;
  $('#case-note').textContent=current.notes[page]||'';
  for(const b of $('#case-pages').querySelectorAll('button'))b.setAttribute('aria-current',String(Number(b.dataset.page)===page));
}
function open(id,button){
  const c=cases.find(c=>c.id===id);if(!c)return;
  if(!dialog.open)trigger=button||document.activeElement;
  stop();current=c;page=0;
  $('#case-owner').textContent=c.repository+' / '+c.style;
  $('#case-title').textContent=c.title;
  $('#case-state').textContent=c.format==='pptx'?'完成PPTXをPowerPointで出力したプレビュー / 文字・図形・ノートを編集できます':'元のスキルを適用したHTML / スライド固有の演出を再生';
  $('#case-download').href=c.artifact_download;
  $('#case-download').textContent=c.format==='pptx'?'PowerPointをダウンロード ↓':'Webスライド一式をダウンロード ↓';
  $('#case-make').href=c.guide;
  $('#case-origin').href='https://github.com/'+c.repository+'/tree/'+c.upstream_commit;
  $('#case-compare').hidden=!c.compare;
  if(c.compare){$('#case-compare').dataset.openCase=c.compare;$('#case-compare').href=cases.find(x=>x.id===c.compare).guide;$('#case-compare').textContent=c.format==='pptx'?'同じ入力のWeb版と比べる ↗':'同じ入力のPPTX版と比べる ↗'}
  $('#case-note').hidden=true;$('#case-notes').setAttribute('aria-expanded','false');
  $('#case-pages').innerHTML=c.titles.map((t,i)=>'<button type="button" data-page="'+i+'" aria-label="'+(i+1)+'ページ目 '+esc(t)+'"><img src="'+esc(imagePath(c,i))+'" alt=""><span>'+String(i+1).padStart(2,'0')+' '+esc(t)+'</span></button>').join('');
  if(c.preview_kind==='html'){
    const frame=document.createElement('iframe');frame.src=c.preview;frame.title=c.title;frame.setAttribute('sandbox','allow-scripts allow-same-origin');frame.addEventListener('load',()=>{fit();send()});$('#case-stage').replaceChildren(frame);
  }
  go(0);if(!dialog.open)dialog.showModal();fit();
}
function play(){
  if(!current)return;if(playing){stop();return}
  if(page===current.page_count-1)go(0);playing=true;$('#case-play').textContent='Ⅱ 停止';
  function tick(){if(!playing)return;if(page===current.page_count-1){stop();return}go(page+1);timer=setTimeout(tick,5500)}
  timer=setTimeout(tick,5500);
}
async function detail(){
  const root=$('#case-detail');if(!root)return;
  const id=new URLSearchParams(location.search).get('id'),c=cases.find(c=>c.id===id);
  if(!c){root.innerHTML='<p>制作事例が見つかりません。<a href="./#examples">一覧へ戻る</a></p>';return}
  document.title=c.title+'｜AIスライドスキル集';
  root.innerHTML='<a class="text-link" href="./#examples">← 日本語の制作事例へ</a><div class="detail-heading"><p class="eyebrow">'+esc(c.use_case)+' / '+(c.format==='pptx'?'POWERPOINT':'WEB SLIDES')+' / '+c.page_count+' PAGES</p><h1>'+esc(c.title)+'</h1><p>'+esc(c.repository)+' / '+esc(c.style)+'</p></div><div class="detail-layout"><div><button class="case-card-image detail-cover" data-open-case="'+esc(c.id)+'"><img src="'+esc(c.interior)+'" alt="実際に制作した資料の本文"><span class="watch">▶ スライド事例を見る</span></button><div class="detail-actions"><a class="button primary" href="'+esc(c.artifact_download)+'" download>資料をダウンロード ↓</a>'+(c.pdf_download?'<a class="button outline" href="'+esc(c.pdf_download)+'" download>PDF ↓</a>':'')+'<a class="text-link" href="'+esc(c.source_download)+'" download>制作ソース一式 ↓</a></div><p class="case-sample-note">'+esc(c.sample_notice)+'</p>'+(c.compare?'<div class="detail-block"><h2>同じ入力で、別の形式へ。</h2><p>入力・数値・判断材料を共有。PowerPointで編集する資料と、演出付きのWeb発表を比較できます。</p><a class="button outline" href="'+esc(cases.find(x=>x.id===c.compare).guide)+'">もう一方を見る ↗</a></div>':'')+'<div class="detail-block"><h2>制作に使った入力</h2><div class="details-links"><a href="'+esc(c.input)+'">原稿・制作ブリーフ</a><a href="'+esc(c.input_data)+'">数値と条件</a></div><pre class="detail-data" id="input-data">読込中…</pre></div></div><div><section class="detail-block"><h2>このスキルで作る</h2><ol class="detail-steps"><li><a href="'+esc(c.fork_download)+'" download>日本語版 '+esc(c.fork_id)+' を取得</a>し、使用するエージェントのskillsへ配置。</li><li>入力の読者・数値・結論を、自分の資料へ変更。</li><li>下の依頼文と入力を渡して制作。</li><li>完成ファイルを開き、日本語と図表を確認。</li></ol><textarea id="case-prompt" aria-label="日本語の再制作依頼文" readonly>'+esc(c.prompt_text)+'</textarea><button class="button primary" id="copy-prompt" type="button">依頼文をコピー</button><span class="copy-status" id="copy-status" role="status"></span></section><section class="detail-block"><h2>方式と、日本語の改良</h2><p>'+esc(c.method)+'</p><p>'+(c.format==='pptx'?'文字・図形・ノートを編集できるPPTX。フォントは未埋め込みのため、受け手にもNoto Sans JPが必要です。':'日本語の改行・禁則・字形を調整。書体と依存を同梱し、ローカル閲覧に対応。'+(c.fork_id==='frontend-slides-ja'?'Eで編集、Ctrl+SでHTML保存。':'元の発表者モードとページ演出を保持。'))+'</p><div class="details-links"><a href="https://github.com/'+esc(c.repository)+'/tree/'+esc(c.upstream_commit)+'">使用した原典 ↗</a><a href="'+esc(c.provenance)+'">制作方法・出典記録</a><a href="'+esc(c.qa)+'">確認範囲</a><a href="licenses.html">個別の利用条件</a></div></section></div></div>';
  const input=await fetch(c.input_data);$('#input-data').textContent=JSON.stringify(await input.json(),null,2);
  $('#copy-prompt').onclick=async()=>{
    try{await navigator.clipboard.writeText(c.prompt_text);$('#copy-status').textContent='コピーしました'}
    catch{$('#case-prompt').focus();$('#case-prompt').select();$('#copy-status').textContent='依頼文を選択しました。Ctrl+Cでコピーしてください'}
  };
}
document.addEventListener('click',e=>{
  const opener=e.target.closest('[data-open-case]');if(opener){e.preventDefault();open(opener.dataset.openCase,opener);return}
  const pageButton=e.target.closest('[data-page]');if(pageButton){stop();go(Number(pageButton.dataset.page));return}
  const u=e.target.closest('[data-use]');if(u){use=u.dataset.use;document.querySelectorAll('[data-use]').forEach(b=>b.setAttribute('aria-pressed',String(b===u)));caseCards()}
  const cat=e.target.closest('[data-category]');if(cat){category=cat.dataset.category;document.querySelectorAll('[data-category]').forEach(b=>b.setAttribute('aria-pressed',String(b===cat)));skillCards()}
});
$('#case-close').onclick=()=>dialog.close();$('#case-prev').onclick=()=>{stop();go(page-1)};$('#case-next').onclick=()=>{stop();go(page+1)};$('#case-play').onclick=play;
$('#case-notes').onclick=()=>{$('#case-note').hidden=!$('#case-note').hidden;$('#case-notes').setAttribute('aria-expanded',String(!$('#case-note').hidden))};
$('#case-fullscreen').onclick=()=>{dialog.classList.toggle('expanded');$('#case-fullscreen').textContent=dialog.classList.contains('expanded')?'元の大きさへ ↙':'大きく見る ↗';fit()};
dialog.addEventListener('close',()=>{stop();$('#case-stage').replaceChildren();dialog.classList.remove('expanded');$('#case-fullscreen').textContent='大きく見る ↗';trigger?.focus()});
dialog.addEventListener('click',e=>{if(e.target===dialog){const b=dialog.getBoundingClientRect();if(e.clientX<b.left||e.clientX>b.right||e.clientY<b.top||e.clientY>b.bottom)dialog.close()}});
document.addEventListener('keydown',e=>{if(!dialog.open)return;if(e.key==='Escape'){e.preventDefault();dialog.close()}if(['ArrowRight','ArrowLeft'].includes(e.key)){e.preventDefault();stop();go(page+(e.key==='ArrowRight'?1:-1))}});
window.addEventListener('message',e=>{const frame=$('#case-stage iframe');if(!frame||e.source!==frame.contentWindow||e.origin!==location.origin)return;if(e.data?.type==='yebisu-close')dialog.close();if(e.data?.type==='yebisu-page'&&Number.isInteger(e.data.index)){page=Math.max(0,Math.min(e.data.index,current.page_count-1));$('#case-counter').textContent=(page+1)+' / '+current.page_count;$('#case-prev').disabled=page===0;$('#case-next').disabled=page===current.page_count-1;$('#case-note').textContent=current.notes[page]||'';$('#case-pages').querySelectorAll('button').forEach(b=>b.setAttribute('aria-current',String(Number(b.dataset.page)===page))) }});
new ResizeObserver(fit).observe($('#case-stage'));window.addEventListener('resize',fit);
$('#case-format')?.addEventListener('change',caseCards);
for(const id of ['skill-query','skill-status','skill-order'])$('#'+id)?.addEventListener(id==='skill-query'?'input':'change',skillCards);
caseCards();skillCards();await detail();
