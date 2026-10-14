"""Real least-squares calculation and figures from five synthetic teaching points."""
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
