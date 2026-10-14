"""Locate native preview executables without requiring a restarted shell."""
import os
from pathlib import Path
import shutil
import sys


def find_preview_tool(name):
    aliases = ('libreoffice', 'soffice') if name == 'office' else ('pdftoppm',)
    for alias in aliases:
        found = shutil.which(alias)
        if found:
            return found
    candidates = []
    if sys.platform == 'darwin':
        candidates = ([Path('/Applications/LibreOffice.app/Contents/MacOS/soffice'),
                       Path.home() / 'Applications/LibreOffice.app/Contents/MacOS/soffice'] if name == 'office'
                      else [Path('/opt/homebrew/bin/pdftoppm'), Path('/usr/local/bin/pdftoppm')])
    elif sys.platform == 'win32':
        if name == 'office':
            candidates = [Path(os.environ[key]) / 'LibreOffice/program/soffice.exe'
                          for key in ('ProgramFiles', 'ProgramFiles(x86)', 'LOCALAPPDATA') if os.environ.get(key)]
        elif os.environ.get('LOCALAPPDATA'):
            winget = Path(os.environ['LOCALAPPDATA']) / 'Microsoft/WinGet'
            candidates = [winget / 'Links/pdftoppm.exe']
            candidates += sorted((winget / 'Packages').glob('oschwartz10612.Poppler_*/**/pdftoppm.exe'))
    return next((str(path) for path in candidates if path.is_file()), None)
