import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
HTML_TO_SVG_DIR = SCRIPTS_DIR / "html_to_svg"
FIXTURES_DIR = HTML_TO_SVG_DIR / "test-fixtures"
RUNTIME_PATH = SCRIPTS_DIR / "runtime" / "deck_runtime.js"


def browser_test_available() -> bool:
    return bool(
        shutil.which("node")
        and (HTML_TO_SVG_DIR / "node_modules" / "playwright").exists()
    )


@unittest.skipUnless(browser_test_available(), "Node Playwright dependencies are not installed")
class BrowserContractTests(unittest.TestCase):
    def test_text_continuity_and_theme_owned_font_roles_are_review_only(self):
        with tempfile.TemporaryDirectory() as directory:
            receipt = Path(directory) / "dom-audit.json"
            result = subprocess.run(
                [
                    "node",
                    str(HTML_TO_SVG_DIR / "browser_dom_audit.mjs"),
                    str(FIXTURES_DIR / "dom-audit-text-contracts.html"),
                    "-o",
                    str(receipt),
                    "--timeout",
                    "30000",
                ],
                cwd=HTML_TO_SVG_DIR,
                capture_output=True,
                text=True,
                timeout=45,
                check=False,
            )
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            report = json.loads(receipt.read_text(encoding="utf-8"))
            self.assertEqual(0, report["summary"]["blockerCount"])
            by_code = {
                code: sorted(issue["slide"] for issue in report["issues"] if issue["code"] == code)
                for code in {issue["code"] for issue in report["issues"]}
            }
            self.assertEqual([1], by_code.get("text_continuity_review"))
            self.assertEqual([1], by_code.get("font_role_size_review"))

    def test_decorative_svg_canvas_do_not_mask_meaningful_overflow(self):
        with tempfile.TemporaryDirectory() as directory:
            receipt = Path(directory) / "dom-audit.json"
            result = subprocess.run(
                [
                    "node",
                    str(HTML_TO_SVG_DIR / "browser_dom_audit.mjs"),
                    str(FIXTURES_DIR / "dom-audit-decorative-media.html"),
                    "-o",
                    str(receipt),
                    "--timeout",
                    "30000",
                ],
                cwd=HTML_TO_SVG_DIR,
                capture_output=True,
                text=True,
                timeout=45,
                check=False,
            )
            self.assertEqual(2, result.returncode, result.stdout + result.stderr)
            report = json.loads(receipt.read_text(encoding="utf-8"))
            blockers = [issue for issue in report["issues"] if issue["severity"] == "blocker"]
            self.assertEqual([2], sorted({issue["slide"] for issue in blockers}))
            self.assertEqual(["content_outside_canvas"], sorted({issue["code"] for issue in blockers}))

    def test_runtime_keyboard_reduced_motion_and_settlement_in_chromium(self):
        runtime = RUNTIME_PATH.read_text(encoding="utf-8")
        runtime_block = (
            '<script data-seaslides-runtime="deck_runtime">\n'
            + runtime
            + "\n</script>"
        )
        base_style = (
            "<style>html,body,#deck{margin:0;width:1280px;height:720px;overflow:hidden}"
            ".slide{width:1280px;height:720px}</style>"
        )
        slides = (
            '<main id="deck"><section class="slide"><h1>One</h1></section>'
            '<section class="slide"><h1>Two</h1></section></main>'
        )
        runtime_owned = f"<!doctype html><html><head>{base_style}</head><body>{slides}{runtime_block}</body></html>"
        theme_script = (
            "<script>document.addEventListener('keydown',function(event){"
            "if(event.key==='Escape'){document.getElementById('overview').dataset.open='true';}});</script>"
        )
        theme_owned = (
            f'<!doctype html><html><head>{base_style}</head><body>{slides}'
            '<section id="overview" hidden data-open="false"></section>'
            f"{theme_script}{runtime_block}</body></html>"
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            runtime_html = root / "runtime-owned.html"
            theme_html = root / "theme-owned.html"
            runtime_html.write_text(runtime_owned, encoding="utf-8")
            theme_html.write_text(theme_owned, encoding="utf-8")
            result = subprocess.run(
                [
                    "node",
                    str(FIXTURES_DIR / "runtime-contract-smoke.mjs"),
                    str(runtime_html),
                    str(theme_html),
                ],
                cwd=HTML_TO_SVG_DIR,
                capture_output=True,
                text=True,
                timeout=45,
                check=False,
            )
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn("runtime contract smoke passed", result.stdout)


if __name__ == "__main__":
    unittest.main()
