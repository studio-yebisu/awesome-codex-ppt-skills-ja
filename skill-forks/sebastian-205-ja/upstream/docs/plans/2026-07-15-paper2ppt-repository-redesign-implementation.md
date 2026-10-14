# Paper2PPT Repository Redesign Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Rebuild and release `wp-a/nature-paper2ppt` as the Chinese-first, evidence-grounded, Codex- and Claude Code-compatible `wp-a/paper2ppt` Agent Skill.

**Architecture:** Keep `SKILL.md` as the canonical Agent Skills entry point and move conditional guidance into one-level-deep references. Bundle deterministic Python utilities for preflight and PPTX QA, mirror the canonical Skill into Codex and Claude plugin packages, and enforce synchronization with tests and CI. The repository remains an agent workflow rather than a standalone LLM service.

**Tech Stack:** Agent Skills Markdown/YAML, Python 3.10+, pytest, PyYAML, python-pptx 1.0.2, PyMuPDF, Pillow, JSON plugin manifests, GitHub Actions, Codex and Claude Code plugin loaders.

---

## Preconditions

- Work in `/Users/wangpeng/.config/superpowers/worktrees/nature-paper2ppt/paper2ppt-repository-redesign` on branch `feature/paper2ppt-repository-redesign`.
- Read `docs/plans/2026-07-15-paper2ppt-repository-redesign-design.md` before editing.
- Invoke `skill-creator` and `writing-skills` before changing Skill behavior.
- Invoke `plugin-creator` before writing Codex plugin metadata.
- Use `test-driven-development` for scripts and validation behavior.
- Use `presentations` for the example deck and its render-and-review loop.
- Use `requesting-code-review` and `verification-before-completion` before integration.
- Use `finishing-a-development-branch` after all verification passes.

### Task 1: Establish the repository test harness and release identity

**Files:**

- Create: `.gitignore`
- Create: `VERSION`
- Create: `LICENSE`
- Create: `requirements-dev.txt`
- Create: `pytest.ini`
- Create: `tests/__init__.py`
- Create: `tests/helpers.py`
- Create: `tests/test_repository.py`

**Step 1: Write the failing repository metadata test**

Create `tests/test_repository.py`:

```python
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_release_metadata_exists() -> None:
    assert (ROOT / "VERSION").read_text(encoding="utf-8").strip() == "0.1.0"
    assert "MIT License" in (ROOT / "LICENSE").read_text(encoding="utf-8")
    assert (ROOT / "requirements-dev.txt").is_file()


def test_repository_has_no_generated_outputs_tracked_by_default() -> None:
    ignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    for pattern in (".venv/", "__pycache__/", ".pytest_cache/", "output/"):
        assert pattern in ignore
```

Create `tests/helpers.py` with reusable frontmatter parsing:

```python
from pathlib import Path
import re
import yaml


def load_skill(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    assert match, f"Missing YAML frontmatter: {path}"
    return yaml.safe_load(match.group(1)), text[match.end():]
```

**Step 2: Run the test to verify it fails**

Run:

```bash
python3 -m pytest tests/test_repository.py -v
```

Expected: FAIL because `VERSION`, `LICENSE`, and development configuration do not exist.

**Step 3: Add the minimal repository scaffold**

Create:

```text
VERSION: 0.1.0
requirements-dev.txt: pytest>=8,<9; PyYAML>=6,<7; python-pptx==1.0.2; PyMuPDF>=1.24,<2; Pillow>=10,<13
pytest.ini: [pytest] with testpaths = tests and addopts = -ra
```

Use the standard MIT license text with copyright `2026 wp-a`. Ignore local virtual environments, Python caches, test caches, rendered scratch files, and user-generated `output/` directories while allowing the curated `examples/output/` fixture.

**Step 4: Install development dependencies and run the test**

Run:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m pytest tests/test_repository.py -v
```

Expected: 2 tests pass.

**Step 5: Commit**

```bash
git add .gitignore VERSION LICENSE requirements-dev.txt pytest.ini tests
git commit -m "test: establish Paper2PPT repository harness"
```

### Task 2: Rewrite the canonical Skill around the evidence contract

**Files:**

- Modify: `SKILL.md`
- Create: `references/workflow.md`
- Create: `references/paper-types.md`
- Create: `docs/evaluation.md`
- Create: `tests/test_skill.py`

**Step 1: Establish a no-Skill behavioral baseline**

Before editing `SKILL.md`, use fresh evaluation agents that do not load any
paper-to-PPT Skill. Run at least three representative scenarios: a methods/AI
paper for a 15-minute Chinese group meeting, a dense experimental paper, and
partial input containing only an abstract plus figure legends. Capture the
agents' execution choices, missed gates, unnecessary work, output-contract
failures, and rationalizations verbatim in `docs/evaluation.md`.

**Step 2: Write failing Skill contract tests**

Create `tests/test_skill.py`:

```python
from pathlib import Path
import re

from tests.helpers import load_skill

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"


def test_skill_frontmatter_matches_agent_skills_contract() -> None:
    metadata, body = load_skill(SKILL)
    assert set(metadata) == {"name", "description"}
    assert metadata["name"] == "paper2ppt"
    assert 1 <= len(metadata["description"]) <= 1024
    assert len(body.splitlines()) <= 300
    assert len(body.split()) <= 700


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


def test_active_skill_surfaces_do_not_use_legacy_identity() -> None:
    text = SKILL.read_text(encoding="utf-8").lower()
    assert "nature-paper2ppt" not in text
    assert "nature-style" not in text
```

**Step 3: Run the tests to verify they fail**

Run:

```bash
.venv/bin/python -m pytest tests/test_skill.py -v
```

Expected: FAIL because the Skill still uses `nature-paper2ppt`, has a long single-file body, and has no references.

**Step 4: Implement the lean canonical Skill**

Rewrite `SKILL.md` with these exact top-level sections:

```markdown
# Paper2PPT
## Non-negotiable output
## Preflight
## Source sufficiency
## Core workflow
## Evidence and attribution
## Tool routing
## Quality gates
## Output contract
## Failure handling
## Completion checklist
```

Frontmatter requirements:

```yaml
---
name: paper2ppt
description: >-
  Use when a user wants an editable PowerPoint or PPTX made from a scientific or academic paper, paper PDF, DOI, PMID, arXiv link, article text, abstract with figure legends, or research notes for a journal club, group meeting, lab meeting, paper sharing, thesis seminar, or research talk; also when they ask for 论文转PPT, 文献汇报, 组会PPT, or 论文解读PPT. Not for general-purpose slide decks, business presentations, slide-image reconstruction, or paper-search-only requests.
---
```

Keep mandatory decisions and gotchas in the main file. Move detailed paper-type arcs and the expanded extraction sequence into `references/workflow.md` and `references/paper-types.md`, with explicit instructions about when each reference must be read.

**Step 5: Run focused tests**

Run:

```bash
.venv/bin/python -m pytest tests/test_skill.py -v
```

Expected: all Skill tests pass.

**Step 6: Commit**

```bash
git add SKILL.md references/workflow.md references/paper-types.md docs/evaluation.md tests/test_skill.py
git commit -m "feat: rebuild the Paper2PPT evidence workflow"
```

### Task 3: Add adaptive design, tool routing, and quality references

**Files:**

- Create: `references/slide-design.md`
- Create: `references/tool-routing.md`
- Create: `references/quality-gates.md`
- Modify: `SKILL.md`
- Modify: `tests/test_skill.py`

**Step 1: Add failing reference-content tests**

Extend `tests/test_skill.py`:

```python
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
```

**Step 2: Verify failure**

Run:

```bash
.venv/bin/python -m pytest tests/test_skill.py::test_conditional_references_cover_design_routing_and_qa -v
```

Expected: FAIL because the reference files do not exist.

**Step 3: Write the three focused references**

`references/slide-design.md` must define adaptive layout selection, typography hierarchy, accessible colors, evidence-first density, figure cropping, sources, notes, and projection-scale legibility without branded themes.

`references/tool-routing.md` must define this priority:

1. use an installed native presentation artifact Skill when it can satisfy the full output and QA contract;
2. otherwise use the environment's supported PPTX library path;
3. otherwise use PyMuPDF + Pillow + python-pptx;
4. fail during preflight if no editable PPTX path exists.

`references/quality-gates.md` must provide executable checklists for content fidelity, claim-to-source coverage, package validity, speaker notes, embedded media, bounds, rendered previews, and documented limitations.

Update `SKILL.md` with a one-sentence conditional load rule for each file.

**Step 4: Run all Skill tests**

Run:

```bash
.venv/bin/python -m pytest tests/test_skill.py -v
```

Expected: all tests pass and `SKILL.md` remains at or below 300 body lines.

**Step 5: Commit**

```bash
git add SKILL.md references tests/test_skill.py
git commit -m "docs: add adaptive slide and QA guidance"
```

### Task 4: Package the same Skill for Codex and Claude Code

**Files:**

- Create: `.agents/plugins/marketplace.json`
- Create: `.claude-plugin/marketplace.json`
- Create: `plugins/paper2ppt/.codex-plugin/plugin.json`
- Create: `plugins/paper2ppt/.claude-plugin/plugin.json`
- Create: `plugins/paper2ppt/skills/paper2ppt/agents/openai.yaml`
- Create: `scripts/sync_plugin.py`
- Create: `tests/test_manifests.py`
- Modify: `requirements-dev.txt`

**Step 1: Invoke the plugin authoring instructions**

Read and follow `plugin-creator` before choosing manifest fields. Preserve the approved product name and do not add MCP servers, hooks, agents, or settings that Paper2PPT does not need.

**Step 2: Write failing manifest and synchronization tests**

Create `tests/test_manifests.py` with assertions that:

```python
def test_plugin_manifests_match_release_identity() -> None:
    assert codex_manifest["name"] == "paper2ppt"
    assert claude_manifest["name"] == "paper2ppt"
    assert codex_manifest["version"] == claude_manifest["version"] == version()
    assert codex_manifest["license"] == claude_manifest["license"] == "MIT"
    assert codex_manifest["skills"] == "./skills/"
    assert claude_manifest["skills"] == ["./skills/paper2ppt"]


def test_plugin_skill_is_an_exact_mirror() -> None:
    assert packaged("SKILL.md").read_bytes() == root("SKILL.md").read_bytes()
    for name in ("workflow.md", "paper-types.md", "slide-design.md", "tool-routing.md", "quality-gates.md"):
        assert packaged(f"references/{name}").read_bytes() == root(f"references/{name}").read_bytes()
```

Also assert that the Codex `openai.yaml` display name is `Paper2PPT`, its default prompt is Chinese-first, and both marketplace entries point to `./plugins/paper2ppt`.

**Step 3: Verify the tests fail**

Run:

```bash
.venv/bin/python -m pytest tests/test_manifests.py -v
```

Expected: FAIL because no plugin package exists.

**Step 4: Add manifests and the synchronization script**

Implement `scripts/sync_plugin.py` using `pathlib` and `shutil` only. It must copy the canonical `SKILL.md`, `references/`, and runtime helper scripts into `plugins/paper2ppt/skills/paper2ppt/`, delete stale mirrored files inside those managed directories, preserve `agents/openai.yaml`, and support `--check` without modifying files.

Run:

```bash
.venv/bin/python scripts/sync_plugin.py
.venv/bin/python scripts/sync_plugin.py --check
.venv/bin/python -m pytest tests/test_manifests.py -v
```

Expected: sync check exits 0 and all manifest tests pass.

**Step 5: Commit**

```bash
git add .agents .claude-plugin plugins scripts/sync_plugin.py tests/test_manifests.py requirements-dev.txt
git commit -m "feat: add Codex and Claude Paper2PPT plugins"
```

### Task 5: Implement deterministic environment and input preflight

**Files:**

- Create: `scripts/preflight.py`
- Create: `tests/test_preflight.py`
- Modify: `SKILL.md`
- Modify: `references/tool-routing.md`

**Step 1: Write failing preflight tests**

Create tests for:

```python
def test_local_pdf_reports_source_and_capabilities(tmp_path): ...
def test_missing_local_input_is_an_error(tmp_path): ...
def test_doi_and_arxiv_are_recognized_as_remote_identifiers(): ...
def test_output_parent_is_created_only_with_explicit_flag(tmp_path): ...
def test_json_result_has_stable_schema(tmp_path): ...
```

The stable JSON schema is:

```json
{
  "ok": true,
  "source": {"kind": "pdf", "value": "/absolute/paper.pdf", "available": true},
  "output": {"path": "/absolute/output", "writable": true},
  "capabilities": {
    "pymupdf": true,
    "pillow": true,
    "python_pptx": true,
    "renderer": null
  },
  "warnings": [],
  "errors": []
}
```

**Step 2: Run tests to verify failure**

Run:

```bash
.venv/bin/python -m pytest tests/test_preflight.py -v
```

Expected: FAIL because `scripts.preflight` does not exist.

**Step 3: Implement the preflight CLI**

Use `argparse`, `importlib.util`, `json`, `pathlib`, `re`, and `shutil.which`. Support:

```text
python scripts/preflight.py INPUT --output PATH [--create-output] [--json]
```

Recognize PDF paths, DOI, PMID/PMCID, arXiv IDs, HTTP(S) URLs, Markdown/text files, and PPTX templates. Do not fetch remote content. Return exit 0 when the request has a viable source and authoring path, exit 1 when required input or authoring capability is missing, and exit 2 for invalid CLI usage.

**Step 4: Run focused and full tests**

Run:

```bash
.venv/bin/python -m pytest tests/test_preflight.py -v
.venv/bin/python -m pytest -q
```

Expected: all tests pass.

**Step 5: Sync and commit**

```bash
.venv/bin/python scripts/sync_plugin.py
git add SKILL.md references/tool-routing.md scripts/preflight.py plugins tests/test_preflight.py
git commit -m "feat: add Paper2PPT preflight checks"
```

### Task 6: Implement PPTX structural inspection and QA reporting

**Files:**

- Create: `scripts/inspect_pptx.py`
- Create: `tests/test_pptx_inspector.py`
- Create: `tests/fixtures/.gitkeep`
- Modify: `references/quality-gates.md`

**Step 1: Write failing inspector tests**

Generate PPTX fixtures inside pytest temporary directories rather than committing binary test fixtures. Cover:

```python
def test_valid_pptx_reports_slides_media_notes_and_bounds(tmp_path): ...
def test_shape_outside_slide_is_reported(tmp_path): ...
def test_missing_notes_can_be_required(tmp_path): ...
def test_invalid_zip_returns_package_error(tmp_path): ...
def test_markdown_report_contains_actionable_findings(tmp_path): ...
```

The result object must contain:

```python
{
    "ok": bool,
    "file": str,
    "slides": int,
    "media": int,
    "notes_slides": int,
    "out_of_bounds": list[dict],
    "warnings": list[str],
    "errors": list[str],
}
```

**Step 2: Verify failure**

Run:

```bash
.venv/bin/python -m pytest tests/test_pptx_inspector.py -v
```

Expected: FAIL because the inspector is missing.

**Step 3: Implement the inspector**

Use `zipfile` for package-level counts and `python-pptx` for reopen and shape bounds. Support:

```text
python scripts/inspect_pptx.py deck.pptx [--require-notes] [--json] [--report qa_report.md]
```

Do not treat intentional bleed smaller than 1% of slide dimensions as a hard failure. Missing notes should be a warning unless `--require-notes` is present. Invalid packages, unreadable presentations, or shapes materially outside slide bounds are errors.

**Step 4: Run tests and inspect CLI help**

Run:

```bash
.venv/bin/python -m pytest tests/test_pptx_inspector.py -v
.venv/bin/python scripts/inspect_pptx.py --help
```

Expected: tests pass and help documents every flag.

**Step 5: Sync and commit**

```bash
.venv/bin/python scripts/sync_plugin.py
git add scripts/inspect_pptx.py references/quality-gates.md plugins tests
git commit -m "feat: add editable PPTX quality inspection"
```

### Task 7: Add repository self-validation and trigger fixtures

**Files:**

- Create: `scripts/validate_repo.py`
- Create: `tests/test_validator.py`
- Create: `tests/trigger_cases.json`
- Create: `tests/test_trigger_cases.py`
- Modify: `scripts/sync_plugin.py`

**Step 1: Write failing validation tests**

Test that validation catches:

- malformed or mismatched Skill frontmatter;
- missing relative references;
- canonical/plugin drift;
- manifest/version drift;
- forbidden legacy identity in active surfaces;
- too few positive or negative trigger cases;
- malformed trigger case entries.

Use this trigger schema:

```json
{
  "id": "positive-local-pdf-journal-club",
  "query": "把 ~/Downloads/paper.pdf 做成中文组会汇报PPT，15分钟",
  "should_trigger": true,
  "category": "local-pdf"
}
```

Include at least 10 positives spanning PDF, DOI, PMID, arXiv, notes, templates, journal club, thesis seminar, methods papers, and reviews. Include at least 10 near-miss negatives spanning general business slides, image-to-editable-PPT, paper search, manuscript writing, citation formatting, and generic PDF summarization.

**Step 2: Verify failure**

Run:

```bash
.venv/bin/python -m pytest tests/test_validator.py tests/test_trigger_cases.py -v
```

Expected: FAIL because the validator and fixtures do not exist.

**Step 3: Implement validation**

`scripts/validate_repo.py` must compose small validation functions and print a concise report. It must support `--json`, return exit 0 on success and exit 1 on validation failure, and exclude historical design documents from the legacy-identity scan while checking `SKILL.md`, README files, active references, manifests, plugin Skill content, and Codex UI metadata.

**Step 4: Run validation and tests**

Run:

```bash
.venv/bin/python scripts/sync_plugin.py
.venv/bin/python scripts/validate_repo.py
.venv/bin/python -m pytest tests/test_validator.py tests/test_trigger_cases.py -v
```

Expected: validation passes and at least 20 trigger cases are accepted.

**Step 5: Commit**

```bash
git add scripts/validate_repo.py scripts/sync_plugin.py tests plugins
git commit -m "test: add Skill and trigger validation gates"
```

### Task 8: Forward-test and refine the Skill behavior

**Files:**

- Create: `docs/evaluation.md`
- Modify: `SKILL.md`
- Modify: `references/*.md`
- Modify: `tests/trigger_cases.json`

**Step 1: Invoke the Skill authoring evaluation instructions**

Use `skill-creator` and `writing-skills`. Because `writing-skills` explicitly requires baseline and forward tests, it authorizes subagents for this task. Run independent scenarios against the pre-redesign Skill and the redesigned Skill.

**Step 2: Run representative with-Skill cases**

Use four source-grounded prompts:

1. local full-text methods/AI paper for a 15-minute Chinese group meeting;
2. experimental paper with dense multi-panel figures;
3. review paper requiring an evidence-map narrative;
4. abstract plus figure legends only, requiring visible uncertainty.

Compare each result with the no-Skill baseline recorded during Task 2. Record
skipped steps, wrong assumptions, unnecessary work, output-contract misses, and
QA behavior in `docs/evaluation.md`.

**Step 3: Run trigger near-misses**

Use the positive and negative cases in `tests/trigger_cases.json`. Confirm the Skill activates for paper-to-presentation requests and does not claim general business slides, generic paper search, manuscript editing, or image-to-editable-PPT reconstruction.

**Step 4: Make only evidence-backed refinements**

Update instructions only when a baseline or forward trace demonstrates a concrete gap. Do not grow `SKILL.md` past 300 body lines. Move conditional corrections into the relevant reference and add a regression assertion where deterministic.

**Step 5: Re-run all validation and commit**

Run:

```bash
.venv/bin/python scripts/sync_plugin.py
.venv/bin/python scripts/validate_repo.py
.venv/bin/python -m pytest -q
```

Expected: all checks pass.

```bash
git add SKILL.md references plugins tests docs/evaluation.md
git commit -m "test: refine Paper2PPT from forward evaluations"
```

### Task 9: Build a license-safe example deck and showcase

**Files:**

- Create: `examples/source/README.md`
- Create: `examples/source/paper-metadata.json`
- Create: `examples/output/paper2ppt-example-zh.pptx`
- Create: `examples/output/qa_report.md`
- Create: `examples/output/asset_manifest.md`
- Create: `examples/showcase/overview.png`
- Create: `examples/showcase/slide-*.png`
- Create: `tests/test_example.py`

**Step 1: Select and document an open-access source**

Choose a paper whose full text and figures have an explicit CC BY or equivalent redistribution license. Record title, DOI or stable URL, publisher, license, retrieval date, and exact figure attribution in `examples/source/paper-metadata.json`. Do not use a source whose redistribution terms are unclear.

**Step 2: Write the failing example contract test**

Assert that the source metadata includes a license URL, the PPTX exists, the QA report records rendered visual review, every manifest entry has a source anchor, and `inspect_pptx.py --require-notes` passes the example.

**Step 3: Invoke the presentation workflow**

Use `presentations` to build an 8-10 slide Chinese example deck from the selected source. Follow the redesigned `paper2ppt` Skill, include speaker notes and source labels, and keep all scientific claims traceable.

**Step 4: Render and visually inspect**

Render the deck using the presentation tooling's supported workflow. Inspect every slide for overlap, clipping, unreadable panels, underfilled composition, bad crops, and source-label placement. Revise until clean, then generate a 2x2 or 3x2 overview montage and three representative slide images.

**Step 5: Run structural and example tests**

Run:

```bash
.venv/bin/python scripts/inspect_pptx.py examples/output/paper2ppt-example-zh.pptx --require-notes --report examples/output/qa_report.md
.venv/bin/python -m pytest tests/test_example.py -v
```

Expected: inspector and example tests pass with no structural errors.

**Step 6: Commit**

```bash
git add examples tests/test_example.py
git commit -m "docs: add reproducible Paper2PPT showcase"
```

### Task 10: Rewrite the Chinese-first README and English counterpart

**Files:**

- Modify: `README.md`
- Create: `README.en.md`
- Create: `CHANGELOG.md`
- Create: `docs/installation.md`
- Create: `docs/maintenance.md`
- Create: `tests/test_docs.py`

**Step 1: Write failing documentation tests**

Require both READMEs to include:

- Paper2PPT product name and concise value proposition;
- real showcase images with valid relative paths;
- Codex, Claude Code, and generic Agent Skills installation paths;
- supported inputs and exact default outputs;
- workflow and quality gates;
- privacy, paywall, OCR, renderer, and partial-source limitations;
- a factual comparison with outline-only Skills, Beamer generators, and standalone API-key applications;
- no legacy identity or branded visual wording.

**Step 2: Verify failure**

Run:

```bash
.venv/bin/python -m pytest tests/test_docs.py -v
```

Expected: FAIL because the old README is English-only and uses the former identity.

**Step 3: Write the documentation**

Make `README.md` Chinese-first. Its first viewport must show the name, one-sentence positioning, badges, a compact quick-start, and the real showcase montage. Keep the installation commands copyable and distinguish direct Skill installation from plugin installation.

Write `README.en.md` with equivalent facts, not a divergent feature set. Add `docs/installation.md` for client-specific details and `docs/maintenance.md` for sync, tests, example refresh, version bumps, and release steps. Start `CHANGELOG.md` with `0.1.0` and describe the full rename without preserving the old name as an active identifier.

**Step 4: Run docs and full tests**

Run:

```bash
.venv/bin/python -m pytest tests/test_docs.py -v
.venv/bin/python scripts/validate_repo.py
.venv/bin/python -m pytest -q
```

Expected: all checks pass.

**Step 5: Commit**

```bash
git add README.md README.en.md CHANGELOG.md docs tests/test_docs.py
git commit -m "docs: launch the Chinese-first Paper2PPT repository"
```

### Task 11: Add continuous integration and validate both plugin packages

**Files:**

- Create: `.github/workflows/ci.yml`
- Modify: `docs/maintenance.md`
- Modify: `tests/test_repository.py`

**Step 1: Write a failing workflow contract test**

Assert that CI runs on pushes and pull requests, uses Python 3.10 and 3.12, installs `requirements-dev.txt`, runs plugin sync in check mode, runs repository validation, runs pytest, and invokes the Agent Skills reference validator.

**Step 2: Verify failure**

Run:

```bash
.venv/bin/python -m pytest tests/test_repository.py -v
```

Expected: FAIL because `.github/workflows/ci.yml` does not exist.

**Step 3: Add CI**

Use actions/checkout and actions/setup-python pinned to current major versions. Run:

```text
pip install -r requirements-dev.txt
pip install "git+https://github.com/agentskills/agentskills.git#subdirectory=skills-ref"
python scripts/sync_plugin.py --check
python scripts/validate_repo.py
skills-ref validate .
skills-ref validate plugins/paper2ppt/skills/paper2ppt
pytest -q
```

Avoid model API calls and rendering dependencies in CI.

**Step 4: Run the CI commands locally**

Run each command exactly as CI will. Expected: every command exits 0.

**Step 5: Commit**

```bash
git add .github docs/maintenance.md tests/test_repository.py
git commit -m "ci: validate Paper2PPT skills and artifacts"
```

### Task 12: Verify Codex and Claude Code loading behavior

**Files:**

- Modify: `docs/evaluation.md`
- Modify: `docs/installation.md`
- Modify: `SKILL.md` and references only if verified issues are found

**Step 1: Test Codex packaging**

Use the locally supported Codex plugin or Skill installation path. Confirm the Skill is discoverable as `paper2ppt`, the display name is `Paper2PPT`, and representative Chinese and English prompts activate the correct workflow.

**Step 2: Test Claude Code packaging**

Run:

```bash
claude --plugin-dir ./plugins/paper2ppt
```

Within Claude Code, verify `/paper2ppt:paper2ppt` appears, loads the packaged Skill, and follows the same output contract. Run `/reload-plugins` after any manifest change.

**Step 3: Record evidence and correct only verified differences**

Document client versions, commands, observed invocation names, successful prompts, near-miss prompts, and limitations. If one client requires a metadata adjustment, write a failing manifest or docs test before editing.

**Step 4: Re-run all validation and commit**

```bash
.venv/bin/python scripts/sync_plugin.py --check
.venv/bin/python scripts/validate_repo.py
.venv/bin/python -m pytest -q
git add SKILL.md references plugins docs tests
git commit -m "test: verify Codex and Claude compatibility"
```

### Task 13: Final review, in-place rename, installation migration, and v0.1.0 release

**Files:**

- Modify only files identified by final review
- Update: GitHub repository metadata, topics, and release
- Replace local installed Skill directory after repository validation

**Step 1: Run code and Skill review**

Invoke `requesting-code-review`. Address only verified findings, adding regression tests before fixes. Confirm the worktree contains no unrelated changes.

**Step 2: Run the final verification suite**

Invoke `verification-before-completion`, then run:

```bash
.venv/bin/python scripts/sync_plugin.py --check
.venv/bin/python scripts/validate_repo.py
.venv/bin/python scripts/inspect_pptx.py examples/output/paper2ppt-example-zh.pptx --require-notes
.venv/bin/python -m pytest -q
git diff --check main...HEAD
git status --short
```

Expected: all commands pass; status is clean.

**Step 3: Integrate the branch locally**

Invoke `finishing-a-development-branch`. Merge `feature/paper2ppt-repository-redesign` into local `main` only after all checks pass. Re-run the validation suite on `main`.

**Step 4: Push the rebuilt repository**

```bash
git push origin main
```

Verify the remote commit matches local `main` before renaming.

**Step 5: Rename the GitHub repository in place**

```bash
gh repo rename paper2ppt --repo wp-a/nature-paper2ppt --yes
git remote set-url origin https://github.com/wp-a/paper2ppt.git
gh repo edit wp-a/paper2ppt --description "将学术论文转为可编辑、可溯源的中文 PPTX，兼容 Codex 与 Claude Code。" --homepage "https://github.com/wp-a/paper2ppt"
```

Set topics including `agent-skills`, `academic-presentation`, `claude-code`, `codex`, `paper2ppt`, `powerpoint`, `pptx`, and `research-tools`. Verify the old URL redirects and the new URL serves the repository.

**Step 6: Migrate the local installed Skill**

Use `skill-installer` or the documented local install path to install `paper2ppt`. Remove the former installed Skill directory only after the new Skill loads successfully. Verify there is one active `paper2ppt` Skill and no active legacy alias.

**Step 7: Create and verify the release**

```bash
git tag -a v0.1.0 -m "Paper2PPT v0.1.0"
git push origin v0.1.0
gh release create v0.1.0 --repo wp-a/paper2ppt --title "Paper2PPT v0.1.0" --notes-file CHANGELOG.md examples/output/paper2ppt-example-zh.pptx
```

Verify the release points to the merged commit, the example asset downloads, both plugin manifests report `0.1.0`, and all GitHub Actions checks pass.

**Step 8: Record the final state**

Report the new repository URL, release URL, merge commit, tag, verification commands, test count, installed Skill path, and any remaining renderer or client limitation.
