#!/usr/bin/env python3
"""Check that the pinned Python runtime can import its required packages."""

from __future__ import annotations

import argparse
import importlib
import importlib.metadata
import os
from pathlib import Path
import re
import subprocess
import sys


REPO_ROOT = Path(__file__).resolve().parent.parent
REQUIREMENTS = Path(__file__).with_name("requirements-runtime.txt")
MINIMUM_PYTHON = (3, 10)
IMPORT_NAMES = {
    "python-pptx": "pptx",
    "pillow": "PIL",
    "lxml": "lxml",
    "xlsxwriter": "xlsxwriter",
    "typing-extensions": "typing_extensions",
    "contourpy": "contourpy",
    "cycler": "cycler",
    "et-xmlfile": "et_xmlfile",
    "fonttools": "fontTools",
    "kiwisolver": "kiwisolver",
    "matplotlib": "matplotlib",
    "numpy": "numpy",
    "openpyxl": "openpyxl",
    "packaging": "packaging",
    "pandas": "pandas",
    "pyarrow": "pyarrow",
    "pyparsing": "pyparsing",
    "python-dateutil": "dateutil",
    "six": "six",
}
PIN_PATTERN = re.compile(r"^([A-Za-z0-9_.-]+)==([^\s;]+)$")


def normalize_distribution(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def project_venv_python() -> Path:
    if os.name == "nt":
        return REPO_ROOT / ".venv" / "Scripts" / "python.exe"
    return REPO_ROOT / ".venv" / "bin" / "python"


def in_project_venv() -> bool:
    return Path(sys.prefix).resolve() == (REPO_ROOT / ".venv").resolve()


def load_pins() -> list[tuple[str, str, str]]:
    pins: list[tuple[str, str, str]] = []
    for line_number, raw_line in enumerate(
        REQUIREMENTS.read_text(encoding="utf-8").splitlines(), start=1
    ):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        match = PIN_PATTERN.fullmatch(line)
        if match is None:
            raise ValueError(
                f"{REQUIREMENTS.name}:{line_number} must use an exact name==version pin"
            )
        distribution, version = match.groups()
        normalized = normalize_distribution(distribution)
        import_name = IMPORT_NAMES.get(normalized)
        if import_name is None:
            raise ValueError(
                f"{REQUIREMENTS.name}:{line_number} has no import check for {distribution}"
            )
        pins.append((distribution, version, import_name))
    return pins


def print_install_steps() -> None:
    launcher = "py -3" if os.name == "nt" else "python3"
    print("\nInstall or repair the isolated, pinned runtime:")
    print(f"  {launcher} scripts/runtime_doctor.py --bootstrap")


def bootstrap_runtime() -> int:
    try:
        load_pins()
    except (OSError, ValueError) as exc:
        print(f"FAIL Cannot bootstrap runtime: {exc}")
        return 1

    venv_python = project_venv_python()
    commands = [
        [sys.executable, "-m", "venv", str(REPO_ROOT / ".venv")],
        [
            str(venv_python),
            "-m",
            "pip",
            "install",
            "--requirement",
            str(REQUIREMENTS),
        ],
        [
            str(venv_python),
            str(Path(__file__).resolve()),
            "--current-interpreter",
        ],
    ]
    for command in commands:
        try:
            completed = subprocess.run(command, cwd=REPO_ROOT, check=False)
        except OSError as exc:
            print(f"FAIL Could not run runtime setup command: {exc}")
            return 1
        if completed.returncode != 0:
            print(
                f"FAIL Runtime setup command exited {completed.returncode}: "
                f"{' '.join(command)}"
            )
            return completed.returncode
    return 0


def check_runtime() -> int:
    failures: list[str] = []
    version = ".".join(str(part) for part in sys.version_info[:3])

    print("Presentation Skill Python runtime doctor")
    print(f"Interpreter: {sys.executable}")
    print(f"Python: {version}")
    print(f"Pins: {REQUIREMENTS.relative_to(REPO_ROOT)}")

    if sys.version_info < MINIMUM_PYTHON:
        failures.append(
            f"Python {MINIMUM_PYTHON[0]}.{MINIMUM_PYTHON[1]} or newer is required"
        )

    try:
        pins = load_pins()
    except (OSError, ValueError) as exc:
        failures.append(str(exc))
        pins = []

    for distribution, expected_version, import_name in pins:
        try:
            importlib.import_module(import_name)
            installed_version = importlib.metadata.version(distribution)
        except (ImportError, importlib.metadata.PackageNotFoundError) as exc:
            failures.append(
                f"{distribution}=={expected_version}: import {import_name!r} failed "
                f"({exc.__class__.__name__}: {exc})"
            )
            continue
        except Exception as exc:
            failures.append(
                f"{distribution}=={expected_version}: import {import_name!r} raised "
                f"{exc.__class__.__name__}: {exc}"
            )
            continue

        if installed_version != expected_version:
            failures.append(
                f"{distribution}: installed {installed_version}, pinned {expected_version}"
            )
        else:
            print(f"PASS {distribution}=={installed_version} (import {import_name})")

    if failures:
        print("\nFAIL Runtime is not ready:")
        for failure in failures:
            print(f"  - {failure}")
        print_install_steps()
        return 1

    print("\nPASS Runtime imports and pinned versions are ready.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--current-interpreter",
        action="store_true",
        help="check this interpreter instead of an existing project .venv",
    )
    parser.add_argument(
        "--bootstrap",
        action="store_true",
        help="create .venv, install the exact pins, and validate imports",
    )
    args = parser.parse_args()

    if args.bootstrap:
        return bootstrap_runtime()

    venv_python = project_venv_python()
    if not args.current_interpreter and venv_python.is_file() and not in_project_venv():
        completed = subprocess.run(
            [str(venv_python), str(Path(__file__).resolve()), "--current-interpreter"],
            check=False,
        )
        return completed.returncode
    return check_runtime()


if __name__ == "__main__":
    raise SystemExit(main())
