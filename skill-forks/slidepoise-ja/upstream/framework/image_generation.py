"""Shared Agent and Console preferences for image generation."""
import sys

from .paths import DEFAULT_CONFIG, SKILL_ROOT, data_home
from .storage import locked, read, revision, update

sys.path.insert(0, str(SKILL_ROOT / "runtime/src"))
from slidepoise.generation import resolve_preferences


def payload():
    path = data_home() / "config.json"
    with locked(path):
        config = read(path, read(DEFAULT_CONFIG))
        return {"values": resolve_preferences(config.get("generation", {})), "revision": revision(path)}


def configure(values, expected):
    path = data_home() / "config.json"
    def change(config):
        generation = config.setdefault("generation", {})
        generation["preferences"] = resolve_preferences(generation, values)
        return config
    update(path, change, expected=expected, default=read(DEFAULT_CONFIG))
    return payload()
