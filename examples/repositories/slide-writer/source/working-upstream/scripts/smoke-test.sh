#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TARGET="${1:-}"

if [[ -z "$TARGET" ]]; then
    echo "Usage: ./scripts/smoke-test.sh <html-file>"
    exit 1
fi

if [[ "$TARGET" != /* ]]; then
    TARGET="${ROOT_DIR}/${TARGET}"
fi

if [[ ! -f "$TARGET" ]]; then
    echo "ERROR: file not found: $TARGET"
    exit 1
fi

cd "$ROOT_DIR"

echo "Checking ${TARGET#$ROOT_DIR/}"

required_ids=(
    'id="progressBar"'
    'id="navDots"'
    'id="fullscreenBtn"'
    'id="footnote"'
)

required_classes=(
    'class="slide slide-cover"'
    'class="slide slide-section"'
    'class="slide slide-qa"'
)

for pattern in "${required_ids[@]}"; do
    if ! grep -q "$pattern" "$TARGET"; then
        echo "ERROR: missing required element: $pattern"
        exit 1
    fi
done

if ! grep -q 'agenda-item' "$TARGET"; then
    echo "ERROR: missing agenda content for directory slide"
    exit 1
fi

for pattern in "${required_classes[@]}"; do
    if ! grep -q "$pattern" "$TARGET"; then
        echo "ERROR: missing required slide type: $pattern"
        exit 1
    fi
done

if grep -Eq 'src="\./logo-[^"]+\.(png|svg)"' "$TARGET"; then
    echo "ERROR: found legacy root-level logo path; use ./themes/logos/... instead"
    exit 1
fi

for asset in $(grep -Eo 'src="\./[^"]+"' "$TARGET" | sed 's/^src="//;s/"$//' | sort -u); do
    if [[ "$asset" == ./themes/logos/* || "$asset" == ./examples/* ]]; then
        if [[ ! -f "${ROOT_DIR}/${asset#./}" ]]; then
            echo "ERROR: missing local asset: $asset"
            exit 1
        fi
    fi
done

# 检查幻灯片总数（至少 4 页：封面 + 目录 + 章节 + 结尾）
slide_count=$(grep -c 'class="slide ' "$TARGET" || true)
if [[ "$slide_count" -lt 4 ]]; then
    echo "ERROR: too few slides ($slide_count), expected at least 4"
    exit 1
fi
echo "  slide count: $slide_count"

# 检查主题 CSS 变量是否存在覆盖（非默认蚂蚁蓝时应有 --primary 覆盖）
if grep -q 'slide-cover' "$TARGET"; then
    if ! grep -q '\-\-primary:' "$TARGET"; then
        echo "WARNING: no --primary CSS variable found; theme override may be missing"
    fi
fi

# 检查是否引用了 Google Fonts（字体加载失败时有 fallback）
if grep -q 'fonts.googleapis.com' "$TARGET"; then
    if ! grep -q "PingFang\|Hiragino\|Microsoft YaHei\|sans-serif" "$TARGET"; then
        echo "WARNING: Google Fonts referenced but no local font fallback found"
    fi
fi

# 检查文件名是否含中文字符
filename=$(basename "$TARGET")
if echo "$filename" | grep -qP '[\x{4e00}-\x{9fff}]' 2>/dev/null || \
   echo "$filename" | python3 -c "import sys; s=sys.stdin.read(); exit(0 if any(ord(c)>127 for c in s) else 1)" 2>/dev/null; then
    echo "WARNING: filename contains non-ASCII characters: $filename"
fi

echo "Smoke test passed"
