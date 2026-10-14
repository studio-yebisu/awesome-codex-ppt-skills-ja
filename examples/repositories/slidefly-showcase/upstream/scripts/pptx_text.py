"""SlideFly -> PPTX: editable text boxes for the 9 classic layouts (geometry of assets/morph-layouts.css)."""
import math

SIZES = {'bullets': {'lg': (44, 52), 'md': (36, 40), 'sm': (30, 20)}, 'cols': {'lg': (52, 36), 'md': (46, 32), 'sm': (40, 28)},
         'stats': {'lg': (220, 36), 'md': (150, 30), 'sm': (110, 26)}, 'timeline': {'lg': (76, 50, 32), 'md': (64, 42, 29), 'sm': (50, 34, 25)},
         'agenda': {'lg': (120, 52, 30), 'md': (88, 40, 26), 'sm': (64, 32, 22)}}


class Ctx:
    """Theme and output list for one slide."""
    def __init__(self, theme, density, over=None):
        self.t, self.density, self.items = theme, density, []
        self.over = over or {}   # class -> colour the style gives that element on this slide

    def run(self, text, size, role='fg', bold=False, font='body', italic=False):
        bold = self.t.get('display_bold', True) if font == 'display' else bold   # the CSS weight of display type
        return {'text': text, 'size': size, 'color': self.t[role] if isinstance(role, str) else role, 'bold': bold,   # role: theme key or (hex, a)
                'italic': italic, 'font': self.t['font_' + font]}

    def box(self, name, x, y, w, h, paras, anchor='t', fill=None, geom='rect', line=None, rot=0, inset=0):
        # body text fades in after the slide arrives; titles and actors travel with Morph instead
        self.items.append({'name': name, 'x': x, 'y': y, 'w': w, 'h': h, 'paras': paras, 'anchor': anchor, 'fill': fill,
                           'geom': geom, 'line': line, 'rot': rot, 'inset': inset, 'anim': not name.startswith(('!!', 'Title', 'Credit', 'UI'))})

    def rect(self, name, x, y, w, h, fill, geom='rect', line=None):
        self.items.append({'name': name, 'x': x, 'y': y, 'w': w, 'h': h, 'fill': fill, 'geom': geom, 'line': line})

    def icon(self, node, x, y, size, role='accent'):
        __import__('pptx_icons').place(self, node, x, y, size, role)


def runs(ctx, node, size, role='fg', font='body', bold=False):
    """Inline runs of a node: <b>/<strong> bold, <em>/<i> italic, <br> newline (split later)."""
    out, hit, caps = [], next((c for c in node.cls if c in ctx.over), None), bool(set(node.cls) & getattr(ctx, 'caps', set()))
    role = ctx.over[hit] if hit else role

    def walk(n, b, it, mk):
        for k in n.kids:
            if isinstance(k, str):   # keep one space at each edge: "<b>Nêu việc:</b> tóm tắt" must not glue
                if k.strip() or (k and out):
                    txt = (' ' if k[:1].isspace() else '') + ' '.join(k.split()) + (' ' if k[-1:].isspace() and k.strip() else '')
                    out.append(dict(ctx.run(txt, size, role, b, font, it), mark=ctx.t.get('mark') if mk else None, caps=caps))
            elif k.tag == 'br':
                out.append(ctx.run('\n', size, role, b, font, it))
            elif k.tag not in ('svg', 'script', 'style', 'button') and 'ico' not in k.cls:
                walk(k, b or k.tag in ('b', 'strong'), it or k.tag in ('em', 'i'), mk or k.tag == 'mark')   # <mark>: highlighted run
    walk(node, bold, False, False)
    if out:
        out[0]['text'] = out[0]['text'].lstrip()
        out[-1]['text'] = out[-1]['text'].rstrip()
    return [r for r in out if r['text']]


def fit(node, size, width):
    """Shrink a one-line figure ("32 giây", "14-16%") until it fits its column (glyph ~0.58 em)."""
    n = max(len(node.text()), 1) if node else 1
    return min(size, width / (n * 0.58))


def para(rs, align='l', space=0, line=100, bullet=None):
    return {'runs': rs, 'align': align, 'space': space, 'line': line, 'bullet': bullet}


def lines(text, size, width):
    """Rough line count for a text in px (average glyph = 0.5 em)."""
    return max(1, math.ceil(len(text) * size * 0.5 / max(width, 1)))


def title(ctx, slide, frame_box=None, mode=''):
    """Inner-slide title: top-left by default, centred, side (rotated) or placed by a frame."""
    t = slide['node'].find(lambda n: 'title' in n.cls)
    if not t:
        return
    mid = t.attrs.get('data-morph-id')
    name = f'!!t-{mid}' if mid else 'Title'
    if frame_box:
        x, y, w, size, role = frame_box[:5]
        h = lines(t.text(), size, w) * size * 1.15 + 10
        ctx.box(name, x, y, w, h, [para(runs(ctx, t, size, role, 'display', True), frame_box[5] if len(frame_box) > 5 else 'l')], 'b' if y > 700 else 't')
    elif mode == 'side':
        ctx.box(name, 116 - 440, 550 - 45, 880, 90, [para(runs(ctx, t, 54, 'fg', 'display', True))], 'ctr', rot=270)
    else:
        ctx.box(name, 120, 90, 1680 if mode == 'center' else 1500, 150,
                [para(runs(ctx, t, 64, 'fg', 'display', True), 'ctr' if mode == 'center' else 'l')], 't')


def stacked(ctx, slide, x, y, w, h, align, sizes, anchor='ctr'):
    """Cover / closing / section / quote: kicker, numeral, title, subtitle, meta, quote, cite in one box."""
    node, ps = slide['node'], []
    order = [('kicker', 'accent', 'body'), ('num', 'accent', 'display'), ('ch-num', 'accent', 'display'), ('title', 'fg', 'display'),
             ('quote', 'fg', 'display'), ('statement', 'fg', 'display'), ('qa-label', 'accent', 'body'), ('qa-q', 'fg', 'display'),
             ('qa-a', 'muted', 'body'), ('subtitle', 'muted', 'body'), ('cite', 'muted', 'body'), ('pq-who', 'muted', 'body'), ('meta', 'muted', 'body')]
    for cls, role, font in order:
        for n in node.all_class(cls):
            if n.attrs.get('aria-hidden') == 'true' or 'cta-actions' in n.cls:   # drawn by pptx_extras
                continue
            ps.append(para(runs(ctx, n, sizes.get(cls, 30), role, font, font == 'display'), align, 16 if ps else 0))
    if ps:
        ctx.box('Text', x, y, w, h, ps, anchor)


def bullets(ctx, node, x, y, w, h, size_key='bullets', frame=''):
    items = node.children(lambda n: n.tag == 'li')
    fs, gap = SIZES[size_key][ctx.density][:2]
    if frame == 'zigzag':   # each point a card, even ones pushed right
        ch = min(140, (h - 26 * (len(items) - 1)) / max(len(items), 1))
        top = y + (h - len(items) * ch - 26 * (len(items) - 1)) / 2
        for i, li in enumerate(items):
            ctx.box(f'Point {i + 1}', x + (w * 0.26 if i % 2 else 0), top + i * (ch + 26), w * 0.74, ch,
                    [para(runs(ctx, li, fs * 0.8))], 'ctr', fill=ctx.t['tint'], geom=('roundRect', 12000), inset=26)
        return
    if frame == 'stairs':   # numbered cards stepping down and right
        n = len(items)
        ch = min(150, (h - 18 * (n - 1)) / max(n, 1))
        top = y + (h - n * ch - 18 * (n - 1)) / 2
        for i, li in enumerate(items):
            ctx.box(f'Step {i + 1}', x + w * min(i * 0.105, 0.42), top + i * (ch + 18), w * 0.6, ch,
                    [para([ctx.run(f'{i + 1}   ', fs * 1.3, 'accent', True, 'display')] + runs(ctx, li, fs))], 'ctr',
                    fill=ctx.t['tint'], geom=('roundRect', 8000), inset=26)
        return
    if frame == 'spotlight':   # a row of cards under the key sentence
        n, gap = len(items), 40
        cw = (w - gap * (n - 1)) / max(n, 1)
        for i, li in enumerate(items):
            ctx.box(f'Point {i + 1}', x + i * (cw + gap), y, cw, h, [para(runs(ctx, li, 36), 'ctr')], 'ctr',
                    fill=ctx.t['tint'], geom=('roundRect', 10000), inset=30)
        return
    if frame == 'magazine':   # two text columns
        cw = (w - 72) / 2
        for c, part in enumerate((items[0::2], items[1::2])):   # the CSS grid fills row by row
            ps = [para(runs(ctx, li, fs), 'l', gap if i else 0, 112, ctx.t.get('bullet', '•')) for i, li in enumerate(part)]
            if ps:
                ctx.box(f'Column {c + 1}', x + c * (cw + 72), y + h * 0.12, cw, h * 0.88, ps, 't')   # both columns start on the same line, like the CSS grid rows
        return
    if frame == 'numbered':   # big numbers instead of dots
        ps = [para([ctx.run(f'{i + 1:02d}   ', fs * 1.3, 'accent', True, 'display')] + runs(ctx, li, fs), 'l', gap if i else 0, 112)
              for i, li in enumerate(items)]
    else:
        ps = [para(runs(ctx, li, fs), 'l', gap if i else 0, 112, ctx.t.get('bullet', '•')) for i, li in enumerate(items)]
    ctx.box('Bullets', x, y, w, h, ps, 'ctr')


def highlight(ctx, node, x, y, w, h, on_panel=False, big_cap=160, align='ctr'):
    role = 'on_accent' if on_panel else 'accent'
    ps, keep = [], ctx.over
    ctx.over = {} if on_panel else keep   # the style's hl-big colour is usually the accent: invisible on an accent panel
    for n in node.find_all(lambda n: set(n.cls) & {'hl-big', 'hl-text'}):
        big = 'hl-big' in n.cls
        ps.append(para(runs(ctx, n, fit(n, big_cap, w) if big else 34, role if big else ('on_accent' if on_panel else 'fg'), 'display', True), align, 14 if ps else 0))
    ctx.over = keep
    ico = node.find(lambda n: 'ico' in n.cls)
    if ico:   # icon centred above the words
        size = min(200, w * 0.6)
        ctx.icon(ico, x + (w - size) / 2, y + h / 2 - size - 20, size, role)
        if ps:
            ctx.box('Highlight', x, y + h / 2, w, h / 2, ps, 't')
    elif ps:
        ctx.box('Highlight', x, y, w, h, ps, 'ctr')


def cols(ctx, node, x0, x1, y0, y1):
    cs = node.all_class('col')
    hs, fs = SIZES['cols'][ctx.density]
    w = (x1 - x0 - 64 * (len(cs) - 1)) / max(len(cs), 1)
    for i, c in enumerate(cs):
        ps = []
        h3 = c.find(lambda n: n.tag == 'h3')
        if h3:
            ps.append(para(runs(ctx, h3, hs, 'accent', 'display', True)))
        for li in c.find_all(lambda n: n.tag in ('li', 'p') and n.parent.tag != 'li'):
            ps.append(para(runs(ctx, li, fs), 'l', 18, 112, ctx.t.get('bullet', '•') if li.tag == 'li' else None))
        ctx.box(f'Col {i + 1}', x0 + i * (w + 64), y0, w, y1 - y0, ps, 't', fill=ctx.t['card'], geom=('roundRect', 6000), inset=48)


def takeaway(ctx, node, x0, x1, bottom):
    ctx.rect('Takeaway bar', x0, bottom - 110, 10, 110, (ctx.t['accent'][0], 1))
    ctx.box('Takeaway', x0 + 36, bottom - 110, x1 - x0 - 36, 110, [para(runs(ctx, node, 36, 'fg', 'display', True))], 'ctr')


def stats(ctx, node, x0, x1, y0, y1):
    ss = node.all_class('stat')
    num, lab = SIZES['stats'][ctx.density]
    num = 160 if len(ss) >= 4 and ctx.density == 'lg' else num
    w = (x1 - x0 - 48 * (len(ss) - 1)) / max(len(ss), 1)
    for i, s in enumerate(ss):
        ps = [para(runs(ctx, n, fit(n, num, w) if 'stat-num' in n.cls else lab, 'accent' if 'stat-num' in n.cls else 'muted',
                        'display' if 'stat-num' in n.cls else 'body', 'stat-num' in n.cls), 'ctr', 0 if 'stat-num' in n.cls else 22)
              for n in s.find_all(lambda n: set(n.cls) & {'stat-num', 'stat-label'})]
        ctx.box(f'Stat {i + 1}', x0 + i * (w + 48), y0, w, y1 - y0, ps, 'ctr')


def timeline(ctx, node, x0, x1, y0, y1):
    steps = node.all_class('step')
    when, h3s, fs = SIZES['timeline'][ctx.density]
    mid = (y0 + y1) / 2
    ctx.rect('Axis', x0, mid - 2, x1 - x0, 4, (ctx.t['accent'][0], 0.35))
    w = (x1 - x0 - 32 * (len(steps) - 1)) / max(len(steps), 1)
    for i, s in enumerate(steps):
        x = x0 + i * (w + 32)
        ctx.rect(f'Dot {i + 1}', x, mid - 16, 32, 32, (ctx.t['accent'][0], 1), 'ellipse')
        ps = []
        for n in s.find_all(lambda n: n.tag in ('h3', 'p') or 'when' in n.cls):
            size, role, font = {'when': (when, 'accent', 'display'), 'h3': (h3s, 'fg', 'display'), 'p': (fs, 'muted', 'body')}[key := 'when' if 'when' in n.cls else n.tag]
            ps.append(para(runs(ctx, n, size, role, font, key != 'p'), 'l', 8 if ps else 0))
        above = i % 2 == 0
        ctx.box(f'Step {i + 1}', x, y0 if above else mid + 52, w, mid - 52 - y0 if above else y1 - mid - 52, ps, 'b' if above else 't')


def agenda(ctx, node, x0, x1, y0, y1):
    items = node.children(lambda n: n.tag == 'li')
    rows = math.ceil(len(items) / 2) or 1
    num, h3s, ps_ = SIZES['agenda'][ctx.density]
    cw, rh = (x1 - x0 - 80) / 2, (y1 - y0) / rows
    for i, li in enumerate(items):
        c, r = (0, i) if i < rows else (1, i - rows)
        x, y = x0 + c * (cw + 80), y0 + r * rh
        if n := li.by_class('num'):
            ctx.box(f'Num {i + 1}', x, y, num * 1.4, rh, [para(runs(ctx, n, num, 'accent', 'display', True))], 'ctr')
        ps = [para(runs(ctx, k, h3s if k.tag == 'h3' else ps_, 'fg' if k.tag == 'h3' else 'muted', 'display' if k.tag == 'h3' else 'body', k.tag == 'h3'), 'l', 6)
              for k in li.find_all(lambda k: k.tag in ('h3', 'p'))]
        ctx.box(f'Item {i + 1}', x + num * 1.5, y, cw - num * 1.5, rh, ps, 'ctr')
