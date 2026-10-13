"""Canonical release checks for the current Astra specification."""
import subprocess,sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]
raise SystemExit(subprocess.run([sys.executable,str(root/'tools/verify_case_release.py')],cwd=root).returncode)
