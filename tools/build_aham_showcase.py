"""Current Aham source entry; partial layout/conversion demonstration."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).resolve().parents[1]/"examples/repositories/aham-showcase/generate.py"),run_name="__main__")
