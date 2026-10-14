#!/usr/bin/env python3
"""Read-only runtime diagnosis that works even when SlideMuse dependencies are missing."""
from __future__ import annotations

import argparse
import importlib.metadata
import json
import re
import shlex
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True

from runtime_environment import renderer_environment

ROOT = Path(__file__).resolve().parents[1]
MODULES = {"Pillow": "PIL.Image", "python-pptx": "pptx", "jsonschema": "jsonschema"}


def display_command(arguments) -> str:
    # Show shell-specific quoting; commands are advice and never executed here.
    if sys.platform == "win32":
        return "& " + " ".join("'" + str(arg).replace("'", "''") + "'" for arg in arguments)
    return shlex.join([str(arg) for arg in arguments])


def requirement_checks(root: Path):
    try:
        lines = (root / "requirements.txt").read_text(encoding="utf-8-sig").splitlines()
    except OSError as error:
        return [{"id": "requirements", "status": "fail", "message": str(error),
                 "remedy": "Restore requirements.txt by reinstalling SlideMuse."}]
    checks = []
    for line in lines:
        line = line.partition("#")[0].strip()
        if not line:
            continue
        match = re.fullmatch(r"([A-Za-z0-9_.-]+)>=(\d+(?:\.\d+)*)", line)
        if not match or match[1] not in MODULES:
            checks.append({"id": "requirement", "status": "fail", "message": f"Unsupported requirement: {line}",
                           "remedy": "Update the doctor requirement parser for this runtime contract."})
            continue
        name, minimum = match.groups()
        item = {"id": "dependency:" + name, "requirement": line, "status": "pass"}
        try:
            installed = importlib.metadata.version(name)
            item["version"] = installed
            # Runtime requirements use numeric lower bounds. Reject ambiguous
            # prerelease/dev/local versions instead of claiming compatibility.
            release = re.fullmatch(r"\d+(?:\.\d+)*", installed)
            if not release:
                item.update(status="fail", message=f"Cannot verify non-final version {installed}")
            else:
                actual, wanted = tuple(map(int, installed.split("."))), tuple(map(int, minimum.split(".")))
                size = max(len(actual), len(wanted))
                if actual + (0,) * (size - len(actual)) < wanted + (0,) * (size - len(wanted)):
                    item.update(status="fail", message=f"Installed {installed}; requires {line}")
            probe = subprocess.run(
                [sys.executable, "-B", "-c", f"import {MODULES[name]}"],
                capture_output=True, text=True, errors="replace", timeout=15, check=False,
            )
            if probe.returncode:
                item.update(status="fail", message="Import failed", detail=(probe.stderr or probe.stdout)[-600:])
        except importlib.metadata.PackageNotFoundError:
            item.update(status="fail", message="Package is not installed in this Python environment")
        except (OSError, subprocess.TimeoutExpired) as error:
            item.update(status="fail", message="Import probe did not complete", detail=str(error))
        if item["status"] == "fail":
            item["remedy"] = display_command([sys.executable, "-m", "pip", "install", "-r", root / "requirements.txt"])
        checks.append(item)
    if not checks:
        checks.append({"id": "requirements", "status": "fail", "message": "No runtime requirements found",
                       "remedy": "Restore requirements.txt by reinstalling SlideMuse."})
    return checks


def diagnose(root: Path = ROOT, *, backend="auto", require_renderer=False):
    checks = [{"id": "python", "status": "pass" if sys.version_info >= (3, 10) else "fail",
               "message": "Python " + sys.version.split()[0], "minimum": "3.10"}]
    if checks[0]["status"] == "fail":
        checks[0]["remedy"] = "Run SlideMuse with Python 3.10 or newer."
    checks.extend(requirement_checks(root))
    renderer = renderer_environment(backend)
    checks.append({"id": "renderer", "status": "pass" if renderer["ready"] else "fail" if require_renderer else "warning",
                   "message": "Discovery only: program paths and Windows registration; actual rendering is not tested.",
                   "requested": backend, "available": renderer["available"],
                   **({"remedy": "Install PowerPoint on Windows, or put LibreOffice and Poppler (soffice, pdftoppm) on PATH."}
                      if not renderer["ready"] else {})})
    try:
        version_match = re.search(r"^version:\s*(\d+\.\d+\.\d+)\s*$",
                                  (root / "manifest.yaml").read_text(encoding="utf-8-sig"), re.MULTILINE)
        skill_version = version_match[1] if version_match else "unknown"
    except OSError:
        skill_version = "unknown"
    return {"schema_version": "1.0", "skill_version": skill_version,
            "status": "fail" if any(c["status"] == "fail" for c in checks) else
            "warning" if any(c["status"] == "warning" for c in checks) else "pass",
            "python": sys.executable, "skill_root": str(root), "checks": checks,
            "scope": "Local runtime only. Host document reading, vision and image-generation capabilities are not tested."}


def emit(result, as_json=False):
    if as_json:
        # ASCII JSON also works in legacy Windows consoles and redirected files.
        print(json.dumps(result, ensure_ascii=True, indent=2))
        return
    lines = ["SlideMuse runtime: " + result["status"], "Python: " + result["python"]]
    for item in result["checks"]:
        lines.append(f"[{item['status'].upper()}] {item['id']}: {item.get('message', item.get('version', ''))}")
        if item.get("available") is not None:
            lines.append("  Available: " + json.dumps(item["available"]))
        if item.get("detail"):
            lines.append("  Detail: " + item["detail"].strip())
        if item.get("remedy"):
            lines.append("  Next: " + item["remedy"])
    lines.append(result["scope"])
    text = "\n".join(lines)
    print(text.encode(sys.stdout.encoding or "utf-8", errors="backslashreplace").decode(sys.stdout.encoding or "utf-8"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Emit a stable structured report")
    parser.add_argument("--backend", choices=("auto", "powerpoint", "libreoffice"), default="auto")
    parser.add_argument("--require-renderer", action="store_true", help="Treat an undiscovered renderer as a failure")
    args = parser.parse_args()
    result = diagnose(backend=args.backend, require_renderer=args.require_renderer)
    emit(result, args.json)
    raise SystemExit(1 if result["status"] == "fail" else 0)


if __name__ == "__main__":
    main()
