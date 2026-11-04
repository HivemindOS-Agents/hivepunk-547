#!/usr/bin/env python3
"""Self‑test for viewer_fetch.

The test creates a temporary fixture directory with JSON files expected by
viewer_fetch, runs the tool with a dummy dataset id, then compares the JSON output
to the expected values.  It prints a PASS message and the raw stdout/stderr of the
single viewer_fetch invocation.
"""
import json
import os
import pathlib
import subprocess
import sys
import tempfile


def main() -> None:
    dataset_id = "dummy/dataset"
    with tempfile.TemporaryDirectory() as tmp_dir:
        fixture_dir = pathlib.Path(tmp_dir) / "fixtures"
        fixture_dir.mkdir()
        # Create expected fixture files
        (fixture_dir / "splits.json").write_text(
            json.dumps({"splits": {"train": [1, 2]}, "configurations": ["default"]}),
            encoding="utf-8",
        )
        (fixture_dir / "is_valid.json").write_text(json.dumps({"valid": True}), encoding="utf-8")
        (fixture_dir / "size.json").write_text(json.dumps({"size": 42}), encoding="utf-8")
        (fixture_dir / "rows.json").write_text(json.dumps({"size": 100}), encoding="utf-8")

        output_file = pathlib.Path(tmp_dir) / "out.json"
        cmd = [
            sys.executable,
            "viewer_fetch.py",
            "--dataset",
            dataset_id,
            "--output",
            str(output_file),
            "--fixture-dir",
            str(fixture_dir),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        # Read the JSON produced by viewer_fetch
        if not output_file.exists():
            print("FAILED: viewer_fetch did not produce output file")
            sys.exit(1)
        data = json.loads(output_file.read_text(encoding="utf-8"))
        expected = {
            "config": "default",
            "split": "train",
            "valid": True,
            "num_rows": 42,
            "num_rows_total": 100,
        }
        if data != expected:
            print("FAILED: output JSON differs")
            print("Expected:", expected)
            print("Got:", data)
            sys.exit(1)

        # If we reach here, test passed
        print("PASS: viewer_fetch output matches expected")
        print("Viewer_fetch stdout:")
        print(result.stdout.rstrip())
        print("Viewer_fetch stderr:")
        print(result.stderr.rstrip())
        print("Viewer_fetch exit code:", result.returncode)
        sys.exit(0)


if __name__ == "__main__":
    main()
