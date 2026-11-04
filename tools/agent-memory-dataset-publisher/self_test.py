#!/usr/bin/env python3
"""Self‑test for the DatasetPublisher.

The test verifies that the publisher reproduces the expected manifest
structure when run with a temporary source directory containing the
required three files.
"""
import os
import shutil
import tempfile
from pathlib import Path

from upload import DatasetPublisher

# ---------------------------------------------------------------------------
# Helper that creates a minimal source directory
# ---------------------------------------------------------------------------

def create_source(tmpdir: Path) -> Path:
    src = tmpdir / "src"
    src.mkdir()
    # Write minimal files – content does not matter for this test.
    for name in DatasetPublisher.EXPECTED_FILES:
        (src / name).write_text(f"{name} content", encoding="utf-8")
    return src

# ---------------------------------------------------------------------------
# Test cases
# ---------------------------------------------------------------------------

def test_manifest_structure():
    with tempfile.TemporaryDirectory() as td:
        src = create_source(Path(td))
        publisher = DatasetPublisher(src)
        manifest = publisher.prepare()
        assert manifest["url"] == f"https://huggingface.co/datasets/hivepunk-547-db38b7a4/agent-memory-viewer-readback-log"
        assert set(manifest["files"]) == set(DatasetPublisher.EXPECTED_FILES)
        for status in manifest["files"].values():
            assert status == "UNKNOWN"

# ---------------------------------------------------------------------------
# Run tests
# ---------------------------------------------------------------------------

def main():
    try:
        test_manifest_structure()
    except AssertionError as exc:
        print("FAIL:", exc)
        exit(1)
    print("PASS: dataset publisher manifest structure")
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
