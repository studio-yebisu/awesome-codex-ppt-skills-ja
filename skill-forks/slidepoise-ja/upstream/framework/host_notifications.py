"""Best-effort input delivery to an explicitly bound, already-running Codex task.

Never starts a daemon, resumes a task, creates a turn, or acknowledges an event.
The durable run event remains authoritative if the local transport is unavailable.
"""
from __future__ import annotations

from framework import __version__

import json
import queue
import shutil
import subprocess
import threading

from .paths import data_home
from .storage import read, update


class CodexProxy:
    def __enter__(self):
        executable = shutil.which("codex")
        if not executable:
            raise RuntimeError("Codex CLI is unavailable")
        self.process = subprocess.Popen([executable, "app-server", "proxy"], stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, bufsize=1)
        self.messages = queue.Queue()
        self.counter = 0
        def receive():
            for line in self.process.stdout:
                try:
                    self.messages.put(json.loads(line))
                except ValueError:
                    continue
            self.messages.put(None)
        threading.Thread(target=receive, daemon=True).start()
        try:
            self.request("initialize", {"clientInfo": {"name": "slidepoise", "version": __version__}})
            self.send({"method": "initialized"})
        except Exception:
            self.__exit__(None, None, None)
            raise
        return self

    def send(self, message):
        self.process.stdin.write(json.dumps(message) + "\n")
        self.process.stdin.flush()

    def request(self, method, params):
        import time
        self.counter += 1
        identifier = self.counter
        self.send({"id": identifier, "method": method, "params": params})
        deadline = time.monotonic() + 4
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError("Codex did not respond")
            message = self.messages.get(timeout=remaining)
            if message is None:
                raise RuntimeError("Codex control socket is unavailable")
            if message.get("id") == identifier:
                if "error" in message:
                    raise RuntimeError("Codex declined the request")
                return message.get("result", {})

    def __exit__(self, *_):
        self.process.terminate()
        try:
            self.process.wait(timeout=1)
        except subprocess.TimeoutExpired:
            self.process.kill()
            self.process.wait()
        for stream in (self.process.stdin, self.process.stdout):
            stream.close()


def deliver(thread_id, root, event):
    try:
        with CodexProxy() as client:
            thread = client.request("thread/read", {"threadId": thread_id, "includeTurns": True}).get("thread", {})
            active = next((turn for turn in reversed(thread.get("turns", [])) if turn.get("status") == "inProgress"), None)
            if active is None:
                return "waiting_for_checkpoint"
            message = (f"SlidePoise presentation settings changed in the style panel. {event['summary']}. "
                       f"Run folder {root}. Event {event['id']}. Read slidepoise run sync for the current "
                       "settings before the next affected operation.")
            client.request("turn/steer", {"threadId": thread_id, "expectedTurnId": active["id"],
                           "input": [{"type": "text", "text": message}]})
        return "delivered"
    except Exception:
        return "waiting_for_checkpoint"


def notify(root, event):
    targets = set()
    for path in (data_home() / "panels").glob("*.json"):
        try:
            binding = read(path, {})
        except (OSError, ValueError):
            continue
        if isinstance(binding, dict) and binding.get("run") == str(root.resolve()) and isinstance(binding.get("host_thread_id"), str):
            if binding["host_thread_id"]:
                targets.add(binding["host_thread_id"])
    if not targets:
        return
    target = root / "work/panel-events.json"
    def send():
        deliveries = {thread: deliver(thread, root, event) for thread in targets}
        def save(document):
            for item in document.get("events", []):
                if item["id"] == event["id"]:
                    item["delivery"] = deliveries
            return document
        update(target, save, default={"events": []})
    threading.Thread(target=send, daemon=True, name="slidepoise-host-notification").start()
