#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image, ImageOps


IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}
DEFAULT_EXCLUDED_DIR_NAMES = {
    "preview",
    "previews",
    "screenshots",
    "montage",
    "montages",
    "pptx",
    "html",
    "pdf",
    "reports",
    "annotated_issues",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def parse_since(value: str | None) -> float | None:
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        pass
    normalized = value.strip().replace("Z", "+00:00")
    return datetime.fromisoformat(normalized).timestamp()


def marker_time(marker: Path) -> float | None:
    if not marker.exists():
        return None
    try:
        data = json.loads(marker.read_text(encoding="utf-8-sig"))
        if "timestamp" in data:
            return float(data["timestamp"])
    except Exception:
        pass
    try:
        return marker.stat().st_mtime
    except OSError:
        return None


def default_scan_dirs(run_dir: Path) -> list[Path]:
    root = project_root()
    home = Path.home()
    one_drive = home / "OneDrive"
    dirs = [
        run_dir / "images",
        root / "incoming_assets" / "imagegen_handoff",
        root / "incoming_assets",
        root / "outputs",
        root / "capability_tests" / "imagegen_probe",
        home / ".codex" / "generated_images",
        home / ".codex" / "attachments",
        home / "Downloads",
        home / "Desktop",
        home / "Pictures",
        one_drive / "Downloads",
        one_drive / "Desktop",
        one_drive / "Pictures",
        home / "AppData" / "Local" / "Temp",
    ]
    return [d for d in dirs if d.exists()]


def is_excluded_generated_output(path: Path) -> bool:
    lowered_parts = [part.lower() for part in path.parts]
    lowered_name = path.name.lower()
    return (
        any(part in DEFAULT_EXCLUDED_DIR_NAMES for part in lowered_parts)
        or "montage" in lowered_name
        or "reference_board" in lowered_name
        or lowered_name.startswith("screenshot_")
        or lowered_name.startswith("screen shot")
        or lowered_name.startswith("snip")
        or lowered_name.startswith("qa_report")
        or lowered_name.startswith("aesthetic_qa")
    )


def iter_images(base: Path, cutoff: float | None) -> list[Path]:
    if base.is_file():
        candidates = [base]
    else:
        try:
            candidates = [p for p in base.rglob("*") if p.is_file()]
        except OSError:
            return []
    out: list[Path] = []
    for path in candidates:
        if not base.is_file() and is_excluded_generated_output(path.relative_to(base) if path.is_relative_to(base) else path):
            continue
        if path.suffix.lower() not in IMAGE_EXTS:
            continue
        try:
            stat = path.stat()
        except OSError:
            continue
        if cutoff is not None and stat.st_mtime < cutoff - 2:
            continue
        out.append(path)
    return out


def inspect_image(path: Path) -> dict[str, Any] | None:
    try:
        with Image.open(path) as img:
            width, height = img.size
            fmt = img.format or path.suffix.lower().lstrip(".")
        return {
            "path": str(path),
            "width": width,
            "height": height,
            "format": fmt,
            "mtime": path.stat().st_mtime,
            "mtime_iso": datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat(),
            "size_bytes": path.stat().st_size,
        }
    except Exception:
        return None


def parse_aspect(value: str | None) -> float | None:
    if not value:
        return None
    if ":" in value:
        left, right = value.split(":", 1)
        return float(left) / float(right)
    return float(value)


def valid_meta(meta: dict[str, Any], min_width: int, min_height: int, aspect: float | None, aspect_tolerance: float) -> tuple[bool, str]:
    width = int(meta["width"])
    height = int(meta["height"])
    if width < min_width or height < min_height:
        return False, f"too small: {width}x{height}"
    if aspect:
        ratio = width / height
        if abs(ratio - aspect) / aspect > aspect_tolerance:
            return False, f"aspect mismatch: {ratio:.3f}"
    return True, "ok"


def collect_candidates(args: argparse.Namespace, cutoff: float | None) -> tuple[list[dict[str, Any]], list[str]]:
    scan_dirs: list[Path] = []
    warnings: list[str] = []
    for raw in args.candidate or []:
        scan_dirs.append(Path(raw).expanduser())
    for raw in args.scan_dir or []:
        scan_dirs.append(Path(raw).expanduser())
    if not args.no_default_scan:
        scan_dirs.extend(default_scan_dirs(args.run_dir))

    seen: set[Path] = set()
    metas: list[dict[str, Any]] = []
    aspect = parse_aspect(args.aspect)
    for base in scan_dirs:
        if not base.exists():
            warnings.append(f"scan path missing: {base}")
            continue
        for path in iter_images(base, cutoff):
            resolved = path.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            meta = inspect_image(resolved)
            if not meta:
                continue
            ok, reason = valid_meta(meta, args.min_width, args.min_height, aspect, args.aspect_tolerance)
            meta["valid"] = ok
            meta["reject_reason"] = "" if ok else reason
            metas.append(meta)
    metas.sort(key=lambda item: (bool(item["valid"]), float(item["mtime"]), int(item["size_bytes"])), reverse=True)
    return metas, warnings


def wait_for_candidates(args: argparse.Namespace, cutoff: float | None) -> tuple[list[dict[str, Any]], list[str]]:
    deadline = time.time() + max(0, args.watch_seconds)
    all_warnings: list[str] = []
    while True:
        candidates, warnings = collect_candidates(args, cutoff)
        all_warnings = warnings
        if any(item.get("valid") for item in candidates):
            return candidates, all_warnings
        if args.watch_seconds <= 0 or time.time() >= deadline:
            return candidates, all_warnings
        time.sleep(max(0.25, args.poll_interval))


def copy_image(source: Path, dest_dir: Path, slide_id: str | None, force_png: bool) -> Path:
    dest_dir.mkdir(parents=True, exist_ok=True)
    stem = slide_id or f"imagegen_{int(time.time())}"
    ext = source.suffix.lower()
    if force_png or ext not in {".png", ".jpg", ".jpeg"}:
        dest = dest_dir / f"{stem}.png"
        with Image.open(source) as img:
            img = ImageOps.exif_transpose(img)
            if img.mode not in ("RGB", "RGBA"):
                img = img.convert("RGBA")
            img.save(dest)
        return dest.resolve()
    dest = dest_dir / f"{stem}{ext}"
    shutil.copy2(source, dest)
    return dest.resolve()


def load_asset_plan(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"assets": []}
    return json.loads(path.read_text(encoding="utf-8-sig"))


def update_asset_plan(path: Path, slide_id: str | None, dest: Path | None, source: Path | None, status: str, reason: str, allow_create: bool) -> list[str]:
    warnings: list[str] = []
    data = load_asset_plan(path)
    assets = data.setdefault("assets", [])
    item = None
    if slide_id:
        for candidate in assets:
            if candidate.get("slide_id") == slide_id:
                item = candidate
                break
        if item is None and allow_create:
            item = {
                "slide_id": slide_id,
                "visual_need": "required",
                "asset_type": "concept_illustration",
                "generation_required": True,
                "reason": "Captured from Codex built-in image generation.",
                "must_not_skip": True,
            }
            assets.append(item)
        elif item is None:
            warnings.append(f"slide_id not found in asset_plan: {slide_id}")
    if item is not None:
        item["generation_backend"] = "codex_builtin_imagegen"
        item["capture_status"] = status
        item["captured_at"] = utc_now()
        if dest:
            item["status"] = "generated"
            item["output_path"] = str(dest)
            item["capture_source"] = str(source) if source else ""
            item.pop("failed_reason", None)
        else:
            item["status"] = "failed"
            item["failed_reason"] = reason
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return warnings


def write_marker(run_dir: Path, marker: Path) -> None:
    marker.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "created_at": utc_now(),
        "timestamp": time.time(),
        "run_dir": str(run_dir.resolve()),
        "purpose": "Created immediately before calling built-in imagegen so the capture step can find newly persisted images.",
    }
    marker.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Capture a persisted Codex imagegen asset and copy it into a PPT run directory.")
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--asset-plan", type=Path)
    parser.add_argument("--slide-id")
    parser.add_argument("--candidate", action="append", help="Explicit file or directory to prefer.")
    parser.add_argument("--scan-dir", action="append", help="Additional directory to scan.")
    parser.add_argument("--no-default-scan", action="store_true")
    parser.add_argument("--marker", type=Path)
    parser.add_argument("--write-marker", action="store_true")
    parser.add_argument("--since")
    parser.add_argument("--recent-minutes", type=float, default=30)
    parser.add_argument("--watch-seconds", type=float, default=0, help="Poll scan locations for this many seconds before failing.")
    parser.add_argument("--poll-interval", type=float, default=1.0)
    parser.add_argument("--dest-dir", type=Path)
    parser.add_argument("--min-width", type=int, default=256)
    parser.add_argument("--min-height", type=int, default=144)
    parser.add_argument("--aspect", default="")
    parser.add_argument("--aspect-tolerance", type=float, default=0.18)
    parser.add_argument("--force-png", action="store_true")
    parser.add_argument("--allow-create", action="store_true")
    parser.add_argument("--no-update-asset-plan", action="store_true")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    args.run_dir = args.run_dir.resolve()
    asset_plan = args.asset_plan or (args.run_dir / "asset_plan.json")
    marker = args.marker or (args.run_dir / "imagegen_capture_marker.json")
    report_path = args.report or (args.run_dir / "imagegen_capture_report.json")

    if args.write_marker:
        write_marker(args.run_dir, marker)
        report = {"status": "MARKER_WRITTEN", "marker": str(marker.resolve()), "created_at": utc_now()}
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0

    cutoff = parse_since(args.since)
    if cutoff is None:
        cutoff = marker_time(marker)
    if cutoff is None and not args.candidate:
        cutoff = time.time() - args.recent_minutes * 60

    candidates, warnings = wait_for_candidates(args, cutoff)
    selected = next((item for item in candidates if item.get("valid")), None)

    report: dict[str, Any] = {
        "created_at": utc_now(),
        "run_dir": str(args.run_dir),
        "asset_plan": str(asset_plan),
        "slide_id": args.slide_id,
        "marker": str(marker),
        "cutoff": cutoff,
        "status": "",
        "selected": None,
        "copied_to": "",
        "warnings": warnings,
        "candidates": candidates[:30],
    }

    if selected:
        source = Path(str(selected["path"]))
        dest = copy_image(source, args.dest_dir or (args.run_dir / "images"), args.slide_id, args.force_png)
        if not args.no_update_asset_plan:
            report["warnings"].extend(update_asset_plan(asset_plan, args.slide_id, dest, source, "captured", "", args.allow_create))
        report["status"] = "CAPTURED"
        report["selected"] = selected
        report["copied_to"] = str(dest)
    else:
        reason = "IMAGEGEN_OUTPUT_NOT_DISCOVERABLE"
        if not args.no_update_asset_plan and args.slide_id:
            report["warnings"].extend(update_asset_plan(asset_plan, args.slide_id, None, None, "not_discoverable", reason, args.allow_create))
        report["status"] = reason
        report["warnings"].append("No valid persisted image was found. If imagegen only returned an inline UI asset, it cannot be inserted into PPT until it is exposed as a file, attachment, or bytes.")

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "CAPTURED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
