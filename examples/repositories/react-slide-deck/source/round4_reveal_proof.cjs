const {chromium}=require('playwright'),fs=require('fs'),path=require('path');
(async()=>{const r=path.resolve(__dirname,'..'),b=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'}),p=await b.newPage({viewport:{width:1280,height:720},reducedMotion:'no-preference'}),errors=[];p.on('pageerror',e=>errors.push(String(e)));try{
await p.goto('http://127.0.0.1:8847/examples/repositories/react-slide-deck/index.html');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(900);const rows=[];
async function capture(name){const opacity=await p.locator('.questions>div').evaluateAll(es=>es.map(e=>Number(getComputedStyle(e).opacity)));await p.screenshot({path:path.join(r,`render/reveal-${name}.png`)});rows.push({phase:name,opacity,file:`render/reveal-${name}.png`})}
await capture('before');await p.getByRole('button',{name:'次へ',exact:true}).click();await p.waitForSelector('.questions',{state:'attached'});await p.waitForTimeout(70);await capture('mid');await p.waitForTimeout(1000);await capture('after');
fs.writeFileSync(path.join(r,'source/round4-reveal-proof.json'),JSON.stringify({author:'Codex browser QA',naturalOriginalVariants:true,rows,errors,quantitativeFrameRateMeasured:false,independentScore:false},null,2));
}finally{await b.close()}})();
