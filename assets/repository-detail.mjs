import {caseDownloadName} from './download-name.mjs';
const root=document.querySelector('#repository-detail');
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const json=async path=>{const r=await fetch(path,{cache:'no-store'});if(!r.ok)throw Error(path);return r.json()};
function requestComposer({section,caseStudy,official,skillDownload,fontKit}){
 const fontSelect=section.querySelector('#repository-font'),field=section.querySelector('#repository-prompt'),status=section.querySelector('#repository-copy-state');
 section.querySelector('h2').textContent='あなたの原稿で、作る。';
 section.querySelector('.case-sample-note').textContent='スキル本文と一式ZIPをAIへ添付し、ここで作った依頼文も渡してください。'+(/\.pptx$/i.test(caseStudy.input||'')?' 変換したいPowerPointも添付し、原稿欄には変更したい点を書きます。':'');
 const inputs=document.createElement('div');inputs.className='repository-request-inputs';
 inputs.innerHTML='<label for="repository-topic">何の資料を作る？</label><input id="repository-topic" placeholder="例：新しく入るメンバーへの引き継ぎ"><label for="repository-content">自分の原稿・伝えたいこと</label><textarea id="repository-content" placeholder="箇条書きのメモでも大丈夫。使いたい情報を貼り付けてください。"></textarea><div class="repository-request-options"><div><label for="repository-audience">読み手・目的</label><input id="repository-audience" placeholder="例：初めて担当する人が、次の作業を始められる"></div><div><label for="repository-pages">希望枚数</label><input id="repository-pages" type="number" min="1" max="100" value="'+esc(caseStudy.page_count)+'"></div></div>';
 fontSelect.previousElementSibling.before(inputs);
 const assemble=document.createElement('button');assemble.className='button outline';assemble.type='button';assemble.id='repository-assemble';assemble.textContent='この内容で依頼文を組み立てる ↓';
 field.before(assemble);
 const label=document.createElement('label');label.htmlFor='repository-prompt';label.textContent='AIへ渡す依頼文（編集できます）';field.before(label);
 const used=document.createElement('details');used.className='repository-used-prompt';
 const summary=document.createElement('summary');summary.textContent='この作例を作った依頼文';
 const raw=document.createElement('pre');raw.textContent=caseStudy.prompt_text;used.append(summary,raw);section.append(used);
 const fontInstruction=()=>{
  const f=fontKit.presets.find(x=>x.id===fontSelect.value);
  return f?'書体：見出し '+f.heading+'、本文 '+f.body+'、英数字 '+f.latin+'。'+f.instruction+' 公式配布のフォントと原文OFLを使う。':'書体：添付したスキルと作例の書体指定を使う。必要な公式配布フォントと原文OFLも用意する。';
 };
 const compose=()=>{
  const topic=inputs.querySelector('#repository-topic').value.trim()||'［作りたい資料の題材］';
  const content=inputs.querySelector('#repository-content').value.trim()||'［自分の原稿をここに入れる。原典が必要とする論文・画像・PPTX等は別途添付する］';
  const audience=inputs.querySelector('#repository-audience').value.trim()||'［読み手と、この資料で伝えたいこと］';
  const pages=Number(inputs.querySelector('#repository-pages').value);
  const count=Number.isInteger(pages)&&pages>=1&&pages<=100?pages:caseStudy.page_count;
  const output=caseStudy.format==='pptx'?'PowerPoint（PPTX）と制作ソース。文字・図などを編集できる範囲は、この方式に合わせて明記する。':caseStudy.format==='pdf'?'PDFと原典方式の制作ソース。':'ブラウザーで再生できるWebスライドと制作ソース。';
  field.value='添付の日本語スキル「'+skillDownload.split('/').pop()+'」を使い、次の内容で日本語の資料を完成させてください。\n\n題材：'+topic+'\n読み手・目的：'+audience+'\n希望枚数：'+count+'枚。固定の版式など原典の制約があれば、その方式に合わせる。\n\n原稿：\n'+content+'\n\n作風の参考：「'+caseStudy.title+'」\n'+(caseStudy.style?'見た目：'+caseStudy.style+'\n':'')+fontInstruction()+'\n日本語は意味のまとまりで改行する。見出しは短く、余白と文字の強弱で伝える。情報が過密なら内容を分ける。\n\n使う原典：'+official+'\nこの作例の制作方法：'+(caseStudy.method||'添付したスキル本文の固有テンプレート・生成器・変換工程')+'\n原典SKILLにある必要な入力と、固有テンプレート・生成器・変換工程を使う。制作一式ZIP内の実装や、固定原典の参照ファイルを利用する。必須の入力が足りなければ、その内容を確認してから制作する。\n原稿の事実・仮説・仮の数字を区別し、根拠や実測値を補完しない。\n\n完成物：'+output+'\n必要な生成工程と、主要な完成ファイルの初回表示まで進めてください。';
  status.textContent='依頼文を組み立てました。必要なら下で編集できます。';
 };
 assemble.addEventListener('click',compose);
 fontSelect.addEventListener('change',()=>{const f=fontKit.presets.find(x=>x.id===fontSelect.value);section.querySelector('#repository-font-recipe').textContent=(f?f.heading+' / '+f.body+' / '+f.latin:'作例と同じ書体')+'。選んだ書体は「組み立てる」で依頼文へ入ります。';});
 section.querySelector('#repository-copy').addEventListener('click',async()=>{try{await navigator.clipboard.writeText(field.value);status.textContent='依頼文をコピーしました。スキル本文と一緒にAIへ渡してください。';}catch{field.focus();field.select();status.textContent='依頼文を選択しました。Ctrl+Cでコピーしてください。';}});
 compose();status.textContent='入力はこの画面の中だけで使います。依頼文をコピーして、使っているAIへ。';
}
if(root){
 try{
  const [profiles,cases,product,fontKit]=await Promise.all(['data/repository-guides.json','data/case-studies.json','data/product-collection.json','data/oss-font-kit.json'].map(json));
  const repo=new URLSearchParams(location.search).get('repo');
  const p=profiles.find(x=>x.repository===repo),entry=product.entries.find(e=>e.repository===repo);
  if(!p){root.innerHTML='<p>スキルが見つかりません。<a href="./#skills">一覧へ戻る</a></p>'}
  else{
   const works=cases.filter(c=>c.repository===repo).sort((a,b)=>Number(b.id===entry?.featured_case_id)-Number(a.id===entry?.featured_case_id));
   const requestedCase=new URLSearchParams(location.search).get('case');
   const first=works.find(c=>c.id===requestedCase)||works[0],recipe=product.case_recipes?.[first?.id];
   const commit=recipe?.upstream_commit||first?.upstream_commit||p.upstream_commit;
   const official='https://github.com/'+repo+(commit?'/tree/'+commit:'');
   const recipeHref=c=>'repository.html?repo='+encodeURIComponent(repo)+'&case='+encodeURIComponent(c.id);
   const skillDownload=recipe?.skill_download||entry?.skill_download;
   const title=entry?.title_ja||repo.split('/')[1];
   document.title=title+'｜AIスライドアトリエ';
   const list=v=>'<ul>'+v.map(x=>'<li>'+esc(typeof x==='string'?x:JSON.stringify(x))+'</li>').join('')+'</ul>';
   const refs=(p.source_refs||[]).map(r=>typeof r==='string'?(r.startsWith('https://')?{path:new URL(r).pathname.split('/').pop()||'GitHub原典',url:r}:{path:r,url:'https://github.com/'+repo+'/blob/'+p.upstream_commit+'/'+r}):r);
   const evaluationOnly=['excluded_host_runtime_evaluation_only','excluded_required_evaluation_runtime'].includes(p.product_status);
   const bundle=evaluationOnly?null:(recipe?.fork_download||first?.fork_download||entry?.fork_download);
   const skill=entry?'<a class="button primary" href="'+esc(skillDownload)+'" download>スキル本文を取得 ↓</a>':'';
   root.innerHTML='<a class="text-link" href="./#skills">← スキルを選ぶ</a><header class="repo-top"><p class="repo-owner">STUDIO YEBISU / JAPANESE SKILL</p><h1>'+esc(title)+'</h1><p class="repo-desc">'+esc(entry?.description_ja||p.summary_ja)+'</p><div class="repo-chips"><span>'+esc(repo)+'</span><span>'+esc(p.license||'個別条件')+'</span></div><div class="repo-code-actions">'+skill+(bundle?'<a class="button outline" href="'+esc(bundle)+'" download>原典・素材の一式ZIP ↓</a>':'')+'<a class="text-link" href="'+esc(official)+'" target="_blank" rel="noopener noreferrer">GitHub原典 ↗</a></div><p class="case-sample-note">スキル本文はAIへ渡す指示です。実装・テンプレートは一式ZIPか固定原典から。</p></header><div class="repository-layout"><div>'+(first?'<button class="case-card-image detail-cover'+(first.preview_canvas&&first.preview_canvas.width===first.preview_canvas.height?' square-preview':'')+'" data-open-case="'+esc(first.id)+'" aria-label="'+esc(first.title)+'を再生"><img src="'+esc(first.cover)+'?v='+esc(first.content_revision)+'" alt="'+esc(first.title)+'の完成スライド"><span class="watch">▶ スライドを見る</span></button><p class="case-sample-note">'+esc(first.sample_notice)+'</p><h2>このスキルで、実際に作った。</h2>'+works.map(c=>'<article id="example-'+esc(c.id)+'" class="repo-example-row"><button data-open-case="'+esc(c.id)+'" aria-label="'+esc(c.title)+'を再生"><img src="'+esc(c.cover)+'?v='+esc(c.content_revision)+'" alt="'+esc(c.title)+'の表紙"></button><div><h3>'+esc(c.title)+'</h3><p>'+esc(c.format==='pptx'?'PowerPoint':c.format==='pdf'?'PDF':'Web')+' / '+c.page_count+'枚</p><div class="repo-code-actions"><button data-open-case="'+esc(c.id)+'">再生 ↗</button><a href="'+esc(c.artifact_download)+'" download>完成資料 ↓</a>'+(c.pdf_download?'<a href="'+esc(c.pdf_download)+'" download>PDF ↓</a>':'')+(c.pptx_download?'<a href="'+esc(c.pptx_download)+'" download>PowerPoint ↓</a>':'')+'<a href="'+esc(c.source_download)+'" download>制作一式 ↓</a><a href="'+esc(recipeHref(c))+'">この作例を使う →</a>'+(c.comparison?'<a href="'+esc(c.comparison)+'">'+esc(c.comparison_label||'制作元を見る →')+'</a>':'')+'</div></div></article>').join(''):'<p>このスキルは現行の厳選集に含めていません。</p>')+'</div><div><section class="repo-guide-section"><h2>あなたの内容で作る。</h2><ol><li>スキル本文をAIへ添付し、自分の原稿と読み手・目的を渡す。</li><li>本文にある固定原典の方式を使う。必要なら一式ZIPを展開して渡す。</li><li>書体指示を加えて、完成資料と制作ソースを作ってもらう。</li></ol><a class="text-link" href="./#fonts">書体の組み合わせを選ぶ →</a></section>'+(first?'<section class="repo-guide-section"><h2>自分の内容で頼んでみる。</h2><p class="case-sample-note">作例の依頼文を、自分の原稿に合わせて編集できます。</p><label for="repository-font">書体の雰囲気</label><select id="repository-font"><option value="example">作例と同じ</option>'+fontKit.presets.map(f=>'<option value="'+esc(f.id)+'">'+esc(f.title)+'</option>').join('')+'</select><p id="repository-font-recipe" class="case-sample-note"></p><textarea id="repository-prompt" aria-label="日本語の生成依頼文">'+esc(first.prompt_text)+'</textarea><button class="button primary" id="repository-copy" type="button">依頼文をコピー ↗</button><span id="repository-copy-state" role="status"></span><p><a href="'+esc(first.input)+'">入力原稿</a> · <a href="'+esc(first.input_data)+'">入力の条件</a></p></section>':'')+'<section class="repo-guide-section"><details><summary>原典の制作方法と必要な環境</summary><p>'+esc(first?.method||p.method_ja||p.execution_type)+'</p>'+list(p.requirements||[])+(p.steps?.length?list(p.steps):'')+(p.commands?.length?'<pre>'+esc(p.commands.map(c=>typeof c==='string'?c:JSON.stringify(c)).join('\n\n'))+'</pre>':'')+'</details></section><section class="repo-guide-section"><details><summary>改良点・確認範囲・原文の条件</summary><p>'+esc(p.license_note||'原文LICENSE・NOTICEを一式ZIPに保持しています。')+'</p>'+list(p.limitations||[])+works.map(c=>'<p><a href="'+esc(c.provenance)+'">'+esc(c.title)+'：方法と変更点</a> · <a href="'+esc(c.qa)+'">確認範囲</a></p>').join('')+'<p>固定原典: '+esc(p.upstream_commit)+'</p><ul>'+refs.slice(0,10).filter(r=>r.url).map(r=>'<li><a href="'+esc(r.url)+'">'+esc(r.path)+' ↗</a></li>').join('')+'</ul><a href="licenses.html">原典・書体の利用条件 →</a></details></section></div></div>';
   for(const work of works){const row=root.querySelector('#example-'+CSS.escape(work.id));for(const key of ['artifact_download','pdf_download','pptx_download']){const path=work[key];if(!path||!row)continue;const link=[...row.querySelectorAll('a[download]')].find(a=>a.getAttribute('href')===path);if(link)link.download=caseDownloadName(work,path);}}
   if(first?.font_download){const fonts=document.createElement('a');fonts.className='button outline';fonts.href=first.font_download;fonts.setAttribute('download','');fonts.textContent='作例の書体を取得 ↓';root.querySelector('.repo-top .repo-code-actions').append(fonts);}
   if(p.license_notice_ja){const notice=document.createElement('p');notice.className='repo-license-notice';notice.textContent=p.license_notice_ja;root.querySelector('.repo-code-actions').before(notice);}
   if(evaluationOnly){const notice=document.createElement('p');notice.className='repo-archive-note';notice.textContent=first?'この作例はホストSDKの内部評価で制作した履歴です。現在のおすすめから外しています。原典とホストSDKの使用条件は別です。':'この環境の必須ホストSDKは内部評価用途に限定されるため、製品の制作例は生成していません。原典の条件とSDKの用途制限は別に扱います。';root.querySelector('.repo-top').append(notice);root.querySelector('#repository-copy')?.setAttribute('disabled','');}
   if(entry){
    const section=document.createElement('section');section.className='repo-guide-section';
    section.innerHTML='<details id="repository-skill-details"><summary>日本語スキルの本文を読む</summary><p class="case-sample-note">この作例で使った派生スキルの手順を、そのままAIへ渡せます。実装が必要なら一式ZIPも添えてください。</p><pre id="repository-skill-text" class="repository-skill-text">本文を読み込んでいます。</pre><div class="repo-code-actions"><button id="repository-skill-copy" class="button outline" type="button" disabled>本文をコピー</button><a href="'+esc(skillDownload)+'" download>Markdownを取得 ↓</a></div><p id="repository-skill-copy-state" role="status"></p></details>';
    const howTo=root.querySelector('.repo-guide-section');howTo.after(section);
    const details=section.querySelector('details'),body=section.querySelector('pre'),copy=section.querySelector('button'),status=section.querySelector('[role="status"]');
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
   if(works.length>1){
    const chooser=document.createElement('section');chooser.className='repo-guide-section';
    chooser.innerHTML='<label for="repository-case">参考にする作例</label><select id="repository-case">'+works.map(c=>'<option value="'+esc(c.id)+'"'+(c.id===first.id?' selected':'')+'>'+esc(c.title)+'</option>').join('')+'</select><p class="case-sample-note">作例に合わせて、依頼文・スキル本文・一式ZIPが切り替わります。</p>';
    root.querySelector('.repo-guide-section').before(chooser);
    chooser.querySelector('select').addEventListener('change',event=>{const c=works.find(c=>c.id===event.target.value);if(c)location.assign(recipeHref(c));});
   }
   if(first?.case_guide){const sourceGuide=document.createElement('p');sourceGuide.className='case-sample-note';sourceGuide.innerHTML='<a href="'+esc(first.case_guide)+'">この作例の詳しい作り方 →</a>';root.querySelector('.detail-cover')?.after(sourceGuide);}
   if(first&&!evaluationOnly)requestComposer({section:root.querySelector('#repository-prompt').closest('section'),caseStudy:first,official,skillDownload:skillDownload||first.prompt,fontKit});
  }
 }catch(error){root.innerHTML='<p>案内を読み込めませんでした。<a href="./#skills">一覧へ戻る</a></p>';console.error(error)}
}
