# -*- coding: utf-8 -*-
"""
页码集中回填 —— 解决"页码/总页数分散在各脚本、反复不一致（/50 /64 /57 并存）"的坑。
做法：各页渲染时页脚一律写占位（如 chrome 的 page 参数传 "—"，total 传同一个数），
最后用本脚本按全册顺序一次性回填真实页码，并重渲染 PNG。封面/章扉/尾页不含占位串、自动跳过。

用法：
  1) 把 NAMES 改成你的全册页面顺序（文件名不含 .svg）
  2) python pageno_fill.py <svg目录>
"""
import sys, cairosvg

# —— 改成你的全册顺序 ——
NAMES = []   # 例：['n01','n02', ... , 'n_end']

def main(out):
    total = len(NAMES)
    placeholder = f'— / {total}'
    cnt = 0
    for idx, name in enumerate(NAMES):
        p = f'{out}/{name}.svg'
        try:
            t = open(p, encoding='utf-8').read()
        except FileNotFoundError:
            print(f"  缺 {name}.svg"); continue
        if placeholder in t:
            t = t.replace(placeholder, f'{idx+1} / {total}', 1)
            open(p, 'w', encoding='utf-8').write(t)
            cairosvg.svg2png(url=p, write_to=f'{out}/{name}.png', output_width=1280, output_height=720)
            cnt += 1
    print(f"回填 {cnt} 页 / 共 {total} 页（封面/章扉/尾页无占位串、已跳过）")

if __name__ == '__main__':
    if not NAMES:
        print("请先在脚本里把 NAMES 填成全册页面顺序")
    else:
        main(sys.argv[1] if len(sys.argv) > 1 else '.')
