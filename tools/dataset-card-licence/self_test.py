#!/usr/bin/env python3
"""Self-test for dataset-card-licence. No args, no network."""

import contextlib
import io
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
        return __import__("dataset_card_licence")
    except Exception as e:
        raise Fail("could not import dataset_card_licence: %s: %s" % (type(e).__name__, e))


def write(root, name, text):
    path = os.path.join(root, name)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    return path


def run_main(mod, argv):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = mod.main(argv)
    return code, buf.getvalue()


def main():
    try:
        mod = import_tool()
        checks = []
        with tempfile.TemporaryDirectory() as tmp:
            no_lic = write(tmp, "nolic.md", "---\nlanguage: en\ntags:\n- csv\n---\n\n# stated-facts-check\n\nBody text here.\n")
            card, problems = mod.build_card(open(no_lic, encoding="utf-8").read(), None)
            check(card is None and any("missing license" in p for p in problems), "no lic: %r" % (problems,))
            checks.append("missing license reported when no --license given")

            card, problems = mod.build_card(open(no_lic, encoding="utf-8").read(), "mit")
            check(not problems and card is not None, "add lic: %r" % (problems,))
            check("license: mit" in card and "language: en" in card and "tags: csv" in card, "preserved fields: %r" % card)
            check("# stated-facts-check" in card and "Body text here." in card, "body preserved")
            checks.append("license added; other fields and body preserved")

            good = "---\nlicense: mit\nlanguage: en\n---\n\n# stated-facts-check\n\nBody.\n"
            card, problems = mod.build_card(good, "mit")
            check(not problems and "license: mit" in card, "same lic: %r" % (problems,))
            card, problems = mod.build_card(good, "apache-2.0")
            check(card is None and any("conflicts" in p for p in problems), "conflict: %r" % (problems,))
            card, problems = mod.build_card(good, "apache-2.0", force=True)
            check(not problems and "license: apache-2.0" in card, "force: %r" % (problems,))
            checks.append("same license passes; conflicting license refused unless --force")

            card, problems = mod.build_card(good, "not-a-license")
            check(card is None and any("unknown license" in p for p in problems), "bad lic: %r" % (problems,))
            brit = "---\nlicence: mit\n---\n\n# T\n\nBody.\n"
            card, problems = mod.build_card(brit, None)
            check(not problems and "license: mit" in card and "licence:" not in card, "british: %r %r" % (card, problems))
            checks.append("unknown license refused; licence: spelling converted to license:")

            fields, body, p = mod.parse_card(good)
            check(mod.get_field(fields, "license") == "mit" and body.strip().startswith("#"), "parse_card: %r" % (fields,))
            check(mod.is_known_license("MIT") and mod.is_known_license("apache-2.0") and not mod.is_known_license("xyz"), "is_known_license")
            check(mod.check_fields(fields, body) == [], "check_fields clean")
            notitle = "---\nlicense: mit\n---\n\nJust body, no title.\n"
            card, problems = mod.build_card(notitle, "mit")
            check(card is None and any("title" in p for p in problems), "notitle: %r" % (problems,))
            card, problems = mod.build_card(notitle, "mit", title="stated-facts-check")
            check(not problems and "# stated-facts-check" in card, "title fix: %r" % (problems,))
            bare = "# Only a title\n\nBody with no front matter.\n"
            card, problems = mod.build_card(bare, "mit")
            check(not problems and card.startswith("---\nlicense: mit"), "bare card: %r" % (problems,))
            checks.append("parse/check helpers work; missing title fixed by --title; front matter created when absent")

            code, out = run_main(mod, ["dataset_card_licence.py", no_lic, "--license", "mit"])
            check(code == 0 and "license: mit" in out, "CLI stdout: %r %r" % (code, out))
            code, out = run_main(mod, ["dataset_card_licence.py", no_lic])
            check(code == 1 and "FAIL:" in out, "CLI no lic: %r %r" % (code, out))
            code, out = run_main(mod, ["dataset_card_licence.py", no_lic, "--check-only"])
            check(code == 1 and "FAIL:" in out, "CLI check-only bad: %r %r" % (code, out))
            good_path = write(tmp, "good.md", good)
            code, out = run_main(mod, ["dataset_card_licence.py", good_path, "--check-only"])
            check(code == 0 and "PASS:" in out, "CLI check-only good: %r %r" % (code, out))
            out_path = os.path.join(tmp, "README.md")
            code, out = run_main(mod, ["dataset_card_licence.py", no_lic, "--license", "mit", "-o", out_path])
            check(code == 0 and os.path.exists(out_path), "CLI -o: %r %r" % (code, out))
            with open(out_path, encoding="utf-8") as fh:
                check("license: mit" in fh.read(), "-o contents")
            code, out = run_main(mod, ["dataset_card_licence.py", os.path.join(tmp, "nope.md"), "--license", "mit"])
            check(code == 1 and "not found" in out, "CLI missing: %r %r" % (code, out))
            code, out = run_main(mod, ["dataset_card_licence.py"])
            check(code == 2 and "usage" in out, "CLI usage: %r %r" % (code, out))
            checks.append("CLI exits 0 card, 1 problems/missing, 2 usage; -o writes card; --check-only passes clean card")
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
