import json
from pathlib import Path
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
PACKAGED_SKILL = ROOT / "plugins" / "paper2ppt" / "skills" / "paper2ppt"
DECK = ROOT / "examples" / "output" / "paper2ppt-example-zh.pptx"


def test_active_skill_commands_resolve_helpers_from_the_skill_directory() -> None:
    surfaces = (
        ROOT / "SKILL.md",
        ROOT / "references" / "tool-routing.md",
        ROOT / "references" / "quality-gates.md",
    )
    combined = "\n".join(path.read_text(encoding="utf-8") for path in surfaces)

    assert "python scripts/preflight.py" not in combined
    assert "python scripts/inspect_pptx.py" not in combined
    assert 'python "<SKILL_DIR>/scripts/preflight.py"' in combined
    assert 'python "<SKILL_DIR>/scripts/inspect_pptx.py"' in combined
    assert "${CLAUDE_SKILL_DIR}" in combined
    assert "available-skills" in combined
    assert "current working directory" in combined


def test_packaged_helpers_run_from_an_unrelated_working_directory(tmp_path: Path) -> None:
    installed_skill = tmp_path / "installed" / "paper2ppt"
    shutil.copytree(PACKAGED_SKILL, installed_skill)
    workspace = tmp_path / "unrelated-project"
    workspace.mkdir()
    source = workspace / "paper.txt"
    source.write_text("Title\n\nA source-grounded abstract.", encoding="utf-8")
    output = workspace / "output"
    output.mkdir()

    preflight = subprocess.run(
        [
            sys.executable,
            str(installed_skill / "scripts" / "preflight.py"),
            str(source),
            "--output",
            str(output),
            "--json",
        ],
        cwd=workspace,
        capture_output=True,
        text=True,
        check=False,
    )
    assert preflight.returncode == 0, preflight.stdout + preflight.stderr
    assert json.loads(preflight.stdout)["ok"] is True

    inspector = subprocess.run(
        [
            sys.executable,
            str(installed_skill / "scripts" / "inspect_pptx.py"),
            str(DECK),
            "--require-notes",
            "--json",
        ],
        cwd=workspace,
        capture_output=True,
        text=True,
        check=False,
    )
    assert inspector.returncode == 0, inspector.stdout + inspector.stderr
    report = json.loads(inspector.stdout)
    assert report["ok"] is True
    assert report["notes_slides"] == report["slides"] == 9
