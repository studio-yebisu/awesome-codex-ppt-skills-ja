#!/usr/bin/env python3
"""Run Chrome-headless smoke tests for editable deck interactions.

The default test is intentionally sampled, not a full preset matrix. It verifies
the runtime behavior that static validation cannot prove: edit mode activation,
slot editing for ported templates, Pages copy/new-page workflows, persistence,
export cleanup, and viewport overflow. Set SMOKE_PRESET_MATRIX=ported to run the
lightweight interaction checks against every ported template.
"""

from __future__ import annotations

import json
import os
import platform
import html
import importlib.util
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "examples" / "editable-deck-reference.html"
SAMPLES = [
    REFERENCE,
    ROOT / "examples" / "generated" / "presets" / "bold-signal.html",
    ROOT / "examples" / "generated" / "presets" / "soft-editorial.html",
    ROOT / "examples" / "generated" / "presets" / "monochrome-ledger.html",
]
PORTED_SAMPLE_NAMES = {"soft-editorial.html", "monochrome-ledger.html"}
VIEWPORTS = [
    ("desktop", 1280, 720),
    ("mobile-portrait", 390, 844),
    ("mobile-landscape", 844, 390),
]
try:
    TIMEOUT_SECONDS = int(os.environ.get("SMOKE_TIMEOUT_SECONDS", "75"))
except ValueError as e:
    raise SystemExit("SMOKE_TIMEOUT_SECONDS must be an integer") from e
try:
    SMOKE_RETRIES = int(os.environ.get("SMOKE_RETRIES", "1"))
except ValueError as e:
    raise SystemExit("SMOKE_RETRIES must be an integer") from e


def find_chrome() -> str | None:
    env = os.environ.get("CHROME_PATH")
    if env and Path(env).is_file():
        return env
    if platform.system() == "Darwin":
        p = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
        if p.is_file():
            return str(p)
    for name in ("google-chrome-stable", "google-chrome", "chromium", "chromium-browser"):
        found = shutil.which(name)
        if found:
            return found
    return None


def load_builder_ports():
    builder_path = ROOT / "scripts" / "build-template-port-decks.py"
    spec = importlib.util.spec_from_file_location("build_template_port_decks", builder_path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Unable to load {builder_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.PORTS


def sample_paths() -> list[Path]:
    matrix = os.environ.get("SMOKE_PRESET_MATRIX", "").strip().lower()
    if not matrix:
        return SAMPLES
    if matrix == "ported":
        return [ROOT / "examples" / "generated" / "presets" / f"{port.out_slug}.html" for port in load_builder_ports()]
    if matrix == "components":
        return [
            ROOT / "examples" / "generated" / "presets" / "soft-editorial.html",
            ROOT / "examples" / "generated" / "presets" / "monochrome-ledger.html",
            ROOT / "examples" / "generated" / "presets" / "retro-windows.html",
            ROOT / "examples" / "generated" / "presets" / "sakura-chroma.html",
            ROOT / "examples" / "generated" / "presets" / "grove.html",
            ROOT / "examples" / "generated" / "presets" / "pink-script.html",
        ]
    if matrix == "bounds":
        return sorted((ROOT / "examples" / "generated" / "presets").glob("*.html"))
    if matrix == "all":
        return sorted((ROOT / "examples" / "generated" / "presets").glob("*.html"))
    raise SystemExit("SMOKE_PRESET_MATRIX must be empty, 'ported', 'components', 'bounds', or 'all'")


def chrome_eval(chrome: str, html_path: Path, width: int, height: int, script: str) -> dict:
    with tempfile.TemporaryDirectory(prefix="editable-smoke-") as tmp:
        tmp_dir = Path(tmp)
        harness = tmp_dir / html_path.name
        source = html_path.read_text(encoding="utf-8")
        test_script_json = json.dumps(script)
        timeout_ms = TIMEOUT_SECONDS * 1000 - 1000
        injected = """
<script id="editable-smoke-harness">
const testScript = __TEST_SCRIPT__;
function finish(payload) {{
  document.body.setAttribute('data-result', JSON.stringify(payload));
  document.title = 'RESULT:' + JSON.stringify(payload);
}}
window.addEventListener('load', () => {{
  document.documentElement.setAttribute('data-mobile-adaptation', 'enabled');
  setTimeout(() => {{
    try {{
      const fn = new Function('return (async () => {\\n' + testScript + '\\n})()');
      Promise.resolve(fn()).then((payload) => finish(payload)).catch((err) => finish({ok:false,error:String(err && err.message || err)}));
    }} catch (err) {{
      finish({ok:false,error:String(err && err.message || err)});
    }}
  }}, 250);
}});
setTimeout(() => finish({ok:false,error:'timeout'}), __TIMEOUT_MS__);
</script>
""".replace("__TEST_SCRIPT__", test_script_json).replace("__TIMEOUT_MS__", str(timeout_ms))
        if "</body>" in source:
            source = source.replace("</body>", injected + "\n</body>", 1)
        else:
            source += injected
        harness.write_text(source, encoding="utf-8")
        cmd = [
            chrome,
            "--headless=new",
            "--disable-gpu",
            "--disable-background-networking",
            "--disable-default-apps",
            "--disable-dev-shm-usage",
            "--disable-extensions",
            "--disable-web-security",
            "--allow-file-access-from-files",
            "--hide-scrollbars",
            "--no-first-run",
            "--no-default-browser-check",
            f"--window-size={width},{height}",
            "--virtual-time-budget=12000",
            "--dump-dom",
            harness.resolve().as_uri(),
        ]
        attempts = max(1, SMOKE_RETRIES + 1)
        last_timeout = None
        for attempt in range(attempts):
            try:
                proc = subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT_SECONDS)
                break
            except subprocess.TimeoutExpired as e:
                last_timeout = e
                if attempt + 1 >= attempts:
                    raise
        else:
            raise last_timeout or RuntimeError("Chrome smoke did not run")
        dumped = proc.stdout
        attr_match = re.search(r'data-result="([^"]+)"', dumped)
        title_match = re.search(r"<title>RESULT:(.*?)</title>", dumped, flags=re.S)
        raw = attr_match.group(1) if attr_match else (title_match.group(1) if title_match else "")
        if not raw:
            return {"ok": False, "error": (proc.stderr or dumped)[-500:]}
        return json.loads(html.unescape(raw))


EDIT_MODE_SCRIPT = r"""
const edit = document.getElementById('editToggle');
const pages = document.getElementById('pagesToggle');
const hover = document.getElementById('deckLeftHover');
if (!edit) throw new Error('missing Edit button');
if (!pages) throw new Error('missing Pages button');
if (!hover) throw new Error('missing deckLeftHover');
document.body.classList.remove('deck-edit-mode', 'slide-anim-paused');
edit.classList.remove('active', 'show');
pages.classList.remove('active', 'show');
edit.click();
await new Promise((resolve) => setTimeout(resolve, 40));
const clickActivated = document.body.classList.contains('deck-edit-mode') && edit.classList.contains('active');
document.dispatchEvent(new KeyboardEvent('keydown', {key: 'E', bubbles: true, cancelable: true}));
await new Promise((resolve) => setTimeout(resolve, 40));
const keyExited = !document.body.classList.contains('deck-edit-mode');
document.dispatchEvent(new KeyboardEvent('keydown', {key: 'e', bubbles: true, cancelable: true}));
await new Promise((resolve) => setTimeout(resolve, 40));
const keyActivated = document.body.classList.contains('deck-edit-mode') && edit.classList.contains('active');
hover.dispatchEvent(new MouseEvent('mouseenter', {bubbles: true}));
await new Promise((resolve) => setTimeout(resolve, 40));
const hoverShowsControls = edit.classList.contains('show') && pages.classList.contains('show');
return {ok: clickActivated && keyExited && keyActivated && hoverShowsControls, clickActivated, keyExited, keyActivated, hoverShowsControls};
"""


PRESENTATION_TOOLS_SCRIPT = r"""
const laser = document.getElementById('laserToggle');
const fullscreen = document.getElementById('fullscreenToggle');
const edit = document.getElementById('editToggle');
const layer = document.getElementById('deckLaserLayer');
const dot = document.getElementById('laserDot');
if (!laser) throw new Error('missing Laser button');
if (!fullscreen) throw new Error('missing Fullscreen button');
if (!layer) throw new Error('missing laser layer');
if (!dot) throw new Error('missing laser dot');
document.body.classList.remove('deck-edit-mode', 'deck-laser-mode');
laser.classList.remove('active', 'show');
laser.click();
await new Promise((resolve) => setTimeout(resolve, 30));
const laserActivated = document.body.classList.contains('deck-laser-mode') && laser.classList.contains('active');
const pointer = (target, type, x, y, buttons = 1) => target.dispatchEvent(new PointerEvent(type, {
  bubbles: true,
  cancelable: true,
  pointerId: 42,
  pointerType: 'mouse',
  clientX: x,
  clientY: y,
  buttons
}));
pointer(document, 'pointermove', 120, 140, 0);
const dotMoved = dot.style.transform.includes('111px') && dot.style.transform.includes('131px');
let exportedHtml = '';
const originalCreateObjectURL = URL.createObjectURL;
URL.createObjectURL = (blob) => {
  if (blob && typeof blob.text === 'function') {
    blob.text().then((text) => { exportedHtml = text; });
  }
  return 'blob:editable-smoke-laser';
};
URL.revokeObjectURL = () => {};
const originalClick = HTMLAnchorElement.prototype.click;
HTMLAnchorElement.prototype.click = function () {};
const exportButton = document.getElementById('btnExport');
if (!exportButton) throw new Error('missing Export button');
exportButton.click();
for (let i = 0; i < 160 && !exportedHtml; i++) {
  await new Promise((resolve) => setTimeout(resolve, 50));
}
if (!exportedHtml) return {ok: false, error: 'export produced no HTML'};
URL.createObjectURL = originalCreateObjectURL;
HTMLAnchorElement.prototype.click = originalClick;
const exportedDoc = new DOMParser().parseFromString(exportedHtml, 'text/html');
const exportClean = !!exportedHtml
  && !!exportedDoc.querySelector('#laserToggle')
  && !!exportedDoc.querySelector('#fullscreenToggle')
  && exportedHtml.includes('class LaserPointerController')
  && exportedHtml.includes('requestFullscreen')
  && !exportedDoc.body.classList.contains('deck-laser-mode')
  && !exportedDoc.querySelector('.laser-trail-segment')
  && !exportedDoc.querySelector('#laserToggle.active');
laser.click();
laser.click();
await new Promise((resolve) => setTimeout(resolve, 30));
edit.click();
await new Promise((resolve) => setTimeout(resolve, 40));
const editClosesLaser = document.body.classList.contains('deck-edit-mode') && !document.body.classList.contains('deck-laser-mode');
document.dispatchEvent(new KeyboardEvent('keydown', {key: 'e', bubbles: true, cancelable: true}));
await new Promise((resolve) => setTimeout(resolve, 40));
let fullscreenCalls = 0;
Object.defineProperty(document.documentElement, 'requestFullscreen', {
  configurable: true,
  value: () => {
    fullscreenCalls += 1;
    return Promise.resolve();
  }
});
fullscreen.click();
await new Promise((resolve) => setTimeout(resolve, 40));
return {
  ok: laserActivated && dotMoved && editClosesLaser && fullscreenCalls === 1 && exportClean,
  laserActivated,
  dotMoved,
  editClosesLaser,
  fullscreenCalls,
  exportClean
};
"""


PAGES_SCRIPT = r"""
const sidebar = document.getElementById('slideSidebar');
const pages = document.getElementById('pagesToggle');
if (!pages || !sidebar) throw new Error('missing Pages sidebar');
pages.click();
const root = document.querySelector('.slides-offset');
const before = root.querySelectorAll(':scope > section.slide').length;
const storageKey = 'editable-deck:' + (document.documentElement.getAttribute('data-deck-id') || 'default');
localStorage.removeItem(storageKey);
const firstCopy = document.querySelector('[data-filmstrip-action="copy"]');
if (!firstCopy) throw new Error('missing copy button');
firstCopy.click();
const afterCopy = root.querySelectorAll(':scope > section.slide').length;
const newPage = document.getElementById('btnNewPage');
if (!newPage) throw new Error('missing new page button');
newPage.click();
const afterNew = root.querySelectorAll(':scope > section.slide').length;
const ids = Array.from(root.querySelectorAll(':scope > section.slide')).map((s) => s.id);
const oids = Array.from(root.querySelectorAll('[data-oid]')).map((o) => o.getAttribute('data-oid'));
const uniqueIds = new Set(ids).size === ids.length;
const uniqueOids = new Set(oids).size === oids.length;
const undo = document.getElementById('btnUndo');
if (undo) undo.click();
const afterUndo = root.querySelectorAll(':scope > section.slide').length;
let exportedHtml = '';
const originalCreateObjectURL = URL.createObjectURL;
URL.createObjectURL = (blob) => {
  if (blob && typeof blob.text === 'function') {
    blob.text().then((text) => { exportedHtml = text; });
  }
  return 'blob:editable-smoke';
};
URL.revokeObjectURL = () => {};
const originalClick = HTMLAnchorElement.prototype.click;
HTMLAnchorElement.prototype.click = function () {};
window.showSaveFilePicker = async () => ({
  createWritable: async () => ({
    write: async () => {},
    close: async () => {}
  })
});
const save = document.getElementById('btnSave');
if (!save) throw new Error('missing Save button');
save.click();
const saved = JSON.parse(localStorage.getItem(storageKey) || '{}');
const savedCount = saved.deckHtml ? (saved.deckHtml.match(/<section\b[^>]*\bclass="[^"]*\bslide\b/g) || []).length : 0;
const exportButton = document.getElementById('btnExport');
if (!exportButton) throw new Error('missing Export button');
exportButton.click();
for (let i = 0; i < 160 && !exportedHtml; i++) {
  await new Promise((resolve) => setTimeout(resolve, 50));
}
if (!exportedHtml) return {ok: false, error: 'export produced no HTML'};
URL.createObjectURL = originalCreateObjectURL;
HTMLAnchorElement.prototype.click = originalClick;
const exportedDoc = new DOMParser().parseFromString(exportedHtml, 'text/html');
const exportChecks = {
  hasDoctype: exportedHtml.includes('<!DOCTYPE html>'),
  noEditMode: !exportedDoc.body.classList.contains('deck-edit-mode'),
  noSidebarOpen: !exportedDoc.body.classList.contains('deck-sidebar-open'),
  noSelected: !exportedDoc.querySelector('.slide-object.is-selected'),
  noMediaFileInput: !exportedDoc.querySelector('.slide-object-media-file, input[type="file"]'),
  emptyFilmstrip: !exportedDoc.querySelector('#filmstripList') || exportedDoc.querySelector('#filmstripList').children.length === 0
};
const exportClean = Object.values(exportChecks).every(Boolean);
const originalHtml = root.innerHTML;
root.innerHTML = '<section class="slide" id="temporary-slide"></section>';
root.innerHTML = saved.deckHtml || '';
const afterLoad = root.querySelectorAll(':scope > section.slide').length;
root.innerHTML = originalHtml;
return {
  ok: afterCopy === before + 1 && afterNew === before + 2 && afterUndo === before + 1 &&
    uniqueIds && uniqueOids && savedCount === afterUndo && afterLoad === afterUndo && exportClean,
  before, afterCopy, afterNew, afterUndo, savedCount, afterLoad, uniqueIds, uniqueOids, exportClean, exportChecks
};
"""


SLOT_EDIT_SCRIPT = r"""
const root = document.querySelector('.slides-offset');
if (!root) throw new Error('missing slides root');
const slot = root.querySelector('[data-edit-slot][data-slot-type="text"], [data-edit-slot][data-slot-type="metric"], [data-edit-slot][data-slot-type="table-cell"]');
if (!slot) return {ok: true, skipped: true, reason: 'no editable slot'};
const edit = document.getElementById('editToggle');
if (!edit) throw new Error('missing Edit button');
const storageKey = 'editable-deck:' + (document.documentElement.getAttribute('data-deck-id') || 'default');
localStorage.removeItem(storageKey);
if (!document.body.classList.contains('deck-edit-mode')) {
  edit.click();
  await new Promise((resolve) => setTimeout(resolve, 40));
}
if (!document.body.classList.contains('deck-edit-mode')) throw new Error('edit mode did not activate before slot edit');
const before = slot.innerHTML;
const marker = 'Smoke edited slot text';
slot.click();
await new Promise((resolve) => setTimeout(resolve, 40));
const becameEditable = slot.getAttribute('contenteditable') === 'true' || slot.isContentEditable;
slot.textContent = marker;
slot.dispatchEvent(new InputEvent('input', {bubbles: true, inputType: 'insertText', data: marker}));
const focusSink = document.createElement('button');
focusSink.type = 'button';
focusSink.textContent = 'focus sink';
focusSink.style.cssText = 'position:fixed;left:-9999px;top:-9999px;';
document.body.appendChild(focusSink);
focusSink.focus();
slot.blur();
slot.dispatchEvent(new FocusEvent('focusout', {bubbles: true, relatedTarget: focusSink}));
await new Promise((resolve) => setTimeout(resolve, 80));
focusSink.remove();
const committed = slot.getAttribute('contenteditable') !== 'true' && slot.textContent === marker;
const undo = document.getElementById('btnUndo');
const redo = document.getElementById('btnRedo');
if (!undo || !redo) throw new Error('missing undo/redo buttons');
const undoEnabled = !undo.disabled;
undo.click();
await new Promise((resolve) => setTimeout(resolve, 40));
const undoRestored = slot.innerHTML === before;
redo.click();
await new Promise((resolve) => setTimeout(resolve, 40));
const redoApplied = slot.textContent === marker;
const save = document.getElementById('btnSave');
if (!save) throw new Error('missing Save button');
window.showSaveFilePicker = async () => ({
  createWritable: async () => ({
    write: async () => {},
    close: async () => {}
  })
});
save.click();
const saved = JSON.parse(localStorage.getItem(storageKey) || '{}');
const savedHasEdit = typeof saved.deckHtml === 'string' && saved.deckHtml.includes(marker);
let exportedHtml = '';
const originalCreateObjectURL = URL.createObjectURL;
URL.createObjectURL = (blob) => {
  if (blob && typeof blob.text === 'function') {
    blob.text().then((text) => { exportedHtml = text; });
  }
  return 'blob:editable-slot-smoke';
};
URL.revokeObjectURL = () => {};
const originalClick = HTMLAnchorElement.prototype.click;
HTMLAnchorElement.prototype.click = function () {};
const exportButton = document.getElementById('btnExport');
if (!exportButton) throw new Error('missing Export button');
exportButton.click();
for (let i = 0; i < 160 && !exportedHtml; i++) {
  await new Promise((resolve) => setTimeout(resolve, 50));
}
if (!exportedHtml) return {ok: false, error: 'export produced no HTML'};
URL.createObjectURL = originalCreateObjectURL;
HTMLAnchorElement.prototype.click = originalClick;
const exportedDoc = new DOMParser().parseFromString(exportedHtml, 'text/html');
const exportChecks = {
  noEditableSlot: !exportedDoc.querySelector('[data-edit-slot][contenteditable="true"]'),
  noDeckHtmlBefore: !exportedDoc.querySelector('[data-_deck-html-before]'),
  hasMarker: exportedHtml.includes(marker)
};
const exportClean = Object.values(exportChecks).every(Boolean);
return {ok: becameEditable && committed && undoEnabled && undoRestored && redoApplied && savedHasEdit && exportClean,
  becameEditable, committed, undoEnabled, undoRestored, redoApplied, savedHasEdit, exportClean, exportChecks};
"""


COMPONENT_UNLOCK_SCRIPT = r"""
window.confirm = () => true;
const root = document.querySelector('.slides-offset');
if (!root) throw new Error('missing slides root');
const edit = document.getElementById('editToggle');
if (!edit) throw new Error('missing Edit button');
const unlock = document.getElementById('btnUnlockLayout');
if (!unlock) throw new Error('missing Unlock layout button');
if (!document.body.classList.contains('deck-edit-mode')) {
  edit.click();
  await new Promise((resolve) => setTimeout(resolve, 40));
}
if (!document.body.classList.contains('deck-edit-mode')) throw new Error('edit mode did not activate');
const currentSlide = root.querySelector(':scope > section.slide.visible, :scope > section.slide.is-active') ||
  root.querySelector(':scope > section.slide');
if (!currentSlide) throw new Error('missing current slide');
const visibleSlot = (slot) => {
  if (!slot || slot.closest('.slide-edit-layer')) return false;
  if (slot.getAttribute('data-slot-type') === 'image') return false;
  const text = slot.textContent.replace(/\s+/g, ' ').trim();
  if (!text) return false;
  const style = getComputedStyle(slot);
  if (style.display === 'none' || style.visibility === 'hidden') return false;
  const rect = slot.getBoundingClientRect();
  return rect.width > 0 && rect.height > 0;
};
const titleTokens = new Set(['deck-title', 'display', 'h', 'h1', 'h2', 'h3', 'h4', 'headline', 'heading', 'hero', 'hero-title', 'lockup', 'slide-title', 'stmt', 'title', 'ttl']);
const bodyTokens = new Set(['body', 'card-copy', 'card-text', 'copy', 'desc', 'description', 'eyebrow', 'kicker', 'lead', 'lede', 'note', 'paragraph', 'quote', 'subtitle', 'text']);
const metricTokens = new Set(['amount', 'metric', 'percent', 'stat', 'stat-value', 'value']);
const hasToken = (slot, set) => Array.from(slot.classList || []).some((token) => set.has(token.toLowerCase()));
const unlockableShape = (slot) => {
  const tag = slot.tagName.toLowerCase();
  const slotType = (slot.getAttribute('data-slot-type') || '').toLowerCase();
  if (/^h[1-4]$/.test(tag) || hasToken(slot, titleTokens)) return true;
  if (['p', 'li', 'blockquote', 'cite'].includes(tag) || hasToken(slot, bodyTokens)) return true;
  const text = slot.textContent.replace(/\s+/g, ' ').trim();
  return (slotType === 'metric' || hasToken(slot, metricTokens)) && /[0-9]/.test(text) && text.length > 2;
};
const sourceSlot = Array.from(currentSlide.querySelectorAll('[data-edit-slot]:not([data-slot-type="image"])')).find((slot) => visibleSlot(slot) && unlockableShape(slot));
if (!sourceSlot) return {ok: true, skipped: true, reason: 'no eligible unlockable slot'};
const sourceSlotId = sourceSlot.getAttribute('data-edit-slot');
const normalizeText = (value) => String(value || '').replace(/\s+/g, ' ').trim();
const sourceText = normalizeText(sourceSlot.textContent);
const sourceTag = sourceSlot.tagName;
const sourceClasses = Array.from(sourceSlot.classList);
const before = getComputedStyle(sourceSlot);
const beforeStyle = {
  fontFamily: before.fontFamily,
  fontSize: before.fontSize,
  fontWeight: before.fontWeight,
  color: before.color
};
const sourceInline = sourceSlot.querySelector('span, strong, em, b, i, a, small, cite, mark, code');
const beforeInlineStyle = sourceInline ? (() => {
  const cs = getComputedStyle(sourceInline);
  return {selector: sourceInline.tagName, fontFamily: cs.fontFamily, fontSize: cs.fontSize, fontWeight: cs.fontWeight, color: cs.color};
})() : null;
unlock.click();
await new Promise((resolve) => setTimeout(resolve, 120));
const escapedSlotId = CSS.escape(sourceSlotId);
const component = currentSlide.querySelector(`[data-component-source-slot="${escapedSlotId}"]`);
const moved = component && component.querySelector(`[data-edit-slot="${escapedSlotId}"]`);
const sameSlotNodes = Array.from(currentSlide.querySelectorAll(`[data-edit-slot="${escapedSlotId}"]`));
const duplicateOutsideComponent = sameSlotNodes.some((node) => !component || !component.contains(node));
const after = moved ? getComputedStyle(moved) : null;
const fontSizeDelta = after ? Math.abs(parseFloat(after.fontSize) - parseFloat(beforeStyle.fontSize)) : Infinity;
const movedInline = moved && beforeInlineStyle ? moved.querySelector(beforeInlineStyle.selector.toLowerCase()) : null;
const afterInlineStyle = movedInline ? getComputedStyle(movedInline) : null;
const inlineFontSizeDelta = afterInlineStyle && beforeInlineStyle ? Math.abs(parseFloat(afterInlineStyle.fontSize) - parseFloat(beforeInlineStyle.fontSize)) : 0;
const classChecks = sourceClasses.map((className) => ({className, kept: !!moved && moved.classList.contains(className)}));
const tagKept = !!moved && moved.tagName === sourceTag;
const textKept = !!moved && normalizeText(moved.textContent) === sourceText;
const classesKept = classChecks.every((entry) => entry.kept);
const styleChecks = {
  fontFamily: !!after && after.fontFamily === beforeStyle.fontFamily,
  fontSize: fontSizeDelta <= 1,
  fontWeight: !!after && after.fontWeight === beforeStyle.fontWeight,
  color: !!after && after.color === beforeStyle.color
};
const inlineStyleKept = !beforeInlineStyle || (!!afterInlineStyle
  && afterInlineStyle.fontFamily === beforeInlineStyle.fontFamily
  && inlineFontSizeDelta <= 1
  && afterInlineStyle.fontWeight === beforeInlineStyle.fontWeight
  && afterInlineStyle.color === beforeInlineStyle.color);
let dragMoved = false;
if (component) {
  const move = component.querySelector('.slide-object-move');
  if (move) {
    const r = move.getBoundingClientRect();
    const startLeft = component.style.left;
    const startTop = component.style.top;
    const EventCtor = window.PointerEvent || window.MouseEvent;
    const pointer = (target, type, x, y) => target.dispatchEvent(new EventCtor(type, {
      bubbles: true,
      cancelable: true,
      pointerId: 1,
      pointerType: 'mouse',
      isPrimary: true,
      clientX: x,
      clientY: y,
      button: 0,
      buttons: type === 'pointerup' ? 0 : 1
    }));
    pointer(move, 'pointerdown', r.left + r.width / 2, r.top + r.height / 2);
    await new Promise((resolve) => setTimeout(resolve, 20));
    pointer(document, 'pointermove', r.left + r.width / 2 + 96, r.top + r.height / 2 + 64);
    await new Promise((resolve) => setTimeout(resolve, 20));
    pointer(document, 'pointerup', r.left + r.width / 2 + 96, r.top + r.height / 2 + 64);
    await new Promise((resolve) => setTimeout(resolve, 60));
    dragMoved = component.style.left !== startLeft || component.style.top !== startTop;
  }
}
const checks = {
  componentExists: !!component,
  componentIsObject: !!component && component.hasAttribute('data-slide-object'),
  movedExists: !!moved,
  movedSlotIdKept: !!moved && moved.getAttribute('data-edit-slot') === sourceSlotId,
  noDuplicateOutsideComponent: !duplicateOutsideComponent,
  tagKept,
  classesKept,
  textKept,
  fontFamilyKept: styleChecks.fontFamily,
  fontSizeKept: styleChecks.fontSize,
  fontWeightKept: styleChecks.fontWeight,
  colorKept: styleChecks.color,
  inlineStyleKept,
  dragMoved
};
return {
  ok: Object.values(checks).every(Boolean),
  checks,
  sourceSlotId,
  sourceTag,
  movedTag: moved && moved.tagName,
  sourceClasses,
  missingClasses: classChecks.filter((entry) => !entry.kept).map((entry) => entry.className),
  sourceText,
  movedText: moved && normalizeText(moved.textContent),
  beforeStyle,
  afterStyle: after && {fontFamily: after.fontFamily, fontSize: after.fontSize, fontWeight: after.fontWeight, color: after.color},
  beforeInlineStyle,
  afterInlineStyle: afterInlineStyle && {fontFamily: afterInlineStyle.fontFamily, fontSize: afterInlineStyle.fontSize, fontWeight: afterInlineStyle.fontWeight, color: afterInlineStyle.color},
  fontSizeDelta,
  inlineFontSizeDelta,
  sameSlotCount: sameSlotNodes.length,
  outsideDuplicateCount: sameSlotNodes.filter((node) => !component || !component.contains(node)).length
};
"""


UNDO_REDO_CHAIN_SCRIPT = r"""
window.confirm = () => true;
const root = document.querySelector('.slides-offset');
if (!root) throw new Error('missing slides root');
const edit = document.getElementById('editToggle');
if (!edit) throw new Error('missing Edit button');
const undo = document.getElementById('btnUndo');
const redo = document.getElementById('btnRedo');
if (!undo || !redo) throw new Error('missing undo/redo buttons');
const storageKey = 'editable-deck:' + (document.documentElement.getAttribute('data-deck-id') || 'default');
localStorage.removeItem(storageKey);
/* Enter edit mode */
if (!document.body.classList.contains('deck-edit-mode')) {
  edit.click();
  await new Promise(r => setTimeout(r, 40));
}
const initialSlideCount = root.querySelectorAll(':scope > section.slide').length;
const initialObjectCount = root.querySelectorAll('[data-slide-object]').length;
const historyOps = [];
const pointer = (target, type, x, y) => {
  const EventCtor = window.PointerEvent || window.MouseEvent;
  const event = new EventCtor(type, {
    pointerId: 1,
    pointerType: 'mouse',
    isPrimary: true,
    clientX: x,
    clientY: y,
    bubbles: true,
    cancelable: true,
    buttons: type === 'pointerup' ? 0 : 1,
    button: 0
  });
  target.dispatchEvent(event);
};
/* Op 1: New page */
const btnNew = document.getElementById('btnNewPage');
if (!btnNew) throw new Error('missing New Page button');
btnNew.click();
await new Promise(r => setTimeout(r, 60));
const afterNew = root.querySelectorAll(':scope > section.slide').length;
const newPageAdded = afterNew === initialSlideCount + 1;
if (newPageAdded) historyOps.push('newPage');
/* Op 2: Copy first slide */
const copyBtn = document.querySelector('[data-filmstrip-action="copy"]');
if (!copyBtn) throw new Error('missing copy button');
copyBtn.click();
await new Promise(r => setTimeout(r, 60));
const afterAdds = root.querySelectorAll(':scope > section.slide').length;
const copyAdded = afterAdds === initialSlideCount + 2;
if (copyAdded) historyOps.push('copy');
/* Op 3: Move an object if one exists */
const firstObj = root.querySelector('[data-slide-object]');
let moveChanged = false;
if (!firstObj) throw new Error('missing slide object for move test');
const moveHandle = firstObj.querySelector('.slide-object-move');
if (!moveHandle) throw new Error('missing move handle for move test');
{
  const r = firstObj.getBoundingClientRect();
  const beforeLeft = firstObj.style.left;
  const beforeTop = firstObj.style.top;
  const startX = r.left + Math.min(12, Math.max(4, r.width / 2));
  const startY = r.top + Math.min(12, Math.max(4, r.height / 2));
  pointer(moveHandle, 'pointerdown', startX, startY);
  await new Promise(r => setTimeout(r, 20));
  pointer(document, 'pointermove', startX + 36, startY + 24);
  await new Promise(r => setTimeout(r, 20));
  pointer(document, 'pointerup', startX + 36, startY + 24);
  await new Promise(r => setTimeout(r, 80));
  moveChanged = firstObj.style.left !== beforeLeft || firstObj.style.top !== beforeTop;
  if (moveChanged) historyOps.push('move');
}
/* Op 4: Delete the moved object with Backspace */
const deleteBefore = root.querySelectorAll('[data-slide-object]').length;
const selectRect = firstObj.getBoundingClientRect();
pointer(firstObj, 'pointerdown', selectRect.left + selectRect.width / 2, selectRect.top + Math.min(10, Math.max(4, selectRect.height / 2)));
await new Promise(r => setTimeout(r, 40));
const objectSelectedForDelete = firstObj.classList.contains('is-selected');
document.dispatchEvent(new KeyboardEvent('keydown', {key: 'Backspace', bubbles: true, cancelable: true}));
await new Promise(r => setTimeout(r, 80));
const deleteAfter = root.querySelectorAll('[data-slide-object]').length;
const deleteChanged = deleteAfter === deleteBefore - 1;
if (deleteChanged) historyOps.push('delete');
const afterOps = root.querySelectorAll(':scope > section.slide').length;
const afterOpsObjectCount = root.querySelectorAll('[data-slide-object]').length;
/* Now undo until the structural state returns, with a small allowance for
   incidental text/history records generated by focus handoff. */
const undoStepsExpected = historyOps.length;
let undoStepsRun = 0;
for (let i = 0; i < 8; i++) {
  const slideCountNow = root.querySelectorAll(':scope > section.slide').length;
  const objectCountNow = root.querySelectorAll('[data-slide-object]').length;
  if (slideCountNow === initialSlideCount && objectCountNow === initialObjectCount) break;
  if (undo.disabled) break;
  undo.click();
  undoStepsRun += 1;
  await new Promise(r => setTimeout(r, 40));
}
const afterUndoAll = root.querySelectorAll(':scope > section.slide').length;
const afterUndoObjectCount = root.querySelectorAll('[data-slide-object]').length;
const undoRestored = afterUndoAll === initialSlideCount && afterUndoObjectCount === initialObjectCount;
/* Now redo until the post-operation state returns. */
let redoStepsRun = 0;
for (let i = 0; i < 8; i++) {
  const slideCountNow = root.querySelectorAll(':scope > section.slide').length;
  const objectCountNow = root.querySelectorAll('[data-slide-object]').length;
  if (slideCountNow === afterOps && objectCountNow === afterOpsObjectCount) break;
  if (redo.disabled) break;
  redo.click();
  redoStepsRun += 1;
  await new Promise(r => setTimeout(r, 40));
}
const afterRedoAll = root.querySelectorAll(':scope > section.slide').length;
const afterRedoObjectCount = root.querySelectorAll('[data-slide-object]').length;
const redoMatches = afterRedoAll === afterOps && afterRedoObjectCount === afterOpsObjectCount;
/* Verify IDs are still unique after redo */
const ids = Array.from(root.querySelectorAll(':scope > section.slide')).map(s => s.id);
const oids = Array.from(root.querySelectorAll('[data-oid]')).map(o => o.getAttribute('data-oid'));
const uniqueIds = new Set(ids).size === ids.length;
const uniqueOids = new Set(oids).size === oids.length;
return {
  ok: newPageAdded && copyAdded && moveChanged && objectSelectedForDelete && deleteChanged && undoRestored && redoMatches && uniqueIds && uniqueOids,
  initialSlideCount, initialObjectCount, afterNew, afterAdds, afterOps, afterOpsObjectCount,
  afterUndoAll, afterUndoObjectCount, afterRedoAll, afterRedoObjectCount,
  newPageAdded, copyAdded, moveChanged, objectSelectedForDelete, deleteChanged,
  undoRestored, redoMatches, uniqueIds, uniqueOids,
  historyOps, undoStepsExpected, undoStepsRun, redoStepsRun
};
"""

EXPORT_INTEGRITY_SCRIPT = r"""
const root = document.querySelector('.slides-offset');
if (!root) throw new Error('missing slides root');
const edit = document.getElementById('editToggle');
if (!edit) throw new Error('missing Edit button');
const storageKey = 'editable-deck:' + (document.documentElement.getAttribute('data-deck-id') || 'default');
localStorage.removeItem(storageKey);
/* Enter edit mode and select an object */
if (!document.body.classList.contains('deck-edit-mode')) {
  edit.click();
  await new Promise(r => setTimeout(r, 40));
}
const obj = root.querySelector('[data-slide-object]');
if (obj) {
  obj.click();
  await new Promise(r => setTimeout(r, 40));
}
/* Save */
const save = document.getElementById('btnSave');
if (!save) throw new Error('missing Save button');
window.showSaveFilePicker = async () => ({
  createWritable: async () => ({
    write: async () => {},
    close: async () => {}
  })
});
save.click();
const saved = JSON.parse(localStorage.getItem(storageKey) || '{}');
/* Export */
let exportedHtml = '';
let blobReceived = false;
const origCreate = URL.createObjectURL;
URL.createObjectURL = (blob) => {
  blobReceived = true;
  /* Store blob for synchronous read after click */
  window.__exportedBlob = blob;
  return 'blob:export-integrity';
};
URL.revokeObjectURL = () => {};
const origClick = HTMLAnchorElement.prototype.click;
HTMLAnchorElement.prototype.click = function () {};
const exportBtn = document.getElementById('btnExport');
if (!exportBtn) throw new Error('missing Export button');
exportBtn.click();
for (let i = 0; i < 160 && !exportedHtml; i++) {
  await new Promise(r => setTimeout(r, 50));
  try {
    if (window.__exportedBlob) exportedHtml = await window.__exportedBlob.text();
  } catch(e) {}
}
/* Read the captured blob */
if (!exportedHtml && window.__exportedBlob) {
  try {
    exportedHtml = await window.__exportedBlob.text();
  } catch(e) {
    /* fallback: try arrayBuffer */
    try {
      const buf = await window.__exportedBlob.arrayBuffer();
      exportedHtml = new TextDecoder().decode(buf);
    } catch(e2) {}
  }
}
if (!exportedHtml) return {ok: false, error: 'export produced no HTML', blobReceived};
URL.createObjectURL = origCreate;
HTMLAnchorElement.prototype.click = origClick;
const exportedDoc = new DOMParser().parseFromString(exportedHtml, 'text/html');
const slideCount = exportedDoc.querySelectorAll('section.slide').length;
const originalCount = root.querySelectorAll(':scope > section.slide').length;
const checks = {
  hasDoctype: exportedHtml.includes('<!DOCTYPE html>'),
  hasPersistedState: !!exportedDoc.querySelector('#deck-persisted-state[type="application/json"]'),
  hasStandaloneBuilder: exportedHtml.includes('function buildStandaloneHtml'),
  noEditMode: !exportedDoc.body.classList.contains('deck-edit-mode'),
  noSidebarOpen: !exportedDoc.body.classList.contains('deck-sidebar-open'),
  noSelected: !exportedDoc.querySelector('.slide-object.is-selected'),
  noFileInput: !exportedDoc.querySelector('input[type="file"]'),
  noFilmstripClones: !exportedDoc.querySelector('#filmstripList') || exportedDoc.querySelector('#filmstripList').children.length === 0,
  hasAllSlides: slideCount === originalCount,
  noEditableTrue: !exportedDoc.querySelector('[contenteditable="true"]'),
  savedHasContent: typeof saved.deckHtml === 'string' && saved.deckHtml.length > 100,
  noAssetsMediaPath: !/<(?:img|video|source)\b[^>]*\bsrc=["']assets\//i.test(exportedHtml),
};
const allPass = Object.values(checks).every(Boolean);
return {ok: allPass, slideCount, originalCount, checks};
"""

EXPORT_EMBEDDED_STATE_SCRIPT = r"""
const root = document.querySelector('.slides-offset');
if (!root) throw new Error('missing slides root');
const edit = document.getElementById('editToggle');
if (!document.body.classList.contains('deck-edit-mode')) {
  edit.click();
  await new Promise(r => setTimeout(r, 40));
}
const text = root.querySelector('.slide-object-text');
if (!text) throw new Error('missing editable text');
const marker = 'Portable export marker ' + Date.now();
text.innerHTML = marker;
let exportedHtml = '';
const origCreate = URL.createObjectURL;
URL.createObjectURL = (blob) => {
  window.__exportedBlob = blob;
  return 'blob:embedded-state';
};
URL.revokeObjectURL = () => {};
const origClick = HTMLAnchorElement.prototype.click;
HTMLAnchorElement.prototype.click = function () {};
document.getElementById('btnExport').click();
for (let i = 0; i < 160 && !exportedHtml; i++) {
  await new Promise(r => setTimeout(r, 60));
  if (window.__exportedBlob) exportedHtml = await window.__exportedBlob.text();
}
if (!exportedHtml) return {ok: false, error: 'export produced no HTML'};
URL.createObjectURL = origCreate;
HTMLAnchorElement.prototype.click = origClick;
const exportedDoc = new DOMParser().parseFromString(exportedHtml, 'text/html');
const stateEl = exportedDoc.querySelector('#deck-persisted-state[type="application/json"]');
let state = null;
try { state = stateEl ? JSON.parse(stateEl.textContent || '{}') : null; } catch(e) {}
const checks = {
  markerInDom: exportedDoc.querySelector('.slides-offset') && exportedDoc.querySelector('.slides-offset').innerHTML.includes(marker),
  markerInState: !!state && typeof state.deckHtml === 'string' && state.deckHtml.includes(marker),
  hasRevision: !!state && Number(state.revision) > 0,
  noAssetsMediaPath: !/<(?:img|video|source)\b[^>]*\bsrc=["']assets\//i.test(exportedHtml),
};
return {ok: Object.values(checks).every(Boolean), checks};
"""

SAVE_PORTABILITY_SCRIPT = r"""
const root = document.querySelector('.slides-offset');
if (!root) throw new Error('missing slides root');
const save = document.getElementById('btnSave');
if (!save) throw new Error('missing Save button');
const text = root.querySelector('.slide-object-text');
if (!text) throw new Error('missing editable text');
const marker = 'Portable save marker ' + Date.now();
text.innerHTML = marker;
let fileWrite = '';
let fileClosed = false;
window.showSaveFilePicker = async () => ({
  createWritable: async () => ({
    write: async (chunk) => { fileWrite += String(chunk); },
    close: async () => { fileClosed = true; }
  })
});
save.click();
for (let i = 0; i < 160 && !fileClosed; i++) await new Promise(r => setTimeout(r, 60));
const fileDoc = new DOMParser().parseFromString(fileWrite, 'text/html');
const fileState = fileDoc.querySelector('#deck-persisted-state[type="application/json"]');
const fileOk = fileClosed && fileWrite.includes(marker) && !!fileState;
let fallbackHtml = '';
window.showSaveFilePicker = undefined;
const origCreate = URL.createObjectURL;
URL.createObjectURL = (blob) => {
  window.__fallbackBlob = blob;
  return 'blob:save-fallback';
};
URL.revokeObjectURL = () => {};
const origClick = HTMLAnchorElement.prototype.click;
HTMLAnchorElement.prototype.click = function () {};
save.click();
for (let i = 0; i < 160 && !fallbackHtml; i++) {
  await new Promise(r => setTimeout(r, 60));
  if (window.__fallbackBlob) fallbackHtml = await window.__fallbackBlob.text();
}
if (!fallbackHtml) return {ok: false, error: 'fallback save produced no HTML', fileOk, fileClosed, fileBytes: fileWrite.length};
URL.createObjectURL = origCreate;
HTMLAnchorElement.prototype.click = origClick;
const fallbackDoc = new DOMParser().parseFromString(fallbackHtml, 'text/html');
const fallbackOk = fallbackHtml.includes(marker) && !!fallbackDoc.querySelector('#deck-persisted-state[type="application/json"]');
return {ok: fileOk && fallbackOk, fileOk, fallbackOk, fileClosed, fileBytes: fileWrite.length, fallbackBytes: fallbackHtml.length};
"""

ADD_ELEMENT_STRESS_SCRIPT = r"""
const root = document.querySelector('.slides-offset');
if (!root) throw new Error('missing slides root');
const edit = document.getElementById('editToggle');
if (!document.body.classList.contains('deck-edit-mode')) {
  edit.click();
  await new Promise(r => setTimeout(r, 40));
}
const slide = root.querySelector(':scope > section.slide');
if (!slide) throw new Error('missing slide');
const existingLayer = slide.querySelector(':scope > .slide-edit-layer');
if (existingLayer) existingLayer.remove();
const addBtn = document.getElementById('btnAddElement');
const addMenu = document.getElementById('deckAddElementMenu');
if (!addBtn || !addMenu) throw new Error('missing Add element UI');
const added = [];
async function addKind(kind) {
  addBtn.click();
  await new Promise(r => setTimeout(r, 40));
  addBtn.dispatchEvent(new MouseEvent('mouseleave', {bubbles:true}));
  const hover = document.getElementById('deckLeftHover');
  if (hover) hover.dispatchEvent(new MouseEvent('mouseleave', {bubbles:true}));
  await new Promise(r => setTimeout(r, 460));
  const menuStillOpen = addMenu.classList.contains('open') && addMenu.hidden === false;
  const before = slide.querySelectorAll('[data-slide-object]').length;
  const btn = addMenu.querySelector('[data-add-kind="' + kind + '"]');
  if (!btn) throw new Error('missing add kind ' + kind);
  btn.click();
  await new Promise(r => setTimeout(r, 80));
  const layer = slide.querySelector(':scope > .slide-edit-layer');
  const obj = layer && Array.from(layer.querySelectorAll('[data-slide-object]')).find((el) => el.getAttribute('data-object-type') === kind);
  const after = slide.querySelectorAll('[data-slide-object]').length;
  added.push({kind, menuStillOpen, layerCreated: !!layer, countChanged: after === before + 1, selected: !!obj && obj.classList.contains('is-selected')});
}
await addKind('text');
await addKind('image');
await addKind('video');
const undo = document.getElementById('btnUndo');
if (!undo) throw new Error('missing undo button');
const beforeUndo = slide.querySelectorAll('[data-slide-object]').length;
undo.click();
await new Promise(r => setTimeout(r, 80));
const afterUndo = slide.querySelectorAll('[data-slide-object]').length;
const undoRemoved = afterUndo === beforeUndo - 1;
return {ok: added.every((entry) => entry.menuStillOpen && entry.layerCreated && entry.countChanged && entry.selected) && undoRemoved, added, undoRemoved};
"""

MEDIA_PORTABILITY_SCRIPT = r"""
const root = document.querySelector('.slides-offset');
if (!root) throw new Error('missing slides root');
const edit = document.getElementById('editToggle');
if (!document.body.classList.contains('deck-edit-mode')) {
  edit.click();
  await new Promise(r => setTimeout(r, 40));
}
const addBtn = document.getElementById('btnAddElement');
const addMenu = document.getElementById('deckAddElementMenu');
async function addKind(kind) {
  addBtn.click();
  await new Promise(r => setTimeout(r, 30));
  addMenu.querySelector('[data-add-kind="' + kind + '"]').click();
  await new Promise(r => setTimeout(r, 60));
  const objects = Array.from(root.querySelectorAll('.slide-object[data-object-type="' + kind + '"]'));
  return objects[objects.length - 1];
}
const imageObj = await addKind('image');
const videoObj = await addKind('video');
const tinyPng = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/p9sAAAAASUVORK5CYII=';
const tinyVideo = 'data:video/mp4;base64,AAAA';
imageObj.querySelector('.slide-object-graphic').innerHTML = '<img alt="" src="' + tinyPng + '">';
videoObj.querySelector('.slide-object-graphic').innerHTML = '<video controls src="' + tinyVideo + '"></video>';
let exportedHtml = '';
const origCreate = URL.createObjectURL;
URL.createObjectURL = (blob) => {
  window.__mediaBlob = blob;
  return 'blob:media-portability';
};
URL.revokeObjectURL = () => {};
const origClick = HTMLAnchorElement.prototype.click;
HTMLAnchorElement.prototype.click = function () {};
document.getElementById('btnExport').click();
for (let i = 0; i < 160 && !exportedHtml; i++) {
  await new Promise(r => setTimeout(r, 60));
  if (window.__mediaBlob) exportedHtml = await window.__mediaBlob.text();
}
if (!exportedHtml) return {ok: false, error: 'export produced no HTML'};
URL.createObjectURL = origCreate;
HTMLAnchorElement.prototype.click = origClick;
const exportedDoc = new DOMParser().parseFromString(exportedHtml, 'text/html');
const media = Array.from(exportedDoc.querySelectorAll('.slides-offset img[src], .slides-offset video[src], .slides-offset source[src]'));
let state = null;
try {
  const stateEl = exportedDoc.querySelector('#deck-persisted-state');
  state = stateEl ? JSON.parse(stateEl.textContent || '{}') : null;
} catch(e) {}
const checks = {
  hasMedia: media.length >= 2,
  allData: media.every((el) => (el.getAttribute('src') || '').startsWith('data:')),
  noFileInput: !exportedDoc.querySelector('input[type="file"]'),
  noAssetsMediaPath: !/<(?:img|video|source)\b[^>]*\bsrc=["']assets\//i.test(exportedHtml),
  stateHasDataMedia: !!state && /src=\\"data:|src="data:/.test(JSON.stringify(state.deckHtml || '')),
};
return {ok: Object.values(checks).every(Boolean), checks, mediaCount: media.length};
"""

RTE_SMOKE_SCRIPT = r"""
/* B1: Bold/italic toggle, B2: Font family, B3: Font size,
   B6: Backspace delete, B7: Add text element */
const root = document.querySelector('.slides-offset');
if (!root) throw new Error('missing slides root');
const edit = document.getElementById('editToggle');
if (!edit) throw new Error('missing Edit button');
const undo = document.getElementById('btnUndo');
if (!undo) throw new Error('missing undo button');
const results = {};
const pointer = (target, type, x, y) => {
  const EventCtor = window.PointerEvent || window.MouseEvent;
  target.dispatchEvent(new EventCtor(type, {
    pointerId: 1,
    pointerType: 'mouse',
    isPrimary: true,
    clientX: x,
    clientY: y,
    bubbles: true,
    cancelable: true,
    buttons: type === 'pointerup' ? 0 : 1,
    button: 0
  }));
};
const selectNodeContents = (el) => {
  const range = document.createRange();
  range.selectNodeContents(el);
  const sel = window.getSelection();
  sel.removeAllRanges();
  sel.addRange(range);
};

/* Enter edit mode */
if (!document.body.classList.contains('deck-edit-mode')) {
  edit.click();
  await new Promise(r => setTimeout(r, 60));
}

/* B7: Add text element */
const addBtn = document.getElementById('btnAddElement');
const addMenu = document.getElementById('deckAddElementMenu');
if (!addBtn || !addMenu) throw new Error('missing Add element UI');
const objectCountBeforeAdd = root.querySelectorAll('[data-slide-object]').length;
addBtn.click();
await new Promise(r => setTimeout(r, 60));
const textOption = addMenu.querySelector('[data-add-kind="text"]');
if (!textOption) throw new Error('missing Add element text option');
textOption.click();
await new Promise(r => setTimeout(r, 80));
const textObjects = Array.from(root.querySelectorAll('.slide-object[data-object-type="text"]'));
const newObj = textObjects[textObjects.length - 1];
const objectCountAfterAdd = root.querySelectorAll('[data-slide-object]').length;
results.addElementText = !!newObj && objectCountAfterAdd === objectCountBeforeAdd + 1;
if (!newObj) throw new Error('text object was not added');
const textEl = newObj.querySelector('.slide-object-text');
if (!textEl) throw new Error('added text object missing .slide-object-text');

/* Focus text and show RTE toolbar */
{
  const tr = textEl.getBoundingClientRect();
  pointer(textEl, 'pointerdown', tr.left + tr.width / 2, tr.top + Math.min(12, Math.max(4, tr.height / 2)));
}
await new Promise(r => setTimeout(r, 80));
results.textBecameEditable = textEl.getAttribute('contenteditable') === 'true' || textEl.isContentEditable;
if (!results.textBecameEditable) throw new Error('added text did not become contenteditable');
textEl.textContent = 'Smoke RTE text';
selectNodeContents(textEl);
await new Promise(r => setTimeout(r, 20));

/* Check RTE toolbar exists and has expected controls */
const rteToolbar = document.getElementById('rteToolbar');
results.rteToolbarExists = !!rteToolbar;
if (!rteToolbar) throw new Error('missing RTE toolbar');
const boldBtn = rteToolbar.querySelector('button[data-cmd="bold"]');
const italicBtn = rteToolbar.querySelector('button[data-cmd="italic"]');
const fontDrawer = rteToolbar.querySelector('.rte-drawer-trigger[data-rte-drawer="font"]');
const pxDrawer = rteToolbar.querySelector('.rte-drawer-trigger[data-rte-drawer="px"]');
results.hasBoldBtn = !!boldBtn;
results.hasItalicBtn = !!italicBtn;
results.hasFontDrawer = !!fontDrawer;
results.hasSizeDrawer = !!pxDrawer;
if (!boldBtn || !italicBtn || !fontDrawer || !pxDrawer) throw new Error('missing expected RTE controls');

/* B1: Bold toggle through the toolbar button */
const beforeBoldHtml = textEl.innerHTML;
boldBtn.click();
await new Promise(r => setTimeout(r, 60));
results.boldApplied = textEl.innerHTML !== beforeBoldHtml && /<(b|strong|span)\b|font-weight/i.test(textEl.innerHTML);
selectNodeContents(textEl);
boldBtn.click();
await new Promise(r => setTimeout(r, 40));
results.boldToggleOff = true;

/* B2: Font family via drawer */
selectNodeContents(textEl);
fontDrawer.click();
await new Promise(r => setTimeout(r, 40));
const serifBtn = rteToolbar.querySelector('button[data-font*="Georgia"]');
if (!serifBtn) throw new Error('missing serif font option');
const beforeFontHtml = textEl.innerHTML;
serifBtn.click();
await new Promise(r => setTimeout(r, 60));
results.fontApplied = textEl.innerHTML !== beforeFontHtml && /font-family/i.test(textEl.innerHTML);

/* B3: Fixed px size via drawer */
selectNodeContents(textEl);
pxDrawer.click();
await new Promise(r => setTimeout(r, 40));
const pxBtn = rteToolbar.querySelector('button[data-size-px="36"]');
if (!pxBtn) throw new Error('missing 36px option');
const beforePxHtml = textEl.innerHTML;
pxBtn.click();
await new Promise(r => setTimeout(r, 60));
results.pxApplied = textEl.innerHTML !== beforePxHtml && /font-size/i.test(textEl.innerHTML);

/* B6: Delete object with Backspace, then undo */
textEl.blur();
textEl.setAttribute('contenteditable', 'false');
await new Promise(r => setTimeout(r, 40));
const nr = newObj.getBoundingClientRect();
pointer(newObj, 'pointerdown', nr.left + nr.width / 2, nr.top + Math.min(10, Math.max(4, nr.height / 2)));
await new Promise(r => setTimeout(r, 60));
results.objectSelected = newObj.classList.contains('is-selected');
const beforeDeleteCount = root.querySelectorAll('[data-slide-object]').length;
document.dispatchEvent(new KeyboardEvent('keydown', {key: 'Backspace', bubbles: true, cancelable: true}));
await new Promise(r => setTimeout(r, 80));
const afterDeleteCount = root.querySelectorAll('[data-slide-object]').length;
results.backspaceDelete = afterDeleteCount === beforeDeleteCount - 1;
if (!undo.disabled) {
  for (let i = 0; i < 6; i++) {
    const countNow = root.querySelectorAll('[data-slide-object]').length;
    if (countNow === beforeDeleteCount) break;
    if (undo.disabled) break;
    undo.click();
    await new Promise(r => setTimeout(r, 60));
  }
}
const afterUndoCount = root.querySelectorAll('[data-slide-object]').length;
results.deleteUndoRestore = afterUndoCount === beforeDeleteCount;

const allOk = results.addElementText &&
  results.textBecameEditable &&
  results.rteToolbarExists &&
  results.hasBoldBtn &&
  results.hasItalicBtn &&
  results.hasFontDrawer &&
  results.hasSizeDrawer &&
  results.boldApplied &&
  results.fontApplied &&
  results.pxApplied &&
  results.objectSelected &&
  results.backspaceDelete &&
  results.deleteUndoRestore;
return {ok: allOk, ...results};
"""

EDITABLE_BOUNDS_SCRIPT = r"""
await document.fonts.ready;
const root = document.querySelector('.slides-offset');
if (!root) throw new Error('missing slides root');
const slides = root.querySelectorAll(':scope > section.slide');
const clipped = [];
const exempted = [];
const exemptErrors = [];
const TOLERANCE = 5;
for (let si = 0; si < slides.length; si++) {
  const slide = slides[si];
  const sr = slide.getBoundingClientRect();
  /* Use the slide's own bounding rect, not the viewport.
     The slide is 100vh; elements must stay inside it. */
  const slideBottom = sr.bottom;
  const slideRight = sr.right;
  const slideLeft = sr.left;
  const slideTop = sr.top;
  /* Check data-edit-slot elements */
  const slots = slide.querySelectorAll('[data-edit-slot]');
  for (const slot of slots) {
    const style = getComputedStyle(slot);
    if (style.display === 'none' || style.visibility === 'hidden' || style.opacity === '0') continue;
    if (slot.offsetParent === null && style.position !== 'fixed') continue;
    const r = slot.getBoundingClientRect();
    if (r.width < 1 || r.height < 1) continue;
    if (r.bottom > slideBottom + TOLERANCE || r.right > slideRight + TOLERANCE ||
        r.left < slideLeft - TOLERANCE || r.top < slideTop - TOLERANCE) {
      const label = slot.getAttribute('data-edit-slot') || '';
      if (slot.hasAttribute('data-bounds-exempt')) {
        const reason = slot.getAttribute('data-bounds-exempt') || '';
        if (!reason.trim()) {
          exemptErrors.push({slide: slide.id || 'slide-' + si, type: 'slot', label: label});
        } else {
          exempted.push({slide: slide.id || 'slide-' + si, label: label, reason: reason});
        }
        continue;
      }
      const over = {};
      if (r.bottom > slideBottom + TOLERANCE) over.bottom = Math.round(r.bottom - slideBottom);
      if (r.right  > slideRight  + TOLERANCE) over.right  = Math.round(r.right  - slideRight);
      if (r.left   < slideLeft   - TOLERANCE) over.left   = Math.round(slideLeft - r.left);
      if (r.top    < slideTop    - TOLERANCE) over.top    = Math.round(slideTop - r.top);
      clipped.push({
        slide: slide.id || 'slide-' + si,
        type: 'slot',
        label: label,
        slotType: slot.getAttribute('data-slot-type') || '',
        slideH: Math.round(sr.height),
        over: over,
      });
    }
  }
  /* Check data-slide-object elements */
  const objects = slide.querySelectorAll('[data-slide-object]');
  for (const obj of objects) {
    const style = getComputedStyle(obj);
    if (style.display === 'none' || style.visibility === 'hidden') continue;
    const r = obj.getBoundingClientRect();
    if (r.width < 1 || r.height < 1) continue;
    if (r.bottom > slideBottom + TOLERANCE || r.right > slideRight + TOLERANCE ||
        r.left < slideLeft - TOLERANCE || r.top < slideTop - TOLERANCE) {
      const label = obj.getAttribute('data-oid') || '';
      if (obj.hasAttribute('data-bounds-exempt')) {
        const reason = obj.getAttribute('data-bounds-exempt') || '';
        if (!reason.trim()) {
          exemptErrors.push({slide: slide.id || 'slide-' + si, type: 'object', label: label});
        } else {
          exempted.push({slide: slide.id || 'slide-' + si, label: label, reason: reason});
        }
        continue;
      }
      const over = {};
      if (r.bottom > slideBottom + TOLERANCE) over.bottom = Math.round(r.bottom - slideBottom);
      if (r.right  > slideRight  + TOLERANCE) over.right  = Math.round(r.right  - slideRight);
      if (r.left   < slideLeft   - TOLERANCE) over.left   = Math.round(slideLeft - r.left);
      if (r.top    < slideTop    - TOLERANCE) over.top    = Math.round(slideTop - r.top);
      clipped.push({
        slide: slide.id || 'slide-' + si,
        type: 'object',
        label: label,
        objectType: obj.getAttribute('data-object-type') || '',
        slideH: Math.round(sr.height),
        over: over,
      });
    }
  }
}
return {ok: clipped.length === 0 && exemptErrors.length === 0, clippedCount: clipped.length, clipped: clipped, exemptedCount: exempted.length, exempted: exempted, exemptErrors: exemptErrors, totalSlides: slides.length};
"""


OVERFLOW_SCRIPT = r"""
const root = document.querySelector('.slides-offset');
const doc = document.documentElement;
const body = document.body;
const overflow = [
  {id: 'documentElement', scrollWidth: doc.scrollWidth, clientWidth: doc.clientWidth},
  {id: 'body', scrollWidth: body.scrollWidth, clientWidth: body.clientWidth},
  {id: 'slides-offset', scrollWidth: root.scrollWidth, clientWidth: root.clientWidth}
].filter((s) => s.scrollWidth > s.clientWidth + 2);
return {ok: overflow.length === 0, overflow};
"""


def _format_edges(over: dict) -> str:
    parts = [f"{edge}:{over[edge]}" for edge in ("bottom", "right", "left", "top") if edge in over]
    return ",".join(parts) if parts else "none"


BOUNDS_ARTIFACT_PATH = ROOT / ".smoke-artifacts" / "bounds-report.json"


def _load_bounds_report() -> dict:
    try:
        existing = json.loads(BOUNDS_ARTIFACT_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return existing if isinstance(existing, dict) else {}


def _bounds_entry(result: dict) -> dict:
    return {
        "clippedCount": result.get("clippedCount", 0),
        "clipped": result.get("clipped", []),
        "exemptedCount": result.get("exemptedCount", 0),
        "exempted": result.get("exempted", []),
        "exemptErrors": result.get("exemptErrors", []),
        "totalSlides": result.get("totalSlides", 0),
    }


def _flush_bounds_report(report: dict) -> None:
    BOUNDS_ARTIFACT_PATH.parent.mkdir(parents=True, exist_ok=True)
    BOUNDS_ARTIFACT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")


def _bounds_failure(rel: str, result: dict, *, clip_limit: int, show_slide_height: bool) -> str | None:
    """Return an error string for an out-of-bounds result, or None if within bounds."""
    exempt_errors = result.get("exemptErrors", [])
    if exempt_errors:
        detail = "; ".join(
            f"{e.get('slide','?')}:{e.get('type','?')}:{e.get('label','')}"
            for e in exempt_errors[:8]
        )
        return (
            f"{rel} bounds: {len(exempt_errors)} exemptions missing a reason — {detail} "
            f"(report: {BOUNDS_ARTIFACT_PATH})"
        )
    if not result.get("ok"):
        clipped = result.get("clipped", [])
        summary = "; ".join(
            f"{c['slide']}:{c['type']}:{c.get('label') or c.get('objectType','')} "
            f"edges={_format_edges(c.get('over', {}))}"
            + (f" (slideH={c.get('slideH','?')})" if show_slide_height else "")
            for c in clipped[:clip_limit]
        )
        return (
            f"{rel} bounds: {result.get('clippedCount',0)} clipped, {result.get('exemptedCount',0)} exempted — {summary} "
            f"(report: {BOUNDS_ARTIFACT_PATH})"
        )
    return None


def main() -> int:
    chrome = find_chrome()
    if not chrome:
        print("No Chrome/Chromium found. Set CHROME_PATH or install Chrome.", file=sys.stderr)
        return 1
    errors: list[str] = []
    samples = sample_paths()
    matrix_lower = os.environ.get("SMOKE_PRESET_MATRIX", "").strip().lower()
    bounds_report = _load_bounds_report()
    bounds_touched = False
    for sample in samples:
        if not sample.is_file():
            errors.append(f"missing sample {sample.relative_to(ROOT)}")
            continue
        if matrix_lower == "bounds":
            result = chrome_eval(chrome, sample, 1280, 720, EDITABLE_BOUNDS_SCRIPT)
            rel = str(sample.relative_to(ROOT))
            bounds_report[rel] = _bounds_entry(result)
            bounds_touched = True
            failure = _bounds_failure(rel, result, clip_limit=8, show_slide_height=True)
            if failure:
                errors.append(failure)
            else:
                print(
                    f"{rel} bounds ok: 0 clipped, {result.get('exemptedCount', 0)} exempted "
                    f"(report: {BOUNDS_ARTIFACT_PATH})"
                )
            continue
        result = chrome_eval(chrome, sample, 1280, 720, EDIT_MODE_SCRIPT)
        if not result.get("ok"):
            errors.append(f"{sample.relative_to(ROOT)} edit mode failed: {result}")
        matrix_mode = bool(os.environ.get("SMOKE_PRESET_MATRIX"))
        if not matrix_mode:
            result = chrome_eval(chrome, sample, 1280, 720, PRESENTATION_TOOLS_SCRIPT)
            if not result.get("ok"):
                errors.append(f"{sample.relative_to(ROOT)} presentation tools failed: {result}")
            result = chrome_eval(chrome, sample, 1280, 720, PAGES_SCRIPT)
            if not result.get("ok"):
                errors.append(f"{sample.relative_to(ROOT)} pages/export interaction failed: {result}")
            # A5: Undo/redo chain stress test (reference deck only in sample mode)
            if sample == REFERENCE:
                result = chrome_eval(chrome, sample, 1280, 720, UNDO_REDO_CHAIN_SCRIPT)
                if not result.get("ok"):
                    errors.append(f"{sample.relative_to(ROOT)} undo/redo chain failed: {result}")
                # Export integrity test
                result = chrome_eval(chrome, sample, 1280, 720, EXPORT_INTEGRITY_SCRIPT)
                if not result.get("ok"):
                    errors.append(f"{sample.relative_to(ROOT)} export integrity failed: {result}")
                result = chrome_eval(chrome, sample, 1280, 720, EXPORT_EMBEDDED_STATE_SCRIPT)
                if not result.get("ok"):
                    errors.append(f"{sample.relative_to(ROOT)} embedded export state failed: {result}")
                result = chrome_eval(chrome, sample, 1280, 720, SAVE_PORTABILITY_SCRIPT)
                if not result.get("ok"):
                    errors.append(f"{sample.relative_to(ROOT)} portable save failed: {result}")
                result = chrome_eval(chrome, sample, 1280, 720, ADD_ELEMENT_STRESS_SCRIPT)
                if not result.get("ok"):
                    errors.append(f"{sample.relative_to(ROOT)} add element stress failed: {result}")
                result = chrome_eval(chrome, sample, 1280, 720, MEDIA_PORTABILITY_SCRIPT)
                if not result.get("ok"):
                    errors.append(f"{sample.relative_to(ROOT)} media portability failed: {result}")
                # B1-B3/B6/B7: RTE and usability smoke
                result = chrome_eval(chrome, sample, 1280, 720, RTE_SMOKE_SCRIPT)
                if not result.get("ok"):
                    errors.append(f"{sample.relative_to(ROOT)} RTE/usability failed: {result}")
        source = sample.read_text(encoding="utf-8")
        if "data-edit-slot=" in source or sample.name in PORTED_SAMPLE_NAMES or matrix_mode:
            result = chrome_eval(chrome, sample, 1280, 720, SLOT_EDIT_SCRIPT)
            if not result.get("ok"):
                errors.append(f"{sample.relative_to(ROOT)} slot edit failed: {result}")
        if os.environ.get("SMOKE_PRESET_MATRIX", "").strip().lower() in {"components", "ported"}:
            result = chrome_eval(chrome, sample, 1280, 720, COMPONENT_UNLOCK_SCRIPT)
            if not result.get("ok"):
                errors.append(f"{sample.relative_to(ROOT)} unlock layout regression failed: {result}")
        # C0: Editable bounds visibility check
        if matrix_lower == "all":
            result = chrome_eval(chrome, sample, 1280, 720, EDITABLE_BOUNDS_SCRIPT)
            rel = str(sample.relative_to(ROOT))
            bounds_report[rel] = _bounds_entry(result)
            bounds_touched = True
            failure = _bounds_failure(rel, result, clip_limit=3, show_slide_height=False)
            if failure:
                errors.append(failure)
            elif result.get("exemptedCount", 0):
                print(
                    f"{rel} bounds ok: {result.get('exemptedCount', 0)} exempted "
                    f"(report: {BOUNDS_ARTIFACT_PATH})"
                )
        if not matrix_mode:
            for label, width, height in VIEWPORTS:
                result = chrome_eval(chrome, sample, width, height, OVERFLOW_SCRIPT)
                if not result.get("ok"):
                    errors.append(f"{sample.relative_to(ROOT)} {label} overflow: {result}")
    if bounds_touched:
        _flush_bounds_report(bounds_report)
    if errors:
        print("Editable deck smoke failed:")
        for error in errors:
            print(f"- {error}")
        return 2
    matrix = os.environ.get("SMOKE_PRESET_MATRIX", "sample") or "sample"
    print(f"Smoke-tested {len(samples)} decks in {matrix} mode using {chrome}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
