// Artifact-only capture and layout inspection over the local HTTP input.
import { chromium } from 'playwright';
import fs from 'fs/promises';
import path from 'path';
const root=process.argv[process.argv.indexOf('--root')+1];
if(!process.env.YEBISU_DECK_BASE_URL)throw new Error('HTTP base required');
const files=(await fs.readdir(path.join(root,'slides'))).filter(f=>f.endsWith('.html')).sort();
await fs.mkdir(path.join(root,'html-render'),{recursive:true});
const browser=await chromium.launch();
const page=await browser.newPage({viewport:{width:1280,height:720}});
const errors=[];page.on('pageerror',e=>errors.push(String(e)));page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});
const pages=[];
for(const file of files){
  await page.goto(new URL('slides/'+file,process.env.YEBISU_DECK_BASE_URL).href,{waitUntil:'networkidle'});
  await page.evaluate(()=>document.fonts.ready);
  const metrics=await page.evaluate(()=>{
    const body=document.body.getBoundingClientRect();
    const overflow=[];
    for(const el of document.querySelectorAll('p,h1,h2')){
      const r=el.getBoundingClientRect();
      if(r.left<body.left-.5 || r.top<body.top-.5 || r.right>body.right+.5 || r.bottom>body.bottom+.5 || el.scrollWidth>el.clientWidth+1 || el.scrollHeight>el.clientHeight+1)overflow.push(el.textContent);
    }
    return {title:document.title,text:document.body.innerText,width:body.width,height:body.height,overflow,fontReady:document.fonts.check('24px "BIZ UDPGothic"')};
  });
  const id=file.slice(0,2);
  await page.screenshot({path:path.join(root,'html-render',`slide-${id}.png`)});
  pages.push({file,...metrics});
}
await browser.close();
const report={viewport:{width:1280,height:720},protocol:'http',pages,consoleErrors:errors};
await fs.writeFile(path.join(root,'html-render','metrics.json'),JSON.stringify(report,null,2)+'\n');
if(errors.length || pages.some(p=>p.overflow.length || !p.fontReady))throw new Error('HTML capture contains errors; inspect metrics');
console.log(JSON.stringify({pages:pages.length,consoleErrors:0,overflow:0,fontReady:true}));
