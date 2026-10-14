"""Conversation-local panel selection, shared by the browser and host Agent."""
from __future__ import annotations

import re
import uuid

from .paths import data_home
from .sessions import require_run
from .storage import locked, read, revision, write


def binding_path(panel_id):
    if not re.fullmatch(r"[a-zA-Z0-9_-]{1,80}", panel_id):
        raise ValueError("Invalid panel identifier")
    return data_home() / "panels" / f"{panel_id}.json"


def get(panel_id):
    path = binding_path(panel_id)
    with locked(path):
        value = read(path)
        if value is None:
            raise FileNotFoundError("Panel not found")
        return {**value, "revision": revision(path)}


def ensure(panel_id=None, run=None, host_thread_id=None):
    """Create or rebind an Agent-owned panel. Omitted run preserves an existing binding."""
    panel_id = panel_id or uuid.uuid4().hex
    path = binding_path(panel_id)
    root = str(require_run(run)) if run else None
    with locked(path):
        value = read(path)
        if value is None and root is None:
            raise FileNotFoundError("Panel not found")
        value = value or {"id": panel_id, "run": root}
        if root is not None:
            value["run"] = root
        if host_thread_id:
            value["host_thread_id"] = host_thread_id
        write(path, value)
        return {**value, "revision": revision(path)}
