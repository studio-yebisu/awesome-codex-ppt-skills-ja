#!/usr/bin/env python3
"""Validate a PradaSlides layout-manifest.json registry."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

from _report import Diagnostic, emit_report, load_json


ID = re.compile(r"^[a-z][a-z0-9-]*$")
ROLES = {"cover", "section", "content", "pause", "closing", "appendix"}
DENSITIES = {"speaking", "hybrid", "reading"}
TONES = {"light", "dark", "accent", "media"}


def nonempty_strings(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(isinstance(item, str) and item.strip() for item in value)


def validate(value: Any) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    if not isinstance(value, dict):
        return [Diagnostic("error", "LAYOUT_ROOT", "Root must be a JSON object")]
    if value.get("schema_version") != "1.1":
        diagnostics.append(Diagnostic("error", "LAYOUT_SCHEMA", "schema_version must be '1.1'", "schema_version"))
    topologies = value.get("topologies")
    layouts = value.get("layouts")
    if not isinstance(topologies, list) or not topologies:
        return diagnostics + [Diagnostic("error", "LAYOUT_TOPOLOGIES", "topologies must be a non-empty array", "topologies")]
    if not isinstance(layouts, list) or not layouts:
        return diagnostics + [Diagnostic("error", "LAYOUT_LAYOUTS", "layouts must be a non-empty array", "layouts")]

    topology_ids: set[str] = set()
    for index, topology in enumerate(topologies):
        loc = f"topologies[{index}]"
        if not isinstance(topology, dict):
            diagnostics.append(Diagnostic("error", "LAYOUT_TOPOLOGY_TYPE", "Topology must be an object", loc))
            continue
        tid = topology.get("id")
        if not isinstance(tid, str) or not ID.match(tid):
            diagnostics.append(Diagnostic("error", "LAYOUT_TOPOLOGY_ID", "Topology id must be lowercase hyphen-case", f"{loc}.id"))
        elif tid in topology_ids:
            diagnostics.append(Diagnostic("error", "LAYOUT_DUP_TOPOLOGY", f"Duplicate topology {tid}", f"{loc}.id"))
        else:
            topology_ids.add(tid)
        for key in ("encodes", "reading_flow", "avoid_when"):
            if not str(topology.get(key, "")).strip():
                diagnostics.append(Diagnostic("error", "LAYOUT_TOPOLOGY_FIELD", f"{key} is required", f"{loc}.{key}"))
        if not nonempty_strings(topology.get("use_for")):
            diagnostics.append(Diagnostic("error", "LAYOUT_TOPOLOGY_USE", "use_for must be a non-empty array", f"{loc}.use_for"))

    layout_ids: set[str] = set()
    for index, layout in enumerate(layouts):
        loc = f"layouts[{index}]"
        if not isinstance(layout, dict):
            diagnostics.append(Diagnostic("error", "LAYOUT_TYPE", "Layout must be an object", loc))
            continue
        lid = layout.get("id")
        if not isinstance(lid, str) or not ID.match(lid):
            diagnostics.append(Diagnostic("error", "LAYOUT_ID", "Layout id must be lowercase hyphen-case", f"{loc}.id"))
        elif lid in layout_ids:
            diagnostics.append(Diagnostic("error", "LAYOUT_DUP_ID", f"Duplicate layout {lid}", f"{loc}.id"))
        else:
            layout_ids.add(lid)
        if layout.get("topology") not in topology_ids:
            diagnostics.append(Diagnostic("error", "LAYOUT_UNKNOWN_TOPOLOGY", f"Unknown topology {layout.get('topology')!r}", f"{loc}.topology"))
        roles = layout.get("roles")
        if not nonempty_strings(roles) or not set(roles).issubset(ROLES):
            diagnostics.append(Diagnostic("error", "LAYOUT_ROLES", f"roles must use {sorted(ROLES)}", f"{loc}.roles"))
        densities = layout.get("density")
        if not nonempty_strings(densities) or not set(densities).issubset(DENSITIES):
            diagnostics.append(Diagnostic("error", "LAYOUT_DENSITY", f"density must use {sorted(DENSITIES)}", f"{loc}.density"))
        tones = layout.get("tones")
        if not nonempty_strings(tones) or not set(tones).issubset(TONES):
            diagnostics.append(Diagnostic("error", "LAYOUT_TONES", f"tones must use {sorted(TONES)}", f"{loc}.tones"))
        for key in ("relationships", "required_slots", "guardrails"):
            if not nonempty_strings(layout.get(key)):
                diagnostics.append(Diagnostic("error", "LAYOUT_LIST", f"{key} must be a non-empty array", f"{loc}.{key}"))
        optional = layout.get("optional_slots")
        if not isinstance(optional, list) or not all(isinstance(item, str) and item.strip() for item in optional):
            diagnostics.append(Diagnostic("error", "LAYOUT_OPTIONAL", "optional_slots must be an array of strings", f"{loc}.optional_slots"))
        for key in ("media_slots", "max_items"):
            number = layout.get(key)
            if not isinstance(number, int) or number < 0:
                diagnostics.append(Diagnostic("error", "LAYOUT_COUNT", f"{key} must be a non-negative integer", f"{loc}.{key}"))
        if not str(layout.get("fidelity", "")).strip():
            diagnostics.append(Diagnostic("error", "LAYOUT_FIDELITY", "fidelity is required", f"{loc}.fidelity"))

    covered_roles = {role for layout in layouts if isinstance(layout, dict) for role in layout.get("roles", [])}
    missing_roles = sorted(ROLES - covered_roles)
    if missing_roles:
        diagnostics.append(Diagnostic("warning", "LAYOUT_ROLE_COVERAGE", "No layout covers roles: " + ", ".join(missing_roles), "layouts"))
    return diagnostics


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--json-output")
    args = parser.parse_args()
    try:
        value = load_json(args.manifest)
    except ValueError as exc:
        return emit_report("layout manifest validation", [Diagnostic("error", "LAYOUT_JSON", str(exc))], json_output=args.json_output)
    return emit_report(
        "layout manifest validation",
        validate(value),
        json_output=args.json_output,
        extra={"file": str(args.manifest.resolve())},
    )


if __name__ == "__main__":
    raise SystemExit(main())
