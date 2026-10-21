"""Case-local font registration, then the unchanged original native exporter.

The pinned exporter knows common Japanese EA faces but not BIZ UDPGothic.
Register exactly the bundled family in memory so it does not fall back to
Yu Gothic for Japanese. No upstream file or acceptance gate is modified.
"""
from pathlib import Path
import os, sys

SOURCE = Path(__file__).resolve().parent
UPSTREAM = Path(os.environ.get('PPT_MASTER_PATH', str(SOURCE/'upstream')))
sys.path.insert(0, str(UPSTREAM/'scripts'))
from attribution_guard import require_skill_integrity
from console_encoding import configure_utf8_stdio
from svg_to_pptx.drawingml.utils import EA_FONTS
from svg_to_pptx import main

if __name__ == '__main__':
    configure_utf8_stdio()
    require_skill_integrity()
    EA_FONTS.add('BIZ UDPGothic')
    raise SystemExit(main())
