#!/usr/bin/env python3
"""One entry point for SlideMuse's existing local tools (no new dependencies)."""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COMMANDS = {
    "doctor": ("scripts/doctor.py", (), "Check Python, dependencies and renderer discovery"),
    "init": ("scripts/init_deck.py", (), "Create a job from prepared specifications"),
    "check": ("scripts/run_deck.py", ("--check",), "Read-only job preflight"),
    "run": ("scripts/run_deck.py", (), "Build, render, evaluate or resume a job"),
    "render": ("scripts/render_deck.py", (), "Render an existing PPTX for review"),
    "validate": ("scripts/validate_page_spec.py", (), "Validate a Page Spec"),
    "audit": ("scripts/audit_editability.py", (), "Audit native PPTX objects"),
    "review": ("scripts/review_panel.py", (), "Export a review panel or import its records"),
    "sample": ("showcase/editable-irena/reproduce.py", (), "Rebuild the public editable sample"),
}


def skill_version(root: Path) -> str:
    try:
        text = (root / "manifest.yaml").read_text(encoding="utf-8-sig")
    except OSError:
        return "unknown"
    match = re.search(r"^version:\s*(\d+\.\d+\.\d+)\s*$", text, re.MULTILINE)
    return match.group(1) if match else "unknown"


def runtime_python(root: Path) -> Path:
    """Use this installation's environment, even after the directory is moved."""
    candidate = root / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    # Do not resolve POSIX venv symlinks: their path selects pyvenv.cfg.
    return candidate.absolute() if candidate.is_file() else Path(sys.executable)


def main(argv=None) -> int:
    descriptions = "\n".join(f"  {name:10} {entry[2]}" for name, entry in COMMANDS.items())
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=descriptions + "\n\nUse <command> --help for the original tool's options.",
    )
    parser.add_argument("--version", action="version", version="SlideMuse " + skill_version(ROOT))
    parser.add_argument("command", nargs="?", choices=COMMANDS)
    parser.add_argument("arguments", nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)
    if args.command is None:
        parser.print_help()
        return 0
    relative, extra, _ = COMMANDS[args.command]
    script = ROOT / relative
    if not script.is_file():
        parser.exit(2, f"slidemuse: missing packaged tool: {relative}. Reinstall SlideMuse.\n")
    command = [str(runtime_python(ROOT)), str(script), *args.arguments, *extra]
    try:
        # Keep cwd, stdin/stdout/stderr and exit codes identical to direct scripts.
        return subprocess.run(command, check=False).returncode
    except OSError as error:
        parser.exit(2, f"slidemuse: cannot start {command[0]}: {error}\n")
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
