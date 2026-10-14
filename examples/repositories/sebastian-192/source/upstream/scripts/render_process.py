"""Bounded renderer subprocesses; retries never alter user documents."""
from __future__ import annotations

import contextvars
import math
import os
import signal
import subprocess
from contextlib import contextmanager
from pathlib import Path
from types import MappingProxyType

OPTIONS = contextvars.ContextVar("render_options", default=MappingProxyType({"timeout": 120, "retries": 1, "measure_text": False}))


def validate_options(timeout=120, retries=1, measure_text=False):
    if isinstance(timeout, bool) or not isinstance(timeout, (int, float)) or not math.isfinite(timeout) or not 1 <= timeout <= 3600:
        raise ValueError("Render timeout must be finite and between 1 and 3600 seconds")
    if isinstance(retries, bool) or not isinstance(retries, int) or not 0 <= retries <= 2:
        raise ValueError("Render retries must be an integer between 0 and 2")
    if not isinstance(measure_text, bool):
        raise TypeError("measure_text must be boolean")
    return {"timeout": timeout, "retries": retries, "measure_text": measure_text}


@contextmanager
def rendering_options(**options):
    token = OPTIONS.set(validate_options(**options))
    try:
        yield
    finally:
        OPTIONS.reset(token)


def cleanup_powerpoint(shell, marker):
    """The helper checks PID, creation time and confirmed ownership before stopping."""
    if marker and marker.is_file():
        try:
            subprocess.run([shell, "-NoProfile", "-NonInteractive", "-File",
                            str(Path(__file__).with_name("cleanup_powerpoint.ps1")), "-Marker", str(marker)],
                           capture_output=True, timeout=10, check=True)
        except (OSError, subprocess.SubprocessError):
            return "Owned PowerPoint cleanup could not be verified; inspect the renderer process."
    return "Existing PowerPoint processes were preserved; inspect any task-only read-only presentation before resuming."


def execute(command, *, label, retry_safe=True, powerpoint_marker=None):
    options = OPTIONS.get()
    attempts = 1 + (options["retries"] if retry_safe else 0)
    last = ""
    for attempt in range(attempts):
        kwargs = {"stdout": subprocess.PIPE, "stderr": subprocess.PIPE}
        if os.name == "nt":
            kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
        else:
            kwargs["start_new_session"] = True
        process = subprocess.Popen(command, **kwargs)
        try:
            stdout, stderr = process.communicate(timeout=options["timeout"])
        except subprocess.TimeoutExpired:
            if os.name == "nt":
                # Kill only descendants of this newly launched helper; shared COM is separate.
                try:
                    subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"],
                                   capture_output=True, timeout=10, check=True,
                                   creationflags=subprocess.CREATE_NO_WINDOW)
                except (OSError, subprocess.SubprocessError):
                    process.kill()
            else:
                os.killpg(process.pid, signal.SIGKILL)
            process.communicate(timeout=10)
            cleanup = cleanup_powerpoint(command[0], powerpoint_marker) if powerpoint_marker else ""
            last = f"{label} renderer timed out after {options['timeout']} seconds. {cleanup}"
        else:
            if process.returncode == 0:
                return stdout.decode("utf-8", errors="replace")
            last = f"{label} renderer exited {process.returncode}: {stderr.decode('utf-8', errors='replace')[-4000:]}"
        if attempt + 1 == attempts:
            raise RuntimeError(last + f" Attempts: {attempts}. Saved build remains resumable.")
