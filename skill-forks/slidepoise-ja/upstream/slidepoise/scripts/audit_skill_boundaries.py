#!/usr/bin/env python3
"""Collect objective stable-skill boundary facts without claiming quality."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    required = [
        "SKILL.md",
        "agents/openai.yaml",
        "references/workflow.md",
        "references/visual-reasoning.md",
        "references/reconstruction.md",
        "scripts/resolve_config.py",
        "scripts/prepare_generation.py",
        "scripts/collect_semantic_evidence.py",
        "scripts/slidepoise_runtime.py",
        "scripts/collect_release_evidence.py"
    ]
    errors = [{"file": relative, "reason": "required stable skill file missing"} for relative in required if not (ROOT / relative).is_file()]
    for forbidden in (ROOT / "config", ROOT / "assets" / "icons", ROOT / "assets" / "visual_references", ROOT / "assets" / "components"):
        if forbidden.exists():
            errors.append({"file": str(forbidden.relative_to(ROOT)), "reason": "configurable profile state must remain outside the skill"})
    caches = [str(path.relative_to(ROOT)) for path in ROOT.rglob("__pycache__")]
    if caches:
        errors.append({"reason": "Python cache directories must be removed before release", "paths": caches})
    report = {
        "evidence_type": "objective_framework_boundary_facts",
        "blocking_facts": errors,
        "agent_interpretation_required": True,
        "notice": "No overall verdict is produced. The host Agent interprets these boundary facts during maintenance review."
    }
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if not errors else 2)


if __name__ == "__main__":
    main()
