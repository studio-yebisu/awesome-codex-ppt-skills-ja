from __future__ import annotations

import importlib.metadata
import io
import json
import os
import shutil
import subprocess
import sys
import venv
from pathlib import Path
from types import SimpleNamespace

import doctor
import pytest
import runtime_environment

ROOT = Path(__file__).resolve().parents[1]


def no_renderer(backend):
    return {"requested": backend, "ready": False, "available": {"powerpoint": False, "libreoffice": False}}


def dependency_environment(monkeypatch, version="99.0", returncode=0):
    monkeypatch.setattr(doctor.importlib.metadata, "version", lambda name: version)
    monkeypatch.setattr(doctor.subprocess, "run", lambda *args, **kwargs:
                        SimpleNamespace(returncode=returncode, stderr="Broken dependency", stdout=""))


def test_missing_renderer_warns_or_fails_when_required(monkeypatch):
    dependency_environment(monkeypatch)
    monkeypatch.setattr(doctor, "renderer_environment", no_renderer)
    assert doctor.diagnose()["status"] == "warning"
    result = doctor.diagnose(backend="libreoffice", require_renderer=True)
    assert result["status"] == "fail"
    assert result["checks"][-1]["requested"] == "libreoffice"


@pytest.mark.parametrize("version", ["0.1", "10.0rc1", "10.0.dev1"])
def test_old_or_ambiguous_dependencies_do_not_pass(monkeypatch, version):
    dependency_environment(monkeypatch, version=version)
    checks = doctor.requirement_checks(ROOT)
    assert all(c["status"] == "fail" and c["remedy"] for c in checks)


def test_numeric_versions_compare_by_components(monkeypatch):
    dependency_environment(monkeypatch, version="100.0")
    assert all(c["status"] == "pass" for c in doctor.requirement_checks(ROOT))


def test_installed_but_broken_import_fails(monkeypatch):
    dependency_environment(monkeypatch, returncode=1)
    checks = doctor.requirement_checks(ROOT)
    assert all(c["status"] == "fail" and c["message"] == "Import failed" for c in checks)
    assert "Broken dependency" in checks[0]["detail"]


def test_import_timeout_is_actionable(monkeypatch):
    dependency_environment(monkeypatch)

    def timeout(command, **kwargs):
        assert kwargs["timeout"] == 15
        raise subprocess.TimeoutExpired(command, 15)

    monkeypatch.setattr(doctor.subprocess, "run", timeout)
    assert all(c["status"] == "fail" and c["remedy"] for c in doctor.requirement_checks(ROOT))


def test_missing_package_reports_the_selected_interpreter(monkeypatch):
    def missing(name):
        raise importlib.metadata.PackageNotFoundError(name)

    monkeypatch.setattr(doctor.importlib.metadata, "version", missing)
    for check in doctor.requirement_checks(ROOT):
        assert check["status"] == "fail"
        assert sys.executable in check["remedy"]


@pytest.mark.parametrize("requirements", ["", "Pillow==10.0", "unknown>=1.0"])
def test_unknown_or_empty_requirement_contract_fails(tmp_path, requirements):
    (tmp_path / "requirements.txt").write_text(requirements)
    assert doctor.requirement_checks(tmp_path)[0]["status"] == "fail"


def test_missing_requirements_is_actionable(tmp_path):
    assert doctor.requirement_checks(tmp_path)[0]["status"] == "fail"


def test_doctor_is_read_only_and_runs_without_site_packages(tmp_path):
    env = tmp_path / "env"
    venv.EnvBuilder(with_pip=False).create(env)
    python = env / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    skill = tmp_path / "skill"
    (skill / "scripts").mkdir(parents=True)
    for name in ("doctor.py", "runtime_environment.py"):
        shutil.copy2(ROOT / "scripts" / name, skill / "scripts" / name)
    shutil.copy2(ROOT / "requirements.txt", skill)
    shutil.copy2(ROOT / "manifest.yaml", skill)
    before = {p.relative_to(skill): p.read_bytes() for p in skill.rglob("*") if p.is_file()}
    result = subprocess.run([str(python), str(skill / "scripts/doctor.py"), "--json"],
                            cwd=tmp_path, capture_output=True, text=True, check=False)
    assert result.returncode == 1, result.stderr
    report = json.loads(result.stdout)
    assert report["schema_version"] == "1.0"
    assert report["skill_version"] != "unknown"
    failures = [c for c in report["checks"] if c["id"].startswith("dependency:")]
    assert len(failures) == 3
    assert all(c["status"] == "fail" and c["remedy"] for c in failures)
    assert before == {p.relative_to(skill): p.read_bytes() for p in skill.rglob("*") if p.is_file()}


def test_discovery_requires_poppler_and_respects_backend(monkeypatch):
    monkeypatch.setattr(runtime_environment.shutil, "which", lambda name: "/bin/soffice" if name == "soffice" else None)
    assert runtime_environment.renderer_environment("libreoffice")["ready"] is False
    monkeypatch.setattr(runtime_environment.shutil, "which", lambda name: "/bin/" + name if name in ("soffice", "pdftoppm") else None)
    assert runtime_environment.renderer_environment("libreoffice")["ready"] is True
    assert runtime_environment.renderer_environment("powerpoint")["ready"] is False


def test_legacy_console_output_and_json_remain_usable(monkeypatch):
    dependency_environment(monkeypatch)
    monkeypatch.setattr(doctor, "renderer_environment", no_renderer)
    report = doctor.diagnose(Path("C:/用户/🙂"))
    buffer = io.BytesIO()
    output = io.TextIOWrapper(buffer, encoding="gbk")
    monkeypatch.setattr(sys, "stdout", output)
    doctor.emit(report)
    doctor.emit(report, as_json=True)
    output.flush()
    assert "SlideMuse runtime" in buffer.getvalue().decode("gbk")
