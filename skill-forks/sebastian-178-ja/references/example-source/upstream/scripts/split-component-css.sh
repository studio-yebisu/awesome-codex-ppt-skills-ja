#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
skill_root="$(cd "${script_dir}/.." && pwd)"

python3 - "$skill_root" <<'PY'
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
css_path = root / "assets/css/components.css"
manifest_path = root / "assets/css/components/manifest.json"
out_dir = manifest_path.parent

css = css_path.read_text(encoding="utf-8")
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
components = manifest["components"]
families = {name: [] for name in manifest["families"]}

family_patterns = [
    ("process", re.compile(r"^(process|stage|funnel|filter|loop|cycle|cascade|flow|fishbone|screen|triangle|value|vertical|takeaway|deep-dive|chevron|swimlane|customer-journey|journey-loop|input-process|ipo)")),
    ("time", re.compile(r"^(timeline|horizon|journey|phase|meeting-phase|milestone|gantt|stair|calendar|schedule)")),
    ("text", re.compile(r"^(quote|numbered-list|dense-list|contents-card|six-column|conversion|story|step-explanation|icon-outcome|outcome-icon|decision-log|pros-cons|status|agenda|catalog|objective|simple-agenda)")),
    ("data", re.compile(r"^(metric|chart|bar|heatmap|scatter|table|scorecard|sensitivity|portfolio|risk|quadrant|competency|dot|range|pie|donut|stacked|waterfall|axis|plot|part-to-whole|dual-pie|benchmark|line|combo|paired|likert|checkmark|ranked-evidence|driver-recap|matrix|inline-bar|rank-cell)")),
    ("structure", re.compile(r"^(pyramid|cause-effect|outcome|support-stack|diverging|from-to|compass|framework|raci|concept-box|concept-connector|transition-marker|issue-tree|tree|iceberg|capability|coverage)")),
    ("people", re.compile(r"^(profile|contact|avatar|headshot|team-wall|bio-card)")),
    ("shared", re.compile(r"^(callout|card|concept-label|layout-note|viz-)")),
]

def split_blocks(text):
    blocks = []
    i = 0
    n = len(text)
    while i < n:
        while i < n and text[i].isspace():
            i += 1
        if i >= n:
            break
        start = i
        depth = 0
        in_string = None
        escaped = False
        while i < n:
            char = text[i]
            if in_string:
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == in_string:
                    in_string = None
            else:
                if char in ("'", '"'):
                    in_string = char
                elif char == "{":
                    depth += 1
                elif char == "}":
                    depth -= 1
                    if depth == 0:
                        i += 1
                        blocks.append(text[start:i].strip())
                        break
            i += 1
        else:
            tail = text[start:].strip()
            if tail:
                blocks.append(tail)
            break
    return blocks

def selector_classes(block):
    prelude = block.split("{", 1)[0]
    return set(re.findall(r"\.([_a-zA-Z][-_a-zA-Z0-9]*)", prelude))

def class_family(name):
    if name in components:
        return components[name]
    for family, pattern in family_patterns:
        if pattern.search(name):
            return family
    return None

for block in split_blocks(css):
    assigned = {class_family(name) for name in selector_classes(block)}
    assigned.discard(None)
    if not assigned:
        assigned = {"shared"}
    if "shared" in assigned and len(assigned) > 1:
        assigned.discard("shared")
    for family in sorted(assigned):
        families[family].append(block)

for family, blocks in families.items():
    header = f"/* Component family: {family}. Generated from assets/css/components.css for package-time CSS splitting. */\n"
    body = "\n\n".join(blocks).strip()
    (out_dir / f"{family}.css").write_text(header + (body + "\n" if body else ""), encoding="utf-8")

print(f"Wrote {len(families)} component CSS family files to {out_dir}")
PY
