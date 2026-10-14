"""Shared, portable slide-run records. No workflow or visual acceptance decisions."""
from __future__ import annotations

import re
import subprocess
import sys
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path

from .paths import DEFAULT_CONFIG, SKILL_ROOT, active_profiles_root, data_home, workspace_root
from .profiles import canonical_profile_id, active_profile_id, list_profiles
from .storage import ConflictError, locked, read, revision, update, write


def now():
    return datetime.now(timezone.utc).isoformat()


def registry_path():
    return workspace_root() / "runs.json"


def metadata_path(root):
    return Path(root) / "session.json"


def require_run(root):
    root = Path(root).expanduser().resolve()
    if not metadata_path(root).is_file() and not (root / "work/human-approvals.json").is_file():
        raise FileNotFoundError(f"No SlidePoise session at {root}")
    return root


def snapshot():
    config = read(data_home() / "config.json", read(DEFAULT_CONFIG))
    return {"captured_at": now(), "base_config": config, "active_profile": active_profile_id(),
            "profiles_root": str(active_profiles_root()),
            "profiles": {p["id"]: read(Path(p["path"])) for p in list_profiles()}}


def register(root, registry_file=None):
    root = require_run(root)
    meta = read(metadata_path(root), {})
    if not meta:
        meta = {"id": str(uuid.uuid4()), "name": root.name, "state": "active", "requirements": "", "created_at": now()}
        write(metadata_path(root), meta)
    def change(items):
        same_id = [item for item in items if item.get("id") == meta["id"] and item["path"] != str(root)]
        if any(Path(item["path"]).is_dir() for item in same_id):
            raise ConflictError("This is a copy of an available session. Keep the original or create a separate run.")
        items = [item for item in items if item.get("id") != meta["id"] and item["path"] != str(root)]
        return items + [{"id": meta["id"], "name": meta["name"], "path": str(root)}]
    update(Path(registry_file) if registry_file else registry_path(), change, default=[])
    return str(root)


def create(name, location=None, profile=None, *, workspace=None, registry_file=None):
    slug = re.sub(r"[^a-zA-Z0-9._-]+", "-", name).strip("-.").lower() or "slide-run"
    root = Path(location).expanduser().resolve() if location else Path(workspace or workspace_root()) / "runs" / f"{slug}-{uuid.uuid4().hex[:6]}"
    if root.exists() and any(root.iterdir()):
        raise ValueError("Choose an empty dedicated folder, or ask the Agent to continue an existing run.")
    frozen = snapshot()
    selected = canonical_profile_id(profile or frozen["active_profile"])
    if selected not in frozen["profiles"]:
        raise ValueError("Unknown guidance profile")
    for folder in ("work", "work/reviews", "slides", "deliverables", "uploads"):
        (root / folder).mkdir(parents=True, exist_ok=True)
    write(root / "work/session-defaults.json", frozen)
    write(root / "session-overrides.json", {"profile": selected})
    outline = read(SKILL_ROOT / "schemas/deck-outline.example.json")
    outline.update({"deck_id": slug, "title": name.strip() or root.name})
    outline["slides"] = []
    write(root / "work/deck-outline.json", outline)
    write(metadata_path(root), {"id": str(uuid.uuid4()), "name": name.strip() or root.name,
                              "state": "active", "requirements": "", "created_at": now()})
    register(root, registry_file)
    return root


def resolve(root, overrides=None):
    root = require_run(root)
    # A temporary session in the same folder lets the resolver see its frozen defaults.
    session = root / "session-overrides.json"
    with tempfile.TemporaryDirectory(prefix="slidepoise-resolve-") as temporary:
        temp = Path(temporary)
        if overrides is not None:
            write(temp / "session-overrides.json", overrides)
            frozen = read(root / "work/session-defaults.json")
            if frozen:
                write(temp / "work/session-defaults.json", frozen)
            session = temp / "session-overrides.json"
        config = data_home() / "config.json"
        result = subprocess.run([sys.executable, str(SKILL_ROOT / "scripts/resolve_config.py"),
                                 "--base", str(config if config.is_file() else DEFAULT_CONFIG),
                                 "--profiles-root", str(active_profiles_root()), "--session", str(session),
                                 "--output", str(temp / "resolved.json")], capture_output=True, text=True)
        if result.returncode:
            raise ValueError((result.stderr or result.stdout).strip())
        return read(temp / "resolved.json")


def save_overrides(root, value, expected):
    root = require_run(root)
    resolve(root, value)  # Structural validation before replacing the working settings.
    update(root / "session-overrides.json", lambda _: value, expected=expected, default={})
    from . import run_events
    run_events.record(root, "session_setting_applied", "Presentation settings changed", {"overrides": value})


def patchmetadata(root, values, expected):
    root = require_run(root)
    if set(values) - {"name", "requirements", "state"}:
        raise ValueError("Unsupported session field")
    if "state" in values and values["state"] not in {"active", "completed", "hidden"}:
        raise ValueError("Unknown session state")
    if any(not isinstance(value, str) for value in values.values()):
        raise ValueError("Session fields must be text")
    update(metadata_path(root), lambda old: {**old, **values, "updated_at": now()}, expected=expected, default={})
    from . import run_events
    run_events.record(root, "requirements_changed", "Presentation details changed", {"values": values})


def adopt_defaults(root, expected):
    root = require_run(root)
    path = root / "work/session-defaults.json"
    frozen = snapshot()
    overrides = read(root / "session-overrides.json", {})
    if overrides.get("profile") not in frozen["profiles"]:
        raise ValueError("The session profile is no longer installed. Keep its captured defaults.")
    with locked(path):
        if expected != revision(path):
            raise ConflictError("Session defaults changed. Reload before updating.")
        previous = read(path)
        if previous:
            write(root / "work/defaults-history" / f"{uuid.uuid4().hex}.json", previous)
        write(path, frozen)
    from . import run_events
    run_events.record(root, "defaults_updated", "Presentation profile updated")


def list_runs(registry_file=None):
    result = []
    for entry in read(Path(registry_file) if registry_file else registry_path(), []):
        root = Path(entry["path"])
        meta = read(metadata_path(root), {})
        available = root.is_dir() and (metadata_path(root).is_file() or (root / "work/human-approvals.json").is_file())
        result.append({**entry, **meta, "available": available,
                       "state": meta.get("state", "active") if available else "missing"})
    return result
