// Playwright verification for the original Magic Slide server; does not modify its runtime.
const {chromium}=require(process.env.MAGIC_QA_PLAYWRIGHT||'playwright');
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const root=path.resolve(__dirname,'..');
const mode=process.argv[2]||'overview';
const base=process.env.MAGIC_QA_URL||'http://127.0.0.1:8765/deck/magic-slide/index.html';
const entryUrl=q=>{const u=new URL(base);u.search=q;return u.href;};
const pause=ms=>new Promise(resolve=>setTimeout(resolve,ms));
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:process.env.EDGE_PATH});
 const page=await browser.newPage({viewport:{width:1600,height:900},deviceScaleFactor:1});
 const errors=[],outside=[],qaReads=[];
 page.on('response',r=>{if(r.url().endsWith('/qa-issues'))qaReads.push({method:r.request().method(),status:r.status(),authenticated:!!r.request().headers()['x-magic-slide-token']});});
 page.on('pageerror',e=>errors.push(String(e)));
 page.on('request',r=>{if(!r.url().startsWith('http://127.0.0.1:')&&!r.url().startsWith('data:'))outside.push(r.url());});
 fs.mkdirSync(path.join(root,'render'),{recursive:true});
 if(mode==='overview'){
  await page.goto(entryUrl('ms_qa=overview&ms_qa_capture=1'),{waitUntil:'networkidle'});
  await page.waitForSelector('body.ms-qa-ready[data-ms-qa-pending="0"][data-ms-qa-timeouts="0"][data-ms-qa-errors="0"]',{timeout:60000});
  await page.addStyleTag({content:'[id^="ms-cursor"]{display:none!important}'});
  await pause(1500);
  await page.screenshot({path:path.join(root,'render/overview.png'),fullPage:true});
  const status=await page.evaluate(()=>({ready:document.body.classList.contains('ms-qa-ready'),pending:document.body.dataset.msQaPending,timeouts:document.body.dataset.msQaTimeouts,errors:document.body.dataset.msQaErrors,iframeCount:document.querySelectorAll('iframe').length}));
  fs.writeFileSync(path.join(root,'source/overview-capture.json'),JSON.stringify({status,errors,outside,qaReads,method:'Original QA capture URL; Playwright fullPage after readiness and settle'},null,2));
  console.log(JSON.stringify(status));
 } else {
  await page.goto(entryUrl('ms_no_presenter=1'),{waitUntil:'networkidle'});
  await page.waitForFunction(()=>typeof go==='function'&&typeof cur==='number');
  await page.evaluate(()=>document.fonts.ready);
  await pause(1800);
  await page.addStyleTag({content:'[id^="ms-cursor"]{display:none!important}'});
  const pages=[],motion=[];
  for(let i=0;i<5;i++){
   if(i){
    const before=await page.evaluate(()=>({cur,shared:Array.from(slides[cur].querySelectorAll('[data-magic-id]')).map(x=>x.dataset.magicId)}));
    await page.keyboard.press('ArrowRight');
    await pause(70);
    const first=await page.evaluate(()=>Array.from(document.querySelectorAll('[data-ms-magic-clone-id]')).map(e=>({id:e.dataset.msMagicCloneId,transform:getComputedStyle(e).transform})));
    await pause(180);
    const during=await page.evaluate(()=>({cur,animating,clones:Array.from(document.querySelectorAll('[data-ms-magic-clone-id]')).map(e=>({id:e.dataset.msMagicCloneId,transform:getComputedStyle(e).transform,box:{x:e.getBoundingClientRect().x,y:e.getBoundingClientRect().y,width:e.getBoundingClientRect().width,height:e.getBoundingClientRect().height}}))}));
    if(!during.clones.length)throw new Error('No native Magic Move clones at boundary '+i);
    await page.screenshot({path:path.join(root,`render/motion-${i}-${i+1}.png`)});
    await page.waitForFunction(()=>!animating,{timeout:10000});
    await pause(500);motion.push({before,first,during});
   }
   const state=await page.evaluate(()=>({cur,animating,title:slides[cur].querySelector('h1,h2')?.innerText,notes:slides[cur].dataset.speakerNotes,root:slides[cur].getBoundingClientRect().toJSON(),content:slides[cur].querySelector('.slide-content').getBoundingClientRect().toJSON(),cursor:!!document.getElementById('ms-cursor')}));
   if(state.cur!==i)throw new Error('Navigation did not reach '+i);
   await page.screenshot({path:path.join(root,`render/slide-0${i+1}.png`)});pages.push(state);
  }
  await page.keyboard.press('ArrowLeft');await page.waitForFunction(()=>!animating);const reverse=await page.evaluate(()=>cur);
  await page.evaluate(()=>toggleOverview());await pause(700);
  const overviewOpen=await page.evaluate(()=>document.getElementById('slide-overview').classList.contains('show'));
  await page.keyboard.press('Escape');await pause(500);
  const overviewClosed=await page.evaluate(()=>!document.getElementById('slide-overview').classList.contains('show'));
  const unauth=await page.request.get(new URL('qa-issues',base).href);
  const unauthorizedStatus=unauth.status();
  const http=require('http');
  const staticServer=http.createServer((req,res)=>{
   const url=new URL(req.url,'http://localhost');
   if(url.pathname==='/host.html'){res.setHeader('Content-Type','text/html');res.end('<!doctype html><iframe id="deck" src="/index.html?ms_no_presenter=1" style="border:0;width:1600px;height:900px"></iframe>');return;}
   const file=path.join(root,url.pathname.replace(/^\//,''));
   if(!file.startsWith(root+path.sep)||!fs.existsSync(file)||!fs.statSync(file).isFile()){res.statusCode=404;res.end();return;}
   res.setHeader('Content-Type',file.endsWith('.html')?'text/html':file.endsWith('.woff2')?'font/woff2':'application/octet-stream');res.end(fs.readFileSync(file));
  });
  await new Promise(resolve=>staticServer.listen(0,'127.0.0.1',resolve));
  const port=staticServer.address().port;const host=await browser.newPage({viewport:{width:1680,height:960}});const staticErrors=[];
  host.on('pageerror',e=>staticErrors.push(String(e)));
  await host.goto(`http://127.0.0.1:${port}/host.html`,{waitUntil:'networkidle'});
  const frame=host.frames().find(f=>f.url().includes('/index.html'));
  await frame.waitForFunction(()=>typeof go==='function');await pause(1500);
  await host.evaluate(()=>document.getElementById('deck').contentWindow.postMessage({type:'yebisu-slide',index:3},location.origin));
  await frame.waitForFunction(()=>cur===3&&!animating);
  const staticState=await frame.evaluate(()=>({cur,qaAllowed:MS_QA_ALLOWED,hasCursor:!!document.getElementById('ms-cursor'),hasDock:!!document.getElementById('slide-dock'),hasGo:typeof go==='function'}));
  await host.close();await new Promise(resolve=>staticServer.close(resolve));
  fs.writeFileSync(path.join(root,'source/browser-observations.json'),JSON.stringify({pages,motion,reverse,overviewOpen,overviewClosed,errors,outside,staticState,staticErrors,qaReads,unauthorizedStatus},null,2));
  console.log(JSON.stringify({pages:pages.length,motion:motion.map(m=>m.during),reverse,overviewOpen,overviewClosed,errors,outside}));
 }
 await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
