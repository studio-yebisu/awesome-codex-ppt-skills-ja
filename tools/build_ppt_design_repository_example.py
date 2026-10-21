"""Repository entry for the current scoped PPT-Design example builder.

The initial repository builder is retained under the example source history.
Current generation does not write global catalog/profile files.
"""
from pathlib import Path
import runpy
if __name__ == '__main__':
    runpy.run_path(str(Path(__file__).resolve().parents[1]/'examples/repositories/ppt-design-skill/source/build_ppt_design_repository_example.py'),run_name='__main__')
