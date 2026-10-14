"""Standard-library-only renderer discovery shared by preflight and doctor."""
from __future__ import annotations

import os
import shutil


def renderer_environment(backend="auto"):
    if backend not in ("auto", "powerpoint", "libreoffice"):
        raise ValueError("Unknown render backend")
    shell = shutil.which("powershell.exe") or shutil.which("powershell")
    registered = False
    if os.name == "nt":
        import winreg
        try:
            with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r"PowerPoint.Application\CLSID"):
                registered = True
        except OSError:
            pass
    powerpoint = bool(shell and registered)
    libreoffice = bool((shutil.which("soffice") or shutil.which("libreoffice")) and shutil.which("pdftoppm"))
    available = {"powerpoint": powerpoint, "libreoffice": libreoffice}
    candidates = [backend] if backend != "auto" else (["powerpoint", "libreoffice"] if os.name == "nt" else ["libreoffice"])
    return {"requested": backend, "available": available, "ready": any(available.get(name, False) for name in candidates),
            "note": "只检查程序路径和 Windows 注册信息；实际可用性仍以真实渲染为准。"}
