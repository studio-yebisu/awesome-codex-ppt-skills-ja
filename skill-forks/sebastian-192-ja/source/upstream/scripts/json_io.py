"""One UTF-8 JSON reader for user inputs, including Windows UTF-8 BOM files."""
from __future__ import annotations

import json
from pathlib import Path


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))
