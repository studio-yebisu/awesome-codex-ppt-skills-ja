#!/usr/bin/env python3
"""Three rules from the presentation canon that CONVERT into measurements — and the one that did not.

This skill already CITES Duarte, Minto, CRAP, Mayer, Gestalt and cognitive load. Every one of those
lives in prose (SKILL.md, references/, agents/) and NONE of them is measured, which by this skill's
own enforcement invariant makes them advisory. Adding a seventh name would add words, not
capability. So the canon was mined for rules that can be decided from the built .pptx, and each
candidate was calibrated on a corpus of REAL delivered decks rather than on invented examples.

WHAT SHIPPED, and the numbers it was calibrated on (29 decks / 349 slides in ~/Downloads):

  NOTES ECHO SLIDE   Mayer's redundancy principle — narrating text the audience is already reading
                     splits attention and measurably lowers recall. Measured over 253 slides that
                     carry notes: similarity maxes out at 0.53, median 0.10. Every one of those
                     high cases is legitimate — the notes speak the slide's facts in sentences, so
                     they share vocabulary. Verbatim narration sits near 1.0. Threshold 0.75 has
                     real headroom on both sides.

  CATEGORY TITLE     Knaflic's declarative-title rule: a title states a FINDING, not a category.
                     🔴 The obvious measure does NOT work and the corpus proves it: overlap between
                     the rendered title and the recorded takeaway has median 0.33, and the BEST
                     titles score LOWEST ("Door one: buy" vs its takeaway = 0.07; "Powered by wind,
                     by default" = 0.08) because a sharp title deliberately re-words. Judging
                     "declarative" is taste and belongs to the critic rubric. What IS mechanical is
                     the bare category label from an enumerable set — `Overview`, `背景`, `Agenda`.
                     0 hits on 108 content slides, so 0 false positives; low recall by design.

  CHART SAYS IT TWICE  Tufte's erase-redundant-data-ink: data labels PLUS a value axis or gridlines
                     print the same number twice. 0 of the 8 native charts in the corpus does this,
                     so again 0 false positives and low recall — it is a floor, not a critic.

WHAT DID NOT CONVERT — recorded here because "we tried and it does not work" and "nobody thought of
it" must not look the same:

  GESTALT PROXIMITY  "Elements of one group must sit closer to each other than to the next group."
                     Four formulations were measured and every one failed on real decks: grouping
                     by shared top flagged 51 rows that were merely y-aligned (a left label and a
                     page number); adding equal width+height dropped any peer whose caption wrapped
                     to a different height; dropping height left 2 candidates, of which the clearest
                     was a timeline whose 01-04 markers sit on coloured segment boundaries — where
                     uneven spacing is CORRECT; and measuring intra- vs inter-group distance
                     "flagged" 200 of 360 pairs because the pairing itself was guesswork. The root
                     cause is not the formula: a .pptx records coordinates and no notion of which
                     shapes belong together, so every version is geometry guessing at grouping.
                     The rules that DO convert share one property — their criterion is already in
                     the record (notes for Mayer, takeaway for Knaflic, chart XML for Tufte).

    python3 scripts/canon_probe.py <deck.pptx> [--json]

Exit 0 clean · 1 findings · 2 could not run.
"""
from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import sys

NOTES_ECHO = 0.75        # symmetric near-duplication; calibrated: real max 0.53 over 253 slides
NOTES_LIFT = 0.85        # 🔴 the fraction of the NOTES that is verbatim slide text.
# `ratio` alone only catches the degenerate case where the notes copy the WHOLE slide. The real
# "reading your slides" failure lifts one or two lines, and the notes are then much SHORTER than
# the slide — measured on a realistic page, copying one sentence scores ratio 0.59 and two
# sentences 0.70, both UNDER the 0.75 floor, while the lifted fraction is 1.00 for all of them.
# The measure is asymmetric because the defect is. Calibrated over the same 253 real slides:
# max 0.71, p99 0.57, median 0.11 — so 0.85 keeps real headroom while catching a verbatim lift.
MIN_CHARS = 40           # below this, similarity is noise on both sides

# Bare category labels. Deliberately an ENUMERATION, not a heuristic: judging whether a title
# asserts something is taste, and a heuristic that guesses it produces cry-wolf on exactly the
# sharpest titles (see the module docstring).
CATEGORY = {
    "overview", "background", "introduction", "intro", "agenda", "summary", "conclusion",
    "conclusions", "results", "result", "methods", "method", "methodology", "discussion",
    "outline", "contents", "about", "about us", "context", "approach", "scope",
    "next steps", "questions", "thank you", "thanks", "appendix", "references",
    "data", "analysis", "findings", "recommendations", "problem", "solution",
    "概述", "概览", "背景", "简介", "介绍", "目录", "提纲", "总结", "小结", "结论", "方法",
    "方法论", "现状", "分析", "讨论", "结果", "数据", "流程", "下一步",
    "致谢", "谢谢", "附录", "参考文献", "关于我们", "问题", "方案", "展望",
    # 🔴 This skill builds decks in ANY language and the first version of this set covered 2 of the
    # 10 it names — a Japanese or German deck simply went unchecked, which is a silent pass, not a
    # safe default. `_norm` lowercases, so every entry here is lowercase.
    # ja
    "概要", "はじめに", "目次", "まとめ", "結論", "背景", "課題", "方法", "結果", "考察",
    "今後の予定", "参考文献", "ご清聴ありがとうございました", "付録", "アジェンダ",
    # ko
    "개요", "소개", "목차", "요약", "결론", "배경", "방법", "결과", "논의", "참고문헌", "감사합니다",
    # de
    "überblick", "einführung", "einleitung", "agenda", "inhalt", "zusammenfassung", "fazit",
    "hintergrund", "methode", "methoden", "ergebnisse", "diskussion", "ausblick", "anhang",
    "vielen dank", "quellen",
    # fr
    "aperçu", "introduction", "sommaire", "ordre du jour", "résumé", "conclusion", "contexte",
    "méthode", "méthodes", "résultats", "discussion", "annexe", "merci", "références",
    # es
    "resumen", "introducción", "índice", "agenda", "conclusión", "conclusiones", "contexto",
    "método", "métodos", "resultados", "discusión", "anexo", "gracias", "referencias",
    # it
    "panoramica", "introduzione", "indice", "sommario", "conclusione", "contesto", "metodo",
    "risultati", "discussione", "allegato", "grazie", "riferimenti",
    # nl
    "overzicht", "inleiding", "inhoud", "samenvatting", "conclusie", "achtergrond", "methode",
    "resultaten", "discussie", "bijlage", "bedankt", "bronnen",
}
# 🔴 NOT in the set, deliberately: `timeline` / `roadmap` / `时间线` / `路线图` name the OBJECT on
# the page, not the kind of page. A slide whose entire content is one timeline is legitimately
# titled "Timeline" — the word is the artifact. `Overview` / `Background` / `Agenda` never are.
# This gate BLOCKS delivery, so the asymmetry matters: a false positive costs a rename or a
# waiver, a false negative costs a weak title the critic can still catch. Found by running the
# check on the first deck outside the 349-slide calibration corpus — a layout fixture whose
# titles are form names — which is also evidence the rule has real recall.
_ARTIFACT_NAMES = {"timeline", "roadmap", "时间线", "路线图", "gantt", "甘特图",
                   "タイムライン", "ロードマップ", "타임라인", "로드맵",
                   "zeitplan", "zeitachse", "chronologie", "cronología", "cronologia",
                   "tijdlijn", "calendrier"}
SKIP_ROLES = ("cover", "closing", "thanks", "end", "section", "divider")


def _norm(s):
    s = re.sub(r"[\s　]+", " ", (s or "").strip().lower())
    return s.strip(" ：:·.、,，。-—–_|/()（）").strip()


def _title_of(slide, canvas_h):
    """The slide's title, via lint_deck's `_find_title` — one owner of the spelling.

    🔴 NOT "the biggest text": measured on a real deck, the largest run is a hero numeral on 3 of
    12 slides and a wordmark on the cover, so a size-only rule misreads a third of the deck.
    """
    from pptx.util import Emu
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import lint_deck as _L                                            # noqa: PLC0415
    bx = []
    for x in slide.shapes:
        if not getattr(x, "has_text_frame", False) or not x.text_frame.text.strip():
            continue
        try:
            sz = max((r.font.size.pt if r.font.size else 0)
                     for p in x.text_frame.paragraphs for r in p.runs) \
                if any(p.runs for p in x.text_frame.paragraphs) else 0
        except Exception:
            sz = 0
        bx.append({"text": True, "bg": False, "size": sz, "t": Emu(x.top).inches,
                   "full": x.text_frame.text.strip(), "title_ph": False})
    i = _L._find_title(bx, canvas_h)
    return bx[i]["full"] if i is not None else None


def check(pptx, gates=None):
    """Findings as (CODE, slide, message). Never raises on a readable deck."""
    from pptx import Presentation                                     # noqa: PLC0415
    from pptx.util import Emu                                         # noqa: PLC0415
    prs = Presentation(pptx)
    canvas_h = Emu(prs.slide_height).inches
    roles = {}
    if isinstance(gates, dict):
        for r in (gates.get("content", {}) or {}).get("slides") or []:
            try:
                roles[int(r.get("slide"))] = str(r.get("role") or "").lower()
            except Exception:
                continue
    out = []
    for n, s in enumerate(prs.slides, 1):
        body = " ".join(x.text_frame.text.strip() for x in s.shapes
                        if getattr(x, "has_text_frame", False) and x.text_frame.text.strip())
        notes = ""
        try:
            if s.has_notes_slide:
                notes = s.notes_slide.notes_text_frame.text.strip()
        except Exception:
            pass
        if len(body) >= MIN_CHARS and len(notes) >= MIN_CHARS:
            sm = difflib.SequenceMatcher(None, body, notes)
            r = sm.ratio()
            lift = sum(b.size for b in sm.get_matching_blocks()) / float(len(notes))
            if r >= NOTES_ECHO or lift >= NOTES_LIFT:
                why = ("are {:.0%} the same text as the slide".format(r) if r >= NOTES_ECHO
                       else "are {:.0%} verbatim slide text".format(lift))
                out.append(("NOTES ECHO SLIDE", n,
                            "the speaker notes {}. Mayer's redundancy principle: narrating what "
                            "the audience is already reading splits their attention and lowers "
                            "recall — the notes should say what the slide does NOT. (Measured "
                            "across 253 real slides: sameness tops out at 0.53, lifted text at "
                            "0.71.)".format(why)))
        if roles.get(n, "") not in SKIP_ROLES:
            t = _title_of(s, canvas_h)
            if t and _norm(t.replace("\n", " ")) in CATEGORY:
                out.append(("CATEGORY TITLE", n,
                            "the title is the bare category label {!r}. A title is the one line "
                            "everyone reads: spend it on what this slide SAYS, not on what kind of "
                            "slide it is.".format(t.replace("\n", " ")[:40])))
        for x in s.shapes:
            if not getattr(x, "has_chart", False):
                continue
            ch = x.chart
            def _f(fn, d=False):
                try:
                    return bool(fn())
                except Exception:
                    return d
            labels = _f(lambda: any(p.has_data_labels for p in ch.plots))
            axis = _f(lambda: ch.value_axis.visible) or _f(lambda: ch.value_axis.has_major_gridlines)
            if labels and axis:
                out.append(("CHART SAYS IT TWICE", n,
                            "this chart prints every value as a data label AND carries a value "
                            "axis/gridlines — the same number twice. Keep whichever the reader "
                            "actually uses and erase the other (Tufte: erase redundant data-ink)."))
    return out


def faults(pptx, gates=None):
    return ["slide {}: {} — {}".format(n, c, m) for c, n, m in check(pptx, gates)]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("pptx")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if not os.path.exists(a.pptx):
        print("[canon] no such deck: {}".format(a.pptx), file=sys.stderr)
        return 2
    gates = {}
    gp = os.path.join(os.path.dirname(os.path.abspath(a.pptx)) or ".", ".deck-gates.json")
    if os.path.exists(gp):
        try:
            with open(gp, encoding="utf-8") as fh:
                gates = json.load(fh)
        except ValueError:
            gates = {}
    try:
        found = check(a.pptx, gates)
    except Exception as exc:                                          # noqa: BLE001
        print("[canon] could not read {}: {}: {}".format(a.pptx, type(exc).__name__, exc),
              file=sys.stderr)
        return 2
    if a.json:
        print(json.dumps([{"code": c, "slide": n, "message": m} for c, n, m in found],
                         ensure_ascii=False, indent=1))
        return 1 if found else 0
    n = len(found)
    for i, (c, sl, m) in enumerate(found, 1):
        print("[canon] [{}/{}] slide {} {}: {}".format(i, n, sl, c, m))
    print("[canon] {} slide(s) checked against 3 canon rules: {} finding(s)."
          .format(len(__import__("pptx").Presentation(a.pptx).slides._sldIdLst), n))
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
