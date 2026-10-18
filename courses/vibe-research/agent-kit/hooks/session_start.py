#!/usr/bin/env python3
"""Vibe Research agent kit: a SessionStart hook for Claude Code.

At the start of every session, it puts your student's research notes into the agent's context, in full.
The agent starts from what the student committed to, not from its own memory of it. Sessions are a
fortnight apart, and an agent's memory of a fortnight ago is the least reliable thing in the room.

It never leaves anything out quietly. The only limit is Claude Code's own (see OUTPUT_LIMIT). If the notes
don't fit under it, the hook leaves out the oldest lines, and says how many and where the full file is,
so the agent can go and read it.

It reads only the files named in NOTES, inside this project, and sends nothing anywhere.
"""
import os
import sys
from pathlib import Path

# The student's notes, relative to the project folder. Change these to wherever they keep them.
NOTES = ["research/PREDICTIONS.md", "research/KILL_LIST.md"]

# Why there's a limit at all, and why this one:
# Claude Code caps a hook's output at 10,000 characters (code.claude.com/docs/en/hooks). Over the cap it
# doesn't trim the end: it swaps the whole output for its first 2,000 characters and a file path, and it
# doesn't ask the agent to read the file. Measured in Claude Code 2.1.301 on 2026-10-18: a 9,776-character
# output arrived whole, and an 11,984-character one arrived as the 2,000-character preview. So this hook
# keeps under the cap, with a margin, and says what it left out. At about 200 characters a prediction,
# 9,500 characters is around 45 predictions before anything is left out.
OUTPUT_LIMIT = 9_500  # Measured: past Claude Code's cap the agent would see only a 2,000-character preview.

INTRO = ("Vibe Research: your student's own notes, newest last. Read them before you help. "
         "They are the student's commitments: format them if asked, but don't rewrite them.")
SOME_LEFT_OUT = (" Some older lines didn't fit in this message. Each file below says how many and where it is: "
                 "read those files in full before you help.")


def size(text):
    # Counted the way Claude Code counts (JavaScript string length), where an emoji counts as two.
    return len(text.encode("utf-16-le")) // 2


def count(n):
    return "1 line" if n == 1 else f"{n} lines"


class Note:
    def __init__(self, rel, path, lines):
        self.rel, self.path, self.lines = rel, path, lines
        self.start = 0  # Index of the first line shown. Everything before it is left out, and says so.

    def shown_size(self):
        return sum(size(line) + 1 for line in self.lines[self.start:])

    def render(self):
        n = len(self.lines)
        if n == 0:
            return f"\n--- {self.rel}: empty, nothing written yet ---"
        if self.start == 0:
            return f"\n--- {self.rel} (all {count(n)}) ---\n" + "\n".join(self.lines)
        return (f"\n--- {self.rel} (last {n - self.start} of {count(n)}) ---\n"
                f"[LEFT OUT: lines 1-{self.start}, the oldest {self.start} of {n}. They didn't fit under Claude Code's "
                f"10,000-character limit for a hook. Read the full file before you help: {self.path}]\n"
                + "\n".join(self.lines[self.start:]))


def render(blocks, notes):
    intro = INTRO + (SOME_LEFT_OUT if any(note.start for note in notes) else "")
    return "\n".join([intro] + [b.render() if isinstance(b, Note) else b for b in blocks])


def fit(blocks, notes):
    """Leave out the oldest lines, and only as many as it takes to get under OUTPUT_LIMIT."""
    if size(render(blocks, notes)) <= OUTPUT_LIMIT:
        return
    # Share the room fairly: shortest file first, so a short file is shown whole and the room it doesn't use goes
    # to the longer ones, which give up their oldest lines.
    by_size = sorted(notes, key=Note.shown_size)  # Before anything is cut, so this sorts by whole-file size.
    for note in notes:
        note.start = len(note.lines)
    room = OUTPUT_LIMIT - size(render(blocks, notes))
    for i, note in enumerate(by_size):
        share, used, start = room // (len(by_size) - i), 0, len(note.lines)
        while start > 0 and used + size(note.lines[start - 1]) + 1 <= share:
            start -= 1
            used += size(note.lines[start]) + 1
        note.start, room = start, room - used
    # The shares are estimates (a header changes length with its numbers, and a file shown whole drops its note),
    # so finish exactly: take lines away until it fits, then give lines back while they still fit.
    while size(render(blocks, notes)) > OUTPUT_LIMIT:
        cuttable = [note for note in notes if note.start < len(note.lines)]
        if not cuttable:
            break
        max(cuttable, key=Note.shown_size).start += 1
    grew = True
    while grew:
        grew = False
        for note in (note for note in notes if note.start > 0):
            note.start -= 1
            if size(render(blocks, notes)) <= OUTPUT_LIMIT:
                grew = True
            else:
                note.start += 1


def main():
    root = Path(os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd())
    blocks, notes = [], []
    for rel in NOTES:
        path = root / rel
        if not path.is_file():
            # Say so plainly. A missing file and an empty one must not look the same.
            blocks.append(f"\n--- {rel}: NOT FOUND in {root}. That is not the same as 'nothing written yet'. "
                          f"Ask your student where they keep it.")
            continue
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError as error:
            blocks.append(f"\n--- {rel}: found, but it couldn't be read ({error}). Ask your student to check it.")
            continue
        note = Note(rel, path.resolve(), lines)
        blocks.append(note)
        notes.append(note)
    fit(blocks, notes)
    # Write UTF-8 bytes. Printing text would use the console's code page on Windows (cp1252), and one arrow
    # or emoji in a prediction would crash the hook, so that the agent saw nothing at all.
    sys.stdout.buffer.write((render(blocks, notes) + "\n").encode("utf-8"))
    sys.stdout.flush()


if __name__ == "__main__":
    main()
