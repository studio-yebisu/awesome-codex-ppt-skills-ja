const root=new URL('../',import.meta.url),url=p=>new URL(p,root).href;
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const norm=v=>String(v??'').normalize('NFKC').toLowerCase();
const kinds={sans:'ゴシック',serif:'明朝・セリフ',rounded:'丸みのある書体',display:'見出し・手書き調',mono:'等幅・コード'};
export async function mountFontAtelier(target=document.querySelector('#font-atelier')){
 if(!target||target.dataset.fontAtelierMounted)return;
 const host=target.matches('section')?(target.querySelector('[data-font-atelier]')||target.querySelector('div')||target.appendChild(document.createElement('div'))):target;
 host.classList.add('font-atelier');
 try{
  const response=await fetch(url('data/oss-font-kit.json'),{cache:'no-store'});
  if(!response.ok)throw Error('font data: '+response.status);
  const data=await response.json();
  const bundles=data.bundles?.length?data.bundles:[{title:'フォントセット',families:data.families.map(f=>f.id),download:'downloads/yebisu-oss-font-kit.zip'}];
  host.innerHTML=`<div class="fa-intro"><h3>組み合わせを試す</h3><p>${data.families.length}ファミリーを用途・日本語対応・種類から探せます。${data.presets.length}通りの組み合わせはAIへの指示に使えます。</p></div><div class="fa-tabs" role="tablist" aria-label="書体の組み合わせ">${data.presets.map((p,i)=>`<button type="button" role="tab" id="fa-tab-${esc(p.id)}" aria-controls="fa-specimen" aria-selected="${i===0}" tabindex="${i===0?0:-1}" data-preset="${esc(p.id)}"><span>${esc(p.title)}</span></button>`).join('')}</div><div class="fa-specimen" id="fa-specimen" role="tabpanel"><div class="fa-sample"><p class="fa-label">見出し / 本文 / 英数字</p><h4></h4><p class="fa-body"></p><p class="fa-latin"></p></div><div class="fa-recipe"><h4>AIへ渡す書体指定</h4><dl></dl><p class="fa-direction"></p><button type="button" class="fa-copy">この書体指示をコピー</button><p class="fa-status" role="status" aria-live="polite"></p><textarea class="fa-copy-fallback" aria-label="コピー用の書体指示" hidden readonly></textarea></div></div><div class="fa-download-head"><h4>用途別にダウンロード</h4><a href="https://fonts.google.com/" target="_blank" rel="noopener noreferrer">Google Fontsでさらに探す ↗</a><a href="${url('downloads/fonts/AI-FONT-GUIDE.md')}" download>組み合わせの指示書 ↓</a></div><div class="fa-bundles">${bundles.map(b=>`<a class="fa-kit" href="${url(b.download)}" download><b>${esc(b.title)}</b><span>${b.families.length}ファミリー${b.bytes?' / '+Math.ceil(b.bytes/1024/1024)+' MB':''} ZIP ↓</span></a>`).join('')}</div><div class="fa-library-head"><h4>個別に探す</h4><label for="fa-query">フォント名・用途<input id="fa-query" type="search" placeholder="例：明朝、技術、Noto、コード"></label></div><div class="fa-font-filters" role="group" aria-label="フォントの種類">${[['all','すべて'],['japanese-sans','日本語ゴシック'],['japanese-serif','日本語明朝'],['display','見出し・手書き調'],['latin','欧文・数字'],['mono','コード']].map(([id,label])=>`<button type="button" data-font-filter="${id}" aria-pressed="${id==='all'}">${label}</button>`).join('')}</div><p class="fa-font-results" aria-live="polite"></p><div class="fa-downloads"></div><p class="fa-license">同梱ファイルは公式配布元の未改変TTF/OTFと原文OFLです。再配布時は原文ライセンスを添えてください。欧文・コード向け書体は日本語を含まない場合があるため、和文書体を組み合わせます。見本は外部CDNを使わず、このサイトから必要な書体だけを読み込みます。</p>`;
  let active,filter='all';
  const mobileLabel=document.createElement('label');mobileLabel.className='fa-mobile-preset';mobileLabel.textContent='書体の組み合わせ';
  const mobileSelect=document.createElement('select');mobileSelect.setAttribute('aria-label','書体の組み合わせを選ぶ');
  mobileSelect.innerHTML=data.presets.map(p=>'<option value="'+esc(p.id)+'">'+esc(p.title)+'</option>').join('');mobileLabel.append(mobileSelect);host.querySelector('.fa-tabs').before(mobileLabel);
  const buttons=[...host.querySelectorAll('[data-preset]')];
  function select(id,focus=false){
   active=data.presets.find(p=>p.id===id)||data.presets[0];
   mobileSelect.value=active.id;
   const panel=host.querySelector('.fa-specimen');panel.dataset.style=active.id;panel.dataset.code=String(Boolean(active.code));panel.setAttribute('aria-labelledby','fa-tab-'+active.id);
   for(const [role,family] of [['heading',active.heading],['body',active.body],['latin',active.latin],['code',active.code||active.latin]])panel.style.setProperty('--fa-'+role,'"Atelier '+family+'"');
   panel.querySelector('h4').textContent='調査結果と\n次の対応';panel.querySelector('.fa-body').textContent='見出し、本文、図のラベルを区別します。数値には単位と比較対象を添え、出典を図の近くに置きます。';
   panel.querySelector('.fa-latin').textContent=active.code?'const total = price * count;':'0123456789 / 24.8%';
   panel.querySelector('.fa-label').textContent=active.code?'見出し / 本文 / 英数字 / コード':'見出し / 本文 / 英数字';
   panel.querySelector('dl').innerHTML=[['見出し',active.heading],['本文',active.body],['英数字',active.latin],...(active.code?[['コード',active.code]]:[])].map(([k,v])=>'<div><dt>'+k+'</dt><dd>'+esc(v)+'</dd></div>').join('');
   panel.querySelector('.fa-direction').textContent=active.instruction;host.querySelector('.fa-status').textContent='';host.querySelector('.fa-copy-fallback').hidden=true;
   buttons.forEach(b=>{const chosen=b.dataset.preset===active.id;b.setAttribute('aria-selected',String(chosen));b.tabIndex=chosen?0:-1;if(chosen&&focus)b.focus()});
  }
  buttons.forEach((b,i)=>{b.onclick=()=>select(b.dataset.preset);b.onkeydown=e=>{let n;if(e.key==='ArrowRight')n=(i+1)%buttons.length;if(e.key==='ArrowLeft')n=(i+buttons.length-1)%buttons.length;if(e.key==='Home')n=0;if(e.key==='End')n=buttons.length-1;if(n!==undefined){e.preventDefault();select(buttons[n].dataset.preset,true)}}});
  mobileSelect.addEventListener('change',()=>select(mobileSelect.value));
  function cards(){
   const term=norm(host.querySelector('#fa-query').value);
   const list=data.families.filter(f=>{const ja=f.language==='ja',kind=f.category||'';return (filter==='all'||filter==='japanese-sans'&&ja&&['sans','rounded'].includes(kind)||filter==='japanese-serif'&&ja&&kind==='serif'||filter==='display'&&kind==='display'||filter==='latin'&&!ja||filter==='mono'&&kind==='mono')&&(!term||norm([f.family,f.use_ja,kinds[kind],ja?'日本語 和文':'欧文 英字 数字',kind==='mono'?'コード 等幅':''].join(' ')).includes(term))});
   host.querySelector('.fa-font-results').textContent=data.families.length+'ファミリー中 '+list.length+'件';
   host.querySelector('.fa-downloads').innerHTML=list.length?list.map(f=>`<article class="fa-family" data-font-id="${esc(f.id)}"><h5>${esc(f.family)}</h5><p>${esc(f.use_ja)}</p><p class="fa-font-meta">${f.language==='ja'?'日本語対応':'欧文・英数字'} / ${esc(kinds[f.category]||'書体')} / ${f.files.length}ファイル</p><div class="fa-family-actions"><a href="${url(f.download)}" download>フォント ZIP ↓</a>${f.official_url?`<a href="${esc(f.official_url)}" target="_blank" rel="noopener noreferrer">公式サイト ↗</a>`:''}<a href="${url(f.license_file)}">原文 OFL ↗</a></div><button type="button" class="fa-preview-toggle" data-font-preview="${esc(f.id)}" aria-expanded="false" aria-controls="fa-preview-${esc(f.id)}">見本を表示</button><div class="fa-individual-preview" id="fa-preview-${esc(f.id)}" hidden><p class="fa-font-sample"></p><p class="fa-font-load" role="status"></p></div></article>`).join(''):'<p>一致するフォントがありません。検索語や種類を変更してください。</p>';
   host.querySelectorAll('[data-font-preview]').forEach(button=>button.onclick=async()=>{
    const family=data.families.find(f=>f.id===button.dataset.fontPreview),preview=host.querySelector('#fa-preview-'+family.id),open=preview.hidden;
    preview.hidden=!open;button.setAttribute('aria-expanded',String(open));button.textContent=open?'見本を閉じる':'見本を表示';if(!open)return;
    const sample=preview.querySelector('.fa-font-sample');sample.style.fontFamily='"Atelier '+family.family+'", '+(family.language==='ja'?'sans-serif':'monospace');sample.textContent=family.language==='ja'?'日本語の見出しと図の説明\nあいうえお 0123456789':'Ag 0123456789\nThe quick brown fox';
    const status=preview.querySelector('.fa-font-load');status.textContent='書体を読み込んでいます。';
    try{const loaded=await document.fonts.load('24px "Atelier '+family.family+'"');status.textContent=loaded.length?'このフォントの公式配布ファイルで表示しています。':'表示を確認できません。公式サイトでも見本を確認できます。';}catch{status.textContent='書体を読み込めません。公式サイトまたはZIPから確認してください。';}
   });
  }
  host.querySelector('#fa-query').addEventListener('input',cards);host.querySelectorAll('[data-font-filter]').forEach(button=>button.onclick=()=>{filter=button.dataset.fontFilter;host.querySelectorAll('[data-font-filter]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));cards()});
  host.querySelector('.fa-copy').onclick=async()=>{
   const text='選んだスライドスキルの固有方式を使ってください。書体は「'+active.title+'」：見出し '+active.heading+'、本文 '+active.body+'、英数字・数値 '+active.latin+(active.code?'、コード '+active.code:'')+'。\n'+active.instruction+'\n日本語は意味のまとまりで改行し、句読点を行頭に孤立させない。見出し・本文・英数字の役割とサイズ差を明確にする。文字を小さくして詰め込まず、過密なら内容を分ける。配布時は使用フォントの原文OFLを同梱する。';
   try{await navigator.clipboard.writeText(text);host.querySelector('.fa-status').textContent='書体指示をコピーしました。'}catch{const field=host.querySelector('.fa-copy-fallback');field.value=text;field.hidden=false;field.focus();field.select();host.querySelector('.fa-status').textContent='この欄を選択してコピーしてください。';}
  };
  select(data.presets[0].id);cards();target.dataset.fontAtelierMounted='true';
 }catch(error){host.innerHTML='<p class="fa-error">フォント一覧を読み込めませんでした。<a href="https://fonts.google.com/">Google Fontsで探す</a></p>';console.error(error)}
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>mountFontAtelier());else mountFontAtelier();
