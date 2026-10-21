#!/usr/bin/env python3
"""Run a deterministic routing smoke eval against the skill description."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^\w\u4e00-\u9fff.]+", " ", text.lower())).strip()


def present(text: str, phrase: str) -> bool:
    text = normalize(text)
    phrase = normalize(phrase)
    if re.search(r"[\u4e00-\u9fff]", phrase) or "." in phrase:
        return phrase in text
    return f" {phrase} " in f" {text} "


def load(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {}


def description(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not text.startswith("---\n"):
        return text
    end = lines[1:].index("---") + 1
    if yaml is not None:
        meta = yaml.safe_load("\n".join(lines[1:end])) or {}
        if isinstance(meta, dict):
            return str(meta.get("description", ""))
    return text


def hits(text: str, concepts: dict[str, list[str]]) -> set[str]:
    return {
        name
        for name, phrases in concepts.items()
        if any(present(text, phrase) for phrase in phrases)
    }


def items(cases: dict[str, Any], bucket: str) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for raw in cases.get(bucket, []):
        output.append(raw if isinstance(raw, dict) else {"text": str(raw), "family": "default"})
    return output


def evaluate(root: Path, cases_path: Path) -> dict[str, Any]:
    cases = load(cases_path)
    concepts = cases["positive_concepts"]
    desc_hits = hits(description(root / "SKILL.md"), concepts)
    required = set(cases["description_required_concepts"])
    missing = sorted(required - desc_hits)
    negative_patterns = cases.get("negative_patterns", [])
    prompt_required_any = set(cases.get("prompt_required_any", []))
    threshold = float(cases.get("recommended_threshold", 0.5))
    denominator = max(1, int(cases.get("score_denominator", 3)))
    results: dict[str, list[dict[str, Any]]] = {}
    failures: list[dict[str, Any]] = []
    total = passed_count = 0
    for bucket in ("should_trigger", "should_not_trigger", "near_neighbor"):
        expected = bucket == "should_trigger"
        results[bucket] = []
        for item in items(cases, bucket):
            prompt = str(item.get("text", ""))
            matched = sorted(hits(prompt, concepts) & desc_hits)
            prompt_hits = hits(prompt, concepts)
            negative = next((pattern for pattern in negative_patterns if present(prompt, pattern)), None)
            score = min(1.0, len(matched) / denominator)
            has_required_prompt_concept = not prompt_required_any or bool(prompt_hits & prompt_required_any)
            predicted = score >= threshold and negative is None and has_required_prompt_concept
            passed = predicted == expected
            record = {
                "prompt": prompt,
                "family": item.get("family", "default"),
                "expected_trigger": expected,
                "predicted_trigger": predicted,
                "passed": passed,
                "score": round(score, 3),
                "matched_concepts": matched,
                "has_required_prompt_concept": has_required_prompt_concept,
                "negative_pattern": negative,
            }
            results[bucket].append(record)
            total += 1
            passed_count += int(passed)
            if not passed:
                failures.append({"bucket": bucket, **record})
    return {
        "ok": not missing and not failures,
        "threshold": threshold,
        "description_concepts": sorted(desc_hits),
        "missing_description_concepts": missing,
        "summary": {
            "total": total,
            "passed": passed_count,
            "pass_rate": round(passed_count / total, 3) if total else 0,
        },
        "failures": failures,
        "results": results,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate qiaomu-bento-ppt routing.")
    parser.add_argument("skill_dir", nargs="?", default=".")
    parser.add_argument("--cases", default="evals/trigger_cases.json")
    parser.add_argument("--output", "-o")
    args = parser.parse_args()
    root = Path(args.skill_dir).resolve()
    cases = Path(args.cases)
    if not cases.is_absolute():
        cases = root / cases
    result = evaluate(root, cases)
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        output = Path(args.output)
        if not output.is_absolute():
            output = root / output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    if not result["ok"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
