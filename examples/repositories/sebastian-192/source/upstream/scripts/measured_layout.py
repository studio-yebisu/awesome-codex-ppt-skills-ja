"""Interpret real PowerPoint text bounds; warnings never substitute for visual review."""
from __future__ import annotations

import math


def findings(measurement, slide_id):
    items = measurement["items"]
    result, visible = [], []
    width, height = measurement["slide_width_pt"], measurement["slide_height_pt"]
    for item in items:
        identity = {"page_number": measurement["page_number"], "slide_id": slide_id,
                    "element_id": item["element_id"], "method": "powerpoint-text-bounds"}
        if "cell" in item:
            identity["cell"] = item["cell"]
        if item["status"] == "unverified":
            result.append({**identity, "status": "unverified", "reason": item["reason"]})
            continue
        numeric = [*item["bounds"], width, height]
        if not all(isinstance(n, (int, float)) and not isinstance(n, bool) and math.isfinite(n) for n in numeric):
            raise ValueError("Nonfinite PowerPoint bounds")
        x, y, w, h = item["bounds"]
        outside = x < -1 or y < -1 or x + w > width + 1 or y + h > height + 1
        if item["status"] == "table_bounds":
            if outside:
                result.append({**identity, "status": "risk", "kind": "table_outside_slide",
                               "reason": "Actual PowerPoint table bounds extend outside the slide", "bounds": item["bounds"]})
            continue
        overflow = (item["content_width_pt"] > item["available_width_pt"] + 1
                    or item["content_height_pt"] > item["available_height_pt"] + 1)
        result.append({**identity, "status": "risk" if overflow or outside else "no_obvious_risk",
                       "kind": "measured_text_overflow", "reason": "Actual text bounds exceed available space" if overflow or outside else "No measured overflow; visual review remains required",
                       "measurement": item})
        if w > 0 and h > 0:
            visible.append((identity, item["bounds"]))
    for index, (first, a) in enumerate(visible):
        for second, b in visible[index + 1:]:
            if first["element_id"] == second["element_id"]:
                continue
            overlap_w = min(a[0] + a[2], b[0] + b[2]) - max(a[0], b[0])
            overlap_h = min(a[1] + a[3], b[1] + b[3]) - max(a[1], b[1])
            if overlap_w > 1 and overlap_h > 1 and overlap_w * overlap_h > min(a[2] * a[3], b[2] * b[3]) * .05:
                result.append({**first, "status": "risk", "kind": "text_overlap", "other_element_id": second["element_id"],
                               "reason": "Actual text bounds overlap; check intentional layering in the render"})
    return result
