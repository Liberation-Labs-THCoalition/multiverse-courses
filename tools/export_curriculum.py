#!/usr/bin/env python3
"""Export the student-facing course as a folder of Markdown for the Multiverse School's /curriculum/upload.

    python tools/build_site.py                      # first: the export reads the site's staging output
    python tools/export_curriculum.py OUT_DIR       # writes OUT_DIR, or refuses and writes nothing

The upload takes a folder of Markdown, keeps its structure, titles each page from its first "#" heading, links the
pages to the class for access, and skips pages that already exist. So this script:

- reads `_staging/`, never raw repo files, so the export inherits every exclusion the site already has (the same
  rule as tools/publish_hedgedoc.py);
- takes every page in mkdocs.yml's nav except the "For instructors" section and pages still marked "(coming)":
  students get the course, and instructors keep using the site;
- strips front matter, so each page starts at its "#" title, and refuses a page that doesn't;
- rewrites relative links to the public site's URLs, because an uploaded page can't resolve a repo path (fenced
  code is left alone);
- runs the answer-key gate before anything is kept: tools/publish_hedgedoc.key_gate (imported, not copied) on
  `_staging/` and on the export, then tools/check_public_build.py on the export, then a positive control on a copy
  (a planted key line and a planted facilitator page must both be caught). Any finding, or a plant that isn't
  caught, and nothing is written.
"""
from __future__ import annotations

import argparse
import posixpath
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import yaml                            # noqa: E402  (installed with mkdocs: requirements-site.txt)
import build_site                      # noqa: E402  STAGING, SITE_URL, split_front_matter, outside_code
import check_public_build as cpb       # noqa: E402  the key definitions
import publish_hedgedoc                # noqa: E402  key_gate: the gate HedgeDoc publishing already uses

STAGING = build_site.STAGING
SITE_URL = build_site.SITE_URL         # ends with "/"
LEFT_OUT_SECTIONS = {"For instructors"}
LINK = re.compile(r"(!?\[[^\]]*\]\()([^)\s]+)(\))")


class ExportError(Exception):
    pass


def nav_pages(mkdocs_yml: Path) -> list[str]:
    """Every page path in the nav, minus the left-out sections and any '(coming)' page."""
    class NavLoader(yaml.SafeLoader):
        """mkdocs.yml holds python/object tags (a slugify function); the nav needs none of them, so they load as
        None. Safe: nothing is constructed or run."""
    NavLoader.add_multi_constructor("tag:yaml.org,2002:python/", lambda loader, suffix, node: None)
    nav = yaml.load(mkdocs_yml.read_text(encoding="utf-8"), Loader=NavLoader)["nav"]
    out: list[str] = []

    def walk(items):
        for item in items:
            for title, value in item.items():
                if title in LEFT_OUT_SECTIONS or "(coming)" in title:
                    continue
                if isinstance(value, list):
                    walk(value)
                else:
                    out.append(value)
    walk(nav)
    return out


def page_url(rel: str) -> str:
    """The public URL MkDocs gives a page (use_directory_urls: true)."""
    stem = rel[:-3]
    if stem == "index" or stem.endswith("/index"):
        return SITE_URL + stem[: -len("index")]
    return SITE_URL + stem + "/"


def absolutise(text: str, rel: str) -> str:
    here = posixpath.dirname(rel)

    def fix(m: re.Match) -> str:
        target = m.group(2)
        if re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I) or target.startswith(("#", "/")):
            return m.group(0)                      # absolute URL, mailto:, in-page anchor, or site-absolute
        path, _, anchor = target.partition("#")
        resolved = posixpath.normpath(posixpath.join(here, path))
        if resolved.startswith(".."):
            raise ExportError(f"{rel}: link {target!r} leaves the site")
        url = page_url(resolved) if resolved.endswith(".md") else SITE_URL + resolved
        return m.group(1) + url + (("#" + anchor) if anchor else "") + m.group(3)

    return build_site.outside_code(text, lambda chunk: LINK.sub(fix, chunk))


ADMONITION = re.compile(r'^!!!\s+(\w+)(?:\s+"([^"]*)")?\s*$')
LEADING_COMMENT = re.compile(r"\A\s*<!--.*?-->\s*", re.S)


def plain_admonitions(text: str) -> str:
    """MkDocs admonitions (`!!! kind "Title"` + a 4-space-indented body) become blockquotes. A plain Markdown
    renderer would show the marker as text and the indented body as a code block."""
    lines, out, i = text.split("\n"), [], 0
    while i < len(lines):
        m = ADMONITION.match(lines[i])
        if not m:
            out.append(lines[i])
            i += 1
            continue
        out.append(f"> **{m.group(2) or m.group(1).capitalize()}**")
        i += 1
        while i < len(lines) and (lines[i].startswith("    ") or
                                  (lines[i] == "" and i + 1 < len(lines) and lines[i + 1].startswith("    "))):
            out.append(">" if lines[i] == "" else "> " + lines[i][4:])
            i += 1
    return "\n".join(out)


def export(out: Path, staging: Path = STAGING) -> list[str]:
    if not staging.is_dir():
        raise ExportError(f"{staging} is missing: run `python tools/build_site.py` first")
    pages = nav_pages(build_site.REPO / "mkdocs.yml")
    written: list[str] = []
    for rel in pages:
        src = staging / rel
        if not src.is_file():
            raise ExportError(f"nav page {rel} is not in {staging}: rebuild the staging output")
        _front, body = build_site.split_front_matter(src.read_text(encoding="utf-8"))
        body = LEADING_COMMENT.sub("", body, count=1).lstrip("\n")   # the generator's provenance comment
        body = build_site.outside_code(body, plain_admonitions)
        if not body.startswith("# "):
            raise ExportError(f"{rel}: the upload titles a page from its first '#', and this page has none")
        dest = out / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(absolutise(body, rel), encoding="utf-8", newline="\n")
        written.append(rel)
    return written


def positive_control(out: Path, keys) -> list[str]:
    """The gate must be able to fail on THIS export. check_public_build's --self-test plants into built HTML pages,
    so it can't run on a Markdown folder; this does the equivalent here, on a copy:
      1. the clean copy passes;
      2. one distinctive line of a real key, planted in a session page, is caught;
      3. a page whose front matter says `audience: facilitator` is caught.
    A plant that isn't caught means a gate that can't fail, and the export is refused."""
    problems: list[str] = []
    source = max(keys, key=lambda k: len(k.distinctive))
    if not source.distinctive:
        return ["positive control: no key has a plaintext line to plant (fingerprint-only keys)"]
    line = source.distinctive[0][1]          # (normalised, line): plant the line as it appears in the key
    with tempfile.TemporaryDirectory(prefix="curriculum-control-") as tmp:
        copy = Path(tmp) / "c"
        shutil.copytree(out, copy)
        if publish_hedgedoc.key_gate(keys, [copy]):
            problems.append("positive control: the clean copy did not pass")
        page = copy / "sessions" / "session-1-the-question.md"
        clean = page.read_text(encoding="utf-8")
        page.write_text(clean + "\n" + line + "\n", encoding="utf-8")
        if not publish_hedgedoc.key_gate(keys, [copy]):
            problems.append(f"positive control: a line of {source.rel} planted in session 1 was NOT caught")
        page.write_text(clean, encoding="utf-8")
        (copy / "planted.md").write_text("---\naudience: facilitator\n---\n# Planted\n", encoding="utf-8")
        if not publish_hedgedoc.key_gate(keys, [copy]):
            problems.append("positive control: a page marked audience: facilitator was NOT caught")
    return problems


def gate(out: Path) -> list[str]:
    """Every reason to refuse. Empty means the export may be kept."""
    problems: list[str] = []
    keys = cpb.discover(build_site.REPO, site=STAGING)
    for f in publish_hedgedoc.key_gate(keys, [STAGING, out]):
        problems.append(f"key gate: {f}")
    p = subprocess.run([sys.executable, str(TOOLS / "check_public_build.py"), str(out)],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if p.returncode != 0:
        tail = (p.stdout + p.stderr).strip().splitlines()[-3:]
        problems.append(f"check_public_build exited {p.returncode}: " + " | ".join(tail))
    problems += positive_control(out, keys)
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("out", type=Path, help="folder to write (must not exist yet)")
    a = ap.parse_args(argv)
    if a.out.exists():
        print(f"export_curriculum.py: {a.out} already exists; give a new folder", file=sys.stderr)
        return 2
    with tempfile.TemporaryDirectory(prefix="curriculum-export-") as tmp:
        work = Path(tmp) / "curriculum"
        try:
            written = export(work)
        except ExportError as e:
            print(f"export_curriculum.py: REFUSING -- {e}", file=sys.stderr)
            return 1
        problems = gate(work)
        if problems:
            print(f"export_curriculum.py: REFUSING -- {len(problems)} problem(s); nothing written:", file=sys.stderr)
            for p in problems:
                print("  " + p, file=sys.stderr)
            return 1
        shutil.copytree(work, a.out)
    print(f"export_curriculum.py: {len(written)} pages written to {a.out}; key gate clean, check_public_build "
          f"passed, and the positive control caught both planted keys")
    for rel in written:
        print("  " + rel)
    return 0


if __name__ == "__main__":
    sys.exit(main())
