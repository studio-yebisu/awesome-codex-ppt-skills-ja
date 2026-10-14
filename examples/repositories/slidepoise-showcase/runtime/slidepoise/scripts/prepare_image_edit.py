"""Bind a focused image edit to a verified generation request and candidate pixels."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from PIL import Image, UnidentifiedImageError
from prepare_generation import dump_json, file_binding, load, validate_prompt_capacity, verify_request
from slidepoise.artifacts import write_json


def build_edit_request(
    generation_request: Path, candidate: Path, changes: Path, *, max_prompt_chars: int | None = None,
) -> dict:
    base = verify_request(generation_request)
    bindings = {name: file_binding(path) for name, path in (
        ("generation_request", generation_request), ("candidate", candidate), ("changes", changes),
    )}
    corrections = changes.read_text(encoding="utf-8").strip()
    if not corrections:
        raise SystemExit("Image edit changes are empty. Record the focused correction identified by the Agent or user.")
    try:
        with Image.open(candidate) as image:
            dimensions = list(image.size)
            image.verify()
    except (OSError, UnidentifiedImageError, SyntaxError) as error:
        raise SystemExit(f"Cannot read the candidate image. {candidate}. {error}") from error

    # An edit retains the generation host's capacity and may impose a tighter one.
    validate_prompt_capacity("", max_prompt_chars)
    limits = [value for value in (max_prompt_chars, base["host_constraints"]["max_prompt_chars"]) if value is not None]
    maximum = min(limits) if limits else None
    prompt = "\n\n".join([
        "# SlidePoise targeted image edit",
        ("Edit the first attachment, current-candidate, in place. Apply the scoped corrections below. "
         "Preserve unspecified content, composition, asset identities and style."),
        ("This is an edit operation. The verified generation brief defines the content and visual constraints, "
         "including the substantive-only canvas and shared deck design. It does not request a new composition. "
         "Changes to those constraints require updated source inputs and a newly compiled generation request."),
        "## Scoped corrections",
        corrections,
        "## Verified content and visual constraints",
        base["prompt"],
    ])
    validate_prompt_capacity(prompt, maximum)
    primary = {"id": "current-candidate", "purpose": "Current image to edit in place", **bindings["candidate"]}
    return {
        "schema_version": "1.0", "purpose": "host_image_edit_request", "prompt": prompt,
        "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
        "prompt_character_count": len(prompt), "host_constraints": {"max_prompt_chars": maximum},
        "preferred_model": base["preferred_model"], "canvas": base["canvas"],
        "candidate_dimensions_px": dimensions,
        "reference_images": [primary, *[item for item in base["reference_images"] if item["path"] != primary["path"]]],
        "input_bindings": bindings,
    }


def verify_edit_request(path: Path) -> dict:
    request = load(path)
    if request.get("schema_version") != "1.0" or request.get("purpose") != "host_image_edit_request":
        raise SystemExit("Unsupported image edit request")
    bindings = request.get("input_bindings", {})
    if set(bindings) != {"generation_request", "candidate", "changes"}:
        raise SystemExit("Image edit request is missing source bindings")
    for name, record in bindings.items():
        if file_binding(Path(record["path"])) != record:
            raise SystemExit(f"Image edit input changed. Recompile the request. {name}")
    expected = build_edit_request(
        *(Path(bindings[name]["path"]) for name in ("generation_request", "candidate", "changes")),
        max_prompt_chars=(request.get("host_constraints") or {}).get("max_prompt_chars"),
    )
    if request != expected:
        raise SystemExit("Image edit request differs from its compiled prompt or attachments. Recompile the request.")
    return request


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--generation-request", type=Path, help="Fresh request produced by prepare_generation.py")
    parser.add_argument("--candidate", type=Path, help="Current substantive-region candidate image")
    parser.add_argument("--changes", type=Path, help="Plain-text focused corrections from Agent review or user feedback")
    parser.add_argument("--output", type=Path, help="Compiled image edit request JSON")
    parser.add_argument("--max-prompt-chars", type=int, help="Optional tighter host capacity. The generation limit remains in force.")
    parser.add_argument("--verify-request", type=Path, help="Verify freshness and emit the exact edit request for the host")
    args = parser.parse_args()
    if args.verify_request:
        if any(getattr(args, name) is not None for name in ("generation_request", "candidate", "changes", "output", "max_prompt_chars")):
            parser.error("--verify-request does not accept edit input or output options")
        print(dump_json(verify_edit_request(args.verify_request)))
        return
    if any(getattr(args, name) is None for name in ("generation_request", "candidate", "changes", "output")):
        parser.error("Image editing requires --generation-request, --candidate, --changes and --output")
    request = build_edit_request(args.generation_request, args.candidate, args.changes, max_prompt_chars=args.max_prompt_chars)
    base = load(args.generation_request)
    sources = [*request["input_bindings"].values(), *base["input_bindings"].values(), *request["reference_images"]]
    if args.output.resolve() in {Path(item["path"]).resolve() for item in sources}:
        raise SystemExit("The image edit output must be distinct from all source inputs and reference images")
    write_json(args.output, request)
    print(dump_json({"request": str(args.output.resolve()), "prompt_character_count": request["prompt_character_count"]}))


if __name__ == "__main__":
    main()
