// Native reconstruction from measured ImageGen blueprints. One page per call.
const fs=require('fs'),path=require('path');
let PptxGenJS;try{PptxGenJS=require('pptxgenjs')}catch{PptxGenJS=require(path.resolve(__dirname,'../../../../.build/node_modules/pptxgenjs'))}
const out=path.resolve(__dirname,'..'), n=Number(process.argv[2]||1);
const recipe=JSON.parse(fs.readFileSync(path.join(out,`design/slide-${String(n).padStart(2,'0')}-elements.json`),'utf8'));
const pptx=new PptxGenJS();pptx.defineLayout({name:'CYBER',width:13.333,height:7.5});pptx.layout='CYBER';pptx.author='CyberPPT Japanese repository example';pptx.subject='架空の商店街企画';pptx.title=recipe.title;pptx.lang='ja-JP';
const s=pptx.addSlide();s.background={color:'F4F0E8'};
const sx=13.333/1672,sy=7.5/941;
const alignment=JSON.parse(fs.readFileSync(path.join(out,'source/optical-alignment.json'),'utf8')).pages.find(x=>x.slide===n);
for(const e of recipe.elements){
 const raw=e.draw_bbox_px||e.blueprint_bbox_px,a=alignment.elements.find(v=>v.element_id===e.element_id),b={...raw,x:raw.x+(a?.dx||0),y:e.element_id==='title'&&[2,3].includes(n)?Math.max(40,raw.y+(a?.dy||0)):raw.y+(a?.dy||0)},o={x:b.x*sx,y:b.y*sy,w:b.w*sx,h:b.h*sy,objectName:e.element_id};
 if(e.kind==='text')s.addText(e.text,{...o,fontFace:e.font||'Yu Gothic',fontSize:e.font_size_pt,color:e.color||'161616',bold:e.bold||false,margin:0,breakLine:false,align:e.align||'left',valign:'mid',paraSpaceAfterPt:0,transparency:0});
 else if(e.kind==='line')s.addShape(pptx.ShapeType.line,{...o,line:{color:e.color||'B8B6B1',width:e.width||0.8,beginArrowType:undefined,endArrowType:e.arrow?'triangle':undefined},flipV:e.flipV||false});
 else if(e.kind==='rect'||e.kind==='ellipse')s.addShape(pptx.ShapeType[e.kind],{...o,line:{color:e.stroke==='none'?'B8B6B1':e.stroke||'B8B6B1',width:e.width||0.8,transparency:e.stroke==='none'?100:0},fill:{color:e.fill||'F4F0E8',transparency:e.fill?0:100}});
 else if(e.kind==='icon'){let svg=fs.readFileSync(path.join(out,'design/icons/tabler-outline',e.icon+'.svg'),'utf8').replaceAll('currentColor','#9A5A2E');s.addImage({...o,data:'image/svg+xml;base64,'+Buffer.from(svg).toString('base64')});}
}
s.addNotes(recipe.notes);fs.mkdirSync(path.join(out,'pages'),{recursive:true});pptx.writeFile({fileName:path.join(out,`pages/slide-${String(n).padStart(2,'0')}.pptx`)});
