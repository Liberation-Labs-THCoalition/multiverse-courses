#!/usr/bin/env python3
"""Fail if an answer key, or text found only in one, is in the built site.

    python tools/check_public_build.py [SITE_DIR]               (default SITE_DIR: _site)
    python tools/check_public_build.py --self-test [SITE_DIR]   positive control

Spec: docs/site-spec.md, "Answer keys". Keys are found by walking the repo, not from a list
of paths: every FACILITATOR.md, verify_floor.py and AGENT_REVIEW_RESULTS.md; grim_reference.py
(build-grim's working solution, marked "FACILITATOR REFERENCE ONLY"); and any markdown file
whose front matter says `audience: facilitator`.

The check fails if any file in the site
  1. is named like a key (FACILITATOR.md, FACILITATOR/index.html, verify_floor.py, ...);
  2. is a byte-for-byte copy of a key, under any name;
  3. links to a key (an href or src whose last path segment is a key's name); or
  4. contains a distinctive string of a key.

A distinctive string is a line of a key that is at least MIN_CHARS letters and digits long
once markup, spacing and punctuation are dropped, and that occurs in no other file tracked in
the repo: the spec's "any string unique to it". Every text file in the site is compared in
the same normalised form (HTML with its tags stripped and entities decoded, the strings in the
search index, JS, CSS, sitemaps), so rendering cannot hide a match.

A key line that also occurs in another repo file is not distinctive. It is reported as a NOTE
instead: a key line repeated in a student-facing page is a spoiler there, although it is not
a leak of the key file.

--self-test copies the site to a temporary folder and never touches SITE_DIR. It checks that
the copy passes, then plants a key four ways, one at a time: a verbatim copy under the key's
own name; the key rendered to HTML under a neutral name; one short line of it inside an
existing page; and a dummy key recognised only by its front matter. Each plant must fail the
check, and the copy must pass again once the plant is removed.

This script deliberately does not import tools/build_site.py: a check that shared the
builder's idea of what is public would share its blind spots.

FINGERPRINT MODE (2026-10-08). The keys live in a private repo, so they cannot be in this one. When the repo holds
no keys, the check reads tools/key_fingerprints.json instead. For every distinctive line it stores an 8-byte hash of
the first ANCHOR_CHARS normalised characters and a 16-byte hash of the whole normalised line, plus the sha256 of each
key file.

The rule is the same: a site file fails when a distinctive line is a substring of its normalised text. Every
ANCHOR_CHARS window of the page is hashed once and looked up, and a hit is confirmed on the full-length hash, so no
key text is ever needed. Names, copies and links are checked as before.

In this mode, a key line that has since been repeated in a public page FAILS. With no plaintext there is no way to
tell "shared" from "leaked"; that is stricter, and correct for a spoiler.

The self-test plants a synthetic key, fingerprinted the same way, so the positive control still exercises the real
matcher.

To rebuild the file:
  python tools/check_public_build.py --write-fingerprints [--keys-dir PRIVATE_CHECKOUT]
This reads the keys in this repo. With --keys-dir, it lays the private checkout's keys over a temporary copy of this
repo's tracked files, so "distinctive" is still judged against this repo's own text.

Exit status: 0 pass; 1 leak found, or self-test failed; 2 cannot check (e.g. no keys found).
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import unquote, urlparse

REPO = Path(__file__).resolve().parent.parent
MIN_CHARS = 24
ANCHOR_CHARS = MIN_CHARS   # every distinctive line is at least this long, so its first ANCHOR_CHARS anchor it
FINGERPRINTS = REPO / "tools" / "key_fingerprints.json"

KEY_NAMES = {"facilitator.md", "verify_floor.py", "agent_review_results.md", "grim_reference.py"}
KEY_STEMS = {name.split(".")[0] for name in KEY_NAMES}
FACILITATOR_AUDIENCE = re.compile(r"^audience:\s*['\"]?facilitator['\"]?\s*$", re.M | re.I)
FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)
# Build output, dependencies and caches: never part of the key search or the corpus.
SKIP_DIRS = {".git", "node_modules", "__pycache__", "_site", "site", "_staging", "dist",
             "dist-artifact"}

MD_LINK = re.compile(r"!?\[((?:\\.|[^\]\\])*)\]\([^)\n]*\)")
HTML_COMMENT = re.compile(r"<!--.*?-->", re.S)
TAG = re.compile(r"<[^>]*>")
URL_ATTR = re.compile(r"""(?:href|src)\s*=\s*["']([^"']+)["']""", re.I)
JS_ESCAPE = re.compile(r"\\u([0-9a-fA-F]{4})")
MARKUP_EXT = {".html", ".htm", ".xml", ".svg"}
JSON_EXT = {".json", ".map", ".webmanifest"}


def norm(text: str) -> str:
    """Letters and digits only, lowercased."""
    return re.sub(r"[\W_]+", "", text.lower())


def read_text(path: Path) -> str | None:
    try:
        return path.read_bytes().decode("utf-8-sig").replace("\r\n", "\n")
    except (UnicodeDecodeError, OSError):
        return None


def md_visible(text: str) -> str:
    """What a reader sees of markdown: link text without its target, and no comments."""
    return MD_LINK.sub(r"\1", HTML_COMMENT.sub("", text))


def digests(data: bytes) -> set[str]:
    return {hashlib.sha256(d).hexdigest() for d in (data, data.replace(b"\r\n", b"\n"))}


def named_like_key(name: str) -> bool:
    low = name.lower()
    return bool(low) and (low in KEY_NAMES or low.split(".")[0] in KEY_STEMS)


# ----------------------------------------------------------------------------------- keys


@dataclass
class Key:
    path: Path
    rel: str
    why: str
    hashes: set[str]
    distinctive: list[tuple[str, str]] = field(default_factory=list)   # (normalised, line)
    shared: list[tuple[str, list[str]]] = field(default_factory=list)  # (line, other files)
    # fingerprint mode: anchor hash -> [(line length, full hash)]; no plaintext anywhere
    fingerprints: dict[str, list[tuple[int, str]]] = field(default_factory=dict)

    def n_lines(self) -> int:
        return len(self.distinctive) if self.distinctive else sum(len(v) for v in self.fingerprints.values())


def walk(root: Path, skip: set[Path]) -> list[Path]:
    found = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames
                       if d not in SKIP_DIRS and not d.startswith(".venv")
                       and (Path(dirpath) / d).resolve() not in skip]
        found.extend(Path(dirpath) / name for name in filenames)
    return found


def tracked(root: Path) -> list[Path] | None:
    try:
        out = subprocess.run(["git", "-C", str(root), "ls-files", "-z"],
                             capture_output=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return None
    return [root / p for p in out.decode("utf-8").split("\0") if p and (root / p).is_file()]


def key_reason(path: Path) -> str | None:
    if path.name.lower() in KEY_NAMES:
        return "file name"
    if path.suffix.lower() == ".md":
        m = FRONT_MATTER.match(read_text(path) or "")
        if m and FACILITATOR_AUDIENCE.search(m.group(1)):
            return "front matter"
    return None


def discover(repo: Path, site: Path | None = None, use_git: bool = True) -> list[Key]:
    """Find the keys, and split each key's lines into distinctive and shared."""
    skip = {site.resolve()} if site else set()
    walked = walk(repo, skip)
    listed = tracked(repo) if use_git else None
    keys, seen = [], set()
    for path in sorted({p.resolve(): p for p in walked + (listed or [])}.values()):
        why = key_reason(path)
        if why and path.resolve() not in seen:
            seen.add(path.resolve())
            keys.append(Key(path, path.relative_to(repo).as_posix(), why, digests(path.read_bytes())))
    key_paths = {k.path.resolve() for k in keys}
    key_hashes = {h for k in keys for h in k.hashes}
    corpus = {}
    for path in (listed if listed is not None else walked):
        resolved = path.resolve()
        if resolved in key_paths or any(s in resolved.parents for s in skip):
            continue
        data = path.read_bytes()
        if len(data) > 5_000_000 or digests(data) & key_hashes:   # a copy of a key is a key
            continue
        text = read_text(path)
        if text is not None:
            corpus[path.relative_to(repo).as_posix()] = norm(md_visible(text))
    for key in keys:
        text = read_text(key.path) or ""
        visible = md_visible(text) if key.path.suffix.lower() == ".md" else text
        done = set()
        for line in visible.split("\n"):
            n = norm(line)
            if len(n) < MIN_CHARS or n in done:
                continue
            done.add(n)
            others = [rel for rel, body in corpus.items() if n in body]
            if others:
                key.shared.append((line.strip(), others))
            else:
                key.distinctive.append((n, line.strip()))
    return keys


def _h(s: str, size: int) -> str:
    return hashlib.blake2b(s.encode("utf-8"), digest_size=size).hexdigest()


def fingerprint_key(key: Key) -> Key:
    """The same key with its distinctive lines replaced by hashes: what may live in a public repo."""
    fps: dict[str, list[tuple[int, str]]] = {}
    for n, _line in key.distinctive:
        fps.setdefault(_h(n[:ANCHOR_CHARS], 8), []).append((len(n), _h(n, 16)))
    return Key(key.path, key.rel, key.why, set(key.hashes), [], [], fps)


def load_fingerprints(path: Path = FINGERPRINTS) -> list[Key]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("anchor_chars") != ANCHOR_CHARS or data.get("min_chars") != MIN_CHARS:
        raise ValueError(f"{path}: made with different MIN_CHARS/ANCHOR_CHARS; regenerate it")
    keys = []
    for k in data["keys"]:
        fps: dict[str, list[tuple[int, str]]] = {}
        for length, anchor, full in k["lines"]:
            fps.setdefault(anchor, []).append((int(length), full))
        keys.append(Key(path, k["rel"], k["why"], set(k["file_sha256"]), [], [], fps))
    return keys


def write_fingerprints(keys: list[Key], path: Path = FINGERPRINTS) -> None:
    out = {"version": 1, "hash": "blake2b", "min_chars": MIN_CHARS, "anchor_chars": ANCHOR_CHARS,
           "note": "Hashes of the answer keys' distinctive lines; the keys themselves are in the private repo.",
           "keys": []}
    for key in keys:
        fk = fingerprint_key(key) if key.distinctive else key
        lines = sorted([length, anchor, full] for anchor, v in fk.fingerprints.items() for length, full in v)
        out["keys"].append({"rel": key.rel, "why": key.why, "file_sha256": sorted(key.hashes), "lines": lines})
    path.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")


def text_index(keys: list[Key]) -> dict[str, list[tuple[Key, int, str]]]:
    """anchor hash -> [(key, line length, full hash)] for every fingerprinted key."""
    index: dict[str, list[tuple[Key, int, str]]] = {}
    for key in keys:
        for anchor, v in key.fingerprints.items():
            for length, full in v:
                index.setdefault(anchor, []).append((key, length, full))
    return index


def fingerprint_hits(blob: str, index) -> dict[str, int]:
    """rel -> how many distinctive lines are a substring of blob (by fingerprint)."""
    found: dict[str, set[str]] = {}
    for i in range(len(blob) - ANCHOR_CHARS + 1):
        cands = index.get(_h(blob[i:i + ANCHOR_CHARS], 8))
        if cands:
            for key, length, full in cands:
                if _h(blob[i:i + length], 16) == full:
                    found.setdefault(key.rel, set()).add(full)
    return {rel: len(v) for rel, v in found.items()}


# ----------------------------------------------------------------------------------- site


@dataclass
class Finding:
    file: str
    kind: str      # name | copy | link | text
    detail: str


def site_forms(path: Path, data: bytes) -> tuple[str | None, str]:
    """The file as text, and every normalised form of it, joined."""
    name = path.name.lower()
    if name.endswith(".gz"):
        try:
            data, name = gzip.decompress(data), name[:-3]
        except (OSError, EOFError):
            return None, ""
    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError:
        return None, ""
    ext = os.path.splitext(name)[1]
    forms = [text]
    if ext in MARKUP_EXT:
        forms.append(html.unescape(TAG.sub(" ", text)))
    elif ext in JSON_EXT:
        strings: list[str] = []

        def collect(value) -> None:
            if isinstance(value, str):
                strings.append(value)
            elif isinstance(value, dict):
                for k, v in value.items():
                    strings.append(k)
                    collect(v)
            elif isinstance(value, list):
                for v in value:
                    collect(v)

        try:
            collect(json.loads(text))
        except ValueError:
            pass
        joined = "\n".join(strings)
        forms += [joined, html.unescape(TAG.sub(" ", joined))]
    elif ext in {".js", ".mjs", ".cjs"}:
        forms.append(JS_ESCAPE.sub(lambda m: chr(int(m.group(1), 16)), text))
    return text, "\x00".join(norm(f) for f in forms)


def check(site: Path, keys: list[Key]) -> tuple[list[Finding], int]:
    findings: list[Finding] = []
    by_hash = {h: k for k in keys for h in k.hashes}
    index = text_index(keys)
    files = sorted(p for p in site.rglob("*") if p.is_file())
    for path in files:
        rel = path.relative_to(site).as_posix()
        part = next((p for p in rel.split("/") if named_like_key(p)), None)
        if part:
            findings.append(Finding(rel, "name", f"{part!r} is named like an answer key"))
        data = path.read_bytes()
        twin = next((by_hash[h] for h in digests(data) if h in by_hash), None)
        if twin:
            findings.append(Finding(rel, "copy", f"identical to {twin.rel}"))
        text, blob = site_forms(path, data)
        if text is None:
            continue
        if os.path.splitext(path.name.lower())[1] in MARKUP_EXT:
            for url in URL_ATTR.findall(text):
                last = unquote(urlparse(html.unescape(url)).path).rstrip("/").split("/")[-1]
                if named_like_key(last):
                    findings.append(Finding(rel, "link", f"links to an answer key: {url}"))
        for key in keys:
            hits = [line for n, line in key.distinctive if n in blob]
            if hits:
                findings.append(Finding(rel, "text", f"{len(hits)} line(s) found only in "
                                                     f"{key.rel}, e.g. {hits[0][:90]!r}"))
        if index:
            for krel, count in fingerprint_hits(blob, index).items():
                findings.append(Finding(rel, "text", f"{count} line(s) found only in {krel} "
                                                     f"(matched by fingerprint)"))
    return findings, len(files)


# ------------------------------------------------------------------------------ self-test


def render_html(text: str, markdown_source: bool) -> str:
    if markdown_source:
        try:
            import markdown   # installed with mkdocs
            body = markdown.markdown(text, extensions=["tables", "fenced_code"])
        except ImportError:
            body = "".join(f"<p>{html.escape(p)}</p>" for p in text.split("\n\n"))
    else:
        body = f"<pre><code>{html.escape(text)}</code></pre>"
    return f"<!doctype html><html><body><article>{body}</article></body></html>"


def self_test(site: Path, keys: list[Key], source: Key | None = None) -> int:
    """`source` is the plaintext key to plant from. In fingerprint mode it is a synthetic key whose fingerprinted
    twin is among `keys`, so the plants exercise the fingerprint matcher."""
    source = source or max(keys, key=lambda k: len(k.distinctive))
    rows: list[tuple[bool, str, str]] = []
    print(f"self-test: on a copy of {site} in a temporary folder ({site} itself is not touched)")
    print(f"  planting from {source.rel} ({len(source.distinctive)} distinctive strings)")
    with tempfile.TemporaryDirectory(prefix="public-build-selftest-") as tmp:
        copy = Path(tmp) / "site"
        shutil.copytree(site, copy)

        baseline, _ = check(copy, keys)
        rows.append((not baseline, "control: the unmodified copy",
                     "clean" if not baseline else f"NOT clean: {len(baseline)} findings; "
                                                  f"the site already leaks"))

        # `want`: detectors that must fire. `forbid`: detectors that must NOT, which proves a
        # plant really is invisible to names and hashes, so the text detector alone caught it.
        def case(label, plant, unplant, want: set[str], forbid: frozenset = frozenset(),
                 keys_=keys):
            plant()
            found, _ = check(copy, keys_)
            unplant()
            after, _ = check(copy, keys_)
            kinds = {f.kind for f in found}
            ok = want <= kinds and not (kinds & forbid) and not after
            n = len(found)
            detail = (f"caught ({', '.join(sorted(kinds)) or 'nothing'}; {n} finding"
                      f"{'' if n == 1 else 's'})"
                      f"{', clean after removal' if not after else ', NOT clean after removal'}")
            rows.append((ok, label, detail))

        blind = frozenset({"name", "copy"})
        planted = copy / "selftest-planted"
        case("A: key copied verbatim, under its own name",
             lambda: (planted.mkdir(), shutil.copy2(source.path, planted / source.path.name)),
             lambda: shutil.rmtree(planted), want={"name", "copy", "text"})

        neutral = copy / "selftest-notes" / "index.html"
        rendered = render_html(read_text(source.path) or "", source.path.suffix.lower() == ".md")
        case("B: key rendered to HTML, under a neutral name",
             lambda: (neutral.parent.mkdir(), neutral.write_text(rendered, encoding="utf-8")),
             lambda: shutil.rmtree(neutral.parent), want={"text"}, forbid=blind)

        pages = sorted(copy.rglob("index.html"), key=lambda p: (len(p.parts), str(p)))
        page = next((p for p in pages if p.parent.name == "course"), pages[0])
        original = page.read_bytes()
        n, line = min(source.distinctive, key=lambda d: len(d[0]))
        snippet = render_html(line, True).split("<article>")[1].split("</article>")[0]
        marker = b"</article>" if b"</article>" in original else b"</body>"
        case(f"C: one {len(n)}-character line inside {page.relative_to(copy).as_posix()}",
             lambda: page.write_bytes(original.replace(marker, snippet.encode() + marker, 1)),
             lambda: page.write_bytes(original), want={"text"}, forbid=blind)

        fake_repo = Path(tmp) / "repo"
        dummy = fake_repo / "notes" / "session-notes.md"
        dummy_body = ("# Dummy facilitator notes (self-test)\n\n"
                      "The planted answer: the patient quokka counted forty-one lanterns.\n"
                      "No page of this course has ever said anything about quokkas or lanterns.\n")
        dummy.parent.mkdir(parents=True)
        dummy.write_text("---\naudience: facilitator\n---\n" + dummy_body, encoding="utf-8")
        fake_keys = discover(fake_repo, use_git=False)
        if any(k.fingerprints for k in keys):   # fingerprint mode: D must be caught by fingerprint too
            fake_keys = [fingerprint_key(k) for k in fake_keys]
        if [(k.rel, k.why, bool(k.distinctive or k.fingerprints)) for k in fake_keys] != \
                [("notes/session-notes.md", "front matter", True)]:
            rows.append((False, "D: dummy key recognised only by its front matter",
                         f"key discovery did not find it by front matter: {fake_keys}"))
        else:
            spot = copy / "selftest-dummy.html"
            case("D: dummy key recognised only by its front matter",
                 lambda: spot.write_text(render_html(dummy_body, True), encoding="utf-8"),
                 lambda: spot.unlink(), want={"text"}, forbid=blind, keys_=fake_keys)

    for ok, label, detail in rows:
        print(f"  {'ok  ' if ok else 'FAIL'}  {label:<58} -> {detail}")
    if all(ok for ok, _, _ in rows):
        print("self-test PASSED: the clean copy passes, and every planted key fails the check.")
        return 0
    print("self-test FAILED: see the FAIL rows above.")
    return 1


def self_test_fingerprints(site: Path, keys: list[Key]) -> int:
    """Fingerprint mode: plant a synthetic key (named like one, with distinctive lines), fingerprinted the same
    way as the real ones, so the self-test exercises the matcher the real check uses."""
    with tempfile.TemporaryDirectory(prefix="public-build-synthkey-") as tmp:
        repo = Path(tmp) / "repo"
        synth = repo / "synthetic-exercise" / "FACILITATOR.md"
        synth.parent.mkdir(parents=True)
        synth.write_text("# Synthetic facilitator notes (self-test only)\n\n"
                         "Ground truth for the self test: seventeen marmots guarded the amber reservoir.\n"
                         "The synthetic floor is exactly nine hundred and four grams of cobalt dust.\n"
                         "No page of this course mentions marmots, cobalt dust or amber reservoirs.\n",
                         encoding="utf-8")
        plain = discover(repo, use_git=False)
        got = [(k.rel, len(k.distinctive)) for k in plain]
        if got != [("synthetic-exercise/FACILITATOR.md", 4)]:
            print(f"self-test FAILED: the synthetic key was not discovered as expected: {got}")
            return 1
        print("self-test (fingerprint mode): planting a synthetic key, fingerprinted like the real ones")
        return self_test(site, keys + [fingerprint_key(plain[0])], source=plain[0])


def write_mode(keys_dir: Path | None) -> int:
    if keys_dir is None:
        keys = discover(REPO)
        write_fingerprints(keys)
    else:
        with tempfile.TemporaryDirectory(prefix="key-overlay-") as tmp:
            overlay = Path(tmp) / "repo"
            for path in tracked(REPO) or []:   # this repo's tracked text, with the private keys laid over it
                dest = overlay / path.relative_to(REPO)
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, dest)
            for path in walk(keys_dir, set()):
                if key_reason(path):
                    dest = overlay / path.relative_to(keys_dir)
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(path, dest)
            keys = discover(overlay, use_git=False)
            write_fingerprints(keys)
    total = sum(k.n_lines() for k in keys)
    print(f"wrote {FINGERPRINTS.relative_to(REPO).as_posix()}: {len(keys)} keys, {total} distinctive lines")
    return 0 if keys and total else 2


# ----------------------------------------------------------------------------------- main


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):   # a cp1252 console must not crash on a quote
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="backslashreplace")
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("site", nargs="?", default="_site", help="built site (default: _site)")
    parser.add_argument("--self-test", action="store_true", help="run the positive control")
    parser.add_argument("--allow-no-keys", action="store_true",
                        help="pass when the repo holds no keys (e.g. once they move to a private repo)")
    parser.add_argument("-v", "--verbose", action="store_true", help="print every NOTE line")
    parser.add_argument("--write-fingerprints", action="store_true",
                        help="write tools/key_fingerprints.json from the keys, and exit")
    parser.add_argument("--keys-dir", help="with --write-fingerprints: a private checkout holding the keys")
    args = parser.parse_args(argv)

    if args.write_fingerprints:
        return write_mode(Path(args.keys_dir) if args.keys_dir else None)
    site = Path(args.site).resolve()
    if not site.is_dir():
        print(f"check_public_build.py: no site at {site}", file=sys.stderr)
        return 2
    keys = discover(REPO, site)
    mode = "repo"
    if not keys and FINGERPRINTS.is_file():
        keys, mode = load_fingerprints(), "fingerprints"
    if not keys:
        print("check_public_build.py: found NO answer keys in the repo and no fingerprint file, so this check "
              "cannot fail." + ("" if args.allow_no_keys else " Pass --allow-no-keys if that is expected."))
        return 0 if args.allow_no_keys else 2
    total = sum(k.n_lines() for k in keys)
    where = "in the repo" if mode == "repo" else f"by fingerprint ({FINGERPRINTS.relative_to(REPO).as_posix()})"
    print(f"check_public_build.py: {len(keys)} answer keys {where}, {total} distinctive strings")
    for k in keys:
        print(f"  {k.rel:<80} by {k.why:<12} {k.n_lines():>3} distinctive, "
              f"{len(k.shared):>2} shared")
    if total == 0:
        print("check_public_build.py: no key has a distinctive string; only names and copies "
              "could be caught.", file=sys.stderr)
        return 2
    if args.self_test:
        return self_test(site, keys) if mode == "repo" else self_test_fingerprints(site, keys)

    findings, scanned = check(site, keys)
    shared = [(k, line, others) for k in keys for line, others in k.shared]
    if shared:
        print(f"NOTES (not failures): {len(shared)} key lines also occur in other repo files, so "
              f"they are not unique to a key. Where that other file is student-facing, the line is "
              f"a spoiler there.")
        for k in keys:
            counts: dict[str, int] = {}
            for _, others in k.shared:
                for other in others:
                    counts[other] = counts.get(other, 0) + 1
            if counts:
                listing = ", ".join(f"{o} ({c})" for o, c in sorted(counts.items()))
                print(f"  {k.rel}: {len(k.shared)} shared with {listing}")
                if args.verbose:
                    for line, _ in k.shared:
                        print(f"      {line[:110]}")
    if findings:
        print(f"FAIL: answer-key material in {site} ({len(findings)} findings, {scanned} files scanned):")
        for f in findings:
            print(f"  [{f.kind}] {f.file}: {f.detail}")
        return 1
    print(f"PASS: no answer key, and no line found only in one, in {scanned} files under {site}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
