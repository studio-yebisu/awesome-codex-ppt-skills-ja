"""User changes from the session panel that the host Agent must consume."""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from .sessions import require_run
from .storage import read, revision, update, locked


def path(root):
    return require_run(root) / "work/panel-events.json"


def record(root, kind, summary, details=None):
    target = path(root)
    event = {"id": uuid.uuid4().hex, "kind": kind, "summary": summary,
             "details": details or {}, "created_at": datetime.now(timezone.utc).isoformat(), "status": "pending"}
    update(target, lambda value: {"events": value.get("events", []) + [event]}, default={"events": []})
    from .host_notifications import notify
    notify(target.parent.parent, event)
    return event


def pending(root):
    target = path(root)
    with locked(target):
        value = read(target, {"events": []})
        return {"events": [event for event in value["events"] if event.get("status") == "pending"],
                "revision": revision(target)}


def acknowledge(root, ids, expected):
    target = path(root)
    wanted = set(ids)
    def change(value):
        for event in value.get("events", []):
            if event["id"] in wanted:
                event["status"] = "acknowledged"
        return value
    update(target, change, expected=expected, default={"events": []})
    return pending(root)
