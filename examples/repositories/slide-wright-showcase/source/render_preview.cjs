// Artifact rendering only: a fresh headless browser, no user profile or user tabs.
const { chromium } = require('playwright');
const fs = require('node:fs');
const path = require('node:path');
(async () => {
 const target=process.argv[2],caseDir=path.resolve(process.argv[3]);
 const browser=await chromium.launch({channel:'chrome',headless:true});
 try {
  const page=await browser.newPage({viewport:{width:1920,height:1080}});
  await page.goto(target,{waitUntil:'networkidle'});
  await page.waitForFunction(()=>window.Reveal && Reveal.isReady());
  await page.evaluate(()=>document.fonts.ready);
  await page.waitForTimeout(900);
  const engine=await page.evaluate(()=>({ready:Reveal.isReady(),version:Reveal.VERSION,pages:Reveal.getTotalSlides(),first_index:Reveal.getIndices().h}));
  if(engine.pages!==2) throw new Error('Render the real two-slide stage before append.');
  fs.mkdirSync(path.join(caseDir,'render'),{recursive:true});
  await page.screenshot({path:path.join(caseDir,'render/slide-01.png')});
  await page.keyboard.press('ArrowRight');
  await page.waitForFunction(()=>Reveal.getIndices().h===1);
  await page.waitForTimeout(1000);
  await page.screenshot({path:path.join(caseDir,'render/slide-02.png')});
  engine.second_index=await page.evaluate(()=>Reveal.getIndices().h);
  fs.writeFileSync(path.join(caseDir,'source/preview-runtime.json'),JSON.stringify(engine,null,2)+'\n');
  console.log(JSON.stringify(engine));
 } finally {await browser.close();}
})().catch(err=>{console.error(err);process.exit(1)});
