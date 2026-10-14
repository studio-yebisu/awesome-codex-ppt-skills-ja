#!/usr/bin/env python3
"""Generate a delivery job from existing specifications without changing approvals."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from deck_diagnostics import preflight, print_result
from validate_page_spec import _relative_path


def initialize(directory, mode="image", backend="auto", width=1600, output="job.json",
               page_spec="page-spec.json", scene="scene.json"):
    directory = directory.resolve()
    if not directory.is_dir():
        raise ValueError("任务材料目录不存在")
    if mode not in ("image", "editable") or backend not in ("auto", "powerpoint", "libreoffice"):
        raise ValueError("交付模式或渲染后端不合法")
    if isinstance(width, bool) or not isinstance(width, int) or not 320 <= width <= 16384:
        raise ValueError("渲染宽度必须为 320–16384 的整数")
    job = _relative_path(directory, output)
    # Paths are relative to the job, including jobs placed in a subdirectory.
    def relative(value):
        path = _relative_path(directory, value)
        if not path.is_relative_to(job.parent):
            raise ValueError("配置文件必须与输入处于同一目录或其父目录")
        return path.relative_to(job.parent).as_posix()
    config = {"version": "1.0", "mode": mode, "page_spec": relative(page_spec), "backend": backend, "width": width}
    if mode == "editable":
        config["scene"] = relative(scene)
    job.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive creation: never overwrite a hand-edited job or any source input.
    with job.open("x", encoding="utf-8") as stream:
        json.dump(config, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    result = preflight(job, directory.parent / (directory.name + "-output"))
    result["created_job"] = str(job)
    result["message"] = "任务配置已生成。图片与内容批准状态保持原样；待办见预检结果。"
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--mode", choices=("image", "editable"), default="image")
    parser.add_argument("--backend", choices=("auto", "powerpoint", "libreoffice"), default="auto")
    parser.add_argument("--width", type=int, default=1600)
    parser.add_argument("--output", default="job.json")
    parser.add_argument("--page-spec", default="page-spec.json")
    parser.add_argument("--scene", default="scene.json")
    args = parser.parse_args()
    try:
        result = initialize(args.directory, args.mode, args.backend, args.width, args.output, args.page_spec, args.scene)
    except (ValueError, OSError) as error:
        result = {"status": "blocked", "status_label": "配置未生成", "actions": [{"kind": "configuration", "message": str(error)}]}
    print_result(result)
    if result["status"] == "blocked":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
