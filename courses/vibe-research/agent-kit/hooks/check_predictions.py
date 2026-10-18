#!/usr/bin/env python3
"""Vibe Research agent kit: a git pre-commit check that makes your predictions file append-only.

A prediction is worth something because it was written before you looked. If it can be quietly reworded
afterwards, it stops being a prediction, and nobody reading the file can tell. So before each commit, this
compares the version of PREDICTIONS you're about to commit with the one in your last commit:

- New lines at the bottom: fine.
- An existing line changed, deleted or moved, or a new line slipped in above an existing one: refused,
  unless the same commit adds a new line starting with REVISION: that says what changed and why.
- The whole file deleted or renamed: refused.

What counts as a change:
- Line endings (CRLF or LF), trailing spaces and blank lines are ignored. They're invisible, editors change
  them on their own, and none of them changes a word.
- Everything else counts, including spaces at the start of a line, which can move a point from one list
  item to another.
- A REVISION line licenses one commit's changes. It has to be new in that commit (an old one, or a copy of
  one, doesn't count), and once committed it stays: REVISION lines are the record of what changed, so they
  can't be edited or deleted, even with another REVISION line.

It reads what git is about to commit (the staged version), not the file on your disk. It runs git and
nothing else, and sends nothing anywhere. Exit 0 lets the commit through; exit 1 stops it.
"""
import codecs
import difflib
import os
import subprocess
import sys
from collections import Counter

# The predictions file, relative to the top of your git repository. Keep it the same as in the other hooks.
PREDICTIONS = "research/PREDICTIONS.md"
LABEL = "REVISION:"


def git(*args):
    return subprocess.run(["git", *args], capture_output=True)


def present(*args):
    """Does git list PREDICTIONS here? `ls-tree HEAD` asks the last commit, `ls-files` asks the staged one."""
    result = git(*args, "--", PREDICTIONS)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.decode(errors="replace").strip())
    return bool(result.stdout.strip())


def read_blob(spec):
    result = git("cat-file", "blob", spec)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.decode(errors="replace").strip())
    return result.stdout


def lines_of(data):
    """(line number, text) for each non-blank line, with line endings and trailing whitespace removed."""
    if data.startswith((codecs.BOM_UTF16_LE, codecs.BOM_UTF16_BE)):
        text = data.decode("utf-16")
    else:
        # surrogateescape keeps bytes that aren't valid UTF-8 distinct, so two different ones can't compare equal.
        text = data.decode("utf-8", errors="surrogateescape")
    text = text.lstrip("﻿")  # A byte-order mark is another invisible thing editors add and remove.
    numbered = ((n, line.rstrip()) for n, line in enumerate(text.split("\n"), 1))
    return [(n, line) for n, line in numbered if line]


def is_label(line):
    return line.lstrip().startswith(LABEL)


def describe(old, new):
    """Plain-language list of what changed above the bottom of the file."""
    a, b = [t for _, t in old], [t for _, t in new]
    found = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if op == "equal" or (op == "insert" and i1 == len(a)):
            continue  # Unchanged, or appended at the bottom.
        if op == "insert":
            found.append(f"  new line {new[j1][0]} is above existing line {old[i1][0]}; new lines go at the bottom")
            found += [f"    added: {t}" for t in b[j1:j2]]
            continue
        if op == "delete":
            found.append(f"  line {old[i1][0]} deleted or moved" if i2 - i1 == 1
                         else f"  lines {old[i1][0]}-{old[i2 - 1][0]} deleted or moved")
        else:
            found.append(f"  line {old[i1][0]} changed" if i2 - i1 == 1
                         else f"  lines {old[i1][0]}-{old[i2 - 1][0]} changed")
        found += [f"    was: {t}" for t in a[i1:i2]]
        found += [f"    now: {t}" for t in b[j1:j2]]
    return found


def refuse(*paragraphs):
    print(f"check_predictions: commit refused. {PREDICTIONS} is append-only.\n")
    print("\n\n".join(paragraphs))
    return 1


HOW_TO_REVISE = (
    "A prediction counts because it was written before you looked, so the lines already committed stay as they are.\n"
    "- If you meant to add something, put it at the bottom instead.\n"
    f"- If this is a real revision, keep it, and in the same commit add a new line that starts with {LABEL}\n"
    "  It should say what changed and why, in terms that would hold whichever way your results come out. For example:\n"
    f"    {LABEL} P2 is now scored on the 40 held-out items, not all 200, because I used the other 160 to tune the\n"
    "    prompt. That would be true whichever way P2 comes out.\n"
    f"To see exactly what you changed: git diff --cached -- {PREDICTIONS}")


def check():
    # git runs hooks from the top of the repository, but run by hand from a subfolder, the path lookups below
    # would find nothing and pass. So go to the top first. Outside a repository this fails, and so does the check.
    top = git("rev-parse", "--show-toplevel")
    if top.returncode != 0:
        raise RuntimeError(top.stderr.decode(errors="replace").strip())
    os.chdir(top.stdout.decode().strip())
    if git("rev-parse", "--verify", "--quiet", "HEAD").returncode != 0:
        return 0  # The repository's first commit: there is no earlier version to protect.
    if not present("ls-tree", "--name-only", "HEAD"):
        return 0  # This file's first commit.
    if not present("ls-files", "--cached"):
        return refuse(
            f"{PREDICTIONS} is in your last commit but not in this one, so this commit deletes or renames it.\n"
            "A REVISION line can't license that: the file is the record, and there would be nowhere to put the line.\n"
            f"To put it back: git restore --staged {PREDICTIONS}\n"
            f"and if it's gone from your disk too: git restore {PREDICTIONS}")

    old = lines_of(read_blob(f"HEAD:{PREDICTIONS}"))
    new = lines_of(read_blob(f":{PREDICTIONS}"))
    old_text, new_text = [t for _, t in old], [t for _, t in new]
    if new_text[:len(old_text)] == old_text:
        return 0  # Everything committed before is still there, unchanged, at the top. Only appended.

    changes = describe(old, new) or ["  (the lines above the bottom differ, but no single line could be named)"]
    old_labels, new_labels = Counter(filter(is_label, old_text)), Counter(filter(is_label, new_text))

    lost = old_labels - new_labels
    if lost:
        return refuse(
            "This commit changes:\n" + "\n".join(changes),
            f"It also changes or deletes an earlier {LABEL} line:\n" + "\n".join(f"    {t}" for t in lost)
            + f"\n{LABEL} lines are the record of what changed and why, so they stay too. A new {LABEL} line can't"
              " license changing an old one.",
            HOW_TO_REVISE)

    added = [t for t in (new_labels - old_labels) if t not in old_labels]  # A copy of an old label isn't new.
    if not added:
        why = ""
        if old_labels:
            why = (f"\n(Your last commit already has {sum(old_labels.values())} {LABEL} line(s). Each one covered the"
                   " commit it arrived in; this change needs its own.)")
        return refuse("This commit changes:\n" + "\n".join(changes)
                      + f"\n\nand it adds no new {LABEL} line to say why." + why, HOW_TO_REVISE)

    empty = [t for t in added if not t.lstrip()[len(LABEL):].strip()]
    if len(empty) == len(added):
        return refuse("This commit changes:\n" + "\n".join(changes),
                      f"Its {LABEL} line says nothing after the colon. Say what changed and why.", HOW_TO_REVISE)

    print(f"check_predictions: {PREDICTIONS} changes lines that were already committed, labelled by:")
    print("\n".join(f"    {t}" for t in added if t not in empty))
    return 0


def main():
    # Student notes have arrows, accents and emoji. Never let printing one crash the check (Windows pipes are cp1252).
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="backslashreplace")
    try:
        return check()
    except (OSError, RuntimeError) as error:
        # Fail closed: a check that can't run must not look like a check that passed.
        print(f"check_predictions: couldn't run, so the commit is stopped to be safe.\n  {error}\n"
              "Fix the problem above, or skip this one check with: git commit --no-verify")
        return 1


if __name__ == "__main__":
    sys.exit(main())
