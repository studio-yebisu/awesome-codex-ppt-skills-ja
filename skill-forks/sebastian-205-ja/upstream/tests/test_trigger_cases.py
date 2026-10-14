import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "tests" / "trigger_cases.json"
EXPECTED_KEYS = {"id", "query", "should_trigger", "category"}


def load_cases() -> list[dict]:
    return json.loads(CASES_PATH.read_text(encoding="utf-8"))


def test_trigger_fixture_has_balanced_boundary_coverage() -> None:
    cases = load_cases()
    positives = [case for case in cases if case["should_trigger"] is True]
    negatives = [case for case in cases if case["should_trigger"] is False]

    assert len(positives) >= 10
    assert len(negatives) >= 10
    assert len({case["category"] for case in positives}) >= 10
    assert len({case["category"] for case in negatives}) >= 10


def test_trigger_fixture_schema_and_identifiers_are_exact_and_unique() -> None:
    cases = load_cases()
    assert all(set(case) == EXPECTED_KEYS for case in cases)
    assert all(isinstance(case["id"], str) and case["id"].strip() for case in cases)
    assert all(
        isinstance(case["query"], str) and case["query"].strip() for case in cases
    )
    assert all(type(case["should_trigger"]) is bool for case in cases)
    assert all(
        isinstance(case["category"], str) and case["category"].strip()
        for case in cases
    )
    assert len({case["id"] for case in cases}) == len(cases)
    assert len({case["query"] for case in cases}) == len(cases)


def test_positive_cases_cover_supported_paper_inputs_and_talks() -> None:
    positives = [case for case in load_cases() if case["should_trigger"]]
    categories = {case["category"] for case in positives}
    required = {
        "local-pdf",
        "doi",
        "pmid",
        "pmcid",
        "arxiv",
        "notes",
        "template",
        "thesis-seminar",
        "methods-ai",
        "review",
    }
    assert required <= categories
    assert all(
        any(token in case["query"].lower() for token in ("ppt", "powerpoint"))
        for case in positives
    )


def test_negative_cases_cover_near_miss_boundaries() -> None:
    negatives = [case for case in load_cases() if not case["should_trigger"]]
    categories = {case["category"] for case in negatives}
    required = {
        "business-slides",
        "general-slides",
        "image-reconstruction",
        "paper-search",
        "manuscript-writing",
        "academic-polishing",
        "citations",
        "pdf-summary",
    }
    assert required <= categories
    assert any("ppt" in case["query"].lower() for case in negatives)
    assert any("论文" in case["query"] for case in negatives)
