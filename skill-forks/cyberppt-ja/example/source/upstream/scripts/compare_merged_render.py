#!/usr/bin/env python3
"""Compare merged-deck page renders against approved single-page renders."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def mean_abs_diff(path_a: Path, path_b: Path) -> float:
    try:
        from PIL import Image
        import numpy as np
    except ImportError as exc:
        raise SystemExit("Pillow and numpy are required for compare_merged_render.py") from exc
    with Image.open(path_a).convert("RGB") as a, Image.open(path_b).convert("RGB") as b:
        b = b.resize(a.size)
        return float(np.mean(np.abs(np.asarray(a, dtype="int16") - np.asarray(b, dtype="int16"))))


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare merged render PNGs to approved page render PNGs.")
    parser.add_argument("--approved-dir", required=True)
    parser.add_argument("--merged-dir", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--threshold", type=float, default=2.0)
    args = parser.parse_args()

    approved_dir = Path(args.approved_dir)
    merged_dir = Path(args.merged_dir)
    results = []
    failures = []
    for approved in sorted(approved_dir.glob("*.png")):
        merged = merged_dir / approved.name
        if not merged.exists():
            failures.append({"page": approved.name, "code": "MERGED_RENDER_MISSING"})
            continue
        diff = mean_abs_diff(approved, merged)
        row = {"page": approved.name, "mean_abs_diff": round(diff, 3), "threshold": args.threshold}
        results.append(row)
        if diff > args.threshold:
            failures.append({"page": approved.name, "code": "MERGE_RENDER_DIFF_EXCEEDED", "mean_abs_diff": round(diff, 3)})

    report = {"passed": not failures, "results": results, "failures": failures}
    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"path": str(output), "passed": report["passed"], "failures": len(failures)}, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
