"""Console access to the same indexed reference recall used by the Agent."""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

from .paths import SKILL_ROOT
from .profiles import profile_record, library_catalog
from .library_sets import set_catalog, set_record

sys.path.insert(0, str(SKILL_ROOT / "runtime/src"))
from slidepoise.reference_retrieval import build_index, load_records, query_index
from slidepoise.resource_catalogs import scope_reference_records


def search(profile_id: str, query: str, authenticity: str = "authentic") -> dict:
    if not isinstance(query, str) or not query.strip() or len(query) > 1200:
        raise ValueError("Describe the slide's message or visual relationship in up to 1,200 characters")
    profile = profile_record(profile_id)["profile"]
    selections = profile.get("library_sets", {})
    sources = []
    if "visual_references" not in selections:
        catalog, _ = library_catalog(profile_id, "visual_references")
        sources.append({"catalog": str(catalog)})
    for set_id in selections.get("visual_references", []):
        if set_record(set_id).get("source") != "local":
            continue
        catalog, _ = set_catalog(set_id)
        source = {"set_id": set_id, "catalog": str(catalog)}
        subsets = profile.get("library_items", {}).get("visual_references", {})
        if set_id in subsets:
            source["item_ids"] = subsets[set_id]
        sources.append(source)
    records, _ = load_records([Path(source["catalog"]) for source in sources])
    records = scope_reference_records(records, sources)
    # Build from current catalog and source files so Console edits apply immediately.
    with tempfile.TemporaryDirectory(prefix="slidepoise-reference-search-") as directory:
        index = Path(directory) / "references.sqlite"
        build_index(records, index)
        result = query_index(index, {"communication_job": query}, authenticity=authenticity, limit=24)
    return {**result, "profile_id": profile_id, "selection_owner": "host_agent"}
