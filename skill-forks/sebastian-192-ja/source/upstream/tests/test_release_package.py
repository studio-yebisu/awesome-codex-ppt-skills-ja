import json
import subprocess
import sys
import zipfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_manifest_packaged_zip_is_installable(tmp_path):
    manifest = yaml.safe_load((ROOT / "manifest.yaml").read_text(encoding="utf-8"))
    archive = tmp_path / "release.zip"
    # Exercise the same file selection and archive layout as the release workflow.
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as output:
        for name in manifest["files"]:
            output.write(ROOT / name, "slidemuse/" + name)
    bundle = tmp_path / "bundle"
    with zipfile.ZipFile(archive) as released:
        released.extractall(bundle)
    completed = subprocess.run(
        [sys.executable, str(bundle / "slidemuse" / "install.py"), "--client", "codex",
         "--home", str(tmp_path / "home"), "--skip-deps", "--json"],
        check=True, capture_output=True, text=True,
    )
    result = json.loads(completed.stdout)
    installed = Path(result["target"])
    installed_manifest = yaml.safe_load((installed / "manifest.yaml").read_text(encoding="utf-8"))
    assert installed_manifest["version"] == manifest["version"]
    assert (installed / "docs/cli.md").is_file()
    assert (installed / "docs/cli.en.md").is_file()
    assert (installed / "README.md").is_file()
    assert (installed / "docs/guide.md").is_file()
    assert (installed / "LICENSE").is_file()
    diagnosed = subprocess.run(
        [sys.executable, str(installed / "slidemuse.py"), "doctor", "--json"],
        check=True, capture_output=True, text=True,
    )
    assert json.loads(diagnosed.stdout)["status"] in ("pass", "warning")
    subprocess.run(
        [sys.executable, str(installed / "slidemuse.py"), "validate",
         str(installed / "examples" / "page-spec.example.json"), "--strict"],
        check=True, capture_output=True, text=True,
    )
    sample = installed / "showcase" / "editable-irena"
    assert (sample / "decks" / "editable.pptx").is_file()
    rebuilt = tmp_path / "sample-rebuilt"
    subprocess.run(
        [sys.executable, str(installed / "slidemuse.py"), "sample", "--verify", "--output", str(rebuilt)],
        check=True, capture_output=True, text=True,
    )
    report = json.loads((rebuilt / "reproduction.json").read_text(encoding="utf-8"))
    assert report["status"] == "pass"
    assert len(report["decks"]) == 6
