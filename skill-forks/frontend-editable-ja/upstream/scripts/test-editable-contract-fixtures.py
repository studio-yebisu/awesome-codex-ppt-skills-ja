#!/usr/bin/env python3
"""Regression fixtures for the editable deck static validator.

These are deliberately tiny broken decks. The test proves the public validator
fails for the core regressions it is supposed to catch, without relying on a
large generated preset fixture.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate-editable-decks.py"
PORT_VALIDATOR = ROOT / "scripts" / "validate-template-ports.py"

BASE_HTML = """<!doctype html>
<html data-mobile-adaptation="desktop-default">
<head>
<style>
@media (max-width: 700px) and (orientation: portrait) {{ .slide {{ overflow-x:hidden; }} }}
@media (max-height: 500px) and (orientation: landscape) {{ .slide {{ overflow-x:hidden; }} }}
</style>
</head>
<body>
<aside id="slideSidebar"><button id="btnNewPage">+New Page</button></aside>
<div class="slides-offset" id="deck">
{slides}
</div>
<script>
document.querySelector('.slides-offset').querySelectorAll(':scope > section.slide');
function renumberDeckSlides() {{}}
function renumberDeckObjects() {{}}
function createBlankSlideFromPreset() {{}}
function _copySlide(index) {{}}
function _newPageAfterCurrent() {{}}
function exportHtml() {{}}
function sanitizeExportDocument() {{}}
function serializeDeckState() {{}}
function buildStandaloneHtml() {{}}
function downloadHtml() {{}}
window.showSaveFilePicker = window.showSaveFilePicker || function () {{}};
localStorage.setItem('x','y');
document.createElement('button').setAttribute('data-filmstrip-action', 'copy');
</script>
<script type="application/json" id="deck-persisted-state">{{"v":3,"revision":1,"updatedAt":"1970-01-01T00:00:00.001Z","deckHtml":""}}</script>
</body>
</html>
"""

GOOD_SLIDES = """
<section class="slide" id="slide-0">
  <h1 data-edit-slot="s0-title">Editable title</h1>
</section>
"""

FIXTURES = {
    "duplicate_slide_ids": BASE_HTML.format(
        slides="""
<section class="slide" id="slide-0"><h1 data-edit-slot="a">A</h1></section>
<section class="slide" id="slide-0"><h1 data-edit-slot="b">B</h1></section>
"""
    ),
    "duplicate_object_ids": BASE_HTML.format(
        slides="""
<section class="slide" id="slide-0">
  <div data-slide-object data-oid="dup"><div class="slide-object-text">A</div></div>
  <div data-slide-object data-oid="dup"><div class="slide-object-text">B</div></div>
</section>
"""
    ),
    "static_title": BASE_HTML.format(
        slides="""
<section class="slide" id="slide-0">
  <h1>Static title</h1>
  <p data-edit-slot="body">Editable body</p>
</section>
"""
    ),
    "missing_mobile_marker": BASE_HTML.replace(' data-mobile-adaptation="desktop-default"', "").format(slides=GOOD_SLIDES),
    "missing_slot_editor_runtime": BASE_HTML.format(slides=GOOD_SLIDES),
    "missing_portable_state": BASE_HTML.replace(
        '<script type="application/json" id="deck-persisted-state">{{"v":3,"revision":1,"updatedAt":"1970-01-01T00:00:00.001Z","deckHtml":""}}</script>\n',
        "",
    ).format(slides=GOOD_SLIDES),
    "assets_media_path": BASE_HTML.format(
        slides="""
<section class="slide" id="slide-0">
  <div data-slide-object data-oid="img"><img src="assets/photo.png" alt=""></div>
</section>
"""
    ),
}

EXPECTED_MESSAGES = {
    "duplicate_slide_ids": "slide ids are not unique",
    "duplicate_object_ids": "data-oid values are not unique",
    "static_title": "title-like authored text is not editable",
    "missing_mobile_marker": "missing mobile adaptation marker",
    "missing_slot_editor_runtime": "editable slots require the injected SlotEditor runtime",
    "missing_portable_state": "missing embedded persisted state",
    "assets_media_path": "media src uses non-portable assets/ path",
}

PORT_BASE_HTML = """<!doctype html>
<html data-template-source="fixture" data-template-edit-mode="{mode}" data-mobile-adaptation="desktop-default">
<head></head>
<body>
<div id="deck" class="slides-offset" data-ported-template="fixture">
{slides}
</div>
<script id="swiss-slot-edit-runtime-js">
document.querySelector('.slides-offset').querySelectorAll(':scope > section.slide');
class SlotEditor {{}}
function exportHtml() {{}}
function sanitizeEditableState() {{}}
function serializeDeckState() {{}}
function buildStandaloneHtml() {{}}
function downloadHtml() {{}}
window.showSaveFilePicker = window.showSaveFilePicker || function () {{}};
localStorage.setItem('x','y');
</script>
<script type="application/json" id="deck-persisted-state">{{"v":3,"revision":1,"updatedAt":"1970-01-01T00:00:00.001Z","deckHtml":""}}</script>
<style>.filmstrip-thumb-host .slide {{ opacity:1; }}</style>
</body>
</html>
"""


def port_html(slides: str, mode: str = "slots") -> str:
    return PORT_BASE_HTML.format(mode=mode, slides=slides)


PORT_GOOD_FIXTURES = {
    "ported_slot_mode": port_html("""
<section class="slide" id="slide-0">
  <h1 data-edit-slot="s0-title-1" data-slot-type="title" data-slot-locked-layout="true">Editable title</h1>
  <p data-edit-slot="s0-slot-1" data-slot-type="text" data-slot-locked-layout="true">Editable body copy</p>
  <div class="slide-edit-layer" aria-hidden="true"></div>
</section>
"""
    ),
}


PORT_FIXTURES = {
    "static_body": port_html("""
<section class="slide" id="slide-0">
  <h1 data-edit-slot="title">Editable title</h1>
  <p>Static body copy</p>
</section>
"""
    ),
    "static_card_text": port_html("""
<section class="slide" id="slide-0">
  <h1 data-edit-slot="title">Editable title</h1>
  <div class="card-copy">Static card copy</div>
</section>
"""
    ),
    "static_image_placeholder": port_html("""
<section class="slide" id="slide-0">
  <h1 data-edit-slot="title">Editable title</h1>
  <div class="img-placeholder">Image Placeholder</div>
</section>
"""
    ),
    "missing_port_slot_editor": port_html("""
<section class="slide" id="slide-0">
  <h1 data-edit-slot="s0-title">Editable title</h1>
</section>
""").replace(' id="swiss-slot-edit-runtime-js"', "").replace("class SlotEditor {}", ""),
    "missing_template_edit_mode": PORT_BASE_HTML.replace(' data-template-edit-mode="{mode}"', "").format(
        mode="slots",
        slides="""
<section class="slide" id="slide-0">
  <h1 data-edit-slot="s0-title">Editable title</h1>
</section>
""",
    ),
    "ported_assets_media_path": port_html("""
<section class="slide" id="slide-0">
  <h1 data-edit-slot="title">Editable title</h1>
  <img data-edit-slot="image" data-slot-type="image" src="assets/photo.png" alt="">
</section>
"""
    ),
    "component_mode_default": port_html("""
<section class="slide" id="slide-0">
  <h1 data-edit-slot="title">Editable title</h1>
  <p data-edit-slot="body">Editable body</p>
</section>
""", mode="components"
    ),
    "build_time_component_object": port_html("""
<section class="slide" id="slide-0">
  <h1 data-edit-slot="title">Editable title</h1>
  <p data-edit-slot="body">Editable body</p>
  <div class="slide-edit-layer" aria-hidden="true">
    <div class="slide-object template-component-object" data-slide-object data-oid="component-title">
      <div class="slide-object-text">Lifted title</div>
    </div>
  </div>
</section>
"""
    ),
}

PORT_EXPECTED_MESSAGES = {
    "static_body": "body/card authored text is not slot-editable",
    "static_card_text": "body/card authored text is not slot-editable",
    "static_image_placeholder": "image content is not slot-editable",
    "missing_port_slot_editor": "ported editable slots require the injected SlotEditor runtime",
    "missing_template_edit_mode": "missing or invalid data-template-edit-mode",
    "ported_assets_media_path": "media src uses non-portable assets/ path",
    "component_mode_default": 'ported template must default to data-template-edit-mode="slots"',
    "build_time_component_object": "ported template contains build-time component objects",
}


def load_builder():
    builder_path = ROOT / "scripts" / "build-template-port-decks.py"
    spec = importlib.util.spec_from_file_location("build_template_port_decks", builder_path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Unable to load {builder_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def run_validator(path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), "--file", str(path)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=15,
    )


def run_port_validator(path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(PORT_VALIDATOR), "--file", str(path)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=15,
    )


def main() -> int:
    builder = load_builder()
    with tempfile.TemporaryDirectory(prefix="editable-contract-fixtures-") as tmp:
        tmp_dir = Path(tmp)
        errors: list[str] = []
        for name, source in FIXTURES.items():
            path = tmp_dir / f"{name}.html"
            path.write_text(source, encoding="utf-8")
            proc = run_validator(path)
            expected = EXPECTED_MESSAGES[name]
            output = proc.stdout + proc.stderr
            if proc.returncode == 0:
                errors.append(f"{name}: validator unexpectedly passed")
            elif expected not in output:
                errors.append(f"{name}: missing expected message {expected!r}; got {output!r}")
        for name, source in PORT_GOOD_FIXTURES.items():
            path = tmp_dir / f"{name}.html"
            path.write_text(source, encoding="utf-8")
            proc = run_port_validator(path)
            output = proc.stdout + proc.stderr
            if proc.returncode != 0:
                errors.append(f"{name}: port validator unexpectedly failed; got {output!r}")
        for name, source in PORT_FIXTURES.items():
            path = tmp_dir / f"{name}.html"
            path.write_text(source, encoding="utf-8")
            proc = run_port_validator(path)
            expected = PORT_EXPECTED_MESSAGES[name]
            output = proc.stdout + proc.stderr
            if proc.returncode == 0:
                errors.append(f"{name}: port validator unexpectedly passed")
            elif expected not in output:
                errors.append(f"{name}: missing expected port message {expected!r}; got {output!r}")
        classifications = {
            "card": builder.classify_template_node("div", ' class="card"', "<h3>Feature</h3><p>Copy</p>"),
            "stat": builder.classify_template_node("div", ' class="stat-block"', "<div>42%</div><p>Growth</p>"),
            "image": builder.classify_template_node("img", ' src="x.png"', ""),
            "quote": builder.classify_template_node("div", ' class="quote-container"', "<blockquote>Quote</blockquote>"),
            "decor": builder.classify_template_node("div", ' class="gridline"', ""),
        }
        expected_classifications = {
            "card": "component",
            "stat": "component",
            "image": "slot",
            "quote": "component",
            "decor": "locked",
        }
        for name, expected in expected_classifications.items():
            if classifications.get(name) != expected:
                errors.append(f"classifier {name}: expected {expected}, got {classifications.get(name)}")
        componentized = builder.prepare_componentized_sections([
            """<section class="slide">
  <h1>Title</h1>
  <div class="card"><h3>Card title</h3><p>Card copy</p></div>
  <div class="gridline"></div>
</section>"""
        ])
        if 'data-template-edit-mode="components"' in componentized:
            errors.append("componentized sections should not set document-level edit mode")
        if 'data-slide-object' not in componentized or 'data-component-source-slot=' not in componentized:
            errors.append("componentized fixture did not create slide objects")
        if 'class="gridline" data-slide-object' in componentized:
            errors.append("decorative gridline was componentized")
        if errors:
            print("Editable contract fixture tests failed:")
            for error in errors:
                print(f"- {error}")
            return 2
    print(f"Editable contract fixtures passed ({len(PORT_GOOD_FIXTURES)} good, {len(FIXTURES) + len(PORT_FIXTURES)} failing cases).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
