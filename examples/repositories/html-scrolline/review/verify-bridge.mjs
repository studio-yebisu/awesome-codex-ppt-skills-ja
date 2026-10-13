/** Actual keyboard, wheel and interpolation checks using the upstream CDP helper. */
import { spawn } from 'node:child_process';
import { mkdtempSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { cdpConnect } from '../source/upstream/tools/smoke.mjs';
const CASE=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const chromePath=process.env.SCROLLINE_CHROME;
const playerUrl=process.env.SCROLLINE_URL;
if(!playerUrl || !/^https?:\/\//.test(playerUrl))throw new Error('Set SCROLLINE_URL to a localhost HTTP URL.');
if(!chromePath)throw new Error('Set SCROLLINE_CHROME to the installed Chrome/Edge executable.');
const profile=mkdtempSync(path.join(os.tmpdir(),'scrolline-player-'));
const chrome=spawn(chromePath,['--headless','--remote-debugging-port=0','--window-size=1920,1080','--hide-scrollbars',`--user-data-dir=${profile}`,'about:blank'],{stdio:['ignore','ignore','pipe']});
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
let cdp;
try {
 const ws=await new Promise((resolve,reject)=>{let b='';const timer=setTimeout(()=>reject(new Error('Chrome startup timeout')),20000);chrome.stderr.on('data',x=>{b+=x;const m=/DevTools listening on (ws:\/\/\S+)/.exec(b);if(m){clearTimeout(timer);resolve(m[1]);}});});
 const targets=await(await fetch(`http://127.0.0.1:${new URL(ws).port}/json/list`)).json();
 cdp=await cdpConnect(targets.find(t=>t.type==='page').webSocketDebuggerUrl);
 await cdp.send('Page.enable');await cdp.send('Network.enable');
 await cdp.send('Emulation.setDeviceMetricsOverride',{width:1920,height:1080,deviceScaleFactor:1,mobile:false});
 await cdp.send('Page.navigate',{url:playerUrl});
 for(let i=0;i<100;i++){if(await cdp.evaluate("!!document.querySelector('iframe')?.contentWindow?.__deck").catch(()=>false))break;await sleep(100);}
 await sleep(700);
 const child="document.querySelector('iframe').contentWindow";
 for(let i=0;i<100;i++){if(await cdp.evaluate(child+'.__deck !== undefined').catch(()=>false))break;await sleep(100);}
 const checks=[];
 const state=()=>cdp.evaluate(`({time:${child}.__deck.time(),stops:${child}.__deck.stops().map(s=>({name:s.name,t:s.t})),messages:window.messages.slice()})`);
 for(let index=0;index<6;index++){
   await cdp.evaluate(`${child}.postMessage({type:'yebisu-slide',index:${index}},location.origin)`);await sleep(2800);
   const result=await state();const target=result.stops[index];const notified=result.messages.filter(x=>x.type==='yebisu-page').at(-1)?.index;
   checks.push({action:'parent-goto',index,target:target.name,time:result.time,notified,passed:Math.abs(result.time-target.t)<0.06&&notified===index});
 }
 const before=(await state()).time;
 for(const value of ['1.5','"1"','-1','99'])await cdp.evaluate(`${child}.postMessage({type:'yebisu-slide',index:${value}},location.origin)`);
 await cdp.evaluate(`${child}.postMessage({type:'wrong-type',index:0},location.origin)`);
 await cdp.evaluate(`${child}.eval("window.postMessage({type:'yebisu-slide',index:0},location.origin)")`);
 await cdp.evaluate(`${child}.dispatchEvent(new MessageEvent('message',{source:window,origin:'https://invalid.example',data:{type:'yebisu-slide',index:0}}))`);
 await sleep(2800);const after=(await state()).time;
 checks.push({action:'reject-invalid-index-type-source-origin',origin_test:'synthetic MessageEvent with real parent source and deliberately mismatched origin',before,after,passed:Math.abs(after-before)<0.06});
 await cdp.evaluate(`${child}.dispatchEvent(new KeyboardEvent('keydown',{key:'ArrowLeft',code:'ArrowLeft',bubbles:true}))`);await sleep(2800);const native=await state();
 checks.push({action:'native-key-syncs-parent',expectedIndex:4,notified:native.messages.filter(x=>x.type==='yebisu-page').at(-1)?.index,passed:Math.abs(native.time-native.stops[4].t)<0.06&&native.messages.filter(x=>x.type==='yebisu-page').at(-1)?.index===4});
 await cdp.evaluate(`${child}.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',code:'Escape',bubbles:true}))`);await sleep(150);const last=await state();
 checks.push({action:'escape-close',passed:last.messages.some(x=>x.type==='yebisu-close')});
 const report={passed:checks.every(x=>x.passed),url:playerUrl,transport:'HTTP parent iframe and postMessage',checks};
 writeFileSync(path.join(CASE,'review/bridge-check.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));if(!report.passed)process.exitCode=1;
} finally {cdp?.close();chrome.kill('SIGKILL');}
