#!/usr/bin/env python3
"""Check internal links in the course site and the splash, as GitHub Pages serves them.

    python tools/check_links.py                 # assemble splash/dist + site/ like pages.yml, then check
    python tools/check_links.py --tree _site    # check a tree that is already assembled
    python tools/check_links.py --self-test     # the planted-link controls

The check runs on the DEPLOYED layout, not on each build alone. `.github/workflows/pages.yml` copies
`splash/dist/` to the root of `_site/` and `site/` to `_site/course/`, and Pages serves `_site/` under the
project path `/multiverse-courses/`. That path is read from `SITE_URL` in `tools/build_site.py`, minus the
course mount, so it is configuration and is never inferred from the links being checked. (The first version
inferred it from the links, which let a broken root-absolute link vouch for itself. Found in review,
2026-10-05.)

How each `href` / `src` is judged:
- external: has a scheme (`https:`, `mailto:`, ...) or starts `//host`. Listed, never fetched. The one
  exception is a full URL into this project (`https://<origin>/multiverse-courses/...`): that is our own site
  written out in full, so it is checked like the root-absolute path it names.
- a bare fragment or query (`#x`, `?x`): an in-page anchor, skipped.
- relative (`x`, `./x`, `../x`): resolved against the page's own directory in the tree.
- root-absolute (`/x`): must start with the project path. The rest is resolved from the tree's root. A
  root-absolute link outside the project path is BROKEN: on Pages it leaves this site.
- A target is OK when it is a file, or a directory holding index.html / index.htm, AND it is inside the tree.
  A path that climbs out of the tree is BROKEN even if the file exists on this disk.
- Percent-escapes are decoded before the lookup (`a%20b.html` is the file `a b.html`).

Not checked: `srcset`, CSS `url()`, and letter case on case-insensitive disks (Windows). Pages is
case-sensitive, so run it on Linux (CI or MTH) to catch case errors.

--self-test plants each kind of link above in a temporary assembled copy, broken and valid alike, and requires
every verdict to come out as expected. It never writes to a real build.

Exit status: 0 no broken internal links (or a self-test that behaved); 1 broken links (or a self-test that did
not behave); 2 the check could not run (a build directory or SITE_URL is missing).
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

REPO = Path(__file__).resolve().parent.parent
DEFAULT_SITE = REPO / "site"
DEFAULT_SPLASH = REPO / "splash" / "dist"
BUILD_SITE = REPO / "tools" / "build_site.py"
COURSE_MOUNT = "course"  # pages.yml: cp -R site _site/course
HTML_EXT = {".html", ".htm"}
INDEX_NAMES = ("index.html", "index.htm")
# A link that begins with "<scheme>:" or "//" is external (or not a path to a file).
EXTERNAL = re.compile(r"^(?:[a-z][a-z0-9+.-]*:|//)", re.I)
SITE_URL_RE = re.compile(r"""^SITE_URL\s*=\s*["']([^"']+)["']""", re.M)


class LinkCollector(HTMLParser):
    """Collect href and src attribute values from an HTML document."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[str] = []

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if value is not None and name in ("href", "src"):
                self.links.append(value.strip())


def pages_location(build_site: Path = BUILD_SITE) -> tuple[str, str]:
    """(origin, project path) of the deployed site, from SITE_URL in build_site.py.

    SITE_URL is the course's URL (https://host/multiverse-courses/course/). The project path is that path
    without the course mount. Raises ValueError when SITE_URL is missing or doesn't end in the mount, so a
    changed layout stops the check instead of silently mis-resolving every link."""
    match = SITE_URL_RE.search(build_site.read_text(encoding="utf-8"))
    if not match:
        raise ValueError(f"no SITE_URL in {build_site}")
    url = urlsplit(match.group(1))
    path = url.path if url.path.endswith("/") else url.path + "/"
    mount = f"/{COURSE_MOUNT}/"
    if not path.endswith(mount):
        raise ValueError(f"SITE_URL's path {path!r} does not end in {mount!r}: has pages.yml's layout changed?")
    return f"{url.scheme}://{url.netloc}", path[: len(path) - len(mount) + 1]


def assemble(splash: Path, site: Path, dest: Path) -> Path:
    """The deployed tree, built the way pages.yml builds it: the splash at the root, the course under course/."""
    shutil.copytree(splash, dest)
    shutil.copytree(site, dest / COURSE_MOUNT, dirs_exist_ok=True)
    return dest


def in_project(path: str, prefix: str) -> bool:
    return path.startswith(prefix) or path + "/" == prefix


def target_ok(tree: Path, page: Path, link: str, prefix: str) -> bool:
    """True when an internal link names an existing file, or a directory with an index, inside the tree."""
    path = unquote(link.split("#", 1)[0].split("?", 1)[0])
    if not path:
        return True  # '#x' or '?x': an in-page anchor, not a file
    if path.startswith("/"):
        if not in_project(path, prefix):
            return False  # on Pages this leaves the project's site
        target = tree / path[len(prefix):]
    else:
        target = page.parent / path
    target = Path(os.path.normpath(target))  # '..' is resolved by name, never through the local disk
    if target != tree and tree not in target.parents:
        return False  # climbs out of the deployed tree
    if target.is_file():
        return True
    return target.is_dir() and any((target / name).is_file() for name in INDEX_NAMES)


def check_tree(tree: Path, origin: str, prefix: str) -> tuple[list[str], list[str], int]:
    """Return (broken, external, html_count) for one assembled tree."""
    tree = Path(os.path.normpath(tree.resolve()))
    broken: list[str] = []
    external: set[str] = set()
    pages = sorted(p for p in tree.rglob("*") if p.suffix.lower() in HTML_EXT and p.is_file())
    for page in pages:
        where = page.relative_to(tree).as_posix()
        try:
            text = page.read_bytes().decode("utf-8-sig")
        except (OSError, UnicodeDecodeError) as exc:
            broken.append(f"{where}: (page unreadable: {type(exc).__name__})")
            continue
        collector = LinkCollector()
        collector.feed(text)
        for link in collector.links:
            if not link:
                continue
            if link.startswith(origin + "/") and in_project(urlsplit(link).path, prefix):
                link_to_check = link[len(origin):]  # this project, written as a full URL
            elif EXTERNAL.match(link):
                external.add(link)
                continue
            else:
                link_to_check = link
            if not target_ok(tree, page, link_to_check, prefix):
                broken.append(f"{where}: {link}")
    return broken, sorted(external), len(pages)


def report(broken: list[str], external: list[str], html_count: int, label: str) -> int:
    print(f"check_links.py: {label}")
    print(f"   {html_count} HTML file(s), {len(external)} external link(s) listed (not fetched)")
    if external:
        print("  external (listed only, not fetched):")
        for link in external:
            print(f"     - {link}")
    if broken:
        print(f"  FAIL: {len(broken)} broken internal link(s):")
        for item in broken:
            print(f"     [broken] {item}")
        return 1
    print("  PASS: no broken internal links")
    return 0


def plants(origin: str, prefix: str) -> list[tuple[str, str, str, bool]]:
    """(what it is, page in the tree, tag to plant, must it be reported?). Broken and valid kinds alike: a
    checker that reports everything would fail the valid rows, and one that reports nothing the broken rows."""
    return [
        ("relative link to a missing file", "index.html",
         '<a href="definitely-missing-file.html">x</a>', True),
        ("root-absolute link outside the project path", "index.html",
         '<a href="/no-such-page/">x</a>', True),
        ("root-absolute link inside the project path, to a missing page", "index.html",
         f'<a href="{prefix}{COURSE_MOUNT}/no-such-page/">x</a>', True),
        ("full URL into this project, to a missing page", f"{COURSE_MOUNT}/index.html",
         f'<a href="{origin}{prefix}{COURSE_MOUNT}/no-such-page/">x</a>', True),
        ("relative link climbing out of the tree to a file that exists on disk", "index.html",
         '<a href="../outside.html">x</a>', True),
        ("one broken root-absolute image (src, not href)", "index.html",
         '<img src="/missing-image.png" alt="">', True),
        ("VALID: relative link from the course up to the splash", f"{COURSE_MOUNT}/index.html",
         '<a href="../index.html">x</a>', False),
        ("VALID: root-absolute link to the course", "index.html",
         f'<a href="{prefix}{COURSE_MOUNT}/">x</a>', False),
        ("VALID: full URL to another project on the same origin (external)", "index.html",
         f'<a href="{origin}/another-project/">x</a>', False),
    ]


def self_test(tree: Path, origin: str, prefix: str) -> int:
    print("check_links.py: self-test on a temporary assembled copy (real builds are not touched)")
    (tree.parent / "outside.html").write_text("<!doctype html><p>outside the tree</p>", encoding="utf-8")
    baseline, _, _ = check_tree(tree, origin, prefix)
    ok = not baseline
    print(f"    {'ok  ' if ok else 'FAIL'}  control: the unmodified copy is "
          f"{'clean' if ok else f'NOT clean ({len(baseline)} broken)'}")
    for what, rel, tag, must_report in plants(origin, prefix):
        page = tree / rel
        original = page.read_bytes()
        html = original.decode("utf-8-sig")
        planted_html = html.replace("</body>", tag + "</body>", 1) if "</body>" in html else html + tag
        page.write_text(planted_html, encoding="utf-8")
        try:
            broken, _, _ = check_tree(tree, origin, prefix)
        finally:
            page.write_bytes(original)
        reported = len(broken) > len(baseline)
        good = reported == must_report
        ok = ok and good
        verdict = "reported" if reported else "passed"
        print(f"    {'ok  ' if good else 'FAIL'}  {what}: {verdict}")
    after, _, _ = check_tree(tree, origin, prefix)
    clean_again = after == baseline
    ok = ok and clean_again
    print(f"    {'ok  ' if clean_again else 'FAIL'}  the copy is back to its baseline after the plants")
    print("self-test PASSED: every planted link got the expected verdict." if ok
          else "self-test FAILED: see the FAIL rows above.")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="backslashreplace")
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--site", type=Path, default=DEFAULT_SITE, help="the built course site (default: site/)")
    parser.add_argument("--splash", type=Path, default=DEFAULT_SPLASH,
                        help="the built splash (default: splash/dist/)")
    parser.add_argument("--tree", type=Path, help="check an already-assembled tree (pages.yml's _site) instead")
    parser.add_argument("--self-test", action="store_true",
                        help="the planted-link controls, on a temporary copy; does not touch real builds")
    args = parser.parse_args(argv)

    try:
        origin, prefix = pages_location()
    except (OSError, ValueError) as exc:
        print(f"check_links.py: cannot locate the deployed site: {exc}", file=sys.stderr)
        return 2

    if args.tree is not None and not args.self_test:
        if not args.tree.is_dir():
            print(f"check_links.py: no such tree: {args.tree}", file=sys.stderr)
            return 2
        broken, external, count = check_tree(args.tree, origin, prefix)
        return report(broken, external, count, f"{args.tree} as served at {origin}{prefix}")

    missing = [d for d in (args.splash, args.site) if not d.is_dir()]
    if missing:
        for d in missing:
            print(f"check_links.py: no such built directory: {d}", file=sys.stderr)
        return 2
    with tempfile.TemporaryDirectory(prefix="check-links-") as tmp:
        tree = assemble(args.splash, args.site, Path(tmp) / "_site")
        if args.self_test:
            return self_test(tree, origin, prefix)
        broken, external, count = check_tree(tree, origin, prefix)
        return report(broken, external, count,
                      f"{args.splash} + {args.site}, assembled like pages.yml, as served at {origin}{prefix}")


if __name__ == "__main__":
    sys.exit(main())
