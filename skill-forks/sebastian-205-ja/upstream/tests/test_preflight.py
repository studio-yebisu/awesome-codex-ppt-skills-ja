import json
import os
from pathlib import Path
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
PREFLIGHT = ROOT / "scripts" / "preflight.py"


def run_preflight(
    input_value: str,
    output: Path,
    *extra: str,
    no_site_packages: bool = False,
    cwd: Path = ROOT,
    python_path: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    command = [sys.executable]
    if no_site_packages:
        command.append("-S")
    command.extend(
        [str(PREFLIGHT), input_value, "--output", str(output), "--json", *extra]
    )
    environment = os.environ.copy()
    if python_path is not None:
        environment["PYTHONPATH"] = str(python_path)
    return subprocess.run(
        command,
        cwd=cwd,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )


def result_json(result: subprocess.CompletedProcess[str]) -> dict:
    assert result.stderr == ""
    return json.loads(result.stdout)


def test_local_pdf_reports_source_and_capabilities(tmp_path: Path) -> None:
    paper = tmp_path / "paper.pdf"
    paper.write_bytes(b"%PDF-1.7\n")
    output = tmp_path / "output"
    output.mkdir()

    result = run_preflight(str(paper), output)

    assert result.returncode == 0
    payload = result_json(result)
    assert payload["ok"] is True
    assert payload["source"] == {
        "kind": "pdf",
        "value": str(paper.resolve()),
        "available": True,
    }
    assert payload["output"] == {
        "path": str(output.resolve()),
        "writable": True,
    }
    assert payload["capabilities"]["pymupdf"] is True
    assert payload["capabilities"]["pillow"] is True
    assert payload["capabilities"]["python_pptx"] is True
    assert payload["capabilities"]["renderer"] in (True, None)
    assert payload["errors"] == []


def test_missing_local_input_is_an_error(tmp_path: Path) -> None:
    paper = tmp_path / "missing.pdf"
    output = tmp_path / "output"
    output.mkdir()

    result = run_preflight(str(paper), output)

    assert result.returncode == 1
    payload = result_json(result)
    assert payload["ok"] is False
    assert payload["source"] == {
        "kind": "pdf",
        "value": str(paper.resolve()),
        "available": False,
    }
    assert any("does not exist" in error for error in payload["errors"])


@pytest.mark.parametrize(
    ("input_value", "kind", "normalized"),
    [
        ("doi:10.1371/journal.pone.0276250", "doi", "10.1371/journal.pone.0276250"),
        ("10.48550/arXiv.2401.12345", "doi", "10.48550/arXiv.2401.12345"),
        ("arXiv:2401.12345v2", "arxiv", "2401.12345v2"),
        ("2401.12345", "arxiv", "2401.12345"),
    ],
)
def test_doi_and_arxiv_are_recognized_as_remote_identifiers(
    tmp_path: Path, input_value: str, kind: str, normalized: str
) -> None:
    output = tmp_path / "output"
    output.mkdir()

    result = run_preflight(input_value, output)

    assert result.returncode == 0
    payload = result_json(result)
    assert payload["source"] == {
        "kind": kind,
        "value": normalized,
        "available": None,
    }
    assert any("not fetched" in warning for warning in payload["warnings"])


def test_output_parent_is_created_only_with_explicit_flag(tmp_path: Path) -> None:
    notes = tmp_path / "notes.md"
    notes.write_text("# Notes\n", encoding="utf-8")
    output = tmp_path / "nested" / "output"

    without_flag = run_preflight(str(notes), output)

    assert without_flag.returncode == 1
    assert not output.exists()
    assert not output.parent.exists()
    assert result_json(without_flag)["output"]["writable"] is False

    with_flag = run_preflight(str(notes), output, "--create-output")

    assert with_flag.returncode == 0
    assert output.is_dir()
    assert result_json(with_flag)["output"]["writable"] is True


def test_json_result_has_stable_schema(tmp_path: Path) -> None:
    text = tmp_path / "paper.txt"
    text.write_text("paper text\n", encoding="utf-8")
    output = tmp_path / "output"
    output.mkdir()

    payload = result_json(run_preflight(str(text), output))

    assert list(payload) == [
        "ok",
        "source",
        "output",
        "capabilities",
        "warnings",
        "errors",
    ]
    assert list(payload["source"]) == ["kind", "value", "available"]
    assert list(payload["output"]) == ["path", "writable"]
    assert list(payload["capabilities"]) == [
        "pymupdf",
        "pillow",
        "python_pptx",
        "renderer",
    ]
    assert isinstance(payload["warnings"], list)
    assert isinstance(payload["errors"], list)


@pytest.mark.parametrize(
    ("input_value", "kind", "normalized"),
    [
        ("PMID: 12345678", "pmid", "12345678"),
        ("12345678", "pmid", "12345678"),
        ("PMC1234567", "pmcid", "PMC1234567"),
        ("https://example.org/paper", "url", "https://example.org/paper"),
        ("https://doi.org/10.1000/example", "doi", "10.1000/example"),
        ("https://arxiv.org/abs/2401.12345v3", "arxiv", "2401.12345v3"),
    ],
)
def test_remote_source_variants_are_normalized_without_fetching(
    tmp_path: Path, input_value: str, kind: str, normalized: str
) -> None:
    output = tmp_path / "output"
    output.mkdir()

    result = run_preflight(input_value, output)

    assert result.returncode == 0
    payload = result_json(result)
    assert payload["source"] == {
        "kind": kind,
        "value": normalized,
        "available": None,
    }
    assert any("not fetched" in warning for warning in payload["warnings"])


@pytest.mark.parametrize(
    ("suffix", "kind"),
    [
        (".md", "markdown"),
        (".markdown", "markdown"),
        (".txt", "text"),
        (".pptx", "pptx-template"),
    ],
)
def test_supported_local_file_types_are_recognized(
    tmp_path: Path, suffix: str, kind: str
) -> None:
    source = tmp_path / f"source{suffix}"
    source.write_bytes(b"source")
    output = tmp_path / "output"
    output.mkdir()

    result = run_preflight(str(source), output)

    assert result.returncode == 0
    assert result_json(result)["source"] == {
        "kind": kind,
        "value": str(source.resolve()),
        "available": True,
    }


def test_existing_unsupported_local_file_is_rejected(tmp_path: Path) -> None:
    source = tmp_path / "paper.docx"
    source.write_bytes(b"source")
    output = tmp_path / "output"
    output.mkdir()

    result = run_preflight(str(source), output)

    assert result.returncode == 1
    payload = result_json(result)
    assert payload["source"]["kind"] == "unsupported"
    assert any("unsupported" in error for error in payload["errors"])


def test_missing_authoring_capability_is_an_error_without_site_packages(
    tmp_path: Path,
) -> None:
    source = tmp_path / "notes.txt"
    source.write_text("notes\n", encoding="utf-8")
    output = tmp_path / "output"
    output.mkdir()

    result = run_preflight(
        str(source), output, no_site_packages=True
    )

    assert result.returncode == 1
    payload = result_json(result)
    assert payload["capabilities"]["python_pptx"] is False
    assert any("python-pptx" in error for error in payload["errors"])


def test_confirmed_native_authoring_overrides_only_missing_python_pptx(
    tmp_path: Path,
) -> None:
    source = tmp_path / "notes.txt"
    source.write_text("notes\n", encoding="utf-8")
    output = tmp_path / "output"
    output.mkdir()

    result = run_preflight(
        str(source),
        output,
        "--native-authoring",
        no_site_packages=True,
    )

    assert result.returncode == 0
    payload = result_json(result)
    assert payload["capabilities"]["python_pptx"] is False
    assert any("native authoring" in warning.lower() for warning in payload["warnings"])
    assert not any("python-pptx" in error for error in payload["errors"])


def test_native_authoring_does_not_override_missing_source_or_output(
    tmp_path: Path,
) -> None:
    missing_source = tmp_path / "missing.txt"
    missing_output = tmp_path / "missing-output"

    result = run_preflight(
        str(missing_source),
        missing_output,
        "--native-authoring",
        no_site_packages=True,
    )

    assert result.returncode == 1
    payload = result_json(result)
    assert payload["ok"] is False
    assert payload["source"]["available"] is False
    assert payload["output"]["writable"] is False


def test_confirmed_native_pdf_and_authoring_override_only_their_dependencies(
    tmp_path: Path,
) -> None:
    source = tmp_path / "paper.pdf"
    source.write_bytes(b"%PDF-1.7\n")
    output = tmp_path / "output"
    output.mkdir()

    result = run_preflight(
        str(source),
        output,
        "--native-authoring",
        "--native-pdf",
        no_site_packages=True,
    )

    assert result.returncode == 0
    payload = result_json(result)
    assert payload["capabilities"]["python_pptx"] is False
    assert payload["capabilities"]["pymupdf"] is False
    assert any("native authoring" in warning.lower() for warning in payload["warnings"])
    assert any("native pdf" in warning.lower() for warning in payload["warnings"])
    assert payload["errors"] == []


def test_native_pdf_does_not_override_source_output_or_authoring(
    tmp_path: Path,
) -> None:
    output = tmp_path / "output"
    output.mkdir()
    missing_source = run_preflight(
        str(tmp_path / "missing.pdf"),
        output,
        "--native-authoring",
        "--native-pdf",
        no_site_packages=True,
    )

    source = tmp_path / "paper.pdf"
    source.write_bytes(b"%PDF-1.7\n")
    missing_output = run_preflight(
        str(source),
        tmp_path / "missing-output",
        "--native-authoring",
        "--native-pdf",
        no_site_packages=True,
    )
    missing_authoring = run_preflight(
        str(source),
        output,
        "--native-pdf",
        no_site_packages=True,
    )

    assert missing_source.returncode == 1
    assert result_json(missing_source)["source"]["available"] is False
    assert missing_output.returncode == 1
    assert result_json(missing_output)["output"]["writable"] is False
    assert missing_authoring.returncode == 1
    assert any(
        "python-pptx" in error
        for error in result_json(missing_authoring)["errors"]
    )


def write_fake_distribution(
    site: Path,
    *,
    module: str,
    distribution: str | None = None,
    version: str | None = None,
) -> None:
    module_path = site / f"{module}.py"
    module_path.write_text(
        "raise RuntimeError('capability detection must not import package code')\n",
        encoding="utf-8",
    )
    if distribution is None or version is None:
        return
    normalized = distribution.lower().replace("-", "_")
    metadata = site / f"{normalized}-{version}.dist-info" / "METADATA"
    metadata.parent.mkdir()
    metadata.write_text(
        "Metadata-Version: 2.1\n"
        f"Name: {distribution}\n"
        f"Version: {version}\n",
        encoding="utf-8",
    )


def fake_capability_site(
    tmp_path: Path,
    *,
    python_pptx: str | None,
    pymupdf: str | None,
    pillow: str | None,
) -> Path:
    site = tmp_path / "fake-site"
    site.mkdir()
    write_fake_distribution(
        site,
        module="pptx",
        distribution="python-pptx" if python_pptx else None,
        version=python_pptx,
    )
    write_fake_distribution(
        site,
        module="pymupdf",
        distribution="PyMuPDF" if pymupdf else None,
        version=pymupdf,
    )
    write_fake_distribution(
        site,
        module="PIL",
        distribution="Pillow" if pillow else None,
        version=pillow,
    )
    return site


def test_capabilities_require_distribution_metadata(tmp_path: Path) -> None:
    site = fake_capability_site(
        tmp_path,
        python_pptx=None,
        pymupdf=None,
        pillow=None,
    )
    source = tmp_path / "notes.txt"
    source.write_text("notes\n", encoding="utf-8")
    output = tmp_path / "output"
    output.mkdir()

    result = run_preflight(
        str(source),
        output,
        "--native-authoring",
        no_site_packages=True,
        python_path=site,
    )

    capabilities = result_json(result)["capabilities"]
    assert capabilities["python_pptx"] is False
    assert capabilities["pymupdf"] is False
    assert capabilities["pillow"] is False


def test_capabilities_reject_versions_below_minimum(tmp_path: Path) -> None:
    site = fake_capability_site(
        tmp_path,
        python_pptx="1.0.1",
        pymupdf="1.23.9",
        pillow="9.5.0",
    )
    source = tmp_path / "notes.txt"
    source.write_text("notes\n", encoding="utf-8")
    output = tmp_path / "output"
    output.mkdir()

    result = run_preflight(
        str(source),
        output,
        no_site_packages=True,
        python_path=site,
    )

    assert result.returncode == 1
    capabilities = result_json(result)["capabilities"]
    assert capabilities["python_pptx"] is False
    assert capabilities["pymupdf"] is False
    assert capabilities["pillow"] is False


def test_capabilities_accept_minimum_versions_without_importing(
    tmp_path: Path,
) -> None:
    site = fake_capability_site(
        tmp_path,
        python_pptx="1.0.2",
        pymupdf="1.24.0",
        pillow="10.0.0",
    )
    source = tmp_path / "notes.txt"
    source.write_text("notes\n", encoding="utf-8")
    output = tmp_path / "output"
    output.mkdir()

    result = run_preflight(
        str(source),
        output,
        no_site_packages=True,
        python_path=site,
    )

    assert result.returncode == 0
    capabilities = result_json(result)["capabilities"]
    assert capabilities["python_pptx"] is True
    assert capabilities["pymupdf"] is True
    assert capabilities["pillow"] is True


def test_existing_numeric_filename_beats_bare_pmid(tmp_path: Path) -> None:
    source = tmp_path / "12345678"
    source.write_text("local source\n", encoding="utf-8")
    output = tmp_path / "output"
    output.mkdir()

    result = run_preflight(source.name, output, cwd=tmp_path)

    assert result.returncode == 1
    payload = result_json(result)
    assert payload["source"] == {
        "kind": "unsupported",
        "value": str(source.resolve()),
        "available": True,
    }
    assert not any("not fetched" in warning for warning in payload["warnings"])


def test_existing_doi_shaped_pdf_path_beats_bare_doi(tmp_path: Path) -> None:
    source = tmp_path / "10.1234" / "paper.pdf"
    source.parent.mkdir()
    source.write_bytes(b"%PDF-1.7\n")
    output = tmp_path / "output"
    output.mkdir()

    result = run_preflight("10.1234/paper.pdf", output, cwd=tmp_path)

    assert result.returncode == 0
    assert result_json(result)["source"] == {
        "kind": "pdf",
        "value": str(source.resolve()),
        "available": True,
    }


def test_original_filename_whitespace_is_preserved_before_identifier_matching(
    tmp_path: Path,
) -> None:
    source = tmp_path / " 2401.12345 "
    source.write_text("local source\n", encoding="utf-8")
    output = tmp_path / "output"
    output.mkdir()

    result = run_preflight(source.name, output, cwd=tmp_path)

    assert result.returncode == 1
    payload = result_json(result)
    assert payload["source"]["kind"] == "unsupported"
    assert payload["source"]["value"] == str(source.resolve())
    assert payload["source"]["available"] is True


def test_explicit_identifier_prefix_beats_existing_local_filename(
    tmp_path: Path,
) -> None:
    (tmp_path / "PMID:12345678").write_text("local source\n", encoding="utf-8")
    output = tmp_path / "output"
    output.mkdir()

    result = run_preflight("PMID:12345678", output, cwd=tmp_path)

    assert result.returncode == 0
    assert result_json(result)["source"] == {
        "kind": "pmid",
        "value": "12345678",
        "available": None,
    }


def test_doi_url_drops_query_and_fragment(tmp_path: Path) -> None:
    output = tmp_path / "output"
    output.mkdir()
    secret = "private-token"

    result = run_preflight(
        f"https://doi.org/10.1000/example?token={secret}#signed-fragment",
        output,
    )

    assert result.returncode == 0
    payload = result_json(result)
    assert payload["source"]["kind"] == "doi"
    assert payload["source"]["value"] == "10.1000/example"
    assert secret not in result.stdout
    assert "signed-fragment" not in result.stdout
    assert any("redact" in warning.lower() for warning in payload["warnings"])


def test_generic_url_preserves_plos_source_identity_query(tmp_path: Path) -> None:
    output = tmp_path / "output"
    output.mkdir()
    url = (
        "https://journals.plos.org/plosone/article/file"
        "?id=10.1371/journal.pone.0276250&type=printable"
    )

    result = run_preflight(url, output)

    assert result.returncode == 0
    payload = result_json(result)
    assert payload["source"] == {
        "kind": "url",
        "value": url,
        "available": None,
    }
    assert not any("redact" in warning.lower() for warning in payload["warnings"])


def test_url_redacts_userinfo_query_and_fragment_from_json_and_human_output(
    tmp_path: Path,
) -> None:
    output = tmp_path / "output"
    output.mkdir()
    input_value = (
        "https://alice:super-secret@example.org/paper.pdf"
        "?id=paper&X-Amz-Signature=signed-secret#private-fragment"
    )

    json_result = run_preflight(input_value, output)
    human_result = subprocess.run(
        [
            sys.executable,
            str(PREFLIGHT),
            input_value,
            "--output",
            str(output),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert json_result.returncode == human_result.returncode == 0
    payload = result_json(json_result)
    assert payload["source"]["value"] == "https://example.org/paper.pdf?id=paper"
    assert any("redact" in warning.lower() for warning in payload["warnings"])
    for secret in (
        "alice",
        "super-secret",
        "X-Amz-Signature",
        "signed-secret",
        "private-fragment",
    ):
        assert secret not in json_result.stdout
        assert secret not in human_result.stdout


def test_url_with_malformed_port_is_rejected(tmp_path: Path) -> None:
    output = tmp_path / "output"
    output.mkdir()

    result = run_preflight("https://example.org:not-a-port/paper?id=1", output)

    assert result.returncode == 1
    payload = result_json(result)
    assert payload["ok"] is False
    assert payload["source"]["kind"] == "url"
    assert any("port" in error.lower() for error in payload["errors"])


def test_invalid_cli_usage_returns_argparse_exit_two() -> None:
    result = subprocess.run(
        [sys.executable, str(PREFLIGHT)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 2
    assert "usage:" in result.stderr


def test_human_output_is_available_without_json(tmp_path: Path) -> None:
    source = tmp_path / "notes.txt"
    source.write_text("notes\n", encoding="utf-8")
    output = tmp_path / "output"
    output.mkdir()

    result = subprocess.run(
        [
            sys.executable,
            str(PREFLIGHT),
            str(source),
            "--output",
            str(output),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert result.stderr == ""
    assert "Paper2PPT preflight: OK" in result.stdout


def test_skill_documents_the_deterministic_preflight_command() -> None:
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    routing = (ROOT / "references" / "tool-routing.md").read_text(encoding="utf-8")
    command = 'python "<SKILL_DIR>/scripts/preflight.py" INPUT --output PATH'

    assert command in skill
    assert command in routing
    assert "--create-output" in routing
    assert "--json" in routing
    assert "--native-authoring" in skill
    assert "--native-authoring" in routing
    assert "--native-pdf" in skill
    assert "--native-pdf" in routing
    assert "page-grounded" in routing
    assert "source and output" in routing.lower()
    assert "does not fetch" in routing.lower()
