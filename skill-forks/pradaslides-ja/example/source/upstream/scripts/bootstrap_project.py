#!/usr/bin/env python3
"""Create a safe PradaSlides workspace, with optional file-backed contracts."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


INTENTS = [
    "portfolio",
    "work-results",
    "business-proposal",
    "sales",
    "investor-pitch",
    "strategy-decision",
    "research-technical",
    "teaching-workshop",
    "keynote-launch",
    "report-async",
    "template-system",
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, help="New or empty project directory")
    parser.add_argument("--intent", required=True, choices=INTENTS)
    parser.add_argument("--project", help="Human-readable project name")
    parser.add_argument(
        "--contracts",
        choices=("none", "full"),
        default="none",
        help="Create starter JSON contracts. Default: none (internal planning model only)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="With --contracts full, overwrite starter JSON files; never delete other files",
    )
    args = parser.parse_args()

    target = Path(args.output).expanduser().resolve()
    target.mkdir(parents=True, exist_ok=True)
    starter = Path(__file__).resolve().parents[1] / "assets" / "starter"
    if not starter.is_dir():
        raise SystemExit(f"Starter assets missing: {starter}")

    for name in ("src", "assets", "previews", "qa", "exports"):
        (target / name).mkdir(exist_ok=True)

    copied: list[str] = []
    skipped: list[str] = []
    if args.contracts == "full":
        for source in sorted(starter.glob("*.json")):
            destination = target / source.name
            if destination.exists() and not args.force:
                skipped.append(source.name)
                continue
            shutil.copy2(source, destination)
            copied.append(source.name)

    brief_path = target / "brief.json"
    if args.contracts == "full" and brief_path.exists() and ("brief.json" in copied or args.force):
        brief = json.loads(brief_path.read_text(encoding="utf-8"))
        brief["primary_intent"] = args.intent
        brief["project"] = args.project or target.name
        brief_path.write_text(
            json.dumps(brief, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    print(f"PradaSlides project ready: {target}")
    print(f"Planning contracts: {args.contracts}")
    if copied:
        print("Created/updated: " + ", ".join(copied))
    if skipped:
        print("Preserved existing: " + ", ".join(skipped))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
