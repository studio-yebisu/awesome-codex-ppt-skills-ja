#!/usr/bin/env bash
set -euo pipefail

# Native Windows tools (poppler, MiKTeX) take Windows-style paths; Git Bash
# may run without MSYS path conversion, so convert explicitly when possible.
to_windows_path() { command -v cygpath >/dev/null 2>&1 && cygpath -m "$1" || printf '%s' "$1"; }

if [[ $# -ne 8 ]]; then
  echo "Usage: $0 PDF PAGE OUTPUT_PREFIX DPI X Y WIDTH HEIGHT" >&2
  exit 2
fi

pdf_path=$1
page_number=$2
output_prefix=$3
dpi=$4
crop_x=$5
crop_y=$6
crop_width=$7
crop_height=$8

if [[ ! -f "$pdf_path" ]]; then
  echo "PDF not found: $pdf_path" >&2
  exit 2
fi

command -v pdftoppm >/dev/null 2>&1 || {
  echo "pdftoppm is required" >&2
  exit 2
}

mkdir -p "$(dirname "$output_prefix")"
pdftoppm \
  -f "$page_number" -l "$page_number" -singlefile -png \
  -r "$dpi" -x "$crop_x" -y "$crop_y" \
  -W "$crop_width" -H "$crop_height" \
  "$(to_windows_path "$pdf_path")" "$(to_windows_path "$output_prefix")"

echo "Crop: ${output_prefix}.png"
