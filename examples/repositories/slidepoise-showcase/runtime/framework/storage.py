"""Atomic local JSON updates with optimistic revisions shared by CLI and Console."""
from __future__ import annotations

import hashlib
import json
import os
import tempfile
from contextlib import contextmanager
from pathlib import Path


class ConflictError(ValueError):
    pass


def revision(path: Path) -> str:
    return hashlib.sha256(path.read_bytes() if path.exists() else b"").hexdigest()


def read(path: Path, default=None):
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else default


def write(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
            temporary = Path(handle.name)
            json.dump(value, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        temporary.replace(path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


@contextmanager
def locked(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.with_name(path.name + ".lock").open("a+b") as handle:
        if os.name == "nt":
            import msvcrt
            handle.seek(0)
            handle.write(b"0")
            handle.flush()
            handle.seek(0)
            msvcrt.locking(handle.fileno(), msvcrt.LK_LOCK, 1)
        else:
            import fcntl
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            if os.name == "nt":
                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def update(path: Path, change, *, expected: str | None = None, default=None):
    with locked(path):
        if expected is not None and expected != revision(path):
            raise ConflictError("Changed in another window or Agent. Reload before saving your changes.")
        value = change(read(path, default))
        write(path, value)
        return value
