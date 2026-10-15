#!/usr/bin/env python3
"""Vibe Research agent kit: a SessionStart hook for Claude Code.

At the start of every session, it puts the newest lines of your student's research notes into the
agent's context. The agent starts from what the student committed to, not from its own memory of it.
Sessions are a fortnight apart, and an agent's memory of a fortnight ago is the least reliable thing in
the room.

It reads only the files named in NOTES, inside this project, and sends nothing anywhere.
"""
import os
from pathlib import Path

# The student's notes, relative to the project folder. Change these to wherever they keep them.
NOTES = ["research/PREDICTIONS.md", "research/KILL_LIST.md"]
TAIL_LINES = 40


def main():
    root = Path(os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd())
    out = ["Vibe Research: your student's own notes, newest last. Read them before you help. "
           "They are the student's commitments: format them if asked, but don't rewrite them."]
    for rel in NOTES:
        path = root / rel
        if not path.is_file():
            # Say so plainly. A missing file and an empty one must not look the same.
            out.append(f"\n--- {rel}: NOT FOUND in {root}. That is not the same as 'nothing written yet'. "
                       f"Ask your student where they keep it.")
            continue
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        shown = lines[-TAIL_LINES:]
        out.append(f"\n--- {rel} (last {len(shown)} of {len(lines)} lines) ---\n" + "\n".join(shown))
    print("\n".join(out))


if __name__ == "__main__":
    main()
