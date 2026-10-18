#!/usr/bin/env python3
"""Tests for the agent kit's hooks. Python's standard library only; nothing to install.

    python test_hooks.py           test the hooks next to this file
    python test_hooks.py --naive   also run the gate's tests against two broken gates, to show they catch them

Each gate test builds a throwaway git repository in a temp folder, installs check_predictions.py as its real
.git/hooks/pre-commit, and makes a real commit, so the hook is tested the way git runs it. The tests assume
the default paths at the top of the hooks. To test copies somewhere else, pass --gate PATH or --session PATH.
"""
import argparse
import os
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
PRED = "research/PREDICTIONS.md"
HARNESS_CAP = 10_000  # Not ours: Claude Code's cap on hook output, measured 2026-10-18 (see session_start.py).

BASE = ("# Predictions\n"
        "\n"
        "P1: B beats A by 0.2 or more.\n"
        "P2: the effect vanishes on the 40 held-out items.\n"   # line 4, the one most tests change
        "P3: fewer than 10 of the 200 answers change.\n")
P2_OLD = "P2: the effect vanishes on the 40 held-out items."
P2_NEW = "P2: the effect shrinks on the 40 held-out items."
REVISION = "REVISION: P2 now says 'shrinks', because 'vanishes' can't be tested with 40 items, whatever P2 shows.\n"

# Two broken gates, for --naive. The first can't fail. The second is the one most people write first: it
# reads the file on disk, checks that each old line is still in there somewhere, and lets any REVISION line
# anywhere through. It catches the easy breakages, which is what makes it dangerous.
NAIVE_GATES = {
    "always-passes": "import sys\nsys.exit(0)\n",
    "reads-disk": '''import subprocess, sys
PATH = "research/PREDICTIONS.md"
old = subprocess.run(["git", "show", "HEAD:" + PATH], capture_output=True, text=True, encoding="utf-8")
if old.returncode != 0:
    sys.exit(0)  # nothing committed yet
try:
    new = [line.rstrip() for line in open(PATH, encoding="utf-8").read().splitlines()]
except FileNotFoundError:
    print(PATH + " deletes or renames it")
    sys.exit(1)
if any(line.startswith("REVISION:") for line in new):
    sys.exit(0)
missing = [line for line in old.stdout.splitlines() if line.rstrip() not in new]
for line in missing:
    print("changed or deleted:", line)
sys.exit(1 if missing else 0)
''',
}


# --- plumbing -----------------------------------------------------------------------------------------

def clean_env(home):
    """git with none of this machine's settings: no global hooksPath, no autocrlf, no templates."""
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    empty = home / "empty.gitconfig"
    empty.touch()
    env.update(GIT_CONFIG_GLOBAL=str(empty), GIT_CONFIG_NOSYSTEM="1")
    return env


class Repo:
    def __init__(self, root, gate, env):
        self.dir = Path(tempfile.mkdtemp(dir=root))
        self.env, self.gate = env, gate
        self.git("init", "-q")
        self.git("config", "user.name", "Kit Test")
        self.git("config", "user.email", "kit-test@example.invalid")
        # Without this, git could turn CRLF into LF before the gate sees it, and the CRLF test couldn't fail.
        self.git("config", "core.autocrlf", "false")
        hook = self.dir / ".git" / "hooks" / "pre-commit"
        hook.parent.mkdir(parents=True, exist_ok=True)
        hook.write_bytes(f'#!/bin/sh\nexec "{Path(sys.executable).as_posix()}" "{Path(gate).as_posix()}"\n'.encode())
        hook.chmod(0o755)

    def git(self, *args):
        r = subprocess.run(["git", *args], cwd=self.dir, env=self.env, capture_output=True)
        if r.returncode != 0:
            raise RuntimeError(f"git {' '.join(args)} failed: {r.stderr.decode(errors='replace')}")
        return r.stdout.decode(errors="replace")

    def write(self, text, path=PRED):
        p = self.dir / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(text.encode("utf-8"))

    def head(self):
        r = subprocess.run(["git", "rev-parse", "-q", "--verify", "HEAD"], cwd=self.dir, env=self.env,
                           capture_output=True)
        return r.stdout.strip()

    def staged_something(self):
        return subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=self.dir, env=self.env).returncode == 1

    def commit(self, *extra):
        """Try a commit. Returns (went through, everything git and the hook printed)."""
        before = self.head()
        r = subprocess.run(["git", "commit", "-q", "-m", "test", *extra], cwd=self.dir, env=self.env,
                           capture_output=True)
        return self.head() != before, (r.stdout + r.stderr).decode("utf-8", errors="replace")

    def save(self, text, path=PRED):
        """Write, stage and commit, expecting it to go through (test set-up, not the thing under test)."""
        self.write(text, path)
        self.git("add", "-A")
        ok, out = self.commit()
        if not ok:
            raise RuntimeError("set-up commit was refused:\n" + out)


def passes(repo, *extra):
    if not repo.staged_something() and "-a" not in extra:
        raise AssertionError("nothing was staged, so this test couldn't have failed")
    ok, out = repo.commit(*extra)
    if not ok:
        raise AssertionError("refused, but should have gone through:\n" + indent(out))


def refused(repo, *must_say, extra=()):
    ok, out = repo.commit(*extra)
    if ok:
        raise AssertionError("went through, but should have been refused")
    missing = [s for s in must_say if s not in out]
    if missing:
        raise AssertionError(f"refused, but the message doesn't say {missing}:\n" + indent(out))


def indent(text):
    return "\n".join("      " + line for line in text.strip().splitlines())


# --- the gate's tests --------------------------------------------------------------------------------
# Each is (name, should it be refused?, function(repo)). A refusal test passes only if the commit is
# stopped AND the message names what changed.

def t_append(r):
    r.save(BASE)
    r.write(BASE + "P4: the gap closes by session 4.\n")
    r.git("add", PRED)
    passes(r)


def t_edit(r):
    r.save(BASE)
    r.write(BASE.replace(P2_OLD, P2_NEW))
    r.git("add", PRED)
    refused(r, "line 4", P2_OLD, P2_NEW, "REVISION:")


def t_delete(r):
    r.save(BASE)
    r.write(BASE.replace(P2_OLD + "\n", ""))
    r.git("add", PRED)
    refused(r, P2_OLD)


def t_edit_with_revision(r):
    r.save(BASE)
    r.write(BASE.replace(P2_OLD, P2_NEW) + REVISION)
    r.git("add", PRED)
    passes(r)


def t_crlf_flip(r):
    r.save(BASE)
    r.write(BASE.replace("\n", "\r\n"))
    r.git("add", PRED)
    passes(r)


def t_trailing_whitespace(r):
    r.save(BASE)
    r.write(BASE.replace(".\n", ".   \n").replace("# Predictions\n", "# Predictions\t\n"))
    r.git("add", PRED)
    passes(r)


def t_blank_lines(r):
    r.save(BASE)
    r.write(BASE.replace("\n\n", "\n").replace("P2:", "\nP2:") + "\n\n")
    r.git("add", PRED)
    passes(r)


def t_bom(r):
    r.save(BASE)
    r.write("﻿" + BASE)
    r.git("add", PRED)
    passes(r)


def t_first_commit(r):
    r.write(BASE)
    r.git("add", PRED)
    passes(r)


def t_files_first_commit(r):
    r.save("# Project\n", "README.md")
    r.write(BASE)
    r.git("add", PRED)
    passes(r)


def t_delete_file(r):
    r.save(BASE)
    r.git("rm", "-q", PRED)
    refused(r, PRED, "deletes or renames")


def t_rename_file(r):
    r.save(BASE)
    r.git("mv", PRED, "research/OLD_PREDICTIONS.md")
    refused(r, PRED, "deletes or renames")


def t_real_change_inside_crlf_flip(r):
    r.save(BASE)
    r.write(BASE.replace(P2_OLD, P2_NEW).replace("\n", "\r\n"))
    r.git("add", PRED)
    refused(r, "line 4", P2_OLD)
    _, out = r.commit()
    if "line 3" in out or "line 5" in out:
        raise AssertionError("named lines whose only change was the line ending:\n" + indent(out))


def t_inserted_above(r):
    r.save(BASE)
    r.write(BASE.replace("P2:", "P1b: written after the results, slipped in above P2.\nP2:"))
    r.git("add", PRED)
    refused(r, "P1b", "bottom")


def t_commit_all(r):
    r.save(BASE)
    r.write(BASE.replace(P2_OLD, P2_NEW))  # Not staged: `git commit -a` stages it in a temporary index.
    refused(r, P2_OLD, extra=("-a",))


def t_empty_revision(r):
    r.save(BASE)
    r.write(BASE.replace(P2_OLD, P2_NEW) + "REVISION:\n")
    r.git("add", PRED)
    refused(r, P2_OLD, "says nothing")


# UNLIKE cases: breakages a gate built only against the easy ones (edit, delete) would wave through.

def t_untracked_but_on_disk(r):
    r.save(BASE)
    r.git("rm", "-q", "--cached", PRED)  # Gone from the commit, still on the disk.
    refused(r, PRED, "deletes or renames")


def t_staged_edit_disk_restored(r):
    r.save(BASE)
    r.write(BASE.replace(P2_OLD, P2_NEW))
    r.git("add", PRED)
    r.write(BASE)  # The disk looks untouched; the commit doesn't.
    refused(r, P2_OLD)


def t_run_by_hand_from_subfolder(r):
    r.save(BASE)
    r.write(BASE.replace(P2_OLD, P2_NEW))
    r.git("add", PRED)
    # Not through git this time: a student checking by hand, from inside research/.
    run = subprocess.run([sys.executable, str(r.gate)], cwd=r.dir / "research", env=r.env, capture_output=True)
    out = (run.stdout + run.stderr).decode("utf-8", errors="replace")
    if run.returncode != 1 or P2_OLD not in out:
        raise AssertionError(f"exit {run.returncode}, should be 1 and name the changed line:\n" + indent(out or "(nothing)"))


def t_moved_line(r):
    r.save(BASE)
    r.write(BASE.replace("P1: B beats A by 0.2 or more.\n", "") + "P1: B beats A by 0.2 or more.\n")
    r.git("add", PRED)
    refused(r, "line 3", "P1: B beats A")


def t_old_revision_reused(r):
    r.save(BASE)
    r.save(BASE.replace(P2_OLD, P2_NEW) + REVISION)  # A labelled revision: allowed.
    r.write(BASE.replace(P2_OLD, P2_NEW).replace("fewer than 10", "fewer than 20") + REVISION)
    r.git("add", PRED)
    refused(r, "fewer than 10", "already")


def t_revision_copied(r):
    r.save(BASE)
    r.save(BASE.replace(P2_OLD, P2_NEW) + REVISION)
    r.write(BASE.replace(P2_OLD, P2_NEW).replace("fewer than 10", "fewer than 20") + REVISION + REVISION)
    r.git("add", PRED)
    refused(r, "fewer than 10")


def t_revision_reworded(r):
    r.save(BASE)
    r.save(BASE.replace(P2_OLD, P2_NEW) + REVISION)
    reworded = REVISION.replace("can't be tested", "is hard to test")
    r.write(BASE.replace(P2_OLD, P2_NEW) + reworded + "REVISION: tidied the wording of the line above.\n")
    r.git("add", PRED)
    refused(r, "can't be tested", "stay too")


GATE_TESTS = [
    ("append at the bottom passes", False, t_append),
    ("edit an existing line is refused", True, t_edit),
    ("delete an existing line is refused", True, t_delete),
    ("edit plus a REVISION line passes", False, t_edit_with_revision),
    ("CRLF/LF flip only passes", False, t_crlf_flip),
    ("trailing-whitespace-only change passes", False, t_trailing_whitespace),
    ("blank lines added or removed pass", False, t_blank_lines),
    ("byte-order mark added passes", False, t_bom),
    ("repository's first commit passes", False, t_first_commit),
    ("file's first commit passes", False, t_files_first_commit),
    ("whole file deleted is refused", True, t_delete_file),
    ("whole file renamed is refused", True, t_rename_file),
    ("real edit inside a CRLF flip is refused, and only it is named", True, t_real_change_inside_crlf_flip),
    ("new line slipped in above an old one is refused", True, t_inserted_above),
    ("edit committed with `git commit -a` is refused", True, t_commit_all),
    ("edit with an empty REVISION line is refused", True, t_empty_revision),
    ("UNLIKE: removed from the commit but kept on disk is refused", True, t_untracked_but_on_disk),
    ("UNLIKE: staged edit with the disk file put back is refused", True, t_staged_edit_disk_restored),
    ("UNLIKE: run by hand from a subfolder, it still refuses", True, t_run_by_hand_from_subfolder),
    ("UNLIKE: a line moved to the bottom is refused", True, t_moved_line),
    ("UNLIKE: an old REVISION line doesn't license a new edit", True, t_old_revision_reused),
    ("UNLIKE: a copy of an old REVISION line doesn't license a new edit", True, t_revision_copied),
    ("UNLIKE: an old REVISION line reworded is refused, even with a new one", True, t_revision_reworded),
]


def run_gate_tests(gate, root, env):
    results = {}
    for name, _, fn in GATE_TESTS:
        try:
            fn(Repo(root, gate, env))
            results[name] = None
        except AssertionError as failure:
            results[name] = str(failure)
        except RuntimeError as broken:  # The set-up itself failed, so the test never ran. Never counts as caught.
            results[name] = "SET-UP FAILED, test not run: " + str(broken)
    return results


# --- the session hook's tests ------------------------------------------------------------------------

def run_session(hook, project, env):
    r = subprocess.run([sys.executable, str(hook)], env={**env, "CLAUDE_PROJECT_DIR": str(project)},
                       capture_output=True)
    if r.returncode != 0:
        raise AssertionError("the hook crashed:\n" + indent(r.stderr.decode("utf-8", errors="replace")))
    return r.stdout.decode("utf-8", errors="replace").replace("\r\n", "\n")


def make_project(root, files):
    project = Path(tempfile.mkdtemp(dir=root))
    for rel, text in files.items():
        (project / rel).parent.mkdir(parents=True, exist_ok=True)
        (project / rel).write_bytes(text.encode("utf-8"))
    return project


def s_200_in_full(hook, root, env):
    lines = [f"P{i:03d}: prediction number {i}." for i in range(1, 201)]
    out = run_session(hook, make_project(root, {PRED: "\n".join(lines) + "\n", "research/KILL_LIST.md": "K1\n"}), env)
    missing = [line for line in lines if line not in out]
    if missing:
        raise AssertionError(f"{len(missing)} of 200 lines not shown; the first missing is {missing[0]!r}")
    if out.index(lines[0]) > out.index(lines[-1]):
        raise AssertionError("lines out of order")
    if "LEFT OUT" in out:
        raise AssertionError("says it left something out, but everything fitted")


def s_not_found(hook, root, env):
    out = run_session(hook, make_project(root, {PRED: "P1\n"}), env)
    if "research/KILL_LIST.md: NOT FOUND" not in out:
        raise AssertionError("a missing file isn't reported as NOT FOUND:\n" + indent(out))


def s_empty_is_not_missing(hook, root, env):
    out = run_session(hook, make_project(root, {PRED: "", "research/KILL_LIST.md": "K1\n"}), env)
    if "PREDICTIONS.md: NOT FOUND" in out or "PREDICTIONS.md" not in out:
        raise AssertionError("an empty file looks like a missing one:\n" + indent(out))


def s_over_the_cap(hook, root, env):
    lines = [f"P{i:03d}: the effect will be larger in condition B than in A, by at least 0.2." for i in range(1, 401)]
    kills = ["K1: idea one, killed in session 2.", "K2: idea two, killed in session 3."]
    project = make_project(root, {PRED: "\n".join(lines) + "\n", "research/KILL_LIST.md": "\n".join(kills) + "\n"})
    out = run_session(hook, project, env)
    if len(out.encode("utf-16-le")) // 2 > HARNESS_CAP:
        raise AssertionError(f"output is over Claude Code's {HARNESS_CAP:,}-character cap, so the agent would see "
                             "only a 2,000-character preview")
    shown = [i for i, line in enumerate(lines) if line in out]
    if not shown or shown != list(range(shown[0], 400)):
        raise AssertionError("the lines shown aren't the newest ones, in one unbroken run")
    left_out = shown[0]
    if f"lines 1-{left_out}" not in out or f"oldest {left_out} of 400" not in out:
        raise AssertionError(f"{left_out} lines were left out, but the output doesn't say so in those numbers:\n"
                             + indent(out[:600]))
    if str((project / PRED).resolve()) not in out:
        raise AssertionError("doesn't say where the full file is")
    if not all(k in out for k in kills):
        raise AssertionError("the short kill list was cut too, though it fits")


def s_non_ascii(hook, root, env):
    text = "P1: effect ≥ 0.3 → keep. Café. 💀\n"
    out = run_session(hook, make_project(root, {PRED: text, "research/KILL_LIST.md": "K1\n"}), env)
    if text.strip() not in out:
        raise AssertionError("the line didn't come through intact")


SESSION_TESTS = [
    ("a 200-line file is shown in full", s_200_in_full),
    ("a missing file says NOT FOUND", s_not_found),
    ("an empty file doesn't look missing", s_empty_is_not_missing),
    ("over Claude Code's cap: under it, and says how many lines were left out and where", s_over_the_cap),
    ("arrows, accents and emoji don't crash it (Windows pipes)", s_non_ascii),
]


# --- running -----------------------------------------------------------------------------------------

def force_remove(func, path, _):
    os.chmod(path, stat.S_IWRITE)  # git makes its object files read-only, which stops Windows deleting them.
    func(path)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--gate", default=HERE / "check_predictions.py", type=Path)
    ap.add_argument("--session", default=HERE / "session_start.py", type=Path)
    ap.add_argument("--naive", action="store_true", help="also run the gate's tests against two broken gates")
    args = ap.parse_args()
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="backslashreplace")

    root = Path(tempfile.mkdtemp(prefix="agent-kit-tests-"))
    env = clean_env(root)
    failed = 0
    try:
        print(f"check_predictions.py ({args.gate})")
        real = run_gate_tests(args.gate.resolve(), root, env)
        for name, should_refuse, _ in GATE_TESTS:
            print(f"  {'ok  ' if real[name] is None else 'FAIL'}  {name}")
            if real[name] is not None:
                print(indent(real[name]))
                failed += 1

        print(f"\nsession_start.py ({args.session})")
        for name, fn in SESSION_TESTS:
            try:
                fn(args.session.resolve(), root, env)
                print(f"  ok    {name}")
            except AssertionError as failure:
                print(f"  FAIL  {name}\n{indent(str(failure))}")
                failed += 1

        if args.naive:
            print("\nThe same gate tests against two broken gates. Every refusal test should catch at least one.")
            caught = {name: [] for name, refuse, _ in GATE_TESTS if refuse}
            for label, source in NAIVE_GATES.items():
                path = root / f"naive_{label.replace('-', '_')}.py"
                path.write_text(source, encoding="utf-8")
                print(f"\n  naive gate: {label}")
                for name, outcome in run_gate_tests(path, root, env).items():
                    reason = "" if outcome is None else outcome.splitlines()[0].rstrip(":")
                    print(f"    {'ok    ' if outcome is None else 'CAUGHT'}  {name}" + (f"  ({reason})" if reason else ""))
                    if outcome is not None and name in caught and not outcome.startswith("SET-UP"):
                        caught[name].append(label)
            uncaught = [name for name, by in caught.items() if not by]
            print()
            if uncaught:
                failed += len(uncaught)
                print("  Refusal tests that no broken gate could fail (so they prove nothing yet):")
                print("\n".join(f"    {name}" for name in uncaught))
            else:
                print(f"  Every one of the {len(caught)} refusal tests failed against at least one broken gate.")
    finally:
        shutil.rmtree(root, onerror=force_remove)

    print(f"\n{'All tests passed.' if not failed else f'{failed} FAILED.'}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
