from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".md", ".txt", ".yaml", ".yml", ".py", ".json", ".svg"}


def published_text_files():
    # Inspect the distributed skill, not local ignored task outputs or old installers.
    manifest = yaml.safe_load((ROOT / "manifest.yaml").read_text(encoding="utf-8"))
    return [ROOT / name for name in manifest["files"] if Path(name).suffix.lower() in TEXT_SUFFIXES]


def test_no_legacy_repository_url_remains() -> None:
    legacy = "github.com/helloo1568/" + "image-ppt"
    hits: list[str] = []

    for path in published_text_files():
        text = path.read_text(encoding="utf-8")
        if legacy in text:
            hits.append(str(path.relative_to(ROOT)))

    assert not hits, f"Legacy repository URL remains in: {hits}"


def test_slidemuse_identity_is_consistent() -> None:
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    manifest = (ROOT / "manifest.yaml").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    assert "name: slidemuse" in skill
    assert "name: slidemuse" in manifest
    assert "display_name: SlideMuse" in manifest
    assert "github.com/helloo1568/slidemuse" in readme
    assert "$slidemuse" in readme


def test_legacy_project_name_only_exists_in_compatibility_history() -> None:
    legacy_name = "image" + "-ppt"
    allowed = {"CHANGELOG.md", "install.py", "tests/test_branding.py"}
    hits: list[str] = []

    for path in published_text_files():
        rel = path.relative_to(ROOT).as_posix()
        if rel in allowed:
            continue
        text = path.read_text(encoding="utf-8")
        if legacy_name in text:
            hits.append(rel)

    assert not hits, f"Legacy project name remains outside compatibility/history: {hits}"
