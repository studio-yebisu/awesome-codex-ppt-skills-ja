/** Actual keyboard, wheel and interpolation checks using the upstream CDP helper. */
import { spawn } from 'node:child_process';
import { mkdtempSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { cdpConnect } from './upstream/tools/smoke.mjs';
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
 for(let i=0;i<100;i++){if(await cdp.evaluate('!!window.__deck').catch(()=>false))break;await sleep(100);}
 await sleep(700);
 const state=()=>cdp.evaluate('({time:window.__deck.time(),stops:window.__deck.stops().map(s=>({name:s.name,t:s.t})),lang:document.documentElement.lang})');
 const initial=await state();const checks=[];
 async function key(name,target){await cdp.send('Input.dispatchKeyEvent',{type:'keyDown',key:name,code:name});await cdp.send('Input.dispatchKeyEvent',{type:'keyUp',key:name,code:name});await sleep(2800);const after=await state();const goal=initial.stops.find(s=>s.name===target).t;checks.push({action:name,target,expected:goal,actual:after.time,passed:Math.abs(after.time-goal)<0.06});}
 checks.push({action:'initial-load',target:'opening',actual:initial.time,passed:Math.abs(initial.time-initial.stops[0].t)<0.06});
 await key('ArrowRight','prepare');await key('ArrowRight','prepare/venue');await key('ArrowLeft','prepare');await key('End','closing');await key('Home','opening');
 const beforeWheel=(await state()).time;await cdp.send('Input.dispatchMouseEvent',{type:'mouseWheel',x:960,y:540,deltaX:0,deltaY:550});await sleep(1500);const afterWheel=(await state()).time;checks.push({action:'wheel',before:beforeWheel,after:afterWheel,passed:afterWheel>beforeWheel+0.1});
 const motion=[];
 for(const t of [3.45,3.8,5.25,6.25]){await cdp.evaluate(`window.__deck.seek(${t})`);await sleep(650);motion.push(await cdp.evaluate(`({requested:${t},time:window.__deck.time(),prepareTrack:getComputedStyle(document.querySelector('[data-beat="prepare"] [data-part="track"]')).transform,deliverTrack:getComputedStyle(document.querySelector('[data-beat="deliver"] [data-part="track"]')).transform})`));}
 checks.push({action:'rail-advance-interpolation',passed:motion[0].prepareTrack!==motion[1].prepareTrack});
 checks.push({action:'era-shift-interpolation',passed:motion[2].deliverTrack!==motion[3].deliverTrack});
 const report={passed:checks.every(x=>x.passed),url:playerUrl,file_url:false,external_network_blocked:false,viewport:{width:1920,height:1080},language:initial.lang,checks,motion,scope:'Actual key and wheel input; intermediate original move transform values. No human adoption claimed.'};
 writeFileSync(path.join(CASE,'review/player-check.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));if(!report.passed)process.exitCode=1;
} finally {cdp?.close();chrome.kill('SIGKILL');}
