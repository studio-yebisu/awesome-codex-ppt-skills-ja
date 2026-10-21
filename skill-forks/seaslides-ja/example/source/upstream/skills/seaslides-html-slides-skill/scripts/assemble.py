#!/usr/bin/env python3
"""Assemble HTML presentation: merge index-template + content into index.html.

Template-Content Separation (TCS) Structure:
  - index-template.html : HTML shell with CDN links, <link rel="stylesheet"
                          href="template.css">, navigation JS, and a
                          {{CONTENT}} placeholder. No slide content.
  - template.css        : All presentation CSS (variables, components, layout).
                          Referenced by index-template.html during development.
  - content.html        : Only <section class="slide"> blocks. Pure structure,
                          no styling. This is what the LLM generates.
  - index.html          : Assembled output -- standalone HTML with CSS inlined.
                          Can be opened directly in any browser.

The assembly step:
  1. Reads index-template.html
  2. If template has <link rel="stylesheet" href="template.css">, reads that
     file relative to the template's directory and inlines it as <style>
  3. Replaces {{CONTENT}} with content.html contents
  4. Writes final index.html

Backward compatibility:
  - Also accepts the old single-file template.html format (with <style> already
    inline and {{CONTENT}} placeholder). Works as before.

Usage:
    python3 assemble.py <index-template.html> <content.html> [-o output.html]

Examples:
    # New structure (CSS inlined automatically):
    python3 scripts/assemble.py templates/corporate/index-template.html project/content.html -o project/index.html

    # Old single-file template (backward compatible):
    python3 scripts/assemble.py templates/corporate.html project/content.html -o project/index.html
"""
import sys
import re
import argparse
from pathlib import Path


RUNTIME_PATH = Path(__file__).resolve().parent / "runtime" / "deck_runtime.js"


class AssemblyError(RuntimeError):
    """Controlled assembly failure."""


def inline_css(template_text: str, template_dir: Path) -> str:
    """Replace <link rel="stylesheet" href="template.css"> with inlined <style> block.

    Only inlines local CSS files (not CDN links). Handles the specific pattern
    where href points to a relative CSS file that exists on disk.
    """
    css_placeholder = "{{CSS}}"
    if css_placeholder in template_text:
        css_path = template_dir / "template.css"
        if css_path.exists():
            css_content = css_path.read_text(encoding="utf-8")
            template_text = template_text.replace(css_placeholder, css_content)
        else:
            raise AssemblyError(f"CSS file not found for {{CSS}} placeholder: {css_path}")

    def replace_local_link(match: re.Match) -> str:
        href = match.group(1)
        # Skip CDN/external links
        if href.startswith(('http://', 'https://', '//')):
            return match.group(0)
        css_path = template_dir / href
        if css_path.exists():
            css_content = css_path.read_text(encoding='utf-8')
            return f'<style>\n{css_content}</style>'
        else:
            raise AssemblyError(f"Local stylesheet not found: {css_path}")

    # Match <link rel="stylesheet" href="..."> where href is a local file
    pattern = r'<link\s+rel="stylesheet"\s+href="([^"]+)">'
    result = re.sub(pattern, replace_local_link, template_text)

    # Also handle href before rel ordering
    pattern2 = r'<link\s+href="([^"]+)"\s+rel="stylesheet">'
    result = re.sub(pattern2, replace_local_link, result)

    return result


def inline_runtime(template_text: str) -> str:
    """Inline the common runtime contract into the standalone deck."""
    if not RUNTIME_PATH.exists():
        raise AssemblyError(f"SeaSlides runtime not found: {RUNTIME_PATH}")
    runtime = RUNTIME_PATH.read_text(encoding="utf-8")
    block = f"<script data-seaslides-runtime=\"{RUNTIME_PATH.stem}\">\n{runtime}\n</script>"
    placeholder = "{{SEASLIDES_RUNTIME}}"
    if placeholder in template_text:
        return template_text.replace(placeholder, block)
    match = re.search(r"</body\s*>", template_text, re.IGNORECASE)
    if not match:
        raise AssemblyError("Template does not contain </body> for runtime injection.")
    return template_text[:match.start()] + block + "\n" + template_text[match.start():]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Merge index-template.html + content.html into final index.html"
    )
    parser.add_argument(
        "template",
        help="Path to index-template.html (or legacy template.html)"
    )
    parser.add_argument("content", help="Path to content.html")
    parser.add_argument(
        "-o", "--output",
        default="index.html",
        help="Output file path (default: index.html)"
    )
    args = parser.parse_args()

    template_path = Path(args.template)
    content_path = Path(args.content)

    if not template_path.exists():
        print(f"ERROR: Template not found: {template_path}", file=sys.stderr)
        sys.exit(1)
    if not content_path.exists():
        print(f"ERROR: Content not found: {content_path}", file=sys.stderr)
        sys.exit(1)

    template_text = template_path.read_text(encoding="utf-8")
    content_text = content_path.read_text(encoding="utf-8")

    if "{{CONTENT}}" not in template_text:
        print("ERROR: Template does not contain {{CONTENT}} placeholder.", file=sys.stderr)
        sys.exit(1)

    try:
        # Inline local CSS and the dependency-free runtime contract.
        template_text = inline_css(template_text, template_path.parent)
        template_text = inline_runtime(template_text)
        result = template_text.replace("{{CONTENT}}", content_text)
    except (AssemblyError, OSError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)

    # Write output
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(result, encoding="utf-8")
    print(f"Assembled: {args.output} ({len(result):,} bytes)")


if __name__ == "__main__":
    main()
