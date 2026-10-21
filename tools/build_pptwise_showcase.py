"""Current source-built original pptwise replay entry. See retained case source."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).resolve().parents[1]/"examples/repositories/pptwise-showcase/source/rebuild_pptwise.py"),run_name="__main__")
