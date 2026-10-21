#!/usr/bin/env python3
"""Validate PradaSlides source-ledger.json provenance links."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

from _report import Diagnostic, emit_report, load_json


SOURCE_ID = re.compile(r"^S\d{2,}$")
CLAIM_ID = re.compile(r"^C\d{2,}$")
CLASSES = {"supplied-fact", "external-fact", "calculation", "judgment", "assumption", "scenario", "quote"}
STATUSES = {"verified", "needs-check", "scenario", "excluded", "confidential"}


def validate(data: Any) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    if not isinstance(data, dict):
        return [Diagnostic("error", "LEDGER_ROOT", "Root must be a JSON object")]
    sources = data.get("sources")
    claims = data.get("claims")
    if not isinstance(sources, list):
        diagnostics.append(Diagnostic("error", "LEDGER_SOURCES", "sources must be an array", "sources"))
        sources = []
    if not isinstance(claims, list):
        diagnostics.append(Diagnostic("error", "LEDGER_CLAIMS", "claims must be an array", "claims"))
        claims = []
    source_ids: set[str] = set()
    source_support: dict[str, set[str]] = {}
    for index, source in enumerate(sources):
        loc = f"sources[{index}]"
        if not isinstance(source, dict):
            diagnostics.append(Diagnostic("error", "LEDGER_SOURCE_TYPE", "Source entry must be an object", loc))
            continue
        source_id = source.get("id")
        if not isinstance(source_id, str) or not SOURCE_ID.match(source_id):
            diagnostics.append(Diagnostic("error", "LEDGER_SOURCE_ID", "Source id must match S01, S02, ...", f"{loc}.id"))
            continue
        if source_id in source_ids:
            diagnostics.append(Diagnostic("error", "LEDGER_SOURCE_DUP", f"Duplicate source id {source_id}", f"{loc}.id"))
        source_ids.add(source_id)
        if not str(source.get("title", "")).strip():
            diagnostics.append(Diagnostic("error", "LEDGER_SOURCE_TITLE", "Source title is required", f"{loc}.title"))
        if not str(source.get("uri_or_path", "")).strip():
            diagnostics.append(Diagnostic("error", "LEDGER_SOURCE_PATH", "uri_or_path is required", f"{loc}.uri_or_path"))
        status = source.get("status")
        if status not in STATUSES:
            diagnostics.append(Diagnostic("error", "LEDGER_SOURCE_STATUS", f"Unknown status {status!r}", f"{loc}.status"))
        supports = source.get("supports", [])
        if not isinstance(supports, list) or not all(isinstance(item, str) for item in supports):
            diagnostics.append(Diagnostic("error", "LEDGER_SUPPORTS", "supports must be an array of claim IDs", f"{loc}.supports"))
            supports = []
        source_support[source_id] = set(supports)

    claim_ids: set[str] = set()
    for index, claim in enumerate(claims):
        loc = f"claims[{index}]"
        if not isinstance(claim, dict):
            diagnostics.append(Diagnostic("error", "LEDGER_CLAIM_TYPE", "Claim entry must be an object", loc))
            continue
        claim_id = claim.get("id")
        if not isinstance(claim_id, str) or not CLAIM_ID.match(claim_id):
            diagnostics.append(Diagnostic("error", "LEDGER_CLAIM_ID", "Claim id must match C01, C02, ...", f"{loc}.id"))
            continue
        if claim_id in claim_ids:
            diagnostics.append(Diagnostic("error", "LEDGER_CLAIM_DUP", f"Duplicate claim id {claim_id}", f"{loc}.id"))
        claim_ids.add(claim_id)
        if not str(claim.get("text", "")).strip():
            diagnostics.append(Diagnostic("error", "LEDGER_CLAIM_TEXT", "Claim text is required", f"{loc}.text"))
        claim_class = claim.get("class")
        if claim_class not in CLASSES:
            diagnostics.append(Diagnostic("error", "LEDGER_CLASS", f"Unknown claim class {claim_class!r}", f"{loc}.class"))
        status = claim.get("status")
        if status not in STATUSES:
            diagnostics.append(Diagnostic("error", "LEDGER_CLAIM_STATUS", f"Unknown status {status!r}", f"{loc}.status"))
        linked = claim.get("source_ids", [])
        if not isinstance(linked, list) or not all(isinstance(item, str) for item in linked):
            diagnostics.append(Diagnostic("error", "LEDGER_CLAIM_SOURCES", "source_ids must be an array", f"{loc}.source_ids"))
            linked = []
        missing = sorted(set(linked) - source_ids)
        if missing:
            diagnostics.append(Diagnostic("error", "LEDGER_SOURCE_MISSING", f"Unknown source IDs: {', '.join(missing)}", f"{loc}.source_ids"))
        if claim_class in {"supplied-fact", "external-fact", "calculation", "quote"} and not linked:
            diagnostics.append(Diagnostic("error", "LEDGER_EVIDENCE", f"{claim_class} requires at least one source", f"{loc}.source_ids"))
        if claim_class == "scenario" and status != "scenario":
            diagnostics.append(Diagnostic("error", "LEDGER_SCENARIO", "Scenario claim must use status 'scenario'", f"{loc}.status"))
        if status == "verified" and claim_class in {"assumption", "scenario"}:
            diagnostics.append(Diagnostic("warning", "LEDGER_STATUS_CLASS", f"{claim_class} should not normally be marked verified", f"{loc}.status"))
        for source_id in linked:
            if source_id in source_support and claim_id not in source_support[source_id]:
                diagnostics.append(Diagnostic("warning", "LEDGER_BACKLINK", f"{source_id}.supports does not list {claim_id}", loc))

    for source_id, supports in source_support.items():
        unknown = sorted(supports - claim_ids)
        if unknown:
            diagnostics.append(Diagnostic("error", "LEDGER_CLAIM_MISSING", f"{source_id} supports unknown claims: {', '.join(unknown)}", source_id))
    pending = [claim.get("id", "?") for claim in claims if isinstance(claim, dict) and claim.get("status") == "needs-check"]
    if pending:
        diagnostics.append(Diagnostic("warning", "LEDGER_PENDING", "Claims still need verification: " + ", ".join(pending), "claims"))
    return diagnostics


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger")
    parser.add_argument("--json-output")
    args = parser.parse_args()
    try:
        data = load_json(args.ledger)
    except ValueError as exc:
        return emit_report("source ledger validation", [Diagnostic("error", "LEDGER_JSON", str(exc))], json_output=args.json_output)
    return emit_report(
        "source ledger validation",
        validate(data),
        json_output=args.json_output,
        extra={"file": str(Path(args.ledger).resolve())},
    )


if __name__ == "__main__":
    raise SystemExit(main())
