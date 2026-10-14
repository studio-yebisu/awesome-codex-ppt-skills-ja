#!/usr/bin/env python3
"""Validate the internal evidence record behind an owner-facing report."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


ALLOWED_STATUS = {"completed", "partial", "in_progress", "blocked", "failed"}
EMPTY_GAP = {"", "none", "no", "没有", "无"}
TECH_PATTERN = re.compile(
    r"(?:\b(?:sha-?256|hash|event|draw|gate|buffer|pointer|pid|hwnd|mrt|cb|vb|ib|rdc)\b|"
    r"\bstage\s*\d+\b|\b0x[0-9a-f]+\b|\b[a-f0-9]{32,}\b)",
    re.IGNORECASE,
)


def load_report(path: str) -> dict:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("report root must be an object")
    return data


def nonempty_text(data: dict, key: str, errors: list[str]) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{key} must be nonempty owner-readable text")
        return ""
    return value.strip()


def validate_report(data: dict) -> list[str]:
    errors: list[str] = []
    status = data.get("status")
    if status not in ALLOWED_STATUS:
        errors.append("status must distinguish completed/partial/in_progress/blocked/failed")

    opening = nonempty_text(data, "opening", errors)
    observable = nonempty_text(data, "observable_result", errors)
    remaining = nonempty_text(data, "remaining_gap", errors)
    impact = nonempty_text(data, "owner_impact", errors)
    next_action = nonempty_text(data, "next_action", errors)
    nonempty_text(data, "owner_action", errors)

    if len(opening) > 220:
        errors.append("opening is too long to function as a direct owner-level answer")
    if TECH_PATTERN.search(opening):
        errors.append("opening leads with implementation jargon or raw identifiers")
    if len(observable) < 12:
        errors.append("observable_result does not explain what a person can see or use")
    if len(impact) < 8:
        errors.append("owner_impact does not explain why the current state matters")
    if len(next_action) > 220:
        errors.append("next_action is not concise")

    usable_now = data.get("usable_now")
    if not isinstance(usable_now, bool):
        errors.append("usable_now must be a boolean")

    if status == "completed":
        if usable_now is not True:
            errors.append("completed work must be usable_now")
        if remaining.lower() not in EMPTY_GAP:
            errors.append("completed work cannot retain a material remaining gap")
    elif isinstance(status, str) and remaining.lower() in EMPTY_GAP:
        errors.append("unfinished work must name the remaining gap")

    changes_visible = data.get("changes_visible")
    inspected = data.get("fresh_result_inspected")
    observation = data.get("human_observation")
    if not isinstance(changes_visible, bool):
        errors.append("changes_visible must be a boolean")
    if changes_visible:
        if inspected is not True:
            errors.append("visible work requires fresh_result_inspected=true")
        if not isinstance(observation, str) or not observation.strip():
            errors.append("visible work requires a concrete human_observation")

    evidence = data.get("technical_evidence")
    if not isinstance(evidence, list):
        errors.append("technical_evidence must be a list")
    else:
        for index, item in enumerate(evidence):
            if not isinstance(item, dict):
                errors.append(f"technical_evidence[{index}] must be an object")
                continue
            fact = item.get("fact")
            meaning = item.get("meaning")
            if not isinstance(fact, str) or not fact.strip():
                errors.append(f"technical_evidence[{index}].fact is missing")
            if not isinstance(meaning, str) or len(meaning.strip()) < 6:
                errors.append(f"technical_evidence[{index}].meaning must explain owner impact")

    return errors


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("report")
    args = parser.parse_args(argv)
    try:
        errors = validate_report(load_report(args.report))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors = [str(exc)]
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("owner-facing report contract: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
