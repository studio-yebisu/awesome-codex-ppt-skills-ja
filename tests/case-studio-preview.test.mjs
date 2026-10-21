import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';

const root=new URL('../',import.meta.url);
const urls=['data/case-studies.json','data/repository-guides.json','data/product-collection.json','data/skill-effects.json'];
const data=new Map(await Promise.all(urls.map(async url=>[url,JSON.parse(await fs.readFile(new URL(url,root),'utf8'))])));
let run=0;

async function renderCatalog(changeCase){
  const fixtures=structuredClone(data),cases=fixtures.get('data/case-studies.json');
  const study=cases.find(c=>c.id==='presentation-forge-showcase');
  assert.ok(study,'Use the real case that exposed the missing interior failure');
  changeCase(study);
  const nodes=new Map();
  const defaults={'#skill-query':'','#skill-need':'all','#skill-format':'all','#skill-tag':'all'};
  const document={
    querySelector(selector){
      if(selector==='#case-detail')return null;
      if(!nodes.has(selector))nodes.set(selector,{value:defaults[selector]??'',innerHTML:'',textContent:'',addEventListener(){}});
      return nodes.get(selector);
    },
    addEventListener(){}
  };
  const globals={document,location:{href:'http://127.0.0.1:8847/',search:'',origin:'http://127.0.0.1:8847'},window:{addEventListener(){}},ResizeObserver:class{observe(){}},fetch:async url=>({ok:fixtures.has(url),json:async()=>fixtures.get(url)})};
  const previous=new Map(Object.keys(globals).map(key=>[key,Object.getOwnPropertyDescriptor(globalThis,key)]));
  try{
    for(const [key,value] of Object.entries(globals))Object.defineProperty(globalThis,key,{value,writable:true,configurable:true});
    await import(new URL('../assets/case-studio.mjs?preview-regression='+run++,import.meta.url));
    return {nodes,study,product:fixtures.get('data/product-collection.json')};
  }finally{
    for(const [key,descriptor] of previous)if(descriptor)Object.defineProperty(globalThis,key,descriptor);else delete globalThis[key];
  }
}

test('missing optional interior does not block the skill list or replace its recorded proof page',async()=>{
  const {nodes,study,product}=await renderCatalog(c=>{delete c.interior;});
  const skills=nodes.get('#skill-list').innerHTML;
  assert.equal([...skills.matchAll(/class="effect-card"/g)].length,product.entries.length);
  const skill=skills.split('<article ').find(part=>part.includes('data-open-case="'+study.id+'"'));
  assert.ok(skill.includes('data-open-page="3"'));
  assert.ok(skill.includes('4ページ目'));
  assert.ok(!/src="(?:undefined|null)/.test(skills));
});

test('a case with no optional interiors still links its recorded proof page',async()=>{
  const {nodes,study}=await renderCatalog(c=>{delete c.interior;delete c.representative_previews;});
  const skill=nodes.get('#skill-list').innerHTML.split('<article ').find(part=>part.includes('data-open-case="'+study.id+'"'));
  assert.ok(!/src="(?:undefined|null)/.test(skill));
  assert.ok(skill.includes('data-open-page="3"'));
});

test('a missing mandatory cover remains a catalog error',async()=>{
  await assert.rejects(()=>renderCatalog(c=>{delete c.cover;}),TypeError);
});
