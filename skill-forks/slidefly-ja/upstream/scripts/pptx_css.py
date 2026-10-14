"""SlideFly -> PPTX: a small CSS cascade for actor poses and theme tokens (standard library only).

A style file says where each actor stands for each stage state:
  [data-layout="cover"] [data-actor="ring"] { --x: 120px; ... }
  .deck-stage[data-layout="stats"] { --fg: #fff; }
`Sheet.actor(name, state)` and `Sheet.tokens(state)` replay the cascade for one stage state
(layout, parity, variant, pose, kind). Rules that depend on the slide's content (`:has(...)`)
are skipped: the actor keeps its plain pose for that layout.
"""
import re

ATTR = re.compile(r'\[data-([a-z-]+)(?:="([^"]*)")?\]')
SKIP = re.compile(r':has\(|:where\(|::|:hover|:focus|@')


def first_url(text):
    """The first complete `url(...)` token, honouring quotes and nested parentheses inside an SVG data URI
    (`url(#g)`, `rotate(30)`), or None."""
    i = text.find('url(')
    if i < 0:
        return None
    depth, quote = 0, ''
    for j in range(i + 3, len(text)):
        ch = text[j]
        if quote:
            quote = '' if ch == quote else quote
        elif ch in '"\'':
            quote = ch
        elif ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1
            if depth == 0:
                return text[i:j + 1]
    return None


def split_top(text, sep=','):
    """Split on `sep` outside parentheses and quotes."""
    out, depth, cur, quote = [], 0, '', ''
    for ch in text:
        if quote:
            quote = '' if ch == quote else quote
            cur += ch
            continue
        if ch in '"\'':
            quote = ch
        depth += ch == '('
        depth -= ch == ')'
        if ch == sep and depth == 0:
            out.append(cur)
            cur = ''
        else:
            cur += ch
    out.append(cur)
    return [s.strip() for s in out if s.strip()]


def expand_is(sel):
    """`.a:is(X, Y) .b` -> ['.a X .b', '.a Y .b'] (attribute-only alternatives in practice)."""
    m = re.search(r':is\(', sel)
    if not m:
        return [sel]
    depth, i = 1, m.end()
    while depth:
        depth += {'(': 1, ')': -1}.get(sel[i], 0)
        i += 1
    alts = split_top(sel[m.end():i - 1])
    return [s for a in alts for s in expand_is(sel[:m.start()] + a + sel[i:])]


def parse(css):
    """-> list of (selector, specificity, order, {prop: value})."""
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    # @import url(...) may hold ';' inside the URL (Google Fonts "wght@400;500"): drop the url() first
    css = re.sub(r'@import\s+url\([^)]*\)[^;]*;', '', css)
    css = re.sub(r'@(?:import|charset)\s+["\'][^"\']*["\'][^;]*;', '', css)
    rules, order = [], 0
    # drop @media / @keyframes blocks (one nesting level)
    css = re.sub(r'@[a-z-]+[^{]*\{(?:[^{}]*\{[^{}]*\})*[^{}]*\}', '', css)
    for sels, body in re.findall(r'([^{}]+)\{([^{}]*)\}', css):
        decl = {}
        for part in split_top(body, ';'):
            if ':' in part:
                k, v = part.split(':', 1)
                decl[k.strip()] = v.replace('!important', '').strip()
        for sel in split_top(sels):
            for s in expand_is(sel):
                order += 1
                spec = len(ATTR.findall(s)) + s.count('.') + s.count(':not(')
                rules.append((s, spec, order, decl))
    return rules


def matches_stage(sel, state):
    """True if every stage condition in the selector holds for this state."""
    if SKIP.search(sel):
        return False
    for neg in re.findall(r':not\(([^()]*)\)', sel):
        tests = ATTR.findall(neg)
        if tests and all(state.get(k) == v for k, v in tests):
            return False
    plain = re.sub(r':not\([^()]*\)', '', sel)
    for key, val in ATTR.findall(plain):
        if key == 'actor':
            continue
        have = state.get(key, '')
        if (val and have != val) or (not val and not have):
            return False
    return True


class Sheet:
    def __init__(self, css_texts):
        # Source order runs across files in document order, as in the browser: the deck's own <style>
        # (loaded last) beats a style file rule of the same specificity.
        self.rules = [(s, spec, i * 1_000_000 + o, d) for i, t in enumerate(css_texts) for s, spec, o, d in parse(t)]

    def _cascade(self, wanted, state):
        out = {}
        for sel, spec, order, decl in sorted((r for r in self.rules if wanted(r[0])), key=lambda r: (r[1], r[2])):
            if matches_stage(sel, state):
                out.update(decl)
        return out

    def tokens(self, state):
        """Custom properties and theme values on .deck-stage for this state."""
        def stage_rule(sel):
            last = sel.split()[-1] if sel.split() else ''
            return (last.startswith('.deck-stage') or last.startswith(':root')) and 'data-actor' not in sel
        return self._cascade(stage_rule, state)

    def slide_rule(self, state, cls=None):
        """Declarations a style puts on the slide itself (cls None) or on `.cls` inside it, for this slide layout."""
        def wanted(sel):
            parts = sel.split()
            if not parts or 'data-actor' in sel:
                return False
            if cls is None:
                return parts[-1].startswith('.slide[') or parts[-1] == '.slide'
            # only `.deck-stage ... .slide[...] .cls`: an ancestor like `.photo-text` scopes the rule elsewhere
            scoped = all(p in ('>', '+', '~') or p.startswith(('.deck-stage', '.slide', ':root')) for p in parts[:-1])
            return scoped and bool(re.search(r'\.' + re.escape(cls) + r'(?![\w-])', parts[-1])) and len(re.findall(r'\.[\w-]+', parts[-1])) == 1
        return self._cascade(wanted, state)

    def actor(self, name, state):
        """Declarations that land on actor `name` in this state (its own default rule included)."""
        def actor_rule(sel):   # [data-actor="x"], and the group forms ^= $= *= and a bare [data-actor]
            last = sel.split()[-1] if sel.split() else ''
            m = re.search(r'\[data-actor(?:([\^$*~|]?)=["\']?([\w-]+)["\']?)?\]', last)
            if not m:
                return False
            op, v = m.group(1), m.group(2)
            return (v is None or (op == '' and name == v) or (op == '^' and name.startswith(v)) or (op == '$' and name.endswith(v))
                    or (op == '*' and v in name) or (op == '|' and (name == v or name.startswith(v + '-'))))
        return self._cascade(actor_rule, state)


def resolve(value, scopes, depth=0):
    """Expand var(--a, fallback) using the first scope that defines --a."""
    if depth > 12 or 'var(' not in value:
        return value

    def sub(m):
        inner = m.group(1)
        name, _, fb = inner.partition(',')
        for sc in scopes:
            if name.strip() in sc:
                return resolve(sc[name.strip()], scopes, depth + 1)
        return resolve(fb.strip(), scopes, depth + 1)
    prev = None
    while 'var(' in value and value != prev:
        prev = value
        value = re.sub(r'var\(((?:[^()]|\([^()]*\))*)\)', sub, value)
    return value


NAMED = {'white': 'FFFFFF', 'black': '000000', 'transparent': None, 'none': None, 'red': 'FF0000'}


def color(value):
    """CSS colour -> (RRGGBB, alpha) or None."""
    v = value.strip().lower()
    if v in NAMED:
        return (NAMED[v], 1.0) if NAMED[v] else None
    m = re.match(r'#([0-9a-f]{3,8})\b', v)
    if m:
        h = m.group(1)
        if len(h) in (3, 4):
            h = ''.join(c * 2 for c in h)
        return h[:6].upper(), (int(h[6:8], 16) / 255 if len(h) == 8 else 1.0)
    m = re.match(r'rgba?\(([^)]*)\)', v)
    if m:
        p = [float(x.strip().rstrip('%')) for x in re.split(r'[,\s/]+', m.group(1)) if x.strip()]
        return '%02X%02X%02X' % tuple(int(round(x)) for x in p[:3]), (p[3] if len(p) > 3 else 1.0)
    m = re.match(r'color-mix\(in srgb,\s*(.+)\)$', v)
    if m:
        a, b = split_top(m.group(1))
        pa = re.search(r'\s(\d+(?:\.\d+)?)%$', a)
        wa = float(pa.group(1)) / 100 if pa else 0.5
        ca, cb = color(re.sub(r'\s\d+(?:\.\d+)?%$', '', a)), color(re.sub(r'\s\d+(?:\.\d+)?%$', '', b))
        if not ca and not cb:
            return None
        ca, cb = ca or (cb[0], 0.0), cb or (ca[0], 0.0)
        mix = [int(int(ca[0][i:i + 2], 16) * wa + int(cb[0][i:i + 2], 16) * (1 - wa)) for i in (0, 2, 4)]
        return '%02X%02X%02X' % tuple(mix), ca[1] * wa + cb[1] * (1 - wa)
    m = re.search(r'gradient\((.*)\)', v)
    if m:   # first colour stop stands for the whole gradient
        for part in split_top(m.group(1)):
            c = color(part.split(' ')[0] if not part.startswith(('rgb', 'color-mix')) else re.match(r'[a-z-]+\([^)]*\)', part).group(0))
            if c:
                return c
    return None


def px(value, default=0.0):
    if value and 'calc(' in value:   # calc(960px - 720px / 2): px arithmetic only (vars already resolved)
        expr = re.sub(r'(\d)(px|deg)\b', r'\1', value.replace('calc', ''))
        if re.fullmatch(r'[\d\s.+\-*/()]+', expr):
            try:
                return float(eval(expr, {'__builtins__': {}}))   # noqa: S307 - digits and operators only
            except (SyntaxError, ZeroDivisionError):
                return default
    m = re.match(r'\s*(-?(?:\d+(?:\.\d+)?|\.\d+))', value or '')   # '12px', '-50%', '.4'
    return float(m.group(1)) if m else default
