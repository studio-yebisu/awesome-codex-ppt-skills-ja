// 八百万図AIツールボックス catalog UI. The original 209 repositories remain the identity keys.
const $=s=>document.querySelector(s);
const categories={pptx:'パワーポイント',image:'画像スライド',html:'ウェブスライド',business:'ビジネス資料',convert:'発表資料',general:'資料制作総合'};
const escape=value=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
let projects=[],category='all',current=null,example=null,page=0,playing=false,timer=null,trigger=null;
const dialog=$('#skill-dialog');
const stage=$('#actual-stage');
// Keep each upstream deck at its real 1280×720 viewport, then scale the viewer.
// Small iframe widths must not trigger a different layout or clip its content.
const fitPreview=()=>{const style=getComputedStyle(stage),w=parseFloat(style.width),h=parseFloat(style.height);if(w&&h)stage.style.setProperty('--preview-scale',String(Math.min(w/1280,h/720)))};
new ResizeObserver(fitPreview).observe(stage);
window.addEventListener('resize',fitPreview);
function safeUrl(url){try{const u=new URL(url,location.href);return ['http:','https:'].includes(u.protocol)?u.href:null}catch{return null}}
function previewSrc(preview){
  if(/^assets\/project-previews\/[\w.-]+\.jpg$/.test(preview?.src||''))return preview.src;
  if(!preview?.src)return null;
  try{const u=new URL(preview.src);return u.protocol==='https:'&&['opengraph.githubassets.com','repository-images.githubusercontent.com'].includes(u.hostname)?u.href:null}catch{return null}
}
function render(){
  const term=$('#catalog-query').value.trim().normalize('NFKC').toLowerCase(),mode=$('#catalog-example').value;
  const shown=projects.filter(p=>(category==='all'||p.original_project.kind===category)&&(!term||(p.repository+' '+p.original_project.description_ja).normalize('NFKC').toLowerCase().includes(term))&&(mode==='all'||mode==='japanese'&&p.examples.length||mode==='published'&&p.preview?.kind==='project')).sort((a,b)=>$('#catalog-order').value==='stars'?b.original_project.stars-a.original_project.stars||a.repository.localeCompare(b.repository):a.repository.localeCompare(b.repository));
  $('#catalog-grid').innerHTML=shown.map(p=>{
    const [owner,name]=p.repository.split('/'),real=p.examples[0],preview=p.preview;
    const image=real?.cover||previewSrc(preview),state=real?'日本語の実制作':preview?.kind==='project'?'公開作例・紹介画像':'日本語作例は未制作';
    const visual=image?`<img src="${escape(image)}" alt="${escape(real?`${p.repository}の該当スキルで制作した日本語作例`:preview.alt)}" width="520" height="293" loading="lazy" decoding="async" referrerpolicy="no-referrer">`:`<span class="catalog-artifact-placeholder"><small>${escape(categories[p.original_project.kind])}</small>${escape(name)}</span>`;
    return `<article class="deck-card catalog-card" data-repository="${escape(p.repository)}"><button class="deck-open" type="button" data-open-project="${escape(p.repository)}" aria-label="${escape(p.repository)}の${real?'日本語スライドを再生':'作例と紹介を開く'}">${visual}<span class="open-affordance">${real?'▶ 日本語のスライドを再生':preview?.kind==='project'?'公開作例を見る ↗':'スキルの紹介を見る ↗'}</span></button><div class="deck-meta"><span>${escape(categories[p.original_project.kind])}</span><span class="${real?'state-japanese':''}">${escape(state)}</span></div><p class="project-author">${escape(owner)}</p><h3><button type="button" data-open-project="${escape(p.repository)}">${escape(name)}</button></h3><p class="deck-description">${escape(p.original_project.description_ja)}</p><div class="deck-info"><span>★ ${p.original_project.stars.toLocaleString('ja-JP')} · ${escape(p.license||'ライセンス要確認')}</span><a href="${escape(p.repository_url)}" target="_blank" rel="noopener noreferrer">元のスキル ↗</a></div></article>`;
  }).join('');
  $('#catalog-count').textContent=`${projects.length}件中 ${shown.length}件${term?` /「${term}」`:''}`;$('#catalog-empty').hidden=shown.length>0;
}
function stop(){playing=false;clearTimeout(timer);timer=null;$('#actual-play').textContent='▶ 再生'}
function sendPage(){
  const frame=$('#actual-stage iframe');
  if(frame&&example?.kind==='html')frame.contentWindow.postMessage({type:'yebisu-slide',index:page},location.origin);
}
function setPage(index){
  if(!example)return;page=Math.max(0,Math.min(index,example.slide_count-1));
  if(example.kind==='svg-pages')$('#actual-stage').innerHTML=`<img src="${escape(example.pages[page])}" alt="${escape(example.titles[page])}">`;
  else sendPage();
  $('#actual-counter').textContent=`${page+1} / ${example.slide_count}`;$('#actual-prev').disabled=page===0;$('#actual-next').disabled=page===example.slide_count-1;
  $('#actual-note-panel').textContent=example.notes?.[page]||'';
}
function play(){
  if(playing){stop();return}
  if(page===example.slide_count-1)setPage(0);
  playing=true;$('#actual-play').textContent='Ⅱ 停止';
  const tick=()=>{if(!playing)return;if(page===example.slide_count-1){stop();return}setPage(page+1);timer=setTimeout(tick,6500)};
  timer=setTimeout(tick,6500);
}
function selectExample(index){
  stop();example=current.examples[index]||null;page=0;
  const preview=current.preview;
  $('#actual-controls').hidden=!example;$('#actual-note-panel').hidden=true;$('#actual-notes').setAttribute('aria-expanded','false');
  for(const b of $('#example-tabs').querySelectorAll('button'))b.setAttribute('aria-pressed',String(Number(b.dataset.example)===index));
  $('#detail-download').hidden=!example?.download;$('#detail-fork').hidden=!example?.fork_download;
  if(example?.download)$('#detail-download').href=example.download;
  if(example?.fork_download)$('#detail-fork').href=example.fork_download;
  if(example){
    $('#example-state').textContent=`日本語の実制作 / ${example.method_label}`;
    $('#detail-origin').href=current.repository_url+'/tree/'+example.commit;$('#detail-origin').textContent='使用した固定コミット ↗';
    $('#detail-proof').href=example.proof;$('#detail-proof').hidden=false;
    if(example.kind==='html'){
      const frame=document.createElement('iframe');frame.title=example.title;frame.src=example.html;frame.setAttribute('sandbox','allow-scripts allow-same-origin');frame.addEventListener('load',sendPage);$('#actual-stage').replaceChildren(frame);
    }
    setPage(0);
  }else{
    $('#detail-proof').hidden=true;
    const src=preview?.kind==='project'?previewSrc(preview):null;
    $('#actual-stage').innerHTML=src?`<img src="${escape(src)}" alt="${escape(preview.alt)}">`:`<div class="repo-introduction"><h3>${escape(current.repository)}</h3><p>${escape(current.original_project.description_ja)}</p><p>このスキルを使った日本語作例は、まだ制作していません。原典で導入方法と出力例を確認できます。</p></div>`;
    $('#example-state').textContent=src?'原作者の公開作例・紹介画像 / このサイトでの実制作ではありません':'日本語の実制作は未実施 / GitHub紹介画像はスライドとして再生しません';
    $('#detail-origin').href=safeUrl(preview?.source)||current.repository_url;$('#detail-origin').textContent=src?'元の作例の出典 ↗':'原典のREADME ↗';
  }
}
function openProject(repository,button){
  const p=projects.find(p=>p.repository===repository);if(!p)return;
  current=p;trigger=button;
  const [owner,name]=p.repository.split('/');$('#skill-dialog-owner').textContent=`${owner} / ${categories[p.original_project.kind]}`;$('#skill-dialog-title').textContent=name;
  $('#skill-detail-description').textContent=p.original_project.description_ja;$('#detail-repository').href=p.repository_url;
  $('#detail-license').textContent=`掲載スキル：${p.license||'個別ライセンス要確認'}。${p.license_checked_at?'固定コミットの原文を確認済み。':'原版カタログの記録。導入・再配布の前に原典を確認してください。'} 公開画像には個別の出典条件が適用されます。`;
  $('#example-tabs').innerHTML=p.examples.map((e,i)=>`<button type="button" data-example="${i}" aria-pressed="${i===0}">${escape(e.style||e.title)}</button>`).join('')+(p.preview?.kind==='project'?`<button type="button" data-example="-1" aria-pressed="${!p.examples.length}">原作者の公開作例</button>`:'');
  selectExample(p.examples.length?0:-1);dialog.showModal();fitPreview();dialog.scrollTop=0;document.body.classList.add('body-lock');(example?$('#actual-play'):$('#skill-dialog-close')).focus();
}
document.addEventListener('click',event=>{
  const open=event.target.closest('[data-open-project]');if(open){openProject(open.dataset.openProject,open);return}
  const filter=event.target.closest('[data-category]');if(filter){category=filter.dataset.category;for(const b of document.querySelectorAll('[data-category]'))b.setAttribute('aria-pressed',String(b===filter));render();return}
  const tab=event.target.closest('[data-example]');if(tab)selectExample(Number(tab.dataset.example));
});
for(const id of ['catalog-query','catalog-example','catalog-order'])$('#'+id).addEventListener(id==='catalog-query'?'input':'change',render);
$('#catalog-clear').addEventListener('click',()=>{$('#catalog-query').value='';$('#catalog-example').value='all';render();$('#catalog-query').focus()});
$('#skill-dialog-close').addEventListener('click',()=>dialog.close());dialog.addEventListener('close',()=>{stop();$('#actual-stage').replaceChildren();document.body.classList.remove('body-lock');trigger?.focus()});
dialog.addEventListener('click',e=>{if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)dialog.close()}});
$('#actual-prev').addEventListener('click',()=>{stop();setPage(page-1)});$('#actual-next').addEventListener('click',()=>{stop();setPage(page+1)});$('#actual-play').addEventListener('click',play);
$('#actual-notes').addEventListener('click',()=>{const visible=$('#actual-note-panel').hidden;$('#actual-note-panel').hidden=!visible;$('#actual-notes').setAttribute('aria-expanded',String(visible))});
dialog.addEventListener('keydown',e=>{if(!example||['INPUT','TEXTAREA','SELECT'].includes(e.target.tagName))return;if(e.key==='ArrowRight'){e.preventDefault();stop();setPage(page+1)}if(e.key==='ArrowLeft'){e.preventDefault();stop();setPage(page-1)}if(e.code==='Space'&&e.target.tagName!=='BUTTON'){e.preventDefault();play()}});
document.addEventListener('visibilitychange',()=>{if(document.hidden)stop()});
window.addEventListener('message',event=>{const frame=$('#actual-stage iframe');if(!frame||event.source!==frame.contentWindow||event.origin!==location.origin)return;if(event.data?.type==='yebisu-close'){dialog.close();return}if(event.data?.type!=='yebisu-page')return;const index=event.data.index;if(Number.isInteger(index)&&index>=0&&index<example.slide_count){page=index;$('#actual-counter').textContent=`${page+1} / ${example.slide_count}`;$('#actual-prev').disabled=page===0;$('#actual-next').disabled=page===example.slide_count-1;$('#actual-note-panel').textContent=example.notes?.[page]||''}});
$('#open-featured').addEventListener('click',()=>{const p=projects.find(p=>p.repository==='op7418/guizang-ppt-skill'&&p.examples.length)||projects.find(p=>p.examples.length)||projects.find(p=>p.repository==='op7418/guizang-ppt-skill');if(p)openProject(p.repository,$('#open-featured'))});
try{
  const r=await fetch('data/project-workflows.json');if(!r.ok)throw new Error('スキルデータを読み込めません');
  const data=await r.json();projects=data.projects;
  if(projects.length!==209||new Set(projects.map(p=>p.repository)).size!==209)throw new Error('209件の原典対応に不一致があります');
  for(const p of projects)if(!/^[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+$/.test(p.repository))throw new Error('不正なリポジトリ名');
  render();
  const featured=projects.find(p=>p.repository==='op7418/guizang-ppt-skill');
  if(featured?.examples[0]?.cover){$('#catalog-hero-stage').innerHTML=`<img src="${escape(featured.examples[0].cover)}" alt="Guizangの実際のテンプレートで制作した日本語作例">`;$('#hero-source').textContent='op7418 / guizang-ppt-skill · 日本語の実制作';}
}catch(error){console.error(error);$('#catalog-count').textContent='読み込みに失敗しました。再読み込みするかGitHubのカタログをご覧ください。'}
