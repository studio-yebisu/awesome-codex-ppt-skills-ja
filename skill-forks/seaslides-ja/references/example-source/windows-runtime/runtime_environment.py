"""Stable, local-only fingerprints for the HTML rendering environment."""

from __future__ import annotations

import json
import platform
import subprocess
from importlib import metadata
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parent


def _command_version(command: list[str]) -> str | None:
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    value = (result.stdout or result.stderr).strip()
    return value if result.returncode == 0 and value else None


def _browser_version() -> str | None:
    candidates = [
        Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
        Path("/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"),
        Path("/usr/bin/google-chrome"),
        Path("/usr/bin/google-chrome-stable"),
        Path("/usr/bin/chromium"),
        Path("/usr/bin/chromium-browser"),
        Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
        Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
        Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
        Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
    ]
    for candidate in candidates:
        if candidate.is_file():
            version = _command_version([str(candidate), "--version"])
            if version:
                return version
    return None


def runtime_environment_fingerprint() -> dict[str, str]:
    """Capture versions that can materially affect generated slide artifacts.

    The probe is deterministic, local-only, and best effort. Missing optional
    tools are omitted rather than causing compilation or validation to fail.
    """
    fingerprint: dict[str, str] = {"python": platform.python_version()}
    node = _command_version(["node", "--version"])
    if node:
        fingerprint["node"] = node
    browser = _browser_version()
    if browser:
        fingerprint["browser"] = browser

    for package in ("Pillow", "python-pptx", "lxml", "CairoSVG"):
        try:
            fingerprint[f"python:{package}"] = metadata.version(package)
        except metadata.PackageNotFoundError:
            continue

    for package_file, key in (
        (
            SCRIPTS_DIR / "html_to_svg" / "node_modules" / "playwright" / "package.json",
            "playwright",
        ),
        (
            SCRIPTS_DIR / "html_to_svg" / "node_modules" / "playwright-core" / "browsers.json",
            "playwright_browsers",
        ),
    ):
        try:
            data = json.loads(package_file.read_text(encoding="utf-8"))
            if key == "playwright" and isinstance(data.get("version"), str):
                fingerprint[key] = data["version"]
            elif key == "playwright_browsers":
                browsers = data.get("browsers", []) if isinstance(data, dict) else data
                chromium = next(
                    (
                        item for item in browsers
                        if isinstance(item, dict) and item.get("name") == "chromium"
                    ),
                    None,
                )
                if chromium and isinstance(chromium.get("revision"), (str, int)):
                    fingerprint["chromium_revision"] = str(chromium["revision"])
        except (OSError, json.JSONDecodeError, TypeError):
            continue
    return dict(sorted(fingerprint.items()))
