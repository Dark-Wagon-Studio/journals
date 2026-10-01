# Journal meta/000 — succeed baseline: the journal convention gets its own repo

Status: Executed.
Date: 2026-10-01. Depends on: none.
Schema: 5.

## Goal

Record the founding of this repository. The owner split the retired
`baseline` repo into two successors: this repo, which carries the journal
convention and its machinery, and a `yard` repo, which carries the repo
common standard. This entry records the rulings behind the split, what this
repo inherited, and how citations to the predecessor work now that its
mirror is gone.

## Current state (evidence, verified 2026-10-01)

This repo is a fresh git tree with no history before the bootstrap commit.
The baseline repository, locally at `../baseline`, retired after this
split. The probe of the inherited tree found:

- `journals/README.md` — the contract, copied verbatim from
  `baseline/journals/README.md`. The two ledger lines (`Schema: 4. Adopted:
  2026-09-30.` and `Schema: 5. Adopted: 2026-10-01.`) came over
  byte-identical, verified with `cmp`. The ledger never resets.
- `skills/journal-craft/` and `skills/ste-writing/` — copied verbatim,
  `__pycache__` dropped. `diff -r` clean.
- `templates/journals-README.md` — copied verbatim, `cmp` clean.
- `prompts/journals-init.md` — re-cut from `baseline-init.md`, scoped to
  the journal convention.
- `README.md`, `AGENTS.md` — new. The README is the public installer
  manual; `AGENTS.md` is a minimal entry point.
- `.gitignore` — `.agents/` and `**/.pi-subagents/*`.

No other baseline file came over. The baseline `journals/meta/` instance
data stays in the retired baseline and stays citable by name. The baseline
docs contract, conventions lint, orientation skill, and other templates
belong to the yard layer.

## Gap inventory

| Gap | Severity | Dimension |
| --- | --- | --- |
| The journal convention had no home independent of the retired baseline | major | infra |
| The contract mandated `ste-writing`, which lived beside unrelated skills | major | docs |
| The public install story bundled the convention with the repo standard | major | docs |
| Citations to baseline risked dangling once its mirror went away | medium | record |

This entry closes all four. The convention now lives in a public repo of
its own, the skills it mandates ship with it, the installer installs only
this layer, and the citation grammar names the predecessor without
resolving it.

## Decisions

1. **D1 — Full succession.** The owner split baseline by ruling:
   "Full succession. journals = journal convention + its machinery. yard =
   everything else of baseline's repo common standard + today's catalog and
   installer." This repo takes the first half. Everything else went to the
   yard repo. No baseline capability falls between the two.
2. **D2 — Public hosting on GitHub.** The owner ruled: "journals: public,
   GitHub org `Dark-Wagon-Studio`." The repo publishes at
   `https://github.com/Dark-Wagon-Studio/journals`. The yard repo is
   private on the forge and is not this repo's concern.
3. **D3 — Verbatim inheritance; the ledger never resets.** The contract,
   both skills, and the template copied byte-identical. Schema 4 and
   schema 5 stay in the ledger with their original adoption dates. A fresh
   history does not reset a ledger. Every entry written here carries a
   `Schema:` line against that ledger.
4. **D4 — Baseline is named, never resolved.** The owner amended the plan
   at approval: "the baseline mirror no longer exists on GitHub. Refer to
   baseline by name in records and citations, but never probe the remote,
   never push to it." Citations to the predecessor use the `ext:` form
   (`ext:baseline/meta/003`), which the lints shape-check and never
   resolve. The README provenance section names both predecessor
   repositories and links neither.
5. **D5 — The bootstrap commit cites this entry.** The commit tie
   (`ext:baseline/meta/007`) governs from the first commit: the bootstrap
   commit's body names `meta/000` as its authorizing entry. The owner's
   brief for this bootstrap is the explicit instruction to execute; the
   no-same-session-execution gate does not block it.

## Execution phases

1. **Inherit.** Copy the contract, both skills, and the template
   verbatim; verify with `cmp` and `diff -r`. Done.
2. **Re-cut the installer.** Write `prompts/journals-init.md` with the
   five-phase structure scoped to this layer. Done.
3. **Author the public surfaces.** Write `README.md` and `AGENTS.md`.
   Depends on 2. Done.
4. **Record.** Write this entry. Depends on 1 to 3. Done.
5. **Verify.** Run the lints and the tree check. Depends on 4. Done.
6. **Publish.** Commit, create the GitHub repo, push, and smoke-clone.
   Depends on 5. Done.

## Verification

- `grep -n "Adopted: 2026" journals/README.md` shows both ledger lines
  exact.
- `python3 skills/journal-craft/journal-lint.py` exits with 0 errors
  against schema 5.
- The conventions lint (run from the baseline tree until the yard repo
  carries its own copy) reports 0 errors on `README.md`.
- The tree matches the inventory table, nothing extra.
- `gh repo view Dark-Wagon-Studio/journals` reports visibility PUBLIC.
- A fresh clone diffs clean against the local tree, excluding `.git` and
  `.agents`.

## Files this entry will touch

- `journals/README.md` — inherited verbatim from `baseline/journals/README.md`.
- `skills/journal-craft/` — inherited verbatim.
- `skills/ste-writing/` — inherited verbatim.
- `templates/journals-README.md` — inherited verbatim.
- `prompts/journals-init.md` — re-cut from `baseline/prompts/baseline-init.md`.
- `README.md`, `AGENTS.md`, `.gitignore` — new.
- `journals/meta/000-succession.md` — this entry.

## Risk & rollback

Risk is low. Every file in the tree is new or a verified verbatim copy of a
retired source. Rollback deletes the repository and the local tree; the
retired baseline remains the record of the prior state. The ledger lines
are the one asset with no recovery path except the archived baseline tree,
so their byte-identity was verified before any commit.

## Non-goals

- No yard repo work here. The yard layer builds, hosts, and records
  elsewhere.
- No changes to consumer repositories (the org repo, rook) from this repo.
  Their updates follow their own entries.
- No license file. The question stays open, as it was in the predecessor
  (`ext:baseline/meta/000 D6`).
- No upgrade path in the installer. A target that already carries a schema
  ledger stops the install; reconciliation is future work.

## Execution log

- 2026-10-01. Ran the bootstrap brief against the new tree.
- Inheritance: contract, both skills, and template copied. `cmp` and
  `diff -r` verified byte identity. `__pycache__` dropped from the
  journal-craft copy.
- Wrote `prompts/journals-init.md`, `README.md`, `AGENTS.md`,
  `.gitignore`, and this entry. The installer keeps the five-phase shape
  and the never-overwrite-a-ledger guard from `baseline-init.md`.
- Verification: both ledger lines exact; `journal-lint.py` 0 errors;
  conventions lint 0 errors on `README.md`; tree matches the inventory.
- Publish: `git init -b main`, one bootstrap commit whose body names this
  entry, `gh repo create Dark-Wagon-Studio/journals --public --source .
  --push`, and a smoke clone diffed clean against the local tree.
