"""Tabler icons for SlideFly: build the index, search, suggest per slide, fetch SVGs (cached).

Usage:
  python icons.py search <từ khóa ...>        tìm icon theo từ tiếng Việt hoặc tag tiếng Anh
  python icons.py suggest <deck.html>          gợi ý tối đa 3 icon cho mỗi slide từ chữ trên slide
  python icons.py build-index                  tải lại danh mục Tabler (bản ghim TABLER_VERSION)

Markup trong deck:  <i class="ico" data-icon="database"></i>   (thêm data-style="filled" cho bản tô đặc)
inline-assets.py gọi inline_icons() để nhúng SVG thật vào file cuối, nên deck chạy được khi không có mạng.
Icons: Tabler Icons (MIT, Copyright (c) 2020-2026 Paweł Kuna), https://tabler.io/icons
"""
import json
import re
import sys
import urllib.request
from html import unescape
from pathlib import Path

TABLER_VERSION = "3.48.0"
CDN = f"https://cdn.jsdelivr.net/npm/@tabler/icons@{TABLER_VERSION}"
ICON_DIR = Path(__file__).resolve().parent.parent / "assets" / "icons"
INDEX = ICON_DIR / "tabler-index.json"
VI_KEYWORDS = ICON_DIR / "vi-keywords.json"
CACHE = Path.home() / ".cache" / "slidefly" / f"tabler-{TABLER_VERSION}"
ICO_RE = re.compile(r'<i\b(?=[^>]*\bclass="[^"]*\bico\b)([^>]*)>\s*</i>', re.I)


def _get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "slidefly-icons"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def build_index() -> None:
    """Compact index: name -> [category, 'tag tag ...', has_filled]."""
    raw = json.loads(_get(f"{CDN}/icons.json"))
    icons = {}
    for name, it in raw.items():
        tags = " ".join(str(t).lower() for t in (it.get("tags") or [])[:10])
        icons[name] = [it.get("category") or "", tags, 1 if "filled" in (it.get("styles") or {}) else 0]
    ICON_DIR.mkdir(parents=True, exist_ok=True)
    INDEX.write_text(json.dumps({"version": TABLER_VERSION, "icons": icons}, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Wrote {INDEX} ({len(icons)} icons, Tabler {TABLER_VERSION})")


def load_index() -> dict:
    return json.loads(INDEX.read_text(encoding="utf-8"))["icons"]


def load_vi() -> dict:
    data = json.loads(VI_KEYWORDS.read_text(encoding="utf-8"))
    return {k.lower(): v for k, v in data.items() if not k.startswith("_")}


def search(words: list[str], limit: int = 12) -> list[tuple[str, int]]:
    """Score icons: Vietnamese keyword hit = 10, exact name = 8, tag hit = 3, name contains = 2."""
    idx, vi = load_index(), load_vi()
    q = " ".join(words).lower()
    score: dict[str, int] = {}
    for phrase, names in vi.items():
        if re.search(rf"(?<!\w){re.escape(phrase)}(?!\w)", q):  # whole words: "ai" must not hit "tài"
            for rank, n in enumerate(names):
                score[n] = score.get(n, 0) + 10 - rank
    for w in re.findall(r"\b[a-z][a-z0-9-]{3,}\b", q):
        for name, (_, tags, _) in idx.items():
            s = (8 if name == w else 0) + (3 if w in tags.split() else 0) + (2 if w in name else 0)
            if s:
                score[name] = score.get(name, 0) + s
    return sorted(((n, s) for n, s in score.items() if n in idx), key=lambda x: -x[1])[:limit]


def slide_texts(html: str) -> list[str]:
    out = []
    for sec in re.findall(r"<section\b[^>]*>(.*?)</section>", html, re.S | re.I):
        sec = re.sub(r"<(script|style|pre)\b.*?</\1>", " ", sec, flags=re.S | re.I)
        out.append(unescape(re.sub(r"<[^>]+>", " ", sec)))
    return out


def suggest(path: Path) -> None:
    for i, text in enumerate(slide_texts(path.read_text(encoding="utf-8")), 1):
        hits = search([text], 3)
        line = ", ".join(f"{n} ({s})" for n, s in hits) or "không có gợi ý: slide này có thể không cần icon"
        print(f"{i:>3}. {line}")


def fetch_svg(name: str, style: str = "outline") -> str:
    """SVG markup without fixed width/height (CSS sizes it), cached on disk."""
    style = "filled" if style == "filled" else "outline"
    if not re.fullmatch(r"[a-z0-9-]+", name):
        raise ValueError(f"Tên icon không hợp lệ: {name!r}")
    f = CACHE / style / f"{name}.svg"
    if not f.is_file():
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_bytes(_get(f"{CDN}/icons/{style}/{name}.svg"))
    svg = f.read_text(encoding="utf-8")
    svg = re.sub(r'\s(width|height)="24"', "", svg)
    svg = re.sub(r'\sclass="[^"]*"', ' aria-hidden="true" focusable="false"', svg, count=1)
    return re.sub(r">\s+<", "><", svg).strip()


def inline_icons(html: str) -> tuple[str, list[str]]:
    """Replace empty <i class="ico" data-icon=...></i> with the SVG inside. Returns (html, missing names)."""
    idx, missing = load_index(), []

    def rep(m):
        attrs = m.group(1)
        name = (re.search(r'data-icon="([^"]+)"', attrs) or [None, ""])[1]
        style = (re.search(r'data-style="([^"]+)"', attrs) or [None, "outline"])[1]
        if name not in idx or (style == "filled" and not idx[name][2]):
            missing.append(name)
            return m.group(0)
        return f"<i{attrs}>{fetch_svg(name, style)}</i>"

    # only markup: examples inside comments, <style> and <script> are not icons
    parts = re.split(r"(<!--.*?-->|<style\b.*?</style>|<script\b.*?</script>)", html, flags=re.I | re.S)
    return "".join(p if i % 2 else ICO_RE.sub(rep, p) for i, p in enumerate(parts)), missing


def main() -> int:
    cmd, args = (sys.argv[1], sys.argv[2:]) if len(sys.argv) > 1 else ("", [])
    if cmd == "build-index":
        build_index()
    elif cmd == "search" and args:
        for n, s in search(args):
            print(f"{s:>3}  {n}")
    elif cmd == "suggest" and args:
        suggest(Path(args[0]))
    else:
        print(__doc__)
        return 1
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
