#!/usr/bin/env python3
"""Validate a PradaSlides asset-manifest.json and optional semantic review."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

from _report import Diagnostic, emit_report, load_json


ASSET_ID = re.compile(r"^A\d{2,}$")
KINDS = {"image", "video"}
REVIEW_STATUS = {"pending", "reviewed", "excluded"}
ROLES = {
    "unclassified",
    "exclude",
    "logo",
    "hero-editorial",
    "product-evidence",
    "screenshot-ui",
    "chart-data",
    "diagram-process",
    "portrait-team",
    "document-proof",
    "texture-background",
    "icon",
    "video-demo",
    "other",
}
CROP = {"unknown", "none", "low", "medium", "high"}
PHASES = {"attention", "orientation", "tension", "insight", "proof", "resolution", "decision", "retention"}


def validate(data: Any, manifest_path: Path, require_reviewed: bool, path_check: bool) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    if not isinstance(data, dict):
        return [Diagnostic("error", "ASSET_ROOT", "Root must be a JSON object")]
    assets = data.get("assets")
    if not isinstance(assets, list):
        return [Diagnostic("error", "ASSET_LIST", "assets must be an array", "assets")]
    seen: set[str] = set()
    known = {item.get("id") for item in assets if isinstance(item, dict)}
    hashes: dict[str, str] = {}
    for index, asset in enumerate(assets):
        loc = f"assets[{index}]"
        if not isinstance(asset, dict):
            diagnostics.append(Diagnostic("error", "ASSET_TYPE", "Asset entry must be an object", loc))
            continue
        asset_id = asset.get("id")
        if not isinstance(asset_id, str) or not ASSET_ID.match(asset_id):
            diagnostics.append(Diagnostic("error", "ASSET_ID", "Asset id must match A01, A02, ...", f"{loc}.id"))
            continue
        if asset_id in seen:
            diagnostics.append(Diagnostic("error", "ASSET_DUP_ID", f"Duplicate asset id {asset_id}", f"{loc}.id"))
        seen.add(asset_id)
        if asset.get("kind") not in KINDS:
            diagnostics.append(Diagnostic("error", "ASSET_KIND", f"Unknown kind {asset.get('kind')!r}", f"{loc}.kind"))
        path_value = asset.get("path")
        if not isinstance(path_value, str) or not path_value.strip():
            diagnostics.append(Diagnostic("error", "ASSET_PATH", "path is required", f"{loc}.path"))
        elif path_check:
            source = Path(path_value)
            if not source.is_absolute():
                source = manifest_path.parent / source
            if not source.exists():
                diagnostics.append(Diagnostic("error", "ASSET_FILE_MISSING", f"Asset file not found: {source.resolve()}", f"{loc}.path"))
        digest = asset.get("sha256")
        if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
            diagnostics.append(Diagnostic("error", "ASSET_HASH", "sha256 must contain 64 lowercase hex characters", f"{loc}.sha256"))
        elif digest in hashes and not asset.get("duplicate_of"):
            diagnostics.append(Diagnostic("warning", "ASSET_DUP_HASH", f"Matches {hashes[digest]} but duplicate_of is empty", loc))
        else:
            hashes.setdefault(digest, asset_id)
        duplicate_of = asset.get("duplicate_of")
        if duplicate_of is not None and duplicate_of not in known:
            diagnostics.append(Diagnostic("error", "ASSET_DUP_REF", f"duplicate_of references unknown asset {duplicate_of}", f"{loc}.duplicate_of"))
        technical = asset.get("technical")
        if not isinstance(technical, dict):
            diagnostics.append(Diagnostic("error", "ASSET_TECH", "technical must be an object", f"{loc}.technical"))
        elif technical.get("inspection_error"):
            diagnostics.append(Diagnostic("warning", "ASSET_INSPECTION", str(technical["inspection_error"]), f"{loc}.technical"))

        semantic = asset.get("semantic")
        if not isinstance(semantic, dict):
            diagnostics.append(Diagnostic("error", "ASSET_SEMANTIC", "semantic must be an object", f"{loc}.semantic"))
            semantic = {}
        status = semantic.get("review_status")
        if status not in REVIEW_STATUS:
            diagnostics.append(Diagnostic("error", "ASSET_REVIEW_STATUS", f"Unknown review_status {status!r}", f"{loc}.semantic.review_status"))
        role = semantic.get("role")
        if role not in ROLES:
            diagnostics.append(Diagnostic("error", "ASSET_ROLE", f"Unknown role {role!r}", f"{loc}.semantic.role"))
        crop = semantic.get("crop_tolerance")
        if crop not in CROP:
            diagnostics.append(Diagnostic("error", "ASSET_CROP", f"Unknown crop_tolerance {crop!r}", f"{loc}.semantic.crop_tolerance"))

        placement = asset.get("placement")
        if not isinstance(placement, dict):
            diagnostics.append(Diagnostic("error", "ASSET_PLACEMENT", "placement must be an object", f"{loc}.placement"))
            placement = {}
        phases = placement.get("journey_phases", [])
        if not isinstance(phases, list) or any(phase not in PHASES for phase in phases):
            diagnostics.append(Diagnostic("error", "ASSET_PHASE", "journey_phases contains an unknown value", f"{loc}.placement.journey_phases"))

        if require_reviewed and status == "pending":
            diagnostics.append(Diagnostic("error", "ASSET_PENDING", "Semantic review is still pending", f"{loc}.semantic.review_status"))
        if require_reviewed and status == "reviewed":
            if role in {"unclassified", "exclude"}:
                diagnostics.append(Diagnostic("error", "ASSET_UNCLASSIFIED", "Reviewed asset needs a usable role or status excluded", f"{loc}.semantic.role"))
            for key in ("subject", "message", "rights", "sensitivity", "alt_text"):
                value = semantic.get(key)
                if not isinstance(value, str) or not value.strip() or value.strip().casefold() in {"unknown", "unreviewed"}:
                    diagnostics.append(Diagnostic("error", "ASSET_REVIEW_FIELD", f"Reviewed asset requires resolved '{key}'", f"{loc}.semantic.{key}"))
            if crop == "unknown":
                diagnostics.append(Diagnostic("error", "ASSET_REVIEW_CROP", "Reviewed asset needs a crop tolerance", f"{loc}.semantic.crop_tolerance"))
            if not str(placement.get("recommended", "")).strip():
                diagnostics.append(Diagnostic("error", "ASSET_RECOMMEND", "Reviewed asset needs placement.recommended", f"{loc}.placement.recommended"))
        if status == "excluded" and role != "exclude":
            diagnostics.append(Diagnostic("warning", "ASSET_EXCLUDE_ROLE", "Excluded asset should normally use role 'exclude'", f"{loc}.semantic.role"))
    return diagnostics


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest")
    parser.add_argument("--require-reviewed", action="store_true")
    parser.add_argument("--skip-path-check", action="store_true")
    parser.add_argument("--json-output")
    args = parser.parse_args()
    path = Path(args.manifest).expanduser().resolve()
    try:
        data = load_json(path)
    except ValueError as exc:
        return emit_report("asset manifest validation", [Diagnostic("error", "ASSET_JSON", str(exc))], json_output=args.json_output)
    return emit_report(
        "asset manifest validation",
        validate(data, path, args.require_reviewed, not args.skip_path_check),
        json_output=args.json_output,
        extra={"file": str(path)},
    )


if __name__ == "__main__":
    raise SystemExit(main())
