# -*- coding: utf-8 -*-
"""
图标缩略校验 —— 新增 / 修改图标后必跑，肉眼确认"图标长得像它的名字"。
（实战教训：gearmold 曾画成"中心圆+放射线"→渲染成太阳，还被一图三用。图标必须一物一图、命名即语义。）
用法：在 assets/components 目录下 python ../tools/icons_preview.py
输出 icons_preview.png（每格一个图标 + 名称）。
"""
import sys, os
sys.path.insert(0, os.getcwd())
import mes_icons as M

names = list(M.ALL.keys())
cols = 6
cell = 120
rows = (len(names) + cols - 1) // cols
W, H = cols*cell, rows*cell + 30
s = f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg"><rect width="{W}" height="{H}" fill="#FFFFFF"/>'
for i, nm in enumerate(names):
    cx = (i % cols)*cell + cell/2
    cy = (i // cols)*cell + cell/2 - 6
    s += f'<rect x="{(i%cols)*cell+8}" y="{(i//cols)*cell+8}" width="{cell-16}" height="{cell-16}" rx="10" fill="none" stroke="#ECECEC"/>'
    s += M.ALL[nm](cx, cy, 48, "#262626")
    s += f'<text x="{cx}" y="{(i//cols)*cell+cell-14}" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#6E6E6E">{nm}</text>'
s += '</svg>'
open('icons_preview.svg', 'w', encoding='utf-8').write(s)
import cairosvg
cairosvg.svg2png(url='icons_preview.svg', write_to='icons_preview.png', output_width=W, output_height=H)
print(f"已渲染 {len(names)} 个图标 → icons_preview.png（请肉眼核对每个图标是否符合其名称语义）")
