#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <deck.html-or-url>" >&2
  exit 2
fi

target="$1"

if [[ -n "${CHROME_BIN:-}" ]]; then
  chrome="$CHROME_BIN"
elif [[ -x "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" ]]; then
  chrome="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
elif command -v google-chrome >/dev/null 2>&1; then
  chrome="$(command -v google-chrome)"
elif command -v chromium >/dev/null 2>&1; then
  chrome="$(command -v chromium)"
elif command -v chromium-browser >/dev/null 2>&1; then
  chrome="$(command -v chromium-browser)"
else
  echo "Chrome/Chromium not found. Set CHROME_BIN=/path/to/chrome and retry." >&2
  exit 2
fi

if [[ "$target" =~ ^https?:// || "$target" =~ ^file:// ]]; then
  url="$target"
  slide_count="${SLIDE_COUNT:-1}"
else
  input_path="$(cd "$(dirname "$target")" && pwd)/$(basename "$target")"
  if [[ ! -f "$input_path" ]]; then
    echo "Deck not found: $target" >&2
    exit 2
  fi
  url="file://${input_path}"
  slide_count="$(python3 - "$input_path" <<'PY'
from html.parser import HTMLParser
from pathlib import Path
import sys

class SlideCounter(HTMLParser):
    def __init__(self):
        super().__init__()
        self.count = 0

    def handle_starttag(self, tag, attrs):
        if tag.lower() != "section":
            return
        values = dict(attrs)
        classes = values.get("class", "")
        if "slide" in classes.split():
            self.count += 1

parser = SlideCounter()
parser.feed(Path(sys.argv[1]).read_text(encoding="utf-8"))
print(parser.count or 1)
PY
)"
fi

append_query() {
  local raw_url="$1"
  local query="$2"
  local base="$raw_url"
  local hash=""
  if [[ "$base" == *"#"* ]]; then
    hash="#${base#*#}"
    base="${base%%#*}"
  fi
  if [[ "$base" == *"?"* ]]; then
    printf '%s&%s%s' "$base" "$query" "$hash"
  else
    printf '%s?%s%s' "$base" "$query" "$hash"
  fi
}

dump_file="$(mktemp)"
trap 'rm -f "$dump_file"' EXIT

failed=0
for ((i = 1; i <= slide_count; i += 1)); do
  audit_url="$(append_query "$url" "slide=${i}&export=1&fitAudit=1")"
  "$chrome" \
    --headless=new \
    --disable-gpu \
    --no-first-run \
    --no-default-browser-check \
    --hide-scrollbars \
    --force-device-scale-factor=1 \
    --window-size=1600,900 \
    --virtual-time-budget=3000 \
    --dump-dom "$audit_url" > "$dump_file" 2>/dev/null

  if grep -q "DECK_FIT_AUDIT_FAIL" "$dump_file"; then
    echo "Deck fit audit failed on slide ${i}:" >&2
    grep -o "DECK_FIT_AUDIT_FAIL .*" "$dump_file" | sed 's/<.*$//' >&2
    failed=1
  elif ! grep -q "DECK_FIT_AUDIT_PASS" "$dump_file"; then
    echo "Deck fit audit did not run on slide ${i}. Ensure the deck loads the current assets/js/runtime.js from this skill." >&2
    failed=1
  fi
done

if [[ "$failed" -ne 0 ]]; then
  exit 1
fi

echo "Deck fit audit passed: $target"
