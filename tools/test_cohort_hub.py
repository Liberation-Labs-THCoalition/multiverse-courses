#!/usr/bin/env python3
"""Tests for the site's Cohort hub page (tools/build_site.py, stage_cohort_hub).

    python tools/build_site.py                      # first: the test reads the hub it staged
    python tools/test_cohort_hub.py                 # check _staging/cohort-hub.md
    python tools/test_cohort_hub.py --self-test     # positive control: every planted bad hub must fail

The hub is the class's plain-links page, for students who cannot use the campus game. It must hold:

  1. every raw-download link names a file the site publishes as a code page: a nav Page with code=True
     whose download build_site.py staged. Every such file has one, and nothing else does;
  2. no raw link names a file on CLAUDE.md's answer-key lists. Both lists are parsed from CLAUDE.md, so
     the test follows them; a file with marked spoiler sections counts too, as a raw download is whole;
  3. every raw link's file is tracked in git (git ls-files), so the link cannot 404 on GitHub;
  4. the sections are Sessions, Course spine, Exercises, then Links, last; the page links in the first
     three follow the nav's own order; and no link's text is a bare URL (it overflows a phone).

The self-test never opens an answer key. It plants a key's PATH, a string read from CLAUDE.md, and the
hub generator only writes that string into a link; nothing reads the file.

Exit status: 0 pass; 1 a check failed, or the self-test did not catch a plant.
"""
from __future__ import annotations

import dataclasses
import posixpath
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

TOOLS = Path(__file__).resolve().parent
REPO = TOOLS.parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import build_site as bs                # noqa: E402

CLAUDE_MD = REPO / "CLAUDE.md"
HUB = bs.STAGING / bs.COHORT_HUB.dest

# The hub's sections, in order, and the nav group each of the first three must mirror.
SECTIONS = ["Sessions", "Course spine", "Exercises", "Links"]
NAV_GROUP = {"Sessions": "Sessions", "Course spine": "The course spine", "Exercises": "Exercises"}
KEY_LISTS = (r"^## Do not open\b.*$", r"^## Skip the marked spoiler sections\b.*$")

LINK = re.compile(r"\[([^\]]*)\]\(([^)\s]+)\)")
HEADING = re.compile(r"^## (.+?)[ \t]*$", re.M)


# --------------------------------------------------------------------------- facts the checks rest on


def answer_key_paths(text: str | None = None) -> set[str]:
    """Every path in CLAUDE.md's two answer-key lists. Fails loudly if a list cannot be found, so a
    reworded CLAUDE.md cannot quietly empty the check."""
    text = CLAUDE_MD.read_text(encoding="utf-8-sig") if text is None else text
    paths: set[str] = set()
    for heading in KEY_LISTS:
        m = re.search(heading, text, re.M)
        if not m:
            raise AssertionError(f"CLAUDE.md: no heading matching {heading!r}; the answer-key list cannot be read")
        body = text[m.end():]
        nxt = re.search(r"^## ", body, re.M)
        found = re.findall(r"^- `([^`]+)`", body[:nxt.start()] if nxt else body, re.M)
        if not found:
            raise AssertionError(f"CLAUDE.md: the list under {m.group(0)!r} has no `path` bullets")
        paths.update(found)
    return paths


def tracked_files() -> set[str]:
    out = subprocess.run(["git", "ls-files", "-z"], cwd=REPO, capture_output=True, check=True).stdout
    return {p for p in out.decode("utf-8").split("\0") if p}


def published_code_sources(nav: list) -> set[str]:
    """Sources the site publishes as code pages: a nav Page with code=True whose download is staged."""
    out = set()
    for _, page in bs.pages_in(nav):
        if page.code and page.source:
            staged = bs.STAGING / posixpath.dirname(page.dest) / posixpath.basename(page.source)
            if staged.is_file():
                out.add(page.source)
    return out


def sections_of(hub: str) -> dict[str, str]:
    heads = list(HEADING.finditer(hub))
    return {m.group(1): hub[m.end(): (heads[i + 1].start() if i + 1 < len(heads) else len(hub))]
            for i, m in enumerate(heads)}


# ---------------------------------------------------------------------------------------- checks


def problems(hub: str, nav: list, keys: set[str], tracked: set[str]) -> list[str]:
    out: list[str] = []
    raw_prefix = f"{bs.RAW_BASE}/{bs.BRANCH}/"
    published = published_code_sources(nav)
    keys_lower = {k.lower() for k in keys}

    heads = HEADING.findall(hub)
    if heads != SECTIONS:
        out.append(f"sections are {heads}; want {SECTIONS} (Sessions first, Links last)")

    links = LINK.findall(hub)
    for text, target in links:
        if re.match(r"\s*(https?:|www\.)", text):
            out.append(f"link text is a bare URL: [{text}]({target})")

    raw_seen = []
    for text, target in links:
        if not target.startswith("https://raw.githubusercontent.com/"):
            continue
        if not target.startswith(raw_prefix):
            out.append(f"raw link not into {raw_prefix}: {target}")
            continue
        path = unquote(target[len(raw_prefix):])
        raw_seen.append(path)
        if path not in published:
            out.append(f"raw link to {path}: not a file the site publishes as a code page")
        if path.lower() in keys_lower:
            out.append(f"raw link to {path}: on CLAUDE.md's answer-key list")
        if path not in tracked:
            out.append(f"raw link to {path}: not tracked in git (git ls-files)")
        if text != f"{posixpath.basename(path)} (raw)":
            out.append(f"raw link to {path}: text is {text!r}; want {posixpath.basename(path) + ' (raw)'!r}")
    for path in sorted(published - set(raw_seen)):
        out.append(f"code page {path} has no raw link")
    if len(raw_seen) != len(set(raw_seen)):
        out.append("a raw link appears twice")

    groups = {item[0]: item[1] for item in nav if not isinstance(item, bs.Page)}
    secs = sections_of(hub)
    base = posixpath.dirname(bs.COHORT_HUB.dest)
    for title, group in NAV_GROUP.items():
        if group not in groups:
            out.append(f"the nav has no {group!r} group")
            continue
        want = [p.dest for _, p in bs.pages_in(groups[group])]
        got = [posixpath.normpath(posixpath.join(base, t)) for _, t in LINK.findall(secs.get(title, ""))
               if not re.match(r"[a-z][a-z0-9+.-]*:", t)]
        if got != want:
            out.append(f"'{title}' page links are not the nav's {group!r} pages in nav order:\n"
                       f"        got  {got}\n        want {want}")
    return out


def check_staged() -> int:
    if not HUB.is_file():
        print(f"FAIL  {HUB.relative_to(REPO)} is missing: run python tools/build_site.py first")
        return 1
    hub = HUB.read_text(encoding="utf-8")
    keys = answer_key_paths()
    found = problems(hub, bs.NAV, keys, tracked_files())
    raw = sum(1 for _, t in LINK.findall(hub) if t.startswith("https://raw.githubusercontent.com/"))
    if found:
        print(f"FAIL  {HUB.relative_to(REPO)}: {len(found)} problem(s)")
        for p in found:
            print(f"      - {p}")
        return 1
    print(f"ok    {HUB.relative_to(REPO)}: sections {SECTIONS}; {raw} raw links, each to a published code page, "
          f"tracked in git, on neither of CLAUDE.md's answer-key lists ({len(keys)} paths); "
          f"sessions, spine and exercises in nav order")
    return 0


# ------------------------------------------------------------------------------------- self-test


def self_test() -> int:
    """Each case plants one kind of bad hub; each must be caught, by the check it names. The clean hub
    must pass first, or a 'catch' could be the check failing on everything."""
    keys = answer_key_paths()
    tracked = tracked_files()
    staged = HUB.read_text(encoding="utf-8") if HUB.is_file() else ""
    clean = bs.stage_cohort_hub()
    failed = 0

    def report(label: str, found: list[str], want: str | None) -> None:
        nonlocal failed
        if want is None:
            ok = not found
            print(f"{'ok  ' if ok else 'FAIL'}  clean: {label}" + ("" if ok else f" -> {found}"))
        else:
            ok = any(want in p for p in found)
            print(f"{'ok  ' if ok else 'FAIL'}  plant: {label} -> {'caught' if ok else 'NOT caught'}")
            for p in found:
                print(f"        {p}")
        failed += not ok

    report("the staged hub equals stage_cohort_hub() and passes",
           problems(clean, bs.NAV, keys, tracked) + ([] if staged == clean else
                                                     ["_staging/cohort-hub.md differs: rerun build_site.py"]), None)

    def with_extra(group: list, page: bs.Page) -> list[str]:
        """The problems of the hub built with one extra Page in a nav group, checked while it is there."""
        group.append(page)
        try:
            return problems(bs.stage_cohort_hub(), bs.NAV, keys, tracked)
        finally:
            group.remove(page)

    def key_path(suffix: str) -> str:
        hits = sorted(k for k in keys if k.endswith(suffix))
        if not hits:
            raise AssertionError(f"no CLAUDE.md answer-key path ends with {suffix!r}; pick another plant")
        return hits[0]

    # A. The task's case: an extra code Page whose source is an answer key, by its PATH only.
    key = key_path("/verify_gate.py")
    plant = bs.Page("verify_gate.py", "exercises/seeded-04-all-checks-passed/verify_gate.md",
                    key, code=True, exercise=True)
    report(f"extra code Page in Exercises at answer key {key}",
           with_extra(bs.EXERCISES, plant), "answer-key list")

    # B. Unlike A: a file with marked spoiler sections made a code page. Its staged page shares the
    # download's name, so the published check alone passes it; only the key list can catch it.
    spine = bs.SPINE
    i = next(n for n, p in enumerate(spine) if p.source == f"{bs.COURSE}/the-target-bank.md")
    orig = spine[i]
    spine[i] = dataclasses.replace(orig, code=True)
    try:
        hub_b = bs.stage_cohort_hub()
        found_b = problems(hub_b, bs.NAV, keys, tracked)
    finally:
        spine[i] = orig
    report(f"spine page {orig.source} (marked spoiler sections) turned into a code page", found_b,
           "answer-key list")

    # C. A raw link the allowlist never produced (a generator bug): to a page the site shows, not as code.
    review = f"{bs.S01}/review.md"
    hub_c = clean.replace("## Links", f"- [review.md (raw)]({bs.raw_url(review)})\n\n## Links", 1)
    report(f"raw link injected for {review}, a page but not a code page",
           problems(hub_c, bs.NAV, keys, tracked), "not a file the site publishes as a code page")

    # D. A code Page whose file git does not track.
    ghost = f"{bs.S04}/not_in_git.py"
    plant_d = bs.Page("not_in_git.py", "exercises/seeded-04-all-checks-passed/not_in_git.md", ghost, code=True)
    report(f"code Page for untracked {ghost}",
           with_extra(bs.EXERCISES, plant_d), "not tracked in git")

    # E. Two spine links swapped: out of nav order.
    a, b = (f"- [{p.label}]({p.dest})" for p in bs.SPINE[:2])
    hub_e = clean.replace(a, "\0").replace(b, a).replace("\0", b)
    report("first two spine links swapped", problems(hub_e, bs.NAV, keys, tracked), "nav order")

    # F. The Links section moved first.
    head, links = clean.split("## Links", 1)
    hub_f = head.replace("## Sessions", "## Links" + links.rstrip("\n") + "\n\n## Sessions", 1)
    report("Links section moved before Sessions", problems(hub_f, bs.NAV, keys, tracked), "sections are")

    # G. A raw link labelled with its bare URL.
    url = bs.raw_url(f"{bs.S01}/analysis.py")
    hub_g = clean.replace(f"[analysis.py (raw)]({url})", f"[{url}]({url})", 1)
    report("raw link text is the bare URL", problems(hub_g, bs.NAV, keys, tracked), "bare URL")

    # H. A code page dropped from the hub's raw links.
    url_h = bs.raw_url(f"{bs.S04}/gate.py")
    hub_h = clean.replace(f"    - [gate.py (raw)]({url_h})\n", "", 1)
    report("gate.py's raw link removed", problems(hub_h, bs.NAV, keys, tracked), "has no raw link")

    # I. The key-list parser itself: a CLAUDE.md without the list must fail, not return an empty set.
    try:
        answer_key_paths("# Answer keys\n\nNothing here.\n")
        report("CLAUDE.md with no key list", [], "cannot be read")
    except AssertionError as err:
        report("CLAUDE.md with no key list", [str(err)], "cannot be read")

    print(f"\nself-test {'FAILED' if failed else 'PASSED'}: "
          + (f"{failed} case(s) wrong" if failed else "the clean hub passes and every plant is caught"))
    return 1 if failed else 0


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):   # a cp1252 console must not crash on a quote
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="backslashreplace")
    argv = sys.argv[1:] if argv is None else argv
    try:
        return self_test() if "--self-test" in argv else check_staged()
    except AssertionError as err:
        print(f"FAIL  {err}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
