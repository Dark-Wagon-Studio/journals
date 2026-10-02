# Journal meta/002 — the journals-reconcile prompt

Status: Executed.
Date: 2026-10-02. Depends on: meta/001.
Schema: 5.

## Goal

Close the deferred reconcile mechanism. `prompts/journals-init.md` stops
on an installed convention and carries no upgrade path; `meta/000`
deferred one as future work. This entry writes
`prompts/journals-reconcile.md` — the upgrade path for a target that
already carries the journal convention — and re-points the installer
and the repo docs at it.

The user instructed this line of work on 2026-10-02, restated here: the
convention is to be reconciled into a consuming repository, and the
missing reconcile prompt is to be authored first. The autonomy ruling,
quoted verbatim (it names nothing private):

> "autonomy granted for execution until rcc complete. report once ready to push."
> — the user, 2026-10-02

## Current state (evidence, verified 2026-10-02)

- `prompts/` holds `journals-init.md` only. No reconcile prompt exists.
- `prompts/journals-init.md` line 113 (step 3.1): on an existing contract
  with a `Schema:` or `Modifiers:` line it stops: "This installer carries
  no upgrade path." Phase 2 stop condition 1 (line 70: "`journals/` exists
  — a convention may already be installed") also earns the pointer.
- `README.md` §Install (lines 40-45) names `prompts/journals-init.md`
  only.
- `AGENTS.md` repository map lists `journals/meta/`, `skills/`, and
  `.agents/work/` — no `prompts/` row.
- Sources for skill copies: `skills/journal-craft/` and
  `skills/ste-writing/` at this repo's root.

## Gap inventory

| Gap | Severity | Dimension |
| --- | --- | --- |
| A target with an installed convention has no upgrade path; the installer stops | major | docs |
| The installer and README do not point at the upgrade path when it lands | medium | docs |
| The repository map omits `prompts/` | low | docs |

## Decisions

1. **D1 — A reconcile prompt, mirroring the installer.** Write
   `prompts/journals-reconcile.md` in the structure of
   `prompts/journals-init.md`: title, intro, Probe, Steps, Limits. The
   invocation authorizes the reconcile and nothing else. A step whose
   target is already current is a no-op. The journals tree is the
   source.
2. **D2 — Skills step copies and preserves.** Step 1 copies both skills
   into the target's `.agents/skills/`, overwriting, after diffing each
   skill before and after and restoring every target-only addition. A
   legacy root `skills/<skill>` tree migrates to `.agents/skills/` (ask,
   default: migrate). Never leave both locations. Drop `__pycache__`.
3. **D3 — Contract sync lettered (a)-(h), with (h) the `## Commits`
   insertion.** Step 2 syncs, in order: (a) the where-things-go table
   rows, (b) §Layout and citation grammar, (c) §Status, (d) §Workflow,
   (e) §Entry format, (f) §Style run paths, (g) §Schema prose, (h) the
   `## Commits` section when the target's contract lacks it, placed where
   the template carries it — between §Layout and §Status. Each sub-step is
   a no-op when current. The ledger block and any declared
   `Citations:`/`Modifiers:` lines are protected zones, never touched.
   When the target's ledger top is lower than the template's, stop and
   offer the bump as an owner decision; never append silently; the
   adoption date follows the contract's rules.
4. **D4 — Record after the work, schema from the target.** Step 4 writes
   `journals/<area>/<NNN>-journals-reconcile.md` with `Status: Executed.`
   and the `Schema:` line read from the target's ledger. The record area
   follows the prior install or reconcile entry, else ask with default
   `meta`.
5. **D5 — Verify, no commits.** Step 5 runs the journal-craft lint from
   the vendored copy, checks both skills, checks the ignore lines, and
   reports errors and notes separately. No commits.
6. **D6 — The installer and docs re-point.** Step 3.1's stop and Phase 2
   stop condition 1 of `prompts/journals-init.md` name
   `prompts/journals-reconcile.md`. `README.md` §Install names the
   reconcile prompt. The `AGENTS.md` map gains a `prompts/` row.
7. **D7 — This public repo names no private workspace repo.** The owner
   ruled on 2026-10-02, restated: this repository is public, depends on
   nothing else in the workspace, and never mentions sibling private
   repositories or workspace internals. Session rulings whose verbatim
   words name such repos are restated in this record, not quoted. The
   consuming repository keeps the verbatim receipts in its own private
   record.

## Execution phases

1. **Materialize** this entry. Done.
2. **Write** `prompts/journals-reconcile.md`. Depends on 1.
3. **Re-point** `prompts/journals-init.md`. Depends on 2.
4. **Update** `README.md` §Install and the `AGENTS.md` map. Depends on 2.
5. **Verify**: lint, porcelain set, read-through of the 2(h) lettering.
   Depends on 2 to 4.
6. **Flip** this entry to `Status: Executed.` and append the execution
   log. Depends on 5.

## Verification

- `python3 skills/journal-craft/journal-lint.py` from the journals root
  exits with 0 errors.
- `git status --porcelain` shows exactly the new prompt, this entry,
  `prompts/journals-init.md`, `README.md`, and `AGENTS.md`.
- Read-through: the new prompt's step 2 letters (a)-(h) with (h) the
  `## Commits` insertion.
- Read-through: the installer stop and stop condition 1, the §Install
  section, and the map row match the quotes above.
- A case-insensitive search for each sibling repository's name, run
  over this repo's uncommitted files, finds no match: the new surfaces
  name no private workspace repo (D7). This record does not spell the
  names out. The historical `meta/000` record predates the ruling and
  stays untouched, per the entry-immutability contract.

## Files this entry will touch

- `prompts/journals-reconcile.md` — new.
- `prompts/journals-init.md` — two pointers.
- `README.md` — §Install sentence.
- `AGENTS.md` — one repository map row.
- `journals/meta/002-journals-reconcile-prompt.md` — this entry.

## Risk & rollback

Risk is low. The work adds one prompt and edits prose pointers. No ledger
line, historical entry, template, or skill changes. Rollback reverts the
working tree with `git checkout` and removes the new files; no external
state changes.

## Non-goals

- No target-repo work here; running the prompt against a consuming
  repository is that repo's own line of work, outside this entry.
- No schema bump.
- No ledger change in any target.
- No rewrite of the historical record; `meta/000` keeps what it wrote.
- Push out of scope.

## Execution log

- 2026-10-02. Wrote `prompts/journals-reconcile.md` per D1 to D5: intro
  with the authorization clause and the no-op rule, Probe, Steps 1-5,
  Limits. Step 2 letters its contract-sync sub-steps (a)-(h); (h) inserts
  the `## Commits` section between §Layout and §Status.
- Re-pointed `prompts/journals-init.md`: Phase 2 stop condition 1 and the
  step 3.1 stop now name `prompts/journals-reconcile.md` as the upgrade
  path.
- Updated `README.md` §Install: one reconcile paragraph.
- Updated `AGENTS.md`: one `prompts/` row in the repository map.
- On the owner's D7 ruling, scrubbed this entry before commit: the
  receipts that named a private workspace repo in verbatim words became
  restatements, and the dangling cross-reference sentences that named it
  came out. The consuming repo's private record holds the verbatim
  receipts.
- Verification: `python3 skills/journal-craft/journal-lint.py` from the
  journals root reports 0 errors, 0 notes. `git status --porcelain` shows
  exactly `AGENTS.md`, `README.md`, `prompts/journals-init.md`,
  `prompts/journals-reconcile.md`, and this entry. Read-through confirms
  the (a)-(h) lettering and the three re-points.
- Review pass (conductor, 2026-10-02): qualified the §Install reconcile
  paragraph — it states the never-edit-a-ledger-line rule and the
  owner-decided bump, not a blanket "without touching the ledger".
  Re-ran the journal-craft lint: 0 errors, 0 notes.
