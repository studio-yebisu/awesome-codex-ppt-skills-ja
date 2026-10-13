#!/usr/bin/env python3
"""No written-reason floor may be measured with `len()` — it is twice as strict in Chinese.

🔴 WHY. A floor like `len(reason) < 12` counts CODEPOINTS. A Chinese sentence carries roughly
twice the information per codepoint as an English one, so the SAME number means "12 letters" in
English and "12 characters" — about 24 letters' worth — in Chinese. The bar is silently doubled
for exactly the users least able to see why their reason was rejected.

MEASURED, on this repo, on a real Chinese deck: `audience_brief` rejected
an 11-codepoint Chinese brief (display width 22) against `MIN_TEXT = 12`, while a 12-letter
English phrase carrying a third as much information passed. `written_reason.reason_width` was
written for precisely this and shipped months earlier — four modules simply never reached for it,
including two written the same day as a module that used it correctly. That is what makes this a
guard rather than a fix: knowing the rule did not make anyone apply it.

WHAT IT CHECKS. Every `len(...) < <FLOOR>` and `len(...) <= <FLOOR>` in scripts/ whose floor is a
NAMED constant matching the reason-floor naming (MIN_TEXT / MIN_WHY / MIN_RULE / MIN_QUOTE /
MIN_BASIS / MIN_ALT / …). Comparisons against literals are left alone: `len(x) < 2` is an
emptiness test, not an information floor, and flagging it would make the guard noise.

    python3 scripts/check_reason_width.py        # from the skill directory
    python3 scripts/check_reason_width.py --list

Exit 0 clean · 1 a floor measured in codepoints · 2 could not run.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent

# A floor whose NAME says it bounds written text. `len()` against one of these is the bug.
#
# 🔴 The first version of this pattern was `len\s*\([^)]*\)\s*<=?\s*MIN_…` and it was NOT a
# detector: `[^)]*` cannot cross the inner `)` of `len(str(x.get("k") or "").strip())`, which is
# the form 10 of the 12 real sites were written in. Planting the bug back reported CLEAN. So the
# match is split in two — find the FLOOR, then ask whether the expression being compared calls
# `len()` — which is paren-depth-agnostic by construction.
_FLOOR_NAME = r"MIN_(?:TEXT|WHY|RULE|QUOTE|BASIS|ALT|REASON|WORDS)"
FLOOR = re.compile(r"<=?\s*(" + _FLOOR_NAME + r")\b")
_LEN = re.compile(r"\blen\s*\(")

# Deliberately one-sided, with the reason. An empty reason is what this script prevents.
ALLOWLIST: dict[str, str] = {
    "written_reason.py": "it DEFINES reason_width; measuring codepoints there is the thing being "
                         "converted, not a floor being applied",
}


def hits(path: Path) -> list[tuple[int, str, str]]:
    """Lines where the expression compared against a reason floor is a `len()` call.

    Only the text LEFT of the comparison is searched for `len(`, so `x < MIN_TEXT and len(y) > 3`
    — a floor and an unrelated length on one line — is not a hit.
    """
    out = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        m = FLOOR.search(line)
        if m and _LEN.search(line[:m.start()]):
            out.append((i, m.group(1), line.strip()))
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args(argv)

    files = sorted(SCRIPTS.glob("*.py"))
    if not files:
        print("[reason-width] found no scripts to scan — a guard that matches nothing reports "
              "clean forever.", file=sys.stderr)
        return 2

    bad, scanned = [], 0
    for f in files:
        if f.name == Path(__file__).name:
            continue
        scanned += 1
        for ln, floor, src in hits(f):
            if f.name in ALLOWLIST:
                if a.list:
                    print("{:<10} {}:{} ({})".format("skip", f.name, ln, ALLOWLIST[f.name][:40]))
                continue
            bad.append((f.name, ln, floor, src))

    if a.list:
        print("[reason-width] scanned {} file(s); {} codepoint floor(s)".format(scanned, len(bad)))
        return 0

    for name, ln, floor, src in bad:
        print("[reason-width] {}:{} measures a written-reason floor ({}) with `len()`, which "
              "counts CODEPOINTS — the same number is twice as strict in Chinese. Use "
              "`written_reason.reason_width` (this repo already ships it):\n    {}"
              .format(name, ln, floor, src))
    print("[reason-width] {} file(s) scanned: {} problem(s).".format(scanned, len(bad)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
