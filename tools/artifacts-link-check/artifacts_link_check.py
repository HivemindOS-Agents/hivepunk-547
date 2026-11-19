#!/usr/bin/env python3
"""artifacts_link_check.py: check links in a supplied ARTIFACTS.md.

Usage (from this folder):
    python3 artifacts_link_check.py ARTIFACTS.md
    python3 artifacts_link_check.py ARTIFACTS.md --allow-relative

Extracts Markdown links [text](url) (including images ![alt](url))
and bare http:// or https:// URLs from the supplied file. Fenced
code blocks and inline code spans are ignored. Reports, with line
numbers: empty link targets, malformed targets (whitespace inside
the URL, a bare web address without http(s)://, or broken Markdown
link syntax), and duplicate URLs, plus counts of total / Markdown /
bare / valid / empty / duplicate / malformed links.

Relative links, anchors (#...), mailto: and tel: targets are
accepted unless --allow-relative is absent... they are always
accepted as valid format; they are simply not counted as duplicates
failures differently. Duplicates are exact URL repeats.

Read-only and format-only: no network fetch, no liveness check,
nothing is written. Exit 0 when no problems, 1 when problems or
unreadable/missing/empty input, 2 on usage error.
"""

import os
import re
import sys
from collections import Counter

FENCE = "`" * 3
MD_LINK_RE = re.compile(r"(!?)\[([^\[\]]*)\]\(([^)]*)\)")
# A Markdown link opened but never closed on the line.
MD_BROKEN_RE = re.compile(r"!?\[[^\[\]]*\]\([^)]*$")
BARE_RE = re.compile(r"https?://[^\s<>\"'\[\]()]+" )
SCHEME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
TRAILING_PUNCT = ".,;:!?"


def _strip_code(text):
    """Blank out fenced blocks and inline code, preserving line numbers."""
    out = []
    in_fence = False
    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith(FENCE) or stripped.startswith("~~~"):
            in_fence = not in_fence
            out.append("")
            continue
        if in_fence:
            out.append("")
            continue
        out.append(re.sub(r"`[^`]*`", "", line))
    return "\n".join(out)


def _clean_bare(url):
    while url and url[-1] in TRAILING_PUNCT:
        url = url[:-1]
    while url.endswith(")") and url.count("(") < url.count(")"):
        url = url[:-1]
    return url


def extract_links(text):
    """Return list of dicts: url, text, kind (markdown|bare), line (1-based)."""
    cleaned = _strip_code(text)
    links = []
    broken = []
    for lineno, line in enumerate(cleaned.splitlines(), 1):
        spans = []
        for m in MD_LINK_RE.finditer(line):
            url = m.group(3).strip()
            # Support <url> target form: [t](<url>)
            if url.startswith("<") and url.endswith(">"):
                url = url[1:-1].strip()
            links.append({"url": url, "text": m.group(2), "kind": "markdown", "line": lineno})
            spans.append(m.span())
        for m in MD_BROKEN_RE.finditer(line):
            broken.append({"url": m.group(0), "text": "", "kind": "broken", "line": lineno})
        masked = list(line)
        for a, b in spans:
            for i in range(a, min(b, len(masked))):
                masked[i] = " "
        for m in BARE_RE.finditer("".join(masked)):
            url = _clean_bare(m.group(0))
            if url:
                links.append({"url": url, "text": url, "kind": "bare", "line": lineno})
    links.extend(broken)
    links.sort(key=lambda e: (e["line"], e["url"]))
    return links


def classify(link):
    """Return 'empty', 'malformed' or 'ok' for one extracted link."""
    url = link["url"]
    if link["kind"] == "broken":
        return "malformed"
    if not url.strip():
        return "empty"
    if any(ch.isspace() for ch in url):
        return "malformed"
    if "<>" in url or "|" in url:
        return "malformed"
    # Bare links already matched http(s)://; Markdown targets may be
    # http(s) URLs, relative paths, anchors, or mailto:/tel:.
    if url.startswith(("#", "./", "../", "/")):
        return "ok"
    if SCHEME_RE.match(url):
        scheme = url.split(":", 1)[0].lower()
        if scheme in ("http", "https"):
            rest = url.split("://", 1)[1] if "://" in url else ""
            return "ok" if rest and "." in rest.split("/")[0] or rest else "malformed"
        if scheme in ("mailto", "tel"):
            return "ok" if len(url) > len(scheme) + 1 else "malformed"
        return "malformed"
    # Looks like a bare domain/path without scheme, e.g. example.com/x
    if re.match(r"^[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)+(/|$)", url):
        return "malformed"
    if re.match(r"^[A-Za-z0-9_./-]+$", url):
        return "ok"  # plain relative path like docs/page.md
    return "malformed"


def check_text(text):
    """Return (report_dict, problems_list_of_strings)."""
    links = extract_links(text)
    problems = []
    empty, malformed = [], []
    urls = []
    for link in links:
        cls = classify(link)
        link["status"] = cls
        if cls == "empty":
            empty.append(link)
            problems.append("line %d: empty link target (%s)" % (link["line"], link["kind"]))
        elif cls == "malformed":
            malformed.append(link)
            problems.append("line %d: malformed link: %r" % (link["line"], link["url"]))
        else:
            urls.append(link["url"])
    counts = Counter(urls)
    duplicates = sorted(u for u, c in counts.items() if c > 1)
    for url in duplicates:
        lines = [str(l["line"]) for l in links if l["url"] == url]
        problems.append("duplicate link (%d times, lines %s): %s" % (counts[url], ", ".join(lines), url))
    report = {
        "total": len(links),
        "markdown": sum(1 for l in links if l["kind"] == "markdown"),
        "bare": sum(1 for l in links if l["kind"] == "bare"),
        "broken": sum(1 for l in links if l["kind"] == "broken"),
        "valid": len(urls),
        "empty": len(empty),
        "malformed": len(malformed),
        "duplicates": len(duplicates),
        "duplicate_urls": duplicates,
        "links": links,
    }
    return report, problems


def check_file(path):
    """Return (report_or_None, problems). Missing/empty input is a problem."""
    if not os.path.exists(path):
        return None, ["input file not found: %s" % path]
    if not os.path.isfile(path):
        return None, ["input path is not a file: %s" % path]
    try:
        with open(path, encoding="utf-8-sig") as fh:
            text = fh.read()
    except (OSError, UnicodeError) as e:
        return None, ["could not read input: %s: %s" % (type(e).__name__, e)]
    if not text.strip():
        return None, ["input file is empty: %s" % path]
    report, problems = check_text(text)
    if report["total"] == 0:
        problems.append("no links found in %s" % path)
    return report, problems


def main(argv):
    args = list(argv[1:])
    positional = []
    for arg in args:
        if arg in ("-h", "--help"):
            print(__doc__.strip())
            return 0
        elif arg == "--allow-relative":
            continue  # relative targets are always accepted; flag kept for clarity
        elif arg.startswith("--"):
            print("FAIL: unknown option %s" % arg)
            return 2
        else:
            positional.append(arg)
    if len(positional) != 1:
        print("FAIL: usage: python3 artifacts_link_check.py ARTIFACTS.md [--allow-relative]")
        return 2
    path = positional[0]
    report, problems = check_file(path)
    if report is None:
        for p in problems:
            print("FAIL: %s: %s" % (path, p))
        return 1
    print("counts: total=%d markdown=%d bare=%d valid=%d empty=%d malformed=%d duplicates=%d" % (
        report["total"], report["markdown"], report["bare"], report["valid"],
        report["empty"], report["malformed"], report["duplicates"]))
    if problems:
        for p in problems:
            print("FAIL: %s: %s" % (path, p))
        print("FAIL: %s (problems: %d)" % (path, len(problems)))
        return 1
    print("PASS: %s (links: %d)" % (path, report["total"]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
