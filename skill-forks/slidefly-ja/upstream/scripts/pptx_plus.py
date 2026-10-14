"""SlideFly -> PPTX: the 12 new kinds (morph-layouts-plus.css), frames (morph-frames.css), mocks, diagrams.
Geometry mirrors the CSS; anything this module does not recognise still lands in a plain text box."""
import re

from pptx_css import color
from pptx_text import fit, para, runs

# frame -> body box (left, right, top, bottom margins), title (x, y, w, size, role), panel boxes, highlight box
FRAMES = {
    'split-left': ((860, 120, 140, 110), (90, 130, 580, 70, 'on_accent'), [(0, 0, 760, 1080)], (90, 520, 580, 450)),
    'split-right': ((120, 860, 140, 110), (1250, 130, 580, 70, 'on_accent'), [(1160, 0, 760, 1080)], (1250, 520, 580, 450)),
    'poster': ((120, 120, 460, 90), (120, 100, 1680, 120, 'fg'), [(120, 420, 140, 8)], (1320, 460, 480, 530)),
    'band': ((120, 120, 300, 300), (120, 860, 1680, 72, 'fg'), [('tint', 0, 260, 1920, 560)], (1320, 300, 480, 480)),
    'rail': ((820, 120, 140, 110), (120, 130, 560, 76, 'fg'), [(740, 140, 6, 830)], (120, 560, 560, 410)),
    'bottom': ((120, 120, 110, 280), (120, 880, 1680, 80, 'fg'), [(120, 840, 1680, 4)], (1260, 110, 540, 690)),
    'stack': ((240, 240, 260, 90), (240, 100, 1440, 64, 'fg', 'ctr'), [(900, 222, 120, 5)], (1220, 260, 400, 730)),
    'corner': ((120, 120, 470, 90), (120, 110, 700, 64, 'on_accent'), [(0, 0, 900, 410)], (1000, 90, 800, 340)),
    'diagonal': ((120, 820, 270, 90), None, [('poly', 1000, 0, 920, 1080)], (1300, 270, 530, 720)),
    'frame': ((170, 170, 250, 120), (140, 110, 1500, 60, 'fg'), [('outline', 90, 150, 1740, 860)], (1270, 250, 480, 710)),
    'zigzag': ((120, 120, 270, 90), None, [], None),
    'numbered': ((120, 120, 270, 90), None, [], None),
    'media-left': ((1000, 120, 330, 110), (1000, 130, 800, 72, 'fg'), [('tint', 0, 0, 900, 1080)], (60, 140, 780, 800)),
    'media-right': ((120, 1000, 330, 110), (120, 130, 800, 72, 'fg'), [('tint', 1020, 0, 900, 1080)], (1080, 140, 780, 800)),
    'magazine': ((120, 620, 380, 100), (120, 100, 1400, 96, 'fg'), [(120, 336, 1680, 4)], (1380, 380, 420, 600)),
    'spotlight': ((120, 120, 650, 110), (160, 150, 1600, 104, 'fg', 'ctr'), [(900, 586, 120, 8)], None),
    'stairs': ((120, 120, 270, 90), None, [], None),
}
ON_PANEL = {'split-left', 'split-right', 'diagonal'}


def frame_panels(ctx, frame):
    acc = (ctx.t['accent'][0], 1)
    for p in FRAMES[frame][2]:
        if p[0] == 'tint':
            ctx.rect('Frame band', *p[1:], ctx.t['tint'])
        elif p[0] == 'poly':
            ctx.items.append({'name': 'Frame panel', 'x': p[1], 'y': p[2], 'w': p[3], 'h': p[4], 'fill': acc,
                              'geom': ('poly', [(0.3, 0), (1, 0), (1, 1), (0, 1)])})
        elif p[0] == 'outline':
            ctx.rect('Frame outline', *p[1:], None, line=(acc, 6))
        else:
            ctx.rect('Frame panel', *p, acc)


def count_text(node):
    """.count spans are filled by JS from --to: read it back."""
    for c in node.all_class('count'):
        m = re.search(r'--to:\s*([\d.,]+)', c.attrs.get('style', ''))
        c.kids = [(c.attrs.get('data-prefix', '') + (m.group(1) if m else '') + c.attrs.get('data-suffix', ''))]


def cards(ctx, x0, x1, y0, y1, groups, cols, fill, name='Card', anchor='ctr', gap=24, icons=None):
    rows = max(1, -(-len(groups) // cols))
    w, h = (x1 - x0 - gap * (cols - 1)) / cols, (y1 - y0 - gap * (rows - 1)) / rows
    for i, ps in enumerate(groups):
        r, c = divmod(i, cols)
        x, y = x0 + c * (w + gap), y0 + r * (h + gap)
        ico = icons[i] if icons and i < len(icons) else None
        if ico:   # icon on top, words under it
            ctx.icon(ico, x + w / 2 - 36, y + h / 2 - 90, 72)
            ctx.box(f'{name} {i + 1}', x, y + h / 2 - 6, w, h / 2, [dict(p, align='ctr') for p in ps], 't', fill=None, inset=20)
        else:
            ctx.box(f'{name} {i + 1}', x, y, w, h, ps, anchor, fill=fill, geom=('roundRect', 6000), inset=28)


def h3p(ctx, node, big=None, h3=34, p=24, role='fg'):
    ps = []
    for n in node.find_all(lambda n: n.tag in ('h3', 'p') or set(n.cls) & {'big', 'n', 'rk', 'ba-tag'}):
        if set(n.cls) & {'big', 'n', 'rk'}:
            ps.append(para(runs(ctx, n, big or 64, 'accent' if role == 'fg' else role, 'display', True)))
        elif 'ba-tag' in n.cls:
            ps.append(para(runs(ctx, n, 20, 'muted', 'body', True)))
        elif n.tag == 'h3':
            ps.append(para(runs(ctx, n, h3, role, 'display', True), 'l', 8 if ps else 0))
        elif n.parent and not (set(n.parent.cls) & {'big'}):
            ps.append(para(runs(ctx, n, p, 'muted' if role == 'fg' else role), 'l', 6))
    for li in node.find_all(lambda n: n.tag == 'li'):
        ps.append(para(runs(ctx, li, p, role), 'l', 6, 110, ctx.t.get('bullet', '•')))
    return ps


def plus(ctx, slide, box):
    """Body of the new kinds inside box (x0, x1, y0, y1). Returns True if handled."""
    node, kind = slide['node'], slide['kind']
    x0, x1, y0, y1 = box
    if kind == 'big-number' and node.by_class('bignum'):
        count_text(node)
        b = node.by_class('bignum')
        fig = b.by_class('fig')
        ctx.box('Figure', x0, y0, (x1 - x0) * 0.45, y1 - y0, [para(runs(ctx, fig, fit(fig, 300, (x1 - x0) * 0.45), 'accent', 'display', True))], 'ctr')
        ps = [para(runs(ctx, n, 40 if 'lead' in n.cls else 22, 'fg' if 'lead' in n.cls else 'muted'), 'l', 18)
              for n in b.find_all(lambda n: set(n.cls) & {'lead', 'src'})]
        ctx.box('Say', x0 + (x1 - x0) * 0.5, y0, (x1 - x0) * 0.5, y1 - y0, ps, 'ctr')
    elif kind == 'bento' and node.by_class('bento'):
        cells = node.all_class('cell')
        groups = [h3p(ctx, c, 120, 36, 24, 'on_accent' if 'hot' in c.cls else 'fg') for c in cells]
        taken, spots = set(), []   # CSS grid auto-placement: 4 columns, .wide spans 2 columns, .tall 2 rows
        for c in cells:
            cw, ch = (2 if 'wide' in c.cls else 1), (2 if 'tall' in c.cls else 1)
            cy, cx = next((r, q) for r in range(99) for q in range(5 - cw)
                          if not any((r + a, q + b) in taken for a in range(ch) for b in range(cw)))
            taken |= {(cy + a, cx + b) for a in range(ch) for b in range(cw)}
            spots.append((cx, cy, cw, ch))
        w = (x1 - x0 - 72) / 4
        h = (y1 - y0 - 24 * (max(r for r, _ in taken))) / (max(r for r, _ in taken) + 1)
        for i, (c, ps) in enumerate(zip(cells, groups)):
            cx, cy, cw, ch = spots[i]
            fill = (ctx.t['accent'][0], 1) if 'hot' in c.cls else ctx.t['card']
            bx, by = x0 + cx * (w + 24), y0 + cy * (h + 24)
            ctx.box(f'Cell {i + 1}', bx, by, w * cw + 24 * (cw - 1), h * ch + 24 * (ch - 1), ps, 'b', fill=fill, geom=('roundRect', 6000), inset=28)
            ico = c.find(lambda n: 'ico' in n.cls)
            if ico:
                ctx.icon(ico, bx + 28, by + 28, 56, 'on_accent' if 'hot' in c.cls else 'accent')
    elif kind == 'process' and node.by_class('process'):
        steps = node.by_class('process').children(lambda n: n.tag == 'li')
        w = (x1 - x0 - 8 * (len(steps) - 1)) / max(len(steps), 1)
        mid = color(f'color-mix(in srgb, #{ctx.t["accent"][0]} 72%, #{ctx.t["bg"][0]})')   # even steps, as morph-layouts-plus
        for i, s in enumerate(steps):
            x = x0 + i * (w + 8)
            n = s.by_class('n')
            ctx.box(f'Step {i + 1}', x, y0 + 60, w, 130, [para(runs(ctx, n, 64, 'on_accent', 'display'))] if n else [],
                    'ctr', fill=(ctx.t['accent'][0], 1) if i % 2 == 0 else mid, geom='homePlate' if i == 0 else 'chevron', inset=40)
            ps = [para(runs(ctx, k, 46 if k.tag == 'h3' else 31, 'fg' if k.tag == 'h3' else 'muted', 'display' if k.tag == 'h3' else 'body'), 'l', 18)
                  for k in s.children(lambda k: k.tag in ('h3', 'p'))]
            ctx.box(f'Step text {i + 1}', x, y0 + 200, w, y1 - y0 - 200, ps, 't', inset=14)
    elif kind == 'compare-table' and node.find(lambda n: n.tag == 'table'):
        rows = list(node.find_all(lambda n: n.tag == 'tr'))
        cols_n = max(len(r.children(lambda c: c.tag in ('td', 'th'))) for r in rows)
        rh, cw = (y1 - y0) / max(len(rows), 1), (x1 - x0) / max(cols_n, 1)
        for r, tr in enumerate(rows):
            for c, cell in enumerate(tr.children(lambda k: k.tag in ('td', 'th'))):
                pick = 'pick' in cell.cls
                fill = (ctx.t['accent'][0], 1) if pick and r == 0 else (ctx.t['tint'] if pick else None)
                role = 'on_accent' if pick and r == 0 else ('fg' if c == 0 or pick else 'muted')
                ctx.box(f'Cell {r}-{c}', x0 + c * cw, y0 + r * rh, cw, rh, [para(runs(ctx, cell, 26 if r else 22, role, 'body', r == 0 or c == 0 or pick))],
                        'ctr', fill=fill, inset=14)
    elif kind == 'countdown' and node.by_class('countdown'):
        items = node.by_class('countdown').children(lambda n: n.tag == 'li')
        unit = (y1 - y0) / (len(items) + 0.5)   # grid 150px | 560px | rest, rows split by a hairline, number one 1.5x taller
        y = y0
        for i, li in enumerate(items):
            last = i == len(items) - 1
            h = unit * (1.5 if last else 1)
            ctx.rect(f'Rank line {i + 1}', x0, y, x1 - x0, 1.5, (ctx.t['fg'][0], 0.15))
            rk, h3, p = li.by_class('rk'), li.find(lambda k: k.tag == 'h3'), li.find(lambda k: k.tag == 'p')
            if rk:
                ctx.box(f'Rank {i + 1}', x0, y, 150, h, [para(runs(ctx, rk, 128 if last else 76, 'accent' if last else 'muted', 'display'))], 'ctr')
            if h3:
                ctx.box(f'Rank title {i + 1}', x0 + 180, y, 560, h, [para(runs(ctx, h3, 50 if last else 38, 'accent' if last else 'fg', 'display'))], 'ctr')
            if p:
                ctx.box(f'Rank text {i + 1}', x0 + 770, y, x1 - x0 - 770, h, [para(runs(ctx, p, 27, 'muted'))], 'ctr')
            y += h
    elif kind == 'before-after' and node.by_class('ba'):
        __import__('pptx_extras').before_after(ctx, node, x0, x1, y0, y1)
    elif node.by_class('ico-grid'):
        items = node.by_class('ico-grid').children(lambda n: n.tag == 'li')
        cards(ctx, x0, x1, y0, y1, [h3p(ctx, li, None, 34, 24) for li in items], 2 if len(items) == 4 else 3, None, 'Point',
              icons=[li.find(lambda n: 'ico' in n.cls) for li in items])
    else:
        return False
    return True


def style_box(node):
    """left/top/width/height px written inline on a mock or diagram, else None."""
    st = node.attrs.get('style', '')
    g = {k: float(v) for k, v in re.findall(r'(left|top|width|height|right|bottom):\s*(-?\d+(?:\.\d+)?)px', st)}
    if 'left' in g or 'right' in g:
        w = g.get('width', 1920 - g.get('left', 0) - g.get('right', 0))
        x = g.get('left', 1920 - g.get('right', 0) - w)
        top = g.get('top', 270)
        h = g.get('height', 1080 - top - g.get('bottom', 90))
        return x, top, w, h
    return None


def leftover_text(ctx, node, used, box):
    """Text of top-level children no other rule consumed: never lose content. A child placed with an
    inline left/top keeps that spot; the rest (source lines, notes) goes in a small strip at the foot."""
    rest = [k for k in node.children() if k not in used and k.text() and 'photo-credit' not in k.cls
            and k.tag not in ('img', 'script', 'style', 'svg') and 'frame-panel' not in k.cls]
    notes, body = [], []
    for k in rest:
        spot = style_box(k) or __import__('pptx_free').css_box(ctx, k)
        if spot:   # free slides: the block keeps its spot and its CSS look (pptx_free)
            __import__('pptx_free').free_box(ctx, k, spot)
        elif len(k.text()) < 220 and not k.find(lambda n: n.tag == 'li'):
            notes.append(para(runs(ctx, k, 18, 'muted')))
        else:   # a real block (a source list, a paragraph): one paragraph per line or item in the body zone
            items = k.find_all(lambda n: n.tag in ('li', 'p', 'h3'))
            body += [para(runs(ctx, n, 30 if n.tag == 'h3' else 22, 'fg' if n.tag == 'h3' else 'muted', 'display' if n.tag == 'h3' else 'body', n.tag == 'h3'), 'l', 8)
                     for n in items] or [para(runs(ctx, k, 26))]
    if body:
        ctx.box('Text', box[0], box[2], box[1] - box[0], box[3] - box[2] - 80, body, 't')
    if notes:
        ctx.box('Note', box[0], 1080 - 76, box[1] - box[0], 60, notes, 'b')
    return bool(rest)
