"""Shared speaker-note handling; production notes are separate from work records."""
from __future__ import annotations


def canonical_notes(text: str) -> str:
    """Normalize platform newlines without removing whitespace or changing wording."""
    return text.replace("\r\n", "\n").replace("\r", "\n")


def scene_notes(slide: dict) -> str:
    # Scene v1's legacy notes field remains supported for existing decks.
    return canonical_notes(slide.get("speaker_notes", slide.get("notes", "")))


def read_notes(slide) -> str:
    # Inspect without creating a notes part in decks that have none.
    if not slide.has_notes_slide:
        return ""
    frame = slide.notes_slide.notes_text_frame
    return canonical_notes(frame.text) if frame is not None else ""


def check_notes(presentation, slides: list[dict], *, scene: bool = False) -> list[str]:
    errors = []
    if len(presentation.slides) != len(slides):
        errors.append("Slide count differs from speaker-note source")
    for index, (actual, expected) in enumerate(zip(presentation.slides, slides), 1):
        if not scene and "speaker_notes" not in expected:
            continue  # Legacy Page Specs did not declare exportable speaker notes.
        wanted = scene_notes(expected) if scene else canonical_notes(expected["speaker_notes"])
        if read_notes(actual) != wanted:
            errors.append(f"Slide {index}/{expected['id']}: speaker notes differ from source")
    return errors


def check_scene_notes(spec: dict, scene: dict) -> list[str]:
    errors = []
    if [s["id"] for s in spec["slides"]] != [s["id"] for s in scene["slides"]]:
        errors.append("Scene slide IDs/order differ from Page Spec")
        return errors
    for expected, actual in zip(spec["slides"], scene["slides"]):
        if "speaker_notes" in expected and (
            "speaker_notes" not in actual or canonical_notes(expected["speaker_notes"]) != scene_notes(actual)
        ):
            errors.append(f"{expected['id']}: Scene speaker_notes missing or differ from Page Spec")
    return errors
