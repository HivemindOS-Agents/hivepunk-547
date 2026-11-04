#!/usr/bin/env python3
"""Small command‑line tool to fetch four Hugging Face Dataset Viewer endpoints.

Usage
-----
    python3 viewer_fetch.py --dataset my-dataset          # real network
    python3 viewer_fetch.py --dataset my-dataset \
          --fixture-dir fixtures --output out.json    # offline test

The tool writes one JSON file containing the four read‑back values or the
string ``UNKNOWN`` when a request fails or the expected field is missing.

Version
-------
Only the logic needed for the "splits", "is‑valid", "size" and "rows"
endpoints is implemented.  It purposely keeps the implementation minimal.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from pathlib import Path

# Endpoint map: logical name -> path fragment
ENDPOINTS = {
    "splits": "/viewer/splits",
    "is_valid": "/viewer/is-valid",
    "size": "/viewer/size",
    "rows": "/viewer/rows",
}

# Default values used when a request fails or the expected field is missing
UNKNOWN = "UNKNOWN"

# Helper that performs the HTTP GET or reads a fixture file

def _fetch(dataset_id: str, endpoint: str, fixture_dir: Path | None = None) -> dict:
    if fixture_dir is not None:
        try:
            json_path = fixture_dir / f"{endpoint}.json"
            with json_path.open("r", encoding="utf-8") as fh:
                data = json.load(fh)
            return data
        except FileNotFoundError:
            # Simulate a network error if fixture missing
            raise
    # Normal network mode
    url = f"https://datasets-server.huggingface.co/dataset/{dataset_id}{ENDPOINTS[endpoint]}"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status != 200:
                raise urllib.error.HTTPError(url, resp.status, resp.reason, resp.headers, None)
            body = resp.read().decode("utf-8")
            return json.loads(body)
    except urllib.error.URLError:
        raise
    except Exception:
        raise


def _extract_values(dataset_id: str, fixture_dir: Path | None = None) -> dict:
    values: dict[str, object] = {}

    # 1. /viewer/splits – expect JSON with "splits" and "configurations"
    try:
        data = _fetch(dataset_id, "splits", fixture_dir)
        splits = data.get("splits")
        confs = data.get("configurations")
        if splits and isinstance(splits, (list, dict)) and confs and isinstance(confs, list):
            # If splits is dict, take first key; if list, take first item.
            if isinstance(splits, dict):
                split = next(iter(splits))
            else:
                split = splits[0]
            config = confs[0] if confs else UNKNOWN
            values["config"] = config
            values["split"] = split
        else:
            values["config"] = UNKNOWN
            values["split"] = UNKNOWN
    except Exception:
        values["config"] = UNKNOWN
        values["split"] = UNKNOWN

    # 2. /viewer/is-valid – expect JSON with "valid"
    try:
        data = _fetch(dataset_id, "is_valid", fixture_dir)
        if isinstance(data, dict) and "valid" in data:
            values["valid"] = bool(data["valid"])
        else:
            values["valid"] = UNKNOWN
    except Exception:
        values["valid"] = UNKNOWN

    # 3. /viewer/size – expect JSON with "size"
    try:
        data = _fetch(dataset_id, "size", fixture_dir)
        if isinstance(data, dict) and "size" in data:
            values["num_rows"] = int(data["size"])
        else:
            values["num_rows"] = UNKNOWN
    except Exception:
        values["num_rows"] = UNKNOWN

    # 4. /viewer/rows – expect JSON with "size"
    try:
        data = _fetch(dataset_id, "rows", fixture_dir)
        if isinstance(data, dict) and "size" in data:
            values["num_rows_total"] = int(data["size"])
        else:
            values["num_rows_total"] = UNKNOWN
    except Exception:
        values["num_rows_total"] = UNKNOWN

    return values


def write_output(values: dict, output_path: Path) -> None:
    with output_path.open("w", encoding="utf-8") as fh:
        json.dump(values, fh, indent=2, sort_keys=True)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Fetch Dataset Viewer read‑back values.")
    parser.add_argument("--dataset", required=True, help="Hugging Face dataset id (owner/dataset)")
    parser.add_argument("--output", default="viewer.json", help="JSON output file path")
    parser.add_argument("--fixture-dir", help="Read fixture files instead of making network calls")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    fixture_dir = Path(args.fixture_dir) if args.fixture_dir else None
    values = _extract_values(args.dataset, fixture_dir)
    write_output(values, Path(args.output))
    sys.exit(0)


if __name__ == "__main__":
    main()
