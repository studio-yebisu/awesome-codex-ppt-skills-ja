// Original fixed-stage scaling expression from references/html-generation-rules.md.
const stage = document.querySelector('.stage');
function fit() {
  const scale = Math.min(window.innerWidth / 1920, window.innerHeight / 1080);
  stage.style.transform = `scale(${scale})`;
}
addEventListener('resize',fit);fit();
// Deck navigation authored locally under the upstream fixed-stage visibility contract.
const slides = document.querySelectorAll('.slide');
let current = 0;
function go(n) {
  if (!Number.isInteger(n) || n < 0 || n >= slides.length) return;
  slides[current].classList.remove('active');current=n;slides[current].classList.add('active');
  document.querySelector('#counter').textContent=String(current+1).padStart(2,'0')+' / '+String(slides.length).padStart(2,'0');
  document.querySelector('#prev').disabled=current===0;
  document.querySelector('#next').disabled=current===slides.length-1;
  if(parent!==window && location.origin!=='null')parent.postMessage({type:'yebisu-page',index:current},location.origin);
}
document.querySelector('#prev').onclick=()=>go(current-1);
document.querySelector('#next').onclick=()=>go(current+1);
addEventListener('keydown',e=>{if(['ArrowRight','ArrowDown',' '].includes(e.key)){e.preventDefault();go(current+1)}if(['ArrowLeft','ArrowUp'].includes(e.key)){e.preventDefault();go(current-1)}if(e.key==='Home')go(0);if(e.key==='End')go(slides.length-1)});
let touchX=0;addEventListener('touchstart',e=>{touchX=e.touches[0].clientX});addEventListener('touchend',e=>{let dx=e.changedTouches[0].clientX-touchX;if(Math.abs(dx)>50)go(current+(dx<0?1:-1))});
go(0);

addEventListener('message',e=>{if(e.source===parent&&e.origin===location.origin&&e.data?.type==='yebisu-slide'&&Number.isInteger(e.data.index))go(e.data.index)});
window.deckPage=()=>current;
