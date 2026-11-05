#!/usr/bin/env python3
"""Self-test for the dataset publisher (upload.py).

Runs with no arguments and no network.  It puts its own folder first on
sys.path before importing the module beside it, so the runner's working
directory cannot break the import.  Exits 0 only when every check passes.

Checks: exported names; manifest structure; module-level prepare/publish;
missing-file reporting; publish() is a local dry run with no credential and no
network call; upload is refused in Python and on the command line; the CLI dry
run works from a different working directory; and upload.py's own source text
names no networking library and no credential variable.
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from upload import DatasetPublisher, EXPECTED_FILES, prepare, publish  # noqa: E402

URL = (
    "https://huggingface.co/datasets/"
    "hivepunk-547-db38b7a4/agent-memory-viewer-readback-log"
)
UNKNOWN = "UNKNOWN"

# Built from pieces so this test file itself never contains the banned names.
BANNED_MODULES = (
    "url" + "lib",
    "requ" + "ests",
    "huggingface" + "_hub",
    "http" + ".client",
    "sock" + "et",
    "sub" + "process",
    "os" + ".system",
)
BANNED_WORDS = ("tok" + "en", "pass" + "word", "secr" + "et", "api" + "_key")


def write_source(root) -> Path:
    """Sample source folder: exactly the three expected file names."""
    src = Path(root) / "src"
    src.mkdir(parents=True, exist_ok=True)
    (src / "README.md").write_text("# sample card\n", encoding="utf-8")
    (src / "sample_records.jsonl").write_text('{"id": "L004"}\n', encoding="utf-8")
    (src / "data.csv").write_text("id,text\nL004,sample\n", encoding="utf-8")
    return src


def run_cli(args, cwd):
    return subprocess.run(
        [sys.executable, str(HERE / "upload.py")] + list(args),
        capture_output=True,
        text=True,
        cwd=str(cwd),
    )


def check_exports():
    assert isinstance(EXPECTED_FILES, tuple), type(EXPECTED_FILES)
    assert tuple(EXPECTED_FILES) == ("README.md", "sample_records.jsonl", "data.csv")
    assert DatasetPublisher.EXPECTED_FILES == EXPECTED_FILES
    assert callable(prepare) and callable(publish)


def check_manifest():
    with tempfile.TemporaryDirectory() as td:
        src = write_source(td)
        manifest = DatasetPublisher(src).prepare()
        assert manifest["url"] == URL, manifest["url"]
        assert set(manifest["files"]) == set(EXPECTED_FILES), manifest["files"]
        for name, status in manifest["files"].items():
            assert status == UNKNOWN, (name, status)
        assert manifest["missing"] == [], manifest["missing"]
        assert manifest["network_calls"] == 0


def check_module_level():
    with tempfile.TemporaryDirectory() as td:
        src = write_source(td)
        manifest = prepare(src)
        assert manifest["url"] == URL and set(manifest["files"]) == set(EXPECTED_FILES)
        result = publish(src)
        assert result["status"] == "DRY_RUN", result["status"]
        assert result["uploaded"] is False and result["network_calls"] == 0


def check_missing_files():
    with tempfile.TemporaryDirectory() as td:
        empty = Path(td) / "empty"
        empty.mkdir()
        publisher = DatasetPublisher(empty)
        assert set(publisher.missing_files()) == set(EXPECTED_FILES)
        assert publisher.present_files() == []
        manifest = publisher.prepare()
        assert set(manifest["missing"]) == set(EXPECTED_FILES)
        assert all(v is None for v in manifest["sizes"].values())


def check_dry_run_publish():
    with tempfile.TemporaryDirectory() as td:
        result = publish(write_source(td))
        assert result["uploaded"] is False
        assert result["network_calls"] == 0, result["network_calls"]
        assert result["credentials_read"] is False, result["credentials_read"]
        assert set(result["files"]) == set(EXPECTED_FILES)
        for name, status in result["files"].items():
            assert status == UNKNOWN, (name, status)
        blob = json.dumps(result).lower()
        for word in BANNED_WORDS:
            assert word not in blob, word


def check_refuse_in_python():
    with tempfile.TemporaryDirectory() as td:
        result = publish(write_source(td), upload=True)
        assert result["status"] == "REFUSED", result["status"]
        assert result["uploaded"] is False and result["network_calls"] == 0


def check_cli_refuse():
    with tempfile.TemporaryDirectory() as td:
        src = write_source(td)
        done = run_cli(["--source-dir", str(src), "--upload"], cwd=td)
        assert done.returncode == 2, done.returncode
        assert "REFUSED" in (done.stdout + done.stderr), done.stdout + done.stderr


def check_cli_dry_run_other_cwd():
    with tempfile.TemporaryDirectory() as td:
        src = write_source(td)
        other = Path(td) / "elsewhere"
        other.mkdir()
        out = other / "published.json"
        done = run_cli(["--source-dir", str(src), "--out", str(out)], cwd=other)
        assert done.returncode == 0, (done.returncode, done.stderr)
        data = json.loads(out.read_text(encoding="utf-8"))
        assert data["network_calls"] == 0, data["network_calls"]
        assert set(data["files"]) == set(EXPECTED_FILES)
        for status in data["files"].values():
            assert status == UNKNOWN, status
        print("CLI dry-run stdout (raw):")
        print(done.stdout.rstrip())


def check_source_text():
    text = (HERE / "upload.py").read_text(encoding="utf-8").lower()
    for name in BANNED_MODULES:
        assert name not in text, name
    for word in BANNED_WORDS:
        assert word not in text, word


def main() -> int:
    checks = (
        ("exported names", check_exports),
        ("manifest structure", check_manifest),
        ("module-level prepare and publish", check_module_level),
        ("missing-file reporting", check_missing_files),
        ("publish() is a local dry run", check_dry_run_publish),
        ("python publish refuses upload", check_refuse_in_python),
        ("CLI --upload refused with exit 2", check_cli_refuse),
        ("CLI dry run from another cwd", check_cli_dry_run_other_cwd),
        ("upload.py names no networking or credential symbol", check_source_text),
    )
    failures = 0
    for index, (name, func) in enumerate(checks, start=1):
        try:
            func()
        except Exception as exc:  # noqa: BLE001 - report, do not crash
            failures += 1
            print(f"FAIL {index}/{len(checks)} {name}: {exc!r}")
        else:
            print(f"PASS {index}/{len(checks)} {name}")
    if failures:
        print(f"FAIL: agent-memory-dataset-publisher self-test ({failures} failed)")
        return 1
    print(f"PASS: agent-memory-dataset-publisher self-test ({len(checks)}/{len(checks)} checks)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
