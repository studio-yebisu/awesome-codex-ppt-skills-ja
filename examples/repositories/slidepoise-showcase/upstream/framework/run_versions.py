"""Preserve a complete presentation snapshot before a host-authored revision."""
from __future__ import annotations

import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from .sessions import require_run


def archive(root):
    root = require_run(root)
    name = "iteration-" + datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S-%f")
    history = root / "history"
    history.mkdir(parents=True, exist_ok=True)
    target = history / name
    with tempfile.TemporaryDirectory(prefix=".snapshot-", dir=history) as temporary:
        staged = Path(temporary) / "snapshot"
        staged.mkdir()
        for folder in ("work", "deliverables", "uploads", "slides"):
            if (root / folder).is_dir():
                shutil.copytree(root / folder, staged / folder)
        for filename in ("accepted-slide.png", "session.json", "session-overrides.json"):
            if (root / filename).is_file():
                shutil.copy2(root / filename, staged / filename)
        staged.rename(target)
    return {"id": name, "path": str(target)}
