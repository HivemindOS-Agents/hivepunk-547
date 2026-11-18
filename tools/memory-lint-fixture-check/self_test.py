#!/usr/bin/env python3
"""Self-test for memory-lint-fixture-check.

Run from this folder with no arguments and no network. Imports
memory_lint_check, then checks it on synthetic fixtures in a
temp directory: valid JSON/JSONL, missing fields, duplicate
ids, empty prompts, unsafe paths, empty file, and CLI exit
codes. Exits 0 only if all checks pass.
"""

import contextlib
import io
import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))


class Fail(Exception):
    pass


def check(cond, msg):
    if not cond:
        raise Fail(msg)


def import_tool():
    sys.dont_write_bytecode = True
    if HERE not in sys.path:
        sys.path.insert(0, HERE)
    try:
        return __import__("memory_lint_check")
    except Exception as e:
        raise Fail("could not import memory_lint_check: %s: %s" % (type(e).__name__, e))


def write(root, name, text):
    path = os.path.join(root, name)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)
    return path


def main():
    try:
        mod = import_tool()
        checks = []
        with tempfile.TemporaryDirectory() as tmp:
            valid = write(tmp, "valid.json", json.dumps([
                {"id": "recall-1", "prompt": "What did I say?", "expected": "You said hello."},
                {"id": "recall-2", "prompt": "Summarise the note.", "expected": ["It was about memory.", "Short."], "path": "notes/a.md"},
                {"id": "recall-3", "prompt": "Anything else?", "expect": "No."},
            ]))
            ok, problems, notes, counts = mod.check(valid)
            check(ok and problems == [] and counts == {"fixtures": 3, "valid": 3, "invalid": 0}, "valid: %r %r" % (problems, counts))
            checks.append("valid JSON list passes with counts 3/3/0")

            wrapped = write(tmp, "wrapped.json", json.dumps({"fixtures": [
                {"id": "a", "prompt": "p", "expected": "e"},
            ]}))
            ok, problems, notes, counts = mod.check(wrapped)
            check(ok and counts["fixtures"] == 1, "wrapped: %r %r" % (problems, counts))
            checks.append("wrapped fixtures object passes")

            jsonl = write(tmp, "valid.jsonl", "\n".join([
                json.dumps({"id": "j1", "prompt": "p1", "expected": "e1"}),
                "",
                json.dumps({"id": "j2", "prompt": "p2", "output": "e2"}),
            ]) + "\n")
            ok, problems, notes, counts = mod.check(jsonl)
            check(ok and counts == {"fixtures": 2, "valid": 2, "invalid": 0}, "jsonl: %r %r" % (problems, counts))
            checks.append("valid JSONL passes (blank line ignored, output alias)")

            missing = write(tmp, "missing.json", json.dumps([
                {"prompt": "no id", "expected": "e"},
                {"id": "no-prompt", "expected": "e"},
                {"id": "no-expected", "prompt": "p"},
                {"id": "bad-type", "prompt": 42, "expected": ""},
            ]))
            ok, problems, notes, counts = mod.check(missing)
            joined = " ".join(problems)
            check(not ok and counts["valid"] == 0 and counts["invalid"] == 4, "missing: %r %r" % (problems, counts))
            check("missing required field 'id'" in joined and "missing required field 'prompt'" in joined and "missing required field 'expected'" in joined, "missing messages: %r" % (problems,))
            check("must be a string" in joined and "non-empty string" in joined, "bad-type messages: %r" % (problems,))
            checks.append("missing/invalid required fields fail per fixture")

            dup = write(tmp, "dup.json", json.dumps([
                {"id": "same", "prompt": "p1", "expected": "e1"},
                {"id": "same", "prompt": "p2", "expected": "e2"},
            ]))
            ok, problems, notes, counts = mod.check(dup)
            check(not ok and any("duplicate id 'same'" in p for p in problems) and counts["valid"] == 1 and counts["invalid"] == 1, "dup: %r %r" % (problems, counts))
            checks.append("duplicate id fails naming the id and first fixture")

            emptyp = write(tmp, "empty_prompt.json", json.dumps([
                {"id": "e1", "prompt": "   ", "expected": "e"},
                {"id": "e2", "prompt": "ok", "expected": []},
            ]))
            ok, problems, notes, counts = mod.check(emptyp)
            joined = " ".join(problems)
            check(not ok and "field 'prompt' is empty" in joined and "non-empty" in joined and counts["invalid"] == 2, "empty: %r %r" % (problems, counts))
            checks.append("empty prompt and empty expected list fail")

            unsafe = write(tmp, "unsafe.json", json.dumps([
                {"id": "../evil", "prompt": "p", "expected": "e"},
                {"id": "ok1", "prompt": "p", "expected": "e", "path": "../secret.md"},
                {"id": "ok2", "prompt": "p", "expected": "e", "source": "/abs/file.md"},
                {"id": "ok3", "prompt": "p", "expected": "e", "file": "notes\\..\\secret.md"},
            ]))
            ok, problems, notes, counts = mod.check(unsafe)
            joined = " ".join(problems)
            check(not ok and counts["invalid"] == 4 and joined.count("unsafe path") == 4, "unsafe: %r %r" % (problems, counts))
            checks.append("unsafe ../, absolute and backslash paths are rejected")

            empty = write(tmp, "empty.json", "")
            ok, problems, notes, counts = mod.check(empty)
            check(not ok and any("fixture file is empty" in p for p in problems), "empty file: %r" % (problems,))
            checks.append("empty file fails")

            empty_list = write(tmp, "empty_list.json", "[]")
            ok, problems, notes, counts = mod.check(empty_list)
            check(not ok and any("no fixtures" in p for p in problems), "empty list: %r" % (problems,))
            checks.append("empty fixture list fails")

            not_obj = write(tmp, "bad.jsonl", "not json\n")
            ok, problems, notes, counts = mod.check(not_obj)
            check(not ok and any("not valid JSON" in p for p in problems), "bad jsonl: %r" % (problems,))
            checks.append("invalid JSONL line fails")

            ok, problems, notes, counts = mod.check(os.path.join(tmp, "nope.json"))
            check(not ok and any("not found" in p for p in problems), "missing file: %r" % (problems,))
            checks.append("missing fixture file fails with not found")

            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = mod.main(["memory_lint_check.py", valid])
            out = buf.getvalue()
            check(code == 0 and "PASS:" in out and "fixtures: 3" in out, "CLI valid: %r %r" % (code, out))
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = mod.main(["memory_lint_check.py", dup])
            out = buf.getvalue()
            check(code == 1 and "FAIL:" in out and "duplicate" in out, "CLI fail: %r %r" % (code, out))
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = mod.main(["memory_lint_check.py", valid, "--strict"])
            check(code == 0 and "NOTE:" in buf.getvalue(), "CLI strict: %r %r" % (code, buf.getvalue()))
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = mod.main(["memory_lint_check.py"])
            check(code == 1 and "usage" in buf.getvalue(), "CLI no args: %r %r" % (code, buf.getvalue()))
            checks.append("CLI exits 0 with PASS, 1 with FAIL, handles --strict and no args")
    except Fail as e:
        sys.stderr.write("FAIL: %s\n" % e)
        return 1
    except Exception as e:
        sys.stderr.write("FAIL: unexpected %s: %s\n" % (type(e).__name__, e))
        return 1
    for line in checks:
        print(line)
    print("self-test: all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
