#!/usr/bin/env python3
"""Build and validate the file-backed fixture without keeping the deck output."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, text=True, capture_output=True)


def parse_stdout(process: subprocess.CompletedProcess[str]) -> dict[str, Any]:
    try:
        payload = json.loads(process.stdout)
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def main() -> None:
    parser = argparse.ArgumentParser(description="Run qiaomu-bento-ppt output fixture.")
    parser.add_argument("--repo", help="Optional bento checkout for compatibility shell-gate.")
    parser.add_argument("--output", required=True, help="Report JSON path.")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[2]
    fixture = root / "evals" / "fixtures" / "minimal-deck.json"
    tool = root / "scripts" / "bento_deck.py"
    before = hashlib.sha256(fixture.read_bytes()).hexdigest()

    with tempfile.TemporaryDirectory(prefix="qiaomu-bento-ppt-") as temp:
        temp_root = Path(temp)
        deck = temp_root / "fixture.bento.html"
        extracted = temp_root / "fixture.json"
        edited_deck = temp_root / "fixture.updated.bento.html"
        build_report = temp_root / "build-report.json"
        build_command = [
            "python3",
            str(tool),
            "build",
            str(fixture),
            "--output",
            str(deck),
            "--new-document",
            "--report",
            str(build_report),
        ]
        if args.repo:
            build_command.extend(["--repo", str(Path(args.repo).expanduser().resolve())])
        build = run(build_command)
        validate = run(["python3", str(tool), "validate", str(deck)]) if build.returncode == 0 else None
        original_deck_hash = hashlib.sha256(deck.read_bytes()).hexdigest() if deck.is_file() else ""
        extract = run([
            "python3",
            str(tool),
            "extract",
            str(deck),
            "--output",
            str(extracted),
        ]) if build.returncode == 0 else None
        edit_command = [
            "python3",
            str(tool),
            "build",
            str(extracted),
            "--identity-source",
            str(deck),
            "--output",
            str(edited_deck),
        ]
        if args.repo:
            edit_command.extend(["--repo", str(Path(args.repo).expanduser().resolve())])
        edit = run(edit_command) if extract and extract.returncode == 0 else None
        edit_payload = parse_stdout(edit) if edit else {}
        original_deck_after = hashlib.sha256(deck.read_bytes()).hexdigest() if deck.is_file() else ""
        build_payload = parse_stdout(build)
        validate_payload = parse_stdout(validate) if validate else {}
        after = hashlib.sha256(fixture.read_bytes()).hexdigest()
        project_gate = build_payload.get("shell_gate", {}).get("project", {})
        bundled_shell = root / "assets" / "bento" / "Bento_Slides.bento.html"
        checks = {
            "build_exit_zero": build.returncode == 0,
            "validate_exit_zero": bool(validate and validate.returncode == 0),
            "deck_created": deck.is_file(),
            "fixture_unchanged": before == after,
            "doc_id_minted_once": bool(build_payload.get("identity", {}).get("minted_once")),
            "standalone_shell_used": build_payload.get("shell") == str(bundled_shell),
            "internal_shell_gate": bool(
                build_payload.get("shell_gate", {}).get("internal", {}).get("ok")
            ),
            "project_shell_gate_optional": (
                bool(project_gate.get("ok")) if args.repo else not project_gate.get("ran")
            ),
            "output_validation": bool(validate_payload.get("ok")),
            "edit_extract_exit_zero": bool(extract and extract.returncode == 0),
            "edit_build_exit_zero": bool(edit and edit.returncode == 0),
            "edit_doc_id_preserved": bool(edit_payload.get("identity", {}).get("preserved")),
            "edit_source_deck_unchanged": bool(
                original_deck_hash and original_deck_hash == original_deck_after
            ),
        }

    result = {
        "ok": all(checks.values()),
        "file-backed fixture": str(fixture.relative_to(root)),
        "input_files": [
            str(fixture.relative_to(root)),
            "bundled assets/bento/Bento_Slides.bento.html"
        ],
        "output contract": [
            "new .bento.html",
            "UUID docId minted once",
            "structure report",
            "internal shell gate",
            "optional upstream project shell gate"
        ],
        "rollback boundary": "fixture hash unchanged; output existed only in a temporary directory",
        "trust report": "reports/trust.md",
        "checks": checks,
        "build_stderr": build.stderr.strip(),
        "validate_stderr": validate.stderr.strip() if validate else "",
        "extract_stderr": extract.stderr.strip() if extract else "",
        "edit_stderr": edit.stderr.strip() if edit else "",
        "missing evidence": [
            "browser visual review",
            "human-reviewed real-world deck quality"
        ],
    }
    output = Path(args.output).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not result["ok"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
