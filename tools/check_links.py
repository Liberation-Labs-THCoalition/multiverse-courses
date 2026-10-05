#!/usr/bin/env python3
"""Check internal links in the built course site and the built splash.

    python tools/check_links.py [SITE_DIR SPLASH_DIR]
    python tools/check_links.py --self-test

Every internal ``href``/``src`` in the built course site (default ``site/``) and
the built splash (default ``splash/dist/``) is resolved against its built directory
and checked for existence on disk. A broken internal target is reported, and the
exit status is 1.

What counts as internal, external, or not-a-file-link:
    - external: carries a scheme (``http``, ``https``, ``mailto``, ``tel``, ...),
     or is protocol-relative (``//host``). These are NOT fetched; they are listed
     only, as the card requires.
    - fragment: a bare in-page anchor (``#section``). It is not a link to a file and
     is ignored.
    - internal: a relative (``./x``, ``../x``) or root-absolute (``/x``) path. A
     relative link resolves against the HTML file's own directory. A root-absolute
     one is resolved against the built directory, and also with the deployment base
     stripped: a site built for a sub-path (MkDocs with a ``site_url``) emits links
     like ``/multiverse-courses/course/cohort-hub/`` that live locally at
     ``site/cohort-hub/`` -- correct for the deployed site, so neither kind is a
     false positive. A query string and a fragment are stripped. The target is OK
     when it exists as a file, or as a directory holding an ``index.html`` /
     ``index.htm`` (so a link like ``/course/`` is fine). Otherwise it is broken.

--self-test is the positive control: it copies a built directory into a temporary
folder, plants a page that links to a file that does not exist, and shows the
checker failing on the copy while the real build still passes. It never writes to
a real build.

Exit status: 0 no broken internal links (or a self-test that behaved); 1 one or
more broken internal links, or a self-test that did not behave; 2 a built
directory is missing, so the check could not run.
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DEFAULT_SITE = REPO / "site"
DEFAULT_SPLASH = REPO / "splash" / "dist"
HTML_EXT = {".html", ".htm"}
INDEX_NAMES = ("index.html", "index.htm")
# A link that begins with "<scheme>:" or "//" is external (or not a path to a file).
EXTERNAL = re.compile(r"^(?:[a-z][a-z0-9+.-]*:|//)", re.I)


class LinkCollector(HTMLParser):
    """Collect href and src attribute values from an HTML document."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[str] = []

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if value is None:
                continue
            if name in ("href", "src"):
                self.links.append(value.strip())


def is_external(link: str) -> bool:
    return bool(EXTERNAL.match(link))


def path_segments(path_part: str) -> list[str]:
    """Path segments of a link, without empty segments and '.' ('..' is kept)."""
    return [p for p in path_part.split("/") if p not in ("", ".")]


def detect_base(root_abs_links: list[str]) -> str:
    """The deployment base: the path prefix shared by every root-absolute link."""
    seg_lists = [path_segments(l) for l in root_abs_links]
    if not seg_lists:
        return ""
    common: list[str] = []
    for i in range(min(len(s) for s in seg_lists)):
        head = seg_lists[0][i]
        if all(s[i] == head for s in seg_lists):
            common.append(head)
        else:
            break
    return "/" + "/".join(common) + "/" if common else ""


def resolves(root: Path, html_file: Path, link: str, base: str) -> bool:
    """True when an internal link points at a real file or an index-bearing dir."""
    path_part = link.split("#", 1)[0].split("?", 1)[0]
    if link.startswith("#") or not path_part:
        return True     # a bare fragment / query: an in-page anchor, not a file
    if path_part.startswith("/"):
        remainder = path_part[len(base):] if base and path_part.startswith(base) else ""
        candidates = [(root / (remainder or ".")).resolve(),
                      (root / path_part.lstrip("/")).resolve()]
    else:
        candidates = [(html_file.parent / path_part).resolve()]
    for candidate in candidates:
        if candidate.is_file():
            return True
        if candidate.is_dir() and any((candidate / name).is_file() for name in INDEX_NAMES):
            return True
    return False


def check_dir(root: Path) -> tuple[list[str], list[str], int]:
    """Return (broken, external, html_count) for one built directory."""
    broken: list[str] = []
    external: set[str] = set()
    html_files = sorted(p for p in root.rglob("*") if p.suffix.lower() in HTML_EXT)

    # First pass: gather the internal links so the deployment base can be detected
    # before root-absolute ones are resolved (second pass).
    per_file: dict[Path, list[str]] = {}
    root_abs: list[str] = []
    for html in html_files:
        try:
            raw = html.read_bytes().decode("utf-8-sig")
        except (UnicodeDecodeError, OSError):
            continue
        parser = LinkCollector()
        try:
            parser.feed(raw)
        except Exception:
            continue
        links = [l for l in parser.links if l]
        per_file[html] = links
        for link in links:
            if not is_external(link) and link.split("#", 1)[0].startswith("/"):
                root_abs.append(link)
    base = detect_base(root_abs)

    for html, links in per_file.items():
        for link in links:
            if is_external(link):
                external.add(link)
                continue
            if not resolves(root, html, link, base):
                broken.append(f"{html.relative_to(root).as_posix()}: {link}")
    return broken, sorted(external), len(html_files)


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


def self_test(site: Path, splash: Path) -> int:
    print("check_links.py: self-test on a temporary copy (real builds are not touched)")
    source = splash if splash.is_dir() else site
    if not source.is_dir():
        print("  cannot self-test: no built directory to copy")
        return 2
    ok = True
    with tempfile.TemporaryDirectory(prefix="check-links-selftest-") as tmp:
        copy = Path(tmp) / "site"
        shutil.copytree(source, copy)

        # 1) The unmodified copy must pass.
        baseline_broken, _, _ = check_dir(copy)
        ok = ok and not baseline_broken
        print(f"    {'ok   ' if not baseline_broken else 'FAIL'}  control: the unmodified copy "
              f"{'is clean' if not baseline_broken else f'is NOT clean ({len(baseline_broken)} broken)'}")

        # 2) Plant a page that links to a missing file; the check must fail.
        planted = copy / "planted-broken-link.html"
        planted.write_text(
            "<!doctype html><html><body>"
            "<a href=\"definitely-missing-file.html\">x</a></body></html>",
            encoding="utf-8",
        )
        planted_broken, _, _ = check_dir(copy)
        caught = any("definitely-missing-file.html" in b for b in planted_broken)
        ok = ok and caught
        print(f"    {'ok   ' if caught else 'FAIL'}  planted broken link is reported "
              f"({'caught' if caught else 'NOT caught'})")

        # 3) Remove the plant; the copy must pass again.
        planted.unlink()
        after_broken, _, _ = check_dir(copy)
        ok = ok and not after_broken
        print(f"    {'ok   ' if not after_broken else 'FAIL'}  clean again after removal")

    if ok:
        print("self-test PASSED: the clean copy passes and the planted link fails the check.")
        return 0
    print("self-test FAILED: see the FAIL rows above.")
    return 1


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="backslashreplace")
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("dirs", nargs="*",
                        help="built directories to check (default: site/ and splash/dist/)")
    parser.add_argument("--self-test", action="store_true",
                        help="positive control on a temporary copy; does not touch real builds")
    args = parser.parse_args(argv)

    if args.self_test:
        return self_test(DEFAULT_SITE, DEFAULT_SPLASH)

    targets = [Path(d) for d in args.dirs] if args.dirs else [DEFAULT_SITE, DEFAULT_SPLASH]
    missing = [d for d in targets if not d.is_dir()]
    if missing:
        for d in missing:
            print(f"check_links.py: no such built directory: {d}", file=sys.stderr)
        return 2

    status = 0
    for d in targets:
        broken, external, count = check_dir(d)
        status = max(status, report(broken, external, count, str(d)))
    return status


if __name__ == "__main__":
    sys.exit(main())
