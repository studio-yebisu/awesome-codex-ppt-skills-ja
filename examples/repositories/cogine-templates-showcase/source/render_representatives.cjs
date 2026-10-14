// Artifact output only: render two representatives in a fresh browser, using the original controller.
const {chromium}=require('playwright');
const fs=require('node:fs');
const path=require('node:path');
(async()=>{
 const url=process.argv[2],dir=path.resolve(process.argv[3]);
 const browser=await chromium.launch({channel:'chrome',headless:true});
 try {
  const page=await browser.newPage({viewport:{width:1600,height:900}});
  await page.goto(url,{waitUntil:'load'});
  await page.evaluate(()=>document.fonts.ready);
  await page.waitForTimeout(500);
  fs.mkdirSync(path.join(dir,'render'),{recursive:true});
  await page.screenshot({path:path.join(dir,'render/slide-01.png')});
  await page.locator('#nextBtn').click();
  await page.waitForFunction(()=>document.querySelector('#current').textContent==='2');
  await page.waitForTimeout(500);
  await page.screenshot({path:path.join(dir,'render/slide-02.png')});
  const state=await page.evaluate(()=>({total:document.querySelector('#total').textContent,page:document.querySelector('#current').textContent,title:document.title,activeHeading:document.querySelector('.slide.active h2').textContent}));
  fs.writeFileSync(path.join(dir,'source/first-display.json'),JSON.stringify({canvas:[1600,900],original_navigation:'nextBtn onclick changeSlide(1) → original updateSlide',...state},null,2)+'\n');
  console.log(JSON.stringify(state));
 } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
