import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
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


manager_module = load_script("seaslides_html_project_manager", "project_manager.py")
project_utils_module = load_script("seaslides_html_project_utils", "project_utils.py")
source_inventory_module = load_script("seaslides_html_source_inventory", "source_inventory.py")


class BatchValidateCliTests(unittest.TestCase):
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
        (project / "content.html").write_text(
            """
<section class="slide light" data-layout="T01" data-notes="Introduce the topic.">
  <h1>One</h1><p>First point.</p>
</section>
""".strip(),
            encoding="utf-8",
        )
        return project

    def test_json_mode_stays_valid_json_with_no_projects_and_export(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            report = root / "report.txt"
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS_DIR / "batch_validate.py"),
                    "--dir",
                    str(root),
                    "--source-only",
                    "--json",
                    "--export",
                    str(report),
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual([], json.loads(result.stdout))
            self.assertTrue(report.is_file())
            self.assertIn("Report exported to:", result.stderr)

    def test_source_only_passes_without_compiled_artifacts(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_source_project(root)
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS_DIR / "batch_validate.py"),
                    "--dir", str(root), "--source-only", "--json",
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertTrue(payload[0]["passed"], payload)
            self.assertEqual("source-only", payload[0]["validation_mode"])
            self.assertFalse(payload[0]["build_required"])

    def test_require_build_fails_without_a_current_receipt(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_source_project(root)
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS_DIR / "batch_validate.py"),
                    "--dir", str(root), "--require-build", "--json",
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(1, result.returncode, result.stderr)
            self.assertFalse(payload[0]["passed"])
            self.assertEqual("build-visual", payload[0]["validation_mode"])
            self.assertTrue(payload[0]["build_required"])
            self.assertTrue(any("BUILD RECEIPT MISSING" in error for error in payload[0]["errors"]))
            self.assertFalse((root / "deck" / "index.html").exists())

    def test_source_only_and_require_build_are_mutually_exclusive(self):
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS_DIR / "batch_validate.py"),
                "--source-only", "--require-build",
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(2, result.returncode)
        self.assertIn("not allowed with argument", result.stderr)

    def test_mode_is_required_and_legacy_assembly_flags_are_rejected(self):
        script = str(SCRIPTS_DIR / "batch_validate.py")
        for legacy_args in ([], ["--no-assemble"], ["--strict"]):
            result = subprocess.run(
                [sys.executable, script, *legacy_args],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(2, result.returncode)
            self.assertIn("--source-only", result.stderr)


class SourceInventoryAndProjectDiscoveryTests(unittest.TestCase):
    def test_source_count_and_inventory_ignore_receipts_hidden_and_temporary_files(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / "deck"
            sources = project / "sources"
            (sources / ".cache").mkdir(parents=True)
            (sources / "notes.md").write_text("Useful source", encoding="utf-8")
            (sources / "compile.receipt.json").write_text("{}", encoding="utf-8")
            (sources / "partial.md.tmp").write_text("partial", encoding="utf-8")
            (sources / "~$lock.md").write_text("lock", encoding="utf-8")
            (sources / ".cache" / "hidden.md").write_text("hidden", encoding="utf-8")

            info = project_utils_module.get_project_info(str(project))
            report = source_inventory_module.build_inventory(sources)

            self.assertEqual(1, info["source_count"])
            self.assertIn("notes.md", report)
            self.assertNotIn("compile.receipt.json", report)
            self.assertNotIn("partial.md.tmp", report)
            self.assertNotIn("hidden.md", report)

    def test_unreadable_markdown_is_reported_without_crashing(self):
        with tempfile.TemporaryDirectory() as directory:
            sources = Path(directory)
            (sources / "unreadable.md").write_text("content", encoding="utf-8")
            original_read_text = Path.read_text

            def controlled_read(path, *args, **kwargs):
                if path.name == "unreadable.md":
                    raise OSError("permission denied")
                return original_read_text(path, *args, **kwargs)

            with mock.patch.object(
                source_inventory_module.Path, "read_text", controlled_read
            ):
                report = source_inventory_module.build_inventory(sources)

            self.assertIn("## Source Read Warnings", report)
            self.assertIn("unreadable.md", report)

    def test_inventory_and_source_count_skip_external_symlinks(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            sources = root / "deck" / "sources"
            sources.mkdir(parents=True)
            outside = root / "outside.md"
            outside.write_text("outside", encoding="utf-8")
            (sources / "linked.md").symlink_to(outside)

            report = source_inventory_module.build_inventory(sources)
            info = project_utils_module.get_project_info(str(sources.parent))

            self.assertIn("Skipped symlink outside", report)
            self.assertNotIn("### Markdown Files", report)
            self.assertEqual(0, info["source_count"])

    def test_project_discovery_excludes_partial_and_output_directories(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            partial = root / "partial"
            partial.mkdir()
            (partial / "template.css").write_text("", encoding="utf-8")
            (root / "notes").mkdir()
            (root / "notes" / "content_design_spec.md").write_text(
                "reference only", encoding="utf-8"
            )
            output = root / "output"
            output.mkdir()
            for name in ("content.html", "index-template.html", "template.css"):
                (output / name).write_text("", encoding="utf-8")
            project = root / "deck_20260101"
            for name in ("sources", "assets", "output"):
                (project / name).mkdir(parents=True, exist_ok=True)

            discovered = project_utils_module.find_all_projects(str(root))

            self.assertEqual([project], discovered)


class ProjectManagerTests(unittest.TestCase):
    def test_exact_name_and_help_are_explicit(self):
        script = SCRIPTS_DIR / "project_manager.py"
        help_result = subprocess.run(
            [sys.executable, str(script), "--help"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, help_result.returncode)
        self.assertIn("--exact-name", help_result.stdout)

        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory) / "projects"
            result = subprocess.run(
                [
                    sys.executable, str(script), "init", "stable deck",
                    "--dir", str(base), "--exact-name",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertTrue((base / "stable_deck").is_dir())

    def test_init_sanitizes_project_name_without_escaping_base_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base = root / "projects"
            manager = manager_module.ProjectManager(str(base))

            project = Path(manager.init_project("../../outside"))

            self.assertTrue(project.is_dir())
            self.assertEqual(base.resolve(), project.parent.resolve())
            self.assertTrue(project.name.startswith("outside_"))
            self.assertIn("content.html", (project / "README.md").read_text(encoding="utf-8"))

    def test_copy_theme_copies_only_current_html_inputs(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / "deck"
            project.mkdir()

            result = manager_module.ProjectManager().copy_theme(
                str(project), "soft-pastel"
            )

            self.assertEqual("html", result["category"])
            self.assertEqual({"index-template.html", "template.css"}, set(result["copied"]))
            self.assertFalse((project / "output").exists())
            self.assertFalse((project / "demo.html").exists())

    def test_failed_url_import_removes_partial_output_and_record(self):
        class FailingManager(manager_module.ProjectManager):
            def _import_url(self, url, markdown_path):
                markdown_path.write_text("partial", encoding="utf-8")
                raise RuntimeError("network failed")

        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / "deck"
            project.mkdir()

            summary = FailingManager().import_sources(
                str(project), ["https://example.com/article"]
            )

            self.assertEqual([], summary["archived"])
            self.assertEqual([], summary["markdown"])
            self.assertEqual(1, len(summary["skipped"]))
            self.assertEqual([], list((project / "sources").iterdir()))

    def test_wechat_import_uses_the_receipt_aware_python_converter(self):
        manager = manager_module.ProjectManager()
        with mock.patch.object(manager, "_run_tool") as run_tool:
            manager._import_url(
                "https://mp.weixin.qq.com/s/example", Path("article.md")
            )

        command = run_tool.call_args.args[0]
        self.assertEqual(sys.executable, command[0])
        self.assertEqual("web_to_md.py", Path(command[1]).name)
        self.assertNotIn("web_to_md.cjs", " ".join(command))

    def test_import_defaults_to_copy_even_for_repo_internal_sources(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            project = root / "deck"
            project.mkdir()
            source = root / "source.md"
            source.write_text("Source", encoding="utf-8")
            summary = manager_module.ProjectManager().import_sources(
                str(project), [str(source)]
            )

            self.assertTrue(source.is_file())
            self.assertEqual([str(project / "sources" / "source.md")], summary["archived"])

    def test_init_rejects_unknown_or_incomplete_options(self):
        script = SCRIPTS_DIR / "project_manager.py"
        for option in ("--format", "ppt169", "--dir"):
            command = [sys.executable, str(script), "init", "deck", option]
            result = subprocess.run(command, capture_output=True, text=True, check=False)
            self.assertEqual(1, result.returncode)
            self.assertIn("[ERROR]", result.stdout)

    def test_import_cli_returns_nonzero_for_skipped_source(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / "deck"
            project.mkdir()
            result = subprocess.run(
                [
                    sys.executable, str(SCRIPTS_DIR / "project_manager.py"),
                    "import-sources", str(project), str(project / "missing.md"),
                ],
                capture_output=True, text=True, check=False,
            )
            self.assertEqual(1, result.returncode)
            self.assertIn("[WARN] Imported sources with failures", result.stdout)
            self.assertIn("[ERROR] One or more requested sources", result.stdout)


if __name__ == "__main__":
    unittest.main()
