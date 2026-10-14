#!/usr/bin/env python3
"""Start a new, empty deck: the engine, the themes and a config, no slides.

A deck starts empty on purpose. Its slides are written from the user's brief,
so the result is a first draft of their talk - never a reworded copy of an
example deck.

    python3 new_deck.py <folder> --title "Q3 results" --lang fr \\
        --theme obsidian --motion balanced --transition fade

Then write slides/01-*.html, 02-*.html, ... and run build.py inside <folder>.
Refuses to write into a folder that already has files in it.
Standard library only.
"""

import argparse
import json
import shutil
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
TEMPLATE = SKILL / "template"
MOTION_LEVELS = ("none", "subtle", "balanced", "lively", "extra")
TRANSITIONS = ("none", "fade", "slide", "zoom", "rise", "blur", "flip")
IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store", "index.html",
                                "index.unmerged-edits.html")


def main() -> int:
    themes = sorted(p.name for p in (TEMPLATE / "themes").iterdir() if p.is_dir())
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("folder", help="where to create the deck (new or empty folder)")
    ap.add_argument("--title", default="Presentation", help="the deck's title")
    ap.add_argument("--lang", default="en", help="document language: en, fr, ...")
    ap.add_argument("--theme", default="obsidian", choices=themes)
    ap.add_argument("--motion", default="balanced", choices=MOTION_LEVELS,
                    help="animation level (default: balanced)")
    ap.add_argument("--transition", default="fade", choices=TRANSITIONS,
                    help="default slide transition (default: fade)")
    args = ap.parse_args()

    target = Path(args.folder).resolve()
    if target.exists() and (not target.is_dir() or any(target.iterdir())):
        print(f"error: {target} already exists and is not empty - pick a new folder",
              file=sys.stderr)
        return 1

    shutil.copytree(TEMPLATE, target, ignore=IGNORE, dirs_exist_ok=True)
    config_path = target / "deck.config.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    config.update(title=args.title, lang=args.lang, theme=args.theme,
                  motion=args.motion, transition=args.transition)
    config_path.write_text(json.dumps(config, indent=2, ensure_ascii=False) + "\n",
                           encoding="utf-8", newline="\n")

    print(f"New deck in {target}")
    print(f"  title \"{args.title}\" · lang {args.lang} · theme {args.theme} · "
          f"motion {args.motion} · transition {args.transition}")
    print("Next: write slides/01-*.html, 02-*.html, ... then run build.py there.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
