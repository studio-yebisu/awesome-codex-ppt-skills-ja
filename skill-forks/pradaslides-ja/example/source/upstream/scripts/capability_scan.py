#!/usr/bin/env python3
"""Report locally discoverable presentation-production capabilities."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


EXECUTABLES = {
    "python": ["python", "python3", "py"],
    "node": ["node"],
    "npm": ["npm"],
    "npx": ["npx"],
    "libreoffice": ["soffice", "libreoffice"],
    "powerpoint": ["POWERPNT.EXE", "powerpnt"],
    "pdftoppm": ["pdftoppm"],
    "mutool": ["mutool"],
    "ffmpeg": ["ffmpeg"],
    "ffprobe": ["ffprobe"],
    "dot": ["dot"],
}

PYTHON_MODULES = {
    "python-pptx": "pptx",
    "Pillow": "PIL",
    "pypdf": "pypdf",
    "pdfplumber": "pdfplumber",
    "reportlab": "reportlab",
}

NODE_PACKAGES = ["pptxgenjs", "@slidev/cli", "playwright", "@oai/artifact-tool"]


def first_executable(candidates: list[str]) -> str | None:
    for candidate in candidates:
        found = shutil.which(candidate)
        if found:
            return found
    return None


def find_powerpoint_fallback() -> str | None:
    if os.name != "nt":
        return None
    roots = [
        os.environ.get("ProgramFiles"),
        os.environ.get("ProgramFiles(x86)"),
    ]
    relative = Path("Microsoft Office") / "root" / "Office16" / "POWERPNT.EXE"
    for root in roots:
        if root:
            candidate = Path(root) / relative
            if candidate.exists():
                return str(candidate)
    return None


def node_package_available(node: str | None, package: str) -> dict[str, Any]:
    if not node:
        return {"available": False, "detail": "Node.js not found"}
    probe = "try{console.log(require.resolve(process.argv[1]))}catch(e){process.exit(2)}"
    try:
        result = subprocess.run(
            [node, "-e", probe, package],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"available": False, "detail": str(exc)}
    if result.returncode == 0:
        return {"available": True, "detail": result.stdout.strip()}
    return {"available": False, "detail": "Not resolvable from current workspace"}


def build_report() -> dict[str, Any]:
    executables: dict[str, dict[str, Any]] = {}
    for name, candidates in EXECUTABLES.items():
        path = first_executable(candidates)
        if name == "powerpoint" and not path:
            path = find_powerpoint_fallback()
        executables[name] = {"available": bool(path), "path": path}

    python_modules = {
        label: {
            "available": importlib.util.find_spec(module) is not None,
            "module": module,
        }
        for label, module in PYTHON_MODULES.items()
    }
    node_path = executables["node"]["path"]
    node_packages = {
        package: node_package_available(node_path, package) for package in NODE_PACKAGES
    }

    candidates = []
    if node_packages["@oai/artifact-tool"]["available"]:
        candidates.append("host/artifact-tool native presentation route")
    if node_packages["pptxgenjs"]["available"]:
        candidates.append("PptxGenJS native PPTX route")
    if python_modules["python-pptx"]["available"]:
        candidates.append("python-pptx native PPTX route")
    if node_packages["@slidev/cli"]["available"]:
        candidates.append("Slidev web/technical route")
    if executables["node"]["available"] and node_packages["playwright"]["available"]:
        candidates.append("fixed-stage HTML + browser render route")
    if executables["powerpoint"]["available"]:
        candidates.append("Microsoft PowerPoint render/round-trip QA")
    elif executables["libreoffice"]["available"]:
        candidates.append("LibreOffice render/compatibility QA")
    if executables["pdftoppm"]["available"]:
        candidates.append("PDF raster QA")

    return {
        "schema_version": "1.0",
        "platform": sys.platform,
        "python_runtime": sys.executable,
        "cwd": str(Path.cwd()),
        "executables": executables,
        "python_modules": python_modules,
        "node_packages": node_packages,
        "candidate_routes": candidates,
        "note": (
            "Presence does not prove fitness. Verify notes, charts, masters, fonts, "
            "rendering, export, and editability against the brief."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()
    report = build_report()
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0

    print("PradaSlides capability scan")
    for name, info in report["executables"].items():
        marker = "yes" if info["available"] else "no"
        print(f"  {name:14} {marker:3} {info.get('path') or ''}")
    print("Python modules:")
    for name, info in report["python_modules"].items():
        print(f"  {name:14} {'yes' if info['available'] else 'no'}")
    print("Node packages:")
    for name, info in report["node_packages"].items():
        print(f"  {name:20} {'yes' if info['available'] else 'no'}")
    print("Candidate routes:")
    for route in report["candidate_routes"] or ["No complete local route detected"]:
        print(f"  - {route}")
    print(report["note"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
