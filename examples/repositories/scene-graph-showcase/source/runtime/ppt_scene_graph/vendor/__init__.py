# Vendor package for bundled dependencies
# This allows ppt_scene_graph to be self-contained without external dependencies

__version__ = "1.0.2"

# Expose the vendored pptx package
from .pptx import *
