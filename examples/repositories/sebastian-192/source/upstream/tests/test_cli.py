from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import venv
from pathlib import Path
from types import SimpleNamespace

import pytest

import slidemuse

ROOT = Path(__file__).resolve().parents[1]


def invoke(*arguments, cwd=None):
    return subprocess.run([sys.executable, str(ROOT / "slidemuse.py"), *map(str, arguments)],
                          cwd=cwd, capture_output=True, text=True, errors="replace", check=False)


def test_help_and_version_work_without_dependencies(tmp_path):
    env = tmp_path / "env"
    venv.EnvBuilder(with_pip=False).create(env)
    python = env / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    for args in (("--help",), ("--version",)):
        result = subprocess.run([str(python), str(ROOT / "slidemuse.py"), *args],
                                capture_output=True, text=True, check=False)
        assert result.returncode == 0, result.stderr
        assert "SlideMuse" in result.stdout


def test_validate_matches_direct_script_from_another_directory(tmp_path):
    spec = ROOT / "examples/page-spec.example.json"
    direct = subprocess.run([sys.executable, str(ROOT / "scripts/validate_page_spec.py"), str(spec), "--strict"],
                            cwd=tmp_path, capture_output=True, text=True, check=False)
    wrapped = invoke("validate", spec, "--strict", cwd=tmp_path)
    assert wrapped.returncode == direct.returncode == 0
    assert wrapped.stdout == direct.stdout
    assert wrapped.stderr == direct.stderr


def test_subcommand_help_is_forwarded():
    result = invoke("render", "--help")
    assert result.returncode == 0
    assert "--measure-text" in result.stdout
    assert "--backend" in result.stdout


@pytest.mark.parametrize("exit_code", [0, 1, 2, 3])
def test_dispatch_preserves_arguments_cwd_and_exit_code(monkeypatch, exit_code):
    calls = []

    def run(command, **kwargs):
        calls.append((command, kwargs))
        return SimpleNamespace(returncode=exit_code)

    monkeypatch.setattr(slidemuse.subprocess, "run", run)
    assert slidemuse.main(["check", "材料/job.json", "输出", "--backend-is-invalid"]) == exit_code
    command, kwargs = calls[0]
    assert command[2:] == ["材料/job.json", "输出", "--backend-is-invalid", "--check"]
    assert kwargs == {"check": False}  # No cwd change or output interception.


def test_unknown_command_and_missing_packaged_tool_fail(tmp_path, monkeypatch):
    assert invoke("not-a-command").returncode == 2
    monkeypatch.setattr(slidemuse, "ROOT", tmp_path)
    with pytest.raises(SystemExit) as error:
        slidemuse.main(["sample"])
    assert error.value.code == 2


def test_check_does_not_create_workspace(tmp_path):
    result = invoke("check", tmp_path / "missing-job.json", tmp_path / "output")
    assert result.returncode == 1
    assert json.loads(result.stdout)["status"] == "blocked"
    assert not (tmp_path / "output").exists()


def test_runtime_python_uses_local_venv_path_without_resolving_symlink(tmp_path):
    python = tmp_path / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    python.parent.mkdir(parents=True)
    if os.name == "nt":
        python.touch()
    else:
        python.symlink_to(sys.executable)
    (tmp_path / ".skill-python").write_text("/stale/location/python\n")
    assert slidemuse.runtime_python(tmp_path) == python.absolute()


def test_installed_launcher_selects_isolated_python_after_relocation(tmp_path):
    stage = tmp_path / "original"
    stage.mkdir()
    shutil.copy2(ROOT / "slidemuse.py", stage)
    shutil.copy2(ROOT / "manifest.yaml", stage)
    (stage / "scripts").mkdir()
    (stage / "scripts/doctor.py").write_text(
        "import json, sys\nprint(json.dumps({'prefix': sys.prefix, 'args': sys.argv[1:]}))\n", encoding="utf-8")
    venv.EnvBuilder(with_pip=False).create(stage / ".venv")
    (stage / ".skill-python").write_text("/stale/interpreter/path\n")
    moved = tmp_path / "moved skill with spaces"
    stage.rename(moved)
    result = subprocess.run([sys.executable, str(moved / "slidemuse.py"), "doctor", "--json"],
                            cwd=tmp_path, capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    assert Path(report["prefix"]) == moved / ".venv"
    assert report["args"] == ["--json"]
