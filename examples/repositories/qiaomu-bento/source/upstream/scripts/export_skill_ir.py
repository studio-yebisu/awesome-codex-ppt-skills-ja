#!/usr/bin/env python3
"""Export a compact platform-neutral Skill IR for qiaomu-bento-ppt."""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None


def load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {}


def load_yaml(path: Path) -> dict[str, Any]:
    if yaml is None or not path.is_file():
        return {}
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return payload if isinstance(payload, dict) else {}


def frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not text.startswith("---\n") or yaml is None:
        return {}
    end = lines[1:].index("---") + 1
    payload = yaml.safe_load("\n".join(lines[1:end])) or {}
    return payload if isinstance(payload, dict) else {}


def trigger_samples(root: Path, bucket: str) -> list[str]:
    cases = load_json(root / "evals" / "trigger_cases.json")
    return [
        str(item.get("text", ""))
        for item in cases.get(bucket, [])
        if isinstance(item, dict) and item.get("text")
    ][:8]


def files(root: Path, folder: str) -> list[str]:
    target = root / folder
    return [
        str(path.relative_to(root))
        for path in sorted(target.rglob("*"))
        if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc"
    ] if target.is_dir() else []


def build(root: Path) -> dict[str, Any]:
    manifest = load_json(root / "manifest.json")
    meta = frontmatter(root / "SKILL.md")
    interface = load_yaml(root / "agents" / "interface.yaml")
    compatibility = interface.get("compatibility", {})
    intent = manifest.get("intent", {})
    return {
        "schema_version": "2.0.0-qiaomu-lite",
        "generated_at": date.today().isoformat(),
        "package": {
            "name": meta.get("name"),
            "version": manifest.get("version"),
            "owner": manifest.get("owner"),
            "maturity_tier": manifest.get("maturity_tier"),
            "lifecycle_stage": manifest.get("lifecycle_stage"),
            "upstream_inspiration": manifest.get("upstream_inspiration"),
        },
        "intent": {
            "description": meta.get("description", ""),
            "job_to_be_done": intent.get("job_to_be_done"),
            "target_users": intent.get("target_users", []),
            "inputs": intent.get("inputs", []),
            "outputs": intent.get("outputs", []),
            "exclusions": intent.get("exclusions", []),
        },
        "triggers": {
            "should_trigger": trigger_samples(root, "should_trigger"),
            "should_not_trigger": trigger_samples(root, "should_not_trigger"),
            "near_neighbor": trigger_samples(root, "near_neighbor"),
        },
        "workflow": {
            "proposal_first": True,
            "official_schema_runtime_source": "bundled pinned snapshots",
            "standalone": True,
            "steps": [
                "route and clarify delivery",
                "create source-grounded deck plan",
                "read current official bento guide",
                "extract or author document JSON",
                "map content to native bento capabilities",
                "build into a clean shell",
                "run structure, shell, identity, and browser gates",
            ],
        },
        "output_contract": intent.get("outputs", []),
        "resources": {
            "assets": files(root, "assets"),
            "references": files(root, "references"),
            "scripts": files(root, "scripts"),
            "evals": files(root, "evals"),
            "examples": files(root, "examples"),
            "reports": files(root, "reports"),
            "docs": files(root, "docs"),
            "workflows": files(root, ".github"),
            "third_party_licenses": files(root, "THIRD_PARTY_LICENSES"),
        },
        "portability": {
            "canonical_format": compatibility.get("canonical_format"),
            "adapter_targets": compatibility.get("adapter_targets", []),
            "activation": compatibility.get("activation", {}),
            "execution": compatibility.get("execution", {}),
            "trust": compatibility.get("trust", {}),
            "permissions": compatibility.get("permissions", {}),
            "degradation": compatibility.get("degradation", {}),
        },
        "gates": interface.get("gates", {}),
        "evidence_boundary": {
            "file_backed_fixture": "evals/fixtures/minimal-deck.json",
            "input_files": [
                "source material",
                "optional existing .bento.html",
                "bundled pinned bento shell",
            ],
            "output_contract": ["deck-plan.md", "deck.json", ".bento.html", "validation report"],
            "rollback_boundary": "new output by default; overwrite requires explicit flag",
            "trust_report": "reports/trust.md",
            "output_quality_scorecard": "reports/output_quality_scorecard.md",
            "browser_evidence": "docs/assets/qiaomu-bento-ppt-hero.png",
            "example_deck": "examples/qiaomu-bento-ppt-intro.bento.html",
            "upstream_lock": "upstream.lock.json",
            "upstream_sync_evidence": "reports/upstream-sync-eval.json",
            "missing_evidence": ["cross-platform browser review"],
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Export qiaomu-bento-ppt Skill IR.")
    parser.add_argument("skill_dir", nargs="?", default=".")
    parser.add_argument("--output", "-o")
    args = parser.parse_args()
    root = Path(args.skill_dir).resolve()
    payload = build(root)
    rendered = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.output:
        output = Path(args.output)
        if not output.is_absolute():
            output = root / output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
