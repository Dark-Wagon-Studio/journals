#!/usr/bin/env python3
"""widen-entry-numbers.py — one-shot migration: two-digit journal numbers to three.

Widens every two-digit journal entry to the three-digit shape (D7): the file
`journals/<area>/<NN>-<slug>.md` is `git mv`d to the zero-padded three-digit
name so history follows, the entry's line-1 heading number gains a digit, and
every two-digit citation or entry path in scope is padded in place. Numbers
keep their value and gain a digit; nothing renumbers. The only edits are
address edits — filenames, the heading number, citations (D10). Prose, dates,
decisions, statuses, and execution logs stay untouched.

The script carries its own two-digit source patterns, mirroring the citation
grammar's shape: an optional `journals/` prefix, one or two area segments with
a letter-led first segment (so ratio tokens like `31/37` never match), `/` +
two digits, an optional `-slug`, an optional `.md`, and the lint's boundary
guards. It never imports the lint's patterns: those are already widened to
three digits and would find nothing (D13). Code spans rewrite too, unlike the
lint: a backticked entry path is an address. Front matter is in scope:
`Depends on:` and `Status: ... Superseded by <area>/<NN>` lines are citations.

Scopes: every `.md` under `journals/` (README.md included), every `.md` under
`docs/`, the root `AGENTS.md`, and the root `README.md`. Never `templates/`,
`prompts/`, or `skills/`. Dot-directories are skipped everywhere.

Dry run is the default: it prints the per-file plan — each rename (old → new)
and, per rewritten file, each line number with before → after — and changes
nothing. `--apply` performs the work (git mv + rewrites) and prints the same
plan as it executes. A migrated tree can still hold citation-shaped
historical prose: a rename-illustration Before column, or dated evidence.
The dry run names those lines, and the operator keeps them. Review the plan
before every `--apply`. The lints are its verifier: this script writes
files, which the lints never do. It is a one-shot migration, not a lint.

Exit codes: 0 in both modes; 1 with a clear message when the tree is not a
git work tree (git mv is required so history follows), when `journals/` is
missing, when a rename source is not git-tracked, when a rename target
already exists, when an in-scope file cannot be read or written, or when an
entry heading still holds the two-digit shape after the rewrites.

Usage (from the repo root):

    python3 skills/journal-craft/widen-entry-numbers.py [--apply]

Inputs: the `journals/`, `docs/` trees and the two root Markdown files above.
Deterministic: two runs on the same tree print identical output. Python 3
standard library only; no network.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

# Two-digit source shapes (D13). The migration owns these; it imports nothing
# from journal-lint, whose patterns phase 2 already widened to three digits.
FILENAME_RE = re.compile(r"^(\d{2})-(.+)\.md$")
HEADING_RE = re.compile(r"^# Journal (.+)/(\d{2}) — (.+)$")
# Post-check shape: a line-1 heading that still carries a two-digit number
# after the rewrites. The digit-run guards keep a padded three-digit heading
# from matching.
HEADING_TWO_DIGIT_RE = re.compile(r"^# Journal .+/(?<!\d)\d{2}(?!\d) — ")
# Citation grammar, two-digit source form. Same head, area, slug, and tail
# guards as the importable lint grammar: an optional `journals/` prefix, one
# or two area segments with a letter-led first segment, /<NN>, an optional
# -slug and .md. The lookbehind keeps a filesystem path from reading as a
# citation; the trailing guards keep a longer path, a wider number (`002`),
# or a non-.md extension from matching.
_HEAD = r"(?<![\w./-])(?:journals/)?"
_AREA = r"([A-Za-z][A-Za-z0-9_-]*(?:/[A-Za-z0-9][A-Za-z0-9_-]*)?)"
_ENTRY = r"/(\d{2})(?:-[A-Za-z0-9][A-Za-z0-9_-]*)?(?:\.md)?"
_TAIL = r"(?![\w/-])(?!\.[A-Za-z0-9])"
CITATION_RE = re.compile(_HEAD + _AREA + _ENTRY + _TAIL)

SCOPED_ROOT_FILES = ("AGENTS.md", "README.md")


def pad_citation(m):
    """re.sub callback: rewrite only the number subexpression, zero-padded."""
    whole = m.group(0)
    s = m.start(2) - m.start(0)
    e = m.end(2) - m.start(0)
    return whole[:s] + m.group(2).zfill(3) + whole[e:]


def pad_heading(m):
    return f"# Journal {m.group(1)}/{m.group(2).zfill(3)} — {m.group(3)}"


def widen_line(line, pad_first):
    new = line
    if pad_first:
        new = HEADING_RE.sub(pad_heading, new)
    if CITATION_RE.search(new):
        new = CITATION_RE.sub(pad_citation, new)
    return new


def under_hidden(rel):
    return any(part.startswith(".") for part in rel.parts)


def discover_renames(root, journals):
    """Two-digit entries under journals/ as (old_rel, new_rel), sorted.

    README.md and dot-directories are skipped; a three-digit filename cannot
    match the anchored two-digit pattern, so a migrated tree yields nothing.
    """
    renames = []
    for p in sorted(journals.rglob("*.md")):
        if p.name == "README.md" or not p.is_file():
            continue
        rel = p.relative_to(root)
        if under_hidden(rel):
            continue
        fm = FILENAME_RE.match(p.name)
        if fm is None:
            continue
        new_name = fm.group(1).zfill(3) + "-" + fm.group(2) + ".md"
        renames.append((rel, rel.with_name(new_name)))
    return renames


def scoped_files(root, journals):
    """Every in-scope .md as a repo-relative path, in walk order.

    journals/ first (README.md included), then docs/, then the two root
    files. Never templates/, prompts/, or skills/.
    """
    files = []
    for base in (journals, root / "docs"):
        if not base.is_dir():
            continue
        for p in sorted(base.rglob("*.md")):
            rel = p.relative_to(root)
            if not under_hidden(rel):
                files.append(rel)
    for name in SCOPED_ROOT_FILES:
        if (root / name).is_file():
            files.append(Path(name))
    return files


def read_text(path):
    """Read bytes as text without newline translation, or None on failure."""
    try:
        with open(path, "r", encoding="utf-8", newline="") as fh:
            return fh.read()
    except (OSError, UnicodeDecodeError):
        return None


def build_changes(root, renames):
    """Per in-scope file: (display_rel, new_text, edits) for changed files.

    display_rel is the post-rename path, so the plan addresses what exists
    after --apply. edits are (lineno, before, after) tuples in file order.
    """
    renamed = dict(renames)
    changes = []
    for rel in scoped_files(root, root / "journals"):
        text = read_text(root / rel)
        if text is None:
            print(f"error: cannot read {rel.as_posix()}", file=sys.stderr)
            return None
        lines = text.split("\n")
        edits = []
        out = []
        for i, line in enumerate(lines, 1):
            new = widen_line(line, pad_first=rel in renamed)
            if new != line:
                edits.append((i, line, new))
            out.append(new)
        if edits:
            changes.append((renamed.get(rel, rel), "\n".join(out), edits))
    return changes


def inside_work_tree(root):
    res = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"], cwd=root,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    return res.returncode == 0 and res.stdout.strip() == b"true"


def git_tracked(root, rel):
    """True when git tracks the path (ls-files --error-unmatch)."""
    res = subprocess.run(
        ["git", "ls-files", "--error-unmatch", rel.as_posix()], cwd=root,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    return res.returncode == 0


def two_digit_headings(root, journals):
    """In-scope entry files under journals/ whose line 1 still carries the
    two-digit heading shape, as repo-relative paths, sorted.
    """
    bad = []
    for p in sorted(journals.rglob("*.md")):
        if p.name == "README.md" or not p.is_file():
            continue
        rel = p.relative_to(root)
        if under_hidden(rel):
            continue
        text = read_text(p)
        if text is None:
            continue
        if HEADING_TWO_DIGIT_RE.match(text.split("\n", 1)[0]):
            bad.append(rel)
    return bad


def git_mv(root, old, new):
    res = subprocess.run(
        ["git", "mv", old.as_posix(), new.as_posix()], cwd=root,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if res.returncode != 0:
        sys.stderr.write(res.stderr.decode("utf-8", "replace"))
        return False
    return True


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Widen two-digit journal entry numbers to three "
                    "(dry run by default; --apply to execute).")
    ap.add_argument("--apply", action="store_true",
                    help="perform the renames and rewrites (default: dry run)")
    args = ap.parse_args(argv)
    root = Path.cwd()

    if not inside_work_tree(root):
        print("error: not a git work tree; git mv is required so history "
              "follows", file=sys.stderr)
        return 1
    journals = root / "journals"
    if not journals.is_dir():
        print("error: journals/ is missing; nothing to migrate",
              file=sys.stderr)
        return 1

    renames = discover_renames(root, journals)
    for old, new in renames:
        if not git_tracked(root, old):
            print(f"error: {old.as_posix()} is not tracked by git; a rename "
                  f"needs a tracked source", file=sys.stderr)
            return 1
        if (root / new).exists():
            print(f"error: {new.as_posix()} already exists; refusing to "
                  f"overwrite ({old.as_posix()} -> {new.as_posix()})",
                  file=sys.stderr)
            return 1
    changes = build_changes(root, renames)
    if changes is None:
        return 1

    mode = "apply" if args.apply else "dry run"
    for old, new in renames:
        print(f"rename: {old.as_posix()} -> {new.as_posix()}")
        if args.apply and not git_mv(root, old, new):
            print(f"error: git mv failed for {old.as_posix()}",
                  file=sys.stderr)
            return 1
    for rel, new_text, edits in changes:
        print()
        print(rel.as_posix())
        for lineno, before, after in edits:
            print(f"{rel.as_posix()}:{lineno}")
            print(f"- {before}")
            print(f"+ {after}")
        if args.apply:
            try:
                with open(root / rel, "w", encoding="utf-8", newline="") as fh:
                    fh.write(new_text)
            except OSError:
                print(f"error: cannot write {rel.as_posix()}", file=sys.stderr)
                return 1

    if args.apply:
        bad = two_digit_headings(root, journals)
        for rel in bad:
            print(f"error: {rel.as_posix()}: line 1 still holds a two-digit "
                  f"heading number", file=sys.stderr)
        if bad:
            return 1

    n_edits = sum(len(edits) for _r, _t, edits in changes)
    print()
    if not renames and not changes:
        print(f"{mode}: nothing to do (0 renames, 0 line edits); the tree is "
              f"already three-digit")
    elif args.apply:
        print(f"applied: {len(renames)} renames, {n_edits} line edits in "
              f"{len(changes)} files")
    else:
        print(f"dry run: {len(renames)} renames, {n_edits} line edits in "
              f"{len(changes)} files; no changes made, pass --apply to "
              f"execute")
    return 0


if __name__ == "__main__":
    sys.exit(main())
