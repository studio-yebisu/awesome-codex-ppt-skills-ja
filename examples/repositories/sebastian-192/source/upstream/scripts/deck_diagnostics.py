"""Read-only preflight and Chinese task descriptions for deck delivery."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from json_io import read_json
from PIL import Image
from runtime_environment import renderer_environment
from scene import load_scene
from speaker_notes import check_scene_notes
from validate_page_spec import _relative_path, load_page_spec

STATUS_LABELS = {"running": "运行中", "complete": "检查通过", "stopped": "已保存阶段", "ready": "可继续",
                 "awaiting_review": "等待审阅", "failed": "检查失败", "blocked": "需要修复输入"}


def print_result(result):
    """Readable Chinese JSON, preserving diagnostics on legacy console encodings."""
    encoding = sys.stdout.encoding or "utf-8"
    text = json.dumps(result, ensure_ascii=False, indent=2)
    try:
        text.encode(encoding)
    except UnicodeEncodeError:
        text = json.dumps(result, ensure_ascii=True, indent=2)
    print(text)


def action(kind, message, *, file=None, slide_id=None, page_number=None, detail=None):
    item = {"kind": kind, "message": message}
    for name, value in (("file", file), ("slide_id", slide_id), ("page_number", page_number), ("detail", detail)):
        if value is not None:
            item[name] = str(value) if isinstance(value, Path) else value
    return item


def error_action(error, file=None):
    detail = str(error)
    if "stale" in detail.lower():
        message = "审阅证据与当前文件不一致。重新生成当前模板，查看新画面后填写；保留旧记录。"
    elif "workspace" in detail.lower() or "state" in detail.lower():
        message = "检查工作目录归属或状态完整性。保留原目录，改用新的空工作目录后重试。"
    elif "renderer" in detail.lower() or "PowerPoint" in detail:
        message = "渲染未完成。检查 PowerPoint 或 LibreOffice/Poppler 环境，修复后重复原命令。"
    elif "notes" in detail:
        message = "讲稿与规格不一致。按页面同步讲稿内容后重试。"
    elif "dependencies" in detail:
        message = "声明的数据依赖不一致。核对图表、正文、公式和讲稿后重试。"
    else:
        message = "输入或交付检查未通过。按下方原始诊断修复对应文件，再重复原命令。"
    return action("repair", message, file=file, detail=detail)


def preflight(config_path, work, *, check_renderer=True):
    """Collect page-specific input problems without generating or modifying artifacts."""
    config_path, work = config_path.resolve(), work.resolve()
    result = {"status": "ready", "status_label": STATUS_LABELS["ready"], "actions": [], "checks": [],
              "job": str(config_path), "workspace": str(work)}
    actions = result["actions"]
    try:
        config = read_json(config_path)
        from run_deck import FIELDS, cached_state, load_inputs
        if (not isinstance(config, dict) or set(config) - FIELDS or config.get("version") != "1.0"
                or config.get("mode") not in ("image", "editable")):
            raise ValueError("Job needs version 1.0, mode image/editable and supported fields")
        width = config.get("width", 1600)
        if isinstance(width, bool) or not isinstance(width, int) or not 320 <= width <= 16384:
            raise ValueError("Render width must be an integer between 320 and 16384")
        backend = config.get("backend", "auto")
        if backend not in ("auto", "powerpoint", "libreoffice"):
            raise ValueError("Unknown render backend")
        resolve = lambda name: _relative_path(config_path.parent, name)
        spec_path = resolve(config["page_spec"])
        scene_path = resolve(config["scene"]) if config.get("scene") else None
        if config["mode"] == "editable" and not scene_path:
            actions.append(action("scene", "可编辑任务缺少 scene 配置。请指定已准备好的重建规格。", file=config_path))
        if config["mode"] == "image" and scene_path:
            actions.append(action("scene", "图片任务应省略 scene 字段。", file=config_path))
        spec = None
        try:
            spec, _ = load_page_spec(spec_path, strict=True)
            result["checks"].append("页面规格结构与内容确认通过")
        except (ValueError, OSError, TypeError, KeyError) as error:
            actions.append(error_action(error, spec_path))
        if spec:
            for n, slide in enumerate(spec["slides"], 1):
                path = _relative_path(spec_path.parent, slide["image_file"])
                info = {"file": path, "slide_id": slide["id"], "page_number": n}
                allowed = ("approved",) if config["mode"] == "image" else ("approved", "revision")
                if slide["image_status"] not in allowed:
                    actions.append(action("image_approval", "请实际检查此页图片并确认状态；工具不会自动批准。", **info))
                if not path.is_file():
                    actions.append(action("missing_image", "缺少此页图片。补齐规格中声明的文件后重试。", **info))
                else:
                    try:
                        with Image.open(path) as image:
                            if image.format not in ("PNG", "JPEG"):
                                raise ValueError("Reference image must be PNG or JPEG")
                            image.verify()
                    except (ValueError, OSError) as error:
                        actions.append(action("invalid_image", "此页图片无法读取，请检查文件格式或重新导出。", detail=str(error), **info))
            if config["mode"] == "image" and not actions:
                load_page_spec(spec_path, strict=True, require_images=True)
        if scene_path:
            try:
                scene, _ = load_scene(scene_path)
                if spec and (errors := check_scene_notes(spec, scene)):
                    raise ValueError("; ".join(errors))
                result["checks"].append("重建规格、素材、页序与已声明讲稿通过")
            except (ValueError, OSError, KeyError, TypeError) as error:
                actions.append(error_action(error, scene_path))
        if work.exists() and any(work.iterdir()):
            owner = work / "owner.json"
            if not owner.is_file() or read_json(owner) != {"version": "1.0", "config": str(config_path)}:
                actions.append(action("workspace", "工作目录包含其他材料或属于不同任务。请使用新的空目录。", file=work))
            else:
                cached_state(work)
        if not actions:
            inputs = load_inputs(config_path, work)
            if "data_bindings" in inputs["optional"]:
                from update_data_bindings import inspect
                check = inspect(inputs["optional"]["data_bindings"], inputs["spec_path"], inputs["scene_path"])
                if check["status"] != "pass":
                    actions.append(action("data_bindings", "数据依赖存在冲突。核对声明的数值、正文和讲稿。",
                                          file=inputs["optional"]["data_bindings"], detail=json.dumps(check["errors"], ensure_ascii=False)))
        environment = renderer_environment(backend) if check_renderer else None
        if environment:
            result["renderer"] = environment
            if not environment["ready"]:
                actions.append(action("renderer_environment", "未发现所选渲染环境。Windows 需 PowerPoint；或配置 LibreOffice 和 pdftoppm。"))
    except (ValueError, OSError, KeyError, TypeError) as error:
        actions.append(error_action(error, config_path))
    if actions:
        result.update(status="blocked", status_label=STATUS_LABELS["blocked"])
    result["note"] = "预检不编译、不渲染、不填写审阅结论；通过只表示声明输入检查完成。"
    return result
