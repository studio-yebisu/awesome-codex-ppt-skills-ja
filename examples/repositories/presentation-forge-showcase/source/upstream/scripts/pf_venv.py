#!/usr/bin/env python3
"""Shared helper so optional Python deps (currently just Pillow) never get
installed into the system/global Python - a global `pip install` can clobber
a version another project on the machine relies on.

A script that needs a package beyond stdlib should catch its ImportError and
call `reexec_in_venv("<pypi-name>", ...)`: it creates (or reuses) a venv at
`~/.cache/presentation-forge/venv`, installs whatever's missing there, and
replaces the current process with that venv's interpreter re-running the same
script and args. It never returns on success.

Standard library only (it has to be, to bootstrap the venv in the first place).
"""

import importlib.metadata
import os
import subprocess
import sys
import venv
from pathlib import Path

VENV_DIR = Path.home() / ".cache" / "presentation-forge" / "venv"


def _python() -> Path:
    if sys.platform == "win32":
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python3"


def _has(py: Path, dist_name: str) -> bool:
    r = subprocess.run(
        [str(py), "-c",
         f"import importlib.metadata as m; m.distribution({dist_name!r})"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    return r.returncode == 0


def reexec_in_venv(*packages: str) -> None:
    """Ensure `packages` (PyPI distribution names, e.g. "pillow") are
    installed in the dedicated venv, then exec this same script under that
    venv's python. Raises on failure (no network, no venv module, ...) -
    callers should catch that and fall back to telling the user what to do."""
    py = _python()
    if not py.exists():
        venv.EnvBuilder(with_pip=True).create(VENV_DIR)
    missing = [p for p in packages if not _has(py, p)]
    if missing:
        subprocess.run([str(py), "-m", "pip", "install", "-q", *missing],
                        check=True)
    os.execv(str(py), [str(py), sys.argv[0], *sys.argv[1:]])
