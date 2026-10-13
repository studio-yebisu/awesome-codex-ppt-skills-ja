#!/usr/bin/env python3
"""Build, extract, locate, and validate bento/slides documents.

This script never downloads, publishes, signs, deploys, or rotates document
identity. It writes a new output by default and requires --overwrite to replace
an existing path.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DOC_OPEN = '<script type="application/bento+json" id="bento-doc">'
DOC_CLOSE = "</scr" + "ipt>"
DOC_BLOCK_RE = re.compile(
    r'<script type="application/bento\+json" id="bento-doc">\s*([\s\S]*?)\s*</script>'
)
SKILL_ROOT = Path(__file__).resolve().parents[1]
BUNDLED_SHELL = SKILL_ROOT / "assets" / "bento" / "Bento_Slides.bento.html"
BUNDLED_OFFICIAL_SKILL = SKILL_ROOT / "references" / "upstream" / "bento-official-skill.md"
BUNDLED_AGENTS_GUIDE = SKILL_ROOT / "references" / "upstream" / "bento-agents.md"
BUNDLED_FORMAT_GUIDE = SKILL_ROOT / "references" / "upstream" / "bento-format.md"
TRANSITIONS = {"none", "fade", "slide", "zoom", "morph"}
ELEMENT_TYPES = {"text", "shape", "image", "svg", "chart", "table", "media"}
BASE_NUMBERS = ("x", "y", "w", "h", "rotation", "opacity")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def write_text(path: Path, text: str, overwrite: bool = False) -> None:
    if path.exists() and not overwrite:
        raise ValueError(f"output exists: {path} (choose a new path or pass --overwrite)")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, payload: dict[str, Any], overwrite: bool = True) -> None:
    write_text(path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n", overwrite)


def load_json_text(text: str, label: str) -> dict[str, Any]:
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"{label}: invalid JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"{label}: expected a JSON object")
    if payload.get("format") == "bento/enc":
        raise ValueError(f"{label}: encrypted bento/enc documents must be unlocked in bento first")
    return payload


def extract_doc_from_html(text: str, label: str) -> dict[str, Any]:
    matches = list(DOC_BLOCK_RE.finditer(text))
    if len(matches) != 1:
        raise ValueError(f"{label}: expected exactly one plaintext #bento-doc block, found {len(matches)}")
    return load_json_text(matches[0].group(1).strip(), label)


def load_document(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    if path.name.endswith(".bento.html") or DOC_OPEN in text:
        return extract_doc_from_html(text, str(path)), "html"
    return load_json_text(text, str(path)), "json"


def is_checkout(path: Path) -> bool:
    return (
        (path / "slides" / "package.json").is_file()
        and (path / "scripts" / "shell-gate.mjs").is_file()
        and (path / "plugins" / "bento-slides" / "skills" / "bento-slides" / "SKILL.md").is_file()
    )


def discover_repo(explicit: str | None = None) -> Path | None:
    candidates: list[Path] = []
    if explicit:
        candidates.append(Path(explicit).expanduser())
    env_repo = os.environ.get("BENTO_REPO")
    if env_repo:
        candidates.append(Path(env_repo).expanduser())
    cwd = Path.cwd().resolve()
    candidates.extend([cwd, *cwd.parents])

    seen: set[Path] = set()
    for candidate in candidates:
        try:
            resolved = candidate.resolve()
        except OSError:
            continue
        if resolved in seen:
            continue
        seen.add(resolved)
        if is_checkout(resolved):
            return resolved
    return None


def repo_info(repo: Path | None) -> dict[str, Any]:
    bundled = {
        "shell": str(BUNDLED_SHELL),
        "shell_exists": BUNDLED_SHELL.is_file(),
        "official_skill": str(BUNDLED_OFFICIAL_SKILL),
        "agents_guide": str(BUNDLED_AGENTS_GUIDE),
        "format_guide": str(BUNDLED_FORMAT_GUIDE),
        "guides_exist": all(
            path.is_file()
            for path in (BUNDLED_OFFICIAL_SKILL, BUNDLED_AGENTS_GUIDE, BUNDLED_FORMAT_GUIDE)
        ),
    }
    checkout: dict[str, Any] | None = None
    if repo is not None:
        shell = repo / "slides" / "dist-single" / "Bento_Slides.bento.html"
        checkout = {
            "repo": str(repo),
            "shell": str(shell),
            "shell_exists": shell.is_file(),
            "official_skill": str(
                repo / "plugins" / "bento-slides" / "skills" / "bento-slides" / "SKILL.md"
            ),
            "agents_guide": str(repo / "docs" / "agents.md"),
            "format_guide": str(repo / "docs" / "format.md"),
            "model": str(repo / "slides" / "src" / "model.ts"),
        }
    standalone_ok = bool(bundled["shell_exists"] and bundled["guides_exist"])
    return {
        "ok": standalone_ok,
        "standalone": standalone_ok,
        "bundled": bundled,
        "checkout": checkout,
        "message": (
            "standalone assets ready; bento checkout is optional"
            if standalone_ok
            else "bundled bento assets are incomplete; reinstall the skill"
        ),
    }


def add_error(report: dict[str, Any], path: str, message: str) -> None:
    report["errors"].append({"path": path, "message": message})


def add_warning(report: dict[str, Any], path: str, message: str) -> None:
    report["warnings"].append({"path": path, "message": message})


def is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def valid_uuid(value: str) -> bool:
    try:
        uuid.UUID(value)
        return True
    except (ValueError, AttributeError):
        return False


def plain_text(html: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]*>", " ", html)).strip()


def validate_asset_ref(
    report: dict[str, Any], value: Any, path: str, assets: dict[str, Any]
) -> None:
    if not isinstance(value, str) or not value:
        add_error(report, path, "source must be a non-empty string")
        return
    if value.startswith("asset:"):
        key = value.split(":", 1)[1]
        if key not in assets:
            add_error(report, path, f"missing doc.assets entry: {key}")
    elif value.startswith(("http://", "https://")):
        add_warning(report, path, "external URL breaks the fully offline guarantee")


def validate_chart(report: dict[str, Any], element: dict[str, Any], path: str) -> None:
    option = element.get("option")
    if not isinstance(option, dict):
        add_error(report, f"{path}.option", "chart option must be a pure JSON object")
        return
    series = option.get("series", [])
    if isinstance(series, dict):
        series = [series]
    if not isinstance(series, list):
        add_error(report, f"{path}.option.series", "series must be an array or object")
        return
    for index, item in enumerate(series):
        if not isinstance(item, dict):
            add_error(report, f"{path}.option.series[{index}]", "series entry must be an object")
            continue
        kind = item.get("type")
        data = item.get("data", [])
        if kind in {"bar", "line", "scatter"} and isinstance(data, list):
            for data_index, value in enumerate(data):
                if not is_number(value):
                    add_error(
                        report,
                        f"{path}.option.series[{index}].data[{data_index}]",
                        f"{kind} data must contain plain numbers",
                    )


def validate_table(report: dict[str, Any], element: dict[str, Any], path: str) -> None:
    columns = element.get("columns")
    rows = element.get("rows")
    style = element.get("style")
    if not isinstance(columns, list) or not columns:
        add_error(report, f"{path}.columns", "table needs at least one column")
        return
    if not isinstance(rows, list) or not rows:
        add_error(report, f"{path}.rows", "table needs at least one row")
    if not isinstance(style, dict):
        add_error(report, f"{path}.style", "table style object is required")
    for row_index, row in enumerate(rows if isinstance(rows, list) else []):
        cells = row.get("cells") if isinstance(row, dict) else None
        if not isinstance(cells, list) or len(cells) != len(columns):
            add_error(
                report,
                f"{path}.rows[{row_index}].cells",
                f"cell count must match {len(columns)} columns",
            )


def validate_element(
    report: dict[str, Any],
    element: Any,
    path: str,
    slide_size: tuple[float, float],
    assets: dict[str, Any],
    slide_ids: set[str],
) -> tuple[str | None, bool]:
    if not isinstance(element, dict):
        add_error(report, path, "element must be an object")
        return None, False
    element_id = element.get("id")
    if not isinstance(element_id, str) or not element_id:
        add_error(report, f"{path}.id", "element id is required")
        element_id = None
    kind = element.get("type")
    if kind not in ELEMENT_TYPES:
        add_error(report, f"{path}.type", f"unsupported element type: {kind!r}")
    for key in BASE_NUMBERS:
        if not is_number(element.get(key)):
            add_error(report, f"{path}.{key}", "must be a number")
    width, height = slide_size
    x, y, w, h = (element.get(key) for key in ("x", "y", "w", "h"))
    if all(is_number(value) for value in (x, y, w, h)):
        if w <= 0 or h <= 0:
            add_error(report, path, "element width and height must be positive")
        if x < 0 or y < 0 or x + w > width or y + h > height:
            add_warning(report, path, "element extends outside the slide bounds")
    opacity = element.get("opacity")
    if is_number(opacity) and not 0 <= opacity <= 1:
        add_error(report, f"{path}.opacity", "must be between 0 and 1")
    link = element.get("link")
    if link is not None and link not in slide_ids:
        add_error(report, f"{path}.link", f"target slide does not exist: {link}")

    has_motion = bool(element.get("fx"))
    if kind == "text":
        for key in ("html", "fontSize", "fontFamily", "fontWeight", "color", "align", "valign", "lineHeight"):
            if key not in element:
                add_error(report, f"{path}.{key}", "required text field is missing")
        html = element.get("html", "")
        if isinstance(html, str):
            length = len(plain_text(html))
            if length > 320:
                add_warning(report, f"{path}.html", f"text is dense ({length} characters)")
        font_size = element.get("fontSize")
        if is_number(font_size) and font_size < 18:
            add_warning(report, f"{path}.fontSize", "text below 18px may be hard to read")
    elif kind == "shape":
        for key in ("shape", "fill", "stroke", "strokeWidth", "radius"):
            if key not in element:
                add_error(report, f"{path}.{key}", "required shape field is missing")
    elif kind == "image":
        validate_asset_ref(report, element.get("src"), f"{path}.src", assets)
        for key in ("fit", "radius"):
            if key not in element:
                add_error(report, f"{path}.{key}", "required image field is missing")
    elif kind == "svg":
        if not element.get("asset") and not element.get("markup"):
            add_error(report, path, "svg needs asset or markup")
        if element.get("asset") and element["asset"] not in assets:
            add_error(report, f"{path}.asset", f"missing doc.assets entry: {element['asset']}")
    elif kind == "chart":
        validate_chart(report, element, path)
    elif kind == "table":
        validate_table(report, element, path)
    elif kind == "media":
        if element.get("kind") not in {"video", "audio"}:
            add_error(report, f"{path}.kind", "media kind must be video or audio")
        validate_asset_ref(report, element.get("src"), f"{path}.src", assets)
        if element.get("autoplay") and element.get("kind") == "video" and not element.get("muted"):
            add_warning(report, path, "autoplay video normally requires muted:true")
    return element_id, has_motion


def validate_doc(doc: dict[str, Any], allow_missing_doc_id: bool = False) -> dict[str, Any]:
    report: dict[str, Any] = {
        "ok": True,
        "format": doc.get("format"),
        "doc_id": doc.get("docId"),
        "slide_count": 0,
        "errors": [],
        "warnings": [],
    }
    if doc.get("format") != "bento/slides":
        add_error(report, "format", "must be 'bento/slides'")
    if not isinstance(doc.get("version"), int) or doc.get("version", 0) < 1:
        add_error(report, "version", "must be a positive integer")

    doc_id = doc.get("docId")
    if doc_id is None and allow_missing_doc_id:
        add_warning(report, "docId", "missing on fresh input; build will mint it once")
    elif not isinstance(doc_id, str) or not valid_uuid(doc_id):
        add_error(report, "docId", "must be a UUID and remain stable for the document lifetime")

    for key in ("title", "modified"):
        if not isinstance(doc.get(key), str) or not doc.get(key):
            add_error(report, key, "must be a non-empty string")
    size = doc.get("size")
    if not isinstance(size, dict) or not all(is_number(size.get(key)) and size[key] > 0 for key in ("width", "height")):
        add_error(report, "size", "must contain positive numeric width and height")
        slide_size = (1280.0, 720.0)
    else:
        slide_size = (float(size["width"]), float(size["height"]))
    theme = doc.get("theme")
    if not isinstance(theme, dict):
        add_error(report, "theme", "theme object is required")
    else:
        for key in ("background", "color", "accent", "fontFamily"):
            if not isinstance(theme.get(key), str) or not theme.get(key):
                add_error(report, f"theme.{key}", "required theme string is missing")

    if doc.get("template") and doc.get("readonly"):
        add_error(report, "template", "template and readonly cannot both be enabled")
    assets = doc.get("assets", {})
    if not isinstance(assets, dict):
        add_error(report, "assets", "must be an object when present")
        assets = {}
    slides = doc.get("slides")
    if not isinstance(slides, list) or not slides:
        add_error(report, "slides", "must be a non-empty array")
        report["ok"] = False
        return report

    report["slide_count"] = len(slides)
    slide_ids: set[str] = set()
    for index, slide in enumerate(slides):
        path = f"slides[{index}]"
        if not isinstance(slide, dict):
            add_error(report, path, "slide must be an object")
            continue
        slide_id = slide.get("id")
        if not isinstance(slide_id, str) or not slide_id:
            add_error(report, f"{path}.id", "slide id is required")
        elif slide_id in slide_ids:
            add_error(report, f"{path}.id", f"duplicate slide id: {slide_id}")
        else:
            slide_ids.add(slide_id)

    any_motion = False
    for slide_index, slide in enumerate(slides):
        if not isinstance(slide, dict):
            continue
        path = f"slides[{slide_index}]"
        if slide.get("transition") not in TRANSITIONS:
            add_error(report, f"{path}.transition", "unsupported transition")
        if not isinstance(slide.get("background"), str):
            add_error(report, f"{path}.background", "background string is required")
        notes = slide.get("notes")
        if not isinstance(notes, str):
            add_error(report, f"{path}.notes", "speaker notes string is required")
        elif not notes.strip():
            add_warning(report, f"{path}.notes", "speaker notes are empty")
        state_of = slide.get("stateOf")
        if state_of is not None and state_of not in slide_ids:
            add_error(report, f"{path}.stateOf", f"parent slide does not exist: {state_of}")
        elements = slide.get("elements")
        if not isinstance(elements, list):
            add_error(report, f"{path}.elements", "elements must be an array")
            continue
        if len(elements) > 24:
            add_warning(report, f"{path}.elements", f"high element count ({len(elements)})")
        element_ids: set[str] = set()
        morph_keys: set[str] = set()
        for element_index, element in enumerate(elements):
            element_path = f"{path}.elements[{element_index}]"
            element_id, has_motion = validate_element(
                report, element, element_path, slide_size, assets, slide_ids
            )
            any_motion = any_motion or has_motion
            if element_id:
                if element_id in element_ids:
                    add_error(report, f"{element_path}.id", f"duplicate element id on slide: {element_id}")
                element_ids.add(element_id)
            if isinstance(element, dict) and element_id:
                morph_key = element.get("morphId") or element_id
                if morph_key in morph_keys:
                    add_error(
                        report,
                        element_path,
                        f"duplicate effective morph key on the same slide: {morph_key}",
                    )
                morph_keys.add(morph_key)
        any_motion = any_motion or slide.get("transition") == "morph"

    if not any_motion:
        add_warning(report, "slides", "no morph or presentation motion found")
    if doc.get("collab"):
        add_warning(report, "collab", "document carries collaboration capabilities; preserve and handle deliberately")
    report["ok"] = not report["errors"]
    return report


def serialize_doc(doc: dict[str, Any]) -> str:
    return json.dumps(doc, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")


def splice_shell(shell: str, doc: dict[str, Any]) -> str:
    matches = list(DOC_BLOCK_RE.finditer(shell))
    if len(matches) != 1:
        raise ValueError(f"shell must contain exactly one #bento-doc block, found {len(matches)}")
    payload = serialize_doc(doc)
    block = f"{DOC_OPEN}\n{payload}\n{DOC_CLOSE}"
    output = DOC_BLOCK_RE.sub(lambda _match: block, shell, count=1)
    if payload not in output:
        raise ValueError("document splice failed")
    return output


def gate_shell_text(text: str) -> dict[str, Any]:
    matches = list(DOC_BLOCK_RE.finditer(text))
    errors: list[str] = []
    if len(matches) != 1:
        errors.append(f"expected one regex-extractable #bento-doc block, found {len(matches)}")
    opens = len(re.findall(r"<script[\s>]", text))
    closes = text.count(DOC_CLOSE)
    if opens != closes:
        errors.append(f"script tag imbalance ({opens}/{closes})")
    doc = None
    if len(matches) == 1:
        block_text = matches[0].group(1)
        if "</scr" + "ipt>" in block_text.lower():
            errors.append("literal script close appears inside #bento-doc")
        try:
            doc = load_json_text(block_text.strip(), "#bento-doc")
        except ValueError as exc:
            errors.append(str(exc))
    return {"ok": not errors, "errors": errors, "doc": doc}


def choose_shell(args: argparse.Namespace, repo: Path | None) -> Path:
    if args.shell:
        shell = Path(args.shell).expanduser().resolve()
    elif os.environ.get("BENTO_SHELL"):
        shell = Path(os.environ["BENTO_SHELL"]).expanduser().resolve()
    elif BUNDLED_SHELL.is_file():
        shell = BUNDLED_SHELL
    elif repo:
        shell = repo / "slides" / "dist-single" / "Bento_Slides.bento.html"
    else:
        raise ValueError("bundled shell is missing; reinstall the skill or pass --shell")
    if not shell.is_file() and args.build_shell:
        if repo is None:
            raise ValueError("--build-shell requires a bento checkout")
        subprocess.run(["npm", "run", "build:single"], cwd=repo / "slides", check=True)
    if not shell.is_file():
        raise ValueError(f"built shell not found: {shell}; run npm run build:single or pass --build-shell")
    return shell


def command_locate(args: argparse.Namespace) -> int:
    info = repo_info(discover_repo(args.repo))
    print(json.dumps(info, ensure_ascii=False, indent=2))
    return 0 if info["ok"] else 2


def command_extract(args: argparse.Namespace) -> int:
    source = Path(args.input).expanduser().resolve()
    doc, source_type = load_document(source)
    report = validate_doc(doc, allow_missing_doc_id=True)
    output = Path(args.output).expanduser().resolve()
    write_text(output, json.dumps(doc, ensure_ascii=False, indent=2) + "\n", args.overwrite)
    result = {
        "ok": report["ok"],
        "source": str(source),
        "source_type": source_type,
        "output": str(output),
        "doc_id": doc.get("docId"),
        "validation": report,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if report["ok"] else 2


def command_validate(args: argparse.Namespace) -> int:
    source = Path(args.input).expanduser().resolve()
    doc, source_type = load_document(source)
    report = validate_doc(doc, allow_missing_doc_id=args.allow_missing_doc_id)
    report["source"] = str(source)
    report["source_type"] = source_type
    if source_type == "html":
        gate = gate_shell_text(source.read_text(encoding="utf-8"))
        report["shell_gate"] = {"ok": gate["ok"], "errors": gate["errors"]}
        if not gate["ok"]:
            report["ok"] = False
    if args.report:
        write_json(Path(args.report).expanduser().resolve(), report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["ok"] else 2


def command_build(args: argparse.Namespace) -> int:
    source = Path(args.input).expanduser().resolve()
    doc, source_type = load_document(source)
    input_doc_id = doc.get("docId")
    identity_source: Path | None = None
    identity_doc_id = input_doc_id
    if not args.new_document:
        if args.identity_source:
            identity_source = Path(args.identity_source).expanduser().resolve()
            identity_doc, _identity_source_type = load_document(identity_source)
            identity_doc_id = identity_doc.get("docId")
            if input_doc_id != identity_doc_id:
                raise ValueError(
                    "input docId does not match --identity-source; restore the original identity before building"
                )
        elif source_type == "json":
            raise ValueError(
                "editing from JSON requires --identity-source <original.bento.html> to prove docId preservation"
            )
        else:
            identity_source = source
    if args.new_document:
        if doc.get("collab"):
            raise ValueError("fresh documents must not inherit collab capabilities")
        if not input_doc_id:
            doc["docId"] = str(uuid.uuid4())
        doc.setdefault("modified", utc_now())
    elif not input_doc_id:
        raise ValueError("editing build requires an existing docId; use --new-document only for a fresh deck")

    preflight = validate_doc(doc)
    if not preflight["ok"]:
        if args.report:
            write_json(Path(args.report).expanduser().resolve(), preflight)
        print(json.dumps(preflight, ensure_ascii=False, indent=2))
        return 2

    repo = discover_repo(args.repo)
    if not args.shell and not args.new_document and identity_source:
        args.shell = str(identity_source)
    shell_path = choose_shell(args, repo)
    shell = shell_path.read_text(encoding="utf-8")
    output_html = splice_shell(shell, doc)
    output = Path(args.output).expanduser().resolve()
    write_text(output, output_html, args.overwrite)

    internal_gate = gate_shell_text(output_html)
    project_gate: dict[str, Any] = {"ran": False, "ok": None}
    if repo:
        process = subprocess.run(
            ["node", str(repo / "scripts" / "shell-gate.mjs"), str(output)],
            cwd=repo,
            text=True,
            capture_output=True,
        )
        project_gate = {
            "ran": True,
            "ok": process.returncode == 0,
            "stdout": process.stdout.strip(),
            "stderr": process.stderr.strip(),
        }

    output_doc = internal_gate.get("doc")
    output_report = validate_doc(output_doc) if isinstance(output_doc, dict) else {
        "ok": False,
        "errors": [{"path": "#bento-doc", "message": "output document could not be parsed"}],
        "warnings": [],
    }
    output_doc_id = output_doc.get("docId") if isinstance(output_doc, dict) else None
    identity = {
        "mode": "new" if args.new_document else "edit",
        "input_doc_id": input_doc_id,
        "identity_source": str(identity_source) if identity_source else None,
        "source_doc_id": identity_doc_id,
        "output_doc_id": output_doc_id,
        "preserved": identity_doc_id == output_doc_id if identity_doc_id else None,
        "minted_once": bool(args.new_document and not input_doc_id and output_doc_id),
    }
    identity_ok = identity["minted_once"] if args.new_document and not input_doc_id else identity["preserved"]
    ok = bool(
        output_report.get("ok")
        and internal_gate["ok"]
        and identity_ok
        and (project_gate["ok"] is not False)
    )
    result = {
        "ok": ok,
        "input": str(source),
        "shell": str(shell_path),
        "output": str(output),
        "identity": identity,
        "validation": output_report,
        "shell_gate": {
            "internal": {"ok": internal_gate["ok"], "errors": internal_gate["errors"]},
            "project": project_gate,
        },
        "rollback_boundary": "source unchanged; output written separately"
        if source.resolve() != output.resolve()
        else "explicit overwrite requested",
    }
    if args.report:
        write_json(Path(args.report).expanduser().resolve(), result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if ok else 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Work with bento/slides JSON and .bento.html files.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    locate = subparsers.add_parser("locate", help="Locate a bento checkout and its official guides.")
    locate.add_argument("--repo", help="Path to a bento checkout.")
    locate.set_defaults(func=command_locate)

    extract = subparsers.add_parser("extract", help="Extract #bento-doc JSON from a deck.")
    extract.add_argument("input", help="Input .bento.html or JSON.")
    extract.add_argument("--output", "-o", required=True, help="Output JSON path.")
    extract.add_argument("--overwrite", action="store_true", help="Allow replacing the output path.")
    extract.set_defaults(func=command_extract)

    validate = subparsers.add_parser("validate", help="Validate deck JSON or .bento.html.")
    validate.add_argument("input", help="Input .bento.html or JSON.")
    validate.add_argument("--report", help="Write the validation report as JSON.")
    validate.add_argument(
        "--allow-missing-doc-id",
        action="store_true",
        help="Allow a fresh pre-build JSON fixture to omit docId.",
    )
    validate.set_defaults(func=command_validate)

    build = subparsers.add_parser("build", help="Splice deck JSON into a clean bento shell.")
    build.add_argument("input", help="Input deck JSON or .bento.html.")
    build.add_argument("--output", "-o", required=True, help="Output .bento.html path.")
    build.add_argument("--repo", help="Path to a bento checkout.")
    build.add_argument("--shell", help="Explicit clean Bento_Slides.bento.html shell.")
    build.add_argument(
        "--identity-source",
        help="Original .bento.html used to prove docId preservation when editing extracted JSON.",
    )
    build.add_argument("--build-shell", action="store_true", help="Run npm run build:single if needed.")
    build.add_argument(
        "--new-document",
        action="store_true",
        help="Mint docId only when absent; rejects inherited collab capabilities.",
    )
    build.add_argument("--overwrite", action="store_true", help="Allow replacing the output path.")
    build.add_argument("--report", help="Write the build and validation report as JSON.")
    build.set_defaults(func=command_build)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    try:
        raise SystemExit(args.func(args))
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False, indent=2), file=sys.stderr)
        raise SystemExit(2) from exc


if __name__ == "__main__":
    main()
