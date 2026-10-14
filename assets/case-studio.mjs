const $=s=>document.querySelector(s);
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const [cases,collection,previews,pins,profiles,product]=await Promise.all(['data/case-studies.json','data/skills.json','data/previews.json','data/upstreams.json','data/repository-guides.json','data/product-collection.json'].map(async url=>{const r=await fetch(url,{cache:'no-store'});if(!r.ok)throw Error(url);return r.json()}));
const profileByRepo=new Map(profiles.map(p=>[p.repository,p]));
const entryByRepo=new Map(product.entries.map(e=>[e.repository,e]));
const caseRecipes=product.case_recipes||{};
const recipeUrl=c=>{const url=new URL(c.guide,location.href);if(url.pathname.endsWith('/repository.html'))url.searchParams.set('case',c.id);return url.href;};
const caseById=new Map(cases.map(c=>[c.id,c]));
const activeCases=product.active_case_ids.map(id=>caseById.get(id)).filter(Boolean);
const skills=collection.skills.filter(s=>entryByRepo.has(s.repo_full_name)),categories={general:'資料制作総合',pptx:'パワーポイント',html:'ウェブスライド',image:'画像スライド',business:'ビジネス資料',convert:'発表資料'};
for(const c of cases)c.compare=c.compare||c.compare_id;
let use='all',look='all',category='all',current=null,page=0,playing=false,timer=null,trigger=null,nativeObserver=null;
function caseUse(c){if(/企画/.test(c.use_case))return '企画';if(/研修/.test(c.use_case))return '研修';if(/報告/.test(c.use_case))return '報告';if(/提案|改善/.test(c.use_case))return '提案';return c.use_case}
const dialog=$('#case-dialog');
function previewUrl(c,path){const q=new URLSearchParams(path===c.preview?c.preview_options||{}:{});q.set('v',c.content_revision);return path+(path.includes('?')?'&':'?')+q}
function imagePath(c,i){return previewUrl(c,c.pages?.[i]||'examples/cases/'+c.id+'/render/slide-'+String(i+1).padStart(2,'0')+'.png')}
function formatLabel(c){return c.format==='pptx'?'PowerPoint':c.format==='pdf'?'PDF':'Web'}
function caseCards(){
  if(!$('#case-grid'))return;
  const format=$('#case-format').value;
  const list=activeCases.filter(c=>(use==='all'||caseUse(c)===use)&&(look==='all'||entryByRepo.get(c.repository)?.style===look)&&(format==='all'||c.format===format||(format==='pptx'&&c.pptx_download)));
  $('#case-results').textContent=list.length+'冊 / '+list.reduce((n,c)=>n+c.page_count,0)+'枚';
  $('#case-grid').innerHTML=list.length?list.map((c,i)=>'<article class="case-card" data-style="'+esc(entryByRepo.get(c.repository)?.style)+'"><button class="case-card-image'+(c.preview_canvas&&c.preview_canvas.width===c.preview_canvas.height?' square-preview':'')+'" data-open-case="'+esc(c.id)+'" aria-label="'+esc(c.title)+'のスライドを見る"><img src="'+esc(previewUrl(c,c.cover))+'" alt="'+esc(c.title)+'の表紙" loading="lazy"><img class="interior-thumb" src="'+esc(previewUrl(c,c.interior))+'" alt="本文の見本" loading="lazy"><span class="watch">▶ スライドを見る</span></button><div class="case-card-copy"><div class="case-tag"><span>'+esc(entryByRepo.get(c.repository)?.title_ja||c.use_case)+'</span><span>'+formatLabel(c)+' · '+c.page_count+'枚</span></div><h3>'+esc(c.title)+'</h3><p class="skill-name">'+esc(c.style)+'</p><div class="case-card-actions"><button data-open-case="'+esc(c.id)+'">再生する ↗</button><a href="'+esc(entryByRepo.get(c.repository)?.skill_download)+'" download>スキル本文 ↓</a><a href="'+esc(recipeUrl(c))+'">作り方 →</a></div></div></article>').join(''):'<p class="case-empty">この作風の制作事例はまだありません。別の作風・形式を選んでください。</p>';
}
function previewFor(repo){return Array.isArray(previews)?previews.find(p=>p.repository===repo||p.repo_full_name===repo):previews.images?.[repo]||previews[repo]}
function skillCards(){
  if(!$('#skill-grid'))return;
  const term=$('#skill-query').value.trim().normalize('NFKC').toLowerCase(),local=$('#skill-status').value==='local';
  const hasExamples=s=>cases.some(c=>c.repository===s.repo_full_name);
  const list=skills.filter(s=>(category==='all'||s.kind===category)&&(!term||(s.repo_full_name+' '+s.description_ja+' '+entryByRepo.get(s.repo_full_name).title_ja).normalize('NFKC').toLowerCase().includes(term))&&(!local||hasExamples(s))).sort((a,b)=>{const order=$('#skill-order').value;if(order==='produced')return product.entries.findIndex(e=>e.repository===a.repo_full_name)-product.entries.findIndex(e=>e.repository===b.repo_full_name);return order==='name'?a.repo_full_name.localeCompare(b.repo_full_name):b.stars-a.stars||a.repo_full_name.localeCompare(b.repo_full_name)});
  $('#skill-results').textContent=skills.length+'件中 '+list.length+'件'+(term?' /「'+term+'」':'');
  $('#skill-grid').innerHTML=list.map(s=>{
    const repo=s.repo_full_name,entry=entryByRepo.get(repo),works=cases.filter(c=>c.repository===repo).sort((a,b)=>Number(b.id===entry.featured_case_id)-Number(a.id===entry.featured_case_id)),p=previewFor(repo),profile=profileByRepo.get(repo),trial=profile?.execution_status==='local_trial_generated_not_packaged',[owner,name]=repo.split('/');
    const cover=(works[0]?previewUrl(works[0],works[0].interior):null)||(p?.kind==='project'&&p.license&&!/非商用|不一致|未確定/.test(profile?.license_note||'')?(p.src||p.image||p.local_path):null);
    const guide='repository.html?repo='+encodeURIComponent(repo);
    const visual=cover?(works.length?'<button class="repo-image'+(works[0].preview_canvas&&works[0].preview_canvas.width===works[0].preview_canvas.height?' square-preview':'')+'" data-open-case="'+esc(works[0].id)+'" aria-label="'+esc(repo)+'の日本語スライドを見る"><img src="'+esc(cover)+'" alt="ここで制作した日本語資料" loading="lazy"><span class="watch">▶ このリポの実例を見る</span></button>':'<div class="repo-image repo-original-visual"><img src="'+esc(cover)+'" alt="原作者の公開作例・紹介画像" loading="lazy"></div>'):'<div class="repo-placeholder"><span>'+esc(name.slice(0,2).toUpperCase())+'</span><small>'+(trial?'ローカル試用 / 配布条件を確認中':'日本語の作例は制作前')+'</small></div>';
    return '<article class="skill-item" id="skill-'+esc(repo.replace('/','--'))+'">'+visual+'<span class="owner">'+esc(owner)+' / '+esc(categories[s.kind])+'</span><h3><a href="'+guide+'">'+esc(entry.title_ja)+'</a></h3><p>'+esc(entry.description_ja)+'</p><div class="skill-item-actions"><a href="'+esc(entry.skill_download)+'" download>スキル本文 ↓</a>'+(entry.fork_download?'<a href="'+esc(entry.fork_download)+'" download>一式ZIP ↓</a>':'')+'<a href="'+guide+'">作り方 →</a><a href="https://github.com/'+esc(repo)+'" target="_blank" rel="noopener noreferrer">GitHub ↗</a></div><p class="case-sample-note">'+esc(name)+' / '+esc(entry.license||s.license||'個別条件')+'</p></article>';
  }).join('')||'<p class="case-empty">該当するスキルがありません。</p>';
}
function stop(){playing=false;clearTimeout(timer);timer=null;$('#case-play').textContent='▶ 再生'}
function fit(){
  const stage=$('#case-stage'),frame=stage?.querySelector('iframe');if(!frame)return;
  const width=current?.preview_canvas?.width||1280,height=current?.preview_canvas?.height||720;
  frame.style.width=width+'px';frame.style.height=height+'px';
  stage.style.setProperty('--case-scale',String(stage.clientWidth/width));
}
function send(){
  const frame=$('#case-stage iframe');if(!frame)return;
  if(current?.navigation==='native-keyboard'){
    const doc=frame.contentDocument;if(!doc)return;
    const sections=[...doc.querySelectorAll('.reveal .slides>section')],idx=sections.findIndex(s=>s.classList.contains('present'));
    if(idx<0)return;
    const key=page>idx?'ArrowRight':'ArrowLeft';
    for(let n=0;n<Math.abs(page-idx);n++)doc.body.dispatchEvent(new frame.contentWindow.KeyboardEvent('keydown',{key,keyCode:key==='ArrowRight'?39:37,which:key==='ArrowRight'?39:37,bubbles:true}));
  }else frame.contentWindow.postMessage({type:'yebisu-slide',index:page},location.origin);
}
const nativeDOM={
  'qiaomu-bento':['.reveal .slides>section','.present','.reveal .slides'],
  'revealjs-skill':['.reveal .slides>section','.present','.reveal .slides'],
  'lewis-html-ppt':['.deck>.slide','.is-active','.deck'],
  'neon-slides':['.deck>.slide','.active','.deck'],
  'make-slide':['.deck>.slide','.active','.deck'],
  'minorun-marp':['svg[data-marpit-svg].bespoke-marp-slide','.bespoke-marp-active','body'],
  'frontend-editable':['#navDots>button','.active','#navDots'],
  'dashi-ppt':['#deck>.slide','.active','#deck'],
  'magic-slide':['#deck>.slide','.active','#deck']
};
function nativeSync(frame){
  const doc=frame.contentDocument;if(!doc||!current)return;
  const config=nativeDOM[current.id];if(!config)return;
  const sections=[...doc.querySelectorAll(config[0])],idx=sections.findIndex(s=>s.matches(config[1]));
  if(idx<0||idx>=current.page_count||idx===page)return;page=idx;
  $('#case-counter').textContent=(page+1)+' / '+current.page_count;
  $('#case-prev').disabled=page===0;$('#case-next').disabled=page===current.page_count-1;
  $('#case-note').textContent=current.notes[page]||'';
  $('#case-pages').querySelectorAll('button').forEach(b=>b.setAttribute('aria-current',String(Number(b.dataset.page)===page)));
}
function go(n){
  if(!current)return;page=Math.max(0,Math.min(n,current.page_count-1));
  if(['powerpoint-render','pdf-render','artifact-tool-pptx-import-render','image-slides'].includes(current.preview_kind))$('#case-stage').innerHTML='<img src="'+esc(imagePath(current,page))+'" alt="'+esc(current.titles[page])+'">';
  else send();
  $('#case-counter').textContent=(page+1)+' / '+current.page_count;
  $('#case-prev').disabled=page===0;$('#case-next').disabled=page===current.page_count-1;
  $('#case-note').textContent=current.notes[page]||'';
  for(const b of $('#case-pages').querySelectorAll('button'))b.setAttribute('aria-current',String(Number(b.dataset.page)===page));
}
function open(id,button){
  const c=cases.find(c=>c.id===id);if(!c)return;
  if(!dialog.open)trigger=button||document.activeElement;
  stop();nativeObserver?.disconnect();nativeObserver=null;current=c;page=0;
  dialog.classList.toggle('square-preview',Boolean(c.preview_canvas&&c.preview_canvas.width===c.preview_canvas.height));
  $('#case-owner').textContent=c.repository+' / '+c.style;
  $('#case-title').textContent=c.title;
  $('#case-state').textContent=c.preview_notice||(c.format==='pptx'?(c.editability==='raster_slides'?'原典で生成・組版した画像のPPTX / 発表ノート付き・ページ内の文字と図は画像です':'完成PPTXをPowerPointで出力したプレビュー / 文字・図形・ノートを編集できます'):c.format==='pdf'?'完成PDFのプレビュー / 制作ソースから編集できます':'元のスキルを適用したHTML / スライド固有の演出を再生');
  let licenseNotice=$('#case-license');if(!licenseNotice){licenseNotice=document.createElement('p');licenseNotice.id='case-license';licenseNotice.className='case-sample-note';$('#case-state').after(licenseNotice)}
  licenseNotice.textContent=profileByRepo.get(c.repository)?.license_notice_ja||'';licenseNotice.hidden=!licenseNotice.textContent;
  $('#case-download').href=c.artifact_download;
  $('#case-download').textContent=c.format==='pptx'?'PowerPointをダウンロード ↓':c.format==='pdf'?'PDFをダウンロード ↓':'Webスライド一式をダウンロード ↓';
  for(const [id,path,label] of [['case-pptx',c.pptx_download===c.artifact_download?null:c.pptx_download,'PowerPoint版 ↓'],['case-pdf',c.pdf_download===c.artifact_download?null:c.pdf_download,'PDF ↓']]){
    let link=$('#'+id);if(!link){link=document.createElement('a');link.id=id;link.className='button outline';link.setAttribute('download','');$('#case-download').after(link);}
    link.hidden=!path;link.href=path||'#';link.textContent=label;
  }
  $('#case-make').href=recipeUrl(c);
  $('#case-origin').href='https://github.com/'+c.repository+'/tree/'+c.upstream_commit;
  $('#case-compare').hidden=!c.compare;
  if(c.compare){$('#case-compare').dataset.openCase=c.compare;$('#case-compare').href=cases.find(x=>x.id===c.compare).guide;$('#case-compare').textContent=c.format==='pptx'?'同じ入力のWeb版と比べる ↗':'同じ入力のPPTX版と比べる ↗'}
  $('#case-note').hidden=true;$('#case-notes').setAttribute('aria-expanded','false');
  $('#case-pages').innerHTML=c.titles.map((t,i)=>'<button type="button" data-page="'+i+'" aria-label="'+(i+1)+'ページ目 '+esc(t)+'">'+(c.preview_kind==='html'&&!c.pages?'':'<img src="'+esc(imagePath(c,i))+'" alt="">')+'<span>'+String(i+1).padStart(2,'0')+' '+esc(t)+'</span></button>').join('');
  const skillLink=$('#case-skill');if(skillLink){const download=caseRecipes[c.id]?.skill_download||entryByRepo.get(c.repository)?.skill_download;skillLink.hidden=!download;skillLink.href=download||'#'}
  if(c.preview_kind==='html'){
    const frame=document.createElement('iframe');frame.src=previewUrl(c,c.preview);frame.title=c.title;frame.setAttribute('sandbox','allow-scripts allow-same-origin');frame.addEventListener('load',()=>{fit();send();const doc=frame.contentDocument;if(!doc)return;doc.addEventListener('keydown',e=>{if(e.key==='Escape'){e.preventDefault();dialog.close()}},true);const config=nativeDOM[c.id],slides=config&&doc.querySelector(config[2]);if(slides){nativeObserver=new MutationObserver(()=>nativeSync(frame));nativeObserver.observe(slides,{attributes:true,childList:true,subtree:true,attributeFilter:['class']});nativeSync(frame)}});$('#case-stage').replaceChildren(frame);
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
  location.replace(c.guide+'#example-'+encodeURIComponent(c.id));return;
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
  const l=e.target.closest('[data-look]');if(l){look=l.dataset.look;document.querySelectorAll('[data-look]').forEach(b=>b.setAttribute('aria-pressed',String(b===l)));caseCards()}
  const cat=e.target.closest('[data-category]');if(cat){category=cat.dataset.category;document.querySelectorAll('[data-category]').forEach(b=>b.setAttribute('aria-pressed',String(b===cat)));skillCards()}
});
$('#case-close').onclick=()=>dialog.close();$('#case-prev').onclick=()=>{stop();go(page-1)};$('#case-next').onclick=()=>{stop();go(page+1)};$('#case-play').onclick=play;
$('#case-notes').onclick=()=>{$('#case-note').hidden=!$('#case-note').hidden;$('#case-notes').setAttribute('aria-expanded',String(!$('#case-note').hidden))};
$('#case-fullscreen').onclick=()=>{dialog.classList.toggle('expanded');$('#case-fullscreen').textContent=dialog.classList.contains('expanded')?'元の大きさへ ↙':'大きく見る ↗';fit()};
dialog.addEventListener('close',()=>{stop();nativeObserver?.disconnect();nativeObserver=null;$('#case-stage').replaceChildren();dialog.classList.remove('expanded');$('#case-fullscreen').textContent='大きく見る ↗';trigger?.focus()});
dialog.addEventListener('click',e=>{if(e.target===dialog){const b=dialog.getBoundingClientRect();if(e.clientX<b.left||e.clientX>b.right||e.clientY<b.top||e.clientY>b.bottom)dialog.close()}});
document.addEventListener('keydown',e=>{if(!dialog.open)return;if(e.key==='Escape'){e.preventDefault();dialog.close()}if(['ArrowRight','ArrowLeft'].includes(e.key)){e.preventDefault();stop();go(page+(e.key==='ArrowRight'?1:-1))}});
window.addEventListener('message',e=>{const frame=$('#case-stage iframe');if(!frame||e.source!==frame.contentWindow||e.origin!==location.origin)return;if(e.data?.type==='yebisu-close')dialog.close();if(e.data?.type==='yebisu-page'&&Number.isInteger(e.data.index)){page=Math.max(0,Math.min(e.data.index,current.page_count-1));$('#case-counter').textContent=(page+1)+' / '+current.page_count;$('#case-prev').disabled=page===0;$('#case-next').disabled=page===current.page_count-1;$('#case-note').textContent=current.notes[page]||'';$('#case-pages').querySelectorAll('button').forEach(b=>b.setAttribute('aria-current',String(Number(b.dataset.page)===page))) }});
new ResizeObserver(fit).observe($('#case-stage'));window.addEventListener('resize',fit);
$('#case-format')?.addEventListener('change',caseCards);
for(const id of ['skill-query','skill-status','skill-order'])$('#'+id)?.addEventListener(id==='skill-query'?'input':'change',skillCards);
caseCards();skillCards();await detail();
