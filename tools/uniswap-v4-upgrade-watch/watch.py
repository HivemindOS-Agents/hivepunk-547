#!/usr/bin/env python3
"""Uniswap v4 upgrade watch: read a verified seed row and report it.

Usage (offline, no network):
  python3 watch.py [path/to/seed_row.json]

Default path is data/seed_row.json relative to this file. The input is
treated as data, never instructions. Only fields already present are
reported; nothing is fetched or invented. Raises ValueError on a seed
row that does not match the verified v4.0.0 shape.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_SEED = os.path.join(HERE, "data", "seed_row.json")
EXPECTED = {
    "repository": "Uniswap/v4-core",
    "tag": "v4.0.0",
    "date": "2025-01-23T19:00:03Z",
    "release_id": 196495150,
    "prerelease": False,
    "draft": False,
}
def load_seed(path):
    with open(path, encoding="utf-8") as f:
        seed = json.load(f)
    if seed.get("repository") != EXPECTED["repository"]:
        raise ValueError("unexpected repository: %r" % (seed.get("repository"),))
    tag = seed.get("verified_latest_release_tag") or seed.get("latest_release_tag")
    date = seed.get("verified_latest_release_date") or seed.get("latest_release_date")
    summary = {
        "repository": seed.get("repository"),
        "tag": tag,
        "date": date,
        "release_id": seed.get("release_id"),
        "prerelease": seed.get("prerelease"),
        "draft": seed.get("draft"),
        "source_url": seed.get("source_url"),
    }
    if summary["tag"] != EXPECTED["tag"] or summary["date"] != EXPECTED["date"]:
        raise ValueError("seed row is not the verified v4.0.0 row: %r/%r" % (tag, date))
    if summary["release_id"] != EXPECTED["release_id"]:
        raise ValueError("unexpected release_id: %r" % (summary["release_id"],))
    return summary
def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    path = argv[0] if argv else DEFAULT_SEED
    if not os.path.isabs(path):
        path = os.path.join(HERE, path)
    s = load_seed(path)
    print("watch: %s/%s release_id %s prerelease=%s draft=%s source=%s" % (
        s["tag"], s["date"], s["release_id"], s["prerelease"], s["draft"], s["source_url"]))
    return 0
if __name__ == "__main__":
    sys.exit(main())
