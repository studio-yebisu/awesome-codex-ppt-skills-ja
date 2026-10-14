"""Read-only renderer, dependency and installed-font fingerprints for render caches."""
from __future__ import annotations

import hashlib
import importlib.metadata
import json
import os
import platform
import re
import shutil
from pathlib import Path

_HASHES = {}


def file_identity(path):
    path = Path(path)
    try:
        stat = path.stat()
        key = (str(path.resolve()), stat.st_size, stat.st_mtime_ns, stat.st_ctime_ns)
        if key not in _HASHES:
            value = hashlib.sha256()
            with path.open("rb") as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    value.update(block)
            _HASHES[key] = value.hexdigest()
        return {"path": str(path.resolve()), "sha256": _HASHES[key]}
    except OSError as error:
        return {"path": str(path), "unavailable": type(error).__name__}


def font_directories():
    if os.name == "nt":
        return [Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts",
                Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "Microsoft/Windows/Fonts"]
    return [Path("/usr/share/fonts"), Path("/usr/local/share/fonts"), Path.home() / ".fonts",
            Path.home() / ".local/share/fonts", Path("/System/Library/Fonts"), Path("/Library/Fonts")]


def powerpoint_binary():
    if os.name != "nt":
        return None
    import winreg
    try:
        with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r"PowerPoint.Application\CLSID") as key:
            clsid = winreg.QueryValue(key, None)
        with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, fr"CLSID\{clsid}\LocalServer32") as key:
            command = winreg.QueryValue(key, None)
        match = re.match(r'^\s*"([^"]+)"|^\s*(.*?\.exe)(?:\s|$)', command, re.IGNORECASE)
        return Path(match.group(1) or match.group(2)) if match else None
    except OSError:
        return None


def fingerprint():
    binaries = {name: file_identity(path) if path else None for name, path in (
        ("powerpoint", powerpoint_binary()),
        ("libreoffice", shutil.which("soffice") or shutil.which("libreoffice")),
        ("pdftoppm", shutil.which("pdftoppm")),
        ("powershell", shutil.which("powershell.exe") or shutil.which("powershell")))}
    for name, filenames in (("powerpoint", ("PPCORE.DLL", "MSO.DLL", "MSOINTL.DLL")),
                            ("libreoffice", ("soffice.bin", "libmergedlo.so", "mergedlo.dll"))):
        if binaries[name]:
            parent = Path(binaries[name]["path"]).parent
            binaries[name]["components"] = {filename: file_identity(parent / filename)
                                            for filename in filenames if (parent / filename).is_file()}
    fonts, problems = {}, []
    for directory in font_directories():
        if directory.exists():
            try:
                for path in sorted(directory.rglob("*")):
                    if path.suffix.lower() in (".ttf", ".otf", ".ttc", ".otc") and path.is_file():
                        fonts[str(path.resolve())] = file_identity(path)
            except OSError as error:
                problems.append(f"{directory}: {type(error).__name__}")
    dependencies = {}
    for name in ("Pillow", "python-pptx", "jsonschema"):
        try:
            dependencies[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            dependencies[name] = None
    return {"version": "1.0", "system": platform.platform(), "python": platform.python_version(),
            "binaries": binaries, "dependencies": dependencies, "fonts": fonts, "font_scan_problems": problems,
            "scope": "Installed font inventory and executable bytes; not a guarantee of Office layout or font selection."}


def environment_key(snapshot, backend):
    names = ("powerpoint", "powershell") if backend == "powerpoint" else ("libreoffice", "pdftoppm")
    value = {**snapshot, "binaries": {name: snapshot["binaries"].get(name) for name in names}}
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
