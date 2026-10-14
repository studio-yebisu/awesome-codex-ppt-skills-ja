import type {Position,TimelineHost} from 'beatdeck';
import {reducedMotion} from 'beatdeck';
export interface Live {breadReady:boolean}
export function initialLive({scene,beat}:Position):Live {return {breadReady:scene>3||(scene===3&&beat>=1)};}
/** Visual timing only: not baking time. Never auto-advance; every next step remains a click. */
export function timeline({scene,beat}:Position,host:TimelineHost<Live>) {
 if(scene===3&&beat===0) {
  if(reducedMotion.get())host.setLive({breadReady:true});
  else host.at(550,()=>host.setLive({breadReady:true}));
 }
}
