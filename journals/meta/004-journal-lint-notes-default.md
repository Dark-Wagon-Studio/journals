# Journal meta/004 — hide lint notes from the default report

Status: Executed.
Date: 2026-10-07. Depends on: none.
Schema: 5.

## Goal

Keep a legacy-heavy repo's lint run from flooding context with note lines.
The lint's report prints every finding one per line before the summary, so
a repo whose legacy entries carry many notes drowns its errors and its
summary in a wall of note lines. Monsoon's run today prints 595 note lines
before a clean summary. The fix is presentation only: hide note lines from
the default report, keep both counts in the summary, and recover the note
list with `--notes`.

Receipts:

> "evaluate the journal lint and whether notes can be off by default so it
> doesn't flood context @journals/. and want to update to @yard/ and
> @monsoon/"
> — the user, 2026-10-07

> "Hide notes; keep counts in summary"
> — the user, 2026-10-07

## Current state (evidence, verified 2026-10-07)

- The lint docstring reads: "Findings print one per line as
  `<path>:<line> <class> <code> <message>`, then a summary line." Nothing
  distinguishes classes in the report shape.
- `references/rules.md` opens with the same claim: "Findings print one per
  line … then a summary line."
- Monsoon's run under schema 5: `summary: 0 errors, 595 notes`, preceded by
  595 note lines. That wall is the flood.
- Notes are "information, not work" (`SKILL.md`, Checking): they never
  fail a run and fixing them is never required.

## Gap inventory

- The default report prints note-class findings unconditionally (medium,
  tooling). A zero-error run still floods context when the tree carries
  many legacy entries.

## Decisions

1. **D1 — quiet default with `--notes`.** Error lines and the summary line
   always print. Note lines print only when `--notes` is passed. Exit
   codes do not change; notes never fail the run.
2. **D2 — the summary carries both counts.** The summary line keeps its
   error and note counts in both modes, so a quiet run still reports how
   many notes exist.

Presentation only: every check, every classification, and every exit code
stay as they are.

## Phases

1. This entry.
2. The lint edit: usage line, report sentence, `--notes` flag in `main()`.
3. The prose edits: `references/rules.md` intro, `SKILL.md` Checking.
4. Fixture smoke: default output, `--notes` output, exit codes, determinism
   diff, schema-6 notice case.
5. Repo lint, execution log, commit.

## Verification

- The fixture table holds: default hides notes, `--notes` lists them,
   exit codes unchanged (1 errors, 2 notice, 0 otherwise), the second-run
   diff is empty, the schema-6 notice prints in both modes.
- `python3 skills/journal-craft/journal-lint.py` from the repo root: exit
  0, one summary line.

## Files

- `skills/journal-craft/journal-lint.py` — the report changes.
- `skills/journal-craft/references/rules.md` — the report sentence.
- `skills/journal-craft/SKILL.md` — the Checking paragraph.
- `journals/meta/004-journal-lint-notes-default.md` — this entry.

## Risk & rollback

Risk: a current entry's note hides from the default run and goes unread.
The summary count still names it and `--notes` recovers the list. Rollback:
`git revert` of the landing commit.

## Non-goals

- No schema bump; no ledger edit.
- No change to any check, classification, or exit code.
- No fix of monsoon's legacy notes: the contract calls them information,
  not work.
- No change to the fork's `widen-entry-numbers.py`.

## Execution log

- 2026-10-07. Wrote this entry, then the lint edit (usage line, report
  sentence, `--notes` in `main()`) and the two prose edits per D1/D2.
- Verification: fixture smoke in scratch held the full table — default
  prints the error line and summary only (`1 error, 2 notes`), `--notes`
  lists all findings, exit 1/1/1 with errors and 0 after the fix, second-
  run diff empty, schema-6 ledger prints the notice alone with exit 2 in
  both modes. Repo lint: exit 0, one summary line (0 errors, 0 notes).
  `git status --porcelain` shows exactly the three skill files and this
  entry.
