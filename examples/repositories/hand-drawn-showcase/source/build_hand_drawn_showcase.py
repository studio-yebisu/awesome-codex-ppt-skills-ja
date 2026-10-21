"""Portable entry to this example only; does not update catalog data."""
from pathlib import Path
import subprocess,sys,os,shutil
C=Path(__file__).resolve().parents[1]
if __name__=='__main__':
 node=shutil.which('node')
 if not node:raise SystemExit('Prepared Node.js runtime required.')
 raise SystemExit(subprocess.run([node,'build.cjs'],cwd=C,env=dict(os.environ,HANDDRAWN_PYTHON=sys.executable)).returncode)
