"""Inline local CSS/JS into one self-contained HTML file.

Usage: python inline-assets.py <input.html> <output.html>

- <link rel="stylesheet" href="x.css"> -> <style>...</style> (attribute order does not matter)
- <script src="x.js"></script>          -> <script>...</script>
- <img src="logo.png">                  -> <img src="data:image/png;base64,..."> (png, jpg, gif, webp, svg)
- Remote URLs (http/https, e.g. Google Fonts) and anything inside <!-- comments --> are left untouched.
- Only .css / .js / image files located under the input file's folder or this skill's folder are inlined
  (protects against embedding arbitrary files from the machine into a deck you share).
- Refuses to overwrite the input file. Creates the output folder if needed.
- Empty <i class="ico" data-icon="..."></i> get the Tabler SVG embedded (icons.py, cached download).
Exit code: 0 ok, 1 error, 2 local references left in the output.
"""
import base64
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from icons import inline_icons  # noqa: E402

SKILL_DIR = Path(__file__).resolve().parent.parent
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
LINK_RE = re.compile(r"<link\b[^>]*>", re.I)
SCRIPT_RE = re.compile(r"<script\b([^>]*)>\s*</script>", re.I)
IMG_RE = re.compile(r"<img\b[^>]*>", re.I)
IMG_TYPES = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".gif": "image/gif",
             ".webp": "image/webp", ".svg": "image/svg+xml"}


def attr(tag: str, name: str) -> str | None:
    m = re.search(rf'\b{name}\s*=\s*(["\'])(.*?)\1', tag, re.I | re.S)
    return m.group(2) if m else None


def is_remote(href: str) -> bool:
    return href.startswith(("http://", "https://", "//", "data:"))


def asset_path(base: Path, href: str, exts: tuple[str, ...]) -> Path:
    path = Path(href)
    path = (path if path.is_absolute() else base / href).resolve()
    if path.suffix.lower() not in exts:
        raise ValueError(f"Refusing to inline non-{'/'.join(exts)} file: {path}")
    if not (path.is_relative_to(base.resolve()) or path.is_relative_to(SKILL_DIR)):
        raise ValueError(f"Refusing to inline file outside the deck folder or skill folder: {path}")
    if not path.is_file():
        raise FileNotFoundError(f"Asset not found: {path}")
    return path


def read_asset(base: Path, href: str, ext: str) -> str:
    return asset_path(base, href, (ext,)).read_text(encoding="utf-8")


def inline_part(html: str, base: Path) -> str:
    def css(m):
        tag = m.group(0)
        href = attr(tag, "href")
        if (attr(tag, "rel") or "").lower() != "stylesheet" or not href or is_remote(href):
            return tag
        code = read_asset(base, href, ".css").replace("</style", "<\\/style")
        return f"<style>\n{code}\n</style>"

    def js(m):
        src = attr(m.group(0), "src")
        if not src or is_remote(src):
            return m.group(0)
        # "</script" inside JS would close the tag early
        code = read_asset(base, src, ".js").replace("</script", "<\\/script")
        return f"<script>\n{code}\n</script>"

    def img(m):
        tag = m.group(0)
        src = attr(tag, "src")
        if not src or is_remote(src):
            return tag
        path = asset_path(base, src, tuple(IMG_TYPES))
        if path.stat().st_size > 1_500_000:
            print(f"Warning: {path.name} is {path.stat().st_size / 1e6:.1f} MB; resize to 1920 px wide, JPG quality about 80")
        data = base64.b64encode(path.read_bytes()).decode("ascii")
        return tag.replace(src, f"data:{IMG_TYPES[path.suffix.lower()]};base64,{data}", 1)

    # images first: inlined CSS/JS may mention <img> in their comments
    return SCRIPT_RE.sub(js, LINK_RE.sub(css, IMG_RE.sub(img, html)))


def inline(html: str, base: Path) -> str:
    """Process only the text between HTML comments."""
    out, pos = [], 0
    for m in COMMENT_RE.finditer(html):
        out += [inline_part(html[pos:m.start()], base), m.group(0)]
        pos = m.end()
    out.append(inline_part(html[pos:], base))
    return "".join(out)


def local_refs_left(html: str) -> list[str]:
    html = COMMENT_RE.sub("", html)
    refs = [attr(t, "href") for t in LINK_RE.findall(html) if (attr(t, "rel") or "").lower() == "stylesheet"]
    refs += [attr(m.group(0), "src") for m in SCRIPT_RE.finditer(html)]
    markup = re.sub(r"<(style|script)\b[^>]*>.*?</\1>", "", html, flags=re.I | re.S)
    refs += [attr(t, "src") for t in IMG_RE.findall(markup)]
    return [r for r in refs if r and not is_remote(r)]


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 1
    src, dst = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    if src == dst:
        print("Error: output must differ from input (back up and write to a new path).")
        return 1
    try:
        out = inline(src.read_text(encoding="utf-8"), src.parent)
        out, missing_icons = inline_icons(out)
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(out, encoding="utf-8")
    except (OSError, ValueError, UnicodeDecodeError) as err:  # OSError covers a failed icon download
        print(f"Error: {err}")
        return 1
    left = local_refs_left(out)
    print(f"Wrote {dst} ({len(out):,} chars). Local refs left: {len(left)} {left if left else ''}")
    if missing_icons:
        print(f"Icons not found in Tabler (check the name with icons.py search): {sorted(set(missing_icons))}")
    return 0 if not (left or missing_icons) else 2


if __name__ == "__main__":
    sys.exit(main())
