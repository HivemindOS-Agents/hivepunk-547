#!/usr/bin/env python3
"""artifacts_index_check.py: check an ARTIFACTS.md artifact index.

Usage (from this folder):
    python3 artifacts_index_check.py                 # ./ARTIFACTS.md
    python3 artifacts_index_check.py ARTIFACTS.md
    python3 artifacts_index_check.py /path/to/ARTIFACTS.md
    python3 artifacts_index_check.py /path/to/folder  # folder/ARTIFACTS.md
    python3 artifacts_index_check.py --check FILE ...

Reads only the named index as data (no network, no publish,
writes nothing). An entry is a bullet line (`- ...`, `* ...`)
or a table row (`| ... |`) in ARTIFACTS.md. From each entry
the parser extracts:
  * URLs: any http:// or https:// token on the line, and
    markdown link targets `[text](target)`.
  * local paths: backticked path-like strings, markdown link
    targets that are not URLs/anchors, and table cells that
    look like paths (contain a `/` or end in a file extension)
    and are not URLs.

Every listed local path must exist relative to the directory
containing ARTIFACTS.md. Every listed URL must be well-formed:
http/https scheme, non-empty host, no spaces or invalid
characters, and a valid port if one is given. Reachability is
NOT checked (no network).

On success prints `ok: <file> (N entries, X local file(s),
Y URL(s))` and exits 0. Otherwise prints one
`FAIL: <file>: <problem>` line per problem and exits 1.
"""

import os
import re
import sys
import urllib.parse

URL_RE = re.compile(r"https?://[^\s<>\"'\]]+")
MD_LINK_RE = re.compile(r"\[([^\]]*)\]\(\s*([^)\s]+)(?:\s+[^)]*)?\s*\)")
BACKTICK_RE = re.compile(r"`([^`\n]+)`")
PATH_CELL_RE = re.compile(r"^(?:\.{0,2}/)?[\w.\-]+(?:/[\w.\-]+)+$|^[\w.\-]+\.(?:md|txt|py|json|csv|html?|png|jpe?g|gif|svg|pdf|zip|gz)$", re.IGNORECASE)
INVALID_URL_CHARS = set(' <>"\'{}|^`')


def _clean_url(raw):
    url = raw.strip().rstrip(",;)")
    while url.endswith(".") and "://" in url:
        # Keep a trailing dot only if it is part of the host-less path;
        # simplest safe rule: strip sentence punctuation.
        url = url[:-1]
    return url.rstrip(",;)")


def _is_path_like(cell):
    cell = cell.strip().strip("`")
    if not cell or cell.startswith(("http://", "https://", "#", "mailto:")):
        return False
    if cell in ("---", "--", "-", "|"):
        return False
    # Require slash or a known extension so plain titles are ignored.
    return bool(PATH_CELL_RE.match(cell))


def parse_entries(text):
    """Return list of dicts {line, title, files, urls}."""
    entries = []
    for lineno, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("<!--"):
            continue
        is_bullet = bool(re.match(r"^[-*+]\s+", line))
        is_table = line.startswith("|") and line.endswith("|")
        if not (is_bullet or is_table):
            continue
        if is_table:
            cells = [c.strip() for c in line.strip("|").split("|")]
            if all(re.fullmatch(r":?-{3,}:?", c or "-") for c in cells):
                continue  # separator row
            if not any(cells):
                continue
        urls = []
        for m in URL_RE.finditer(line):
            u = _clean_url(m.group(0))
            if u not in urls:
                urls.append(u)
        files = []
        for m in MD_LINK_RE.finditer(line):
            target = m.group(2).strip()
            if target.startswith(("http://", "https://")):
                t = _clean_url(target)
                if t not in urls:
                    urls.append(t)
            elif target and not target.startswith("#") and target not in files:
                files.append(target)
        for m in BACKTICK_RE.finditer(line):
            token = m.group(1).strip()
            if _is_path_like(token) and token not in files:
                files.append(token)
        if is_table:
            for cell in cells:
                for m in URL_RE.finditer(cell):
                    u = _clean_url(m.group(0))
                    if u not in urls:
                        urls.append(u)
                cleaned = cell.strip().strip("`")
                if _is_path_like(cell) and cleaned not in files:
                    files.append(cleaned)
        title = re.sub(r"^[-*+]\s+", "", line)
        title = title[:60] + ("..." if len(title) > 60 else "")
        entries.append({"line": lineno, "title": title, "files": files, "urls": urls})
    return entries


def url_problem(url):
    """Return a specific problem string, or None if well-formed."""
    bad = sorted(INVALID_URL_CHARS & set(url))
    if bad:
        return "malformed URL %r: contains invalid character(s) %s" % (url, " ".join(bad))
    try:
        parts = urllib.parse.urlparse(url)
    except ValueError as e:
        return "malformed URL %r: %s" % (url, e)
    if parts.scheme not in ("http", "https"):
        return "malformed URL %r: scheme must be http or https, got %r" % (url, parts.scheme or "(none)")
    if not parts.netloc:
        return "malformed URL %r: missing host" % url
    host = parts.hostname
    if not host:
        return "malformed URL %r: missing host" % url
    if host != "localhost" and "." not in host:
        return "malformed URL %r: host %r has no dot and is not localhost" % (url, host)
    try:
        port = parts.port
    except ValueError as e:
        return "malformed URL %r: invalid port (%s)" % (url, e)
    if port is not None and not (1 <= port <= 65535):
        return "malformed URL %r: port %d out of range" % (url, port)
    if " " in url:
        return "malformed URL %r: contains a space" % url
    return None


def check_text(text, base_dir, label="ARTIFACTS.md"):
    """Return (problems, entry_count, file_count, url_count)."""
    problems = []
    entries = parse_entries(text)
    if not entries:
        problems.append("%s: no artifact entries found (expected bullet or table entries)" % label)
        return problems, 0, 0, 0
    n_files = n_urls = 0
    for entry in entries:
        where = "%s: line %d" % (label, entry["line"])
        for path in entry["files"]:
            n_files += 1
            full = path if os.path.isabs(path) else os.path.join(base_dir, path)
            if not os.path.exists(full):
                problems.append("%s: listed local file not found: %s" % (where, path))
        for url in entry["urls"]:
            n_urls += 1
            problem = url_problem(url)
            if problem:
                problems.append("%s: %s" % (where, problem))
    return problems, len(entries), n_files, n_urls


def check_file(path):
    """Return (ok, problems, stats_string)."""
    if not os.path.exists(path):
        return False, ["%s: not found: %s" % (path, path)], ""
    if not os.path.isfile(path):
        return False, ["%s: not a file: %s" % (path, path)], ""
    try:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
    except (OSError, UnicodeError) as e:
        return False, ["%s: could not read %s: %s: %s" % (path, path, type(e).__name__, e)], ""
    base = os.path.dirname(os.path.abspath(path))
    problems, n_entries, n_files, n_urls = check_text(text, base, label=path)
    stats = "(%d entries, %d local file(s), %d URL(s))" % (n_entries, n_files, n_urls)
    return not problems, problems, stats


def resolve(args):
    if not args:
        return [os.path.join(os.getcwd(), "ARTIFACTS.md")]
    out = []
    for arg in args:
        if os.path.isdir(arg):
            out.append(os.path.join(arg, "ARTIFACTS.md"))
        else:
            out.append(arg)
    return out


def main(argv):
    args = [a for a in argv[1:] if a != "--check"]
    files = resolve(args)
    ok_all = True
    for path in files:
        ok, problems, stats = check_file(path)
        if ok:
            print("ok: %s %s" % (path, stats))
        else:
            ok_all = False
            for p in problems:
                print("FAIL: " + p)
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
