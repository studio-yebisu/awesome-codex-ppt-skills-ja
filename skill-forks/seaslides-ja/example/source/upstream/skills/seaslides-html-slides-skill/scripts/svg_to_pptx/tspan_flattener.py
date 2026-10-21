"""In-memory flattening of positional ``<tspan>`` elements.

DrawingML's text-run model has no way to express "jump to a new x/y inside
the same paragraph". Every ``<tspan>`` carrying ``x``, ``y`` or non-zero
``dy`` is therefore a layout instruction this converter cannot honour
inline — without flattening, a 4-line dy-stacked block collapses onto a
single baseline and an x-anchored tspan jumps to the wrong column.

The on-disk ``finalize_svg`` pipeline solves this by promoting each
positional tspan to an independent ``<text>`` element. This module
performs the same transformation in memory so ``svg_to_pptx`` can consume
``svg_output/`` directly without that disk step.

Public API:
    flatten_positional_tspans(tree) -> bool
        Walk the SVG element tree, replace every positional ``<tspan>``
        with an independent ``<text>``, and return whether anything
        changed.

Heavy lifting is delegated to ``svg_finalize.flatten_tspan`` so the two
pipelines stay behaviourally aligned.
"""

from __future__ import annotations

import sys
from pathlib import Path
from xml.etree import ElementTree as ET


def flatten_positional_tspans(
    tree: ET.ElementTree,
    merge_paragraphs: bool = False,
) -> bool:
    """Flatten positional ``<tspan>`` elements into independent ``<text>``.

    Delegates to ``svg_finalize.flatten_tspan.flatten_text_with_tspans`` when
    available (ppt-master environment). Falls back to a simple inline
    implementation for standalone use with browser-exported SVG output.

    When ``merge_paragraphs`` is True, mergeable paragraph blocks are preserved
    as a single <text> for downstream multi-<a:p> conversion.

    Returns True if any tspan was rewritten.
    """
    scripts_dir = Path(__file__).resolve().parent.parent
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    try:
        from svg_finalize.flatten_tspan import flatten_text_with_tspans  # type: ignore
        import inspect
        sig = inspect.signature(flatten_text_with_tspans)
        if 'merge_paragraphs' in sig.parameters:
            return flatten_text_with_tspans(tree, merge_paragraphs=merge_paragraphs)
        else:
            return flatten_text_with_tspans(tree)
    except ImportError:
        pass

    # Fallback: simple inline flattening for SVGs with split text spans
    # Promote each positional <tspan> (with x/y/non-zero dy) to independent <text>
    SVG_NS = 'http://www.w3.org/2000/svg'
    root = tree.getroot()
    changed = False

    for text_elem in list(root.iter(f'{{{SVG_NS}}}text')) + list(root.iter('text')):
        tspans = list(text_elem)
        positional = []
        for ts in tspans:
            tag = ts.tag.split('}')[-1] if '}' in str(ts.tag) else str(ts.tag)
            if tag != 'tspan':
                continue
            if ts.get('x') or ts.get('y') or (ts.get('dy') and ts.get('dy') != '0'):
                positional.append(ts)

        if not positional:
            continue

        parent = None
        for p in root.iter():
            if text_elem in list(p):
                parent = p
                break
        if parent is None:
            continue

        idx = list(parent).index(text_elem)
        base_attribs = dict(text_elem.attrib)

        for ts in positional:
            new_text = ET.Element(text_elem.tag)
            new_text.attrib.update(base_attribs)
            # Override with tspan's positioning
            for attr in ('x', 'y', 'dx', 'dy'):
                if ts.get(attr):
                    new_text.set(attr, ts.get(attr))
            # Copy style-related attributes
            for attr in ('font-size', 'font-family', 'font-weight', 'font-style',
                         'fill', 'opacity', 'text-anchor', 'letter-spacing'):
                if ts.get(attr):
                    new_text.set(attr, ts.get(attr))
            new_text.text = ts.text or ''
            new_text.tail = ts.tail
            idx += 1
            parent.insert(idx, new_text)
            text_elem.remove(ts)
            changed = True

        # Remove original <text> if all children were promoted
        if not list(text_elem) and not (text_elem.text and text_elem.text.strip()):
            parent.remove(text_elem)

    return changed
