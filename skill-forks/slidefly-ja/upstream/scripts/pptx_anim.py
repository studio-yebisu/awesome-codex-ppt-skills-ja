"""SlideFly -> PPTX: entrance animations that follow the HTML deck.

Each text box is traced back to the DOM element it came from (by its text). That element (or its closest
ancestor) tells the effect: reveal = rise, reveal-left/right = slide in, reveal-scale/fx-pop = zoom, type = letters
appear one by one, draw = wipe; its data-step puts it on a click (like the arrow key in the HTML deck); --i / --d
give the order and delay. Boxes with several paragraphs (bullets, lists) animate paragraph by paragraph.
"""
import re

KIND = {'reveal': 'rise', 'reveal-left': 'left', 'reveal-right': 'right', 'reveal-scale': 'zoom', 'reveal-blur': 'fade',
        'fx-up': 'rise', 'fx-down': 'drop', 'fx-right': 'left', 'fx-left': 'right', 'fx-pop': 'zoom', 'fx-fade': 'fade',
        'slam': 'slam', 'type': 'type', 'draw': 'wipe'}
REVEALS = ('reveal', 'reveal-left', 'reveal-right', 'reveal-scale', 'reveal-blur')
DUR = {'fade': 500, 'rise': 600, 'drop': 600, 'left': 600, 'right': 600, 'zoom': 500, 'slam': 350, 'wipe': 900, 'type': 500}
PRESET = {'fade': (10, 0), 'rise': (42, 0), 'drop': (42, 0), 'left': (42, 0), 'right': (42, 0), 'zoom': (53, 16), 'slam': (53, 16),
          'wipe': (22, 8), 'type': (10, 0)}
MOVE = {'rise': ('ppt_y', '#ppt_y+0.03'), 'drop': ('ppt_y', '#ppt_y-0.03'), 'left': ('ppt_x', '#ppt_x-0.03'), 'right': ('ppt_x', '#ppt_x+0.03')}


def _norm(s):
    return re.sub(r'\s+', '', s or '')


def _walk(node):
    for k in node.kids:
        if not isinstance(k, str):
            yield k
            yield from _walk(k)


def _fx(node, slide, order):
    """Closest animated ancestor -> dict kind, step, delay (ms)."""
    kind, step, delay, n, anchor = None, 0, None, node, None
    while n is not None and n is not slide:
        cls = set(n.cls)
        if kind is None:
            hit = next((KIND[c] for c in ('type', 'draw', 'slam', 'fx-pop', 'fx-up', 'fx-down', 'fx-right', 'fx-left', 'fx-fade') + REVEALS if c in cls), None)
            if hit:
                kind, anchor = hit, id(n)
                st = n.attrs.get('style', '')
                d = re.search(r'--d:\s*(-?[\d.]+)', st)
                i = re.search(r'--i:\s*(\d+)', st)
                delay = float(d.group(1)) * 1000 if d else (int(i.group(1)) if i else order.get(id(n), 0)) * 110
        if not step and n.attrs.get('data-step', '').isdigit():
            step = int(n.attrs['data-step'])
        n = n.parent
    return {'kind': kind or 'fade', 'step': step, 'delay': delay or 0, 'anchor': anchor}


def _inside(n, top):
    while n is not None:
        if n is top:
            return True
        n = n.parent
    return False


def annotate(items, slide):
    """Give every animated item its effects: it['fx'] = [(paragraph index | None, info)]."""
    order = {id(n): i for i, n in enumerate(n for n in _walk(slide) if set(n.cls) & set(REVEALS))}
    texts = [(_norm(n.text()), n) for n in _walk(slide) if n.tag not in ('script', 'style')]
    texts = [(t, n) for t, n in texts if t]

    def find(t, pool):
        for cand in (t, re.sub(r'^\d+', '', t)):   # "01 Ý" of a numbered frame: the number is drawn, not in the HTML
            exact = [n for s, n in pool if s == cand]
            if exact:
                return exact[-1]   # deepest element with exactly this text
            inside = [(len(s), n) for s, n in pool if cand and cand in s]
            if inside:
                return min(inside, key=lambda x: x[0])[1]
        return None

    for it in items:
        if not it.get('anim'):
            continue
        paras = it.get('paras') or []
        src = it.get('src')   # set by builders that know their element (UI mocks)
        if src is not None:
            it['fx'] = [(None, _fx(src, slide, order))]
            if it['fx'][0][1]['kind'] == 'type':
                it['chars'] = sum(len(r['text']) for p in paras for r in p['runs'])
            continue
        pool = [(t, n) for t, n in texts if src is None or n is src or _inside(n, src)]
        found = [find(_norm(''.join(r['text'] for r in p['runs'])), pool) for p in paras]
        infos = [_fx(n, slide, order) if n is not None else None for n in found]
        known = [x for x in infos if x]
        if not known:
            it['fx'] = [(None, {'kind': 'fade', 'step': 0, 'delay': 0})]
        elif len(paras) > 1 and len({x['anchor'] for x in known}) > 1:
            it['fx'] = [(i, x or known[0]) for i, x in enumerate(infos)]
        else:
            it['fx'] = [(None, known[0])]
        if known and known[0]['kind'] == 'type':
            it['chars'] = sum(len(r['text']) for p in paras for r in p['runs'])


class _Ids:
    def __init__(self):
        self.n = 3

    def __call__(self):
        self.n += 1
        return self.n


def _bhvr(ids, tgt, attr, frm, to, dur):
    return (f'<p:anim calcmode="lin" valueType="num"><p:cBhvr><p:cTn id="{ids()}" dur="{dur}" fill="hold"/>{tgt}'
            f'<p:attrNameLst><p:attrName>{attr}</p:attrName></p:attrNameLst></p:cBhvr><p:tavLst>'
            f'<p:tav tm="0"><p:val><p:strVal val="{frm}"/></p:val></p:tav><p:tav tm="100000"><p:val><p:strVal val="{to}"/></p:val></p:tav></p:tavLst></p:anim>')


def _effect(ids, spid, prg, info, node_type, chars):
    kind, (pid, sub) = info['kind'], PRESET[info['kind']]
    dur = DUR[kind]
    tgt = (f'<p:tgtEl><p:spTgt spid="{spid}">' + (f'<p:txEl><p:pRg st="{prg}" end="{prg}"/></p:txEl>' if prg is not None else '')
           + '</p:spTgt></p:tgtEl>')
    body = (f'<p:set><p:cBhvr><p:cTn id="{ids()}" dur="1" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn>{tgt}'
            '<p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set>')
    filt = 'wipe(left)' if kind == 'wipe' else 'fade'
    body += f'<p:animEffect transition="in" filter="{filt}"><p:cBhvr><p:cTn id="{ids()}" dur="{dur}"/>{tgt}</p:cBhvr></p:animEffect>'
    if kind in MOVE:
        attr, frm = MOVE[kind]
        body += _bhvr(ids, tgt, attr, frm, '#' + attr, dur)
    if kind in ('zoom', 'slam'):
        f = '0.85' if kind == 'zoom' else '1.4'
        body += _bhvr(ids, tgt, 'ppt_w', f'#ppt_w*{f}', '#ppt_w', dur) + _bhvr(ids, tgt, 'ppt_h', f'#ppt_h*{f}', '#ppt_h', dur)
    it = f'<p:iterate type="lt"><p:tmAbs val="{max(8, min(40, 2500 // max(chars, 1)))}"/></p:iterate>' if kind == 'type' else ''
    return (f'<p:par><p:cTn id="{ids()}" presetID="{pid}" presetClass="entr" presetSubtype="{sub}" fill="hold" grpId="0" nodeType="{node_type}">'
            f'<p:stCondLst><p:cond delay="{int(info["delay"])}"/></p:stCondLst>{it}<p:childTnLst>{body}</p:childTnLst></p:cTn></p:par>')


def timing(items):
    """p:timing for items carrying 'fx' (spid = list index + 2): step 0 plays after the slide arrives, steps 1.. on clicks."""
    groups, builds = {}, {}
    for i, it in enumerate(items):
        for prg, info in it.get('fx') or []:
            groups.setdefault(info['step'], []).append((info['delay'], i, prg, info, it.get('chars', 0)))
            if it.get('paras') is not None:
                builds[i + 2] = 'p' if prg is not None else builds.get(i + 2, 'whole')
    if not groups:
        return ''
    ids, seq = _Ids(), ''
    for step in sorted(groups):
        effs = sorted(groups[step], key=lambda g: (g[0], g[1], g[2] or 0))
        base, outer, mid = effs[0][0], ids(), ids()
        inner =''.join(_effect(ids, i + 2, prg, dict(info, delay=d - base if step else d),
                                ('clickEffect' if step else 'afterEffect') if k == 0 else 'withEffect', ch)
                        for k, (d, i, prg, info, ch) in enumerate(effs))
        cond = ('<p:cond delay="indefinite"/><p:cond evt="onBegin" delay="0"><p:tn val="2"/></p:cond>' if not step
                else '<p:cond delay="indefinite"/>')
        seq += (f'<p:par><p:cTn id="{outer}" fill="hold"><p:stCondLst>{cond}</p:stCondLst><p:childTnLst>'
                f'<p:par><p:cTn id="{mid}" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>{inner}'
                '</p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par>')
    bld = ''.join(f'<p:bldP spid="{s}" grpId="0" build="p"/>' if b == 'p' else f'<p:bldP spid="{s}" grpId="0" animBg="1"/>' for s, b in builds.items())
    return ('<p:timing><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot"><p:childTnLst>'
            f'<p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst>{seq}</p:childTnLst></p:cTn>'
            '<p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst>'
            '<p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst></p:seq>'
            f'</p:childTnLst></p:cTn></p:par></p:tnLst><p:bldLst>{bld}</p:bldLst></p:timing>')
