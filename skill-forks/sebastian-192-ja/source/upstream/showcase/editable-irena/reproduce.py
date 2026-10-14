#!/usr/bin/env python3
"""Rebuild the public IRENA sample with repository or bundled SlideMuse scripts."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

CASE = Path(__file__).resolve().parent
VARIANTS = ("text-edit", "object-move", "table-edit", "chart-edit")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def runtime_root(explicit: Path | None) -> Path:
    candidates = [explicit] if explicit else [CASE / "runtime", *CASE.parents]
    for candidate in candidates:
        if candidate and (candidate / "scripts/build_editable_ppt.py").is_file():
            return candidate.resolve()
    raise ValueError("Use --runtime with a SlideMuse checkout, or download the complete sample ZIP.")


def verify_package() -> dict:
    manifest = json.loads((CASE / "manifest.json").read_text(encoding="utf-8"))
    for item in manifest["files"]:
        path = (CASE / item["path"]).resolve()
        if not path.is_relative_to(CASE) or not path.is_file():
            raise ValueError(f"Missing or unsafe sample file: {item['path']}")
        if digest(path) != item["sha256"]:
            raise ValueError(f"Sample file changed: {item['path']}")
    snapshot = CASE / "runtime/runtime-manifest.json"
    runtime_files = 0
    if snapshot.is_file():
        data = json.loads(snapshot.read_text(encoding="utf-8"))
        for item in data["files"]:
            path = (snapshot.parent / item["path"]).resolve()
            if not path.is_relative_to(snapshot.parent) or not path.is_file() or digest(path) != item["sha256"]:
                raise ValueError(f"Bundled runtime changed: {item['path']}")
        runtime_files = len(data["files"])
    return {"sample_files": len(manifest["files"]), "bundled_runtime_files": runtime_files}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime", type=Path, help="SlideMuse repository or bundled runtime root")
    parser.add_argument("--output", type=Path, default=CASE / "outputs", help="Separate build directory")
    parser.add_argument("--render", action="store_true", help="Also export all 36 pages with a real renderer")
    parser.add_argument("--backend", choices=("auto", "powerpoint", "libreoffice"), default="auto")
    parser.add_argument("--verify", action="store_true", help="Check the published file hashes before rebuilding")
    args = parser.parse_args()
    root = runtime_root(args.runtime)
    output = args.output.resolve()
    if output == CASE or CASE.is_relative_to(output):
        parser.error("Output must be a separate child or external directory.")
    output.mkdir(parents=True, exist_ok=True)
    report = {
        "started_at": datetime.now(timezone.utc).isoformat(),
        "runtime": str(root),
        "python": sys.version,
        "input_scene_sha256": digest(CASE / "scene.json"),
        "source_pdf_sha256": digest(CASE / "source/IRENA_Renewable_Capacity_Statistics_2025.pdf"),
        "steps": [],
    }
    if args.verify:
        report["package_verification"] = verify_package()

    def run(script: str, *arguments: str | Path) -> None:
        command = [sys.executable, str(root / "scripts" / script), *map(str, arguments)]
        started = datetime.now(timezone.utc)
        result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", check=False, env={**os.environ, "PYTHONUTF8": "1"})
        record = {
            "script": script,
            "arguments": list(map(str, arguments)),
            "runtime_script_sha256": digest(root / "scripts" / script),
            "elapsed_seconds": round((datetime.now(timezone.utc) - started).total_seconds(), 3),
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
        report["steps"].append(record)
        print(f"{script}: {'OK' if result.returncode == 0 else 'FAIL'}", flush=True)
        if result.returncode:
            print(result.stdout + result.stderr, file=sys.stderr)
            raise RuntimeError(f"{script} exited {result.returncode}")

    try:
        spec = CASE / "page-spec.json"
        run("validate_page_spec.py", spec, "--strict", "--require-images")
        image = output / "image.pptx"
        run("build_image_ppt.py", spec, image)
        run("audit_speaker_notes.py", spec, image, "--output", output / "image-notes.json")
        run("export_speaker_notes.py", spec, output / "speaker-notes.md")
        decks = [("image", image)]
        for name in ("editable", *VARIANTS):
            suffix = "" if name == "editable" else f"-{name}"
            scene = CASE / f"scene{suffix}.json"
            current_spec = CASE / f"page-spec{suffix}.json"
            if suffix:
                run("validate_page_spec.py", current_spec, "--strict")
            deck = output / f"{name}.pptx"
            run("build_editable_ppt.py", scene, deck, "--page-spec", current_spec)
            run("audit_editability.py", deck, "--scene", scene, "--output", output / f"{name}-objects.json")
            run("audit_speaker_notes.py", current_spec, deck, "--scene", scene, "--output", output / f"{name}-notes.json")
            decks.append((name, deck))
        if args.render:
            for name, deck in decks:
                run("render_deck.py", deck, output / f"render-{name}", "--backend", args.backend, "--overwrite")
        report["decks"] = [{"path": path.name, "sha256": digest(path), "pages": 6} for _, path in decks]
        report["status"] = "pass"
    except (ValueError, OSError, RuntimeError) as error:
        report["status"] = "fail"
        report["error"] = str(error)
        raise
    finally:
        report["finished_at"] = datetime.now(timezone.utc).isoformat()
        (output / "reproduction.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Built 6 decks. Report: {output / 'reproduction.json'}")


if __name__ == "__main__":
    main()
