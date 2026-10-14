/* A small, independent type specimen. Data and font URLs resolve from this module. */
const root = new URL('../', import.meta.url);
const url = path => new URL(path, root).href;
const samples = {
 editorial: ['言葉に、\n余白を。', '伝えたいことを絞ると、読む人の時間がひらく。見出しと本文の距離で、視線の流れをつくる。', '2026 / TYPE'],
 motion: ['夜から、\n次の一冊。', '短い言葉を大きく。図形と文字が順に現れ、ひとつの主張に視線が集まる。', '06 / NIGHT'],
 friendly: ['わかるから、\nやってみたくなる。', 'むずかしいことも、一歩ずつ。図解と短い説明で、次にすることが見つかる教材へ。', '01 / STEP'],
 poster: ['その一言で、\n目が覚める。', '強い見出しは、短く使う。本文には読みやすい書体を選び、ひとつの画面にひとつの印象を。', '24 / IMPACT'],
 work: ['数字にも、\n読む順番がある。', '結論を先に、説明は短く。単位と比較対象を添えると、同じ数字を同じ意味で読める。', '120 / 30%'],
 research: ['図と出典が、\n主張を支える。', '変数と単位を揃え、仮説と結果を分ける。図の読み方を短く添えると、研究の道筋が伝わる。', 'N = 24 / 95%'],
 explain: ['図を見て、\n関係がわかる。', '題名は明朝、説明はゴシック。式と図のラベルを対応させ、学ぶ人が次に考えることを示す。', '12 / 40 = 30%'],
};
const escape = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

export async function mountFontAtelier(target = document.querySelector('#font-atelier')) {
 if (!target || target.dataset.fontAtelierMounted) return;
 const host = target.matches('section') ? (target.querySelector('[data-font-atelier]') || target.querySelector('div') || target.appendChild(document.createElement('div'))) : target;
 host.classList.add('font-atelier');
 try {
  const response = await fetch(url('data/oss-font-kit.json'));
  if (!response.ok) throw new Error(`font data: ${response.status}`);
  const data = await response.json();
  host.innerHTML = `<div class="fa-intro"><p class="fa-kicker">TYPE ATELIER / ${String(data.presets.length).padStart(2,'0')} DIRECTIONS</p><h3>文字から、<br>スライドの空気を変える。</h3><p>見出し・本文・英数字。それぞれの役割を決めた、${data.presets.length}つの書体セット。</p></div><div class="fa-tabs" role="tablist" aria-label="書体プリセット">${data.presets.map((p,i)=>`<button type="button" role="tab" id="fa-tab-${escape(p.id)}" aria-controls="fa-specimen" aria-selected="${i===0}" tabindex="${i===0?0:-1}" data-preset="${escape(p.id)}">${String(i+1).padStart(2,'0')}<span>${escape(p.title)}</span></button>`).join('')}</div><div class="fa-specimen" id="fa-specimen" role="tabpanel"><div class="fa-sample"><p class="fa-label">見出し / 本文 / 英数字</p><h4></h4><p class="fa-body"></p><p class="fa-latin"></p></div><div class="fa-recipe"><p class="fa-label">FONT RECIPE</p><dl></dl><p class="fa-direction"></p><button type="button" class="fa-copy">この書体指示をコピー <span aria-hidden="true">↗</span></button><p class="fa-status" role="status" aria-live="polite"></p><textarea class="fa-copy-fallback" aria-label="コピー用の書体指示" hidden readonly></textarea></div></div><div class="fa-download-head"><h4>書体を手元に。</h4><a class="fa-kit" href="${url('downloads/yebisu-oss-font-kit.zip')}" download>${data.families.length}書体まとめて ZIP ↓</a></div><div class="fa-downloads">${data.families.map(f=>`<div class="fa-family"><h5>${escape(f.family)}</h5><p>${escape(f.use_ja)}</p><div><a href="${url(f.download)}" download>書体 ZIP ↓</a><a href="${url(f.license_file)}">原文 OFL ↗</a></div></div>`).join('')}</div><p class="fa-license">すべて SIL Open Font License 1.1。ZIPには実フォントと原文OFLを収録。フォントを端末にインストールするか、制作HTMLへ組み込み、配布時はライセンスも添えてください。</p>`;
  let active;
  const buttons = [...host.querySelectorAll('[data-preset]')];
  function select(id, focus = false) {
   active = data.presets.find(p=>p.id===id) || data.presets[0];
   const sample = samples[active.id] || samples.editorial;
   const panel = host.querySelector('.fa-specimen');
   panel.dataset.style=active.id;
   panel.setAttribute('aria-labelledby',`fa-tab-${active.id}`);
   panel.style.setProperty('--fa-heading',`"Atelier ${active.heading}"`);
   panel.style.setProperty('--fa-body',`"Atelier ${active.body}"`);
   panel.style.setProperty('--fa-latin',`"Atelier ${active.latin}"`);
   panel.querySelector('h4').textContent=sample[0];
   panel.querySelector('.fa-body').textContent=sample[1];
   panel.querySelector('.fa-latin').textContent=sample[2];
   panel.querySelector('dl').innerHTML=[['見出し',active.heading],['本文',active.body],['英数字',active.latin]].map(([k,v])=>`<div><dt>${k}</dt><dd>${escape(v)}</dd></div>`).join('');
   panel.querySelector('.fa-direction').textContent=active.instruction;
   host.querySelector('.fa-status').textContent='';
   host.querySelector('.fa-copy-fallback').hidden=true;
   buttons.forEach(b=>{const selected=b.dataset.preset===active.id;b.setAttribute('aria-selected',selected);b.tabIndex=selected?0:-1;if(selected&&focus)b.focus()});
  }
  buttons.forEach((b,i)=>{b.onclick=()=>select(b.dataset.preset);b.onkeydown=e=>{let n;if(e.key==='ArrowRight')n=(i+1)%buttons.length;if(e.key==='ArrowLeft')n=(i+buttons.length-1)%buttons.length;if(e.key==='Home')n=0;if(e.key==='End')n=buttons.length-1;if(n!==undefined){e.preventDefault();select(buttons[n].dataset.preset,true)}}});
  host.querySelector('.fa-copy').onclick=async()=>{
   const text=`原典スライドスキルを適用し、その固有テンプレート・制作方式を使ってください。書体は「${active.title}」：見出し ${active.heading}、本文 ${active.body}、英数字・大きな数値 ${active.latin}。\n${active.instruction}\n日本語は意味のまとまりで改行し、句読点や助詞を行頭に孤立させない。見出し・本文・英数字の役割とサイズ差を明確にする。文字を小さくして詰め込まず、過密なら内容を分けて余白を保つ。配布時は使用フォントの原文OFLを同梱する。`;
   try{await navigator.clipboard.writeText(text);host.querySelector('.fa-status').textContent='書体指示をコピーしました。'}catch{const field=host.querySelector('.fa-copy-fallback');field.value=text;field.hidden=false;field.focus();field.select();host.querySelector('.fa-status').textContent='この欄を選択してコピーしてください。'}
  };
  select(data.presets[0].id);
  target.dataset.fontAtelierMounted='true';
 } catch(error) {host.innerHTML=`<p class="fa-error">書体見本を読み込めませんでした。<a href="${url('downloads/yebisu-oss-font-kit.zip')}">フォント一式をダウンロード</a></p>`;console.error(error);}
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>mountFontAtelier());else mountFontAtelier();
