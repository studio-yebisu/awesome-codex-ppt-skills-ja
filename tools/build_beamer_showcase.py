"""Build Japanese Beamer with the upstream Warm Editorial theme, not a generic renderer.

The bundled example/build.py also rebuilds the packaged source directly.
TeX binaries and package caches are intentionally not packaged.
"""
from pathlib import Path
import argparse, hashlib, json, os, shutil, subprocess, sys, zipfile

SCRIPT = Path(__file__).resolve()
ROOT = SCRIPT.parents[1]
CASE = ROOT / 'examples/repositories/beamer-showcase' if SCRIPT.parent.name == 'tools' else SCRIPT.parent
PIN = 'e63b61b140a00596e5260ec7611e42bfde7efb5f'
TITLES = ['待ち時間のしくみ', '一つの窓口に、仕事が届く', '待ち時間を式にする', '間隔が1秒違うと、待ちは積み上がる', '待ち時間を減らす、三つの方法']
PROMPT = '''日本語で5枚の学習用Beamer資料「待ち時間のしくみ」を制作してください。
原典xukp20/build-beamer-slidesのWarm Editorial template-169.texとtheme.texを実際に使ってください。
温かい紙色、墨紺、銅色。明朝の大見出し、ゴシックの本文、数式とTikZの流れ・タイムライン・グラフ、余白のある構図。
一つの窓口、受付順、一定処理時間5秒、一定到着間隔を仮定します。実測や性能実績として扱わないでください。
図はベクトルで編集可能な.texとして作成し、PDFを主成果にします。PowerPoint形式と称しません。
原典review-loopとpage-audit-checklistに従い2回compile、全ページ180〜220dpiと重要箇所400〜600dpi cropを描画し、文字・数式・罫線・図・接続を目視してdraft-ready gateまで修正。Kimi K3とOpus5.5の独立評価は別記録に残し、未評価を合格扱いしない。
編集可能な.tex、PDF、各ページPNG、日本語ガイド、入力、依頼文、出典、原典source/license、字体OFLを含む制作ZIPと日本語skill ZIPを仕上げてください。'''

TEX = r'''% Derived from upstream styles/warm-editorial/template-169.tex at PIN.
\documentclass[aspectratio=169,10pt]{beamer}
\input{font-paths.tex}
\input{theme-portable.tex}
\usepackage{xeCJK}
\setCJKmainfont[Path=fonts/shipporimincho/,BoldFont=ShipporiMincho-Bold.ttf]{ShipporiMincho-Regular.ttf}
\setCJKsansfont[Path=fonts/zenkakugothicnew/,BoldFont=ZenKakuGothicNew-Bold.ttf]{ZenKakuGothicNew-Regular.ttf}
% Japanese type adapter and user-requested ink navy; original macro geometry remains.
\definecolor{BMEInk}{HTML}{243746}
\definecolor{BMEBrown}{HTML}{243746}
\newcommand{\Base}[3]{\fill[BMEIvory] (current page.south west) rectangle (current page.north east);\WarmFrameHeader{#1}{#2}{#3}}
\newcommand{\Foot}{\WarmFrameFooter{学習用の仮定・試算 / 一つの窓口・受付順・一定処理時間 / 実測値ではありません}}
\tikzset{jptext/.style={anchor=north west,inner sep=0pt,align=left,font=\sffamily\fontsize{9}{13}\selectfont,text=BMEInk},jpsmall/.style={font=\sffamily\fontsize{7}{10}\selectfont,text=BMEMuted}}
\begin{document}

% Cover geometry follows the original Warm Editorial starter.
\begin{frame}[plain]
\begin{tikzpicture}[remember picture,overlay]
\fill[BMEIvory] (current page.south west) rectangle (current page.north east);
\fill[BMETerracotta] ([xshift=.88cm,yshift=-1.22cm]current page.north west) rectangle ++(.14cm,-.86cm);
\node[anchor=north west,inner sep=0pt,text=BMETerracotta,font=\sffamily\fontsize{7}{9}\selectfont\bfseries] at ([xshift=1.24cm,yshift=-1.25cm]current page.north west) {SYSTEMS / 学習ノート};
\node[anchor=north west,inner sep=0pt,text=BMEBrown,font=\rmfamily\fontsize{29}{37}\selectfont\bfseries,text width=8cm] at ([xshift=1.22cm,yshift=-2.60cm]current page.north west) {待ち時間の\\しくみ};
\node[jptext,text width=8cm,text=BMEMuted] at ([xshift=1.25cm,yshift=-5.15cm]current page.north west) {仕事の速さと、届く間隔。\\二つの時間から、列の長さを考える。};
\draw[BMEStone,line width=.55pt] ([xshift=1.25cm,yshift=-6.45cm]current page.north west) -- ++(7.3cm,0);
\node[anchor=south west,inner sep=0pt,jpsmall] at ([xshift=1.25cm,yshift=.72cm]current page.south west) {仮定に基づく5枚の教材 / 2026.10};
\begin{scope}[shift={([xshift=11.2cm,yshift=-3.1cm]current page.north west)}]
\foreach \y/\qname in {0/qone,-.9/qtwo,-1.8/qthree} {\node[warm/node,minimum width=2.5cm,minimum height=.65cm] (\qname) at (0,\y) {待っている仕事};}
\node[warm/node,draw=BMETerracotta,fill=BMESand,minimum width=2.5cm] (service) at (0,-3.25) {窓口で処理};
\draw[warm/highlight] (qthree.south) -- (service.north);
\node[jpsmall] at (0,.75) {順番が来るまで待つ};
\end{scope}
\end{tikzpicture}
\end{frame}

\begin{frame}[plain]\begin{tikzpicture}[remember picture,overlay]
\Base{一つの窓口に、仕事が届く}{MODEL / 前提}{02}
\node[jptext,text width=13cm] at ([xshift=.98cm,yshift=-1.72cm]current page.north west) {窓口は一つ。先に届いた仕事から、1件ずつ処理する。};
\begin{scope}[shift={([xshift=.98cm,yshift=-3.25cm]current page.north west)}]
\node[warm/terminal,minimum width=2.3cm,font=\sffamily\fontsize{9}{12}\selectfont] (a) at (1.2,0) {到着};
\node[warm/node,minimum width=2.3cm,font=\sffamily\fontsize{9}{12}\selectfont] (w) at (5,0) {順番待ち};
\node[warm/node,fill=BMESand,draw=BMETerracotta,minimum width=2.3cm,font=\sffamily\fontsize{9}{12}\selectfont] (p) at (8.8,0) {処理};
\node[warm/terminal,minimum width=2.3cm,font=\sffamily\fontsize{9}{12}\selectfont] (f) at (12.6,0) {完了};
\draw[warm/flow] (a.east) -- (w.west);\draw[warm/flow] (w.east) -- (p.west);\draw[warm/flow] (p.east) -- (f.west);
\end{scope}
\draw[BMEStone,line width=.45pt] ([xshift=.98cm,yshift=-4.65cm]current page.north west) -- ++(13.8cm,0);
\node[jptext,text width=5.8cm] at ([xshift=1.02cm,yshift=-5.05cm]current page.north west) {\color{BMETerracotta}\bfseries 処理時間 $p=5$ 秒\par\vspace{.25cm}\WarmBodyText 1件の仕事が、窓口を使う時間。\\途中で割り込まず、毎回同じ長さ。};
\node[jptext,text width=6cm] at ([xshift=8cm,yshift=-5.05cm]current page.north west) {\color{BMESage}\bfseries 到着間隔 $d$ 秒\par\vspace{.25cm}\WarmBodyText 次の仕事が届くまでの時間。\\この教材では一定の間隔にする。};
\Foot\end{tikzpicture}\end{frame}

\begin{frame}[plain]\begin{tikzpicture}[remember picture,overlay]
\Base{待ち時間を式にする}{RECURRENCE / 計算}{03}
% Heading and each formula are separate nodes; \strut gives every formula the same WarmDisplayMath line box.
\node[jptext,text width=6cm] at ([xshift=.98cm,yshift=-1.8cm]current page.north west) {\bfseries 前の仕事が終わったら、始める};
\node[jptext] at ([xshift=.98cm,yshift=-2.45cm]current page.north west) {\WarmDisplayMath\strut$s_i=\max(a_i,f_{i-1})$};
\node[jptext] at ([xshift=.98cm,yshift=-3.20cm]current page.north west) {\WarmDisplayMath\strut$f_i=s_i+p$};
\node[jptext] at ([xshift=.98cm,yshift=-3.95cm]current page.north west) {\WarmDisplayMath\strut$w_i=s_i-a_i$};
\node[jptext,text width=6.2cm] at ([xshift=8cm,yshift=-1.85cm]current page.north west) {\WarmBodyText $a_i$：到着時刻　$s_i$：開始時刻\\$f_i$：完了時刻　$w_i$：待ち時間\par\vspace{.45cm}最初の仕事は時刻0に到着。\\初期値は $f_0=0$ とする。};
\draw[BMEStone,line width=.45pt] ([xshift=.98cm,yshift=-4.95cm]current page.north west) -- ++(13.8cm,0);
\node[jptext,text width=13cm] at ([xshift=1cm,yshift=-5.25cm]current page.north west) {例：3件目は8秒に到着。前の仕事は10秒に完了。};
\begin{scope}[shift={([xshift=2cm,yshift=-6.85cm]current page.north west)}]
\draw[warm/flow] (0,0) -- (10.8,0);
\foreach \x/\t in {0/8,3/10,10.5/15} {\draw[BMEInk] (\x,-.1) -- (\x,.1);\node[jpsmall,below] at (\x,-.2) {\t 秒};}
\draw[BMESage,line width=3pt] (0,.3) -- (3,.3);\draw[BMETerracotta,line width=3pt] (3,.3) -- (10.5,.3);
\node[jpsmall,above] at (1.5,.5) {待ち $2$ 秒};\node[jpsmall,above] at (6.75,.5) {処理 $5$ 秒};
\end{scope}
\Foot\end{tikzpicture}\end{frame}

\begin{frame}[plain]\begin{tikzpicture}[remember picture,overlay]
\Base{間隔が1秒違うと、待ちは積み上がる}{COMPARISON / 仮の試算}{04}
\begin{scope}[shift={([xshift=1.45cm,yshift=-6.4cm]current page.north west)},x=1cm,y=.24cm]
\foreach \y in {0,5,10,15} {\draw[BMEStone,line width=.35pt] (0,\y) -- (7.4,\y);\node[jpsmall,left] at (-.1,\y) {\y};}
\draw[warm/flow] (0,0) -- (7.9,0);\draw[warm/flow] (0,0) -- (0,17.3);
\foreach \x in {0,...,7} {\pgfmathtruncatemacro{\n}{\x+1}\node[jpsmall,below] at (\x,-.3) {\n};}
\draw[BMETerracotta,line width=1.3pt] (0,0) -- (7,14);
\draw[BMEInk,line width=1.1pt] (0,0) -- (7,7);
\draw[BMESage,line width=1.2pt] (0,0) -- (7,0);
\foreach \x in {0,...,7} {\fill[BMETerracotta] (\x,2*\x) circle[radius=1.3pt];\fill[BMEInk] (\x,\x) circle[radius=1.3pt];}
\node[jpsmall,anchor=west,text=BMETerracotta] at (7.2,14) {$d=3$ 秒};\node[jpsmall,anchor=west,text=BMEInk] at (7.2,7) {$d=4$ 秒};\node[jpsmall,anchor=west,text=BMESage] at (7.2,1) {$d=6$ 秒};
\node[jpsmall,anchor=west] at (0,18) {待ち時間（秒）};\node[jpsmall,anchor=west] at (6,-2.5) {仕事の番号};
\end{scope}
\node[jptext,text width=4cm] at ([xshift=11cm,yshift=-2.15cm]current page.north west) {\bfseries 処理は毎回5秒\par\vspace{.45cm}\WarmBodyText 3秒間隔なら、\\1件進むごとに2秒ずつ\\待ちが増える。\par\vspace{.35cm}6秒間隔なら、この仮定では\\順番待ちは生じない。\par\vspace{.5cm}\WarmDisplayMath\raggedright $w_i=(i-1)$\par\vspace{.08cm}$\phantom{w_i=}\cdot\max(0,p-d)$};
\Foot\end{tikzpicture}\end{frame}

\begin{frame}[plain]\begin{tikzpicture}[remember picture,overlay]
\Base{待ち時間を減らす、三つの方法}{DESIGN / 考え方}{05}
\node[anchor=north west,inner sep=0pt,slide/prose,text width=3.8cm] at ([xshift=.98cm,yshift=-1.85cm]current page.north west) {\color{BMETerracotta}\sffamily\fontsize{7}{9}\selectfont\bfseries 01 / 処理を短く\par\vspace{.3cm}\color{BMEBrown}\rmfamily\fontsize{15}{19}\selectfont\bfseries 5秒を4秒に\par\vspace{.4cm}\WarmBodyText 4秒間隔の到着に間に合う。\\同じ仮定なら待ちは0秒。};
\node[anchor=north west,inner sep=0pt,slide/prose,text width=3.8cm] at ([xshift=5.55cm,yshift=-1.85cm]current page.north west) {\color{BMESage}\sffamily\fontsize{7}{9}\selectfont\bfseries 02 / 到着を分散\par\vspace{.3cm}\color{BMEBrown}\rmfamily\fontsize{15}{19}\selectfont\bfseries 4秒を5秒に\par\vspace{.4cm}\WarmBodyText 5秒の処理と到着間隔が揃う。\\変動があれば余裕も必要。};
\node[anchor=north west,inner sep=0pt,slide/prose,text width=3.8cm] at ([xshift=10.12cm,yshift=-1.85cm]current page.north west) {\color{BMETerracotta}\sffamily\fontsize{7}{9}\selectfont\bfseries 03 / 窓口を増やす\par\vspace{.3cm}\color{BMEBrown}\rmfamily\fontsize{15}{19}\selectfont\bfseries 同時に処理\par\vspace{.4cm}\WarmBodyText 仕事を複数の窓口に配分する。\\窓口ごとの空き時刻を計算。};
\draw[BMEStone,line width=.45pt] ([xshift=.98cm,yshift=-4.65cm]current page.north west) -- ++(13.8cm,0);
\node[jptext,text width=13cm] at ([xshift=1.02cm,yshift=-5.15cm]current page.north west) {\color{BMEBrown}\rmfamily\fontsize{16}{22}\selectfont\bfseries 平均だけでなく、ばらつきも見る\par\vspace{.4cm}\WarmBodyText 実際の仕事は、到着も処理も一定ではない。\\この式で関係を理解したら、次は到着時刻と処理時間の記録で確かめる。};
\Foot\end{tikzpicture}\end{frame}
\end{document}
'''.replace('at PIN.', 'at ' + PIN + '.')

def write(p, text):
    p.parent.mkdir(parents=True, exist_ok=True); p.write_text(text, encoding='utf-8')
def dump(p, value): write(p, json.dumps(value, ensure_ascii=False, indent=2)+'\n')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def prepare():
    upstream=ROOT/'.build/actual-upstreams/xukp20__build-beamer-slides'
    for rel in ['LICENSE','SKILL.md','styles/warm-editorial/theme.tex','styles/warm-editorial/template-169.tex','styles/warm-editorial/STYLE.md','references/diagram-design.md','references/review-loop.md','references/page-audit-checklist.md','references/slide-text.md','references/reviewer-workflow.md','scripts/render_and_check.sh','scripts/render_pdf_crop.sh']:
        target=CASE/'upstream'/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(upstream/rel,target)
    shutil.copy2(upstream/'LICENSE',CASE/'LICENSE')
    # Fonts are originals downloaded from GUST, never extracted from OS installations.
    fontpath=r'''\usepackage{fontspec}
\defaultfontfeatures[TeX Gyre Pagella]{Path=fonts/tex-gyre/,UprightFont=texgyrepagella-regular.otf,BoldFont=texgyrepagella-bold.otf,ItalicFont=texgyrepagella-italic.otf,BoldItalicFont=texgyrepagella-bolditalic.otf}
\defaultfontfeatures[TeX Gyre Heros]{Path=fonts/tex-gyre/,UprightFont=texgyreheros-regular.otf,BoldFont=texgyreheros-bold.otf,ItalicFont=texgyreheros-italic.otf,BoldItalicFont=texgyreheros-bolditalic.otf}
'''
    write(CASE/'font-paths.tex',fontpath)
    portable_theme=(upstream/'styles/warm-editorial/theme.tex').read_text(encoding='utf-8').replace(r'\setmathfont{TeX Gyre Pagella Math}',r'\setmathfont[Path=fonts/tex-gyre/]{texgyrepagella-math.otf}')
    write(CASE/'theme-portable.tex',portable_theme)
    dump(CASE/'fonts/tex-gyre/SOURCE.json',{
        'license':'GUST Font License / LPPL-1.3c-or-later','modified':False,
        'text_version':'2.501','math_version':'1.632',
        'text_archive':'https://www.gust.org.pl/projects/e-foundry/tex-gyre/whole/tg2_501otf.zip',
        'math_archive':'https://www.gust.org.pl/projects/e-foundry/tg-math/download/texgyrepagella-math-1632.zip',
        'text_archive_sha256':sha(ROOT/'.build/beamer-texgyre/texgyre.zip'),
        'math_archive_sha256':sha(ROOT/'.build/beamer-texgyre/math.zip'),
        'files':{p.name:sha(p) for p in (CASE/'fonts/tex-gyre').glob('*.otf')},
        'note':'Original GUST OTF files. No OS font extraction. font-paths.tex maps the exact upstream font family names to these files.'})
    for family in ['shipporimincho','zenkakugothicnew']:
        for name in ['OFL.txt', 'ShipporiMincho-Regular.ttf','ShipporiMincho-Bold.ttf'] if family=='shipporimincho' else ['OFL.txt','ZenKakuGothicNew-Regular.ttf','ZenKakuGothicNew-Bold.ttf']:
            target=CASE/'fonts'/family/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/'downloads/fonts'/family/name,target)
    write(CASE/'deck.tex',TEX); write(CASE/'PROMPT.md',PROMPT+'\n')
    dump(CASE/'input/model.json', {'notice':'学習用の一定時間モデル。実測ではありません。','processing_seconds':5,'arrival_intervals_seconds':[3,4,6],'jobs':8,'formula':'w_i = (i-1)*max(0,p-d)','chart':[{ 'interval_seconds':d,'waiting_seconds':[i*max(0,5-d) for i in range(8)]} for d in [3,4,6]]})
    write(CASE/'input/BRIEF.md','# 待ち時間のしくみ\n\n一つの窓口、受付順、一定処理時間5秒、一定到着間隔の仮定を図と式で説明する5枚の教材。実績、推定性能、一般的な待ち行列の保証として扱わない。第5枚の複数窓口は設計上の考え方で、一窓口の式をそのまま適用しない。\n')
    write(CASE/'README.md',f'''# 待ち時間のしくみ

5枚の日本語Beamer教材。PDFが主出力で、編集は `deck.tex` で行います。PPTXは生成していません。

## 使用した原典

[xukp20/build-beamer-slides](https://github.com/xukp20/build-beamer-slides/tree/{PIN}) / MIT / `{PIN}`。
原典の `styles/warm-editorial/template-169.tex` の表紙構図と `theme.tex` を実際に使用。`WarmFrameHeader`、`WarmFrameFooter`、`WarmBodyText`、`WarmDisplayMath`、`warm/node`、`warm/flow` 等を直接呼び出します。原典は `upstream/` に変更せず保管。

和文用xeCJKと字体指定、墨紺の色だけを `deck.tex` 側に追加。数式と図はLaTeX/TikZのベクトルです。Shippori Minchoの明朝見出し、Zen Kaku Gothic Newの本文。公式配布の未変更TTFとOFLを `fonts/` に同梱し、OSから字体を抽出していません。

原典が使うTeX Gyre Pagella、Heros、Pagella Mathも、[公式GUST](https://www.gust.org.pl/projects/e-foundry/tex-gyre)から取得した未変更OTFとGUST Font License/LPPLを同梱。`font-paths.tex` が原典の欧文字体名を相対ファイルへ結び付けます。`theme-portable.tex` は原典themeの数学字体指定1行だけを、同じPagella Mathのファイルパスへ変更したもの。全macro・幾何・色定義は原典のままで、OSへの字体登録は不要です。

## 再生成

標準XeLaTeX環境ならこのフォルダで次を実行します。

```powershell
xelatex -interaction=nonstopmode -halt-on-error deck.tex
xelatex -interaction=nonstopmode -halt-on-error deck.tex
```

このPCではXeLaTeXコマンドがないため、公式[Tectonic 0.17.0](https://github.com/tectonic-typesetting/tectonic/releases/tag/tectonic%400.17.0)のXeTeXベースエンジンで同じソースをコンパイルしました。エンジン変更だけで、別の描画方式への代替ではありません。

```powershell
python -m pip install pymupdf
python build.py --tectonic C:/path/to/tectonic.exe
```

Tectonicは初回にTeXパッケージをダウンロードします。字体は同梱を参照します。TeXランタイム、パッケージキャッシュ、OS字体はZIPに含みません。PythonはPNGの作成にだけ使用します。

Windows公式portableの取得例です。公開場所ではなくローカル作業フォルダへ展開してください。

```powershell
Invoke-WebRequest 'https://github.com/tectonic-typesetting/tectonic/releases/download/tectonic%400.17.0/tectonic-0.17.0-x86_64-pc-windows-msvc.zip' -OutFile tectonic.zip
Expand-Archive -LiteralPath tectonic.zip -DestinationPath .build/tectonic
python build.py --tectonic .build/tectonic/tectonic.exe
```

## 内容と確認範囲

到着・処理とも一定の学習用モデル。5秒処理・3/4/6秒到着を仮定した算術で、実測値や性能実績ではありません。到着と処理の変動、優先度、複数窓口を含む実系の予測には別のモデルが必要です。

原典review-loopとpage-audit-checklistに沿って2回compile、全5ページ216dpiと重要箇所500dpi cropを描画し、文字・式・罫線・図と接続を目視します。3枚目の3式を独立した位置へ置き、罫線・例文から離しました。4枚目の「順番待ち」は意味の区切りで改行します。実施結果は `reviews/page-audit.json` と `QA.json`。Kimi K3・Opus5.5の独立再評価は技術検査と区別します。

本PCにはxelatexがないため、原典scripts/render_and_check.shそのものは未実行です。同じTeXを既存Tectonicで2回compileし、同じ解像度条件で描画する実行adapterを使います。専用CLIの実行と原典チェックリストの目視実施を混同しません。
''')
    fork=ROOT/'skill-forks/beamer-ja'
    write(fork/'SKILL.md',f'''---
name: beamer-ja
description: 原典Warm EditorialのBeamerを日本語教材・数式・TikZ資料に使う。
---

# 日本語Beamer

原典xukp20/build-beamer-slides `{PIN}` (MIT)。PDFを主成果とし、.texを編集用に渡す。PPTXと称しない。

1. `upstream/styles/warm-editorial/template-169.tex` から構図を作り、`theme.tex` のmacroを直接使う。色・余白・線・数学字体は原典を基本にする。
2. `xeCJK` を読み、Shippori MinchoとZen Kaku Gothic Newの同梱TTF/OFLを相対パスで指定。見出しは明朝、本文はゴシック。
3. 題材の仮定、式、図の意味を定義し、図はTikZ、数式はLaTeXで実装。ユーザーの構図指定を優先。
4. 原典 `references/review-loop.md` と `page-audit-checklist.md` を読む。XeLaTeXを2回、または採用済みTectonicで同じソースを2回compile。エラーと関連overfullを解消し、全変更ページを180〜220dpi、重要な線・ラベル・式を400〜600dpi cropへ描画する。共通theme/font/macroを変えたら全ページを描画する。
5. 全影響ページとcropを元の解像度で目視し、文字のはみ出し、語中改行、式と罫線の接触、余白、各接続線の始終点を確認する。修正後は再compile・再描画し、原典Draft-Ready Gateを満たすまで繰り返す。実施ページ・修正・結果をreviews/へ記録する。ユーザーは独立評価を指定済みなので再質問せず、作者検査後に独立評価へ渡す。独立合格は別記録に残す。
6. .tex/PDF/PNG/入力/依頼/原典とMIT/fontとOFL/ガイドを渡す。TeXエンジン・cacheを含めない。

## quick_validate

`python build.py --tectonic C:/path/to/tectonic.exe` で2回compileした後、全変更PNGと重要cropをpage-audit-checklistで検査する。生成成功だけで完了としない。標準依存がある環境では原典scripts/render_and_check.shも利用できる。実行していない検査・独立評価を完了と記載しない。
''')
    dump(fork/'SOURCE.json',{'repository':'xukp20/build-beamer-slides','commit':PIN,'license':'MIT','used_files':['styles/warm-editorial/template-169.tex','styles/warm-editorial/theme.tex'],'changes':['Japanese xeCJK font adapter','original TeX Gyre OTF portable path adapter: one math family line only','ink navy palette override','page3 explicit math row placement and page4 clause line breaks; original author QA restored'], 'example':'examples/repositories/beamer-showcase','format':'pdf'})
    for rel in ['LICENSE','SKILL.md','styles/warm-editorial/theme.tex','styles/warm-editorial/template-169.tex','styles/warm-editorial/STYLE.md','references/diagram-design.md','references/review-loop.md','references/page-audit-checklist.md','references/slide-text.md','references/reviewer-workflow.md','scripts/render_and_check.sh','scripts/render_pdf_crop.sh']:
        target=fork/'upstream'/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(upstream/rel,target)
    shutil.copy2(upstream/'LICENSE',fork/'LICENSE');shutil.copy2(fork/'SKILL.md',CASE/'SKILL.md');shutil.copy2(SCRIPT,CASE/'build.py')
    for family in ['shipporimincho','zenkakugothicnew']:
        target=fork/'fonts'/family;target.mkdir(parents=True,exist_ok=True)
        for font in (CASE/'fonts'/family).iterdir():shutil.copy2(font,target/font.name)
    write(fork/'japanese-fonts.tex',r'''\usepackage{xeCJK}
\setCJKmainfont[Path=fonts/shipporimincho/,BoldFont=ShipporiMincho-Bold.ttf]{ShipporiMincho-Regular.ttf}
\setCJKsansfont[Path=fonts/zenkakugothicnew/,BoldFont=ZenKakuGothicNew-Bold.ttf]{ZenKakuGothicNew-Regular.ttf}
''')
    shutil.copytree(CASE/'fonts/tex-gyre',fork/'fonts/tex-gyre',dirs_exist_ok=True)
    write(fork/'font-paths.tex',fontpath)
    write(fork/'theme-portable.tex',portable_theme)
    starter=(upstream/'styles/warm-editorial/template-169.tex').read_text(encoding='utf-8')
    starter=starter.replace(r'\input{theme.tex}',r'\input{font-paths.tex}'+'\n'+r'\input{theme-portable.tex}'+'\n'+r'\input{japanese-fonts.tex}')
    starter=starter.replace('An editorial presentation title','編集可能な日本語発表資料').replace('A restrained subtitle for a mathematical or research talk','数式・図・余白で伝える、学習のための資料').replace('Presenter · Organization · Date','発表者・所属・日付')
    write(fork/'template-ja.tex',starter)
    write(fork/'README.md','# beamer-ja\n\n日本語SKILL、原典Warm Editorial source、日本語font adapter、公式TTF/OFL、template-ja.texを同梱。PDF/.tex用でPPTX未生成。\n\nこのフォルダで `xelatex template-ja.tex` を2回、または公式Tectonic 0.17.0を取得して `tectonic template-ja.tex`。ランタイムやcacheは同梱しない。原典の元英語説明スライドを残した最小スターターで、全5枚の教材は別のbeamer-example-ja.zipを参照。\n')

def compile_deck(engine):
    render=CASE/'render';render.mkdir(parents=True,exist_ok=True)
    env={**os.environ,'TECTONIC_CACHE_DIR':str(ROOT/'.build/beamer-tectonic/cache')}
    outputs=[];passes=[]
    for pass_number in [1,2]:
        run=subprocess.run([str(Path(engine).resolve()),'--keep-logs','--keep-intermediates','--outdir',str(render),'deck.tex'],cwd=CASE,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace')
        text=run.stdout+run.stderr;outputs.append(text);write(CASE/f'.private/runtime-logs/compile-pass-{pass_number}.log',text)
        passes.append({'pass':pass_number,'exit_code':run.returncode})
        if run.returncode:raise RuntimeError(text[-8000:])
    log='\n'.join(outputs)
    relevant=[line for line in log.splitlines() if any(token in line for token in ['Overfull','Missing character','LaTeX Error'])]
    dump(CASE/'source/COMPILE.json',{'engine':'Tectonic 0.17.0 XeTeX','passes':passes,'relevant_diagnostics':relevant,'raw_logs_retained_privately':True,'source_sha256':sha(CASE/'deck.tex')})
    if relevant:raise RuntimeError('Relevant compile diagnostics: '+'\n'.join(relevant))
    import pymupdf
    doc=pymupdf.open(render/'deck.pdf')
    if len(doc)!=5:raise RuntimeError('Expected 5 pages')
    for i,page in enumerate(doc):page.get_pixmap(matrix=pymupdf.Matrix(3,3)).save(render/f'slide-{i+1:02}.png')
    shutil.copy2(render/'deck.pdf',CASE/'deck.pdf')
    return len(doc),log

def finish(count,log):
    provenance={'repository':'xukp20/build-beamer-slides','upstream_commit':PIN,'license':'MIT','method':'Original Warm Editorial template + theme macros unchanged; one math font line mapped to same official OTF file in theme-portable.tex; Japanese xeCJK adapter; same Beamer/TikZ source compiled by Tectonic 0.17.0 XeTeX engine','engine':'Tectonic 0.17.0','engine_url':'https://github.com/tectonic-typesetting/tectonic/releases/tag/tectonic%400.17.0','engine_included':False,'engine_archive_sha256':'f61ce51f0b0ade1015b7de7ef368541c5424e9756ecbd0d7af97d6d48030845f','derived_theme_sha256':sha(CASE/'theme-portable.tex'),'derived_theme_change':'Only setmathfont name to same original Pagella Math OTF file path','font_files':{str(p.relative_to(CASE)):sha(p) for p in (CASE/'fonts').rglob('*') if p.suffix in ['.ttf','.otf']},'fonts':'Unmodified official Google Fonts Shippori Mincho/Zen Kaku Gothic New TTFs (OFL-1.1), GUST TeX Gyre Pagella/Heros/Pagella Math OTFs (GUST Font License/LPPL)','font_sources':json.loads((ROOT/'data/oss-font-kit.json').read_text(encoding='utf-8'))['families'][:2] if SCRIPT.parent.name=='tools' else 'see fonts/OFL.txt','used_upstream_files':{str(p.relative_to(CASE)):sha(p) for p in (CASE/'upstream').rglob('*') if p.is_file()},'output_format':'pdf','editable_source':'deck.tex','content_status':'hypothetical educational arithmetic, not measured performance'}
    dump(CASE/'PROVENANCE.json',provenance)
    dump(CASE/'QA.json',{'status':'compile_and_preview_ready','compile_exit_code':0,'page_count':count,'png_pages_generated':count,'review_mode':'latest_independent_review_requested','representative_page_opened':False,'whole_deck_detailed_review':False,'independent_review':False,'zip_reexecution':False,'native_pptx_audit':'not applicable: PDF/TeX','compile_log':'source/COMPILE.json','relevant_compile_warnings':[line for line in log.splitlines() if 'Overfull' in line or 'Missing character' in line]})
    images=''.join(f'<figure><img src="render/slide-{i+1:02}.png" alt="{title}"><figcaption>{i+1}. {title}</figcaption></figure>' for i,title in enumerate(TITLES))
    write(CASE/'index.html','''<!doctype html><html lang="ja"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>待ち時間のしくみ</title><style>body{margin:0;background:#f7f2e8;color:#243746;font-family:sans-serif}header,main{max-width:1200px;margin:auto;padding:24px}h1{font-family:serif}a{color:#974b35}figure{margin:0 0 32px}img{display:block;width:100%;box-shadow:0 8px 30px #24374618}figcaption{padding:10px 0;font-size:13px}nav{position:fixed;bottom:15px;right:18px;background:#243746;color:#fff;padding:9px 16px;border-radius:8px}button{background:transparent;color:inherit;border:0;padding:5px;cursor:pointer}</style><header><h1>待ち時間のしくみ</h1><p>Warm Editorial / 日本語Beamer / 学習用の仮定・試算</p><a href="deck.pdf">PDF</a> · <a href="deck.tex">編集用TeX</a> · <a href="README.md">日本語ガイド</a> · <a href="../../../downloads/beamer-example-ja.zip">制作ZIP</a></header><main>'''+images+'''</main><nav><button onclick="go(-1)" aria-label="前のページ">◀</button><span id="page">1 / 5</span><button onclick="go(1)" aria-label="次のページ">▶</button></nav><script>let current=0;const slides=[...document.querySelectorAll('figure')];function go(delta){current=Math.max(0,Math.min(4,current+delta));slides[current].scrollIntoView({behavior:'smooth',block:'center'});document.querySelector('#page').textContent=(current+1)+' / 5'}document.addEventListener('keydown',e=>{if(e.key==='ArrowRight')go(1);if(e.key==='ArrowLeft')go(-1)})</script></html>''')

def package():
    excluded={'.private','.build','.git','node_modules','__pycache__','cache'}
    for folder,name in [(CASE,'beamer-example-ja.zip'),(ROOT/'skill-forks/beamer-ja','beamer-ja.zip')]:
        target=ROOT/'downloads'/name;target.parent.mkdir(exist_ok=True)
        with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as z:
            for current,dirs,files in os.walk(folder,followlinks=False):
                dirs[:]=[d for d in dirs if d not in excluded and not (Path(current)/d).is_symlink() and not os.path.isjunction(Path(current)/d)]
                for file in sorted(files):
                    p=Path(current)/file
                    if not p.is_symlink() and p.suffix not in {'.aux','.nav','.snm','.toc','.vrb','.log','.pyc'}:z.write(p,str(p.relative_to(folder.parent)))

def fragments():
    base='examples/repositories/beamer-showcase'
    dump(ROOT/'data/sol-beamer-repository-examples.json',[{'id':'beamer-showcase','title':'待ち時間のしくみ','use_case':'数式とTikZで説明する5枚の学習教材','repository':'xukp20/build-beamer-slides','skill_repository':'xukp20/build-beamer-slides','upstream_commit':PIN,'fork_id':'beamer-ja','page_count':5,'format':'pdf','preview_kind':'pdf-render','preview_notice':'PDFを表示。編集は.texで行います。PPTX未生成。','style':'Warm Editorial / 紙色・墨紺・銅色 / 明朝・ゴシック / 数式・TikZ','cover':base+'/render/slide-01.png','interior':base+'/render/slide-04.png','preview':base+'/index.html','artifact_download':base+'/deck.pdf','pdf_download':base+'/deck.pdf','source_download':'downloads/beamer-example-ja.zip','fork_download':'downloads/beamer-ja.zip','input':base+'/input/BRIEF.md','input_data':base+'/input/model.json','prompt':base+'/PROMPT.md','prompt_text':PROMPT,'provenance':base+'/PROVENANCE.json','qa':base+'/QA.json','guide':base+'/README.md','titles':TITLES,'notes':['学習用の一定到着・一定処理時間モデル。実測値・性能実績ではありません。']*5,'method':'原典Warm Editorial template/themeを直接使用し、xeCJK和文字体adapterを追加。原典の数学字体行を同じ公式OTFのパス指定にしたadapterを使い、Tectonic 0.17.0のXeTeX engineでBeamer/TikZ .texをPDFへcompile。','sample_notice':'仮定に基づく教材。PDFが主成果、編集は.tex。PPTXは生成していません。','pages':[base+f'/render/slide-{i:02}.png' for i in range(1,6)],'slides':[{'title':title,'image':base+f'/render/slide-{i+1:02}.png'} for i,title in enumerate(TITLES)]}])
    dump(ROOT/'data/sol-beamer-repository-guides.json',[{'repository':'xukp20/build-beamer-slides','summary_ja':'Warm Editorialを日本語に対応させ、数式・TikZの編集可能なTeXとPDFへ。','example_ids':['beamer-showcase'],'upstream_commit':PIN,'license':'MIT','license_paths':[base+'/LICENSE'],'skill_paths':['skill-forks/beamer-ja/SKILL.md'],'production_status':'light_check_complete','requirements':['XeLaTeX standard workflow or official Tectonic 0.17.0 XeTeX adapter','Shippori Mincho / Zen Kaku Gothic New (同梱TTF, OFL)','Python + PyMuPDF (PNG出力のみ)'],'commands':['xelatex -interaction=nonstopmode -halt-on-error deck.tex (2回)','python build.py --tectonic C:/path/to/tectonic.exe'],'guide':base+'/README.md','source_download':'downloads/beamer-example-ja.zip','fork_download':'downloads/beamer-ja.zip','limitations':['学習用の一定時間モデル。実測ではない','PDFが主出力、.texで編集、PPTX未生成','代表表示の最小確認のみ。全ページ詳細監査・独立レビュー・ZIP再実行なし']}])

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--tectonic');parser.add_argument('--case-only',action='store_true');parser.add_argument('--package-only',action='store_true');args=parser.parse_args()
    if args.package_only:package();raise SystemExit(0)
    if not args.tectonic:parser.error('--tectonic is required to compile')
    if SCRIPT.parent.name=='tools':prepare()
    count,log=compile_deck(args.tectonic)
    if SCRIPT.parent.name=='tools':
        finish(count,log)
        if not args.case_only:fragments();package()
    print(f'Compiled {count} pages: {CASE / "deck.pdf"}')
