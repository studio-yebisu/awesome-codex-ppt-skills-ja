import fs from 'node:fs/promises';
import { FileBlob, PresentationFile } from '@oai/artifact-tool';
const root=new URL('../',import.meta.url).pathname;
const p=await PresentationFile.importPptx(await FileBlob.load(root+'/deck.pptx'));
for(const [i,s] of p.slides.items.entries()) {const b=await p.export({slide:s,format:'png',scale:1.5});await fs.writeFile(root+'/render/slide-'+String(i+1).padStart(2,'0')+'.png',new Uint8Array(await b.arrayBuffer()));}
const m=await p.export({format:'webp',montage:true});await fs.writeFile(root+'/render/montage.webp',new Uint8Array(await m.arrayBuffer())); console.log('rendered',p.slides.items.length);
