import {useSyncExternalStore} from 'react';
import {Reveal,Scene,Typewriter,reducedMotion,useScene} from 'beatdeck';
import {Bread} from './Illustrations';

function Statement({on,out=false,text,body,size=140}:{on:boolean;out?:boolean;text:React.ReactNode;body?:string;size?:number}) {
 return <><Reveal on={on} out={out} x={140} y={180}><div className="t-statement bread-heading" style={{fontSize:size}}>{text}</div></Reveal>{body&&<Reveal on={on} out={out} x={140} y={565}><p className="bread-body">{body}</p></Reveal>}</>;
}
function Opening_(){const {here,b}=useScene();return <>
 <Reveal on={here&&b===0} out={here&&b>0} x={200} y={430}><div className="t-editorial" style={{fontSize:72}}>パンが、店先に届くまで。</div><p className="bread-body" style={{marginTop:42}}>架空のパン店の概念資料。クリックで開始。</p></Reveal>
 <Reveal on={here&&b>=1} x={140} y={220}><div className="t-statement" style={{fontSize:144}}>パンが、店先に<br/>届くまで。</div><p className="bread-body" style={{marginTop:54}}>素材から、誰かの手へ。</p><p className="brand-caption" style={{marginTop:38}}>架空のパン店を説明する概念資料。</p></Reveal>
 <Reveal on={here&&b>=1} x={1380} y={420}><div style={{width:350,height:250}}><Bread warm/></div></Reveal>
 </>;}
export const Opening=()=> <Scene index={0}><Opening_/></Scene>;
function Materials_(){const {here,b}=useScene();return <><Statement on={here&&b===0} out={here&&b>0} text={<>はじまりは、<br/>素材から。</>} body="流れの最初の位置を、ひとつの図で見る。"/><Statement on={here&&b===1} text="次の工程へ。" body="素材から、生地をつくるところへ。"/></>;}
export const Materials=()=> <Scene index={1}><Materials_/></Scene>;
function DoughScene_(){const {here,b}=useScene();return <><Statement on={here&&b===0} out={here&&b>0} text="混ぜる。" size={180} body="素材が、生地になる場面。"/><Statement on={here&&b===1} out={here&&b>1} text="形づくる。" size={170} body="生地の形を整え、次の工程へ渡す。"/><Statement on={here&&b===2} text="焼く場所へ。" body="形を整えた生地を、焼く工程へ渡す。"/></>;}
export const DoughScene=()=> <Scene index={2}><DoughScene_/></Scene>;
function Baking_(){const {here,b}=useScene();return <><Statement on={here&&b===0} out={here&&b>0} text="焼く。" size={180} body="生地を焼き、パンへ変わるところ。"/><Statement on={here&&b===1} text={<>パンとして、<br/>店先へ。</>} body="焼く工程を終え、店先へ運ぶ。"/></>;}
export const Baking=()=> <Scene index={3}><Baking_/></Scene>;
function Shop_(){const {here,b}=useScene();return <><Statement on={here&&b===0} out={here&&b>0} text="店先に、届く。" body="焼く工程から、並べる場所へ。"/><Statement on={here&&b===1} out={here&&b>1} text={<>並べて、<br/>見つけやすく。</>} body="棚の中で、並べる位置を整える。"/><Statement on={here&&b===2} text="選ぶ時間へ。" body="つくる流れから、選ぶ体験へ。"/></>;}
export const Shop=()=> <Scene index={4}><Shop_/></Scene>;
function Handoff_(){const {here,b,entry}=useScene();const reduced=useSyncExternalStore(reducedMotion.subscribe,reducedMotion.get);return <>
 <Statement on={here&&b===0} out={here&&b>0} text="選ぶ。" size={180} body="店先で、気になるパンを見つける。"/>
 <Reveal on={here&&b===1} out={here&&b>1} x={140} y={180}><Typewriter run={here&&b===1&&!reduced} entry={entry} lines={['ひとつを、','手渡す。']} charMs={60} lineStyle={{fontFamily:'BreadDisplay',fontSize:140,lineHeight:1.25}}/></Reveal>
 <Reveal on={here&&b===1} out={here&&b>1} x={140} y={565}><p className="bread-body">店先から、手へ渡る場面。</p></Reveal>
 <Statement on={here&&b===2} text={<>店先から、<br/>誰かの手へ。</>} body="架空のパン店の概念資料。素材から、誰かの手へ。"/>
 </>;}
export const Handoff=()=> <Scene index={5}><Handoff_/></Scene>;
