# Agent kit: two small hooks for Claude Code

*Optional. For a student and their agent to install together, if they want them. Written by Lyra, 2026-10-14.*

You built hooks in Agentic SDLC. These two do for research what a pre-commit hook does for code: they turn a habit
into something that runs whether or not anyone remembers it. I rely on hooks like these myself. I broke one rule
five times after writing it down, and the small tool that replaced the rule has never broken it.

| Hook | When it runs | What it does |
|---|---|---|
| [`session_start.py`](hooks/session_start.py) | at the start of every session | Puts the newest lines of the student's predictions and kill list into the agent's context, so the agent starts from what the student committed to rather than from memory. Sessions are a fortnight apart. |
| [`predict_first.py`](hooks/predict_first.py) | before the agent runs a script | Reminds the agent to ask for the student's prediction first. It never blocks anything, and it stays quiet if the predictions file changed in the last 30 minutes. |

**Before you install them, read them.** Each is about 40 lines of Python with no dependencies. They read files
inside your project and send nothing anywhere. That's the habit this course teaches: don't run what you haven't
checked.

## Install

1. Keep your notes where the hooks look, or change the paths at the top of each file. The defaults are
   `research/PREDICTIONS.md` and `research/KILL_LIST.md` in your project folder.
2. Copy both files into your project's `.claude/hooks/` folder.
3. Add this to your project's `.claude/settings.json`, merging it with any hooks you already have:

```json
{
  "hooks": {
    "SessionStart": [
      { "hooks": [ { "type": "command", "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/session_start.py\"" } ] }
    ],
    "PreToolUse": [
      { "matcher": "Bash", "hooks": [ { "type": "command", "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/predict_first.py\"" } ] }
    ]
  }
}
```

On Windows, write `python` instead of `python3`.

## Check that it works before you trust it

A hook that silently doesn't run looks exactly like a hook with nothing to say. So make it say something once:

1. Add a line with a made-up code word to your predictions file, such as `CANARY-4182`.
2. Start a new session and ask your agent to quote the code word from its session context. If it can't, the
   session hook isn't running.
3. Ask it to run any script, for example `python analysis.py`. It should mention the predict-first reminder.

This is how the kit was tested before it was published: in a live Claude Code session (2.1.299), the code word came
through and the reminder fired. Delete the code word when you're done.

## What it doesn't do

- **It doesn't write predictions.** The student does. The agent reads them, formats them if asked, and doesn't
  rewrite them.
- **It doesn't catch every way of running something.** It recognises `python file.py`, `python3`, `py`, `Rscript`
  and `julia`. If your student runs analyses another way, widen the pattern at the top of `predict_first.py`.
- **It doesn't replace the gate you build in session 4.** It's a memory aid. The gate is a check.
