#!/usr/bin/env python3
"""Validate the qiaomu-bento-ppt package structure and local links."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None


REQUIRED_FILES = [
    "SKILL.md",
    "README.md",
    "LICENSE",
    "NOTICE.md",
    "THIRD_PARTY_LICENSES/bento-MIT.txt",
    "agents/interface.yaml",
    "manifest.json",
    "upstream.lock.json",
    "references/workflow.md",
    "references/upstream-contract.md",
    "references/upstream/bento-official-skill.md",
    "references/upstream/bento-agents.md",
    "references/upstream/bento-format.md",
    "assets/bento/Bento_Slides.bento.html",
    "scripts/bento_deck.py",
    "scripts/export_skill_ir.py",
    "scripts/trigger_eval.py",
    "scripts/sync_upstream.py",
    "evals/trigger_cases.json",
    "evals/fixtures/minimal-deck.json",
    "evals/output/run_fixture.py",
    "evals/upstream/run_fixture.py",
    "examples/build_intro_deck.py",
    "examples/qiaomu-bento-ppt-intro-deck-plan.md",
    "examples/qiaomu-bento-ppt-intro.json",
    "examples/qiaomu-bento-ppt-intro.bento.html",
    "docs/assets/qiaomu-bento-ppt-hero.png",
    "reports/intro-deck-json-validation.json",
    "reports/intro-deck-validation.json",
    "reports/upstream-sync.json",
    "reports/upstream-sync-eval.json",
    "reports/publication.md",
    ".github/workflows/sync-bento-upstream.yml",
]

UPSTREAM_TARGETS = {
    "assets/bento/Bento_Slides.bento.html",
    "references/upstream/bento-agents.md",
    "references/upstream/bento-format.md",
    "references/upstream/bento-official-skill.md",
}


def load_yaml(path: Path) -> dict[str, Any]:
    if yaml is None:
        return {}
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return payload if isinstance(payload, dict) else {}


def frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    lines = text.splitlines()
    try:
        end = lines[1:].index("---") + 1
    except ValueError:
        return {}
    if yaml is not None:
        payload = yaml.safe_load("\n".join(lines[1:end])) or {}
        return payload if isinstance(payload, dict) else {}
    return {}


def validate(root: Path) -> dict[str, Any]:
    root = root.resolve()
    failures: list[str] = []
    warnings: list[str] = []
    for rel in REQUIRED_FILES:
        if not (root / rel).is_file():
            failures.append(f"missing required file: {rel}")
    if (root / "upstream.lock.json").is_file():
        try:
            upstream_lock = json.loads((root / "upstream.lock.json").read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            failures.append(f"upstream.lock.json invalid: {exc}")
            upstream_lock = {}
        if upstream_lock.get("repository") != "nyblnet/bento":
            failures.append("upstream.lock.json repository must be nyblnet/bento")
        release = upstream_lock.get("release", {})
        if not release.get("tag") or not re.fullmatch(r"[0-9a-f]{40}", str(release.get("commit", ""))):
            failures.append("upstream.lock.json release tag/commit is invalid")
        locked_files = upstream_lock.get("files", {})
        if set(locked_files) != UPSTREAM_TARGETS:
            failures.append("upstream.lock.json must lock exactly the four governed snapshots")
        for rel in UPSTREAM_TARGETS:
            path = root / rel
            spec = locked_files.get(rel, {}) if isinstance(locked_files, dict) else {}
            if path.is_file():
                data = path.read_bytes()
                if hashlib.sha256(data).hexdigest() != spec.get("sha256"):
                    failures.append(f"bundled asset checksum mismatch: {rel}")
                if len(data) != spec.get("bytes"):
                    failures.append(f"bundled asset size mismatch: {rel}")

    workflow = root / ".github" / "workflows" / "sync-bento-upstream.yml"
    if workflow.is_file():
        workflow_text = workflow.read_text(encoding="utf-8")
        for token in ("schedule:", "pull-requests: write", "gh pr create", "sync_upstream.py"):
            if token not in workflow_text:
                failures.append(f"upstream workflow missing governed token: {token}")

    if (root / "SKILL.md").is_file():
        meta = frontmatter(root / "SKILL.md")
        if meta.get("name") != "qiaomu-bento-ppt":
            failures.append("SKILL.md frontmatter name must be qiaomu-bento-ppt")
        description = str(meta.get("description", "")).lower()
        for token in ("qiaomu", "bento", "presentation", "workflow", "skill"):
            if token not in description:
                failures.append(f"SKILL.md description missing routing token: {token}")
        skill_text = (root / "SKILL.md").read_text(encoding="utf-8")
        for rel in re.findall(r"\]\(([^)]+\.md)\)", skill_text):
            if not rel.startswith(("http://", "https://")) and not (root / rel).is_file():
                failures.append(f"SKILL.md links to missing file: {rel}")
        skill_text_lower = skill_text.lower()
        for label in (
            "rollback boundary",
            "missing evidence",
            "docid",
            "output contract",
            "standalone",
        ):
            if label not in skill_text_lower:
                failures.append(f"SKILL.md missing governed label: {label}")

    if (root / "agents/interface.yaml").is_file() and yaml is not None:
        interface = load_yaml(root / "agents/interface.yaml")
        fields = interface.get("interface", {})
        for key in ("display_name", "short_description", "default_prompt"):
            if not fields.get(key):
                failures.append(f"agents/interface.yaml missing interface.{key}")
        targets = interface.get("compatibility", {}).get("adapter_targets", [])
        for target in ("openai", "claude", "generic", "agent-skills-compatible"):
            if target not in targets:
                failures.append(f"agents/interface.yaml missing adapter target: {target}")

    if (root / "manifest.json").is_file():
        try:
            manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            failures.append(f"manifest.json invalid: {exc}")
            manifest = {}
        for key in ("name", "version", "owner", "updated_at", "status", "maturity_tier", "release_gates"):
            if not manifest.get(key):
                failures.append(f"manifest.json missing {key}")
        if manifest.get("version") and not re.match(r"^\d+\.\d+\.\d+$", manifest["version"]):
            failures.append("manifest.json version must be semver-like")

    readme = (root / "README.md").read_text(encoding="utf-8") if (root / "README.md").is_file() else ""
    for token in ("npx skills add", "你可以直接这样说", "Troubleshooting", "missing evidence"):
        if token not in readme:
            warnings.append(f"README may be missing: {token}")

    return {"ok": not failures, "root": str(root), "failures": failures, "warnings": warnings}


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate qiaomu-bento-ppt skill package.")
    parser.add_argument("skill_dir", nargs="?", default=".")
    args = parser.parse_args()
    result = validate(Path(args.skill_dir))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not result["ok"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
