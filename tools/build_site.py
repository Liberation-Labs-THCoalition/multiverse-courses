#!/usr/bin/env python3
"""Stage the Vibe Research course pages for MkDocs, and write mkdocs.yml.

    python tools/build_site.py        then        mkdocs build --strict

Spec: docs/site-spec.md. The repo is the single source of truth. This script reads the
site-map files as they are at build time and copies them into _staging/. It never writes to
a source file. The only text it adds is navigation, labels, the prerequisite line on each
session, the "In development" banners, the solutions box, and the Home page's headings
around wording taken from courses/vibe-research/README.md. Everything else is mechanical:

  links       Relative links are re-pointed at the staged copies. A link to another repo
              file goes to that file on GitHub. Links to answer keys, and to audit and
              review notes (which discuss the answers), are removed and their text kept:
              the site never points at a key.
  lists       A blank line is added where a list directly follows a paragraph line. GitHub
              renders that as a list; Python-Markdown would fold it into the paragraph.
  code pages  Each seeded exercise's analysis.py is shown as a page, with the file itself
              beside it for download.

It refuses to stage an answer key, or anything the spec puts out of scope. The built site is
checked separately by tools/check_public_build.py, which deliberately does not import this.
"""
from __future__ import annotations

import json
import posixpath
import re
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import quote, unquote

REPO = Path(__file__).resolve().parent.parent

# ------------------------------------------------------------------------------ settings

# The spec's `solutions_url`: where the "Solutions and facilitator notes" box on every
# exercise page links to. Empty until Thomas decides where the keys live (docs/site-spec.md,
# "Answer keys"). While it is empty, the box is shown without a link.
SOLUTIONS_URL = ""

SITE_NAME = "Vibe Research"
SITE_URL = "https://liberation-labs-thcoalition.github.io/multiverse-courses/course/"
GITHUB = "https://github.com/Liberation-Labs-THCoalition/multiverse-courses"
BRANCH = "master"

STAGING = REPO / "_staging"        # MkDocs docs_dir: rebuilt on every run, gitignored
MKDOCS_YML = REPO / "mkdocs.yml"   # generated on every run, gitignored


# ------------------------------------------------------------------------------ site map


@dataclass(frozen=True)
class Page:
    label: str                  # nav label
    dest: str                   # path inside the staging dir
    source: str | None = None   # repo path; None for the two generated pages
    code: bool = False          # show the source file as a code page
    exercise: bool = False      # end the page with the solutions box


COURSE = "courses/vibe-research"
S01 = f"{COURSE}/exercises/seeded-01-the-approved-analysis"
S02 = f"{COURSE}/exercises/seeded-02-the-fix-that-broke-it"

SESSIONS = [
    Page("Session 1: The question", "sessions/session-1-the-question.md",
         f"{COURSE}/session-1-the-question.md"),
    Page("Session 2: Designing to fail", "sessions/session-2-designing-to-fail.md",
         f"{COURSE}/session-2-designing-to-fail.md"),
    Page("Session 3: Reading what came back", "sessions/session-3-reading-what-came-back.md",
         f"{COURSE}/session-3-reading-what-came-back.md"),
    Page("Session 4: The gate and the room", "sessions/session-4-the-gate-and-the-room.md",
         f"{COURSE}/session-4-the-gate-and-the-room.md"),
]
# Session 1's prerequisite lies outside this course. Wording from courses/vibe-research/README.md.
FIRST_PREREQUISITE = "Multiverse agentic coursework"

SPINE = [
    Page("The pipeline", "spine/the-pipeline.md", f"{COURSE}/the-pipeline.md"),
    Page("The target bank", "spine/the-target-bank.md", f"{COURSE}/the-target-bank.md"),
    Page("Toolset", "spine/toolset.md", f"{COURSE}/toolset.md"),
    Page("Tools by stage", "spine/tools-by-stage.md", f"{COURSE}/tools-by-stage.md"),
]

EXERCISES = [
    Page("Build GRIM", "exercises/build-grim/index.md",
         f"{COURSE}/exercises/build-grim/README.md", exercise=True),
    ("Seeded 01: The approved analysis", [
        # analysis.py first: it says "Before reading review.md, answer these three".
        Page("analysis.py", "exercises/seeded-01-the-approved-analysis/analysis.md",
             f"{S01}/analysis.py", code=True, exercise=True),
        Page("Review", "exercises/seeded-01-the-approved-analysis/review.md",
             f"{S01}/review.md", exercise=True),
    ]),
    ("Seeded 02: The fix that broke it", [
        # review.md first: it hands the student analysis.py ("in this directory is v2").
        Page("Review", "exercises/seeded-02-the-fix-that-broke-it/review.md",
             f"{S02}/review.md", exercise=True),
        Page("analysis.py", "exercises/seeded-02-the-fix-that-broke-it/analysis.md",
             f"{S02}/analysis.py", code=True, exercise=True),
    ]),
]

INSTRUCTORS = [
    Page("Running a session", "instructors/running-a-session.md", "docs/running-a-session.md"),
    Page("Session clocks", "instructors/session-clocks.md", "docs/session-clocks.md"),
    Page("Delivery model", "instructors/delivery-model.md", "docs/delivery-model.md"),
    Page("Between sessions and tone", "instructors/between-sessions-and-tone.md",
         "docs/between-sessions-and-tone.md"),
]

HOME = Page("Home", "index.md")                                      # generated
INTERACTIVE = Page("Interactive pieces (coming)", "interactive-pieces.md")  # generated

NAV = [
    HOME,
    ("Sessions", SESSIONS),
    ("The course spine", SPINE),
    ("Exercises", EXERCISES),
    ("For instructors", INSTRUCTORS),
    INTERACTIVE,
]


# ------------------------------------------------------------------ gaps (in development)


@dataclass(frozen=True)
class Gap:
    source: str
    hour: int
    notes: tuple[str, ...]   # VERBATIM quotes from the session file's own notes


# Hours not yet written ("Gaps are visible, not hidden", docs/site-spec.md). Each gets an
# "In development" banner under its heading, quoting what the session file itself says will
# go there, and its page gets front matter `status: in-development`.
#
# The build FAILS if a quote is no longer in the file, so this list cannot silently outlive
# the gap it describes. When an hour is written, delete its entry.
#
# Session 1 hours 2-3 were on this list until 2026-09-29, when commit 4024468 wrote them
# (their materials are in a facilitator pack outside this repo, by design).
GAPS = [
    # 2026-09-29: session 2 hour 3 written (its case lives in the private facilitator pack).
]


# ------------------------------------------------------------------------- keys and scope

# docs/site-spec.md: the keys are the FACILITATOR.md files, verify_floor.py and
# AGENT_REVIEW_RESULTS.md, plus anything with front matter `audience: facilitator`.
# grim_reference.py is added: it is build-grim's working solution ("FACILITATOR REFERENCE
# ONLY. DO NOT GIVE THIS FILE TO STUDENTS").
KEY_NAMES = {"facilitator.md", "verify_floor.py", "agent_review_results.md", "grim_reference.py"}
FACILITATOR_AUDIENCE = re.compile(r"^audience:\s*['\"]?facilitator['\"]?\s*$", re.M | re.I)

# Out of scope for v0 (docs/site-spec.md): never staged.
OUT_OF_SCOPE = re.compile(
    r"^(accelerator|meetup|standards)/|^docs/audit-|(^|/)REVIEW_[^/]*$"
    r"|(^|/)OUTLINE_v2\.md$|(^|/)__pycache__/"
)
# Never linked either: audit and review notes discuss the answers
# (docs/audit-2026-09-09.md states seeded-01's).
NEVER_LINK = re.compile(r"^docs/audit-|(^|/)REVIEW_[^/]*$")


class BuildError(Exception):
    pass


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")   # universal newlines: CRLF becomes \n


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)


def split_front_matter(text: str) -> tuple[str, str]:
    m = FRONT_MATTER.match(text)
    return (m.group(1), text[m.end():]) if m else ("", text)


def is_key(rel: str) -> bool:
    """An answer key, by the spec's list of names or by front matter."""
    if posixpath.basename(rel).lower() in KEY_NAMES:
        return True
    path = REPO / rel
    if path.suffix.lower() == ".md" and path.is_file():
        front, _ = split_front_matter(read(path))
        return bool(FACILITATOR_AUDIENCE.search(front))
    return False


def norm(text: str) -> str:
    """Letters and digits only, lowercased: compares text across markup and line wrapping."""
    return re.sub(r"[\W_]+", "", text.lower())


# ------------------------------------------------------------------------------- markdown

FENCE_OPEN = re.compile(r"^[ \t]*(`{3,}|~{3,})")
INLINE = re.compile(
    r"(?P<code>``.+?``|`[^`\n]+`)"                             # inline code: left alone
    r"|(?P<bang>!?)\[(?P<text>(?:\\.|[^\]\\])*)\]"              # [text]
    r"\((?P<target><[^>\n]*>|[^)\s]+)(?P<title>[ \t]+\"[^\"\n]*\")?\)",
    re.S,
)
LIST_ITEM = re.compile(r"^ {0,3}([-*+]|\d{1,9}[.)])[ \t]+\S")
# GitHub lets a bullet list, or an ordered list starting at 1, interrupt a paragraph.
INTERRUPTING_ITEM = re.compile(r"^ {0,3}([-*+]|1[.)])[ \t]+\S")
NOT_PARAGRAPH = re.compile(r"^( {4}|\t| {0,3}(>|#|\||<|!!!|```|~~~|---|\*\*\*|___))")


def outside_code(text: str, fn) -> str:
    """Apply fn to the parts of text that are not fenced code blocks."""
    out, buf, fence = [], [], None
    for line in text.splitlines(keepends=True):
        m = FENCE_OPEN.match(line)
        if fence is None:
            if m:
                out.append(fn("".join(buf)))
                buf, fence = [line], m.group(1)
            else:
                buf.append(line)
        else:
            buf.append(line)
            close = re.match(r"^[ \t]*(`{3,}|~{3,})[ \t]*$", line)
            if close and close.group(1)[0] == fence[0] and len(close.group(1)) >= len(fence):
                out.append("".join(buf))
                buf, fence = [], None
    out.append(fn("".join(buf)) if fence is None else "".join(buf))
    return "".join(out)


@dataclass
class Report:
    internal: int = 0
    github: int = 0
    unlinked: list[tuple[str, str, str]] = field(default_factory=list)
    lists_separated: dict[str, int] = field(default_factory=dict)


def rewrite_links(text: str, src: str, dest: str, dest_of: dict[str, str], report: Report) -> str:
    def repl(m: re.Match) -> str:
        if m.group("code"):
            return m.group(0)
        target = m.group("target")
        raw = target[1:-1] if target.startswith("<") else target
        if re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:|#|//", raw):
            return m.group(0)                          # external, or an anchor on this page
        path, _, frag = raw.partition("#")
        rel = posixpath.normpath(posixpath.join(posixpath.dirname(src), unquote(path)))
        if rel == ".." or rel.startswith("../"):
            raise BuildError(f"{src}: link {raw!r} points outside the repo")
        anchor = f"#{frag}" if frag else ""
        title = m.group("title") or ""
        if rel in dest_of:
            report.internal += 1
            new = posixpath.relpath(dest_of[rel], posixpath.dirname(dest) or ".")
            return f"{m.group('bang')}[{m.group('text')}]({new}{anchor}{title})"
        if is_key(rel) or NEVER_LINK.search(rel):
            report.unlinked.append((src, m.group("text"), rel))
            return m.group("text")
        full = REPO / rel
        if not full.exists():
            raise BuildError(f"{src}: link {raw!r} resolves to {rel}, which is not in the repo")
        report.github += 1
        kind = "tree" if full.is_dir() else "blob"
        return f"{m.group('bang')}[{m.group('text')}]({GITHUB}/{kind}/{BRANCH}/{quote(rel)}{anchor}{title})"

    return INLINE.sub(repl, text)


def separate_lists(text: str, src: str, report: Report) -> str:
    """Insert a blank line where a list directly follows a paragraph line (see docstring)."""
    lines = text.split("\n")
    out: list[str] = []
    in_paragraph = False       # inside a block that began as a paragraph and has no list yet
    for i, line in enumerate(lines):
        if not line.strip():
            in_paragraph = False
        elif i == 0 or not lines[i - 1].strip():
            in_paragraph = not (LIST_ITEM.match(line) or NOT_PARAGRAPH.match(line))
        elif in_paragraph and INTERRUPTING_ITEM.match(line):
            out.append("")
            report.lists_separated[src] = report.lists_separated.get(src, 0) + 1
            in_paragraph = False
        elif LIST_ITEM.match(line):
            in_paragraph = False
        out.append(line)
    return "\n".join(out)


# --------------------------------------------------------------------------- page makers


def admonition(kind: str, title: str, body_lines: list[str]) -> str:
    return "\n".join([f'!!! {kind} "{title}"', *[f"    {l}" if l else "" for l in body_lines]])


def solutions_box() -> str:
    text = "Available after you complete this session."
    body = f"[{text}]({SOLUTIONS_URL})" if SOLUTIONS_URL else text
    return admonition("note", "Solutions and facilitator notes", [body])


def gap_banner(gap: Gap) -> str:
    body = ["This hour is not finished. What will go here, in the session file's own notes:", ""]
    for i, note in enumerate(gap.notes):
        if i:
            body.append(">")
        body.append(f"> {note}")
    return admonition("warning", "In development", body)


def with_front_matter(front: str, body: str, extra: dict[str, str]) -> str:
    lines = [l for l in front.split("\n") if l.strip()]
    for key, value in extra.items():
        if not any(re.match(rf"{re.escape(key)}\s*:", l) for l in lines):
            lines.append(f"{key}: {value}")
    head = "---\n" + "\n".join(lines) + "\n---\n\n" if lines else ""
    return head + body.lstrip("\n")


def insert_after_title(body: str, block: str, where: str) -> str:
    m = re.search(r"^# .*$", body, re.M)
    if not m:
        raise BuildError(f"{where}: no '# ' title line to put the prerequisite under")
    return body[:m.end()] + "\n\n" + block + "\n" + body[m.end():]


def stage_markdown(page: Page, dest_of: dict[str, str], report: Report, prereq: str | None) -> str:
    source_text = read(REPO / page.source)
    front, body = split_front_matter(source_text)
    body = outside_code(body, lambda s: separate_lists(
        rewrite_links(s, page.source, page.dest, dest_of, report), page.source, report))
    if prereq:
        body = insert_after_title(body, prereq, page.source)
    extra = {}
    for gap in (g for g in GAPS if g.source == page.source):
        for note in gap.notes:
            if norm(note) not in norm(source_text):
                raise BuildError(
                    f"GAPS entry for {gap.source} hour {gap.hour}: this note is no longer in the "
                    f"file:\n    {note[:100]!r}\n  If the hour has been written, delete the entry "
                    f"from GAPS in tools/build_site.py. Otherwise re-quote the file's own note.")
        heads = list(re.finditer(rf"^##[ \t]+Hour[ \t]+{gap.hour}(?!\w).*$", body, re.M | re.I))
        if len(heads) != 1:
            raise BuildError(f"GAPS entry for {gap.source} hour {gap.hour}: expected one "
                             f"'## Hour {gap.hour}' heading, found {len(heads)}")
        at = heads[0].end()
        body = body[:at] + "\n\n" + gap_banner(gap) + "\n" + body[at:]
        extra["status"] = "in-development"
    if page.exercise:
        body = body.rstrip("\n") + "\n\n" + solutions_box() + "\n"
    return with_front_matter(front, body, extra)


def stage_code(page: Page) -> str:
    src = REPO / page.source
    code = read(src)
    longest = max((len(run) for run in re.findall(r"`+", code)), default=0)
    fence = "`" * max(3, longest + 1)
    lang = {".py": "python"}.get(src.suffix.lower(), "text")
    write(STAGING / posixpath.dirname(page.dest) / src.name, code)      # the download
    body = (f"# {src.name}\n\n[Download {src.name}]({src.name})\n\n"
            f"{fence}{lang}\n{code.rstrip()}\n{fence}\n")
    return body + ("\n" + solutions_box() + "\n" if page.exercise else "")


def stage_home(dest_of: dict[str, str], report: Report) -> str:
    readme_rel = f"{COURSE}/README.md"
    readme = read(REPO / readme_rel)
    section = re.search(r"^## What the series is for[ \t]*\n(.*?)(?=^## |\Z)", readme, re.M | re.S)
    if not section:
        raise BuildError(f"{readme_rel}: no '## What the series is for' section for the Home page")
    para = next((p for p in re.split(r"\n[ \t]*\n", readme) if "Prerequisite:" in p), None)
    if para is None:
        raise BuildError(f"{readme_rel}: no 'Prerequisite:' sentence for the Home page")
    what_for = section.group(1).strip().rstrip("-").strip()
    who_for = " ".join(para[para.index("Prerequisite:"):].split())
    what_for, who_for = (rewrite_links(t, readme_rel, HOME.dest, dest_of, report)
                         for t in (what_for, who_for))
    sessions = [f"{i}. [{p.label}]({p.dest})" for i, p in enumerate(SESSIONS, 1)]
    return "\n".join([
        f"<!-- Generated by tools/build_site.py. Wording from {readme_rel}. -->",
        "",
        f"# {SITE_NAME}",
        "",
        admonition("info", "Developed in public", [
            "This course is being developed in public. Unfinished hours are marked "
            "*In development*."]),
        "",
        "## What the series is for",
        "",
        what_for,
        "",
        "## Who it is for",
        "",
        who_for,
        "",
        "## Sessions",
        "",
        *sessions,
        "",
    ])


def stage_interactive() -> str:
    body = "\n".join([f"# {INTERACTIVE.label}", "",
                      admonition("warning", "In development", ["Nothing is built here yet."]), ""])
    return with_front_matter("", body, {"status": "in-development"})


# ------------------------------------------------------------------------------ mkdocs.yml


def q(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)   # a JSON string is a valid YAML scalar


def nav_yaml(items: list, indent: int = 2) -> list[str]:
    lines = []
    for item in items:
        if isinstance(item, Page):
            lines.append(" " * indent + f"- {q(item.label)}: {q(item.dest)}")
        else:
            label, children = item
            lines.append(" " * indent + f"- {q(label)}:")
            lines.extend(nav_yaml(children, indent + 4))
    return lines


MKDOCS_TEMPLATE = """\
# GENERATED by tools/build_site.py on every run. Edit that script, not this file.
site_name: {site_name}
site_url: {site_url}
docs_dir: {docs_dir}
site_dir: site
use_directory_urls: true
theme:
  name: material
  font: false                # system fonts: no requests to Google Fonts
  features:
    - navigation.sections
    - navigation.footer
    - content.code.copy
  palette:
    - media: "(prefers-color-scheme: light)"
      scheme: default
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      toggle:
        icon: material/brightness-4
        name: Switch to light mode
markdown_extensions:
  - admonition
  - tables
  - attr_list
  - toc:
      permalink: true
      # GitHub-style heading anchors, so a link to a heading works on GitHub and here.
      slugify: !!python/object/apply:pymdownx.slugs.slugify
        kwds:
          case: lower
  - pymdownx.highlight
  - pymdownx.superfences
  - pymdownx.tilde           # ~~strikethrough~~, used in the sessions' Open lists
plugins:
  - search
extra:
  status:
    in-development: In development
  solutions_url: {solutions_url}
validation:
  nav:
    omitted_files: warn
    not_found: warn
    absolute_links: warn
  links:
    not_found: warn
    absolute_links: warn
    unrecognized_links: warn
    anchors: warn
nav:
"""


def write_mkdocs_yml() -> None:
    head = MKDOCS_TEMPLATE.format(site_name=q(SITE_NAME), site_url=q(SITE_URL),
                                  docs_dir=q(STAGING.name), solutions_url=q(SOLUTIONS_URL))
    write(MKDOCS_YML, head + "\n".join(nav_yaml(NAV)) + "\n")


# ------------------------------------------------------------------------------------ main


def pages_in(items: list, trail: tuple[str, ...] = ()):
    for item in items:
        if isinstance(item, Page):
            yield trail, item
        else:
            yield from pages_in(item[1], trail + (item[0],))


def check_site_map(pages: list[Page]) -> None:
    dests, sources = set(), set()
    for page in pages:
        if page.dest in dests:
            raise BuildError(f"site map: {page.dest} is used twice")
        dests.add(page.dest)
        if page.source is None:
            continue
        if page.source in sources:
            raise BuildError(f"site map: {page.source} is listed twice")
        sources.add(page.source)
        if is_key(page.source):
            raise BuildError(f"site map: {page.source} is an answer key; it must never be staged")
        if OUT_OF_SCOPE.search(page.source):
            raise BuildError(f"site map: {page.source} is out of scope for v0 (docs/site-spec.md)")
        if not (REPO / page.source).is_file():
            raise BuildError(f"site map: {page.source} does not exist")
    for gap in GAPS:
        if gap.source not in sources:
            raise BuildError(f"GAPS: {gap.source} is not in the site map")


def main() -> int:
    for stream in (sys.stdout, sys.stderr):   # a cp1252 console must not crash on a quote
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="backslashreplace")
    entries = list(pages_in(NAV))
    pages = [page for _, page in entries]
    try:
        check_site_map(pages)
        if STAGING.parent != REPO or STAGING.name != "_staging":
            raise BuildError(f"refusing to clear unexpected staging dir {STAGING}")
        if STAGING.exists():
            shutil.rmtree(STAGING)
        dest_of = {p.source: p.dest for p in pages if p.source}   # analysis.py -> its code page
        report = Report()
        sessions = {p.source: i for i, p in enumerate(SESSIONS)}
        for page in pages:
            if page is HOME:
                text = stage_home(dest_of, report)
            elif page is INTERACTIVE:
                text = stage_interactive()
            elif page.code:
                text = stage_code(page)
            else:
                prereq = None
                if page.source in sessions:
                    i = sessions[page.source]
                    if i == 0:
                        prereq = f"**Prerequisite:** {FIRST_PREREQUISITE}."
                    else:
                        prev = SESSIONS[i - 1]
                        link = posixpath.relpath(prev.dest, posixpath.dirname(page.dest))
                        prereq = f"**Prerequisite:** [{prev.label}]({link})"
                text = stage_markdown(page, dest_of, report, prereq)
            write(STAGING / page.dest, text)
        write_mkdocs_yml()
    except BuildError as err:
        print(f"build_site.py: ERROR: {err}", file=sys.stderr)
        return 1

    print(f"build_site.py: staged {len(pages)} pages into {STAGING.name}/ and wrote {MKDOCS_YML.name}")
    print("  nav -> source (every site-map file, in nav order):")
    for trail, page in entries:
        where = " / ".join(trail + (page.label,))
        origin = page.source or ("generated from " + f"{COURSE}/README.md" if page is HOME
                                 else "generated placeholder")
        print(f"    {where:<58} {origin}")
    print(f"  links: {report.internal} re-pointed at staged pages, {report.github} sent to GitHub, "
          f"{len(report.unlinked)} removed (text kept):")
    for src, text, target in report.unlinked:
        why = "answer key" if is_key(target) else "audit/review notes"
        print(f"    {src}: [{' '.join(text.split())}] -> {target} ({why})")
    for gap in GAPS:
        print(f"  in development: {gap.source}, hour {gap.hour} (banner + status front matter)")
    boxes = sum(p.exercise for p in pages)
    print(f"  solutions box: {boxes} exercise pages; solutions_url = "
          f"{SOLUTIONS_URL or '(empty: the box is shown without a link)'}")
    for src, n in report.lists_separated.items():
        print(f"  lists separated from a preceding paragraph: {src} x{n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
