
if(parent!==window){
document.addEventListener('keydown', e=>{if(e.key==='Escape'){e.preventDefault();e.stopImmediatePropagation();parent.postMessage({type:'yebisu-close'},location.origin)}},true);
window.addEventListener('message', e=>{if(e.source!==parent||e.origin!==location.origin||e.data?.type!=='yebisu-slide')return;const n=e.data.index; if(!Number.isInteger(n))return;location.hash=String(n+1);});
}
