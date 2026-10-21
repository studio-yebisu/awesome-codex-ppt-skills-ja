#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat >&2 <<'EOF'
Usage:
  scripts/fetch-fonts.sh

Downloads the default Google-hosted Latin fonts into assets/fonts/google and
rewrites assets/css/fonts.css to use local @font-face URLs.

The default set intentionally excludes full CJK webfont binaries because they
add tens of megabytes to the installable skill. CJK text uses system CJK fonts
from the font stack.
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_dir="$(cd "$script_dir/.." && pwd)"
fonts_dir="${repo_dir}/assets/fonts/google"
css_file="${repo_dir}/assets/css/fonts.css"

mkdir -p "$fonts_dir"

python3 - "$fonts_dir" "$css_file" <<'PY'
import re
import sys
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

fonts_dir = Path(sys.argv[1])
css_file = Path(sys.argv[2])

families_url = (
    "https://fonts.googleapis.com/css2"
    "?family=Inter:wght@400;500;600;700;800"
    "&family=Libre+Baskerville:wght@400;700"
    "&display=swap"
)
headers = {
    "User-Agent": "Mozilla/5.0 AppleWebKit/537.36 Chrome Safari",
    "Accept": "text/css,*/*;q=0.1",
}

request = urllib.request.Request(families_url, headers=headers)
css = urllib.request.urlopen(request, timeout=30).read().decode("utf-8")
url_re = re.compile(r"url\((https://fonts\.gstatic\.com/[^)]+)\)")

def local_name(url):
    path = Path(urlparse(url).path)
    family = "font"
    parts = path.parts
    if len(parts) > 2:
        family = parts[2].replace("-", "")
    return f"{family}-{path.name}"

def replace_url(match):
    url = match.group(1)
    name = local_name(url)
    target = fonts_dir / name
    if not target.exists():
        req = urllib.request.Request(url, headers=headers)
        target.write_bytes(urllib.request.urlopen(req, timeout=30).read())
    return f"url('../fonts/google/{name}')"

local_css = url_re.sub(replace_url, css)
local_css += """

:root {
  --font-cjk-sans: "Noto Sans SC", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
  --font-cjk-serif: "Noto Serif SC", "Songti SC", "STSong", serif;
  --font-sans: "Inter", var(--font-cjk-sans), Arial, Helvetica, sans-serif;
  --font-serif: "Libre Baskerville", var(--font-cjk-serif), Georgia, serif;
}
"""

css_file.write_text(local_css, encoding="utf-8")
print(f"Wrote {css_file}")
for path in sorted(fonts_dir.iterdir()):
    print(f"Font: {path.relative_to(fonts_dir.parent.parent)}")
PY
