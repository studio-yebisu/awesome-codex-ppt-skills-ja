"""Generation preferences and objective tool compatibility. The host chooses tools."""
from __future__ import annotations

DEFAULTS = {"mode": "auto", "tool": "", "model": "", "instructions": ""}


def preferences(values=None):
    if values is None:
        return dict(DEFAULTS)
    if not isinstance(values, dict) or set(values) - DEFAULTS.keys():
        raise ValueError("Unknown image generation setting")
    result = {**DEFAULTS, **values}
    if not isinstance(result["mode"], str) or result["mode"] not in {"auto", "tool", "manual"}:
        raise ValueError("Choose automatic, a specific tool or manual image generation")
    for key, maximum in (("tool", 300), ("model", 200), ("instructions", 4000)):
        if not isinstance(result[key], str) or len(result[key]) > maximum:
            raise ValueError(f"Image generation {key} must be text of at most {maximum} characters")
        result[key] = result[key].strip()
    if result["mode"] == "tool" and not result["tool"]:
        raise ValueError("Name the image tool you want the Agent to use")
    return result


def resolve_preferences(generation, override=None):
    if not isinstance(generation, dict):
        raise ValueError("Image generation configuration must be an object")
    result = preferences(generation.get("preferences"))
    if override is not None:
        if not isinstance(override, dict):
            raise ValueError("Image generation overrides must be an object")
        result = preferences({**result, **override})
    return result


def compatible_tools(request, inventory, settings):
    """Check host-authored capability facts, without ranking visual quality."""
    if not isinstance(inventory, dict) or not isinstance(inventory.get("tools"), list):
        raise ValueError("Provide the tools discovered in this conversation")
    result, seen = [], set()
    operation = "generate" if request["purpose"] == "host_image_generation_request" else "edit"
    for tool in inventory["tools"]:
        if not isinstance(tool, dict) or not isinstance(tool.get("id"), str) or not tool["id"].strip() or tool["id"] in seen:
            raise ValueError("Discovered tools need unique, non-empty IDs")
        seen.add(tool["id"])
        if not isinstance(tool.get("operations"), list) or any(not isinstance(op, str) or op not in {"generate", "edit"} for op in tool["operations"]):
            raise ValueError("Tool operations must list generate and/or edit")
        reasons = []
        if tool.get("available") is not True:
            reasons.append("Availability has not been confirmed in this conversation")
        if operation not in tool.get("operations", []):
            reasons.append(f"The tool does not declare support for {operation}")
        if request.get("reference_images") and tool.get("reference_images") is not True:
            reasons.append("The request requires image attachments")
        if request.get("background") == "transparent" and tool.get("transparent_background") is not True:
            reasons.append("The request requires genuine transparency")
        for field, required in (("max_prompt_chars", len(request["prompt"])), ("max_reference_images", len(request.get("reference_images", [])))):
            limit = tool.get(field)
            if limit is not None:
                if isinstance(limit, bool) or not isinstance(limit, int) or limit < 0:
                    raise ValueError(f"{field} must be a non-negative integer or null")
                if required > limit:
                    reasons.append(f"Request exceeds {field} ({required} > {limit})")
        model = settings["model"]
        if model and (not isinstance(tool.get("models"), list) or model not in tool["models"]):
            reasons.append("The selected model is not confirmed for this tool")
        result.append({"id": tool["id"], "compatible": not reasons, "reasons": reasons})
    return result
