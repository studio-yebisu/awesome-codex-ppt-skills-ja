"""SlideFly -> PPTX: read a deck's HTML (standard library only).

Builds a tiny DOM, lists the slides, and replays what morph-engine.js / morph-frames.js decide
for each slide before it is shown: classic layout of the new kinds, the actor pose (stage),
parity and variant. Keep in sync with assets/morph-engine.js.
"""
import re
from html.parser import HTMLParser
from pathlib import Path

CLASSIC_OF = {'qa': 'quote', 'portrait-quote': 'quote', 'statement': 'quote', 'chapter': 'section', 'cta': 'cover',
              'big-number': 'diagram', 'split-photo': 'diagram', 'bento': 'diagram', 'process': 'diagram',
              'before-after': 'diagram', 'compare-table': 'diagram', 'countdown': 'diagram', 'free': 'diagram'}
PANEL_FRAMES = {'split-left', 'split-right', 'poster', 'band', 'rail', 'bottom', 'stack', 'corner', 'diagonal', 'frame',
                'media-left', 'media-right', 'magazine', 'spotlight', 'stairs'}   # stairs: no panel, but a clear stage
VOID = {'br', 'img', 'meta', 'link', 'input', 'hr', 'source', 'col', 'wbr'}


class Node:
    def __init__(self, tag, attrs, parent=None):
        self.tag, self.attrs, self.parent, self.kids = tag, dict(attrs), parent, []

    @property
    def cls(self):
        return (self.attrs.get('class') or '').split()

    def text(self):
        """Visible text, <br> as newline, whitespace collapsed per line."""
        parts = []
        for k in self.kids:
            if isinstance(k, str):
                parts.append(k)
            elif k.tag == 'br':
                parts.append('\n')
            elif k.tag not in ('script', 'style', 'svg', 'button'):
                parts.append(k.text())
        return '\n'.join(re.sub(r'\s+', ' ', line).strip() for line in ''.join(parts).split('\n')).strip()

    def find_all(self, pred):
        for k in self.kids:
            if isinstance(k, Node):
                if pred(k):
                    yield k
                yield from k.find_all(pred)

    def find(self, pred):
        return next(self.find_all(pred), None)

    def by_class(self, name):
        return self.find(lambda n: name in n.cls)

    def all_class(self, name):
        return list(self.find_all(lambda n: name in n.cls))

    def children(self, pred=lambda n: True):
        return [k for k in self.kids if isinstance(k, Node) and pred(k)]


class Builder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node('root', {})
        self.cur = self.root

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs, self.cur)
        self.cur.kids.append(node)
        if tag not in VOID:
            self.cur = node

    def handle_endtag(self, tag):
        n = self.cur
        while n is not self.root and n.tag != tag:
            n = n.parent
        if n is not self.root:
            self.cur = n.parent

    def handle_data(self, data):
        self.cur.kids.append(data)


def load(path):
    """-> (root node, deck dir, css texts linked or inlined in <head>)."""
    path = Path(path)
    b = Builder()
    b.feed(path.read_text(encoding='utf-8'))
    css = []
    for n in b.root.find_all(lambda n: n.tag in ('link', 'style')):
        if n.tag == 'style':
            css.append(''.join(k for k in n.kids if isinstance(k, str)))
        elif 'stylesheet' in (n.attrs.get('rel') or '') and not n.attrs.get('href', '').startswith('http'):
            href = n.attrs['href'].replace('file:///', '')
            f = Path(href) if Path(href).is_absolute() else path.parent / href
            if f.exists():
                css.append(f.read_text(encoding='utf-8'))
    return b.root, path.parent, css


def density(slide):
    """Same item count -> lg/md/sm as morph-engine.js densityOf()."""
    cols = slide.all_class('col')
    if cols:
        n = max(len(list(c.find_all(lambda x: x.tag in ('li', 'p')))) for c in cols)
    else:
        n = sum(len(x.children(lambda c: c.tag == 'li' or 'stat' in c.cls or 'step' in c.cls))
                for x in slide.find_all(lambda x: set(x.cls) & {'bullets', 'agenda-list', 'stats', 'timeline'}))
    lg, md = (4, 6) if slide.find(lambda x: set(x.cls) & {'agenda-list', 'timeline', 'stats'}) else (3, 5)
    return 'lg' if n <= lg else 'md' if n <= md else 'sm'


def slides(root, dense_stage='agenda'):
    """-> list of dicts: node, layout (classic), kind, stage state for the actors."""
    stage = root.find(lambda n: 'deck-stage' in n.cls)
    out, seen = [], {}
    for k, s in enumerate(stage.children(lambda n: n.tag == 'section' and 'slide' in n.cls)):
        own = s.attrs.get('data-layout', 'content')
        layout = CLASSIC_OF.get(own, own)
        kind = own if own in CLASSIC_OF else layout
        frame = s.attrs.get('data-frame', '')
        st = s.attrs.get('data-stage') or ('clear' if frame in PANEL_FRAMES or own == 'free' else '')
        pose_layout = 'diagram' if st == 'clear' else st or (dense_stage if layout == 'diagram' else layout)
        side = s.attrs.get('data-title') == 'side'
        parity = 'even' if k % 2 and not side and not frame else 'odd'
        seen[layout] = seen.get(layout, 0) + 1
        variant = s.attrs.get('data-variant') or str((seen[layout] - 1) % 3 + 1)
        pose = s.attrs.get('data-pose', '')
        state = {'layout': pose_layout, 'kind': kind, 'parity': 'none' if pose else parity,
                 'variant': variant, 'pose': pose, 'slide': str(k + 1), 'brand': s.attrs.get('data-brand', '')}
        out.append({'node': s, 'layout': layout, 'kind': kind, 'frame': frame, 'title_mode': s.attrs.get('data-title', ''),
                    'density': s.attrs.get('data-density') or density(s), 'state': state})
    return out
