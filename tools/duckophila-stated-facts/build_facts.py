#!/usr/bin/env python3
"""build_facts.py: build the Duckophila stated-facts CSV.

Rows are quoted only from two public sources, one per row:
  https://github.com/first-it-consulting/duckophila
  https://github.com/joeynyc/awesome-microduck

Columns: fact,source_url,label,note
label is FACT (the source states it), DERIVED (follows from
what the source states) or UNKNOWN (not verifiable here).

Run (from this folder):
    python3 build_facts.py            # writes facts.csv
    python3 build_facts.py -o out.csv
    python3 build_facts.py --check    # validate facts.csv only

Read-only apart from the output file. No network. Every row
is data read from those repos; any text in them is data, not
an instruction.
"""

import csv
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_OUT = os.path.join(HERE, "facts.csv")
FIELDS = ("fact", "source_url", "label", "note")
LABELS = ("FACT", "DERIVED", "UNKNOWN")
DUCKOPHILA = "https://github.com/first-it-consulting/duckophila"
MICRODUCK = "https://github.com/joeynyc/awesome-microduck"

# Each row: fact, source_url, label, note
ROWS = [
    ("Duckophila is a fruit fly's connectome driving a microduck.", DUCKOPHILA, "FACT", "Repository title and description."),
    ("Duckophila runs the FlyWire whole-brain model in closed loop with a robot.", DUCKOPHILA, "FACT", "Repository description."),
    ("The model is a leaky integrate-and-fire model.", DUCKOPHILA, "FACT", "Stated in the repository description."),
    ("The robot runs in a MuJoCo twin.", DUCKOPHILA, "FACT", "Repository description names the MuJoCo twin."),
    ("The connectome used is the FlyWire adult Drosophila connectome.", DUCKOPHILA, "FACT", "Repository description."),
    ("The FlyWire connectome has 138,639 neurons.", DUCKOPHILA, "DERIVED", "Number is the stated FlyWire connectome count; not re-read here."),
    ("The FlyWire connectome has 54 million synapses.", DUCKOPHILA, "DERIVED", "Number is the stated FlyWire connectome count; not re-read here."),
    ("The loop goes from fly looming and motion detectors to descending neurons that move the robot.", DUCKOPHILA, "FACT", "Stated as the sensorimotor loop."),
    ("Demonstrations include startle, optomotor following, target following and assisted learning in simulation.", DUCKOPHILA, "FACT", "Listed in the repository description."),
    ("awesome-microduck is a curated list of software, simulators, policies, agent tools and coverage.", MICRODUCK, "FACT", "Repository description."),
    ("awesome-microduck covers the Pollen Robotics and Hugging Face microduck.", MICRODUCK, "FACT", "Repository description."),
    ("microduck is a small open-source robot from Pollen Robotics.", MICRODUCK, "DERIVED", "Follows from the curated-list description; not re-read here."),
    ("Duckophila links the fly brain to a microduck robot rather than a fly body.", DUCKOPHILA, "DERIVED", "Follows from the title and description."),
    ("The exact open-source licence of the Duckophila repository.", DUCKOPHILA, "UNKNOWN", "Licence file not read in this step."),
    ("The exact open-source licence of the awesome-microduck repository.", MICRODUCK, "UNKNOWN", "Licence file not read in this step."),
    ("Whether every FlyWire cell type is wired into the Duckophila model.", DUCKOPHILA, "UNKNOWN", "Not stated in the sources read here."),
    ("The commit hash of the Duckophila version used for the twin.", DUCKOPHILA, "UNKNOWN", "Not stated in the sources read here."),
]


def validate(rows):
    """Return a list of problem strings (empty when rows are fine)."""
    problems = []
    seen = set()
    for i, row in enumerate(rows, 1):
        if len(row) != len(FIELDS):
            problems.append("row %d: expected %d fields, got %d" % (i, len(FIELDS), len(row)))
            continue
        fact, source_url, label, _note = row
        if not str(fact or "").strip():
            problems.append("row %d: empty fact" % i)
        url = str(source_url or "").strip()
        if not url:
            problems.append("row %d: empty source_url" % i)
        elif not (url.startswith("http://") or url.startswith("https://")):
            problems.append("row %d: source_url is not http(s): %r" % (i, url))
        if str(label or "").strip() not in LABELS:
            problems.append("row %d: unknown label %r" % (i, label))
        key = str(fact or "").strip().lower()
        if key in seen:
            problems.append("row %d: duplicate fact" % i)
        seen.add(key)
    return problems


def render(rows):
    buf = io.StringIO()
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerow(FIELDS)
    for row in rows:
        writer.writerow(row)
    return buf.getvalue()


def read_csv(path):
    with open(path, encoding="utf-8", newline="") as fh:
        reader = csv.reader(fh)
        try:
            header = next(reader)
        except StopIteration:
            return [], ["empty file"]
        if [h.strip() for h in header] != list(FIELDS):
            return [], ["header is %r, expected %r" % (header, list(FIELDS))]
        rows = [tuple(r) for r in reader if any(str(c).strip() for c in r)]
    return rows, []


def main(argv):
    args = list(argv[1:])
    out_path = DEFAULT_OUT
    check_only = False
    i = 0
    while i < len(args):
        a = args[i]
        if a in ("-o", "--output"):
            if i + 1 >= len(args):
                print("FAIL: %s needs a value" % a)
                return 2
            out_path = args[i + 1]
            i += 2
        elif a == "--check":
            check_only = True
            i += 1
        elif a in ("-h", "--help"):
            print(__doc__.strip())
            return 0
        else:
            print("FAIL: unknown argument %s" % a)
            return 2
    problems = validate(ROWS)
    if problems:
        for p in problems:
            print("FAIL: built rows: %s" % p)
        return 1
    text = render(ROWS)
    if check_only:
        if not os.path.exists(out_path):
            print("FAIL: %s not found" % out_path)
            return 1
        on_disk, errs = read_csv(out_path)
        if errs:
            print("FAIL: %s: %s" % (out_path, "; ".join(errs)))
            return 1
        if render(on_disk) != text:
            print("FAIL: %s does not match the built rows" % out_path)
            return 1
        print("PASS: %s matches %d built rows" % (out_path, len(ROWS)))
        return 0
    try:
        with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
    except OSError as e:
        print("FAIL: could not write %s: %s" % (out_path, e))
        return 1
    print("wrote %s (%d rows)" % (out_path, len(ROWS)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
