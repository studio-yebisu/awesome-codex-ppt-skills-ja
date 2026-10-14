import importlib.util
import json
from pathlib import Path

import pytest
import yaml


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "paper2ppt"
PACKAGED_SKILL = PLUGIN / "skills" / "paper2ppt"
SYNC_SCRIPT = ROOT / "scripts" / "sync_plugin.py"


def read_json(path: Path) -> dict:
    assert path.is_file(), f"Missing JSON file: {path}"
    return json.loads(path.read_text(encoding="utf-8"))


def version() -> str:
    return (ROOT / "VERSION").read_text(encoding="utf-8").strip()


def packaged(relative: str) -> Path:
    return PACKAGED_SKILL / relative


@pytest.fixture(scope="module")
def sync_plugin():
    assert SYNC_SCRIPT.is_file()
    spec = importlib.util.spec_from_file_location("sync_plugin", SYNC_SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_plugin_manifests_match_release_identity() -> None:
    codex_manifest = read_json(PLUGIN / ".codex-plugin" / "plugin.json")
    claude_manifest = read_json(PLUGIN / ".claude-plugin" / "plugin.json")

    assert codex_manifest["name"] == "paper2ppt"
    assert claude_manifest["name"] == "paper2ppt"
    assert codex_manifest["version"] == claude_manifest["version"] == version()
    assert codex_manifest["license"] == claude_manifest["license"] == "MIT"
    assert codex_manifest["homepage"] == "https://github.com/wp-a/paper2ppt"
    assert claude_manifest["homepage"] == "https://github.com/wp-a/paper2ppt"
    assert codex_manifest["repository"] == "https://github.com/wp-a/paper2ppt"
    assert claude_manifest["repository"] == "https://github.com/wp-a/paper2ppt"
    assert codex_manifest["skills"] == "./skills/"
    assert "skills" not in claude_manifest
    assert claude_manifest["$schema"] == (
        "https://anthropic.com/claude-code/plugin.schema.json"
    )


def test_plugin_manifests_do_not_declare_unused_components() -> None:
    codex_manifest = read_json(PLUGIN / ".codex-plugin" / "plugin.json")
    claude_manifest = read_json(PLUGIN / ".claude-plugin" / "plugin.json")
    forbidden = {"agents", "apps", "hooks", "mcpServers", "settings"}

    assert forbidden.isdisjoint(codex_manifest)
    assert forbidden.isdisjoint(claude_manifest)


def test_codex_ui_metadata_is_chinese_first() -> None:
    metadata_path = packaged("agents/openai.yaml")
    assert metadata_path.is_file()
    metadata = yaml.safe_load(metadata_path.read_text(encoding="utf-8"))
    interface = metadata["interface"]

    assert interface["display_name"] == "Paper2PPT"
    assert 25 <= len(interface["short_description"]) <= 64
    assert "$paper2ppt" in interface["default_prompt"]
    assert any("\u4e00" <= char <= "\u9fff" for char in interface["default_prompt"])
    assert metadata["policy"]["allow_implicit_invocation"] is True
    assert "dependencies" not in metadata


def test_marketplaces_point_to_the_local_plugin() -> None:
    codex_marketplace = read_json(ROOT / ".agents" / "plugins" / "marketplace.json")
    claude_marketplace = read_json(ROOT / ".claude-plugin" / "marketplace.json")
    codex_entry = next(
        entry for entry in codex_marketplace["plugins"] if entry["name"] == "paper2ppt"
    )
    claude_entry = next(
        entry for entry in claude_marketplace["plugins"] if entry["name"] == "paper2ppt"
    )

    assert codex_entry["source"] == {
        "source": "local",
        "path": "./plugins/paper2ppt",
    }
    assert codex_entry["policy"] == {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL",
    }
    assert claude_entry["source"] == "./plugins/paper2ppt"
    assert claude_marketplace["$schema"] == (
        "https://anthropic.com/claude-code/marketplace.schema.json"
    )


def test_plugin_skill_is_an_exact_mirror() -> None:
    assert packaged("SKILL.md").read_bytes() == (ROOT / "SKILL.md").read_bytes()
    canonical_root = ROOT / "references"
    packaged_root = packaged("references")
    canonical_files = {
        path.relative_to(canonical_root)
        for path in canonical_root.rglob("*")
        if path.is_file()
    }
    packaged_files = {
        path.relative_to(packaged_root)
        for path in packaged_root.rglob("*")
        if path.is_file()
    }
    assert packaged_files == canonical_files
    for relative in canonical_files:
        assert (packaged_root / relative).read_bytes() == (
            canonical_root / relative
        ).read_bytes()


def test_sync_check_detects_drift_without_modifying_files(
    tmp_path: Path, sync_plugin
) -> None:
    (tmp_path / "SKILL.md").write_text("canonical skill\n", encoding="utf-8")
    (tmp_path / "references").mkdir()
    (tmp_path / "references" / "workflow.md").write_text(
        "canonical reference\n", encoding="utf-8"
    )
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "preflight.py").write_text(
        "# canonical runtime helper\n", encoding="utf-8"
    )

    target = tmp_path / "plugins" / "paper2ppt" / "skills" / "paper2ppt"
    (target / "references").mkdir(parents=True)
    (target / "scripts").mkdir()
    (target / "agents").mkdir()
    (target / "SKILL.md").write_text("drifted skill\n", encoding="utf-8")
    (target / "references" / "stale.md").write_text("stale\n", encoding="utf-8")
    (target / "scripts" / "stale.py").write_text("# stale\n", encoding="utf-8")
    metadata = target / "agents" / "openai.yaml"
    metadata.write_text("interface: {}\n", encoding="utf-8")

    drift = sync_plugin.sync(tmp_path, check=True)

    assert drift
    assert (target / "SKILL.md").read_text(encoding="utf-8") == "drifted skill\n"
    assert (target / "references" / "stale.md").is_file()
    assert (target / "scripts" / "stale.py").is_file()
    assert metadata.read_text(encoding="utf-8") == "interface: {}\n"


def test_sync_removes_stale_managed_files_and_preserves_ui_metadata(
    tmp_path: Path, sync_plugin
) -> None:
    (tmp_path / "SKILL.md").write_text("canonical skill\n", encoding="utf-8")
    (tmp_path / "references").mkdir()
    (tmp_path / "references" / "workflow.md").write_text(
        "canonical reference\n", encoding="utf-8"
    )
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "inspect_pptx.py").write_text(
        "# canonical runtime helper\n", encoding="utf-8"
    )

    target = tmp_path / "plugins" / "paper2ppt" / "skills" / "paper2ppt"
    (target / "references").mkdir(parents=True)
    (target / "scripts").mkdir()
    (target / "agents").mkdir()
    (target / "references" / "stale.md").write_text("stale\n", encoding="utf-8")
    (target / "scripts" / "stale.py").write_text("# stale\n", encoding="utf-8")
    metadata = target / "agents" / "openai.yaml"
    metadata.write_text("interface: {}\n", encoding="utf-8")

    changes = sync_plugin.sync(tmp_path, check=False)

    assert changes
    assert (target / "SKILL.md").read_text(encoding="utf-8") == "canonical skill\n"
    assert not (target / "references" / "stale.md").exists()
    assert not (target / "scripts" / "stale.py").exists()
    assert metadata.read_text(encoding="utf-8") == "interface: {}\n"
    assert sync_plugin.sync(tmp_path, check=True) == []


def test_sync_rejects_packaged_managed_directory_symlink(
    tmp_path: Path, sync_plugin
) -> None:
    root = tmp_path / "repo"
    external = tmp_path / "external"
    root.mkdir()
    external.mkdir()
    (root / "SKILL.md").write_text("canonical skill\n", encoding="utf-8")
    (root / "references").mkdir()
    (root / "references" / "workflow.md").write_text(
        "canonical reference\n", encoding="utf-8"
    )
    external_reference = external / "workflow.md"
    external_reference.write_text("external sentinel\n", encoding="utf-8")

    target = root / "plugins" / "paper2ppt" / "skills" / "paper2ppt"
    target.mkdir(parents=True)
    (target / "references").symlink_to(external, target_is_directory=True)

    try:
        with pytest.raises(RuntimeError, match="unsafe symlink"):
            sync_plugin.sync(root)
    finally:
        assert external_reference.read_text(encoding="utf-8") == "external sentinel\n"


def test_sync_rejects_packaged_destination_file_symlink(
    tmp_path: Path, sync_plugin
) -> None:
    root = tmp_path / "repo"
    external = tmp_path / "external"
    root.mkdir()
    external.mkdir()
    (root / "SKILL.md").write_text("canonical skill\n", encoding="utf-8")
    (root / "references").mkdir()
    external_skill = external / "SKILL.md"
    external_skill.write_text("external sentinel\n", encoding="utf-8")

    target = root / "plugins" / "paper2ppt" / "skills" / "paper2ppt"
    target.mkdir(parents=True)
    (target / "SKILL.md").symlink_to(external_skill)

    try:
        with pytest.raises(RuntimeError, match="unsafe symlink"):
            sync_plugin.sync(root)
    finally:
        assert external_skill.read_text(encoding="utf-8") == "external sentinel\n"


def test_sync_rejects_canonical_reference_symlink(
    tmp_path: Path, sync_plugin
) -> None:
    root = tmp_path / "repo"
    external = tmp_path / "external"
    root.mkdir()
    external.mkdir()
    (root / "SKILL.md").write_text("canonical skill\n", encoding="utf-8")
    (root / "references").mkdir()
    external_reference = external / "workflow.md"
    external_reference.write_text("external sentinel\n", encoding="utf-8")
    (root / "references" / "workflow.md").symlink_to(external_reference)

    try:
        with pytest.raises(RuntimeError, match="unsafe symlink"):
            sync_plugin.sync(root)
    finally:
        assert external_reference.read_text(encoding="utf-8") == "external sentinel\n"


def test_sync_rejects_packaged_target_ancestor_symlink(
    tmp_path: Path, sync_plugin
) -> None:
    root = tmp_path / "repo"
    external = tmp_path / "external"
    root.mkdir()
    external.mkdir()
    (root / "SKILL.md").write_text("canonical skill\n", encoding="utf-8")
    (root / "references").mkdir()
    (root / "plugins").symlink_to(external, target_is_directory=True)

    expected_external_target = external / "paper2ppt" / "skills" / "paper2ppt"
    try:
        with pytest.raises(RuntimeError, match="unsafe symlink"):
            sync_plugin.sync(root)
    finally:
        assert not expected_external_target.exists()


def _prepare_blocked_destination_parent(root: Path) -> tuple[Path, Path]:
    root.mkdir()
    (root / "SKILL.md").write_text("canonical skill\n", encoding="utf-8")
    nested_reference = root / "references" / "nested" / "workflow.md"
    nested_reference.parent.mkdir(parents=True)
    nested_reference.write_text("canonical reference\n", encoding="utf-8")

    target = root / "plugins" / "paper2ppt" / "skills" / "paper2ppt"
    (target / "references").mkdir(parents=True)
    packaged_skill = target / "SKILL.md"
    packaged_skill.write_text("stale skill\n", encoding="utf-8")
    blocking_parent = target / "references" / "nested"
    blocking_parent.write_text("blocking sentinel\n", encoding="utf-8")
    return packaged_skill, blocking_parent


def test_sync_rejects_non_directory_destination_parent_without_partial_mutation(
    tmp_path: Path, sync_plugin
) -> None:
    root = tmp_path / "repo"
    packaged_skill, blocking_parent = _prepare_blocked_destination_parent(root)

    try:
        with pytest.raises(RuntimeError, match="unsafe non-directory"):
            sync_plugin.sync(root)
    finally:
        assert packaged_skill.read_text(encoding="utf-8") == "stale skill\n"
        assert blocking_parent.read_text(encoding="utf-8") == "blocking sentinel\n"


def test_sync_cli_returns_exit_two_for_non_directory_destination_parent(
    tmp_path: Path, sync_plugin, capsys
) -> None:
    root = tmp_path / "repo"
    packaged_skill, blocking_parent = _prepare_blocked_destination_parent(root)

    result = sync_plugin.main([], root=root)

    captured = capsys.readouterr()
    assert result == 2
    assert captured.out == ""
    assert "Paper2PPT sync error: unsafe non-directory" in captured.err
    assert packaged_skill.read_text(encoding="utf-8") == "stale skill\n"
    assert blocking_parent.read_text(encoding="utf-8") == "blocking sentinel\n"
