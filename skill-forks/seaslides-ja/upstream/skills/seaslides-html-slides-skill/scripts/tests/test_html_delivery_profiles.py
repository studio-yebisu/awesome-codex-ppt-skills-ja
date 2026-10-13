"""Regression coverage for HTML compiler delivery receipts and profiles."""

import importlib.util
import io
import json
import tempfile
import unittest
import zipfile
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock


SCRIPTS_DIR = Path(__file__).resolve().parents[1]


def load_script(module_name: str, filename: str):
    spec = importlib.util.spec_from_file_location(module_name, SCRIPTS_DIR / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {filename}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


compiler = load_script("seaslides_html_delivery_compiler", "html_compiler.py")
validator = load_script("seaslides_html_delivery_validator", "validate_project.py")


class DeliveryReceiptFixture:
    """Creates a compact, internally consistent delivery receipt."""

    @staticmethod
    def write_png(path: Path, size: tuple[int, int] = (1280, 720)) -> None:
        from PIL import Image

        Image.new("RGB", size, (245, 245, 245)).save(path, format="PNG")

    @staticmethod
    def write_pdf(path: Path, page_count: int = 2) -> None:
        objects = [
            b"<< /Type /Catalog /Pages 2 0 R >>",
            (
                b"<< /Type /Pages /Count "
                + str(page_count).encode("ascii")
                + b" /Kids ["
                + b" ".join(
                    f"{number + 2} 0 R".encode("ascii")
                    for number in range(1, page_count + 1)
                )
                + b"] >>"
            ),
        ]
        objects.extend(
            b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 1280 720] >>"
            for _ in range(page_count)
        )
        data = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
        offsets = [0]
        for number, body in enumerate(objects, 1):
            offsets.append(len(data))
            data.extend(f"{number} 0 obj\n".encode("ascii"))
            data.extend(body)
            data.extend(b"\nendobj\n")
        xref_offset = len(data)
        data.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
        data.extend(b"0000000000 65535 f \n")
        for offset in offsets[1:]:
            data.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
        data.extend(
            f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
            f"startxref\n{xref_offset}\n%%EOF\n".encode("ascii")
        )
        path.write_bytes(data)

    @staticmethod
    def write_pptx(
        path: Path, slide_count: int = 2, *, duplicate_first_relationship: bool = False
    ) -> None:
        presentation_ns = (
            "http://schemas.openxmlformats.org/presentationml/2006/main"
        )
        relationships_ns = (
            "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
        )
        slide_ids = "".join(
            f'<p:sldId id="{255 + number}" '
            f'r:id="rId{1 if duplicate_first_relationship else number}"/>'
            for number in range(1, slide_count + 1)
        )
        presentation = (
            f'<p:presentation xmlns:p="{presentation_ns}" '
            f'xmlns:r="{relationships_ns}"><p:sldIdLst>{slide_ids}'
            "</p:sldIdLst></p:presentation>"
        )
        content_types = (
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="xml" ContentType="application/xml"/>'
            + "".join(
                f'<Override PartName="/ppt/notesSlides/notesSlide{number}.xml" '
                'ContentType="application/vnd.openxmlformats-officedocument.presentationml.notesSlide+xml"/>'
                for number in range(1, slide_count + 1)
            )
            + '</Types>'
        )
        slide = f'<p:sld xmlns:p="{presentation_ns}"><p:cSld/></p:sld>'
        package_relationships_ns = (
            "http://schemas.openxmlformats.org/package/2006/relationships"
        )
        slide_relationship_type = (
            "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide"
        )
        relationship_rows = "".join(
            f'<Relationship Id="rId{number}" Type="{slide_relationship_type}" '
            f'Target="slides/slide{number}.xml"/>'
            for number in range(1, slide_count + 1)
        )
        relationships = (
            f'<Relationships xmlns="{package_relationships_ns}">'
            f'{relationship_rows}</Relationships>'
        )
        notes_relationship_type = (
            "http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesSlide"
        )
        drawing_ns = "http://schemas.openxmlformats.org/drawingml/2006/main"
        notes_ns = "http://schemas.openxmlformats.org/presentationml/2006/main"
        with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            archive.writestr("[Content_Types].xml", content_types)
            archive.writestr("ppt/presentation.xml", presentation)
            archive.writestr("ppt/_rels/presentation.xml.rels", relationships)
            for number in range(1, slide_count + 1):
                archive.writestr(f"ppt/slides/slide{number}.xml", slide)
                archive.writestr(
                    f"ppt/slides/_rels/slide{number}.xml.rels",
                    f'<Relationships xmlns="{package_relationships_ns}">'
                    f'<Relationship Id="rIdNotes" Type="{notes_relationship_type}" '
                    f'Target="../notesSlides/notesSlide{number}.xml"/>'
                    '</Relationships>',
                )
                archive.writestr(
                    f"ppt/notesSlides/notesSlide{number}.xml",
                    f'<p:notes xmlns:p="{notes_ns}" xmlns:a="{drawing_ns}">'
                    f'<p:cSld><p:spTree><p:sp><p:txBody><a:p><a:r><a:t>Note {number}</a:t>'
                    '</a:r></a:p></p:txBody></p:sp></p:spTree></p:cSld></p:notes>',
                )

    @staticmethod
    def project(root: Path) -> Path:
        project = root / "deck"
        project.mkdir()
        (project / "index-template.html").write_text(
            "<html><body>{{CONTENT}}</body></html>", encoding="utf-8"
        )
        (project / "template.css").write_text(
            ".slide { width: 100vw; height: 100vh; }", encoding="utf-8"
        )
        (project / "content.html").write_text(
            '<section class="slide light" data-layout="T01" data-notes="Introduce.">\n'
            "  <h1>One</h1>\n</section>\n"
            '<section class="slide dark" data-layout="T02" data-notes="Close.">\n'
            "  <h2>Two</h2>\n</section>\n",
            encoding="utf-8",
        )
        (project / "index.html").write_text("<html>assembled</html>", encoding="utf-8")
        return project

    @staticmethod
    def write_receipt(project: Path, *, include_pptx: bool = False) -> None:
        output = project / "output"
        svgs = output / "svgs"
        pngs = output / "pngs"
        browser_pngs = output / "browser_pngs"
        for directory in (svgs, pngs, browser_pngs):
            directory.mkdir(parents=True)
        for number in (1, 2):
            (svgs / f"slide_{number:02d}.svg").write_text(
                '<svg viewBox="0 0 1280 720"></svg>', encoding="utf-8"
            )
            DeliveryReceiptFixture.write_png(pngs / f"slide_{number:02d}.png")
            DeliveryReceiptFixture.write_png(browser_pngs / f"slide_{number:02d}.png")
        dom_audit = output / "dom-audit.json"
        dom_audit.write_text(
            json.dumps({
                "schema": "seaslides.browser-dom-audit",
                "version": 1,
                "summary": {
                    "status": "pass",
                    "slideCount": 2,
                    "issueCount": 0,
                    "blockerCount": 0,
                    "reviewCount": 0,
                },
                "issues": [],
                "slides": [{"index": 1, "issues": []}, {"index": 2, "issues": []}],
            }),
            encoding="utf-8",
        )
        artifacts = [
            ("svg", svgs),
            ("dom_audit", dom_audit),
            ("png", pngs),
            ("browser_png", browser_pngs),
        ]
        overview = output / "overview.png"
        DeliveryReceiptFixture.write_png(overview, (640, 360))
        artifacts.append(("overview", overview))
        pdf = output / "slides.pdf"
        DeliveryReceiptFixture.write_pdf(pdf)
        artifacts.append(("pdf", pdf))
        render_fidelity = output / "render-fidelity.json"
        render_fidelity.write_text(
            json.dumps({
                "schema": "seaslides.html-render-fidelity/v1",
                "status": "pass",
                "slide_count": 2,
                "review_slides": [],
                "slides": [
                    {"slide": 1, "status": "pass"},
                    {"slide": 2, "status": "pass"},
                ],
            }),
            encoding="utf-8",
        )
        artifacts.append(("render_fidelity", render_fidelity))
        if include_pptx:
            pptx = output / "slides.pptx"
            DeliveryReceiptFixture.write_pptx(pptx)
            artifacts.append(("pptx", pptx))

        def artifact_row(name: str, path: Path) -> dict:
            row = {
                "name": name,
                "path": path.relative_to(project).as_posix(),
                "kind": "directory" if path.is_dir() else "file",
                "sha256": (
                    validator.sha256_directory(path)
                    if path.is_dir() else validator.sha256_file(path)
                ),
            }
            if path.is_dir():
                row["file_count"] = len([item for item in path.rglob("*") if item.is_file()])
            else:
                row["bytes"] = path.stat().st_size
            return row

        input_names = ["index-template.html", "template.css", "content.html"]
        tool_names = [
            "requirements.txt",
            "scripts/html_compiler.py", "scripts/assemble.py",
            "scripts/runtime_environment.py",
            "scripts/runtime/deck_runtime.js",
            "scripts/html_to_svg/browser_dom_to_svg.mjs",
            "scripts/html_to_svg/browser_dom_audit.mjs",
            "scripts/html_to_svg/chart_renderer.mjs",
            "scripts/html_to_svg/package.json",
            "scripts/html_to_svg/package-lock.json",
            "scripts/html_to_svg/browser_svg_to_png.mjs",
            "scripts/html_to_svg/browser_html_to_png.mjs",
            "scripts/html_to_svg/browser_svg_to_pdf.mjs",
        ]
        if include_pptx:
            tool_names.append("scripts/svg_to_pptx.py")
            for package_name in ("svg_to_pptx", "svg_finalize"):
                tool_names.extend(
                    path.relative_to(validator.SKILL_ROOT).as_posix()
                    for path in (SCRIPTS_DIR / package_name).rglob("*.py")
                    if path.is_file()
                )
        tool_names = sorted(set(tool_names))
        requested_formats = ["svg", "png", "browser_png", "overview", "pdf"]
        if include_pptx:
            requested_formats.append("pptx")
        receipt = {
            "schema": "seaslides-html-compile/v1",
            "status": "pass",
            "entry": "content.html",
            "slide_count": 2,
            "requested_formats": requested_formats,
            "canvas": {
                "width": 1280,
                "height": 720,
                "source": "test",
                "png_scale": 1,
            },
            "inputs": [
                {
                    "path": name,
                    "bytes": (project / name).stat().st_size,
                    "sha256": validator.sha256_file(project / name),
                }
                for name in input_names
            ],
            "toolchain": [
                {
                    "path": name,
                    "bytes": (validator.SKILL_ROOT / name).stat().st_size,
                    "sha256": validator.sha256_file(validator.SKILL_ROOT / name),
                }
                for name in tool_names
            ],
            "runtime_environment": validator.runtime_environment_fingerprint(),
            "assembled_index_sha256": validator.sha256_file(project / "index.html"),
            "artifacts": [artifact_row(name, path) for name, path in artifacts],
        }
        (output / "compile-manifest.json").write_text(
            json.dumps(receipt), encoding="utf-8"
        )

    @staticmethod
    def refresh_artifact(project: Path, name: str) -> None:
        manifest_path = project / "output" / "compile-manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        row = next(item for item in manifest["artifacts"] if item["name"] == name)
        path = project / row["path"]
        if path.is_dir():
            row["file_count"] = len(
                [item for item in path.rglob("*") if item.is_file()]
            )
            row["sha256"] = validator.sha256_directory(path)
        else:
            row["bytes"] = path.stat().st_size
            row["sha256"] = validator.sha256_file(path)
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")


class CompilerDeliveryTests(unittest.TestCase):
    def _compile_all_with_stubs(self, project: Path, *, include_pptx: bool) -> tuple[dict, mock.Mock]:
        def assemble(_template: Path, _content: Path, target: Path) -> Path:
            target.write_text("<html>assembled</html>", encoding="utf-8")
            return target

        def svg_export(_index: Path, target: Path, **_kwargs) -> Path:
            target.mkdir()
            (target / "slide_01.svg").write_text(
                '<svg viewBox="0 0 1280 720"></svg>', encoding="utf-8"
            )
            return target

        def audit(_index: Path, target: Path, **_kwargs) -> dict:
            target.write_text(json.dumps({"summary": {
                "slideCount": 1, "blockerCount": 0, "reviewCount": 0,
            }}), encoding="utf-8")
            return {"summary": {"slideCount": 1, "blockerCount": 0, "reviewCount": 0}}

        def png_export(_source: Path, target: Path, **_kwargs) -> Path:
            target.mkdir(exist_ok=True)
            (target / "slide_01.png").write_bytes(b"png")
            return target

        def overview(_pngs: Path, target: Path, **_kwargs) -> Path:
            target.write_bytes(b"overview")
            return target

        def single_file(_source: Path, target: Path, **_kwargs) -> Path:
            target.write_bytes(b"artifact")
            return target

        def fidelity(_svg_pngs: Path, _browser_pngs: Path, target: Path) -> dict:
            target.write_text("{}", encoding="utf-8")
            return {"status": "pass", "review_slides": []}

        pptx_export = mock.Mock(side_effect=single_file)
        with redirect_stdout(io.StringIO()):
            with mock.patch.multiple(
                compiler,
                step_assemble=assemble,
                step_html_to_svg=svg_export,
                step_browser_dom_audit=audit,
                step_svg_to_png_browser=png_export,
                step_html_to_png_browser=png_export,
                step_png_to_overview=overview,
                step_svg_to_pdf_browser=single_file,
                step_svg_to_pptx=pptx_export,
                check_svg_images_embedded=lambda _path: None,
                verify_png_set=lambda *_args, **_kwargs: None,
                compare_render_routes=fidelity,
                collect_local_dependencies=lambda *_args: [],
            ):
                results = compiler.compile_project(project, output_format="all", include_pptx=include_pptx)
        return results, pptx_export

    def test_all_receipt_excludes_pptx_by_default_and_includes_it_on_request(self):
        with tempfile.TemporaryDirectory() as directory:
            project = DeliveryReceiptFixture.project(Path(directory))
            results, pptx_export = self._compile_all_with_stubs(project, include_pptx=False)
            manifest = json.loads((project / "output" / "compile-manifest.json").read_text())
            self.assertEqual(["svg", "png", "browser_png", "overview", "pdf"], manifest["requested_formats"])
            self.assertNotIn("pptx", results)
            pptx_export.assert_not_called()

            results, pptx_export = self._compile_all_with_stubs(project, include_pptx=True)
            manifest = json.loads((project / "output" / "compile-manifest.json").read_text())
            self.assertEqual(
                ["svg", "png", "browser_png", "overview", "pdf", "pptx"],
                manifest["requested_formats"],
            )
            self.assertIn("pptx", results)
            pptx_export.assert_called_once()

    def test_include_pptx_is_rejected_unless_all_is_selected(self):
        script = SCRIPTS_DIR / "html_compiler.py"
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / "deck"
            project.mkdir()
            with mock.patch("sys.argv", [str(script), str(project), "--format", "pdf", "--include-pptx"]):
                with redirect_stderr(io.StringIO()):
                    with self.assertRaisesRegex(SystemExit, "2"):
                        compiler.main()


class DeliveryProfileTests(unittest.TestCase):
    def test_visual_profile_passes_while_delivery_requires_pptx(self):
        with tempfile.TemporaryDirectory() as directory:
            project = DeliveryReceiptFixture.project(Path(directory))
            DeliveryReceiptFixture.write_receipt(project)

            visual_errors, _ = validator.check_compile_receipt(
                project, require_build=True, artifact_profile="visual"
            )
            delivery_errors, _ = validator.check_compile_receipt(
                project, require_build=True, artifact_profile="delivery"
            )

            self.assertEqual([], visual_errors)
            self.assertTrue(any("missing pptx" in error for error in delivery_errors))

    def test_final_delivery_gate_rejects_sources_edited_after_build(self):
        with tempfile.TemporaryDirectory() as directory:
            project = DeliveryReceiptFixture.project(Path(directory))
            DeliveryReceiptFixture.write_receipt(project, include_pptx=True)
            passed, results = validator.validate_project(
                str(project), require_build=True, artifact_profile="delivery"
            )
            self.assertTrue(passed, results["errors"])

            with (project / "template.css").open("a", encoding="utf-8") as handle:
                handle.write("\n/* changed after build */\n")
            passed, results = validator.validate_project(
                str(project), require_build=True, artifact_profile="delivery"
            )
            self.assertFalse(passed)
            self.assertTrue(any("template.css changed after compilation" in error for error in results["errors"]))

    def test_receipt_rejects_an_unsupported_schema(self):
        with tempfile.TemporaryDirectory() as directory:
            project = DeliveryReceiptFixture.project(Path(directory))
            DeliveryReceiptFixture.write_receipt(project, include_pptx=True)
            manifest_path = project / "output" / "compile-manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["schema"] = "seaslides-html-compile/v0"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            errors, _ = validator.check_compile_receipt(
                project, require_build=True, artifact_profile="delivery"
            )
            self.assertTrue(any("unsupported schema" in error for error in errors))

    def test_toolchain_requires_chart_renderer_and_pptx_package_modules(self):
        with tempfile.TemporaryDirectory() as directory:
            project = DeliveryReceiptFixture.project(Path(directory))
            DeliveryReceiptFixture.write_receipt(project, include_pptx=True)
            manifest_path = project / "output" / "compile-manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            omitted = {
                "scripts/html_to_svg/chart_renderer.mjs",
                "scripts/svg_to_pptx/pptx_builder.py",
            }
            manifest["toolchain"] = [
                row for row in manifest["toolchain"] if row["path"] not in omitted
            ]
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            errors, _ = validator.check_compile_receipt(
                project, require_build=True, artifact_profile="delivery"
            )

            for expected in omitted:
                self.assertTrue(any(expected in error for error in errors), errors)

    def test_runtime_environment_drift_is_review_not_false_current_or_blocker(self):
        with tempfile.TemporaryDirectory() as directory:
            project = DeliveryReceiptFixture.project(Path(directory))
            DeliveryReceiptFixture.write_receipt(project)
            manifest_path = project / "output" / "compile-manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["runtime_environment"] = {"node": "v0.0.0"}
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            errors, reviews = validator.check_compile_receipt(
                project, require_build=True, artifact_profile="visual"
            )

            self.assertEqual([], errors)
            self.assertTrue(any("BUILD ENVIRONMENT REVIEW" in item for item in reviews))

            manifest["runtime_environment"] = {"node": 1}
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            errors, _ = validator.check_compile_receipt(
                project, require_build=True, artifact_profile="visual"
            )
            self.assertTrue(any("runtime_environment" in item for item in errors))

    def test_semantically_bogus_png_pdf_and_pptx_cannot_pass_with_fresh_hashes(self):
        mutations = {
            "png": lambda project: (project / "output/pngs/slide_01.png").write_bytes(
                b"not a png"
            ),
            "pdf": lambda project: DeliveryReceiptFixture.write_pdf(
                project / "output/slides.pdf", page_count=1
            ),
            "pptx": lambda project: DeliveryReceiptFixture.write_pptx(
                project / "output/slides.pptx", slide_count=1
            ),
        }
        expected_markers = {
            "png": "PNG ARTIFACT INVALID",
            "pdf": "PDF ARTIFACT ROSTER INVALID",
            "pptx": "PPTX ARTIFACT ROSTER INVALID",
        }
        for artifact_name, mutate in mutations.items():
            with self.subTest(artifact=artifact_name), tempfile.TemporaryDirectory() as directory:
                project = DeliveryReceiptFixture.project(Path(directory))
                DeliveryReceiptFixture.write_receipt(project, include_pptx=True)
                mutate(project)
                DeliveryReceiptFixture.refresh_artifact(project, artifact_name)

                errors, _ = validator.check_compile_receipt(
                    project, require_build=True, artifact_profile="delivery"
                )

                self.assertTrue(
                    any(expected_markers[artifact_name] in error for error in errors),
                    errors,
                )

    def test_pdf_header_and_page_token_are_not_a_semantic_pdf(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fake.pdf"
            path.write_bytes(b"%PDF-1.4\n/Type /Page\n%%EOF\n")

            errors = validator._validate_pdf(path, 1)

            self.assertTrue(any("PDF ARTIFACT INVALID" in error for error in errors))

    def test_pptx_slide_list_must_resolve_to_the_exact_slide_roster(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "duplicate-relationship.pptx"
            DeliveryReceiptFixture.write_pptx(
                path, slide_count=2, duplicate_first_relationship=True
            )

            errors = validator._validate_pptx(path, 2)

            self.assertTrue(
                any("presentation relationship order" in error for error in errors),
                errors,
            )

    def test_pptx_delivery_requires_one_nonempty_notes_part_per_slide(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            complete = root / "complete.pptx"
            missing = root / "missing-note.pptx"
            DeliveryReceiptFixture.write_pptx(complete, slide_count=2)
            with zipfile.ZipFile(complete) as source, zipfile.ZipFile(
                missing, "w", compression=zipfile.ZIP_DEFLATED
            ) as target:
                for member in source.infolist():
                    if member.filename == "ppt/notesSlides/notesSlide2.xml":
                        continue
                    target.writestr(member, source.read(member.filename))

            errors = validator._validate_pptx(
                missing, 2, required_notes_count=2
            )

            self.assertTrue(any("PPTX NOTES ROSTER INVALID" in error for error in errors))

    def test_exact_roster_rejects_nested_extras_but_handles_more_than_99_slides(self):
        with tempfile.TemporaryDirectory() as directory:
            roster = Path(directory) / "svgs"
            roster.mkdir()
            for number in range(1, 106):
                (roster / f"slide_{number:02d}.svg").write_text("<svg/>", encoding="utf-8")
            files, errors = validator._slide_artifact_roster(roster, "svg", 105)
            self.assertEqual([], errors)
            self.assertEqual(105, len(files))

            nested = roster / "unexpected"
            nested.mkdir()
            (nested / "extra.svg").write_text("<svg/>", encoding="utf-8")
            _, errors = validator._slide_artifact_roster(roster, "svg", 105)
            self.assertTrue(any("ROSTER INVALID" in error for error in errors))

    def test_artifact_roster_rejects_symlink_children(self):
        with tempfile.TemporaryDirectory() as directory:
            roster = Path(directory) / "svgs"
            roster.mkdir()
            outside = Path(directory) / "outside.svg"
            outside.write_text("<svg/>", encoding="utf-8")
            (roster / "slide_01.svg").symlink_to(outside)

            _, errors = validator._slide_artifact_roster(roster, "svg", 1)

            self.assertTrue(any("symlink or escaping child" in error for error in errors))

    def test_review_receipts_remain_reviews_and_blockers_remain_errors(self):
        with tempfile.TemporaryDirectory() as directory:
            receipt_path = Path(directory) / "dom.json"
            base = {
                "schema": "seaslides.browser-dom-audit",
                "version": 1,
                "issues": [{"slide": 1, "severity": "review"}],
                "slides": [{"index": 1, "issues": []}],
                "summary": {
                    "status": "review",
                    "slideCount": 1,
                    "issueCount": 1,
                    "blockerCount": 0,
                    "reviewCount": 1,
                },
            }
            receipt_path.write_text(json.dumps(base), encoding="utf-8")
            errors, reviews = validator._validate_dom_receipt(receipt_path, 1)
            self.assertEqual([], errors)
            self.assertTrue(any("DOM QUALITY REVIEW" in review for review in reviews))

            base["issues"][0]["severity"] = "blocker"
            base["summary"].update({
                "status": "blocker", "blockerCount": 1, "reviewCount": 0,
            })
            receipt_path.write_text(json.dumps(base), encoding="utf-8")
            errors, reviews = validator._validate_dom_receipt(receipt_path, 1)
            self.assertTrue(any("DOM QUALITY BLOCKER" in error for error in errors))
            self.assertEqual([], reviews)

    def test_fidelity_review_roster_must_match_slide_rows(self):
        with tempfile.TemporaryDirectory() as directory:
            receipt_path = Path(directory) / "fidelity.json"
            receipt_path.write_text(json.dumps({
                "schema": "seaslides.html-render-fidelity/v1",
                "status": "review",
                "slide_count": 2,
                "review_slides": [2],
                "slides": [
                    {"slide": 1, "status": "pass"},
                    {"slide": 2, "status": "review"},
                ],
            }), encoding="utf-8")
            errors, reviews = validator._validate_fidelity_receipt(receipt_path, 2)
            self.assertEqual([], errors)
            self.assertTrue(reviews)

            payload = json.loads(receipt_path.read_text(encoding="utf-8"))
            payload["review_slides"] = [1]
            receipt_path.write_text(json.dumps(payload), encoding="utf-8")
            errors, _ = validator._validate_fidelity_receipt(receipt_path, 2)
            self.assertTrue(any("review_slides" in error for error in errors))

    def test_fidelity_blocker_status_is_compatible_but_review_only(self):
        with tempfile.TemporaryDirectory() as directory:
            receipt_path = Path(directory) / "fidelity.json"
            receipt_path.write_text(json.dumps({
                "schema": "seaslides.html-render-fidelity/v1",
                "status": "blocker",
                "slide_count": 1,
                "review_slides": [1],
                "slides": [{"slide": 1, "status": "blocker"}],
            }), encoding="utf-8")

            errors, reviews = validator._validate_fidelity_receipt(receipt_path, 1)

            self.assertEqual([], errors)
            self.assertTrue(any("RENDER FIDELITY REVIEW" in review for review in reviews))


if __name__ == "__main__":
    unittest.main()
