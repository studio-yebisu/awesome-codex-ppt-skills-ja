// CC0-1.0. Standalone, dependency-free deck export.
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {renderSlide,validateDeck,xml} from '../assets/slide-renderer.mjs';

export async function exportDeck(deck, output, {overwrite=false}={}) {
  validateDeck(deck);
  if(!overwrite){try{await fs.stat(output);throw new Error('出力フォルダが存在します。新しいフォルダを指定してください。')}catch(error){if(error.code!=='ENOENT')throw error;}}
  await fs.mkdir(output,{recursive:true});
  const slides=deck.slides.map((_,i)=>renderSlide(deck,i));
  for(const [i,svg] of slides.entries())await fs.writeFile(path.join(output,`slide-${String(i+1).padStart(2,'0')}.svg`),svg);
  await fs.writeFile(path.join(output,'deck.json'),JSON.stringify(deck,null,2)+'\n');
  const notes=deck.slides.map((s,i)=>`## ${i+1}. ${s.title}\n\n${s.notes||''}\n`).join('\n');
  await fs.writeFile(path.join(output,'speaker-notes.md'),`# ${deck.title}\n\n${notes}`);
  const htmlSlides=deck.slides.map((_,i)=>renderSlide(deck,i,{animate:true}));
  const html=`<!doctype html><html lang="ja"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${xml(deck.title)}</title><style>*{box-sizing:border-box}body{margin:0;background:#11151e;color:white;font-family:'Noto Sans JP',sans-serif;display:grid;min-height:100svh;place-content:center;padding:24px}main{width:min(1200px,calc(100vw - 48px))}section{aspect-ratio:16/9;display:none}section.active{display:block}svg{width:100%;height:100%}nav{display:flex;align-items:center;justify-content:center;gap:16px;padding:20px}button{font:inherit;border:1px solid #6a7283;color:white;border-radius:8px;background:#252b38;padding:10px 18px;cursor:pointer}button:focus-visible{outline:3px solid #cfff66}details{max-width:900px;margin:auto}pre{font:inherit;white-space:pre-wrap}@media print{body{padding:0;background:white}main{width:100%}section{display:block;break-after:page}nav,details{display:none}@page{size:landscape;margin:0}}</style><main>${htmlSlides.map((s,i)=>`<section${i===0?' class="active"':''}>${s}</section>`).join('')}<nav aria-label="スライド操作"><button id="prev" aria-label="前のスライド">←</button><span id="counter"></span><button id="next" aria-label="次のスライド">→</button><button id="play">自動再生</button></nav><details><summary>発表者ノート</summary><pre id="notes"></pre></details></main><script type="application/json" id="data">${JSON.stringify(deck).replace(/</g,'\\u003c')}</script><script>const deck=JSON.parse(document.querySelector('#data').textContent),slides=[...document.querySelectorAll('section')];let i=0,timer;function show(n){i=(n+slides.length)%slides.length;slides.forEach((s,j)=>s.classList.toggle('active',j===i));document.querySelector('#counter').textContent=(i+1)+' / '+slides.length;document.querySelector('#notes').textContent=deck.slides[i].notes||''}function stop(){clearTimeout(timer);timer=null;document.querySelector('#play').textContent='自動再生'}function play(){stop();document.querySelector('#play').textContent='停止';timer=setTimeout(()=>{if(i===slides.length-1){stop();return}show(i+1);play()},(deck.slides[i].duration||6)*1000)}document.querySelector('#prev').onclick=()=>{stop();show(i-1)};document.querySelector('#next').onclick=()=>{stop();show(i+1)};document.querySelector('#play').onclick=()=>timer?stop():play();document.addEventListener('keydown',e=>{if(e.key==='ArrowRight'){e.preventDefault();stop();show(i+1)}if(e.key==='ArrowLeft'){e.preventDefault();stop();show(i-1)}if(e.code==='Space'&&!['BUTTON','SUMMARY','INPUT'].includes(e.target.tagName)){e.preventDefault();timer?stop():play()}});document.addEventListener('visibilitychange',()=>{if(document.hidden)stop()});show(0);</script></html>`;
  await fs.writeFile(path.join(output,'index.html'),html);
  return output;
}
if(process.argv[1] && fileURLToPath(import.meta.url)===path.resolve(process.argv[1])){
  const [input,output]=process.argv.slice(2);
  if(!input||!output)throw new Error('使い方: node tools/render-deck.mjs deck.json output-directory');
  const deck=JSON.parse(await fs.readFile(input,'utf8'));
  await exportDeck(deck,path.resolve(output));
  console.log(`生成: ${deck.slides.length}枚 / ${path.resolve(output)}`);
}
