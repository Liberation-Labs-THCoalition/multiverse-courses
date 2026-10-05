#!/usr/bin/env python3
"""Tests for the HedgeDoc publisher and archiver (docs/run-card-hedgedoc-v1.md, "Checks").

    .venv-site/bin/python tools/test_publish_hedgedoc.py            # offline + build checks
    .venv-site/bin/python tools/test_publish_hedgedoc.py --live     # also checks 4-6, if an
                                                                     # instance is up at the base URL

Checks 4-6 publish to and archive from a running HedgeDoc. With no instance they are skipped, not
failed -- the rest of the suite, which is what a publisher's correctness actually rests on, runs
with no server: the positive control (a planted key refuses the publish), the loopback guard, the
byte-for-byte verify, the slide "no words changed" property, the archiver's link-walking and its
inside-repo refusal, and the git fence that keeps build and archive output out of the tree.

No check makes a network call except to a loopback host.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
REPO = TOOLS.parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import build_site as bs                # noqa: E402
import check_public_build as cpb       # noqa: E402
import publish_hedgedoc as ph          # noqa: E402
import archive_hedgedoc as ar          # noqa: E402

BASE_URL = "http://127.0.0.1:3000"
COHORT = "test-001"

# The files this run is allowed to change or add (run card, "Files you create or change").
ALLOWED = {
     ".gitignore",
     "hedgedoc/docker-compose.yml",
     "hedgedoc/README.md",
     "tools/build_site.py",
     "tools/publish_hedgedoc.py",
     "tools/test_publish_hedgedoc.py",
     "tools/archive_hedgedoc.py",
     "docs/cohort-links.md",
     "docs/hedgedoc-v1-report.md",
}


class Skip(Exception):
    pass


# --------------------------------------------------------------------------- shared helpers


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, *cmd], cwd=REPO, capture_output=True, text=True)


def ensure_staging() -> None:
    if not bs.STAGING.is_dir():
        r = run(["tools/build_site.py"])
        if r.returncode != 0:
            raise AssertionError(f"build_site.py failed:\n{r.stderr}")


def server_up() -> bool:
    try:
        with urllib.request.urlopen(BASE_URL, timeout=4) as resp:
            return resp.getcode() == 200
    except Exception:
        return False


# ------------------------------------------------------------------------------- check 1


def test_check1_build_and_strict() -> None:
    """build_site.py and `mkdocs build --strict` both exit 0."""
    r = run(["tools/build_site.py"])
    assert r.returncode == 0, f"build_site.py failed:\n{r.stderr}"
    try:
        import mkdocs             # in the .venv-site venv
    except ImportError:
        raise Skip("mkdocs is not importable here; run with .venv-site/bin/python")
    r = run(["-m", "mkdocs", "build", "--strict"])
    assert r.returncode == 0, f"mkdocs build --strict failed:\n{r.stderr[-2000:]}"
    assert (REPO / "site").is_dir(), "mkdocs did not write site/"


# ------------------------------------------------------------------------------- check 2


def test_check2_public_build_passes() -> None:
    """`python tools/check_public_build.py site` passes."""
    if not (REPO / "site").is_dir():
        raise Skip("site/ not built; run check 1 first (or the suite in order)")
    r = run(["tools/check_public_build.py", "site"])
    assert r.returncode == 0, f"check_public_build failed:\n{r.stderr[-2000:]}\n{r.stdout[-1000:]}"


# ------------------------------------------------------------- check 3: positive control


def test_check3_positive_control() -> None:
    """A key planted anywhere in _staging refuses the publish; removing it, it passes.

    This is the run card's check 3, run exactly: plant _staging/zz_control/FACILITATOR.md with
    CONTROL-KEY-12345, a dry-run must REFUSE, delete the file, the dry-run passes."""
    ensure_staging()
    planted = bs.STAGING / "zz_control" / "FACILITATOR.md"
    planted.parent.mkdir(parents=True, exist_ok=True)
    try:
        planted.write_text("CONTROL-KEY-12345\n", encoding="utf-8")
        with tempfile.TemporaryDirectory() as dry:
            r = run(["tools/publish_hedgedoc.py", "--cohort", COHORT, "--dry-run", dry])
        assert r.returncode != 0, "a planted key did NOT refuse the publish (exit 0)"
        assert "REFUSING" in r.stdout, f"no REFUSING message:\n{r.stdout}"
    finally:
        if planted.exists():
            planted.unlink()
    stray = bs.STAGING / "zz_control"
    if stray.is_dir():
        shutil.rmtree(stray)                 # a leftover plant would break the "passes" half
    with tempfile.TemporaryDirectory() as dry:
        r = run(["tools/publish_hedgedoc.py", "--cohort", COHORT, "--dry-run", dry])
    assert r.returncode == 0, f"publish refused after the key was removed:\n{r.stderr}\n{r.stdout}"
    assert not list(bs.STAGING.rglob("zz_control")), "a plant is still in _staging"


# ------------------------------------------------------ the payload logic (offline, always)


def test_frontmatter_control() -> None:
    """Lyra's review control (2026-10-05): a key by FRONT MATTER, not by file name, must refuse too.

    Check 3 plants a file NAMED like a key. This plants an ordinary-looking notes.md whose front
    matter says `audience: facilitator`, which check_public_build's own definition counts as a key."""
    ensure_staging()
    planted = bs.STAGING / "zz_fm_control" / "notes.md"
    planted.parent.mkdir(parents=True, exist_ok=True)
    try:
        planted.write_text("---\naudience: facilitator\n---\n# notes\nLYRA-CONTROL-777\n", encoding="utf-8")
        with tempfile.TemporaryDirectory() as dry:
            r = run(["tools/publish_hedgedoc.py", "--cohort", COHORT, "--dry-run", dry])
        assert r.returncode != 0, "a front-matter facilitator file did NOT refuse the publish (exit 0)"
        assert "REFUSING" in r.stdout, f"no REFUSING message:\n{r.stdout}"
    finally:
        shutil.rmtree(planted.parent, ignore_errors=True)


def test_loopback_guard() -> None:
    """A --base-url off the loopback is refused; the loopback is allowed."""
    for bad in ("http://example.com:3000", "https://hedgedoc.example.org", "http://10.0.0.1:3000"):
        try:
            ph.assert_loopback(bad)
            raise AssertionError(f"loopback guard accepted {bad}")
        except ph.PublishError:
            pass
    for good in (ph.DEFAULT_BASE_URL, "http://127.0.0.1:3000", "http://localhost:3000"):
        ph.assert_loopback(good)             # must not raise


def test_notes_match() -> None:
    """The verify is byte-for-byte, allowing a single trailing newline."""
    assert ph.notes_match(b"abc\n", b"abc\n")
    assert ph.notes_match(b"abc", b"abc\n\n")       # HedgeDoc may add trailing newlines on storage
    assert not ph.notes_match(b"abc\n", b"abcd\n")
    assert not ph.notes_match(b"abc", b"ac\n")


def test_payloads_structure() -> None:
    """build_payloads yields the hub, s1-s4, and the four slide decks, with the right aliases."""
    ensure_staging()
    payloads = ph.build_payloads(COHORT, ph.DEFAULT_BASE_URL, bs.STAGING)
    aliases = [a for a, _, _ in payloads]
    expected = (["vr-test-001-hub"]
                + [f"vr-test-001-s{i}" for i in range(1, 5)]
                + [f"vr-test-001-s{i}-slides" for i in range(1, 5)])
    assert aliases == expected, f"unexpected alias set: {aliases}"
    # the hub links to each session and to the past-cohorts index, and carries a Links section
    hub_content = next(c for a, _, c in payloads if a.endswith("-hub"))
    for i in range(1, 5):
        assert f"/vr-test-001-s{i}" in hub_content, f"hub missing link to s{i}"
    assert f"/{ph.PAST_COHORTS}" in hub_content, "hub missing the past-cohorts link"
    assert "## Links" in hub_content, "hub missing the Links section"
    # each session note ends with the empty live-edit section
    for i in range(1, 5):
        sess = next(c for a, _, c in payloads if a == f"vr-test-001-s{i}")
        assert sess.rstrip().endswith(ph.COHORT_NOTES_HEADING), f"s{i} missing {ph.COHORT_NOTES_HEADING}"


def test_slides_no_words_changed() -> None:
    """The deck is the session note with separators and front matter only: the words are unchanged."""
    ensure_staging()
    for i, page in enumerate(bs.SESSIONS, 1):
        staged = bs.STAGING / page.dest
        sess = ph.session_payload(staged, i)
        slide = ph.slide_payload(staged, i)
        assert slide.startswith("---\ntype: slide\nslideOptions: {transition: slide}\n---"), "front matter"
        body = "\n".join(slide.split("\n", 3)[3:])           # after the front-matter block
        # every non-blank session line appears in the deck, in order; the deck may add only blanks
        it = iter(body.split("\n"))
        for want in sess.split("\n"):
            if want.strip() == "":
                continue
            got = next((x for x in it if x == want), None)
            assert got is not None, f"s{i}: line not found in deck: {want!r}"
        # a break is inserted before each heading the session has (a session may have neither)
        if re.search(r"^##\s+Hour", sess, re.M):
            assert re.search(r"^---$\n##.*Hour", body, re.M), "no slide break before a ## Hour heading"
        if re.search(r"^###\s", sess, re.M):
            assert re.search(r"^----$\n###", body, re.M), "no sub-slide break before a ### heading"


def test_archiver_link_walking() -> None:
    """The archiver walks student notes off the hub's Links and a session's Cohort notes, but not
    the public site, the repo, static files, or the vr-past-cohorts index."""
    core = ar.core_aliases("2026-10a")
    assert len(core) == 9, f"expected 9 core aliases, got {core}"
    hub = ("# hub\n\n## Sessions\n\n- [s1](http://localhost:3000/vr-2026-10a-s1)\n\n## Elsewhere\n\n"
             "- [Public site](https://liberation-labs-thcoalition.github.io/x)\n"
             "- [Repository](https://github.com/Liberation-Labs-THCoalition/multiverse-courses)\n"
             "- [Back](http://localhost:3000/vr-past-cohorts)\n\n## Links\n\n"
             "- [Glossary](http://localhost:3000/vr-2026-10a-glossary)\n")
    assert ar.note_links(ar.section_after(hub, ar.HUB_LINKS), "localhost") == ["vr-2026-10a-glossary"]
    # a session note links an alias, a static file, and an external URL; only the alias survives
    sess = ("# s1\n\ntext\n\n## Cohort notes\n\n"
              "- [glossary](http://localhost:3000/vr-2026-10a-glossary)\n"
              "- [data](http://localhost:3000/report.md)\n"
              "- [blog](https://example.com/post)\n")
    assert ar.note_links(ar.section_after(sess, ar.COHORT_NOTES), "localhost") == ["vr-2026-10a-glossary"]


def test_archiver_refuses_inside_repo() -> None:
    """Writing the archive inside the repo's working tree is refused."""
    for bad in (REPO / "cohort-archives", REPO, REPO / "site" / "archives"):
        out = bad.resolve()
        assert ar.REPO.resolve() in out.parents or out == ar.REPO.resolve()
    default = (REPO.parent / "course-cohort-archives").resolve()
    assert ar.REPO.resolve() not in default.parents and default != ar.REPO.resolve()


# ------------------------------------------------------------- live checks 4, 5, 6


def test_check4_publish_byte_equal() -> None:
    """publish test-001: every alias published (or already there) and byte-equal."""
    if not server_up():
        raise Skip("no HedgeDoc instance at " + BASE_URL)
    r = run(["tools/publish_hedgedoc.py", "--cohort", COHORT, "--base-url", BASE_URL])
    assert r.returncode == 0, f"publish failed:\n{r.stdout}\n{r.stderr}"
    assert "VERIFY FAILED" not in r.stdout, "a note was not byte-equal"
    assert "published (verified)" in r.stdout or "skipped" in r.stdout, r.stdout


def test_check5_rerun_skips() -> None:
    """Re-running the same cohort skips every alias and overwrites nothing."""
    if not server_up():
        raise Skip("no HedgeDoc instance at " + BASE_URL)
    r = run(["tools/publish_hedgedoc.py", "--cohort", COHORT, "--base-url", BASE_URL])
    assert r.returncode == 0, f"re-publish failed:\n{r.stdout}\n{r.stderr}"
    assert "skipped (already exists)" in r.stdout, "a re-run did not skip existing notes"
    assert "published (verified)" not in r.stdout, "a re-run published something it should skip"


def test_check6_archive_snapshot() -> None:
    """Archive test-001 twice: each file's sha256 matches a fresh download, a second folder appears,
    the first is untouched, --out inside the repo is refused, and the past-cohorts index lists
    test-001 exactly once."""
    if not server_up():
        raise Skip("no HedgeDoc instance at " + BASE_URL)
    out_root = REPO.parent / "course-cohort-archives"
    cohort_dir = out_root / COHORT

    # 0. an in-repo --out is refused
    r = run(["tools/archive_hedgedoc.py", "--cohort", COHORT, "--base-url", BASE_URL, "--out",
              "cohort-archives"])
    assert r.returncode == 2, "an in-repo --out was not refused"
    assert "inside the repo" in r.stderr.lower(), r.stderr

    def snapshot_folders() -> list[Path]:
        return sorted(p for p in cohort_dir.iterdir() if p.is_dir()) if cohort_dir.is_dir() else []

    def manifest_of(folder: Path) -> dict:
        return json.loads((folder / "manifest.json").read_text(encoding="utf-8"))

    # first snapshot
    r = run(["tools/archive_hedgedoc.py", "--cohort", COHORT, "--base-url", BASE_URL, "--out",
              str(out_root)])
    assert r.returncode == 0, f"first archive failed:\n{r.stdout}\n{r.stderr}"
    folders = snapshot_folders()
    assert folders, "no snapshot folder created"
    first = folders[0]
    m1 = manifest_of(first)
    aliased = [n["alias"] for n in m1["notes"]]
    assert "vr-test-001-hub" in aliased and all(f"vr-test-001-s{i}" in aliased for i in range(1, 5)), aliased
    for note in m1["notes"]:
        with urllib.request.urlopen(f"{BASE_URL}/{note['alias']}/download", timeout=15) as resp:
            fresh = resp.read()
        on_disk = (first / f"{note['alias']}.md").read_bytes()
        assert hashlib.sha256(fresh).hexdigest() == note["sha256"], note["alias"]
        assert on_disk.rstrip(b"\n") == fresh.rstrip(b"\n"), f"archive != download for {note['alias']}"

    # second snapshot: a new folder, the first untouched
    def digest_all(folder: Path) -> dict:
        return {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(folder.iterdir())}
    first_before = digest_all(first)
    r = run(["tools/archive_hedgedoc.py", "--cohort", COHORT, "--base-url", BASE_URL, "--out",
              str(out_root)])
    assert r.returncode == 0, f"second archive failed:\n{r.stdout}\n{r.stderr}"
    folders2 = snapshot_folders()
    assert len(folders2) >= len(folders) + 1, "no second snapshot folder appeared"
    assert digest_all(folders2[0]) == first_before, "the first snapshot was changed"
    # the past-cohorts index lists test-001 exactly once
    with urllib.request.urlopen(f"{BASE_URL}/{ph.PAST_COHORTS}/download", timeout=15) as resp:
        idx = resp.read().decode("utf-8-sig", errors="replace")
    assert ar.lists_cohort(idx, COHORT), "vr-past-cohorts does not list " + COHORT
    assert idx.count(f"/vr-{COHORT}-hub") == 1, f"vr-past-cohorts lists {COHORT} more than once"


# ----------------------------------------------------------------- check 7: the git fence


def test_check7_git_fence() -> None:
    """Only the run's own files changed, and no build or archive artifact is in the tree."""
    r = subprocess.run(["git", "status", "--porcelain", "-uall"], cwd=REPO,
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    paths = []
    for line in r.stdout.splitlines():
        if not line.strip():
            continue
        paths.append(line[3:].split(" -> ", 1)[-1].strip().strip('"'))
    unexpected = [p for p in paths if p not in ALLOWED]
    assert not unexpected, f"git shows changes outside the run's file list: {unexpected}"
    artifacts = [p for p in paths
                 if any(t in p for t in ("course-cohort-archives", "cohort-archives",
                                          "_staging", "/site/", "mkdocs.yml", "zz_control"))]
    assert not artifacts, f"a build/archive artifact is in the git tree: {artifacts}"


# ------------------------------------------------------------------------------- the runner


LIVE = ("check 4", "check 5", "check 6")

CHECKS = [
     ("check 1: build_site + mkdocs build --strict", test_check1_build_and_strict),
     ("check 2: check_public_build passes", test_check2_public_build_passes),
     ("check 3: positive control (planted key refuses)", test_check3_positive_control),
     ("front-matter control (audience: facilitator refuses)", test_frontmatter_control),
     ("loopback guard", test_loopback_guard),
     ("notes_match (byte-for-byte, trailing newline ok)", test_notes_match),
     ("payload structure (hub + s1-s4 + 4 decks)", test_payloads_structure),
     ("slides change no words (separators + front matter only)", test_slides_no_words_changed),
     ("archiver walks student notes, filters the rest", test_archiver_link_walking),
     ("archiver refuses to write inside the repo", test_archiver_refuses_inside_repo),
     ("check 4: publish test-001, byte-equal", test_check4_publish_byte_equal),
     ("check 5: re-run skips everything", test_check5_rerun_skips),
     ("check 6: archive twice, sha256 matches, second folder, fence", test_check6_archive_snapshot),
     ("check 7: only the run's files changed, no artifacts", test_check7_git_fence),
]


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    selected = CHECKS
    if "--live" not in argv:
        selected = [c for c in CHECKS if c[0].split(":")[0] not in LIVE]
    failed = skipped = 0
    for name, fn in selected:
        try:
            fn()
            print(f"ok    {name}")
        except Skip as s:
            skipped += 1
            print(f"skip  {name}   ({s})")
        except AssertionError as a:
            failed += 1
            print(f"FAIL  {name}\n      {a}")
        except Exception as exc:        # a test bug must not read as a pass
            failed += 1
            print(f"FAIL  {name}\n      {type(exc).__name__}: {exc}")
    print(f"\n{len(selected) - failed - skipped}/{len(selected)} passed, "
          f"{skipped} skipped, {failed} failed"
          + ("  (skips are not failures)" if skipped else ""))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
