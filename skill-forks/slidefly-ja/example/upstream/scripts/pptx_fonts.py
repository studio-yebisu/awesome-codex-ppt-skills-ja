"""SlideFly -> PPTX: embed the style's Google Fonts so PowerPoint shows the same type as the HTML deck.

PowerPoint keeps embedded fonts as EOT (Embedded OpenType) parts, ppt/fonts/fontN.fntdata. The TTF files come
from the Google Fonts CSS API (a plain user agent gets TTF links, full character set incl. Vietnamese) and are
cached in ~/.cache/slidefly/fonts. No network: nothing is embedded and PowerPoint substitutes a font.
"""
import re
import struct
import urllib.request
from pathlib import Path

CACHE = Path.home() / '.cache' / 'slidefly' / 'fonts'
UA = {'User-Agent': 'Mozilla/4.0'}   # old agent -> truetype links
SLOTS = ('regular', 'bold', 'italic', 'boldItalic')


def _get(url, timeout=30):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout).read()


def faces(css_texts):
    """@import Google Fonts in the deck CSS -> [(family, italic, weight, ttf url)]."""
    out = []
    for url in {u for t in css_texts for u in re.findall(r"@import\s+url\(['\"]?(https://fonts\.googleapis\.com/[^'\")]+)", t)}:
        try:
            css = _get(url.replace('&amp;', '&'), 20).decode()
        except OSError:
            continue
        out += [(f, s == 'italic', int(w), u) for f, s, w, u in
                re.findall(r"font-family: '([^']+)';\s*font-style: (\w+);\s*font-weight: (\d+);.*?url\((\S+?)\)", css, re.S)]
    return out


def _tables(ttf):
    n = struct.unpack('>H', ttf[4:6])[0]
    return {ttf[12 + 16 * i:16 + 16 * i].decode('latin-1'): struct.unpack('>II', ttf[20 + 16 * i:28 + 16 * i]) for i in range(n)}


def _names(ttf, t):
    off, _ = t['name']
    count, base = struct.unpack('>HH', ttf[off + 2:off + 6])
    names = {}
    for i in range(count):
        pid, eid, lid, nid, ln, so = struct.unpack('>6H', ttf[off + 6 + 12 * i:off + 18 + 12 * i])
        if pid == 3 and eid in (0, 1) and lid == 0x409 and nid in (1, 2, 4, 5, 16, 17):
            names[nid] = ttf[off + base + so:off + base + so + ln]   # already UTF-16BE
    return names


def eot(ttf):
    """Uncompressed EOT 0x00020002 around a TrueType font -> (bytes, family, panose hex)."""
    t = _tables(ttf)
    o2 = t['OS/2'][0]
    weight, fstype = struct.unpack('>H', ttf[o2 + 4:o2 + 6])[0], struct.unpack('>H', ttf[o2 + 8:o2 + 10])[0]
    panose = ttf[o2 + 32:o2 + 42]
    ur = struct.unpack('>4I', ttf[o2 + 42:o2 + 58])
    italic = 1 if struct.unpack('>H', ttf[o2 + 62:o2 + 64])[0] & 1 else 0
    cp = struct.unpack('>2I', ttf[o2 + 78:o2 + 86]) if struct.unpack('>H', ttf[o2:o2 + 2])[0] >= 1 else (0, 0)
    csa = struct.unpack('>I', ttf[t['head'][0] + 8:t['head'][0] + 12])[0]
    nm = _names(ttf, t)
    le = lambda b: bytes(b[i ^ 1] for i in range(len(b)))   # UTF-16BE -> UTF-16LE
    fam, sty = nm.get(16, nm.get(1, b'')), nm.get(17, nm.get(2, b''))
    strs = b''.join(struct.pack('<HH', 0, len(s)) + le(s) for s in (fam, sty, nm.get(5, b''), nm.get(4, b'')))
    head =(struct.pack('<II', 0x00020002, 0) + panose + struct.pack('<BBIHH', 1, italic, weight, fstype, 0x504C)
            + struct.pack('<4I', *ur) + struct.pack('<2I', *cp) + struct.pack('<I', csa) + b'\0' * 16
            + strs + struct.pack('<HH', 0, 0)                       # RootString: none
            + struct.pack('<IIHH', 0x50475342, 65001, 0, 0) + struct.pack('<II', 0, 0))   # root checksum (empty ^ key), EUDC, signature
    data = struct.pack('<I', len(ttf)) + head + ttf
    family = fam.decode('utf-16-be')
    return struct.pack('<I', len(data) + 4) + data, family, panose.hex().upper()


def embed(css_texts, families):
    """-> (embeddedFontLst xml, {part name: bytes}); families = typefaces the slides use."""
    picks, heavy = {}, {}
    for fam, it, w, url in faces(css_texts):
        if fam not in families:
            continue
        if not it and w > heavy.get(fam, (0,))[0]:
            heavy[fam] = (w, url)   # no 600+ weight loaded: the heaviest one stands in for bold
        slot = ('bold' if w >= 600 else 'regular') if not it else ('boldItalic' if w >= 600 else 'italic')
        best = picks.get((fam, slot))
        if not best or abs(w - (700 if 'old' in slot else 400)) < abs(best[0] - (700 if 'old' in slot else 400)):
            picks[(fam, slot)] = (w, url)
    for fam, best in heavy.items():
        picks.setdefault((fam, 'bold'), best)
    CACHE.mkdir(parents=True, exist_ok=True)
    xml, files, k = '', {}, 0
    for fam in families:
        inner, panose = '', ''
        for slot in SLOTS:
            if (fam, slot) not in picks:
                continue
            url = picks[(fam, slot)][1]
            f = CACHE / url.rsplit('/', 1)[-1]
            try:
                if not f.exists():
                    f.write_bytes(_get(url))
                data, _, panose = eot(f.read_bytes())
            except (OSError, KeyError, struct.error):
                continue
            k += 1
            files[f'ppt/fonts/font{k}.fntdata'] = data
            inner += f'<p:{slot} r:id="rIdF{k}"/>'
        if inner:
            xml += f'<p:embeddedFont><p:font typeface="{fam}" panose="{panose}" charset="0"/>{inner}</p:embeddedFont>'
    return (f'<p:embeddedFontLst>{xml}</p:embeddedFontLst>' if xml else ''), files
