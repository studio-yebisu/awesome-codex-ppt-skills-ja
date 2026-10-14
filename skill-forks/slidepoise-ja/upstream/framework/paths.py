from __future__ import annotations

import os
from pathlib import Path


FRAMEWORK_ROOT = Path(__file__).resolve().parent
REPOSITORY_ROOT = FRAMEWORK_ROOT.parent
BUNDLED_ROOT = FRAMEWORK_ROOT / "_bundled"
BUNDLED_PROFILES_ROOT = REPOSITORY_ROOT / "profiles" if (REPOSITORY_ROOT / "profiles").is_dir() else BUNDLED_ROOT / "profiles"
BUNDLED_LIBRARY_SETS_ROOT = REPOSITORY_ROOT / "library-sets" if (REPOSITORY_ROOT / "library-sets").is_dir() else BUNDLED_ROOT / "library-sets"
SKILL_ROOT = REPOSITORY_ROOT / "slidepoise" if (REPOSITORY_ROOT / "slidepoise" / "SKILL.md").is_file() else BUNDLED_ROOT / "slidepoise"
DEFAULT_CONFIG = FRAMEWORK_ROOT / "defaults" / "slidepoise-config.json"
SESSION_TEMPLATE = FRAMEWORK_ROOT / "templates" / "session-overrides-template.json"
NODE_RUNTIME_PACKAGE = FRAMEWORK_ROOT / "node-runtime-package.json"


def data_home() -> Path:
    override = os.environ.get("SLIDEPOISE_HOME")
    return Path(override).expanduser().resolve() if override else (Path.home() / ".slidepoise").resolve()


def installed_profiles_root() -> Path:
    return data_home() / "profiles"


def installed_library_sets_root() -> Path:
    return data_home() / "library-sets"


def active_library_sets_root() -> Path:
    installed = installed_library_sets_root()
    return installed if (installed / "catalog.json").is_file() else BUNDLED_LIBRARY_SETS_ROOT


def active_profiles_root() -> Path:
    installed = installed_profiles_root()
    return installed if installed.is_dir() and any(installed.glob("*/profile.json")) else BUNDLED_PROFILES_ROOT


def settings_path() -> Path:
    return data_home() / "settings.json"


def workspace_root() -> Path:
    return data_home() / "workspace"


def node_runtime_root() -> Path:
    return data_home() / "node"
