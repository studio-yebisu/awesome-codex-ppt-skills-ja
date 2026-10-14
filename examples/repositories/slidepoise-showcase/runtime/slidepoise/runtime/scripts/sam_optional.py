"""Optional SAM 2 measurement support for explicitly eligible semantic entities.

OpenCV remains the complete measurement path. This module is imported lazily and
returns pixel masks only. The host Agent owns entity meaning, eligibility, and the
visual review that determines whether the resulting boundary is useful.
"""
from __future__ import annotations

import time
from pathlib import Path
from typing import Any

import numpy as np


def eligible_entities(entities: list[dict[str, Any]], config: dict[str, Any]) -> list[dict[str, Any]]:
    policy = config.get("measurement", {}).get("segmentation", {}) or {}
    roles = set(policy.get("eligible_roles", []))
    return [
        entity
        for entity in entities
        if entity.get("segmentation_role") in roles
        and entity.get("segmentation_preference", "sam_if_available") == "sam_if_available"
        and entity.get("kind") not in {"text", "table", "chart", "connector", "icon", "icon_slot"}
    ]


def resolve_device(requested: str) -> str:
    import torch

    if requested != "auto":
        return requested
    if torch.cuda.is_available():
        return "cuda"
    if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def run(
    image_rgb: np.ndarray,
    entities: list[dict[str, Any]],
    *,
    checkpoint: Path,
    model_config: str,
    device: str,
) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    from sam2.build_sam import build_sam2
    from sam2.sam2_image_predictor import SAM2ImagePredictor

    started = time.perf_counter()
    model = build_sam2(model_config, str(checkpoint), device=device)
    predictor = SAM2ImagePredictor(model)
    loaded = time.perf_counter()
    predictor.set_image(image_rgb)
    embedded = time.perf_counter()
    results: dict[str, dict[str, Any]] = {}
    for entity in entities:
        x, y, width, height = [float(value) for value in (entity.get("bbox_hint") or entity.get("bbox"))]
        box = np.asarray([x, y, x + width, y + height], dtype=np.float32)
        prompt_started = time.perf_counter()
        masks, scores, _logits = predictor.predict(box=box, multimask_output=True)
        results[str(entity["id"])] = {
            "candidate_masks": [(mask > 0).astype(np.uint8) for mask in masks],
            "candidate_scores": [float(value) for value in scores],
            "prompt_time_sec": time.perf_counter() - prompt_started,
        }
    return results, {
        "model_load_sec": loaded - started,
        "image_embedding_sec": embedded - loaded,
        "total_sec": time.perf_counter() - started,
        "device": device,
    }


def attempt(
    image_rgb: np.ndarray,
    entities: list[dict[str, Any]],
    config: dict[str, Any],
    *,
    mode_override: str | None = None,
) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    policy = config.get("measurement", {}).get("segmentation", {}) or {}
    mode = mode_override or str(policy.get("mode", "never"))
    eligible = eligible_entities(entities, config)
    report: dict[str, Any] = {
        "provider": "sam2",
        "mode": mode,
        "eligible_entity_ids": [str(entity["id"]) for entity in eligible],
        "executed": False,
        "candidate_entity_ids": [],
        "selected_entity_ids": [],
        "skip_reason": None,
        "error": None,
    }
    if mode == "never":
        report["skip_reason"] = "disabled"
        return {}, report
    if not eligible:
        report["skip_reason"] = "no_host_authored_eligible_entities"
        return {}, report
    checkpoint_value = policy.get("checkpoint")
    if not checkpoint_value:
        report["skip_reason"] = "checkpoint_not_configured"
        if mode == "required":
            raise RuntimeError("SAM is required but measurement.segmentation.checkpoint is not configured")
        return {}, report
    checkpoint = Path(str(checkpoint_value)).expanduser().resolve()
    if not checkpoint.is_file():
        report["skip_reason"] = "checkpoint_unavailable"
        if mode == "required":
            raise FileNotFoundError(f"Required SAM checkpoint is unavailable: {checkpoint}")
        return {}, report
    try:
        device = resolve_device(str(policy.get("device", "auto")))
        results, timing = run(
            image_rgb,
            eligible,
            checkpoint=checkpoint,
            model_config=str(policy.get("model_config", "configs/sam2.1/sam2.1_hiera_t.yaml")),
            device=device,
        )
    except (ImportError, ModuleNotFoundError) as error:
        report["skip_reason"] = "optional_dependencies_unavailable"
        report["error"] = f"{type(error).__name__}: {error}"
        if mode == "required":
            raise RuntimeError(report["error"]) from error
        return {}, report
    except Exception as error:
        report["skip_reason"] = "runtime_error"
        report["error"] = f"{type(error).__name__}: {error}"
        if mode == "required":
            raise
        return {}, report
    report.update({
        "executed": True,
        "checkpoint": str(checkpoint),
        "candidate_entity_ids": sorted(results),
        **timing,
    })
    return results, report
