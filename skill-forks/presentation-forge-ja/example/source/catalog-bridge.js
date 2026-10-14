// Added after the original engine; DeckStage.show/index are original APIs.
(function(){const stage=document.querySelector('deck-stage');
const tell=()=>{if(parent!==window&&location.origin!=='null')parent.postMessage({type:'yebisu-page',index:stage.index},location.origin)};
addEventListener('message',e=>{if(e.source!==parent||e.origin!==location.origin||e.data?.type!=='yebisu-slide')return;const i=e.data.index;if(Number.isInteger(i)&&i>=0&&i<stage.count)stage.show(i)});
new MutationObserver(tell).observe(stage.overlay,{childList:true});tell();
})();
