import {createRequire} from 'node:module';
const {PDFDocument}=createRequire(import.meta.url)('./runtime/node_modules/pdf-lib');
import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const pdf=await PDFDocument.load(fs.readFileSync(path.join(root,'original/deck.pdf')));const report={page_count:pdf.getPageCount(),sizes:pdf.getPages().map(p=>p.getSize()),source:'original/deck.pdf'};
fs.writeFileSync(path.join(root,'review/pdf-report.json'),JSON.stringify(report,null,2)+'\n');if(report.page_count!==7)throw Error('Expected seven pages');console.log(JSON.stringify(report));
