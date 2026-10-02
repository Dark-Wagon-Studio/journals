# Reconcile an installed journal convention

Run this in a repository that already carries the journal convention: a
`journals/README.md` with a `Schema:` ledger, and the two skills installed.
The invocation authorizes this reconcile and nothing else — no code
changes, no commits, no other files. A step whose target is already current
is a no-op.

The journals tree (this repo, cloned to a temporary directory) is the
source. Reference that clone root as the journals tree. When the target is
missing the convention entirely, run `prompts/journals-init.md` instead.

Write every generated file in the ste-writing style: active voice, short
sentences, one name for one thing.

## Probe

Gather these facts in one pass before writing anything:

- Is this a git work tree? (`git rev-parse --is-inside-work-tree`)
- Does `journals/README.md` exist and carry a `Schema:` ledger line or a
  `Modifiers:` line? Absent means stop — the convention installs first,
  with `prompts/journals-init.md`.
- The ledger lines in the target's contract, and the last date in them.
- Declared `Citations:` and `Modifiers:` lines in the target's contract.
- Do `.agents/skills/journal-craft/` and `.agents/skills/ste-writing/`
  exist? Does a legacy root `skills/journal-craft/` or
  `skills/ste-writing/` exist?
- Does `.gitignore` cover `.agents/work/` and `**/.pi-subagents/*`? Does
  it carry a blanket `.agents/` line?
- Does the target's contract carry a `## Commits` section? Which contract
  sections exist, and do they match the journals tree's
  `templates/journals-README.md`?
- The location and path of any prior journals install or reconcile entry
  in the target, for the record area.
- The highest `Schema:` line in the journals tree's
  `templates/journals-README.md`.
- Today's date.

## Steps

1. Copy `skills/journal-craft/` and `skills/ste-writing/` from the
   journals tree into the target's `.agents/skills/`, overwriting the
   target's copies. Diff each skill against the journals tree before and
   after the copy. Restore every target-only addition; keep the journals
   delta; record both in the reconcile record. Drop any `__pycache__` in
   the copy. When the target holds a legacy root `skills/<skill>` tree,
   ask whether to migrate it to `.agents/skills/` (default: migrate).
   Never leave both locations. When `.agents/skills/` holds other skills,
   leave them alone.
2. Sync the target's `journals/README.md` against the journals tree's
   `templates/journals-README.md`, one sub-step per contract area, in this
   order. Each sub-step is a no-op when the target's text is already
   current:

   (a) The where-things-go table rows.

   (b) §Layout and the citation grammar.

   (c) §Status.

   (d) §Workflow.

   (e) §Entry format.

   (f) §Style and the run paths.

   (g) §Schema prose.

   (h) Insert the `## Commits` section when the target's contract lacks
   it. Place it where the template carries it: between §Layout and
   §Status.

   Protected zones, never touched: the ledger block, and any declared
   `Citations:` or `Modifiers:` line. When the target's ledger top is
   lower than the template's highest `Schema:`, stop and offer the bump as
   an owner decision. Never append a ledger line silently. The adoption
   date follows the contract's rules: after the newest entry that carries
   no `Schema:` line, and after the last ledger date.
3. Make `.gitignore` cover `.agents/work/` and `**/.pi-subagents/*`.
   **Replace** any blanket `.agents/` ignore line with the two lines — a
   leftover blanket line silently gitignores the committed
   `.agents/skills/`.
4. Record the reconcile at `journals/<area>/<NNN>-journals-reconcile.md`,
   after the work. `Status: Executed.` — bare, no date in the status line.
   The `Schema:` line is read from the target's ledger. The record area is
   the area of the prior install or reconcile entry; when none exists, ask
   one bounded question — record under which journal area? Default:
   `meta`. `NNN` is the next free number in that area. The entry names
   what landed, the diffs restored, and the verification results.
5. Verify and present: `python3
   .agents/skills/journal-craft/journal-lint.py` from the target root
   exits with 0 errors; both skills are present at
   `.agents/skills/`; no blanket ignore line remains. Report finding
   counts, errors and notes separately. Do not commit. The reconcile
   stays in the working tree. The user commits.

## Limits

Never rewrite a legacy entry. Never add a `Schema:` line to an entry
already in the record. This does not bind the reconcile record of step 4:
that entry is yours to write, and it carries the line. Never edit a ledger
line that exists. Never append a ledger line without the owner's
confirmation. Never leave both skill locations. No commits.
