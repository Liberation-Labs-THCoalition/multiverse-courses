#!/usr/bin/env python3
"""Vibe Research agent kit: a PreToolUse hook (matcher: Bash) for Claude Code.

When the agent is about to run a script, it reminds the agent to ask for the student's prediction first.
It never blocks anything. It stays quiet if the predictions file changed in the last QUIET_MINUTES,
since the student has probably just written one.

It catches `python analysis.py`-style runs (also python3, py, Rscript, julia). If your student runs
things another way, widen RUNS_A_SCRIPT. It reads one file's timestamp and sends nothing anywhere.
"""
import json
import os
import re
import sys
import time
from pathlib import Path

PREDICTIONS = "research/PREDICTIONS.md"
QUIET_MINUTES = 30
RUNS_A_SCRIPT = re.compile(
    r"(^|[\s;&|(])(python3?|py|Rscript|julia)(\s+-[A-Za-z]+)*\s+[^\s-]\S*\.(py|R|jl)\b")
REMINDER = ("predict-first: you are about to run a script. If its output is a result your student will "
            "interpret, have they written down what they expect, before now? If not, ask them first, and "
            "keep their answer where both of you can see it. (If this run is plumbing, ignore this.)")


def recently_predicted():
    root = Path(os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd())
    try:
        return time.time() - (root / PREDICTIONS).stat().st_mtime < QUIET_MINUTES * 60
    except OSError:
        return False


def main():
    try:
        data = json.load(sys.stdin)
    except ValueError:
        return  # Not the input we expect: stay out of the way rather than break the tool call.
    command = (data.get("tool_input") or {}).get("command", "")
    if RUNS_A_SCRIPT.search(command) and not recently_predicted():
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse",
                                                 "additionalContext": REMINDER}}))


if __name__ == "__main__":
    main()
