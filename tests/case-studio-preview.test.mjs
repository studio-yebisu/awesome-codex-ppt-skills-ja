import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';

const root=new URL('../',import.meta.url);
const urls=['data/case-studies.json','data/skills.json','data/previews.json','data/upstreams.json','data/repository-guides.json','data/product-collection.json'];
const data=new Map(await Promise.all(urls.map(async url=>[url,JSON.parse(await fs.readFile(new URL(url,root),'utf8'))])));
let run=0;

async function renderCatalog(changeCase){
  const fixtures=structuredClone(data),cases=fixtures.get('data/case-studies.json');
  const study=cases.find(c=>c.id==='presentation-forge-showcase');
  assert.ok(study,'Use the real case that exposed the missing interior failure');
  changeCase(study);
  const nodes=new Map();
  const defaults={'#case-format':'all','#case-editing':'all','#case-query':'','#skill-query':'','#skill-status':'all','#skill-order':'produced'};
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

test('missing optional interior uses the existing representative preview without blocking either catalog',async()=>{
  const {nodes,study,product}=await renderCatalog(c=>{delete c.interior;});
  const cards=nodes.get('#case-grid').innerHTML,skills=nodes.get('#skill-grid').innerHTML;
  assert.equal([...cards.matchAll(/class="case-card"/g)].length,product.active_case_ids.length);
  assert.equal([...skills.matchAll(/class="skill-item"/g)].length,product.entries.length);
  const card=cards.split('<article ').find(part=>part.includes('data-open-case="'+study.id+'"'));
  const skill=skills.split('<article ').find(part=>part.includes('data-open-case="'+study.id+'"'));
  assert.ok(card.includes(study.representative_previews[1]));
  assert.ok(skill.includes(study.representative_previews[1]));
  assert.ok(!/src="(?:undefined|null)/.test(cards+skills));
});

test('a cover-only case omits the optional interior image and uses its cover for the skill',async()=>{
  const {nodes,study}=await renderCatalog(c=>{delete c.interior;delete c.representative_previews;});
  const card=nodes.get('#case-grid').innerHTML.split('<article ').find(part=>part.includes('data-open-case="'+study.id+'"'));
  const skill=nodes.get('#skill-grid').innerHTML.split('<article ').find(part=>part.includes('data-open-case="'+study.id+'"'));
  assert.ok(!card.includes('interior-thumb'));
  assert.ok(card.includes(study.cover));
  assert.ok(skill.includes(study.cover));
});

test('a missing mandatory cover remains a catalog error',async()=>{
  await assert.rejects(()=>renderCatalog(c=>{delete c.cover;}),TypeError);
});
