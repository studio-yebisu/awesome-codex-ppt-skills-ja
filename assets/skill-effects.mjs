// Shared reading of data/skill-effects.json for the list, the player and repository.html.
// Missing records stay missing: nothing here fills in an effect that the data does not state.
import {playbackOrdinal} from './case-units.mjs';

export const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
export const IMAGE_PREVIEW_KINDS=['powerpoint-render','pdf-render','artifact-tool-pptx-import-render','libreoffice-pptx-pdf-render','generated-png-byte-matched-to-pptx-media','image-slides'];
const IMAGE=/\.(png|jpe?g|webp|gif|svg)(?:[?#]|$)/i;

// Arrays, strings or small objects ({必須:[...]}) become readable lines.
export function lines(v){
  if(Array.isArray(v))return v.flatMap(lines);
  if(v&&typeof v==='object')return Object.entries(v).map(([k,x])=>k+'：'+lines(x).join('、')).filter(s=>!s.endsWith('：'));
  const s=String(v??'').trim();return s?[s]:[];
}
export const text=v=>lines(v).join('、');

// Only repository-relative paths or https URLs are shown. Local absolute paths never reach the page.
export function safePath(p){
  const s=String(p??'').trim();
  if(!s||/^[A-Za-z]:|^[\\/]|\\|(^|\/)\.\.(\/|$)/.test(s))return '';
  if(/^[a-z][a-z0-9+.-]*:/i.test(s)&&!/^https:\/\//i.test(s))return '';
  return s;
}
export const isImage=p=>IMAGE.test(p||'');

export function previewUrl(c,path){const q=new URLSearchParams(path===c.preview?c.preview_options||{}:{});q.set('v',c.content_revision);return path+(path.includes('?')?'&':'?')+q}
export function interiorPath(c){return c.interior||c.representative_previews?.find(path=>path&&path!==c.cover)}
export function imagePath(c,i){return previewUrl(c,c.pages?.[i]||'examples/cases/'+c.id+'/render/slide-'+String(i+1).padStart(2,'0')+'.png')}
// A page image exists only for rendered previews or recorded page captures; Web decks without captures return ''.
export function pageImage(c,i){return c.pages?.[i]||IMAGE_PREVIEW_KINDS.includes(c.preview_kind)?imagePath(c,i):''}
export const formatLabel=c=>c?.format==='pptx'?'PowerPoint':c?.format==='pdf'?'PDF':'Web';
export const pageOrdinal=(c,i)=>playbackOrdinal(c,i);
export const unitWord=c=>c?.page_unit==='段階'?'段階':'ページ';

export async function loadSkillEffects(url='data/skill-effects.json'){
  try{
    const r=await fetch(url,{cache:'no-store'});if(!r.ok)return {skills:[],missing:true};
    const data=await r.json();
    return {...data,skills:Array.isArray(data?.skills)?data.skills.filter(s=>s&&typeof s.repository==='string'):[],missing:false};
  }catch{return {skills:[],missing:true}}
}

// Improvement entrances. Matching uses the recorded tags, plus production facts already in case-studies.json.
export const NEEDS=[
  {id:'motion',label:'動きで順に見せる',hint:'段階表示・アニメーション',words:['動き','アニメ','モーション','段階','演出','トランジション'],fact:c=>c?.page_unit==='段階'},
  {id:'edit',label:'受け取った人が編集できる',hint:'PowerPoint・ブラウザー編集',words:['編集','ネイティブ','native'],fact:c=>c?.format==='pptx'&&/native/i.test(c.editability||'')},
  {id:'diagram',label:'図解・概念図にする',hint:'矢印・注釈・構造',words:['図解','概念図','ダイアグラム','図表','チャート','フロー']},
  {id:'convert',label:'既存の資料を変換する',hint:'HTML・画像・PDF・PPTXから',words:['変換','既存','移行','取り込み'],fact:c=>/\.(pptx|pdf|png|jpe?g)$/i.test(c?.input||'')},
  {id:'layout',label:'レイアウトと書体を整える',hint:'版面・余白・デザイン規則',words:['レイアウト','デザイン','書体','タイポ','版面','配色']},
  {id:'academic',label:'数式・論文を発表にする',hint:'数式・研究発表',words:['数式','論文','学会','研究','TeX','LaTeX'],fact:c=>c?.editability==='native_math'||/tex/i.test(c?.editability||'')}
];
export function matchesNeed(item,id){
  const need=NEEDS.find(n=>n.id===id);if(!need)return true;
  if(Array.isArray(item.effect?.needs))return item.effect.needs.includes(id);
  const tags=item.tags.map(t=>t.normalize('NFKC').toLowerCase());
  return need.words.some(w=>tags.some(t=>t.includes(w.toLowerCase())))||Boolean(need.fact?.(item.case));
}
export const matchesFormat=(item,f)=>!f||f==='all'||item.case?.format===f||(f==='pptx'&&Boolean(item.case?.pptx_download));

export const pageHeading=(c,p)=>playbackOrdinal(c,p.index)+(p.title?'「'+p.title+'」':p.label?' '+p.label:'');
export const sourceLabel=p=>p.split('/').pop()||p;
export const skillName=item=>text(item.effect?.name)||item.entry?.title_ja||item.repository.split('/').pop();
export const detailUrl=item=>'repository.html?repo='+encodeURIComponent(item.repository)+(item.case?'&case='+encodeURIComponent(item.case.id):'')+(item.index>0?'&effect='+item.index:'');
export function upstreamUrl(item){
  const u=safePath(item.effect?.upstream?.url);
  if(/^https:\/\/github\.com\//i.test(u))return u;
  const commit=item.effect?.upstream?.commit||item.case?.upstream_commit;
  return 'https://github.com/'+item.repository+(commit?'/tree/'+commit:'');
}

function makeItem(repo,entry,record,index,own,fallback){
  const c=own||fallback,matches=Boolean(record&&own);
  const demo=record?.demonstration||{};
  const anchors=new Set();
  const pages=(Array.isArray(demo.pages)?demo.pages:[]).map((p,proofIndex)=>{
    const n=Number(p?.index),valid=Boolean(matches&&Number.isInteger(n)&&n>=0&&n<c.page_count);
    const proof=safePath(p?.proof_path),local=proof&&!/^https:/i.test(proof);
    const candidateInput=safePath(p?.input_path);
    const inputImage=valid&&candidateInput&&isImage(candidateInput)&&!/^https:/i.test(candidateInput)?previewUrl(c,candidateInput):'';
    const candidateArtifact=safePath(p?.artifact_path);
    const artifact=valid&&candidateArtifact&&!/^https:/i.test(candidateArtifact)&&/\.pptx$/i.test(candidateArtifact)?candidateArtifact:'';
    const primary=valid?pageImage(c,n):'';
    const supplemental=Boolean(primary&&local&&isImage(proof)&&proof.split(/[?#]/)[0]!==primary.split(/[?#]/)[0]);
    let anchor=supplemental?'proof-'+(proofIndex+1):'page-'+(n+1);
    if(anchors.has(anchor))anchor+='-proof-'+(proofIndex+1);
    anchors.add(anchor);
    // "4ページ目" in label repeats the ordinal shown from index; the page title is shown instead.
    const label=text(p?.label).replace(/^\d+\s*(ページ|段階|枚)目?$/,'');
    return {index:n,valid,anchor,supplemental,inputImage,artifact,artifactLabel:text(p?.artifact_label)||'この検証のPPTXを取得 ↓',inputLabel:text(p?.input_label)||'入力の図',outputLabel:text(p?.output_label)||'復元した図',label,title:text(p?.title).replace(/\s*\n\s*/g,' '),inspect:text(p?.what_to_inspect),rule:text(p?.skill_rule),proof,proofIsImage:isImage(proof),image:valid?(local&&isImage(proof)?previewUrl(c,proof):primary):''};
  });
  const r=record||{};
  const sources=lines(demo.source_proof_paths).map(safePath).filter(Boolean);
  const search=[r.name,r.job,r.problem,r.change,r.when_to_use,r.input,r.output,demo.applied_features,r.tags,repo,entry?.title_ja,entry?.description_ja,c?.title,c?.use_case].flatMap(lines).join(' ').normalize('NFKC').toLowerCase();
  return {key:repo+'#'+index,index,repository:repo,entry,effect:record,case:c,caseMatches:matches,recordedCaseId:text(record?.case_id),pages,sources,tags:lines(record?.tags),others:[],search};
}

// One item per effect record; repositories without a record still get one item so nothing published disappears.
export function buildSkillItems({entries,cases,activeIds,effects}){
  const byId=new Map(cases.map(c=>[c.id,c]));
  const active=activeIds.map(id=>byId.get(id)).filter(Boolean);
  for(const c of active)if(!c.cover)throw TypeError('作例の表紙がありません: '+c.id);
  const records=effects?.skills||[];
  const repos=[...new Set([...entries.map(e=>e.repository),...active.map(c=>c.repository)])];
  const result=[];
  for(const repo of repos){
    const entry=entries.find(e=>e.repository===repo)||null,repoCases=active.filter(c=>c.repository===repo);
    const fallback=repoCases.find(c=>c.id===entry?.featured_case_id)||repoCases[0]||null;
    const group=records.filter(r=>r.repository===repo).map((r,i)=>makeItem(repo,entry,r,i,byId.get(r.case_id)||null,fallback));
    if(!group.length)group.push(makeItem(repo,entry,null,0,null,fallback));
    const shown=new Set(group.map(i=>i.case?.id));
    group[0].others=repoCases.filter(c=>!shown.has(c.id));
    result.push(...group);
  }
  return result;
}
export const itemFor=(items,repo,caseId,effectIndex)=>{
  const own=items.filter(i=>i.repository===repo);
  return own.find(i=>i.index===effectIndex&&(!caseId||i.case?.id===caseId))||own.find(i=>i.case?.id===caseId)||own[0]||null;
};
