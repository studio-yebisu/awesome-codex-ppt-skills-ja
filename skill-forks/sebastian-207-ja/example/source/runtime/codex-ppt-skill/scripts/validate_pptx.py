#!/usr/bin/env python3
from __future__ import annotations

import argparse
import io
import json
import re
import sys
import zipfile
from html import unescape
from pathlib import Path
from xml.etree import ElementTree as ET

from PIL import Image

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from inspect_pptx import inspect_pptx  # noqa: E402

EMU_PER_INCH = 914400
PLACEHOLDER_RE = re.compile(r"\b(lorem|ipsum|xxxx|todo|placeholder|待补充|占位)\b", re.I)
GENERATED_IMAGE_BACKENDS = {"codex_builtin_imagegen"}


def read_xml(z: zipfile.ZipFile, name: str) -> str:
    return z.read(name).decode("utf-8", errors="replace")


def parse_shapes(path: Path) -> list[dict[str, object]]:
    shapes: list[dict[str, object]] = []
    ns = {
        "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
        "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    }
    with zipfile.ZipFile(path) as z:
        slide_parts = sorted(n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n))
        for slide_idx, part in enumerate(slide_parts, start=1):
            root = ET.fromstring(read_xml(z, part))
            for sp in root.findall(".//p:sp", ns) + root.findall(".//p:pic", ns) + root.findall(".//p:graphicFrame", ns):
                off = sp.find(".//a:off", ns)
                ext = sp.find(".//a:ext", ns)
                text = " ".join(t.text or "" for t in sp.findall(".//a:t", ns)).strip()
                shapes.append(
                    {
                        "slide": slide_idx,
                        "tag": sp.tag.split("}")[-1],
                        "x": int(off.attrib.get("x", "0")) / EMU_PER_INCH if off is not None else 0,
                        "y": int(off.attrib.get("y", "0")) / EMU_PER_INCH if off is not None else 0,
                        "w": int(ext.attrib.get("cx", "0")) / EMU_PER_INCH if ext is not None else 0,
                        "h": int(ext.attrib.get("cy", "0")) / EMU_PER_INCH if ext is not None else 0,
                        "text": text,
                    }
                )
    return shapes


def notes_text(path: Path) -> list[str]:
    values: list[str] = []
    with zipfile.ZipFile(path) as z:
        for name in sorted(n for n in z.namelist() if n.startswith("ppt/notesSlides/notesSlide") and n.endswith(".xml")):
            xml = read_xml(z, name)
            values.append(" ".join(unescape(t) for t in re.findall(r"<a:t[^>]*>(.*?)</a:t>", xml, flags=re.S)))
    return values


def validate_asset_plan(asset_plan: Path | None, errors: list[str], warnings: list[str]) -> None:
    if not asset_plan:
        return
    if not asset_plan.exists():
        errors.append(f"asset_plan not found: {asset_plan}")
        return
    data = json.loads(asset_plan.read_text(encoding="utf-8-sig"))
    assets = data.get("assets") or data.get("slides") or []
    seen = set()
    generated_images = []
    generated_sources: dict[str, list[str]] = {}
    for item in assets:
        sid = item.get("slide_id")
        seen.add(sid)
        if "visual_need" not in item:
            errors.append(f"{sid} missing visual_need")
        if item.get("visual_need") == "required":
            if item.get("generation_required") and not item.get("output_path") and not item.get("failed_reason"):
                errors.append(f"{sid} required generation has no output_path or failed_reason")
            if item.get("output_path") and not Path(str(item.get("output_path"))).exists():
                errors.append(f"{sid} required visual output_path does not exist: {item.get('output_path')}")
            if item.get("must_not_skip") is not True:
                errors.append(f"{sid} required visual missing must_not_skip=true")
            if item.get("status") not in ("generated", "replaced_by_chart", "replaced_by_screenshot", "replaced_by_user_asset", "failed"):
                errors.append(f"{sid} required visual has unresolved status {item.get('status')}")
        if (
            item.get("generation_required") is True
            and item.get("generation_backend") in GENERATED_IMAGE_BACKENDS
            and item.get("status") == "generated"
            and item.get("output_path")
        ):
            out = Path(str(item.get("output_path")))
            if out.exists() and out.is_file() and out.stat().st_size > 0:
                generated_images.append(item)
                generated_sources.setdefault(str(out.resolve()), []).append(str(sid))
                binding = item.get("semantic_binding") or {}
                if binding.get("bound_to_slide") is not True:
                    errors.append(f"{sid} generated image is not semantically bound to the slide")
                if not str(binding.get("slide_title") or "").strip():
                    errors.append(f"{sid} generated image missing semantic_binding.slide_title")
                if not str(binding.get("core_message") or "").strip():
                    errors.append(f"{sid} generated image missing semantic_binding.core_message")
                if not str(binding.get("visual_brief") or "").strip():
                    errors.append(f"{sid} generated image missing semantic_binding.visual_brief")
                prompt_path = item.get("prompt_path")
                if not prompt_path or not Path(str(prompt_path)).exists():
                    errors.append(f"{sid} generated image missing prompt_path")
                else:
                    prompt_text = Path(str(prompt_path)).read_text(encoding="utf-8-sig", errors="ignore")
                    generic_markers = [
                        "mandatory generated-image gate",
                        "deck-level image generation requirement",
                        "Phase 3 mandatory",
                        "seed generated asset",
                        "reused for regression",
                    ]
                    if any(marker.lower() in prompt_text.lower() for marker in generic_markers):
                        errors.append(f"{sid} generated image prompt is generic gate text, not a page-specific prompt")
                    title = str(binding.get("slide_title") or "").strip()
                    core = str(binding.get("core_message") or "").strip()
                    title_hit = title and (title in prompt_text or title[: max(2, min(6, len(title)))] in prompt_text)
                    core_hit = core and (core in prompt_text or core[: max(2, min(8, len(core)))] in prompt_text)
                    if not (title_hit or core_hit):
                        errors.append(f"{sid} generated image prompt does not reference the slide title or core message")
    if not assets:
        warnings.append("asset_plan exists but has no assets/slides entries")
    if not generated_images:
        errors.append("mandatory generated image missing: at least one generated image asset with existing output_path is required")
    for source, slide_ids in generated_sources.items():
        if len(slide_ids) > 1:
            errors.append(f"generated image reused across slides {', '.join(slide_ids)}: {source}")


def rel_target(base_part: str, target: str) -> str:
    if target.startswith("/"):
        return target.lstrip("/")
    base = Path(base_part).parent
    return str((base / target).as_posix()).replace("ppt/slides/../", "ppt/")


def detect_picture_integrity(path: Path, errors: list[str], warnings: list[str], strict_image_ratio: bool = False) -> None:
    ns = {
        "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
        "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
        "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
        "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
    }
    with zipfile.ZipFile(path) as z:
        names = set(z.namelist())
        slide_parts = sorted(n for n in names if re.match(r"ppt/slides/slide\d+\.xml$", n))
        for slide_idx, part in enumerate(slide_parts, start=1):
            rel_part = f"ppt/slides/_rels/slide{slide_idx}.xml.rels"
            rels: dict[str, str] = {}
            if rel_part in names:
                rel_root = ET.fromstring(read_xml(z, rel_part))
                for rel in rel_root.findall(".//rel:Relationship", ns):
                    rels[rel.attrib.get("Id", "")] = rel.attrib.get("Target", "")
            root = ET.fromstring(read_xml(z, part))
            for pic_idx, pic in enumerate(root.findall(".//p:pic", ns), start=1):
                blip = pic.find(".//a:blip", ns)
                embed = blip.attrib.get(f"{{{ns['r']}}}embed") if blip is not None else ""
                target = rels.get(embed or "")
                if not target:
                    errors.append(f"slide {slide_idx} picture {pic_idx} missing image relationship")
                    continue
                image_name = rel_target(part, target)
                if image_name not in names:
                    errors.append(f"slide {slide_idx} picture {pic_idx} missing image file: {image_name}")
                    continue
                ext = pic.find(".//a:ext", ns)
                if ext is None:
                    continue
                try:
                    display_w = int(ext.attrib.get("cx", "0"))
                    display_h = int(ext.attrib.get("cy", "0"))
                    if display_w <= 0 or display_h <= 0:
                        continue
                    image = Image.open(io.BytesIO(z.read(image_name)))
                    native_w, native_h = image.size
                    if native_w <= 0 or native_h <= 0:
                        continue
                    display_ratio = display_w / display_h
                    native_ratio = native_w / native_h
                    distortion = max(display_ratio / native_ratio, native_ratio / display_ratio)
                    if distortion > 1.35:
                        message = f"slide {slide_idx} picture {pic_idx} image aspect ratio distorted: display {display_ratio:.2f}, source {native_ratio:.2f}"
                        if strict_image_ratio:
                            errors.append(message)
                        else:
                            warnings.append(message)
                except Exception as exc:
                    warnings.append(f"slide {slide_idx} picture {pic_idx} image ratio check failed: {exc}")


def detect_overlaps(shapes: list[dict[str, object]], warnings: list[str]) -> None:
    for i, a in enumerate(shapes):
        if a["w"] <= 0 or a["h"] <= 0:
            continue
        for b in shapes[i + 1 :]:
            if a["slide"] != b["slide"] or b["w"] <= 0 or b["h"] <= 0:
                continue
            ax2, ay2 = a["x"] + a["w"], a["y"] + a["h"]
            bx2, by2 = b["x"] + b["w"], b["y"] + b["h"]
            area = max(0, min(ax2, bx2) - max(a["x"], b["x"])) * max(0, min(ay2, by2) - max(a["y"], b["y"]))
            min_area = min(a["w"] * a["h"], b["w"] * b["h"])
            if min_area > 0.18 and area / min_area > 0.65:
                ta, tb = str(a.get("text", ""))[:30], str(b.get("text", ""))[:30]
                if ta or tb:
                    warnings.append(f"slide {a['slide']} possible overlap: {ta} / {tb}")


def validate(
    path: Path,
    expected_count: int | None = None,
    asset_plan: Path | None = None,
    preview_dir: Path | None = None,
    require_notes: bool = False,
    expected_aspect_ratio: str | None = None,
    strict_image_ratio: bool = False,
) -> dict[str, object]:
    errors: list[str] = []
    warnings: list[str] = []
    if not path.exists() or path.stat().st_size == 0:
        return {"valid": False, "errors": ["PPTX missing or empty"], "warnings": warnings}
    info = inspect_pptx(path)
    if expected_count is not None and info["slide_count"] != expected_count:
        errors.append(f"slide count {info['slide_count']} != expected {expected_count}")
    if info["slide_size"].get("aspect_ratio") == "unknown":
        warnings.append("slide size unknown")
    if expected_aspect_ratio and info["slide_size"].get("aspect_ratio") != expected_aspect_ratio:
        errors.append(f"slide aspect ratio {info['slide_size'].get('aspect_ratio')} != expected {expected_aspect_ratio}")
    for slide in info["slides"]:
        texts = slide.get("text_runs", [])
        for text in texts:
            if PLACEHOLDER_RE.search(text):
                errors.append(f"slide {slide['slide_number']} placeholder-like text: {text[:80]}")
            if len(text) > 420:
                warnings.append(f"slide {slide['slide_number']} long text run may overflow")
        if slide.get("shape_count", 0) == 0 and slide.get("picture_count", 0) == 0:
            warnings.append(f"slide {slide['slide_number']} has no detected shapes or pictures")
    shapes = parse_shapes(path)
    detect_overlaps(shapes, warnings)
    detect_picture_integrity(path, errors, warnings, strict_image_ratio)
    note_values = notes_text(path)
    if require_notes and len(note_values) < int(info["slide_count"]):
        errors.append("speaker notes missing on one or more slides")
    body_runs = [text for slide in info["slides"] for text in slide.get("text_runs", [])]
    body_text = "\n".join(body_runs)
    body_norm = re.sub(r"\s+", " ", body_text)
    for idx, note in enumerate(note_values, start=1):
        clean = re.sub(r"\s+", " ", note).strip()
        threshold = 24 if re.search(r"[\u4e00-\u9fff]", clean) else 40
        leaked = len(clean) >= threshold and clean in body_norm
        if not leaked:
            for run in body_runs:
                run_clean = re.sub(r"\s+", " ", run).strip()
                run_threshold = 24 if re.search(r"[\u4e00-\u9fff]", run_clean) else 40
                if len(run_clean) >= run_threshold and run_clean in clean:
                    leaked = True
                    break
        if leaked:
            errors.append(f"speaker notes leaked into body text on slide {idx}")
    validate_asset_plan(asset_plan, errors, warnings)
    if preview_dir:
        pdf = preview_dir / "final.pdf"
        if not pdf.exists() or pdf.stat().st_size == 0:
            errors.append("preview/final.pdf missing or empty")
        if expected_count:
            for idx in range(1, expected_count + 1):
                png = preview_dir / f"slide_{idx:02d}.png"
                if not png.exists() or png.stat().st_size == 0:
                    errors.append(f"preview PNG missing: {png.name}")
    return {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "summary": {k: info[k] for k in ("slide_count", "slide_size", "media_count")},
        "notes_count": len(note_values),
    }


def write_md(report: dict[str, object], output: Path) -> None:
    lines = ["# QA Report", "", f"- Status: {'PASS' if report.get('valid') else 'FAIL'}", f"- Slide count: {report.get('summary', {}).get('slide_count')}", f"- Notes count: {report.get('notes_count', 0)}", "", "## Errors"]
    errors = report.get("errors") or []
    lines.extend([f"- {e}" for e in errors] or ["- none"])
    lines.append("")
    lines.append("## Warnings")
    warnings = report.get("warnings") or []
    lines.extend([f"- {w}" for w in warnings] or ["- none"])
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pptx", type=Path)
    parser.add_argument("--expected-slide-count", type=int)
    parser.add_argument("--asset-plan", type=Path)
    parser.add_argument("--preview-dir", type=Path)
    parser.add_argument("--require-notes", action="store_true")
    parser.add_argument("--expected-aspect-ratio")
    parser.add_argument("--strict-image-ratio", action="store_true")
    parser.add_argument("--output", "-o", type=Path)
    parser.add_argument("--markdown", type=Path)
    args = parser.parse_args()
    report = validate(args.pptx, args.expected_slide_count, args.asset_plan, args.preview_dir, args.require_notes, args.expected_aspect_ratio, args.strict_image_ratio)
    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    if args.markdown:
        write_md(report, args.markdown)
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
