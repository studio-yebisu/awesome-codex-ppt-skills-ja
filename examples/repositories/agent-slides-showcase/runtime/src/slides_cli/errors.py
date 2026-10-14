from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class SlidesError(Exception):
    """Structured error designed for machine handling by agent workflows."""

    code: str
    message: str
    path: str | None = None
    suggested_fix: str | None = None

    def __str__(self) -> str:
        suffix = []
        if self.path:
            suffix.append(f"path={self.path}")
        if self.suggested_fix:
            suffix.append(f"suggested_fix={self.suggested_fix}")
        extra = f" ({', '.join(suffix)})" if suffix else ""
        return f"[{self.code}] {self.message}{extra}"
