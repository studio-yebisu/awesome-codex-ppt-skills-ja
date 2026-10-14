#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
scratch="$(mktemp -d "${TMPDIR:-/tmp}/quarto-talks.XXXXXX")"
trap 'rm -rf "$scratch"' EXIT

cd "$scratch"
quarto add "$repo_root" --no-prompt
test -f "$scratch/_extensions/quarto-talks/_extension.yml"
cp "$repo_root/template.qmd" "$scratch/template.qmd"
quarto render "$scratch/template.qmd" --quiet
test -s "$scratch/template.html"

cp "$repo_root/tests/bluesky.qmd" "$scratch/bluesky.qmd"
quarto render "$scratch/bluesky.qmd" --quiet
test -s "$scratch/bluesky.html"
grep -q 'data-bluesky-url="https://bsky.app/profile/bsky.app/post/3lndjyecwcs2a"' "$scratch/bluesky.html"
grep -q 'data-bluesky-max-width="520"' "$scratch/bluesky.html"
grep -q 'Open post on Bluesky' "$scratch/bluesky.html"
grep -q 'data-bluesky-state="invalid"' "$scratch/bluesky.html"
grep -q 'embed.bsky.app/oembed' "$scratch/bluesky.html"

cp "$repo_root/tests/bluesky-disabled.qmd" "$scratch/bluesky-disabled.qmd"
quarto render "$scratch/bluesky-disabled.qmd" --quiet
test -s "$scratch/bluesky-disabled.html"
grep -q 'data-bluesky-enabled="false"' "$scratch/bluesky-disabled.html"
grep -q 'Open post on Bluesky' "$scratch/bluesky-disabled.html"
! grep -q 'embed.bsky.app/oembed' "$scratch/bluesky-disabled.html"

cd "$repo_root"
decks=(
  "examples/research/research.qmd"
  "examples/conceptual/conceptual.qmd"
  "examples/math-code/math-code.qmd"
)

for deck in "${decks[@]}"; do
  quarto render "$deck" --quiet
  test -s "${deck%.qmd}.html"
  echo "rendered $deck"
done

grep -q 'fig-visits' "examples/research/research.html"
grep -q '10.1198/jcgs.2009.07098' "examples/research/research.html"
grep -q 'running_mean(values)' "examples/math-code/math-code.html"
grep -q 'bar{x}' "examples/math-code/math-code.html"

echo "all quarto-talks render checks passed"
