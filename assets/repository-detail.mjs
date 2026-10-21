import {caseDownloadName} from './download-name.mjs';
import {caseCountLabel,playbackOrdinal} from './case-units.mjs';
import {esc,lines,text,safePath,formatLabel,loadSkillEffects,buildSkillItems,itemFor,skillName,detailUrl,upstreamUrl,previewUrl,sourceLabel} from './skill-effects.mjs';
const root=document.querySelector('#repository-detail');
const json=async path=>{const r=await fetch(path,{cache:'no-store'});if(!r.ok)throw Error(path);return r.json()};
function installProofViewer(host){
 const links=[...host.querySelectorAll('a[data-proof-image]')];if(!links.length)return;
 const dialog=document.createElement('dialog');dialog.className='effect-proof-dialog';dialog.setAttribute('aria-labelledby','effect-proof-title');
 dialog.innerHTML='<header><h2 id="effect-proof-title"></h2><button type="button" class="button outline" aria-label="検証画像を閉じる">閉じる ×</button></header><nav class="repo-code-actions effect-proof-actions" aria-label="検証資料の取得"><a class="button outline" data-native download hidden>この検証のPPTXを取得 ↓</a><a class="button outline" data-save download>検証画像を保存 ↓</a></nav><div class="effect-proof-images"><figure data-input hidden><img alt=""><figcaption>入力の図</figcaption></figure><figure data-output><img alt=""><figcaption>検証画像</figcaption></figure></div><dl class="effect-proof-context"><dt>見る箇所</dt><dd data-inspect></dd><dt>スキルの指示</dt><dd data-rule></dd></dl>';
 document.body.append(dialog);let opener=null;
 dialog.querySelector('button').addEventListener('click',()=>dialog.close());
 dialog.addEventListener('close',()=>{opener?.focus();});
 for(const link of links)link.addEventListener('click',event=>{
  if(event.ctrlKey||event.metaKey||event.shiftKey||event.altKey||typeof dialog.showModal!=='function')return;
  event.preventDefault();opener=link;
  const input=link.dataset.proofInput||'',label=link.dataset.proofLabel||'検証画像';
  dialog.querySelector('h2').textContent=label;
  const before=dialog.querySelector('[data-input]');before.hidden=!input;
  if(input){before.querySelector('img').src=input;before.querySelector('img').alt=label+'の入力';before.querySelector('figcaption').textContent=link.dataset.proofInputLabel||'入力の図';}
  const after=dialog.querySelector('[data-output]');after.querySelector('img').src=link.href;after.querySelector('img').alt=label;
  after.querySelector('figcaption').textContent=input?(link.dataset.proofOutputLabel||'復元した図'):'検証画像';
  dialog.querySelector('[data-inspect]').textContent=link.dataset.proofInspect||'この画像の文言・図形を確認します。';
  dialog.querySelector('[data-rule]').textContent=link.dataset.proofRule||'記録なし';
  dialog.querySelector('[data-save]').href=link.href;
  const native=dialog.querySelector('[data-native]');native.hidden=!link.dataset.proofArtifact;
  if(!native.hidden){native.href=link.dataset.proofArtifact;native.textContent=link.dataset.proofArtifactLabel||'この検証のPPTXを取得 ↓';}
  dialog.showModal();
 });
}
function requestComposer({section,caseStudy,official,skillDownload,fontKit,item}){
 const desiredCount=caseStudy.scene_count||caseStudy.page_count;
 const fontSelect=section.querySelector('#repository-font'),field=section.querySelector('#repository-prompt'),status=section.querySelector('#repository-copy-state');
 section.querySelector('h2').textContent='自分の原稿で依頼文を作る';
 section.querySelector('.case-sample-note').textContent='スキル本文と一式ZIPをAIへ添付し、ここで作った依頼文も渡してください。'+(/\.pptx$/i.test(caseStudy.input||'')?' 変換したいPowerPointも添付し、原稿欄には変更したい点を書きます。':'');
 const inputs=document.createElement('div');inputs.className='repository-request-inputs';
 inputs.innerHTML='<label for="repository-topic">何の資料を作る？</label><input id="repository-topic" placeholder="例：新しく入るメンバーへの引き継ぎ"><label for="repository-content">自分の原稿・伝えたいこと</label><textarea id="repository-content" placeholder="使いたい情報を貼り付けてください。原典が論文・画像・PPTXなどを必須にする場合、それは別に添付します。"></textarea><div class="repository-request-options"><div><label for="repository-audience">読み手・目的</label><input id="repository-audience" placeholder="例：初めて担当する人が、次の作業を始められる"></div><div><label for="repository-pages">希望枚数</label><input id="repository-pages" type="number" min="1" max="100" value="'+esc(desiredCount)+'"></div></div>';
 if(caseStudy.page_unit==='段階')inputs.querySelector('label[for=repository-pages]').textContent=caseStudy.scene_count?'希望する場面数':'希望する段階数';
 fontSelect.previousElementSibling.before(inputs);
 const assemble=document.createElement('button');assemble.className='button outline';assemble.type='button';assemble.id='repository-assemble';assemble.textContent='この内容で依頼文を組み立てる ↓';
 field.before(assemble);
 const label=document.createElement('label');label.htmlFor='repository-prompt';label.textContent='AIへ渡す依頼文（編集できます）';field.before(label);
 const used=document.createElement('details');used.className='repository-used-prompt';
 const summary=document.createElement('summary');summary.textContent='この作例を作った依頼文';
 const raw=document.createElement('pre');raw.textContent=caseStudy.prompt_text;used.append(summary,raw);section.append(used);
 const fontInstruction=()=>{
  const f=fontKit.presets.find(x=>x.id===fontSelect.value);
  return f?'書体：見出し '+f.heading+'、本文 '+f.body+'、英数字 '+f.latin+(f.code?'、コード '+f.code:'')+'。'+f.instruction+' 公式配布のフォントと原文OFLを使う。':'書体：'+(Array.isArray(caseStudy.font_families)?caseStudy.font_families.join('、'):caseStudy.font_families||'添付したスキルと作例の指定')+'。'+(caseStudy.font_notice_ja||'入手元と利用・再配布条件は添付したスキルに従う。');
 };
 const feature=item?.effect?'使うスキルの機能：'+skillName(item)+(text(item.effect.change)?'（'+text(item.effect.change)+'）':'')+'\n':'';
 const compose=()=>{
  const topic=inputs.querySelector('#repository-topic').value.trim()||'［作りたい資料の題材］';
  const content=inputs.querySelector('#repository-content').value.trim()||'［自分の原稿をここに入れる。原典が必要とする論文・画像・PPTX等は別途添付する］';
  const audience=inputs.querySelector('#repository-audience').value.trim()||'［読み手と、この資料で伝えたいこと］';
  const pages=Number(inputs.querySelector('#repository-pages').value);
  const count=Number.isInteger(pages)&&pages>=1&&pages<=100?pages:desiredCount;
  const structure=caseStudy.page_unit==='段階'?(caseStudy.scene_count?'希望する場面数：'+count+'場面。各場面の中で、一度の操作につき一つの考えを段階表示する。':'希望する段階数：'+count+'段階。原典の共通画面と同じ図形を使い、一度の操作につき一つの考えを見せる。'):'希望枚数：'+count+'枚。固定の版式など原典の制約があれば、その方式に合わせる。';
  const output=caseStudy.format==='pptx'?'PowerPoint（PPTX）と制作ソース。文字・図などを編集できる範囲は、この方式に合わせて明記する。':caseStudy.format==='pdf'?'PDFと原典方式の制作ソース。':'ブラウザーで再生できるWebスライドと制作ソース。';
  field.value='添付の日本語スキル「'+skillDownload.split('/').pop()+'」を使い、次の内容で日本語の資料を完成させてください。\n\n題材：'+topic+'\n読み手・目的：'+audience+'\n'+structure+'\n\n原稿：\n'+content+'\n\n'+feature+'参考にする作例：「'+caseStudy.title+'」\n'+(caseStudy.style?'見た目：'+caseStudy.style+'\n':'')+fontInstruction()+'\n原稿の意味・数値・参照関係を保ち、原典が定める文字量・改行・配置の規則に従ってください。復元・変換では元の文言や構造を優先してください。\n\n使う原典：'+official+'\n原典SKILLにある必要な入力と、固有テンプレート・生成器・変換工程を使う。制作一式ZIP内の実装や、固定原典の参照ファイルを利用する。必須の入力が足りなければ、その内容を確認してから制作する。\n原稿の事実・仮説・仮の数字を区別し、根拠や実測値を補完しない。\n\n完成物：'+output+'\n原典で必須の生成・検査を実行し、全ページを描画して本文・図表・数式・日本語の表示を確認してください。問題を修正して再生成し、実施した確認と残る制約を記録してください。';
  status.textContent='依頼文を組み立てました。必要なら下で編集できます。';
 };
 assemble.addEventListener('click',compose);
 fontSelect.addEventListener('change',()=>{const f=fontKit.presets.find(x=>x.id===fontSelect.value);section.querySelector('#repository-font-recipe').textContent=(f?f.heading+' / '+f.body+' / '+f.latin+(f.code?' / コード '+f.code:''):'作例と同じ書体')+'。選んだ書体は「組み立てる」で依頼文へ入ります。';});
 section.querySelector('#repository-copy').addEventListener('click',async()=>{try{await navigator.clipboard.writeText(field.value);status.textContent='依頼文をコピーしました。スキル本文と一緒にAIへ渡してください。';}catch{field.focus();field.select();status.textContent='依頼文を選択しました。Ctrl+Cでコピーしてください。';}});
 compose();status.textContent='入力はこの画面の中だけで使います。依頼文をコピーして、使っているAIへ。';
}
const list=v=>{const xs=lines(v);return xs.length?'<ul>'+xs.map(x=>'<li>'+esc(x)+'</li>').join('')+'</ul>':''};
const missing=what=>'<p class="effect-missing">'+what+'は未記録です。</p>';
const section=(id,n,title,body)=>'<section class="effect-section" id="'+id+'" aria-labelledby="'+id+'-title"><h2 id="'+id+'-title"><span class="effect-step">'+n+'</span>'+title+'</h2>'+body+'</section>';
if(root){
 try{
  const [profiles,cases,product,fontKit,effects]=await Promise.all([...['data/repository-guides.json','data/case-studies.json','data/product-collection.json','data/oss-font-kit.json'].map(json),loadSkillEffects()]);
  const params=new URLSearchParams(location.search),repo=params.get('repo');
  const p=profiles.find(x=>x.repository===repo),entry=product.entries.find(e=>e.repository===repo);
  if(!p){root.innerHTML='<p>スキルが見つかりません。<a href="./#skills">スキル一覧へ戻る</a></p>'}
  else{
   const items=buildSkillItems({entries:product.entries,cases,activeIds:product.active_case_ids,effects});
   const requestedCase=params.get('case'),effectIndex=params.has('effect')?Number(params.get('effect')):undefined;
   const item=itemFor(items,repo,requestedCase,effectIndex)||{repository:repo,entry,effect:null,case:null,pages:[],tags:[],others:[],index:0,key:repo+'#0'};
   const siblings=items.filter(i=>i.repository===repo);
   const e=item.effect,demo=e?.demonstration||{};
   const works=cases.filter(c=>c.repository===repo).sort((a,b)=>Number(b.id===item.case?.id)-Number(a.id===item.case?.id)||Number(b.id===entry?.featured_case_id)-Number(a.id===entry?.featured_case_id));
   const first=works.find(c=>c.id===requestedCase)||item.case||works[0],proofCase=item.case,recipe=product.case_recipes?.[first?.id];
   const recipeWorks=works.filter(c=>items.some(i=>i.case?.id===c.id&&i.caseMatches)),reusableFirst=recipeWorks.some(c=>c.id===first?.id);
   const commit=recipe?.upstream_commit||first?.upstream_commit||p.upstream_commit;
   const official='https://github.com/'+repo+(commit?'/tree/'+commit:'');
   const recipeHref=c=>'repository.html?repo='+encodeURIComponent(repo)+'&case='+encodeURIComponent(c.id);
   const skillDownload=recipe?.skill_download||entry?.skill_download;
   const name=skillName(item),[owner,repoName]=repo.split('/');
   document.title=name+'｜スキルの効果と使い方';
   const refs=(p.source_refs||[]).map(r=>typeof r==='string'?(r.startsWith('https://')?{path:new URL(r).pathname.split('/').pop()||'GitHub原典',url:r}:{path:r,url:'https://github.com/'+repo+'/blob/'+p.upstream_commit+'/'+r}):r);
   const evaluationOnly=['excluded_host_runtime_evaluation_only','excluded_required_evaluation_runtime'].includes(p.product_status);
   const bundle=evaluationOnly?null:(recipe?.fork_download||first?.fork_download||entry?.fork_download);
   const upstreamCommit=e?.upstream?.commit||proofCase?.upstream_commit||p.upstream_commit;
   const skillPath=safePath(e?.upstream?.skill_path)||(p.skill_paths||[])[0]||'';
   const skillUrl=/^https:\/\/github\.com\//i.test(safePath(e?.upstream?.url))?safePath(e.upstream.url):skillPath&&upstreamCommit?'https://github.com/'+repo+'/blob/'+upstreamCommit+'/'+skillPath:upstreamUrl(item);
   const licensePath=(p.license_paths||[])[0],licenseUrl=licensePath&&p.upstream_commit?'https://github.com/'+repo+'/blob/'+p.upstream_commit+'/'+licensePath:'';
   const nc=/非商用|NC-/.test((p.license_notice_ja||'')+(entry?.license_notice_ja||'')+(p.license||''));

   const head='<a class="text-link" href="./#skills">← スキル一覧へ</a><header class="repo-top effect-top"><p class="repo-owner"><a href="https://github.com/'+esc(repo)+'" target="_blank" rel="noopener noreferrer">'+esc(owner)+' / <b>'+esc(repoName)+'</b> ↗</a><span>'+esc(p.license||entry?.license||'個別条件')+'</span>'+(nc?'<span class="effect-warning">非商用条件あり</span>':'')+'</p><h1>'+esc(name)+'</h1>'
    +(e?(text(e.change)?'<p class="repo-desc">'+esc(text(e.change))+'</p>':''):'<p class="effect-missing">このスキルの効果・入力・見る箇所の記録はまだありません。以下は掲載時の紹介文と制作記録です。</p><p class="repo-desc">'+esc(entry?.description_ja||p.summary_ja)+'</p>')
    +(siblings.length>1?'<p class="effect-siblings">このリポジトリで記録した機能：'+siblings.map(s=>s===item?'<b>'+esc(skillName(s))+'</b>':'<a href="'+esc(detailUrl(s))+'">'+esc(skillName(s))+'</a>').join(' ／ ')+'</p>':'')
    +'<div class="repo-code-actions">'+(entry?'<a class="button primary" href="'+esc(skillDownload)+'" download>日本語スキル本文 ↓</a>':'')+(bundle?'<a class="button outline" href="'+esc(bundle)+'" download>原典・素材の一式ZIP ↓</a>':'')+'<a class="text-link" href="'+esc(skillUrl)+'" target="_blank" rel="noopener noreferrer">固定原典のSKILL ↗</a></div><p class="case-sample-note">スキル本文はAIへ渡す日本語の指示です。テンプレート・生成器・原文LICENSEは一式ZIPか固定原典にあります。</p>'
    +'<nav class="effect-toc" aria-label="このページの順序"><a href="#problem">1 改善すること</a><a href="#does">2 スキルがすること</a><a href="#io">3 入力と完成物</a><a href="#used">4 作例で使った機能</a><a href="#pages">5 見る箇所</a><a href="#apply">6 自分の資料へ</a></nav></header>';

   const s1=section('problem',1,'何を改善するか',e?((text(e.problem)?'<p class="effect-lead">'+esc(text(e.problem))+'</p>':missing('改善する問題'))+(lines(e.when_to_use).length?'<h3>使う場面</h3>'+list(e.when_to_use):'')):missing('改善する問題'));
   const s2=section('does',2,'スキルがすること',(e&&text(e.change)?'<p class="effect-lead">'+esc(text(e.change))+'</p>':missing('スキルの効果'))
    +(text(e?.upstream?.principle)?'<div class="effect-upstream"><p class="effect-label">原典SKILLの指示</p><p>'+esc(text(e.upstream.principle))+'</p></div>':'')
    +'<p class="effect-source"><a href="'+esc(skillUrl)+'" target="_blank" rel="noopener noreferrer">'+esc(skillPath||'GitHub原典')+(upstreamCommit?' @ '+esc(String(upstreamCommit).slice(0,7)):'')+' ↗</a>（固定した原典）</p>');
   // Constraints already listed under "この作例では確認していないこと" are shown once, there.
   const notShown=new Set(item.caseMatches?lines(demo.not_demonstrated):[]),constraints=lines(e?.constraints).filter(x=>!notShown.has(x));
   const io=e?'<div class="effect-io"><div><h3>渡すもの</h3>'+(list(e.input)||missing('入力'))+'</div><div><h3>受け取るもの</h3>'+(list(e.output)||missing('完成物'))+'</div></div>':missing('入力と完成物');
   const s3=section('io',3,'渡すものと受け取るもの',io
    +(first?'<p class="effect-note">この作例で渡した入力：<a href="'+esc(first.input)+'">入力原稿</a> · <a href="'+esc(first.input_data)+'">入力の条件</a></p>':'')
    +(constraints.length?'<h3>使う前に確認する条件</h3>'+list(constraints):e&&lines(e.constraints).length?'':'<h3>使う前に確認する条件</h3><p class="effect-missing">スキル固有の制約は未記録です。下の環境と利用条件を確認してください。</p>')
    +'<p class="effect-note">利用条件：'+esc(p.license||entry?.license||'個別条件')+(licenseUrl?' · <a href="'+esc(licenseUrl)+'" target="_blank" rel="noopener noreferrer">原文LICENSE ↗</a>':'')+' · <a href="licenses.html">原典・利用条件の一覧</a></p>'
    +'<h3>必要な環境</h3>'+list(p.requirements)
    +'<details class="effect-details"><summary>制作方法と実行コマンド</summary><p>'+esc(first?.method||p.method_ja||p.execution_type)+'</p>'+(p.steps?.length?list(p.steps):'')+(p.commands?.length?'<pre>'+esc(p.commands.map(c=>typeof c==='string'?c:JSON.stringify(c)).join('\n\n'))+'</pre>':'')+'</details>');

   const caseHead=c=>'<h3 class="effect-case-title">作例：'+esc(c.title)+'</h3><p class="effect-case-meta">'+formatLabel(c)+' · '+esc(caseCountLabel(c))+(c.sample_notice?' · '+esc(c.sample_notice):'')+'</p>';
   const s4=section('used',4,'この作例で使った機能',(proofCase?caseHead(proofCase):'<p class="effect-missing">掲載中の作例はありません。</p>')
    +(first&&proofCase&&first.id!==proofCase.id?'<p class="effect-note">選択中の作例「'+esc(first.title)+'」には見る箇所の記録がありません。記録は上の作例にあります。</p>':'')
    +(e&&!item.caseMatches?'<p class="effect-missing">効果記録の作例「'+esc(item.recordedCaseId||'未記入')+'」が掲載データにありません。記録された機能とページはこの作例に当てはめていません。</p>':'')
    +(e&&!item.caseMatches?'':(text(demo.summary)?'<p>'+esc(text(demo.summary))+'</p>':'')
    +(lines(demo.cautions).length?'<div class="effect-cautions">'+list(demo.cautions)+'</div>':'')
    +'<div class="effect-scope"><div><h4>この作例で使った機能</h4>'+(list(demo.applied_features)||missing('使った機能'))+'</div><div><h4>この作例では確認していないこと</h4>'+(list(demo.not_demonstrated)||missing('確認していない機能'))+'</div></div>')
    +(item.caseMatches&&item.sources?.length?'<p class="effect-note">制作の根拠：'+item.sources.map(s=>'<a href="'+esc(s)+'"'+(/^https:/i.test(s)?' target="_blank" rel="noopener noreferrer"':'')+'>'+esc(sourceLabel(s))+'</a>').join(' · ')+'</p>':'')
    +'<p class="effect-boundary">原典には、ここに挙げていない機能もあります。全体は<a href="'+esc(skillUrl)+'" target="_blank" rel="noopener noreferrer">固定原典のSKILL</a>とREADMEで確認してください。</p>');

   let pagesBody='';
   const shown=item.caseMatches?item.pages:[];
   if(proofCase&&shown.length){
    pagesBody='<ol class="effect-pages">'+shown.map(pg=>{
     const ord=pg.supplemental?(pg.label||'検証画像'):pg.valid?playbackOrdinal(proofCase,pg.index):'記録の番号 '+esc(pg.index);
     const open='data-open-case="'+esc(proofCase.id)+'" data-open-page="'+pg.index+'" data-effect="'+esc(item.key)+'"';
     const proofName=pg.proofIsImage?'ページ画像':'制作ソース',proofLink=pg.proof?(/^https:/i.test(pg.proof)?'<a href="'+esc(pg.proof)+'" target="_blank" rel="noopener noreferrer">'+proofName+' ↗</a>':'<a href="'+esc(pg.proof)+'">'+proofName+'</a>'):'';
     const image=pg.image?'<img src="'+esc(pg.image)+'" alt="" loading="lazy">':'<span class="effect-page-noimage">このページの画像はありません<br>再生して確認</span>';
     const proofAttrs=' data-proof-image data-proof-label="'+esc(pg.title||ord)+'" data-proof-input="'+esc(pg.inputImage)+'" data-proof-input-label="'+esc(pg.inputLabel)+'" data-proof-output-label="'+esc(pg.outputLabel)+'" data-proof-artifact="'+esc(pg.artifact)+'" data-proof-artifact-label="'+esc(pg.artifactLabel)+'" data-proof-inspect="'+esc(pg.inspect)+'" data-proof-rule="'+esc(pg.rule)+'"';
     const thumbnail=pg.supplemental?'<a class="effect-page-image" href="'+esc(pg.proof)+'"'+proofAttrs+' aria-label="'+esc(pg.title||ord)+'の検証画像を開く">'+image+'</a>':'<button type="button" class="effect-page-image" '+open+' aria-label="'+esc(ord)+'を開く">'+image+'</button>';
     const action=pg.supplemental?'<a class="button outline" href="'+esc(pg.proof)+'"'+proofAttrs+'>検証画像を見る →</a>':'<button type="button" class="button outline" '+open+'>'+esc(ord)+'を見る ▶</button>';
     const inputLink=pg.inputImage?'<a href="'+esc(pg.inputImage)+'" data-proof-image data-proof-label="'+esc(pg.title||ord)+'の入力" data-proof-inspect="'+esc(pg.inspect)+'" data-proof-rule="'+esc(pg.rule)+'">入力画像を見る</a>':'';
     return '<li class="effect-page"'+(pg.valid?' id="'+esc(pg.anchor)+'"':'')+'>'+(pg.valid?thumbnail:'<div class="effect-page-image is-invalid"><span>作例と番号が一致しません</span></div>')
      +'<div class="effect-page-copy"><p class="effect-page-label"><b>'+esc(ord)+'</b>'+esc(pg.title||pg.label)+'</p><dl><dt>見る箇所</dt><dd>'+(pg.inspect?esc(pg.inspect):'未記録')+'</dd><dt>スキルの指示</dt><dd>'+(pg.rule?esc(pg.rule):'未記録')+'</dd></dl><p class="effect-page-actions">'+(pg.valid?action:'')+(pg.supplemental?'':proofLink)+inputLink+(pg.artifact?'<a href="'+esc(pg.artifact)+'" download>'+esc(pg.artifactLabel)+'</a>':'')+'</p></div></li>';
    }).join('')+'</ol>';
   }else if(proofCase)pagesBody='<p class="effect-missing">ページごとの見る箇所は未記録です。作例全体を再生して確認できます。</p><button type="button" class="button outline" data-open-case="'+esc(proofCase.id)+'" data-effect="'+esc(item.key)+'">作例を再生 ▶</button>';
   else pagesBody=missing('見る箇所');
   if(proofCase){
    const c=proofCase,pptx=c.format==='pptx'?(c.pptx_download||c.artifact_download):c.pptx_download;
    const raster=['raster_slides','image_only_with_editable_speaker_notes'].includes(c.editability);
    const editDescription=c.format==='pptx'?(raster?'このPPTXのページ内の文字と図は画像です。編集できるのは発表ノートなど一部です。':'編集できる範囲は、PPTXをPowerPointで開くか制作ソースで確認できます。'):'編集できる範囲は、'+formatLabel(c)+'の制作ソースで確認できます。';
    pagesBody+='<p class="effect-edit-note">'+editDescription+'</p><div class="repo-code-actions effect-edit-downloads">'+(pptx?'<a class="button outline" href="'+esc(pptx)+'" download data-name-key="'+(c.pptx_download&&pptx===c.pptx_download?'pptx_download':'artifact_download')+'">PPTXを取得 ↓</a>':'')+(c.source_download?'<a class="button outline" href="'+esc(c.source_download)+'" download>制作ソース一式 ↓</a>':'')+(c.provenance?'<a href="'+esc(c.provenance)+'">制作方法と変更点</a>':'')+(c.qa?'<a href="'+esc(c.qa)+'">確認範囲</a>':'')+'</div>';
   }
   const editProof=e?.demonstration?.editability;
   if(item.caseMatches&&editProof){
    const before=safePath(editProof.before_path),after=safePath(editProof.after_path),artifactPath=safePath(editProof.artifact_path),artifact=/\.pptx$/i.test(artifactPath)?artifactPath:'',report=safePath(editProof.report_path);
    if(before&&after)pagesBody+='<p><a class="button outline" href="'+esc(after)+'" data-proof-image data-proof-label="文字を直して保存した結果" data-proof-input="'+esc(before)+'" data-proof-input-label="'+esc(editProof.before_label||'編集前')+'" data-proof-output-label="'+esc(editProof.after_label||'編集後')+'" data-proof-artifact="'+esc(artifact)+'" data-proof-artifact-label="'+esc(editProof.artifact_label||'編集したPPTXを取得 ↓')+'" data-proof-inspect="'+esc(editProof.description)+'" data-proof-rule="元のPPTXを保持し、編集したコピーを保存して再表示する。">編集前後の画像を拡大 →</a></p>';
    if(before&&after)pagesBody+='<div class="effect-edit-proof"><h3>文字を直して、保存した結果</h3><p>'+esc(editProof.description)+'</p><div class="effect-edit-comparison"><figure><img src="'+esc(before)+'" alt="'+esc(editProof.before_label)+'" loading="lazy"><figcaption>'+esc(editProof.before_label)+'</figcaption></figure><figure><img src="'+esc(after)+'" alt="'+esc(editProof.after_label)+'" loading="lazy"><figcaption>'+esc(editProof.after_label)+'</figcaption></figure></div><p>'+(artifact?'<a href="'+esc(artifact)+'" download>'+esc(editProof.artifact_label||'変更したPPTXを取得 ↓')+'</a>':'')+(report?' · <a href="'+esc(report)+'">保存・再表示の確認記録</a>':'')+'</p></div>';
   }
   const s5=section('pages',5,proofCase?'ページごとの見る箇所':'見る箇所',pagesBody);

   const steps=lines(e?.how_to_use);
   const s6=section('apply',6,'自分の資料へ使う',(steps.length?'<ol class="effect-howto">'+steps.map(x=>'<li>'+esc(x)+'</li>').join('')+'</ol>':'<ol class="effect-howto"><li>日本語スキル本文を取得し、AIへ添付する。</li><li>上の「渡すもの」をそろえる。必須の論文・画像・PPTXなどはメモで代用しない。</li><li>下の依頼文を自分の原稿に合わせて組み立て、完成物と制作ソースを受け取る。</li></ol><p class="effect-missing">このスキル固有の手順は未記録です。上は共通の手順です。</p>')
    +'<div class="repo-code-actions">'+(entry?'<a class="button primary" href="'+esc(skillDownload)+'" download>日本語スキル本文 ↓</a>':'')+(bundle?'<a class="button outline" href="'+esc(bundle)+'" download>原典・素材の一式ZIP ↓</a>':'')+'<a class="text-link" href="./#fonts">書体の組み合わせ →</a></div><div id="repository-skill-slot"></div>');
   const composer=first&&reusableFirst?'<section class="repo-guide-section effect-composer"><h2>自分の原稿で依頼文を作る</h2><p class="case-sample-note">作例の依頼文を、自分の原稿に合わせて編集できます。</p><label for="repository-font">書体の雰囲気</label><select id="repository-font"><option value="example">作例と同じ</option>'+fontKit.presets.map(f=>'<option value="'+esc(f.id)+'">'+esc(f.title)+'</option>').join('')+'</select><p id="repository-font-recipe" class="case-sample-note"></p><textarea id="repository-prompt" aria-label="日本語の生成依頼文">'+esc(first.prompt_text)+'</textarea><button class="button primary" id="repository-copy" type="button">依頼文をコピー ↗</button><span id="repository-copy-state" role="status"></span></section>':'';
   const record='<section class="repo-guide-section"><details><summary>改良点・確認範囲・原文の条件</summary><p>'+esc(p.license_note||'原文LICENSE・NOTICEを一式ZIPに保持しています。')+'</p>'+list(p.limitations)+works.map(c=>'<p><a href="'+esc(c.provenance)+'">'+esc(c.title)+'：方法と変更点</a> · <a href="'+esc(c.qa)+'">確認範囲</a></p>').join('')+'<p>固定原典: '+esc(p.upstream_commit)+'</p><ul>'+refs.slice(0,10).filter(r=>r.url).map(r=>'<li><a href="'+esc(r.url)+'">'+esc(r.path)+' ↗</a></li>').join('')+'</ul><a href="licenses.html">原典・書体の利用条件 →</a></details></section>';
   const rows=works.length?'<section class="repo-guide-section effect-works"><h2>このスキルの作例と完成資料</h2>'+works.map(c=>'<article id="example-'+esc(c.id)+'" class="repo-example-row"><button type="button" data-open-case="'+esc(c.id)+'" data-effect="'+esc(item.key)+'" aria-label="'+esc(c.title)+'を再生"><img src="'+esc(previewUrl(c,c.cover))+'" alt="'+esc(c.title)+'の表紙" loading="lazy"></button><div><h3>'+esc(c.title)+'</h3><p>'+formatLabel(c)+' / '+caseCountLabel(c)+(c.id===proofCase?.id&&e?' / 見る箇所を記録した作例':'')+'</p>'+(!recipeWorks.some(r=>r.id===c.id)?'<p class="effect-note">過去の応用例です。原典の中心機能を示す作例とは制作範囲が異なります。</p>':'')+'<div class="repo-code-actions"><button type="button" data-open-case="'+esc(c.id)+'" data-effect="'+esc(item.key)+'">再生 ↗</button><a href="'+esc(c.artifact_download)+'" download>完成資料 ↓</a>'+(c.pdf_download?'<a href="'+esc(c.pdf_download)+'" download>PDF ↓</a>':'')+(c.pptx_download?'<a href="'+esc(c.pptx_download)+'" download>PowerPoint ↓</a>':'')+(c.draft_download?'<a href="'+esc(c.draft_download)+'" download>変更前のPowerPoint ↓</a>':'')+(c.source_download?'<a href="'+esc(c.source_download)+'" download>制作一式 ↓</a>':'')+(c.id!==first?.id&&recipeWorks.some(r=>r.id===c.id)?'<a href="'+esc(recipeHref(c))+'">この作例で依頼文を作る →</a>':'')+(c.comparison?'<a href="'+esc(c.comparison)+'">'+esc(c.comparison_label||'制作元を見る →')+'</a>':'')+'</div></div></article>').join('')+'</section>':'<p>このスキルは現行の厳選集に含めていません。</p>';
   root.innerHTML=head+'<div class="effect-flow">'+s1+s2+s3+s4+s5+s6+composer+record+rows+'</div>';
   installProofViewer(root);

   for(const work of works){const row=root.querySelector('#example-'+CSS.escape(work.id));for(const key of ['artifact_download','pdf_download','pptx_download','draft_download']){const path=work[key];if(!path||!row)continue;const link=[...row.querySelectorAll('a[download]')].find(a=>a.getAttribute('href')===path);if(link)link.download=caseDownloadName(key==='draft_download'?{...work,title:work.title.replace(/[。．. ]+$/,'')+'（変更前）'}:work,path);}}
   const editLink=root.querySelector('.effect-edit-downloads a[data-name-key]');if(editLink&&proofCase)editLink.download=caseDownloadName(proofCase,editLink.getAttribute('href'));
   if(first?.font_download){const fonts=document.createElement('a');fonts.className='button outline';fonts.href=first.font_download;fonts.setAttribute('download','');fonts.textContent='作例の書体を取得 ↓';root.querySelector('#apply .repo-code-actions').append(fonts);}
   if(p.license_notice_ja){const notice=document.createElement('p');notice.className='repo-license-notice';notice.textContent=p.license_notice_ja;root.querySelector('#io .effect-note:last-of-type').after(notice);}
   if(evaluationOnly){const notice=document.createElement('p');notice.className='repo-archive-note';notice.textContent=first?'この作例はホストSDKの内部評価で制作した履歴です。現在のおすすめから外しています。原典とホストSDKの使用条件は別です。':'この環境の必須ホストSDKは内部評価用途に限定されるため、製品の制作例は生成していません。原典の条件とSDKの用途制限は別に扱います。';root.querySelector('.repo-top').append(notice);root.querySelector('#repository-copy')?.setAttribute('disabled','');}
   if(entry){
    const holder=document.createElement('div');
    holder.innerHTML='<details id="repository-skill-details" class="effect-details"><summary>日本語スキルの本文を読む</summary><p class="case-sample-note">この作例で使った派生スキルの手順を、そのままAIへ渡せます。実装が必要なら一式ZIPも添えてください。</p><pre id="repository-skill-text" class="repository-skill-text">本文を読み込んでいます。</pre><div class="repo-code-actions"><button id="repository-skill-copy" class="button outline" type="button" disabled>本文をコピー</button><a href="'+esc(skillDownload)+'" download>Markdownを取得 ↓</a></div><p id="repository-skill-copy-state" role="status"></p></details>';
    root.querySelector('#repository-skill-slot').replaceWith(...holder.childNodes);
    const details=root.querySelector('#repository-skill-details'),body=details.querySelector('pre'),copy=details.querySelector('button'),status=details.querySelector('[role="status"]');
    let skillText='',loading=false;
    details.addEventListener('toggle',async()=>{
     if(!details.open||skillText||loading)return;
     loading=true;
     try{const response=await fetch(skillDownload,{cache:'no-store'});if(!response.ok)throw Error('skill download');skillText=await response.text();body.textContent=skillText;copy.disabled=false}
     catch{body.textContent='本文を読み込めませんでした。Markdownの取得リンクから開いてください。'}
     finally{loading=false}
    });
    copy.addEventListener('click',async()=>{
     try{await navigator.clipboard.writeText(skillText);status.textContent='スキル本文をコピーしました。'}
     catch{const selection=getSelection(),range=document.createRange();range.selectNodeContents(body);selection.removeAllRanges();selection.addRange(range);status.textContent='本文を選択しました。Ctrl+Cでコピーしてください。'}
    });
   }
   if(recipeWorks.length>1&&first&&reusableFirst){
    const chooser=document.createElement('div');chooser.className='effect-chooser';
    chooser.innerHTML='<label for="repository-case">依頼文の参考にする作例</label><select id="repository-case">'+recipeWorks.map(c=>'<option value="'+esc(c.id)+'"'+(c.id===first.id?' selected':'')+'>'+esc(c.title)+'</option>').join('')+'</select><p class="case-sample-note">作例に合わせて、依頼文・スキル本文・一式ZIPが切り替わります。</p>';
    root.querySelector('.effect-composer h2')?.after(chooser);
    chooser.querySelector('select').addEventListener('change',event=>{const c=works.find(c=>c.id===event.target.value);if(c)location.assign(recipeHref(c)+(item.index>0?'&effect='+item.index:''));});
   }
   if(first?.case_guide){const sourceGuide=document.createElement('p');sourceGuide.className='effect-note';sourceGuide.innerHTML='<a href="'+esc(first.case_guide)+'">この作例の詳しい作り方 →</a>';root.querySelector('#used').append(sourceGuide);}
   if(first&&!evaluationOnly&&reusableFirst)requestComposer({section:root.querySelector('#repository-prompt').closest('section'),caseStudy:first,official,skillDownload:skillDownload||first.prompt,fontKit,item});
   const hashPage=/^#page-(\d+)$/.exec(location.hash);if(hashPage)root.querySelector('#page-'+hashPage[1])?.scrollIntoView();
  }
 }catch(error){root.innerHTML='<p>案内を読み込めませんでした。<a href="./#skills">スキル一覧へ戻る</a></p>';console.error(error)}
}
