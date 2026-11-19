#!/usr/bin/env python3
"""stated_facts_check.py: validate a stated-facts dataset CSV.

Usage (from this folder):
    python3 stated_facts_check.py data.csv
    python3 stated_facts_check.py data.csv --allow-domain duckspace.org
    python3 stated_facts_check.py data.csv --allow-domain duckspace.org --allow-domain example.org

Required header (exact, any order tolerated but all four required):
    fact_id,topic,claim,source

Checks, per data row (line 2+ in file):
    - fact_id, topic, claim and source are non-empty after stripping
    - fact_id is unique (exact string, case-sensitive)
    - source is an http:// or https:// URL with a host containing a dot
    - if --allow-domain is given (repeatable), source host equals the
      domain or is a subdomain of it (case-insensitive)
    - claim is not a bare URL and topic contains no URL
    - no extra columns beyond the header, no missing columns

Also reported: blank lines are skipped (counted on stderr note),
duplicate claims are reported as problems (same claim text twice),
and total/valid row counts. Read-only, no network, writes nothing
except optional -o report file. Exit 0 PASS, 1 problems or bad
input, 2 usage error.
"""

import csv
import os
import re
import sys
from collections import Counter
from urllib.parse import urlparse

REQUIRED = ("fact_id", "topic", "claim", "source")
URL_RE = re.compile(r"https?://\S+", re.I)


def parse_domains(domains):
    out = []
    for d in domains or []:
        d = str(d).strip().lower().strip(".")
        if d.startswith("http://") or d.startswith("https://"):
            d = urlparse(d).hostname or d
        if d:
            out.append(d.lower())
    return out


def host_of(url):
    try:
        return (urlparse(url).hostname or "").lower()
    except ValueError:
        return ""


def is_http_url(url):
    if any(ch.isspace() for ch in url):
        return False
    try:
        p = urlparse(url)
    except ValueError:
        return False
    if p.scheme.lower() not in ("http", "https"):
        return False
    host = (p.hostname or "")
    return bool(host and "." in host)


def check_rows(rows, allowed_domains=None):
    """rows: list of dicts with _line. Return (valid_count, problems)."""
    allowed = parse_domains(allowed_domains or [])
    problems = []
    ids = []
    claims = []
    valid = 0
    for row in rows:
        line = row.get("_line", "?")
        bad = False
        vals = {k: str(row.get(k, "") or "").strip() for k in REQUIRED}
        for k in REQUIRED:
            if not vals[k]:
                problems.append("line %s: empty %s" % (line, k))
                bad = True
        if vals["fact_id"]:
            ids.append(vals["fact_id"])
        if vals["claim"]:
            claims.append(vals["claim"])
        if vals["source"] and not is_http_url(vals["source"]):
            problems.append("line %s: source is not a valid http(s) URL: %r" % (line, vals["source"]))
            bad = True
        if vals["source"] and allowed and is_http_url(vals["source"]):
            host = host_of(vals["source"])
            if not any(host == d or host.endswith("." + d) for d in allowed):
                problems.append("line %s: source host %r not in allowed domains %s" % (line, host, ", ".join(allowed)))
                bad = True
        if vals["claim"] and URL_RE.fullmatch(vals["claim"]):
            problems.append("line %s: claim is a bare URL, not a fact" % line)
            bad = True
        if vals["topic"] and URL_RE.search(vals["topic"]):
            problems.append("line %s: topic contains a URL" % line)
            bad = True
        if not bad:
            valid += 1
    for value, count in sorted(Counter(ids).items()):
        if count > 1:
            problems.append("duplicate fact_id (%d times): %s" % (count, value))
    for value, count in sorted(Counter(claims).items()):
        if count > 1:
            problems.append("duplicate claim (%d times): %r" % (count, value[:80]))
    return valid, problems


def load_csv(path):
    """Return (rows, problems, skipped_blank). Header problems are fatal-ish.

    Uses csv.reader directly: csv.DictReader silently discards blank
    lines, so they would never be counted as skipped.
    """
    problems = []
    rows = []
    skipped = 0
    with open(path, encoding="utf-8-sig", newline="") as fh:
        reader = csv.reader(fh)
        try:
            raw_header = next(reader)
        except StopIteration:
            return [], ["missing header (expected fact_id,topic,claim,source)"], 0
        headers = [h.strip() for h in raw_header]
        missing = [c for c in REQUIRED if c not in headers]
        extra = [h for h in headers if h and h not in REQUIRED]
        if missing:
            problems.append("missing column(s): %s" % ", ".join(missing))
        if extra:
            problems.append("unexpected column(s): %s" % ", ".join(extra))
        if problems:
            return [], problems, 0
        index = {name: headers.index(name) for name in REQUIRED}
        for lineno, raw in enumerate(reader, 2):
            if not raw or all(not str(v).strip() for v in raw):
                skipped += 1
                continue
            if len(raw) > len(headers):
                problems.append("line %d: extra fields beyond header" % lineno)
                continue
            vals = {k: (raw[index[k]] if index[k] < len(raw) else "") for k in REQUIRED}
            vals["_line"] = lineno
            rows.append(vals)
    if not rows and not problems:
        problems.append("no data rows found")
    return rows, problems, skipped


def check_file(path, allowed_domains=None):
    if not os.path.exists(path):
        return None, ["input file not found: %s" % path], 0
    if not os.path.isfile(path):
        return None, ["input path is not a file: %s" % path], 0
    try:
        rows, problems, skipped = load_csv(path)
    except (OSError, UnicodeError) as e:
        return None, ["could not read input: %s: %s" % (type(e).__name__, e)], 0
    except csv.Error as e:
        return None, ["invalid CSV: %s" % e], 0
    if problems and not rows:
        return {"total": 0, "valid": 0, "rows": []}, problems, skipped
    valid, row_problems = check_rows(rows, allowed_domains)
    problems.extend(row_problems)
    report = {"total": len(rows), "valid": valid, "rows": rows}
    return report, problems, skipped


def main(argv):
    args = list(argv[1:])
    input_path = None
    output_path = None
    allowed = []
    i = 0
    while i < len(args):
        arg = args[i]
        if arg in ("-o", "--output"):
            if i + 1 >= len(args):
                print("FAIL: %s needs a value" % arg)
                return 2
            output_path = args[i + 1]
            i += 2
        elif arg == "--allow-domain":
            if i + 1 >= len(args):
                print("FAIL: --allow-domain needs a value")
                return 2
            allowed.append(args[i + 1])
            i += 2
        elif arg in ("-h", "--help"):
            print(__doc__.strip())
            return 0
        elif arg.startswith("--"):
            print("FAIL: unknown option %s" % arg)
            return 2
        elif input_path is None:
            input_path = arg
            i += 1
        else:
            print("FAIL: unexpected extra argument %s" % arg)
            return 2
    if not input_path:
        print("FAIL: usage: python3 stated_facts_check.py data.csv [--allow-domain DOMAIN] [-o REPORT.txt]")
        return 2
    report, problems, skipped = check_file(input_path, allowed)
    if report is None:
        for p in problems:
            print("FAIL: %s: %s" % (input_path, p))
        return 1
    if skipped:
        print("NOTE: skipped %d blank row(s)" % skipped, file=sys.stderr)
    lines = []
    lines.append("counts: total=%d valid=%d problems=%d" % (report["total"], report["valid"], len(problems)))
    if problems:
        for p in problems:
            lines.append("FAIL: %s: %s" % (input_path, p))
        lines.append("FAIL: %s (problems: %d)" % (input_path, len(problems)))
        code = 1
    else:
        lines.append("PASS: %s (rows: %d)" % (input_path, report["total"]))
        code = 0
    text = "\n".join(lines) + "\n"
    if output_path:
        try:
            with open(output_path, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(text)
        except OSError as e:
            print("FAIL: could not write output: %s: %s" % (type(e).__name__, e))
            return 1
        print("wrote report to %s" % output_path)
    else:
        sys.stdout.write(text)
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv))
