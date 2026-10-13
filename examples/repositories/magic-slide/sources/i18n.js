// Catalog navigation only. Native runtime owns rendering, animation and cursor.
(()=>{let pending=null,timer;
 const move=()=>{if(pending===null)return;if(typeof go!=='function'||typeof cur!=='number'){timer=setTimeout(move,100);return}if(cur===pending){pending=null;return}if(typeof animating==='undefined'||!animating)go(cur,pending);timer=setTimeout(move,100)};
 addEventListener('message',e=>{if(e.source!==parent||e.origin!==location.origin)return;
  const d=e.data;if(!d||d.type!=='yebisu-slide'||!Number.isInteger(d.index))return;
  pending=Math.max(0,Math.min(document.querySelectorAll('#deck>.slide').length-1,d.index));clearTimeout(timer);move();
 });
})();
