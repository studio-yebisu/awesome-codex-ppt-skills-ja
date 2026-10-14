#!/usr/bin/env python3
"""Package a writable SlidePoise Skill copy as skill.zip after objective preflight."""
from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAX_BYTES = 25 * 1024 * 1024
SKIP_PARTS = {"__pycache__", ".DS_Store", ".git", "work", "deliverables"}


def run(script: str, *args: str) -> None:
    result = subprocess.run([sys.executable, str(ROOT / "scripts" / script), *args], text=True, capture_output=True)
    if result.returncode:
        raise SystemExit((result.stderr or result.stdout).strip())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path.cwd())
    args = parser.parse_args()
    if not (ROOT / "SKILL.md").is_file() or not (ROOT / "agents/openai.yaml").is_file():
        raise SystemExit("Skill root is incomplete")
    run("audit_skill_boundaries.py")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    output = args.output_dir / "skill.zip"
    if args.output_dir.resolve().is_relative_to(ROOT.resolve()):
        raise SystemExit("Package output directory must be outside the skill source")
    with tempfile.NamedTemporaryFile(dir=args.output_dir, suffix=".zip", delete=False) as handle:
        staged = Path(handle.name)
    try:
        with zipfile.ZipFile(staged, "w", zipfile.ZIP_DEFLATED) as archive:
            for path in sorted(ROOT.rglob("*")):
                if not path.is_file() or any(part in SKIP_PARTS for part in path.relative_to(ROOT).parts):
                    continue
                archive.write(path, Path(ROOT.name) / path.relative_to(ROOT))
        size = staged.stat().st_size
        if size > MAX_BYTES:
            raise SystemExit(f"Packaged Skill exceeds 25 MB: {size} bytes")
        staged.replace(output)
    finally:
        staged.unlink(missing_ok=True)
    print(output)


if __name__ == "__main__":
    main()
