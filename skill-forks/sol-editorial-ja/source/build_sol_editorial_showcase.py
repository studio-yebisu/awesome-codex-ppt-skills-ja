"""Japanese editorial extension of likaku's MckEngine. Apache-2.0.

Uses the upstream DeckBuilder type/data schema and original native PPTX core.
This is an explicit layout extension, not the original consulting appearance.
"""
from pathlib import Path
import argparse, json, sys, shutil, hashlib, subprocess
import importlib.metadata

ROOT=Path(__file__).resolve().parents[1]
UP=ROOT/'upstream' if (ROOT/'upstream/mck_ppt').exists() else ROOT/'.build/actual-upstreams/likaku__Mck-ppt-design-skill'
OUT=ROOT/'examples/repositories/sol-editorial-showcase'
sys.path.insert(0,str(UP))
from mck_ppt.engine import MckEngine
import mck_ppt.deck_builder as builder
from mck_ppt.core import add_text, add_rect, add_hline
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

IVORY=RGBColor.from_string('F4F0E6')
INK=RGBColor.from_string('191918')
RED=RGBColor.from_string('F14A24')
MUTED=RGBColor.from_string('6B685F')
JP='Zen Kaku Gothic New'
SERIF='Shippori Mincho'
EN='Space Grotesk'

def write(p,s):
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
def dump(p,v):write(p,json.dumps(v,ensure_ascii=False,indent=2))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

class EditorialEngine(MckEngine):
    """Six explicit overrides; original _ns, save and cleanup are inherited."""
    def text(self,s,x,y,w,h,t,size=24,color=INK,font=JP,bold=False):
        return add_text(s,Inches(x),Inches(y),Inches(w),Inches(h),t,
          font_size=Pt(size),font_name=font,ea_font=font,font_color=color,bold=bold)
    def rect(self,s,x,y,w,h,c):return add_rect(s,Inches(x),Inches(y),Inches(w),Inches(h),c)
    def line(self,s,x,y,w,c=INK):return add_hline(s,Inches(x),Inches(y),Inches(w),c,Pt(.7))
    def page(self,label,bg=IVORY,fg=INK):
        s=self._ns();s.background.fill.solid();s.background.fill.fore_color.rgb=bg
        self.text(s,.65,.35,10,.3,label,11,fg,EN)
        self.text(s,.65,7.06,10,.24,'架空のブランド企画 / CONCEPT STUDY',9,fg)
        self.text(s,11.9,7.03,.8,.3,f'{self._page:02d} / 06',10,fg,EN)
        return s
    def cover(self,title,subtitle='',author='',date='',cover_image=None):
        s=self.page('YOHAKU  /  BRAND PROPOSAL 2026')
        self.rect(s,9.1,0,4.233,7.5,RED)
        self.text(s,.65,1.5,8.2,2.5,title,70,bold=True)
        self.line(s,.7,4.3,7.7)
        self.text(s,.7,4.68,7.5,1.3,subtitle,25,font=SERIF)
        self.text(s,.7,6.27,7.4,.4,author,12)
        self.text(s,9.55,1.25,3.3,4.4,['余','白'],104,IVORY,bold=True)
        self.text(s,9.6,6.16,3,.4,'A DAY TO THINK.',14,IVORY,EN)
    def quote(self,quote_text,attribution=''):
        s=self.page('01  /  THE NEED',INK,IVORY)
        self.rect(s,.7,1.48,.13,3.65,RED)
        self.text(s,1.15,1.45,10.8,3.6,quote_text,48,IVORY,font=SERIF)
        self.line(s,1.2,5.45,10.8,RED)
        self.text(s,1.2,5.85,10.4,.9,attribution,20,IVORY)
    def section_divider(self,section_label,title,subtitle=''):
        s=self.page('02  /  BRAND IDENTITY')
        self.text(s,.7,1.15,7.2,.55,section_label,16,RED,EN)
        self.text(s,.65,1.9,7.6,2.3,title,66,bold=True)
        self.text(s,.72,4.4,7.05,1.5,subtitle,23,font=SERIF)
        self.rect(s,9.2,1.3,3.35,4.85,RED)
        self.rect(s,9.65,1.75,2.45,3.95,IVORY)
        self.text(s,9.88,2.3,2.1,2.4,['余','白'],58,bold=True)
        self.text(s,9.98,5.04,2,.4,'YOHAKU',13,font=EN)
        self.text(s,.75,6.3,11.5,.4,'日帰りワークラウンジ  /  静けさ・余裕・帰れる距離',15)
    def timeline(self,title,milestones,source='',bottom_bar=None):
        s=self.page('03  /  A DAY AT YOHAKU')
        self.text(s,.65,1.15,11.8,1.5,title,45,bold=True)
        self.line(s,.75,3.13,11.7,RED)
        for i,(time,head,body) in enumerate(milestones):
            x=.75+i*3
            self.rect(s,x,2.96,.07,.36,RED)
            self.text(s,x,3.55,2.6,.65,time,29,RED,EN)
            self.text(s,x,4.46,2.7,.7,head,24,bold=True)
            self.text(s,x,5.33,2.65,1.1,body,17)
        self.text(s,.75,6.6,11.6,.3,source,10,MUTED)
    def big_number(self,title,number,unit='',description='',detail_items=None,source='',bottom_bar=None):
        s=self.page('04  /  EXPERIENCE DESIGN')
        self.text(s,.7,1.15,11.7,1,title,37,bold=True)
        self.text(s,.55,2.4,6.7,2.8,number,108,RED,bold=True)
        self.text(s,.75,5.6,5.75,.9,description,22,font=SERIF)
        for i,item in enumerate(detail_items or []):
            y=2.53+i*1.35
            self.text(s,7.2,y,.5,.45,f'{i+1:02d}',13,RED,EN)
            self.text(s,7.9,y,4.5,.8,item,23)
            self.line(s,7.2,y+1.04,5.2)
    def closing(self,title,message='',source_text=''):
        s=self.page('05  /  BRAND PROMISE',RED,IVORY)
        self.text(s,.75,1.15,10.7,4.3,title,58,IVORY,bold=True)
        self.line(s,.8,5.85,11.6,IVORY)
        self.text(s,.8,6.15,8.7,.58,message,20,IVORY,font=SERIF)
        self.text(s,10.25,6.1,2.3,.65,'YOHAKU',22,IVORY,EN)

STORY=[
 {'type':'cover','data':{'title':'余白を買う。','subtitle':'日帰りワークラウンジの\nブランド提案','author':'企画名：YOHAKU / 架空の制作サンプル','date':'2026'}},
 {'type':'quote','data':{'quote_text':'家でも、職場でもない。\n考えるために、\n少しだけ離れる。','attribution':'移動は短く。頭の中には、広い余白を。'}},
 {'type':'section_divider','data':{'section_label':'NAME & VOICE','title':'余白\nYOHAKU','subtitle':'予定を詰める場所から、\n考えをほどく場所へ。'}},
 {'type':'timeline','data':{'title':'一日を、ひとつのリズムに。','milestones':[['09:30','切り替える','一杯のお茶から。\n今日の問いを置く。'],['10:00','深く潜る','会話を控えた席で、\nひとつに向き合う。'],['13:00','ほどく','軽い食事と散歩。\n画面から目を離す。'],['16:30','持ち帰る','考えを一枚にする。\n夕方には、いつもの街へ。']],'source':'時刻・体験は企画上のモデル。営業条件や実績を示すものではありません。'}},
 {'type':'big_number','data':{'title':'売るのは席より、考えられる一日。','number':'一日','description':'場所と時間を、\nひとつの体験として届ける。','detail_items':['静けさを選べる席','途中でほどける余裕','帰る前に整理する時間']}},
 {'type':'closing','data':{'title':'今日は、\n遠くまで\n考えよう。','message':'体は、日帰り。考えは、少し先へ。','source_text':'架空のブランド提案'}}
]
PROMPT='''架空の日帰りワークラウンジ「YOHAKU」のブランド提案を日本語6ページで作ってください。タイトルは「余白を買う」。対象は企画担当者と空間運営者。席数や売上の実績を作らず、企画の約束・一日の体験・言葉の使い方を伝えてください。アイボリー、墨黒、鮮やかな赤橙。大きな和文タイポと編集誌の余白、平面図形を使い、角丸カードや管理画面のような構成を避けてください。原典likaku/Mck-ppt-design-skillのDeckBuilderとtype/data schemaを使い、MckEngineの派生版としてレイアウト変更を明記。編集可能なPPTX、入力JSON、生成コードとプレビューを残してください。'''

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--render',action='store_true');args=ap.parse_args()
    dump(OUT/'input/storyline.json',STORY)
    write(OUT/'PROMPT.txt',PROMPT)
    write(OUT/'input/BRIEF.md','# 余白を買う\n\n読者：企画担当者・空間運営者。目的：日帰りラウンジの名前、約束、体験の方向を提案する。6分、6ページ。組織・サービスは架空。売上、利用者数、満足度などの実績は掲載しない。\n')
    builder.MckEngine=EditorialEngine
    builder.DeckBuilder.build(json.loads((OUT/'input/storyline.json').read_text(encoding='utf-8')),str(OUT/'deck.pptx'))
    (OUT/'source').mkdir(parents=True,exist_ok=True)
    shutil.copy2(__file__,OUT/'source/build_sol_editorial_showcase.py')
    for f in ['LICENSE','NOTICE','SKILL.md']:
        shutil.copy2(UP/f,OUT/('UPSTREAM-SKILL.md' if f=='SKILL.md' else f))
    acquisition=json.loads((UP/'ACQUISITION.json').read_text(encoding='utf-8'))
    dump(OUT/'environment.json',{'python_executable':sys.executable,'python_version':sys.version,'python-pptx':importlib.metadata.version('python-pptx'),'lxml':importlib.metadata.version('lxml'),'actual_generate_command':[sys.executable,'tools/build_sol_editorial_showcase.py']+(['--render'] if args.render else []),'font_embedding':False})
    reads=['SKILL.md','references/framework/engine-api.md','references/team/brand-guide.md','references/framework/guard-rails.md','references/layout-matrix.yaml','mck_ppt/engine.py','mck_ppt/core.py','mck_ppt/deck_builder.py']
    dump(OUT/'PROVENANCE.json',{'repository':acquisition['repository'],'upstream_commit':acquisition['commit'],'method':'Original DeckBuilder type/data schema -> EditorialEngine(MckEngine) -> original core native shapes and text -> inherited save/full_cleanup','read_files':reads,'changes':'Six layout methods explicitly overridden; Japanese editorial palette/type scale replaces consulting brand rules under the requested art direction. Upstream files unmodified.','command':'python tools/build_sol_editorial_showcase.py --render','license':'Apache-2.0; upstream LICENSE and NOTICE retained','pptx_sha256':sha(OUT/'deck.pptx'),'fonts':[JP,SERIF,EN],'verification_scope':'Light check only. Original S3/S4 gates, independent review and exhaustive all-page QA were not run.'})
    if args.render:
        subprocess.run(['pwsh','-NoProfile','-File',str(ROOT/'tools/render_powerpoint.ps1'),'-PresentationPath',str(OUT/'deck.pptx'),'-OutputDirectory',str(OUT/'render')],check=True)
    pages=[f'render/slide-{i:02d}.png' for i in range(1,7)]
    write(OUT/'index.html','<!doctype html><html lang="ja"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>余白を買う</title><style>body{margin:0;background:#191918;color:#f4f0e6;font-family:sans-serif}header{padding:24px 5vw}h1{font-size:26px}a{color:#ff7856}main{display:grid;gap:30px;padding:0 5vw 50px}img{width:100%;display:block}figcaption{padding:12px 0;font-size:13px}figure{margin:0}</style><header><h1>余白を買う — 日帰りワークラウンジのブランド提案</h1><p>架空の企画 / 原典MckEngineの編集誌レイアウト派生 / 軽い動作確認済み</p><a href="deck.pptx">編集可能なPowerPoint</a> · <a href="SKILL.md">日本語SKILL</a> · <a href="PROMPT.txt">AIへの依頼文</a> · <a href="README.md">制作方法</a></header><main>'+''.join(f'<figure><img src="{p}" alt="第{i}ページ: {r["data"].get("title",r["data"].get("quote_text",""))}"><figcaption>{i:02d} / 06</figcaption></figure>' for i,(p,r) in enumerate(zip(pages,STORY),1))+'</main></html>')
    skill='''---
name: sol-editorial-ja
description: 原典MckEngineを編集誌風へ明示拡張し、大胆な日本語タイポでブランド提案を作る。
---

# 日本語の編集誌風ブランド提案

1. 読者、企画の約束、一日の体験を短く決める。実績のない数値は作らない。
2. upstreamのSKILL.mdとengine-api、core、DeckBuilderを読む。入力は `[{"type":"cover","data":{"title":"..."}}]` という原典schemaを使う。
3. `source/build_sol_editorial_showcase.py` のSTORYを編集する。cover / quote / section_divider / timeline / big_number / closing の順で6ページ。コード内のMckEngine派生版がネイティブ文字・図形を生成する。
4. Zen Kaku Gothic New、Shippori Mincho、Space Groteskを用意する。書体変更時はJP/SERIF/ENを更新する。
5. カタログrepoのrootで `python tools/build_sol_editorial_showcase.py --render` を実行。python-pptx/lxmlと固定原典が必要。PNG描画にはWindowsのMicrosoft PowerPointを使う。
6. PPTXと表紙PNGが開くことを確認。今回のlight checkを全ページの品質承認や原典gate通過と扱わない。

原典：likaku/Mck-ppt-design-skill、commit e190e083b715b63172e1c4fea01bc5f9bb21a021。Apache-2.0のLICENSE/NOTICEを保持。これはStudio Yebisuの日本語編集誌レイアウト派生例で、原作者の公式日本語版ではない。
'''
    write(OUT/'SKILL.md',skill)
    write(ROOT/'skill-forks/sol-editorial-ja/SKILL.md',skill)
    for f in ['LICENSE','NOTICE']:shutil.copy2(UP/f,ROOT/'skill-forks/sol-editorial-ja'/f)
    fork=ROOT/'skill-forks/sol-editorial-ja'
    for d in ['mck_ppt','references']:
        shutil.copytree(UP/d,fork/'upstream'/d,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    for f in ['SKILL.md','LICENSE','NOTICE']:shutil.copy2(UP/f,fork/'upstream'/f)
    (fork/'source').mkdir(exist_ok=True)
    shutil.copy2(__file__,fork/'source/build_sol_editorial_showcase.py')
    write(OUT/'README.md','# 余白を買う\n\n日帰りワークラウンジ「YOHAKU」の架空ブランド提案。6ページ。企画上の体験を示し、売上や利用実績は掲載していません。\n\n## 制作方式\n\nlikaku/Mck-ppt-design-skill の固定原典DeckBuilderとMckEngineを使用。type/dataの入力JSONをDeckBuilderへ渡し、6つのlayout methodをEditorialEngineで上書きしています。原典coreのadd_text/add_rect/add_hlineとMckEngineの_ns/save、full_cleanupを直接使用。文字と図形は編集可能なネイティブPowerPointです。コンサルティング標準版式の単なる色替えや翻訳ではなく、明示的なレイアウト派生です。上流本体は改変していません。\n\n## 再制作\n\nPythonにpython-pptx/lxml、repo内 .build/actual-upstreams/likaku__Mck-ppt-design-skill にPROVENANCE記載の原典を用意します。Zen Kaku Gothic New、Shippori Mincho、Space Groteskをインストールし、repoのrootで実行。\n\n```powershell\npython tools/build_sol_editorial_showcase.py --render\n```\n\n原典入力はinput/storyline.json、AI依頼文はPROMPT.txt、生成コードはsource/に保持。描画にはMicrosoft PowerPointが必要です。PPTXに書体自体は埋め込んでいません。\n\n## 確認範囲\n\nPowerPointによる初回PNG/PDF描画、ページ数と主スライドが開くことのみを確認。全ページ詳細検査、原典S3/S4 gate、native ZIP監査、独立レビュー、配布ZIPからの再実行は未実施。QA.jsonに実際の状態を記録します。\n\n## 条件\n\n原典 Apache-2.0、Kaku Li (likaku) のLICENSEとNOTICEを保持。この例はStudio Yebisuの派生制作。原作者の公式日本語版でもMcKinseyの公式資料でもありません。書体のOFL条件はdownloads/fontsの親管理資料を参照してください。\n')
    p='examples/repositories/sol-editorial-showcase/'
    titles=[r['data'].get('title',r['data'].get('quote_text','')) for r in STORY]
    record={'id':'sol-editorial-showcase','title':'余白を買う — 日帰りワークラウンジのブランド提案','use_case':'ブランド提案','repository':acquisition['repository'],'skill_repository':acquisition['repository'],'upstream_commit':acquisition['commit'],'fork_id':'sol-editorial-ja','page_count':6,'format':'pptx','preview_kind':'powerpoint-render','style':'日本語編集誌 / アイボリー・墨黒・赤橙 / native typography','cover':p+pages[0],'interior':p+pages[2],'preview':p+'index.html','artifact_download':p+'deck.pptx','source_download':p+'source/build_sol_editorial_showcase.py','input':p+'input/BRIEF.md','input_data':p+'input/storyline.json','prompt':p+'PROMPT.txt','prompt_text':PROMPT,'provenance':p+'PROVENANCE.json','qa':p+'QA.json','guide':p+'README.md','titles':titles,'notes':['架空の企画。実績や販売条件を示しません。']*6,'method':'原典DeckBuilder / MckEngineを使用し、原典core primitivesで6版式を明示拡張したnative PPTX。','sample_notice':'サービスと体験は架空の企画サンプルです。','pages':[p+x for x in pages],'pdf_download':p+'render/deck.pdf'}
    dump(ROOT/'data/sol-editorial-repository-examples.json',[record])
    dump(ROOT/'data/sol-editorial-repository-guides.json',[{'repository':acquisition['repository'],'example_ids':['sol-editorial-showcase'],'summary_ja':'原典MckEngineのnative PPTXを編集誌風に拡張した日本語ブランド提案。','upstream_commit':acquisition['commit'],'license':'Apache-2.0','license_paths':[p+'LICENSE',p+'NOTICE'],'skill_paths':[p+'SKILL.md'],'production_status':'light_check_complete' if args.render else 'generated','requirements':['Python / python-pptx / lxml','固定原典Mck-ppt-design-skill','描画: Windows Microsoft PowerPoint','Zen Kaku Gothic New / Shippori Mincho / Space Grotesk'],'commands':['python tools/build_sol_editorial_showcase.py --render'],'steps':['input/storyline.jsonとPROMPT.txtを読む','6版式のMckEngine派生コードを実行','主スライドが開くことを確認'],'guide':p+'README.md','limitations':['原典の標準ブランドルールをユーザー指定の編集誌風へ置換した明示派生','S3/S4 gateと全ページ詳細QAは未実施']}])
    dump(OUT/'QA.json',{'status':'light_check_complete' if args.render else 'generated','slide_count':6,'native_pptx_created':(OUT/'deck.pptx').exists(),'powerpoint_first_render':args.render,'preview_count':sum((OUT/x).exists() for x in pages),'main_slide_visual_check':'pending','exhaustive_all_page_review':False,'upstream_s3_s4_gates_run':False,'independent_review':False,'zip_replay':False})
    print(OUT/'deck.pptx')

if __name__=='__main__':main()
