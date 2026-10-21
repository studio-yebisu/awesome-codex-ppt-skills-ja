#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Does this deck fit the time the user gave for it?

The interview ASKS for it — `deck_gates.py interview` says, in both languages, "for a talk, give me
the time budget and I will confirm the slide count". Measured by grep before this file existed,
NOTHING then compared the built deck against that answer: no words-per-minute, no per-slide budget,
nothing. So the one number the speaker is actually judged on — does it end on time — was collected
and dropped, which is this repo's recurring failure shape (a rule that lives in prose and is
measured nowhere).

WHAT IS COUNTED. The SPEAKER NOTES, and only those. They are what the presenter says out loud, and
this skill already insists the spoken thread lives there rather than on the slide (PRE-FLIGHT 1).
On-slide text is deliberately not counted: a presenter who reads their slides aloud has a different
problem, and counting both would double-count every deck that does it right.

THE RATE IS A BAND, NOT A NUMBER, and the report says so. A single figure would be false precision
about someone else's delivery:

    Latin    130-150 words per minute      prepared presentation (coaching consensus; the National
                                           Communication Association puts the ideal at 120-150, and
                                           above ~160 comprehension of complex material drops)
    CJK      180-220 characters per minute formal Chinese presentation (professional speakers;
                                           announcers run ~240, which is not a talk)

Mixed text is split by character class and the two estimates are added, so a bilingual deck is not
measured on the wrong scale — the same reasoning as the CJK width work in deckkit.

WHAT IT REFUSES TO DO. With no time budget recorded, there is nothing to check and it says so: a
deck that will be read rather than presented is not late. With notes on fewer than half the content
slides the estimate is not trustworthy, and it reports THAT instead of a number — an estimate built
from a third of the talk is worse than no estimate, because it reads like one.

    python3 scripts/check_talk_time.py <deck.pptx> --minutes 12 [--json] [--waive "<why>"]
    python3 scripts/check_talk_time.py --selftest

Exit 0 clean · 1 findings · 2 could not run (NOT the same as clean, and it says so).
"""
from __future__ import annotations

import argparse
import json
import re
import sys

# Fallback only — deckkit owns the CJK classifier, and the two must not drift. `_cjk_ranges()`
# prefers deckkit's; this copy exists so the gate still runs where deckkit cannot be imported.
_FALLBACK_CJK = ((0x1100, 0x11FF), (0x2E80, 0x9FFF), (0xAC00, 0xD7AF),
                 (0xF900, 0xFAFF), (0xFF00, 0xFFEF), (0x20000, 0x3134F))

LATIN_WPM = (130, 150)          # prepared presentation, words per minute
CJK_CPM = (180, 220)            # formal presentation, characters per minute
MIN_NOTED_SHARE = 0.5           # below this, the estimate is reported as untrustworthy, not shown
OVERRUN_TOLERANCE = 1.05        # 5% over the budget is a rounding argument, not an overrun
THIN_SHARE = 0.6                # a talk using less than this much of its slot under-fills it

# ANY script's word, not just the Latin alphabet. `[A-Za-z0-9]` scored a Russian, Greek, Arabic or
# Hebrew deck at ZERO words — and since a slide with no scored load reads as a slide with no notes,
# a fully-noted Cyrillic deck was refused with "only 0 of 12 slides carry speaker notes", which
# sends the author to write notes they had already written. `[^\W_]` is Unicode-aware, and CJK is
# removed before the count so a character is never charged twice.
_WORD = re.compile(r"[^\W_]+(?:['’\-][^\W_]+)*", re.UNICODE)

# Below this ratio of scored tokens to written characters, the notes are in a script this cannot
# segment (Thai, Lao, Khmer have no word spaces and are not CJK). Refusing is the only honest
# answer: a words-per-minute rate applied to two tokens is not an estimate.
MIN_SCORED_RATIO = 0.05

# Scripts written WITHOUT word spaces that are not CJK. This module has no sourced speaking rate
# for them and will not print an unsourced one: `[^\W_]+` splits Thai at its combining marks, which
# yields a token count that looks like words and is not, so the estimate would be wrong in a way
# nobody could see. Named and refused instead.
_UNSEGMENTED = ((0x0E00, 0x0E7F, "Thai"), (0x0E80, 0x0EFF, "Lao"), (0x0F00, 0x0FFF, "Tibetan"),
                (0x1000, 0x109F, "Burmese"), (0x1780, 0x17FF, "Khmer"))
_UNSEGMENTED_SHARE = 0.2


def unsegmented_script(text):
    """The name of an unsegmentable script this text is mostly written in, or None."""
    t = "".join((text or "").split())
    if len(t) < 40:
        return None
    for lo, hi, name in _UNSEGMENTED:
        if sum(1 for ch in t if lo <= ord(ch) <= hi) >= len(t) * _UNSEGMENTED_SHARE:
            return name
    return None


def _cjk_ranges():
    try:
        import deckkit
        return tuple(deckkit._CJK_ORD)
    except Exception:
        return _FALLBACK_CJK


def spoken_load(text, ea_ord=None):
    """(words, cjk_chars) in one piece of spoken text — words in ANY word-delimited script.

    The word-per-minute band is calibrated on English prepared speech; applied to Russian, Greek,
    Arabic or Hebrew it is an approximation rather than a measurement, and that is still the right
    answer, because the alternative was scoring those decks at zero.
    """
    ea_ord = ea_ord or _cjk_ranges()
    t = text or ""
    cjk = sum(1 for ch in t if any(a <= ord(ch) <= b for a, b in ea_ord))
    rest = "".join(" " if any(a <= ord(ch) <= b for a, b in ea_ord) else ch for ch in t)
    return len(_WORD.findall(rest)), cjk


def minutes_band(latin_words, cjk_chars):
    """(fastest, slowest) minutes this much speech takes, at the rates above."""
    lo = latin_words / LATIN_WPM[1] + cjk_chars / CJK_CPM[1]
    hi = latin_words / LATIN_WPM[0] + cjk_chars / CJK_CPM[0]
    return lo, hi


# "20 min" · "20-minute" · "20 分钟" · "45m" · "1 hour" · "10+5" (talk plus questions -> the TALK)
_MIN_PATTERNS = (
    # the separator may be a hyphen: "a 20-minute talk" is how people write it more often than not
    (re.compile(r"(\d+(?:\.\d+)?)[\s\-–—]*(?:hours?|hrs?|小时)\b", re.I), 60.0),
    (re.compile(r"(\d+(?:\.\d+)?)[\s\-–—]*(?:minutes?|mins?\.?|min\b|m\b|分钟|分)", re.I), 1.0),
    (re.compile(r"(\d+(?:\.\d+)?)\s*['′]"), 1.0),
)


def parse_minutes(text):
    """The TALK's length in minutes from a free-text answer, or None.

    The interview records `length` as prose, so the budget arrives as "12 pages / 10 min" or
    "20 分钟 + 5 分钟提问". The FIRST duration is the talk; a second one after a `+` is the question
    time, which the slides do not have to fill — reading it as part of the budget would licence a
    deck that runs over the part the speaker controls.
    """
    if not isinstance(text, str) or not text.strip():
        return None
    head = re.split(r"[+＋]|\bplus\b|\band\b(?=[^+]*(?:Q&A|questions?|提问|问答))", text, maxsplit=1)[0]
    for pat, mult in _MIN_PATTERNS:
        m = pat.search(head)
        if m:
            # 🔴 "10 minutes each" is a PER-SLIDE budget. Read as the talk's length it makes a
            # correctly sized deck look twelve times too long, so it is refused (NOT CHECKED)
            # rather than guessed at — the one reading that cannot mislead.
            if re.match(r"\s*(?:each|apiece|per\b|/\s*(?:slide|page)|每)",
                        head[m.end():m.end() + 14], re.I) or \
               re.search(r"(?:\b(?:per|each)\s*$|每[^0-9]{0,6}$)", head[:m.start()], re.I):
                return None
            try:
                val = float(m.group(1)) * mult
            except ValueError:
                continue
            if 0 < val <= 600:                       # a "talk" longer than ten hours is a typo
                return val
    return None


def recorded_minutes(gates):
    """The time budget from either runtime's record, or None.

    Read from the several places it can legitimately live, because the two schemas differ and the
    interview stores prose: an explicit `content.talk_minutes` (or the Codex `design` twin), the
    `interview.length` answer the question itself asks for, and the delegated `length` pick.
    """
    if not isinstance(gates, dict):
        return None
    for holder in ("content", "design_plan", "design"):
        blk = gates.get(holder)
        if isinstance(blk, dict):
            val = blk.get("talk_minutes")
            if isinstance(val, (int, float)) and 0 < val <= 600:
                return float(val)
            got = parse_minutes(val if isinstance(val, str) else "")
            if got:
                return got
    iv = gates.get("interview") if isinstance(gates.get("interview"), dict) else {}
    got = parse_minutes(iv.get("length") if isinstance(iv.get("length"), str) else "")
    if got:
        return got
    for pick in (iv.get("picks") or []):
        if isinstance(pick, dict) and pick.get("axis") == "length":
            got = parse_minutes(str(pick.get("value") or ""))
            if got:
                return got
    return parse_minutes(str(iv.get("record") or "")) if isinstance(iv.get("record"), str) else None


def notes_by_slide(pptx):
    """[(slide number, notes text)] — the spoken thread, slide by slide."""
    from pptx import Presentation
    out = []
    for i, slide in enumerate(Presentation(pptx).slides, 1):
        text = ""
        try:
            if slide.has_notes_slide:
                text = slide.notes_slide.notes_text_frame.text or ""
        except Exception:
            text = ""
        out.append((i, text))
    return out


def check(pptx, minutes, *, waive=None):
    """(findings, facts). findings = [(severity, code, message)] — 'block' | 'note'."""
    if not minutes:
        raise RuntimeError("no time budget recorded — the interview asks for one on a talk "
                           "(`interview.length`, or `content.talk_minutes`). Nothing to check: a "
                           "deck that will be READ rather than presented is never late")
    try:
        slides = notes_by_slide(pptx)
    except Exception as exc:
        raise RuntimeError("could not read %s: %s" % (pptx, exc))
    if not slides:
        raise RuntimeError("the deck has no slides")

    ea = _cjk_ranges()
    per = []
    for n, text in slides:
        latin, cjk = spoken_load(text, ea)
        lo, hi = minutes_band(latin, cjk)
        per.append({"slide": n, "words": latin, "cjk": cjk, "lo": lo, "hi": hi,
                    "chars": len("".join((text or "").split()))})
    noted = [p for p in per if p["words"] or p["cjk"]]
    facts = {"minutes": minutes, "slides": len(per), "noted": len(noted),
             "per_slide": per, "rates": {"latin_wpm": list(LATIN_WPM), "cjk_cpm": list(CJK_CPM)}}
    written = sum(p["chars"] for p in per)
    script = unsegmented_script(" ".join(t or "" for _n, t in slides))
    if script:
        raise RuntimeError(
            "the speaker notes are written in %s, which has no word spaces and is not CJK. This "
            "module has a sourced speaking rate for neither, and it will not print an unsourced "
            "one: the word count would come from where the combining marks fall, which looks like "
            "an estimate and is not. Judge the length by rehearsing it." % script)
    if written >= 200 and sum(p["words"] + p["cjk"] for p in per) < written * MIN_SCORED_RATIO:
        raise RuntimeError(
            "the speaker notes are %d characters long and almost none of them can be scored — the "
            "script they are written in is one this cannot segment. A words-per-minute rate "
            "applied to a handful of tokens is not an estimate" % written)
    if len(noted) < max(1, int(round(MIN_NOTED_SHARE * len(per)))):
        raise RuntimeError(
            "only %d of %d slides carry speaker notes, so a duration built from them would be an "
            "estimate of a third of the talk wearing the clothes of a whole one. Write the spoken "
            "thread into the notes (PRE-FLIGHT 1) and run this again"
            % (len(noted), len(per)))

    lo = sum(p["lo"] for p in per)
    hi = sum(p["hi"] for p in per)
    facts["estimate"] = [lo, hi]
    findings = []
    band = "%.0f-%.0f min of speech for a %.0f-minute slot" % (lo, hi, minutes)
    if lo > minutes * OVERRUN_TOLERANCE:
        over = lo - minutes
        cut = max(1, int(round(over / max(0.1, lo / len(per)))))
        findings.append(("block", "OVER THE SLOT",
                         "%s — over even at the FAST end of the rate band (%d wpm / %d CJK chars "
                         "per minute). Cut about %d slide(s) worth of speech, or shorten the notes; "
                         "a talk that needs every word delivered at a sprint is one that runs over."
                         % (band, LATIN_WPM[1], CJK_CPM[1], cut)))
    elif hi > minutes:
        findings.append(("note", "TIGHT",
                         "%s — it fits only if delivery stays at the fast end of the band. That is "
                         "the pace at which complex material stops landing, so treat it as full."
                         % band))
    if hi < minutes * THIN_SHARE:
        findings.append(("note", "UNDER THE SLOT",
                         "%s — under %d%% of the slot even at the slow end. Either there is more to "
                         "say than the notes carry, or the slot can be given back."
                         % (band, int(THIN_SHARE * 100))))

    # one slide that eats the talk: the classic is a methods slide with a page of notes under it
    slide_cap = max(1.5, minutes * 0.25)
    heavy = [p for p in per if p["hi"] > slide_cap]
    if heavy:
        findings.append(("note", "ONE SLIDE EATS THE TALK",
                         "slide(s) %s each carry %.0f+ minutes of speech (cap %.1f min = a quarter "
                         "of the slot). A slide nobody can leave in under a minute is two slides."
                         % (", ".join(str(p["slide"]) for p in heavy),
                            min(p["hi"] for p in heavy), slide_cap)))
    if waive and findings:
        facts["waived"] = waive
    return findings, facts


def _selftest():
    bad = []
    # the two rate bands must stay ordered and sane, or every estimate below is meaningless
    if not (0 < LATIN_WPM[0] < LATIN_WPM[1] and 0 < CJK_CPM[0] < CJK_CPM[1]):
        bad.append("the rate bands are not ordered")
    lat, cjk = spoken_load("Ten words of English here, plus 中文 五个字.")   # 5 CJK chars, 6 words
    if cjk != 5 or lat != 6:
        bad.append("mixed text split wrong: %d latin, %d cjk" % (lat, cjk))
    lo, hi = minutes_band(1500, 0)
    if not (9.9 < lo < 10.1 and 11.4 < hi < 11.6):
        bad.append("1500 English words should be ~10-11.5 min, got %.1f-%.1f" % (lo, hi))
    lo, hi = minutes_band(0, 2200)
    if not (9.9 < lo < 10.1 and 12.1 < hi < 12.3):
        bad.append("2200 CJK characters should be ~10-12 min, got %.1f-%.1f" % (lo, hi))
    for text, want in (("12 pages / 10 min", 10), ("20 分钟", 20), ("a 45m slot", 45),
                       ("1 hour", 60), ("10 min + 5 Q&A", 10), ("20 分钟 + 5 分钟提问", 20),
                       ("a 20-minute talk", 20), ("30–minute slot", 30),
                       ("about 9-15 slides", None), ("", None), (None, None)):
        got = parse_minutes(text)
        if (got is None) != (want is None) or (want is not None and abs(got - want) > 0.01):
            bad.append("parse_minutes(%r) -> %r, wanted %r" % (text, got, want))
    if recorded_minutes({"interview": {"length": "12 pages / 10 min"}}) != 10:
        bad.append("the interview's own answer is not read")
    if recorded_minutes({"content": {"talk_minutes": 20}}) != 20:
        bad.append("an explicit content.talk_minutes is not read")
    if recorded_minutes({"design": {"talk_minutes": "20 minutes"}}) != 20:
        bad.append("the Codex twin is not read")
    if recorded_minutes({"interview": {"length": "9-15 slides"}}) is not None:
        bad.append("a slide count was read as a duration")
    for b in bad:
        print("  ✗", b)
    print("[talk-time] selftest %s" % ("FAILED" if bad else "ok"))
    return 1 if bad else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pptx", nargs="?")
    ap.add_argument("--minutes", type=float, help="the talk's slot; else read from --gates")
    ap.add_argument("--gates", help="a .deck-gates.json / codex evidence file to read the budget from")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--waive", default=None, help="a written reason; reports but does not fail")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return _selftest()
    if not a.pptx:
        ap.error("a deck path is required")
    minutes = a.minutes
    if minutes is None and a.gates:
        try:
            minutes = recorded_minutes(json.load(open(a.gates, encoding="utf-8")))
        except Exception as exc:
            print("[talk-time] NOT CHECKED — could not read %s: %s" % (a.gates, exc))
            return 2
    try:
        findings, facts = check(a.pptx, minutes, waive=a.waive)
    except Exception as exc:
        print("[talk-time] NOT CHECKED — %s" % exc)
        print("            NOT the same as clean.")
        return 2
    if a.json:
        print(json.dumps({"findings": [{"severity": s, "code": c, "why": m} for s, c, m in findings],
                          "facts": facts}, indent=1, ensure_ascii=False))
    print("[talk-time] %.0f-%.0f min of speech in %d slides for a %.0f-minute slot "
          "(%d slides carry notes)" % (facts["estimate"][0], facts["estimate"][1], facts["slides"],
                                       facts["minutes"], facts["noted"]))
    for sev, code, why in findings:
        print("[talk-time] %s %s: %s" % ("✗" if sev == "block" else "•", code, why))
    if facts.get("waived"):
        print("[talk-time] WAIVED — %s" % facts["waived"])
        return 0
    if not findings:
        print("[talk-time] the deck fits its slot at a normal delivery pace")
    return 1 if any(s == "block" for s, _c, _m in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
