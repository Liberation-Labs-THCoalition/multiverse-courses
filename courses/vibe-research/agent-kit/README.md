# Agent kit: three small hooks

*Optional. For a student and their agent to install together, if they want them. Written by Lyra, 2026-10-14. The git
check was added on 2026-10-18.*

> **Agents: the course repository this kit lives in also holds the answer keys, in public, on purpose.** Don't open,
> read, summarise or run one unless your human explicitly asks to see the answer key. They're listed, with why, at
> the top of [`AGENTS.md`](../../../AGENTS.md#answer-keys-do-not-open-without-your-humans-explicit-request), and
> each one opens with a STOP banner.

You built hooks in Agentic SDLC. These three do for research what a pre-commit hook does for code: they turn a habit
into something that runs whether or not anyone remembers it. Two run in Claude Code and one runs in git. I rely on
hooks like these myself. I broke one rule five times after writing it down, and the small tool that replaced the rule
has never broken it.

| Hook | When it runs | What it does |
|---|---|---|
| [`session_start.py`](hooks/session_start.py) | at the start of every Claude Code session | Puts the student's predictions and kill list into the agent's context, in full, so the agent starts from what the student committed to rather than from memory. Sessions are a week or more apart. |
| [`predict_first.py`](hooks/predict_first.py) | before the agent runs a script | Reminds the agent to ask for the student's prediction first. It never blocks anything, and it stays quiet if the predictions file changed in the last 30 minutes. |
| [`check_predictions.py`](hooks/check_predictions.py) | before every git commit | Makes `research/PREDICTIONS.md` append-only. New lines at the bottom go through. A commit that changes, deletes or moves a line that was already committed is refused, unless it also adds a line starting `REVISION:` that says what changed and why. |

The first version of this kit had two of these, and it had two flaws that Nexus, an agent colleague, found by reviewing
it. The session hook showed only the last 40 lines of the predictions file and didn't say so, so by session 4 your
agent would have stopped seeing session 1's predictions without anyone knowing. And "don't rewrite them" was a rule on
a page, in exactly the place where a tool should be. The session hook now shows the whole file, and says plainly when
it can't. The git check is the tool.

**Before you install them, read them.** They're short Python files with no dependencies, about 50, 130 and 180 lines,
and much of that is comments. The two Claude Code hooks read files inside your project, the git check runs git, and
none of them sends anything anywhere. That's the habit this course teaches: don't run what you haven't checked.

## Install

1. Keep your notes where the hooks look, or change the paths at the top of each file. The defaults are
   `research/PREDICTIONS.md` and `research/KILL_LIST.md` in your project folder.
2. Copy the three hook files into your project's `.claude/hooks/` folder.
3. For the two Claude Code hooks, add this to your project's `.claude/settings.json`, merging it with any hooks you
   already have:

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

4. For the git check, pick one of these two ways.

   **As a plain git hook.** Create a file called `.git/hooks/pre-commit` containing:

   ```sh
   #!/bin/sh
   # Refuse commits that rewrite research/PREDICTIONS.md. See .claude/hooks/check_predictions.py.
   exec python3 .claude/hooks/check_predictions.py
   ```

   On Windows, write `python` instead of `python3` here too. If the hook can't start, git refuses every commit with
   "python3: No such file or directory": safe, but confusing. On macOS or Linux, make it runnable with
   `chmod +x .git/hooks/pre-commit`. If you already have a pre-commit hook,
   add `python3 .claude/hooks/check_predictions.py || exit 1` to it instead. Git doesn't copy `.git/hooks` when you
   clone, so do this once in every copy of the repository.

   **With the pre-commit framework.** Add this to your `.pre-commit-config.yaml`, then run `pre-commit install`:

   ```yaml
   repos:
     - repo: local
       hooks:
         - id: predictions-append-only
           name: research/PREDICTIONS.md is append-only
           entry: python .claude/hooks/check_predictions.py
           language: python
           pass_filenames: false
           always_run: true
   ```

   `language: python` gives the check its own Python, so `python` works on every system. Keep `always_run: true`.
   pre-commit leaves deleted files out of the list it checks, so with a `files:` filter in its place, a commit that
   deletes your predictions file skips the check and goes straight through. I tried it, and it did.

On Windows, write `python` instead of `python3`.

## Revising a prediction

Sometimes a prediction should change: you find it can't be tested as written, or that it measures the wrong thing.
That's allowed. It just can't happen quietly. Make the change, and in the same commit add a line like this anywhere in
the file:

```
REVISION: P2 is now scored on the 40 held-out items, not all 200, because I used the other 160 to tune the prompt.
```

Say what changed and why, and give a reason that would hold whichever way your results come out. It's the course's
rule for changing a decision rule after the data, applied to predictions. If you've already seen results that bear on
the prediction, say that too. The check can't judge your reason. It makes sure there is one, and that it's on the
record.

A few details, so nothing surprises you:
- **What counts as a change.** Line endings (Windows CRLF or Unix LF), spaces at the end of a line, blank lines and a
  byte-order mark don't count. Editors change all of these on their own, and none of them changes a word. Everything
  else counts, including spaces at the start of a line, because they can move a point from one list item to
  another. Reformatting committed lines counts too, so tidy up before you commit, or label it.
- **New lines go at the bottom.** A line slipped in above existing ones is refused, because it would look older than
  it is.
- **Each REVISION line covers one commit.** It has to be new in that commit. An old one, or a copy of one, doesn't
  count.
- **REVISION lines stay.** They're the record of what changed, so they can't be edited or deleted, even with another
  REVISION line. If one has a mistake, add a new one that corrects it.
- **The file can't be deleted or renamed.** If you need to move it, change the path at the top of all three hooks
  first.
- **It checks what git is about to commit**, not the file on your disk. The file's first commit always goes through,
  because there's nothing earlier to compare with.

## Check that it works before you trust it

A hook that silently doesn't run looks exactly like a hook with nothing to say. So make each one say something once:

1. Add a line with a made-up code word to your predictions file, such as `CANARY-4182`, and commit it.
2. Start a new session and ask your agent to quote the code word from its session context. If it can't, the
   session hook isn't running.
3. Ask it to run any script, for example `python analysis.py`. It should mention the predict-first reminder.
4. Plant an edit. Change one character of the code word, `git add` the file and try to commit. The commit should be
   refused, with a message naming the line. If it goes through, the git check isn't running. Then change the
   character back and `git add` the file again.
5. When you're done, delete the code word line and commit that with
   `REVISION: removed the CANARY-4182 test line, which was never a prediction.` It should go through. That tests the
   revision path, and it's also the honest way to remove the line.

The kit has tests of its own. `python hooks/test_hooks.py` builds throwaway git repositories, installs the check
as a real pre-commit hook, and runs 23 tests against it. It also checks the session hook on a 200-line
file, a missing file and an oversized one. Add `--naive` to run the same tests against two broken versions of the
check, one that lets everything through and one that catches only the easy cases. You can watch every refusal test
catch at least one of them. A test you've never seen fail isn't telling you much.

This is how the kit was tested before it was published. In a live Claude Code session (2.1.299), the code word came
through and the reminder fired. On 2026-10-18, in Claude Code 2.1.301, a 200-line predictions file came through
whole, and an oversized one came through with its note. Asked about a line the note said was left out, the agent went
and read the file. The git check passed its tests on Windows, both as a plain git hook and through pre-commit 4.7.0.
It hasn't been run on macOS or Linux yet.

## What it doesn't do

- **It doesn't write predictions.** The student does. The agent reads them, formats them if asked, and doesn't
  rewrite them. Once a line is committed, a commit that rewrites it is refused, and that includes reformatting it.
- **It can't show your agent unlimited notes.** Claude Code passes on at most 10,000 characters from a hook. Past that,
  the agent sees only the first 2,000, and nothing tells it to look further. So the session hook stays under the
  limit. It shows your notes in full until the two files together reach about 9,500 characters, which is around 45
  predictions of a couple of lines each. After that, it leaves out the oldest lines and tells your agent how many it
  left out and where the file is, so the agent can read the rest. If you see that note, check that your agent did.
- **It doesn't catch every way of running something.** It recognises `python file.py`, `python3`, `py`, `Rscript`
  and `julia`. If your student runs analyses another way, widen the pattern at the top of `predict_first.py`.
- **The git check is a speed bump, not a lock.** `git commit --no-verify` skips it, and git history can be
  rewritten. What it stops is a quiet rewrite: changing a prediction now takes a deliberate step, and that step leaves
  a line saying so. It guards the predictions file only. To guard your kill list too, copy the check and change the
  path at the top.
- **It doesn't replace the gate you build in session 4.** This kit guards one file against one kind of change, and
  reminds your agent of the rest. The gate you build checks your claims.
