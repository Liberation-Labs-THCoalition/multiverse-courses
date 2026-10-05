#!/usr/bin/env python3
"""Publish a cohort's notes to HedgeDoc. docs/run-card-hedgedoc-v1.md, item 3.

    python tools/publish_hedgedoc.py --cohort 2026-10a
    python tools/publish_hedgedoc.py --cohort 2026-10a --base-url http://localhost:3000
    python tools/publish_hedgedoc.py --cohort 2026-10a --dry-run ./preview

The input is the site's staging output (_staging/), never raw repo files, so HedgeDoc inherits
every exclusion the site already has (run `python tools/build_site.py` first). For each cohort
we build:

  vr-<cohort>-hub            the cohort's front page
  vr-<cohort>-s1 .. s4       the session's lesson as the site renders it, plus a "## Cohort notes"
                             section that starts empty and is edited live in class
  vr-<cohort>-s<n>-slides    the same lesson as a reveal.js deck (stretch goal)

Before anything is sent, the same answer-key detection as tools/check_public_build.py runs on
every payload -- and, so a key planted anywhere in _staging is caught, on the whole staging dir
too. If anything matches, publication is refused. (The detection is imported from
check_public_build, not re-implemented: a publisher that shared the builder's idea of what is
public would share its blind spots.)

We create only. An alias that already exists is reported and skipped, never overwritten -- so a
re-running cohort cannot clobber a returning student's edits. Each note we create is then
verified: its `GET /<alias>/download` must equal the payload byte for byte (a trailing newline is
allowed). A table of alias, status and URL is printed.

`--dry-run DIR` writes the payloads to DIR and sends nothing.

No network call is made except to a loopback host; a --base-url pointing elsewhere is refused.
"""
from __future__ import annotations

import argparse
import re
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import build_site                    # noqa: E402  site map: session pages, links, cohort-links
import check_public_build as cpb      # noqa: E402  the answer-key detection -- imported, not copied

REPO = build_site.REPO
STAGING = build_site.STAGING

DEFAULT_BASE_URL = "http://localhost:3000"
LOOPBACK_HOSTS = {"localhost", "127.0.0.1", "::1"}

# A cohort note's live-edit section, appended to each session payload. It starts empty; the cohort
# fills it in during the class.
COHORT_NOTES_HEADING = "## Cohort notes"

# The global index of every past cohort's hub (docs/run-card-hedgedoc-v1.md, item 6 updates it).
PAST_COHORTS = "vr-past-cohorts"

# reveal.js slide breaks: a new "## Hour" heading starts a slide; a "###" inside an hour a
# sub-slide. Only separator lines are inserted -- no words change.
HOUR = re.compile(r"^##[ \t]+Hour\b")
SUB = re.compile(r"^###[ \t]")


class PublishError(Exception):
    pass


# ---------------------------------------------------------------------------------- payloads


def hub_payload(cohort: str, base_url: str) -> str:
    """The cohort's front page: title, a link to each session note, a link to the public site and
    the repo, a link back to vr-past-cohorts, and a Links section from docs/cohort-links.md."""
    lines = [f"# {build_site.SITE_NAME} — cohort {cohort}", "", "## Sessions", ""]
    for i, page in enumerate(build_site.SESSIONS, 1):
        lines.append(f"- [{page.label}]({base_url}/vr-{cohort}-s{i})")
    lines += ["", "## Elsewhere", ""]
    lines.append(f"- [Public site]({build_site.SITE_URL})")
    lines.append(f"- [Repository]({build_site.GITHUB})")
    lines.append(f"- [Coming back from an earlier cohort? Your notes are here]"
                 f"({base_url}/{PAST_COHORTS})")
    lines += [""]
    lines += [build_site.cohort_links_section().strip()]    # "## Links" + the list, comment stripped
    lines += [""]
    return "\n".join(lines).rstrip("\n") + "\n"


def session_payload(staged: Path, i: int) -> str:
    """The session's note: the lesson exactly as the site renders it, then an empty
    "## Cohort notes"."""
    body = staged.read_text(encoding="utf-8")
    return body.rstrip("\n") + "\n\n" + COHORT_NOTES_HEADING + "\n"


def slide_payload(staged: Path, i: int) -> str:
    """The session's note as a reveal.js deck (stretch goal): the session payload with slide front
    matter, a `---` before each "## Hour" heading and a `----` before each "###". No words change."""
    body = session_payload(staged, i)
    out: list[str] = []
    for line in body.split("\n"):
        if HOUR.match(line):
            sep = "---"
        elif SUB.match(line):
            sep = "----"
        else:
            sep = None
        if sep:
            if out and out[-1].strip() != "":
                out.append("")
            out.append(sep)
        out.append(line)
    front = "---\ntype: slide\nslideOptions: {transition: slide}\n---\n\n"
    return front + "\n".join(out).rstrip("\n") + "\n"


def build_payloads(cohort: str, base_url: str, staging: Path) -> list[tuple[str, str, str]]:
    """(alias, filename, content) for the hub, the four sessions, and their slide decks."""
    payloads: list[tuple[str, str, str]] = []
    payloads.append((f"vr-{cohort}-hub", "hub.md", hub_payload(cohort, base_url)))
    for i, page in enumerate(build_site.SESSIONS, 1):
        staged = staging / page.dest
        payloads.append((f"vr-{cohort}-s{i}", f"s{i}.md", session_payload(staged, i)))
    for i, page in enumerate(build_site.SESSIONS, 1):
        staged = staging / page.dest
        payloads.append((f"vr-{cohort}-s{i}-slides", f"s{i}-slides.md", slide_payload(staged, i)))
    return payloads


# --------------------------------------------------------------- answer-key detection gate


def key_gate(keys, dirs: list[Path]) -> list[cpb.Finding]:
    """Run check_public_build.check on each dir and return all findings. This is the same
    detection as tools/check_public_build.py, imported -- not copied."""
    findings: list[cpb.Finding] = []
    for d in dirs:
        found, _ = cpb.check(d, keys)
        findings += found
        # Lyra review 2026-10-05: cpb.check catches key-NAMED files and copies of KNOWN keys, but
        # it does not apply the front-matter rule to the files it scans. A staged markdown file
        # whose front matter says `audience: facilitator` passed this gate. cpb.key_reason is the
        # same rule check_public_build uses to define a key, imported, not copied.
        for p in sorted(Path(d).rglob("*.md")):
            if cpb.key_reason(p) == "front matter":
                findings.append(cpb.Finding(str(p.relative_to(d)), "front-matter",
                                            "front matter says audience: facilitator"))
    return findings


# ----------------------------------------------------------------------------- HedgeDoc API


def assert_loopback(base_url: str) -> None:
    host = urllib.parse.urlparse(base_url).hostname or ""
    if host not in LOOPBACK_HOSTS:
        raise PublishError(
            f"refusing to publish to a non-loopback host: {base_url!r} "
            "(the card allows no network call except to localhost)")


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """Keep the 302 from POST /new so we can tell 'created' from 'already exists'."""
    def redirect_request(self, *a, **k):
        return None


def http_get(base_url: str, path: str) -> tuple[int, bytes]:
    url = base_url.rstrip("/") + "/" + path.lstrip("/")
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return r.getcode(), r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def http_create(base_url: str, alias: str, data: bytes) -> int:
    """POST /new/<alias>; returns the status code. 302 = created, 409 = already exists."""
    url = base_url.rstrip("/") + "/new/" + urllib.parse.quote(alias, safe="")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "text/markdown")
    opener = urllib.request.build_opener(_NoRedirect)
    try:
        with opener.open(req, timeout=30) as r:
            return r.getcode()
    except urllib.error.HTTPError as e:
        return e.code


def notes_match(payload: bytes, downloaded: bytes) -> bool:
    """Byte for byte, allowing a trailing newline (HedgeDoc may add one on storage)."""
    return payload.rstrip(b"\n") == downloaded.rstrip(b"\n")


# ------------------------------------------------------------------------------ main / CLI


def run(cohort: str, base_url: str, dry_run: Path | None) -> int:
    assert_loopback(base_url)
    if not STAGING.is_dir():
        raise PublishError(f"{STAGING} not found -- run `python tools/build_site.py` first")

    keys = cpb.discover(REPO, site=STAGING)
    payloads = build_payloads(cohort, base_url, STAGING)
    # Gate 1: the whole staging output, so a key planted anywhere in _staging is caught.
    # Gate 2: the assembled payloads themselves.
    with tempfile.TemporaryDirectory(prefix="publish-hedgedoc-") as tmp:
        work = Path(tmp)
        for alias, name, content in payloads:
            (work / name).write_text(content, encoding="utf-8")
        findings = key_gate(keys, [STAGING, work])
    if findings:
        print(f"publish_hedgedoc.py: REFUSING -- answer-key material, {len(findings)} "
              f"finding(s):")
        for f in findings:
            print(f"    [{f.kind}] {f.file}: {f.detail}")
        return 1

    url_of = lambda alias: f"{base_url.rstrip('/')}/{alias}"

    if dry_run is not None:
        dry_run.mkdir(parents=True, exist_ok=True)
        for alias, name, content in payloads:
            (dry_run / f"{alias}.md").write_text(content, encoding="utf-8")
        print(f"publish_hedgedoc.py: --dry-run: wrote {len(payloads)} payload(s) to {dry_run} "
              f"(nothing sent):")
        for alias, _, _ in payloads:
            print(f"    {alias:<24} {'written (dry-run)':<22} {url_of(alias)}")
        return 0

    print(f"publish_hedgedoc.py: cohort {cohort} -> {base_url} (create-only, never overwrite)")
    ok = True
    for alias, name, content in payloads:
        code, _ = http_get(base_url, f"{alias}/info")
        if code == 200:
            print(f"    {alias:<24} {'skipped (already exists)':<22} {url_of(alias)}")
            continue
        data = content.encode("utf-8")
        status = http_create(base_url, alias, data)
        if status == 409:                       # a race: someone else created it first
            print(f"    {alias:<24} {'skipped (created meanwhile)':<22} {url_of(alias)}")
            continue
        if status not in (302, 200, 201):
            raise PublishError(f"{alias}: POST /new returned HTTP {status}")
        code, got = http_get(base_url, f"{alias}/download")
        if code != 200:
            raise PublishError(f"{alias}: GET /download returned HTTP {code} after creating")
        if not notes_match(data, got):
            ok = False
            print(f"    {alias:<24} {'VERIFY FAILED':<22} {url_of(alias)}")
            continue
        print(f"    {alias:<24} {'published (verified)':<22} {url_of(alias)}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):      # a cp1252 console must not crash on a quote
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="backslashreplace")
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--cohort", default=None,
                       help="cohort id, e.g. 2026-10a (required for a real publish)")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL,
                       help=f"HedgeDoc base URL (default: {DEFAULT_BASE_URL})")
    parser.add_argument("--dry-run", metavar="DIR", dest="dry_run", nargs="?", const="__AUTO__",
                       default=None,
                       help="write the payloads to DIR and send nothing (no DIR: a temp dir)")
    args = parser.parse_args(argv)

    cohort = args.cohort or "dry-run"           # a dry run needs no real cohort to name its payloads
    if args.cohort is None and args.dry_run is None:
        print("publish_hedgedoc.py: --cohort is required for a real publish "
              "(omit --dry-run only with a cohort)", file=sys.stderr)
        return 2

    out = Path(args.dry_run) if (args.dry_run and args.dry_run != "__AUTO__") else None
    if args.dry_run == "__AUTO__":
        out = Path(tempfile.mkdtemp(prefix="publish-dryrun-"))
    try:
        return run(cohort, args.base_url, out)
    except PublishError as err:
        print(f"publish_hedgedoc.py: ERROR: {err}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
