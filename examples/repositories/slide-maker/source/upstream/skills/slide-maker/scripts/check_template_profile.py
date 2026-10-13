#!/usr/bin/env python3
"""A registered template's `profile.md` must be OBEYED, not merely available.

🔴 WHY. The template registry is the one artefact in this skill that gets BETTER every time a
template is used: layout indices, the placeholders to drop, a bare decorative rectangle that must
be covered, which font the theme actually declares and whether it is installed. Measured by grep,
`profile.md` is read by `registry.py` and `deckkit.py` — both producers — and by NO check. A build
could ignore every line of it and nothing downstream would know.

Compare `check_direction_applied.py`, which exists precisely because "the look a user PICKED must
be verified against the deck that SHIPS". A template profile is the same claim with a longer
memory, and it had no such check. MEASURED, on the LKEB/LUMC template: the profile warns that the
title layout carries a bare grey rectangle which must be covered, and that the theme's Calibri
lives inside the PowerPoint app bundle on macOS so a Calibri deck is measured against a
substitute. Both are real traps, both were caught only because a human had written them down and
another human happened to read them.

HOW A PROFILE DECLARES A CONTRACT. `profile.md` stays prose — that is what makes it useful to a
reader — and gains ONE fenced block:

    ## Machine-checkable contract
    ```json
    {
      "match":       {"layout_names": ["1_Title and Content with Logo"],
                      "slide_size_in": [10.0, 5.625]},
      "layouts":     {"title": "Title Slide", "content": "1_Title and Content with Logo"},
      "fonts":       {"FONT": "Calibri"},
      "title_color": "FFFFFF",
      "must_cover":  [{"layout": "Title Slide", "rect": [7.14, 2.50, 2.54, 2.54],
                       "why": "a bare grey accent rectangle lives on the layout"}]
    }
    ```

One file, so the prose and the contract cannot drift into two truths. Every key is OPTIONAL: a
profile that declares only `match` + `fonts` is checked on fonts alone.

BINDING A DECK TO A PROFILE is by FINGERPRINT, not by trust: `match` is compared against the built
deck's own layout names and canvas size. That matters for the runtimes this skill does not
control — a Codex or Kimi run that never records which template it used still gets checked,
because the deck itself says.

🔴 A DESIGNED TEMPLATE HAS NO LAYOUT NAMES TO FINGERPRINT. Measured: 10 of the 11 registered
templates ship a `style.py` + `profile.md` and NO .pptx, so they have neither layout names nor a
canvas size — the `match` block above cannot describe them, and `declared_preset` does not know
them either (they are not among the 18 built-in presets). A deck built from one of them was checked
against its template's look by nothing at all. What those templates DO have that reaches the
pixels is a palette and a type decision, so they fingerprint on colour:

    "match":   {"palette_any": ["14181F", "34D1A6"]},
    "palette": {"expect": ["14181F", "1E242E", "ECEFF4", "C2C9D4", "7A8495", "34D1A6", "F2B04E"],
                "min_share": 0.6},
    "fonts":   {"FONT": "Helvetica Neue", "MONO": "Menlo"}

Binding takes TWO identifying colours; the check wants most of the palette. That gap is the whole
point — a deck that painted the background right and set everything else in deckkit's stock navy
binds and then fails, which is exactly the "declared it, did not build it" shape.

🔴 NO CONTRACT, NO CLAIM. A registered template with no `## Machine-checkable contract` block
reports NOT CHECKED and exits 2. "There was nothing to check" and "everything checked out" are
different sentences and this never prints the second one for the first reason.

    python3 scripts/check_template_profile.py <deck.pptx> [--profile NAME] [--json]
    python3 scripts/check_template_profile.py --selftest

Exit 0 clean · 1 findings · 2 could not run / no contract.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

EMU = 914400.0
_A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"

_P = "{http://schemas.openxmlformats.org/presentationml/2006/main}"


def qn_p(tag):
    return _P + tag


def _sp_direct_fill(sp):
    """Does this shape DECLARE a fill on its own spPr? hex / "UNKNOWN" / None (paints nothing).

    Direct children only — never `.//`. A PowerPoint placeholder routinely carries `<a:noFill/>`
    in spPr plus an `<a14:hiddenFill>` with a real colour inside `spPr/a:extLst`; that hidden fill
    is what the shape WOULD be if it were filled, i.e. explicitly not painted.
    """
    try:
        spPr = sp.find(_P + "spPr")
        if spPr is None:
            return None
        for child in spPr:
            if child.tag == _A + "noFill":
                return None
            if child.tag in (_A + "blipFill", _A + "gradFill", _A + "pattFill"):
                return "UNKNOWN"
            if child.tag == _A + "solidFill":
                srgb = child.find(_A + "srgbClr")
                return srgb.get("val").upper() if srgb is not None else "UNKNOWN"
    except Exception:
        return None
    return None


CONTRACT_RE = re.compile(
    r"^##\s*Machine-checkable contract\s*$.*?^```(?:json)?\s*$(?P<body>.*?)^```\s*$",
    re.M | re.S)


# ─────────────────────────────────────────────────────────── loading profiles

def load_profiles():
    """[(name, dir, contract_dict_or_None, profile_path), ...] across every registry root."""
    out = []
    try:
        import registry
        pairs = registry.list_templates()
    except Exception:
        return out
    for name, d in pairs:
        pf = Path(d) / "profile.md"
        if not pf.exists():
            out.append((name, Path(d), None, pf))
            continue
        try:
            m = CONTRACT_RE.search(pf.read_text(encoding="utf8", errors="replace"))
        except OSError:
            out.append((name, Path(d), None, pf))
            continue
        if not m:
            out.append((name, Path(d), None, pf))
            continue
        try:
            out.append((name, Path(d), json.loads(m.group("body")), pf))
        except json.JSONDecodeError as exc:
            # a malformed contract is a LOUD problem, never a silent "no contract"
            out.append((name, Path(d), {"__error__": str(exc)}, pf))
    return out


def _deck_facts(prs):
    names, sizes = [], (prs.slide_width / EMU, prs.slide_height / EMU)
    # `colours` is filled lazily by bind(): walking every slide's XML is wasted on the templates
    # that fingerprint on layout names, which is most of the supplied-.pptx ones.
    for lay in prs.slide_layouts:
        try:
            names.append(lay.name)
        except Exception:
            pass
    return {"layout_names": names, "slide_size_in": [round(sizes[0], 3), round(sizes[1], 3)],
            "colours": None}


def recorded_template(gates):
    """The template the record NAMES, or None — from either runtime's shape.

    🔴 WHY THIS MATTERS MORE THAN THE FINGERPRINT for a designed template. A fingerprint answers
    "which template is this deck?", which a deck that IGNORED its template cannot be asked: it has
    none of that template's colours, so it binds to nothing and the gate says NOT CHECKED. Measured:
    a stock deckkit deck claiming `modern-dark` bound to nothing by fingerprint and, bound BY NAME,
    was caught twice over (PALETTE OFF PROFILE + FONT OFF PROFILE). "Declared it and did not build
    it" is the failure this gate is for, and only the recorded name reaches it.
    """
    if not isinstance(gates, dict):
        return None
    picks = ((gates.get("interview") or {}).get("picks")
             if isinstance(gates.get("interview"), dict) else None)
    for row in (picks or []):
        if isinstance(row, dict) and str(row.get("axis") or "").strip().lower() == "template":
            val = str(row.get("value") or "").strip()
            if val and not val.startswith("<"):
                return val
    for holder in ("design_plan", "design", "content"):
        blk = gates.get(holder)
        if isinstance(blk, dict):
            val = str(blk.get("template") or "").strip()
            if val and not val.startswith("<"):
                return val
    return None


def resolve_wanted(name, profiles):
    """The registered template a recorded name refers to, or None. Tolerant on purpose: a record
    says "modern-dark" or "modern dark (registry)" or a path, and none of those should be an error
    — an unrecognised name falls back to the fingerprint rather than failing the deck."""
    if not name:
        return None
    key = re.sub(r"[^a-z0-9]+", "", str(name).lower())
    for n, _d, _c, _pf in profiles:
        if re.sub(r"[^a-z0-9]+", "", n.lower()) == key:
            return n
    for n, _d, _c, _pf in profiles:                   # "modern-dark (registry template)"
        if re.sub(r"[^a-z0-9]+", "", n.lower()) in key:
            return n
    return None


def bind(prs, profiles, want=None):
    """The profile whose `match` fingerprint fits this deck — or None. `want` forces a name."""
    facts = _deck_facts(prs)
    if want:
        for name, d, c, pf in profiles:
            if name == want:
                return (name, d, c, pf)
        return None
    best = None
    for name, d, c, pf in profiles:
        if not isinstance(c, dict) or "__error__" in c:
            continue
        match = c.get("match") or {}
        want_names = [n for n in (match.get("layout_names") or []) if n]
        if want_names and not all(n in facts["layout_names"] for n in want_names):
            continue
        size = match.get("slide_size_in")
        if size and any(abs(float(a) - float(b)) > 0.05
                        for a, b in zip(size, facts["slide_size_in"])):
            continue
        want_pal = [c.upper().lstrip("#") for c in (match.get("palette_any") or []) if c]
        if want_pal:
            if facts["colours"] is None:
                facts["colours"] = deck_colours(prs)
            hits = [c for c in want_pal if c in facts["colours"]]
            if len(hits) < len(want_pal):
                continue                              # the ground AND the ink, or it is not this one
        if not want_names and not size and not want_pal:
            continue                                  # a match-less contract binds to nothing
        score = len(want_names) + (1 if size else 0) + (2 if want_pal else 0)
        if best is None or score > best[0]:
            best = (score, (name, d, c, pf))
    return best[1] if best else None


# ─────────────────────────────────────────────────────────── the checks

def _run_colours(shape):
    out = []
    try:
        for p in shape.text_frame.paragraphs:
            for r in p.runs:
                if not (r.text or "").strip():
                    continue
                try:
                    rgb = r.font.color.rgb
                except Exception:
                    rgb = None
                out.append(str(rgb).upper() if rgb is not None else None)
    except Exception:
        pass
    return out


def unmeasurable_ground(prs):
    """Why the painted colours cannot answer 'is this the template's ground?', or None.

    🔴 TWO REAL DECKS BREAK THE ASSUMPTION, both measured. A deck whose slides are grounded in a
    FULL-BLEED PICTURE paints no ground colour at all — blueprint-tech and nvidia-dark both ship
    hero images, and a cover built that way contributed only its ink. A deck set entirely in THEME
    colours paints no explicit RGB either. In both cases "the ground colour is absent" means the
    reader cannot see it, not that the build ignored its template, and a gate that cannot tell
    those apart accuses a correct deck.
    """
    slides = list(prs.slides)
    if not slides:
        return None
    sw, sh = prs.slide_width / EMU, prs.slide_height / EMU
    covered = 0
    for slide in slides:
        for sp in slide.shapes:
            try:
                if sp.shape_type is None or "PICTURE" not in str(sp.shape_type):
                    continue
                if (sp.width / EMU) >= 0.92 * sw and (sp.height / EMU) >= 0.92 * sh:
                    covered += 1
                    break
            except Exception:
                continue
    if covered >= max(1, int(round(0.8 * len(slides)))):
        return ("%d of %d slides are grounded in a full-bleed picture, so no fill declares the "
                "ground colour" % (covered, len(slides)))
    if not deck_colours(prs):
        return "this deck declares no explicit RGB at all — its colours come from the theme"
    return None


def deck_colours(prs):
    """Every explicit RGB the deck paints — fills, lines and text alike, as upper-case hex.

    Read from `srgbClr` elements rather than from python-pptx accessors: a designed template sets
    its palette through deckkit, which writes explicit RGB, and walking the XML catches the colour
    wherever it landed (a box fill, a rule, a run) without a per-shape-type reader for each.
    """
    seen = {}
    for slide in prs.slides:
        for el in slide._element.iter(_A + "srgbClr"):
            v = (el.get("val") or "").upper()
            if len(v) == 6:
                seen[v] = seen.get(v, 0) + 1
    return seen


def _dominant_face(prs):
    counts = {}
    for slide in prs.slides:
        for r in slide._element.iter(_A + "r"):
            t = r.find(_A + "t")
            n = len(t.text or "") if t is not None else 0
            rPr = r.find(_A + "rPr")
            if not n or rPr is None:
                continue
            el = rPr.find(_A + "latin")
            face = el.get("typeface") if el is not None else None
            if face and not face.startswith("+"):
                counts[face] = counts.get(face, 0) + n
    return max(counts, key=counts.get) if counts else None


def check(pptx, want=None, gates=None):
    """(findings, facts). findings = [(code, message), ...]. Raises when it cannot run.

    `want` forces a template by name; `gates` lets the RECORD name it, which is the only path that
    catches a deck that declared a template and then ignored it.
    """
    from pptx import Presentation
    prs = Presentation(pptx)
    profiles = load_profiles()
    if not profiles:
        raise RuntimeError("no template profiles are registered (scripts/registry.py --list)")
    if want is None and gates is not None:
        want = resolve_wanted(recorded_template(gates), profiles)
    bound = bind(prs, profiles, want=want)
    if bound is None:
        # A profile with no contract block has no `match` fingerprint either — the fingerprint
        # lives IN the contract — so it is genuinely unbindable rather than merely unchecked.
        # Saying which registered templates are in that state is the actionable half: "no template
        # matched" and "the template that would have matched declares nothing checkable" lead to
        # different next moves, and only one of them is the reader's to fix.
        mute = [n for n, _d, c, _pf in profiles if c is None]
        hint = ("" if not mute else
                " — note that %s registered template(s) declare no `## Machine-checkable contract` "
                "block and therefore cannot be matched at all: %s"
                % (len(mute), ", ".join(sorted(mute))))
        raise RuntimeError(
            "this deck matches no registered template profile's `match` fingerprint" + hint)
    name, _d, contract, pf = bound
    if contract is None:
        raise RuntimeError(
            "template %r has a profile.md but NO `## Machine-checkable contract` block, so nothing "
            "about it can be verified against the built deck (%s)" % (name, pf))
    if "__error__" in contract:
        raise RuntimeError("template %r has a malformed contract block: %s"
                           % (name, contract["__error__"]))

    finds, facts = [], {"template": name, "profile": str(pf), "checked": []}

    # 1 ─ the layouts the profile names must be the layouts the deck actually uses
    want_layouts = contract.get("layouts") or {}
    if want_layouts:
        facts["checked"].append("layouts")
        allowed = {v for v in want_layouts.values() if isinstance(v, str)}
        used = {}
        for i, slide in enumerate(prs.slides, 1):
            try:
                used.setdefault(slide.slide_layout.name, []).append(i)
            except Exception:
                pass
        facts["layouts_used"] = used
        if allowed:
            stray = {k: v for k, v in used.items() if k not in allowed}
            if stray:
                finds.append(("LAYOUT OFF PROFILE",
                              "slides %s use layout(s) the profile does not name (%s). The profile "
                              "records which layouts carry this template's branding; anything else "
                              "is an untested surface."
                              % (", ".join(str(n) for v in stray.values() for n in sorted(v)),
                                 ", ".join(sorted(stray)))))

    # 1b ─ the PALETTE a designed template is, since it has no layouts to be off
    want_pal = contract.get("palette") or {}
    core = [c.upper().lstrip("#") for c in (want_pal.get("core") or []) if c]
    accents = [c.upper().lstrip("#") for c in (want_pal.get("accents") or []) if c]
    expect = [c.upper().lstrip("#") for c in (want_pal.get("expect") or []) if c]
    if core or accents:
        blind = unmeasurable_ground(prs)
        if blind:
            facts["palette_not_checked"] = blind
        facts["checked"].append("palette" if not blind else "palette (NOT measurable)")
        painted = deck_colours(prs)
        core_missing = [c for c in core if c not in painted]
        accent_hits = [c for c in accents if c in painted]
        facts["palette"] = {"core": core, "core_missing": core_missing,
                            "accents_present": accent_hits,
                            "coverage": "%d/%d" % (len([c for c in expect if c in painted]),
                                                   len(expect)) if expect else None}
        # 🔴 STRUCTURAL, not a share. MEASURED: a 4-slide deck built with modern-dark's own api
        # painted 7 of its 11 declared colours — a "60% of the palette" floor would fire on a
        # correct deck one slide shorter, because a short deck has no reason to reach the third
        # accent or the raised panel. The ground and the ink it cannot avoid.
        if blind:
            pass                                      # say nothing rather than accuse — see above
        elif core_missing:
            finds.append(("PALETTE OFF PROFILE",
                          "this deck paints none of %s — the ground and the text colour are the "
                          "two a deck built from this template cannot avoid. A deck that declared "
                          "the template and then built in stock colours is the 'declared it, did "
                          "not build it' shape this gate exists for."
                          % ", ".join("#" + c for c in core_missing)))
        elif accents and not accent_hits and not blind:
            finds.append(("PALETTE OFF PROFILE",
                          "the ground and ink match but NOT ONE of this template's %d accent "
                          "colours (%s) appears. The accents are what make it this template rather "
                          "than a grey rectangle in its ground colour."
                          % (len(accents), ", ".join("#" + c for c in accents[:5]))))

    # 2 ─ the font the profile decided on
    want_fonts = contract.get("fonts") or {}
    if want_fonts.get("FONT"):
        facts["checked"].append("fonts")
        dom = _dominant_face(prs)
        facts["dominant_face"] = dom
        if dom and dom != want_fonts["FONT"]:
            finds.append(("FONT OFF PROFILE",
                          "the profile decided FONT=%r for this template and the deck is set in "
                          "%r. A template's type decision is the part a later deck is most likely "
                          "to re-litigate by accident." % (want_fonts["FONT"], dom)))

    # 3 ─ the title colour the profile requires on the branded band
    want_title = (contract.get("title_color") or "").upper().lstrip("#")
    if want_title:
        facts["checked"].append("title_color")
        bad = []
        for i, slide in enumerate(prs.slides, 1):
            try:
                title = slide.shapes.title
            except Exception:
                title = None
            if title is None or not (title.text_frame.text or "").strip():
                continue
            cols = [c for c in _run_colours(title) if c]
            if cols and all(c != want_title for c in cols):
                bad.append((i, cols[0]))
        facts["title_colors"] = bad
        if bad:
            finds.append(("TITLE COLOUR OFF PROFILE",
                          "the profile requires #%s on this template's title band; slide(s) %s set "
                          "the title in another colour (%s). On a coloured band this is the "
                          "difference between a readable title and an invisible one."
                          % (want_title, ", ".join(str(n) for n, _ in bad),
                             ", ".join(sorted({c for _, c in bad})))))

    # 4 ─ decorative furniture the profile says the BUILD must cover
    covers = contract.get("must_cover") or []
    if covers:
        facts["checked"].append("must_cover")
        uncovered = []
        for spec in covers:
            rect = spec.get("rect") or []
            if len(rect) != 4:
                continue
            rx, ry, rw, rh = (float(v) for v in rect)
            lay_name = spec.get("layout")
            area = max(rw * rh, 1e-6)
            for i, slide in enumerate(prs.slides, 1):
                try:
                    if lay_name and slide.slide_layout.name != lay_name:
                        continue
                except Exception:
                    continue
                best = 0.0
                for sh in slide.shapes:
                    # 🔴 Only a shape that actually PAINTS can cover anything. An empty text box
                    # overlapping the rect satisfies a naive containment test and covers nothing —
                    # caught in this checker's own test, which "covered" the LKEB grey block with a
                    # transparent textbox and passed. A picture counts; an <p:sp> counts only when
                    # it declares a real fill.
                    try:
                        el = sh._element
                        if el.tag == qn_p("pic"):
                            pass
                        elif el.tag == qn_p("sp"):
                            if _sp_direct_fill(el) is None:
                                continue
                        else:
                            continue          # graphicFrame/group: cannot confirm it paints
                        l, t = sh.left / EMU, sh.top / EMU
                        w, h = sh.width / EMU, sh.height / EMU
                    except (TypeError, AttributeError):
                        continue
                    ix = max(0.0, min(l + w, rx + rw) - max(l, rx))
                    iy = max(0.0, min(t + h, ry + rh) - max(t, ry))
                    best = max(best, ix * iy / area)
                if best < 0.9:
                    uncovered.append((i, spec.get("why") or "declared furniture", round(best, 2)))
        facts["uncovered"] = uncovered
        if uncovered:
            finds.append(("UNCOVERED TEMPLATE FURNITURE",
                          "; ".join("slide %d leaves %s exposed (%.0f%% covered)"
                                    % (n, why, frac * 100) for n, why, frac in uncovered)
                          + ". The profile records it because it cannot be deleted from a layout "
                            "— it has to be covered by the build."))
    if not facts["checked"]:
        raise RuntimeError("template %r declares a contract block with no checkable keys" % name)
    return finds, facts


def _selftest():
    bad = []
    body = '{"match": {"layout_names": ["X"]}, "fonts": {"FONT": "Calibri"}}'
    doc = "# t\n\nprose\n\n## Machine-checkable contract\n```json\n%s\n```\n\nmore prose\n" % body
    m = CONTRACT_RE.search(doc)
    if not m:
        bad.append("the contract block was not found in a normal profile.md")
    elif json.loads(m.group("body")).get("fonts", {}).get("FONT") != "Calibri":
        bad.append("the contract block parsed to the wrong value")
    if CONTRACT_RE.search("# t\n\nprose only, no contract\n"):
        bad.append("a profile with NO contract block was read as having one")
    # a contract with no `match` must bind to nothing rather than to everything
    class _P:
        slide_width = int(10 * EMU); slide_height = int(5.625 * EMU)
        slide_layouts = []
    if bind(_P(), [("x", Path("."), {"fonts": {"FONT": "A"}}, Path("p"))]) is not None:
        bad.append("a contract with no `match` fingerprint bound to a deck anyway")
    for b in bad:
        print("  ✗", b)
    print("[template-profile] selftest %s" % ("FAILED" if bad else "ok"))
    return 1 if bad else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pptx", nargs="?")
    ap.add_argument("--profile", default=None, help="force a template name instead of fingerprinting")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return _selftest()
    if not a.pptx:
        ap.error("a deck path is required")
    try:
        finds, facts = check(a.pptx, want=a.profile)
    except Exception as exc:
        print("[template-profile] NOT CHECKED — %s" % exc)
        print("        NOT the same as clean.")
        return 2
    if a.json:
        print(json.dumps({"findings": [{"code": c, "why": m} for c, m in finds],
                          "facts": facts}, indent=1))
    for c, m in finds:
        print("[template-profile] ✗ %s: %s" % (c, m))
    if not finds:
        print("[template-profile] %r honoured — checked: %s"
              % (facts["template"], ", ".join(facts["checked"])))
    return 1 if finds else 0


if __name__ == "__main__":
    raise SystemExit(main())
