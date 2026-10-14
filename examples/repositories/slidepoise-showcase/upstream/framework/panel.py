"""Start or reuse the local companion server and return a run-bound URL."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from urllib.parse import urlencode

from .paths import data_home
from . import panel_binding


def open_panel(run: str | None = None, port: int = 18765, view: str = "session", panel_id: str | None = None) -> dict:
    if not 1024 <= port <= 65535:
        raise ValueError("Choose a local port between 1024 and 65535")
    if view not in {"session", "style"}:
        raise ValueError("The session panel only supports style and asset overrides")
    if run is None and panel_id is None:
        raise ValueError("Bind the style panel to a presentation run")
    binding = panel_binding.ensure(panel_id, run, host_thread_id=os.environ.get("CODEX_THREAD_ID"))
    base = f"http://127.0.0.1:{port}"
    def running():
        try:
            with urllib.request.urlopen(base + "/api/context", timeout=.5) as response:
                result = json.load(response)
                if result.get("service") != "slidepoise":
                    raise ValueError("This port belongs to another service")
                return True
        except urllib.error.URLError:
            return False
    started = False
    if not running():
        directory = data_home() / "logs"
        directory.mkdir(parents=True, exist_ok=True)
        with (directory / "panel.log").open("ab") as log:
            process = subprocess.Popen([sys.executable, "-m", "webapp.server", "--host", "127.0.0.1", "--port", str(port), "--no-open"],
                                       stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
        for _ in range(40):
            if running():
                started = True
                break
            if process.poll() is not None:
                raise RuntimeError("Panel server could not start. See the panel log.")
            time.sleep(.1)
        else:
            raise RuntimeError("Panel server is still starting. Try the panel command again.")
    url = base + "/?" + urlencode({"panel": binding["id"]})
    return {"url": url, "panel_id": binding["id"], "run": binding["run"], "revision": binding["revision"], "server_started": started}
