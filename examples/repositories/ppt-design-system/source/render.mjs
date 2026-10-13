// Local example verification. Node.js 22+, no npm dependencies. HTTP only.
import {spawn} from 'node:child_process';
import {mkdtempSync,writeFileSync,mkdirSync} from 'node:fs';
import os from 'node:os';import path from 'node:path';
const [url,chromePath]=process.argv.slice(2);if(!/^http:\/\/127\.0\.0\.1:\d+\/$/.test(url))throw Error('Local HTTP URL required');
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const chrome=spawn(chromePath,['--headless','--remote-debugging-port=0','--hide-scrollbars',`--user-data-dir=${mkdtempSync(path.join(os.tmpdir(),'designsystem-'))}`,'about:blank'],{stdio:['ignore','ignore','pipe']});
let ws;
try{
 const endpoint=await new Promise((resolve,reject)=>{let b='';const timeout=setTimeout(()=>reject(Error('Chrome startup timeout')),20000);chrome.stderr.on('data',x=>{b+=x;const m=/DevTools listening on (ws:\/\/\S+)/.exec(b);if(m){clearTimeout(timeout);resolve(m[1])}})});
 const targets=await(await fetch(`http://127.0.0.1:${new URL(endpoint).port}/json/list`)).json();ws=new WebSocket(targets.find(t=>t.type==='page').webSocketDebuggerUrl);await new Promise(r=>ws.addEventListener('open',r,{once:true}));
 let seq=0;const pending=new Map(),errors=[];ws.addEventListener('message',e=>{const d=JSON.parse(e.data);if(d.id){const p=pending.get(d.id);pending.delete(d.id);if(d.error)p?.reject(Error(JSON.stringify(d.error)));else p?.resolve(d.result)}else if(d.method==='Runtime.exceptionThrown')errors.push(d.params)});
 const send=(method,params={})=>new Promise((resolve,reject)=>{const id=++seq;pending.set(id,{resolve,reject});ws.send(JSON.stringify({id,method,params}))});
 const evaluate=async expression=>{const r=await send('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});if(r.exceptionDetails)throw Error(JSON.stringify(r.exceptionDetails));return r.result.value};
 await send('Page.enable');await send('Runtime.enable');await send('Emulation.setDeviceMetricsOverride',{width:1920,height:1080,deviceScaleFactor:1,mobile:false});
 await send('Page.navigate',{url:url+'deck.html'});await sleep(1400);mkdirSync('render',{recursive:true});const pages=[];
 for(let i=0;i<6;i++){
  await evaluate(`document.querySelectorAll('.slide')[${i}].scrollIntoView({behavior:'instant'})`);await sleep(450);
  const measured=await evaluate(`(()=>{const s=document.querySelectorAll('.slide')[${i}],bounds=s.getBoundingClientRect();const text=[...s.querySelectorAll('*')].filter(e=>e.children.length===0&&e.textContent.trim());return {index:${i},title:s.getAttribute('aria-label'),visible:Math.abs(bounds.left)<1,clipped:text.filter(e=>{const r=e.getBoundingClientRect();return r.top<bounds.top-1||r.bottom>bounds.bottom+1||r.left<bounds.left-1||r.right>bounds.right+1||e.scrollWidth>e.clientWidth+2}).map(e=>e.textContent),minFont:Math.min(...text.map(e=>parseFloat(getComputedStyle(e).fontSize)))}})()`);
  pages.push(measured);const png=await send('Page.captureScreenshot',{format:'png'});writeFileSync(`render/slide-${String(i+1).padStart(2,'0')}.png`,Buffer.from(png.data,'base64'));
 }
 const current=()=>evaluate("Math.round(document.getElementById('deck').scrollLeft/innerWidth)");const checks=[];
 await send('Input.dispatchKeyEvent',{type:'keyDown',key:'ArrowLeft',code:'ArrowLeft'});await send('Input.dispatchKeyEvent',{type:'keyUp',key:'ArrowLeft',code:'ArrowLeft'});await sleep(850);checks.push({action:'native ArrowLeft',passed:(await current())===4});
 await evaluate("document.querySelectorAll('#nav .dot')[1].click()");await sleep(850);checks.push({action:'native dot click',passed:(await current())===1});
 // Actual parent/child message exchange using a same-origin iframe harness.
 await send('Page.navigate',{url:url+'review/bridge-harness.html'});await sleep(1000);
 for(let i=0;i<6;i++){await evaluate(`document.querySelector('iframe').contentWindow.postMessage({type:'yebisu-slide',index:${i}},location.origin)`);await sleep(850);const result=await evaluate(`(()=>{const w=document.querySelector('iframe').contentWindow;return {index:Math.round(w.document.getElementById('deck').scrollLeft/w.innerWidth),notified:messages.some(m=>m.type==='yebisu-page'&&m.index===${i})}})()`);checks.push({action:'bridge '+i,...result,passed:result.index===i&&result.notified})}
 for(const bad of [-1,99,1.5,'2'])await evaluate(`document.querySelector('iframe').contentWindow.postMessage({type:'yebisu-slide',index:${JSON.stringify(bad)}},location.origin)`);await sleep(850);checks.push({action:'reject invalid indices',passed:await evaluate("Math.round(document.querySelector('iframe').contentWindow.document.getElementById('deck').scrollLeft/1920)===5")});
 await evaluate("document.querySelector('iframe').contentWindow.document.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',bubbles:true}))");await sleep(100);checks.push({action:'Escape close notification',passed:await evaluate("messages.some(m=>m.type==='yebisu-close')")});
 const report={passed:pages.every(p=>p.visible&&!p.clipped.length)&&checks.every(c=>c.passed)&&!errors.length,viewport:{width:1920,height:1080},http_only:true,pages,checks,errors};writeFileSync('render/report.json',JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));if(!report.passed)process.exitCode=1;
}finally{ws?.close();chrome.kill('SIGKILL')}
