#!/usr/bin/env python3
"""Do the faces this deck NAMES actually resolve on the machine that measured it?

This is not the portability question. "Will the presenter have Calibri?" is unknowable from the
file and is correctly an advisory (PRE-FLIGHT 10). The question here is decidable and much more
consequential:

    every fit, wrap, overflow, footer-clearance and grid guard in this library sits on
    `deckkit._measure_lines`, which measures with the face it can RESOLVE. When the named face is
    absent, a metric-incompatible stand-in is measured instead, so the build and the lint are
    computed from the same wrong number and AGREE WITH EACH OTHER while the render disagrees with
    both.

`deckkit.font_health()` has always been able to see this, and `lint_layout` prints it — as a
`print`, not a finding. It is therefore in no `--json`, gates nothing, and is one line in a
scrolling build log. MEASURED, in this repo's own history: an install command that fit its panel
by 10% under substituted metrics still broke across three lines in the render and was copied back
as a repo path that 404s. MEASURED again on the LKEB/LUMC deck this check was written for: the
template's own theme font is Calibri, Calibri lives only inside the PowerPoint app bundle on
macOS, and the whole deck would have been laid out against a substitute — caught only because the
template's hand-written `profile.md` happened to warn about it.

🔴 IT REPORTS; IT DOES NOT BLOCK — learned the expensive way. Written as a blocking hand-off
gate, it broke FOUR CI runs across THREE unrelated suites before the reason became clear, and the
reason is conceptual rather than a bug:

    this check runs on the machine doing the GATING, which is not necessarily the machine that
    did the MEASURING, and nothing in a .pptx says which was which.

A deck authored on a Mac with Helvetica Neue installed was measured correctly; re-gating it on a
Linux box reports, truthfully, that the face does not resolve THERE — and blocking on that would
refuse delivery of a deck with nothing wrong with it. The same applied to deckkit's own shipped
defaults (FONT='Calibri', MONO='Consolas'), which ship with neither macOS nor Linux, so the
blocking version refused essentially every stock build.

So the finding is printed on both gate paths and carried in `--json`, and the severity split below
is kept because it is real information — it just no longer decides delivery. That is still a large
improvement on what existed before: the condition was a `print()` inside `lint_layout`, in no
`--json`, gating nothing, one line in a scrolling build log. `--strict` makes the CLI exit 1 for a
caller that owns BOTH the build and the gate, and therefore knows the measuring machine is this one.

What it reports, per face that DRAWS text on these slides. Decided per CHARACTER — East-Asian
text is drawn from a run's <a:ea> face, complex scripts (Arabic, Hebrew, Thai, Indic…) from <a:cs>,
the rest from <a:latin> — and found on the run, its paragraph, its list style, or the theme
(including an Office theme's per-script face, picked by the run's `lang`), in plain shapes, groups,
table cells and fields. `faces_in_use(prs)` is that inventory, and PRE-FLIGHT 10 reads the same one,
so the two can no longer disagree about a face:

  UNRESOLVED BODY FACE    a face drawing real text does not resolve here -> every geometry number
                          computed for that text is the wrong face's. Block severity.
  UNRESOLVED THEME FACE   the theme's major/minor LATIN face does not resolve — judged even when no
                          slide run is attributed to it, since chart / SmartArt / notes text inherits
                          it and is not read here. Block severity. An East-Asian or complex-script
                          theme face that draws none of its script draws nothing and is not reported.
  trace-only              a face drawing < `MIN_CHARS` characters is REPORTED at note severity —
                          a stray run in a decorative face cannot move a layout.
  (no face named)         >= `MIN_CHARS` East-Asian or complex-script characters that no run, style
                          or theme names a face for; the presenting application picks one. Note.

    python3 scripts/check_fonts_resolve.py <deck.pptx> [--json] [--waive "<why>"]
    python3 scripts/check_fonts_resolve.py --selftest

Exit 0 clean · 1 findings · 2 could not run (NOT the same as clean, and it says so).
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# A face carrying fewer characters than this cannot plausibly drive a wrap/fit decision that
# matters, so it is reported and never blocked. Deliberately low: a 12-character heading in the
# wrong face is exactly the kind of thing that overflows a title band.
MIN_CHARS = 8

# 🔴 deckkit's SHIPPED DEFAULTS are reported and never blocked, however much text they carry.
# The condition is identical either way — a substituted measurement — but the RESPONSIBILITY is
# not, and only one of the two is a decision anybody made:
#   * a face the author SET is a choice the machine cannot honour -> block, make them decide;
#   * a face the LIBRARY chose is an environment fact about this host. `FONT='Calibri'` and
#     `MONO='Consolas'` ship with neither macOS nor Linux, so blocking on them would refuse
#     delivery of a perfectly correct deck on essentially every stock machine — including this
#     repo's own Ubuntu CI, which is how the over-reach was caught: a suite that passes on a Mac
#     with Office fonts installed failed 8 assertions on CI, all of them "a thing that should
#     pass". A gate that fires on the whole population is not a floor, it is an outage.
# The fix for this arm is one call (`deckkit.use_platform_fonts()`), and it is named in the note.
# Read from deckkit's SOURCE, not from the live module: a build script assigns `dk.FONT = ...`
# before this runs, so the imported globals are the deck's choice, not the library's default —
# reading them would classify every author-set face as "shipped" and defeat the whole split.
# The literal set is the documented fallback and a test pins the two against each other.
_FALLBACK_DEFAULT_FACES = {"Calibri", "Consolas", "Arial", "STIX Two Math", "Cambria Math"}


def _shipped_defaults():
    import re as _re
    try:
        src = (pathlib.Path(__file__).with_name("deckkit.py")).read_text(encoding="utf8")
    except Exception:
        return set(_FALLBACK_DEFAULT_FACES)
    out = set()
    for attr in ("FONT", "MONO", "DISPLAY", "EAFONT", "EADISPLAY", "EQFONT", "EQ_MATHFONT"):
        m = _re.search(r"^%s\s*=\s*[\"']([^\"']+)[\"']" % attr, src, _re.M)
        if m:
            out.add(m.group(1))
    return out or set(_FALLBACK_DEFAULT_FACES)


DEFAULT_FACES = _shipped_defaults()

_A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
_P = "{http://schemas.openxmlformats.org/presentationml/2006/main}"


def _resolver():
    """`face -> bool` (does it resolve here), from deckkit, or None when deckkit is unavailable."""
    try:
        import deckkit
    except Exception:
        return None
    ff = getattr(deckkit, "_font_file", None)
    if not callable(ff):
        return None

    def ok(face):
        try:
            path = ff(face)
        except Exception:
            return None                              # cannot tell -> never claim either way
        if not path:
            return False
        # `_font_file` falls back to a stand-in rather than returning None, so a resolved PATH is
        # not by itself evidence the NAMED face was found. deckkit exposes the real predicate.
        try:
            return not deckkit._font_substituted(face)
        except Exception:
            return bool(path)
    return ok


def an_installed_face():
    """A family name this machine can actually resolve, or None.

    🔴 ASK the font machinery; never guess. A test that hardcodes "Helvetica on macOS, DejaVu Sans
    on Linux" is asserting a fact about somebody else's container, and it fails there for a reason
    that has nothing to do with the code under test — measured, on this repo's own Ubuntu CI,
    where `DejaVu Sans` does not resolve. The only honest source for "a face that resolves here"
    is the same resolver everything else in this module uses.
    """
    ok = _resolver()
    if ok is None:
        return None
    try:
        import matplotlib.font_manager as fm
        names = []
        seen = set()
        for f in fm.fontManager.ttflist:
            if f.name not in seen:
                seen.add(f.name)
                names.append(f.name)
    except Exception:
        names = []
    for face in names:
        if ok(face):
            return face
    return None


# Which face draws a character is decided by the CHARACTER, not by the run. PowerPoint draws
# East-Asian text from a run's <a:ea> face, complex scripts (Arabic, Hebrew, Thai, Indic…) from
# <a:cs>, and everything else from <a:latin>. 🔴 Getting that wrong fails in BOTH directions:
#   * crediting a whole run to every slot it names made an English deck built with EAFONT set
#     "carry" every word in its CJK face — a block for a face that draws nothing;
#   * reading <a:latin> alone (what python-pptx's `run.font.name` does) made a Chinese deck look
#     clean. MEASURED (before deckkit read font name tables and macOS's asset store): EAFONT=
#     'PingFang SC' laid 24 CJK glyphs out at 60% of their true width while PRE-FLIGHT 10 printed
#     "all 1 font(s) resolve locally: ['Calibri']".
_CS_ORD = ((0x0590, 0x08FF),   # Hebrew · Arabic · Syriac · Thaana · NKo · Arabic Extended-A
           (0x0900, 0x0DFF),   # Devanagari … Sinhala
           (0x0E00, 0x0EFF),   # Thai · Lao
           (0x0F00, 0x109F),   # Tibetan · Myanmar
           (0x1780, 0x17FF),   # Khmer
           (0xFB1D, 0xFDFF),   # Hebrew / Arabic presentation forms A
           (0xFE70, 0xFEFC))   # Arabic presentation forms B
_SLOTS = ("latin", "ea", "cs")

# An Office theme usually leaves `<a:ea typeface=""/>` EMPTY and names the East-Asian face per
# script (`<a:font script="Hans" typeface="…"/>`), chosen by the run's language. A template authored
# in Chinese PowerPoint is exactly this shape, so without the mapping its CJK face is invisible.
_LANG_SCRIPT = (("zh-tw", "Hant"), ("zh-hk", "Hant"), ("zh-mo", "Hant"), ("zh", "Hans"),
                ("ja", "Jpan"), ("ko", "Hang"), ("ar", "Arab"), ("fa", "Arab"), ("ur", "Arab"),
                ("he", "Hebr"), ("th", "Thai"), ("hi", "Deva"))
_TITLE_PH = ("title", "ctrTitle")


def _ea_ranges():
    """deckkit's own CJK classifier — ONE definition of East-Asian for the builder and this check.

    Deliberately no local copy: a second range table is a second definition, and it drifts.
    """
    import deckkit
    return tuple(deckkit._CJK_ORD)


def _by_slot(text, ea_ord):
    ea = cs = 0
    for ch in text:
        o = ord(ch)
        if any(a <= o <= b for a, b in ea_ord):
            ea += 1
        elif any(a <= o <= b for a, b in _CS_ORD):
            cs += 1
    return {"latin": len(text) - ea - cs, "ea": ea, "cs": cs}


def _theme_of(master):
    """{(scheme, slot): face} and {(scheme, 'script:Hans'): face} for one master's theme."""
    from lxml import etree
    out = {}
    for rel in master.part.rels.values():
        if not rel.reltype.endswith("/theme"):
            continue
        root = etree.fromstring(rel.target_part.blob)
        for scheme, tag in (("major", "majorFont"), ("minor", "minorFont")):
            el = root.find(".//" + _A + tag)
            if el is None:
                continue
            for slot in _SLOTS:
                node = el.find(_A + slot)
                face = node.get("typeface") if node is not None else None
                if face and not face.startswith("+"):
                    out[(scheme, slot)] = face
            for node in el.findall(_A + "font"):
                if node.get("script") and node.get("typeface"):
                    out[(scheme, "script:" + node.get("script"))] = node.get("typeface")
    return out


def _script_of(rPr):
    for attr in ("lang", "altLang"):
        lang = (rPr.get(attr) or "").lower() if rPr is not None else ""
        for prefix, script in _LANG_SCRIPT:
            if lang.startswith(prefix):
                return script
    return None


def _defaults_chain(run):
    """[run rPr, paragraph defRPr, list-style defRPr] nearest first, and the theme scheme in force."""
    rPr = run.find(_A + "rPr")
    para = run.getparent()
    pPr = para.find(_A + "pPr") if para is not None else None
    lvl = int(pPr.get("lvl") or 0) if pPr is not None else 0
    chain = [rPr, pPr.find(_A + "defRPr") if pPr is not None else None]
    body = para.getparent() if para is not None else None
    scheme = "minor"
    if body is not None:
        lst = body.find(_A + "lstStyle")
        lvlpPr = lst.find(_A + "lvl%dpPr" % (lvl + 1)) if lst is not None else None
        chain.append(lvlpPr.find(_A + "defRPr") if lvlpPr is not None else None)
        shape = body.getparent()
        ph = shape.find(_P + "nvSpPr/" + _P + "nvPr/" + _P + "ph") if shape is not None else None
        if ph is not None and ph.get("type") in _TITLE_PH:
            scheme = "major"                      # a title placeholder inherits the HEADING face
    return rPr, chain, scheme


def _face_for(chain, slot, scheme, theme, script):
    """(face, how) for one slot of one run — 'named', 'theme', or (None, None) when nothing names one."""
    for props in chain:
        node = props.find(_A + slot) if props is not None else None
        face = node.get("typeface") if node is not None else ""
        if not face:
            continue                              # typeface="" means "not set HERE" — keep walking
        if face.startswith("+"):                  # "+mj-ea" / "+mn-lt": a pointer INTO the theme
            scheme = "major" if face.startswith("+mj") else "minor"
            break
        return face, "named"
    face = theme.get((scheme, slot))
    if not face and slot != "latin" and script:
        face = theme.get((scheme, "script:" + script))
    return (face, "theme") if face else (None, None)


def faces_in_use(prs):
    """Which face draws how much of this deck's text, per script slot.

    Returns (carried, theme_faces, unattributed):
      carried       {face: {"latin": n, "ea": n, "cs": n}} — characters that face DRAWS, whether it
                    was named on the run, its paragraph, its list style, or inherited from the theme
      theme_faces   {face: {(scheme, slot), …}} — every face a theme declares, used or not
      unattributed  {"ea": n, "cs": n} — characters no run, style or theme names a face for; the
                    viewer's application picks one, so nothing here can say what they measured as

    Reads the XML of every `<a:r>` and `<a:fld>` on every slide, so text in groups, tables and
    fields is counted — the python-pptx shape walk misses table cells entirely. PRE-FLIGHT 10 and
    this module's `check` read THIS inventory, so the two can no longer disagree about a face.
    """
    ea_ord = _ea_ranges()
    carried, theme_faces, unattributed = {}, {}, {"latin": 0, "ea": 0, "cs": 0}
    themes = {}
    for slide in prs.slides:
        try:
            master = slide.slide_layout.slide_master
            key = str(master.part.partname)
            if key not in themes:
                themes[key] = _theme_of(master)
            theme = themes[key]
        except Exception:
            theme = {}
        for (scheme, slot), face in theme.items():
            theme_faces.setdefault(face, set()).add((scheme, slot))
        for run in slide._element.iter(_A + "r", _A + "fld"):
            t = run.find(_A + "t")
            text = t.text if t is not None and t.text else ""
            if not text:
                continue
            counts = _by_slot(text, ea_ord)
            rPr, chain, scheme = _defaults_chain(run)
            script = _script_of(rPr)
            for slot in _SLOTS:
                n = counts[slot]
                if not n:
                    continue
                face, _how = _face_for(chain, slot, scheme, theme, script)
                if face is None:
                    unattributed[slot] += n
                    continue
                carried.setdefault(face, {"latin": 0, "ea": 0, "cs": 0})[slot] += n
    return carried, theme_faces, unattributed


def check(pptx):
    """(findings, facts). findings = list of (severity, face, message). severity: 'block'|'note'."""
    try:
        from pptx import Presentation
        prs = Presentation(pptx)
    except Exception as exc:                          # unreadable deck -> exit 2, never "clean"
        raise RuntimeError("could not open %s: %s" % (pptx, exc))

    ok = _resolver()
    if ok is None:
        raise RuntimeError("deckkit is not importable, so font resolution cannot be tested here")

    carried, theme_faces, unattributed = faces_in_use(prs)
    named = {face: sum(by.values()) for face, by in carried.items()}
    # `theme` lists only the theme faces JUDGED beyond `named`: the Latin ones (see the loop below).
    # It used to list every face the theme declares, and an Office theme names ~30 per-script faces,
    # so a one-face deck reported "33 face(s) checked" on both gate paths — a count of nothing.
    theme_judged = sorted(f for f, uses in theme_faces.items()
                          if f not in named and any(slot == "latin" for _s, slot in uses))
    findings, facts = [], {"named": named, "theme": theme_judged, "unresolved": [],
                           "undecidable": [], "by_slot": carried, "unattributed": unattributed,
                           "theme_declared": sorted(theme_faces)}

    def what(by):
        parts = []
        if by.get("ea"):
            parts.append("%d East-Asian" % by["ea"])
        if by.get("cs"):
            parts.append("%d complex-script" % by["cs"])
        if by.get("latin"):
            parts.append("%d Latin" % by["latin"])
        return " + ".join(parts) + " character(s)"

    for face, chars in sorted(named.items(), key=lambda kv: -kv[1]):
        good = ok(face)
        if good is None:
            facts["undecidable"].append(face)
            findings.append(("note", face,
                             "could not be tested on this machine — reported, not assumed fine"))
            continue
        if good:
            continue
        facts["unresolved"].append(face)
        shipped = face in DEFAULT_FACES
        sev = "note" if (shipped or chars < MIN_CHARS) else "block"
        if shipped:
            findings.append(("note", face,
                             "carries %s and does not resolve here, but it is one of deckkit's "
                             "SHIPPED DEFAULTS rather than a face this deck chose — an environment "
                             "fact about this host, not a defect in the deck. Every wrap/fit number "
                             "for it was still measured in a stand-in: fix with "
                             "deckkit.use_platform_fonts(), or install the face."
                             % what(carried[face])))
            continue
        cjk = carried[face].get("ea", 0)
        findings.append((sev, face,
                         "carries %s of this deck's text but does NOT resolve here — every wrap, "
                         "fit and overflow number computed for it was measured in a "
                         "metric-incompatible stand-in%s%s"
                         % (what(carried[face]),
                            "; for CJK text the stand-in need not be a CJK face at all (measured: "
                            "60% of the true width), so build with a CJK face that resolves here "
                            "— references/multilingual.md §CJK faces on macOS" if cjk else "",
                            "" if sev == "block" else " (under the %d-character floor, so "
                            "reported only)" % MIN_CHARS)))

    # A theme LATIN face is judged even when no slide run is attributed to it: it is the face for
    # chart, SmartArt and notes text this inventory does not read. An East-Asian or complex-script
    # theme face draws only its own script, so one carrying none of it draws nothing on these
    # slides and is not reported.
    for face in theme_judged:
        good = ok(face)
        if good is None:
            facts["undecidable"].append(face)
            continue
        if not good:
            facts["unresolved"].append(face)
            # 🔴 The shipped-default rule applies HERE TOO. It was written into the named-faces
            # loop above and not into this one, so a deck whose THEME names a default the host
            # lacks blocked unconditionally — and python-pptx's own default template declares
            # Calibri, which is absent from Linux. Net effect: every deck blocked on Ubuntu,
            # including this repo's CI fixtures. Three red runs, and it stayed invisible for two
            # of them because the failing assertion printed no evidence about WHICH face blocked.
            if face in DEFAULT_FACES:
                findings.append(("note", face,
                                 "is the THEME face inherited by runs with no explicit typeface "
                                 "and does not resolve here — but it is one of deckkit's SHIPPED "
                                 "DEFAULTS, an environment fact about this host rather than a "
                                 "choice this deck made. Fix with deckkit.use_platform_fonts(), "
                                 "or install the face."))
            else:
                findings.append(("block", face,
                                 "is the THEME face every run with no explicit typeface inherits, "
                                 "and it does not resolve here"))

    if unattributed["ea"] >= MIN_CHARS or unattributed["cs"] >= MIN_CHARS:
        findings.append(("note", "(no face named)",
                         "%d East-Asian and %d complex-script character(s) name no face on the "
                         "run, its paragraph, its list style or the theme — the presenting "
                         "application picks one, so nothing here knows what they were measured "
                         "as. Set deckkit.EAFONT (or the theme's script face) to decide it."
                         % (unattributed["ea"], unattributed["cs"])))
    return findings, facts


def _selftest():
    bad = []
    ok = _resolver()
    if ok is None:
        print("[fonts] selftest SKIPPED — deckkit not importable")
        return 0
    # A face that certainly does not exist must read as unresolved; one deckkit itself falls back
    # to must read as resolved. Both directions, so a resolver that always says yes fails here.
    if ok("Definitely Not A Real Face 9Z") is not False:
        bad.append("a nonexistent face did not read as unresolved")
    known = an_installed_face()
    if known is None:
        print("  note: no resolvable face found on this host — the positive direction cannot be "
              "tested here, and that is reported rather than passed over")
    elif ok(known) is False:
        bad.append("%r was reported installed and then read as unresolved" % known)
    # MIN_CHARS must actually gate: a 1-character unresolved face is a note, not a block.
    if MIN_CHARS < 2:
        bad.append("MIN_CHARS floor is too low to distinguish a stray run from body text")
    for b in bad:
        print("  ✗", b)
    print("[fonts] selftest %s" % ("FAILED" if bad else "ok"))
    return 1 if bad else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pptx", nargs="?")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--waive", default=None, help="a written reason; silences the report")
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 on a blocking finding — for a caller that owns the build AND the "
                         "gate, and therefore knows the measuring machine is this one")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return _selftest()
    if not a.pptx:
        ap.error("a deck path is required")
    try:
        findings, facts = check(a.pptx)
    except Exception as exc:
        print("[fonts] NOT CHECKED — %s" % exc)
        print("        NOT the same as clean: the faces this deck names were never tested.")
        return 2
    if a.json:
        print(json.dumps({"findings": [{"severity": s, "face": f, "why": m}
                                       for s, f, m in findings], "facts": facts}, indent=1))
    blocks = [f for f in findings if f[0] == "block"]
    if a.waive and blocks:
        print("[fonts] WAIVED — %s" % a.waive)
        for _s, f, m in findings:
            print("        %s: %s" % (f, m))
        return 0
    for s, f, m in findings:
        print("[fonts] %s %s: %s" % ("✗" if s == "block" else "•", f, m))
    if not findings:
        print("[fonts] every face this deck names resolves here (%d face(s) checked)"
              % (len(facts["named"]) + len(facts["theme"])))
    return 1 if (blocks and a.strict) else 0


if __name__ == "__main__":
    raise SystemExit(main())
