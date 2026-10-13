import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import types
import unittest
import zipfile
import xml.etree.ElementTree as ET
from contextlib import redirect_stdout
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


assemble = load_script("seaslides_html_assemble", "assemble.py")
image_analyzer = load_script("seaslides_html_image_analyzer", "analyze_images.py")
compiler = load_script("seaslides_html_compiler", "html_compiler.py")
legacy_html_to_pptx = load_script("seaslides_html_to_pptx", "html_to_pptx.py")
validator = load_script("seaslides_html_validator", "validate_project.py")

from svg_to_pptx.drawingml_styles import build_gradient_fill
from svg_to_pptx.pptx_discovery import (
    NotesFileReadError,
    find_notes_files,
    find_svg_files,
)


class AssembleTests(unittest.TestCase):
    def test_missing_local_stylesheet_is_a_controlled_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            template = '<link rel="stylesheet" href="missing.css">'
            with self.assertRaisesRegex(assemble.AssemblyError, "Local stylesheet not found"):
                assemble.inline_css(template, Path(directory))

    def test_runtime_is_injected_before_body_close(self):
        template = "<html><body><main>deck</main></body></html>"

        result = assemble.inline_runtime(template)

        marker = 'data-seaslides-runtime="deck_runtime"'
        self.assertEqual(1, result.count(marker))
        self.assertIn("SeaSlidesRuntime", result)
        self.assertLess(result.index(marker), result.lower().index("</body>"))


class AnalyzeImagesTests(unittest.TestCase):
    def test_svg_assets_use_intrinsic_dimensions(self):
        with tempfile.TemporaryDirectory() as directory:
            images = Path(directory)
            (images / "viewbox.svg").write_text(
                '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720"/>',
                encoding="utf-8",
            )
            (images / "physical.svg").write_text(
                '<svg xmlns="http://www.w3.org/2000/svg" width="10in" height="5in"/>',
                encoding="utf-8",
            )

            results = image_analyzer.analyze_images(str(images))

            self.assertEqual(
                [("physical.svg", 960, 480), ("viewbox.svg", 1280, 720)],
                [(row["filename"], row["width"], row["height"]) for row in results],
            )


class CompilerPublicationTests(unittest.TestCase):
    def test_publish_target_normalization_rejects_duplicates_and_managed_output(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / "deck"
            project.mkdir()
            duplicate = project / "custom-output"
            with self.assertRaisesRegex(RuntimeError, "must be disjoint"):
                compiler.normalize_publish_targets(
                    project, {"svg": duplicate, "pdf": duplicate}
                )
            with self.assertRaisesRegex(RuntimeError, "must be disjoint"):
                compiler.normalize_publish_targets(
                    project, {"output": project / "output", "svg": project / "output" / "svgs"}
                )
            with self.assertRaisesRegex(RuntimeError, "compiler-managed artifact"):
                compiler.resolve_output_target(
                    project, str(project / "output" / "compile-manifest.json"),
                    project / "output" / "slides.pdf",
                )
            with self.assertRaisesRegex(RuntimeError, "compiler-managed artifact"):
                compiler.resolve_output_target(
                    project, str(project / "index.html"), project / "output" / "slides.pdf",
                )
            for target in (project / "output", project / "output" / "svgs" / "custom"):
                with self.subTest(target=target):
                    with self.assertRaisesRegex(RuntimeError, "compiler-managed artifact"):
                        compiler.resolve_output_target(
                            project, str(target), project / "output" / "slides.pdf",
                        )

    def test_compile_rejects_managed_output_before_assembly(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / "deck"
            project.mkdir()
            (project / "index-template.html").write_text("{{CONTENT}}", encoding="utf-8")
            (project / "content.html").write_text("<section></section>", encoding="utf-8")
            with mock.patch.object(compiler, "step_assemble") as assemble:
                for target in (
                    project / "output" / "compile-manifest.json",
                    project / "output",
                    project / "output" / "svgs" / "custom",
                ):
                    with self.subTest(target=target):
                        with self.assertRaisesRegex(RuntimeError, "compiler-managed artifact"):
                            compiler.compile_project(
                                project, output_format="svg", output_path=str(target),
                            )
            assemble.assert_not_called()

    def test_local_dependencies_recurse_through_nested_css_and_reject_escapes(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / "deck"
            styles = project / "styles"
            images = project / "images"
            styles.mkdir(parents=True)
            images.mkdir()
            template = project / "index-template.html"
            template.write_text('<link href="styles/base.css" rel="stylesheet">', encoding="utf-8")
            base = styles / "base.css"
            nested = styles / "nested.css"
            base.write_text('@import "nested.css"; .hero { background: url("../images/bg.png"); }', encoding="utf-8")
            nested.write_text('@import url("more.css");', encoding="utf-8")
            more = styles / "more.css"
            more.write_text(
                '.x { background: url("../images/texture.png"); } '
                '@font-face { src: url("../images/font%20file.woff"); }',
                encoding="utf-8",
            )
            (images / "bg.png").write_bytes(b"bg")
            texture = images / "texture.png"
            texture.write_bytes(b"texture-v1")
            encoded = images / "font file.woff"
            encoded.write_bytes(b"font")

            dependencies = compiler.collect_local_dependencies(project, [template])
            self.assertEqual(
                {
                    base.resolve(), nested.resolve(), more.resolve(),
                    (images / "bg.png").resolve(), texture.resolve(), encoded.resolve(),
                },
                set(dependencies),
            )
            before = compiler.sha256_file(texture)
            texture.write_bytes(b"texture-v2")
            refreshed = compiler.collect_local_dependencies(project, [template])
            self.assertIn(texture.resolve(), refreshed)
            self.assertNotEqual(before, compiler.sha256_file(texture))

            nested.write_text('@import "../../outside.css";', encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "escapes the project"):
                compiler.collect_local_dependencies(project, [template])

    def test_atomic_publish_rolls_back_an_already_replaced_target(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            staged = root / "staged.txt"
            missing = root / "missing.txt"
            first_target = root / "first.txt"
            second_target = root / "second.txt"
            staged.write_text("new", encoding="utf-8")
            first_target.write_text("old-first", encoding="utf-8")
            second_target.write_text("old-second", encoding="utf-8")

            with self.assertRaisesRegex(RuntimeError, "staged artifact is missing"):
                compiler.publish_atomically(
                    [(staged, first_target), (missing, second_target)],
                    token="regression",
                )

            self.assertEqual("old-first", first_target.read_text(encoding="utf-8"))
            self.assertEqual("old-second", second_target.read_text(encoding="utf-8"))
            self.assertEqual([], list(root.glob(".*.backup-regression")))

    def test_pptx_false_success_removes_staged_file_and_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            svgs = root / "svgs"
            svgs.mkdir()
            (svgs / "slide_01.svg").write_text("<svg></svg>", encoding="utf-8")
            output = root / "slides.pptx"
            output.write_bytes(b"stale")

            fake_module = types.ModuleType("svg_to_pptx")
            fake_module.create_pptx_with_native_svg = lambda **_: False
            with mock.patch.dict(sys.modules, {"svg_to_pptx": fake_module}):
                with redirect_stdout(io.StringIO()):
                    with self.assertRaises(SystemExit):
                        compiler.step_svg_to_pptx(svgs, output)

            self.assertFalse(output.exists())

    def test_pptx_export_embeds_data_notes_for_every_slide(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            svgs = root / "svgs"
            svgs.mkdir()
            for number in (1, 2):
                (svgs / f"slide_{number:02d}.svg").write_text(
                    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720">'
                    f'<text x="80" y="120">Slide {number}</text></svg>',
                    encoding="utf-8",
                )
            content = root / "content.html"
            content.write_text(
                '<section class="slide" data-notes="First speaker note."></section>\n'
                '<section class="slide" data-notes="Second speaker note."></section>\n',
                encoding="utf-8",
            )
            output = root / "slides.pptx"

            with redirect_stdout(io.StringIO()):
                compiler.step_svg_to_pptx(svgs, output, content_html=content)

            with zipfile.ZipFile(output) as archive:
                presentation = ET.fromstring(archive.read("ppt/presentation.xml"))
                slide_size = presentation.find(
                    "{http://schemas.openxmlformats.org/presentationml/2006/main}sldSz"
                )
                self.assertIsNotNone(slide_size)
                self.assertNotIn("type", slide_size.attrib)

                note_names = sorted(
                    name for name in archive.namelist()
                    if name.startswith("ppt/notesSlides/notesSlide")
                    and name.endswith(".xml")
                )
                self.assertEqual(
                    [
                        "ppt/notesSlides/notesSlide1.xml",
                        "ppt/notesSlides/notesSlide2.xml",
                    ],
                    note_names,
                )
                self.assertIn(b"First speaker note.", archive.read(note_names[0]))
                self.assertIn(b"Second speaker note.", archive.read(note_names[1]))

            self.assertEqual([], validator._validate_pptx(output, 2, required_notes_count=2))


class SvgToPptxRegressionTests(unittest.TestCase):
    def test_svg_discovery_uses_numeric_filename_order(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            svg_dir = root / "svg_output"
            svg_dir.mkdir()
            for name in ("slide_100.svg", "slide_10.svg", "slide_2.svg", "slide_1.svg"):
                (svg_dir / name).write_text("<svg/>", encoding="utf-8")

            files, source = find_svg_files(root)

            self.assertEqual("svg_output", source)
            self.assertEqual(
                ["slide_1.svg", "slide_2.svg", "slide_10.svg", "slide_100.svg"],
                [path.name for path in files],
            )

    def test_matched_invalid_utf8_notes_raise_a_controlled_error(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            notes_dir = root / "notes"
            notes_dir.mkdir()
            notes_file = notes_dir / "slide_1.md"
            notes_file.write_bytes(b"\xff\xfe")
            svg_files = [root / "slide_1.svg"]

            with self.assertRaisesRegex(NotesFileReadError, str(notes_file)):
                find_notes_files(root, svg_files)

    def test_default_linear_gradient_is_horizontal(self):
        namespace = "{http://www.w3.org/2000/svg}"
        gradient = ET.Element(f"{namespace}linearGradient")
        ET.SubElement(
            gradient,
            f"{namespace}stop",
            {"offset": "0", "stop-color": "#ffffff"},
        )
        ET.SubElement(
            gradient,
            f"{namespace}stop",
            {"offset": "1", "stop-color": "#000000"},
        )

        xml = build_gradient_fill(gradient)

        self.assertIn('<a:lin ang="0"', xml)


class LegacyHtmlToPptxTests(unittest.TestCase):
    def test_pptx_failure_is_not_reported_as_success(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            svg_dir = root / "svgs"
            svg_dir.mkdir()
            (svg_dir / "slide_01.svg").write_text("<svg/>", encoding="utf-8")
            fake_module = types.ModuleType("svg_to_pptx")
            fake_module.create_pptx_with_native_svg = lambda **_: False
            with mock.patch.dict(sys.modules, {"svg_to_pptx": fake_module}):
                with self.assertRaisesRegex(RuntimeError, "PPTX creation did not produce"):
                    legacy_html_to_pptx.run_svg_to_pptx(svg_dir, root / "slides.pptx")

    def test_requested_png_failure_is_controlled(self):
        result = types.SimpleNamespace(returncode=1, stdout="", stderr="renderer failed")
        with mock.patch.object(legacy_html_to_pptx.subprocess, "run", return_value=result):
            with self.assertRaisesRegex(RuntimeError, "renderer failed"):
                legacy_html_to_pptx.run_svg_to_png(Path("svgs"), Path("pngs"))


class ValidateProjectTests(unittest.TestCase):
    @staticmethod
    def make_source_project(root: Path) -> Path:
        project = root / "deck"
        project.mkdir()
        (project / "index-template.html").write_text(
            "<html><body>{{CONTENT}}</body></html>", encoding="utf-8"
        )
        (project / "template.css").write_text(
            ".slide { width: 100vw; height: 100vh; }", encoding="utf-8"
        )
        (project / "demo.html").write_text(
            """
<section class="slide light" data-layout="T01" data-notes="Introduce the topic.">
  <h1>One</h1>
  <p>First point.</p>
</section>
<section class="slide dark" data-layout="T02" data-notes="Close the argument.">
  <h2>Two</h2>
  <p>Second point.</p>
</section>
""".strip(),
            encoding="utf-8",
        )
        return project

    def test_entry_and_source_only_do_not_require_build_artifacts(self):
        with tempfile.TemporaryDirectory() as directory:
            project = self.make_source_project(Path(directory))

            passed, source_result = validator.validate_project(
                str(project), entry="demo.html", source_only=True
            )
            build_passed, build_result = validator.validate_project(
                str(project), entry="demo.html", require_build=True
            )

            self.assertTrue(passed, source_result["errors"])
            self.assertNotIn("Output Files", source_result["checks"])
            self.assertNotIn("Compile Receipt", source_result["checks"])
            self.assertFalse(build_passed)
            self.assertIn("Output Files", build_result["checks"])
            self.assertTrue(
                any("BUILD MISSING" in error for error in build_result["errors"])
            )
            self.assertFalse(any("content.html does not exist" in error for error in build_result["errors"]))

            script = SCRIPTS_DIR / "validate_project.py"
            source_cli = subprocess.run(
                [
                    sys.executable,
                    str(script),
                    str(project),
                    "--entry",
                    "demo.html",
                    "--source-only",
                    "--quiet",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            build_cli = subprocess.run(
                [
                    sys.executable,
                    str(script),
                    str(project),
                    "--entry",
                    "demo.html",
                    "--require-build",
                    "--quiet",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(0, source_cli.returncode, source_cli.stderr)
            self.assertEqual("PASS", source_cli.stdout.strip())
            self.assertEqual(1, build_cli.returncode, build_cli.stderr)
            self.assertEqual("FAIL", build_cli.stdout.strip())

    def test_cli_entry_option_order_is_stable(self):
        with tempfile.TemporaryDirectory() as directory:
            project = self.make_source_project(Path(directory))
            script = SCRIPTS_DIR / "validate_project.py"
            commands = [
                [
                    sys.executable, str(script), "--entry", "demo.html", str(project),
                    "--source-only", "--quiet",
                ],
                [
                    sys.executable, str(script), str(project), "--entry", "demo.html",
                    "--source-only", "--quiet",
                ],
            ]
            results = [
                subprocess.run(command, capture_output=True, text=True, check=False)
                for command in commands
            ]
            self.assertEqual([0, 0], [result.returncode for result in results])
            self.assertEqual(["PASS", "PASS"], [result.stdout.strip() for result in results])

    def test_nested_slide_and_external_required_source_symlink_fail_source_gate(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            project = self.make_source_project(root)
            (project / "demo.html").write_text(
                '<section class="slide light" data-layout="T01" data-notes="One.">\n'
                '  <section class="slide dark" data-layout="T02" data-notes="Two."></section>\n'
                '</section>',
                encoding="utf-8",
            )
            passed, result = validator.validate_project(
                str(project), entry="demo.html", source_only=True
            )
            self.assertFalse(passed)
            self.assertTrue(any("must not nest" in error for error in result["errors"]))

            outside = root / "outside.css"
            outside.write_text(".slide {}", encoding="utf-8")
            (project / "template.css").unlink()
            (project / "template.css").symlink_to(outside)
            passed, result = validator.validate_project(
                str(project), entry="demo.html", source_only=True
            )
            self.assertFalse(passed)
            self.assertTrue(any("symlink escapes project" in error for error in result["errors"]))

    def test_project_cli_requires_an_explicit_validation_stage(self):
        with tempfile.TemporaryDirectory() as directory:
            project = self.make_source_project(Path(directory))
            script = SCRIPTS_DIR / "validate_project.py"
            missing_stage = subprocess.run(
                [sys.executable, str(script), str(project)],
                capture_output=True,
                text=True,
                check=False,
            )
            source_with_artifacts = subprocess.run(
                [
                    sys.executable, str(script), str(project), "--source-only",
                    "--artifact-profile", "current",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            strict_alias = subprocess.run(
                [sys.executable, str(script), str(project), "--source-only", "--strict"],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(2, missing_stage.returncode)
            self.assertIn("requires exactly one", missing_stage.stderr)
            self.assertEqual(2, source_with_artifacts.returncode)
            self.assertIn("requires --require-build", source_with_artifacts.stderr)
            self.assertEqual(2, strict_alias.returncode)
            self.assertIn("unrecognized arguments: --strict", strict_alias.stderr)

    def test_missing_paths_and_invalid_utf8_are_controlled_failures(self):
        script = SCRIPTS_DIR / "validate_project.py"
        missing = subprocess.run(
            [
                sys.executable, str(script), "/definitely/missing/html-project",
                "--source-only", "--json",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(1, missing.returncode, missing.stderr)
        payload = json.loads(missing.stdout)
        self.assertEqual(1, payload["error_count"])
        self.assertEqual([], payload["reviews"])
        self.assertEqual({}, payload["checks"])

        with tempfile.TemporaryDirectory() as directory:
            project = self.make_source_project(Path(directory))
            (project / "demo.html").write_bytes(b"\xff\xfe")
            passed, results = validator.validate_project(
                str(project), entry="demo.html", source_only=True
            )
            self.assertFalse(passed)
            self.assertTrue(any("not valid UTF-8" in error for error in results["errors"]))

    def test_legacy_mode_does_not_invent_a_light_dark_requirement(self):
        with tempfile.TemporaryDirectory() as directory:
            content = Path(directory) / "content.html"
            content.write_text(
                '<section class="slide" data-notes="Notes"><h1>Title</h1></section>',
                encoding="utf-8",
            )
            passed, results = validator.validate_single_file(str(content))
            self.assertTrue(passed, results["errors"])
            self.assertEqual([], results["reviews"])

    def test_pseudocode_marker_pairing_is_class_order_independent(self):
        with tempfile.TemporaryDirectory() as directory:
            project = self.make_source_project(Path(directory))
            entry = project / "demo.html"
            canonical = (
                "<pre data-kind='algorithm' class='technical pseudocode'>"
                r"\begin{algorithm}\begin{algorithmic}"
                r"\State Work\end{algorithmic}\end{algorithm}"
                "</pre>"
            )
            entry.write_text(
                entry.read_text(encoding="utf-8").replace("<p>First point.</p>", canonical),
                encoding="utf-8",
            )
            errors, reviews = validator.check_pseudocode_markup(project, "demo.html")
            self.assertEqual([], errors)
            self.assertEqual([], reviews)

            entry.write_text(
                entry.read_text(encoding="utf-8").replace(r"\end{algorithmic}", ""),
                encoding="utf-8",
            )
            _, reviews = validator.check_pseudocode_markup(project, "demo.html")
            self.assertTrue(any("algorithmic" in review for review in reviews))

    def test_tcs_profiles_and_numeric_geometry(self):
        with tempfile.TemporaryDirectory() as directory:
            project = self.make_source_project(Path(directory))
            entry = project / "demo.html"
            entry.write_text(
                entry.read_text(encoding="utf-8").replace(
                    "<p>First point.</p>",
                    '<div class="bar-fill" style="width: .5px"></div>'
                    '<div class="authoring" style="grid-template-columns: 1fr 2fr"></div>',
                ),
                encoding="utf-8",
            )

            standard_errors, standard_reviews = validator.check_tcs_compliance(
                project, "demo.html", "standard-project"
            )
            demo_errors, demo_reviews = validator.check_tcs_compliance(
                project, "demo.html", "theme-demo"
            )

            self.assertTrue(any("1 forbidden inline style" in error for error in standard_errors))
            self.assertEqual([], standard_reviews)
            self.assertEqual([], demo_errors)
            self.assertTrue(any("1 forbidden inline style" in review for review in demo_reviews))
            self.assertTrue(
                validator.is_allowed_data_inline_style(
                    '<div class="bar-fill">', "width: .5px"
                )
            )
            self.assertFalse(
                validator.is_allowed_data_inline_style(
                    '<div class="bar-fill">', "width: -5px"
                )
            )

    def test_shell_handlers_and_external_images_are_blockers(self):
        with tempfile.TemporaryDirectory() as directory:
            project = self.make_source_project(Path(directory))
            entry = project / "demo.html"
            entry.write_text(
                entry.read_text(encoding="utf-8").replace(
                    "<p>First point.</p>",
                    '<meta name="bad" content="1"><button onclick="go()">Go</button>'
                    '<img src="https://example.com/image.png">',
                ),
                encoding="utf-8",
            )
            tcs_errors, _ = validator.check_tcs_compliance(project, "demo.html")
            image_errors, _ = validator.check_image_usage(project, "demo.html")
            self.assertTrue(any("<meta>" in error for error in tcs_errors))
            self.assertTrue(any("onclick" in error for error in tcs_errors))
            self.assertTrue(any("external source" in error for error in image_errors))
            self.assertTrue(any("missing an alt" in error for error in image_errors))

    def test_missing_template_css_blocks_source_validation(self):
        with tempfile.TemporaryDirectory() as directory:
            project = self.make_source_project(Path(directory))
            (project / "template.css").unlink()
            passed, results = validator.validate_project(
                str(project), entry="demo.html", source_only=True
            )
            self.assertFalse(passed)
            self.assertTrue(any("template.css" in error for error in results["errors"]))

    def test_receipt_detects_entry_changed_after_compilation(self):
        with tempfile.TemporaryDirectory() as directory:
            project = self.make_source_project(Path(directory))
            output = project / "output"
            svgs = output / "svgs"
            svgs.mkdir(parents=True)
            (svgs / "slide_01.svg").write_text(
                '<svg viewBox="0 0 1280 720"></svg>', encoding="utf-8"
            )
            (svgs / "slide_02.svg").write_text(
                '<svg viewBox="0 0 1280 720"></svg>', encoding="utf-8"
            )
            dom_audit = output / "dom-audit.json"
            dom_audit.write_text(
                json.dumps(
                    {
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
                        "slides": [
                            {"index": 1, "issues": []},
                            {"index": 2, "issues": []},
                        ],
                    }
                ),
                encoding="utf-8",
            )
            index = project / "index.html"
            index.write_text("<html><body>compiled</body></html>", encoding="utf-8")

            input_names = ["index-template.html", "template.css", "demo.html"]
            receipt = {
                "schema": "seaslides-html-compile/v1",
                "status": "pass",
                "entry": "demo.html",
                "slide_count": 2,
                "requested_formats": ["svg"],
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
                    for name in [
                        "requirements.txt",
                        "scripts/html_compiler.py",
                        "scripts/runtime_environment.py",
                        "scripts/assemble.py",
                        "scripts/runtime/deck_runtime.js",
                        "scripts/html_to_svg/browser_dom_to_svg.mjs",
                        "scripts/html_to_svg/browser_dom_audit.mjs",
                        "scripts/html_to_svg/chart_renderer.mjs",
                        "scripts/html_to_svg/package.json",
                        "scripts/html_to_svg/package-lock.json",
                    ]
                ],
                "runtime_environment": validator.runtime_environment_fingerprint(),
                "assembled_index_sha256": validator.sha256_file(index),
                "artifacts": [
                    {
                        "name": "svg",
                        "path": "output/svgs",
                        "kind": "directory",
                        "file_count": 2,
                        "sha256": validator.sha256_directory(svgs),
                    },
                    {
                        "name": "dom_audit",
                        "path": "output/dom-audit.json",
                        "kind": "file",
                        "bytes": dom_audit.stat().st_size,
                        "sha256": validator.sha256_file(dom_audit),
                    }
                ],
            }
            (output / "compile-manifest.json").write_text(
                json.dumps(receipt), encoding="utf-8"
            )

            errors, _ = validator.check_compile_receipt(
                project, entry="demo.html", require_build=True,
                artifact_profile="current",
            )
            self.assertEqual([], errors)

            with (project / "demo.html").open("a", encoding="utf-8") as handle:
                handle.write("\n<!-- edited -->\n")

            errors, _ = validator.check_compile_receipt(
                project, entry="demo.html", require_build=True,
                artifact_profile="current",
            )
            self.assertTrue(
                any("demo.html changed after compilation" in error for error in errors),
                errors,
            )


if __name__ == "__main__":
    unittest.main()
