// Two artifact images only. No verify walk, comparison, all-beat capture, or layout audit.
const {createRequire}=require('node:module');
const fs=require('node:fs'),path=require('node:path');
(async()=>{
 const url=process.argv[2],dir=path.resolve(process.argv[3]),runtime=path.resolve(process.argv[4]);
 const {chromium}=createRequire(path.join(runtime,'package.json'))('playwright-core');
 const browser=await chromium.launch({channel:'chrome',headless:true});
 try{
  const page=await browser.newPage({viewport:{width:1920,height:1080}});
  await page.goto(url,{waitUntil:'networkidle'});
  await page.waitForSelector('.stage');await page.evaluate(()=>document.fonts.ready);
  await page.waitForTimeout(1500);
  fs.mkdirSync(path.join(dir,'render'),{recursive:true});
  await page.screenshot({path:path.join(dir,'render/major-01.png')});
  const before=await page.evaluate(()=>location.hash);
  await page.locator('.viewport').click();
  await page.waitForFunction(()=>location.hash==='#2.1');await page.waitForTimeout(1500);
  await page.screenshot({path:path.join(dir,'render/major-02.png')});
  const state=await page.evaluate(()=>({hash:location.hash,scene_count:window.__beatdeck.beats.length,flattened_beats:window.__beatdeck.beats.reduce((n,s)=>n+s.length,0),qr:window.__beatdeck.qrUrl}));
  fs.writeFileSync(path.join(dir,'source/first-display.json'),JSON.stringify({canvas:[1920,1080],before,one_click_after:state.hash,cover_flattened_index:1,interior_flattened_index:2,...state},null,2)+'\n');
  console.log(JSON.stringify(state));
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
