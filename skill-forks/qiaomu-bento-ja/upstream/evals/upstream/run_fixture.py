#!/usr/bin/env python3
"""Exercise upstream refresh and rollback without network access."""

from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "sync_upstream.py"
DOC_CLOSE = "</scr" + "ipt>"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def run(root: Path, source: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            "python3",
            "-B",
            str(SCRIPT),
            "--root",
            str(root),
            "--source-dir",
            str(source),
            "--update",
        ],
        check=False,
        capture_output=True,
        text=True,
    )


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="qiaomu-bento-upstream-") as temporary:
        base = Path(temporary)
        skill = base / "skill"
        source = base / "source"
        write(
            source / "metadata.json",
            json.dumps(
                {
                    "tag": "v9.9.9",
                    "commit": "a" * 40,
                    "published_at": "2026-07-27T00:00:00Z",
                }
            ),
        )
        write(
            source / "release" / "Bento_Slides.bento.html",
            '<!doctype html><script type="application/bento+json" id="bento-doc">'
            '{"format":"bento/slides","version":1,"docId":"fixture"}'
            + DOC_CLOSE,
        )
        write(
            source / "repository" / "plugins/bento-slides/skills/bento-slides/SKILL.md",
            "---\nname: bento-slides\ndescription: fixture\n---\n# Fixture\n",
        )
        write(source / "repository" / "docs/agents.md", "# Agents\n\nbento/slides uses #bento-doc.\n")
        write(source / "repository" / "docs/format.md", "# Format\n\nbento/slides keeps docId stable.\n")
        first = run(skill, source)
        first_payload = json.loads(first.stdout) if first.stdout else {}
        lock = json.loads((skill / "upstream.lock.json").read_text(encoding="utf-8"))
        tracked = [skill / item for item in lock["files"]]
        before = {str(path): digest(path) for path in tracked}
        second = run(skill, source)
        second_payload = json.loads(second.stdout) if second.stdout else {}

        write(source / "metadata.json", json.dumps({"tag": "v9.9.10", "commit": "b" * 40}))
        write(source / "release" / "Bento_Slides.bento.html", "not an html shell")
        failed = run(skill, source)
        after = {str(path): digest(path) for path in tracked}
        checks = {
            "first_update_succeeded": first.returncode == 0 and first_payload.get("updated") is True,
            "lock_created": lock.get("release", {}).get("tag") == "v9.9.9",
            "notice_created": (skill / "NOTICE.md").is_file(),
            "second_update_is_noop": second.returncode == 0 and second_payload.get("updated") is False,
            "invalid_bundle_rejected": failed.returncode != 0,
            "rollback_preserved_snapshot": before == after,
        }
        report = {
            "ok": all(checks.values()),
            "file-backed fixture": "temporary offline upstream release mirror",
            "input_files": ["release shell", "official skill", "docs/agents.md", "docs/format.md"],
            "output contract": ["upstream.lock.json", "NOTICE.md", "validated pinned assets"],
            "rollback boundary": "invalid staged release leaves every previously pinned file unchanged",
            "checks": checks,
        }
        print(json.dumps(report, ensure_ascii=False, indent=2))
        if not report["ok"]:
            raise SystemExit(2)


if __name__ == "__main__":
    main()
