#!/usr/bin/env python3
"""Preview numeric dependencies and export a separate review draft; never edit source files."""
from __future__ import annotations

import argparse
import ast
import copy
import json
import math
import operator
import os
import re
import shutil
import string
import tempfile
from pathlib import Path

from json_io import read_json
from render_deck import sha256
from scene import load_scene, walk
from validate_page_spec import _relative_path, load_page_spec

OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv}
NAME = re.compile(r"^[A-Za-z][A-Za-z0-9_]*$")


def finite(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError("Inputs and derived values must be finite numbers")
    try:
        valid = math.isfinite(value)
    except OverflowError:
        valid = False
    if not valid:
        raise ValueError("Inputs and derived values must be finite numbers")
    return value


def values_for(contract, overrides=None):
    inputs, formulas = contract.get("inputs"), contract.get("formulas", {})
    if not isinstance(inputs, dict) or not inputs or not isinstance(formulas, dict):
        raise ValueError("Provide inputs and an optional formulas mapping")
    if set(inputs) & set(formulas) or any(not NAME.fullmatch(k) for k in [*inputs, *formulas]):
        raise ValueError("Input/formula names must be unique plain identifiers")
    overrides = {} if overrides is None else overrides
    if not isinstance(overrides, dict) or set(overrides) - set(inputs):
        raise ValueError("Only declared numeric inputs can be changed")
    values = {}
    for key, item in inputs.items():
        if (not isinstance(item, dict) or set(item) != {"value", "unit", "source_ref"}
                or not all(isinstance(item[k], str) and item[k].strip() for k in ("unit", "source_ref"))):
            raise ValueError("Each input needs value, unit and source_ref")
        values[key] = finite(overrides.get(key, item["value"]))
    active = set()

    def resolve(key):
        if key in values:
            return values[key]
        if key not in formulas or key in active:
            raise ValueError(f"Unknown dependency or cyclic formula: {key}")
        expression = formulas[key]
        if not isinstance(expression, str) or len(expression) > 500:
            raise ValueError("Formulas must be short arithmetic expressions")
        active.add(key)
        try:
            tree = ast.parse(expression, mode="eval")
            if sum(1 for _ in ast.walk(tree)) > 100:
                raise ValueError("Formula is too complex")
            result = calculate(tree.body)
        except (SyntaxError, ZeroDivisionError, OverflowError, RecursionError) as error:
            raise ValueError(f"Invalid formula {key}: {error}") from error
        finally:
            active.remove(key)
        values[key] = finite(result)
        return result

    def calculate(node):
        if isinstance(node, ast.Constant):
            return finite(node.value)
        if isinstance(node, ast.Name):
            return resolve(node.id)
        if isinstance(node, ast.BinOp) and type(node.op) in OPS:
            return finite(OPS[type(node.op)](calculate(node.left), calculate(node.right)))
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            return finite(calculate(node.operand) * (-1 if isinstance(node.op, ast.USub) else 1))
        raise ValueError("Only numbers, names, +, -, *, / and parentheses are allowed")

    for key in formulas:
        resolve(key)
    return values


def binding_value(binding, values):
    if set(binding) not in ({"document", "pointer", "value"}, {"document", "pointer", "template"}):
        raise ValueError("Bindings need document, pointer, and exactly one value or template")
    if "value" in binding:
        key = binding["value"]
        if not isinstance(key, str) or key not in values:
            raise ValueError("Binding names an unknown value")
        return values[key]
    template = binding["template"]
    if not isinstance(template, str) or len(template) > 10000:
        raise ValueError("Template must be text")
    result = []
    for literal, key, fmt, conversion in string.Formatter().parse(template):
        result.append(literal)
        if key is not None:
            if key not in values or conversion or not re.fullmatch(r"(?:[+\-])?(?:\.\d{1,2})?[fg%]?", fmt):
                raise ValueError("Template fields must name values with simple numeric formatting")
            if re.search(r"\.(\d+)", fmt) and int(re.search(r"\.(\d+)", fmt)[1]) > 12:
                raise ValueError("Template precision exceeds 12")
            result.append(format(values[key], fmt))
    return "".join(result)


def target(document, pointer, kind):
    if not isinstance(pointer, str):
        raise TypeError("Binding pointer must be a string")
    if kind == "page_spec":
        pattern = (r"/slides/\d+/(?:speaker_notes|title|core_message|source_refs/\d+|required_visible_values/\d+"
                   r"|elements/\d+/(?:text|source_ref|notes|data/(?:[^/]+/)*[^/]+))")
    else:
        pattern = (r"/slides/\d+/(?:speaker_notes|elements/\d+/(?:children/\d+/)*"
                   r"(?:text|runs/\d+/text|series/\d+/values/\d+|categories/\d+|rows/\d+/\d+))")
    if not re.fullmatch(pattern, pointer):
        raise ValueError(f"Binding cannot change metadata, geometry or assets: {pointer}")
    tokens = [t.replace("~1", "/").replace("~0", "~") for t in pointer.split("/")[1:]]
    parent = document
    for token in tokens[:-1]:
        parent = parent[int(token)] if isinstance(parent, list) else parent[token]
    key = int(tokens[-1]) if isinstance(parent, list) else tokens[-1]
    current = parent[key]
    if isinstance(current, bool) or not isinstance(current, (str, int, float)):
        raise TypeError("Bindings must target existing text or numeric leaves")
    return parent, key, tokens[1], current


def read_contract(path):
    contract = read_json(path)
    if (not isinstance(contract, dict) or contract.get("version") != "1.0"
            or set(contract) != {"version", "documents", "inputs", "formulas", "bindings"}):
        raise ValueError("Invalid data binding contract")
    names = contract["documents"]
    if (not isinstance(names, dict) or not names or set(names) - {"page_spec", "scene"}
            or not isinstance(contract["bindings"], list) or not contract["bindings"]):
        raise ValueError("Declare Page Spec/Scene documents and nonempty bindings")
    paths = {kind: _relative_path(path.parent, name) for kind, name in names.items()}
    if len(set(paths.values())) != len(paths) or path.resolve() in paths.values():
        raise ValueError("Document and contract paths must be distinct")
    documents = {kind: (load_page_spec(p)[0] if kind == "page_spec" else load_scene(p)[0])
                 for kind, p in paths.items()}
    if len(documents) == 2 and ([s["id"] for s in documents["page_spec"]["slides"]]
                              != [s["id"] for s in documents["scene"]["slides"]]):
        raise ValueError("Page Spec and Scene must declare the same slide IDs and order")
    return contract, paths, documents


def inspect(path, page_spec=None, scene=None):
    contract, paths, documents = read_contract(path.resolve())
    for kind, actual in (("page_spec", page_spec), ("scene", scene)):
        if actual and (kind not in paths or paths[kind] != actual.resolve()):
            raise ValueError(f"Data contract is bound to a different {kind}")
    values = values_for(contract)
    errors, seen = [], set()
    for binding in contract["bindings"]:
        kind = binding.get("document")
        if kind not in documents:
            raise ValueError("Binding document is not declared")
        identity = (kind, binding["pointer"])
        if identity in seen:
            raise ValueError("Duplicate binding target")
        seen.add(identity)
        _, _, _, current = target(documents[kind], binding["pointer"], kind)
        expected = binding_value(binding, values)
        if type(current) is str and not isinstance(expected, str) or not isinstance(current, str) and isinstance(expected, str):
            raise ValueError("Binding output changes the target type")
        if current != expected:
            errors.append({"document": kind, "pointer": binding["pointer"], "expected": expected, "actual": current})
    return {"status": "fail" if errors else "pass", "errors": errors, "values": values,
            "contract_sha256": sha256(path), "document_sha256": {kind: sha256(p) for kind, p in paths.items()},
            "scope": "Declared arithmetic and bindings only; not source truth or semantic completeness."}


def page_dependencies(path):
    """Visible bindings plus their transitive numeric provenance, scoped to each page."""
    contract, _, documents = read_contract(path.resolve())
    values_for(contract)  # Validate every formula, including unrelated/cyclic definitions.
    result = {slide["id"]: {"bindings": [], "inputs": {}, "formulas": {}}
              for document in documents.values() for slide in document["slides"]}
    for binding in contract["bindings"]:
        kind = binding["document"]
        _, _, index, _ = target(documents[kind], binding["pointer"], kind)
        if binding["pointer"].endswith("/speaker_notes"):
            continue  # Notes are checked/rebuilt globally, without invalidating visible pixels.
        page = result[documents[kind]["slides"][int(index)]["id"]]
        page["bindings"].append(binding)
        names = [binding["value"]] if "value" in binding else [name for _, name, _, _ in string.Formatter().parse(binding["template"]) if name is not None]

        def include(name, page=page):
            if name in contract["inputs"]:
                page["inputs"][name] = contract["inputs"][name]
            elif name not in page["formulas"]:
                expression = contract["formulas"][name]
                page["formulas"][name] = expression
                for node in ast.walk(ast.parse(expression, mode="eval")):
                    if isinstance(node, ast.Name):
                        include(node.id)

        for name in names:
            include(name)
    for page in result.values():
        page["bindings"].sort(key=lambda b: (b["document"], b["pointer"]))
    return result


def plan_update(path, overrides):
    path = path.resolve()
    baseline = inspect(path)
    if baseline["errors"]:
        raise ValueError("Current documents disagree with bindings; resolve stale content before updating")
    contract, paths, documents = read_contract(path)
    values = values_for(contract, overrides)
    changes, affected, visible = [], set(), set()
    for binding in contract["bindings"]:
        kind = binding["document"]
        parent, key, slide_index, before = target(documents[kind], binding["pointer"], kind)
        after = binding_value(binding, values)
        if before != after:
            parent[key] = after
            slide_id = documents[kind]["slides"][int(slide_index)]["id"]
            affected.add(slide_id)
            if not binding["pointer"].endswith("/speaker_notes"):
                visible.add(slide_id)
            changes.append({"document": kind, "pointer": binding["pointer"], "slide_id": slide_id,
                            "before": before, "after": after})
    updated = copy.deepcopy(contract)
    for key, value in overrides.items():
        updated["inputs"][key]["value"] = value
    return {"source_contract_sha256": sha256(path), "source_document_sha256": baseline["document_sha256"],
            "values": values, "changes": changes, "affected_slides": sorted(affected),
            "visible_slides": sorted(visible), "documents": documents, "contract": updated,
            "required_reviews": ["source and statistical scope", "dependent prose and notes", "rendered affected pages"],
            "scope": "Explicit bindings only. Undeclared dependencies still require review."}, paths


def export_draft(path, output, plan, paths):
    output = output.resolve()
    if output.exists() or output == path.parent or path.parent.is_relative_to(output):
        raise ValueError("Draft output must be a new directory and must not contain source files")
    if (sha256(path) != plan["source_contract_sha256"]
            or any(sha256(p) != plan["source_document_sha256"][kind] for kind, p in paths.items())):
        raise ValueError("Source changed after preview; create a new update plan")
    output.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=".data-draft-", dir=output.parent))
    try:
        # Preserve relative asset paths, without copying work logs or old QA evidence.
        assets = set()
        for kind, document in plan["documents"].items():
            base = paths[kind].parent
            if kind == "page_spec":
                names = [s["image_file"] for s in document["slides"]]
                names += document["style"].get("tokens", {}).get("reference_images", [])
            else:
                names = [s["source_image"] for s in document["slides"] if s.get("source_image")]
                names += [e["path"] for s in document["slides"] for e in walk(s["elements"]) if e["type"] == "image"]
            for name in names:
                asset = _relative_path(base, name)
                if asset.is_file():
                    assets.add(asset)
        destination_names = {p.relative_to(path.parent) for p in paths.values()}
        if destination_names & {Path("data-bindings.json"), Path("update-plan.json")}:
            raise ValueError("Document path collides with draft metadata")
        for asset in assets:
            relative = asset.relative_to(path.parent)
            if relative in destination_names or relative in (Path("data-bindings.json"), Path("update-plan.json")):
                raise ValueError("Asset path collides with draft documents")
            target_path = stage / relative
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(asset, target_path)
        for kind, document in plan["documents"].items():
            document = copy.deepcopy(document)
            if kind == "page_spec" and plan["visible_slides"]:
                # Intentionally rejected by production Page Spec validation until reviewed.
                document["content_approved"] = False
                for slide in document["slides"]:
                    if slide["id"] in plan["visible_slides"]:
                        slide["image_status"] = "pending"
            target_path = stage / paths[kind].relative_to(path.parent)
            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        for name, data in (("data-bindings.json", plan["contract"]),
                           ("update-plan.json", {k: v for k, v in plan.items() if k not in ("documents", "contract")})):
            (stage / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        os.rename(stage, output)
    finally:
        if stage.exists():
            shutil.rmtree(stage)
    return str(output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("contract", type=Path)
    parser.add_argument("--set", dest="updates", default="{}", help='Numeric JSON input changes, e.g. {"current":125}')
    parser.add_argument("--check", action="store_true", help="Verify current declared bindings")
    parser.add_argument("--output-dir", type=Path, help="Export a separate review draft; omit to preview")
    args = parser.parse_args()
    try:
        if args.check:
            if args.output_dir or args.updates != "{}":
                raise ValueError("--check cannot be combined with updates or export")
            result = inspect(args.contract.resolve())
        else:
            plan, paths = plan_update(args.contract, json.loads(args.updates))
            result = {k: v for k, v in plan.items() if k not in ("documents", "contract")}
            if args.output_dir:
                result["draft_directory"] = export_draft(args.contract.resolve(), args.output_dir, plan, paths)
        print(json.dumps(result, ensure_ascii=True, indent=2))
        if result.get("status") == "fail":
            raise SystemExit(1)
    except (ValueError, OSError, KeyError, IndexError, TypeError, RecursionError) as error:
        parser.exit(2, f"update_data_bindings: {error}\n")


if __name__ == "__main__":
    main()
