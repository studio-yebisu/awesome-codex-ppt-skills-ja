import hashlib
import importlib.util
import json
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
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


validator = load_script("seaslides_source_receipt_validator", "validate_project.py")
inventory = load_script("seaslides_source_receipt_inventory", "source_inventory.py")


def fingerprint(path: Path) -> dict:
    data = path.read_bytes()
    return {
        "kind": "file",
        "path": path.name,
        "sha256": hashlib.sha256(data).hexdigest(),
        "size_bytes": len(data),
    }


class SourceReceiptValidationTests(unittest.TestCase):
    def make_receipt(self, root: Path, *, source_kind: str = "file") -> tuple[Path, dict]:
        sources = root / "sources"
        sources.mkdir(parents=True)
        output = sources / "converted.md"
        output.write_text("# Converted\n", encoding="utf-8")
        payload = {
            "schema": "seaslides-source-conversion/v1",
            "status": "pass",
            "converter": {"name": "unit-test", "version": "1"},
            "warnings": [],
            "output": fingerprint(output),
        }
        if source_kind == "file":
            source = sources / "original.txt"
            source.write_text("original", encoding="utf-8")
            payload["source"] = fingerprint(source)
        else:
            payload["source"] = {
                "kind": "url",
                "uri": "https://example.com/article",
                "sha256": "a" * 64,
                "size_bytes": 42,
            }
        receipt = sources / "converted.md.receipt.json"
        receipt.write_text(json.dumps(payload), encoding="utf-8")
        return receipt, payload

    def receipt_errors(self, root: Path) -> list[str]:
        return validator.check_source_conversion_receipts(root)[0]

    def test_no_receipt_is_valid_and_source_only_checks_existing_receipts(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "sources").mkdir()
            self.assertEqual([], self.receipt_errors(root))

            _, payload = self.make_receipt(root / "with-receipt")
            payload["status"] = "failed"
            receipt = root / "with-receipt" / "sources" / "converted.md.receipt.json"
            receipt.write_text(json.dumps(payload), encoding="utf-8")
            self.assertTrue(self.receipt_errors(root / "with-receipt"))
            _, result = validator.validate_project(
                str(root / "with-receipt"), source_only=True
            )
            self.assertTrue(result["checks"]["Source Conversion Receipts"]["errors"])

    def test_valid_relative_local_and_url_receipts(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_receipt(root)
            self.assertEqual([], self.receipt_errors(root))

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_receipt(root, source_kind="url")
            self.assertEqual([], self.receipt_errors(root))

    def test_stale_output_and_local_source_are_blockers(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_receipt(root)
            (root / "sources" / "converted.md").write_text("changed", encoding="utf-8")
            self.assertTrue(any("output changed" in error for error in self.receipt_errors(root)))

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_receipt(root)
            (root / "sources" / "original.txt").write_text("changed", encoding="utf-8")
            self.assertTrue(any("source changed" in error for error in self.receipt_errors(root)))

    def test_converter_and_warning_contract_separates_review_from_invalid_receipts(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            receipt, payload = self.make_receipt(root)
            payload["status"] = "pass_with_warnings"
            payload["warnings"] = ["table extraction needs review"]
            receipt.write_text(json.dumps(payload), encoding="utf-8")
            errors, reviews = validator.check_source_conversion_receipts(root)
            self.assertEqual([], errors)
            self.assertTrue(any("SOURCE CONVERSION REVIEW" in item for item in reviews))

        invalid_cases = (
            lambda payload: payload["converter"].update({"version": ""}),
            lambda payload: payload.update({"warnings": ["unexpected warning"]}),
            lambda payload: payload.update({"status": "pass_with_warnings", "warnings": []}),
            lambda payload: payload.update({"warnings": ["same", "same"]}),
        )
        for mutate in invalid_cases:
            with self.subTest(mutation=mutate), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                receipt, payload = self.make_receipt(root)
                mutate(payload)
                receipt.write_text(json.dumps(payload), encoding="utf-8")
                self.assertTrue(self.receipt_errors(root))

    def test_receipt_io_errors_and_invalid_utf8_do_not_escape(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            receipt, _ = self.make_receipt(root)
            receipt.write_bytes(b"\xff\xfe")
            errors = self.receipt_errors(root)
            self.assertTrue(any("SOURCE RECEIPT INVALID" in error for error in errors))

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _, payload = self.make_receipt(root)
            output = root / "sources" / "converted.md"
            with mock.patch.object(
                validator, "sha256_file", side_effect=OSError("permission denied")
            ):
                matches, error = validator._fingerprint_matches(output, payload["output"])
            self.assertFalse(matches)
            self.assertIn("permission denied", error)

    def test_malformed_schema_status_path_escape_and_url_metadata_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            sources = root / "sources"
            sources.mkdir()
            (sources / "bad.receipt.json").write_text("{not json", encoding="utf-8")
            self.assertTrue(any("SOURCE RECEIPT INVALID" in error for error in self.receipt_errors(root)))

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            receipt, payload = self.make_receipt(root)
            payload["schema"] = "wrong"
            payload["status"] = "pending"
            payload["output"]["sha256"] = "bad"
            payload["output"]["size_bytes"] = True
            payload["source"]["path"] = "../../outside.txt"
            receipt.write_text(json.dumps(payload), encoding="utf-8")
            errors = self.receipt_errors(root)
            self.assertTrue(any("unsupported schema" in error for error in errors))
            self.assertTrue(any("status must be" in error for error in errors))
            self.assertTrue(any("sha256" in error for error in errors))
            self.assertTrue(any("size_bytes" in error for error in errors))
            self.assertTrue(any("escapes sources/" in error for error in errors))

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            receipt, payload = self.make_receipt(root, source_kind="url")
            payload["source"]["uri"] = ""
            receipt.write_text(json.dumps(payload), encoding="utf-8")
            self.assertTrue(any("source.uri" in error for error in self.receipt_errors(root)))

    def test_inventory_excludes_receipt_names_and_content(self):
        with tempfile.TemporaryDirectory() as directory:
            sources = Path(directory)
            (sources / "notes.md").write_text("# Notes", encoding="utf-8")
            (sources / "notes.md.receipt.json").write_text(
                '{"secret": "receipt-only"}', encoding="utf-8"
            )
            report = inventory.build_inventory(sources)
            self.assertIn("sources/notes.md", report)
            self.assertNotIn("receipt.json", report)
            self.assertNotIn("receipt-only", report)


if __name__ == "__main__":
    unittest.main()
