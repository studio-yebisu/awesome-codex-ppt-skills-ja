import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1]


def load_script(module_name: str, filename: str):
    spec = importlib.util.spec_from_file_location(module_name, SCRIPTS_DIR / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {filename}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


project_utils = load_script("seaslides_html_project_utils", "project_utils.py")
project_manager = load_script("seaslides_html_project_manager_utils", "project_manager.py")


class HtmlProjectUtilsTests(unittest.TestCase):
    def test_init_structure_is_valid_with_later_step_warnings(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(project_manager.ProjectManager(directory).init_project("deck"))

            valid, errors, warnings = project_utils.validate_project_structure(str(project))

            self.assertTrue(valid)
            self.assertEqual([], errors)
            self.assertEqual(
                {
                    "Missing index-template.html (copied during theme selection, Step 3)",
                    "Missing template.css (copied during theme selection, Step 3)",
                    "Missing content.html (created during authoring, Step 6)",
                    "Missing design specification file (suggested: content_design_spec.md)",
                },
                set(warnings),
            )

    def test_complete_html_project_reports_html_inputs_and_directories(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / "deck_20260101"
            for dirname in ("sources", "assets", "output"):
                (project / dirname).mkdir(parents=True, exist_ok=True)
            for filename in ("index-template.html", "template.css", "content.html", "index.html", "content_design_spec.md"):
                (project / filename).write_text("fixture", encoding="utf-8")
            (project / "sources" / "brief.md").write_text("brief", encoding="utf-8")

            info = project_utils.get_project_info(str(project))
            valid, errors, warnings = project_utils.validate_project_structure(str(project))

            self.assertEqual(3, info["html_count"])
            self.assertEqual(["content.html", "index-template.html", "index.html"], info["html_files"])
            self.assertTrue(info["has_theme_files"])
            self.assertTrue(info["has_content"])
            self.assertTrue(info["has_index_html"])
            self.assertTrue(info["has_source"])
            self.assertEqual(1, info["source_count"])
            self.assertTrue(info["has_sources_dir"])
            self.assertTrue(info["has_assets_dir"])
            self.assertTrue(info["has_output_dir"])
            self.assertNotIn("typ_count", info)
            self.assertTrue(valid)
            self.assertEqual([], errors)
            self.assertEqual([], warnings)

    def test_discovery_uses_html_markers_not_typst_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            html_project = root / "html_deck"
            html_project.mkdir()
            (html_project / "content.html").write_text("fixture", encoding="utf-8")
            typst_only = root / "typst_deck"
            typst_only.mkdir()
            (typst_only / "main.typ").write_text("fixture", encoding="utf-8")

            projects = project_utils.find_all_projects(str(root))

            self.assertEqual([html_project], projects)

    def test_info_cli_uses_html_fields(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / "deck_20260101"
            for dirname in ("sources", "assets", "output"):
                (project / dirname).mkdir(parents=True, exist_ok=True)
            for filename in ("index-template.html", "template.css", "content.html"):
                (project / filename).write_text("fixture", encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "project_manager.py"), "info", str(project)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn("HTML files: 2", result.stdout)
            self.assertIn("Theme shell: Yes", result.stdout)
            self.assertIn("Content file: Yes", result.stdout)
            self.assertNotIn("Typst", result.stdout)

    def test_validate_cli_identifies_itself_as_nonfinal(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(project_manager.ProjectManager(directory).init_project("deck"))

            result = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "project_manager.py"), "validate", str(project)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn("Project structure check:", result.stdout)
            self.assertIn("not the final source or build gate", result.stdout)
            self.assertIn("validate_project.py", result.stdout)


if __name__ == "__main__":
    unittest.main()
