from pathlib import Path
import re

import yaml


def load_skill(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    assert match, f"Missing YAML frontmatter: {path}"
    return yaml.safe_load(match.group(1)), text[match.end():]
