"""Build a Japanese deck from slide-deck-generator's actual React/Vite example."""
from pathlib import Path
import argparse, difflib, hashlib, json, shutil, subprocess, sys
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
REPO = 'code-on-sunday/slide-deck-generator'
COMMIT = 'a6369f31b0cc4dd5830796455326777a8fe4c7c6'
DEFAULT = ROOT / 'examples/repositories/react-slide-deck'
UPSTREAM = ROOT / '.build/actual-upstreams/code-on-sunday__slide-deck-generator'
TEMPLATE = 'examples/en-context-engineering'
FONT_PIN = '66928797f271fed5ee428544e7229685e2d90127'
FONT_SHA = 'c2f3b4d463500a2ddcd3849cded1fceeb9fd6d1c32e6cbecd568453ba50fc68f'
PROMPT = '原典slide-deckのReact/Vite工程とen-context-engineeringのApp・SlideLayout・useSlideScale・animation variantsを使い、日本語でFAQ整備の4週間プランを5枚作る。架空の社内チームの計画で、10問は目標。Bold Signalの配色を保ち、Noto Sans JPで日本語化。問題→問い→概念→例→持ち帰りの順に、段階的な図解と週別タブを入れる。外部AI APIや画像生成は不要。'
DATA = {
    'title': 'FAQを育てる4週間', 'notice': '架空の社内チームの企画案。4週間・10問は目標で、実績ではありません。',
    'titles': ['問い合わせを、FAQに育てる。', '同じ質問が、何度も戻ってくる。', '答えと、更新先をセットにする。', '4週間で、10問だけ整える。', 'まず1問、書いてみる。'],
    'notes': [
        'これは架空の社内チームのFAQ整備案です。4週間で10問を整理する目標を置きます。問い合わせ件数の削減や所要時間の改善を実測した資料ではありません。',
        '申請場所、締切、承認者という三つの例から、同じ質問が繰り返される状況を考えます。話し合いでは、皆さんのチームで最近繰り返された質問を一つ挙げてください。実際の社内ルールを説明するページではありません。',
        '質問を集め、答えに根拠となる資料への入口を付け、更新担当と日付を残します。図の線が順に現れ、三つの作業のつながりを示します。',
        '第1週に質問収集、第2週に回答と出典、第3週に初めて読む人の確認、第4週に更新担当と公開場所を決める案です。週のボタンで各作業を切り替えられます。10問は試行規模を絞る目標です。',
        '最初の作業は質問を一つ選び、短い答え、根拠への入口、更新担当を書くことです。ここでは入口を必ず実在の社内資料で確認し、分からない回答は決めつけず保留します。',
    ],
    'questions': ['申請はどこ？', '締切はいつ？', '誰が承認する？'],
    'steps': ['質問を集める', '答えに出典を付ける', '更新先を決める'],
    'weeks': [
        {'label': 'W1', 'title': '質問を集める', 'detail': '直近の問い合わせから、まず10問を選ぶ。'},
        {'label': 'W2', 'title': '回答と出典を書く', 'detail': '短い答えと、根拠になる資料の入口を並べる。'},
        {'label': 'W3', 'title': '初めて読む人に試す', 'detail': '見つからない言葉、迷う説明を一緒に直す。'},
        {'label': 'W4', 'title': '更新を引き継ぐ', 'detail': '公開場所、更新担当、次の確認日を決める。'},
    ],
    'takeaway': ['質問を1つ選ぶ', '短い答えを書く', '出典と担当を添える'],
}

SLIDES = r'''import { useState } from 'react';
import { motion, useReducedMotion } from 'framer-motion';
import { MessageCircle, BookOpen, RefreshCw, ArrowRight } from 'lucide-react';
import SlideLayout from '../components/SlideLayout';
import { fadeUp, staggerContainer } from '../lib/animations';
import data from '../content.json';

const accent = '#FF5722';
function Heading({index}: {index:number}) { return <motion.h1 variants={fadeUp}>{data.titles[index]}</motion.h1>; }
function Intro() { return <SlideLayout><div className="content intro"><motion.p variants={fadeUp} initial="hidden" animate="visible" className="eyebrow">SMALL TEAM / KNOWLEDGE</motion.p><motion.h1 variants={fadeUp} initial="hidden" animate="visible">問い合わせを、<br/>FAQに育てる。</motion.h1><motion.p variants={fadeUp} initial="hidden" animate="visible" custom={1} className="lead">架空チームの4週間プラン</motion.p><div className="number-mark" aria-label="4週間の企画">4<span>WEEKS / 企画案</span></div><div className="accent-rule"/></div></SlideLayout>; }
function Problem() { return <SlideLayout><motion.div className="content" variants={staggerContainer} initial="hidden" animate="visible"><p className="eyebrow">01 / PROBLEM → DISCUSSION</p><Heading index={1}/><div className="questions">{data.questions.map((q,i)=><motion.div variants={fadeUp} custom={i} key={q}><MessageCircle size={72} color={i===1?accent:'#777'}/><p>{q}</p><span>{['聞く','答える','また聞く'][i]}</span></motion.div>)}</div><motion.p variants={fadeUp} custom={3} className="prompt">あなたのチームで、最近繰り返された質問は？</motion.p></motion.div></SlideLayout>; }
function Concept() { const reduce=useReducedMotion(); return <SlideLayout><motion.div className="content" variants={staggerContainer} initial="hidden" animate="visible"><p className="eyebrow">02 / CONCEPT</p><Heading index={2}/><div className="flow">{data.steps.map((s,i)=>{const Icon=[MessageCircle,BookOpen,RefreshCw][i];return <motion.div key={s} variants={fadeUp} custom={i}><Icon size={82} color={i===1?accent:'#eee'}/><p>{s}</p><span>{['問い合わせを入口に','根拠に戻れるように','担当と日付を残す'][i]}</span></motion.div>})}<svg className="connectors" viewBox="0 0 1080 240" aria-hidden="true"><motion.path d="M120 43 H348 M488 43 H722" stroke={accent} strokeWidth="3" fill="none" initial={{pathLength:reduce?1:0}} animate={{pathLength:1}} transition={{duration:reduce?0:.7,delay:reduce?0:.2}}/><path d="M338 35 L350 43 L338 51 M712 35 L724 43 L712 51" fill="none" stroke={accent} strokeWidth="3"/></svg></div><p className="minor">答えだけで終えず、次に直せる形へ。</p></motion.div></SlideLayout>; }
function Plan() { const reduce=useReducedMotion(); const [selected,setSelected]=useState(0);return <SlideLayout><motion.div className="content" variants={staggerContainer} initial="hidden" animate="visible"><p className="eyebrow">03 / EXAMPLE — TARGET</p><Heading index={3}/><div className="plan"><div className="week-tabs" data-interactive role="tablist" aria-label="週別の作業">{data.weeks.map((w,i)=><button key={w.label} id={'week-'+i} role="tab" aria-selected={selected===i} aria-controls="week-panel" onClick={()=>setSelected(i)} style={{padding:'16px 32px',background:selected===i?accent:'transparent',color:selected===i?'#1a1a1a':'#ddd'}}>{w.label}</button>)}</div><motion.div id="week-panel" data-interactive role="tabpanel" aria-labelledby={'week-'+selected} key={selected} initial={reduce?false:{opacity:0,y:8}} animate={{opacity:1,y:0}} transition={{duration:reduce?0:.25}} className="week-panel"><h2>{data.weeks[selected].title}</h2><p>{data.weeks[selected].detail}</p></motion.div><div className="goal-number">10<span>QUESTIONS / 目標</span></div></div></motion.div></SlideLayout>; }
function Takeaway() { return <SlideLayout><motion.div className="content" variants={staggerContainer} initial="hidden" animate="visible"><p className="eyebrow">04 / TAKEAWAY</p><Heading index={4}/><ol className="takeaways">{data.takeaway.map((t,i)=><motion.li variants={fadeUp} key={t} custom={i}><span>0{i+1}</span>{t}<ArrowRight size={38} color={accent}/></motion.li>)}</ol><p className="minor">分からない答えは、保留にして確認する。</p></motion.div></SlideLayout>; }
export const deckSlides = [Intro,Problem,Concept,Plan,Takeaway];
'''

CSS = '''@font-face{font-family:'FAQ Japanese';src:url('/fonts/faq-japanese.woff2') format('woff2');font-weight:100 900;font-display:block}
:root{--font-display:'FAQ Japanese',sans-serif;--font-body:'FAQ Japanese',sans-serif}
.content{width:100%;height:100%;padding:72px 90px;position:relative}
.content h1{font-family:var(--font-display);font-size:clamp(48px,4.5vw,64px);font-weight:850;line-height:1.35;letter-spacing:-.025em;margin-top:20px}
.eyebrow{font-size:clamp(16px,1.4vw,20px);letter-spacing:.12em;color:#aaa}
.intro h1{font-size:clamp(78px,7.2vw,94px);line-height:1.35;margin-top:55px;position:relative;z-index:1}
.intro .lead{font-size:clamp(28px,2.5vw,36px);color:#bdbdbd;margin-top:32px}
.number-mark{position:absolute;right:80px;top:166px;font-size:clamp(160px,17vw,228px);font-weight:900;color:#FF5722;line-height:1;letter-spacing:-.08em}
.number-mark span,.goal-number span{display:block;font-size:clamp(16px,1.6vw,22px);letter-spacing:.15em;margin-top:22px;text-align:center}
.accent-rule{position:absolute;bottom:94px;left:90px;width:480px;height:3px;background:#FF5722}
.questions,.flow{display:grid;grid-template-columns:repeat(3,1fr);gap:46px;margin-top:80px;position:relative}
.questions p,.flow p{font-size:clamp(28px,2.5vw,36px);font-weight:700;margin-top:28px}
.questions span,.flow span{display:block;font-size:clamp(20px,1.8vw,26px);color:#aaa;margin-top:18px}
.prompt{font-size:clamp(26px,2.3vw,32px);margin-top:65px;color:#FF875A}
.flow{gap:50px;margin-top:75px}
.connectors{position:absolute;top:0;left:0;width:100%;height:240px;pointer-events:none}
.minor{font-size:clamp(20px,1.9vw,28px);color:#aaa;margin-top:48px}
.plan{position:relative;margin-top:64px;padding-right:360px}
.week-tabs{display:flex;gap:14px;border-bottom:1px solid #555;padding-bottom:16px}
.week-tabs button{font:inherit;font-size:clamp(24px,2.1vw,30px);border:1px solid #777;cursor:pointer}
.week-tabs button:focus-visible,.native-nav button:focus-visible{outline:3px solid white;outline-offset:5px}
.week-panel{min-height:144px;margin-top:35px}
.week-panel h2{font-size:clamp(32px,3vw,44px)}
.week-panel p{font-size:clamp(24px,2.1vw,30px);color:#bbb;line-height:1.6;margin-top:18px}
.goal-number{position:absolute;right:0;top:0;font-size:clamp(100px,11vw,154px);font-weight:850;color:#FF5722;line-height:1}
.takeaways{list-style:none;margin-top:50px;width:850px}
.takeaways li{display:flex;align-items:center;gap:36px;border-bottom:1px solid #555;padding:18px 0;font-size:clamp(32px,3vw,44px)}
.takeaways li span{font-size:clamp(30px,2.8vw,40px);color:#FF5722}
.takeaways li svg{margin-left:auto}
.native-nav{position:fixed;bottom:22px;left:26px;display:flex;align-items:center;gap:8px;z-index:60}
.native-nav button{font:inherit;font-size:clamp(13px,1vw,16px);border:1px solid #666;color:#eee;cursor:pointer;border-radius:0;background:#1a1a1a}
.native-nav button:disabled{opacity:.3;cursor:default}
.native-nav p{font-size:clamp(12px,1vw,16px);color:#aaa;margin-left:10px}
@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important}}
'''

CSS += '\n/* Round4: Bold Signal focal colour card on the title. */\n.number-mark{right:90px;top:178px;width:255px;height:300px;background:#FF5722;color:#171717;padding:26px 10px;text-align:center;font-size:180px;letter-spacing:-.05em}.number-mark span{font-size:18px;letter-spacing:.03em;margin-top:10px}\n'

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def write(p,s): p=Path(p); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(s,encoding='utf-8',newline='\n')
def save(p,v): write(p,json.dumps(v,ensure_ascii=False,indent=2)+'\n')

def run(argv, cwd, out, name):
    p=subprocess.run([str(x)for x in argv],cwd=cwd,capture_output=True,text=True,encoding='utf-8',errors='replace')
    path=out/'source/logs'/name;write(path,json.dumps([str(x)for x in argv])+'\n'+p.stdout+'\n'+p.stderr)
    receipt={'argv':[str(x)for x in argv],'cwd':str(cwd),'exit_code':p.returncode,'log':path.relative_to(out).as_posix(),'log_sha256':sha(path)}
    if p.returncode: raise RuntimeError(p.stdout+'\n'+p.stderr)
    return receipt

def build(out,up,inp,node):
    out.mkdir(parents=True,exist_ok=True);data=load(inp)if inp else DATA
    assert len(data['titles'])==len(data['notes'])==5 and len(data['weeks'])==4
    save(out/'input/data.json',data);write(out/'input/BRIEF.md','# '+data['title']+'\n\n'+data['notice']+'\n\n目的: 社内の情報整理を小さく始める日本語研修例。雰囲気: Focused / Bold Signal。\n\n'+'\n'.join(f'{i+1}. {t}'for i,t in enumerate(data['titles']))+'\n')
    write(out/'PROMPT.txt',PROMPT+'\n');shutil.copy2(up/'LICENSE',out/'LICENSE.upstream')
    frozen=out/'source/upstream'
    for name in ['LICENSE','README.md','skills/slide-deck/SKILL.md','skills/slide-deck/slide-guidelines.md']:
        dest=frozen/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(up/name,dest)
    shutil.copytree(up/TEMPLATE,frozen/TEMPLATE,dirs_exist_ok=True,ignore=shutil.ignore_patterns('node_modules','dist','.git'))
    app=out/'source/app';shutil.copytree(frozen/TEMPLATE,app,dirs_exist_ok=True,ignore=shutil.ignore_patterns('node_modules','dist'))
    slide_dir=app/'src/slides'
    # Only the generated app's English slide modules are replaced, never the frozen source.
    for p in slide_dir.glob('*'):
        if p.is_file():p.unlink()
    write(slide_dir/'deck.tsx',SLIDES);write(slide_dir/'index.ts',"export { deckSlides as slides } from './deck';\n")
    save(app/'src/content.json',data)
    original=(app/'src/App.tsx').read_text(encoding='utf-8')
    bridge='''
  useEffect(() => {
    const receive = (e: MessageEvent) => {if(e.origin!==location.origin||e.source!==parent||e.data?.type!=='yebisu-slide'||!Number.isInteger(e.data.index))return;setCurrent(Math.max(0,Math.min(total-1,e.data.index)));};
    window.addEventListener('message',receive);return()=>window.removeEventListener('message',receive);
  },[total]);
  useEffect(()=>{if(parent!==window)parent.postMessage({type:'yebisu-page',index:current,total},location.origin)},[current,total]);
'''
    text=original.replace('  const CurrentSlide = slides[current];',bridge+'\n  const CurrentSlide = slides[current];')
    text=text.replace("      if (e.key === 'ArrowRight'", "      if(e.key==='Escape'&&parent!==window){parent.postMessage({type:'yebisu-close'},location.origin);return;}\n      if((e.target as Element).closest('input,textarea,select,[data-interactive]:not(.native-nav)'))return;\n      if((e.key===' '||e.key==='Enter')&&(e.target as Element).closest('button,a'))return;\n      if (e.key === 'ArrowRight'")
    text=text.replace("      {/* Progress bar */}",'''      <nav className="native-nav" data-interactive aria-label="資料のページ移動">
        <button style={{padding:'10px 24px'}} onClick={goPrev} disabled={current===0}>前へ</button>
        <button style={{padding:'10px 24px'}} onClick={goNext} disabled={current===total-1}>次へ</button>
        <p>架空の企画案</p>
      </nav>
      {/* Progress bar */}''')
    text=text.replace('<div style={{ width:',"<div data-deck-page={current} onClick={(e)=>{if((e.target as Element).closest('button,input,textarea,select,a,[data-interactive]'))return;(e.clientX>innerWidth/2?goNext:goPrev)();}} style={{ width:")
    text=text.replace('fontSize: 13,',"fontSize: 'clamp(13px,1.2vw,18px)',").replace("color: 'rgba(255,255,255,0.3)'","color: '#a0a0a0'").replace("fontFamily: \"'Space Grotesk', sans-serif\"","fontFamily: \"'FAQ Japanese', sans-serif\"")
    write(app/'src/App.tsx',text)
    layout=app/'src/components/SlideLayout.tsx';text=layout.read_text(encoding='utf-8').replace('transform: `scale(${scale})`,','scale,')
    write(layout,text)
    animation=app/'src/lib/animations.ts';text=animation.read_text(encoding='utf-8')+"\nif(window.matchMedia('(prefers-reduced-motion: reduce)').matches){for(const variants of [slideVariants,fadeUp,fadeIn,scaleIn,staggerContainer])for(const key of Object.keys(variants)){const v=variants[key];variants[key]=typeof v==='function'?()=>({opacity:1,y:0,scale:1,transition:{duration:0}}):{opacity:1,y:0,scale:1,transition:{duration:0}};}}\n"
    write(animation,text)
    css=(app/'src/index.css').read_text(encoding='utf-8');css='\n'.join(l for l in css.splitlines()if 'fonts.googleapis'not in l)
    write(app/'src/index.css',css+'\n'+CSS)
    # tsconfig is JSONC: preserve its comments rather than parsing it as JSON.
    config=app/'tsconfig.app.json'
    write(config,config.read_text().replace('"compilerOptions": {','"compilerOptions": {\n    "resolveJsonModule": true,',1))
    config=app/'vite.config.ts';write(config,config.read_text().replace('plugins: [','base: \'./\',\n  plugins: ['))
    write(app/'index.html','<!doctype html><html lang="ja"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+data['title']+'</title></head><body><div id="root"></div><script type="module" src="/src/main.tsx"></script></body></html>')
    changes=[]
    for name in ['src/App.tsx','src/components/SlideLayout.tsx','src/lib/animations.ts','src/index.css','vite.config.ts','tsconfig.app.json','index.html']:
        changes.extend(difflib.unified_diff((frozen/TEMPLATE/name).read_text().splitlines(True),(app/name).read_text().splitlines(True),fromfile='upstream/'+name,tofile='japanese/'+name))
    write(out/'source/japanese.patch',''.join(changes))
    # Public font source, not a copy of an installed Windows font.
    font=ROOT/'.build/fonts/NotoSansJP[wght].ttf';font.parent.mkdir(parents=True,exist_ok=True)
    if not font.exists():font.write_bytes(urlopen(f'https://raw.githubusercontent.com/google/fonts/{FONT_PIN}/ofl/notosansjp/NotoSansJP%5Bwght%5D.ttf').read())
    assert sha(font)==FONT_SHA
    from fontTools import subset
    from fontTools.ttLib import TTFont
    f=TTFont(font);opts=subset.Options();opts.flavor='woff2';opts.layout_features=['*'];sub=subset.Subsetter(options=opts)
    sub.populate(text=json.dumps(data,ensure_ascii=False)+SLIDES+CSS+'0123456789前へ次へ架空の企画案SMALL TEAM KNOWLEDGE FAQ WEEKS');sub.subset(f);f.flavor='woff2'
    dest=app/'public/fonts/faq-japanese.woff2';dest.parent.mkdir(parents=True,exist_ok=True);f.save(dest)
    ofl=app/'public/fonts/OFL.txt';ofl.write_bytes(urlopen(f'https://raw.githubusercontent.com/google/fonts/{FONT_PIN}/ofl/notosansjp/OFL.txt').read())
    node=Path(shutil.which(node or 'node')or node or 'node');npm=node.parent/'node_modules/npm/bin/npm-cli.js'
    if not npm.exists():raise RuntimeError('Pass --node pointing to Node.js with its npm installation.')
    failed=out/'source/logs/npm-ci.log';original_failure=out/'source/logs/original-npm-ci.log'
    if failed.exists()and 'ERESOLVE' in failed.read_text()and not original_failure.exists():shutil.copy2(failed,original_failure)
    package=load(app/'package.json');original_lock=load(frozen/TEMPLATE/'package-lock.json')
    for group in ['dependencies','devDependencies']:
        for name in package[group]:package[group][name]=original_lock['packages']['node_modules/'+name]['version']
    # Original 4.2.1 rejects the original Vite 8.0.0 peer. 4.2.2 declares Vite 8 support.
    package['dependencies'].update({'@tailwindcss/vite':'4.2.2','tailwindcss':'4.2.2'})
    save(app/'package.json',package)
    commands=[run([node,'--version'],app,out,'node-version.log')]
    recorded_lock=(inp.parent/'package-lock.json')if inp else(out/'input/package-lock.json')
    if recorded_lock.exists():shutil.copy2(recorded_lock,app/'package-lock.json')
    else:
        commands.append(run([node,npm,'install','--package-lock-only','--ignore-scripts','--no-fund','--no-audit'],app,out,'dependency-lock.log'))
        shutil.copy2(app/'package-lock.json',out/'input/package-lock.json')
    commands.append(run([node,npm,'ci','--ignore-scripts','--no-fund','--no-audit'],app,out,'npm-ci.log'))
    save(out/'source/dependency-resolution.json',{'original_vite':'8.0.0','original_tailwind':'4.2.1','patched_tailwind':'4.2.2','reason':'Original Tailwind Vite plugin peer range excludes Vite8. Minimal patch 4.2.2 officially accepts Vite8. No --force or --legacy-peer-deps. Other direct versions pinned to original lock.','official_peer_source':'https://github.com/tailwindlabs/tailwindcss/blob/v4.2.2/packages/@tailwindcss-vite/package.json','original_failure_log':'source/logs/original-npm-ci.log'if original_failure.exists()else None,'original_failure_sha256':sha(original_failure)if original_failure.exists()else None,'patched_lock_sha256':sha(app/'package-lock.json')})
    commands.append(run([node,npm,'run','build'],app,out,'vite-build.log'))
    package_patch=''.join(difflib.unified_diff((frozen/TEMPLATE/'package.json').read_text().splitlines(True),(app/'package.json').read_text().splitlines(True),fromfile='upstream/package.json',tofile='japanese/package.json'))
    write(out/'source/package.patch',package_patch)
    commands.append(run([node,app/'node_modules/typescript/bin/tsc','--noEmit','-p','tsconfig.app.json'],app,out,'typescript.log'))
    shutil.copytree(app/'dist',out,dirs_exist_ok=True)
    notices=out/'source/dependency-notices';notices.mkdir(parents=True,exist_ok=True)
    for pkg in ['react','react-dom','scheduler','framer-motion','motion-dom','motion-utils','lucide-react','tailwindcss']:
        for n in ['LICENSE','LICENSE.md','LICENSE.txt']:
            src=app/'node_modules'/pkg/n
            if src.exists():shutil.copy2(src,notices/(pkg+'-'+n));break
    write(out/'NOTICE.md','原典MIT: Trung。React、Framer Motion、Lucide等のライセンスはsource/dependency-notices。日本語フォントはGoogle Fontsの固定版Noto Sans JPをsubset、fonts/OFL.txtを保持。\n')
    write(out/'source/build_reactdeck_repository_example.py',Path(__file__).read_text(encoding='utf-8'))
    refs=[{'path':p.relative_to(frozen).as_posix(),'sha256':sha(p),'url':f'https://github.com/{REPO}/blob/{COMMIT}/'+p.relative_to(frozen).as_posix()}for p in sorted(frozen.rglob('*'))if p.is_file()]
    built_assets=[{'path':p.relative_to(app/'dist').as_posix(),'sha256':sha(p)}for p in sorted((app/'dist').rglob('*'))if p.is_file()]
    import fontTools
    save(out/'PROVENANCE.json',{'repository':REPO,'upstream_commit':COMMIT,'execution_type':'original_react_vite_example_and_instruction_skill','references':refs,'input_sha256':sha(out/'input/data.json'),'artifact_sha256':sha(out/'index.html'),'output':'index.html','built_assets':built_assets,'commands_executed':commands,'dependency_resolution':'source/dependency-resolution.json','python_version':sys.version.split()[0],'fonttools_version':fontTools.__version__,'changes':'Japanese content modules, local Noto font, original scale routed through Motion scale property, reduced-motion variants, native controls and same-origin catalog bridge. Original App/SlideLayout/useSlideScale/animation lane retained; raw originals and diff provided. Tailwind4.2.1 ->4.2.2 for original Vite8 compatibility; resolved lock included.','font_source_sha256':sha(font),'font_pin':FONT_PIN,'third_party_ai_api':False})
    save(out/'QA.json',{'status':'generated_awaiting_review','page_count':5,'artifact_sha256':sha(out/'index.html'),'browser_review':'pending','visual_review':{'pages_reviewed':[],'method':'pending','result':'pending'},'human_adoption':'pending'})
    write(out/'README.md','# '+data['title']+'\n\n原典en-context-engineeringのReact App、SlideLayout、useSlideScale、Framer Motion variantsを使った日本語5枚。原典のtraining-cycleとBold Signal配色を採用。4週間・10問は架空の企画目標です。\n\n## 再現\n\nPython3.13とNode.js24（npm同梱）を用意し、配布キットのreproduce/Reproduce.ps1を実行。制作ソースはsource/app/src/content.jsonとslides/deck.tsx。原稿に合わせた図の配置も編集します。スキルの質問工程は今回の依頼で承認された実例制作の目的から題材とスタイルを選び、input/BRIEF.mdに記録しました。\n\nindex.htmlはHTTPで配信してください。ファイルのダブルクリックによるES Module表示は保証しません。npm run devは開発用、npm run buildは配布用。外部AI APIや画像生成は使っていません。\n\n原典の英字フォントを公式配布の日本語フォントへ替え、フォントを同梱。スライドの遷移と内部の週別タブはReactの実状態です。日本語の原稿、ノート、原典hash、局所diff、実行ログと表示QAを保存します。\n')
    if out.resolve()==DEFAULT.resolve():
        p='examples/repositories/react-slide-deck/'
        save(ROOT/'data/reactdeck-repository-examples.json',[{'id':'react-slide-deck','title':data['title'],'repository':REPO,'skill_repository':REPO,'upstream_commit':COMMIT,'fork_id':'react-slide-deck-ja','page_count':5,'format':'html','preview_kind':'html','style':'Bold Signal / React + Motion','use_case':'社内研修・FAQ整備','cover':p+'render/slide-01.png','interior':p+'render/slide-04.png','preview':p+'index.html','artifact_download':p+'index.html','source_download':'downloads/react-slide-deck-example-ja.zip','input':p+'input/BRIEF.md','input_data':p+'input/data.json','input_sha256':sha(out/'input/data.json'),'prompt':p+'PROMPT.txt','prompt_text':PROMPT,'provenance':p+'PROVENANCE.json','qa':p+'QA.json','guide':p+'README.md','method':'原典React App / SlideLayout / useSlideScale / Framer Motion variants / Vite build','sample_notice':data['notice'],'editability':'tsx_source','titles':data['titles'],'notes':data['notes'],'pages':[p+f'render/slide-{i:02}.png'for i in range(1,6)],'navigation':'native-runtime-bridge'}])
        save(ROOT/'data/reactdeck-repository-guides.json',[{'repository':REPO,'execution_type':'original_react_vite_example_and_instruction_skill','execution_status':'generated_awaiting_review','case_ids':['react-slide-deck'],'summary_ja':'原典React/Viteのページ状態とMotion演出で、日本語5枚と週別タブを制作。','requirements':['Python3.13 / fontTools / Brotli','Node.js24とnpm','HTTPの配信環境'],'steps':['原典スキルとtraining-cycleを読む','en-context-engineeringの共通部品を保持し日本語原稿を組む','npm ci → npm run build → TypeScript確認','原典React状態で全ページ・週別タブを確認'],'commands':['python tools/build_reactdeck_repository_example.py --input examples/repositories/react-slide-deck/input/data.json'],'source_refs':refs,'limitations':['架空の計画。改善効果や完成実績ではない。','PPTXは生成しない。','HTTP表示が必要。','60fpsの定量計測や全端末の確認は未実施。'],'guide':p+'README.md'}])
    print(out)

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--output-dir',type=Path,default=DEFAULT);a.add_argument('--upstream-dir',type=Path,default=UPSTREAM);a.add_argument('--input',type=Path);a.add_argument('--node');v=a.parse_args();build(v.output_dir.resolve(),v.upstream_dir.resolve(),v.input,v.node)
