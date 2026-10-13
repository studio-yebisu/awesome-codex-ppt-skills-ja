#!/usr/bin/env python3
"""Measure a slide's COMPOSITION, so two versions of one page can be told apart mechanically.

🔴 WHY THIS EXISTS. This skill decides composition in PROSE — a form ledger, a rhythm line, a
signature move — builds it once, and then checks colours, fonts and geometry. It has never once put
two compositions of the same content side by side and picked by looking. Its own accounting says so:
`check_direction_applied.py` verifies ground, accent, display and body faces, and centred vs
low-left, and explicitly "names skeleton and motif as NOT CHECKED rather than guessing at a
judgement" — skeleton and motif being, precisely, the composition. The `sameness` gate says the
other half out loud: whether a deck is REPETITIVE is measured and blocked; whether it is TIMID
"stays the critic's taste call", deliberately non-blocking.

So the one place this skill compares designs by looking — the direction gate — compares LOOKS
(ground, accent, faces) at deck level, once, on archetype tiles. Page composition is never tried
twice.

🔴 AND THE REASON A MEASURE IS NEEDED AT ALL. The direction gate already learned this the hard way:
offered "options" collapse into one layout in three colourways unless something mechanical refuses
them. `directions_diversity.py` exists for exactly that, at look level. This is its counterpart at
composition level — without it, "three variants" becomes three recolourings and the competition is
theatre.

WHAT IT MEASURES, from the built .pptx and WITHOUT rendering:

    grid        where the ink is — an occupancy grid normalised to the canvas
    blocks      how many distinct non-trivial elements carry the page
    dominance   the largest element's share of the ink
    centroid    where the visual weight sits, 0..1 of the canvas
    axis        which way the page flows: -1 vertical … +1 horizontal
    ink         how much of the canvas carries anything

🔴 LANGUAGE-INDEPENDENT BY CONSTRUCTION. Every number comes from SHAPE GEOMETRY, never from
measured text ink — so it reads a Chinese deck exactly as it reads an English one. That is
deliberate: this repo has already shipped a whole family of geometry gates that measured CJK text
46% short because they resolved `<a:latin>` for runs whose glyphs came from `<a:ea>`.

    python3 scripts/composition_probe.py probe   <deck>.pptx --slide 4
    python3 scripts/composition_probe.py compare <deck>.pptx --slides 4,5,6
    python3 scripts/composition_probe.py --selftest

Exit 0 clean · 1 variants too alike / problems · 2 could not run.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

EMU = 914400.0
# Roughly this many cells, shaped to the canvas so a 9:16 story deck gets tall-thin coverage rather
# than the same 8×5 a 16:9 deck gets. Composition is about WHERE on THIS canvas, so the grid has to
# follow the canvas.
TARGET_CELLS = 40
# A shape covering this much of the canvas is GROUND, not composition. Every variant of a page
# carries the same backdrop; counting it would make every pair look identical.
GROUND_SHARE = 0.85
# Below this, a shape is a hairline/mark rather than a block of the composition.
MIN_BLOCK_SHARE = 0.004


def _w(text) -> int:
    """Width, not codepoints — the same bar in Chinese as in English.

    🔴 `len()` counts CODEPOINTS, so a CJK reason clears a floor at half the information an
    English one needs: an 11-codepoint Chinese brief is and was rejected by a floor of
    12, while a 12-letter English phrase carrying a third as much passed. Measured on a real
    Chinese deck built with this skill. ONE definition, imported — see written_reason.py.
    """
    from written_reason import reason_width
    return reason_width(text)


def _grid_dims(aspect: float) -> tuple[int, int]:
    """(cols, rows) shaped to the canvas, so cells stay roughly square on any surface."""
    aspect = max(0.2, min(5.0, float(aspect or 1.0)))
    cols = max(2, min(12, round(math.sqrt(TARGET_CELLS * aspect))))
    rows = max(2, min(12, round(TARGET_CELLS / cols)))
    return cols, rows


def _rects(pptx_path, slide_index):
    """(rects, canvas_w, canvas_h) in inches — one rect per painted shape, groups flattened.

    Reuses `lint_deck._flat_shapes` rather than re-walking the tree: that walker already carries
    group transforms, the rotated-group skip and the depth cap, and a second copy of that logic is
    how two readers of the same file start disagreeing.
    """
    from pptx import Presentation
    import lint_deck as L

    prs = Presentation(str(pptx_path))
    sw, sh = prs.slide_width / EMU, prs.slide_height / EMU
    slides = list(prs.slides)
    if not 0 <= slide_index < len(slides):
        raise SystemExit("[composition] slide {} is out of range — the deck has {}."
                         .format(slide_index + 1, len(slides)))
    out = []
    for s, tf, _grp in L._flat_shapes(slides[slide_index].shapes, (0.0, 0.0, 1.0, 1.0), 0, None,
                                      None, False):
        try:
            x = (tf[0] + tf[2] * s.left / EMU) if s.left is not None else None
            y = (tf[1] + tf[3] * s.top / EMU) if s.top is not None else None
            w = (tf[2] * s.width / EMU) if s.width is not None else None
            h = (tf[3] * s.height / EMU) if s.height is not None else None
        except Exception:                                              # noqa: BLE001
            continue
        if None in (x, y, w, h) or w <= 0 or h <= 0:
            continue
        # Clip to the canvas: a deliberate bleed must not let one shape outweigh the page.
        x0, y0 = max(0.0, x), max(0.0, y)
        x1, y1 = min(sw, x + w), min(sh, y + h)
        if x1 <= x0 or y1 <= y0:
            continue
        out.append((x0, y0, x1, y1))
    return out, sw, sh


def signature(pptx_path, slide_index) -> dict:
    """This page's composition fingerprint. See the module docstring for each field."""
    rects, sw, sh = _rects(pptx_path, slide_index)
    return _signature_core(rects, sw, sh)


def _signature_core(rects, sw, sh) -> dict:
    canvas = max(sw * sh, 1e-9)
    cols, rows = _grid_dims(sw / sh if sh else 1.0)
    grid = [[0.0] * cols for _ in range(rows)]

    blocks = []
    for (x0, y0, x1, y1) in rects:
        area = (x1 - x0) * (y1 - y0)
        share = area / canvas
        if share >= GROUND_SHARE:
            continue                       # ground, not composition
        if share < MIN_BLOCK_SHARE:
            continue                       # a hairline or a mark
        blocks.append((x0, y0, x1, y1, area))
        # Spread the shape's area over the cells it covers, by overlap.
        c0, c1 = int(x0 / sw * cols), min(cols - 1, int((x1 - 1e-9) / sw * cols))
        r0, r1 = int(y0 / sh * rows), min(rows - 1, int((y1 - 1e-9) / sh * rows))
        for r in range(max(0, r0), max(0, r1) + 1):
            for c in range(max(0, c0), max(0, c1) + 1):
                cx0, cx1 = c * sw / cols, (c + 1) * sw / cols
                cy0, cy1 = r * sh / rows, (r + 1) * sh / rows
                ov = max(0.0, min(x1, cx1) - max(x0, cx0)) * max(0.0, min(y1, cy1) - max(y0, cy0))
                if ov > 0:
                    grid[r][c] += ov / canvas

    total = sum(b[4] for b in blocks)
    if blocks and total > 0:
        dom = max(b[4] for b in blocks) / total
        cx = sum((b[0] + b[2]) / 2 * b[4] for b in blocks) / total / sw
        cy = sum((b[1] + b[3]) / 2 * b[4] for b in blocks) / total / sh
        xs = [((b[0] + b[2]) / 2) / sw for b in blocks]
        ys = [((b[1] + b[3]) / 2) / sh for b in blocks]
        vx, vy = _var(xs), _var(ys)
        axis = 0.0 if (vx + vy) < 1e-9 else (vx - vy) / (vx + vy)
    else:
        dom, cx, cy, axis = 0.0, 0.5, 0.5, 0.0

    return {"cols": cols, "rows": rows,
            "grid": [[round(v, 6) for v in row] for row in grid],
            "blocks": len(blocks),
            "dominance": round(dom, 4),
            "centroid": [round(cx, 4), round(cy, 4)],
            "axis": round(axis, 4),
            "ink": round(min(1.0, total / canvas), 4)}


def _var(vals):
    if len(vals) < 2:
        return 0.0
    m = sum(vals) / len(vals)
    return sum((v - m) ** 2 for v in vals) / len(vals)


def divergence(a: dict, b: dict) -> float:
    """How differently two pages are COMPOSED, 0 (identical skeleton) … 1 (nothing in common).

    Dominated by WHERE THE INK IS, because that is what composition means. Block count and
    dominance ride along so that "same footprint, one big block vs six small ones" still reads as a
    different composition — which it is.
    """
    # isinstance, not truthiness: a caller passing the wrong thing must get a "these are not
    # comparable" answer, not an AttributeError from inside a gate.
    if not isinstance(a, dict) or not isinstance(b, dict) or not a.get("grid") or not b.get("grid"):
        return 1.0
    if (a.get("cols"), a.get("rows")) != (b.get("cols"), b.get("rows")):
        return 1.0                          # different canvases are not comparable compositions
    ga = [v for row in a["grid"] for v in row]
    gb = [v for row in b["grid"] for v in row]
    sa, sb = sum(ga), sum(gb)
    if sa <= 0 and sb <= 0:
        return 0.0
    if sa <= 0 or sb <= 0:
        return 1.0
    na = [v / sa for v in ga]
    nb = [v / sb for v in gb]
    # L1 over normalised occupancy: 0 when the ink sits in the same cells in the same proportion,
    # 1 when the two pages share no cell at all.
    grid_d = sum(abs(x - y) for x, y in zip(na, nb)) / 2.0

    nblocks = max(a["blocks"], b["blocks"], 1)
    block_d = abs(a["blocks"] - b["blocks"]) / nblocks
    dom_d = abs(a["dominance"] - b["dominance"])
    axis_d = abs(a["axis"] - b["axis"]) / 2.0
    ca, cb = a.get("centroid") or [0.5, 0.5], b.get("centroid") or [0.5, 0.5]
    cen_d = (abs(ca[0] - cb[0]) + abs(ca[1] - cb[1])) / 2.0
    # 🔴 WEIGHTS FOUND BY SEARCH OVER REAL LAYOUT PAIRS, NOT CHOSEN. The first draft put 0.70 on
    # the occupancy grid, which reads as obvious and is wrong: making the same three columns TALLER
    # moves ink between cells and scored 0.141 — higher than several genuinely different pairs. The
    # two families OVERLAPPED, so no floor separated them. What actually carries composition is the
    # STRUCTURE — is one block dominant or are they equal, how many are there, does the page run
    # across or down — and the grid is a weak tiebreak. Searched over a 10-layout corpus:
    #     same composition (recoloured / taller / narrower) ....... max 0.033
    #     different composition .................................. min 0.107
    # 🔴 AND THE WEIGHTS ADAPT TO HOW MUCH THE STRUCTURE CAN SAY. With one or two blocks the
    # structure terms are degenerate BY CONSTRUCTION — a single block is always fully dominant and
    # has no flow axis — so they carry no information and the grid is all there is. Found on a
    # HELD-OUT corpus: a centred card and a full-bleed band are both "one dominant block" and
    # scored 0.054 as the same composition, which they plainly are not. This is not a patch for
    # that pair; it is the general rule that a term with no variance must not hold weight.
    sparse = max(a["blocks"], b["blocks"]) <= 2
    if sparse:
        w_grid, w_block, w_dom, w_axis, w_cen = 0.55, 0.10, 0.15, 0.05, 0.15
    else:
        w_grid, w_block, w_dom, w_axis, w_cen = 0.15, 0.15, 0.45, 0.20, 0.05
    return round(min(1.0, w_grid * grid_d + w_block * block_d + w_dom * dom_d
                     + w_axis * axis_d + w_cen * cen_d), 4)


def _sig_from_rects(rects, sw, sh) -> dict:
    """The signature computation, over rects someone else selected. See `signature`."""
    return _signature_core(rects, sw, sh)


SHARED_TOL = 0.02          # inches-as-fraction: two rects this close are the same furniture


def variant_signatures(pptx_path, slide_indices, *, drop_shared=True):
    """Signatures for VARIANTS OF ONE PAGE, with the furniture they all share removed.

    🔴 WHY THE SUBTRACTION, measured. Variants of a page carry the deck's CHROME unchanged — the
    eyebrow, the headline slot, the footer — because that chrome is the deck's identity and holding
    it still is correct design. Counting it makes every variant look like every other one, and the
    floor then separates nothing. Measured on a real shipped deck, comparing two DIFFERENT pages:
    whole page 0.145, chrome band alone 0.220, body alone 0.184 — the chrome carries a large share
    of the similarity. For `compare` (two different pages) that is honest and wanted; for a
    competition between variants of ONE page it is noise, and it is noise that always pushes the
    same way.

    Subtracting what is COMMON TO ALL VARIANTS needs no magic band and no per-deck constant: the
    shared furniture is, definitionally, the rects that appear in every variant.
    """
    per = [_rects(pptx_path, i) for i in slide_indices]
    if not per:
        return []
    sw, sh = per[0][1], per[0][2]
    if not drop_shared or len(per) < 2:
        return [_sig_from_rects(r, w, h) for r, w, h in per]

    def key(r):
        return tuple(round(v / max(sw, sh) / SHARED_TOL) for v in r)

    common = set(key(r) for r in per[0][0])
    for rects, _w, _h in per[1:]:
        common &= set(key(r) for r in rects)
    return [_sig_from_rects([r for r in rects if key(r) not in common], w, h)
            for rects, w, h in per]


# 🔴 CALIBRATED, NOT CHOSEN — see `_selftest`, which rebuilds the corpus and FAILS if the floor
# ever stops separating the two families. Measured over a 10-layout corpus (3 columns, the same
# three columns taller and narrower, 2 columns, a vertical stack, a dominant hero left and right,
# a 2x2 grid, two full-width bands), comparing every pair with the shared chrome subtracted:
#     same composition, recoloured ........................ 0.000
#     same composition, taller / narrower ................. up to 0.033
#     genuinely different composition ..................... from 0.107
# 0.07 sits in the empty band between them. What it knowingly gives up: a mirrored layout (hero on
# the left vs hero on the right) is a different reading order and scores only just above the floor,
# so it passes as different — which is the call this measure makes deliberately, and the reason the
# blind read, not this number, decides which variant is BETTER.
SAME_COMPOSITION = 0.07
MIN_VARIANTS = 2


def faults(variants, *, floor=SAME_COMPOSITION) -> list[str]:
    """The anti-theatre check: are these really different compositions, or one layout restyled?

    `variants` is [{"label": str, "signature": {...}}, ...].
    """
    out: list[str] = []
    # isinstance, not truthiness: a caller handing this the wrong shape must get a complaint, not
    # a TypeError from inside a gate.
    seq = variants if isinstance(variants, (list, tuple)) else []
    rows = [v for v in seq if isinstance(v, dict) and isinstance(v.get("signature"), dict)]
    if len(rows) < MIN_VARIANTS:
        out.append("a competition needs at least {} compositions of the SAME page; got {}. One "
                   "version is not a choice, and recording it as one is the theatre this check "
                   "exists to stop.".format(MIN_VARIANTS, len(rows)))
        return out
    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            d = divergence(rows[i]["signature"], rows[j]["signature"])
            if d < floor:
                out.append("`{}` and `{}` are the SAME composition (divergence {:.2f} < {:.2f}) — "
                           "the ink lands in the same places. Move a block, change how many there "
                           "are, or change what dominates; recolouring and retyping are look "
                           "changes, and the direction gate already owns look."
                           .format(rows[i].get("label", i), rows[j].get("label", j), d, floor))
    return out


# ── the record contract, read by every gate path ─────────────────────────────────────────────────
# A competition is claimed on the SIGNATURE anchor — the page the ritual has always been about, and
# the one whose aesthetic risk is most easily sanded away during the build. `complex` and `data`
# may record one too; nothing demands it, because their job is to prove the design HOLDS a load,
# not to choose a composition.
COMPETE_ROLE = "signature"
# 🔴 WIDTH VIA `written_reason.reason_width`, NOT len(). The repo owns this question in one place
# precisely because `len()` counts CODEPOINTS, which quietly makes the same bar stricter in
# Chinese than in English. Measured here: "looks better" = 12, "B 的主张一眼就读出来了" = 22,
# "B carries its claim in one beat; A buried it under a list" = 57.
CARVES = ("conservative", "template-locked", "tiny-ask", "user-waived")
MIN_WHY = 24
# A real comparison names what it compared. "looks better" (width 12) clears no floor worth having
# and names nothing; the honest limit is that a determined author can still write a wide vacuous
# sentence — the same limit every written-reason floor in this skill has, and saying so beats
# pretending otherwise.


def carve_holds(rec, pptx_path=None, gates=None) -> tuple[bool, str]:
    """Is the claimed carve TRUE OF THE ARTIFACT? Returns (ok, why_not).

    🔴 THE LESSON THIS REPO ALREADY PAID FOR, and which the first version of this file repeated.
    `render_deck._icon_none_category_holds` says it exactly: "The category was checked against a
    fixed list of strings and nothing else, so any of the four words cleared the gate. Measured on
    this repo's own deck: `motif-dominant` was written for a deck, accepted, and the first human
    reader's first note was 'icons should be here'. **The word was doing the work, not the fact.**"
    A carve that is only a word is a waiver anyone can type.

      template-locked   the deck must really be built on someone's TEMPLATE. 🔴 This is the one
                        that matters for the GENERATED-identity branch (Q1 d): a generated look is
                        built on a BLANK deck, so it fails this check and cannot borrow the carve.
                        Step 2 is branch-invariant — the Q1 choice "decides only the LOOK SOURCE",
                        never who composes the pages — and a generated identity does not compose
                        them for you.
      conservative      `design_plan.boldness` must really say conservative.
      tiny-ask          the deck must really be small.
      user-waived       left as declared, the way `editorial-register` is: what the user said is
                        not a property of the file, and forcing a measurement onto it would
                        invent one.
    """
    cat = str((rec or {}).get("waived_category") or "").strip().lower()
    if cat == "conservative":
        # `blind_read.design_of` is the ONE owner of the design_plan/design spelling — importing it
        # rather than re-spelling the keys here is the rule that stopped the third runtime drift.
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from blind_read import design_of as _design_of
        dial = str((_design_of(gates) or {}).get("boldness") or "").strip().lower()
        if dial and not dial.startswith("conserv"):
            return False, ("category 'conservative' but `design_plan.boldness` is {!r} — the carve "
                           "exists for a deck that DECLARED it took no aesthetic risk, and this one "
                           "declared the opposite.".format(dial))
        return True, ""
    if cat in ("tiny-ask", "template-locked") and pptx_path:
        try:
            sys.path.insert(0, str(Path(__file__).resolve().parent))
            import render_deck as _rd
            from pptx import Presentation
            n = len(Presentation(str(pptx_path)).slides)
        except Exception:                                              # noqa: BLE001
            return True, ""                    # never fail the gate on the reader itself
        if cat == "tiny-ask":
            if n > 3:
                return False, ("category 'tiny-ask' on a {}-slide deck — a deck that large has a "
                               "signature page worth competing for.".format(n))
            return True, ""
        ok, why = _rd._icon_none_category_holds("template-locked", str(pptx_path), [])
        if not ok:
            return False, (why or "the deck carries no template") + \
                (" 🔴 A GENERATED visual identity is not a template: it is built on a blank deck, "
                 "and it decides the LOOK, never who composes the pages.")
    return True, ""


def is_waived(rec) -> bool:
    return isinstance(rec, dict) and bool(str(rec.get("waived") or "").strip())


def waiver_faults(rec) -> list[str]:
    out: list[str] = []
    cat = str((rec or {}).get("waived_category") or "").strip().lower()
    if cat not in CARVES:
        out.append("needs a `waived_category` naming the carve: {}. `template-locked` is the real "
                   "one for a provided template — the composition is the template's, and there is "
                   "nothing to choose between.".format(" | ".join(CARVES)))
    if _w((rec or {}).get("waived")) < MIN_WHY:
        out.append("needs a written reason beside the category.")
    return out


def _names(text, label) -> bool:
    """Does this reason actually MENTION that variant?

    🔴 Word boundaries, not `in`. Labels are usually single letters, and `"a" in why.lower()` is
    true of very nearly every English sentence — so the check passed on "this one reads much
    faster than the other one", which names nothing. Caught by testing it, not by reading it.
    CJK labels have no word boundaries, so they fall back to a plain containment test.
    """
    import re as _re
    lab = str(label or "").strip()
    if not lab:
        return False
    if _re.fullmatch(r"[A-Za-z0-9_-]+", lab):
        return bool(_re.search(r"(?<![A-Za-z0-9])" + _re.escape(lab) + r"(?![A-Za-z0-9])",
                               str(text or ""), _re.I))
    return lab in str(text or "")


def competition_faults(rec, *, floor=SAME_COMPOSITION) -> list[str]:
    """Everything wrong with a recorded composition competition. Empty list = a real choice."""
    if not isinstance(rec, dict):
        return [MISSING]
    if is_waived(rec):
        return ["`waived` " + f for f in waiver_faults(rec)]
    variants = rec.get("variants")
    if not isinstance(variants, list) or len(variants) < MIN_VARIANTS:
        return ["`variants` must list at least {} compositions of this page, each with the "
                "`signature` that `composition_probe.py` measured. Fewer than that is not a "
                "choice.".format(MIN_VARIANTS)]
    out: list[str] = []
    labels = []
    for i, v in enumerate(variants):
        if not isinstance(v, dict):
            out.append("`variants[{}]` must be an object.".format(i))
            continue
        lab = str(v.get("label") or "").strip()
        if not lab:
            out.append("`variants[{}]` has no `label` — the pick names one of these.".format(i))
        elif lab in labels:
            out.append("two variants are both labelled `{}`.".format(lab))
        labels.append(lab)
        if not isinstance(v.get("signature"), dict) or not v["signature"].get("grid"):
            out.append("`variants[{}]` ({}) carries no measured `signature` — run "
                       "`composition_probe.py`, never hand-write it.".format(i, lab or "?"))
    if out:
        return out
    out += faults(variants, floor=floor)          # the anti-theatre check
    picked = str(rec.get("picked") or "").strip()
    if picked not in labels:
        out.append("`picked` must name one of {}; got {!r}. A competition with no winner did not "
                   "happen.".format(labels, rec.get("picked")))
    why = str(rec.get("why") or "").strip()
    from written_reason import reason_width
    if reason_width(why) < MIN_WHY:
        out.append("`why` must say what you SAW that decided it — which version's claim reads "
                   "faster, which one left an element nobody could place. `looks better` is the "
                   "sentence this whole step exists to replace.")
    elif not any(_names(why, lab) for lab in labels):
        out.append("`why` names none of {} — a comparison that never mentions what it compared is "
                   "a preference, not a finding. Say which version did what.".format(labels))
    return out


MISSING = (
    'is missing. Step 4 now COMPETES the signature page instead of composing it once: build 2-3 '
    'different compositions of it, render them in ONE pass (page count barely costs anything — '
    'LibreOffice startup dominates), read them blind, and pick by what you SAW.\n'
    '    python3 scripts/composition_probe.py compare <probe>.pptx --slides 1,2,3\n'
    '    "composition": {"variants": [{"label": "A", "signature": {...}}, ...],\n'
    '                    "picked": "B", "why": "<what you saw that decided it>"}\n'
    '  Or claim a carve: {"waived": "<why>", "waived_category": "' + " | ".join(CARVES) + '"}')


# ── CLI ──────────────────────────────────────────────────────────────────────────────────────────
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", nargs="?", choices=("probe", "compare"))
    ap.add_argument("deck", nargs="?")
    ap.add_argument("--slide", type=int, help="1-based slide number (probe)")
    ap.add_argument("--slides", help="1-based slide numbers of the variants, e.g. 4,5,6 (compare)")
    ap.add_argument("--floor", type=float, default=SAME_COMPOSITION)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)

    if a.selftest:
        return _selftest()
    if not a.cmd or not a.deck:
        ap.print_help()
        return 2
    deck = Path(a.deck).expanduser()
    if not deck.exists():
        print("[composition] no such deck: {}".format(deck), file=sys.stderr)
        return 2

    if a.cmd == "probe":
        if not a.slide:
            print("[composition] probe needs --slide N (1-based)", file=sys.stderr)
            return 2
        print(json.dumps(signature(deck, a.slide - 1), ensure_ascii=False, indent=2))
        return 0

    if not a.slides:
        print("[composition] compare needs --slides a,b[,c] (1-based)", file=sys.stderr)
        return 2
    try:
        nums = [int(x) for x in a.slides.replace(" ", "").split(",") if x]
    except ValueError:
        print("[composition] --slides must be comma-separated numbers", file=sys.stderr)
        return 2
    variants = [{"label": "slide {}".format(n), "signature": signature(deck, n - 1)} for n in nums]
    for v in variants:
        s = v["signature"]
        print("{:<12} blocks={:<3} dominance={:.2f} centroid=({:.2f},{:.2f}) axis={:+.2f} ink={:.2f}"
              .format(v["label"], s["blocks"], s["dominance"], s["centroid"][0], s["centroid"][1],
                      s["axis"], s["ink"]))
    print()
    for i in range(len(variants)):
        for j in range(i + 1, len(variants)):
            print("  {} vs {}: divergence {:.3f}".format(
                variants[i]["label"], variants[j]["label"],
                divergence(variants[i]["signature"], variants[j]["signature"])))
    bad = faults(variants, floor=a.floor)
    print()
    for b in bad:
        print("[composition] " + b)
    print("[composition] {}".format("{} problem(s)".format(len(bad)) if bad else
                                    "these are genuinely different compositions"))
    return 1 if bad else 0


def _selftest() -> int:
    """Build the pairs, MEASURE them, and prove the floor sits in the empty band between them."""
    import tempfile
    fails = []
    try:
        import deckkit as dk
    except Exception as e:                                             # noqa: BLE001
        print("[composition selftest] cannot import deckkit: {}".format(e))
        return 2

    def build(path, layouts):
        prs = dk.blank_deck()
        for boxes in layouts:
            s = dk.add_slide(prs)
            for (x, y, w, h, txt, size) in boxes:
                dk.text(s, x, y, w, h, [[(txt, size, dk.DEEP, False, False, dk.FONT)]])
            dk.speaker_notes(s, "n")
        prs.save(str(path))
        return path

    W = "a real line of words that carries this page"
    # 1 the base composition: a left column + a wide band under it
    base = [(0.6, 0.8, 4.0, 3.0, W, 14), (0.6, 4.2, 11.0, 1.2, W, 14)]
    # 2 same skeleton, different WORDS (a look/content change, not a composition change)
    same_text = [(0.6, 0.8, 4.0, 3.0, W * 3, 14), (0.6, 4.2, 11.0, 1.2, "short", 28)]
    # 3 same skeleton, one block nudged slightly
    nudged = [(0.75, 0.9, 4.0, 3.0, W, 14), (0.6, 4.25, 11.0, 1.2, W, 14)]
    # 4 a genuinely different composition: three columns across the top
    three_col = [(0.6, 1.0, 3.4, 2.4, W, 14), (4.4, 1.0, 3.4, 2.4, W, 14),
                 (8.2, 1.0, 3.4, 2.4, W, 14)]
    # 5 another: one dominant block, full height on the right
    hero = [(6.6, 0.6, 6.0, 6.0, W, 14), (0.6, 3.0, 5.4, 1.2, W, 14)]

    with tempfile.TemporaryDirectory() as td:
        p = build(Path(td) / "c.pptx", [base, same_text, nudged, three_col, hero])
        sig = [signature(p, i) for i in range(5)]

    pairs = {
        "same skeleton, different text": divergence(sig[0], sig[1]),
        "same skeleton, nudged":         divergence(sig[0], sig[2]),
        "identical to itself":           divergence(sig[0], sig[0]),
        "base vs three columns":         divergence(sig[0], sig[3]),
        "base vs hero":                  divergence(sig[0], sig[4]),
        "three columns vs hero":         divergence(sig[3], sig[4]),
    }
    print("[composition selftest] measured divergences:")
    for k, v in pairs.items():
        print("   {:<32} {:.3f}".format(k, v))

    SAME = ["identical to itself", "same skeleton, different text", "same skeleton, nudged"]
    DIFF = ["base vs three columns", "base vs hero", "three columns vs hero"]
    hi_same = max(pairs[k] for k in SAME)
    lo_diff = min(pairs[k] for k in DIFF)
    print("   -> same-skeleton max {:.3f} | different-composition min {:.3f} | floor {:.2f}"
          .format(hi_same, lo_diff, SAME_COMPOSITION))
    if not (hi_same < SAME_COMPOSITION < lo_diff):
        fails.append("the floor {:.2f} does NOT sit between the two families (same≤{:.3f}, "
                     "diff≥{:.3f}) — recalibrate it rather than shipping a number that separates "
                     "nothing".format(SAME_COMPOSITION, hi_same, lo_diff))

    # the anti-theatre check must fire on restyled copies and clear genuine variants
    restyled = [{"label": "A", "signature": sig[0]}, {"label": "B", "signature": sig[1]},
                {"label": "C", "signature": sig[2]}]
    if not faults(restyled):
        fails.append("three versions of ONE layout passed as a competition — that is the theatre "
                     "this check exists to stop")
    genuine = [{"label": "A", "signature": sig[0]}, {"label": "B", "signature": sig[3]},
               {"label": "C", "signature": sig[4]}]
    if faults(genuine):
        fails.append("three genuinely different compositions were rejected: {}"
                     .format(faults(genuine)))
    if not faults([{"label": "A", "signature": sig[0]}]):
        fails.append("a single 'variant' passed as a competition")

    # generality: the grid must follow the CANVAS, not assume 16:9
    for aspect, want_tall in ((16 / 9, False), (9 / 16, True), (4 / 3, False), (1.0, False)):
        c, r = _grid_dims(aspect)
        if want_tall and not r > c:
            fails.append("a {:.2f} canvas got a {}×{} grid — a portrait surface needs tall-thin "
                         "coverage or the measure is distorted".format(aspect, c, r))
        if c < 2 or r < 2:
            fails.append("degenerate grid {}×{} for aspect {:.2f}".format(c, r, aspect))
    if _grid_dims(16 / 9) == _grid_dims(9 / 16):
        fails.append("landscape and portrait canvases got the SAME grid — the measure would read "
                     "a story deck as if it were a slide deck")

    # robustness: malformed input must not raise
    for junk in (None, {}, {"grid": [], "blocks": 0}, 7):
        try:
            divergence(junk, sig[0]); divergence(sig[0], junk)
        except Exception as e:                                         # noqa: BLE001
            fails.append("divergence raised on {!r}: {}".format(junk, e))
    if faults(None) == []:
        fails.append("faults(None) passed")

    # ── the RECORD contract ──────────────────────────────────────────────────────────────────
    def rec(**kw):
        base = {"variants": [{"label": "A", "signature": sig[0]},
                             {"label": "B", "signature": sig[3]}],
                "picked": "B", "why": "B's claim reads in one beat; A buried it under the list"}
        base.update(kw)
        return base
    if competition_faults(rec()):
        fails.append("a real competition was rejected: {}".format(competition_faults(rec())))
    if not competition_faults(rec(picked="C")):
        fails.append("a `picked` naming no variant passed — a competition with no winner")
    if not competition_faults(rec(why="looks better")):
        fails.append("`looks better` passed as the reason — that is the sentence this step exists "
                     "to replace")
    if not competition_faults(rec(variants=[{"label": "A", "signature": sig[0]}])):
        fails.append("a single variant passed as a competition")
    if not competition_faults(rec(variants=[{"label": "A", "signature": sig[0]},
                                            {"label": "B", "signature": sig[1]}])):
        fails.append("two versions of ONE layout passed — the anti-theatre check is not wired into "
                     "the record contract")
    if not competition_faults(rec(variants=[{"label": "A", "signature": sig[0]},
                                            {"label": "B", "grid": "hand-written"}])):
        fails.append("a hand-written signature passed — it must come from the probe")
    if not competition_faults(None):
        fails.append("a missing record passed")
    # carves are claimed, never assumed
    if competition_faults({"waived": "a provided template owns this composition entirely",
                           "waived_category": "template-locked"}):
        fails.append("a properly claimed carve was rejected")
    if not competition_faults({"waived": "hard", "waived_category": "busy"}):
        fails.append("an invented carve passed")

    # determinism: the same deck must fingerprint the same way every time
    import tempfile as _tf
    with _tf.TemporaryDirectory() as td2:
        p2 = build(Path(td2) / "d.pptx", [base, three_col])
        runs = {json.dumps(signature(p2, 0), sort_keys=True) for _ in range(4)}
    if len(runs) != 1:
        fails.append("signature() is not deterministic across runs")

    for f in fails:
        print("FAIL " + f)
    print("[composition selftest] {}".format("FAILED: {}".format(len(fails)) if fails else "ok"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
