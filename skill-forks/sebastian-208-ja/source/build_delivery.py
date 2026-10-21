"""Portable compatibility entry forwarding to current example; legacy cloud preparation preserved locally."""
from pathlib import Path
import runpy
if __name__ == "__main__":
    runpy.run_path(str(Path(__file__).resolve().parents[1] / "example/source/reproduce.py"), run_name="__main__")
