#!/usr/bin/env python3
"""Validate Paper2PPT inputs, output access, and local runtime capabilities."""

from __future__ import annotations

import argparse
import importlib.metadata
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import sys
from typing import Any
from urllib.parse import (
    SplitResult,
    parse_qsl,
    unquote,
    urlencode,
    urlsplit,
    urlunsplit,
)


LOCAL_KINDS = {
    ".pdf": "pdf",
    ".md": "markdown",
    ".markdown": "markdown",
    ".txt": "text",
    ".pptx": "pptx-template",
}
DOI_VALUE = r"10\.\d{4,9}/\S+"
DOI = re.compile(rf"^({DOI_VALUE})$", re.IGNORECASE)
DOI_PREFIX = re.compile(rf"^doi:\s*({DOI_VALUE})$", re.IGNORECASE)
ARXIV_VALUE = r"(?:\d{4}\.\d{4,5}|[a-z-]+(?:\.[a-z-]+)?/\d{7})(?:v\d+)?"
ARXIV_ID = re.compile(rf"^({ARXIV_VALUE})$", re.IGNORECASE)
ARXIV_PREFIX = re.compile(rf"^arxiv:\s*({ARXIV_VALUE})$", re.IGNORECASE)
PMID = re.compile(r"^(\d{1,9})$")
PMID_PREFIX = re.compile(r"^pmid:\s*(\d{1,9})$", re.IGNORECASE)
PMCID = re.compile(r"^(PMC\d+)$", re.IGNORECASE)
PMCID_PREFIX = re.compile(r"^pmcid:\s*(PMC\d+)$", re.IGNORECASE)
HTTP_PREFIX = re.compile(r"^https?://", re.IGNORECASE)
SENSITIVE_QUERY_KEYS = {
    "access-token",
    "api-key",
    "auth",
    "authorization",
    "client-secret",
    "credential",
    "credentials",
    "id-token",
    "key",
    "password",
    "passwd",
    "refresh-token",
    "secret",
    "sig",
    "signature",
    "token",
    "x-amz-credential",
    "x-amz-security-token",
    "x-amz-signature",
}
URL_REDACTION_WARNING = (
    "URL credentials, sensitive query values, or fragment were redacted from "
    "the reported source."
)


def _version_at_least(version: str, minimum: str) -> bool:
    """Compare stable numeric releases without a third-party version parser."""
    version_match = re.fullmatch(r"\s*(\d+(?:\.\d+)*)(.*)\s*", version)
    minimum_match = re.fullmatch(r"(\d+(?:\.\d+)*)", minimum)
    if not version_match or not minimum_match:
        return False

    installed = tuple(int(part) for part in version_match.group(1).split("."))
    required = tuple(int(part) for part in minimum_match.group(1).split("."))
    width = max(len(installed), len(required))
    installed += (0,) * (width - len(installed))
    required += (0,) * (width - len(required))
    if installed != required:
        return installed > required

    suffix = version_match.group(2).strip().lower()
    return not suffix or suffix.startswith(".post") or suffix.startswith("+")


def _package_available(module: str, distribution: str, minimum: str) -> bool:
    """Require both an import target and qualifying distribution metadata."""
    try:
        if importlib.util.find_spec(module) is None:
            return False
        installed = importlib.metadata.version(distribution)
    except (
        ImportError,
        ModuleNotFoundError,
        ValueError,
        importlib.metadata.PackageNotFoundError,
    ):
        return False
    return _version_at_least(installed, minimum)


def detect_capabilities() -> dict[str, bool | None]:
    renderer = shutil.which("libreoffice") or shutil.which("soffice")
    return {
        "pymupdf": _package_available("pymupdf", "PyMuPDF", "1.24"),
        "pillow": _package_available("PIL", "Pillow", "10"),
        "python_pptx": _package_available("pptx", "python-pptx", "1.0.2"),
        "renderer": True if renderer else None,
    }


def _remote_result(
    kind: str, value: str, extra_warnings: list[str] | None = None
) -> tuple[dict[str, Any], list[str], list[str]]:
    warnings = list(extra_warnings or [])
    warnings.append(
        "Remote input was recognized but not fetched; resolve its availability "
        "with the active agent before analysis."
    )
    return (
        {"kind": kind, "value": value, "available": None},
        warnings,
        [],
    )


def _safe_query(query: str) -> tuple[str, bool]:
    retained: list[tuple[str, str]] = []
    redacted = False
    for key, value in parse_qsl(query, keep_blank_values=True):
        normalized_key = key.strip().lower().replace("_", "-")
        if normalized_key in SENSITIVE_QUERY_KEYS:
            redacted = True
        else:
            retained.append((key, value))
    return urlencode(retained, doseq=True, safe="/"), redacted


def _safe_url(parts: SplitResult, port: int | None, query: str) -> str:
    host = parts.hostname
    if host is None:
        return f"{parts.scheme.lower()}://[invalid-host]"
    if ":" in host:
        host = f"[{host}]"
    netloc = f"{host}:{port}" if port is not None else host
    return urlunsplit((parts.scheme.lower(), netloc, parts.path, query, ""))


def _http_source(token: str) -> tuple[dict[str, Any], list[str], list[str]]:
    try:
        parts = urlsplit(token)
        host = (parts.hostname or "").lower()
    except ValueError:
        scheme = token.split(":", 1)[0].lower()
        source = {
            "kind": "url",
            "value": f"{scheme}://[invalid-host]",
            "available": None,
        }
        return source, [], ["HTTP(S) input is not a valid URL."]

    try:
        port = parts.port
    except ValueError:
        source = {
            "kind": "url",
            "value": f"{parts.scheme.lower()}://[invalid-port]",
            "available": None,
        }
        return source, [], ["HTTP(S) URL has an invalid port."]

    safe_query, query_redacted = _safe_query(parts.query)
    redacted = bool(
        parts.username or parts.password or parts.fragment or query_redacted
    )
    extra_warnings = [URL_REDACTION_WARNING] if redacted else []

    decoded_path = unquote(parts.path).lstrip("/")
    if host in {"doi.org", "dx.doi.org"}:
        match = DOI.fullmatch(decoded_path)
        if match:
            return _remote_result("doi", match.group(1), extra_warnings)

    if host in {"arxiv.org", "www.arxiv.org"}:
        match = re.fullmatch(
            rf"(?:abs|pdf)/({ARXIV_VALUE})(?:\.pdf)?",
            decoded_path,
            re.IGNORECASE,
        )
        if match:
            return _remote_result("arxiv", match.group(1), extra_warnings)

    if not host:
        source = {
            "kind": "url",
            "value": f"{parts.scheme.lower()}://[invalid-host]",
            "available": None,
        }
        return source, [], ["HTTP(S) input is not a valid URL."]
    return _remote_result(
        "url",
        _safe_url(parts, port, safe_query),
        extra_warnings,
    )


def _explicit_remote(
    token: str,
) -> tuple[dict[str, Any], list[str], list[str]] | None:
    if HTTP_PREFIX.match(token):
        return _http_source(token)
    for pattern, kind, transform in (
        (DOI_PREFIX, "doi", lambda match: match.group(1)),
        (ARXIV_PREFIX, "arxiv", lambda match: match.group(1)),
        (PMID_PREFIX, "pmid", lambda match: match.group(1)),
        (PMCID_PREFIX, "pmcid", lambda match: match.group(1).upper()),
    ):
        match = pattern.fullmatch(token)
        if match:
            return _remote_result(kind, transform(match))
    return None


def _bare_remote(
    token: str,
) -> tuple[dict[str, Any], list[str], list[str]] | None:
    for pattern, kind, transform in (
        (DOI, "doi", lambda match: match.group(1)),
        (ARXIV_ID, "arxiv", lambda match: match.group(1)),
        (PMID, "pmid", lambda match: match.group(1)),
        (PMCID, "pmcid", lambda match: match.group(1).upper()),
    ):
        match = pattern.fullmatch(token)
        if match:
            return _remote_result(kind, transform(match))
    return None


def _existing_path(value: str) -> bool:
    try:
        return Path(value).expanduser().exists()
    except (OSError, ValueError):
        return False


def classify_source(value: str) -> tuple[dict[str, Any], list[str], list[str]]:
    token = value.strip()
    explicit = _explicit_remote(token)
    if explicit is not None:
        return explicit

    if _existing_path(value):
        return classify_local_source(value)
    if token != value and _existing_path(token):
        return classify_local_source(token)

    bare = _bare_remote(token)
    if bare is not None:
        return bare
    return classify_local_source(token)


def classify_local_source(
    value: str,
) -> tuple[dict[str, Any], list[str], list[str]]:
    path = Path(value).expanduser().resolve(strict=False)
    suffix = Path(path.name.rstrip()).suffix.lower()
    kind = LOCAL_KINDS.get(suffix, "unsupported")
    available = path.is_file()
    source = {"kind": kind, "value": str(path), "available": available}
    warnings: list[str] = []
    errors: list[str] = []

    if kind == "unsupported":
        errors.append(
            "Input is unsupported; use a PDF, Markdown/text file, PPTX template, "
            "DOI, PMID/PMCID, arXiv ID, or HTTP(S) URL."
        )
    elif not available:
        errors.append(f"Local input does not exist or is not a file: {path}")
    return source, warnings, errors


def check_output(
    value: str, *, create: bool, allow_creation: bool
) -> tuple[dict[str, Any], list[str]]:
    path = Path(value).expanduser().resolve(strict=False)
    errors: list[str] = []

    if path.exists():
        if not path.is_dir():
            errors.append(f"Output path is not a directory: {path}")
            return {"path": str(path), "writable": False}, errors
    elif create and allow_creation:
        try:
            path.mkdir(parents=True, exist_ok=False)
        except OSError as error:
            errors.append(f"Could not create output directory {path}: {error}")
            return {"path": str(path), "writable": False}, errors
    elif create:
        errors.append(
            "Output directory was not created because an earlier preflight check failed: "
            f"{path}"
        )
        return {"path": str(path), "writable": False}, errors
    else:
        errors.append(
            f"Output directory does not exist: {path}; rerun with --create-output "
            "to create it."
        )
        return {"path": str(path), "writable": False}, errors

    writable = os.access(path, os.W_OK | os.X_OK)
    if not writable:
        errors.append(f"Output directory is not writable: {path}")
    return {"path": str(path), "writable": writable}, errors


def preflight(
    input_value: str,
    output_value: str,
    *,
    create_output: bool = False,
    native_authoring: bool = False,
    native_pdf: bool = False,
) -> dict[str, Any]:
    source, warnings, errors = classify_source(input_value)
    capabilities = detect_capabilities()

    if native_authoring:
        warnings.append(
            "Native authoring was explicitly confirmed by the active agent; the "
            "capability must preserve editable PPTX objects, speaker notes, and QA."
        )
    if not capabilities["python_pptx"] and not native_authoring:
        errors.append(
            "Editable PPTX authoring is unavailable; install python-pptx 1.0.2 or newer."
        )
    local_pdf = source["kind"] == "pdf" and source["available"] is True
    if native_pdf:
        if local_pdf:
            warnings.append(
                "Native PDF extraction was explicitly confirmed by the active agent; "
                "the capability must preserve page-grounded text and figures."
            )
        else:
            warnings.append(
                "Native PDF confirmation was ignored because the input is not an "
                "available local PDF."
            )
    if local_pdf and not capabilities["pymupdf"] and not native_pdf:
        errors.append("PDF extraction is unavailable; install PyMuPDF 1.24 or newer.")
    if capabilities["renderer"] is None:
        warnings.append(
            "No LibreOffice/soffice renderer was detected; visual QA must be "
            "reported as unavailable unless the active environment provides a renderer."
        )

    output, output_errors = check_output(
        output_value,
        create=create_output,
        allow_creation=not errors,
    )
    errors.extend(output_errors)
    return {
        "ok": not errors,
        "source": source,
        "output": output,
        "capabilities": capabilities,
        "warnings": warnings,
        "errors": errors,
    }


def _human_report(result: dict[str, Any]) -> str:
    lines = [f"Paper2PPT preflight: {'OK' if result['ok'] else 'FAILED'}"]
    source = result["source"]
    lines.append(
        f"Source: {source['kind']} ({source['value']}), available={source['available']}"
    )
    output = result["output"]
    lines.append(f"Output: {output['path']}, writable={output['writable']}")
    capabilities = result["capabilities"]
    lines.append(
        "Capabilities: "
        + ", ".join(f"{name}={value}" for name, value in capabilities.items())
    )
    lines.extend(f"Warning: {warning}" for warning in result["warnings"])
    lines.extend(f"Error: {error}" for error in result["errors"])
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check a Paper2PPT source, output directory, and local capabilities."
    )
    parser.add_argument("input", metavar="INPUT")
    parser.add_argument("--output", required=True, metavar="PATH")
    parser.add_argument(
        "--create-output",
        action="store_true",
        help="Create the output directory and missing parents after other checks pass.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="as_json",
        help="Write the stable machine-readable result to stdout.",
    )
    parser.add_argument(
        "--native-authoring",
        action="store_true",
        help=(
            "Declare a confirmed native editable-PPTX, notes, and QA capability "
            "when python-pptx is unavailable."
        ),
    )
    parser.add_argument(
        "--native-pdf",
        action="store_true",
        help=(
            "Declare confirmed page-grounded native PDF extraction when PyMuPDF "
            "is unavailable for a local PDF."
        ),
    )
    args = parser.parse_args(argv)

    result = preflight(
        args.input,
        args.output,
        create_output=args.create_output,
        native_authoring=args.native_authoring,
        native_pdf=args.native_pdf,
    )
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(_human_report(result))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
