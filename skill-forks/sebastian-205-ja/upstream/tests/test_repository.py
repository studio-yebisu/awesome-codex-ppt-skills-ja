from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_release_metadata_exists() -> None:
    assert (ROOT / "VERSION").read_text(encoding="utf-8").strip() == "0.1.0"
    assert "MIT License" in (ROOT / "LICENSE").read_text(encoding="utf-8")
    assert (ROOT / "requirements-dev.txt").is_file()


def test_repository_has_no_generated_outputs_tracked_by_default() -> None:
    ignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    for pattern in (".venv/", "__pycache__/", ".pytest_cache/", "output/"):
        assert pattern in ignore


def test_ci_runs_the_deterministic_repository_contract() -> None:
    workflow_path = ROOT / ".github/workflows/ci.yml"
    workflow_text = workflow_path.read_text(encoding="utf-8")
    workflow = yaml.safe_load(workflow_text)

    assert set(workflow["on"]) == {"push", "pull_request"}

    job = workflow["jobs"]["validate"]
    assert job["strategy"]["matrix"]["python-version"] == ["3.10", "3.12"]

    uses = [step["uses"] for step in job["steps"] if "uses" in step]
    assert "actions/checkout@v6" in uses
    assert "actions/setup-python@v6" in uses

    skills_ref_steps = [
        step for step in job["steps"] if "Agent Skills" in step.get("name", "")
    ]
    assert len(skills_ref_steps) == 2
    assert all(
        step.get("if") == "matrix.python-version == '3.12'"
        for step in skills_ref_steps
    )

    commands = {
        line.strip()
        for step in job["steps"]
        for line in step.get("run", "").splitlines()
        if line.strip()
    }
    for command in (
        "pip install -r requirements-dev.txt",
        'pip install "git+https://github.com/agentskills/agentskills.git#subdirectory=skills-ref"',
        "python scripts/sync_plugin.py --check",
        "python scripts/validate_repo.py",
        'ln -s "$PWD" "$RUNNER_TEMP/paper2ppt"',
        'skills-ref validate "$RUNNER_TEMP/paper2ppt"',
        "skills-ref validate plugins/paper2ppt/skills/paper2ppt",
        "pytest -q",
    ):
        assert command in commands

    lower_workflow = workflow_text.lower()
    for forbidden in (
        "openai_api_key",
        "anthropic_api_key",
        "libreoffice",
        "soffice",
        "pdftoppm",
    ):
        assert forbidden not in lower_workflow
