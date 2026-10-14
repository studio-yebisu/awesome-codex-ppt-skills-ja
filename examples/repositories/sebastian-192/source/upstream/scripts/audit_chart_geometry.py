#!/usr/bin/env python3
"""Check manually observed bar endpoints against source values; does not perform vision/OCR."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from json_io import read_json
from PIL import Image, ImageOps
from render_deck import sha256
from validate_page_spec import _relative_path, load_page_spec


def number(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError("Geometry coordinates and values must be finite numbers")
    return value


def chart_series(element):
    data = element["data"]
    if not isinstance(data, dict) or data.get("chart_type") not in ("bar", "column"):
        raise ValueError("Geometry audit supports bar/column charts only")
    categories, series = data.get("categories"), data.get("series")
    if (not isinstance(categories, list) or not categories or any(not isinstance(c, str) for c in categories)
            or len(set(categories)) != len(categories) or not isinstance(series, list) or not series):
        raise ValueError("Charts require distinct categories and at least one series")
    names = []
    for item in series:
        name = item.get("name", "Series" if len(series) == 1 else None) if isinstance(item, dict) else None
        if not isinstance(name, str) or not name:
            raise ValueError("Every series needs a nonempty name")
        names.append(name)
        values = item.get("values")
        if not isinstance(values, list) or len(values) != len(categories):
            raise ValueError("Categories/values mismatch")
        for value in values:
            number(value)
    if len(set(names)) != len(names):
        raise ValueError("Series names must be distinct")
    if data.get("stacked", False):
        raise ValueError("Stacked charts are not supported by this geometry contract")
    if number(data.get("baseline", 0)) != 0:
        raise ValueError("This bar geometry audit requires a zero baseline")
    series = [{**item, "name": name} for item, name in zip(series, names)]
    return data, categories, series


def bar_data(element):
    data, categories, series = chart_series(element)
    if len(series) != 1:
        raise ValueError("This operation requires one series")
    return data, categories, series[0]["values"]


def bar_items(categories, series):
    return [({"category": category, **({"series": item["name"]} if len(series) > 1 else {})},
             item["values"][index])
            for index, category in enumerate(categories) for item in series]


def charts(spec, slide_id=None):
    if slide_id and slide_id not in {s["id"] for s in spec["slides"]}:
        raise ValueError(f"Unknown slide: {slide_id}")
    return [(slide, element) for slide in spec["slides"] if not slide_id or slide["id"] == slide_id
            for element in slide["elements"] if element["kind"] == "chart"
            and isinstance(element["data"], dict) and element["data"].get("chart_type") in ("bar", "column")]


def template(spec_path, spec, slide_id=None):
    result = {"version": "1.0", "page_spec_sha256": sha256(spec_path), "charts": []}
    for slide, element in charts(spec, slide_id):
        _, categories, series = chart_series(element)
        image = _relative_path(spec_path.parent, slide["image_file"])
        result["charts"].append({"slide_id": slide["id"], "element_id": element["id"],
                                 "image_sha256": sha256(image), "status": "pending",
                                 "axis": [{"value": None, "pixel": None}, {"value": None, "pixel": None}],
                                 "bars": [{**identity, "start": None, "end": None}
                                          for identity, _ in bar_items(categories, series)]})
    return result


def audit(spec_path, observation_path, slide_id=None, tolerance=2.5):
    spec_path = spec_path.resolve()
    spec, _ = load_page_spec(spec_path)
    observations = read_json(observation_path)
    if observations.get("version") != "1.0" or observations.get("page_spec_sha256") != sha256(spec_path):
        raise ValueError("Chart geometry observations are stale; recreate after Page Spec changes")
    tolerance = number(tolerance)
    if not 0 <= tolerance <= 10:
        raise ValueError("Pixel tolerance must be between 0 and 10")
    expected = {(s["id"], e["id"]): (s, e) for s, e in charts(spec, slide_id)}
    all_expected = {(s["id"], e["id"]) for s, e in charts(spec)}
    entries = observations.get("charts")
    if not isinstance(entries, list):
        raise TypeError("Geometry observations need a charts list")
    seen, findings, pending, results = set(), [], [], []
    for entry in entries:
        key = (entry["slide_id"], entry["element_id"])
        if key in seen or key not in all_expected:
            raise ValueError(f"Unknown or duplicate chart geometry entry: {key}")
        seen.add(key)
        if key not in expected:
            continue
        slide, element = expected[key]
        data, categories, series = chart_series(element)
        image = _relative_path(spec_path.parent, slide["image_file"])
        if entry.get("image_sha256") != sha256(image):
            raise ValueError(f"Chart image changed: {key}")
        if entry.get("status") == "pending":
            pending.append(list(key))
            continue
        if entry.get("status") != "complete":
            raise ValueError(f"Geometry status must be pending or complete: {key}")
        anchors = entry.get("axis")
        if not isinstance(anchors, list) or len(anchors) != 2:
            raise ValueError("Record two independently observed axis anchors")
        a, b = anchors
        av, bv, ap, bp = (number(a["value"]), number(b["value"]), number(a["pixel"]), number(b["pixel"]))
        if av == bv or ap == bp:
            raise ValueError("Axis anchors must span distinct values and pixels")
        with Image.open(image) as opened:
            size = ImageOps.exif_transpose(opened).size
        extent = size[0 if data["chart_type"] == "bar" else 1]
        if not all(0 <= p < extent for p in (ap, bp)):
            raise ValueError("Axis pixel outside image")
        scale = (bp - ap) / (bv - av)
        if (data["chart_type"] == "bar" and scale < 0) or (data["chart_type"] == "column" and scale > 0):
            raise ValueError("Axis direction disagrees with chart orientation")
        zero = ap - av * scale
        if not 0 <= zero < extent:
            raise ValueError("Zero baseline is outside image")
        bars = entry.get("bars")
        items = bar_items(categories, series)
        if (not isinstance(bars, list) or len(bars) != len(items)
                or any(any(bar.get(k) != v for k, v in identity.items())
                       or (len(series) == 1 and "series" in bar and bar["series"] != series[0]["name"])
                       for bar, (identity, _) in zip(bars, items))):
            raise ValueError("Observed bars must match source category and series order")
        for bar, (identity, value) in zip(bars, items):
            start, end = number(bar["start"]), number(bar["end"])
            if not all(0 <= p < extent for p in (start, end)):
                raise ValueError("Bar pixel outside image")
            wanted = zero + value * scale
            residual = max(abs(start - zero), abs(end - wanted))
            direction_ok = abs(value * scale) <= tolerance or (end - start) * value * scale > 0
            result = {"slide_id": key[0], "element_id": key[1], **identity,
                      "value": value, "expected_start": zero, "expected_end": wanted,
                      "observed_start": start, "observed_end": end, "max_error_px": residual,
                      "status": "pass" if residual <= tolerance and direction_ok else "fail"}
            results.append(result)
            if result["status"] == "fail":
                findings.append(result)
    pending.extend(list(key) for key in expected if key not in seen)
    return {"status": "fail" if findings else "incomplete" if pending else "pass",
            "page_spec_sha256": sha256(spec_path), "observations_sha256": sha256(observation_path),
            "pixel_tolerance": tolerance, "charts_checked": len(expected) - len(pending),
            "failed": findings, "pending": pending, "bars": results,
            "note": "Checks recorded pixel observations, not image recognition or source reliability."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("page_spec", type=Path)
    parser.add_argument("observations", type=Path)
    parser.add_argument("--init", action="store_true")
    parser.add_argument("--slide")
    parser.add_argument("--tolerance", type=float, default=2.5)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        if args.init:
            if args.observations.exists():
                raise ValueError("Observation file already exists")
            spec, _ = load_page_spec(args.page_spec)
            result = template(args.page_spec.resolve(), spec, args.slide)
            target = args.observations
        else:
            result = audit(args.page_spec, args.observations, args.slide, args.tolerance)
            target = args.output
        if target:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps(result, ensure_ascii=True))
        if not args.init and result["status"] != "pass":
            raise SystemExit(1)
    except (ValueError, OSError, KeyError, TypeError) as error:
        parser.exit(2, f"audit_chart_geometry: {error}\n")


if __name__ == "__main__":
    main()
