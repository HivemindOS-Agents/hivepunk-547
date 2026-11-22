#!/usr/bin/env python3
"""Validator and CLI for agent-memory research rows (rows.csv).
No network. Usage:
  python3 agent_memory_rows.py --check [rows.csv]
  python3 agent_memory_rows.py [rows.csv]
Exit 0 when valid, 1 when invalid, 2 on bad arguments.
"""
import csv, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
COLUMNS = ["row_id", "subject", "claim", "label", "source_url", "observed_date"]
LABELS = {"FACT", "DERIVED", "UNKNOWN"}
SUBJECT = "rohitg00/agentmemory"
ALLOWED = {
    "https://github.com/rohitg00/agentmemory",
    "https://github.com/rohitg00/agentmemory/blob/main/README.md",
    "https://github.com/rohitg00/agentmemory/blob/HEAD/eval/README.md",
    "https://github.com/rohitg00/agentmemory/releases",
    "https://api.github.com/repos/rohitg00/agentmemory/commits?per_page=50&since=2026-10-23T05:42:15.012Z",
}
DATE = "2026-11-22"
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
def validate(rows):
    problems, seen = [], set()
    for i, r in enumerate(rows, 1):
        if len(r) != 6:
            problems.append("row %d: expected 6 fields got %d" % (i, len(r))); continue
        rid, subj, claim, label, url, date = r
        if not rid.strip(): problems.append("row %d: empty row_id" % i)
        if rid in seen: problems.append("row %d: duplicate row_id %r" % (i, rid))
        seen.add(rid)
        if subj != SUBJECT: problems.append("row %d: bad subject %r" % (i, subj))
        if not claim.strip(): problems.append("row %d: empty claim" % i)
        if label not in LABELS: problems.append("row %d: unknown label %r" % (i, label))
        if not url.strip(): problems.append("row %d: empty source_url" % i)
        elif not url.startswith("https://"): problems.append("row %d: source_url not http(s) %r" % (i, url))
        elif url not in ALLOWED: problems.append("row %d: source outside allowed set %r" % (i, url))
        if not DATE_RE.match(date): problems.append("row %d: observed_date not YYYY-MM-DD %r" % (i, date))
        elif date != DATE: problems.append("row %d: observed_date %r != %s" % (i, date, DATE))
    return problems
def read_csv(path):
    rows, errs = [], []
    try:
        with open(path, newline="", encoding="utf-8") as fh:
            reader = csv.reader(fh)
            header = next(reader, None)
            if header != COLUMNS: errs.append("header %r != %r" % (header, COLUMNS))
            for row in reader:
                if row: rows.append(tuple(row))
    except FileNotFoundError:
        errs.append("file not found: %s" % path)
    return rows, errs
def render(rows):
    import io
    buf = io.StringIO(); w = csv.writer(buf, lineterminator="\n")
    w.writerow(COLUMNS); w.writerows(rows); return buf.getvalue()
def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    check = "--check" in argv; argv = [a for a in argv if a != "--check"]
    if len(argv) > 1 or (argv and argv[0].startswith("-")):
        print("usage: agent_memory_rows.py [--check] [rows.csv]"); return 2
    path = argv[0] if argv else os.path.join(HERE, "rows.csv")
    rows, errs = read_csv(path); problems = errs + validate(rows)
    if problems:
        for p in problems: print("FAIL: " + p)
        return 1
    print("PASS: %d rows valid" % len(rows)); return 0
if __name__ == "__main__":
    sys.exit(main())
