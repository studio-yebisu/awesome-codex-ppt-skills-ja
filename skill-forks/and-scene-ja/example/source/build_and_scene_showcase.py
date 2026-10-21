"""Scaffold the original and-scene bootstrap, author typed steps, install and build."""
from pathlib import Path
import argparse, difflib, hashlib, json, shutil, subprocess
ROOT=Path(__file__).resolve().parents[1]
PIN='5ce44dff61f181db35b0c98a1cb86c71c7e062cb'
UP=ROOT/'.build/actual-upstreams/Codagent-AI__and-scene'
APP=ROOT/'.build/and-scene-app'
CASE=ROOT/'examples/repositories/and-scene-showcase'

def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
def js(p,d):write(p,json.dumps(d,ensure_ascii=False,indent=2))
TITLES=['一冊の本が、次の人へ。','読み終えた一冊を、本棚へ。','本の名前と、ひとことを添える。','次の読み手が、一冊を見つける。','読みたい本を、持ち帰る。','読み終えたら、次へつなぐ。','もう一度、本棚へ。','一冊を、次の人へ。']
CAPTIONS=['架空の交換本棚の提案。同じ一冊が、置く・見つける・戻すをつなぎます。','持ち主から、共通の本棚へ。一冊の位置が変わり、関係が見えてきます。','本の名前と短いひとことを添える、という参加の案。','本棚を眺める次の読み手と、同じ一冊をつなぎます。','本棚の一冊が、次の読み手の側へ移ります。','読み終わった一冊を、次の人へつなぐことを考えます。','同じ一冊を共通の本棚へ戻す。交換の輪をもう一度。','本棚を介して、一冊を次の人へ。料金・住所・営業実績は未設定です。']
PAYLOADS=[
 {'book':[340,55,200,270],'owner':0,'shelf':0,'reader':0,'arrow':'','note':False},
 {'book':[290,132,106,145],'owner':1,'shelf':1,'reader':0,'arrow':'place','note':False},
 {'book':[433,153,66,95],'owner':.18,'shelf':1,'reader':0,'arrow':'','note':True},
 {'book':[433,153,66,95],'owner':.12,'shelf':1,'reader':1,'arrow':'find','note':False},
 {'book':[545,142,80,116],'owner':.12,'shelf':.45,'reader':1,'arrow':'take','note':False},
 {'book':[545,142,80,116],'owner':.12,'shelf':.12,'reader':1,'arrow':'','note':False},
 {'book':[433,153,66,95],'owner':.12,'shelf':1,'reader':.22,'arrow':'return','note':False},
 {'book':[433,153,66,95],'owner':1,'shelf':1,'reader':1,'arrow':'cycle','note':False},
]

def prepare():
    assert APP.resolve().is_relative_to((ROOT/'.build').resolve())
    boot=UP/'skills/presentation/templates/bootstrap'
    if APP.exists() and not (APP/'AND-SCENE-OWNED.json').exists():raise RuntimeError('Private app exists without ownership receipt')
    APP.mkdir(parents=True,exist_ok=True)
    js(APP/'AND-SCENE-OWNED.json',{'repository':'Codagent-AI/and-scene','commit':PIN,'scaffold_target':str(APP.resolve()),'initial_target':'private empty app','original_bootstrap':str(boot)})
    shutil.copytree(boot,APP,dirs_exist_ok=True,ignore=shutil.ignore_patterns('assets'))
    CASE.mkdir(parents=True,exist_ok=True)
    original=CASE/'source/upstream'
    shutil.copytree(UP/'skills/presentation',original/'skills/presentation',dirs_exist_ok=True,ignore=shutil.ignore_patterns('assets'))
    shutil.copy2(UP/'LICENSE',CASE/'LICENSE');shutil.copy2(UP/'LICENSE',original/'LICENSE')
    package=json.loads((APP/'package.json').read_text());package['name']='and-scene-book-exchange-ja';js(APP/'package.json',package)
    write(APP/'vite.config.ts',"import { defineConfig } from 'vite'\nimport react from '@vitejs/plugin-react'\nexport default defineConfig({plugins:[react()],base:'./'})\n")
    write(APP/'src/Root.tsx',ROOT_TSX)
    write(APP/'src/index.css','html,body,#root{margin:0;min-height:100%;background:#081629;}body{font-family:"BIZ UDPGothic",sans-serif;}*{box-sizing:border-box;}button,a{font:inherit;}button{cursor:pointer;}a{color:inherit;}\n')
    registry=(boot/'src/presentations/index.ts').read_text(encoding='utf-8')
    write(APP/'src/presentations/index.ts',REGISTRY)
    talk=APP/'src/presentations/book-exchange'
    shutil.copytree(UP/'skills/presentation/templates/presentation',talk,dirs_exist_ok=True)
    write(talk/'entities.ts',"export const ENTITIES={book:'book-world/book',owner:'book-world/owner',shelf:'book-world/shelf',reader:'book-world/reader',arrow:'book-world/arrow',note:'book-world/note'} as const\n")
    write(talk/'Scene.tsx',SCENE)
    write(talk/'Talk.tsx',TALK)
    for i,(title,caption,payload) in enumerate(zip(TITLES,CAPTIONS,PAYLOADS)):
        era='置く' if i<3 else '見つける' if i<5 else '戻す'
        # Actual original Step template becomes typed metadata + persistent Scene.
        text='''import type { Step } from '../../../presentation-kit'\nimport { BookWorld, type WorldPayload } from '../Scene'\nexport const step: Step<WorldPayload> = {\n'''+f"  id:'book-step-{i+1}',era:{json.dumps(era,ensure_ascii=False)},title:{json.dumps(title,ensure_ascii=False)},caption:{json.dumps(caption,ensure_ascii=False)},groupKey:'book-world',payload:{json.dumps(payload,ensure_ascii=False)},Scene:BookWorld\n}}\n"
        write(talk/f'steps/step{i+1:02}.tsx',text)
    # Bootstrap's example intro is not registered; do not keep unresolved template tokens in build.
    intro=talk/'steps/intro.tsx'
    if intro.exists():intro.unlink()
    fonts=json.loads((ROOT/'data/oss-font-kit.json').read_text(encoding='utf-8'))['families'];receipts=[];faces=[]
    choices={'bizudpgothic':['BIZUDPGothic-Regular.ttf'],'shipporimincho':['ShipporiMincho-Bold.ttf'],'manrope':['Manrope[wght].ttf']}
    for family in fonts:
        if family['id'] not in choices:continue
        selected=[];folder=APP/'public/fonts'/family['id'];folder.mkdir(parents=True,exist_ok=True)
        shutil.copy2(ROOT/family['license_file'],folder/'OFL.txt')
        for entry in family['files']:
            src=ROOT/entry['file']
            if src.name not in choices[family['id']]:continue
            assert hashlib.sha256(src.read_bytes()).hexdigest()==entry['sha256']
            shutil.copy2(src,folder/src.name);selected.append({**entry,'file':f"fonts/{family['id']}/{src.name}"})
            weight='700' if 'Bold' in src.name else '200 800' if family['id']=='manrope' else '400'
            faces.append(f'@font-face{{font-family:"{family["family"]}";src:url("/fonts/{family["id"]}/{src.name}") format("truetype");font-weight:{weight};font-display:block;}}')
        receipts.append({**{k:v for k,v in family.items() if k!='files'},'files':selected})
    js(APP/'public/fonts/SOURCE.json',receipts)
    write(talk/'style.css','\n'.join(faces)+'\n'+CSS)
    navfile=APP/'src/presentation-kit/usePresentationNav.ts'
    nav=navfile.read_text(encoding='utf-8')
    nav=nav.replace('  return { step, setStep, next, prev, last, mode, toggleMode }',BRIDGE+'\n  return { step, setStep, next, prev, last, mode, toggleMode }')
    write(navfile,nav)
    write(APP/'public/favicon.svg','<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><path fill="#578aff" d="M6 3h21v26H6z"/><path stroke="#ffb5a5" stroke-width="2" d="M9 3v26"/></svg>')
    write(APP/'index.html','<!doctype html><html lang="ja"><head><meta charset="UTF-8"><link rel="icon" href="./favicon.svg"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>一冊の本が、次の人へ。</title></head><body><div id="root"></div><script type="module" src="/src/main.tsx"></script></body></html>\n')
    patches=[]
    for rel in ['package.json','vite.config.ts','src/Root.tsx','src/index.css','src/presentations/index.ts','src/presentation-kit/usePresentationNav.ts','index.html']:
        a=(boot/rel).read_text(encoding='utf-8');b=(APP/rel).read_text(encoding='utf-8')
        patches.append(''.join(difflib.unified_diff(a.splitlines(True),b.splitlines(True),fromfile='upstream/bootstrap/'+rel,tofile='app/'+rel)))
    write(CASE/'source/local.diff','\n'.join(patches)+'\n# Added src/presentations/book-exchange typed steps, persistent Scene, stable ids, own styles.\n# Replaced demo Landing entry with registered book-exchange route; omitted unused upstream images/logos.\n')
    hashes={str(p.relative_to(boot)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in (boot/'src/presentation-kit').rglob('*') if p.is_file()}
    js(CASE/'source/UPSTREAM-KIT-SHA256.json',hashes)
    js(CASE/'input/steps.json',{'common_canvas':[880,380],'stable_namespace':['book','owner','shelf','reader','arrow'],'groupKey':'book-world','steps':[{'index':i,'title':t,'caption':c,'payload':p} for i,(t,c,p) in enumerate(zip(TITLES,CAPTIONS,PAYLOADS))]})

ROOT_TSX='''import { PresentationRouter } from './presentations/PresentationRouter'
export function Root(){return <PresentationRouter slug="book-exchange" />}
'''
REGISTRY='''export const presentations=[{slug:'book-exchange',title:'一冊の本が、次の人へ。',load:()=>import('./book-exchange/Talk')}]\nexport const presentationSlugs=new Set(presentations.map(p=>p.slug))\n'''
TALK='''import { Presentation, type Step } from '../../presentation-kit'
import type { WorldPayload } from './Scene'
'''+''.join(f"import {{step as step{i}}} from './steps/step{i:02}'\n" for i in range(1,9))+'''import './style.css'
const STEPS:Step<WorldPayload>[]=['''+','.join(f'step{i}' for i in range(1,9))+''']
export default function Talk(){return <main className="book-talk"><Presentation steps={STEPS} title="一冊の本が、次の人へ。" initialMode="browse" brand={<span className="proposal">交換本棚の提案 <small>架空の企画</small></span>} homeHref="./index.html" homeLabel="提案の最初へ" marker={i=>`${String(i+1).padStart(2,'0')} / 08`} /></main>}
'''
SCENE='''import { motion } from 'motion/react'
import { SceneLayer, MotionNode, Label, Arrow, type SceneProps } from '../../presentation-kit'
import { ENTITIES } from './entities'
export type WorldPayload={book:number[];owner:number;shelf:number;reader:number;arrow:string;note:boolean}
const labelOpacity=(n:number)=>n===0?0:Math.max(n,.75)
function Person({role,opacity}:{role:string;opacity:number}){return <><motion.svg animate={{opacity}} viewBox="0 0 100 110" aria-hidden="true"><circle cx="50" cy="28" r="19"/><path d="M15 104V91c0-22 16-35 35-35s35 13 35 35v13"/></motion.svg><motion.span animate={{opacity:labelOpacity(opacity)}}>{role}</motion.span></>}
function Book(){return <svg viewBox="0 0 150 205" aria-label="同じ一冊の本"><path className="book-front" d="M13 7H143V196H13c-9 0-12-7-12-15V24C1 13 5 7 13 7Z"/><path className="book-spine" d="M13 7V196M14 185H140"/><path className="book-lines" d="M44 55H111M44 63H90"/><text x="77" y="113" textAnchor="middle">BOOK</text><path className="book-mark" d="M100 7V35l10-6 10 6V7"/></svg>}
export function BookWorld({step}:SceneProps<WorldPayload>){const p=step.payload!;const [x,y,w,h]=p.book;return <SceneLayer className="world">
<div className="place owner-place"><MotionNode layoutId={ENTITIES.owner}><motion.div className="person"><Person role="持ち主" opacity={p.owner}/></motion.div></MotionNode></div>
<div className="place shelf-place"><MotionNode layoutId={ENTITIES.shelf}><motion.div className="shelf"><motion.svg animate={{opacity:p.shelf}} viewBox="0 0 230 250" aria-hidden="true"><path d="M20 20H210V230H20ZM20 100H210M20 180H210M44 230V245M186 230V245"/></motion.svg><motion.span animate={{opacity:labelOpacity(p.shelf)}}>共通の本棚</motion.span></motion.div></MotionNode></div>
<div className="place reader-place"><MotionNode layoutId={ENTITIES.reader}><motion.div className="person reader"><Person role="次の読み手" opacity={p.reader}/></motion.div></MotionNode></div>
<div className="place book-place" style={{left:x,top:y}} data-allow-overlap><MotionNode layoutId={ENTITIES.book} className="book" style={{width:w,height:h}}><Book/></MotionNode></div>
<div className="place arrow-place"><Arrow layoutId={ENTITIES.arrow}><motion.div animate={{opacity:p.arrow?1:0}} className={'connector '+p.arrow}>{p.arrow==='cycle'?<svg viewBox="0 0 526 340" aria-label="本棚から次の読み手へ。読んだら本棚へ戻す"><defs><marker id="cycle-tip" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10"/></marker></defs><path d="M10 35H515" markerEnd="url(#cycle-tip)"/><path d="M515 270V325H275V310" markerEnd="url(#cycle-tip)"/><text x="263" y="15" textAnchor="middle">本棚から、次の読み手へ</text><text x="395" y="302" textAnchor="middle">読んだら、本棚へ</text></svg>:p.arrow==='return'?'←':'→'}</motion.div></Arrow></div>
<div className="place note-place"><Label layoutId={ENTITIES.note}><motion.div animate={{opacity:p.note?1:0}} className="note">本の名前<br/><span>ひとこと</span></motion.div></Label></div>
</SceneLayer>}
'''
CSS='''
.book-talk{--ink:#ecf2fc;--muted:#9eafca;--blue:#578aff;--coral:#ffb5a5;background:#081629;color:var(--ink);min-height:100vh;}
.book-talk [data-presentation-title]{font-family:"Shippori Mincho",serif;font-weight:700;font-size:clamp(24px,3.5vw,48px);line-height:1.3;letter-spacing:.025em;}
.book-talk .proposal{color:var(--muted);font-size:14px;letter-spacing:.12em;}.book-talk .proposal small{margin-left:16px;font-size:11px;}
.book-talk [data-presentation-home]{text-decoration:none;}.book-talk [data-presentation-marker]{font-family:Manrope,sans-serif;color:var(--blue);font-size:20px;letter-spacing:.1em;}
.book-talk [data-presentation-toc-list]{list-style:none;}.book-talk [data-presentation-toc-item]{border:0;border-left:2px solid transparent;background:transparent;color:#7284a2;font-size:17px;padding:10px 14px;}
.book-talk [data-presentation-toc-item][data-active=true]{border-left-color:var(--blue);color:var(--ink);}
.book-talk [data-presentation-caption]{font-size:16px;line-height:1.65;color:#ced8e9;max-width:760px;}
.book-talk [data-presentation-progress-dot]{width:28px;height:5px;background:#283b57;border:0;padding:0;}
.book-talk [data-presentation-progress-dot][data-active=true]{background:var(--coral);height:7px;}
.book-talk [data-presentation-button]{background:transparent;border:1px solid #435573;color:var(--ink);padding:10px 18px;font-family:Manrope,sans-serif;font-size:14px;text-decoration:none;}
.book-talk [data-presentation-button]:disabled{opacity:.25;cursor:default;}.book-talk [data-presentation-attribution]{color:var(--muted);text-decoration:none;font-family:Manrope,sans-serif;}
.world .place{position:absolute;}.world .owner-place{left:145px;top:135px;}.world .reader-place{left:670px;top:125px;}.world .shelf-place{left:355px;top:65px;}.world .arrow-place{left:264px;top:162px;}.world .note-place{left:605px;top:140px;}
.world .person{width:90px;text-align:center;color:var(--ink);}.world .person svg{display:block;width:76px;margin:auto;fill:none;stroke:currentColor;stroke-width:2;}.world .person span{display:block;font-size:16px;white-space:nowrap;margin-top:12px;}
.world .reader{color:var(--coral);}.world .shelf{width:220px;text-align:center;color:#738aad;}.world .shelf svg{width:220px;height:240px;fill:none;stroke:currentColor;stroke-width:1.5;}.world .shelf span{font-size:15px;display:block;color:var(--ink);}
.world .book svg{width:100%;height:100%;overflow:visible;}.world .book-front{fill:var(--blue);stroke:#8badff;stroke-width:1.2;}.world .book-spine{stroke:#16346f;fill:none;stroke-width:2;}.world .book-lines{stroke:#dce7ff;stroke-width:1;}.world .book-mark{fill:var(--coral);}.world .book text{fill:#fff;font-family:Manrope,sans-serif;font-size:20px;letter-spacing:2px;font-weight:600;}
.world .connector{font-family:Manrope,sans-serif;color:var(--coral);font-size:40px;line-height:1;}.world .connector.find,.world .connector.take{margin-left:327px;}.world .connector.return{margin-left:327px;}.world .connector.take{margin-left:366px;font-size:30px}.world .connector.cycle{margin-left:-74px;margin-top:-137px;width:526px;height:340px;color:#ffb5a5;}.world .connector.cycle svg{width:100%;height:100%;stroke:currentColor;fill:none;stroke-width:1.5;overflow:visible;}.world .connector.cycle marker path{fill:currentColor;stroke:none}.world .connector.cycle text{font-family:"BIZ UDPGothic",sans-serif;font-size:14px;fill:currentColor;stroke:none}
.world .note{font-size:18px;color:var(--ink);line-height:1.9;padding-left:15px;border-left:1px solid var(--coral);}.world .note span{font-size:14px;color:var(--muted);}
'''
BRIDGE='''  // Local adapter: original state/controller remains the only navigation owner.
  useEffect(() => {
    const onMessage = (e: MessageEvent) => {
      if (e.origin !== window.location.origin || e.source !== window.parent || e.data?.type !== 'yebisu-slide' || !Number.isInteger(e.data.index)) return
      setStep(Math.max(0, Math.min(last, e.data.index)))
    }
    window.addEventListener('message', onMessage)
    return () => window.removeEventListener('message', onMessage)
  }, [last])
  useEffect(() => {
    if (window.parent !== window) window.parent.postMessage({ type: 'yebisu-page', index: step }, window.location.origin)
  }, [step])
'''

def main():
    p=argparse.ArgumentParser();p.add_argument('--prepare',action='store_true');p.add_argument('--app',type=Path,default=APP);a=p.parse_args()
    if a.prepare:prepare()
    for args,name in [(['npm.cmd','install'],'install'),(['npm.cmd','run','build'],'build')]:
        run=subprocess.run(args,cwd=a.app,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace')
        write(CASE/f'output/npm-{name}.log',run.stdout);print(run.stdout);run.check_returncode()
    shutil.copytree(a.app,CASE/'app',dirs_exist_ok=True,ignore=shutil.ignore_patterns('node_modules','dist','.git','.vite','*.tsbuildinfo'))
    shutil.copytree(a.app/'dist',CASE/'dist',dirs_exist_ok=True)
    shutil.copy2(Path(__file__),CASE/'source/build.py')
    print('Original kit scaffold/build complete. Web output:',CASE/'dist')
if __name__=='__main__':main()
