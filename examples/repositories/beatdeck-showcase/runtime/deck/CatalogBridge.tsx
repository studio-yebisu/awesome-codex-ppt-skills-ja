import {useEffect} from 'react';
import {deck} from 'beatdeck';
/** Outside the engine: flatten its scene/beat positions, then call its original public API. */
export function CatalogBridge(){useEffect(()=>{
 const positions=deck.scenes.flatMap((scene,s)=>scene.beats.map((_,b)=>({scene:s,beat:b})));
 const report=()=>{const p=deck.getState();const index=positions.findIndex(q=>q.scene===p.scene&&q.beat===p.beat);if(parent!==window)parent.postMessage({type:'yebisu-page',index,total:positions.length},location.origin);};
 const receive=(e:MessageEvent)=>{if(e.source!==parent||e.origin!==location.origin||e.data?.type!=='yebisu-slide'||!Number.isInteger(e.data.index))return;const p=positions[e.data.index];if(p)deck.go(p);};
 const unsubscribe=deck.subscribe(report);addEventListener('message',receive);report();
 return()=>{unsubscribe();removeEventListener('message',receive);};
 },[]);return null;}
