"""Resolve a real preview of a native component without making design choices."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


def ensure_preview(source: Path, preview: Path, slide_number: int = 1) -> Path:
    if source.suffix.lower() != ".pptx":
        if not preview.is_file():
            raise ValueError("Component preview is missing")
        return preview
    binding = preview.with_suffix(preview.suffix + ".source.json")
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    expected = {"source_sha256": digest, "slide_number": slide_number}
    if preview.is_file():
        try:
            recorded = json.loads(binding.read_text()) if binding.is_file() else {}
        except (ValueError, OSError):
            recorded = {}
        if all(recorded.get(key) == value for key, value in expected.items()) and recorded.get("preview_sha256") == hashlib.sha256(preview.read_bytes()).hexdigest():
            return preview
    command = [sys.executable, str(Path(__file__).with_name("slidepoise_runtime.py")),
               "render-preview", "--pptx", str(source), "--output", str(preview),
               "--slide-number", str(slide_number)]
    result = subprocess.run(command, capture_output=True, text=True, timeout=180)
    if result.returncode:
        raise ValueError("This component needs a preview of its selected PowerPoint page. "
                         "Install LibreOffice and Poppler, or provide a host-rendered preview. " + result.stderr.strip())
    if hashlib.sha256(source.read_bytes()).hexdigest() != digest:
        raise ValueError("The component changed during preview rendering. Retry with its latest source.")
    expected["preview_sha256"] = hashlib.sha256(preview.read_bytes()).hexdigest()
    binding.write_text(json.dumps(expected) + "\n")
    return preview
