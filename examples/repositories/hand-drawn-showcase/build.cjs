/* Direct adaptation of the original SKILL's PptxGenJS + sharp template. */
const fs=require('fs'),path=require('path');
const here=__dirname;
function load(name){try{return require(name)}catch{return require(path.resolve(here,'../../../.build/node_modules',name))}}
const pptxgen=load('pptxgenjs'),sharp=load('sharp');
async function svgToBase64Png(svgString,width,height){const pngBuffer=await sharp(Buffer.from(svgString)).resize(width,height,{fit:'contain',background:{r:0,g:0,b:0,alpha:0}}).png().toBuffer();return 'image/png;base64,'+pngBuffer.toString('base64')}
async function main(){const data=JSON.parse(fs.readFileSync(path.join(here,'input/data.json'),'utf8'));const pres=new pptxgen();pres.defineLayout({name:'CUSTOM_16x9',width:13.333,height:7.5});pres.layout='CUSTOM_16x9';pres.author='Studio Yebisu';pres.subject='日本語の手描き章扉サンプル';pres.title=data.title;pres.company='Studio Yebisu';pres.lang='ja-JP';
for(let i=0;i<data.slides.length;i++){const item=data.slides[i],slide=pres.addSlide();slide.background={color:item.background};
 const frame=`<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="950" viewBox="0 0 1800 950"><path d="M55 60 Q 885 48 1740 65 Q1753 450 1740 885 Q 900 896 55 881 Q43 430 55 60" fill="none" stroke="#DE4634" stroke-width="3" stroke-linejoin="round"/></svg>`;
 slide.addImage({data:await svgToBase64Png(frame,1800,950),x:.25,y:.2,w:12.82,h:6.76});
 const svg=fs.readFileSync(path.join(here,'illustrations',`chapter-${String(i).padStart(2,'0')}.svg`),'utf8');
 slide.addImage({data:await svgToBase64Png(svg,900,750),x:i===0?7.0:5.0,y:i===0?.65:.4,w:i===0?5.5:8.0,h:i===0?4.9:5.5});
 if(i===0){slide.addText(item.label,{x:.9,y:.75,w:6.5,h:.35,fontFace:'Manrope',fontSize:14,color:'141413',margin:0,charSpacing:2});slide.addText(item.title,{x:.88,y:2.0,w:7.0,h:2.15,fontFace:'Dela Gothic One',fontSize:42,color:'141413',bold:false,margin:0,breakLine:false});slide.addText(item.caption,{x:.95,y:5.65,w:9.5,h:.5,fontFace:'Zen Maru Gothic',fontSize:20,color:'141413',margin:0});}
 else{slide.addText(item.label,{x:1.0,y:4.96,w:6.5,h:.3,fontFace:'Manrope',fontSize:14,color:'141413',margin:0,valign:'bottom',charSpacing:1.5});slide.addText(item.title,{x:1.0,y:5.3,w:9.0,h:.8,fontFace:'Zen Maru Gothic',fontSize:44,color:'141413',bold:true,margin:0,valign:'top'});slide.addText(item.caption,{x:1.02,y:6.26,w:10.8,h:.5,fontFace:'Zen Maru Gothic',fontSize:18,color:'141413',margin:0});}
 slide.addText(String(i+1).padStart(2,'0'),{x:12.0,y:7.0,w:.65,h:.25,fontFace:'Manrope',fontSize:14,color:'141413',align:'right',margin:0,valign:'bottom'});
 slide.addText(i===0?'架空のチームワークショップ / 章扉の作例':'チームのアイデアを、育てる。 / 章扉サンプル',{x:.8,y:7.03,w:10.5,h:.22,fontFace:'Zen Maru Gothic',fontSize:9,color:'645D53',margin:0});slide.addNotes(item.notes);
}await pres.writeFile({fileName:path.join(here,'deck.pptx')});console.log('Generated original-recipe chapter dividers: 5 slides');}
main().catch(e=>{console.error(e);process.exit(1)});
