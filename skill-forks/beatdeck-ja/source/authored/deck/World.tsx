import {Arrow,NodeBox,Reveal,useDeck,usePos,type Rect} from 'beatdeck';
import type {Live} from './timeline';
import {ProcessVisual} from './ProcessVisual';
const labels=['素材','混ぜる・形','焼く','店先','選ぶ','手渡す'];
const nodes:Rect[]=labels.map((_,i)=>({x:140+i*280,y:785,w:240,h:140}));
/** One persistent world spans scenes; its position is derived from the original engine. */
export function World() {
 const {s,b}=usePos();const ready=useDeck<boolean,Live>(state=>state.live.breadReady);
 const on=s>=1;const active=s===1?0:s===2?1:s===3?2:s===4?3:b===0?4:5;
 return <>
  {nodes.map((rect,i)=><NodeBox key={i} rect={rect} on={on} tone={i===active?'hot':i<active?'normal':'dim'} kind={String(i+1).padStart(2,'0')} value={<span style={{fontFamily:'var(--font-sans)',fontSize:32}}>{labels[i]}</span>}/>)}
  {nodes.slice(0,-1).map((rect,i)=><Arrow key={i} from={rect} to={nodes[i+1]} on={on} tone={i===active-1?'hot':i<active?'normal':'dim'}/>)}
  <div className="world-art" data-visual-step={`${s}.${b}`} style={{left:1350,top:255,width:340,height:270,opacity:on?1:0}}><ProcessVisual scene={s} beat={b} ready={ready}/></div>
  <Reveal on={on} x={140} y={971}><p className="brand-caption">架空のパン店 / 工程を示す概念図</p></Reveal>
 </>;
}
