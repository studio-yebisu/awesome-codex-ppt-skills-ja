from pathlib import Path
import re

from tests.helpers import load_skill

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
WORKFLOW = ROOT / "references" / "workflow.md"
QUALITY_GATES = ROOT / "references" / "quality-gates.md"
TOOL_ROUTING = ROOT / "references" / "tool-routing.md"
EVALUATION = ROOT / "docs" / "evaluation.md"
ACTIVE_SKILL_SURFACES = (SKILL, *sorted((ROOT / "references").glob("*.md")))
BASELINE_RUN_IDS = (
    "/root/baseline_methods",
    "/root/baseline_dense",
    "/root/baseline_partial",
)
PAPER_TYPE_CONDITION = (
    "when the user has not fixed the narrative or slide plan and the task is not a narrow repair"
)


def test_skill_frontmatter_matches_shared_contract() -> None:
    metadata, body = load_skill(SKILL)
    assert set(metadata) == {"name", "description"}
    assert metadata["name"] == "paper2ppt"
    assert 1 <= len(metadata["description"]) <= 1024
    assert len(body.splitlines()) <= 300
    assert len(body.split()) <= 650


def test_skill_description_has_precise_positive_and_negative_scope() -> None:
    metadata, _ = load_skill(SKILL)
    description = metadata["description"].lower()
    for phrase in ("paper", "ppt", "journal club", "group meeting"):
        assert phrase in description
    assert "not for general-purpose slide decks" in description


def test_skill_links_only_to_existing_one_level_resources() -> None:
    _, body = load_skill(SKILL)
    links = re.findall(r"\]\((references/[^)]+)\)", body)
    assert links
    assert all(link.count("/") == 1 for link in links)
    assert all((ROOT / link).is_file() for link in links)


def test_skill_contains_required_evidence_and_completion_gates() -> None:
    text = SKILL.read_text(encoding="utf-8")
    for phrase in (
        "source sufficiency",
        "claim-to-source",
        "editable `.pptx`",
        "speaker notes",
        "Do not fabricate",
        "qa_report.md",
        "references/workflow.md",
        "references/paper-types.md",
    ):
        assert phrase in text


def test_root_skill_exposes_exact_completion_states_without_loading_references() -> None:
    text = SKILL.read_text(encoding="utf-8")
    quality_section = text.split("## Quality gates", maxsplit=1)[1].split(
        "## Output contract", maxsplit=1
    )[0]

    for state in ("`pass`", "`structurally-verified-with-disclosure`", "`blocked`"):
        assert state in quality_section


def test_active_skill_surfaces_do_not_use_legacy_identity() -> None:
    for path in ACTIVE_SKILL_SURFACES:
        text = path.read_text(encoding="utf-8").lower()
        assert "nature-paper2ppt" not in text
        assert "nature-style" not in text


def test_skill_loads_references_only_when_the_task_needs_them() -> None:
    text = SKILL.read_text(encoding="utf-8")
    assert re.search(r"Read .*workflow.* when ", text, re.IGNORECASE)
    assert re.search(r"Read .*paper-type.* when ", text, re.IGNORECASE)
    assert "narrow existing-deck audit or repair" in text
    assert "load only" in text


def test_conditional_references_cover_design_routing_and_qa() -> None:
    skill = SKILL.read_text(encoding="utf-8")
    expected = {
        "references/slide-design.md": ("figure-led", "conclusion-style title", "50/50"),
        "references/tool-routing.md": ("Codex", "Claude Code", "python-pptx"),
        "references/quality-gates.md": ("content QA", "structural QA", "visual QA"),
    }
    for relative, phrases in expected.items():
        assert relative in skill
        text = (ROOT / relative).read_text(encoding="utf-8")
        assert all(phrase in text for phrase in phrases)

    assert re.search(
        r"Read .*slide-design\.md.* only when .*designing or revising layouts.*visual defects",
        skill,
        re.IGNORECASE,
    )
    assert re.search(
        r"After preflight, read .*tool-routing\.md.* when selecting or falling back between .*authoring.*rendering tools",
        skill,
        re.IGNORECASE,
    )
    assert re.search(
        r"Read .*quality-gates\.md.* before final verification or when fixing QA failures",
        skill,
        re.IGNORECASE,
    )


def test_quality_gates_protect_figure_integrity_and_completion_states() -> None:
    text = QUALITY_GATES.read_text(encoding="utf-8")
    for phrase in (
        "correct figure, panel, and crop selection",
        "labels, axes, units, scales, legends, colorbars, and statistical marks",
        "figure-to-claim correspondence",
        "misleading exclusion",
    ):
        assert phrase in text

    completion_states, schema = text.split("## Minimal `qa_report.md`", maxsplit=1)
    identifiers = ("`pass`", "`structurally-verified-with-disclosure`", "`blocked`")
    assert all(identifier in completion_states for identifier in identifiers)
    assert "pass | structurally-verified-with-disclosure | blocked" in schema


def test_quality_gate_terminal_states_close_all_unresolved_failures() -> None:
    text = QUALITY_GATES.read_text(encoding="utf-8")
    completion = text.split("## Completion states", maxsplit=1)[1].split(
        "## Minimal `qa_report.md`", maxsplit=1
    )[0].lower()
    blocked_rules = [line for line in completion.splitlines() if "`blocked`" in line]

    for gate in ("content qa", "structural qa"):
        assert any("unresolved" in line and gate in line for line in blocked_rules)
    assert any(
        "unresolved" in line
        and "visual qa" in line
        and "renderer" in line
        and "available" in line
        for line in blocked_rules
    )

    disclosure_rules = [
        line
        for line in completion.splitlines()
        if "`structurally-verified-with-disclosure`" in line
    ]
    required = (
        "only",
        "content qa",
        "structural qa",
        "pass",
        "visual qa",
        "unavailable",
        "no renderer",
    )
    assert any(all(term in line for term in required) for line in disclosure_rules)


def test_tool_routing_describes_pixel_preserving_crops_accurately() -> None:
    text = TOOL_ROUTING.read_text(encoding="utf-8")
    assert "lossless crops" not in text
    assert "pixel-preserving crops without resampling" in text
    assert "PNG or another lossless output" in text


def test_reconstructed_diagrams_require_fully_supported_structure() -> None:
    for path in (SKILL, WORKFLOW):
        text = path.read_text(encoding="utf-8").lower()
        for phrase in (
            "every component and relationship",
            "source-supported",
            "otherwise omit",
            "original paper figure",
        ):
            assert phrase in text


def test_root_and_workflow_share_paper_type_loading_condition() -> None:
    root_text = SKILL.read_text(encoding="utf-8").lower()
    workflow_text = WORKFLOW.read_text(encoding="utf-8").lower()
    assert PAPER_TYPE_CONDITION in root_text
    assert PAPER_TYPE_CONDITION in workflow_text
    assert "[the paper-type routes](paper-types.md)" in workflow_text


def test_local_markdown_links_resolve_across_active_surfaces() -> None:
    for source in ACTIVE_SKILL_SURFACES:
        text = source.read_text(encoding="utf-8")
        for target in re.findall(r"\]\(([^)]+)\)", text):
            if target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            local_part = target.split("#", 1)[0]
            assert (source.parent / local_part).is_file(), f"Broken link in {source}: {target}"


def test_output_filename_tracks_explicit_language_requests() -> None:
    for path in (SKILL, WORKFLOW):
        text = path.read_text(encoding="utf-8")
        assert "presentation_zh.pptx" in text
        assert "presentation_<language-code>.pptx" in text
        assert "explicitly requests another language" in text


def test_evaluation_records_reproducible_baseline_evidence() -> None:
    text = EVALUATION.read_text(encoding="utf-8")
    headers = list(re.finditer(r"^## (/root/baseline_[a-z]+)$", text, re.MULTILINE))
    assert [match.group(1) for match in headers] == list(BASELINE_RUN_IDS)
    assert "UUIDs" in text
    assert "durable log paths" in text

    for index, match in enumerate(headers):
        end = headers[index + 1].start() if index + 1 < len(headers) else len(text)
        section = text[match.start():end]
        run_id = match.group(1)
        assert f"canonical_run_id: `{run_id}`" in section
        assert "fork_turns: `none`" in section
        assert "不要读取或调用任何 Paper2PPT、nature-paper2ppt 或论文转幻灯片 Skill。" in section

        prompt = re.search(
            r"\*\*Exact user prompt\*\*\n\n```text\n(.+?)\n```",
            section,
            re.DOTALL,
        )
        raw_response = re.search(
            r"\*\*Raw response \(verbatim\)\*\*\n\n```text\n(.+?)\n```",
            section,
            re.DOTALL,
        )
        assert prompt and len(prompt.group(1).strip()) >= 50
        assert raw_response and len(raw_response.group(1).strip()) >= 500
        assert "**Rationalization**" in section

    assert text.count(
        "No explicit rationalization was emitted; extra deliverables were execution choices."
    ) >= 2
