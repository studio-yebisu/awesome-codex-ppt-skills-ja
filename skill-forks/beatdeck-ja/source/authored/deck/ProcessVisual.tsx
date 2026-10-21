import {Bread,Dough,Shelf} from './Illustrations';
/** Beat-specific explanatory states. No ingredient, quantity, temperature or duration is asserted. */
export function ProcessVisual({scene,beat,ready}:{scene:number;beat:number;ready:boolean}) {
 if(scene===1)return <svg viewBox="0 0 360 260" role="img" aria-label={beat===0?'素材を置く':'素材を次の工程へつなぐ'}>
  {[70,170,270].map((x,i)=><circle key={x} cx={beat===0?x:70+i*45} cy={beat===0?110:80+i*30} r={beat===0?30:23} fill="var(--surface)" stroke="var(--accent)" strokeWidth="4"/>)}
  {beat===1&&<><path d="M90 190 H270 l-25 -17 M270 190 l-25 17" fill="none" stroke="var(--accent)" strokeWidth="7"/><text x="180" y="245" textAnchor="middle" fontSize="27" fill="var(--ink)">混ぜる工程へ</text></>}
 </svg>;
 if(scene===2&&beat===0)return <svg viewBox="0 0 360 260" role="img" aria-label="混ぜる状態"><path d="M45 110 Q55 230 180 230 Q305 230 315 110Z" fill="var(--surface)" stroke="var(--ink)" strokeWidth="5"/><path d="M90 120 Q180 50 270 120 M125 80 L160 180" fill="none" stroke="var(--accent)" strokeWidth="9"/></svg>;
 if(scene===2&&beat===1)return <Dough/>;
 if(scene===2)return <svg viewBox="0 0 360 260" role="img" aria-label="形を整えた生地を焼く場所へ"><path d="M95 140 Q95 65 180 65 Q265 65 265 140Z" fill="var(--surface)" stroke="var(--ink)" strokeWidth="5"/><path d="M50 150 H310 M65 165 H295 M180 205 H310 l-22 -17 M310 205 l-22 17" fill="none" stroke="var(--accent)" strokeWidth="6"/></svg>;
 if(scene===3)return <svg viewBox="0 0 360 260" role="img" aria-label={beat===0?'焼く工程の状態':'パンを店先へ移す状態'}><rect x="28" y="30" width="280" height="190" rx="8" fill="none" stroke="var(--ink)" strokeWidth="5"/><path d="M65 155 Q65 80 165 80 Q265 80 265 155Z" fill={ready?'var(--accent)':'var(--surface)'} stroke="var(--ink)" strokeWidth="4"/>{beat===0?<path d="M90 55 Q100 35 90 17 M165 55 Q175 35 165 17 M240 55 Q250 35 240 17" fill="none" stroke="var(--accent)" strokeWidth="4"/>:<path d="M230 235 H340 l-20 -15 M340 235 l-20 15" fill="none" stroke="var(--accent)" strokeWidth="6"/>}</svg>;
 if(scene===4)return <div style={{position:'relative',width:'100%',height:'100%'}}><Shelf/>{beat===0?<div style={{position:'absolute',left:5,top:0,width:95}}><Bread warm/></div>:beat===1?<svg viewBox="0 0 360 260" style={{position:'absolute',inset:0}} aria-label="棚で位置をそろえる"><path d="M65 210 H295 M65 200 V220 M180 200 V220 M295 200 V220" stroke="var(--accent)" strokeWidth="5"/></svg>:<svg viewBox="0 0 360 260" style={{position:'absolute',inset:0}} aria-label="選ぶパンに注目する"><rect x="125" y="65" width="110" height="130" fill="none" stroke="var(--accent)" strokeWidth="6"/></svg>}</div>;
 if(scene===5&&beat===0)return <Shelf/>;
 if(scene===5&&beat===1)return <svg viewBox="0 0 360 260" role="img" aria-label="パンを手へ渡す"><path d="M40 110 Q40 45 120 45 Q200 45 200 110Z" fill="var(--accent)" stroke="var(--ink)" strokeWidth="4"/><path d="M180 145 H310 l-20 -15 M310 145 l-20 15 M190 205 H315 V235 H190Z" fill="none" stroke="var(--ink)" strokeWidth="5"/></svg>;
 return <Bread warm/>;
}
