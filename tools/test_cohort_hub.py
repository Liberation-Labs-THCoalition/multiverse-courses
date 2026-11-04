#!/usr/bin/env python3
"""Tests for the site's Cohort hub page (tools/build_site.py, stage_cohort_hub).

    python tools/build_site.py                      # first: the test reads the hub it staged
    python tools/test_cohort_hub.py                 # check _staging/cohort-hub.md
    python tools/test_cohort_hub.py --self-test     # positive control: every planted bad hub must fail

The hub is the class's plain-links page, for students who cannot use the campus game. It must hold:

  1. every raw-download link in the generated sections (all but Links) names a file the site publishes as a code page: a nav Page with code=True
     whose download build_site.py staged. Every such file has one, and nothing else does;
  2. no raw link names a file on CLAUDE.md's answer-key lists. Both lists are parsed from CLAUDE.md, so
     the test follows them; a file with marked spoiler sections counts too, as a raw download is whole;
  3. every raw link's file is tracked in git (git ls-files), so the link cannot 404 on GitHub;
  4. the sections are Sessions, Course spine, Exercises, then Links, last; the page links in the first
     three follow the nav's own order; and no link's text is a bare URL (a filename says what you get);
  5. no link lands on an answer key, in the forms link_lands() resolves: this repo's files on
     raw.githubusercontent.com and github.com (blob, raw, tree, edit; a branch, a commit or refs/heads/;
     '..' resolved; any scheme or letter case), this site's pages (full URL, root-relative or relative),
     and, on any other host, a path that ends in a key's repo path. Each is checked against both CLAUDE.md
     lists and build_site.py's key names (by name only: this test never opens a file). A file with marked
     spoiler sections may be linked as its site page, but never whole and never by anchor. A link form
     not resolved here is still checked by its file name, and nothing more;
  6. labels and links only (docs/run-card-hedgedoc-v1.md): every line is a heading, a link item or a nav
     group label, except in Links, where a non-link line must appear verbatim in docs/cohort-links.md.
     That file is edited by hand, so 5 and 6 cover it too.

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
from urllib.parse import unquote, urlsplit

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

# A link target may hold balanced parentheses (…/Confounding_(statistics)) and be followed by a "title".
LINK_TARGET = r"((?:[^()\s]|\([^()\s]*\))+)"
LINK_TITLE = r'(?:\s+"[^"]*")?'
LINK = re.compile(r"\[([^\]]*)\]\(" + LINK_TARGET + LINK_TITLE + r"\)")
HEADING = re.compile(r"^## (.+?)[ \t]*$", re.M)


# --------------------------------------------------------------------------- facts the checks rest on


def answer_key_lists(text: str | None = None) -> tuple[set[str], set[str]]:
    """CLAUDE.md's two lists: (do not open, marked spoiler sections). Fails loudly if a list cannot be
    found, so a reworded CLAUDE.md cannot quietly empty the check."""
    text = CLAUDE_MD.read_text(encoding="utf-8-sig") if text is None else text
    lists = []
    for heading in KEY_LISTS:
        m = re.search(heading, text, re.M)
        if not m:
            raise AssertionError(f"CLAUDE.md: no heading matching {heading!r}; the answer-key list cannot be read")
        body = text[m.end():]
        nxt = re.search(r"^## ", body, re.M)
        found = re.findall(r"^- `([^`]+)`", body[:nxt.start()] if nxt else body, re.M)
        if not found:
            raise AssertionError(f"CLAUDE.md: the list under {m.group(0)!r} has no `path` bullets")
        lists.append(set(found))
    return lists[0], lists[1]


def answer_key_paths(text: str | None = None) -> set[str]:
    """Every path on either of CLAUDE.md's answer-key lists."""
    closed, spoiler = answer_key_lists(text)
    return closed | spoiler


KEY_STEMS = {posixpath.splitext(n)[0] for n in bs.KEY_NAMES}


def name_is_key(name: str) -> bool:
    """build_site.is_key's NAME rule only. is_key itself reads a .md file's front matter, and this test
    must never open a file a link points at, so it is not called here. A code page is staged as .md, so
    a key's stem counts too (verify_floor.md, the page a verify_floor.py would get)."""
    n = name.lower()
    stem = posixpath.splitext(n)[0]
    return (n in bs.KEY_NAMES or bool(bs.VERIFY_SCRIPT.match(n)) or stem in KEY_STEMS
            or bool(bs.VERIFY_SCRIPT.match(stem + ".py")))


def site_page(path: str) -> str:
    """A site path as the staged page it serves: 'x/review/' and 'x/review/index.html' are 'x/review.md'."""
    path = path.lower()
    if path.endswith("/index.html"):
        path = path[: -len("/index.html")]
    path = path.rstrip("/")
    return path if posixpath.splitext(path)[1] else path + ".md"


def repo_file(rest: list[str]) -> str | None:
    """The repo path after a ref: 'master/a/b' or 'refs/heads/master/a/b' (or a commit) give 'a/b',
    with '..' and '.' segments resolved as a client resolves them before it asks."""
    if len(rest) >= 3 and rest[0].lower() == "refs" and rest[1].lower() in ("heads", "tags"):
        rest = rest[3:]
    else:
        rest = rest[1:]
    return posixpath.normpath("/".join(rest)) if rest else None


def link_lands(target: str, base: str) -> tuple[str | None, str, str]:
    """Where a link lands, without opening anything: (path, fragment, kind).
    - 'repo': this repo's files on raw.githubusercontent.com, or github.com blob/raw/tree/edit URLs, at a
      branch, a commit or refs/heads/<branch>; path is repo-relative, '..' resolved.
    - 'site': this site's pages, as a full URL, a root-relative path or a relative one; path is staged.
    - 'other': anything else; path is the URL's path, still checked by file name and by key-path suffix.
    Scheme and host are compared without letter case. Forms not listed here are not resolved."""
    parts = urlsplit(target)
    frag, path, host = parts.fragment, unquote(parts.path), parts.netloc.lower()
    site = urlsplit(bs.SITE_URL)
    if parts.scheme or host:
        segs = [s for s in path.split("/") if s]
        org_repo = [s.lower() for s in urlsplit(bs.GITHUB).path.strip("/").split("/")]
        if [s.lower() for s in segs[:2]] == org_repo:
            if host == "raw.githubusercontent.com":
                found = repo_file(segs[2:])
                if found:
                    return found, frag, "repo"
            if host in ("github.com", "www.github.com") and len(segs) > 3 \
                    and segs[2].lower() in ("blob", "raw", "tree", "edit"):
                found = repo_file(segs[3:])
                if found:
                    return found, frag, "repo"
        if host == site.netloc.lower() and path.lower().startswith(site.path.lower()):
            return site_page(path[len(site.path):] or bs.COHORT_HUB.dest), frag, "site"
        return path, frag, "other"
    if not path:                                   # an anchor on the hub itself
        return site_page(bs.COHORT_HUB.dest), frag, "site"
    if path.startswith("/"):                       # root-relative
        if path.lower().startswith(site.path.lower()):
            return site_page(path[len(site.path):] or bs.COHORT_HUB.dest), frag, "site"
        return path, frag, "other"
    return site_page(posixpath.normpath(posixpath.join(base, path))), frag, "site"


def key_targets(closed: set[str], spoiler: set[str], nav: list) -> dict[str, dict[str, str]]:
    """For each kind of landing, the lower-cased paths that are keys: {'repo'|'site': {path: 'closed'|'spoiler'}}.
    A key's site forms are its path under the course folder, as itself and as a .md page, plus the dest of
    any nav Page built from it."""
    dest_of = {p.source: p.dest for _, p in bs.pages_in(nav) if p.source}
    out: dict[str, dict[str, str]] = {"repo": {}, "site": {}}
    for kind_name, paths in (("spoiler", spoiler), ("closed", closed)):      # closed wins a tie
        for k in paths:
            out["repo"][k.lower()] = kind_name
            under = k[len(bs.COURSE) + 1:] if k.startswith(bs.COURSE + "/") else k
            for form in (under, posixpath.splitext(under)[0] + ".md", dest_of.get(k, "")):
                if form:
                    out["site"][site_page(form)] = kind_name
    return out


def group_labels(items: list):
    for item in items:
        if not isinstance(item, bs.Page):
            yield item[0]
            yield from group_labels(item[1])


LINK_ITEM = re.compile(r"^\s*- \[[^\]]*\]\(" + LINK_TARGET + LINK_TITLE + r"\)$")


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

    # 5. every link, whatever its scheme, host or letter case, resolved and checked against the keys
    spoiler = answer_key_lists()[1] & keys
    targets = key_targets(keys - spoiler, spoiler, nav)
    base = posixpath.dirname(bs.COHORT_HUB.dest)
    for text, target in links:
        path, frag, kind = link_lands(target, base)
        if not path:
            continue
        name = posixpath.basename(path.rstrip("/"))
        if kind == "other":             # a mirror or another host: does its path END in a key's repo path?
            low = path.lower()
            hits = {v for k, v in targets["repo"].items() if low == k or low.endswith("/" + k)}
            hit = "closed" if "closed" in hits else ("spoiler" if hits else None)
        else:
            hit = targets[kind].get(path.lower() if kind == "repo" else site_page(path))
        if hit == "closed" or name_is_key(name):
            out.append(f"link [{text}]({target}) lands on an answer key ({path}): never link one, in any form")
        elif hit == "spoiler" and kind in ("repo", "other"):
            out.append(f"link [{text}]({target}) gives the whole of {path}, which has marked spoiler sections")
        elif hit == "spoiler" and frag:
            out.append(f"link [{text}]({target}) anchors into {path}, which has marked spoiler sections")

    # 6. labels and links only; in Links, a non-link line must come verbatim from docs/cohort-links.md
    labels = set(group_labels(nav))
    cohort = {s.strip() for s in bs.cohort_links_section().splitlines() if s.strip()}
    section = None
    for line in hub.splitlines():
        s = line.strip()
        m = re.match(r"^## (.+?)[ \t]*$", line)
        if not s or m:
            section = m.group(1) if m else section
            continue
        if section is None and (re.match(r"^# \S", line) or (s.startswith("<!--") and s.endswith("-->"))):
            continue
        if LINK_ITEM.match(line):
            continue
        g = re.match(r"^\s*- (.+?)\s*$", line)
        if g and g.group(1) in labels and section != "Links":
            continue
        if section == "Links" and s in cohort and not LINK.search(s):
            continue
        out.append(f"line is not a heading, a link item or a nav label (labels and links only): {s!r}")

    # 1-3 apply to the generated sections. Links comes from docs/cohort-links.md, edited by hand: a raw link
    # there (a dataset elsewhere, this repo's README) need not be a code page, and 5 still checks it for keys.
    raw_seen = []
    for text, target in LINK.findall(re.split(r"^## Links", hub, maxsplit=1, flags=re.M)[0]):
        if urlsplit(target).netloc.lower() != "raw.githubusercontent.com":
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

    # J-O: links that are not raw https downloads. Found by the 2026-11-04 answer-key verifier (J-M got
    # through the first version of this test) and two more unlike them (N, O). Path strings only.
    def in_section(hub: str, section: str, line: str) -> str:
        return hub.replace(f"## {section}\n\n", f"## {section}\n\n{line}\n", 1)

    fac01 = key_path("seeded-01-the-approved-analysis/FACILITATOR.md")
    fac02 = key_path("seeded-02-the-fix-that-broke-it/FACILITATOR.md")
    prereg = key_path("seeded-04-all-checks-passed/AGENT_REVIEW_PREREG.md")
    bank = f"{bs.COURSE}/the-target-bank.md"
    site_host = urlsplit(bs.SITE_URL).netloc.upper()
    site_path = urlsplit(bs.SITE_URL).path
    under = fac02[len(bs.COURSE) + 1:]
    plants = [
        ("J", "a github.com /blob/ link to a key, in Exercises", "Exercises",
         f"- [Notes]({bs.GITHUB}/blob/{bs.BRANCH}/{fac01})", "lands on an answer key"),
        ("K", "an http:// (not https) raw link to a key, in Links", "Links",
         f"- [Notes]({bs.raw_url(fac01).replace('https://', 'http://', 1)})", "lands on an answer key"),
        ("L", "an anchor into the target bank, in Links", "Links",
         "- [Hints](spine/the-target-bank.md#answer-key)", "anchors into"),
        ("M", "a line of prose under Exercises", "Exercises",
         "Start with Seeded 01; it is the easiest.", "labels and links only"),
        ("N", "this site's own URL for a key's page, host in capitals", "Links",
         f"- [Notes](HTTPS://{site_host}{site_path}{posixpath.splitext(under)[0]}/)", "lands on an answer key"),
        ("O", "a relative link to a key only CLAUDE.md lists (not a build_site key name)", "Links",
         f"- [Notes]({prereg[len(bs.COURSE) + 1:]})", "lands on an answer key"),
        ("P", "the target bank whole from GitHub", "Links",
         f"- [Bank]({bs.GITHUB}/blob/{bs.BRANCH}/{bank})", "marked spoiler sections"),
    ]
    # Q-T: forms the pre-merge checker got through J-P's version (2026-11-04).
    org_repo = urlsplit(bs.GITHUB).path.strip("/")
    s01, s04 = fac01.rsplit("/", 1)[0], prereg.rsplit("/", 1)[0]
    plants += [
        ("Q", "a '..' segment walking from Seeded 01 to a key only CLAUDE.md lists", "Links",
         f"- [Notes]({bs.GITHUB}/blob/{bs.BRANCH}/{s01}/../{s04.rsplit('/', 1)[1]}/{prereg.rsplit('/', 1)[1]})",
         "lands on an answer key"),
        ("R", "GitHub's Raw button form, raw/refs/heads/<branch>/", "Links",
         f"- [Notes]({bs.GITHUB}/raw/refs/heads/{bs.BRANCH}/{prereg})", "lands on an answer key"),
        ("S", "a CDN mirror of the repo (another host), to a key only CLAUDE.md lists", "Links",
         f"- [Notes](https://cdn.jsdelivr.net/gh/{org_repo}@{bs.BRANCH}/{prereg})", "lands on an answer key"),
        ("T", "the target bank whole, by blob/refs/heads/", "Links",
         f"- [Bank]({bs.GITHUB}/blob/refs/heads/{bs.BRANCH}/{bank})", "marked spoiler sections"),
    ]
    for tag, label, section, line, want in plants:
        report(f"{tag}. {label}", problems(in_section(clean, section, line), bs.NAV, keys, tracked), want)

    # Negative controls: ordinary links a maintainer adds to docs/cohort-links.md must NOT be flagged.
    for label, line in [
        ("a link whose URL has parentheses", "- [Confounding](https://en.wikipedia.org/wiki/Confounding_(statistics))"),
        ("a link with a title", '- [Call](https://zoom.us/j/1 "Weekly call")'),
        ("a Matrix room", "- [Chat](https://matrix.to/#/#room:example.org)"),
        ("a glossary anchor", "- [Confound](spine/glossary.md#confound)"),
        ("an email address", "- [Write to us](mailto:class@example.org)"),
    ]:
        report(f"ordinary link passes: {label}", problems(in_section(clean, "Links", line), bs.NAV, keys, tracked),
               None)

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
