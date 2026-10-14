#!/usr/bin/env python3
"""Validate Paper2PPT repository identity, packaging, and trigger fixtures."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from typing import Any, Iterable
from urllib.parse import unquote

import yaml


PLUGIN_SKILL = Path("plugins/paper2ppt/skills/paper2ppt")
RUNTIME_HELPERS = ("preflight.py", "inspect_pptx.py")
PLUGIN_URL = "https://github.com/wp-a/paper2ppt"
CLAUDE_PLUGIN_SCHEMA = "https://anthropic.com/claude-code/plugin.schema.json"
CLAUDE_MARKETPLACE_SCHEMA = (
    "https://anthropic.com/claude-code/marketplace.schema.json"
)
FORBIDDEN_PLUGIN_COMPONENTS = {"agents", "apps", "hooks", "mcpServers", "settings"}
TRIGGER_KEYS = {"id", "query", "should_trigger", "category"}
MIN_TRIGGER_CASES_PER_SIDE = 10
MIN_TRIGGER_CATEGORIES_PER_SIDE = 10
LEGACY_PRODUCT_PATTERN = re.compile(r"nature-paper2ppt", re.IGNORECASE)
NATURE_STYLE_PATTERN = re.compile(
    r"\bnature(?:[\s\-\u2010-\u2015]style\b|\s*风格)",
    re.IGNORECASE,
)
ALLOWED_NATURE_STYLE_CONTEXT = re.compile(
    r"^[\s:：,，-]*(?:citations?|references?|bibliograph(?:y|ies)|"
    r"(?:的)?(?:引用|参考文献|参考书目|引文))",
    re.IGNORECASE,
)
BRANDING_COORDINATOR = re.compile(
    r"\b(?:and|plus|with|as\s+well\s+as|along\s+with|"
    r"(?:should\s+)?(?:define|govern)|apply\s+to|extend\s+to)\b|"
    r"[,;，；]|以及|同时|和|与|及|并",
    re.IGNORECASE,
)
BRANDING_PREDICATE = re.compile(
    r"\b(?:(?:slides?|decks?|presentations?)\s+"
    r"(?:design|layout|theme|template|narrative|style)|"
    r"design|layout|theme|template|narrative|style|default)\b|"
    r"(?:幻灯片|演示文稿|演示|汇报)(?:的)?(?:设计|排版|版式|主题|模板|叙事)|默认",
    re.IGNORECASE,
)
DEFAULT_BRANDING_PREFIX = re.compile(r"\bdefault\b|默认", re.IGNORECASE)
CONTROLLED_FILES = (
    Path("VERSION"),
    Path("SKILL.md"),
    Path(".agents/plugins/marketplace.json"),
    Path(".claude-plugin/marketplace.json"),
    Path("plugins/paper2ppt/.codex-plugin/plugin.json"),
    Path("plugins/paper2ppt/.claude-plugin/plugin.json"),
    PLUGIN_SKILL / "SKILL.md",
    PLUGIN_SKILL / "agents/openai.yaml",
    Path("scripts/preflight.py"),
    Path("scripts/inspect_pptx.py"),
    Path("tests/trigger_cases.json"),
)
CONTROLLED_TREES = (
    Path("references"),
    PLUGIN_SKILL / "references",
    PLUGIN_SKILL / "scripts",
)


def finding(code: str, path: Path | str, message: str) -> dict[str, str]:
    """Create a stable validation finding for human and JSON reports."""
    return {"code": code, "path": Path(path).as_posix(), "message": message}


def _read_text(
    root: Path, relative: Path
) -> tuple[str | None, list[dict[str, str]]]:
    path = root / relative
    try:
        return path.read_text(encoding="utf-8"), []
    except UnicodeError:
        return None, [finding("file.unreadable", relative, "file is not valid UTF-8")]
    except OSError as error:
        message = error.strerror or type(error).__name__
        return None, [finding("file.unreadable", relative, message)]


def _read_json(root: Path, relative: Path) -> tuple[Any | None, list[dict[str, str]]]:
    text, errors = _read_text(root, relative)
    if text is None:
        return None, errors
    try:
        return json.loads(text), []
    except json.JSONDecodeError as error:
        return None, [finding("json.malformed", relative, str(error))]


def _parse_skill(
    root: Path, relative: Path
) -> tuple[dict[str, Any] | None, str, list[dict[str, str]]]:
    text, errors = _read_text(root, relative)
    if text is None:
        return None, "", errors
    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.DOTALL)
    if not match:
        return None, text, [
            finding("skill.frontmatter", relative, "missing or malformed YAML frontmatter")
        ]
    try:
        metadata = yaml.safe_load(match.group(1))
    except yaml.YAMLError as error:
        return None, text[match.end() :], [
            finding("skill.frontmatter", relative, f"invalid YAML frontmatter: {error}")
        ]
    if not isinstance(metadata, dict):
        return None, text[match.end() :], [
            finding("skill.frontmatter", relative, "frontmatter must be a mapping")
        ]
    return metadata, text[match.end() :], []


def _unsafe_controlled_component(root: Path, relative: Path) -> Path | None:
    boundary = root.resolve(strict=False)
    if root.is_symlink():
        return Path(".")
    current = root
    traversed = Path()
    for part in relative.parts:
        current /= part
        traversed /= part
        if current.is_symlink():
            return traversed
    resolved = current.resolve(strict=False)
    if resolved != boundary and not resolved.is_relative_to(boundary):
        return relative
    return None


def _controlled_tree_symlinks(root: Path, relative: Path) -> set[Path]:
    unsafe: set[Path] = set()
    component = _unsafe_controlled_component(root, relative)
    if component is not None:
        unsafe.add(component)
        return unsafe
    directory = root / relative
    if not directory.is_dir():
        return unsafe
    try:
        children = sorted(directory.iterdir())
    except OSError:
        return unsafe
    for child in children:
        child_relative = child.relative_to(root)
        component = _unsafe_controlled_component(root, child_relative)
        if component is not None:
            unsafe.add(component)
        elif child.is_dir():
            unsafe.update(_controlled_tree_symlinks(root, child_relative))
    return unsafe


def validate_controlled_paths(root: Path) -> list[dict[str, str]]:
    """Reject controlled paths that use symlinks or resolve outside the repo."""
    unsafe: set[Path] = set()
    if root.is_symlink():
        unsafe.add(Path("."))
    else:
        files = list(CONTROLLED_FILES)
        try:
            files.extend(
                child.relative_to(root)
                for child in root.iterdir()
                if child.name.startswith("README") and child.suffix == ".md"
            )
        except OSError:
            pass
        for relative in files:
            component = _unsafe_controlled_component(root, relative)
            if component is not None:
                unsafe.add(component)
        for relative in CONTROLLED_TREES:
            unsafe.update(_controlled_tree_symlinks(root, relative))
    return [
        finding(
            "path.unsafe",
            relative,
            "controlled path uses a symlink component or resolves outside the repository",
        )
        for relative in sorted(unsafe)
    ]


def validate_skill_frontmatter(root: Path) -> list[dict[str, str]]:
    """Validate the shared Codex/Claude metadata subset on both Skill copies."""
    errors: list[dict[str, str]] = []
    for relative in (Path("SKILL.md"), PLUGIN_SKILL / "SKILL.md"):
        metadata, _, parse_errors = _parse_skill(root, relative)
        errors.extend(parse_errors)
        if metadata is None:
            continue
        if set(metadata) != {"name", "description"}:
            errors.append(
                finding(
                    "skill.frontmatter-fields",
                    relative,
                    "frontmatter must contain only name and description",
                )
            )
        if metadata.get("name") != "paper2ppt":
            errors.append(
                finding("skill.name", relative, "Skill name must be paper2ppt")
            )
        description = metadata.get("description")
        if not isinstance(description, str):
            errors.append(
                finding("skill.description", relative, "description must be a string")
            )
            continue
        normalized = " ".join(description.split())
        trigger_only = normalized.lower().startswith("use when ")
        negative_boundary = bool(re.search(r"\bnot for\b", normalized, re.IGNORECASE))
        process_summary = bool(
            re.search(r"\b(?:first|then|workflow|steps?)\b", normalized, re.IGNORECASE)
            or re.search(
                r"\b(?:it|this skill|the skill|paper2ppt)\s+"
                r"(?:extracts?|analy[sz]es?|builds?|creates?|generates?|"
                r"validates?|renders?|checks?|selects?|writes?)\b",
                normalized,
                re.IGNORECASE,
            )
        )
        if not (
            1 <= len(normalized) <= 1024
            and trigger_only
            and negative_boundary
            and not process_summary
        ):
            errors.append(
                finding(
                    "skill.description",
                    relative,
                    "description must be 1-1024 characters, start with 'Use when', "
                    "include a 'Not for' boundary, and contain no workflow summary",
                )
            )
    return errors


def _active_markdown_files(root: Path) -> list[Path]:
    files = [Path("SKILL.md")]
    files.extend(path.relative_to(root) for path in sorted(root.glob("README*.md")))
    files.extend(
        path.relative_to(root) for path in sorted((root / "references").rglob("*.md"))
    )
    files.append(PLUGIN_SKILL / "SKILL.md")
    files.extend(
        path.relative_to(root)
        for path in sorted((root / PLUGIN_SKILL / "references").rglob("*.md"))
    )
    return [relative for relative in files if (root / relative).is_file()]


def _blank_range(characters: list[str], start: int, end: int) -> None:
    for index in range(start, end):
        if characters[index] not in "\r\n":
            characters[index] = " "


def _mask_markdown_code(text: str) -> str:
    """Mask fenced blocks and matched inline code spans while preserving offsets."""
    characters = list(text)
    offset = 0
    fence_character: str | None = None
    fence_length = 0
    for line in text.splitlines(keepends=True):
        line_without_ending = line.rstrip("\r\n")
        if fence_character is None:
            opener = re.match(r"^ {0,3}(`{3,}|~{3,})", line_without_ending)
            if opener:
                marker = opener.group(1)
                fence_character = marker[0]
                fence_length = len(marker)
                _blank_range(characters, offset, offset + len(line))
        else:
            _blank_range(characters, offset, offset + len(line))
            closer = re.match(
                rf"^ {{0,3}}{re.escape(fence_character)}{{{fence_length},}}\s*$",
                line_without_ending,
            )
            if closer:
                fence_character = None
                fence_length = 0
        offset += len(line)

    masked = "".join(characters)
    index = 0
    while index < len(masked):
        if masked[index] != "`":
            index += 1
            continue
        run_end = index
        while run_end < len(masked) and masked[run_end] == "`":
            run_end += 1
        run_length = run_end - index
        candidate = run_end
        closing_end: int | None = None
        while candidate < len(masked):
            candidate = masked.find("`", candidate)
            if candidate < 0:
                break
            candidate_end = candidate
            while candidate_end < len(masked) and masked[candidate_end] == "`":
                candidate_end += 1
            if candidate_end - candidate == run_length:
                closing_end = candidate_end
                break
            candidate = candidate_end
        if closing_end is None:
            index = run_end
            continue
        _blank_range(characters, index, closing_end)
        masked = "".join(characters)
        index = closing_end
    return "".join(characters)


def _markdown_link_targets(text: str) -> list[str]:
    """Return inline-link payloads while respecting escapes and balanced parentheses."""
    targets: list[str] = []
    index = 0
    while index < len(text) - 1:
        start = text.find("](", index)
        if start < 0:
            break
        backslashes = len(text[:start]) - len(text[:start].rstrip("\\"))
        escaped = backslashes % 2 == 1
        if escaped:
            index = start + 2
            continue
        cursor = start + 2
        depth = 1
        angle = False
        escaped_character = False
        while cursor < len(text):
            character = text[cursor]
            if escaped_character:
                escaped_character = False
            elif character == "\\":
                escaped_character = True
            elif character == "<" and depth == 1:
                angle = True
            elif character == ">" and angle:
                angle = False
            elif not angle and character == "(":
                depth += 1
            elif not angle and character == ")":
                depth -= 1
                if depth == 0:
                    targets.append(text[start + 2 : cursor])
                    index = cursor + 1
                    break
            cursor += 1
        else:
            index = start + 2
    return targets


def _unescape_markdown(value: str) -> str:
    result: list[str] = []
    escaped = False
    for character in value:
        if escaped:
            result.append(character)
            escaped = False
        elif character == "\\":
            escaped = True
        else:
            result.append(character)
    if escaped:
        result.append("\\")
    return "".join(result)


def _local_markdown_target(raw_target: str) -> str | None:
    target = raw_target.strip()
    if target.startswith("<"):
        end = target.find(">", 1)
        if end < 0:
            return None
        target = target[1:end]
    else:
        cursor = 0
        escaped = False
        while cursor < len(target):
            character = target[cursor]
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character.isspace():
                break
            cursor += 1
        target = target[:cursor]
    if not target or target.startswith("#"):
        return None
    if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", target):
        return None
    target = target.split("#", 1)[0].split("?", 1)[0]
    return unquote(_unescape_markdown(target)) or None


def validate_markdown_references(root: Path) -> list[dict[str, str]]:
    """Check relative links in active Markdown without traversing historical docs."""
    errors: list[dict[str, str]] = []
    resolved_root = root.resolve()
    for source in _active_markdown_files(root):
        text, read_errors = _read_text(root, source)
        errors.extend(read_errors)
        if text is None:
            continue
        for raw_target in _markdown_link_targets(_mask_markdown_code(text)):
            local_target = _local_markdown_target(raw_target)
            if local_target is None:
                continue
            destination = (root / source.parent / local_target).resolve(strict=False)
            if not destination.is_relative_to(resolved_root) or not destination.is_file():
                errors.append(
                    finding(
                        "markdown.missing-reference",
                        source,
                        f"relative Markdown target does not exist: {local_target}",
                    )
                )
    return errors


def _file_set(directory: Path) -> set[Path]:
    if not directory.is_dir():
        return set()
    return {path.relative_to(directory) for path in directory.rglob("*") if path.is_file()}


def _compare_mirror_file(
    root: Path, canonical: Path, packaged: Path
) -> list[dict[str, str]]:
    canonical_path = root / canonical
    packaged_path = root / packaged
    try:
        matches = (
            canonical_path.is_file()
            and packaged_path.is_file()
            and canonical_path.read_bytes() == packaged_path.read_bytes()
        )
    except OSError:
        matches = False
    if matches:
        return []
    return [
        finding(
            "mirror.drift",
            packaged,
            f"packaged file must exactly mirror {canonical.as_posix()}",
        )
    ]


def validate_plugin_mirror(root: Path) -> list[dict[str, str]]:
    """Check canonical Skill, reference, and runtime-helper package mirrors."""
    errors = _compare_mirror_file(root, Path("SKILL.md"), PLUGIN_SKILL / "SKILL.md")

    canonical_references = root / "references"
    packaged_references = root / PLUGIN_SKILL / "references"
    canonical_files = _file_set(canonical_references)
    packaged_files = _file_set(packaged_references)
    if canonical_files != packaged_files:
        errors.append(
            finding(
                "mirror.drift",
                PLUGIN_SKILL / "references",
                "packaged reference file set differs from canonical references",
            )
        )
    for relative in sorted(canonical_files & packaged_files):
        errors.extend(
            _compare_mirror_file(
                root,
                Path("references") / relative,
                PLUGIN_SKILL / "references" / relative,
            )
        )

    expected_scripts = {Path(name) for name in RUNTIME_HELPERS}
    packaged_scripts = _file_set(root / PLUGIN_SKILL / "scripts")
    if packaged_scripts != expected_scripts:
        errors.append(
            finding(
                "mirror.drift",
                PLUGIN_SKILL / "scripts",
                "packaged runtime script set must contain exactly the runtime helpers",
            )
        )
    for name in RUNTIME_HELPERS:
        errors.extend(
            _compare_mirror_file(
                root,
                Path("scripts") / name,
                PLUGIN_SKILL / "scripts" / name,
            )
        )
    return errors


def _plugin_entry(data: Any) -> dict[str, Any] | None:
    if not isinstance(data, dict) or not isinstance(data.get("plugins"), list):
        return None
    matches = [
        entry
        for entry in data["plugins"]
        if isinstance(entry, dict) and entry.get("name") == "paper2ppt"
    ]
    return matches[0] if len(matches) == 1 else None


def _version_value(root: Path) -> str | None:
    try:
        value = (root / "VERSION").read_text(encoding="utf-8").strip()
    except (OSError, UnicodeError):
        return None
    return value if re.fullmatch(r"\d+\.\d+\.\d+", value) else None


def validate_release_metadata(root: Path) -> list[dict[str, str]]:
    """Validate the canonical release version file."""
    errors: list[dict[str, str]] = []
    version_text, version_errors = _read_text(root, Path("VERSION"))
    errors.extend(version_errors)
    if version_text is None:
        return errors
    version = version_text.strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        errors.append(
            finding("release.version", "VERSION", "VERSION must be a semantic x.y.z release")
        )
    return errors


def _contains_chinese(value: str) -> bool:
    return _chinese_character_count(value) > 0


def _chinese_character_count(value: str) -> int:
    return sum("\u4e00" <= character <= "\u9fff" for character in value)


def _validate_codex_plugin_interface(
    interface: Any, relative: Path
) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    if not isinstance(interface, dict):
        return [
            finding(
                "plugin.interface",
                relative,
                "Codex manifest interface must be a mapping",
            )
        ]
    if interface.get("displayName") != "Paper2PPT":
        errors.append(
            finding(
                "plugin.interface-display",
                relative,
                "Codex interface displayName must be Paper2PPT",
            )
        )
    short_description = interface.get("shortDescription")
    if not (
        isinstance(short_description, str)
        and 1 <= len(short_description.strip()) <= 64
        and _contains_chinese(short_description)
    ):
        errors.append(
            finding(
                "plugin.interface-short-description",
                relative,
                "Codex shortDescription must be nonempty, Chinese-first, and at most 64 characters",
            )
        )
    long_description = interface.get("longDescription")
    if not _nonempty_string(long_description):
        errors.append(
            finding(
                "plugin.interface-long-description",
                relative,
                "Codex longDescription must be a nonempty string",
            )
        )
    if not _nonempty_string(interface.get("developerName")):
        errors.append(
            finding(
                "plugin.interface-developer",
                relative,
                "Codex developerName must be a nonempty string",
            )
        )
    if not _nonempty_string(interface.get("category")):
        errors.append(
            finding(
                "plugin.interface-category",
                relative,
                "Codex category must be a nonempty string",
            )
        )
    capabilities = interface.get("capabilities")
    if not (
        isinstance(capabilities, list)
        and bool(capabilities)
        and all(_nonempty_string(capability) for capability in capabilities)
    ):
        errors.append(
            finding(
                "plugin.interface-capabilities",
                relative,
                "Codex capabilities must be a nonempty array of nonempty strings",
            )
        )
    if interface.get("websiteURL") != PLUGIN_URL:
        errors.append(
            finding(
                "plugin.interface-website",
                relative,
                f"Codex websiteURL must be {PLUGIN_URL}",
            )
        )
    default_prompts = interface.get("defaultPrompt")
    prompt_contract = (
        isinstance(default_prompts, list)
        and 1 <= len(default_prompts) <= 3
        and all(
            isinstance(prompt, str)
            and 1 <= len(prompt.strip()) <= 128
            and _contains_chinese(prompt)
            and "Paper2PPT" in prompt
            for prompt in default_prompts
        )
    )
    if not prompt_contract:
        errors.append(
            finding(
                "plugin.interface-default-prompt",
                relative,
                "Codex defaultPrompt must contain 1-3 Chinese-first Paper2PPT prompts of at most 128 characters",
            )
        )
    return errors


def validate_plugin_metadata(root: Path) -> list[dict[str, str]]:
    """Validate both plugin manifests against the approved package contract."""
    errors: list[dict[str, str]] = []
    version = _version_value(root)
    manifests = (
        (
            Path("plugins/paper2ppt/.codex-plugin/plugin.json"),
            "./skills/",
            None,
        ),
        (
            Path("plugins/paper2ppt/.claude-plugin/plugin.json"),
            None,
            CLAUDE_PLUGIN_SCHEMA,
        ),
    )
    for relative, expected_skills, expected_schema in manifests:
        data, json_errors = _read_json(root, relative)
        errors.extend(json_errors)
        if json_errors:
            continue
        if not isinstance(data, dict):
            errors.append(
                finding(
                    "plugin.manifest",
                    relative,
                    "plugin manifest root must be a JSON object",
                )
            )
            continue
        if data.get("name") != "paper2ppt":
            errors.append(finding("release.identity", relative, "manifest name must be paper2ppt"))
        if version is not None and data.get("version") != version:
            errors.append(
                finding("release.version-drift", relative, "manifest version must match VERSION")
            )
        if data.get("license") != "MIT":
            errors.append(finding("release.license", relative, "manifest license must be MIT"))
        if not _nonempty_string(data.get("description")):
            errors.append(
                finding(
                    "plugin.description",
                    relative,
                    "manifest description must be a nonempty string",
                )
            )
        author = data.get("author")
        if not (
            isinstance(author, dict) and _nonempty_string(author.get("name"))
        ):
            errors.append(
                finding(
                    "plugin.author",
                    relative,
                    "manifest author.name must be a nonempty string",
                )
            )
        if expected_skills is None and "skills" in data:
            errors.append(
                finding(
                    "plugin.skills",
                    relative,
                    "Claude manifest must use default skills/ discovery and omit skills",
                )
            )
        elif expected_skills is not None and data.get("skills") != expected_skills:
            errors.append(
                finding(
                    "plugin.skills",
                    relative,
                    f"manifest skills must equal {expected_skills!r}",
                )
            )
        if data.get("homepage") != PLUGIN_URL or data.get("repository") != PLUGIN_URL:
            errors.append(
                finding(
                    "plugin.url",
                    relative,
                    f"homepage and repository must both be {PLUGIN_URL}",
                )
            )
        if expected_schema is not None and data.get("$schema") != expected_schema:
            errors.append(
                finding(
                    "plugin.schema",
                    relative,
                    f"Claude plugin $schema must be {expected_schema}",
                )
            )
        forbidden = sorted(FORBIDDEN_PLUGIN_COMPONENTS & set(data))
        if forbidden:
            errors.append(
                finding(
                    "plugin.components",
                    relative,
                    f"unused plugin components are forbidden: {', '.join(forbidden)}",
                )
            )
        if relative.name == "plugin.json" and ".codex-plugin" in relative.parts:
            errors.extend(_validate_codex_plugin_interface(data.get("interface"), relative))
    return errors


def validate_marketplace_metadata(root: Path) -> list[dict[str, str]]:
    """Validate Codex and Claude marketplace discovery metadata."""
    errors: list[dict[str, str]] = []
    version = _version_value(root)

    codex_path = Path(".agents/plugins/marketplace.json")
    codex_data, json_errors = _read_json(root, codex_path)
    errors.extend(json_errors)
    codex_entry = None if json_errors else _plugin_entry(codex_data)
    if not json_errors:
        if codex_entry is None:
            errors.append(
                finding("marketplace.entry", codex_path, "expected one paper2ppt plugin entry")
            )
        elif codex_entry.get("source") != {
            "source": "local",
            "path": "./plugins/paper2ppt",
        }:
            errors.append(
                finding(
                    "marketplace.source",
                    codex_path,
                    "Codex source must point to ./plugins/paper2ppt",
                )
            )
    if codex_entry is not None:
        if codex_entry.get("policy") != {
            "installation": "AVAILABLE",
            "authentication": "ON_INSTALL",
        }:
            errors.append(
                finding(
                    "marketplace.policy",
                    codex_path,
                    "Codex policy must use AVAILABLE installation and ON_INSTALL authentication",
                )
            )
        if codex_entry.get("category") != "Research":
            errors.append(
                finding(
                    "marketplace.category",
                    codex_path,
                    "Codex marketplace category must be Research",
                )
            )

    claude_path = Path(".claude-plugin/marketplace.json")
    claude_data, json_errors = _read_json(root, claude_path)
    errors.extend(json_errors)
    if not json_errors:
        if (
            isinstance(claude_data, dict)
            and claude_data.get("$schema") != CLAUDE_MARKETPLACE_SCHEMA
        ):
            errors.append(
                finding(
                    "marketplace.schema",
                    claude_path,
                    f"Claude marketplace $schema must be {CLAUDE_MARKETPLACE_SCHEMA}",
                )
            )
    claude_entry = None if json_errors else _plugin_entry(claude_data)
    if not json_errors and claude_entry is None:
        errors.append(
            finding("marketplace.entry", claude_path, "expected one paper2ppt plugin entry")
        )
    elif claude_entry is not None:
        if claude_entry.get("source") != "./plugins/paper2ppt":
            errors.append(
                finding("marketplace.source", claude_path, "Claude source must point to ./plugins/paper2ppt")
            )
        if version is not None and claude_entry.get("version") != version:
            errors.append(
                finding("release.version-drift", claude_path, "marketplace version must match VERSION")
            )
    return errors


def validate_codex_ui_metadata(root: Path) -> list[dict[str, str]]:
    """Validate packaged openai.yaml discovery metadata without unsafe YAML loading."""
    relative = PLUGIN_SKILL / "agents/openai.yaml"
    text, read_errors = _read_text(root, relative)
    if text is None:
        return [
            finding("codex-ui.yaml", relative, error["message"])
            for error in read_errors
        ]
    try:
        metadata = yaml.safe_load(text)
    except yaml.YAMLError as error:
        return [finding("codex-ui.yaml", relative, f"invalid YAML: {error}")]
    if not isinstance(metadata, dict):
        return [finding("codex-ui.yaml", relative, "metadata must be a mapping")]

    errors: list[dict[str, str]] = []
    interface = metadata.get("interface")
    if not isinstance(interface, dict):
        interface = {}
        errors.append(
            finding("codex-ui.yaml", relative, "interface must be a mapping")
        )
    if interface.get("display_name") != "Paper2PPT":
        errors.append(
            finding(
                "codex-ui.display-name",
                relative,
                "display_name must be Paper2PPT",
            )
        )
    short_description = interface.get("short_description")
    if not (
        isinstance(short_description, str)
        and 25 <= len(short_description.strip()) <= 64
    ):
        errors.append(
            finding(
                "codex-ui.short-description",
                relative,
                "short_description must contain 25-64 characters",
            )
        )
    default_prompt = interface.get("default_prompt")
    if not (
        isinstance(default_prompt, str)
        and "$paper2ppt" in default_prompt
        and _chinese_character_count(default_prompt) >= 8
    ):
        errors.append(
            finding(
                "codex-ui.default-prompt",
                relative,
                "default_prompt must be Chinese-first and explicitly invoke $paper2ppt",
            )
        )
    policy = metadata.get("policy")
    if not (
        isinstance(policy, dict)
        and policy.get("allow_implicit_invocation") is True
    ):
        errors.append(
            finding(
                "codex-ui.policy",
                relative,
                "allow_implicit_invocation must be true",
            )
        )
    if "dependencies" in metadata:
        errors.append(
            finding(
                "codex-ui.dependencies",
                relative,
                "dependencies are not declared for Paper2PPT",
            )
        )
    return errors


def _identity_surfaces(root: Path) -> list[Path]:
    files: list[Path] = [Path("SKILL.md")]
    files.extend(path.relative_to(root) for path in sorted(root.glob("README*.md")))
    files.extend(
        path.relative_to(root) for path in sorted((root / "references").rglob("*.md"))
    )
    files.extend(
        (
            Path(".agents/plugins/marketplace.json"),
            Path(".claude-plugin/marketplace.json"),
            Path("plugins/paper2ppt/.codex-plugin/plugin.json"),
            Path("plugins/paper2ppt/.claude-plugin/plugin.json"),
            PLUGIN_SKILL / "SKILL.md",
            PLUGIN_SKILL / "agents/openai.yaml",
        )
    )
    files.extend(
        path.relative_to(root)
        for path in sorted((root / PLUGIN_SKILL / "references").rglob("*.md"))
    )
    return [relative for relative in files if (root / relative).is_file()]


def _legacy_branding_match(text: str) -> str | None:
    product = LEGACY_PRODUCT_PATTERN.search(text)
    if product:
        return product.group(0)
    for style in NATURE_STYLE_PATTERN.finditer(text):
        following_context = text[style.end() :]
        citation = ALLOWED_NATURE_STYLE_CONTEXT.match(following_context)
        if citation:
            sentence_start = max(
                text.rfind(separator, 0, style.start())
                for separator in ("\n", ".", "!", "?", "。", "！", "？")
            )
            prefix = text[sentence_start + 1 : style.start()]
            tail = following_context[citation.end() :]
            tail = re.split(r"[\n.!?。！？]", tail, maxsplit=1)[0]
            propagated_branding = any(
                BRANDING_PREDICATE.search(tail[connector.end() :])
                for connector in BRANDING_COORDINATOR.finditer(tail)
            )
            if not DEFAULT_BRANDING_PREFIX.search(prefix) and not propagated_branding:
                continue
        return style.group(0)
    return None


def validate_active_identity(root: Path) -> list[dict[str, str]]:
    """Reject the retired product name and branded default style on active surfaces."""
    errors: list[dict[str, str]] = []
    for path in _identity_surfaces(root):
        text, read_errors = _read_text(root, path)
        errors.extend(read_errors)
        if text is None:
            continue
        legacy_branding = _legacy_branding_match(text)
        if legacy_branding:
            errors.append(
                finding(
                    "identity.legacy",
                    path,
                    f"forbidden legacy branding: {legacy_branding}",
                )
            )
    return errors


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _duplicate_values(cases: Iterable[dict[str, Any]], key: str) -> set[str]:
    values = [case.get(key) for case in cases]
    strings = [value.strip() for value in values if _nonempty_string(value)]
    return {value for value in strings if strings.count(value) > 1}


def validate_trigger_cases(root: Path) -> list[dict[str, str]]:
    """Validate the deterministic discovery-boundary fixture contract."""
    relative = Path("tests/trigger_cases.json")
    data, json_errors = _read_json(root, relative)
    errors = list(json_errors)
    if not isinstance(data, list):
        if not json_errors:
            errors.append(finding("triggers.schema", relative, "trigger fixture must be a JSON array"))
        return errors

    cases = [case for case in data if isinstance(case, dict)]
    malformed = len(cases) != len(data)
    for case in cases:
        if (
            set(case) != TRIGGER_KEYS
            or not _nonempty_string(case.get("id"))
            or not _nonempty_string(case.get("query"))
            or type(case.get("should_trigger")) is not bool
            or not _nonempty_string(case.get("category"))
        ):
            malformed = True
    if malformed:
        errors.append(
            finding(
                "triggers.schema",
                relative,
                "each case must use exactly id/query/should_trigger/category with valid types",
            )
        )

    positive = [case for case in cases if case.get("should_trigger") is True]
    negative = [case for case in cases if case.get("should_trigger") is False]
    positive_categories = {
        case["category"].strip() for case in positive if _nonempty_string(case.get("category"))
    }
    negative_categories = {
        case["category"].strip() for case in negative if _nonempty_string(case.get("category"))
    }
    if len(positive) < MIN_TRIGGER_CASES_PER_SIDE or len(negative) < MIN_TRIGGER_CASES_PER_SIDE:
        errors.append(
            finding(
                "triggers.count",
                relative,
                f"need at least {MIN_TRIGGER_CASES_PER_SIDE} positive and negative cases",
            )
        )
    if (
        len(positive_categories) < MIN_TRIGGER_CATEGORIES_PER_SIDE
        or len(negative_categories) < MIN_TRIGGER_CATEGORIES_PER_SIDE
    ):
        errors.append(
            finding(
                "triggers.categories",
                relative,
                f"need at least {MIN_TRIGGER_CATEGORIES_PER_SIDE} categories on each side",
            )
        )
    if _duplicate_values(cases, "id"):
        errors.append(finding("triggers.duplicate-id", relative, "trigger ids must be unique"))
    if _duplicate_values(cases, "query"):
        errors.append(
            finding("triggers.duplicate-query", relative, "trigger queries must be unique")
        )
    return errors


def validate_repository(root: Path) -> list[dict[str, str]]:
    """Run every repository gate without modifying the supplied root."""
    root = root.absolute()
    unsafe_paths = validate_controlled_paths(root)
    if unsafe_paths:
        return sorted(
            unsafe_paths,
            key=lambda item: (item["code"], item["path"], item["message"]),
        )
    validators = (
        validate_skill_frontmatter,
        validate_markdown_references,
        validate_plugin_mirror,
        validate_release_metadata,
        validate_plugin_metadata,
        validate_marketplace_metadata,
        validate_codex_ui_metadata,
        validate_active_identity,
        validate_trigger_cases,
    )
    errors: list[dict[str, str]] = []
    for validator in validators:
        errors.extend(validator(root))
    return sorted(errors, key=lambda item: (item["code"], item["path"], item["message"]))


def _print_human(errors: list[dict[str, str]]) -> None:
    if not errors:
        print("Paper2PPT repository validation: PASS")
        return
    print(f"Paper2PPT repository validation: FAIL ({len(errors)} errors)")
    for error in errors:
        print(f"- [{error['code']}] {error['path']}: {error['message']}")


def main(argv: list[str] | None = None, *, root: Path | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the Paper2PPT repository.")
    parser.add_argument("--json", action="store_true", help="Print a machine-readable report.")
    args = parser.parse_args(argv)
    validation_root = root if root is not None else Path(__file__).resolve().parents[1]
    errors = validate_repository(validation_root)
    if args.json:
        print(json.dumps({"ok": not errors, "errors": errors}, ensure_ascii=False, indent=2))
    else:
        _print_human(errors)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
