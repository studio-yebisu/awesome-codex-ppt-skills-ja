"""One-time name migration. Historical run evidence stays byte-for-byte intact."""
from __future__ import annotations

import json
import os
import shutil
from pathlib import Path


def _refresh_config_labels(home: Path) -> None:
    """Update product-owned labels without touching user settings or run evidence."""
    path = home / "config.json"
    if not path.is_file():
        return
    payload = json.loads(path.read_text(encoding="utf-8"))
    original = json.dumps(payload, sort_keys=True)
    metadata = payload.get("self_update", {})
    for key in ("config_location", "profiles_location", "manifest_location"):
        value = metadata.get(key)
        if isinstance(value, str):
            metadata[key] = value.replace("$SLIDECRAFT_HOME", "$SLIDEPOISE_HOME")
    def replace_labels(value):
        if isinstance(value, dict):
            return {key: replace_labels(item) for key, item in value.items()}
        if isinstance(value, list):
            return [replace_labels(item) for item in value]
        if isinstance(value, str):
            return value.replace("Slidecraft orchestration", "SlidePoise orchestration")
        return value
    payload = replace_labels(payload)
    if json.dumps(payload, sort_keys=True) != original:
        backup = home / "archive" / "name-migration" / "config.json"
        backup.parent.mkdir(parents=True, exist_ok=True)
        if not backup.exists():
            shutil.copy2(path, backup)
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def migrate_legacy_home() -> dict[str, object]:
    # An explicit data directory is owned by the user and is never relocated.
    if os.environ.get("SLIDEPOISE_HOME"):
        return {"migrated": False, "reason": "explicit_home"}
    if os.environ.get("SLIDECRAFT_HOME"):
        raise RuntimeError("Replace SLIDECRAFT_HOME with SLIDEPOISE_HOME before setup. Custom data is not moved automatically.")
    legacy = Path.home() / ".slidecraft"
    target = Path.home() / ".slidepoise"
    if legacy.is_symlink():
        if legacy.resolve() == target.resolve() and target.is_dir():
            _refresh_config_labels(target)
            return {"migrated": False, "reason": "already_migrated", "compatibility_path": str(legacy)}
        raise RuntimeError(f"Unexpected legacy symlink at {legacy}. Resolve it before setup.")
    if not legacy.exists():
        return {"migrated": False, "reason": "fresh_install"}
    if not legacy.is_dir() or target.exists() or target.is_symlink():
        raise RuntimeError(f"Cannot safely migrate {legacy} to {target}. Both locations must be inspected before merging data.")
    shutil.move(str(legacy), str(target))
    try:
        # Old run JSON and virtualenv launchers can contain absolute legacy paths.
        # Keeping this alias avoids rewriting signed or hash-bound evidence.
        legacy.symlink_to(target, target_is_directory=True)
    except OSError:
        shutil.move(str(target), str(legacy))
        raise
    _refresh_config_labels(target)
    return {"migrated": True, "home": str(target), "compatibility_path": str(legacy)}


if __name__ == "__main__":
    print(json.dumps(migrate_legacy_home(), indent=2))
