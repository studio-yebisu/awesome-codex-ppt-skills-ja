#!/usr/bin/env python3
"""Bundle the deck into a single, self-contained index.html.

Reads the slides (one file per slide in ``slides/``), the engine and the theme,
and inlines everything - script, styles, icons and images - into one portable
``index.html`` you can double-click, email, or host anywhere. No build tools,
no third-party packages: just the Python standard library.

    python3 build.py            # build once -> index.html
    python3 build.py --watch    # rebuild whenever a source file changes
    python3 build.py --open     # build, then open the result in the browser
    python3 build.py --pull     # only bring in-browser edits back into slides/

Text edited in the browser (the deck's Edit button) is saved into index.html.
Every build first copies those edits back into ``slides/*.html``, so rebuilding
never throws them away.

Sources you edit:
    slides/*.html       one <section class="slide"> per file (order = filename)
    themes/<name>/      the look (chosen in deck.config.json)
    deck.css            optional styles for this deck only
    assets/             images referenced from the slides
    deck.config.json    title, language, theme, transition, motion level
"""

import argparse
import base64
import hashlib
import html
import json
import mimetypes
import re
import sys
import time
import webbrowser
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONFIG = ROOT / "deck.config.json"
OUTPUT = ROOT / "index.html"
SLIDES = ROOT / "slides"
ENGINE = ROOT / "engine"
DECK_CSS = ROOT / "deck.css"
# Where a build that could not merge every in-browser edit parks the edited deck.
UNMERGED = ROOT / "index.unmerged-edits.html"

MOTION_LEVELS = ("none", "subtle", "balanced", "lively", "extra")
TRANSITIONS = ("none", "fade", "slide", "zoom", "rise", "blur", "flip")

DEFAULTS = {
    "title": "Presentation",
    "lang": "en",
    "theme": "ink-blue",
    "width": 1920,
    "height": 1080,
    "transition": "fade",
    "motion": "balanced",
    "exit_hint": "Press Esc to exit full screen.",
}

# Matches url(...) inside CSS, a /* ... */ CSS comment, and <img ... src="...">.
CSS_URL_RE = re.compile(r"""url\(\s*["']?([^"')]+)["']?\s*\)""", re.IGNORECASE)
CSS_COMMENT_RE = re.compile(r"/\*.*?\*/", re.DOTALL)
IMG_RE = re.compile(r"""<img\b([^>]*?)\bsrc=["']([^"']+)["']([^>]*?)>""", re.IGNORECASE)
CLASS_RE = re.compile(r"""\bclass\s*=\s*["']([^"']*)["']""", re.IGNORECASE)
ICON_RE = re.compile(r"""<i\b([^>]*?)\bdata-icon=["']([\w-]+)["']([^>]*)>\s*</i>""", re.IGNORECASE)
# An icon as build.py inlines it - used to turn it back into <i data-icon> on pull.
INLINED_ICON_RE = re.compile(r"""(<i\b[^>]*\bdata-icon=["'][\w-]+["'][^>]*>)<svg\b.*?</svg>(</i>)""",
                             re.IGNORECASE | re.DOTALL)
COMPONENT_RE = re.compile(r"@component:\s*([^*\n]+)")


def is_local(ref: str) -> bool:
    """True for paths we should inline (skip http(s):, data:, #anchors)."""
    return not re.match(r"^(?:[a-z]+:|//|#)", ref, re.IGNORECASE)


# --------------------------------------------------------------------------
# Assets: images and fonts become base64 data URIs
# --------------------------------------------------------------------------

# mimetypes.guess_type() partly relies on the OS's own MIME database (e.g. the
# Windows registry), which doesn't reliably know web font types - pin the
# extensions this project actually embeds so every build is deterministic
# regardless of platform, falling back to guess_type() for anything else.
KNOWN_MIME_TYPES = {
    ".woff2": "font/woff2",
    ".woff": "font/woff",
    ".ttf": "font/ttf",
    ".otf": "font/otf",
    ".svg": "image/svg+xml",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".webp": "image/webp",
}


def data_uri(path: Path) -> str:
    mime = KNOWN_MIME_TYPES.get(path.suffix.lower())
    if mime is None:
        mime, _ = mimetypes.guess_type(str(path))
    mime = mime or "application/octet-stream"
    payload = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{payload}"


def inline_css_assets(css: str, css_dir: Path) -> str:
    """Replace url(...) references in a stylesheet with base64 data URIs."""

    def repl(match: re.Match) -> str:
        ref = match.group(1)
        if not is_local(ref):
            return match.group(0)
        asset = (css_dir / ref).resolve()
        if not asset.is_file():
            print(f"  ! missing CSS asset, left as-is: {ref}", file=sys.stderr)
            return match.group(0)
        return f"url({data_uri(asset)})"

    return CSS_URL_RE.sub(repl, css)


def inline_images(markup: str, base: Path) -> str:
    """Replace <img src="..."> with base64 data URIs."""

    def repl(match: re.Match) -> str:
        before, src, after = match.group(1), match.group(2), match.group(3)
        if not is_local(src):
            return match.group(0)
        img = (base / src).resolve()
        if not img.is_file():
            print(f"  ! missing image, left as-is: {src}", file=sys.stderr)
            return match.group(0)
        return f"<img{before}src=\"{data_uri(img)}\"{after}>"

    return IMG_RE.sub(repl, markup)


def image_sources(markup: str, base: Path) -> dict[str, str]:
    """data URI -> original src for every local image a slide references, so
    text pulled back from the built deck gets its real image paths again."""
    found = {}
    for match in IMG_RE.finditer(markup):
        src = match.group(2)
        img = (base / src).resolve()
        if is_local(src) and img.is_file():
            found[data_uri(img)] = src
    return found


# --------------------------------------------------------------------------
# Styles: engine, motion, components (only those used), theme, deck
# --------------------------------------------------------------------------

def read_css(path: Path) -> str:
    # Drop comments first so commented-out url() examples aren't treated as real
    # assets (and to keep the bundle lean).
    css = CSS_COMMENT_RE.sub("", path.read_text(encoding="utf-8"))
    return inline_css_assets(css, path.parent)


def theme_css_files(theme: str) -> list[Path]:
    """The theme's stylesheets, in cascade order: fonts, then tokens, then the
    block styles, then any extra .css the author added."""
    theme_dir = ROOT / "themes" / theme
    order = ["fonts.css", "tokens.css", "slides.css"]
    ordered = [theme_dir / name for name in order if (theme_dir / name).is_file()]
    extra = sorted(p for p in theme_dir.glob("*.css") if p.name not in order)
    return ordered + extra


def used_components(slides_markup: str) -> list[Path]:
    """The engine components a deck actually uses, so an unused chart or
    timeline adds nothing to index.html. Each components/*.css file names what
    triggers it in a header line, e.g. ``@component: stats stat``: a slide
    class equal to one of those names, or starting with ``name__`` / ``name--``,
    pulls the file in. ``[attr]`` triggers on an attribute (``[data-icon]``)."""
    classes = set()
    for value in CLASS_RE.findall(slides_markup):
        classes.update(value.split())
    picked = []
    for path in sorted((ENGINE / "components").glob("*.css")):
        header = COMPONENT_RE.search(path.read_text(encoding="utf-8"))
        triggers = header.group(1).split() if header else [path.stem]
        for trig in triggers:
            if trig.startswith("["):
                hit = trig.strip("[]") in slides_markup
            else:
                hit = any(c == trig or c.startswith((trig + "__", trig + "--")) for c in classes)
            if hit:
                picked.append(path)
                break
    return picked


# --------------------------------------------------------------------------
# Icons: <i data-icon="rocket"></i> gets the SVG inlined
# --------------------------------------------------------------------------

def load_icons() -> dict:
    path = ENGINE / "icons.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {"icons": {}}


def inline_icons(markup: str, icon_set: dict, source: str) -> str:
    icons = icon_set.get("icons", {})
    view_box = icon_set.get("viewBox", "0 0 24 24")

    def repl(match: re.Match) -> str:
        before, name, after = match.groups()
        shapes = icons.get(name)
        if shapes is None:
            print(f"  ! {source}: unknown icon \"{name}\" (see engine/icons.json)", file=sys.stderr)
            return match.group(0)
        svg = f'<svg viewBox="{view_box}" aria-hidden="true" focusable="false">{shapes}</svg>'
        return f'<i{before}data-icon="{name}"{after}>{svg}</i>'

    return ICON_RE.sub(repl, markup)


# --------------------------------------------------------------------------
# A tiny, position-aware HTML tree (standard library only)
#
# In-browser editing needs to know exactly where each editable block sits in
# its slide file, so an edit can be written back without touching anything
# else. This builds a light tree from html.parser that keeps source offsets.
# --------------------------------------------------------------------------

VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
             "meta", "source", "track", "wbr"}
# A start tag of one of these implicitly closes an open <p> (HTML's rule).
CLOSES_P = {"address", "article", "aside", "blockquote", "div", "dl", "fieldset",
            "figure", "footer", "form", "h1", "h2", "h3", "h4", "h5", "h6", "header",
            "hr", "main", "nav", "ol", "p", "pre", "section", "table", "ul"}


class Node:
    __slots__ = ("tag", "attrs", "start", "open_end", "close_start", "end",
                 "children", "parent")

    def __init__(self, tag, attrs, start, open_end, parent=None):
        self.tag = tag
        self.attrs = attrs
        self.start = start            # offset of "<tag"
        self.open_end = open_end      # offset just past the start tag's ">"
        self.close_start = open_end   # offset of "</tag" (inner = open_end..close_start)
        self.end = open_end           # offset just past "</tag>"
        self.children = []
        self.parent = parent

    @property
    def classes(self) -> set:
        return set((self.attrs.get("class") or "").split())

    def iter(self):
        yield self
        for child in self.children:
            yield from child.iter()


class _TreeBuilder(HTMLParser):
    def __init__(self, text: str):
        super().__init__(convert_charrefs=True)
        self.text = text
        self.line_starts = [0] + [i + 1 for i, ch in enumerate(text) if ch == "\n"]
        self.root = Node("#root", {}, 0, 0)
        self.stack = [self.root]

    def _offset(self) -> int:
        line, col = self.getpos()
        return self.line_starts[line - 1] + col

    def _close(self, index: int, close_start: int, end: int) -> None:
        for node in self.stack[index + 1:]:   # implicitly closed by this end tag
            node.close_start = node.end = close_start
        node = self.stack[index]
        node.close_start, node.end = close_start, end
        del self.stack[index:]

    def handle_starttag(self, tag, attrs):
        start = self._offset()
        if tag in CLOSES_P:
            for i in range(len(self.stack) - 1, 0, -1):
                if self.stack[i].tag == "p":
                    self._close(i, start, start)
                    break
        open_end = start + len(self.get_starttag_text())
        node = Node(tag, {k: (v or "") for k, v in attrs}, start, open_end, self.stack[-1])
        self.stack[-1].children.append(node)
        if tag not in VOID_TAGS:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        start = self._offset()
        open_end = start + len(self.get_starttag_text())
        node = Node(tag, {k: (v or "") for k, v in attrs}, start, open_end, self.stack[-1])
        self.stack[-1].children.append(node)

    def handle_endtag(self, tag):
        pos = self._offset()
        end = self.text.find(">", pos) + 1 or len(self.text)
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                self._close(i, pos, end)
                return
        # A stray end tag with nothing open to close: ignore it, like a browser.

    def finish(self) -> Node:
        self.close()
        while len(self.stack) > 1:
            self._close(len(self.stack) - 1, len(self.text), len(self.text))
        self.root.close_start = self.root.end = len(self.text)
        return self.root


def parse_html(text: str) -> Node:
    builder = _TreeBuilder(text)
    builder.feed(text)
    return builder.finish()


def slide_section(root: Node) -> Node | None:
    return next((n for n in root.iter() if n.tag == "section" and "slide" in n.classes), None)


# --------------------------------------------------------------------------
# Editable blocks
#
# The single source of truth for what the browser's Edit mode may change: the
# build stamps these blocks, the engine only ever edits stamped blocks, and the
# pull finds them again in the slide files with the same rules.
# --------------------------------------------------------------------------

EDIT_TAGS = {"h1", "h2", "h3", "h4", "p", "blockquote", "figcaption", "td", "th", "dt", "dd"}
EDIT_CLASSES = {"eyebrow", "display", "title", "subtitle", "lead"}
# A <li> holding one of these is a container: its inner blocks are edited instead.
BLOCKY_TAGS = {"p", "div", "ul", "ol", "dl", "h1", "h2", "h3", "h4", "h5", "h6",
               "blockquote", "table", "pre", "figure", "section"}
# Never editable, nor anything inside: code, drawings, notes (edited through
# their own panel), controls, and zones an author marks decorative or opts out.
NO_EDIT_TAGS = {"pre", "svg", "script", "style", "aside", "button", "select",
                "textarea", "template"}


def _no_edit_zone(node: Node) -> bool:
    return (node.tag in NO_EDIT_TAGS
            or node.attrs.get("aria-hidden") == "true"
            or "data-noedit" in node.attrs)


def _is_editable(node: Node, text: str) -> bool:
    if not text[node.open_end:node.close_start].strip():
        return False                  # nothing to fix in an empty block
    if node.tag in EDIT_TAGS or node.classes & EDIT_CLASSES:
        return True
    return node.tag == "li" and not any(c.tag in BLOCKY_TAGS for c in node.children)


def editable_blocks(section: Node, text: str) -> list[Node]:
    """Outermost editable blocks of a slide, in document order. Outermost only,
    so two editable regions never nest."""
    found = []

    def walk(node: Node) -> None:
        for child in node.children:
            if _no_edit_zone(child):
                continue
            if _is_editable(child, text):
                found.append(child)
            else:
                walk(child)

    walk(section)
    return found


def notes_node(section: Node) -> Node | None:
    return next((n for n in section.iter() if n.tag == "aside" and "notes" in n.classes), None)


def content_hash(inner: str) -> str:
    return hashlib.sha1(inner.strip().encode("utf-8")).hexdigest()[:10]


def stamp_slide(text: str, name: str) -> str:
    """Tag the slide with its source file and every editable block (and the
    speaker notes) with a hash of its original content. That is what lets an
    edit made in the browser find its way back to the right place on pull."""
    section = slide_section(parse_html(text))
    if section is None:
        return text
    inserts = []

    def stamp(node: Node, attr: str, value: str) -> None:
        if attr in node.attrs:
            return
        pos = node.open_end - (2 if text[node.open_end - 2:node.open_end] == "/>" else 1)
        inserts.append((pos, f' {attr}="{html.escape(value)}"'))

    stamp(section, "data-pf-src", name)
    for block in editable_blocks(section, text):
        stamp(block, "data-pf-edit", content_hash(text[block.open_end:block.close_start]))
    notes = notes_node(section)
    if notes is not None:
        stamp(notes, "data-pf-notes", content_hash(text[notes.open_end:notes.close_start]))
    for pos, insert in sorted(inserts, reverse=True):
        text = text[:pos] + insert + text[pos:]
    return text


# --------------------------------------------------------------------------
# Pull: bring text edited in the browser back into slides/*.html
# --------------------------------------------------------------------------

def _squash(s: str) -> str:
    return " ".join(s.split())


def _visible_text(inner: str) -> str:
    return _squash(html.unescape(re.sub(r"<[^>]+>", " ", inner)))


def _clean_inner(inner: str, images: dict[str, str]) -> str:
    """Edited block content as it should read in the slide file: icons back to
    <i data-icon>, images back to their real paths."""
    inner = INLINED_ICON_RE.sub(r"\1\2", inner)
    for uri, src in images.items():
        inner = inner.replace(uri, src)
    return inner


def _keep_edges(old: str, new: str) -> str:
    """Keep the source's own leading/trailing whitespace around the content."""
    lead = old[:len(old) - len(old.lstrip())]
    trail = old[len(old.rstrip()):]
    return lead + new.strip() + trail


def _indent_of(text: str, pos: int) -> str:
    line_start = text.rfind("\n", 0, pos) + 1
    prefix = text[line_start:pos]
    return prefix if not prefix.strip() else "  "


def _format_notes(edited_html: str, notes: Node, indent: str) -> str:
    """Speaker notes from the edit panel (paragraphs and lists only) laid out
    one block per line, indented under their <aside>."""
    lines = []
    for block in notes.children:
        raw = edited_html[block.open_end:block.close_start].strip()
        if block.tag in ("ul", "ol"):
            lines.append(f"{indent}  <{block.tag}>")
            for li in block.children:
                lines.append(f"{indent}    <li>{edited_html[li.open_end:li.close_start].strip()}</li>")
            lines.append(f"{indent}  </{block.tag}>")
        else:
            lines.append(f"{indent}  <{block.tag}>{raw}</{block.tag}>")
    return "\n" + "\n".join(lines) + "\n" + indent


def _safe_slide_name(name: str) -> bool:
    return bool(name) and Path(name).name == name and name.endswith(".html")


def pull_edits(say_if_none: bool = False) -> int:
    """Copy text edited in the browser from index.html back into the slide
    files. Only blocks the browser marked as changed are touched, and only
    where the slide file still holds what the browser started from: a block
    that also changed in slides/ since the last build is never overwritten -
    the edited deck is kept aside instead. Returns the number of edits applied."""
    built = OUTPUT.read_text(encoding="utf-8") if OUTPUT.is_file() else ""
    # Only the slides matter: the engine's own code, after </deck-stage>,
    # mentions these attribute names too.
    end = built.find("</deck-stage>")
    markup = built[:end] if end >= 0 else built
    if "data-pf-changed" not in markup and "data-pf-notes-removed" not in markup:
        if say_if_none:
            print("No in-browser edits to pull.")
        return 0

    applied, unmerged = [], []
    for section in parse_html(markup).iter():
        if section.tag != "section" or "data-pf-src" not in section.attrs:
            continue
        name = section.attrs["data-pf-src"]
        blocks = [n for n in section.iter() if "data-pf-edit" in n.attrs]
        notes = notes_node(section)
        removed = section.attrs.get("data-pf-notes-removed")
        notes_changed = notes is not None and "data-pf-changed" in notes.attrs
        if not (any("data-pf-changed" in n.attrs for n in blocks) or notes_changed or removed):
            continue
        path = SLIDES / name
        if not _safe_slide_name(name) or not path.is_file():
            unmerged.append(f"{name}: slide file not found")
            continue

        source = path.read_text(encoding="utf-8")
        src_section = slide_section(parse_html(source))
        if src_section is None:
            unmerged.append(f"{name}: no <section class=\"slide\"> in the slide file")
            continue
        images = image_sources(source, ROOT)
        src_blocks = editable_blocks(src_section, source)
        by_hash = defaultdict(list)
        for b in src_blocks:
            by_hash[content_hash(source[b.open_end:b.close_start])].append(b)
        edits = []   # (start, end, replacement) in the slide file

        # Text blocks. Same-hash blocks (two identical cells) pair up in order.
        seen = Counter()
        for block in blocks:
            h = block.attrs["data-pf-edit"]
            nth = seen[h]
            seen[h] += 1
            if "data-pf-changed" not in block.attrs:
                continue
            new = _clean_inner(built[block.open_end:block.close_start], images)
            candidates = by_hash.get(h, [])
            if nth < len(candidates):
                target = candidates[nth]
                old = source[target.open_end:target.close_start]
                if _squash(old) != _squash(new):
                    edits.append((target.open_end, target.close_start, _keep_edges(old, new)))
                    applied.append(f"{name}: \"{_visible_text(new)[:60]}\"")
            elif not any(_squash(source[b.open_end:b.close_start]) == _squash(new) for b in src_blocks):
                unmerged.append(f"{name}: \"{_visible_text(new)[:60]}\"")

        # Speaker notes: changed, added, or removed in the browser.
        src_notes = notes_node(src_section)
        src_notes_hash = (content_hash(source[src_notes.open_end:src_notes.close_start])
                          if src_notes is not None else None)
        if notes_changed:
            new_text = _visible_text(built[notes.open_end:notes.close_start])
            expected = notes.attrs.get("data-pf-notes")        # None: notes added
            if src_notes is not None and _visible_text(
                    source[src_notes.open_end:src_notes.close_start]) == new_text:
                pass                                           # already in the file
            elif src_notes is not None and src_notes_hash == expected:
                indent = _indent_of(source, src_notes.start)
                edits.append((src_notes.open_end, src_notes.close_start,
                              _format_notes(built, notes, indent)))
                applied.append(f"{name}: speaker notes")
            elif src_notes is None and expected is None:
                indent = _indent_of(source, src_section.start) + "  "
                at = src_section.close_start
                at = source.rfind("\n", 0, at) if source[source.rfind("\n", 0, at) + 1:at].strip() == "" else at
                block = (f"\n{indent}<aside class=\"notes\">"
                         f"{_format_notes(built, notes, indent)}</aside>")
                edits.append((at, at, block))
                applied.append(f"{name}: speaker notes (new)")
            else:
                unmerged.append(f"{name}: speaker notes")
        elif removed and src_notes is not None:
            if src_notes_hash == removed:
                start = source.rfind("\n", 0, src_notes.start)
                start = start if source[start + 1:src_notes.start].strip() == "" else src_notes.start
                edits.append((start, src_notes.end, ""))
                applied.append(f"{name}: speaker notes removed")
            else:
                unmerged.append(f"{name}: speaker notes (removal)")

        for start, end, replacement in sorted(edits, reverse=True):
            source = source[:start] + replacement + source[end:]
        if edits:
            path.write_text(source, encoding="utf-8", newline="\n")

    if applied:
        print(f"Pulled {len(applied)} in-browser edit(s) into slides/:")
        for line in applied:
            print(f"  + {line}")
    elif say_if_none and not unmerged:
        print("In-browser edits are already in slides/.")
    if unmerged:
        UNMERGED.write_text(built, encoding="utf-8", newline="\n")
        print(f"  ! {len(unmerged)} in-browser edit(s) could not be merged because the "
              f"slide changed since the last build. The edited deck is kept as "
              f"{UNMERGED.name} - copy these over by hand:", file=sys.stderr)
        for line in unmerged:
            print(f"    - {line}", file=sys.stderr)
    return len(applied)


# --------------------------------------------------------------------------
# Build
# --------------------------------------------------------------------------

def load_config() -> dict:
    config = dict(DEFAULTS)
    config.update(json.loads(CONFIG.read_text(encoding="utf-8")))
    for key, allowed in (("motion", MOTION_LEVELS), ("transition", TRANSITIONS)):
        if config[key] not in allowed:
            raise SystemExit(f"error: deck.config.json: \"{key}\" must be one of "
                             f"{', '.join(allowed)} (got {config[key]!r})")
    return config


def slide_files() -> list[Path]:
    return sorted(SLIDES.glob("*.html"))


def source_files() -> list[Path]:
    """Every file whose change should trigger a rebuild (for --watch)."""
    files = [CONFIG, DECK_CSS]
    files += [p for p in ENGINE.rglob("*") if p.is_file()]
    files += slide_files()
    files += [p for p in (ROOT / "themes").rglob("*") if p.is_file()]
    files += [p for p in (ROOT / "assets").rglob("*") if p.is_file()]
    return [f for f in files if f.exists()]


def build() -> Path:
    pull_edits()
    config = load_config()
    theme = config["theme"]
    motion = config["motion"]

    theme_dir = ROOT / "themes" / theme
    if not theme_dir.is_dir():
        raise SystemExit(f"error: theme folder not found: {theme_dir}")
    theme_parts = theme_css_files(theme)
    if not theme_parts:
        raise SystemExit(f"error: no .css files in theme: {theme_dir}")

    slides = slide_files()
    if not slides:
        raise SystemExit("error: no slides found in slides/")
    sources = [p.read_text(encoding="utf-8").strip() for p in slides]

    # Engine first, then the theme (which may restyle components), then the
    # deck's own tweaks. Each part's url() assets are inlined relative to its
    # own folder, so the bundle stays self-contained.
    css_parts = [ENGINE / "base.css"]
    if motion != "none":
        css_parts.append(ENGINE / "motion.css")
    css_parts += used_components("\n".join(sources))
    css_parts += theme_parts
    if DECK_CSS.is_file():
        css_parts.append(DECK_CSS)
    styles = "\n".join(f"<style>\n{read_css(p)}\n</style>" for p in css_parts)

    engine_js = (ENGINE / "deck-stage.js").read_text(encoding="utf-8")
    engine_js = engine_js.replace("</script>", "<\\/script>")

    icon_set = load_icons()
    parts = []
    for path, text in zip(slides, sources):
        # Lightweight author-contract check: each slide file should hold one
        # <section class="slide">. Warn (don't fail) so authoring stays forgiving.
        if 'class="slide' not in text and "class='slide" not in text:
            print(f"  ! {path.name}: no <section class=\"slide\"> found", file=sys.stderr)
        text = stamp_slide(text, path.name)
        text = inline_icons(text, icon_set, path.name)
        parts.append(inline_images(text, ROOT))
    slides_html = "\n".join(parts)

    def attr(value) -> str:
        return html.escape(str(value), quote=True)

    page = f"""<!doctype html>
<html lang="{attr(config['lang'])}">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{html.escape(str(config['title']), quote=False)}</title>
{styles}
</head>
<body>
<deck-stage width="{attr(config['width'])}" height="{attr(config['height'])}" transition="{attr(config['transition'])}" motion="{attr(motion)}" exit-hint="{attr(config['exit_hint'])}">
{slides_html}
</deck-stage>
<script>
{engine_js}
</script>
</body>
</html>
"""
    # newline="\n": keep LF endings regardless of OS, so the output is
    # byte-identical whether build.py runs on Linux, macOS or Windows
    # (Path.write_text defaults to translating "\n" to os.linesep, which is
    # "\r\n" on Windows).
    OUTPUT.write_text(page, encoding="utf-8", newline="\n")
    size_kb = OUTPUT.stat().st_size / 1024
    print(f"Built {OUTPUT.name} - {len(slides)} slides, {size_kb:.0f} KB")
    return OUTPUT


def watch() -> None:
    print("Watching for changes - Ctrl+C to stop.")
    mtimes: dict[Path, float] = {}
    try:
        while True:
            changed = False
            for f in source_files():
                m = f.stat().st_mtime
                if mtimes.get(f) != m:
                    mtimes[f] = m
                    changed = True
            if changed:
                try:
                    build()
                except SystemExit as e:
                    print(e, file=sys.stderr)
            time.sleep(0.4)
    except KeyboardInterrupt:
        print("\nStopped.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--watch", action="store_true", help="rebuild on every change")
    parser.add_argument("--open", action="store_true", help="open the result after building")
    parser.add_argument("--pull", action="store_true",
                        help="only copy in-browser edits back into slides/, don't build")
    args = parser.parse_args()

    if args.pull:
        pull_edits(say_if_none=True)
        return 0
    out = build()
    if args.open:
        webbrowser.open(out.as_uri())
    if args.watch:
        watch()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
