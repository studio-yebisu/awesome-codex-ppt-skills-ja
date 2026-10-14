"""Portable constructor inputs and content-bound presentation bundles.

This boundary checks files and structural facts. It never assigns visual quality
or decides whether a presentation is ready for delivery.
"""
from __future__ import annotations

import copy
import hashlib
import json
import math
import shutil
import tempfile
from pathlib import Path


class ArtifactError(ValueError):
    """An actionable failure in a presentation input or artifact binding."""


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> dict:
    def reject_constant(value: str) -> None:
        raise ValueError(f"Non-finite number {value}")

    try:
        value = json.loads(path.read_text(encoding="utf-8"),
                           parse_constant=reject_constant)
    except (OSError, ValueError) as error:
        raise ArtifactError(f"Cannot read JSON from {path}. {error}") from error
    if not isinstance(value, dict):
        raise ArtifactError(f"JSON document must be an object in {path}")
    return value


def write_json(path: Path, data: dict) -> None:
    """Publish one complete JSON document without truncating an existing file."""
    content = json.dumps(data, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    staged_path = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent, delete=False) as staged:
            staged_path = Path(staged.name)
            staged.write(content)
            staged.flush()
        staged_path.replace(path)
    finally:
        if staged_path is not None:
            staged_path.unlink(missing_ok=True)


def resolve_scene_paths(scene: dict, scene_file: Path) -> dict:
    """Resolve raster inputs without changing the caller's scene or using cwd.

    Scene-relative paths are canonical. The parent-directory fallback retains
    support for older run-root-relative scenes, provided it is unambiguous.
    """
    resolved_scene = copy.deepcopy(scene)
    path_base = scene.get("asset_path_base")
    if path_base not in (None, "scene"):
        raise ArtifactError(f"Unsupported asset_path_base in {scene_file}. {path_base}")
    for item in resolved_scene.get("objects", []):
        value = item.get("source_path")
        if not value:
            if item.get("kind") == "image":
                raise ArtifactError(f"Image {item.get('id')} has no source_path in {scene_file}")
            continue
        if not isinstance(value, str):
            raise ArtifactError(f"Image source_path must be a string in {scene_file}")
        source = Path(value).expanduser()
        candidates = [source] if source.is_absolute() else [scene_file.parent / source]
        if not source.is_absolute() and path_base is None:
            candidates.append(scene_file.parent.parent / source)
        matches = {candidate.resolve() for candidate in candidates if candidate.is_file()}
        if not matches:
            raise ArtifactError(f"Scene raster source does not exist for {item.get('id')} in {scene_file}. {value}")
        if len(matches) > 1:
            raise ArtifactError(f"Scene raster path is ambiguous in {scene_file}. Use an explicit scene-relative path for {value}")
        item["source_path"] = str(matches.pop())
    return resolved_scene


def require_reconstruction_lineage(scene: dict, *, label: str) -> None:
    report = scene.get("compiler_report")
    if not isinstance(report, dict):
        raise ArtifactError(f"{label} is not a packaged SlidePoise constructor scene. compiler_report is missing")
    measurement = report.get("measurement")
    if not isinstance(measurement, dict) or measurement.get("engine") != "OpenCV" or not measurement.get("opencv"):
        raise ArtifactError(f"{label} has no packaged OpenCV measurement lineage")
    bindings = report.get("input_bindings")
    required = ("measured_scene_sha256", "reconstruction_contract_sha256", "resolved_design_sha256")
    if not isinstance(bindings, dict) or any(not bindings.get(key) for key in required):
        raise ArtifactError(f"{label} is missing measured reconstruction input bindings")


def validate_scene(scene: dict, *, label: str) -> None:
    dimensions = scene.get("dimensions_px")
    if not isinstance(dimensions, list) or len(dimensions) != 2 or any(
        isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0
        for value in dimensions
    ):
        raise ArtifactError(f"{label} requires two positive finite dimensions_px")
    objects = scene.get("objects")
    if not isinstance(objects, list):
        raise ArtifactError(f"{label} requires an objects array")
    seen: set[str] = set()
    supported = {"textbox", "shape", "image", "connector_graph", "table", "chart", "freeform"}
    for index, item in enumerate(objects, start=1):
        if not isinstance(item, dict):
            raise ArtifactError(f"{label} object {index} must be an object")
        identity = item.get("id")
        if not isinstance(identity, str) or not identity.strip() or identity in seen:
            raise ArtifactError(f"{label} requires unique non-empty object IDs. Found {identity!r}")
        seen.add(identity)
        if item.get("kind") not in supported:
            raise ArtifactError(f"{label} object {identity} has an unsupported kind {item.get('kind')!r}")
    require_reconstruction_lineage(scene, label=label)


def presentation_spec(scenes: list[dict], *, title: str, language: str, theme: dict | None = None,
                      company: str = "") -> dict:
    if not scenes:
        raise ArtifactError("At least one slide scene is required")
    for index, scene in enumerate(scenes, start=1):
        validate_scene(scene, label=f"Slide {index}")
        if scene.get("dimensions_px") != scenes[0].get("dimensions_px"):
            raise ArtifactError(f"Slide {index} dimensions do not match the first slide")
    if theme is not None and not isinstance(theme, dict):
        raise ArtifactError("Presentation theme must be an object")
    return {"title": title, "company": company, "language": language, "theme": theme or {}, "slides": scenes}


def load_deck(manifest_path: Path) -> dict:
    """Load ordered scenes through the same boundary for rendering and bundling."""
    manifest_path = manifest_path.resolve()
    manifest = read_json(manifest_path)
    entries = manifest.get("slides")
    if not isinstance(entries, list) or not entries:
        raise ArtifactError("Deck scene manifest requires a non-empty slides array")
    seen: set[str] = set()
    scenes: list[dict] = []
    for index, entry in enumerate(entries, start=1):
        if not isinstance(entry, dict):
            raise ArtifactError(f"Slide entry {index} must be an object")
        slide_id = entry.get("slide_id")
        if not isinstance(slide_id, str) or not slide_id.strip():
            raise ArtifactError(f"Slide entry {index} requires slide_id")
        if slide_id in seen:
            raise ArtifactError(f"Duplicate slide_id in deck scene manifest. {slide_id}")
        seen.add(slide_id)
        value = entry.get("scene")
        if isinstance(value, dict):
            scene_file, scene = manifest_path, value
        elif isinstance(value, str) and value.strip():
            scene_file = Path(value).expanduser()
            if not scene_file.is_absolute():
                scene_file = manifest_path.parent / scene_file
            scene = read_json(scene_file)
        else:
            raise ArtifactError(f"Slide {slide_id} requires a scene object or path")
        validate_scene(scene, label=f"Slide {slide_id}")
        scene = resolve_scene_paths(scene, scene_file)
        if scene.get("slide_id") and scene["slide_id"] != slide_id:
            raise ArtifactError(f"Slide {slide_id} references a scene for {scene['slide_id']}")
        scene["slide_id"] = slide_id
        scenes.append(scene)
    return presentation_spec(scenes, title=manifest.get("title") or "SlidePoise presentation",
                             company=manifest.get("company") or "", language=manifest.get("language") or "en-US",
                             theme=manifest.get("theme"))


def _inventory(root: Path) -> list[dict]:
    return [{"path": path.relative_to(root).as_posix(), "sha256": file_hash(path), "bytes": path.stat().st_size}
            for path in sorted(root.rglob("*")) if path.is_file() and path != root / "bundle.json"]


def bundle_deck(manifest_path: Path, output_dir: Path, includes: list[Path] | None = None) -> dict:
    """Copy a renderable deck and optional exact evidence trees into a new folder."""
    spec = load_deck(manifest_path)
    output_dir = output_dir.resolve()
    if output_dir.exists():
        raise ArtifactError(f"Bundle output already exists. Choose a new directory. {output_dir}")
    sources = [source.resolve() for source in includes or []]
    if len({source.name for source in sources}) != len(sources):
        raise ArtifactError("Included evidence paths must have distinct file or directory names")
    for source in sources:
        if not source.exists():
            raise ArtifactError(f"Included evidence does not exist. {source}")
        if output_dir.is_relative_to(source):
            raise ArtifactError("Bundle output must be outside every included evidence directory")
        if source.is_dir() and any(item.is_symlink() for item in source.rglob("*")):
            raise ArtifactError(f"Included evidence contains symbolic links. Include the explicit source files instead. {source}")
    output_dir.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".slidepoise-bundle-", dir=output_dir.parent) as temp:
        root = Path(temp) / "bundle"
        root.mkdir()
        entries = []
        for index, scene in enumerate(spec["slides"], start=1):
            scene["asset_path_base"] = "scene"
            for item in scene["objects"]:
                if not item.get("source_path"):
                    continue
                source = Path(item["source_path"])
                digest = file_hash(source)
                relative = Path("assets") / (digest + source.suffix.lower())
                destination = root / relative
                destination.parent.mkdir(exist_ok=True)
                if not destination.exists():
                    shutil.copyfile(source, destination)
                if file_hash(destination) != digest:
                    raise ArtifactError(f"Raster source changed while bundling. {source}")
                item["source_path"] = (Path("..") / relative).as_posix()
            relative_scene = Path("scenes") / f"slide-{index:03d}.json"
            write_json(root / relative_scene, scene)
            entries.append({"slide_id": scene["slide_id"], "scene": relative_scene.as_posix()})
        evidence = []
        for source in sources:
            relative = Path("evidence") / source.name
            destination = root / relative
            destination.parent.mkdir(exist_ok=True)
            if source.is_dir():
                shutil.copytree(source, destination)
            else:
                shutil.copyfile(source, destination)
            evidence.append(relative.as_posix())
        manifest = {key: value for key, value in spec.items() if key != "slides"}
        manifest.update({"schema_version": "1.0", "slides": entries})
        write_json(root / "deck-scenes.json", manifest)
        record = {"schema_version": "1.0", "manifest": "deck-scenes.json", "slide_ids": [entry["slide_id"] for entry in entries],
                  "evidence": evidence, "files": _inventory(root)}
        write_json(root / "bundle.json", record)
        verify_bundle(root)
        root.rename(output_dir)
    return {"bundle_dir": str(output_dir), "manifest": str(output_dir / "deck-scenes.json"),
            "slides": len(entries), "files": len(record["files"]), "evidence": evidence}


def verify_bundle(root: Path) -> dict:
    """Check bundle completeness and hashes, then load its relative constructor inputs."""
    root = root.resolve()
    if any(path.is_symlink() for path in root.rglob("*")):
        raise ArtifactError("Bundle contains symbolic links. Verification requires regular files and directories")
    record = read_json(root / "bundle.json")
    if record.get("schema_version") != "1.0" or not isinstance(record.get("files"), list):
        raise ArtifactError("Unsupported or malformed bundle manifest")
    expected: set[str] = set()
    for entry in record["files"]:
        relative = entry.get("path") if isinstance(entry, dict) else None
        if not isinstance(relative, str) or not relative or relative in expected:
            raise ArtifactError("Bundle file inventory requires unique relative paths")
        path = root / relative
        if Path(relative).is_absolute() or not path.resolve().is_relative_to(root) or path.is_symlink():
            raise ArtifactError(f"Bundle file escapes its directory. {relative}")
        expected.add(relative)
        if not path.is_file() or file_hash(path) != entry.get("sha256") or path.stat().st_size != entry.get("bytes"):
            raise ArtifactError(f"Bundle file is missing or changed. {relative}")
    actual = {entry["path"] for entry in _inventory(root)}
    if actual != expected:
        raise ArtifactError(f"Bundle file inventory differs. Unlisted files {sorted(actual - expected)}")
    manifest = record.get("manifest")
    if manifest not in expected:
        raise ArtifactError("Bundle manifest is not bound in the file inventory")
    spec = load_deck(root / manifest)
    if [scene["slide_id"] for scene in spec["slides"]] != record.get("slide_ids"):
        raise ArtifactError("Bundle slide order differs from its manifest")
    for scene in spec["slides"]:
        for item in scene["objects"]:
            if item.get("source_path") and not Path(item["source_path"]).is_relative_to(root):
                raise ArtifactError(f"Bundle raster source is outside its directory. {item['id']}")
    return {"bundle_dir": str(root), "slides": len(spec["slides"]), "verified_files": len(expected),
            "slide_ids": record["slide_ids"]}
