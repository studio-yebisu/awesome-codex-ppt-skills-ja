from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
import venv
from pathlib import Path

BRAND_NAME = "SlideMuse"
LEGACY_SKILL_NAME = "image-ppt"

CLIENT_DIRS = {
    "codex": Path(".agents") / "skills",
    "claude": Path(".claude") / "skills",
    "opencode": Path(".config") / "opencode" / "skills",
}

RUNTIME_PATHS = (
    "slidemuse.py",
    "SKILL.md",
    "manifest.yaml",
    "requirements.txt",
    "scripts",
    "references",
    "agents",
    "examples",
)

OPTIONAL_RUNTIME_PATHS = ("showcase/editable-irena", "docs")
OPTIONAL_RUNTIME_FILES = ("README.md", "README.en.md", "CHANGELOG.md", "CONTRIBUTING.md", "LICENSE")


def read_skill_name(root: Path) -> str:
    text = (root / "SKILL.md").read_text(encoding="utf-8")
    match = re.search(
        r"^---\s*$.*?^name:\s*([A-Za-z0-9._-]+)\s*$",
        text,
        re.MULTILINE | re.DOTALL,
    )
    if not match:
        raise RuntimeError("Could not read skill name from SKILL.md frontmatter.")
    return match.group(1)


def detect_client(home: Path) -> str:
    candidates: list[str] = []
    if shutil.which("codex") or (home / ".codex").exists() or (home / ".agents").exists():
        candidates.append("codex")
    if shutil.which("claude") or (home / ".claude").exists():
        candidates.append("claude")
    if shutil.which("opencode") or (home / ".config" / "opencode").exists():
        candidates.append("opencode")

    if not candidates:
        return "codex"
    if len(candidates) == 1:
        return candidates[0]
    detected = ", ".join(candidates)
    raise RuntimeError(
        f"Multiple supported clients detected: {detected}. "
        "Re-run with --client codex, --client claude, or --client opencode."
    )


def venv_python(venv_dir: Path) -> Path:
    if os.name == "nt":
        return venv_dir / "Scripts" / "python.exe"
    return venv_dir / "bin" / "python"


def check_target(target: Path, force: bool) -> None:
    marker = target / ".skill-install.json"
    if target.is_symlink() or (target.exists() and not target.is_dir()):
        raise RuntimeError(f"{target} is not a regular skill directory.")
    if target.exists() and not marker.exists() and any(target.iterdir()) and not force:
        raise RuntimeError(
            f"{target} already exists and was not created by this installer. "
            "Use --force only if you intend to replace it."
        )


def copy_runtime(root: Path, target: Path) -> None:
    missing = [str(root / name) for name in RUNTIME_PATHS if not (root / name).exists()]
    if missing:
        raise RuntimeError(f"Missing runtime paths: {', '.join(missing)}")
    paths = (*RUNTIME_PATHS, *(name for name in OPTIONAL_RUNTIME_PATHS if (root / name).is_dir()),
             *(name for name in OPTIONAL_RUNTIME_FILES if (root / name).is_file()))
    for name in paths:
        source = root / name
        destination = target / name
        if source.is_dir():
            shutil.copytree(source, destination)
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)


def install_dependencies(target: Path, final_target: Path) -> Path:
    env_dir = target / ".venv"
    python = venv_python(env_dir)
    if not python.exists():
        venv.EnvBuilder(with_pip=True, clear=False).create(env_dir)
    subprocess.run(
        [
            str(python),
            "-m",
            "pip",
            "install",
            "--disable-pip-version-check",
            "-r",
            str(target / "requirements.txt"),
        ],
        check=True,
    )
    (target / ".skill-python").write_text(
        str(venv_python(final_target / ".venv")) + "\n",
        encoding="utf-8",
    )
    return python


def validate_install(target: Path, python: Path) -> None:
    subprocess.run(
        [
            str(python),
            str(target / "scripts" / "validate_page_spec.py"),
            str(target / "examples" / "page-spec.example.json"),
            "--strict",
        ],
        check=True,
    )


def retryable_replace_error(exc: OSError) -> bool:
    return os.name == "nt" and getattr(exc, "winerror", None) in (5, 32, 33)


def replace_directory(source: Path, destination: Path) -> None:
    """Allow Windows a moment to release a newly used virtual environment."""
    delays = (0, 0.25, 0.5, 1, 2, 4)
    for attempt, delay in enumerate(delays):
        if delay:
            time.sleep(delay)
        try:
            source.replace(destination)
            return
        except OSError as exc:
            if attempt == len(delays) - 1 or not retryable_replace_error(exc):
                raise


def legacy_installs(home: Path, client: str, skill_name: str) -> list[Path]:
    if skill_name == LEGACY_SKILL_NAME:
        return []
    parents = [home / CLIENT_DIRS[client]]
    if client == "codex":
        parents.append(home / ".codex" / "skills")
    return [parent / LEGACY_SKILL_NAME for parent in parents if (parent / LEGACY_SKILL_NAME).exists()]


def install_skill(
    root: Path, target: Path, client: str, skill_name: str, force: bool, skip_deps: bool
) -> Path:
    check_target(target, force)
    target.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=f".{target.name}-stage-", dir=target.parent))
    backup: Path | None = None
    activated = False
    try:
        copy_runtime(root, staging)
        python = Path(sys.executable)
        if not skip_deps:
            python = install_dependencies(staging, target)

        marker = {
            "installer": "slidemuse",
            "brand": BRAND_NAME,
            "skill": skill_name,
            "client": client,
            "source": str(root),
        }
        (staging / ".skill-install.json").write_text(
            json.dumps(marker, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        if not skip_deps:
            validate_install(staging, python)

        if target.exists():
            backup = target.with_name(f".{target.name}-backup-{uuid.uuid4().hex}")
            replace_directory(target, backup)
        replace_directory(staging, target)
        activated = True

        final_python = venv_python(target / ".venv") if not skip_deps else python
        if not skip_deps:
            validate_install(target, final_python)
    except BaseException:
        failed: Path | None = None
        if activated:
            failed = target.with_name(f".{target.name}-failed-{uuid.uuid4().hex}")
            replace_directory(target, failed)
        if backup is not None and backup.exists():
            replace_directory(backup, target)
        if failed is not None:
            shutil.rmtree(failed)
        raise
    finally:
        if staging.exists():
            shutil.rmtree(staging)

    if backup is not None:
        try:
            shutil.rmtree(backup)
        except OSError as exc:
            print(f"install: warning: could not remove old backup {backup}: {exc}", file=sys.stderr)
    return final_python


def emit(result: dict[str, object], as_json: bool) -> None:
    if as_json:
        print(json.dumps(result, ensure_ascii=False))
        return

    if result.get("dry_run"):
        print(f"{BRAND_NAME} installer dry run")
    else:
        print(f"[OK] {BRAND_NAME} installed successfully")
    print(f"  Client: {result['client']}")
    print(f"  Skill:  ${result['skill']}")
    print(f"  Path:   {result['target']}")
    if result.get("python"):
        print(f"  Python: {result['python']}")
    for legacy in result.get("legacy_targets", []):
        print(
            f"  Note: legacy install found at {legacy}. "
            "You can remove it after confirming $slidemuse works."
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Install SlideMuse and its isolated Python runtime."
    )
    parser.add_argument(
        "--client",
        choices=("auto", "codex", "claude", "opencode"),
        default="auto",
        help="Target agent client. Defaults to automatic detection.",
    )
    parser.add_argument(
        "--home",
        type=Path,
        default=Path.home(),
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--skip-deps",
        action="store_true",
        help="Register the skill without creating its isolated Python environment.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace an existing unrecognized skill directory.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show the selected client and target path without changing files.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON output.",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parent
    skill_name = read_skill_name(root)
    try:
        client = detect_client(args.home) if args.client == "auto" else args.client
    except RuntimeError as exc:
        parser.exit(2, f"install: error: {exc}\n")
    target = args.home / CLIENT_DIRS[client] / skill_name
    legacy = legacy_installs(args.home, client, skill_name)

    result: dict[str, object] = {
        "ok": True,
        "client": client,
        "skill": skill_name,
        "target": str(target),
    }
    if legacy:
        result["legacy_targets"] = [str(path) for path in legacy]
        result["legacy_target"] = str(legacy[0])

    if args.dry_run:
        result["dry_run"] = True
        emit(result, args.json)
        return

    try:
        python = install_skill(root, target, client, skill_name, args.force, args.skip_deps)
    except (OSError, RuntimeError, subprocess.CalledProcessError) as exc:
        parser.exit(2, f"install: error: {exc}\n")

    result["python"] = str(python)
    result["verified"] = not args.skip_deps
    emit(result, args.json)


if __name__ == "__main__":
    main()
