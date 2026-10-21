"""Prepare and render the pinned quarto-talks teaching example (no replacement renderer)."""
from pathlib import Path
import argparse, base64, difflib, hashlib, json, shutil, subprocess, sys

ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / 'examples/repositories/quarto-talks-showcase'
PIN = '60f69c3568181898767470382d5599d4bb86b7b6'
REPO = 'alfredo-hs/quarto-talks'

def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')

def prepare():
    upstream = ROOT / '.build/actual-upstreams/alfredo-hs__quarto-talks'
    CASE.mkdir(parents=True, exist_ok=True)
    shutil.copytree(upstream, CASE / 'source/upstream', dirs_exist_ok=True)
    shutil.copytree(upstream / '_extensions', CASE / '_extensions', dirs_exist_ok=True)
    shutil.copy2(upstream / 'LICENSE', CASE / 'LICENSE')
    shutil.copy2(Path(__file__), CASE / 'source/build.py')
    families = json.loads((ROOT/'data/oss-font-kit.json').read_text(encoding='utf-8'))['families']
    choices = {'shipporimincho': ['ShipporiMincho-Bold.ttf'], 'bizudpgothic':['BIZUDPGothic-Regular.ttf'], 'jetbrainsmono':['JetBrainsMono[wght].ttf']}
    receipts=[]
    for f in families:
        if f['id'] not in choices: continue
        receipt = {k:v for k,v in f.items() if k != 'files'}
        receipt['files']=[]
        folder=CASE/'fonts'/f['id'];folder.mkdir(parents=True,exist_ok=True)
        shutil.copy2(ROOT/f['license_file'], folder/'OFL.txt')
        for item in f['files']:
            src=ROOT/item['file']
            if src.name not in choices[f['id']]:continue
            assert hashlib.sha256(src.read_bytes()).hexdigest()==item['sha256']
            shutil.copy2(src,folder/src.name)
            receipt['files'].append({**item,'file':str((folder/src.name).relative_to(CASE)).replace('\\','/')})
        receipts.append(receipt)
    write(CASE/'fonts/SOURCE.json',json.dumps(receipts,ensure_ascii=False,indent=2))
    write(CASE/'input/data.csv','x,y\n0,1\n1,3\n2,2\n3,5\n4,4\n')
    write(CASE/'source/compute_fit.py',COMPUTE)
    subprocess.run([sys.executable,str(CASE/'source/compute_fit.py')],cwd=CASE,check=True)
    write(CASE/'_quarto.yml','project:\n  type: default\n  render:\n    - talk.qmd\n')
    write(CASE/'talk.qmd',QMD)
    write(CASE/'source/bridge.html',BRIDGE)
    write(CASE/'references.bib',BIB)
    faces=[]
    specs=[('shipporimincho','ShipporiMincho-Bold.ttf','Shippori Mincho','700'),('bizudpgothic','BIZUDPGothic-Regular.ttf','BIZ UDPGothic','400'),('jetbrainsmono','JetBrainsMono[wght].ttf','JetBrains Mono','100 800')]
    for folder,name,family,weight in specs:
        data=base64.b64encode((CASE/'fonts'/folder/name).read_bytes()).decode()
        faces.append(f'@font-face {{font-family:"{family}";font-style:normal;font-weight:{weight};src:url("data:font/ttf;base64,{data}") format("truetype");font-display:block;}}')
    write(CASE/'source/fonts.html','<style>\n'+'\n'.join(faces)+'\n</style>')
    write(CASE/'source/japanese.scss',SCSS.replace('/* FONT_FACES */','/* Font faces embedded in source/fonts.html (outside Sass parser). */'))
    patch=''.join(difflib.unified_diff((upstream/'template.qmd').read_text(encoding='utf-8').splitlines(True),QMD.splitlines(True),fromfile='upstream/template.qmd',tofile='talk.qmd'))
    write(CASE/'source/local.diff',patch+'\n# Added source/japanese.scss: local Japanese font roles / OFL data embedding; original extension SCSS unchanged.\n# Added source/bridge.html: same-origin 0-based Reveal API bridge only.\n# _quarto.yml: render only talk.qmd.\n')

COMPUTE = '''"""Real least-squares calculation and figures from five synthetic teaching points."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

root=Path(__file__).resolve().parents[1]
d=np.genfromtxt(root/'input/data.csv',names=True,delimiter=',')
x,y=d['x'],d['y']
X=np.column_stack([x,np.ones(len(x))])
(a,b),residuals,rank,singular=np.linalg.lstsq(X,y,rcond=None)
fitted=X@np.array([a,b]);errors=y-fitted
result={'data_kind':'synthetic teaching points; unitless', 'numpy_version':np.__version__, 'matplotlib_version':matplotlib.__version__, 'x':x.tolist(), 'y':y.tolist(), 'slope':float(a),'intercept':float(b),'fitted_y':fitted.tolist(),'residual_y':errors.tolist(),'sum_squared_residuals':float(np.sum(errors**2)),'lstsq_returned_residuals':residuals.tolist(),'rank':int(rank),'singular_values':singular.tolist(),'display_equation':f'y = {a:.1f}x + {b:.1f}'}
(root/'output').mkdir(exist_ok=True)
(root/'output/results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
plt.rcParams['svg.fonttype']='path'
mono=FontProperties(fname=root/'fonts/jetbrainsmono/JetBrainsMono[wght].ttf',size=18)
for fitted_plot,name in [(False,'scatter'),(True,'fitted')]:
    fig,ax=plt.subplots(figsize=(12,5.1),layout='constrained')
    ax.spines[['top','right']].set_visible(False)
    for edge in ['bottom','left']:ax.spines[edge].set_color('#d5dde1')
    ax.set_xlim(-.3,4.3);ax.set_ylim(0,6);ax.set_xticks(range(5));ax.set_yticks(range(7))
    ax.tick_params(colors='#62717a',length=0,pad=10)
    for label in ax.get_xticklabels()+ax.get_yticklabels(): label.set_fontproperties(mono)
    ax.set_xlabel('x',fontproperties=mono,color='#20262a',loc='right')
    ax.set_ylabel('y',fontproperties=mono,color='#20262a',rotation=0,loc='top',labelpad=15)
    ax.grid(axis='y',color='#edf0f2',linewidth=.8)
    if fitted_plot:
        ax.plot([0,4],[b,a*4+b],color='#315f7d',linewidth=3)
        ax.vlines(x,np.minimum(y,fitted),np.maximum(y,fitted),color='#62717a',linestyle='dashed',linewidth=1.5)
    ax.scatter(x,y,s=155,c='#315f7d',edgecolors='white',linewidth=2,zorder=4)
    fig.savefig(root/f'output/{name}.svg',format='svg',metadata={'Description':'Synthetic teaching points, not observations. Generated from input/data.csv by source/compute_fit.py.'})
    plt.close(fig)
print(f'Actual calculation: a={a:.1f}, b={b:.1f}, SSE={np.sum(errors**2):.1f}; NumPy {np.__version__}')
'''

QMD = r'''---
pagetitle: "合成5点から最小二乗直線を求める"
lang: ja
bibliography: references.bib
suppress-bibliography: true
format:
  quarto-talks-revealjs:
    output-file: index.html
    theme: [default, "_extensions/quarto-talks/quarto-talks.scss", "source/japanese.scss"]
    include-after-body: source/bridge.html
    include-in-header: source/fonts.html
---

## 合成5点から<br>直線を求める {.opening}

::: {.columns}
::: {.column width="56%"}
5点のばらつきを<br>最小二乗直線で表す

::: {.context}
5分の小教材 ／ 単位のない合成データ<br>
現実の観測値や研究成果ではありません。
:::
:::
::: {.column width="40%"}
| 点 | x | y |
|:--|--:|--:|
| 1 | 0 | 1 |
| 2 | 1 | 3 |
| 3 | 2 | 2 |
| 4 | 3 | 5 |
| 5 | 4 | 4 |

::: {.context}
入力：`input/data.csv`
:::
:::
:::

::: {.notes}
問いを立ててから、5点の表を見せる。xとyは単位を持たない学習用の数。実測や因果関係は示していない。
:::

## 同じ5点を散布図で示す {.visual}

![横にx、縦にy。同じ5点を図へ移した。](output/scatter.svg){fig-alt="合成5点 (0,1), (1,3), (2,2), (3,5), (4,4) の散布図"}

::: {.notes}
表と図は同じ入力を使う。点の上下にばらつきがあるので、すべての点を通る一本の直線にはならない。
:::

## 直線の傾きと切片を求める {.math}

$$
y=ax+b
$$

::: {.definition}
**a**：傾き　　**b**：切片
:::

点から線への縦のずれを二乗し、その合計が小さくなる線を選ぶ。

::: {.context}
この選び方が「最小二乗」。傾きの単位や因果は、この合成例から決めない。
:::

::: {.notes}
NumPy公式linalg.lstsq文書の最小二乗の定義を踏まえる。ここでは二変数の係数aとbで直線を表す。数式は原典のmathクラスとQuarto KaTeXで描画。
:::

## NumPyで係数を計算する {.code}

```python
import numpy as np
d = np.genfromtxt("input/data.csv", names=True, delimiter=",")
x, y = d["x"], d["y"]
X = np.column_stack([x, np.ones(len(x))])
a, b = np.linalg.lstsq(X, y, rcond=None)[0]
print(f"a={a:.1f}, b={b:.1f}")
```

::: {.actual-output}
実行結果　`a=0.8, b=1.4`
:::

::: {.context}
同じ処理を `source/compute_fit.py` で実行済み。<br>
[NumPy公式：linalg.lstsq](https://numpy.org/doc/stable/reference/generated/numpy.linalg.lstsq.html) ／ 詳細値：`output/results.json`
:::

::: {.notes}
コード表示は原典templateの普通のPython fenced block。実際の計算は同梱compute_fit.pyをPythonで実行した。Quartoがこの表示ブロックを実行したとは称さない。aとbを一桁へ丸めた表示と詳細結果JSONを分ける。
:::

## 当てはめた直線と残差を確認する {.visual}

![y = 0.8x + 1.4。点線は、点から線への縦のずれ。](output/fitted.svg){fig-alt="合成5点に最小二乗直線y=0.8x+1.4を重ね、縦の残差を点線で示した図"}

::: {.context .limit}
この5点への当てはめ。外の範囲・現実の予測精度・原因は分からない。
:::

::: {.notes}
縦のずれを二乗した合計は実計算で3.6。これはこの設定の残差の量であり、科学的成果や未来の精度の証明ではない。
:::

## 次の演習：1点を変えて<br>直線を比較する {.question}

::: {.next-step}
1. input/data.csvのyを1点変更する<br>
2. compute_fit.pyを再実行する<br>
3. 係数と残差を変更前と比較する
:::

::: {.context}
入力の5点から、線とその限界を一緒に読む。
:::

::: {.notes}
次の実験を提案する問いで終える。変更後の計算を実行済みとは述べない。学習者がinput/data.csvを変え、同じcompute_fit.pyを実行できる。
:::
'''

SCSS = '''/*-- scss:defaults --*/
$font-family-sans-serif: "BIZ UDPGothic", sans-serif;
$font-family-monospace: "JetBrains Mono", "BIZ UDPGothic", monospace;
$presentation-heading-font: "Shippori Mincho", serif;
$mainFont: "BIZ UDPGothic", sans-serif;
$headingFont: "Shippori Mincho", serif;
$codeFont: "JetBrains Mono", "BIZ UDPGothic", monospace;
/*-- scss:rules --*/
/* FONT_FACES */
.reveal {font-family:"BIZ UDPGothic",sans-serif;}
.reveal h1,.reveal h2,.reveal h3 {font-family:"Shippori Mincho",serif;font-weight:700;line-height:1.24;}
.reveal code,.reveal pre {font-family:"JetBrains Mono","BIZ UDPGothic",monospace;font-variant-ligatures:none;font-feature-settings:"liga" 0,"calt" 0;}
.reveal .slides section.opening h2 {font-size:2.05em;margin-bottom:.7em;}
.reveal .slides .columns {align-items:center;gap:3%;}
.reveal .slides .opening table {width:100%;font-size:.83em;}
.reveal .slides .context {color:#62717a;font-size:.67em;line-height:1.65;margin-top:1.1em;}
.reveal .slides section.math>p {max-width:1100px;font-size:.75em;}
.reveal .definition {font-size:.68em;margin:1em 0 1.8em;}
.reveal .slides section.code div.sourceCode {width:100%;background:#f4f6f7;}
.reveal .slides section.code div.sourceCode pre,.reveal .slides section.code div.sourceCode code {width:100%;max-width:none;box-sizing:border-box;}
.reveal .actual-output {color:#315f7d;font-size:.8em;margin-top:1em;}
.reveal .slides section.visual .limit {margin:.7em auto 0;text-align:center;font-size:.64em;max-width:1350px;}
.reveal .slides section.visual:has(.limit) figure img {max-height:430px;}
.reveal .slides section.question::before {content:"演習";}
.reveal .next-step {margin-top:1.2em;font-size:.88em;line-height:1.8;}
'''

BRIDGE = '''<script>
// Added outside the original Reveal runtime. Same-origin, zero-based horizontal slides.
(()=>{const send=()=>{if(window.parent!==window&&window.Reveal)window.parent.postMessage({type:'yebisu-page',index:Reveal.getIndices().h},location.origin);};
window.addEventListener('message',e=>{if(e.origin!==location.origin||e.source!==window.parent||e.data?.type!=='yebisu-slide'||!Number.isInteger(e.data.index))return;if(window.Reveal)Reveal.slide(Math.max(0,Math.min(5,e.data.index)));});
const bind=()=>{if(!window.Reveal)return;Reveal.on('ready',send);Reveal.on('slidechanged',send);if(Reveal.isReady())send();};
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',bind);else bind();})();
</script>
'''

BIB = '''@online{numpy-lstsq,
  author = {{NumPy Developers}},
  title = {numpy.linalg.lstsq},
  url = {https://numpy.org/doc/stable/reference/generated/numpy.linalg.lstsq.html},
  urldate = {2026-10-14},
  note = {Official NumPy 2.5 API manual; minimum Euclidean 2-norm solution and line-fitting example}
}
'''

def main():
    p=argparse.ArgumentParser();p.add_argument('--prepare',action='store_true');p.add_argument('--quarto',default='quarto');p.add_argument('--case',type=Path,default=CASE);a=p.parse_args()
    if a.prepare:prepare()
    # Portable kit: source/build.py needs no project data when only rendering.
    completed=subprocess.run([a.quarto,'render','talk.qmd'],cwd=a.case,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    write(a.case/'output/quarto-render.log',completed.stdout)
    print(completed.stdout)
    completed.check_returncode()
if __name__=='__main__':main()
