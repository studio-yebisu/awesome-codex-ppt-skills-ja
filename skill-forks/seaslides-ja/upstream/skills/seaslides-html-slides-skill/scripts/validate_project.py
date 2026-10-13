#!/usr/bin/env python3
"""
HTML Slide Project Validator

Validates deterministic source contracts and current compiler receipts for a
SeaSlides HTML project. Visual heuristics remain review work, not static gates.

Project mode checks source structure, speaker notes, TCS, referenced images,
pseudocode marker pairing, and (at the build gate) the compiler manifest plus
published artifact structure. It deliberately does not enforce mode cadence,
layout diversity, density, or other visual heuristics.

Usage:
    python3 validate_project.py <project_path> --source-only
    python3 validate_project.py <project_path> --require-build --artifact-profile visual
    python3 validate_project.py <content.html> [template.css]   # legacy single-file mode
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import posixpath
import re
import sys
import zipfile
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from typing import Dict, List, Optional, Tuple
from urllib.parse import unquote, urlparse
from xml.etree import ElementTree as ET


# ============================================================
# Constants
# ============================================================

SCRIPTS_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPTS_DIR.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from runtime_environment import runtime_environment_fingerprint  # noqa: E402

# Standard-slide inline style allowlist. These values encode data, not decoration.
DATA_INLINE_STYLE_PROPERTIES = {
    'bar-fill': {'width', 'height', '--w', '--h'},
    'row-fill': {'width', '--w'},
    'progress-fill': {'width', '--w'},
    'vbar-fill': {'height', '--h'},
    'funnel-step': {'width', '--w'},
    'waterfall-bar': {'height', 'margin-top', '--h', '--offset'},
}
DATA_INLINE_VALUE_RE = re.compile(r'^(?:\d+(?:\.\d*)?|\.\d+)(?:px|%)$|^0$')
SIGNED_DATA_INLINE_VALUE_RE = re.compile(
    r'^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:px|%)$|^0$'
)
VALID_PROFILES = {'standard-project', 'theme-demo', 'scenario'}
ARTIFACT_PROFILES = {
    'current': {'svg', 'dom_audit'},
    'visual': {
        'svg', 'dom_audit', 'png', 'browser_png', 'overview', 'pdf',
        'render_fidelity',
    },
    'delivery': {
        'svg', 'dom_audit', 'png', 'browser_png', 'overview', 'pdf', 'pptx',
        'render_fidelity',
    },
}
ARTIFACT_PATHS = {
    'svg': ('output/svgs', 'directory'),
    'dom_audit': ('output/dom-audit.json', 'file'),
    'png': ('output/pngs', 'directory'),
    'png_dependency': ('output/pngs', 'directory'),
    'browser_png': ('output/browser_pngs', 'directory'),
    'overview': ('output/overview.png', 'file'),
    'pdf': ('output/slides.pdf', 'file'),
    'pptx': ('output/slides.pptx', 'file'),
    'render_fidelity': ('output/render-fidelity.json', 'file'),
}
ARTIFACT_PROFILE_FORMATS = {
    'visual': {'svg', 'png', 'browser_png', 'overview', 'pdf'},
    'delivery': {'svg', 'png', 'browser_png', 'overview', 'pdf', 'pptx'},
}
VOID_TAGS = {
    'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link',
    'meta', 'param', 'source', 'track', 'wbr',
}


class FragmentParser(HTMLParser):
    """Small dependency-free parser for deterministic source checks."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: List[str] = []
        self.slides: List[dict] = []
        self.open_slides: List[dict] = []
        self.tags: List[dict] = []
        self.top_level_elements: List[str] = []
        self.top_level_text: List[str] = []
        self.pseudocode_blocks: List[dict] = []
        self.open_pseudocode: List[dict] = []

    @staticmethod
    def _attrs(attrs) -> dict:
        return {str(name).lower(): value if value is not None else '' for name, value in attrs}

    def handle_starttag(self, tag: str, attrs) -> None:
        tag = tag.lower()
        attr_map = self._attrs(attrs)
        classes = set(attr_map.get('class', '').split())
        depth = len(self.stack)
        record = {'tag': tag, 'attrs': attr_map, 'classes': classes, 'depth': depth}
        self.tags.append(record)

        is_slide = tag == 'section' and 'slide' in classes
        if depth == 0 and not is_slide:
            self.top_level_elements.append(tag)
        if is_slide:
            slide = {
                'attrs': attr_map,
                'classes': classes,
                'headings': [],
                'depth': depth,
            }
            self.slides.append(slide)
            self.open_slides.append(slide)
        elif self.open_slides and re.fullmatch(r'h[1-6]', tag):
            self.open_slides[-1]['headings'].append(tag)

        if classes.intersection({'pseudocode', 'ps-algorithm', 'pseudocode-source'}):
            block = {'tag': tag, 'classes': classes, 'text': []}
            self.pseudocode_blocks.append(block)
            self.open_pseudocode.append(block)

        if tag not in VOID_TAGS:
            self.stack.append(tag)

    def handle_startendtag(self, tag: str, attrs) -> None:
        self.handle_starttag(tag, attrs)
        if tag.lower() not in VOID_TAGS:
            self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        for index in range(len(self.open_pseudocode) - 1, -1, -1):
            if self.open_pseudocode[index]['tag'] == tag:
                del self.open_pseudocode[index:]
                break
        if tag == 'section' and self.open_slides:
            self.open_slides.pop()
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index] == tag:
                del self.stack[index:]
                break

    def handle_data(self, data: str) -> None:
        for block in self.open_pseudocode:
            block['text'].append(data)
        if not self.stack and data.strip():
            self.top_level_text.append(data.strip())


def parse_fragment(text: str) -> FragmentParser:
    parser = FragmentParser()
    parser.feed(text)
    parser.close()
    return parser


def content_path(project_path: Path, entry: str) -> Path:
    """Resolve the content entry without accepting paths outside the project."""
    path = (project_path / entry).resolve()
    try:
        path.relative_to(project_path.resolve())
    except ValueError as error:
        raise ValueError(f"entry must stay inside the project: {entry}") from error
    return path


def canonical_entry(project_path: Path, entry: str) -> str:
    """Return a normalized project-relative entry for receipts and messages."""
    return content_path(project_path, entry).relative_to(project_path.resolve()).as_posix()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_directory(path: Path) -> str:
    digest = hashlib.sha256()
    for child in sorted(item for item in path.rglob('*') if item.is_file()):
        digest.update(child.relative_to(path).as_posix().encode('utf-8'))
        digest.update(b'\0')
        digest.update(bytes.fromhex(sha256_file(child)))
    return digest.hexdigest()


def _is_canonical_relative_posix(value: str) -> bool:
    """Accept only normalized, non-escaping POSIX receipt paths."""
    path = PurePosixPath(value)
    return (
        bool(value)
        and '\\' not in value
        and not path.is_absolute()
        and path.as_posix() == value
        and all(part not in {'.', '..'} for part in path.parts)
    )


SOURCE_RECEIPT_SCHEMA = 'seaslides-source-conversion/v1'
SHA256_RE = re.compile(r'^[0-9a-f]{64}$')


def _receipt_file_path(
    raw_path: object,
    receipt_path: Path,
    sources_root: Path,
    label: str,
) -> Tuple[Optional[Path], Optional[str]]:
    """Resolve a receipt-local file path without permitting project escapes."""
    if not isinstance(raw_path, str) or not raw_path:
        return None, f"SOURCE RECEIPT INVALID: {label}.path must be a non-empty string."
    candidate = Path(raw_path)
    if candidate.is_absolute():
        return None, f"SOURCE RECEIPT INVALID: {label}.path must be relative to its receipt."
    resolved = (receipt_path.parent / candidate).resolve()
    try:
        resolved.relative_to(sources_root)
    except ValueError:
        return None, (
            f"SOURCE RECEIPT UNSAFE: {label}.path escapes sources/: {raw_path!r}."
        )
    return resolved, None


def _receipt_fingerprint_errors(
    row: object,
    label: str,
) -> Tuple[Optional[dict], List[str]]:
    """Validate the common file-fingerprint fields without applying quality thresholds."""
    if not isinstance(row, dict):
        return None, [f"SOURCE RECEIPT INVALID: {label} must be an object."]
    errors: list[str] = []
    fingerprint = row.get('sha256')
    if not isinstance(fingerprint, str) or not SHA256_RE.fullmatch(fingerprint):
        errors.append(f"SOURCE RECEIPT INVALID: {label}.sha256 must be 64 lowercase hex characters.")
    size = row.get('size_bytes')
    if isinstance(size, bool) or not isinstance(size, int) or size < 0:
        errors.append(f"SOURCE RECEIPT INVALID: {label}.size_bytes must be a non-negative integer.")
    return row, errors


def _fingerprint_matches(path: Path, row: dict) -> Tuple[bool, Optional[str]]:
    """Compare a receipt fingerprint without leaking filesystem exceptions."""
    try:
        return (
            row.get('sha256') == sha256_file(path)
            and row.get('size_bytes') == path.stat().st_size,
            None,
        )
    except OSError as error:
        return False, str(error)


def check_source_conversion_receipts(project_path: Path) -> Tuple[List[str], List[str]]:
    """Validate conversion provenance receipts stored below ``sources/``.

    A receipt is optional, but once present it is a blocking integrity contract.
    URL sources are intentionally not fetched again; their captured fingerprint is
    validated structurally while local source and output files are re-fingerprinted.
    """
    errors: List[str] = []
    warnings: List[str] = []
    sources_dir = project_path / 'sources'
    if not sources_dir.is_dir():
        return errors, warnings

    sources_root = sources_dir.resolve()
    try:
        sources_root.relative_to(project_path.resolve())
    except ValueError:
        return ["SOURCE RECEIPT UNSAFE: sources/ resolves outside the project."], warnings
    for receipt_path in sorted(
        path for path in sources_dir.rglob('*')
        if path.is_file() and path.name.endswith('.receipt.json')
    ):
        display = receipt_path.relative_to(project_path).as_posix()
        try:
            receipt_path.resolve().relative_to(sources_root)
        except ValueError:
            errors.append(f"SOURCE RECEIPT UNSAFE: receipt escapes sources/: {display}.")
            continue
        try:
            receipt = json.loads(receipt_path.read_text(encoding='utf-8'))
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            errors.append(f"SOURCE RECEIPT INVALID: {display}: {error}.")
            continue
        if not isinstance(receipt, dict):
            errors.append(f"SOURCE RECEIPT INVALID: {display}: top-level JSON must be an object.")
            continue
        if receipt.get('schema') != SOURCE_RECEIPT_SCHEMA:
            errors.append(f"SOURCE RECEIPT INVALID: {display}: unsupported schema {receipt.get('schema')!r}.")
        status = receipt.get('status')
        if status not in {'pass', 'pass_with_warnings'}:
            errors.append(f"SOURCE RECEIPT INVALID: {display}: status must be pass or pass_with_warnings.")

        converter = receipt.get('converter')
        if not isinstance(converter, dict):
            errors.append(f"SOURCE RECEIPT INVALID: {display}: converter must be an object.")
        else:
            for field in ('name', 'version'):
                if not isinstance(converter.get(field), str) or not converter[field].strip():
                    errors.append(
                        f"SOURCE RECEIPT INVALID: {display}: converter.{field} must be a non-empty string."
                    )

        receipt_warnings = receipt.get('warnings')
        valid_warnings = (
            isinstance(receipt_warnings, list)
            and all(isinstance(item, str) and item.strip() for item in receipt_warnings)
        )
        if not valid_warnings:
            errors.append(
                f"SOURCE RECEIPT INVALID: {display}: warnings must be an array of non-empty strings."
            )
            receipt_warnings = []
        elif len(receipt_warnings) != len(set(receipt_warnings)):
            errors.append(f"SOURCE RECEIPT INVALID: {display}: warnings must not contain duplicates.")
        if status == 'pass' and receipt_warnings:
            errors.append(f"SOURCE RECEIPT INVALID: {display}: pass status cannot contain warnings.")
        if status == 'pass_with_warnings' and not receipt_warnings:
            errors.append(
                f"SOURCE RECEIPT INVALID: {display}: pass_with_warnings requires at least one warning."
            )
        if status == 'pass_with_warnings' and receipt_warnings:
            warnings.append(
                f"SOURCE CONVERSION REVIEW: {display} records {len(receipt_warnings)} warning(s)."
            )

        output, output_errors = _receipt_fingerprint_errors(receipt.get('output'), 'output')
        errors.extend(f"{display}: {error}" for error in output_errors)
        if output is not None:
            if output.get('kind') != 'file':
                errors.append(f"SOURCE RECEIPT INVALID: {display}: output.kind must be 'file'.")
            output_path, path_error = _receipt_file_path(
                output.get('path'), receipt_path, sources_root, 'output'
            )
            if path_error:
                errors.append(f"{display}: {path_error}")
            elif output_path is not None:
                if not output_path.is_file():
                    errors.append(f"SOURCE RECEIPT STALE: {display}: output no longer exists: {output.get('path')!r}.")
                else:
                    matches, read_error = _fingerprint_matches(output_path, output)
                    if read_error:
                        errors.append(f"SOURCE RECEIPT UNREADABLE: {display}: output: {read_error}.")
                    elif not matches:
                        errors.append(f"SOURCE RECEIPT STALE: {display}: output changed after conversion.")
                    elif output.get('size_bytes') == 0:
                        errors.append(f"SOURCE RECEIPT INVALID: {display}: output is empty.")

        source, source_errors = _receipt_fingerprint_errors(receipt.get('source'), 'source')
        errors.extend(f"{display}: {error}" for error in source_errors)
        if source is None:
            continue
        source_kind = source.get('kind')
        if source_kind == 'file':
            source_path, path_error = _receipt_file_path(
                source.get('path'), receipt_path, sources_root, 'source'
            )
            if path_error:
                errors.append(f"{display}: {path_error}")
            elif source_path is not None:
                if not source_path.is_file():
                    errors.append(f"SOURCE RECEIPT STALE: {display}: source no longer exists: {source.get('path')!r}.")
                else:
                    matches, read_error = _fingerprint_matches(source_path, source)
                    if read_error:
                        errors.append(f"SOURCE RECEIPT UNREADABLE: {display}: source: {read_error}.")
                    elif not matches:
                        errors.append(f"SOURCE RECEIPT STALE: {display}: source changed after conversion.")
        elif source_kind == 'url':
            if not isinstance(source.get('uri'), str) or not source['uri'].strip():
                errors.append(f"SOURCE RECEIPT INVALID: {display}: URL source.uri must be a non-empty string.")
        else:
            errors.append(f"SOURCE RECEIPT INVALID: {display}: source.kind must be 'file' or 'url'.")

    return errors, warnings


def is_allowed_data_style_for_classes(classes: set[str], style_text: str) -> bool:
    """Return whether classes and declarations encode allowlisted data geometry."""
    allowed_properties = set()
    for class_name in classes:
        allowed_properties.update(DATA_INLINE_STYLE_PROPERTIES.get(class_name, set()))
    if not allowed_properties:
        return False

    declarations = [part.strip() for part in style_text.split(';') if part.strip()]
    if not declarations:
        return False

    for declaration in declarations:
        if ':' not in declaration:
            return False
        property_name, value = (part.strip() for part in declaration.split(':', 1))
        property_name = property_name.lower()
        if property_name not in allowed_properties:
            return False
        value_pattern = (
            SIGNED_DATA_INLINE_VALUE_RE
            if property_name in {'margin-top', '--offset'}
            else DATA_INLINE_VALUE_RE
        )
        if not value_pattern.fullmatch(value.lower()):
            return False

    return True


def is_allowed_data_inline_style(tag_text: str, style_text: str) -> bool:
    """Backward-compatible tag-text wrapper for the canonical allowlist."""
    class_match = re.search(
        r'\bclass\s*=\s*(["\'])(.*?)\1', tag_text, re.IGNORECASE | re.DOTALL
    )
    if not class_match:
        return False
    return is_allowed_data_style_for_classes(set(class_match.group(2).split()), style_text)


# ============================================================
# CSS Class Cross-Referencing Helpers
# ============================================================

def extract_defined_classes_from_css(css_text: str) -> set:
    """Extract all class names defined in CSS text."""
    classes = re.findall(r"\.([a-zA-Z][a-zA-Z0-9_-]*)", css_text)
    return set(classes)


def extract_defined_classes_from_html(template_text: str) -> set:
    """Extract all class names defined in <style> blocks of an HTML file."""
    style_blocks = re.findall(r"<style[^>]*>(.*?)</style>", template_text, re.DOTALL)
    css_text = "\n".join(style_blocks)
    return extract_defined_classes_from_css(css_text)


# Built-in classes that are always valid (HTML semantics, not CSS-defined)
BUILTIN_CLASSES = {"slide", "dark", "light", "hero", "grey", "surface"}


# ============================================================
# Validation Functions
# ============================================================

def _read_source_entry(project_path: Path, entry: str) -> Optional[str]:
    """Read a source entry for a secondary check without duplicating I/O errors.

    ``check_content_file`` owns missing-file, regular-file, UTF-8, and readability
    diagnostics. Secondary checks simply skip when that primary contract failed.
    """
    path = content_path(project_path, entry)
    if not path.is_file():
        return None
    try:
        return path.read_text(encoding='utf-8')
    except (OSError, UnicodeError):
        return None


def check_content_file(project_path: Path, entry: str = 'content.html') -> Tuple[List[str], List[str]]:
    """Check that the selected content entry has proper slide structure."""
    errors = []
    warnings = []

    entry = canonical_entry(project_path, entry)
    required = ['index-template.html', 'template.css', entry]
    sources: dict[str, str] = {}
    for relative in required:
        path = project_path / relative
        if path.is_symlink():
            try:
                path.resolve(strict=True).relative_to(project_path.resolve())
            except (OSError, ValueError):
                errors.append(
                    f"SOURCE VIOLATION: required file symlink escapes project: {relative}."
                )
                continue
        if not path.is_file():
            errors.append(
                f"SOURCE MISSING: required file is absent or not a regular file: {relative}."
            )
            continue
        try:
            sources[relative] = path.read_text(encoding='utf-8')
        except UnicodeError as error:
            errors.append(f"SOURCE INVALID: {relative} is not valid UTF-8 ({error}).")
        except OSError as error:
            errors.append(f"SOURCE UNREADABLE: {relative}: {error}.")

    content = sources.get(entry)
    if content is None:
        return errors, warnings

    parser = parse_fragment(content)
    if not parser.slides:
        errors.append(
            f"STRUCTURE VIOLATION: no <section class=\"slide ...\"> elements found in {entry}."
        )
    if parser.top_level_elements or parser.top_level_text:
        details = sorted(set(parser.top_level_elements))
        errors.append(
            f"STRUCTURE VIOLATION: {entry} must contain only top-level slide sections; "
            f"found outside content: {', '.join(details) if details else 'text'}."
        )
    nested_slides = [slide for slide in parser.slides if slide['depth'] != 0]
    if nested_slides:
        errors.append(
            f"STRUCTURE VIOLATION: {entry} must not nest <section class=\"slide ...\"> elements."
        )

    return errors, warnings


def check_output_files(
    project_path: Path,
    entry: str = 'content.html',
    require_build: bool = False,
) -> Tuple[List[str], List[str]]:
    """Check build presence without confusing a source audit with a release gate."""
    errors = []
    warnings = []

    index_html = project_path / 'index.html'
    if not index_html.is_file():
        message = (
            "BUILD MISSING: index.html is absent or not a regular file. "
            f"Run html_compiler.py <project> --entry {entry}."
        )
        (errors if require_build else warnings).append(message)
    else:
        try:
            empty = index_html.stat().st_size == 0
        except OSError as error:
            message = f"BUILD UNREADABLE: index.html: {error}."
            (errors if require_build else warnings).append(message)
        else:
            if empty:
                message = "BUILD INVALID: index.html is empty. Run html_compiler.py again."
                (errors if require_build else warnings).append(message)

    return errors, warnings


def _artifact_directory_safety_errors(path: Path) -> List[str]:
    """Reject artifact trees that can traverse symlinks or leave their root."""
    if path.is_symlink():
        return [f"BUILD ARTIFACT VIOLATION: artifact directory must not be a symlink: {path}."]
    try:
        root = path.resolve(strict=True)
    except OSError as error:
        return [f"BUILD ARTIFACT UNREADABLE: {path}: {error}."]
    try:
        entries = list(path.rglob('*'))
    except OSError as error:
        return [f"BUILD ARTIFACT UNREADABLE: {path}: {error}."]
    unsafe_entries = []
    for item in entries:
        if item.is_symlink():
            unsafe_entries.append(item.relative_to(path).as_posix())
            continue
        try:
            item.resolve(strict=True).relative_to(root)
        except (OSError, ValueError):
            unsafe_entries.append(item.relative_to(path).as_posix())
    if unsafe_entries:
        return [
            f"BUILD ARTIFACT VIOLATION: {path.name} contains symlink or escaping child(ren): "
            f"{sorted(unsafe_entries)}."
        ]
    return []


def _slide_artifact_roster(path: Path, suffix: str, slide_count: int) -> Tuple[List[Path], List[str]]:
    """Return an exact, contiguous slide artifact roster."""
    errors = _artifact_directory_safety_errors(path)
    if errors:
        return [], errors
    expected_names = [f"slide_{number:02d}.{suffix}" for number in range(1, slide_count + 1)]
    try:
        entries = list(path.rglob('*'))
    except OSError as error:
        return [], [f"BUILD ARTIFACT UNREADABLE: {path}: {error}."]
    actual_names = {
        item.relative_to(path).as_posix() + ('/' if item.is_dir() else '')
        for item in entries
    }
    if actual_names != set(expected_names):
        errors.append(
            f"BUILD ARTIFACT ROSTER INVALID: {path.name} has {sorted(actual_names)}, "
            f"expected {expected_names}."
        )
    files = [
        path / name for name in expected_names
        if (path / name).is_file() and not (path / name).is_symlink()
    ]
    return files, errors


def _validate_svg_artifacts(
    path: Path,
    slide_count: int,
    width: int,
    height: int,
) -> List[str]:
    files, errors = _slide_artifact_roster(path, 'svg', slide_count)
    expected = [0.0, 0.0, float(width), float(height)]
    for svg_path in files:
        try:
            root = ET.parse(svg_path).getroot()
            if root.tag.rsplit('}', 1)[-1].lower() != 'svg':
                raise ValueError("root element is not <svg>")
            values = [float(value) for value in root.attrib.get('viewBox', '').replace(',', ' ').split()]
            if len(values) != 4 or any(abs(a - b) > 0.01 for a, b in zip(values, expected)):
                raise ValueError(
                    f"viewBox {root.attrib.get('viewBox')!r} does not match {width}x{height}"
                )
        except (OSError, ET.ParseError, ValueError) as error:
            errors.append(f"SVG ARTIFACT INVALID: {svg_path.name}: {error}.")
    return errors


def _inspect_png(path: Path) -> Tuple[Optional[Tuple[int, int]], Optional[str]]:
    try:
        from PIL import Image
    except ImportError:
        return None, "Pillow is required to validate PNG artifacts"
    try:
        with Image.open(path) as image:
            if image.format != 'PNG':
                return None, f"format is {image.format!r}, expected PNG"
            size = image.size
            image.verify()
        return size, None
    except (OSError, ValueError) as error:
        return None, str(error)


def _validate_png_artifacts(
    path: Path,
    slide_count: int,
    expected_size: Tuple[int, int],
) -> List[str]:
    files, errors = _slide_artifact_roster(path, 'png', slide_count)
    for png_path in files:
        size, error = _inspect_png(png_path)
        if error:
            errors.append(f"PNG ARTIFACT INVALID: {png_path.name}: {error}.")
        elif size != expected_size:
            errors.append(
                f"PNG ARTIFACT INVALID: {png_path.name} is {size}, expected {expected_size}."
            )
    return errors


def _validate_overview(path: Path) -> List[str]:
    size, error = _inspect_png(path)
    if error:
        return [f"OVERVIEW ARTIFACT INVALID: {error}."]
    if size is None or size[0] <= 0 or size[1] <= 0:
        return ["OVERVIEW ARTIFACT INVALID: image has no positive dimensions."]
    return []


def _validate_pdf(path: Path, slide_count: int) -> List[str]:
    try:
        from pypdf import PdfReader
    except ImportError:
        return [
            "PDF ARTIFACT VALIDATION UNAVAILABLE: pypdf is required by the "
            "HTML delivery profile."
        ]
    try:
        reader = PdfReader(str(path), strict=True)
        if reader.is_encrypted:
            return ["PDF ARTIFACT INVALID: encrypted PDF cannot be validated."]
        page_count = len(reader.pages)
        # Resolve each page and its media box. This traverses the real page tree;
        # a header or a stray /Type /Page token is not semantic evidence.
        for page in reader.pages:
            _ = tuple(page.mediabox)
    except Exception as error:
        return [f"PDF ARTIFACT INVALID: {error}."]
    if page_count != slide_count:
        return [
            f"PDF ARTIFACT ROSTER INVALID: {page_count} parsed page(s), "
            f"expected {slide_count}."
        ]
    return []


def _validate_pptx(
    path: Path,
    slide_count: int,
    required_notes_count: int | None = None,
) -> List[str]:
    errors: List[str] = []
    try:
        with zipfile.ZipFile(path) as archive:
            corrupt = archive.testzip()
            if corrupt:
                errors.append(f"PPTX ARTIFACT INVALID: corrupt member {corrupt}.")
            member_names = archive.namelist()
            names = set(member_names)
            required = {
                '[Content_Types].xml',
                'ppt/presentation.xml',
                'ppt/_rels/presentation.xml.rels',
            }
            missing = sorted(required - names)
            if missing:
                errors.append(f"PPTX ARTIFACT INVALID: missing {', '.join(missing)}.")
                return errors
            slide_names = sorted(
                (
                    name for name in member_names
                    if re.fullmatch(r'ppt/slides/slide\d+\.xml', name)
                ),
                key=lambda name: int(re.search(r'(\d+)\.xml$', name).group(1)),
            )
            expected = [f'ppt/slides/slide{number}.xml' for number in range(1, slide_count + 1)]
            if slide_names != expected:
                errors.append(
                    f"PPTX ARTIFACT ROSTER INVALID: {slide_names}, expected {expected}."
                )
            for name in required.union(slide_names):
                try:
                    ET.fromstring(archive.read(name))
                except (KeyError, ET.ParseError) as error:
                    errors.append(f"PPTX ARTIFACT INVALID: {name}: {error}.")

            if required_notes_count is not None:
                note_names = sorted(
                    (
                        name for name in member_names
                        if re.fullmatch(r'ppt/notesSlides/notesSlide\d+\.xml', name)
                    ),
                    key=lambda name: int(re.search(r'(\d+)\.xml$', name).group(1)),
                )
                expected_notes = [
                    f'ppt/notesSlides/notesSlide{number}.xml'
                    for number in range(1, required_notes_count + 1)
                ]
                if note_names != expected_notes:
                    errors.append(
                        "PPTX NOTES ROSTER INVALID: "
                        f"{note_names}, expected {expected_notes}."
                    )
                drawing_namespace = {
                    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'
                }
                for name in note_names:
                    try:
                        note_root = ET.fromstring(archive.read(name))
                    except (KeyError, ET.ParseError) as error:
                        errors.append(f"PPTX NOTES INVALID: {name}: {error}.")
                        continue
                    note_text = ''.join(
                        node.text or '' for node in note_root.findall('.//a:t', drawing_namespace)
                    ).strip()
                    if not note_text:
                        errors.append(f"PPTX NOTES INVALID: {name} contains no note text.")

                package_relationship_namespace = {
                    'pr': 'http://schemas.openxmlformats.org/package/2006/relationships'
                }
                for number in range(1, required_notes_count + 1):
                    rels_name = f'ppt/slides/_rels/slide{number}.xml.rels'
                    if rels_name not in names:
                        errors.append(
                            f"PPTX NOTES INVALID: missing slide relationships {rels_name}."
                        )
                        continue
                    try:
                        rels_root = ET.fromstring(archive.read(rels_name))
                    except ET.ParseError as error:
                        errors.append(f"PPTX NOTES INVALID: {rels_name}: {error}.")
                        continue
                    note_relations = [
                        relation
                        for relation in rels_root.findall('pr:Relationship', package_relationship_namespace)
                        if relation.attrib.get('Type', '').endswith('/notesSlide')
                    ]
                    if len(note_relations) != 1:
                        errors.append(
                            f"PPTX NOTES INVALID: slide {number} has "
                            f"{len(note_relations)} notesSlide relationship(s), expected 1."
                        )
                        continue
                    relation = note_relations[0]
                    target = relation.attrib.get('Target', '')
                    if relation.attrib.get('TargetMode', 'Internal') != 'Internal' or not target:
                        errors.append(
                            f"PPTX NOTES INVALID: slide {number} notes target is not internal."
                        )
                        continue
                    normalized_target = posixpath.normpath(
                        target.lstrip('/') if target.startswith('/') else posixpath.join('ppt/slides', target)
                    )
                    expected_target = f'ppt/notesSlides/notesSlide{number}.xml'
                    if normalized_target != expected_target:
                        errors.append(
                            f"PPTX NOTES INVALID: slide {number} resolves to "
                            f"{normalized_target!r}, expected {expected_target!r}."
                        )
            try:
                presentation = ET.fromstring(archive.read('ppt/presentation.xml'))
                namespace = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}
                ids = presentation.findall('.//p:sldIdLst/p:sldId', namespace)
                if len(ids) != slide_count:
                    errors.append(
                        f"PPTX ARTIFACT ROSTER INVALID: presentation lists {len(ids)} slide(s), "
                        f"expected {slide_count}."
                    )
                relationships = ET.fromstring(
                    archive.read('ppt/_rels/presentation.xml.rels')
                )
                rel_namespace = {
                    'pr': 'http://schemas.openxmlformats.org/package/2006/relationships'
                }
                relation_by_id: Dict[str, ET.Element] = {}
                for relation in relationships.findall('pr:Relationship', rel_namespace):
                    relation_id = relation.attrib.get('Id')
                    if not relation_id:
                        errors.append(
                            "PPTX ARTIFACT INVALID: presentation relationship has no Id."
                        )
                    elif relation_id in relation_by_id:
                        errors.append(
                            "PPTX ARTIFACT INVALID: duplicate presentation relationship "
                            f"Id {relation_id!r}."
                        )
                    else:
                        relation_by_id[relation_id] = relation

                relationship_id_key = (
                    '{http://schemas.openxmlformats.org/officeDocument/2006/'
                    'relationships}id'
                )
                resolved_slides: List[str] = []
                for slide_id in ids:
                    relation_id = slide_id.attrib.get(relationship_id_key)
                    relation = relation_by_id.get(relation_id or '')
                    if relation is None:
                        errors.append(
                            "PPTX ARTIFACT ROSTER INVALID: slide list references missing "
                            f"relationship {relation_id!r}."
                        )
                        continue
                    relation_type = relation.attrib.get('Type', '')
                    target = relation.attrib.get('Target')
                    if not relation_type.endswith('/slide') or not target:
                        errors.append(
                            "PPTX ARTIFACT ROSTER INVALID: relationship "
                            f"{relation_id!r} is not an internal slide target."
                        )
                        continue
                    if relation.attrib.get('TargetMode', 'Internal') != 'Internal':
                        errors.append(
                            "PPTX ARTIFACT ROSTER INVALID: external slide target in "
                            f"relationship {relation_id!r}."
                        )
                        continue
                    if target.startswith('/'):
                        normalized_target = posixpath.normpath(target.lstrip('/'))
                    else:
                        normalized_target = posixpath.normpath(
                            posixpath.join('ppt', target)
                        )
                    if normalized_target == '..' or normalized_target.startswith('../'):
                        errors.append(
                            "PPTX ARTIFACT ROSTER INVALID: slide relationship escapes "
                            f"the package root: {target!r}."
                        )
                        continue
                    resolved_slides.append(normalized_target)
                if resolved_slides != expected:
                    errors.append(
                        "PPTX ARTIFACT ROSTER INVALID: presentation relationship order "
                        f"resolves to {resolved_slides}, expected {expected}."
                    )
            except (KeyError, ET.ParseError):
                pass  # The parse error is already reported above.
    except (OSError, zipfile.BadZipFile) as error:
        errors.append(f"PPTX ARTIFACT INVALID: {error}.")
    return errors


def _validate_dom_receipt(path: Path, slide_count: int) -> Tuple[List[str], List[str]]:
    errors: List[str] = []
    warnings: List[str] = []
    try:
        receipt = json.loads(path.read_text(encoding='utf-8'))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        return [f"DOM AUDIT RECEIPT INVALID: {error}."], warnings
    if not isinstance(receipt, dict) or receipt.get('schema') != 'seaslides.browser-dom-audit':
        return ["DOM AUDIT RECEIPT INVALID: unsupported schema."], warnings
    if receipt.get('version') != 1:
        errors.append(f"DOM AUDIT RECEIPT INVALID: unsupported version {receipt.get('version')!r}.")
    summary = receipt.get('summary')
    if not isinstance(summary, dict):
        return errors + ["DOM AUDIT RECEIPT INVALID: summary is missing."], warnings
    counts = {}
    for field in ('slideCount', 'issueCount', 'blockerCount', 'reviewCount'):
        value = summary.get(field)
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            errors.append(f"DOM AUDIT RECEIPT INVALID: summary.{field} must be a non-negative integer.")
        else:
            counts[field] = value
    if counts.get('slideCount') != slide_count:
        errors.append("DOM AUDIT RECEIPT STALE: slide count does not match build.")

    issues = receipt.get('issues')
    if not isinstance(issues, list):
        errors.append("DOM AUDIT RECEIPT INVALID: issues must be an array.")
        issues = []
    issue_blockers = 0
    issue_reviews = 0
    for issue in issues:
        if not isinstance(issue, dict):
            errors.append("DOM AUDIT RECEIPT INVALID: malformed issue row.")
            continue
        slide = issue.get('slide')
        severity = issue.get('severity')
        if isinstance(slide, bool) or not isinstance(slide, int) or not 1 <= slide <= slide_count:
            errors.append(f"DOM AUDIT RECEIPT INVALID: issue slide {slide!r} is out of range.")
        if severity == 'blocker':
            issue_blockers += 1
        elif severity == 'review':
            issue_reviews += 1
        else:
            errors.append(f"DOM AUDIT RECEIPT INVALID: issue severity {severity!r} is unsupported.")
    if counts.get('issueCount') != len(issues):
        errors.append("DOM AUDIT RECEIPT INVALID: issueCount does not match issues array.")
    if counts.get('blockerCount') != issue_blockers or counts.get('reviewCount') != issue_reviews:
        errors.append("DOM AUDIT RECEIPT INVALID: blocker/review counts do not match issues array.")
    if counts and counts.get('issueCount') != counts.get('blockerCount', 0) + counts.get('reviewCount', 0):
        errors.append("DOM AUDIT RECEIPT INVALID: summary issue counts are inconsistent.")

    slides = receipt.get('slides')
    if not isinstance(slides, list):
        errors.append("DOM AUDIT RECEIPT INVALID: slides must be an array.")
    else:
        roster = [row.get('index') for row in slides if isinstance(row, dict)]
        if roster != list(range(1, slide_count + 1)):
            errors.append(f"DOM AUDIT RECEIPT INVALID: slide roster is {roster}.")

    expected_status = 'blocker' if issue_blockers else 'review' if issue_reviews else 'pass'
    if summary.get('status') != expected_status:
        errors.append(
            f"DOM AUDIT RECEIPT INVALID: status {summary.get('status')!r} "
            f"does not match {expected_status!r}."
        )
    if issue_blockers:
        errors.append(f"DOM QUALITY BLOCKER: receipt records {issue_blockers} blocker(s).")
    if issue_reviews:
        warnings.append(f"DOM QUALITY REVIEW: receipt records {issue_reviews} review item(s).")
    return errors, warnings


def _validate_fidelity_receipt(path: Path, slide_count: int) -> Tuple[List[str], List[str]]:
    errors: List[str] = []
    warnings: List[str] = []
    try:
        receipt = json.loads(path.read_text(encoding='utf-8'))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        return [f"RENDER FIDELITY RECEIPT INVALID: {error}."], warnings
    if not isinstance(receipt, dict) or receipt.get('schema') != 'seaslides.html-render-fidelity/v1':
        return ["RENDER FIDELITY RECEIPT INVALID: unsupported schema."], warnings
    if receipt.get('slide_count') != slide_count:
        errors.append("RENDER FIDELITY RECEIPT STALE: slide count does not match build.")
    rows = receipt.get('slides')
    if not isinstance(rows, list):
        errors.append("RENDER FIDELITY RECEIPT INVALID: slides must be an array.")
        rows = []
    roster: List[int] = []
    row_reviews: List[int] = []
    for row in rows:
        if not isinstance(row, dict):
            errors.append("RENDER FIDELITY RECEIPT INVALID: malformed slide row.")
            continue
        slide = row.get('slide')
        status = row.get('status')
        if isinstance(slide, bool) or not isinstance(slide, int):
            errors.append(f"RENDER FIDELITY RECEIPT INVALID: slide {slide!r} is not an integer.")
            continue
        roster.append(slide)
        if status == 'review':
            row_reviews.append(slide)
        elif status == 'blocker':
            # Older receipts may contain this value. Pixel-route differences
            # are always review-only; retain schema compatibility without
            # turning a fidelity finding into a delivery gate failure.
            row_reviews.append(slide)
        elif status != 'pass':
            errors.append(f"RENDER FIDELITY RECEIPT INVALID: status {status!r} is unsupported.")
    expected_roster = list(range(1, slide_count + 1))
    if roster != expected_roster:
        errors.append(f"RENDER FIDELITY RECEIPT INVALID: slide roster is {roster}.")
    review_slides = receipt.get('review_slides')
    if review_slides != row_reviews:
        errors.append(
            "RENDER FIDELITY RECEIPT INVALID: review_slides does not match slide rows."
        )
    expected_status = 'review' if row_reviews else 'pass'
    receipt_status = receipt.get('status')
    if receipt_status not in {expected_status, 'blocker' if row_reviews else expected_status}:
        errors.append(
            f"RENDER FIDELITY RECEIPT INVALID: status {receipt_status!r} "
            f"does not match {expected_status!r}."
        )
    if row_reviews:
        warnings.append(
            f"RENDER FIDELITY REVIEW: inspect browser/SVG differences on slides {row_reviews}."
        )
    return errors, warnings


def check_compile_receipt(
    project_path: Path,
    entry: str = 'content.html',
    require_build: bool = False,
    artifact_profile: str = 'visual',
) -> Tuple[List[str], List[str]]:
    """Verify that published artifacts match the compiler's current inputs."""
    errors: List[str] = []
    warnings: List[str] = []
    entry = canonical_entry(project_path, entry)
    manifest_path = project_path / 'output' / 'compile-manifest.json'
    if not manifest_path.exists():
        message = (
            "BUILD RECEIPT MISSING: output/compile-manifest.json is absent. "
            "Run html_compiler.py after source validation."
        )
        (errors if require_build else warnings).append(message)
        return errors, warnings

    try:
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        errors.append(f"BUILD RECEIPT INVALID: {error}")
        return errors, warnings

    if not isinstance(manifest, dict):
        errors.append("BUILD RECEIPT INVALID: top-level JSON value must be an object.")
        return errors, warnings

    if manifest.get('schema') != 'seaslides-html-compile/v1':
        errors.append(
            f"BUILD RECEIPT INVALID: unsupported schema {manifest.get('schema')!r}."
        )
    if manifest.get('status') != 'pass':
        errors.append(
            f"BUILD RECEIPT INVALID: status is {manifest.get('status')!r}, expected 'pass'."
        )
    if manifest.get('entry') != entry:
        errors.append(
            f"BUILD RECEIPT STALE: receipt entry {manifest.get('entry')!r} does not "
            f"match requested entry {entry!r}."
        )

    canvas = manifest.get('canvas')
    canvas_width = canvas_height = 0
    png_scale = 0.0
    if not isinstance(canvas, dict):
        errors.append("BUILD RECEIPT INVALID: canvas must be an object.")
    else:
        width_value = canvas.get('width')
        height_value = canvas.get('height')
        scale_value = canvas.get('png_scale')
        if isinstance(width_value, bool) or not isinstance(width_value, int) or width_value <= 0:
            errors.append("BUILD RECEIPT INVALID: canvas.width must be a positive integer.")
        else:
            canvas_width = width_value
        if isinstance(height_value, bool) or not isinstance(height_value, int) or height_value <= 0:
            errors.append("BUILD RECEIPT INVALID: canvas.height must be a positive integer.")
        else:
            canvas_height = height_value
        if (
            isinstance(scale_value, bool)
            or not isinstance(scale_value, (int, float))
            or not math.isfinite(scale_value)
            or scale_value <= 0
        ):
            errors.append("BUILD RECEIPT INVALID: canvas.png_scale must be a positive finite number.")
        else:
            png_scale = float(scale_value)

    requested_formats = manifest.get('requested_formats')
    requested_formats_valid = (
        isinstance(requested_formats, list)
        and all(isinstance(item, str) and item for item in requested_formats)
        and len(requested_formats) == len(set(requested_formats))
    )
    if not requested_formats_valid:
        errors.append("BUILD RECEIPT INVALID: requested_formats must be an array of unique names.")
        requested_formats = []
    unsupported_formats = sorted(
        set(requested_formats) - {'svg', 'png', 'browser_png', 'overview', 'pdf', 'pptx'}
    )
    if unsupported_formats:
        requested_formats_valid = False
        errors.append(
            "BUILD RECEIPT INVALID: requested_formats contains unsupported name(s): "
            f"{', '.join(unsupported_formats)}."
        )
    required_formats = ARTIFACT_PROFILE_FORMATS.get(artifact_profile, set())
    missing_formats = sorted(required_formats - set(requested_formats))
    if missing_formats:
        errors.append(
            f"BUILD RECEIPT INCOMPLETE for {artifact_profile!r}: requested_formats omits "
            f"{', '.join(missing_formats)}."
        )

    raw_inputs = manifest.get('inputs')
    input_rows: dict[str, dict] = {}
    if not isinstance(raw_inputs, list):
        errors.append("BUILD RECEIPT INVALID: inputs must be an array.")
        raw_inputs = []
    for row in raw_inputs:
        if not isinstance(row, dict) or not isinstance(row.get('path'), str):
            errors.append("BUILD RECEIPT INVALID: malformed input fingerprint row.")
            continue
        relative = row['path']
        if not _is_canonical_relative_posix(relative):
            errors.append(f"BUILD RECEIPT INVALID: input path is not canonical relative POSIX: {relative!r}.")
            continue
        if relative in input_rows:
            errors.append(f"BUILD RECEIPT INVALID: duplicate input fingerprint {relative!r}.")
            continue
        input_rows[relative] = row

    expected_inputs = ['index-template.html', 'template.css', entry]
    for relative in expected_inputs:
        if relative not in input_rows:
            errors.append(f"BUILD RECEIPT STALE: missing input fingerprint for {relative}.")

    for relative, row in input_rows.items():
        raw_input = project_path / relative
        if raw_input.is_symlink():
            try:
                raw_input.resolve(strict=True).relative_to(project_path.resolve())
            except (OSError, ValueError):
                errors.append(f"BUILD RECEIPT INVALID: input symlink escapes project: {relative}.")
                continue
        path = raw_input.resolve()
        try:
            path.relative_to(project_path.resolve())
        except ValueError:
            errors.append(f"BUILD RECEIPT INVALID: input path escapes project: {relative}.")
            continue
        if not path.is_file():
            errors.append(f"BUILD RECEIPT STALE: input no longer exists: {relative}.")
            continue
        try:
            actual_size = path.stat().st_size
            actual_hash = sha256_file(path)
        except OSError as error:
            errors.append(f"BUILD INPUT UNREADABLE: {relative}: {error}.")
            continue
        if row.get('bytes') != actual_size:
            errors.append(f"BUILD RECEIPT STALE: {relative} byte size changed after compilation.")
        if row.get('sha256') != actual_hash:
            errors.append(f"BUILD RECEIPT STALE: {relative} changed after compilation.")

    recorded_slide_count = manifest.get('slide_count')
    if not isinstance(recorded_slide_count, int) or recorded_slide_count <= 0:
        errors.append("BUILD RECEIPT INVALID: slide_count must be a positive integer.")
    else:
        source_entry = project_path / entry
        if source_entry.is_file():
            try:
                source_slide_count = len(parse_fragment(source_entry.read_text(encoding='utf-8')).slides)
            except (OSError, UnicodeError) as error:
                errors.append(f"BUILD INPUT UNREADABLE: {entry}: {error}.")
            else:
                if source_slide_count != recorded_slide_count:
                    errors.append(
                        "BUILD RECEIPT STALE: source slide count "
                        f"{source_slide_count} != recorded {recorded_slide_count}."
                    )

    index_html = project_path / 'index.html'
    if not index_html.is_file():
        errors.append("BUILD ARTIFACT MISSING: index.html is absent.")
    else:
        try:
            index_size = index_html.stat().st_size
            index_hash = sha256_file(index_html)
        except OSError as error:
            errors.append(f"BUILD ARTIFACT UNREADABLE: index.html: {error}.")
        else:
            if index_size == 0:
                errors.append("BUILD ARTIFACT INVALID: index.html is empty.")
            if manifest.get('assembled_index_sha256') != index_hash:
                errors.append("BUILD RECEIPT STALE: index.html does not match the compiled receipt.")

    artifact_rows = manifest.get('artifacts', [])
    if not isinstance(artifact_rows, list) or not artifact_rows:
        errors.append("BUILD RECEIPT INVALID: no artifacts are recorded.")
        return errors, warnings

    recorded_names = set()
    artifact_by_name: dict[str, tuple[dict, Path]] = {}
    project_root = project_path.resolve()
    for row in artifact_rows:
        if not isinstance(row, dict):
            errors.append("BUILD RECEIPT INVALID: artifact row is not an object.")
            continue
        name = row.get('name')
        raw_path = row.get('path')
        if not isinstance(name, str) or not isinstance(raw_path, str):
            errors.append("BUILD RECEIPT INVALID: artifact name/path is missing.")
            continue
        if name in recorded_names:
            errors.append(f"BUILD RECEIPT INVALID: duplicate artifact name {name!r}.")
            continue
        recorded_names.add(name)
        contract = ARTIFACT_PATHS.get(name)
        if contract is None:
            errors.append(f"BUILD RECEIPT INVALID: unknown artifact name {name!r}.")
            continue
        expected_path, expected_kind = contract
        if raw_path != expected_path:
            errors.append(
                f"BUILD RECEIPT INVALID: {name} path is {raw_path!r}, expected {expected_path!r}."
            )
            continue
        if row.get('kind') != expected_kind:
            errors.append(
                f"BUILD RECEIPT INVALID: {name}.kind is {row.get('kind')!r}, "
                f"expected {expected_kind!r}."
            )
        raw_artifact = project_path / raw_path
        if raw_artifact.is_symlink():
            errors.append(f"BUILD RECEIPT INVALID: artifact must not be a symlink: {raw_path}.")
            continue
        artifact = raw_artifact.resolve()
        try:
            artifact.relative_to(project_root)
        except ValueError:
            errors.append(f"BUILD RECEIPT INVALID: artifact escapes project: {raw_path}.")
            continue
        artifact_by_name[name] = (row, artifact)
        actual_kind = 'directory' if artifact.is_dir() else 'file' if artifact.is_file() else None
        if actual_kind is None:
            errors.append(f"BUILD ARTIFACT MISSING: {raw_path} ({name}).")
            continue
        if actual_kind != expected_kind:
            errors.append(
                f"BUILD ARTIFACT INVALID: {raw_path} is {actual_kind}, expected {expected_kind}."
            )
            continue
        if actual_kind == 'directory':
            directory_errors = _artifact_directory_safety_errors(artifact)
            if directory_errors:
                errors.extend(directory_errors)
                continue
        try:
            if actual_kind == 'directory':
                actual_count = len([item for item in artifact.rglob('*') if item.is_file()])
                actual_hash = sha256_directory(artifact)
                if row.get('file_count') != actual_count:
                    errors.append(
                        f"BUILD RECEIPT STALE: {raw_path} file_count is {actual_count}, "
                        f"recorded {row.get('file_count')!r}."
                    )
                if actual_count == 0:
                    errors.append(f"BUILD ARTIFACT INVALID: {raw_path} is empty.")
            else:
                actual_size = artifact.stat().st_size
                actual_hash = sha256_file(artifact)
                if row.get('bytes') != actual_size:
                    errors.append(
                        f"BUILD RECEIPT STALE: {raw_path} byte size is {actual_size}, "
                        f"recorded {row.get('bytes')!r}."
                    )
                if actual_size == 0:
                    errors.append(f"BUILD ARTIFACT INVALID: {raw_path} is empty.")
        except OSError as error:
            errors.append(f"BUILD ARTIFACT UNREADABLE: {raw_path}: {error}.")
            continue
        if actual_hash != row.get('sha256'):
            errors.append(f"BUILD RECEIPT STALE: {raw_path} changed after compilation.")

    if requested_formats_valid:
        requested_set = set(requested_formats)
        expected_artifacts = {'svg', 'dom_audit'} | requested_set
        if 'overview' in requested_set and 'png' not in requested_set:
            expected_artifacts.add('png_dependency')
        if 'browser_png' in requested_set and requested_set.intersection({'png', 'overview'}):
            expected_artifacts.add('render_fidelity')
        missing_requested = sorted(expected_artifacts - recorded_names)
        unexpected_recorded = sorted(recorded_names - expected_artifacts)
        if missing_requested:
            errors.append(
                "BUILD RECEIPT INVALID: requested_formats is missing matching artifact(s): "
                f"{', '.join(missing_requested)}."
            )
        if unexpected_recorded:
            errors.append(
                "BUILD RECEIPT INVALID: artifact(s) were not requested: "
                f"{', '.join(unexpected_recorded)}."
            )

    required_artifacts = ARTIFACT_PROFILES.get(artifact_profile)
    if required_artifacts is None:
        raise ValueError(f"unknown artifact profile: {artifact_profile}")
    missing_artifacts = sorted(required_artifacts - recorded_names)
    if missing_artifacts:
        errors.append(
            f"BUILD RECEIPT INCOMPLETE for {artifact_profile!r}: missing "
            f"{', '.join(missing_artifacts)}."
        )

    toolchain_rows = manifest.get('toolchain')
    required_tools = {
        'requirements.txt',
        'scripts/html_compiler.py',
        'scripts/runtime_environment.py',
        'scripts/assemble.py',
        'scripts/runtime/deck_runtime.js',
        'scripts/html_to_svg/browser_dom_to_svg.mjs',
        'scripts/html_to_svg/browser_dom_audit.mjs',
        'scripts/html_to_svg/chart_renderer.mjs',
        'scripts/html_to_svg/package.json',
        'scripts/html_to_svg/package-lock.json',
    }
    requested_set = set(requested_formats)
    if requested_set.intersection({'png', 'overview'}) or recorded_names.intersection(
        {'png', 'png_dependency'}
    ):
        required_tools.add('scripts/html_to_svg/browser_svg_to_png.mjs')
    if 'browser_png' in requested_set or 'browser_png' in recorded_names:
        required_tools.add('scripts/html_to_svg/browser_html_to_png.mjs')
    if 'pdf' in requested_set or 'pdf' in recorded_names:
        required_tools.add('scripts/html_to_svg/browser_svg_to_pdf.mjs')
    if 'pptx' in requested_set or 'pptx' in recorded_names:
        required_tools.update({
            'scripts/svg_to_pptx.py',
            'scripts/svg_to_pptx/__init__.py',
            'scripts/svg_to_pptx/pptx_builder.py',
            'scripts/svg_finalize/__init__.py',
        })
        for package_name in ('svg_to_pptx', 'svg_finalize'):
            package_root = SCRIPTS_DIR / package_name
            required_tools.update(
                path.relative_to(SKILL_ROOT).as_posix()
                for path in package_root.rglob('*.py')
                if path.is_file()
            )
    recorded_tools = set()
    if not isinstance(toolchain_rows, list):
        errors.append("BUILD RECEIPT INVALID: toolchain fingerprints are missing.")
    else:
        for row in toolchain_rows:
            if not isinstance(row, dict) or not isinstance(row.get('path'), str):
                errors.append("BUILD RECEIPT INVALID: malformed toolchain row.")
                continue
            relative = row['path']
            if not _is_canonical_relative_posix(relative):
                errors.append(f"BUILD RECEIPT INVALID: tool path is not canonical: {relative!r}.")
                continue
            if relative in recorded_tools:
                errors.append(f"BUILD RECEIPT INVALID: duplicate tool fingerprint {relative!r}.")
                continue
            recorded_tools.add(relative)
            tool_path = (SKILL_ROOT / relative).resolve()
            try:
                tool_path.relative_to(SKILL_ROOT)
            except ValueError:
                errors.append(f"BUILD RECEIPT INVALID: tool path escapes the skill: {relative}.")
                continue
            if not tool_path.is_file():
                errors.append(f"BUILD TOOL MISSING: {relative}.")
                continue
            try:
                actual_size = tool_path.stat().st_size
                actual_hash = sha256_file(tool_path)
            except OSError as error:
                errors.append(f"BUILD TOOL UNREADABLE: {relative}: {error}.")
                continue
            if row.get('bytes') != actual_size:
                errors.append(f"BUILD RECEIPT STALE: tool size changed: {relative}.")
            if row.get('sha256') != actual_hash:
                errors.append(f"BUILD RECEIPT STALE: renderer/runtime changed: {relative}.")
    missing_tools = sorted(required_tools - recorded_tools)
    if missing_tools:
        errors.append(
            "BUILD RECEIPT INVALID: missing required tool fingerprints: "
            f"{', '.join(missing_tools)}."
        )

    recorded_environment = manifest.get('runtime_environment')
    if recorded_environment is not None:
        valid_environment = (
            isinstance(recorded_environment, dict)
            and all(
                isinstance(key, str) and key
                and isinstance(value, str) and value
                for key, value in recorded_environment.items()
            )
        )
        if not valid_environment:
            errors.append(
                "BUILD RECEIPT INVALID: runtime_environment must map non-empty names "
                "to non-empty version strings."
            )
        else:
            current_environment = runtime_environment_fingerprint()
            if recorded_environment != current_environment:
                changed = sorted(
                    key for key in set(recorded_environment) | set(current_environment)
                    if recorded_environment.get(key) != current_environment.get(key)
                )
                warnings.append(
                    "BUILD ENVIRONMENT REVIEW: renderer/runtime version changed since "
                    f"compilation ({', '.join(changed)}); rebuild before final delivery."
                )

    if isinstance(recorded_slide_count, int) and recorded_slide_count > 0:
        if canvas_width > 0 and canvas_height > 0:
            svg_record = artifact_by_name.get('svg')
            if svg_record and svg_record[1].is_dir():
                errors.extend(
                    _validate_svg_artifacts(
                        svg_record[1], recorded_slide_count, canvas_width, canvas_height
                    )
                )
            expected_png_size = (
                round(canvas_width * png_scale),
                round(canvas_height * png_scale),
            )
            for name in ('png', 'png_dependency', 'browser_png'):
                record = artifact_by_name.get(name)
                if record and record[1].is_dir() and png_scale > 0:
                    errors.extend(
                        _validate_png_artifacts(record[1], recorded_slide_count, expected_png_size)
                    )
        overview_record = artifact_by_name.get('overview')
        if overview_record and overview_record[1].is_file():
            errors.extend(_validate_overview(overview_record[1]))
        pdf_record = artifact_by_name.get('pdf')
        if pdf_record and pdf_record[1].is_file():
            errors.extend(_validate_pdf(pdf_record[1], recorded_slide_count))
        pptx_record = artifact_by_name.get('pptx')
        if pptx_record and pptx_record[1].is_file():
            errors.extend(
                _validate_pptx(
                    pptx_record[1],
                    recorded_slide_count,
                    required_notes_count=recorded_slide_count,
                )
            )
        dom_record = artifact_by_name.get('dom_audit')
        if dom_record and dom_record[1].is_file():
            dom_errors, dom_reviews = _validate_dom_receipt(
                dom_record[1], recorded_slide_count
            )
            errors.extend(dom_errors)
            warnings.extend(dom_reviews)
        fidelity_record = artifact_by_name.get('render_fidelity')
        if fidelity_record and fidelity_record[1].is_file():
            fidelity_errors, fidelity_reviews = _validate_fidelity_receipt(
                fidelity_record[1], recorded_slide_count
            )
            errors.extend(fidelity_errors)
            warnings.extend(fidelity_reviews)

    return errors, warnings


def check_slide_structure(project_path: Path, entry: str = 'content.html') -> Tuple[List[str], List[str]]:
    """Check deterministic per-slide delivery requirements."""
    errors = []
    warnings = []

    content = _read_source_entry(project_path, entry)
    if content is None:
        return errors, warnings
    slides = parse_fragment(content).slides
    if not slides:
        return errors, warnings

    slides_missing_notes = []
    for i, slide in enumerate(slides, 1):
        if not slide['attrs'].get('data-notes', '').strip():
            slides_missing_notes.append(i)

    if slides_missing_notes:
        if len(slides_missing_notes) == len(slides):
            errors.append(
                "NOTES VIOLATION: no slide has non-empty data-notes. "
                "Speaker notes are a required SeaSlides delivery artifact."
            )
        else:
            errors.append(
                f"NOTES VIOLATION: {len(slides_missing_notes)}/{len(slides)} slides have "
                f"missing or empty data-notes (slides: {slides_missing_notes})."
            )

    return errors, warnings


def check_tcs_compliance(
    project_path: Path,
    entry: str = 'content.html',
    profile: str = 'standard-project',
) -> Tuple[List[str], List[str]]:
    """Check Template-Content Separation compliance.

    content.html must not contain:
    - <style> tags
    - <script> tags
    - <link> tags
    - Inline style attributes except allowlisted numeric data geometry
    """
    errors = []
    warnings = []

    content = _read_source_entry(project_path, entry)
    if content is None:
        return errors, warnings
    parser = parse_fragment(content)

    forbidden = sorted({record['tag'] for record in parser.tags if record['tag'] in {'style', 'script', 'link', 'meta'}})
    if forbidden:
        errors.append(
            "TCS VIOLATION: content contains shell-owned element(s): "
            f"{', '.join(f'<{tag}>' for tag in forbidden)}."
        )

    event_handlers = sorted({
        attr
        for record in parser.tags
        for attr in record['attrs']
        if attr.startswith('on')
    })
    if event_handlers:
        errors.append(
            "TCS VIOLATION: inline event handler(s) belong in index-template.html/runtime: "
            f"{', '.join(event_handlers)}."
        )

    # Standard projects must consume theme classes. Theme demos and declared
    # scenarios may author one-off geometry, but it remains visible for review.
    violations = []
    for record in parser.tags:
        value = record['attrs'].get('style')
        if value is None:
            continue
        if not is_allowed_data_style_for_classes(record['classes'], value.strip()):
            violations.append(value.strip())

    if violations:
        sample = violations[:3]
        sample_str = '; '.join(f'style="{v}"' for v in sample)
        message = (
            f"TCS VIOLATION: {len(violations)} forbidden inline style(s) found in content.html. "
            "Only allowlisted numeric data geometry is allowed. "
            f"Examples: {sample_str}"
        )
        (errors if profile == 'standard-project' else warnings).append(message)

    return errors, warnings


def check_pseudocode_markup(project_path: Path, entry: str = 'content.html') -> Tuple[List[str], List[str]]:
    """Check canonical pseudocode environments with class/order-insensitive HTML parsing."""
    errors = []
    warnings = []

    content = _read_source_entry(project_path, entry)
    if content is None:
        return errors, warnings
    parser = parse_fragment(content)
    for block_number, block in enumerate(parser.pseudocode_blocks, 1):
        body = ''.join(block['text'])
        positions: dict[str, Tuple[int, int]] = {}
        for environment in ('algorithm', 'algorithmic'):
            begin_marker = rf'\begin{{{environment}}}'
            end_marker = rf'\end{{{environment}}}'
            begins = [match.start() for match in re.finditer(re.escape(begin_marker), body)]
            ends = [match.start() for match in re.finditer(re.escape(end_marker), body)]
            if len(begins) != 1 or len(ends) != 1:
                warnings.append(
                    f"PSEUDOCODE REVIEW: block #{block_number} must contain exactly one "
                    f"{begin_marker} and one {end_marker}; found {len(begins)} and {len(ends)}."
                )
                continue
            positions[environment] = (begins[0], ends[0])
            if begins[0] >= ends[0]:
                warnings.append(
                    f"PSEUDOCODE REVIEW: block #{block_number} closes {environment} "
                    "before opening it."
                )
        if 'algorithm' in positions and 'algorithmic' in positions:
            algorithm_begin, algorithm_end = positions['algorithm']
            algorithmic_begin, algorithmic_end = positions['algorithmic']
            if not (
                algorithm_begin < algorithmic_begin < algorithmic_end < algorithm_end
            ):
                warnings.append(
                    f"PSEUDOCODE REVIEW: block #{block_number} must nest algorithmic "
                    "inside algorithm."
                )

    wrong_pseudocode = [
        record for record in parser.tags
        if 'language-pseudocode' in record['classes']
        and not record['classes'].intersection({'pseudocode', 'pseudocode-source'})
    ]
    if wrong_pseudocode:
        warnings.append(
            f"PSEUDOCODE FORMAT ERROR: {len(wrong_pseudocode)} block(s) use "
            "language-pseudocode without a pseudocode source class."
        )

    return errors, warnings


def check_image_usage(project_path: Path, entry: str = 'content.html') -> Tuple[List[str], List[str]]:
    """Validate referenced image assets; never demand that available images be used."""
    errors = []
    warnings = []
    content = _read_source_entry(project_path, entry)
    if content is None:
        return errors, warnings
    images = [record for record in parse_fragment(content).tags if record['tag'] == 'img']
    root = project_path.resolve()
    for index, record in enumerate(images, 1):
        attrs = record['attrs']
        src = attrs.get('src', '').strip()
        if not src:
            errors.append(f"IMAGE VIOLATION: <img> #{index} has no src.")
            continue
        if 'alt' not in attrs:
            errors.append(f"IMAGE VIOLATION: <img> #{index} is missing an alt attribute.")

        parsed = urlparse(src)
        if src.startswith('data:'):
            continue
        if parsed.scheme or parsed.netloc or src.startswith('//'):
            errors.append(
                f"IMAGE VIOLATION: <img> #{index} uses non-deterministic external source {src!r}; "
                "use a relative assets/ path or data URI."
            )
            continue
        asset = (project_path / unquote(parsed.path)).resolve()
        try:
            asset.relative_to(root)
        except ValueError:
            errors.append(f"IMAGE VIOLATION: <img> #{index} escapes the project: {src!r}.")
            continue
        if not asset.is_file():
            errors.append(f"IMAGE MISSING: <img> #{index} references absent file {src!r}.")

    return errors, warnings


# ============================================================
# Main
# ============================================================

def _validation_result(
    project: object,
    errors: List[str],
    reviews: Optional[List[str]] = None,
    *,
    info: Optional[List[str]] = None,
    checks: Optional[Dict[str, Dict]] = None,
    fail_on_review: bool = False,
    extra: Optional[dict] = None,
) -> Tuple[bool, Dict]:
    """Build one stable result schema for success and controlled failures."""
    reviews = list(reviews or [])
    info = list(info or [])
    errors = list(errors)
    passed = not errors and (not fail_on_review or not reviews)
    result = {
        'project': str(project),
        'passed': passed,
        'error_count': len(errors),
        'warning_count': len(reviews),
        'review_count': len(reviews),
        'info_count': len(info),
        'errors': errors,
        'warnings': reviews,
        'reviews': reviews,
        'info': info,
        'checks': checks or {},
    }
    if extra:
        result.update(extra)
    return passed, result


def validate_single_file(
    content_path: str,
    template_path: str = None,
    profile: str = 'standard-project',
) -> Tuple[bool, Dict]:
    """Validate a single content.html file for TCS compliance.

    This is the legacy mode, equivalent to the former validate.py script.
    Checks deterministic TCS rules and optionally cross-references CSS classes
    against a template file.

    Returns (passed, results_dict).
    """
    cpath = Path(content_path)
    if profile not in VALID_PROFILES:
        raise ValueError(f"unknown source profile: {profile}")
    if not cpath.is_file():
        return _validation_result(
            cpath,
            [f"Content file is absent or not a regular file: {content_path}"],
            extra={'class_count': 0},
        )
    try:
        content = cpath.read_text(encoding='utf-8')
    except UnicodeError as error:
        return _validation_result(
            cpath,
            [f"Content file is not valid UTF-8: {error}."],
            extra={'class_count': 0},
        )
    except OSError as error:
        return _validation_result(
            cpath,
            [f"Content file is unreadable: {error}."],
            extra={'class_count': 0},
        )

    errors: List[str] = []
    warnings: List[str] = []

    parser = parse_fragment(content)
    forbidden = sorted({record['tag'] for record in parser.tags if record['tag'] in {'style', 'script', 'link', 'meta'}})
    if forbidden:
        errors.append(f"FORBIDDEN shell element(s): {', '.join(forbidden)}")
    handlers = sorted({
        attr for record in parser.tags for attr in record['attrs'] if attr.startswith('on')
    })
    if handlers:
        errors.append(f"FORBIDDEN inline event handler(s): {', '.join(handlers)}")

    for record in parser.tags:
        value = record['attrs'].get('style')
        if value is None or is_allowed_data_style_for_classes(record['classes'], value.strip()):
            continue
        message = (
            f"FORBIDDEN: inline style=\"{value.strip()}\" "
            "(only allowlisted numeric data geometry is permitted)"
        )
        (errors if profile == 'standard-project' else warnings).append(message)

    # CSS class cross-referencing (if template provided)
    used = set().union(*(record['classes'] for record in parser.tags)) if parser.tags else set()

    if template_path:
        tpath = Path(template_path)
        if not tpath.is_file():
            errors.append(f"Template file is absent or not a regular file: {template_path}")
        else:
            try:
                template_text = tpath.read_text(encoding='utf-8')
            except (OSError, UnicodeError) as error:
                errors.append(f"Template file is unreadable UTF-8: {error}.")
            else:
                if tpath.suffix == '.css':
                    defined = extract_defined_classes_from_css(template_text)
                else:
                    defined = extract_defined_classes_from_html(template_text)

                lang_classes = {c for c in used if c.startswith("language-")}
                undefined = used - defined - BUILTIN_CLASSES - lang_classes
                if undefined:
                    warnings.append(
                        f"UNDEFINED CLASSES ({len(undefined)}): "
                        f"{', '.join(sorted(undefined))}"
                    )

    used_count = len(used)
    return _validation_result(
        cpath, errors, warnings, extra={'class_count': used_count}
    )


def validate_project(
    project_path: str,
    strict: bool = False,
    entry: str = 'content.html',
    require_build: bool = False,
    source_only: bool = False,
    profile: str = 'standard-project',
    artifact_profile: str = 'visual',
) -> Tuple[bool, Dict]:
    """Run all validations on an HTML slide project.

    Returns (passed, results_dict).
    """
    path = Path(project_path)
    if profile not in VALID_PROFILES:
        raise ValueError(f"unknown source profile: {profile}")
    if artifact_profile not in ARTIFACT_PROFILES:
        raise ValueError(f"unknown artifact profile: {artifact_profile}")
    if source_only and require_build:
        raise ValueError("source_only and require_build are mutually exclusive")
    if not path.is_dir():
        return _validation_result(
            path,
            [f"Project path is absent or not a directory: {project_path}"],
            fail_on_review=strict,
        )
    entry = canonical_entry(path, entry)

    all_errors: List[str] = []
    all_reviews: List[str] = []
    info: List[str] = []

    # Run all checks
    checks = [
        ("Source Conversion Receipts", check_source_conversion_receipts),
        ("Content File", lambda path: check_content_file(path, entry)),
        ("Slide Structure", lambda path: check_slide_structure(path, entry)),
        ("TCS Compliance", lambda path: check_tcs_compliance(path, entry, profile)),
        ("Pseudocode Markup", lambda path: check_pseudocode_markup(path, entry)),
        ("Image Assets", lambda path: check_image_usage(path, entry)),
    ]
    if source_only:
        info.append("Source-only validation: compiled artifacts and receipt were not checked.")
    else:
        checks.extend([
            ("Output Files", lambda path: check_output_files(path, entry, require_build)),
            (
                "Compile Receipt",
                lambda path: check_compile_receipt(
                    path, entry, require_build, artifact_profile
                ),
            ),
        ])

    if require_build:
        info.append(f"Source profile: {profile}; artifact profile: {artifact_profile}.")
    else:
        info.append(f"Source profile: {profile}.")

    results_by_check: Dict[str, Dict] = {}
    for check_name, check_fn in checks:
        errs, warns = check_fn(path)
        results_by_check[check_name] = {'errors': errs, 'warnings': warns}
        all_errors.extend(errs)
        all_reviews.extend(warns)

    return _validation_result(
        path,
        all_errors,
        all_reviews,
        info=info,
        checks=results_by_check,
        fail_on_review=strict,
    )


def print_results(results: Dict) -> None:
    """Print validation results in a readable format."""
    project = results['project']
    passed = results['passed']

    if passed:
        print(f"PASSED: {project}")
    else:
        print(f"FAILED: {project}")

    if results['errors']:
        print(f"\n  Errors ({results['error_count']}):")
        for err in results['errors']:
            print(f"    [ERROR] {err}")

    reviews = results.get('reviews', results.get('warnings', []))
    if reviews:
        print(f"\n  Reviews ({len(reviews)}):")
        for review in reviews:
            print(f"    [REVIEW] {review}")

    if results.get('info'):
        print(f"\n  Info ({len(results['info'])}):")
        for message in results['info']:
            print(f"    [INFO]   {message}")

    if not results['errors'] and not reviews:
        print("  All checks passed with no issues.")

    print()


def _is_single_file_mode(path_arg: str) -> bool:
    """Detect whether the positional argument is a content.html file (legacy mode)
    rather than a project directory."""
    p = Path(path_arg)
    suffix_matches = p.suffix.lower() in ('.html', '.htm')
    if p.exists():
        return p.is_file() and suffix_matches
    return suffix_matches


def main():
    parser = argparse.ArgumentParser(
        description="Validate an HTML slide presentation project"
    )
    parser.add_argument(
        "project_path",
        help="Path to the project directory (or path to content.html for legacy single-file mode)"
    )
    parser.add_argument(
        "template_path", nargs="?",
        help="Optional template.css for legacy single-file validation"
    )
    parser.add_argument(
        "--fail-on-review", action="store_true",
        help="Optional review policy: return failure when any review item remains"
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Output results as JSON"
    )
    parser.add_argument(
        "--quiet", action="store_true",
        help="Only output pass/fail status"
    )
    parser.add_argument(
        "--entry", default=None,
        help="Content entry filename inside a project (default: content.html)"
    )
    parser.add_argument(
        "--profile", choices=sorted(VALID_PROFILES), default="standard-project",
        help="Source contract (default: standard-project)"
    )
    parser.add_argument(
        "--artifact-profile", choices=sorted(ARTIFACT_PROFILES), default=None,
        help="Artifacts required by --require-build (default: visual)"
    )
    build_group = parser.add_mutually_exclusive_group()
    build_group.add_argument(
        "--require-build", action="store_true",
        help="Require a current compiler receipt and all recorded artifacts"
    )
    build_group.add_argument(
        "--source-only", action="store_true",
        help="Validate source/TCS only; do not inspect compiled artifacts"
    )

    args = parser.parse_args()

    if _is_single_file_mode(args.project_path):
        invalid = []
        if args.require_build:
            invalid.append('--require-build')
        if args.source_only:
            invalid.append('--source-only')
        if args.entry is not None:
            invalid.append('--entry')
        if args.artifact_profile is not None:
            invalid.append('--artifact-profile')
        if invalid:
            parser.error(
                f"{', '.join(invalid)} is only valid for a project directory"
            )
        passed, results = validate_single_file(
            args.project_path,
            args.template_path,
            profile=args.profile,
        )
        if args.fail_on_review and results.get('warnings'):
            passed = False
            results['passed'] = False
        if args.json:
            print(json.dumps(results, indent=2, ensure_ascii=False))
        elif args.quiet:
            print("PASS" if passed else "FAIL")
        else:
            print_results(results)
            print("Result: PASS" if passed else "Result: FAIL")
        sys.exit(0 if passed else 1)

    if args.template_path:
        parser.error("template_path positional argument is only valid in legacy single-file mode")
    if not args.source_only and not args.require_build:
        parser.error(
            "project validation requires exactly one of --source-only or --require-build"
        )
    if args.source_only and args.artifact_profile is not None:
        parser.error("--artifact-profile requires --require-build")

    entry = args.entry or 'content.html'
    artifact_profile = args.artifact_profile or 'visual'

    try:
        passed, results = validate_project(
            args.project_path,
            strict=args.fail_on_review,
            entry=entry,
            require_build=args.require_build,
            source_only=args.source_only,
            profile=args.profile,
            artifact_profile=artifact_profile,
        )
    except ValueError as error:
        parser.error(str(error))

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    elif args.quiet:
        print("PASS" if passed else "FAIL")
    else:
        print_results(results)
        # Summary line
        if passed:
            print("Result: PASS")
        else:
            print(
                f"Result: FAIL ({results['error_count']} blockers, "
                f"{results['review_count']} reviews)"
            )

    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
