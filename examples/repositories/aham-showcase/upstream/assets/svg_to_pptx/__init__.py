"""svg_to_pptx — SVG to PPTX conversion package.

Public API:
    - convert_svg_to_slide_shapes(): SVG -> DrawingML slide XML
    - create_pptx_with_native_svg(): Build PPTX from SVG files
"""

from .drawingml_converter import convert_svg_to_slide_shapes
from .pptx_builder import create_pptx_with_native_svg

__all__ = [
    'convert_svg_to_slide_shapes',
    'create_pptx_with_native_svg',
]
