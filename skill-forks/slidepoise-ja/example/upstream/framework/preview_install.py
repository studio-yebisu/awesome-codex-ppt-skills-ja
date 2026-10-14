"""Install missing native preview tools through an existing system package manager."""
from __future__ import annotations
import os
from pathlib import Path
import shutil
import subprocess
import sys

from .paths import SKILL_ROOT
sys.path.insert(0, str(SKILL_ROOT / 'runtime/src'))
from slidepoise.preview_tools import find_preview_tool


def preview_status():
    return {'office': find_preview_tool('office'), 'pdftoppm': find_preview_tool('pdftoppm')}


def installation_commands(missing, platform=None):
    platform = platform or sys.platform
    if platform == 'darwin':
        brew = shutil.which('brew')
        if not brew:
            brew = next((str(p) for p in (Path('/opt/homebrew/bin/brew'), Path('/usr/local/bin/brew')) if p.is_file()), None)
        if not brew:
            return [], 'Install Homebrew from https://brew.sh, then run setup again.'
        return ([[brew, 'install', '--cask', 'libreoffice']] if 'office' in missing else []) + ([[brew, 'install', 'poppler']] if 'pdftoppm' in missing else []), None
    if platform == 'win32':
        manager = shutil.which('winget')
        if not manager:
            return [], 'Install Microsoft App Installer to enable winget, then run setup again.'
        packages = {'office': 'TheDocumentFoundation.LibreOffice', 'pdftoppm': 'oschwartz10612.Poppler'}
        return [[manager, 'install', '--exact', '--id', packages[key], '--accept-source-agreements', '--accept-package-agreements'] for key in missing], None
    if platform.startswith('linux'):
        manager = shutil.which('apt-get')
        if not manager:
            return [], 'Automatic preview setup currently supports Debian/Ubuntu. Install LibreOffice Impress and Poppler using your distribution package manager, then run setup again.'
        prefix = []
        if getattr(os, 'geteuid', lambda: 1)() != 0:
            sudo = shutil.which('sudo')
            if not sudo:
                return [], 'An administrator must install libreoffice-impress and poppler-utils, then run setup again.'
            prefix = [sudo]
        packages = {'office': 'libreoffice-impress', 'pdftoppm': 'poppler-utils'}
        return [prefix + [manager, 'update'], prefix + [manager, 'install', '-y'] + [packages[key] for key in missing]], None
    return [], 'Automatic preview installation is unavailable on this operating system.'


def install_preview_tools():
    before = preview_status()
    missing = [key for key, value in before.items() if not value]
    if not missing:
        return {'status': 'ready', 'tools': before, 'commands': []}
    commands, help_text = installation_commands(missing)
    results = []
    for command in commands:
        print('Installing slide preview tools with ' + ' '.join(command), file=sys.stderr, flush=True)
        try:
            result = subprocess.run(command, stdout=sys.stderr, stderr=sys.stderr, check=False)
            code = result.returncode
        except OSError as error:
            code = 1
            help_text = str(error)
        results.append({'command': command, 'exit_code': code})
        if code:
            help_text = 'The system package manager could not finish. Resolve the error above and run setup again.'
            break
    after = preview_status()
    ready = all(after.values())
    return {'status': 'ready' if ready else 'incomplete', 'tools': after, 'commands': results,
            'next_step': None if ready else help_text or 'Preview executables were not found after installation. Check the package manager output and run setup again.'}
