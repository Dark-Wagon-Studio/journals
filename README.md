# journals

A public, standalone installer for the journal convention. It has one job:
install the decision-trail convention — the contract, two skills, and the
git hygiene — into any repository.

The journal convention is harness-agnostic. It describes files and rules,
not tools. A stranger can install it and owe Dark Wagon Studio nothing.

## What the convention is

- **Entry layout.** One directory per line of work, one file per
  materialized plan: `journals/<area>/<NNN>-<slug>.md`, one level of
  nesting at most.
- **Numbering.** Three-digit numbers, restarting in every directory. The
  number orders the entries.
- **Status grammar.** Every entry opens with a status line. One primary
  state — Materialized, Decided, Executed — plus optional modifiers. A
  repo declares extra modifiers in the contract.
- **Citation grammar.** Entries cite by path and number, with an optional
  section or decision: `meta/002 §4`, `meta/002 D3`. External records cite
  with the `ext:` form. The lints shape-check citations; they never
  resolve them.
- **Commit tie.** A commit on the default branch that a journal entry
  authorizes names that entry in the commit body.
- **Schema ledger.** The contract carries a schema version. The ledger is
  append-only and never resets. It is the only versioning surface.

## What an install puts in a target repo

| Target in your repo | Holds |
| --- | --- |
| `journals/README.md` | The planning contract: layout, commits, status grammar, workflow, entry format, schema ledger. |
| `skills/journal-craft/` | The journal entry skill, with `journal-lint.py`. |
| `skills/ste-writing/` | The writing style skill, with its lint. |
| `.gitignore` lines | Coverage for `.agents/` and `**/.pi-subagents/*`. |
| `.agents/` | Scratch space, gitignored, with `.gitkeep` in it. |

## Install

Clone this repo to a temporary directory. Open an agent session in the
target repo. Point the agent at `prompts/journals-init.md`. The prompt is
the installer. The agent probes the target, asks when the convention may
already exist, writes the files, and writes the install record.

## Design

Three laws govern this repo:

1. Every deterministic tool is an advisory lint. It reports claims that do
   not resolve. It never generates, scores, or gates.
2. Every convention ships with the machinery that makes compliance the
   low-effort path. The status grammar ships with the lint that checks it.
3. No index builders, no metrics, no generated maps, no CI gates.

## Versioning

Installs track `main`. This repo is not versioned as a product.

One exception. The journal entry schema carries an integer. The schema
ledger in `journals/README.md` only ever grows. The lint keeps checking
older schemas, and it reports when it meets a newer one.

## Provenance

This repo succeeds the retired `baseline` repository, which succeeded the
experimental `harness` repository. Both mirrors are gone. The records
remain; the names carry the history.

Maintained by Dark Wagon Studio.
