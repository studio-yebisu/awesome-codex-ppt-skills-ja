import importlib.util
import json
from pathlib import Path
import shutil

import pytest
import yaml


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_repo.py"


@pytest.fixture(scope="module")
def validator():
    assert VALIDATOR.is_file(), "scripts/validate_repo.py must exist"
    spec = importlib.util.spec_from_file_location("validate_repo", VALIDATOR)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def valid_repo(tmp_path: Path) -> Path:
    destination = tmp_path / "repo"
    ignored = shutil.ignore_patterns(
        ".git", ".venv", ".pytest_cache", "__pycache__", "docs", "examples", "output"
    )
    shutil.copytree(ROOT, destination, ignore=ignored)
    return destination


def codes(findings: list[dict[str, str]]) -> set[str]:
    return {finding["code"] for finding in findings}


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def test_current_repository_passes_validation(validator) -> None:
    assert validator.validate_repository(ROOT) == []


@pytest.mark.parametrize(
    ("replacement", "expected_code"),
    (
        ("not frontmatter\n", "skill.frontmatter"),
        (
            "---\nname: wrong-name\ndescription: Use when a paper must become a PPT. Not for business slides.\n---\n\n# Wrong\n",
            "skill.name",
        ),
        (
            "---\nname: paper2ppt\ndescription: Builds decks with a six-step workflow.\nextra: forbidden\n---\n\n# Paper2PPT\n",
            "skill.frontmatter-fields",
        ),
        (
            "---\nname: paper2ppt\ndescription: Builds paper decks and checks them.\n---\n\n# Paper2PPT\n",
            "skill.description",
        ),
        (
            "---\nname: paper2ppt\ndescription: Use when a paper needs a PPT; first extract evidence, then build and validate slides. Not for business slides.\n---\n\n# Paper2PPT\n",
            "skill.description",
        ),
        (
            "---\nname: paper2ppt\ndescription: Use when a paper needs a PPT. Not for business slides. Paper2PPT builds the deck and validates it.\n---\n\n# Paper2PPT\n",
            "skill.description",
        ),
    ),
)
def test_skill_frontmatter_failures_are_specific(
    valid_repo: Path, validator, replacement: str, expected_code: str
) -> None:
    (valid_repo / "SKILL.md").write_text(replacement, encoding="utf-8")

    assert expected_code in codes(validator.validate_repository(valid_repo))


def test_missing_relative_markdown_reference_is_detected(
    valid_repo: Path, validator
) -> None:
    skill = valid_repo / "SKILL.md"
    skill.write_text(
        skill.read_text(encoding="utf-8")
        + "\nRead [missing guidance](references/missing.md).\n",
        encoding="utf-8",
    )

    findings = validator.validate_repository(valid_repo)

    assert "markdown.missing-reference" in codes(findings)
    assert any("references/missing.md" in finding["message"] for finding in findings)


@pytest.mark.parametrize(
    ("relative", "expected_code"),
    (
        ("plugins/paper2ppt/skills/paper2ppt/SKILL.md", "mirror.drift"),
        ("plugins/paper2ppt/skills/paper2ppt/references/workflow.md", "mirror.drift"),
        ("plugins/paper2ppt/skills/paper2ppt/scripts/preflight.py", "mirror.drift"),
    ),
)
def test_canonical_plugin_drift_is_detected(
    valid_repo: Path, validator, relative: str, expected_code: str
) -> None:
    path = valid_repo / relative
    path.write_text(path.read_text(encoding="utf-8") + "\nDRIFT\n", encoding="utf-8")

    assert expected_code in codes(validator.validate_repository(valid_repo))


def test_manifest_marketplace_and_version_drift_are_detected(
    valid_repo: Path, validator
) -> None:
    codex_manifest = valid_repo / "plugins/paper2ppt/.codex-plugin/plugin.json"
    data = json.loads(codex_manifest.read_text(encoding="utf-8"))
    data["version"] = "9.9.9"
    codex_manifest.write_text(json.dumps(data), encoding="utf-8")

    marketplace = valid_repo / ".claude-plugin/marketplace.json"
    data = json.loads(marketplace.read_text(encoding="utf-8"))
    data["plugins"][0]["source"] = "./plugins/wrong"
    marketplace.write_text(json.dumps(data), encoding="utf-8")

    found = codes(validator.validate_repository(valid_repo))
    assert "release.version-drift" in found
    assert "marketplace.source" in found


@pytest.mark.parametrize(
    ("relative", "field", "value", "expected_code"),
    (
        (
            "plugins/paper2ppt/.codex-plugin/plugin.json",
            "skills",
            "./wrong/",
            "plugin.skills",
        ),
        (
            "plugins/paper2ppt/.claude-plugin/plugin.json",
            "skills",
            ["./skills/wrong"],
            "plugin.skills",
        ),
        (
            "plugins/paper2ppt/.codex-plugin/plugin.json",
            "homepage",
            "https://example.com/wrong",
            "plugin.url",
        ),
        (
            "plugins/paper2ppt/.claude-plugin/plugin.json",
            "repository",
            "https://example.com/wrong",
            "plugin.url",
        ),
        (
            "plugins/paper2ppt/.claude-plugin/plugin.json",
            "$schema",
            "https://example.com/schema.json",
            "plugin.schema",
        ),
    ),
)
def test_plugin_manifest_semantic_contract_is_validated(
    valid_repo: Path,
    validator,
    relative: str,
    field: str,
    value,
    expected_code: str,
) -> None:
    path = valid_repo / relative
    data = read_json(path)
    data[field] = value
    write_json(path, data)

    assert expected_code in codes(validator.validate_repository(valid_repo))


@pytest.mark.parametrize(
    ("relative", "mutation", "expected_code"),
    (
        ("plugins/paper2ppt/.codex-plugin/plugin.json", "description", "plugin.description"),
        ("plugins/paper2ppt/.codex-plugin/plugin.json", "author", "plugin.author"),
        ("plugins/paper2ppt/.codex-plugin/plugin.json", "author-name", "plugin.author"),
        ("plugins/paper2ppt/.claude-plugin/plugin.json", "description", "plugin.description"),
        ("plugins/paper2ppt/.claude-plugin/plugin.json", "author", "plugin.author"),
        ("plugins/paper2ppt/.claude-plugin/plugin.json", "author-name", "plugin.author"),
    ),
)
def test_plugin_manifests_require_description_and_author_name(
    valid_repo: Path, validator, relative: str, mutation: str, expected_code: str
) -> None:
    path = valid_repo / relative
    data = read_json(path)
    if mutation == "author-name":
        data["author"].pop("name")
    else:
        data.pop(mutation)
    write_json(path, data)

    assert expected_code in codes(validator.validate_repository(valid_repo))


@pytest.mark.parametrize(
    ("relative", "root_value"),
    (
        ("plugins/paper2ppt/.codex-plugin/plugin.json", []),
        ("plugins/paper2ppt/.codex-plugin/plugin.json", "paper2ppt"),
        ("plugins/paper2ppt/.codex-plugin/plugin.json", None),
        ("plugins/paper2ppt/.claude-plugin/plugin.json", []),
        ("plugins/paper2ppt/.claude-plugin/plugin.json", "paper2ppt"),
        ("plugins/paper2ppt/.claude-plugin/plugin.json", None),
    ),
)
def test_plugin_manifest_root_must_be_a_json_object(
    valid_repo: Path, validator, relative: str, root_value
) -> None:
    path = valid_repo / relative
    path.write_text(json.dumps(root_value), encoding="utf-8")

    findings = validator.validate_repository(valid_repo)

    assert "plugin.manifest" in codes(findings)
    matching = [finding for finding in findings if finding["code"] == "plugin.manifest"]
    assert len(matching) == 1
    assert matching[0]["path"] == relative


@pytest.mark.parametrize("mode", ("malformed", "missing"))
def test_plugin_manifest_parse_failures_are_not_duplicated(
    valid_repo: Path, validator, mode: str
) -> None:
    path = valid_repo / "plugins/paper2ppt/.codex-plugin/plugin.json"
    if mode == "malformed":
        path.write_text("{", encoding="utf-8")
        expected_code = "json.malformed"
    else:
        path.unlink()
        expected_code = "file.unreadable"

    findings = validator.validate_repository(valid_repo)

    assert sum(finding["code"] == expected_code for finding in findings) == 1
    assert "plugin.manifest" not in codes(findings)


@pytest.mark.parametrize(
    ("relative", "forbidden_key"),
    (
        ("plugins/paper2ppt/.codex-plugin/plugin.json", "agents"),
        ("plugins/paper2ppt/.codex-plugin/plugin.json", "apps"),
        ("plugins/paper2ppt/.claude-plugin/plugin.json", "hooks"),
        ("plugins/paper2ppt/.claude-plugin/plugin.json", "mcpServers"),
        ("plugins/paper2ppt/.claude-plugin/plugin.json", "settings"),
    ),
)
def test_plugin_manifests_reject_unused_components(
    valid_repo: Path, validator, relative: str, forbidden_key: str
) -> None:
    path = valid_repo / relative
    data = read_json(path)
    data[forbidden_key] = []
    write_json(path, data)

    assert "plugin.components" in codes(validator.validate_repository(valid_repo))


@pytest.mark.parametrize(
    ("mutation", "expected_code"),
    (
        ("codex-policy", "marketplace.policy"),
        ("codex-source", "marketplace.source"),
        ("codex-category", "marketplace.category"),
        ("claude-schema", "marketplace.schema"),
        ("claude-source", "marketplace.source"),
        ("claude-version", "release.version-drift"),
    ),
)
def test_marketplace_semantic_contract_is_validated(
    valid_repo: Path, validator, mutation: str, expected_code: str
) -> None:
    if mutation.startswith("codex-"):
        path = valid_repo / ".agents/plugins/marketplace.json"
        data = read_json(path)
        entry = data["plugins"][0]
        if mutation == "codex-policy":
            entry["policy"] = {"installation": "REQUIRED", "authentication": "NONE"}
        elif mutation == "codex-source":
            entry["source"] = {"source": "local", "path": "./plugins/wrong"}
        else:
            entry["category"] = "Productivity"
    else:
        path = valid_repo / ".claude-plugin/marketplace.json"
        data = read_json(path)
        entry = data["plugins"][0]
        if mutation == "claude-schema":
            data["$schema"] = "https://example.com/marketplace.schema.json"
        elif mutation == "claude-source":
            entry["source"] = "./plugins/wrong"
        else:
            entry["version"] = "9.9.9"
    write_json(path, data)

    assert expected_code in codes(validator.validate_repository(valid_repo))


@pytest.mark.parametrize(
    ("field", "value", "expected_code"),
    (
        ("displayName", "Wrong Product", "plugin.interface-display"),
        ("shortDescription", "", "plugin.interface-short-description"),
        ("defaultPrompt", [], "plugin.interface-default-prompt"),
        (
            "defaultPrompt",
            ["Create slides without naming the product."],
            "plugin.interface-default-prompt",
        ),
    ),
)
def test_codex_plugin_interface_contract_is_validated(
    valid_repo: Path, validator, field: str, value, expected_code: str
) -> None:
    path = valid_repo / "plugins/paper2ppt/.codex-plugin/plugin.json"
    data = read_json(path)
    data["interface"][field] = value
    write_json(path, data)

    assert expected_code in codes(validator.validate_repository(valid_repo))


@pytest.mark.parametrize(
    ("field", "value", "expected_code"),
    (
        ("displayName", None, "plugin.interface-display"),
        ("shortDescription", "x" * 65, "plugin.interface-short-description"),
        ("longDescription", "", "plugin.interface-long-description"),
        ("developerName", None, "plugin.interface-developer"),
        ("category", "", "plugin.interface-category"),
        ("capabilities", [], "plugin.interface-capabilities"),
        ("capabilities", ["Presentation", ""], "plugin.interface-capabilities"),
        ("websiteURL", "https://example.com/wrong", "plugin.interface-website"),
        ("defaultPrompt", ["Paper2PPT 中文提示"] * 4, "plugin.interface-default-prompt"),
        ("defaultPrompt", ["Paper2PPT " + "中" * 129], "plugin.interface-default-prompt"),
    ),
)
def test_codex_plugin_interface_requires_fields_types_and_limits(
    valid_repo: Path, validator, field: str, value, expected_code: str
) -> None:
    path = valid_repo / "plugins/paper2ppt/.codex-plugin/plugin.json"
    data = read_json(path)
    data["interface"][field] = value
    write_json(path, data)

    assert expected_code in codes(validator.validate_repository(valid_repo))


@pytest.mark.parametrize(
    ("field", "expected_code"),
    (
        ("displayName", "plugin.interface-display"),
        ("shortDescription", "plugin.interface-short-description"),
        ("longDescription", "plugin.interface-long-description"),
        ("developerName", "plugin.interface-developer"),
        ("category", "plugin.interface-category"),
        ("capabilities", "plugin.interface-capabilities"),
        ("websiteURL", "plugin.interface-website"),
        ("defaultPrompt", "plugin.interface-default-prompt"),
    ),
)
def test_codex_plugin_interface_rejects_missing_required_fields(
    valid_repo: Path, validator, field: str, expected_code: str
) -> None:
    path = valid_repo / "plugins/paper2ppt/.codex-plugin/plugin.json"
    data = read_json(path)
    data["interface"].pop(field)
    write_json(path, data)

    assert expected_code in codes(validator.validate_repository(valid_repo))


@pytest.mark.parametrize(
    ("mutation", "expected_code"),
    (
        ("malformed", "codex-ui.yaml"),
        ("display-name", "codex-ui.display-name"),
        ("short-description", "codex-ui.short-description"),
        ("english-prompt", "codex-ui.default-prompt"),
        ("token-chinese-prompt", "codex-ui.default-prompt"),
        ("missing-skill-token", "codex-ui.default-prompt"),
        ("implicit-policy", "codex-ui.policy"),
        ("dependencies", "codex-ui.dependencies"),
    ),
)
def test_codex_ui_metadata_contract_is_validated(
    valid_repo: Path, validator, mutation: str, expected_code: str
) -> None:
    path = (
        valid_repo
        / "plugins/paper2ppt/skills/paper2ppt/agents/openai.yaml"
    )
    if mutation == "malformed":
        path.write_text("interface: [unterminated\n", encoding="utf-8")
    else:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if mutation == "display-name":
            data["interface"]["display_name"] = "Wrong Product"
        elif mutation == "short-description":
            data["interface"]["short_description"] = "太短"
        elif mutation == "english-prompt":
            data["interface"]["default_prompt"] = (
                "Use $paper2ppt to create an editable academic presentation."
            )
        elif mutation == "missing-skill-token":
            data["interface"]["default_prompt"] = "把这篇论文制作成中文学术汇报 PPTX。"
        elif mutation == "token-chinese-prompt":
            data["interface"]["default_prompt"] = (
                "请 use $paper2ppt to create an editable academic presentation."
            )
        elif mutation == "implicit-policy":
            data["policy"]["allow_implicit_invocation"] = False
        else:
            data["dependencies"] = {"tools": []}
        path.write_text(
            yaml.safe_dump(data, allow_unicode=True, sort_keys=False),
            encoding="utf-8",
        )

    assert expected_code in codes(validator.validate_repository(valid_repo))


def _replace_with_external_symlink(valid_repo: Path, relative: str) -> Path:
    controlled = valid_repo / relative
    external = valid_repo.parent / ("external-" + relative.replace("/", "-"))
    if controlled.is_dir():
        shutil.copytree(controlled, external)
        shutil.rmtree(controlled)
        controlled.symlink_to(external, target_is_directory=True)
    else:
        shutil.copy2(controlled, external)
        controlled.unlink()
        controlled.symlink_to(external)
    return external


def test_controlled_skill_symlinks_are_rejected_before_external_read(
    valid_repo: Path, validator
) -> None:
    external = valid_repo.parent / "external-skill.md"
    external.write_text(
        "---\nname: paper2ppt\ndescription: Use when external. Not for anything.\n---\n",
        encoding="utf-8",
    )
    relatives = (
        "SKILL.md",
        "plugins/paper2ppt/skills/paper2ppt/SKILL.md",
    )
    for relative in relatives:
        path = valid_repo / relative
        path.unlink()
        path.symlink_to(external)

    findings = validator.validate_repository(valid_repo)

    assert {finding["code"] for finding in findings} == {"path.unsafe"}
    assert {finding["path"] for finding in findings} == set(relatives)
    assert all(str(valid_repo.parent) not in finding["message"] for finding in findings)


@pytest.mark.parametrize(
    "relative",
    (
        "README.md",
        "references",
        ".agents/plugins/marketplace.json",
        ".claude-plugin/marketplace.json",
        "plugins/paper2ppt/.codex-plugin/plugin.json",
        "plugins/paper2ppt/.claude-plugin/plugin.json",
        "plugins/paper2ppt/skills/paper2ppt/references",
        "plugins/paper2ppt/skills/paper2ppt/scripts",
        "plugins/paper2ppt/skills/paper2ppt/agents/openai.yaml",
        "VERSION",
        "tests/trigger_cases.json",
    ),
)
def test_controlled_symlinked_files_and_directories_are_rejected(
    valid_repo: Path, validator, relative: str
) -> None:
    _replace_with_external_symlink(valid_repo, relative)

    findings = validator.validate_repository(valid_repo)

    assert {finding["code"] for finding in findings} == {"path.unsafe"}
    assert relative in {finding["path"] for finding in findings}


def test_controlled_symlink_component_is_rejected(
    valid_repo: Path, validator
) -> None:
    _replace_with_external_symlink(valid_repo, "plugins")

    findings = validator.validate_repository(valid_repo)

    assert {finding["code"] for finding in findings} == {"path.unsafe"}
    assert {finding["path"] for finding in findings} == {"plugins"}


@pytest.mark.parametrize(
    ("filename", "link"),
    (
        ("topic(v1).md", "[topic](references/topic(v1).md)"),
        ("topic one.md", '[topic](<references/topic one.md> "title")'),
        ("topic one.md", "[topic](references/topic%20one.md?download=1#part)"),
        ("topic(escaped).md", r"[topic](references/topic\(escaped\).md)"),
    ),
)
def test_markdown_scanner_resolves_complex_local_destinations(
    valid_repo: Path, validator, filename: str, link: str
) -> None:
    canonical = valid_repo / "references" / filename
    packaged = (
        valid_repo / "plugins/paper2ppt/skills/paper2ppt/references" / filename
    )
    canonical.write_text("# Topic\n", encoding="utf-8")
    packaged.write_text("# Topic\n", encoding="utf-8")
    for relative in ("SKILL.md", "plugins/paper2ppt/skills/paper2ppt/SKILL.md"):
        path = valid_repo / relative
        path.write_text(path.read_text(encoding="utf-8") + f"\n{link}\n", encoding="utf-8")

    findings = validator.validate_repository(valid_repo)

    assert "markdown.missing-reference" not in codes(findings)


def test_markdown_scanner_reports_full_missing_balanced_destination(
    valid_repo: Path, validator
) -> None:
    link = "[missing](references/missing(v1).md)"
    for relative in ("SKILL.md", "plugins/paper2ppt/skills/paper2ppt/SKILL.md"):
        path = valid_repo / relative
        path.write_text(path.read_text(encoding="utf-8") + f"\n{link}\n", encoding="utf-8")

    findings = validator.validate_repository(valid_repo)

    matches = [
        finding
        for finding in findings
        if finding["code"] == "markdown.missing-reference"
    ]
    assert matches
    assert all("references/missing(v1).md" in finding["message"] for finding in matches)


@pytest.mark.parametrize(
    "snippet",
    (
        "```markdown\n[example](references/not-real.md)\n```",
        "~~~md\n[example](references/not-real.md)\n~~~",
        "Inline example: `[example](references/not-real.md)`.",
        "Inline example: ``[example](references/not-real.md)``.",
    ),
)
def test_markdown_links_inside_code_are_ignored(
    valid_repo: Path, validator, snippet: str
) -> None:
    readme = valid_repo / "README.md"
    readme.write_text(
        readme.read_text(encoding="utf-8") + f"\n{snippet}\n",
        encoding="utf-8",
    )

    assert "markdown.missing-reference" not in codes(
        validator.validate_repository(valid_repo)
    )


def test_markdown_link_outside_code_is_still_validated(
    valid_repo: Path, validator
) -> None:
    readme = valid_repo / "README.md"
    readme.write_text(
        readme.read_text(encoding="utf-8")
        + "\n`[ignored](references/code-only.md)`\n"
        + "[real](references/not-real.md)\n",
        encoding="utf-8",
    )

    findings = validator.validate_repository(valid_repo)

    missing = [
        finding
        for finding in findings
        if finding["code"] == "markdown.missing-reference"
    ]
    assert len(missing) == 1
    assert "references/not-real.md" in missing[0]["message"]


@pytest.mark.parametrize(
    ("relative", "cascade_codes"),
    (
        (
            ".agents/plugins/marketplace.json",
            {"marketplace.entry", "marketplace.source", "marketplace.policy"},
        ),
        (
            ".claude-plugin/marketplace.json",
            {"marketplace.entry", "marketplace.schema", "marketplace.source"},
        ),
        (
            "plugins/paper2ppt/.codex-plugin/plugin.json",
            {"plugin.manifest", "plugin.description", "plugin.interface"},
        ),
        (
            "plugins/paper2ppt/.claude-plugin/plugin.json",
            {"plugin.manifest", "plugin.schema", "plugin.description"},
        ),
    ),
)
def test_malformed_json_diagnostics_are_relative_and_do_not_cascade(
    valid_repo: Path, validator, relative: str, cascade_codes: set[str]
) -> None:
    (valid_repo / relative).write_text("{", encoding="utf-8")

    findings = validator.validate_repository(valid_repo)

    malformed = [finding for finding in findings if finding["code"] == "json.malformed"]
    assert len(malformed) == 1
    assert malformed[0]["path"] == relative
    assert not (cascade_codes & codes(findings))
    serialized = json.dumps(findings, ensure_ascii=False)
    assert str(valid_repo) not in serialized


def test_malformed_yaml_diagnostic_is_relative_and_does_not_cascade(
    valid_repo: Path, validator
) -> None:
    relative = "plugins/paper2ppt/skills/paper2ppt/agents/openai.yaml"
    (valid_repo / relative).write_text("interface: [unterminated\n", encoding="utf-8")

    findings = validator.validate_repository(valid_repo)

    assert [finding["code"] for finding in findings] == ["codex-ui.yaml"]
    assert findings[0]["path"] == relative
    assert str(valid_repo) not in json.dumps(findings, ensure_ascii=False)


def test_missing_version_diagnostic_is_relative_and_does_not_cascade(
    valid_repo: Path, validator
) -> None:
    (valid_repo / "VERSION").unlink()

    findings = validator.validate_repository(valid_repo)

    assert [finding["code"] for finding in findings] == ["file.unreadable"]
    assert findings[0]["path"] == "VERSION"
    assert str(valid_repo) not in json.dumps(findings, ensure_ascii=False)


@pytest.mark.parametrize(
    ("relative", "text"),
    (
        ("README.md", "Install nature-paper2ppt here."),
        ("references/workflow.md", "Use a default Nature-style narrative."),
        ("README.md", "默认使用 Nature 风格制作所有幻灯片。"),
        ("README.md", "Use a default Nature–style visual system."),
        ("README.md", "Use a default Nature—style visual system."),
        (
            "plugins/paper2ppt/skills/paper2ppt/agents/openai.yaml",
            'interface:\n  display_name: "nature-paper2ppt"\n',
        ),
    ),
)
def test_legacy_identity_is_rejected_on_controlled_active_surfaces(
    valid_repo: Path, validator, relative: str, text: str
) -> None:
    (valid_repo / relative).write_text(text, encoding="utf-8")

    assert "identity.legacy" in codes(validator.validate_repository(valid_repo))


def test_generic_nature_journal_discussion_is_not_a_branding_failure(
    valid_repo: Path, validator
) -> None:
    readme = valid_repo / "README.md"
    readme.write_text(
        readme.read_text(encoding="utf-8")
        + "\nThis workflow can present a paper published in Nature.\n",
        encoding="utf-8",
    )

    assert "identity.legacy" not in codes(validator.validate_repository(valid_repo))


def test_generic_nature_citation_mention_is_not_a_branding_failure(
    valid_repo: Path, validator
) -> None:
    readme = valid_repo / "README.md"
    readme.write_text(
        readme.read_text(encoding="utf-8")
        + "\nReferences may follow the Nature citation format when requested.\n",
        encoding="utf-8",
    )

    assert "identity.legacy" not in codes(validator.validate_repository(valid_repo))


@pytest.mark.parametrize(
    "text",
    (
        "References use Nature-style citations when the journal requires them.",
        "References use Nature–style references when requested.",
        "The bibliography follows Nature—style bibliography conventions.",
        "参考文献可按 Nature 风格引用格式输出。",
        "按期刊要求使用 Nature 风格参考文献。",
    ),
)
def test_nature_citation_and_bibliography_contexts_are_allowed(
    valid_repo: Path, validator, text: str
) -> None:
    readme = valid_repo / "README.md"
    readme.write_text(text, encoding="utf-8")

    assert "identity.legacy" not in codes(validator.validate_repository(valid_repo))


@pytest.mark.parametrize(
    "text",
    (
        "The presentation uses Nature-style citations when the journal requires them.",
        "This deck includes Nature-style references on its final slide.",
        "The final slide lists Nature—style bibliography entries.",
        "本演示文稿按期刊要求使用 Nature 风格引用。",
        "最后一张幻灯片列出 Nature 风格参考文献。",
    ),
)
def test_citation_context_ignores_subjects_and_locations(
    valid_repo: Path, validator, text: str
) -> None:
    (valid_repo / "README.md").write_text(text, encoding="utf-8")

    assert "identity.legacy" not in codes(validator.validate_repository(valid_repo))


@pytest.mark.parametrize(
    "text",
    (
        "Use Nature-style slides by default.",
        "Use Nature–style design for every deck.",
        "Apply a Nature—style layout to the presentation.",
        "Use a default Nature-style narrative.",
        "默认采用 Nature 风格排版。",
        "Install nature-paper2ppt here.",
    ),
)
def test_nature_visual_branding_contexts_remain_rejected(
    valid_repo: Path, validator, text: str
) -> None:
    (valid_repo / "README.md").write_text(text, encoding="utf-8")

    assert "identity.legacy" in codes(validator.validate_repository(valid_repo))


@pytest.mark.parametrize(
    "text",
    (
        "Use Nature-style citations and slide design by default.",
        "Nature–style references should define the deck layout.",
        "Use Nature—style bibliography with a reusable presentation template.",
        "By default, use Nature-style references for this deck.",
        "使用 Nature 风格引用和幻灯片排版。",
        "Nature 风格参考文献与演示版式保持一致。",
        "默认采用 Nature 风格参考文献和汇报模板。",
        "使用 Nature 风格引用；幻灯片主题也按此设计。",
    ),
)
def test_mixed_citation_and_visual_branding_clauses_are_rejected(
    valid_repo: Path, validator, text: str
) -> None:
    (valid_repo / "README.md").write_text(text, encoding="utf-8")

    assert "identity.legacy" in codes(validator.validate_repository(valid_repo))


def test_historical_plans_and_generated_artifacts_are_excluded_from_legacy_scan(
    valid_repo: Path, validator
) -> None:
    plan = valid_repo / "docs/plans/history.md"
    output = valid_repo / "output/generated.txt"
    plan.parent.mkdir(parents=True)
    output.parent.mkdir(parents=True)
    plan.write_text("nature-paper2ppt and default Nature-style", encoding="utf-8")
    output.write_text("nature-paper2ppt and default Nature-style", encoding="utf-8")

    assert "identity.legacy" not in codes(validator.validate_repository(valid_repo))


def test_trigger_case_count_schema_and_duplicates_are_validated(
    valid_repo: Path, validator
) -> None:
    path = valid_repo / "tests/trigger_cases.json"
    malformed = [
        {
            "id": "duplicate",
            "query": "Make a paper PPT",
            "should_trigger": True,
            "category": "pdf",
        },
        {
            "id": "duplicate",
            "query": "Make a paper PPT",
            "should_trigger": "yes",
            "category": "pdf",
            "extra": "forbidden",
        },
    ]
    path.write_text(json.dumps(malformed), encoding="utf-8")

    found = codes(validator.validate_repository(valid_repo))
    assert {
        "triggers.count",
        "triggers.schema",
        "triggers.duplicate-id",
        "triggers.duplicate-query",
    } <= found


def test_validation_is_read_only(validator, valid_repo: Path) -> None:
    before = {
        path.relative_to(valid_repo): path.read_bytes()
        for path in valid_repo.rglob("*")
        if path.is_file()
    }

    validator.validate_repository(valid_repo)

    after = {
        path.relative_to(valid_repo): path.read_bytes()
        for path in valid_repo.rglob("*")
        if path.is_file()
    }
    assert after == before


def test_cli_supports_human_and_json_reports(validator, capsys) -> None:
    assert validator.main([], root=ROOT) == 0
    human = capsys.readouterr()
    assert human.err == ""
    assert "Paper2PPT repository validation: PASS" in human.out

    assert validator.main(["--json"], root=ROOT) == 0
    machine = capsys.readouterr()
    payload = json.loads(machine.out)
    assert payload == {"ok": True, "errors": []}
    assert machine.err == ""


def test_cli_returns_one_for_validation_failure(validator, valid_repo: Path, capsys) -> None:
    (valid_repo / "README.md").write_text("nature-paper2ppt", encoding="utf-8")

    assert validator.main([], root=valid_repo) == 1
    captured = capsys.readouterr()
    assert "Paper2PPT repository validation: FAIL" in captured.out
    assert "identity.legacy" in captured.out
