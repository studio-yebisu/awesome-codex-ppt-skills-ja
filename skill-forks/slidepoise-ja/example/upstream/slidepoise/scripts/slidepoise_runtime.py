#!/usr/bin/env python3
"""Thin deterministic execution wrapper for the self-contained SlidePoise Skill."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from xml.etree import ElementTree
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "runtime"
SRC = RUNTIME / "src"
sys.path.insert(0, str(SRC))

from slidepoise.reconstruction.contract import build_reconstruction_contract  # noqa: E402
from slidepoise.reconstruction.scene import build_reconstruction_scene  # noqa: E402
from slidepoise.artifacts import (  # noqa: E402
    ArtifactError, bundle_deck, file_hash, load_deck, presentation_spec,
    read_json as read, resolve_scene_paths,
    validate_scene, verify_bundle, write_json as write,
)


def run_checked(command: list[str], *, env: dict[str, str] | None = None) -> None:
    result = subprocess.run(command, text=True, capture_output=True, env=env)
    if result.returncode:
        raise SystemExit((result.stderr or result.stdout or "command failed").strip())
    if result.stdout.strip():
        print(result.stdout.strip())


def command_measure(args: argparse.Namespace) -> None:
    cmd = [sys.executable, str(RUNTIME / "scripts/measure_visual_scene.py"), str(args.image), "--semantic-map", str(args.semantic_map), "--output-dir", str(args.output_dir), "--config", str(args.config)]
    if args.upstream_handoff:
        cmd += ["--upstream-handoff", str(args.upstream_handoff)]
    if args.sam:
        cmd += ["--sam", args.sam]
    run_checked(cmd)


def command_build_contract(args: argparse.Namespace) -> None:
    measured = read(args.measured_scene)
    config = read(args.config)
    contract = build_reconstruction_contract(measured, config["design"])
    write(args.output, contract)
    print(json.dumps({"units": len(contract.get("reconstruction_units", [])), "assets": len(contract.get("canonical_asset_mappings", [])), "connectors": len(contract.get("connector_reconstruction_plans", []))}, indent=2))


def command_compile_scene(args: argparse.Namespace) -> None:
    scene = build_reconstruction_scene(
        measured_scene=read(args.measured_scene),
        contract=read(args.contract),
        design=read(args.config)["design"],
        slide_id=args.slide_id,
    )
    write(args.output, scene)
    print(json.dumps({"objects": len(scene.get("objects", [])), "slide_id": args.slide_id}, indent=2))


def command_reconstruct_slide(args: argparse.Namespace) -> None:
    output_dir = args.output_dir.resolve()
    measurement_dir = output_dir / "measurement"
    command_measure(argparse.Namespace(
        image=args.image,
        semantic_map=args.semantic_map,
        output_dir=measurement_dir,
        upstream_handoff=args.upstream_handoff,
        config=args.config,
        sam=args.sam,
    ))
    measured_scene = measurement_dir / "slide_entities.json"
    contract = output_dir / "reconstruction-contract.json"
    scene = output_dir / "constructor-scene.json"
    command_build_contract(argparse.Namespace(
        measured_scene=measured_scene,
        config=args.config,
        output=contract,
    ))
    command_compile_scene(argparse.Namespace(
        measured_scene=measured_scene,
        contract=contract,
        config=args.config,
        slide_id=args.slide_id,
        output=scene,
    ))
    print(json.dumps({
        "slide_id": args.slide_id,
        "measurement_overlay": str((measurement_dir / "debug_overlay.png").resolve()),
        "measured_scene": str(measured_scene.resolve()),
        "reconstruction_contract": str(contract.resolve()),
        "constructor_scene": str(scene.resolve()),
    }, indent=2))


def node_environment() -> dict[str, str]:
    env = dict(os.environ)
    env["PYTHON"] = sys.executable
    framework_home = Path(env.get("SLIDEPOISE_HOME", str(Path.home() / ".slidepoise"))).expanduser()
    local_runtime = framework_home / "node" / "node_modules"
    roots = [str(local_runtime)] if local_runtime.is_dir() else []
    npm = shutil.which("npm")
    if npm:
        root = subprocess.run([npm, "root", "-g"], text=True, capture_output=True).stdout.strip()
        if root:
            roots.append(root)
    if env.get("NODE_PATH"):
        roots.append(env["NODE_PATH"])
    if roots:
        env["NODE_PATH"] = os.pathsep.join(roots)
    return env


def command_render_pptx(args: argparse.Namespace) -> None:
    scene = read(args.scene)
    validate_scene(scene, label=str(args.scene))
    scene = resolve_scene_paths(scene, args.scene)
    config = read(args.config)
    spec = presentation_spec(
        [scene],
        title=args.title or "SlidePoise presentation",
        language=args.language,
        theme={"display_font": config["design"]["style"].get("display_font", "Georgia"),
               "body_font": config["design"]["style"].get("body_font", "Arial")},
    )
    with tempfile.TemporaryDirectory(prefix="slidepoise-pptx-") as temp:
        spec_path = Path(temp) / "presentation.json"
        write(spec_path, spec)
        run_checked(["node", str(RUNTIME / "js/scene_to_pptx.mjs"), "--input", str(spec_path), "--output", str(args.output)], env=node_environment())
    print(json.dumps({"pptx": str(args.output.resolve())}, indent=2))


def command_render_deck(args: argparse.Namespace) -> None:
    spec = load_deck(args.manifest)
    with tempfile.TemporaryDirectory(prefix="slidepoise-deck-") as temp:
        spec_path = Path(temp) / "presentation.json"
        write(spec_path, spec)
        run_checked(["node", str(RUNTIME / "js/scene_to_pptx.mjs"), "--input", str(spec_path),
                     "--output", str(args.output)], env=node_environment())
    print(json.dumps({"pptx": str(args.output.resolve()), "slides": len(spec["slides"]),
                      "slide_ids": [scene["slide_id"] for scene in spec["slides"]]}, indent=2))


def command_bundle_deck(args: argparse.Namespace) -> None:
    print(json.dumps(bundle_deck(args.manifest, args.output_dir, args.include), indent=2))


def command_verify_bundle(args: argparse.Namespace) -> None:
    print(json.dumps(verify_bundle(args.bundle_dir), indent=2))


def preview_font_environment(env: dict[str, str], directory: Path) -> dict:
    """Expose macOS system fonts to headless Fontconfig without changing the host."""
    configured = env.get("FONTCONFIG_FILE")
    if configured:
        config = Path(configured).expanduser()
        return {"fontconfig_source": "configured", "fontconfig_file": configured,
                "fontconfig_sha256": hashlib.sha256(config.read_bytes()).hexdigest() if config.is_file() else None}
    if sys.platform != "darwin":
        return {"fontconfig_source": "renderer_default"}
    candidates = ("/System/Library/Fonts", "/Library/Fonts", f"{Path.home().as_posix()}/Library/Fonts")
    directories = [item for item in candidates if Path(item).is_dir()]
    if not directories:
        return {"fontconfig_source": "renderer_default"}
    config = directory / "preview-fonts.conf"
    entries = "".join(f"<dir>{escape(item)}</dir>" for item in directories)
    config.write_text(f'<?xml version="1.0"?><fontconfig>{entries}<cachedir>{escape(str(directory / "font-cache"))}</cachedir></fontconfig>', encoding="utf-8")
    env["FONTCONFIG_FILE"] = str(config)
    return {"fontconfig_source": "macos_system_font_directories", "font_directories": directories}


def preview_settings(args: argparse.Namespace) -> tuple[dict[str, str], str, str]:
    env = dict(os.environ)
    font_config = getattr(args, "font_config", None)
    if font_config:
        if not font_config.is_file():
            raise SystemExit(f"Fontconfig file does not exist: {font_config}")
        env["FONTCONFIG_FILE"] = str(font_config.resolve())
    from slidepoise.preview_tools import find_preview_tool
    office = find_preview_tool("office")
    if not office:
        raise SystemExit("No LibreOffice/soffice renderer is available. Use the host's native PPTX rendering capability and persist a raster if possible.")
    pdftoppm = find_preview_tool("pdftoppm")
    if not pdftoppm:
        raise SystemExit("pdftoppm is required for the packaged render-preview path. Use the host's native PPTX rendering capability instead.")
    if args.dpi <= 0:
        raise ArtifactError("Preview DPI must be positive")
    return env, office, pdftoppm


def convert_preview_pdf(pptx: Path, directory: Path, env: dict[str, str], office: str) -> tuple[Path, dict]:
    font_evidence = preview_font_environment(env, directory)
    run_checked([office, "-env:UserInstallation=" + (directory / "office-profile").as_uri(),
                 "--headless", "--convert-to", "pdf", "--outdir", str(directory), str(pptx.resolve())], env=env)
    pdf = directory / (pptx.stem + ".pdf")
    if not pdf.is_file():
        raise ArtifactError("PPTX render did not produce the expected PDF")
    return pdf, font_evidence


def command_render_preview(args: argparse.Namespace) -> None:
    env, office, pdftoppm = preview_settings(args)
    page = getattr(args, "slide_number", 1)
    if page < 1:
        raise ArtifactError("Slide number must be positive")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    source_digest = file_hash(args.pptx)
    with tempfile.TemporaryDirectory(prefix="slidepoise-render-") as temp:
        temp_path = Path(temp)
        pdf, font_evidence = convert_preview_pdf(args.pptx, temp_path, env, office)
        prefix = temp_path / "slide"
        run_checked([pdftoppm, "-png", "-f", str(page), "-singlefile", "-r", str(args.dpi), str(pdf), str(prefix)])
        rendered = prefix.with_suffix(".png")
        if not rendered.is_file():
            raise SystemExit("PPTX render did not produce a PNG")
        text_evidence = rendered_text_evidence(args.pptx, pdf, page=page)
        if file_hash(args.pptx) != source_digest:
            raise SystemExit("PowerPoint changed during rendering. Retry with the latest file.")
        with tempfile.NamedTemporaryFile(dir=args.output.parent, suffix=".png", delete=False) as staged:
            staged_path = Path(staged.name)
        try:
            shutil.copyfile(rendered, staged_path)
            staged_path.replace(args.output)
        finally:
            staged_path.unlink(missing_ok=True)
        evidence_path = args.output.with_suffix(".text-evidence.json")
        write(evidence_path, text_evidence)
        write(args.output.with_suffix(".source.json"), {"source_sha256": source_digest,
              "render_sha256": file_hash(args.output), "slide_number": page, "dpi": args.dpi,
              "rendered_text": {"path": evidence_path.name, "sha256": file_hash(evidence_path)},
              "font_environment": font_evidence})
    print(json.dumps({"render": str(args.output.resolve()),
                      "rendered_text": text_evidence_summary(text_evidence, evidence_path)}, indent=2))


def rendered_text_evidence(pptx: Path, pdf: Path, *, page: int | None = None) -> dict:
    from slidepoise.rendered_text import collect_rendered_table_text
    evidence = collect_rendered_table_text(pptx, pdf)
    if page is not None:
        evidence["slide_number"] = page
        for field in ("cells", "discrepancies"):
            if field in evidence:
                evidence[field] = [item for item in evidence[field] if item["slide_number"] == page]
    return evidence


def text_evidence_summary(evidence: dict, path: Path) -> dict:
    """Surface diagnostics to the calling Agent without a quality verdict."""
    return {"path": str(path.resolve()), "available": evidence.get("available", False),
            "reason": evidence.get("reason"),
            "cells_checked": len(evidence.get("cells", [])) if evidence.get("available") else None,
            "discrepancies": len(evidence.get("discrepancies", [])) if evidence.get("available") else None,
            "scope": "Native table words only. Inspect the images for other text, geometry, relationships and visual quality.",
            "agent_interpretation_required": True}


def make_preview_contact_sheet(pages: list[Path], output: Path) -> None:
    """Provide an ordered overview for host visual review without assigning scores."""
    from PIL import Image, ImageDraw

    columns = min(3, len(pages))
    width, margin, label_height = 480, 16, 24
    with Image.open(pages[0]) as first:
        height = round(width * first.height / first.width)
    rows = (len(pages) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * (width + margin) + margin,
                              rows * (height + label_height + margin) + margin), "#E7E7E7")
    draw = ImageDraw.Draw(sheet)
    for index, page in enumerate(pages):
        x = margin + (index % columns) * (width + margin)
        y = margin + (index // columns) * (height + label_height + margin)
        with Image.open(page) as source:
            thumbnail = source.convert("RGB")
            thumbnail.thumbnail((width, height), Image.Resampling.LANCZOS)
            sheet.paste(thumbnail, (x, y))
        draw.text((x, y + height + 6), f"{index + 1:02d}", fill="#333333")
    sheet.save(output)


def command_render_deck_preview(args: argparse.Namespace) -> None:
    env, office, pdftoppm = preview_settings(args)
    output_dir = args.output_dir.resolve()
    if output_dir.exists():
        raise ArtifactError(f"Preview output already exists. Choose a new directory. {output_dir}")
    source_digest = file_hash(args.pptx)
    try:
        with zipfile.ZipFile(args.pptx) as package:
            presentation = ElementTree.fromstring(package.read("ppt/presentation.xml"))
    except (zipfile.BadZipFile, KeyError, ElementTree.ParseError) as error:
        raise ArtifactError(f"Cannot read the PowerPoint presentation part in {args.pptx}. {error}") from error
    count = len(presentation.findall("./{http://schemas.openxmlformats.org/presentationml/2006/main}sldIdLst/"
                                    "{http://schemas.openxmlformats.org/presentationml/2006/main}sldId"))
    if not count:
        raise ArtifactError("PowerPoint contains no slides")
    output_dir.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".slidepoise-preview-", dir=output_dir.parent) as temp:
        temp_path = Path(temp)
        pdf, font_evidence = convert_preview_pdf(args.pptx, temp_path, env, office)
        raw = temp_path / "raw"
        raw.mkdir()
        run_checked([pdftoppm, "-png", "-r", str(args.dpi), str(pdf), str(raw / "slide")])
        rendered = sorted(raw.glob("slide-*.png"), key=lambda path: int(path.stem.split("-")[-1]))
        if len(rendered) != count:
            raise ArtifactError(f"Preview renderer produced {len(rendered)} pages for a {count}-slide deck")
        staged = temp_path / "preview"
        staged.mkdir()
        text_evidence = rendered_text_evidence(args.pptx, pdf)
        evidence_path = staged / "rendered-text-evidence.json"
        write(evidence_path, text_evidence)
        evidence_binding = {"path": evidence_path.name, "sha256": file_hash(evidence_path)}
        pages = []
        records = []
        for index, image in enumerate(rendered, start=1):
            destination = staged / f"slide-{index:03d}.png"
            image.rename(destination)
            binding = {"source_sha256": source_digest, "render_sha256": file_hash(destination),
                       "rendered_text": evidence_binding,
                       "slide_number": index, "dpi": args.dpi, "font_environment": font_evidence}
            write(destination.with_suffix(".source.json"), binding)
            records.append({"slide_number": index, "render": destination.name,
                            "sha256": binding["render_sha256"]})
            pages.append(destination)
        make_preview_contact_sheet(pages, staged / "contact-sheet.png")
        shutil.copyfile(pdf, staged / "presentation.pdf")
        record = {"schema_version": "1.0", "source_sha256": source_digest, "dpi": args.dpi,
                  "rendered_text": evidence_binding,
                  "font_environment": font_evidence, "slides": records,
                  "contact_sheet": {"path": "contact-sheet.png", "sha256": file_hash(staged / "contact-sheet.png")},
                  "pdf": {"path": "presentation.pdf", "sha256": file_hash(staged / "presentation.pdf")}}
        write(staged / "preview-manifest.json", record)
        if file_hash(args.pptx) != source_digest:
            raise ArtifactError("PowerPoint changed during rendering. Retry with the latest file.")
        staged.rename(output_dir)
    print(json.dumps({"preview_dir": str(output_dir), "slides": count,
                      "contact_sheet": str(output_dir / "contact-sheet.png"),
                      "rendered_text": text_evidence_summary(text_evidence, output_dir / evidence_path.name),
                      "manifest": str(output_dir / "preview-manifest.json")}, indent=2))

def command_audit_text(args: argparse.Namespace) -> None:
    run_checked([sys.executable, str(RUNTIME / "scripts/audit_powerpoint_text.py"), str(args.pptx)])



def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="Measure generated slide targets, compile editable scenes and publish bound artifacts.")
    sub = root.add_subparsers(dest="command", required=True)

    measure = sub.add_parser("measure", help="Measure host-authored entities against the target image with OpenCV")
    measure.add_argument("--image", type=Path, required=True)
    measure.add_argument("--semantic-map", type=Path, required=True)
    measure.add_argument("--output-dir", type=Path, required=True)
    measure.add_argument("--upstream-handoff", type=Path)
    measure.add_argument("--config", type=Path, required=True)
    measure.add_argument("--sam", choices=["auto", "never", "required"], help=argparse.SUPPRESS)
    measure.set_defaults(func=command_measure)

    contract = sub.add_parser("build-contract", help="Bind measured entities to editable reconstruction units")
    contract.add_argument("--measured-scene", type=Path, required=True)
    contract.add_argument("--config", type=Path, required=True)
    contract.add_argument("--output", type=Path, required=True)
    contract.set_defaults(func=command_build_contract)

    compile_scene = sub.add_parser("compile-scene", help="Compile the measured scene and reconstruction contract")
    compile_scene.add_argument("--measured-scene", type=Path, required=True)
    compile_scene.add_argument("--contract", type=Path, required=True)
    compile_scene.add_argument("--config", type=Path, required=True)
    compile_scene.add_argument("--slide-id", default="slide-01")
    compile_scene.add_argument("--output", type=Path, required=True)
    compile_scene.set_defaults(func=command_compile_scene)

    reconstruct = sub.add_parser("reconstruct-slide", help="Run measurement, contract construction and scene compilation for one slide")
    reconstruct.add_argument("--image", type=Path, required=True)
    reconstruct.add_argument("--semantic-map", type=Path, required=True)
    reconstruct.add_argument("--upstream-handoff", type=Path, required=True)
    reconstruct.add_argument("--config", type=Path, required=True)
    reconstruct.add_argument("--slide-id", required=True)
    reconstruct.add_argument("--output-dir", type=Path, required=True)
    reconstruct.add_argument("--sam", choices=["auto", "never", "required"], help=argparse.SUPPRESS)
    reconstruct.set_defaults(func=command_reconstruct_slide)

    render = sub.add_parser("render-pptx", help="Build an editable PowerPoint from one compiled scene")
    render.add_argument("--scene", type=Path, required=True)
    render.add_argument("--config", type=Path, required=True)
    render.add_argument("--output", type=Path, required=True)
    render.add_argument("--title")
    render.add_argument("--language", default="en-US")
    render.set_defaults(func=command_render_pptx)

    deck = sub.add_parser("render-deck", help="Build an editable PowerPoint in manifest order")
    deck.add_argument("--manifest", type=Path, required=True)
    deck.add_argument("--output", type=Path, required=True)
    deck.set_defaults(func=command_render_deck)

    bundle = sub.add_parser("bundle-deck", help="Copy compiled scenes, raster assets and optional source evidence into a portable directory")
    bundle.add_argument("--manifest", type=Path, required=True)
    bundle.add_argument("--output-dir", type=Path, required=True, help="New directory for the portable bundle")
    bundle.add_argument("--include", type=Path, action="append", default=[], help="Source file or directory to preserve under evidence, repeatable")
    bundle.set_defaults(func=command_bundle_deck)

    verify = sub.add_parser("verify-bundle", help="Verify every bundled file and the ordered scene inputs")
    verify.add_argument("--bundle-dir", type=Path, required=True)
    verify.set_defaults(func=command_verify_bundle)

    preview = sub.add_parser("render-preview", help="Render one PowerPoint page and bind it to the source file")
    preview.add_argument("--pptx", type=Path, required=True)
    preview.add_argument("--output", type=Path, required=True)
    preview.add_argument("--dpi", type=int, default=160)
    preview.add_argument("--slide-number", type=int, default=1)
    preview.add_argument("--font-config", type=Path, help="Optional run-local Fontconfig file for the preview renderer")
    preview.set_defaults(func=command_render_preview)

    deck_preview = sub.add_parser("render-deck-preview", help="Render every page, a PDF and an ordered contact sheet in one conversion")
    deck_preview.add_argument("--pptx", type=Path, required=True)
    deck_preview.add_argument("--output-dir", type=Path, required=True, help="New directory for previews and source bindings")
    deck_preview.add_argument("--dpi", type=int, default=120)
    deck_preview.add_argument("--font-config", type=Path)
    deck_preview.set_defaults(func=command_render_deck_preview)

    audit = sub.add_parser("audit-text", help="Inspect native PowerPoint text structure")
    audit.add_argument("--pptx", type=Path, required=True)
    audit.set_defaults(func=command_audit_text)

    return root


def main() -> None:
    args = parser().parse_args()
    try:
        args.func(args)
    except (ArtifactError, OSError, zipfile.BadZipFile, ElementTree.ParseError) as error:
        raise SystemExit(str(error)) from None


if __name__ == "__main__":
    main()
