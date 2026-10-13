#!/usr/bin/env python3
"""Validate SeaSlides HTML projects without changing project files.

Usage:
    python3 batch_validate.py --dir ./projects --source-only --verbose
    python3 batch_validate.py --dir ./projects --require-build --artifact-profile visual
    python3 batch_validate.py --dir ./projects --export report.txt
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from validate_project import validate_project  # noqa: E402


def find_projects(root: Path) -> list[Path]:
    """Find complete source projects while excluding generated output trees."""
    candidates = {
        path.parent
        for path in root.rglob("content.html")
        if not any(
            part == "output" or part.startswith(".")
            for part in path.relative_to(root).parts[:-1]
        )
        and (path.parent / "index-template.html").is_file()
        and (path.parent / "template.css").is_file()
    }
    return sorted(candidates)


def validate_one(
    project: Path,
    *,
    fail_on_review: bool,
    require_build: bool,
    artifact_profile: str = "visual",
) -> dict[str, Any]:
    """Validate one project at either the source or current-build gate."""
    if require_build:
        validation_ok, details = validate_project(
            str(project),
            strict=fail_on_review,
            require_build=True,
            artifact_profile=artifact_profile,
        )
        validation_mode = f"build-{artifact_profile}"
    else:
        validation_ok, details = validate_project(
            str(project), strict=fail_on_review, source_only=True
        )
        validation_mode = "source-only"
    return {
        "name": project.name,
        "path": str(project),
        "validation_mode": validation_mode,
        "build_required": require_build,
        "fail_on_review": fail_on_review,
        "passed": validation_ok,
        "validation_ok": validation_ok,
        "error_count": details.get("error_count", len(details.get("errors", []))),
        "warning_count": details.get("warning_count", len(details.get("warnings", []))),
        "errors": details.get("errors", []),
        "warnings": details.get("warnings", []),
    }


def print_result(result: dict[str, Any], verbose: bool) -> None:
    status = "PASS" if result["passed"] else "FAIL"
    print(
        f"{status:4}  {result['name']}  "
        f"mode={result['validation_mode']} "
        f"errors={result['error_count']} warnings={result['warning_count']}"
    )
    if verbose:
        for message in result["errors"]:
            print(f"      ERROR: {message}")
        for message in result["warnings"]:
            print(f"      WARN:  {message}")


def text_report(
    root: Path,
    results: list[dict[str, Any]],
    mode: str,
) -> str:
    passed = sum(1 for result in results if result["passed"])
    lines = [
        "SeaSlides HTML Batch Validation Report",
        f"Root: {root}",
        f"Validation mode: {mode}",
        f"Projects: {len(results)}",
        f"Passed: {passed}",
        f"Failed: {len(results) - passed}",
    ]
    for result in results:
        status = "PASS" if result["passed"] else "FAIL"
        lines.extend(("", f"[{status}] {result['path']}"))
        lines.append(f"Validation mode: {result['validation_mode']}")
        lines.extend(f"ERROR: {message}" for message in result["errors"])
        lines.extend(f"WARN: {message}" for message in result["warnings"])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate SeaSlides HTML projects without modifying them"
    )
    parser.add_argument(
        "--dir", default=".", help="Root directory containing projects (default: .)"
    )
    parser.add_argument("--verbose", "-v", action="store_true")
    validation_group = parser.add_mutually_exclusive_group(required=True)
    validation_group.add_argument(
        "--source-only",
        action="store_true",
        help="Validate source/TCS only; do not assemble or inspect build artifacts",
    )
    validation_group.add_argument(
        "--require-build",
        action="store_true",
        help="Validate the current compiler receipt and synchronized artifacts without assembling",
    )
    parser.add_argument(
        "--artifact-profile",
        choices=("visual", "delivery"),
        default="visual",
        help="Required artifact set for --require-build (default: visual)",
    )
    parser.add_argument(
        "--fail-on-review",
        action="store_true",
        help="Treat validator review warnings as failures",
    )
    parser.add_argument("--export", help="Write a text report to this path")
    parser.add_argument("--json", action="store_true", help="Print JSON results")
    args = parser.parse_args()
    report_mode = (
        f"build-{args.artifact_profile}"
        if args.require_build
        else "source-only"
    )

    root = Path(args.dir).expanduser().resolve()
    if not root.is_dir():
        print(f"Error: Directory not found: {root}", file=sys.stderr)
        return 1

    projects = find_projects(root)
    if not projects:
        if args.export:
            export_path = Path(args.export).expanduser()
            export_path.parent.mkdir(parents=True, exist_ok=True)
            export_path.write_text(text_report(root, [], report_mode), encoding="utf-8")
            message = f"Report exported to: {export_path}"
            print(message, file=sys.stderr if args.json else sys.stdout)
        if args.json:
            print("[]")
        else:
            print(f"No HTML slide projects found under {root}")
        return 0

    results = [
        validate_one(
            project,
            fail_on_review=args.fail_on_review,
            require_build=args.require_build,
            artifact_profile=args.artifact_profile,
        )
        for project in projects
    ]

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        for result in results:
            print_result(result, args.verbose)
        passed = sum(1 for result in results if result["passed"])
        print(f"\nSummary: {passed}/{len(results)} projects passed")

    if args.export:
        export_path = Path(args.export).expanduser()
        export_path.parent.mkdir(parents=True, exist_ok=True)
        export_path.write_text(text_report(root, results, report_mode), encoding="utf-8")
        message = f"Report exported to: {export_path}"
        print(message, file=sys.stderr if args.json else sys.stdout)

    return 0 if all(result["passed"] for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
