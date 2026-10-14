"""SlideFly -> PPTX: details of the new layouts that plain text boxes miss.

- chapter: the huge outlined number behind the title (.ch-num, -webkit-text-stroke) as outlined text
- cta: the action buttons (.cta-btn) as pills, the primary one filled with the accent
"""
import re

from pptx_css import color, px, resolve
from pptx_text import lines, para, runs


def chapter_num(ctx, node, sheet, sstate, tok, at):
    n = node.by_class('ch-num')
    if not n or not n.text():
        return
    d = sheet.slide_rule(dict(sstate, kind='chapter'), 'ch-num')
    g = lambda k, dv='': resolve(d.get(k, dv), [d, tok]).strip()  # noqa: E731
    m = re.search(r'(\d+(?:\.\d+)?)px', g('font-size') or g('font'))
    size = px(m.group(1)) if m else 680
    stroke = g('-webkit-text-stroke')
    sw = px(g('-webkit-text-stroke-width') or (re.match(r'([\d.]+)px', stroke).group(1) if re.match(r'([\d.]+)px', stroke) else '4'), 4)
    sc = color(g('-webkit-text-stroke-color') or re.sub(r'^[\d.]+px\s*', '', stroke)) or ctx.t['accent']
    op = px(g('opacity', '1'), 1)
    w = len(n.text()) * size * 0.75   # generous box; the text is aligned to the side CSS anchors it to
    right, bottom, left = g('right'), g('bottom'), g('left')
    at_left = bool(left and left != 'auto')
    x = px(left) if at_left else 1920 - px(right or '90') - w
    y = 1080 - px(bottom or '-110') - size
    r = dict(ctx.run(n.text(), size, sc, False, 'display'), outline=((sc[0], sc[1] * op), sw * 0.75))
    p = dict(para([r], 'l' if at_left else 'r'), exact=size)   # line-height: 1
    ctx.items.insert(at, {'name': 'Chapter number', 'x': x, 'y': y, 'w': w, 'h': size, 'paras': [p],
                          'anchor': 't', 'fill': None, 'geom': 'rect', 'line': None, 'rot': 0, 'inset': 0, 'anim': True})


def before_after(ctx, node, x0, x1, y0, y1):
    """Two cards and an arrow: 'before' dashed and muted with crosses, 'after' outlined in the accent with ticks."""
    sides = node.all_class('ba-side')
    cw = (x1 - x0 - 110) / 2
    acc, line = ctx.t['accent'], (ctx.t['fg'][0], 0.18)
    tint = color(f'color-mix(in srgb, #{acc[0]} 8%, #{ctx.t["bg"][0]})')
    for i, s in enumerate(sides[:2]):
        after = 'after' in s.cls
        x = x0 + i * (cw + 110)
        n0 = len(ctx.items)
        ctx.box('Side card', x, y0, cw, y1 - y0, [para([])], 't', fill=tint if after else None,
                line=(acc, 3) if after else (line, 2, 'dash'), geom=('roundRect', 4000))
        tag, h3 = s.by_class('ba-tag'), s.find(lambda n: n.tag == 'h3')
        lis = s.find_all(lambda n: n.tag == 'li')
        ps = [para(runs(ctx, h3, 54, 'fg', 'display'))] if h3 else []
        for li in lis:
            mark = ctx.run('✓  ' if after else '✕  ', 34, 'accent' if after else 'muted', after)
            ps.append(dict(para([mark] + runs(ctx, li, 34, 'fg' if after else 'muted'), 'l', 20), line=135))
        est = (lines(h3.text(), 54, cw - 104) * 54 * 1.2 if h3 else 0) + sum(lines(li.text(), 34, cw - 150) * 34 * 1.4 + 20 for li in lis)
        top = y0 + (y1 - y0 - est - 58) / 2
        if tag:
            tw = len(tag.text()) * 20 * 0.75 + 44
            r = dict(ctx.run(tag.text(), 20, 'on_accent' if after else 'muted', True), caps=True)
            ctx.box('Side tag', x + 52, top, tw, 38, [para([r], 'ctr')], 'ctr', fill=(acc[0], 1) if after else None,
                    line=(acc if after else ctx.t['muted'], 2), geom=('roundRect', 50000))
        ctx.box('Side text', x + 52, top + 58, cw - 104, est + 20, ps, 't')
        for it in ctx.items[n0:]:
            it['src'] = s
    arrow = node.by_class('ba-arrow')
    if arrow:
        ctx.box('Arrow', x0 + cw, (y0 + y1) / 2 - 50, 110, 100, [para([ctx.run(arrow.text(), 76, 'accent', False, 'display')], 'ctr')], 'ctr')
        ctx.items[-1]['src'] = arrow


def css_sizes(ctx, sheet, sstate, tok, sizes):
    """Font sizes a style sets for the stacked parts of this slide (`.slide[data-layout="closing"] .title { font-size }`),
    and the classes it writes in capitals (text-transform: uppercase) -> ctx.caps."""
    out = dict(sizes)
    ctx.caps = set()
    for cls in list(sizes) + ['kicker', 'meta', 'cite']:
        d = sheet.slide_rule(sstate, cls)
        fs = resolve(d.get('font-size', ''), [d, tok])
        if fs.endswith('px') and cls in out:
            out[cls] = px(fs)
        if resolve(d.get('text-transform', ''), [d, tok]).strip() == 'uppercase':
            ctx.caps.add(cls)
    return out


def brand(ctx, slide_node, state, tok):
    """The stage logo (morph-brand.css): hero on cover/closing, small in the corner inside, hidden on quote/photo.
    Its icon and name are named !!brand-* so Morph flies them between poses like the HTML."""
    stage = slide_node.parent
    b = stage.children(lambda n: 'brand' in n.cls)[0] if stage and stage.children(lambda n: 'brand' in n.cls) else None
    if b is None:
        return
    pose = state.get('brand') or ('hero' if state['layout'] in ('cover', 'closing') else 'hide' if state['layout'] in ('quote', 'photo') else 'corner')
    def g(k, d):   # '.4', '-50%', '1840px' -> number
        m = re.search(r'-?\d*\.?\d+', resolve(tok.get(k, d), [tok]))
        return float(m.group()) if m else float(re.search(r'-?\d*\.?\d+', d).group())
    key = 'hero' if pose == 'hero' else 'corner'
    bx, by, s = g(f'--brand-{key}-x', '960px' if key == 'hero' else '1840px'), g(f'--brand-{key}-y', '84px' if key == 'hero' else '34px'), \
        g(f'--brand-{key}-s', '1' if key == 'hero' else '.4')
    a = g(f'--brand-{key}-a', '-50%' if key == 'hero' else '-100%') / 100
    if pose == 'hide':
        by = -200
    name = b.by_class('brand-name')
    W = 144 + (len(name.text()) * 52 * 0.5 if name else 0)
    x = bx + a * W * s
    ico = b.find(lambda n: 'ico' in n.cls)
    if ico:
        n0 = len(ctx.items)
        ctx.icon(ico, x, by, 120 * s, 'accent')
        for it in ctx.items[n0:]:
            it.update(name='!!brand-ico', anim=False)   # flies with Morph, no entrance effect
    if name:
        ctx.box('!!brand-name', x + 144 * s, by, (W - 144) * s + 40, 120 * s, [para(runs(ctx, name, 52 * s, 'fg', 'display'))], 'ctr')


def cta_buttons(ctx, node, x, y, w, h, align):
    """Pills under the cover-shaped text column; the stacked text box above is shortened to make room."""
    acts = node.by_class('cta-actions')
    if not acts:
        return
    btns = acts.all_class('cta-btn')
    text_box = ctx.items[-1] if ctx.items and ctx.items[-1].get('paras') else None
    est = sum(lines(''.join(r['text'] for r in p['runs']), p['runs'][0]['size'], w) * p['runs'][0]['size'] * 1.2 + p.get('space', 0)
              for p in (text_box['paras'] if text_box else []) if p['runs'])
    top = y + (h - est - 110) / 2
    if text_box:
        text_box.update(y=top, h=est + 10, anchor='t')
    bx = x
    for b in btns:
        rs = runs(ctx, b, 28, 'fg', 'body', True)
        bw = len(b.text()) * 28 * 0.56 + 76
        primary = 'primary' in b.cls
        for r in rs:
            r['color'] = ctx.t['on_accent'] if primary else ctx.t['fg']
        ctx.box('Button', bx, top + est + 40, bw, 72, [para(rs, 'ctr')], 'ctr', fill=(ctx.t['accent'][0], 1) if primary else None,
                line=((ctx.t['accent'] if primary else ctx.t['fg']), 3), geom=('roundRect', 50000))
        ctx.items[-1]['src'] = acts
        bx += bw + 20
