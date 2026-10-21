#!/usr/bin/env bash
set -euo pipefail

# Native Windows tools (poppler, MiKTeX) take Windows-style paths; Git Bash
# may run without MSYS path conversion, so convert explicitly when possible.
to_windows_path() { command -v cygpath >/dev/null 2>&1 && cygpath -m "$1" || printf '%s' "$1"; }

if [[ $# -lt 1 || $# -gt 4 ]]; then
  echo "Usage: render_and_check.sh DECK.tex [RENDER_DIR] [FIRST_PAGE] [LAST_PAGE]" >&2
  exit 64
fi

source_tex="$1"
render_dir="${2:-rendered}"
first_page="${3:-1}"
last_page="${4:-}"

if [[ ! -f "$source_tex" ]]; then
  echo "Deck source not found: $source_tex" >&2
  exit 66
fi

for required_command in xelatex pdfinfo pdftoppm; do
  if ! command -v "$required_command" >/dev/null 2>&1; then
    echo "Required command not found: $required_command" >&2
    exit 69
  fi
done

source_dir="$(cd "$(dirname "$source_tex")" && pwd)"
source_name="$(basename "$source_tex")"
deck_stem="${source_name%.tex}"
pdf_path="$source_dir/$deck_stem.pdf"
log_path="$source_dir/$deck_stem.log"
compile_output="$(mktemp)"
trap 'rm -f "$compile_output"' EXIT

if ! (
  cd "$source_dir"
  xelatex -interaction=nonstopmode -halt-on-error "$source_name"
  xelatex -interaction=nonstopmode -halt-on-error "$source_name"
) >"$compile_output" 2>&1; then
  cat "$compile_output" >&2
  exit 65
fi

if [[ ! -f "$pdf_path" || ! -f "$log_path" ]]; then
  echo "Expected PDF or log was not produced." >&2
  exit 70
fi

if grep -E -n 'Overfull \\[hv]box|LaTeX Error|Package .* Error' "$log_path"; then
  echo "Layout-related LaTeX diagnostics remain; fix them before visual review." >&2
  exit 65
fi

page_count="$(pdfinfo "$(to_windows_path "$pdf_path")" | awk '/^Pages:/ {print $2}')"
if [[ -z "$last_page" ]]; then
  last_page="$page_count"
fi

if ! [[ "$first_page" =~ ^[0-9]+$ && "$last_page" =~ ^[0-9]+$ ]]; then
  echo "Page bounds must be positive integers." >&2
  exit 64
fi
if (( first_page < 1 || last_page < first_page || last_page > page_count )); then
  echo "Invalid page range $first_page-$last_page for a $page_count-page PDF." >&2
  exit 64
fi

mkdir -p "$render_dir"
render_dir="$(cd "$render_dir" && pwd)"
pdftoppm -png -r 200 -f "$first_page" -l "$last_page" \
  "$(to_windows_path "$pdf_path")" "$(to_windows_path "$render_dir/$deck_stem-page")"

echo "PDF: $pdf_path"
echo "Pages: $page_count"
echo "Rendered: $first_page-$last_page at 200 dpi"
echo "Preview directory: $render_dir"
echo "Next step: visually inspect every rendered page at original detail."
