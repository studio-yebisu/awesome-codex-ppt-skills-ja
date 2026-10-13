#!/usr/bin/env python3
"""
inline-images.py — 将 HTML 文件中所有外部图片引用转为 base64 data URI，使文件零依赖。

用法：
    python3 scripts/inline-images.py <html_file>
"""

import re, base64, os, sys, mimetypes


def inline_images(html_file):
    html_dir = os.path.dirname(os.path.abspath(html_file))
    with open(html_file, 'r', encoding='utf-8') as f:
        html = f.read()

    refs = sorted(set(re.findall(r'src="([^"]+)"', html)))
    inlined, failed = 0, []

    for ref in refs:
        if ref.startswith('data:'):
            continue
        full_path = os.path.join(html_dir, ref)
        if not os.path.exists(full_path):
            failed.append(ref)
            continue
        mime = mimetypes.guess_type(full_path)[0] or 'image/png'
        with open(full_path, 'rb') as img:
            b64 = base64.b64encode(img.read()).decode()
        html = html.replace(f'src="{ref}"', f'src="data:{mime};base64,{b64}"')
        inlined += 1

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html)

    if failed:
        print(f"⚠️  以下图片未能内嵌（文件不存在）：{failed}")

    remaining = [s for s in re.findall(r'src="([^"]+)"', html) if not s.startswith('data:')]
    if remaining:
        print(f"⚠️  仍有残留外部引用：{remaining}")
    else:
        size_kb = os.path.getsize(html_file) // 1024
        print(f"✅ 内嵌 {inlined} 张图片，文件大小：{size_kb} KB，无外部依赖。")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("用法：python3 scripts/inline-images.py <html_file>")
        sys.exit(1)
    inline_images(sys.argv[1])
