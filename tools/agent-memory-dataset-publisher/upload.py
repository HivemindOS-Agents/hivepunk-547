#!/usr/bin/env python3
"""agent-memory-dataset-publisher -- prepare a manifest for a three-file
folder and dry-run the publish step.

What it does
------------
Given a source folder that should hold exactly the three files named in
``EXPECTED_FILES``, this module lists what is present, what is missing and
sizes, and builds a manifest.  ``publish()`` is a *local dry run*: it makes no
network call, reads no credential, and reports every file status as the string
``UNKNOWN`` instead of inventing a result.

The ``--upload`` flag is refused on purpose with exit code 2.  Uploading is not
this tool's job: the owner's own publish play does that, under the account
``hivepunk-547-db38b7a4`` only, re-publishing the same title to update in
place.

Nothing in this file holds or reads a key, and no uploader command is run.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

DATASET_URL = (
    "https://huggingface.co/datasets/"
    "hivepunk-547-db38b7a4/agent-memory-viewer-readback-log"
)

EXPECTED_FILES = ("README.md", "sample_records.jsonl", "data.csv")
UNKNOWN = "UNKNOWN"
REFUSED = "REFUSED"


class DatasetPublisher:
    """Build a manifest and dry-run a publish. No network, no credential."""

    EXPECTED_FILES = EXPECTED_FILES
    DATASET_URL = DATASET_URL

    def __init__(self, source_dir, dataset_url: str = DATASET_URL) -> None:
        self.source_dir = Path(source_dir)
        self.dataset_url = dataset_url

    def present_files(self):
        return [n for n in self.EXPECTED_FILES if (self.source_dir / n).is_file()]

    def missing_files(self):
        return [n for n in self.EXPECTED_FILES if not (self.source_dir / n).is_file()]

    def file_sizes(self):
        sizes = {}
        for name in self.EXPECTED_FILES:
            path = self.source_dir / name
            sizes[name] = path.stat().st_size if path.is_file() else None
        return sizes

    def prepare(self) -> dict:
        """Manifest for the three files. Statuses are UNKNOWN, never guessed."""
        return {
            "url": self.dataset_url,
            "source_dir": str(self.source_dir),
            "expected_files": list(self.EXPECTED_FILES),
            "files": {name: UNKNOWN for name in self.EXPECTED_FILES},
            "present": self.present_files(),
            "missing": self.missing_files(),
            "sizes": self.file_sizes(),
            "network_calls": 0,
            "credentials_read": False,
        }

    def publish(self, upload: bool = False) -> dict:
        """Local dry run. ``upload=True`` is refused, never attempted."""
        if upload:
            return {
                "status": REFUSED,
                "reason": "upload is refused here; the owner's publish play does that",
                "url": self.dataset_url,
                "uploaded": False,
                "network_calls": 0,
                "credentials_read": False,
                "files": {name: UNKNOWN for name in self.EXPECTED_FILES},
            }
        return {
            "status": "DRY_RUN",
            "url": self.dataset_url,
            "uploaded": False,
            "network_calls": 0,
            "credentials_read": False,
            "manifest": self.prepare(),
            "files": {name: UNKNOWN for name in self.EXPECTED_FILES},
        }


def prepare(source_dir, dataset_url: str = DATASET_URL) -> dict:
    """Module-level wrapper: manifest for ``source_dir``."""
    return DatasetPublisher(source_dir, dataset_url).prepare()


def publish(source_dir, upload: bool = False, dataset_url: str = DATASET_URL) -> dict:
    """Module-level wrapper: local dry run; ``upload=True`` returns REFUSED."""
    return DatasetPublisher(source_dir, dataset_url).publish(upload=upload)


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Prepare a three-file dataset manifest; dry-run only."
    )
    parser.add_argument("--source-dir", default=".", help="folder holding the three files")
    parser.add_argument("--out", default=None, help="write the JSON result to this path")
    parser.add_argument("--dataset-url", default=DATASET_URL, help="dataset URL label")
    parser.add_argument("--dry-run", action="store_true", help="print the manifest only")
    parser.add_argument("--upload", action="store_true", help="refused; exits 2")
    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    if args.upload:
        print(
            "REFUSED: --upload is not available in this tool; the owner's publish "
            "play uploads, under hivepunk-547-db38b7a4 only."
        )
        return 2
    publisher = DatasetPublisher(args.source_dir, args.dataset_url)
    result = publisher.prepare() if args.dry_run else publisher.publish(upload=False)
    text = json.dumps(result, indent=2, sort_keys=True)
    if args.out:
        Path(args.out).write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
