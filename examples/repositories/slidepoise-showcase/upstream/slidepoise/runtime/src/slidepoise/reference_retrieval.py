"""Local reference-slide recall with provenance and explicit host selection.

Scores describe lexical overlap only. This module never judges visual quality,
selects generation references, fetches sources, or verifies source authenticity.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
import sqlite3
import tempfile
import textwrap
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont, ImageOps
from .resource_catalogs import catalog_sources, scope_reference_records

SCHEMA_VERSION = "1"
AUTHENTICITY_MODES = ("authentic", "exclude-generated", "any")
EXCLUSION_KEYS = ("ids", "canonical_paths", "sha256", "source_families", "source_types")
STOP_WORDS = frozenset("a an and are as at be by for from in is it of on or that the this to with".split())
INTENT_FIELDS = (
    "communication_job", "role", "slide_role", "relationships", "semantic_relationships",
    "information_structure", "audience_question", "dominant_message", "required_content",
    "layout", "title", "description", "tags",
)
FOCUS_FIELDS = {"communication_job", "role", "slide_role", "information_structure.type", "query"}


def intent_fields(intent: dict, query: str) -> list[tuple[str, str]]:
    fields = []
    for key in INTENT_FIELDS:
        for field, text in text_fields(intent.get(key), key):
            if key == "required_content" and field.endswith((".role", ".id")):
                continue
            fields.append((field, text))
    if query:
        fields.append(("query", query))
    return fields


def read_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object at {path}")
    return value


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tokens(value: str) -> set[str]:
    return {term for term in re.findall(r"[^\W_]+", value.casefold(), re.UNICODE)
            if len(term) > 1 and term not in STOP_WORDS and not term.isdigit()}


def text_fields(value: Any, prefix: str = "") -> list[tuple[str, str]]:
    """Keep field paths so arbitrary catalog metadata remains explainable."""
    if isinstance(value, dict):
        return [pair for key, item in value.items()
                for pair in text_fields(item, f"{prefix}.{key}" if prefix else str(key))]
    if isinstance(value, list):
        return [pair for item in value for pair in text_fields(item, prefix)]
    return [(prefix, str(value))] if isinstance(value, (str, int, float)) and not isinstance(value, bool) else []


def _boolean(value: Any) -> bool | None:
    if value is True or (isinstance(value, str) and value.casefold() == "true"):
        return True
    if value is False or (isinstance(value, str) and value.casefold() == "false"):
        return False
    return None


def provenance(record: dict) -> dict:
    raw = record.get("provenance") or {}
    raw = raw if isinstance(raw, dict) else {}

    def first(*keys: str) -> Any:
        return next((owner[key] for owner in (record, raw) for key in keys if owner.get(key) not in (None, "")), None)

    flags = [_boolean(owner.get(key)) for owner in (record, raw)
             for key in ("generated_reference", "generated_source", "is_generated")]
    source_type = str(first("source_type") or "unknown")
    source = first("source", "source_url", "source_file", "source_document")
    page = first("source_page", "page", "page_number")
    valid_page = (isinstance(page, int) and not isinstance(page, bool) and page > 0) or (
        isinstance(page, str) and bool(page.strip()) and page.strip() != "0")
    if True in flags or source_type.casefold() in {"generated", "ai_generated", "generated_image", "synthetic"}:
        state = "generated"
    elif False in flags and source and valid_page:
        state = "recorded_authentic"
    else:
        state = "unknown"
    return {"authenticity": state, "source": source, "source_page": page, "source_type": source_type,
            "source_family": first("source_family") or source}


def resolve_preview(record: dict, key: str, catalog: Path, asset_roots: list[Path]) -> tuple[Path | None, str | None]:
    raw = record.get("preview_path") or record.get("path") or record.get("canonical_file") or key
    if not isinstance(raw, str) or not raw.strip() or re.match(r"^[a-zA-Z][\w+.-]*://", raw):
        return None, "preview_path_must_be_local"
    path = Path(raw).expanduser()
    path = (path if path.is_absolute() else catalog.parent / path).resolve()
    roots = [catalog.parent.resolve(), *(root.expanduser().resolve() for root in asset_roots)]
    if not any(path.is_relative_to(root) for root in roots):
        return None, "preview_outside_allowed_roots"
    if not path.is_file():
        return path, "preview_missing"
    return path, None


def load_records(catalogs: list[Path], asset_roots: list[Path] | None = None) -> tuple[list[dict], list[dict]]:
    records, bindings = [], []
    for catalog in dict.fromkeys(path.expanduser().resolve() for path in catalogs):
        data = read_json(catalog)
        items = data.get("items", {})
        if not isinstance(items, (dict, list)):
            raise ValueError(f"Catalog items must be an object or array at {catalog}")
        bindings.append({"path": str(catalog), "sha256": digest(catalog)})
        entries = items.items() if isinstance(items, dict) else enumerate(items)
        for key, item in entries:
            if not isinstance(item, dict):
                raise ValueError(f"Catalog item {key} must be an object at {catalog}")
            path, error = resolve_preview(item, str(key), catalog, asset_roots or [])
            checksum, dimensions = None, None
            if error is None:
                try:
                    with Image.open(path) as preview:
                        preview.verify()
                    with Image.open(path) as preview:
                        dimensions = list(preview.size)
                    checksum = digest(path)
                except (OSError, ValueError, Image.DecompressionBombError):
                    error = "preview_unreadable"
            records.append({"id": str(item.get("id") or key), "catalog_path": str(catalog),
                            "catalog_key": str(key), "metadata": item,
                            "canonical_file": str(path) if path else None, "sha256": checksum,
                            "dimensions_px": dimensions, "asset_error": error, **provenance(item)})
    return records, bindings


def normalize_exclusions(value: dict | None = None, exclude_ids: list[str] | None = None) -> dict:
    value = value or {}
    unknown = set(value) - set(EXCLUSION_KEYS) - {"rationale", "schema_version"}
    if unknown:
        raise ValueError(f"Unknown exclusion fields {sorted(unknown)}")
    result = {}
    for key in EXCLUSION_KEYS:
        items = value.get(key, [])
        if not isinstance(items, list) or any(not isinstance(item, str) for item in items):
            raise ValueError(f"Exclusions {key} must be an array of strings")
        result[key] = list(dict.fromkeys(items))
    result["ids"] = list(dict.fromkeys([*result["ids"], *(exclude_ids or [])]))
    result["canonical_paths"] = [str(Path(path).expanduser().resolve()) for path in result["canonical_paths"]]
    result["sha256"] = [value.lower() for value in result["sha256"]]
    if value.get("rationale"):
        result["rationale"] = value["rationale"]
    return result


def restriction_reason(record: dict, authenticity: str, exclusions: dict, include_ineligible: bool = False) -> str | None:
    if record.get("resource_id") in exclusions.get("ids", []):
        return "excluded_ids"
    for key, field in (("ids", "id"), ("canonical_paths", "canonical_file"), ("sha256", "sha256"),
                       ("source_families", "source_family"), ("source_types", "source_type")):
        if record.get(field) is not None and str(record[field]) in exclusions.get(key, []):
            return f"excluded_{key}"
    if not include_ineligible and _boolean(record["metadata"].get("retrieval_eligible")) is False:
        return "catalog_retrieval_ineligible"
    if authenticity == "authentic" and record["authenticity"] != "recorded_authentic":
        return f"authenticity_{record['authenticity']}"
    if authenticity == "exclude-generated" and record["authenticity"] == "generated":
        return "authenticity_generated"
    return record.get("asset_error")


def _field_weight(field: str) -> float:
    if field.split(".")[0] in {"roles", "role", "communication_job", "relationships", "layout", "tags"}:
        return 3.0
    return 2.0 if field in {"name", "title", "description"} else 1.0


def searchable_fields(metadata: dict) -> list[tuple[str, str]]:
    # Keep arbitrary descriptive metadata, excluding storage and review bookkeeping.
    ignored_roots = {"visual_review", "review", "reviewer", "id", "path", "preview_path", "canonical_file"}
    return [(field, value) for field, value in text_fields(metadata)
            if field.split(".")[0] not in ignored_roots
            and not field.endswith(("sha256", "_path", ".path"))]


def build_index(records: list[dict], path: Path) -> None:
    """Build an owned SQLite term index afresh so catalog edits cannot go stale."""
    path = path.expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        try:
            with sqlite3.connect(f"{path.as_uri()}?mode=ro", uri=True) as existing:
                version = existing.execute("SELECT version FROM reference_index_meta").fetchone()
            if version != (SCHEMA_VERSION,):
                raise ValueError("unrecognized schema")
        except (sqlite3.Error, ValueError) as error:
            raise ValueError(f"Refusing to overwrite an unrelated index file at {path}") from error
    with tempfile.NamedTemporaryFile(prefix="reference-index-", suffix=".sqlite", dir=path.parent, delete=False) as file:
        temporary = Path(file.name)
    try:
        with sqlite3.connect(temporary) as connection:
            connection.executescript("""
                CREATE TABLE reference_index_meta (version TEXT NOT NULL);
                CREATE TABLE reference_records (row_id INTEGER PRIMARY KEY, record_json TEXT NOT NULL);
                CREATE TABLE reference_terms (row_id INTEGER NOT NULL, term TEXT NOT NULL, field TEXT NOT NULL,
                                              weight REAL NOT NULL, PRIMARY KEY (row_id, term, field));
                CREATE INDEX reference_terms_lookup ON reference_terms(term);
            """)
            connection.execute("INSERT INTO reference_index_meta VALUES (?)", (SCHEMA_VERSION,))
            for row_id, record in enumerate(records):
                connection.execute("INSERT INTO reference_records VALUES (?, ?)", (row_id, json.dumps(record)))
                entries = {(term, field, _field_weight(field))
                           for field, text in searchable_fields(record["metadata"]) for term in tokens(text)}
                connection.executemany("INSERT INTO reference_terms VALUES (?, ?, ?, ?)",
                                       [(row_id, term, field, weight) for term, field, weight in entries])
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def query_index(path: Path, intent: dict, *, query: str = "", authenticity: str = "authentic",
                exclusions: dict | None = None, limit: int = 12, include_ineligible: bool = False) -> dict:
    if authenticity not in AUTHENTICITY_MODES or limit < 1:
        raise ValueError("Use a supported authenticity mode and a positive candidate limit")
    exclusions = normalize_exclusions(exclusions)
    fields = intent_fields(intent, query)
    query_terms = sorted(tokens(" ".join(text for _, text in fields)))
    focus_terms = tokens(" ".join(text for field, text in fields if field in FOCUS_FIELDS))
    structure_terms = tokens(" ".join(text for field, text in fields if not field.startswith("required_content")))
    if not query_terms:
        raise ValueError("Intent and query contain no searchable communication, relationship, role or content terms")
    with sqlite3.connect(f"{path.resolve().as_uri()}?mode=ro", uri=True) as connection:
        records = {row_id: json.loads(raw) for row_id, raw in connection.execute(
            "SELECT row_id, record_json FROM reference_records")}
        matches: dict[int, list[tuple[str, str, float]]] = {}
        # One term at a time avoids SQLite's parameter count limit for long intents.
        for term in query_terms:
            hits = connection.execute("SELECT row_id, field, weight FROM reference_terms WHERE term = ?", (term,)).fetchall()
            idf = math.log(1 + len(records) / (1 + len({row[0] for row in hits})))
            for row_id, field, weight in hits:
                matches.setdefault(row_id, []).append((term, field, weight * idf))
    candidates, omitted = [], []
    for row_id, record in records.items():
        reason = restriction_reason(record, authenticity, exclusions, include_ineligible)
        if reason:
            omitted.append({"id": record["id"], "catalog_path": record["catalog_path"], "reason": reason})
            continue
        hits = matches.get(row_id, [])
        if not hits:
            continue
        term_scores: dict[str, float] = {}
        matched_fields: dict[str, set[str]] = {}
        for term, field, score in hits:
            term_scores[term] = max(term_scores.get(term, 0), score)
            matched_fields.setdefault(field, set()).add(term)
        candidates.append({**record, "matched_terms": sorted(term_scores),
                           "matched_fields": {field: sorted(terms) for field, terms in sorted(matched_fields.items())},
                           "matched_intent_fields": {field: sorted(tokens(text) & term_scores.keys())
                                                     for field, text in fields if tokens(text) & term_scores.keys()},
                           "focus_structural_match_count": len({term for term, field, _ in hits
                                                                if term in focus_terms and _field_weight(field) == 3}),
                           "structural_match_count": len({term for term, field, _ in hits
                                                          if term in structure_terms and _field_weight(field) == 3}),
                           "recall_score": round(sum(term_scores.values()), 6)})
    candidates.sort(key=lambda record: (-record["focus_structural_match_count"], -record["structural_match_count"],
                                         -record["recall_score"],
                                         record["id"], record["catalog_path"]))
    total = len(candidates)
    candidates = candidates[:limit]
    for rank, record in enumerate(candidates, 1):
        record["thumbnail_label"] = f"R{rank:02d}"
    return {"query_fields": sorted({field for field, _ in fields}), "query_terms": query_terms,
            "matching_candidate_count": total, "candidates": candidates, "omitted": omitted}


def build_contact_sheet(candidates: list[dict], path: Path) -> dict:
    """Show actual local slide previews for the host's independent inspection."""
    columns, width, image_height, caption_height, margin = 3, 520, 300, 170, 16
    rows = max(1, math.ceil(len(candidates) / columns))
    canvas = Image.new("RGB", (columns * width, 60 + rows * (image_height + caption_height)), "#e9edef")
    draw = ImageDraw.Draw(canvas)
    font = heading = ImageFont.load_default()
    for name in ("DejaVuSans.ttf", "Arial.ttf", "/System/Library/Fonts/Supplemental/Arial.ttf"):
        try:
            font, heading = ImageFont.truetype(name, 17), ImageFont.truetype(name, 22)
            break
        except OSError:
            continue
    draw.text((margin, 18), "Reference candidates | lexical recall only | host selection required", fill="#17232c", font=heading)
    for index, record in enumerate(candidates):
        x, y = (index % columns) * width, 60 + (index // columns) * (image_height + caption_height)
        with Image.open(record["canonical_file"]) as source:
            preview = ImageOps.contain(ImageOps.exif_transpose(source).convert("RGB"),
                                       (width - margin * 2, image_height - margin * 2))
        canvas.paste(preview, (x + (width - preview.width) // 2, y + (image_height - preview.height) // 2))
        name = str(record["metadata"].get("name") or record["id"])
        title_lines = textwrap.wrap(f"{record['thumbnail_label']}  {name}", width=52)[:2]
        caption = "\n".join(title_lines) + f"\nPage {record['source_page']} | {record['source_type']}"
        source_caption = str(record.get("source") or "Source unrecorded")
        caption += "\n" + "\n".join(textwrap.wrap(source_caption, width=54)[:2])
        matches = "Matches " + ", ".join(record["matched_terms"][:6])
        caption += "\n" + "\n".join(textwrap.wrap(matches, width=54)[:2])
        draw.multiline_text((x + margin, y + image_height), caption, fill="#17232c", font=font, spacing=4)
    if not candidates:
        draw.text((margin, 90), "No available candidates matched this intent and the source restrictions.",
                  fill="#17232c", font=heading)
    path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(path, format="PNG")
    return {"path": str(path.resolve()), "sha256": digest(path), "candidate_count": len(candidates)}


def configured_catalogs(config: dict, config_path: Path) -> list[Path]:
    return [Path(source["catalog"]).expanduser().resolve() for source in configured_sources(config, config_path)]


def configured_sources(config: dict, config_path: Path) -> list[dict]:
    library = config.get("libraries", {}).get("visual_references", {})
    sources = catalog_sources(library)
    for source in sources:
        value = source["catalog"]
        if not isinstance(value, str) or not value:
            raise ValueError("Resolved config requires valid reference catalog paths")
        path = Path(value).expanduser()
        source["catalog"] = str((path if path.is_absolute() else config_path.parent / path).resolve())
    return sources


def retrieve(config_path: Path, intent_path: Path, output_path: Path, sheet_path: Path, *,
             index_path: Path | None = None, extra_catalogs: list[Path] | None = None,
             asset_roots: list[Path] | None = None, exclusions: dict | None = None,
             exclude_ids: list[str] | None = None, authenticity: str = "authentic", query: str = "", limit: int = 12,
             include_ineligible: bool = False) -> dict:
    config, intent = read_json(config_path), read_json(intent_path)
    sources = configured_sources(config, config_path)
    scoped_paths = {source["catalog"] for source in sources}
    sources.extend({"catalog": str(path.expanduser().resolve())} for path in (extra_catalogs or [])
                   if str(path.expanduser().resolve()) not in scoped_paths)
    records, bindings = load_records([Path(source["catalog"]) for source in sources], asset_roots)
    records = scope_reference_records(records, sources)
    index_path = (index_path or output_path.with_suffix(".sqlite")).resolve()
    outputs = [output_path.resolve(), sheet_path.resolve(), index_path]
    inputs = {config_path.resolve(), intent_path.resolve(), *(Path(binding["path"]) for binding in bindings),
              *(Path(record["canonical_file"]) for record in records if record.get("canonical_file"))}
    if len(set(outputs)) != len(outputs) or any(path in inputs for path in outputs):
        raise ValueError("Retrieval outputs must be distinct and cannot overwrite input files")
    exclusions = normalize_exclusions(exclusions, exclude_ids)
    build_index(records, index_path)
    result = query_index(index_path, intent, query=query, authenticity=authenticity, exclusions=exclusions, limit=limit,
                         include_ineligible=include_ineligible)
    result.update({"schema_version": "1.0.0", "purpose": "reference_candidate_recall",
                   "ranking_notice": "Lexical recall only. Structural matches from role, communication job, structure type "
                                     "and explicit query come first, then other intent structure matches, then weighted "
                                     "text overlap. Rank and score make no claim about visual quality or suitability.",
                   "provenance_notice": "Authenticity uses recorded metadata and is not independently verified.",
                   "selection_owner": "host_agent", "index_path": str(index_path),
                   "intent": {"path": str(intent_path.resolve()), "sha256": digest(intent_path)},
                   "reference_retrieval": {"selection_mode": "host_selected", "authenticity": authenticity,
                                           "include_ineligible": include_ineligible,
                                           "profile_id": config.get("resolved_profile", {}).get("profile_id"),
                                           "catalogs": bindings, "sources": sources,
                                           "asset_roots": [str(root.expanduser().resolve()) for root in asset_roots or []],
                                           "exclusions": exclusions}})
    result["contact_sheet"] = build_contact_sheet(result["candidates"], sheet_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return result


def validate_host_selection(resources: dict, library: dict | None = None) -> None:
    """Apply the retrieval restrictions again at the generation boundary."""
    policy = resources.get("reference_retrieval")
    if policy is None:
        return
    if not isinstance(policy, dict) or policy.get("selection_mode") != "host_selected":
        raise ValueError("reference_retrieval requires selection_mode host_selected")
    mode = policy.get("authenticity", "authentic")
    if mode not in AUTHENTICITY_MODES:
        raise ValueError("Unsupported reference_retrieval authenticity mode")
    paths = [Path(binding["path"]) for binding in policy.get("catalogs", [])]
    records, _ = load_records(paths, [Path(root) for root in policy.get("asset_roots", [])])
    if "sources" in policy:
        sources = policy["sources"]
        if library is not None and "sources" in library:
            current = {str(Path(source["catalog"]).resolve()): source for source in catalog_sources(library)}
            sources = [current.get(str(Path(source["catalog"]).resolve()), source)
                       for source in sources
                       if not source.get("set_id") or str(Path(source["catalog"]).resolve()) in current]
        records = scope_reference_records(records, sources)
    elif library is not None and "sources" in library:
        records = scope_reference_records(records, catalog_sources(library))
    exclusions = normalize_exclusions(policy.get("exclusions"))
    for selected in resources.get("selected_visual_references", []):
        path = str(Path(selected.get("canonical_file", "")).expanduser().resolve())
        matches = [record for record in records if record["id"] == str(selected.get("id"))
                   and (not selected.get("resource_id") or record.get("resource_id") == selected["resource_id"])
                   and record["canonical_file"] == path]
        if len(matches) != 1:
            raise ValueError(f"Selected reference {selected.get('id')} must resolve uniquely in the retrieval catalogs")
        reason = restriction_reason(matches[0], mode, exclusions, bool(policy.get("include_ineligible")))
        if reason:
            raise ValueError(f"Selected reference {selected['id']} violates retrieval restrictions ({reason})")
        if selected.get("sha256") and selected["sha256"] != matches[0]["sha256"]:
            raise ValueError(f"Selected reference {selected['id']} changed since retrieval")
