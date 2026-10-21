// Artifact render, not a simulated interactive browser review.
const fs=require('fs');const path=require('path');const crypto=require('crypto');
const {chromium}=require('playwright');
const root=path.resolve(__dirname,'..');const hash=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
(async()=>{
 const output=path.join(root,'review/svg-render');fs.mkdirSync(output,{recursive:true});
 const regular=fs.readFileSync(path.join(root,'fonts/BIZUDPGothic-Regular.ttf')).toString('base64');
 const bold=fs.readFileSync(path.join(root,'fonts/BIZUDPGothic-Bold.ttf')).toString('base64');
 const css=`@font-face{font-family:'BIZ UDPGothic';src:url(data:font/ttf;base64,${regular});font-weight:400}@font-face{font-family:'BIZ UDPGothic';src:url(data:font/ttf;base64,${bold});font-weight:700}body{margin:0;width:1600px;height:900px;overflow:hidden}svg{transform-origin:0 0;transform:scale(1.25)}`;
 const browser=await chromium.launch();const page=await browser.newPage({viewport:{width:1600,height:900}});const rows=[];
 try{for(let n=1;n<=8;n++){
  const id=String(n).padStart(2,'0');const svg=path.join(root,`source/svg_output/${id}.svg`);const png=path.join(output,`slide-${id}.png`);
  await page.setContent(`<html lang="ja"><meta charset="utf-8"><style>${css}</style>${fs.readFileSync(svg,'utf8')}</html>`);
  await page.evaluate(()=>document.fonts.ready);
  const fontReady=await page.evaluate(()=>document.fonts.check('24px "BIZ UDPGothic"'));
  if(!fontReady)throw Error('BIZ font not loaded');
  await page.screenshot({path:png});rows.push({page:n,svg:`source/svg_output/${id}.svg`,source_sha256:hash(svg),image:`review/svg-render/slide-${id}.png`,sha256:hash(png),fontReady});
 }}finally{await browser.close();}
 fs.writeFileSync(path.join(output,'receipt.json'),JSON.stringify({renderer:'Playwright Chromium, native SVG + bundled BIZ static font, 1280x720 scaled 1.25 for 1600x900 comparison',pages:rows},null,2)+'\n');
 console.log('Rendered all eight actual source SVG pages with bundled fonts');
})().catch(e=>{console.error(e);process.exit(1)});
