"""Compatibility entry point for the current Japanese atelier."""
from pathlib import Path
import runpy
ROOT=Path(__file__).resolve().parents[1]
runpy.run_path(str(ROOT/'tools/build_curated_collection.py'),run_name='__main__')
runpy.run_path(str(ROOT/'tools/build_atelier_site.py'),run_name='__main__')
