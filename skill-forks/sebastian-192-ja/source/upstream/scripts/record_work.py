#!/usr/bin/env python3
"""Append explicit production events and report costs without inventing missing data."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

KINDS = {"start", "generation", "revision", "review", "delivery", "end", "preparation"}


def seal(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()


def timestamp(value):
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("Production timestamps need a timezone")
    return parsed.astimezone(timezone.utc)


def read_events(path):
    if not path.is_file():
        raise ValueError("Production log does not exist; missing work is not zero cost")
    events, previous = [], None
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        event = json.loads(line)
        unsigned = {k: v for k, v in event.items() if k != "sha256"}
        if event.get("previous_sha256") != previous or seal(unsigned) != event.get("sha256"):
            raise ValueError("Production log is incomplete or changed")
        if events and (event["task_id"] != events[0]["task_id"] or timestamp(event["at"]) < timestamp(events[-1]["at"])):
            raise ValueError("Production events must belong to one task in chronological order")
        events.append(event)
        previous = event["sha256"]
    return events


@contextmanager
def locked_log(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.with_suffix(path.suffix + ".lock").open("a+b") as stream:
        stream.seek(0)
        if not stream.read(1):
            stream.write(b"0")
            stream.flush()
        stream.seek(0)
        if os.name == "nt":
            import msvcrt
            msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl
            fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        try:
            yield
        finally:
            stream.seek(0)
            if os.name == "nt":
                msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


def append(path, task_id, kind, *, page_id=None, seconds=None, status=None, note="", at=None):
    path = path.resolve()
    if kind not in KINDS or not task_id.strip() or not note.strip():
        raise ValueError("Declare task, supported event kind and a factual note")
    if seconds is not None and (isinstance(seconds, bool) or not isinstance(seconds, (int, float)) or not math.isfinite(seconds) or seconds < 0):
        raise ValueError("Event duration must be finite and nonnegative")
    if kind == "revision" and not page_id:
        raise ValueError("Revision needs a page ID")
    if kind == "delivery" and status not in ("pass", "fail", "incomplete") or kind != "delivery" and status is not None:
        raise ValueError("Only delivery events declare pass/fail/incomplete")
    event = {"version": "1.0", "task_id": task_id, "kind": kind, "at": at or datetime.now(timezone.utc).isoformat(),
             "page_id": page_id, "seconds": seconds, "status": status, "note": note}
    moment = timestamp(event["at"])
    with locked_log(path):
        prior = read_events(path) if path.exists() else []
        if prior and (prior[0]["task_id"] != task_id or moment < timestamp(prior[-1]["at"])):
            raise ValueError("Task identity/timestamp differs from existing log")
        if prior and prior[-1]["kind"] == "end":
            raise ValueError("Task is ended; create a new task log")
        if kind == "start" and prior or kind == "end" and not any(e["kind"] == "start" for e in prior):
            raise ValueError("Start must be first; end requires a recorded start")
        event["previous_sha256"] = prior[-1]["sha256"] if prior else None
        event["sha256"] = seal(event)
        with path.open("a", encoding="utf-8", newline="\n") as stream:
            stream.write(json.dumps(event, ensure_ascii=False) + "\n")
            stream.flush()
            os.fsync(stream.fileno())
    return event


def summarize(path):
    events = read_events(path)
    starts = [e for e in events if e["kind"] == "start"]
    ends = [e for e in events if e["kind"] == "end"]
    deliveries = [e for e in events if e["kind"] == "delivery"]
    reviews = [e for e in events if e["kind"] == "review"]
    return {"task_id": events[0]["task_id"] if events else None, "events": len(events),
            "generation_calls": sum(e["kind"] == "generation" for e in events),
            "revised_page_count": len({e["page_id"] for e in events if e["kind"] == "revision"}),
            "review_seconds": sum(e["seconds"] for e in reviews if e["seconds"] is not None) if any(e["seconds"] is not None for e in reviews) else None,
            "review_events_without_duration": sum(e["seconds"] is None for e in reviews),
            "wall_seconds": (timestamp(ends[-1]["at"]) - timestamp(starts[0]["at"])).total_seconds() if starts and ends else None,
            "first_delivery_status": deliveries[0]["status"] if deliveries else None,
            "final_delivery_status": deliveries[-1]["status"] if deliveries else None,
            "complete_task_timing": bool(starts and ends), "log_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "scope": "Explicit recorded events only; unknown time remains null. Hashes do not authenticate factual notes."}


def aggregate(paths):
    summaries = [summarize(path) for path in paths]
    ids = [s["task_id"] for s in summaries]
    if len(set(ids)) != len(ids) or None in ids:
        raise ValueError("Aggregate requires distinct nonempty task logs")
    passed = sum(s["first_delivery_status"] == "pass" for s in summaries)
    return {"tasks": summaries, "registered_tasks": len(summaries), "first_passed": passed,
            "pending_first_delivery": sum(s["first_delivery_status"] is None for s in summaries),
            "first_pass_rate": passed / len(summaries) if summaries else None,
            "scope": "All supplied tasks remain in the denominator; completeness of registration is the caller's responsibility."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("log", type=Path)
    parser.add_argument("--task")
    parser.add_argument("--kind", choices=sorted(KINDS))
    parser.add_argument("--page")
    parser.add_argument("--seconds", type=float)
    parser.add_argument("--delivery-status", choices=("pass", "fail", "incomplete"))
    parser.add_argument("--note", default="")
    parser.add_argument("--at")
    parser.add_argument("--aggregate", type=Path, nargs="*")
    args = parser.parse_args()
    if args.kind:
        if not args.task:
            parser.error("--kind requires --task")
        append(args.log, args.task, args.kind, page_id=args.page, seconds=args.seconds, status=args.delivery_status, note=args.note, at=args.at)
    result = aggregate([args.log, *args.aggregate]) if args.aggregate is not None else summarize(args.log)
    print(json.dumps(result, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
