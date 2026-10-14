# -*- coding: utf-8 -*-
"""
ppt_pipeline — Unified PPT Production Pipeline

This package bundles python-pptx (MIT) in ppt_scene_graph/vendor/pptx/
No external dependency on python-pptx required.
"""
import sys
import os

# Add vendor directory to path so `from pptx import ...` works with bundled version
_vendor_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vendor')
if _vendor_path not in sys.path:
    sys.path.insert(0, _vendor_path)

from .design import DesignSystem, load_theme, list_themes, FONT_SIZES
from .pipeline import beautify, create_from_outline, evaluate, cli_main

__all__ = [
    'DesignSystem', 'load_theme', 'list_themes', 'FONT_SIZES',
    'beautify', 'create_from_outline', 'evaluate', 'cli_main',
]
