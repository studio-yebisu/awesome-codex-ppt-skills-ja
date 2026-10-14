#!/usr/bin/env python3
"""Validate a human-intent-to-machine-evidence audit record."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


SCHEMA = "human-intent-audit.v1"
AUDIT_STATUSES = {"pass", "partial", "open", "blocked", "fail"}
REQUIREMENT_STATUSES = {"pass", "partial", "open", "blocked", "fail"}


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _string_list(value: Any) -> bool:
    return (
        isinstance(value, list)
        and bool(value)
        and all(_nonempty(item) for item in value)
    )


def validate(record: Any) -> list[str]:
    if not isinstance(record, dict):
        return ["record must be a JSON object"]
    errors: list[str] = []
    if record.get("schema") != SCHEMA:
        errors.append(f"schema must be {SCHEMA}")
    status = record.get("status")
    if status not in AUDIT_STATUSES:
        errors.append("invalid top-level status")
    responsibility = record.get("responsibility")
    if not isinstance(responsibility, dict) or (
        responsibility.get("agent_owns_translation") is not True
    ):
        errors.append("agent_owns_translation must be true")
    if isinstance(responsibility, dict) and (
        responsibility.get("user_is_detector_author") is not False
    ):
        errors.append("user_is_detector_author must be false")

    requirements = record.get("requirements")
    if not isinstance(requirements, list) or not requirements:
        return errors + ["requirements must be a nonempty array"]

    seen: set[str] = set()
    requirement_statuses: list[str] = []
    for index, item in enumerate(requirements):
        prefix = f"requirements[{index}]"
        if not isinstance(item, dict):
            errors.append(prefix + " must be an object")
            continue
        requirement_id = item.get("id")
        if not _nonempty(requirement_id):
            errors.append(prefix + ".id is required")
        elif requirement_id in seen:
            errors.append(prefix + ".id is duplicated")
        else:
            seen.add(requirement_id)
        for field in (
            "human_requirement",
            "interpreted_intent",
            "owner_acceptance_scenario",
        ):
            if not _nonempty(item.get(field)):
                errors.append(prefix + f".{field} is required")
        for field in (
            "final_observables",
            "machine_predicates",
            "threshold_basis",
            "evidence",
        ):
            if not _string_list(item.get(field)):
                errors.append(prefix + f".{field} must be a nonempty string array")
        if not isinstance(item.get("proxy_risks"), list):
            errors.append(prefix + ".proxy_risks must be an array")
        item_status = item.get("status")
        if item_status not in REQUIREMENT_STATUSES:
            errors.append(prefix + ".status is invalid")
        else:
            requirement_statuses.append(item_status)
        semantic = item.get("semantic_review")
        if not isinstance(semantic, dict):
            errors.append(prefix + ".semantic_review is required")
        elif item_status == "pass":
            if semantic.get("machine_predicates_match_intent") is not True:
                errors.append(prefix + ".semantic_review does not confirm intent")
            if semantic.get("owner_scenario_executed") is not True:
                errors.append(prefix + ".owner scenario was not executed")
            unresolved = semantic.get("unresolved_gaps")
            if not isinstance(unresolved, list) or unresolved:
                errors.append(prefix + ".semantic_review has unresolved gaps")

    if status == "pass":
        if len(requirement_statuses) != len(requirements) or any(
            value != "pass" for value in requirement_statuses
        ):
            errors.append("top-level pass contradicts non-pass requirements")
        if record.get("user_was_first_qa") is not False:
            errors.append("top-level pass requires user_was_first_qa=false")
        if record.get("machine_to_human_semantic_review") is not True:
            errors.append("top-level pass requires machine_to_human_semantic_review=true")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="JSON file path, or - for stdin")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    try:
        if args.input == "-":
            record = json.load(sys.stdin)
            source = "<stdin>"
        else:
            path = Path(args.input)
            record = json.loads(path.read_text(encoding="utf-8"))
            source = str(path.resolve())
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        errors = [f"record unreadable: {exc}"]
        record = None
        source = args.input
    else:
        errors = validate(record)
    result = {"valid": not errors, "input": source, "errors": errors}
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif errors:
        for error in errors:
            print("FAIL " + error)
    else:
        print("PASS_HUMAN_INTENT_TRACEABILITY")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
