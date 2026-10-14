from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
READMES = (ROOT / "README.md", ROOT / "README.en.md")


def _read(path: Path) -> str:
    assert path.is_file(), f"missing documentation: {path.relative_to(ROOT)}"
    return path.read_text(encoding="utf-8")


def _image_targets(markdown: str) -> list[str]:
    markdown_targets = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", markdown)
    html_targets = re.findall(r"<img\b[^>]*\bsrc=[\"']([^\"']+)[\"']", markdown)
    return [
        target
        for target in (*markdown_targets, *html_targets)
        if target.startswith("examples/showcase/")
    ]


def test_readmes_are_bilingual_and_show_the_real_showcase() -> None:
    zh = _read(READMES[0])
    en = _read(READMES[1])

    assert re.search(r"[\u4e00-\u9fff]", zh[:1200])
    assert "English" in zh[:1200]
    assert "简体中文" in en[:1200]
    for path, text in zip(READMES, (zh, en), strict=True):
        assert text.startswith("# Paper2PPT")
        assert "Paper2PPT" in text[:80]
        assert "examples/showcase/overview.png" in text[:1800]
        assert "presentation_zh.pptx" in text
        targets = _image_targets(text)
        assert targets, f"{path.name} has no showcase image"
        for target in targets:
            assert not target.startswith(("http://", "https://"))
            assert (ROOT / target).is_file(), f"broken image in {path.name}: {target}"


def test_chinese_readme_first_viewport_has_positioning_badges_quickstart_and_montage() -> None:
    first_viewport = _read(ROOT / "README.md")[:1800]

    assert "可编辑" in first_viewport and "可溯源" in first_viewport
    assert "img.shields.io" in first_viewport
    assert "快速开始" in first_viewport
    assert "git clone https://github.com/wp-a/paper2ppt.git" in first_viewport
    assert "examples/showcase/overview.png" in first_viewport


def test_readmes_cover_installation_inputs_outputs_workflow_and_limits() -> None:
    required_concepts = (
        "Codex",
        "Claude Code",
        "Agent Skills",
        "Skill",
        "plugin",
        "PDF",
        "DOI",
        "PMID",
        "arXiv",
        "presentation_zh.pptx",
        "qa_report.md",
        "asset_manifest.md",
        "assets/",
        "content QA",
        "structural QA",
        "visual QA",
        "OCR",
    )
    limitation_terms = (
        ("隐私", "privacy"),
        ("付费墙", "paywall"),
        ("渲染器", "renderer"),
        ("部分来源", "partial source"),
    )

    for path in READMES:
        text = _read(path)
        for concept in required_concepts:
            assert concept.lower() in text.lower(), f"{path.name}: {concept}"
        for alternatives in limitation_terms:
            assert any(term.lower() in text.lower() for term in alternatives), (
                f"{path.name}: {alternatives}"
            )
        assert "~/.agents/skills/paper2ppt" in text
        assert "~/.claude/skills/paper2ppt" in text


def test_readmes_make_a_factual_three_way_comparison() -> None:
    comparison_groups = (
        ("outline-only", "只生成大纲"),
        ("Beamer",),
        ("API key", "API 密钥"),
    )

    for path in READMES:
        text = _read(path)
        for alternatives in comparison_groups:
            assert any(term.lower() in text.lower() for term in alternatives), (
                f"{path.name}: {alternatives}"
            )
        assert "editable" in text.lower() or "可编辑" in text
        assert "speaker notes" in text.lower() or "讲稿" in text


def test_documentation_uses_only_the_paper2ppt_identity() -> None:
    controlled = [*READMES, ROOT / "CHANGELOG.md", ROOT / "docs/installation.md"]
    forbidden = (
        "nature-paper2ppt",
        "nature 风格",
        "nature-style",
        "nature branded",
    )

    for path in controlled:
        text = _read(path).lower()
        assert all(term not in text for term in forbidden), path.name


def test_installation_guide_distinguishes_direct_skills_and_plugins() -> None:
    text = _read(ROOT / "docs/installation.md")

    assert "直接 Skill" in text
    assert "插件" in text
    assert "~/.agents/skills/paper2ppt" in text
    assert "~/.claude/skills/paper2ppt" in text
    assert "codex plugin add paper2ppt@personal" in text
    assert "claude plugin marketplace add wp-a/paper2ppt" in text
    assert "claude plugin install paper2ppt@paper2ppt" in text
    assert "claude --plugin-dir ./plugins/paper2ppt" in text
    assert "/paper2ppt:paper2ppt" in text
    assert "$paper2ppt" in text
    assert "卸载" in text and "迁移" in text
    assert "Codex" in text and "Claude Code" in text and "Agent Skills" in text


def test_changelog_and_maintenance_cover_the_release_lifecycle() -> None:
    changelog = _read(ROOT / "CHANGELOG.md")
    maintenance = _read(ROOT / "docs/maintenance.md")

    assert re.search(r"(?m)^## \[?0\.1\.0\]?", changelog)
    assert "Paper2PPT" in changelog
    assert "更名" in changelog or "rename" in changelog.lower()
    for command in (
        "python scripts/sync_plugin.py --check",
        "python scripts/validate_repo.py",
        "python -m pytest -q",
        "python scripts/inspect_pptx.py",
    ):
        assert command in maintenance
    for concept in ("示例", "VERSION", "CHANGELOG.md", "release", "tag"):
        assert concept.lower() in maintenance.lower()
