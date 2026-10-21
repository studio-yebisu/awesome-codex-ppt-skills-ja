#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: scripts/new-deck.sh <deck-directory>" >&2
  exit 1
fi

target="$1"
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_dir="$(cd "$script_dir/.." && pwd)"

mkdir -p "$target"
cp "$repo_dir/templates/starter-deck.html" "$target/index.html"

if [[ ! -e "$target/assets" ]]; then
  ln -s "$repo_dir/assets" "$target/assets" 2>/dev/null || cp -R "$repo_dir/assets" "$target/assets"
fi

perl -0pi -e 's#\.\./assets#assets#g' "$target/index.html"

echo "Created $target/index.html"
echo "Open it in a browser: $target/index.html"
