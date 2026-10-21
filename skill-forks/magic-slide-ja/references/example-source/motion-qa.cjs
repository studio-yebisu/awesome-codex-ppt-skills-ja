// Real before/mid/after frames from the unchanged native Magic Move controller.
// Supply an authenticated URL via the environment; never store it in public receipts.
const {chromium}=require('playwright');
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const root=path.resolve(__dirname,'..'),pause=ms=>new Promise(r=>setTimeout(r,ms));
const sha=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
(async()=>{
 const url=new URL(process.env.MAGIC_QA_URL);url.search='ms_no_presenter=1';
 const browser=await chromium.launch({headless:true,executablePath:process.env.EDGE_PATH});
 try{
  const page=await browser.newPage({viewport:{width:1600,height:900},deviceScaleFactor:1});
  const errors=[],outside=[];page.on('pageerror',e=>errors.push(String(e)));
  page.on('request',r=>{if(!r.url().startsWith('http://127.0.0.1:')&&!r.url().startsWith('data:'))outside.push(new URL(r.url()).origin)});
  await page.goto(url.href,{waitUntil:'networkidle'});await page.waitForFunction(()=>typeof go==='function'&&typeof cur==='number');await page.evaluate(()=>document.fonts.ready);await pause(1800);
  await page.addStyleTag({content:'[id^="ms-cursor"]{display:none!important}'});
  const states=()=>page.evaluate(()=>({cur,animating,title:slides[cur].querySelector('h1,h2')?.innerText,shared:[...slides[cur].querySelectorAll('[data-magic-id]')].map(e=>({id:e.dataset.magicId,box:e.getBoundingClientRect().toJSON()})),clones:[...document.querySelectorAll('[data-ms-magic-clone-id]')].map(e=>({id:e.dataset.msMagicCloneId,transform:getComputedStyle(e).transform,box:e.getBoundingClientRect().toJSON()}))}));
  const boundaries=[];
  for(let i=0;i<4;i++){
   if(await page.evaluate(()=>cur)!==i)throw Error('unexpected starting page');
   const files={};const before=await states();
   files.before=`render/transition-${i+1}-${i+2}-before.png`;await page.screenshot({path:path.join(root,files.before)});
   await page.keyboard.press('ArrowRight');await pause(100);const early=await states();
   if(!early.animating||!early.clones.length)throw Error('native transition not active at boundary '+i);
   files.mid=`render/transition-${i+1}-${i+2}-mid.png`;await page.screenshot({path:path.join(root,files.mid)});const mid=await states();
   await page.waitForFunction(()=>!animating,{timeout:10000});await pause(350);const after=await states();
   if(after.cur!==i+1)throw Error('wrong destination');
   files.after=`render/transition-${i+1}-${i+2}-after.png`;await page.screenshot({path:path.join(root,files.after)});
   boundaries.push({from:i,to:i+1,before,early,mid,after,frames:Object.fromEntries(Object.entries(files).map(([k,v])=>[k,{path:v,sha256:sha(path.join(root,v))}]))});
  }
  await page.keyboard.press('ArrowLeft');await page.waitForFunction(()=>!animating);const reverse=await page.evaluate(()=>cur);
  const receipt={author:'Codex',route:'Actual original serve.py, authenticated URL supplied only via private environment; original native ArrowRight/ArrowLeft and Magic Move code.',artifact_sha256:sha(path.join(root,'index.html')),viewport:[1600,900],animation_policy:'Natural timing; no frozen animation, duration override, clone reconstruction or substitute renderer. Cursor/trail hidden for clean artifact frames only.',boundaries,reverse,errors,outside,visual_review:'pending',not_tested:['human rehearsal','cross-device motion smoothness','revision/adoption gate']};
  fs.writeFileSync(path.join(root,'source/motion-check.json'),JSON.stringify(receipt,null,2)+'\n');
  console.log(JSON.stringify({boundaries:boundaries.length,real_frames:boundaries.length*3,native_clone_counts:boundaries.map(x=>x.early.clones.length),reverse,errors,outside}));
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exit(1)});
