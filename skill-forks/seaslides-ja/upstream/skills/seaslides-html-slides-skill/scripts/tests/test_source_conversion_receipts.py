import hashlib
import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import types
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
SOURCE_DIR = SCRIPTS_DIR / "source_to_md"
if str(SOURCE_DIR) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIR))


def load_script(module_name: str, filename: str):
    spec = importlib.util.spec_from_file_location(module_name, SOURCE_DIR / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {filename}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


receipt = load_script("seaslides_conversion_receipt", "conversion_receipt.py")
doc = load_script("seaslides_doc_to_md", "doc_to_md.py")
excel = load_script("seaslides_excel_to_md", "excel_to_md.py")
ppt = load_script("seaslides_ppt_to_md", "ppt_to_md.py")


def load_pdf_script():
    fake_aiohttp = types.ModuleType("aiohttp")

    class ClientError(Exception):
        pass

    class ClientResponseError(ClientError):
        status = 500

    fake_aiohttp.ClientError = ClientError
    fake_aiohttp.ClientResponseError = ClientResponseError
    with mock.patch.dict(sys.modules, {"aiohttp": fake_aiohttp}):
        return load_script("seaslides_pdf_to_md", "pdf_to_md.py")


def load_web_script():
    fake_requests = types.ModuleType("requests")
    fake_requests.get = lambda *args, **kwargs: None
    fake_bs4 = types.ModuleType("bs4")

    class BeautifulSoup:
        pass

    class NavigableString(str):
        pass

    class Tag:
        pass

    fake_bs4.BeautifulSoup = BeautifulSoup
    fake_bs4.NavigableString = NavigableString
    fake_bs4.Tag = Tag
    with mock.patch.dict(
        sys.modules,
        {"requests": fake_requests, "bs4": fake_bs4},
    ):
        return load_script("seaslides_web_to_md", "web_to_md.py")


pdf = load_pdf_script()
web = load_web_script()


class ConversionReceiptTests(unittest.TestCase):
    def test_converter_help_does_not_require_optional_http_dependencies(self):
        for filename in ("pdf_to_md.py", "web_to_md.py"):
            with self.subTest(filename=filename):
                result = subprocess.run(
                    [sys.executable, "-S", str(SOURCE_DIR / filename), "--help"],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertTrue(result.stdout.startswith("usage:"), result.stdout)
                self.assertEqual("", result.stderr)

    def test_pdf_converter_has_no_embedded_mineru_credential(self):
        source = (SOURCE_DIR / "pdf_to_md.py").read_text(encoding="utf-8")
        self.assertNotIn("_FALLBACK_KEY", source)
        self.assertIn('os.getenv("MINERU_API_KEY")', source)

    def test_receipt_contains_hashes_sizes_converter_and_warnings(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.txt"
            output = root / "source.md"
            source.write_bytes(b"source bytes")
            output_bytes = (
                b"# Converted\n\n"
                b"| Item |\n| --- |\n| One |\n\n"
                b"![Image](image.png)\n\n"
                b"```text\ncode\n```\n"
            )
            output.write_bytes(output_bytes)

            receipt_path = receipt.write_success_receipt(
                source_path=source,
                output_path=output,
                converter="unit-test",
                version="9.8.7",
                warnings=["degraded image"],
            )
            payload = json.loads(receipt_path.read_text(encoding="utf-8"))

            self.assertEqual("seaslides-source-conversion/v1", payload["schema"])
            self.assertEqual("pass_with_warnings", payload["status"])
            self.assertEqual(len(b"source bytes"), payload["source"]["size_bytes"])
            self.assertEqual(
                hashlib.sha256(b"source bytes").hexdigest(),
                payload["source"]["sha256"],
            )
            self.assertEqual(len(output_bytes), payload["output"]["size_bytes"])
            self.assertEqual("source.txt", payload["source"]["path"])
            self.assertEqual("source.md", payload["output"]["path"])
            self.assertEqual("unit-test", payload["converter"]["name"])
            self.assertEqual("9.8.7", payload["converter"]["version"])
            self.assertEqual(["degraded image"], payload["warnings"])
            self.assertEqual(
                {
                    "line_count": 11,
                    "heading_count": 1,
                    "table_separator_count": 1,
                    "image_reference_count": 1,
                    "fenced_code_block_count": 1,
                    "non_whitespace_chars": sum(
                        not chr(byte).isspace() for byte in output_bytes
                    ),
                },
                payload["content_profile"],
            )

    def test_empty_output_cannot_receive_a_pass_receipt(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.txt"
            output = root / "source.md"
            source.write_text("source", encoding="utf-8")
            output.write_text(" \n", encoding="utf-8")

            with self.assertRaises(receipt.ConversionReceiptError):
                receipt.write_success_receipt(
                    source_path=source,
                    output_path=output,
                    converter="unit-test",
                    version="1",
                )

            self.assertFalse(receipt.receipt_path_for(output).exists())

    def test_receipt_cannot_overwrite_source_or_output(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.txt"
            output = root / "source.md"
            source.write_text("source", encoding="utf-8")
            output.write_text("# Output\n", encoding="utf-8")

            for dangerous_path in (source, output):
                with self.subTest(path=dangerous_path.name):
                    with self.assertRaises(receipt.ConversionReceiptError):
                        receipt.write_success_receipt(
                            source_path=source,
                            output_path=output,
                            converter="unit-test",
                            version="1",
                            receipt_path=dangerous_path,
                        )

            self.assertEqual("source", source.read_text(encoding="utf-8"))
            self.assertEqual("# Output\n", output.read_text(encoding="utf-8"))

            with self.assertRaises(receipt.ConversionReceiptError):
                receipt.clear_receipt(source, protected_paths=[source])

    def test_output_must_match_converter_result(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "source.md"
            output.write_text("# Stale\n", encoding="utf-8")

            with self.assertRaises(receipt.ConversionReceiptError):
                receipt.validate_markdown_output(output, "# New\n")

    def test_partial_publish_failure_restores_old_output_and_assets(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "source.md"
            output.write_text("# Old\n", encoding="utf-8")
            assets = root / "source_files"
            assets.mkdir()
            (assets / "old.png").write_bytes(b"old")

            with receipt.OutputTransaction(output) as transaction:
                transaction.staged_output.write_text("# New\n", encoding="utf-8")
                transaction.staged_assets.mkdir()
                (transaction.staged_assets / "new.png").write_bytes(b"new")
                real_replace = receipt.os.replace
                calls = 0

                def fail_before_install(source, destination):
                    nonlocal calls
                    calls += 1
                    if calls == 3:
                        raise OSError("simulated publish failure")
                    return real_replace(source, destination)

                with mock.patch.object(
                    receipt.os, "replace", side_effect=fail_before_install
                ):
                    with self.assertRaises(OSError):
                        transaction.publish("# New\n")

            self.assertEqual("# Old\n", output.read_text(encoding="utf-8"))
            self.assertEqual(b"old", (assets / "old.png").read_bytes())
            self.assertFalse((assets / "new.png").exists())


class LocalConverterReceiptTests(unittest.TestCase):
    def test_source_mutation_rejects_staged_output(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, output = root / "page.html", root / "page.md"
            source.write_text("<p>before</p>", encoding="utf-8")
            output.write_text("# Old\n", encoding="utf-8")

            def fake_convert(path, destination, _warnings):
                destination.write_text("# New\n", encoding="utf-8")
                path.write_text("<p>after</p>", encoding="utf-8")
                return "# New\n"

            with mock.patch.object(doc, "_convert_html", side_effect=fake_convert), redirect_stdout(io.StringIO()):
                self.assertEqual("", doc.convert_to_markdown(str(source), str(output)))
            self.assertEqual("# Old\n", output.read_text(encoding="utf-8"))
            self.assertFalse(receipt.receipt_path_for(output).exists())

    def test_receipt_failure_rolls_back_markdown_and_assets(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, output = root / "page.html", root / "page.md"
            source.write_text("<p>source</p>", encoding="utf-8")
            output.write_text("# Old\n", encoding="utf-8")
            old_assets = root / "page_files"
            old_assets.mkdir(); (old_assets / "old.png").write_bytes(b"old")

            def fake_convert(_path, destination, _warnings):
                destination.write_text("# New\n", encoding="utf-8")
                assets = destination.parent / "page_files"; assets.mkdir()
                (assets / "new.png").write_bytes(b"new")
                return "# New\n"

            with mock.patch.object(doc, "_convert_html", side_effect=fake_convert), mock.patch.object(doc, "write_success_receipt", side_effect=OSError("disk full")), redirect_stdout(io.StringIO()):
                self.assertEqual("", doc.convert_to_markdown(str(source), str(output)))
            self.assertEqual("# Old\n", output.read_text(encoding="utf-8"))
            self.assertTrue((old_assets / "old.png").exists())
            self.assertFalse((old_assets / "new.png").exists())

    def test_success_replaces_and_removes_old_assets(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, output = root / "page.html", root / "page.md"
            source.write_text("<p>source</p>", encoding="utf-8")
            (root / "page_files").mkdir()

            def fake_convert(_path, destination, _warnings):
                destination.write_text("# New\n", encoding="utf-8")
                return "# New\n"

            with mock.patch.object(doc, "_convert_html", side_effect=fake_convert), redirect_stdout(io.StringIO()):
                self.assertEqual("# New\n", doc.convert_to_markdown(str(source), str(output)))
            self.assertFalse((root / "page_files").exists())
    def test_document_success_writes_default_receipt(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "page.html"
            output = root / "page.md"
            source.write_text("<p>Source</p>", encoding="utf-8")

            def fake_convert(_source, destination, _warnings):
                destination.write_text("# Converted\n", encoding="utf-8")
                return "# Converted\n"

            with mock.patch.object(doc, "_convert_html", side_effect=fake_convert):
                with redirect_stdout(io.StringIO()):
                    result = doc.convert_to_markdown(str(source), str(output))

            self.assertEqual("# Converted\n", result)
            payload = json.loads(
                receipt.receipt_path_for(output).read_text(encoding="utf-8")
            )
            self.assertEqual("pass", payload["status"])
            self.assertEqual("doc_to_md", payload["converter"]["name"])

    def test_document_empty_result_clears_stale_pass_and_never_prints_ok(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "page.html"
            output = root / "page.md"
            source.write_text("<html></html>", encoding="utf-8")
            stale = receipt.receipt_path_for(output)
            stale.write_text('{"status":"pass"}', encoding="utf-8")

            def fake_empty(_source, destination, _warnings):
                destination.write_text("\n", encoding="utf-8")
                return "\n"

            stream = io.StringIO()
            with mock.patch.object(doc, "_convert_html", side_effect=fake_empty):
                with redirect_stdout(stream):
                    result = doc.convert_to_markdown(str(source), str(output))

            self.assertEqual("", result)
            self.assertFalse(stale.exists())
            self.assertNotIn("[OK] Saved Markdown", stream.getvalue())

    def test_document_missing_source_clears_stale_receipt(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "missing.md"
            stale = receipt.receipt_path_for(output)
            stale.write_text('{"status":"pass"}', encoding="utf-8")

            with redirect_stdout(io.StringIO()):
                result = doc.convert_to_markdown(str(root / "missing.docx"), str(output))

            self.assertEqual("", result)
            self.assertFalse(stale.exists())

    def test_document_no_receipt_mode_removes_stale_receipt(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "page.html"
            output = root / "page.md"
            source.write_text("<p>Source</p>", encoding="utf-8")
            stale = receipt.receipt_path_for(output)
            stale.write_text('{"status":"pass"}', encoding="utf-8")

            def fake_convert(_source, destination, _warnings):
                destination.write_text("# Converted\n", encoding="utf-8")
                return "# Converted\n"

            with mock.patch.object(doc, "_convert_html", side_effect=fake_convert):
                with redirect_stdout(io.StringIO()):
                    result = doc.convert_to_markdown(
                        str(source), str(output), emit_receipt=False
                    )

            self.assertEqual("# Converted\n", result)
            self.assertFalse(stale.exists())

    def test_custom_receipt_mode_clears_old_default_and_custom_receipts(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "page.html"
            output = root / "page.md"
            custom = root / "custom.json"
            source.write_text("<p>Source</p>", encoding="utf-8")
            receipt.receipt_path_for(output).write_text(
                '{"status":"pass"}', encoding="utf-8"
            )
            custom.write_text('{"status":"pass"}', encoding="utf-8")

            def fake_empty(_source, destination, _warnings):
                destination.write_text("\n", encoding="utf-8")
                return "\n"

            with mock.patch.object(doc, "_convert_html", side_effect=fake_empty):
                with redirect_stdout(io.StringIO()):
                    result = doc.convert_to_markdown(
                        str(source), str(output), receipt_path=str(custom)
                    )

            self.assertEqual("", result)
            self.assertFalse(receipt.receipt_path_for(output).exists())
            self.assertFalse(custom.exists())

    def test_local_converter_clis_exit_nonzero_on_failed_conversion(self):
        cases = (
            (doc, "doc_to_md.py", "convert_to_markdown", "missing.docx"),
            (excel, "excel_to_md.py", "convert_to_markdown", "missing.xlsx"),
            (
                ppt,
                "ppt_to_md.py",
                "convert_presentation_to_markdown",
                "missing.pptx",
            ),
        )
        for module, program, function_name, source_name in cases:
            with self.subTest(program=program):
                with mock.patch.object(module, function_name, return_value=""):
                    with mock.patch.object(sys, "argv", [program, source_name]):
                        with redirect_stdout(io.StringIO()):
                            with self.assertRaises(SystemExit) as raised:
                                module.main()
                self.assertEqual(1, raised.exception.code)

    def test_excel_exception_is_a_controlled_failure_without_receipt(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "book.xlsx"
            output = root / "book.md"
            source.write_bytes(b"not-a-workbook")

            with mock.patch.object(excel, "_convert_excel", side_effect=ValueError("bad zip")):
                with redirect_stdout(io.StringIO()):
                    result = excel.convert_to_markdown(str(source), str(output))

            self.assertEqual("", result)
            self.assertFalse(receipt.receipt_path_for(output).exists())

    def test_excel_success_writes_default_receipt(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "book.xlsx"
            output = root / "book.md"
            source.write_bytes(b"workbook")

            def fake_convert(_source, destination, **_kwargs):
                destination.write_text("# Workbook\n", encoding="utf-8")
                return "# Workbook\n"

            with mock.patch.object(excel, "_convert_excel", side_effect=fake_convert):
                with redirect_stdout(io.StringIO()):
                    result = excel.convert_to_markdown(str(source), str(output))

            self.assertEqual("# Workbook\n", result)
            payload = json.loads(
                receipt.receipt_path_for(output).read_text(encoding="utf-8")
            )
            self.assertEqual("excel_to_md", payload["converter"]["name"])
            self.assertEqual(1, payload["content_profile"]["heading_count"])

    def test_powerpoint_success_writes_receipt_and_empty_batch_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "deck.pptx"
            output = root / "deck.md"
            source.write_bytes(b"presentation")

            def fake_convert(_source, destination, _warnings):
                destination.write_text("# Deck\n", encoding="utf-8")
                return "# Deck\n"

            with mock.patch.object(
                ppt, "_convert_presentation_to_markdown", side_effect=fake_convert
            ):
                with redirect_stdout(io.StringIO()):
                    result = ppt.convert_presentation_to_markdown(
                        str(source), str(output)
                    )

            self.assertEqual("# Deck\n", result)
            payload = json.loads(
                receipt.receipt_path_for(output).read_text(encoding="utf-8")
            )
            self.assertEqual("ppt_to_md", payload["converter"]["name"])
            empty = root / "empty"
            empty.mkdir()
            with redirect_stdout(io.StringIO()):
                self.assertFalse(ppt.process_directory(str(empty)))


class PdfConverterReceiptTests(unittest.TestCase):
    def test_explicit_pymupdf_success_is_marked_degraded(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "paper.pdf"
            output = root / "paper.md"
            source.write_bytes(b"%PDF test")

            def fake_extract(_source, destination, **_kwargs):
                Path(destination).write_text("# Extracted\n", encoding="utf-8")
                return "# Extracted\n"

            with mock.patch.object(pdf, "extract_pdf_to_markdown", side_effect=fake_extract):
                with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                    result = pdf.convert_pdf(
                        str(source), str(output), backend="pymupdf"
                    )

            self.assertEqual("# Extracted\n", result)
            payload = json.loads(
                receipt.receipt_path_for(output).read_text(encoding="utf-8")
            )
            self.assertEqual("pass_with_warnings", payload["status"])
            self.assertEqual("pdf_to_md", payload["converter"]["name"])
            self.assertTrue(payload["warnings"])

    def test_pdf_main_returns_nonzero_when_converter_returns_empty(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "paper.pdf"
            source.write_bytes(b"%PDF test")
            argv = ["pdf_to_md.py", str(source), "--backend", "pymupdf"]

            with mock.patch.object(pdf, "convert_pdf", return_value=""):
                with mock.patch.object(sys, "argv", argv):
                    self.assertEqual(1, pdf.main())

    def test_pdf_empty_result_removes_stale_pass_receipt(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "paper.pdf"
            output = root / "paper.md"
            source.write_bytes(b"%PDF test")
            stale = receipt.receipt_path_for(output)
            stale.write_text('{"status":"pass"}', encoding="utf-8")

            with mock.patch.object(pdf, "extract_pdf_to_markdown", return_value=""):
                with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                    result = pdf.convert_pdf(
                        str(source), str(output), backend="pymupdf"
                    )

            self.assertEqual("", result)
            self.assertFalse(stale.exists())


class WebConverterReceiptTests(unittest.TestCase):
    @staticmethod
    def metadata():
        return {
            "title": "Page",
            "date": "",
            "description": "",
            "author": "",
            "source_url": "https://example.test/page",
        }

    def test_web_success_hashes_fetched_source(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "page.md"
            html = "<html><body>source</body></html>"

            with mock.patch.object(web, "fetch_url", return_value=html), \
                    mock.patch.object(web, "BeautifulSoup", return_value=object()), \
                    mock.patch.object(web, "extract_metadata", return_value=self.metadata()), \
                    mock.patch.object(web, "find_main_content", return_value=object()), \
                    mock.patch.object(web, "download_and_rewrite_images", return_value=0), \
                    mock.patch.object(
                        web, "simple_html_to_markdown_traversal", return_value="Body text"
                    ):
                with redirect_stdout(io.StringIO()):
                    success, _, error = web.process_url(
                        "https://example.test/page", str(output)
                    )

            self.assertTrue(success, error)
            payload = json.loads(
                receipt.receipt_path_for(output).read_text(encoding="utf-8")
            )
            self.assertEqual("url", payload["source"]["kind"])
            self.assertEqual(len(html.encode("utf-8")), payload["source"]["size_bytes"])
            self.assertEqual("web_to_md", payload["converter"]["name"])

    def test_web_receipt_uses_raw_bytes_and_final_url(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "page.md"
            raw = b"<html>\xff</html>"
            with mock.patch.object(web, "fetch_url", return_value=(raw, "https://example.test/final", "<html>decoded</html>")), \
                    mock.patch.object(web, "BeautifulSoup", return_value=object()), \
                    mock.patch.object(web, "extract_metadata", return_value=self.metadata()), \
                    mock.patch.object(web, "find_main_content", return_value=object()), \
                    mock.patch.object(web, "download_and_rewrite_images", return_value=0), \
                    mock.patch.object(web, "simple_html_to_markdown_traversal", return_value="Body"):
                with redirect_stdout(io.StringIO()):
                    success, _, error = web.process_url("https://example.test/request", str(output))
            self.assertTrue(success, error)
            source = json.loads(receipt.receipt_path_for(output).read_text(encoding="utf-8"))["source"]
            self.assertEqual(hashlib.sha256(raw).hexdigest(), source["sha256"])
            self.assertEqual("https://example.test/final", source["uri"])
            self.assertEqual("https://example.test/request", source["requested_uri"])

    def test_web_automatic_same_title_uses_stable_url_suffix(self):
        with tempfile.TemporaryDirectory() as directory:
            old_dir = web.CONFIG["output_dir"]
            web.CONFIG["output_dir"] = directory
            web.CONFIG.pop("_reserved_outputs", None)
            try:
                Path(directory, "Page.md").write_text("old", encoding="utf-8")
                final_url = "https://example.test/final-a"
                with mock.patch.object(web, "fetch_url", return_value=(b"<html>x</html>", final_url, "<html>x</html>")), \
                        mock.patch.object(web, "BeautifulSoup", return_value=object()), \
                        mock.patch.object(web, "extract_metadata", return_value=self.metadata()), \
                        mock.patch.object(web, "find_main_content", return_value=object()), \
                        mock.patch.object(web, "download_and_rewrite_images", return_value=0), \
                        mock.patch.object(web, "simple_html_to_markdown_traversal", return_value="Body"):
                    with redirect_stdout(io.StringIO()):
                        success, _, error = web.process_url("https://example.test/request-a")
                self.assertTrue(success, error)
                suffix = hashlib.sha256(final_url.encode("utf-8")).hexdigest()[:10]
                self.assertTrue(Path(directory, f"Page_{suffix}.md").exists())
            finally:
                web.CONFIG["output_dir"] = old_dir
                web.CONFIG.pop("_reserved_outputs", None)

    def test_web_empty_body_fails_and_removes_stale_pass(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "page.md"
            stale = receipt.receipt_path_for(output)
            stale.write_text('{"status":"pass"}', encoding="utf-8")

            with mock.patch.object(web, "fetch_url", return_value="<html></html>"), \
                    mock.patch.object(web, "BeautifulSoup", return_value=object()), \
                    mock.patch.object(web, "extract_metadata", return_value=self.metadata()), \
                    mock.patch.object(web, "find_main_content", return_value=object()), \
                    mock.patch.object(web, "download_and_rewrite_images", return_value=0), \
                    mock.patch.object(
                        web, "simple_html_to_markdown_traversal", return_value=""
                    ):
                with redirect_stdout(io.StringIO()):
                    success, _, _ = web.process_url(
                        "https://example.test/page", str(output)
                    )

            self.assertFalse(success)
            self.assertFalse(stale.exists())
            self.assertFalse(
                any(path.name.startswith(".page.md.") for path in Path(directory).iterdir())
            )

    def test_web_main_exits_nonzero_when_any_url_fails(self):
        argv = ["web_to_md.py", "https://example.test/fail"]
        with mock.patch.object(
            web,
            "process_url",
            return_value=(False, "https://example.test/fail", "fetch failed"),
        ):
            with mock.patch.object(sys, "argv", argv):
                with redirect_stdout(io.StringIO()):
                    with self.assertRaises(SystemExit) as raised:
                        web.main()
        self.assertEqual(1, raised.exception.code)


if __name__ == "__main__":
    unittest.main()
