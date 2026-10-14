"""SlideFly -> PPTX: theme colours, actors as shapes, embedded pictures."""
import base64
import re

from pptx_bgsvg import background_svg
from pptx_css import color, px, resolve


def lum(hexv):
    c = [int(hexv[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def theme(tok):
    get = lambda k, d: color(resolve(tok.get(k, d), [tok])) or color(d)  # noqa: E731
    t = {'bg': get('--bg', '#ffffff'), 'fg': get('--fg', '#111111'), 'muted': get('--muted', '#666666'), 'accent': get('--accent', '#2563eb')}
    t['card'] = color(resolve(tok.get('--card-bg', 'transparent'), [tok]))
    if not t['card'] or t['card'][1] < 0.05:   # no card colour: a faint ink wash keeps cards visible
        t['card'] = color(f'color-mix(in srgb, #{t["fg"][0]} 7%, #{t["bg"][0]})')
    t['tint'] = color(f'color-mix(in srgb, #{t["accent"][0]} 14%, #{t["bg"][0]})')
    t['mark'] = color(f'color-mix(in srgb, #{t["accent"][0]} 45%, #{t["bg"][0]})')   # .statement mark
    a = lum(t['accent'][0])
    score = lambda c: (max(a, lum(c[0])) + 0.05) / (min(a, lum(c[0])) + 0.05)  # noqa: E731
    pal = [c for c in (t['bg'], t['fg']) if score(c) >= 4.5]
    t['on_accent'] = pal[0] if pal else max((t['bg'], t['fg'], ('FFFFFF', 1), ('111111', 1)), key=score)
    font = lambda k: re.split(r',', resolve(tok.get(k, 'Arial'), [tok]))[0].strip().strip('"\'') or 'Arial'  # noqa: E731
    t['font_display'], t['font_body'] = font('--font-display'), font('--font-body')
    t['font_mono'] = font('--font-mono') if '--font-mono' in tok else 'Consolas'
    t['bullet'] = '▪' if px(resolve(tok.get('--bullet-radius', '50%'), [tok]), 50) == 0 else '•'   # square markers when the style says so
    t['display_bold'] =px(resolve(tok.get('--title-weight', '800'), [tok]), 800) >= 600   # display type follows --title-weight
    return t


def actor_shape(name, decl, tok):
    g = lambda k, d='': resolve(decl.get(k, d), [decl, tok])  # noqa: E731
    x, y, w = px(g('--x', '-400'), -400), px(g('--y', '-400'), -400), px(g('--w', '200'), 200)
    h, r, s, o = px(g('--h', str(w)), w), px(g('--r', '0')), px(g('--s', '1'), 1), px(g('--o', '1'), 1)
    bw = px(g('--bw', '0'))
    # .actor has the default transform-origin (its centre), like PowerPoint: the centre stays put, the size scales
    cx, cy = x - bw / 2 + (w + bw) / 2, y - bw / 2 + (h + bw) / 2
    w, h = (w + bw) * s, (h + bw) * s
    bg = g('background') or g('background-color') or g('background-image')
    # patterns (grid lines, dot screens, stripes, stamps, masks) become an SVG picture with the same !!name
    svg = background_svg(decl, tok, w, h)
    if svg:
        return {'name': f'!!{name}', 'x': cx - w / 2, 'y': cy - h / 2, 'w': max(w, 0.2), 'h': max(h, 0.2), 'rot': r, 'svg': svg, 'alpha': o,
                'effects': effects(g('filter'), g('box-shadow'), o)}
    pattern = 'url(' in bg or 'transparent' in bg or 'repeating' in bg or bg.count('gradient(') > 1
    fill = None if pattern else color(bg)
    if fill:
        fill = (fill[0], fill[1] * o)
    line = None
    border = g('border')
    if border and border not in ('0', 'none'):
        lw = px(border, 2)
        lc = color(re.sub(r'^[\d.]+px\s+\w+\s*', '', border)) or color(g('border-color', '#000'))
        if lc and lw:
            line = ((lc[0], lc[1] * o), lw)
    rad_css = g('border-radius', g('--rad', ''))
    geom = 'rect'
    if '%' in rad_css and px(rad_css) >= 40:
        geom = 'ellipse'
    elif px(rad_css) > 0:
        geom = ('roundRect', min(50000, px(rad_css) / max(min(w, h), 1) * 100000))
    clip = re.search(r'polygon\(([^)]*)\)', g('clip-path'))
    if clip:
        pts = [tuple(px(v) / 100 for v in p.split()) for p in clip.group(1).split(',')]
        if all(len(p) == 2 for p in pts) and '%' in clip.group(1):
            geom = ('poly', pts)
    return {'name': f'!!{name}', 'x': cx - w / 2, 'y': cy - h / 2, 'w': max(w, 0.2), 'h': max(h, 0.2), 'rot': r,
            'geom': geom, 'fill': fill, 'line': line, 'effects': effects(g('filter'), g('box-shadow'), o)}


def effects(filt, shadow, o=1):
    """filter: blur() -> soft edges; the first box-shadow -> outer shadow (DrawingML effect list, px values)."""
    out = {}
    b = re.search(r'blur\(\s*([\d.]+)px', filt or '')
    if b and float(b.group(1)) > 0:
        out['soft'] = float(b.group(1)) * 1.6
    sh = (shadow or '').split(',')[0].strip()
    if sh and sh != 'none' and 'inset' not in sh:
        nums = [px(v) for v in re.findall(r'-?[\d.]+px|(?<![\w.])0(?![\w.])', re.sub(r'(rgba?|hsla?|color-mix)\([^)]*\)', '', sh))]
        c = color(re.search(r'(rgba?\([^)]*\)|#[0-9a-fA-F]{3,8})', sh).group(1)) if re.search(r'(rgba?\([^)]*\)|#[0-9a-fA-F]{3,8})', sh) else None
        if len(nums) >= 2 and c and c[1] > 0:
            x, y, bl = nums[0], nums[1], nums[2] if len(nums) > 2 else 0
            out['shadow'] = (x, y, bl, (c[0], c[1] * o))
    return out


def image(node, base, store):
    src = node.attrs.get('src', '')
    m = re.match(r'data:image/([\w+.-]+);base64,(.*)', src, re.S)
    if m:
        data, ext = base64.b64decode(m.group(2)), m.group(1).replace('jpeg', 'jpg').replace('svg+xml', 'svg')
    else:
        f = base / src
        if not f.exists():
            return None
        data, ext = f.read_bytes(), f.suffix.lstrip('.').lower()
    rid = f'rId{len(store) + 2}'
    store[rid] = (f'img{abs(hash(src)) % 10**8}_{len(store)}.{ext}', data)
    return rid
