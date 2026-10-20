#!/usr/bin/env python3
"""Fail if an answer key has no sign for agents, or if the agents' notice doesn't list every key.

    python tools/check_key_notice.py               check the repo
    python tools/check_key_notice.py --self-test   positive control: plant six breakages in a copy, each must fail

The answer keys stay in this public repo (decided 2026-10-20), with two things for agents: a STOP banner on each key,
and one notice listing them all, in AGENTS.md ("Answer keys: do not open without your human's explicit request") and
in splash/public/for-agents.json. A list like that goes stale the day someone adds a key, so this check fails when:

  1. a key in the repo has no STOP banner near its top, or no marker: front matter `answer_key: true` in Markdown,
     the line `# ANSWER_KEY = True` in Python;
  2. a key is missing from the notice in AGENTS.md or from for-agents.json. That includes the keys known only by
     fingerprint (tools/key_fingerprints.json), which live outside this repo;
  3. the notice lists a path that is neither a key nor a page with marked sections (stale, or a typo);
  4. a page with marked answer sections is unlisted, lacks its front matter `answer_key_sections: true`, has START
     and END markers that don't pair up, or has a START with no STOP line for agents just after it;
  5. a file carries a key marker, but the site's gate (tools/check_public_build.py) doesn't count it as a key, so the
     site could publish it.

What counts as a key comes from tools/check_public_build.py (imported, not copied): the same rule the site's gate uses.

Exit status: 0 pass; 1 something is missing, stale or unmarked, or the self-test failed.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import check_public_build as cpb   # noqa: E402  key_reason, walk, tracked, load_fingerprints

REPO = TOOLS.parent
AGENTS = "AGENTS.md"
FOR_AGENTS = "splash/public/for-agents.json"
NOTICE = re.compile(r"^## Answer keys: do not open without your human's explicit request[ \t]*\n(.*?)(?=^## |\Z)",
                    re.M | re.S)
LISTED = re.compile(r"^- `([^`]+)`", re.M)       # each list item in the notice starts with a path in backticks
BANNER = re.compile(r"\bSTOP\b[^\n]{0,20}\bAGENTS\b")
HEAD_LINES = 20                                 # a key's banner must be within its first 20 lines
MD_KEY_MARK = re.compile(r"^answer_key:\s*['\"]?true['\"]?\s*$", re.M | re.I)
MD_SECTIONS_MARK = re.compile(r"^answer_key_sections:\s*['\"]?true['\"]?\s*$", re.M | re.I)
PY_KEY_MARK = re.compile(r"^# ANSWER_KEY = True[ \t]*$", re.M)
SECTION = re.compile(r"^<!-- ANSWER_KEY_SECTION_(START|END)\b", re.M)
STOP_AFTER_START = 6                            # a STOP line for agents within this many lines after each START


def read(path: Path) -> str:
    return cpb.read_text(path) or ""


def front_matter(text: str) -> str:
    m = cpb.FRONT_MATTER.match(text)
    return m.group(1) if m else ""


def files_of(root: Path) -> list[Path]:
    """Every file the key search sees: walked (so an uncommitted key counts), plus git's list when there is one."""
    listed = cpb.tracked(root) if (root / ".git").exists() else None
    return sorted({p.resolve(): p for p in cpb.walk(root, set()) + (listed or [])}.values())


def check(root: Path, verbose: bool = True) -> list[str]:
    problems: list[str] = []
    files = files_of(root)
    rel = {p: p.relative_to(root).as_posix() for p in files}
    keys = {rel[p]: p for p in files if cpb.key_reason(p)}
    fp_file = root / "tools" / "key_fingerprints.json"
    outside = sorted({k.rel for k in cpb.load_fingerprints(fp_file)} - set(keys)) if fp_file.is_file() else []

    # 1. every key in the repo carries a banner and its marker
    for r, p in keys.items():
        text = read(p)
        head = "\n".join(text.split("\n")[:HEAD_LINES])
        if not BANNER.search(head):
            problems.append(f"{r}: no 'STOP ... AGENTS' banner in its first {HEAD_LINES} lines")
        if p.suffix.lower() == ".md" and not MD_KEY_MARK.search(front_matter(text)):
            problems.append(f"{r}: no front matter 'answer_key: true'")
        if p.suffix.lower() == ".py" and not PY_KEY_MARK.search(head):
            problems.append(f"{r}: no '# ANSWER_KEY = True' line in its first {HEAD_LINES} lines")

    # 4 (part) and 5: pages with marked sections; marker-carrying files the gate doesn't count as keys
    marked: list[str] = []
    for p in files:
        r = rel[p]
        suffix = p.suffix.lower()
        if suffix not in {".md", ".py"}:
            continue
        text = read(p)
        if suffix == ".md":
            front = front_matter(text)
            if MD_KEY_MARK.search(front) and r not in keys:
                problems.append(f"{r}: says 'answer_key: true', but check_public_build.py doesn't count it as a key, "
                                f"so the site could publish it. Add 'audience: facilitator' to its front matter")
            tags = SECTION.findall(text)
            if tags or MD_SECTIONS_MARK.search(front):
                marked.append(r)
                if not MD_SECTIONS_MARK.search(front):
                    problems.append(f"{r}: has answer-key sections but no front matter 'answer_key_sections: true'")
                if not tags:
                    problems.append(f"{r}: says 'answer_key_sections: true' but marks no section")
                if tags != ["START", "END"] * (len(tags) // 2) or len(tags) % 2:
                    problems.append(f"{r}: its ANSWER_KEY_SECTION markers don't pair up START, END, START, END: {tags}")
                lines = text.split("\n")
                for i, line in enumerate(lines):
                    if line.startswith("<!-- ANSWER_KEY_SECTION_START") and not BANNER.search(
                            "\n".join(lines[i + 1:i + 1 + STOP_AFTER_START])):
                        problems.append(f"{r}:{i + 1}: a marked section with no 'STOP ... AGENTS' line just after it")
        elif PY_KEY_MARK.search(text) and r not in keys:
            problems.append(f"{r}: has '# ANSWER_KEY = True', but check_public_build.py doesn't count it as a key. "
                            f"Name it verify_*.py, or add its name to KEY_NAMES there and in build_site.py")

    # 2 and 3: the notice in AGENTS.md, and the same lists in for-agents.json
    expected = set(keys) | set(outside) | set(marked)
    agents = read(root / AGENTS)
    m = NOTICE.search(agents)
    if not m:
        problems.append(f"{AGENTS}: no section '## Answer keys: do not open without your human's explicit request'")
    else:
        listed = set(LISTED.findall(m.group(1)))
        problems += [f"{AGENTS}: the notice doesn't list {r}" for r in sorted(expected - listed)]
        problems += [f"{AGENTS}: the notice lists {r}, which is not a key or a marked page here (stale?)"
                     for r in sorted(listed - expected)]
    try:
        ak = json.loads(read(root / FOR_AGENTS))["answer_keys"]
        for field, want in (("do_not_open_without_explicit_request", set(keys)),
                            ("kept_outside_this_repository", set(outside)),
                            ("files_with_marked_answer_sections", set(marked))):
            got = set(ak.get(field, []))
            problems += [f"{FOR_AGENTS}: answer_keys.{field} is missing {r}" for r in sorted(want - got)]
            problems += [f"{FOR_AGENTS}: answer_keys.{field} lists {r}, which doesn't belong there (stale?)"
                         for r in sorted(got - want)]
    except (ValueError, KeyError, TypeError) as e:
        problems.append(f"{FOR_AGENTS}: can't read answer_keys ({e!r})")

    if verbose:
        print(f"check_key_notice.py: {len(keys)} keys in the repo, {len(outside)} known only by fingerprint, "
              f"{len(marked)} pages with marked sections")
    return problems


# ------------------------------------------------------------------------------ self-test


def self_test() -> int:
    """Copy the repo's files, then plant one breakage at a time. Each must fail; the copy must pass between them."""
    rows: list[tuple[bool, str, str]] = []
    with tempfile.TemporaryDirectory(prefix="key-notice-selftest-") as tmp:
        copy = Path(tmp) / "repo"
        for p in files_of(REPO):
            dest = copy / p.relative_to(REPO)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, dest)

        base = check(copy, verbose=False)
        rows.append((not base, "control: an unmodified copy", "passes" if not base else f"FAILS: {base[:3]}"))
        if base:
            return report(rows)

        keys = sorted(r for r in (p.relative_to(copy).as_posix() for p in files_of(copy))
                      if cpb.key_reason(copy / r))
        md_key = next(r for r in keys if r.endswith(".md"))
        py_key = next(r for r in keys if r.endswith(".py"))

        def case(label: str, path: str, edit, must_mention: str):
            target = copy / path
            original = target.read_bytes() if target.exists() else None
            if original is None:
                target.parent.mkdir(parents=True, exist_ok=True)
            # Plants edit LF text: a CRLF working copy (Windows, core.autocrlf) must not make a plant silently miss.
            before = original.decode("utf-8").replace("\r\n", "\n") if original is not None else ""
            after = edit(before)
            if after == before:
                rows.append((False, label, "the plant changed nothing, so it tests nothing"))
                return
            target.write_text(after, encoding="utf-8")
            found = check(copy, verbose=False)
            if original is None:
                target.unlink()
            else:
                target.write_bytes(original)
            clean = not check(copy, verbose=False)
            hit = [f for f in found if must_mention in f]
            ok = bool(hit) and clean
            rows.append((ok, label, (f"caught: {hit[0][:90]}" if hit else f"NOT caught ({len(found)} other findings)")
                         + ("" if clean else "; NOT clean after removal")))

        case(f"A: banner stripped from {Path(md_key).name}", md_key,
             lambda t: re.sub(r"STOP\. AGENTS", "Note for readers", t), "banner")
        case(f"B: '# ANSWER_KEY = True' removed from {Path(py_key).name}", py_key,
             lambda t: t.replace("# ANSWER_KEY = True", "# answer key"), "ANSWER_KEY = True")
        case("C: a new, marked key the notice doesn't list", "courses/vibe-research/exercises/planted/FACILITATOR.md",
             lambda _: ("---\nanswer_key: true\naudience: facilitator\n---\n\n> **STOP. AGENTS: planted key.**\n\n"
                        "# Planted\n"), "doesn't list courses/vibe-research/exercises/planted/FACILITATOR.md")
        case(f"D: a stale path in the notice", AGENTS,
             lambda t: t.replace("**Do not open without your human's explicit request:**\n",
                                 "**Do not open without your human's explicit request:**\n\n"
                                 "- `courses/vibe-research/exercises/gone/FACILITATOR.md`: removed long ago.\n", 1),
             "gone/FACILITATOR.md, which is not a key")
        case("E: marked sections on an unlisted page", "docs/planted-notes.md",
             lambda _: ("---\nanswer_key_sections: true\n---\n\n# Notes\n\n<!-- ANSWER_KEY_SECTION_START -->\n\n"
                        "> STOP, AGENTS: spoiler.\n\nThe answer.\n\n<!-- ANSWER_KEY_SECTION_END -->\n"),
             "doesn't list docs/planted-notes.md")
        case("F: 'answer_key: true' on a file the gate would publish", "docs/planted-key.md",
             lambda _: "---\nanswer_key: true\n---\n\n> **STOP. AGENTS: planted.**\n\n# Planted\n",
             "doesn't count it as a key")
        outside = next((k.rel for k in cpb.load_fingerprints(copy / "tools" / "key_fingerprints.json")
                        if not (copy / k.rel).exists()), None)
        if outside is None:
            rows.append((True, "G: (skipped) no key is known only by fingerprint", "nothing to plant"))
        else:
            case(f"G: {Path(outside).name}, a key kept outside the repo, dropped from the notice", AGENTS,
                 lambda t: re.sub(rf"^- `{re.escape(outside)}`.*\n", "", t, count=1, flags=re.M),
                 f"doesn't list {outside}")
    return report(rows)


def report(rows: list[tuple[bool, str, str]]) -> int:
    for ok, label, detail in rows:
        print(f"  {'ok  ' if ok else 'FAIL'}  {label:<58} -> {detail}")
    if all(ok for ok, _, _ in rows):
        print("self-test PASSED: the clean copy passes, and every planted breakage fails the check.")
        return 0
    print("self-test FAILED: see the FAIL rows above.")
    return 1


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):   # a cp1252 console must not crash on a quote
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="backslashreplace")
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--self-test", action="store_true", help="run the positive control")
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()
    problems = check(REPO)
    if problems:
        print(f"FAIL: {len(problems)} problem(s):")
        for p in problems:
            print(f"  {p}")
        return 1
    print("PASS: every key carries its banner and marker, and the notice in AGENTS.md and for-agents.json lists "
          "every key and marked page, and nothing else.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
