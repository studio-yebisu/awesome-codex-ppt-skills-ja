// Original portable native-object exporter by Studio Yebisu. CC0-1.0.
// PptxGenJS is an external MIT-licensed dependency; not bundled in the skill.
import fs from 'node:fs/promises';
import path from 'node:path';
import {validateDeck} from '../assets/slide-renderer.mjs';
const [input,output]=process.argv.slice(2);
if(!input||!output)throw new Error('使い方: node scripts/export-pptx.mjs input.json new-output.pptx');
try{await fs.stat(output);throw new Error('出力ファイルが存在します。新しいファイル名を指定してください。')}catch(error){if(error.code!=='ENOENT')throw error;}
const {default:PptxGenJS}=await import('pptxgenjs');
const deck=validateDeck(JSON.parse(await fs.readFile(input,'utf8')));
const pptx=new PptxGenJS();pptx.defineLayout({name:'YEBISU',width:13.333333,height:7.5});pptx.layout='YEBISU';
pptx.author='Studio Yebisu';pptx.subject='日本語の編集可能スライド';pptx.title=deck.title;pptx.lang='ja-JP';
const color=(s,fallback='171B27')=>/^#[0-9a-f]{6}$/i.test(s||'')?s.slice(1):fallback;
for(const page of deck.slides){
  const slide=pptx.addSlide();slide.background={color:color(page.background||deck.background)};
  for(const n of page.nodes){
    const fill=n.fill==='none'?{color:'FFFFFF',transparency:100}:{color:color(n.fill,deck.ink?.slice(1))};
    const line={color:color(n.stroke,'FFFFFF'),width:(n.strokeWidth||0)*.75,transparency:n.stroke==='none'||!n.stroke?100:0};
    if(n.type==='text'){
      const lines=n.text.split('\n'),fontSize=n.size*.75;
      const estimatedWidth=Math.max(...lines.map(s=>[...s].reduce((w,c)=>w+(/[\u0000-\u00ff]/.test(c)?.59:1),0)))*n.size;
      const w=Math.min(1280,Math.max(estimatedWidth+24,140));
      let left=n.x;if(n.anchor==='middle')left-=w/2;else if(n.anchor==='end')left-=w;
      slide.addText(n.text,{x:left/96,y:(n.y-n.size*1.14)/96,w:Math.min(w,1280-left)/96,h:(lines.length*(n.leading||n.size*1.45)+12)/96,
        fontFace:n.font||page.font||deck.font||'Noto Sans JP',fontSize,bold:(n.weight||400)>=600,color:color(n.fill,deck.ink?.slice(1)),
        margin:0,breakLine:false,align:n.anchor==='middle'?'center':n.anchor==='end'?'right':'left',valign:'top',paraSpaceAfter:0,
        lineSpacingMultiple:1.0,lang:'ja-JP'});
    }else if(n.type==='rect')slide.addShape(pptx.ShapeType.rect,{x:n.x/96,y:n.y/96,w:n.w/96,h:n.h/96,fill,line});
    else if(n.type==='circle')slide.addShape(pptx.ShapeType.ellipse,{x:(n.x-n.r)/96,y:(n.y-n.r)/96,w:n.r*2/96,h:n.r*2/96,fill,line});
    else if(n.type==='line')slide.addShape(pptx.ShapeType.line,{x:Math.min(n.x,n.x2)/96,y:Math.min(n.y,n.y2)/96,w:Math.abs(n.x2-n.x)/96,h:Math.abs(n.y2-n.y)/96,flipV:(n.x2-n.x)*(n.y2-n.y)<0,line:{...line,transparency:0}});
    else if(n.type==='path'){
      const svg=`<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720"><path d="${n.d}" fill="${n.fill||'none'}" stroke="${n.stroke||'#171B27'}" stroke-width="${n.strokeWidth||2}"/></svg>`;
      slide.addImage({data:'image/svg+xml;base64,'+Buffer.from(svg).toString('base64'),x:0,y:0,w:13.333333,h:7.5});
    }
  }
  slide.addNotes(page.notes||page.title);
}
await fs.mkdir(path.dirname(path.resolve(output)),{recursive:true});
await pptx.writeFile({fileName:path.resolve(output)});
console.log(`編集可能PPTX: ${deck.slides.length}枚 / ${path.resolve(output)}`);
