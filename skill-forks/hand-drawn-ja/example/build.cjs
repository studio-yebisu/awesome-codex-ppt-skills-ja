/* Derived from the pinned original PptxGenJS + sharp recipe. See PROVENANCE.json. */
const fs=require('fs'),path=require('path'),cp=require('child_process');
const here=__dirname,pptxgen=require('pptxgenjs'),sharp=require('sharp');
async function svgToBase64Png(svgString,width,height){
 const pngBuffer=await sharp(Buffer.from(svgString)).resize(width,height,{fit:'contain',background:{r:0,g:0,b:0,alpha:0}}).png().toBuffer();
 return 'image/png;base64,'+pngBuffer.toString('base64');
}
async function main(){
 const data=JSON.parse(fs.readFileSync(path.join(here,'input/data.json'),'utf8'));
 const pres=new pptxgen();pres.defineLayout({name:'CUSTOM_16x9',width:13.333,height:7.5});pres.layout='CUSTOM_16x9';
 pres.author='Studio Yebisu';pres.subject='原典の配色・章扉配置による日本語作例';pres.title=data.title;pres.company='Studio Yebisu';pres.lang='ja-JP';
 for(let i=0;i<data.slides.length;i++){
  const item=data.slides[i],slide=pres.addSlide();slide.background={color:item.background};
  const svg=fs.readFileSync(path.join(here,'illustrations',i===0?'cover-sparkle.svg':`chapter-${String(i).padStart(2,'0')}.svg`),'utf8');
  slide.addImage({data:await svgToBase64Png(svg,900,750),x:i===0?10.7:5,y:i===0?1.1:.4,w:i===0?.9:8,h:i===0?.75:5.5});
  if(i===0){
   // Original Step5: title54pt+, upper left, no chapter label/full illustration.
   slide.addText(item.title,{x:1,y:1.8,w:9,h:2.1,fontSize:54,fontFace:'Georgia',bold:false,color:'141413',margin:0,valign:'top',paraSpaceAfterPt:0});
  }else{
   slide.addText(item.label,{x:1,y:5,w:4,h:.3,fontSize:14,fontFace:'Calibri',bold:false,color:'141413',margin:0,valign:'bottom'});
   slide.addText(item.title,{x:1,y:5.3,w:9,h:1,fontSize:40,fontFace:'Georgia',bold:false,color:'141413',margin:0,valign:'top'});
  }
  slide.addText(String(i+1),{x:12.3,y:7,w:.5,h:.25,fontSize:14,fontFace:'Calibri',color:'141413',align:'right',margin:0,valign:'bottom'});
  slide.addNotes(item.notes+' 日本語グリフだけYu Minchoを明示する派生。欧文Georgia/Calibri、原典の字号・位置は保持。');
 }
 await pres.writeFile({fileName:path.join(here,'deck.pptx')});
 const r=cp.spawnSync(process.env.HANDDRAWN_PYTHON||'python',[path.join(here,'source/japanese_font_adapter.py'),path.join(here,'deck.pptx')],{encoding:'utf8'});
 if(r.status!==0)throw new Error(r.stderr||r.stdout||'Japanese font adapter failed');
 console.log(r.stdout.trim());console.log('Generated5chapter dividers using pinned original recipe.');
}
main().catch(e=>{console.error(e);process.exit(1)});
