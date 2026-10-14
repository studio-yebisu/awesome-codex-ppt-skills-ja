"""Export a SlideFly deck to an editable PowerPoint file with Morph transitions.

Usage: python export-pptx.py <deck.html> <out.pptx>

Standard library only, no browser. Reads the deck HTML (source or the single inlined file) and the
style CSS it links. Every actor becomes a shape named "!!<actor>" on every slide, placed in that
slide's pose, so PowerPoint Morph glides it from slide to slide like the HTML engine. Text becomes
editable text boxes laid out like morph-layouts / morph-frames. See references/xuat-pptx.md.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pptx_css import Sheet, color, px, resolve  # noqa: E402
from pptx_shapes import actor_shape, image, theme  # noqa: E402
from pptx_deck import load, slides  # noqa: E402
from pptx_bgsvg import background_svg  # noqa: E402
from pptx_extras import brand, chapter_num, css_sizes, cta_buttons  # noqa: E402
from pptx_free import svg_items, svg_pic  # noqa: E402
from pptx_mock import mock  # noqa: E402
from pptx_plus import FRAMES, ON_PANEL, frame_panels, leftover_text, plus, style_box  # noqa: E402
from pptx_text import Ctx, agenda, bullets, cols, highlight, para, runs, stacked, stats, takeaway, timeline, title  # noqa: E402
from pptx_anim import annotate  # noqa: E402
from pptx_fonts import embed  # noqa: E402
import pptx_xml  # noqa: E402

COVER = {'kicker': 22, 'title': 92, 'subtitle': 34, 'meta': 24}
USED = {'title', 'bullets', 'highlight', 'cols', 'takeaway', 'stats', 'timeline', 'agenda-list', 'bignum', 'bento', 'process',
        'ctable', 'countdown', 'ba', 'ico-grid', 'mock', 'viz', 'frame-panel', 'photo-bg', 'split-img', 'photo-credit'}


OVER = ['title', 'kicker', 'subtitle', 'meta', 'stat-num', 'stat-label', 'hl-text', 'hl-big', 'num', 'quote', 'cite', 'when', 'takeaway', 'statement']


def pad_box(sheet, sstate, tok, pad, align):
    """Text column of a display slide from the style's own padding / text-align on that slide."""
    d = sheet.slide_rule(sstate)
    if d.get('padding'):
        v = [px(p) for p in resolve(d['padding'], [tok]).split()]
        if v:   # CSS shorthand: 1 to 4 values, top right bottom left
            pad = (v * 4)[:4] if len(v) == 1 else (v * 2)[:4] if len(v) == 2 else [v[0], v[1], v[2], v[1]] if len(v) == 3 else v[:4]
    ta = resolve(d.get('text-align', ''), [tok])
    align = {'left': 'l', 'center': 'ctr', 'right': 'r', 'start': 'l'}.get(ta, align)
    top, bottom = max(pad[0], 60), max(pad[2], 60)
    return pad[3], top, 1920 - pad[3] - pad[1], 1080 - top - bottom, align


def build(sl, sheet, base):
    bg, items, timing, images = build_items(sl, sheet, base)
    annotate(items, sl['node'])   # entrance effects, order and click steps from the HTML
    tok = sheet.tokens(sl['state'])
    paper = background_svg(tok, tok, 1920, 1080)   # the stage's own paper: grid, dots, grain stripes
    if paper:
        items.insert(0, {'name': 'Paper', 'x': 0, 'y': 0, 'w': 1920, 'h': 1080, 'svg': paper})
    svg_items(items, images)
    return bg, items, timing, images


def build_items(sl, sheet, base):
    tok = sheet.tokens(sl['state'])
    t = theme(tok)
    sstate = dict(sl['state'], layout=sl['layout'], frame=sl['frame'], title=sl['title_mode'], density=sl['density'])
    over = {}
    for c in OVER:
        v = sheet.slide_rule(sstate, c).get('color')
        col = color(resolve(v, [tok])) if v and not (c == 'title' and sl['frame']) else None
        if col:
            over[c] = col
    ctx, node, images = Ctx(t, sl['density'], over), sl['node'], {}
    ctx.sheet, ctx.tok = sheet, tok   # deck CSS for free-placed blocks (pptx_free)
    names = resolve(tok.get('--actors', ''), [tok]).replace('"', '').replace("'", '').split()
    ctx.items += [actor_shape(n, sheet.actor(n, sl['state']), tok) for n in names]
    lay, kind, frame = sl['layout'], sl['kind'], sl['frame']
    if lay == 'photo':
        img = node.by_class('photo-bg')
        rid = image(img, base, images) if img else None
        if rid:
            ctx.items.append({'name': 'Photo', 'image': True, 'rid': rid, 'x': 0, 'y': 0, 'w': 1920, 'h': 1080})
        ctx.rect('Veil', 0, 0, 1920, 1080, ('000000', 0.55))
        ctx.t, ctx.over = dict(t, fg=('FFFFFF', 1), muted=('E5E7EB', 1), accent=('FFFFFF', 1)), {}   # white on the veil
        stacked(ctx, sl, 120, 300, 1400, 700, 'l', {'kicker': 22, 'title': 96, 'subtitle': 34}, 'b')
    elif lay in ('cover', 'closing'):
        x, y, w, h, al = pad_box(sheet, sstate, tok, [100, 300, 100, 300], 'ctr')
        stacked(ctx, sl, x, y, w, h, al, css_sizes(ctx, sheet, sstate, tok, dict(COVER, title=120 if lay == 'closing' else 92)))
        cta_buttons(ctx, node, x, y, w, h, al)
    elif lay == 'section':
        x, y, w, h, al = pad_box(sheet, sstate, tok, [100, 900, 100, 160], 'l')
        stacked(ctx, sl, x, y, w, h, al, css_sizes(ctx, sheet, sstate, tok, {'num': 220, 'title': 84, 'subtitle': 34, 'kicker': 22}))
        chapter_num(ctx, node, sheet, sstate, tok, len(names))
    elif lay == 'quote':
        x, y, w, h, al = pad_box(sheet, sstate, tok, [100, 280, 100, 280], 'l')
        stacked(ctx, sl, x, y, w, h, al, css_sizes(ctx, sheet, sstate, tok, {'quote': 64, 'statement': 78, 'title': 72, 'cite': 28,
                                                                              'kicker': 22, 'subtitle': 34, 'qa-label': 22, 'qa-q': 72, 'qa-a': 34}))
    else:
        fl, fr, ft, fb = FRAMES[frame][0] if frame in FRAMES else (120, 120, 270, 90)
        if sl['title_mode'] == 'side' and not frame:
            fl, ft = 230, 110
        box = (fl, 1920 - fr, ft, 1080 - fb)
        if frame in FRAMES:
            frame_panels(ctx, frame)
        title(ctx, sl, FRAMES[frame][1] if frame in FRAMES and FRAMES[frame][1] else None, '' if frame else sl['title_mode'])
        if frame == 'frame' and ctx.items and ctx.items[-1].get('paras'):   # the title sits on the border, page colour behind it
            tt = ctx.items[-1]
            tt.update(fill=t['bg'], w=min(tt['w'], sum(len(r['text']) for r in tt['paras'][0]['runs']) * tt['paras'][0]['runs'][0]['size'] * 0.5 + 60), inset=14)
        if kind == 'split-photo':   # picture on one half, a stacked text column on the other
            img, flip = node.by_class('split-img'), 'flip' in node.cls
            rid = image(img, base, images) if img else None
            if rid:
                ctx.items.append({'name': 'Photo', 'image': True, 'rid': rid, 'x': 960 if flip else 0, 'y': 0, 'w': 960, 'h': 1080})
            st = node.by_class('split-text')
            if st:
                stacked(ctx, {'node': st}, 120 if flip else 1060, 100, 740, 440, 'l', {'kicker': 22, 'title': 64, 'subtitle': 30}, 'b')
                lis = st.by_class('bullets')
                if lis:
                    bullets(ctx, lis, 120 if flip else 1060, 560, 740, 400)
            credit = node.by_class('photo-credit')
            if credit:
                ctx.box('Credit', 120, 1030, 1680, 36, [para(runs(ctx, credit, 18, 'muted'))], 'ctr')
            return t['bg'], ctx.items, '', images
        hl = node.by_class('highlight')
        hl_box = FRAMES[frame][3] if frame in FRAMES and FRAMES[frame][3] else (1260, ft, 540, 1080 - fb - ft)
        x0, x1, y0, y1 = box
        if hl:
            if frame == 'magazine':   # pull quote: a short accent rule over left-set italic words
                ctx.rect('Quote rule', hl_box[0], hl_box[1] + hl_box[3] / 2 - 120, 120, 8, (t['accent'][0], 1))
            highlight(ctx, hl, *hl_box, on_panel=frame in ON_PANEL, big_cap=280 if (frame or '').startswith('media') else 160,
                      align='l' if frame == 'magazine' else 'ctr')
            if hl_box[0] > x0 and hl_box[1] < y1 - 100:
                x1 = min(x1, hl_box[0] - 40)
        if node.by_class('bullets') and not plus(ctx, sl, box):
            ul = node.by_class('bullets')
            bx, by, bw, bh = style_box(ul) or (x0, y0, x1 - x0, y1 - y0)   # a list placed inline (next to a UI mock) keeps its spot
            bullets(ctx, ul, bx, by, bw, bh, frame=frame)
        elif node.by_class('cols'):
            tk = node.by_class('takeaway')
            cols(ctx, node, x0, box[1], y0, y1 - (150 if tk else 0))
            if tk:
                takeaway(ctx, tk, x0, box[1], y1)
        elif node.by_class('stats'):
            stats(ctx, node, x0, box[1], y0, y1)
        elif node.by_class('timeline'):
            timeline(ctx, node, x0, box[1], y0, y1)
        elif node.by_class('agenda-list'):
            agenda(ctx, node.by_class('agenda-list'), x0, box[1], y0, y1)
        else:
            plus(ctx, sl, box)
        if True:   # UI mocks and drawn diagrams sit next to any body
            for m in node.all_class('mock'):
                if 'mock' in m.cls and not (m.parent and 'mock' in m.parent.cls):
                    mock(ctx, m, *(style_box(m) or (1000, 250, 800, 740)))
            for v in node.all_class('viz'):
                labels = [s for k in ('labels', 'stages', 'nodes', 'items') for s in v.attrs.get('data-' + k, '').split('|') if s]
                xb = style_box(v) or (x0, y0, box[1] - x0, y1 - y0)
                ctx.box('Diagram', *xb, [para([ctx.run(s, 30)], 'l', 10, 110, '•') for s in labels] or [para([ctx.run('Sơ đồ: xem bản HTML', 26, 'muted')])],
                        'ctr', line=((t['accent'][0], 0.6), 2), geom=('roundRect', 3000), inset=40)
        leftover_text(ctx, node, [k for k in node.children() if set(k.cls) & USED or k.tag in ('h1', 'h2')], box)
    for k in node.children(lambda n: n.tag == 'svg'):   # hand-drawn plans, lines, roads, art of two-layer styles:
        svg_pic(ctx, k, images)                          # SVG pictures on every layout (cover, section, quote, closing too)
    credit = node.by_class('photo-credit')
    if credit:
        ctx.box('Credit', 120, 1030, 1680, 36, [para(runs(ctx, credit, 18, 'muted'))], 'ctr')
    ctx.caps = set()
    brand(ctx, node, sl['state'], tok)   # the stage logo, on top like z-index 30
    return t['bg'], ctx.items, '', images


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    root, base, css = load(src)
    sheet = Sheet(css)
    base_tok = sheet.tokens({'layout': 'cover'})
    dense = resolve(base_tok.get('--dense-stage', 'agenda'), [base_tok]).strip('"\' ') or 'agenda'
    sl = slides(root, dense)
    built = [build(s, sheet, base) for s in sl]
    t0 = theme(base_tok)
    title_node = root.find(lambda n: n.tag == 'title')
    used = sorted({r['font'] for b in built for it in b[1] for p in it.get('paras') or [] for r in p['runs']})
    fonts = embed(css, used)   # the style's Google Fonts travel inside the file
    pptx_xml.write(out, built, title_node.text() if title_node else src.stem, (t0['font_display'], t0['font_body']), fonts)
    print(f'Wrote {out} ({len(built)} slides, Morph on every slide, {len(fonts[1])} embedded font files)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
