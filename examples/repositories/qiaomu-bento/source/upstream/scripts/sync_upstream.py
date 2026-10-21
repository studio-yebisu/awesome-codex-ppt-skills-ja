#!/usr/bin/env python3
"""Check or refresh pinned assets from an official nyblnet/bento release.

Normal deck generation remains fully offline. This maintenance command stages
every upstream file, validates the complete set, and only then replaces the
local snapshot. A failed validation leaves the installed snapshot untouched.
"""

from __future__ import annotations

import argparse
import hashlib
import http.client
import json
import os
import re
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_REPO = "nyblnet/bento"
USER_AGENT = "qiaomu-bento-ppt-upstream-sync/1"
LOCK_NAME = "upstream.lock.json"
NOTICE_NAME = "NOTICE.md"
SOURCES = (
    {
        "target": "assets/bento/Bento_Slides.bento.html",
        "kind": "release",
        "source": "Bento_Slides.bento.html",
    },
    {
        "target": "references/upstream/bento-official-skill.md",
        "kind": "repository",
        "source": "plugins/bento-slides/skills/bento-slides/SKILL.md",
    },
    {
        "target": "references/upstream/bento-agents.md",
        "kind": "repository",
        "source": "docs/agents.md",
    },
    {
        "target": "references/upstream/bento-format.md",
        "kind": "repository",
        "source": "docs/format.md",
    },
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"expected a JSON object: {path}")
    return payload


def local_release_tag(root: Path, lock: dict[str, Any]) -> str | None:
    locked = lock.get("release", {}).get("tag") if lock else None
    if isinstance(locked, str) and locked:
        return locked
    notice = root / NOTICE_NAME
    if not notice.is_file():
        return None
    text = notice.read_text(encoding="utf-8")
    match = re.search(r"- Upstream release: `([^`]+)`", text)
    if match:
        return match.group(1)
    legacy = re.search(r"- App version: `([^`]+)`", text)
    if legacy:
        value = legacy.group(1)
        return value if value.startswith("v") else f"v{value}"
    return None


class GitHubSource:
    def __init__(self, repository: str) -> None:
        self.repository = repository
        token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
        self.headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": USER_AGENT,
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if token:
            self.headers["Authorization"] = f"Bearer {token}"

    def request(self, url: str, *, binary: bool = False, expected_size: int | None = None) -> bytes:
        headers = dict(self.headers)
        if binary:
            headers["Accept"] = "application/octet-stream"
        last_error: Exception | None = None
        accumulated = bytearray()
        for attempt in range(5):
            attempt_headers = dict(headers)
            if accumulated:
                attempt_headers["Range"] = f"bytes={len(accumulated)}-"
            request = urllib.request.Request(url, headers=attempt_headers)
            response_status = 0
            try:
                with urllib.request.urlopen(request, timeout=45) as response:
                    response_status = getattr(response, "status", 200)
                    body = response.read()
                    if accumulated and response_status == 206:
                        accumulated.extend(body)
                    else:
                        accumulated = bytearray(body)
                    if expected_size is not None and len(accumulated) != expected_size:
                        last_error = RuntimeError(
                            f"short asset response: received {len(accumulated)} of {expected_size} bytes"
                        )
                    else:
                        return bytes(accumulated)
            except urllib.error.HTTPError as exc:
                last_error = exc
                if exc.code < 500 and exc.code != 429:
                    raise RuntimeError(f"upstream request failed ({exc.code}): {url}") from exc
            except http.client.IncompleteRead as exc:
                last_error = exc
                if accumulated and response_status == 206:
                    accumulated.extend(exc.partial)
                else:
                    accumulated = bytearray(exc.partial)
            except urllib.error.URLError as exc:
                last_error = exc
            if expected_size is not None and len(accumulated) == expected_size:
                return bytes(accumulated)
            if attempt < 4:
                time.sleep(min(2**attempt, 8))
        raise RuntimeError(
            f"upstream request failed after 5 attempts: {url}: {last_error}; "
            f"received {len(accumulated)} bytes"
        ) from last_error

    def api_json(self, path: str) -> dict[str, Any]:
        payload = json.loads(self.request(f"https://api.github.com/{path}"))
        if not isinstance(payload, dict):
            raise RuntimeError(f"unexpected GitHub API response for {path}")
        return payload

    def release(self, tag: str) -> dict[str, Any]:
        path = (
            f"repos/{self.repository}/releases/latest"
            if tag == "latest"
            else f"repos/{self.repository}/releases/tags/{urllib.parse.quote(tag, safe='')}"
        )
        return self.api_json(path)

    def commit_for_tag(self, tag: str) -> str:
        encoded = urllib.parse.quote(tag, safe="")
        obj = self.api_json(f"repos/{self.repository}/git/ref/tags/{encoded}").get("object", {})
        for _ in range(4):
            kind = obj.get("type")
            value = obj.get("sha")
            if kind == "commit" and isinstance(value, str):
                return value
            if kind == "tag" and isinstance(value, str):
                obj = self.api_json(f"repos/{self.repository}/git/tags/{value}").get("object", {})
                continue
            break
        raise RuntimeError(f"could not resolve release tag to a commit: {tag}")

    def bundle(self, requested_tag: str) -> tuple[dict[str, str], dict[str, bytes]]:
        release = self.release(requested_tag)
        tag = release.get("tag_name")
        if not isinstance(tag, str) or not tag:
            raise RuntimeError("GitHub release does not contain tag_name")
        assets = {
            item.get("name"): item
            for item in release.get("assets", [])
            if isinstance(item, dict)
        }
        result: dict[str, bytes] = {}
        for item in SOURCES:
            if item["kind"] == "release":
                asset = assets.get(item["source"])
                if not isinstance(asset, dict) or not isinstance(asset.get("browser_download_url"), str):
                    raise RuntimeError(f"release {tag} is missing asset: {item['source']}")
                size = asset.get("size")
                result[item["target"]] = self.request(
                    asset["browser_download_url"],
                    binary=True,
                    expected_size=size if isinstance(size, int) else None,
                )
            else:
                source = urllib.parse.quote(item["source"], safe="/")
                url = f"https://raw.githubusercontent.com/{self.repository}/{urllib.parse.quote(tag, safe='')}/{source}"
                result[item["target"]] = self.request(url, binary=True)
        return (
            {
                "tag": tag,
                "commit": self.commit_for_tag(tag),
                "published_at": str(release.get("published_at") or ""),
            },
            result,
        )


class DirectorySource:
    """Deterministic source used by the offline fixture eval."""

    def __init__(self, source_dir: Path) -> None:
        self.source_dir = source_dir.resolve()

    def bundle(self, requested_tag: str) -> tuple[dict[str, str], dict[str, bytes]]:
        metadata = load_json(self.source_dir / "metadata.json")
        tag = str(metadata.get("tag") or "")
        commit = str(metadata.get("commit") or "")
        if not tag or not re.fullmatch(r"[0-9a-f]{40}", commit):
            raise ValueError("fixture metadata needs tag and a 40-character lowercase commit")
        if requested_tag not in {"latest", tag}:
            raise ValueError(f"fixture contains {tag}, not requested {requested_tag}")
        result: dict[str, bytes] = {}
        for item in SOURCES:
            bucket = "release" if item["kind"] == "release" else "repository"
            path = self.source_dir / bucket / item["source"]
            if not path.is_file():
                raise ValueError(f"fixture source is missing: {path}")
            result[item["target"]] = path.read_bytes()
        return (
            {
                "tag": tag,
                "commit": commit,
                "published_at": str(metadata.get("published_at") or ""),
            },
            result,
        )


def validate_bundle(files: dict[str, bytes]) -> list[str]:
    errors: list[str] = []
    expected = {item["target"] for item in SOURCES}
    missing = sorted(expected - files.keys())
    if missing:
        errors.extend(f"missing staged file: {path}" for path in missing)
        return errors

    shell = files["assets/bento/Bento_Slides.bento.html"]
    if not shell.startswith(b"<!doctype html>") and not shell.startswith(b"<!DOCTYPE html>"):
        errors.append("release shell is not an HTML document")
    if shell.count(b'id="bento-doc"') != 1:
        errors.append("release shell must contain exactly one #bento-doc block")
    if b"bento/slides" not in shell:
        errors.append("release shell does not identify bento/slides")

    official = files["references/upstream/bento-official-skill.md"].decode("utf-8", "replace")
    if not official.startswith("---\n") or "name: bento-slides" not in official[:500]:
        errors.append("official skill snapshot has invalid frontmatter")
    agents = files["references/upstream/bento-agents.md"].decode("utf-8", "replace")
    if "bento/slides" not in agents or "#bento-doc" not in agents:
        errors.append("agent authoring guide does not describe bento/slides")
    format_guide = files["references/upstream/bento-format.md"].decode("utf-8", "replace")
    if "bento/slides" not in format_guide or "docId" not in format_guide:
        errors.append("format snapshot is missing bento/slides identity rules")
    return errors


def build_lock(repository: str, release: dict[str, str], files: dict[str, bytes]) -> dict[str, Any]:
    entries: dict[str, Any] = {}
    by_target = {item["target"]: item for item in SOURCES}
    for target in sorted(files):
        item = by_target[target]
        source = (
            f"release:{item['source']}"
            if item["kind"] == "release"
            else f"repository:{item['source']}"
        )
        entries[target] = {"source": source, "sha256": sha256(files[target]), "bytes": len(files[target])}
    return {
        "schema_version": 1,
        "repository": repository,
        "release": {
            "tag": release["tag"],
            "commit": release["commit"],
            "published_at": release.get("published_at", ""),
            "synced_at": utc_now(),
        },
        "files": entries,
    }


def render_notice(lock: dict[str, Any]) -> str:
    release = lock["release"]
    lines = [
        "# Third-party notices",
        "",
        "## bento/slides",
        "",
        "This skill bundles a pinned bento/slides shell and documentation snapshots so",
        "it can run without the original repository or a network connection.",
        "",
        f"- Upstream: https://github.com/{lock['repository']}",
        "- Upstream copyright: Copyright (c) 2026 The Bento authors",
        "- License: MIT",
        f"- Upstream release: `{release['tag']}`",
        f"- Upstream commit: `{release['commit']}`",
        f"- Last synchronized: `{release['synced_at']}`",
        "",
        "Bundled files and SHA-256:",
        "",
        "| File | Source | SHA-256 |",
        "|---|---|---|",
    ]
    for target, item in lock["files"].items():
        lines.append(f"| `{target}` | `{item['source']}` | `{item['sha256']}` |")
    lines.extend(
        [
            "",
            "The bundled HTML shell contains its own runtime notices. The upstream MIT",
            "license text is preserved in `THIRD_PARTY_LICENSES/bento-MIT.txt`.",
            "",
        ]
    )
    return "\n".join(lines)


def local_lock_errors(root: Path, lock: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if lock.get("repository") != DEFAULT_REPO:
        errors.append(f"lock repository must be {DEFAULT_REPO}")
    release = lock.get("release")
    if not isinstance(release, dict) or not release.get("tag") or not release.get("commit"):
        errors.append("lock release metadata is incomplete")
    entries = lock.get("files")
    if not isinstance(entries, dict):
        return errors + ["lock files must be an object"]
    for item in SOURCES:
        target = item["target"]
        spec = entries.get(target)
        path = root / target
        if not isinstance(spec, dict):
            errors.append(f"lock missing file: {target}")
            continue
        if not path.is_file():
            errors.append(f"bundled file missing: {target}")
            continue
        data = path.read_bytes()
        if sha256(data) != spec.get("sha256"):
            errors.append(f"bundled file checksum mismatch: {target}")
        if len(data) != spec.get("bytes"):
            errors.append(f"bundled file size mismatch: {target}")
    return errors


def replace_transaction(root: Path, payloads: dict[str, bytes]) -> None:
    backups: dict[Path, bytes | None] = {}
    staged: dict[Path, Path] = {}
    try:
        for relative, data in payloads.items():
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            backups[target] = target.read_bytes() if target.exists() else None
            with tempfile.NamedTemporaryFile(dir=target.parent, prefix=f".{target.name}.", delete=False) as handle:
                handle.write(data)
                staged[target] = Path(handle.name)
        for target, temporary in staged.items():
            os.replace(temporary, target)
    except Exception:
        for target, original in backups.items():
            if original is None:
                target.unlink(missing_ok=True)
            else:
                target.write_bytes(original)
        raise
    finally:
        for temporary in staged.values():
            temporary.unlink(missing_ok=True)


def write_report(path: Path | None, report: dict[str, Any]) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sync(args: argparse.Namespace) -> dict[str, Any]:
    root = Path(args.root).resolve()
    repository = args.repository
    if repository != DEFAULT_REPO and not args.source_dir:
        raise ValueError(f"public upstream sync is restricted to {DEFAULT_REPO}")
    source = DirectorySource(Path(args.source_dir)) if args.source_dir else GitHubSource(repository)
    current_lock = load_json(root / LOCK_NAME)
    release, staged_files = source.bundle(args.tag)
    stage_errors = validate_bundle(staged_files)
    current_tag = local_release_tag(root, current_lock)
    staged_hashes = {target: sha256(data) for target, data in staged_files.items()}
    changed_files = [
        target
        for target, data in staged_files.items()
        if not (root / target).is_file() or sha256((root / target).read_bytes()) != sha256(data)
    ]
    metadata_changed = (
        current_lock.get("repository") != repository
        or current_lock.get("release", {}).get("tag") != release["tag"]
        or current_lock.get("release", {}).get("commit") != release["commit"]
        or {
            target: item.get("sha256")
            for target, item in current_lock.get("files", {}).items()
            if isinstance(item, dict)
        }
        != staged_hashes
    )
    outdated = bool(changed_files or metadata_changed)
    report: dict[str, Any] = {
        "ok": not stage_errors,
        "mode": "update" if args.update else "check",
        "repository": repository,
        "previous_tag": current_tag,
        "current_tag": current_tag,
        "upstream": release,
        "outdated": outdated,
        "updated": False,
        "changed_files": changed_files,
        "stage_errors": stage_errors,
        "rollback_boundary": "all upstream files are staged and validated before an atomic replacement transaction",
    }
    if stage_errors:
        return report
    if not args.update or not outdated:
        local_errors = local_lock_errors(root, current_lock) if current_lock else ["local lock is missing"]
        report["local_errors"] = local_errors
        report["ok"] = not local_errors if not outdated else True
        return report

    lock = build_lock(repository, release, staged_files)
    payloads = dict(staged_files)
    payloads[LOCK_NAME] = (json.dumps(lock, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    payloads[NOTICE_NAME] = render_notice(lock).encode("utf-8")
    backups = {relative: (root / relative).read_bytes() if (root / relative).exists() else None for relative in payloads}
    try:
        replace_transaction(root, payloads)
        local_errors = local_lock_errors(root, lock)
        if local_errors:
            raise RuntimeError("; ".join(local_errors))
    except Exception:
        restore = {relative: data for relative, data in backups.items() if data is not None}
        replace_transaction(root, restore)
        for relative, data in backups.items():
            if data is None:
                (root / relative).unlink(missing_ok=True)
        raise
    report["updated"] = True
    report["current_tag"] = release["tag"]
    report["local_errors"] = []
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Check or update pinned official bento assets.")
    parser.add_argument("--root", default=Path(__file__).resolve().parents[1])
    parser.add_argument("--repository", default=DEFAULT_REPO)
    parser.add_argument("--tag", default="latest", help="Release tag, or latest (default).")
    parser.add_argument("--update", action="store_true", help="Replace the local snapshot after all checks pass.")
    parser.add_argument("--source-dir", help="Offline fixture source; not used for public upstream sync.")
    parser.add_argument("--report", help="Write a JSON evidence report.")
    args = parser.parse_args()
    report_path = Path(args.report).resolve() if args.report else None
    try:
        result = sync(args)
    except Exception as exc:
        result = {
            "ok": False,
            "mode": "update" if args.update else "check",
            "repository": args.repository,
            "error": str(exc),
            "rollback_boundary": "the previous snapshot is preserved when staging, validation, or replacement fails",
        }
    write_report(report_path, result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not result.get("ok"):
        raise SystemExit(2)


if __name__ == "__main__":
    main()
