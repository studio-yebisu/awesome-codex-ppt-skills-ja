#!/usr/bin/env python3
"""Synchronize the canonical Paper2PPT Skill into its plugin package."""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import sys


PLUGIN_SKILL = Path("plugins/paper2ppt/skills/paper2ppt")
RUNTIME_HELPERS = ("preflight.py", "inspect_pptx.py")


class SyncSafetyError(RuntimeError):
    """Raised when a managed path could escape the repository or plugin root."""


def _display_path(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def _require_contained(path: Path, boundary: Path, root: Path, kind: str) -> None:
    resolved_path = path.resolve(strict=False)
    resolved_boundary = boundary.resolve(strict=False)
    if resolved_path != resolved_boundary and not resolved_path.is_relative_to(
        resolved_boundary
    ):
        raise SyncSafetyError(
            f"unsafe {kind} path escapes its root: {_display_path(path, root)}"
        )


def _reject_symlink_components(
    path: Path, boundary: Path, root: Path, kind: str
) -> None:
    try:
        relative = path.relative_to(boundary)
    except ValueError as error:
        raise SyncSafetyError(
            f"unsafe {kind} path escapes its root: {_display_path(path, root)}"
        ) from error

    current = boundary
    for part in relative.parts:
        current /= part
        if current.is_symlink():
            raise SyncSafetyError(
                f"unsafe symlink in {kind} path: {_display_path(current, root)}"
            )


def _validate_path(path: Path, boundary: Path, root: Path, kind: str) -> None:
    _reject_symlink_components(path, boundary, root, kind)
    _require_contained(path, boundary, root, kind)


def _validate_directory_chain(
    directory: Path, boundary: Path, root: Path, kind: str
) -> None:
    _validate_path(directory, boundary, root, kind)
    current = boundary
    for part in directory.relative_to(boundary).parts:
        current /= part
        if current.exists() and not current.is_dir():
            raise SyncSafetyError(
                f"unsafe non-directory in {kind} path: {_display_path(current, root)}"
            )


def _desired_files(root: Path) -> dict[Path, tuple[Path, Path]]:
    target = root / PLUGIN_SKILL
    canonical_skill = root / "SKILL.md"
    _validate_path(canonical_skill, root, root, "canonical")
    desired = {target / "SKILL.md": (canonical_skill, root)}

    references = root / "references"
    _validate_directory_chain(references, root, root, "canonical")
    if references.is_dir():
        for source in sorted(references.rglob("*")):
            _validate_path(source, references, root, "canonical")
            if source.is_file():
                destination = target / "references" / source.relative_to(references)
                desired[destination] = (source, references)

    scripts = root / "scripts"
    _validate_directory_chain(scripts, root, root, "canonical")
    for name in RUNTIME_HELPERS:
        source = scripts / name
        _validate_path(source, scripts, root, "canonical")
        if source.is_file():
            desired[target / "scripts" / name] = (source, scripts)

    return desired


def _validate_packaged_tree(
    root: Path, desired: dict[Path, tuple[Path, Path]]
) -> Path:
    target = root / PLUGIN_SKILL
    _validate_directory_chain(target, root, root, "packaged")

    for managed in (target / "references", target / "scripts"):
        _validate_path(managed, target, root, "packaged")
        if managed.exists() and not managed.is_dir():
            raise SyncSafetyError(
                f"unsafe non-directory in packaged path: {_display_path(managed, root)}"
            )
        if managed.is_dir():
            for path in sorted(managed.rglob("*")):
                _validate_path(path, target, root, "packaged")

    for destination in desired:
        _validate_directory_chain(destination.parent, target, root, "packaged")
        _validate_path(destination, target, root, "packaged")
        if destination.exists() and not destination.is_file():
            raise SyncSafetyError(
                "unsafe non-file destination in packaged path: "
                f"{_display_path(destination, root)}"
            )

    return target


def _stale_files(
    root: Path, target: Path, desired: dict[Path, tuple[Path, Path]]
) -> list[Path]:
    desired_paths = set(desired)
    stale: list[Path] = []
    for directory in (target / "references", target / "scripts"):
        if directory.is_dir():
            for path in directory.rglob("*"):
                _validate_path(path, target, root, "packaged")
                if path.is_file() and path not in desired_paths:
                    stale.append(path)
    return sorted(stale)


def sync(root: Path, *, check: bool = False) -> list[str]:
    """Return drift actions and, unless checking, synchronize managed files."""
    root = root.resolve()
    desired = _desired_files(root)
    target = _validate_packaged_tree(root, desired)
    stale_files = _stale_files(root, target, desired)
    changes: list[str] = []
    updates: list[Path] = []

    for destination, (source, source_boundary) in desired.items():
        _validate_path(source, source_boundary, root, "canonical")
        _validate_path(destination, target, root, "packaged")
        if not destination.is_file() or destination.read_bytes() != source.read_bytes():
            changes.append(f"update:{destination.relative_to(root)}")
            updates.append(destination)

    for stale in stale_files:
        changes.append(f"remove:{stale.relative_to(root)}")

    if not check:
        for destination in updates:
            source, source_boundary = desired[destination]
            _validate_path(source, source_boundary, root, "canonical")
            _validate_path(destination, target, root, "packaged")
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)

        for stale in stale_files:
            _validate_path(stale, target, root, "packaged")
            stale.unlink()

        for managed in (target / "references", target / "scripts"):
            if managed.is_dir():
                for directory in sorted(
                    (path for path in managed.rglob("*") if path.is_dir()),
                    key=lambda path: len(path.parts),
                    reverse=True,
                ):
                    _validate_path(directory, target, root, "packaged")
                    if not any(directory.iterdir()):
                        directory.rmdir()
                _validate_path(managed, target, root, "packaged")
                if not any(managed.iterdir()):
                    managed.rmdir()

    return changes


def main(argv: list[str] | None = None, *, root: Path | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Synchronize the canonical Paper2PPT Skill into the plugin package."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Report drift without modifying files.",
    )
    args = parser.parse_args(argv)
    sync_root = root if root is not None else Path(__file__).resolve().parents[1]
    try:
        changes = sync(sync_root, check=args.check)
    except SyncSafetyError as error:
        print(f"Paper2PPT sync error: {error}", file=sys.stderr)
        return 2

    if args.check and changes:
        for change in changes:
            print(change)
        return 1
    if changes:
        for change in changes:
            print(change)
    else:
        print("Paper2PPT plugin mirror is synchronized.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
