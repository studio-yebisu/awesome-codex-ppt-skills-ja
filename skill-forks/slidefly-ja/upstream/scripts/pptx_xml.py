"""SlideFly -> PPTX: write a minimal OpenXML package by hand (standard library only).

Units: the deck stage is 1920x1080 px; 1 px = 6350 EMU (12192000 / 1920), font px * 50 = hundredths of pt.
Every slide gets a Morph transition (PowerPoint 2019 / 365); older versions fall back to a fade.
"""
import math
import zipfile
from xml.sax.saxutils import escape

EMU = 6350
NS = ('xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
      'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
      'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"')
REL = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
PKG = 'http://schemas.openxmlformats.org/package/2006/relationships'
MORPH = ('<mc:AlternateContent xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006">'
         '<mc:Choice xmlns:p159="http://schemas.microsoft.com/office/powerpoint/2015/09/main" Requires="p159">'
         '<p:transition spd="slow">'
         '<p159:morph option="byObject"/></p:transition></mc:Choice>'
         '<mc:Fallback><p:transition spd="slow"><p:fade/></p:transition></mc:Fallback></mc:AlternateContent>')


SVG_EXT = ('<a:extLst><a:ext uri="{{96DAC541-7B7A-43D3-8B79-37D633B846F1}}">'
           '<asvg:svgBlip xmlns:asvg="http://schemas.microsoft.com/office/drawing/2016/SVG/main" r:embed="{}"/></a:ext></a:extLst>')


def e(v):
    return int(round(v * EMU))


def fill_xml(fill):
    """fill: None | (hex, alpha) | ('grad', [(hex, alpha, pos%)...], angle)."""
    if not fill:
        return '<a:noFill/>'
    if fill[0] == 'grad':
        stops = ''.join(f'<a:gs pos="{int(p * 1000)}"><a:srgbClr val="{h}"><a:alpha val="{int(a * 100000)}"/></a:srgbClr></a:gs>'
                        for h, a, p in fill[1])
        return f'<a:gradFill rotWithShape="1"><a:gsLst>{stops}</a:gsLst><a:lin ang="{int(fill[2] * 60000)}" scaled="0"/></a:gradFill>'
    h, a = fill
    return f'<a:solidFill><a:srgbClr val="{h}"><a:alpha val="{int(max(0, min(1, a)) * 100000)}"/></a:srgbClr></a:solidFill>'


def geom_xml(geom):
    """geom: 'rect' | 'ellipse' | ('roundRect', adj 0..50000) | ('poly', [(fx, fy) 0..1]) | ('raw', custGeom xml)."""
    if isinstance(geom, tuple) and geom[0] == 'raw':
        return geom[1]
    if isinstance(geom, tuple) and geom[0] == 'poly':
        pts = geom[1]
        path = f'<a:moveTo><a:pt x="{int(pts[0][0] * 100000)}" y="{int(pts[0][1] * 100000)}"/></a:moveTo>'
        path += ''.join(f'<a:lnTo><a:pt x="{int(x * 100000)}" y="{int(y * 100000)}"/></a:lnTo>' for x, y in pts[1:])
        return ('<a:custGeom><a:avLst/><a:gdLst/><a:ahLst/><a:cxnLst/><a:rect l="0" t="0" r="r" b="b"/>'
                f'<a:pathLst><a:path w="100000" h="100000">{path}<a:close/></a:path></a:pathLst></a:custGeom>')
    if isinstance(geom, tuple):
        return f'<a:prstGeom prst="roundRect"><a:avLst><a:gd name="adj" fmla="val {int(geom[1])}"/></a:avLst></a:prstGeom>'
    return f'<a:prstGeom prst="{geom}"><a:avLst/></a:prstGeom>'


def effects_xml(fx):
    """{'soft': px, 'shadow': (dx, dy, blur, (hex, alpha))} -> <a:effectLst> (blur reads as soft edges in PowerPoint)."""
    if not fx:
        return ''
    out = ''
    if fx.get('shadow'):
        dx, dy, bl, col = fx['shadow']
        ang = int((math.degrees(math.atan2(dy, dx)) % 360) * 60000)
        out += (f'<a:outerShdw blurRad="{e(bl)}" dist="{e(math.hypot(dx, dy))}" dir="{ang}" algn="ctr" rotWithShape="0">'
                f'<a:srgbClr val="{col[0]}"><a:alpha val="{int(max(0, min(1, col[1])) * 100000)}"/></a:srgbClr></a:outerShdw>')
    if fx.get('soft'):
        out += f'<a:softEdge rad="{e(fx["soft"])}"/>'
    return f'<a:effectLst>{out}</a:effectLst>'


def run_xml(r):
    """r: dict text, size(px), bold, italic, color(hex,alpha), font. A lone newline is a line break."""
    if r['text'] == '\n':
        return '<a:br/>'
    col = r.get('color') or ('000000', 1)
    b = ' b="1"' if r.get('bold') else ''
    i = (' i="1"' if r.get('italic') else '') + (' cap="all" spc="200"' if r.get('caps') else '')   # text-transform: uppercase
    font = escape(r.get('font') or 'Arial', {'"': '&quot;'})
    ln = f'<a:ln w="{e(r["outline"][1])}">{fill_xml(r["outline"][0])}</a:ln>' if r.get('outline') else ''   # -webkit-text-stroke
    hl = f'<a:highlight><a:srgbClr val="{r["mark"][0]}"/></a:highlight>' if r.get('mark') else ''   # <mark>
    return (f'<a:r><a:rPr lang="vi-VN" sz="{int(r.get("size", 32) * 50)}"{b}{i} dirty="0">{ln}{fill_xml(None if r.get("outline") else col)}{hl}'
            f'<a:latin typeface="{font}"/><a:cs typeface="{font}"/></a:rPr><a:t>{escape(r["text"])}</a:t></a:r>')


def text_xml(paras, anchor='t', inset=0):
    """paras: list of dicts: runs, align(l|ctr|r), space(px before), line(spacing %), bullet(char)."""
    body = ''
    for p in paras:
        algn = p.get('align', 'l')
        sp = f'<a:spcBef><a:spcPts val="{int(p.get("space", 0) * 50)}"/></a:spcBef>' if p.get('space') else ''
        ln = (f'<a:lnSpc><a:spcPts val="{int(p["exact"] * 50)}"/></a:lnSpc>' if p.get('exact')   # CSS line-height in px
              else f'<a:lnSpc><a:spcPct val="{int(p.get("line", 100) * 1000)}"/></a:lnSpc>')
        bu = (f'<a:buFont typeface="Arial"/><a:buChar char="{p["bullet"]}"/>' if p.get('bullet') else '<a:buNone/>')
        ind = ' marL="342900" indent="-342900"' if p.get('bullet') else ''
        runs = ''.join(run_xml(r) for r in p['runs'] if r['text'])
        end = f'<a:endParaRPr lang="vi-VN" sz="{int((p["runs"][0].get("size", 32) if p["runs"] else 32) * 50)}"/>'
        body += f'<a:p><a:pPr algn="{algn}"{ind}>{ln}{sp}{bu}</a:pPr>{runs}{end}</a:p>'
    ins = e(inset)
    return (f'<p:txBody><a:bodyPr wrap="square" lIns="{ins}" tIns="{ins}" rIns="{ins}" bIns="{ins}" anchor="{anchor}" rtlCol="0">'
            f'<a:noAutofit/></a:bodyPr><a:lstStyle/>{body or "<a:p/>"}</p:txBody>')


def shape_xml(sid, s):
    """s: name, x, y, w, h (px), rot (deg), geom, fill, line ((hex, alpha), width px) | None, paras, anchor."""
    cap = ' cap="rnd"' if s.get('round') else ''
    join = '<a:round/>' if s.get('round') else ''
    dash = f'<a:prstDash val="{s["line"][2]}"/>' if s.get('line') and len(s['line']) > 2 else ''   # dashed borders
    line = f'<a:ln w="{e(s["line"][1])}"{cap}>{fill_xml(s["line"][0])}{dash}{join}</a:ln>' if s.get('line') else '<a:ln><a:noFill/></a:ln>'
    rot = f' rot="{int(s.get("rot", 0) * 60000)}"' if s.get('rot') else ''
    tx = text_xml(s['paras'], s.get('anchor', 't'), s.get('inset', 0)) if s.get('paras') is not None else ''
    txbox = ' txBox="1"' if s.get('paras') is not None and not s.get('fill') else ''
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{sid}" name="{escape(s["name"], {chr(34): "&quot;"})}"/><p:cNvSpPr{txbox}/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm{rot}><a:off x="{e(s["x"])}" y="{e(s["y"])}"/><a:ext cx="{max(e(s["w"]), 1)}" cy="{max(e(s["h"]), 1)}"/></a:xfrm>'
            f'{geom_xml(s.get("geom", "rect"))}{fill_xml(s.get("fill"))}{line}{effects_xml(s.get("effects"))}</p:spPr>{tx}</p:sp>')


def pic_xml(sid, s, rid):
    alpha = f'<a:alphaModFix amt="{int(max(0, s["alpha"]) * 100000)}"/>' if s.get('alpha', 1) < 1 else ''
    rot = f' rot="{int(s["rot"] * 60000)}"' if s.get('rot') else ''
    svg = SVG_EXT.format(s['svg_rid']) if s.get('svg_rid') else ''
    return (f'<p:pic><p:nvPicPr><p:cNvPr id="{sid}" name="{escape(s["name"])}"/><p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr><p:nvPr/></p:nvPicPr>'
            f'<p:blipFill><a:blip r:embed="{rid}">{alpha}{svg}</a:blip><a:srcRect/><a:stretch><a:fillRect/></a:stretch></p:blipFill>'
            f'<p:spPr><a:xfrm{rot}><a:off x="{e(s["x"])}" y="{e(s["y"])}"/><a:ext cx="{max(e(s["w"]), 1)}" cy="{max(e(s["h"]), 1)}"/></a:xfrm>'
            f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>{effects_xml(s.get("effects"))}</p:spPr></p:pic>')


def timing_xml(spids, stagger=110, dur=350):
    """Entrance fades that start on their own after the slide arrives, staggered like the HTML reveal."""
    if not spids:
        return ''
    n, effects = 4, ''
    for k, sp in enumerate(spids):
        a, b, c = n, n + 1, n + 2
        n += 3
        effects += (f'<p:par><p:cTn id="{a}" presetID="10" presetClass="entr" presetSubtype="0" fill="hold" '
                    f'nodeType="{"afterEffect" if k == 0 else "withEffect"}"><p:stCondLst><p:cond delay="{k * stagger}"/></p:stCondLst><p:childTnLst>'
                    f'<p:set><p:cBhvr><p:cTn id="{b}" dur="1" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn>'
                    f'<p:tgtEl><p:spTgt spid="{sp}"/></p:tgtEl><p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr>'
                    '<p:to><p:strVal val="visible"/></p:to></p:set>'
                    f'<p:animEffect transition="in" filter="fade"><p:cBhvr><p:cTn id="{c}" dur="{dur}"/><p:tgtEl><p:spTgt spid="{sp}"/></p:tgtEl>'
                    '</p:cBhvr></p:animEffect></p:childTnLst></p:cTn></p:par>')
    return ('<p:timing><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot"><p:childTnLst>'
            '<p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst>'
            '<p:par><p:cTn id="3" fill="hold"><p:stCondLst><p:cond delay="indefinite"/><p:cond evt="onBegin" delay="0"><p:tn val="2"/></p:cond>'
            f'</p:stCondLst><p:childTnLst><p:par><p:cTn id="{n}" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>'
            f'{effects}</p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn>'
            '<p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst>'
            '<p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst></p:seq>'
            '</p:childTnLst></p:cTn></p:par></p:tnLst></p:timing>')


def slide_xml(bg, items, timing=''):
    """items: shapes (dict) or pictures (dict with 'image' and 'rid'); items with 'anim' fade in after the slide arrives."""
    body = ''.join(pic_xml(i + 2, it, it['rid']) if it.get('image') else shape_xml(i + 2, it) for i, it in enumerate(items))
    if not timing and any(it.get('fx') for it in items):
        timing = __import__('pptx_anim').timing(items)   # effects traced back to the HTML (pptx_anim.annotate)
    timing = timing or timing_xml([i + 2 for i, it in enumerate(items) if it.get('anim')])
    return (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:sld {NS}><p:cSld>'
            f'<p:bg><p:bgPr>{fill_xml(bg)}<a:effectLst/></p:bgPr></p:bg><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
            '<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
            f'{body}</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>{MORPH}{timing}</p:sld>')


def write(path, slides, title='SlideFly', fonts=('Arial', 'Arial'), embedded=('', {})):
    """slides: list of (bg, items, timing, images {rid: (name, bytes)}); embedded: pptx_fonts.embed() result."""
    from pptx_parts import package_parts   # boilerplate parts (master, layout, theme, props)
    lst, fparts = embedded
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as z:
        for name, data in package_parts(len(slides), title, fonts, [s[3] for s in slides]).items():
            if fparts and name == 'ppt/presentation.xml':   # embedded fonts (EOT parts) so the style's type travels
                data = data.replace('saveSubsetFonts="1"', 'embedTrueTypeFonts="1"').replace('</p:presentation>', lst + '</p:presentation>')
            elif fparts and name == 'ppt/_rels/presentation.xml.rels':
                data = data.replace('</Relationships>', ''.join(
                    f'<Relationship Id="rIdF{n[14:-8]}" Type="{REL}/font" Target="{n[4:]}"/>' for n in fparts) + '</Relationships>')
            elif fparts and name == '[Content_Types].xml':
                data = data.replace('<Default Extension="xml"', '<Default Extension="fntdata" ContentType="application/x-fontdata"/><Default Extension="xml"')
            z.writestr(name, data)
        for name, data in fparts.items():
            z.writestr(name, data)
        media = set()   # the same picture (paper, pattern, blank PNG) is stored once and shared by every slide
        for n, (bg, items, timing, images) in enumerate(slides, 1):
            z.writestr(f'ppt/slides/slide{n}.xml', slide_xml(bg, items, timing))
            rels = f'<Relationship Id="rId1" Type="{REL}/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>'
            for rid, (fname, data) in images.items():
                if fname not in media:
                    media.add(fname)
                    z.writestr(f'ppt/media/{fname}', data)
                rels += f'<Relationship Id="{rid}" Type="{REL}/image" Target="../media/{fname}"/>'
            z.writestr(f'ppt/slides/_rels/slide{n}.xml.rels',
                       f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="{PKG}">{rels}</Relationships>')
