import {caseDownloadName} from './download-name.mjs';
import {caseCountLabel,playbackCounter,playbackOrdinal} from './case-units.mjs';
import {esc,text,previewUrl,interiorPath,imagePath,IMAGE_PREVIEW_KINDS,formatLabel,unitWord,loadSkillEffects,NEEDS,matchesNeed,matchesFormat,buildSkillItems,itemFor,skillName,detailUrl,pageHeading} from './skill-effects.mjs';
const $=s=>document.querySelector(s);
const all=s=>[...(document.querySelectorAll?.(s)||[])];
const [cases,profiles,product]=await Promise.all(['data/case-studies.json','data/repository-guides.json','data/product-collection.json'].map(async url=>{const r=await fetch(url,{cache:'no-store'});if(!r.ok)throw Error(url);return r.json()}));
const effects=await loadSkillEffects();
const profileByRepo=new Map(profiles.map(p=>[p.repository,p]));
const entryByRepo=new Map(product.entries.map(e=>[e.repository,e]));
const caseRecipes=product.case_recipes||{};
const recipeUrl=c=>{const url=new URL(c.guide,location.href);if(url.pathname.endsWith('/repository.html'))url.searchParams.set('case',c.id);return url.href;};
const caseById=new Map(cases.map(c=>[c.id,c]));
const items=buildSkillItems({entries:product.entries,cases,activeIds:product.active_case_ids,effects});
for(const c of cases)c.compare=c.compare||c.compare_id;
const params=new URLSearchParams(location.search);
const state={query:params.get('q')||'',need:NEEDS.some(n=>n.id===params.get('need'))?params.get('need'):'all',format:['pptx','html','pdf'].includes(params.get('format'))?params.get('format'):'all',tag:'all'};
let current=null,currentItem=null,page=0,target=null,targetTimer=null,playing=false,timer=null,trigger=null,nativeObserver=null;
const dialog=$('#case-dialog');
const squareClass=c=>c?.preview_canvas&&c.preview_canvas.width===c.preview_canvas.height?' square-preview':'';
const nonCommercial=repo=>/非商用|NC-/.test((profileByRepo.get(repo)?.license_notice_ja||'')+(entryByRepo.get(repo)?.license_notice_ja||'')+(profileByRepo.get(repo)?.license||''));

// --- One list: skill function → change → input/output → the page to inspect → actions.
const visibleTags=i=>i.tags.filter(t=>!['pptx','html','pdf'].includes(t.toLowerCase()));
const tagLabels={'MckEngine高水準API':'図表の共通部品','公式PptxGenJS雛形':'公式のPowerPoint生成ひな型','PptxGenJS雛形':'PowerPoint生成ひな型','13-slot版式':'13種類の配置','OMML数式':'PowerPointで編集できる数式','answer-first構成':'結論から示す構成','atomic patch':'部分ごとの修正','claim-to-source map':'主張と出典の対応','hookからCTAの構成':'関心を引き、次の行動へつなぐ構成','native chart':'編集できるグラフ','nativeチャート':'編集できるグラフ','native図形':'編集できる図形','native文字とノート':'編集できる文字と発表ノート','native表':'編集できる表','notes-only判定':'発表ノートだけで伝わるか確認','persistent actor':'同じ要素を場面間で動かす','pose間の移動':'状態の間を動かす','rail移動':'一本の経路に沿う移動','scene/beat map':'場面と表示順の対応','typed Step':'定義した段階ごとの表示','全ページ画像blueprint':'全ページの画像案','内容lock':'本文を先に確定','実MCP stdio':'AIから生成・編集を呼び出す','実MCP呼び出し':'AIから生成・編集を呼び出す','実描画presenter':'発表者用の画面','連続timeline':'連続した時間軸','関係別exhibit':'関係に応じた図表'};
const tagLabel=t=>tagLabels[t]||t;
const allTags=[...items.reduce((m,i)=>{for(const t of visibleTags(i))m.set(t,(m.get(t)||0)+1);return m},new Map())].sort((a,b)=>b[1]-a[1]||a[0].localeCompare(b[0],'ja'));
function filtered(skip){
  const term=state.query.trim().normalize('NFKC').toLowerCase();
  return items.filter(i=>(skip==='query'||!term||i.search.includes(term))&&(skip==='need'||state.need==='all'||matchesNeed(i,state.need))&&(skip==='format'||matchesFormat(i,state.format))&&(skip==='tag'||state.tag==='all'||i.tags.includes(state.tag)));
}
function conditions(){
  const out=[];
  if(state.query.trim())out.push(['query','検索「'+state.query.trim()+'」']);
  if(state.need!=='all')out.push(['need','改善したいこと：'+NEEDS.find(n=>n.id===state.need).label]);
  if(state.format!=='all')out.push(['format','形式：'+{pptx:'PowerPoint',html:'Web',pdf:'PDF'}[state.format]]);
  if(state.tag!=='all')out.push(['tag','方式：'+tagLabel(state.tag)]);
  return out;
}
function proofBlock(i){
  const c=i.case;
  if(!c)return '<div class="effect-proof"><p class="effect-proof-title">この作例で確かめる</p><p class="effect-missing">掲載中の作例はありません。</p></div>';
  const first=i.pages.find(p=>p.valid);
  // Without a capture of the recorded page, the cover is shown and labelled as such, never as that page.
  const image=first?.image||previewUrl(c,c.cover);
  const badge=first?(first.image?playbackOrdinal(c,first.index):'表紙（'+playbackOrdinal(c,first.index)+'は再生して確認）'):'';
  const opener='data-open-case="'+esc(c.id)+'" data-effect="'+esc(i.key)+'"'+(first?' data-open-page="'+first.index+'"':'');
  let note;
  if(first)note='<p class="effect-inspect"><b>'+esc(playbackOrdinal(c,first.index))+'</b>'+esc(first.inspect||first.label||'見る箇所の説明は未記録です。')+'</p>';
  else if(i.effect&&!i.caseMatches)note='<p class="effect-missing">効果記録の作例「'+esc(i.recordedCaseId||'未記入')+'」が掲載データにないため、見る箇所を表示していません。</p>';
  else if(i.effect)note='<p class="effect-missing">見る'+unitWord(c)+'の記録はまだありません。</p>';
  else note='<p class="effect-missing">見る箇所の記録はまだありません。</p>';
  const more=new Set(i.pages.filter(p=>p.valid&&!p.supplemental).map(p=>p.index)).size-1;
  const openLabel=skillName(i)+'：'+(first?playbackOrdinal(c,first.index)+'の見る箇所を開く':'作例を開く');
  return '<div class="effect-proof"><p class="effect-proof-title">この作例で確かめる</p>'+note+'<button type="button" class="effect-proof-image'+squareClass(c)+'" '+opener+' aria-label="'+esc(openLabel)+'"><img src="'+esc(image)+'" alt="" loading="lazy">'+(badge?'<span>'+esc(badge)+'</span>':'')+'</button><p class="effect-case">作例名：'+esc(c.title)+' <span>'+formatLabel(c)+' · '+esc(caseCountLabel(c))+(more>0?' · ほか'+more+unitWord(c)+'にも見る箇所あり':'')+'</span></p></div>';
}
function card(i){
  const e=i.effect,c=i.case,entry=i.entry,first=i.pages.find(p=>p.valid),[owner,name]=i.repository.split('/');
  const license=entry?.license||profileByRepo.get(i.repository)?.license||'個別条件';
  const facts=e?[['どう変わる',text(e.change)],['渡すもの',text(e.input)],['受け取るもの',text(e.output)]].map(([k,v])=>'<div><dt>'+k+'</dt><dd>'+(v?esc(v):'<span class="effect-missing">未記録</span>')+'</dd></div>').join(''):'';
  const others=i.others.length?'<p class="effect-others">同じスキルの作例：'+i.others.map(o=>'<button type="button" data-open-case="'+esc(o.id)+'" data-effect="'+esc(i.key)+'">'+esc(o.title)+'</button>').join('')+'</p>':'';
  return '<article class="effect-card" id="skill-'+esc(i.repository.replace('/','--'))+(i.index?'-'+i.index:'')+'">'
   +'<p class="effect-repo"><a href="https://github.com/'+esc(i.repository)+'" target="_blank" rel="noopener noreferrer">'+esc(owner)+' / <b>'+esc(name)+'</b> ↗</a><span>'+esc(license)+'</span>'+(nonCommercial(i.repository)?'<span class="effect-warning">非商用条件あり</span>':'')+'</p>'
   +'<h3><a href="'+esc(detailUrl(i))+'">'+esc(skillName(i))+'</a></h3>'
   +(e?(text(e.job)&&text(e.job)!==text(e.change)?'<p class="effect-job">'+esc(text(e.job))+'</p>':''):'<p class="effect-missing">このスキルの機能・入力・見る箇所の記録はまだありません。下は掲載時の紹介文です。</p><p class="effect-job">'+esc(entry?.description_ja||'')+'</p>')
   +(facts?'<dl class="effect-facts">'+facts+'</dl>':'')
   +(visibleTags(i).length?'<ul class="effect-tags" aria-label="方式タグ（押すと同じ方式で絞り込み）">'+visibleTags(i).slice(0,5).map(t=>'<li><button type="button" data-tag="'+esc(t)+'" aria-pressed="'+String(state.tag===t)+'">'+esc(tagLabel(t))+'</button></li>').join('')+'</ul>':'')
   +(e?.demonstration?.cautions?.length?'<div class="effect-cautions">'+e.demonstration.cautions.map(s=>'<p>'+esc(s)+'</p>').join('')+'</div>':'')
   +proofBlock(i)+others
   +'<div class="effect-actions"><a class="effect-primary" href="'+esc(detailUrl(i))+'">効果と使い方を見る →</a>'+(c?'<button type="button" data-open-case="'+esc(c.id)+'" data-effect="'+esc(i.key)+'"'+(first?' data-open-page="'+first.index+'">'+esc(playbackOrdinal(c,first.index))+'を確認 ▶':'>作例を再生 ▶')+'</button>':'')+(entry?.skill_download?'<a href="'+esc(entry.skill_download)+'" download>スキル本文 ↓</a>':'')+'</div>'
   +'</article>';
}
function renderList(){
  const grid=$('#skill-list');if(!grid)return;
  const list=filtered(),active=conditions();
  const repos=new Set(list.map(i=>i.repository)).size;
  $('#skill-results').textContent=items.length+'件中 '+list.length+'件を表示'+(repos!==list.length?'（'+repos+'リポジトリ）':'')+(active.length?' ／ '+active.map(a=>a[1]).join(' ／ '):'');
  const chips=$('#skill-active');if(chips)chips.innerHTML=active.map(([key,label])=>'<button type="button" data-remove="'+key+'" aria-label="'+esc(label)+'を解除">'+esc(label)+' <span aria-hidden="true">×</span></button>').join('')+(active.length>1?'<button type="button" data-clear-filters>すべて解除</button>':'');
  if(list.length){grid.innerHTML=list.map(card).join('');return}
  // Explain which single condition blocks the results, so the reader can remove just that one.
  const hints=active.map(([key,label])=>[key,label,filtered(key).length]).filter(x=>x[2]>0);
  grid.innerHTML='<div class="effect-empty"><p><b>条件に合うスキルはありません。</b></p><p>いまの条件：'+esc(active.map(a=>a[1]).join(' ／ '))+'</p>'+(hints.length?'<ul>'+hints.map(([key,label,n])=>'<li><button type="button" data-remove="'+key+'">「'+esc(label)+'」を外す</button>と'+n+'件</li>').join('')+'</ul>':'')+'<button type="button" class="button outline" data-clear-filters>条件をすべて解除して'+items.length+'件を表示</button></div>';
}
function syncControls(){
  for(const b of all('[data-need]'))b.setAttribute('aria-pressed',String(b.dataset.need===state.need));
  const set=(id,v)=>{const el=$(id);if(el&&'value' in el)el.value=v};
  set('#skill-query',state.query);set('#skill-need',state.need);set('#skill-format',state.format);set('#skill-tag',state.tag);
}
// The select lists tags shared by two or more skills; a single-skill tag chosen from a card is added while selected.
function fillTags(){
  const select=$('#skill-tag');if(!select)return;
  const shown=allTags.filter(([t,n])=>n>1||t===state.tag);
  select.innerHTML=shown.length?'<option value="all">すべて</option>'+shown.map(([t,n])=>'<option value="'+esc(t)+'">'+esc(tagLabel(t))+'（'+n+'）</option>').join(''):'<option value="all">記録なし</option>';
  select.disabled=!shown.length;
}
function update(){fillTags();syncControls();renderList()}
function setupControls(){
  const needSelect=$('#skill-need');if(needSelect)needSelect.innerHTML='<option value="all">すべて</option>'+NEEDS.map(n=>'<option value="'+n.id+'">'+esc(n.label)+'</option>').join('');
  for(const el of all('[data-need-count]')){const n=items.filter(i=>matchesNeed(i,el.dataset.needCount)).length;el.textContent=n+'件'}
  $('#skill-query')?.addEventListener('input',e=>{state.query=e.target.value;renderList()});
  for(const [id,key] of [['#skill-need','need'],['#skill-format','format'],['#skill-tag','tag']])$(id)?.addEventListener('change',e=>{state[key]=e.target.value||'all';update()});
  const note=$('#skill-data-note');if(note){const recorded=items.filter(i=>i.effect).length;note.textContent=effects.missing?'効果の記録データを読み込めませんでした。各スキルは掲載時の紹介文だけを表示しています。':recorded<items.length?'効果の記録があるのは'+items.length+'件中'+recorded+'件です。記録のないスキルは「未記録」と表示しています。':'';note.hidden=!note.textContent}
}

// --- Float player. Effects for the open case follow every page change.
function stop(){playing=false;clearTimeout(timer);timer=null;$('#case-play').textContent='▶ 再生'}
function fit(){
  const stage=$('#case-stage'),frame=stage?.querySelector('iframe');if(!stage||!current)return;
  const width=current?.preview_canvas?.width||1280,height=current?.preview_canvas?.height||720;
  stage.style.aspectRatio=width+' / '+height;
  if(!frame)return;
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
// Scroll decks acknowledge go() before scrolling and may then report the old page.
// Keep the startup target through delayed reports; any user navigation cancels it.
function clearTarget(){target=null;clearTimeout(targetTimer);targetTimer=null}
function reported(index){
  if(target!==null){if(index===target)return false;send();return true}
  return false;
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
function showPage(){
  $('#case-counter').textContent=playbackCounter(current,page);
  $('#case-prev').disabled=page===0;$('#case-next').disabled=page===current.page_count-1;
  $('#case-note').textContent=current.notes[page]||'';
  for(const b of $('#case-pages').querySelectorAll('button'))b.setAttribute('aria-current',String(Number(b.dataset.page)===page));
  effectPanel();
}
function nativeSync(frame){
  const doc=frame.contentDocument;if(!doc||!current)return;
  const config=nativeDOM[current.id];if(!config)return;
  const sections=[...doc.querySelectorAll(config[0])],idx=sections.findIndex(s=>s.matches(config[1]));
  if(idx<0||idx>=current.page_count||reported(idx)||idx===page)return;page=idx;showPage();
}
function effectPanel(){
  let panel=$('#case-effect');
  if(!panel&&document.createElement){panel=document.createElement('section');panel.id='case-effect';panel.className='case-effect';panel.setAttribute('aria-label','このスキルの効果');$('#case-controls')?.after(panel)}
  if(!panel||!current)return;
  const i=currentItem,detail=i?detailUrl(i):recipeUrl(current);
  const back='<a class="case-effect-link" href="'+esc(detail)+'">効果と使い方を見る →</a>';
  if(!i?.effect){panel.innerHTML='<div class="case-effect-skill"><p class="case-effect-kicker">スキル</p><p class="case-effect-name">'+esc(i?skillName(i):current.repository)+'</p><p class="case-effect-change">効果の記録はまだありません。</p></div>'+back;return}
  const own=i.case?.id===current.id&&i.caseMatches,playable=own?i.pages.filter(p=>p.valid&&!p.supplemental):[],here=playable.filter(p=>p.index===page),marks=playable.filter((p,n,all)=>all.findIndex(q=>q.index===p.index)===n);
  const ordinal=playbackOrdinal(current,page);
  const pageHtml=here.length?here.map(p=>'<p class="case-effect-label">'+esc(pageHeading(current,p))+'で見る箇所</p><p class="case-effect-inspect">'+esc(p.inspect||'説明は未記録です。')+'</p>'+(p.rule?'<p class="case-effect-rule"><span>スキルの指示</span>'+esc(p.rule)+'</p>':'')).join(''):'<p class="case-effect-label">'+esc(ordinal)+'</p><p class="case-effect-inspect">'+(own?'この'+unitWord(current)+'の見る箇所は記録されていません。':'この作例の見る箇所は記録されていません。')+'</p>';
  const jumps=marks.length?'<p class="case-effect-jumps"><span>見る箇所のある'+unitWord(current)+'</span>'+marks.map(p=>'<button type="button" data-page="'+p.index+'" aria-current="'+String(p.index===page)+'" aria-label="'+esc(playbackOrdinal(current,p.index))+'へ">'+(p.index+1)+'</button>').join('')+'</p>':'';
  panel.innerHTML='<div class="case-effect-skill"><p class="case-effect-kicker">スキル</p><p class="case-effect-name">'+esc(skillName(i))+'</p>'+(text(i.effect.change)?'<p class="case-effect-change">'+esc(text(i.effect.change))+'</p>':'')+'</div><div class="case-effect-page">'+pageHtml+jumps+'</div>'+(own&&i.effect.demonstration?.cautions?.length?'<div class="effect-cautions">'+i.effect.demonstration.cautions.map(s=>'<p>'+esc(s)+'</p>').join('')+'</div>':'')+back;
}
function go(n,keepTarget){
  if(!current)return;page=Math.max(0,Math.min(n,current.page_count-1));
  if(!keepTarget)clearTarget();
  if(IMAGE_PREVIEW_KINDS.includes(current.preview_kind))$('#case-stage').innerHTML='<img src="'+esc(imagePath(current,page))+'" alt="'+esc(current.titles[page])+'">';
  else send();
  showPage();
}
function open(id,button,startPage,effectKey){
  const c=caseById.get(id);if(!c)return;
  if(!dialog.open)trigger=button||document.activeElement;
  stop();nativeObserver?.disconnect();nativeObserver=null;clearTarget();current=c;page=0;
  currentItem=items.find(i=>i.key===effectKey)||items.find(i=>i.case?.id===c.id)||itemFor(items,c.repository,c.id);
  const start=Number.isInteger(startPage)&&startPage>0&&startPage<c.page_count?startPage:0;
  dialog.classList.toggle('square-preview',Boolean(squareClass(c)));
  $('#case-owner').textContent=(currentItem?'スキル：'+skillName(currentItem)+' / ':'')+c.repository;
  $('#case-title').textContent='作例：'+c.title;
  $('#case-state').textContent=c.preview_notice||(c.format==='pptx'?(c.editability==='raster_slides'?'原典で生成・組版した画像のPPTX / 発表ノート付き・ページ内の文字と図は画像です':'完成PPTXをPowerPointで出力したプレビュー / 文字・図形・ノートを編集できます'):c.format==='pdf'?'完成PDFのプレビュー / 制作ソースから編集できます':'元のスキルを適用したHTML / スライド固有の演出を再生');
  let licenseNotice=$('#case-license');if(!licenseNotice){licenseNotice=document.createElement('p');licenseNotice.id='case-license';licenseNotice.className='case-sample-note';$('#case-state').after(licenseNotice)}
  licenseNotice.textContent=profileByRepo.get(c.repository)?.license_notice_ja||'';licenseNotice.hidden=!licenseNotice.textContent;
  $('#case-download').href=c.artifact_download;
  $('#case-download').download=caseDownloadName(c,c.artifact_download);
  $('#case-download').textContent=c.format==='pptx'?'PowerPointをダウンロード ↓':c.format==='pdf'?'PDFをダウンロード ↓':/\.html?(?:[?#]|$)/i.test(c.artifact_download)?'Webスライドをダウンロード ↓':'Webスライド一式をダウンロード ↓';
  for(const [id,path,label,draft] of [['case-pptx',c.pptx_download===c.artifact_download?null:c.pptx_download,'PowerPoint版 ↓'],['case-pdf',c.pdf_download===c.artifact_download?null:c.pdf_download,'PDF ↓'],['case-draft',c.draft_download,'変更前のPowerPoint ↓',true]]){
    let link=$('#'+id);if(!link){link=document.createElement('a');link.id=id;link.className='button outline';link.setAttribute('download','');$('#case-download').after(link);}
    link.hidden=!path;link.href=path||'#';link.textContent=label;if(path)link.download=caseDownloadName(draft?{...c,title:c.title.replace(/[。．. ]+$/,'')+'（変更前）'}:c,path);
  }
  $('#case-make').href=currentItem?detailUrl(currentItem):recipeUrl(c);
  $('#case-make').textContent='スキルの効果と使い方 →';
  $('#case-origin').href='https://github.com/'+c.repository+'/tree/'+c.upstream_commit;
  const comparison=caseById.get(c.compare);
  $('#case-compare').hidden=!comparison;
  if(comparison){$('#case-compare').dataset.openCase=comparison.id;$('#case-compare').href=recipeUrl(comparison);$('#case-compare').textContent=c.comparison_label||(c.format==='pptx'?'同じ入力のWeb版と比べる ↗':'同じ入力のPPTX版と比べる ↗')}
  $('#case-note').hidden=true;$('#case-notes').setAttribute('aria-expanded','false');
  $('#case-pages').innerHTML=c.titles.map((t,i)=>'<button type="button" data-page="'+i+'" aria-label="'+playbackOrdinal(c,i)+' '+esc(t)+'">'+(c.preview_kind==='html'&&!c.pages?'':'<img src="'+esc(imagePath(c,i))+'" alt="">')+'<span>'+String(i+1).padStart(2,'0')+' '+esc(t)+'</span></button>').join('');
  const skillLink=$('#case-skill');if(skillLink){const download=caseRecipes[c.id]?.skill_download||entryByRepo.get(c.repository)?.skill_download;skillLink.hidden=!download;skillLink.href=download||'#'}
  if(c.preview_kind==='html'){
    // Set the requested page before the frame loads; load → send() then carries it into the deck.
    if(start){target=start;targetTimer=setTimeout(clearTarget,6000)}
    page=start;
    const frame=document.createElement('iframe');frame.src=previewUrl(c,c.preview);frame.title=c.title;frame.setAttribute('sandbox','allow-scripts allow-same-origin');frame.addEventListener('load',()=>{fit();send();if(target!==null)for(const wait of [300,900,1800])setTimeout(()=>{if(target!==null&&current===c)send()},wait);const doc=frame.contentDocument;if(!doc)return;doc.addEventListener('pointerdown',clearTarget,true);doc.addEventListener('keydown',e=>{clearTarget();if(e.key==='Escape'){e.preventDefault();dialog.close()}},true);const config=nativeDOM[c.id],slides=config&&doc.querySelector(config[2]);if(slides){nativeObserver=new MutationObserver(()=>nativeSync(frame));nativeObserver.observe(slides,{attributes:true,childList:true,subtree:true,attributeFilter:['class']});nativeSync(frame)}});$('#case-stage').replaceChildren(frame);
    go(start,true);
  }else go(start);
  if(!dialog.open)dialog.showModal();fit();
  // Bring the opened page into the horizontal strip without scrolling the dialog away from the stage.
  const strip=$('#case-pages'),shown=strip.querySelector('[aria-current="true"]');if(shown&&start)strip.scrollLeft+=shown.getBoundingClientRect().left-strip.getBoundingClientRect().left-12;
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
  if(!c){root.innerHTML='<p>制作事例が見つかりません。<a href="./#skills">スキル一覧へ戻る</a></p>';return}
  location.replace(c.guide+'#example-'+encodeURIComponent(c.id));
}
document.addEventListener('click',e=>{
  const opener=e.target.closest('[data-open-case]');if(opener){e.preventDefault();open(opener.dataset.openCase,opener,opener.dataset.openPage===undefined?0:Number(opener.dataset.openPage),opener.dataset.effect);return}
  const pageButton=e.target.closest('[data-page]');if(pageButton){stop();go(Number(pageButton.dataset.page));return}
  const need=e.target.closest('[data-need]');if(need){state.need=need.dataset.need===state.need?'all':need.dataset.need;update();if(need.dataset.scroll!==undefined)$('#skills')?.scrollIntoView({block:'start'});return}
  const tag=e.target.closest('[data-tag]');if(tag){state.tag=tag.dataset.tag===state.tag?'all':tag.dataset.tag;update();$('#skill-tag')?.focus();return}
  const remove=e.target.closest('[data-remove]');if(remove){const key=remove.dataset.remove;state[key]=key==='query'?'':'all';update();$('#skill-query')?.focus();return}
  if(e.target.closest('[data-clear-filters]')){Object.assign(state,{query:'',need:'all',format:'all',tag:'all'});update();$('#skill-query')?.focus()}
});
$('#case-close').onclick=()=>dialog.close();$('#case-prev').onclick=()=>{stop();go(page-1)};$('#case-next').onclick=()=>{stop();go(page+1)};$('#case-play').onclick=play;
$('#case-notes').onclick=()=>{$('#case-note').hidden=!$('#case-note').hidden;$('#case-notes').setAttribute('aria-expanded',String(!$('#case-note').hidden))};
$('#case-fullscreen').onclick=()=>{dialog.classList.toggle('expanded');$('#case-fullscreen').textContent=dialog.classList.contains('expanded')?'元の大きさへ ↙':'大きく見る ↗';fit()};
dialog.addEventListener('close',()=>{stop();clearTarget();nativeObserver?.disconnect();nativeObserver=null;$('#case-stage').replaceChildren();dialog.classList.remove('expanded');$('#case-fullscreen').textContent='大きく見る ↗';trigger?.focus()});
dialog.addEventListener('click',e=>{if(e.target===dialog){const b=dialog.getBoundingClientRect();if(e.clientX<b.left||e.clientX>b.right||e.clientY<b.top||e.clientY>b.bottom)dialog.close()}});
document.addEventListener('keydown',e=>{if(!dialog.open)return;if(e.key==='Escape'){e.preventDefault();dialog.close()}if(['ArrowRight','ArrowLeft'].includes(e.key)){e.preventDefault();stop();go(page+(e.key==='ArrowRight'?1:-1))}});
window.addEventListener('message',e=>{const frame=$('#case-stage iframe');if(!frame||e.source!==frame.contentWindow||e.origin!==location.origin)return;if(e.data?.type==='yebisu-close')dialog.close();if(e.data?.type==='yebisu-page'&&Number.isInteger(e.data.index)){if(reported(e.data.index))return;page=Math.max(0,Math.min(e.data.index,current.page_count-1));showPage()}});
new ResizeObserver(fit).observe($('#case-stage'));window.addEventListener('resize',fit);
setupControls();update();await detail();
