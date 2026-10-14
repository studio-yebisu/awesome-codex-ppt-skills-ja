#!/usr/bin/env python3
"""Small shared helpers for PradaSlides validation scripts."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable


@dataclass(frozen=True)
class Diagnostic:
    severity: str
    code: str
    message: str
    location: str = ""


def load_json(path: str | Path) -> Any:
    source = Path(path)
    try:
        return json.loads(source.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"File not found: {source}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Invalid JSON in {source} at line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc


def write_json(path: str | Path, payload: Any) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def emit_report(
    name: str,
    diagnostics: Iterable[Diagnostic],
    *,
    json_output: str | Path | None = None,
    extra: dict[str, Any] | None = None,
) -> int:
    items = list(diagnostics)
    counts = {
        severity: sum(item.severity == severity for item in items)
        for severity in ("error", "warning", "info")
    }
    status = "failed" if counts["error"] else "passed"
    payload: dict[str, Any] = {
        "name": name,
        "status": status,
        "counts": counts,
        "diagnostics": [asdict(item) for item in items],
    }
    if extra:
        payload.update(extra)

    if json_output:
        write_json(json_output, payload)

    print(f"{name}: {status} ({counts['error']} errors, {counts['warning']} warnings)")
    for item in items:
        location = f" [{item.location}]" if item.location else ""
        print(f"{item.severity.upper():7} {item.code}{location}: {item.message}")
    return 1 if counts["error"] else 0
