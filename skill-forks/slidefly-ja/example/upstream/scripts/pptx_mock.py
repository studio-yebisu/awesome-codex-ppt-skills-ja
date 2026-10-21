"""SlideFly -> PPTX: UI mocks (morph-mock.css) as real windows: rounded frame, title bar with three dots and the
window title, then one text box per block (command, output, message, code) so each block keeps its own entrance."""
import re

from pptx_css import color
from pptx_text import lines, para, runs

TERM = {'bg': ('0E1116', 1), 'bar': ('1A1F27', 1), 'line': ('FFFFFF', 0.12), 'fg': ('E6EDF3', 1), 'out': ('9BA7B4', 1), 'prompt': ('7EE787', 1)}
DOTS = (('FF5F57', 32), ('FEBC2E', 58), ('28C840', 84))


def _mix(a, b, pct):
    return color(f'color-mix(in srgb, #{a[0]} {pct}%, #{b[0]})')


def _blocks(m):
    """Top-level text blocks of a mock, unwrapping plain step wrappers (<div data-step> around commands)."""
    out = []
    for k in m.children():
        if k.tag in ('button', 'script', 'style') or 'cp' in k.cls or 'dots' in k.cls:
            continue
        if k.tag == 'div' and not k.cls and k.children():
            out += [c for c in k.children() if c.text()]
        elif k.text():
            out.append(k)
    return out


def mock(ctx, m, x, y, w, h):
    t = ctx.t
    term = 'mock-term' in m.cls
    pf = re.search(r'--pf:\s*(\d+)px', m.attrs.get('style', ''))
    size = int(pf.group(1)) if pf else (26 if term else 28)
    bg = TERM['bg'] if term else _mix(t['bg'], ('FFFFFF', 1), 82)
    bar = TERM['bar'] if term else _mix(t['fg'], bg, 8)
    line = TERM['line'] if term else (t['fg'][0], 0.16)
    ink, muted = (TERM['fg'], TERM['out']) if term else (t['fg'], t['muted'])
    ctx.rect('UI window', x, y, w, h, bg, ('roundRect', 4000), (line, 2))
    bar_title = m.attrs.get('data-title')
    if 'mock-phone' not in m.cls:
        ctx.rect('UI bar', x + 2, y + 2, w - 4, 58, bar, ('roundRect', 30000))
        ctx.rect('UI bar edge', x + 2, y + 40, w - 4, 20, bar)
        ctx.rect('UI bar line', x, y + 60, w, 2, line)
        for col, cx in DOTS:
            ctx.rect('UI dot', x + cx - 7, y + 23, 14, 14, (col, 1), 'ellipse')
        if bar_title:
            ctx.box('UI title', x + 110, y + 8, w - 220, 46, [para([ctx.run(bar_title, 20, muted, True)], 'ctr')], 'ctr')
    cy, inner = y + 92, w - 80
    for b in _blocks(m):
        mono = term or 'code' in b.cls or b.tag == 'code'
        font = 'mono' if mono else 'body'
        glyph = 0.6 if mono else 0.5
        text_lines = [ln for ln in b.text().split('\n')] or ['']
        if 'msg' in b.cls:   # chat bubble, user on the right, assistant on the left
            user = 'user' in b.cls
            longest = max(len(ln) for ln in text_lines) * size * glyph
            bw = min(inner * 0.84, longest + 56)
            nl = sum(max(1, lines(ln + '   ', size * 1.1 * glyph / 0.5, bw - 60)) for ln in text_lines)
            bh = nl * size * 1.55 + 52
            bx = x + 40 + (inner - bw if user else 0)
            fill = _mix(t['accent'], t['bg'], 22) if user else None
            ps = [para([ctx.run(ln or ' ', size, 'fg', False, font)], 'l', 0, 135) for ln in text_lines]
            ctx.box('Message', bx, cy, bw, bh, ps, 't', fill=fill, line=None if user else (line, 2), geom=('roundRect', 9000), inset=24)
        else:
            role = TERM['prompt'] if 'cmd' in b.cls else None
            col = muted if 'out' in b.cls else ink
            ps = []
            for ln in text_lines:
                rs = [ctx.run('$ ', size, role, False, font)] if role else []
                rs.append(ctx.run(ln or ' ', size, col, False, font))
                ps.append(para(rs, 'l', 0, 140))
            nl = sum(max(1, lines(ln + '  ', size * glyph / 0.5, inner)) for ln in text_lines)
            bh = nl * size * 1.5 + 8
            ctx.box('Code' if mono else 'Text', x + 40, cy, inner, bh, ps, 't')
        ctx.items[-1]['src'] = b
        cy += ctx.items[-1]['h'] + (22 if not term else 6)
        if cy > y + h - 30:
            break
