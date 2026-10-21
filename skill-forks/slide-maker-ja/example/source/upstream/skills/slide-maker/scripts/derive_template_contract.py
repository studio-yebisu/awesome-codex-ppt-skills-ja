#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Derive a registered template's machine-checkable contract FROM THE TEMPLATE, never by retyping.

🔴 WHY THIS IS A SCRIPT AND NOT A WRITING TASK. Measured: 10 of the 11 registered templates carry
no `## Machine-checkable contract` block, so `check_template_profile.py` cannot bind to them and a
deck built from any of them is checked against its template's look by NOTHING. The obvious fix —
read each profile.md and type the palette into a JSON block — is the fix that introduces the
defect: a hand-copied hex is a number somebody remembered, and this skill's whole never-invent
floor says a number nobody can trace is worse than a missing one.

So the contract is EXTRACTED:

  * from `style.py` when the template has one — the `RGBColor(0x.., 0x.., 0x..)` constants and the
    face-name strings ARE what the build paints, so a contract derived from them cannot disagree
    with the deck the template produces;
  * from `profile.md`'s own backticked hex tokens otherwise — the prose is the only machine-
    readable thing left, and a backticked `14181F` is unambiguous where a font name in prose is not.

Anything it cannot derive it LEAVES OUT. Every contract key is optional by design, so a template
that yields only a palette is checked on palette alone — which is nine colours more than nothing.

    python3 scripts/derive_template_contract.py --all            # every registered template
    python3 scripts/derive_template_contract.py modern-dark      # one, to stdout
    python3 scripts/derive_template_contract.py --all --write    # insert the block into profile.md
    python3 scripts/derive_template_contract.py --selftest

Exit 0 · 1 nothing derivable for some template · 2 could not run.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Three dialects, because the registry has three and a reader that knows one silently falls back
# to prose for the other two — which is how this script would quietly stop deriving and start
# guessing. All of them are in registered templates TODAY:
#   BG = RGBColor(0x14, 0x18, 0x1F)      modern-dark
#   BG = C("0A1B38")  /  RGBColor.from_string("0A1B38")      blueprint-tech
#   BG = "101A24"                        nightdata-briefing
_RGB = re.compile(r"^\s*([A-Z][A-Z0-9_]*)\s*=\s*RGBColor\(\s*0x([0-9A-Fa-f]{2})\s*,\s*"
                  r"0x([0-9A-Fa-f]{2})\s*,\s*0x([0-9A-Fa-f]{2})\s*\)", re.M)
_HEXCALL = re.compile(r"^\s*([A-Z][A-Z0-9_]*)\s*=\s*(?:[A-Za-z_][\w.]*)?\(\s*"
                      r"['\"]#?([0-9A-Fa-f]{6})['\"]\s*\)", re.M)
_HEXSTR = re.compile(r"^\s*([A-Z][A-Z0-9_]*)\s*=\s*['\"]#?([0-9A-Fa-f]{6})['\"]\s*(?:#|$)", re.M)
# `BG = RGBColor(20, 24, 31)` — the DECIMAL form of the same constructor, and `BG = (0x14,0x18,0x1F)`
_DEC = re.compile(r"^\s*([A-Z][A-Z0-9_]*)\s*=\s*(?:RGBColor)?\(\s*(\d{1,3}|0x[0-9A-Fa-f]{2})\s*,"
                  r"\s*(\d{1,3}|0x[0-9A-Fa-f]{2})\s*,\s*(\d{1,3}|0x[0-9A-Fa-f]{2})\s*\)", re.M)
# `ACCENTS_HEX = ["34D1A6", "F2B04E"]` — modern-dark ships exactly this, and a template whose
# accents live ONLY in such a list would otherwise contribute none of them.
_HEXLIST = re.compile(r"^\s*([A-Z][A-Z0-9_]*)\s*=\s*\[([^\]]*)\]", re.M)
_HEXITEM = re.compile(r"['\"]#?([0-9A-Fa-f]{6})['\"]")
# `dk.set_palette(font="Helvetica Neue", mono="Menlo")` — deckkit's own documented re-theming call,
# which is how SKILL.md tells a build to set faces in the first place.
_SETPAL = re.compile(r"set_palette\s*\(([^)]*)\)", re.S)
_SETPAL_KW = re.compile(r"\b(font|mono|display|eafont|eadisplay)\s*=\s*['\"]([^'\"]{2,40})['\"]")
# `FONT = "Helvetica Neue"` · `dk.FONT = "Helvetica Neue"` · `dk.FONT = BODY` (one indirection).
# Anchored on `^` OR `;` because blueprint-tech really does write all three faces on one
# semicolon-separated line, and a `^`-only reader takes the first and loses the rest — the
# silent half-derivation this whole script exists to avoid.
_FACE = re.compile(r"(?:^|;)\s*(?:dk\.|deckkit\.)?(FONT|MONO|DISPLAY|EAFONT|EADISPLAY)\s*=\s*"
                   r"['\"]([^'\"]{2,40})['\"]", re.M)
_FACE_REF = re.compile(r"(?:^|;)\s*(?:dk\.|deckkit\.)(FONT|MONO|DISPLAY|EAFONT|EADISPLAY)\s*=\s*"
                       r"([A-Z][A-Z0-9_]*)\s*(?:#|$)", re.M)
_NAMED_STR = re.compile(r"^\s*([A-Z][A-Z0-9_]*)\s*=\s*['\"]([^'\"]{2,40})['\"]", re.M)
# a backticked hex in prose: `14181F`
_HEX_IN_PROSE = re.compile(r"`#?([0-9A-Fa-f]{6})`")

# The colours that IDENTIFY a template rather than merely belong to it: its ground and its loudest
# accent. Two are enough to bind and few enough that binding cannot stand in for checking.
_IDENT_HINTS = ("BG", "GROUND", "PAPER", "CANVAS", "PANEL", "ACCENT", "PRIMARY")


def from_style(py_text):
    """({NAME: 'RRGGBB'}, {FONT: face}) as the style module literally declares them."""
    cols = {}
    for m in _RGB.finditer(py_text):
        cols.setdefault(m.group(1), (m.group(2) + m.group(3) + m.group(4)).upper())
    for rx in (_HEXCALL, _HEXSTR):
        for m in rx.finditer(py_text):
            cols.setdefault(m.group(1), m.group(2).upper())
    for m in _DEC.finditer(py_text):
        try:
            vals = [int(g, 16) if g.lower().startswith("0x") else int(g) for g in m.groups()[1:]]
        except ValueError:
            continue
        if all(0 <= v <= 255 for v in vals):
            cols.setdefault(m.group(1), "%02X%02X%02X" % tuple(vals))
    for m in _HEXLIST.finditer(py_text):
        for i, item in enumerate(_HEXITEM.findall(m.group(2))):
            cols.setdefault("%s_%d" % (m.group(1), i), item.upper())
    faces = {}
    for m in _FACE.finditer(py_text):
        faces.setdefault(m.group(1), m.group(2))
    named = {m.group(1): m.group(2) for m in _NAMED_STR.finditer(py_text)}
    for m in _FACE_REF.finditer(py_text):             # `dk.FONT = BODY` -> resolve BODY once
        val = named.get(m.group(2))
        if val and not re.fullmatch(r"#?[0-9A-Fa-f]{6}", val):
            faces.setdefault(m.group(1), val)
    for m in _SETPAL.finditer(py_text):
        for kw, val in _SETPAL_KW.findall(m.group(1)):
            faces.setdefault(kw.upper(), val)
    return cols, faces


def from_prose(md_text):
    """The backticked hex tokens a profile.md lists, in the order it lists them."""
    out = []
    for m in _HEX_IN_PROSE.finditer(md_text):
        v = m.group(1).upper()
        if v not in out:
            out.append(v)
    return out


def _chroma(hex6):
    """How LOUD a colour is (0-1): saturation times value. Used to find a palette's accent."""
    r, g, b = (int(hex6[i:i + 2], 16) / 255.0 for i in (0, 2, 4))
    hi, lo = max(r, g, b), min(r, g, b)
    return (0.0 if hi == 0 else (hi - lo) / hi) * hi


def _lum(hex6):
    r, g, b = (int(hex6[i:i + 2], 16) / 255.0 for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _ink_for(ground, palette):
    """The palette's TEXT colour: the one furthest from the ground in luminance.

    Not a guess about names — a text colour that does not contrast its ground is not a text
    colour, so the furthest is the only candidate that can be one.
    """
    rest = [c for c in palette if c != ground]
    return max(rest, key=lambda c: abs(_lum(c) - _lum(ground))) if rest else None


def identifying(cols):
    """Two colours that NAME this template: its ground, and its loudest accent.

    The accent is found by chroma, not by constant name. modern-dark calls its accent `TEAL`,
    blueprint-tech calls one `CYAN` and one `CORAL`, nightdata calls its `ORANGE` — a reader that
    looks for the word ACCENT fingerprints those templates on ground + panel instead, i.e. on two
    near-blacks, which is a weak fingerprint and a coincidence away from another dark template.
    """
    if not cols:
        return []
    ground = next((cols[k] for k in cols
                   if any(h in k for h in ("BG", "GROUND", "PAPER", "CANVAS"))), None)
    rest = [v for v in dict.fromkeys(cols.values()) if v != ground]
    accent = max(rest, key=_chroma) if rest else None
    picked = [c for c in (ground, accent) if c]
    for v in dict.fromkeys(cols.values()):
        if len(picked) >= 2:
            break
        if v not in picked:
            picked.append(v)
    return picked[:2]


def _deckkit_palette():
    """deckkit's own declared colours, as upper-case hex — the set that identifies nothing."""
    try:
        import deckkit
    except Exception:
        return set()
    out = set()
    for name in dir(deckkit):
        if not name.isupper():
            continue
        v = getattr(deckkit, name, None)
        try:
            out.add("%02X%02X%02X" % (v[0], v[1], v[2]))
        except Exception:
            continue
    return out


def derive(template_dir):
    """(contract dict or None, how it was derived, what could not be derived)."""
    d = Path(template_dir)
    style = next((d / n for n in ("style.py", "build_example.py") if (d / n).exists()), None)
    prof = d / "profile.md"
    gaps = []
    cols, faces = ({}, {})
    if style is not None:
        cols, faces = from_style(style.read_text(encoding="utf-8", errors="replace"))
        how = style.name
    else:
        how = "profile.md (prose)"
    palette = list(dict.fromkeys(cols.values()))
    if not palette and prof.exists():
        palette = from_prose(prof.read_text(encoding="utf-8", errors="replace"))
        if style is not None:
            # 🔴 SAY IT. Falling back quietly is the failure mode: a template that HAS a style
            # module but declares its palette in a shape this cannot read (a dict, a comprehension,
            # a helper call) would be derived from prose and reported only as "from profile.md",
            # which reads like a template that simply has no style module.
            gaps.append("%s exists but declares no colour this can read (it knows "
                        "RGBColor(0x..)/RGBColor(1..255)/C(\"hex\")/\"hex\"/[\"hex\", …]); the "
                        "palette below came from the PROSE instead — check it is the real one"
                        % style.name)
        how = "%s -> profile.md (prose)" % style.name if style is not None else "profile.md (prose)"
    if not palette:
        return None, how, ["no colour is declared anywhere this can read"]
    # 🔴 A palette that IS the library's default set identifies nothing. lkeb-lumc's profile says
    # so in as many words ("These are the deckkit defaults"), and a fingerprint built from it would
    # match every stock deck ever built while telling no one anything. Refusing here is what keeps
    # a generated contract from replacing a hand-written one that was actually specific — which is
    # exactly what happened once, with --force.
    stock = _deckkit_palette()
    if stock and len([c for c in palette if c in stock]) >= max(3, int(0.8 * len(palette))):
        return None, how, ["its palette is deckkit's own default set (%d of %d colours), so a "
                           "palette fingerprint would match every stock deck and identify nothing"
                           % (len([c for c in palette if c in stock]), len(palette))]
    # From prose there are no constant NAMES, so the ground is the first colour the palette bullet
    # lists (every profile here writes bg first) and the accent is again the loudest — `palette[:2]`
    # would have fingerprinted nvidia-dark on two near-blacks.
    ident = identifying(cols) if cols else (
        [palette[0]] + ([max(palette[1:], key=_chroma)] if len(palette) > 1 else []))
    # 🔴 CALIBRATED ON A REAL BUILD, not on a round number. A 4-slide deck built with modern-dark's
    # OWN api painted 7 of its 11 declared colours — 64% — because a short deck has no reason to
    # reach the raised panel or the third and fourth accents. A "60% of the palette" floor would
    # therefore have fired on a correct deck at the next slide fewer. So the CHECK is structural:
    # the ground and the ink are colours no deck from this template can avoid, and at least one
    # accent must appear; the rest of the palette is reported as coverage, never as a finding.
    ground = ident[0] if ident else palette[0]
    ink = _ink_for(ground, palette)
    accents = [c for c in palette if _chroma(c) >= 0.25 and c not in (ground, ink)]
    core = [c for c in (ground, ink) if c]
    # 🔴 THE FINGERPRINT IS THE CORE, and the first version got this wrong in a way only a real
    # build showed: it fingerprinted on ground + LOUDEST colour, and modern-dark's loudest is its
    # amber secondary, which a 4-slide deck built from the template never paints — so a correct
    # deck bound to nothing and the gate said NOT CHECKED. The ground and the ink are the two a
    # deck cannot avoid, which is exactly what a fingerprint needs.
    #
    # That does make the core check circular when binding happens BY FINGERPRINT: a deck that
    # bound has the core by definition. It is not circular on the path that matters — binding by
    # the RECORDED template name, where "declared it, built it in stock colours" is caught — and
    # the accent and font checks bite either way. Saying so here beats a check that looks stronger
    # than it is.
    contract = {"match": {"palette_any": core},
                "palette": {"core": core, "accents": accents, "expect": palette}}
    if faces.get("FONT"):
        contract["fonts"] = {k: v for k, v in faces.items() if k in ("FONT", "MONO")}
    else:
        gaps.append("no FONT constant to read — the type decision stays prose and is NOT checked")
    return contract, how, gaps


def block(contract):
    return ("## Machine-checkable contract\n\n"
            "<!-- Derived by scripts/derive_template_contract.py from this template's own style "
            "module — never hand-typed. Re-run it after changing the palette. -->\n\n"
            "```json\n" + json.dumps(contract, indent=2) + "\n```\n")


_HAS_CONTRACT = re.compile(r"^##\s*Machine-checkable contract\s*$", re.M)


def insert(profile_path, contract, force=False):
    """Add the contract block to profile.md. Returns 'wrote' | 'kept' | 'unchanged'.

    🔴 It REFUSES to overwrite an existing contract. `lkeb-lumc` is a supplied-.pptx template whose
    hand-written contract carries layout names, a title colour and a `must_cover` rectangle that no
    palette scan can reproduce — running this over it would replace a richer, correct contract with
    a poorer derived one and report success. An existing block is a decision someone made.
    """
    p = Path(profile_path)
    text = p.read_text(encoding="utf-8")
    if _HAS_CONTRACT.search(text) and not force:
        return "kept"
    new = block(contract)
    pat = re.compile(r"^##\s*Machine-checkable contract\s*$.*?^```\s*$\s*", re.M | re.S)
    out = pat.sub(new, text) if pat.search(text) else (text.rstrip() + "\n\n" + new)
    if out == text:
        return "unchanged"
    p.write_text(out, encoding="utf-8")
    return "wrote"


def _selftest():
    bad = []
    cols, faces = from_style('BG = RGBColor(0x14, 0x18, 0x1F)\nTEAL=RGBColor(0x34,0xD1,0xA6)\n'
                             'FONT = "Helvetica Neue"\nMONO = \'Menlo\'\nNOT_A_COLOUR = 3\n')
    if cols != {"BG": "14181F", "TEAL": "34D1A6"}:
        bad.append("style constants: %r" % cols)
    if faces != {"FONT": "Helvetica Neue", "MONO": "Menlo"}:
        bad.append("faces: %r" % faces)
    if from_prose("BG `14181F` . ink `ECEFF4` . again `14181f`") != ["14181F", "ECEFF4"]:
        bad.append("prose hexes: %r" % from_prose("BG `14181F` . ink `ECEFF4` . again `14181f`"))
    # the other two dialects, both live in the registry right now
    c2, f2 = from_style('def C(h): return RGBColor.from_string(h)\nBG = C("0A1B38")\n'
                        '    dk.FONT = "Helvetica Neue"; dk.MONO = "Menlo"\n')
    if c2 != {"BG": "0A1B38"} or f2.get("FONT") != "Helvetica Neue" or f2.get("MONO") != "Menlo":
        bad.append("C(\"hex\") + dk.FONT dialect: %r %r" % (c2, f2))
    c3, f3 = from_style('BG = "101A24"   # ground\nBODY = "Helvetica Neue"\n'
                        'MONO = "Menlo"\ndk.FONT = BODY\n')
    if c3 != {"BG": "101A24"} or f3.get("FONT") != "Helvetica Neue":
        bad.append("bare-hex + one-indirection dialect: %r %r" % (c3, f3))
    if "101A24" in str(f3.values()):
        bad.append("a hex string was read as a FACE name")
    if identifying({"BG": "14181F", "PANEL": "1E242E", "TEAL": "34D1A6"}) != ["14181F", "34D1A6"]:
        bad.append("identifying must pick the LOUDEST colour, not the second constant: %r"
                   % identifying({"BG": "14181F", "PANEL": "1E242E", "TEAL": "34D1A6"}))
    if _chroma("34D1A6") <= _chroma("1E242E"):
        bad.append("chroma ordering is wrong")
    for b in bad:
        print("  ✗", b)
    print("[derive-contract] selftest %s" % ("FAILED" if bad else "ok"))
    return 1 if bad else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("template", nargs="?", help="a registered template name")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--write", action="store_true", help="insert the block into each profile.md")
    ap.add_argument("--force", action="store_true",
                    help="replace a contract that is already there (it is kept by default)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return _selftest()
    try:
        import registry
        pairs = registry.list_templates()
    except Exception as exc:
        print("[derive-contract] could not read the registry: %s" % exc)
        return 2
    if not a.all:
        if not a.template:
            ap.error("name a template or pass --all")
        pairs = [(n, d) for n, d in pairs if n == a.template]
        if not pairs:
            print("[derive-contract] no registered template named %r" % a.template)
            return 2
    problems = 0
    for name, d in pairs:
        contract, how, gaps = derive(d)
        if contract is None:
            problems += 1
            print("[derive-contract] %-22s NOTHING DERIVABLE (%s): %s" % (name, how, "; ".join(gaps)))
            continue
        print("[derive-contract] %-22s from %-22s %d colour(s), fonts=%s%s"
              % (name, how, len(contract["palette"]["expect"]),
                 contract.get("fonts") or "—", ("  [gap] " + "; ".join(gaps)) if gaps else ""))
        if a.write:
            what = insert(Path(d) / "profile.md", contract, force=a.force)
            note = {"kept": "KEPT the contract already there (use --force to replace it)",
                    "wrote": "wrote", "unchanged": "unchanged"}[what]
            print("                  %s %s" % (note, Path(d) / "profile.md"))
        elif not a.all:
            print(block(contract))
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
