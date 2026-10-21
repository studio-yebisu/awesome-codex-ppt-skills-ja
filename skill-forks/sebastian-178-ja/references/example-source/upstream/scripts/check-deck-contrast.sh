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
else
  dir="$(cd "$(dirname "$target")" && pwd)"
  file="$(basename "$target")"
  url="file://${dir}/${file}"
fi

separator="?"
if [[ "$url" == *"?"* ]]; then
  separator="&"
fi
audit_url="${url}${separator}print=1&audit=1"
dump_file="$(mktemp)"
trap 'rm -f "$dump_file"' EXIT

"$chrome" \
  --headless=new \
  --disable-gpu \
  --no-first-run \
  --no-default-browser-check \
  --virtual-time-budget=3000 \
  --dump-dom "$audit_url" > "$dump_file" 2>/dev/null

if grep -q "DECK_AUDIT_FAIL" "$dump_file"; then
  echo "Deck contrast audit failed:" >&2
  grep -o "DECK_AUDIT_FAIL .*" "$dump_file" | sed 's/<.*$//' >&2
  exit 1
fi

if ! grep -q "DECK_AUDIT_PASS" "$dump_file"; then
  echo "Deck contrast audit did not run. Ensure the deck loads the current assets/js/runtime.js from this skill." >&2
  exit 1
fi

echo "Deck contrast audit passed: $target"
