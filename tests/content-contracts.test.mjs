import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {validateDeck,renderSlide} from '../assets/slide-renderer.mjs';
import {exportDeck} from '../tools/render-deck.mjs';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const decks=JSON.parse(await fs.readFile(path.join(root,'data/decks.json'),'utf8'));
test('24ページが制作ソースと講稿を持ち、外部入力の文字はSVGでエスケープされる',()=>{
  assert.equal(decks.length,6);assert.equal(decks.reduce((n,d)=>n+d.slides.length,0),24);
  for(const d of decks){validateDeck(d);for(const s of d.slides)assert.ok(s.notes?.length>20);}
  const fixture=structuredClone(decks[0]);fixture.slides[0].nodes[1].text='<script>alert("x")</script>';
  const svg=renderSlide(fixture);assert.ok(!svg.includes('<script>'));assert.ok(svg.includes('&lt;script&gt;'));
});
test('エクスポートは単独HTMLとSVGを出力し、既存のフォルダを上書きしない',async()=>{
  const parent=await fs.mkdtemp(path.join(os.tmpdir(),'yebisu-contract-'));
  const out=path.join(parent,'new-deck');await exportDeck(decks[0],out);
  assert.ok((await fs.readFile(path.join(out,'index.html'),'utf8')).includes(decks[0].title));
  assert.ok((await fs.readFile(path.join(out,'slide-04.svg'),'utf8')).includes('採用を決める'));
  await assert.rejects(()=>exportDeck(decks[1],out),/存在/);
  assert.equal(JSON.parse(await fs.readFile(path.join(out,'deck.json'),'utf8')).id,decks[0].id);
  assert.equal(path.dirname(path.resolve(parent)),path.resolve(os.tmpdir()));
  assert.ok(path.basename(parent).startsWith('yebisu-contract-'));
  await fs.rm(parent,{recursive:true,force:true});
});
test('異常な座標・不正pathを出力へ通さない',()=>{
  const fixture=structuredClone(decks[0]);fixture.slides[0].nodes[0].w=2000;
  assert.throws(()=>validateDeck(fixture),/範囲/);
  fixture.slides[0].nodes[0]={type:'path',d:'<script>'};assert.throws(()=>validateDeck(fixture),/不正/);
});
test('すべての配布スキルが実行CLI、ライセンス、元の帰属を保持する',async()=>{
  const packs=JSON.parse(await fs.readFile(path.join(root,'data/refined-skills.json'),'utf8'));
  for(const pack of packs){
    const folder=path.join(root,'skills',pack.id);
    assert.ok((await fs.readFile(path.join(folder,'LICENSE'),'utf8')).length>100);
    await fs.access(path.join(folder,'scripts/render-deck.mjs'));await fs.access(path.join(folder,'scripts/export-pptx.mjs'));
    if(pack.upstream){const source=JSON.parse(await fs.readFile(path.join(folder,'UPSTREAM.json'),'utf8'));assert.equal(source.commit,pack.upstream.commit);}
  }
});
