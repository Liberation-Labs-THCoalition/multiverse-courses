#!/usr/bin/env python3
"""Snapshot every note of a cohort from HedgeDoc to a dated folder outside the repo.

    python tools/archive_hedgedoc.py --cohort 2026-10a
    python tools/archive_hedgedoc.py --cohort 2026-10a --out ../course-cohort-archives/
    python tools/archive_hedgedoc.py --cohort 2026-10a --base-url http://localhost:3000

docs/run-card-hedgedoc-v1.md, item 6. At the end of a cohort (or whenever wanted) every note of
the cohort is downloaded and saved to a dated snapshot; a later snapshot never overwrites an
earlier one, so students can dig back through old work, or come back after a life event and pick
up where they left off.

What is archived
  The hub, s1-s4, and the four slide decks (these aliases are seeded, they are the cohort's
  notes), plus any note a student made and linked from the hub's "## Links" section or from a
  session's "## Cohort notes" section. Those links are followed breadth-first: a student note that
  links another is captured too. Links to the public site, the repo, or a static file are not
  followed -- only a same-host HedgeDoc alias is.

Where it is written
  <out>/<cohort>/<snapshot UTC timestamp>/<alias>.md, one file per note, plus a manifest.json.
  The default --out is ../course-cohort-archives/, a sibling of the repo: the archive holds
  student work and this repo is public, so it is written OUTSIDE the tree and is never committed
  (.gitignore fences cohort-archives/ and course-cohort-archives/ as a second fence). Writing
  inside the repo's working tree is refused.

The vr-past-cohorts index
  vr-past-cohorts lists every past cohort's hub. We add this cohort's hub link if it is missing and
  never remove a line. This HedgeDoc has no update route (POST /save and /api/v1 are 404; only
  POST /new writes), so the update is create-only: the index is created once, listing this cohort,
  and a re-run leaves it exactly as it is -- the link already there, so the cohort is listed once.

No network call is made except to a loopback host; a --base-url pointing elsewhere is refused.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import re
import sys
import urllib.parse
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import publish_hedgedoc as ph      # noqa: E402  loopback guard + the HTTP layer

REPO = ph.REPO
SCRIPT_VERSION = "1.0"

# A markdown link, and the section of a note a student edits. The hub's "## Links" section and a
# session's "## Cohort notes" section are where a cohort adds its own links.
MD_LINK = re.compile(r"\[[^\]]*\]\(\s*([^)\s]+)")
COHORT_NOTES = re.compile(r"^##[ \t]+Cohort notes[ \t]*$", re.M)
HUB_LINKS = re.compile(r"^##[ \t]+Links[ \t]*$", re.M)


class ArchiveError(Exception):
    pass


# ----------------------------------------------------------------------------- which notes


def core_aliases(cohort: str) -> list[str]:
    """The cohort's own notes, seeded (not discovered): the hub, s1-s4, and the slide decks."""
    aliases = [f"vr-{cohort}-hub"]
    for i in range(1, 5):
        aliases.append(f"vr-{cohort}-s{i}")
        aliases.append(f"vr-{cohort}-s{i}-slides")
    return aliases


def section_after(text: str, heading: re.Pattern) -> str:
    """The text from a '## ' heading to the next '## ' heading (or end of note)."""
    m = heading.search(text)
    if not m:
        return ""
    rest = text[m.end():]
    nxt = re.search(r"^##[ \t]", rest, re.M)
    return rest[:nxt.start()] if nxt else rest


def note_links(text: str, base_host: str) -> list[str]:
    """HedgeDoc aliases (same host, a single path segment) that this note links to."""
    out: list[str] = []
    for raw in MD_LINK.findall(text):
        parsed = urllib.parse.urlparse(raw.strip("<>"))
        host = parsed.hostname
        # a relative or protocol-relative link inherits the base host; an absolute one must match
        if host and host != base_host:
            continue
        parts = parsed.path.strip("/").split("/")
        if len(parts) != 1 or not parts[0] or "." in parts[0]:
            continue        # not a note alias: a static file, or a multi-segment path
        out.append(parts[0])
    return out


def discover(cohort: str, base_url: str, fetch) -> dict[str, str]:
    """Breadth-first: the core aliases, plus any note linked from the hub's Links section or a
    session's Cohort notes section. `fetch(alias)` returns the note's text, or None if it is gone."""
    base_host = urllib.parse.urlparse(base_url).hostname or "localhost"
    by_alias: dict[str, str] = {}        # alias -> its text, as downloaded
    queue = core_aliases(cohort)
    seen: set[str] = set()
    while queue:
        alias = queue.pop(0)
        if alias in seen:
            continue
        seen.add(alias)
        text = fetch(alias)
        if text is None:
            continue
        by_alias[alias] = text
        if alias.endswith("-hub"):
            linked = note_links(section_after(text, HUB_LINKS), base_host)
        elif "-slides" in alias:
            linked = []                  # a deck is the lesson as slides; it carries no links
        else:
            linked = note_links(section_after(text, COHORT_NOTES), base_host)
        for nxt in linked:
            if nxt not in seen:
                queue.append(nxt)
    return by_alias


# ----------------------------------------------------------------------------- fetch + store


def info_of(base_url: str, alias: str) -> dict:
    """GET /{alias}/info: the title and last-change time. Missing fields degrade to null."""
    code, data = ph.http_get(base_url, f"{alias}/info")
    if code != 200:
        return {}
    try:
        return json.loads(data.decode("utf-8-sig"))
    except (ValueError, UnicodeDecodeError):
        return {}


def download(base_url: str, alias: str) -> bytes | None:
    code, data = ph.http_get(base_url, f"{alias}/download")
    return data if code == 200 else None


def snapshot_dir(out: Path, cohort: str) -> Path:
    """<out>/<cohort>/<UTC timestamp>, bumped with a -N suffix if that name exists, so a later
    snapshot is always a new folder and an earlier one is never touched."""
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    folder = out / cohort / stamp
    n = 2
    while folder.exists():
        folder = out / cohort / f"{stamp}-{n}"
        n += 1
    return folder


# ---------------------------------------------------------------------- vr-past-cohorts


def hub_line(cohort: str, base_url: str) -> str:
    return f"- [cohort {cohort}]({base_url.rstrip('/')}/vr-{cohort}-hub)"


def lists_cohort(text: str, cohort: str) -> bool:
    """Whether a note already links this cohort's hub (robust to the link's label wording)."""
    alias = f"vr-{cohort}-hub"
    return any(urllib.parse.urlparse(raw).path.rstrip("/").split("/")[-1] == alias
               for raw in MD_LINK.findall(text))


def update_past_cohorts(cohort: str, base_url: str, existing: bytes | None) -> tuple[str, int]:
    """Return ('created'|'present', status). Create the index if it is missing, with this cohort's
    hub link; if it is present and already lists the cohort, leave it (create-only: the line stays,
    so the cohort is listed exactly once). Never removes a line."""
    line = hub_line(cohort, base_url)
    if existing is None:                    # the index does not exist yet: create it
        body = "# Past cohorts\n\n" + line + "\n"
        status = ph.http_create(base_url, ph.PAST_COHORTS, body.encode("utf-8"))
        if status == 409:                   # created by a concurrent run just now
            return "present", status
        if status not in (302, 200, 201):
            raise ArchiveError(f"creating {ph.PAST_COHORTS} returned HTTP {status}")
        return "created", status
    if lists_cohort(existing.decode("utf-8-sig", errors="replace"), cohort):
        return "present", 200               # already listed: leave it, do not overwrite
    raise ArchiveError(
        f"{ph.PAST_COHORTS} exists but does not list cohort {cohort}, and this HedgeDoc has no "
        "update route, so the link cannot be appended without overwriting the other cohorts' "
        "lines. Re-create the index from a clean instance.")


# ------------------------------------------------------------------------------ main / CLI


def run(cohort: str, base_url: str, out: Path) -> int:
    ph.assert_loopback(base_url)
    out = out.resolve()
    if REPO.resolve() in out.parents or out == REPO.resolve():
        raise ArchiveError(
            f"refusing to write the archive inside the repo's working tree ({out}); point --out "
            "outside the repo (default ../course-cohort-archives/)")

    def fetch(alias: str) -> str | None:
        data = download(base_url, alias)
        return data.decode("utf-8-sig", errors="replace") if data is not None else None

    print(f"archive_hedgedoc.py: cohort {cohort} <- {base_url} -> {out}")
    by_alias = discover(cohort, base_url, fetch)
    core = core_aliases(cohort)
    missing = [a for a in core if a not in by_alias]
    if missing:
        print(f"   NOTE: these core notes are not on the instance and are not archived: "
              f"{', '.join(missing)}")

    folder = snapshot_dir(out, cohort)
    folder.mkdir(parents=True, exist_ok=True)

    notes = []
    extra = [a for a in by_alias if a not in core]
    for alias in core + extra:
        data = download(base_url, alias)
        if data is None:
            continue
        info = info_of(base_url, alias)
        (folder / f"{alias}.md").write_bytes(data)
        notes.append({
            "alias": alias,
            "title": info.get("title", alias),
            "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
            "last_change": info.get("updatetime") or info.get("createtime"),
            "core": alias in core,
        })
        print(f"    {alias:<28} {'archived':<12} "
              f"{str(info.get('title', ''))[:40]:<40} {len(data)} bytes")

    action, status = update_past_cohorts(cohort, base_url, download(base_url, ph.PAST_COHORTS))
    print(f"    {ph.PAST_COHORTS:<28} {action:<12} "
          f"(cohort's hub link {action})  HTTP {status}")

    manifest = {
        "cohort": cohort,
        "archived_at": folder.name,
        "base_url": base_url,
        "script": f"tools/archive_hedgedoc.py {SCRIPT_VERSION}",
        "notes": notes,
        "missing": missing,
    }
    (folder / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"   snapshot: {folder} ({len(notes)} notes, manifest.json written)")
    return 0


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):      # a cp1252 console must not crash on a quote
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="backslashreplace")
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--cohort", required=True, help="cohort id, e.g. 2026-10a")
    parser.add_argument("--base-url", default=ph.DEFAULT_BASE_URL,
                       help=f"HedgeDoc base URL (default: {ph.DEFAULT_BASE_URL})")
    parser.add_argument("--out", default="../course-cohort-archives/",
                       help="snapshot root, OUTSIDE the repo (default: ../course-cohort-archives/)")
    args = parser.parse_args(argv)
    try:
        return run(args.cohort, args.base_url, Path(args.out))
    except ArchiveError as err:
        print(f"archive_hedgedoc.py: ERROR: {err}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
