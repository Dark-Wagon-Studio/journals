# Journal meta/003 — adopt MIT and state it in the README

Status: Decided.
Date: 2026-10-04. Depends on: meta/000.
Schema: 5.

## Goal

Give the repository a license and make the license visible on its landing
page. The owner settled the choice in the polish-pass session of 2026-10-04:
this repo adopts MIT. A `LICENSE` file makes the README's promise that a
stranger owes Dark Wagon Studio nothing true in law as well as in prose, and
it gives GitHub a license label. A License section in the README states the
grant where a first-time reader looks. Forge-side metadata values make the
GitHub landing page match the README.

This decision closes the open license question. `meta/000` Non-goals left it
open, as its predecessor had (`ext:baseline/meta/000 D6`).

## Current state (evidence, verified 2026-10-04)

- The tree carries no `LICENSE` file. GitHub reports no license.
- `README.md` has no License section; it ends `## Versioning` →
  `## Provenance` → the closing line "Maintained by Dark Wagon Studio."
- The forge metadata on `Dark-Wagon-Studio/journals` is bare: description
  null, no topics, no homepage. Verified with `gh api` this session.
- The journal ledger under `journals/meta/` holds 000–002. The next free
  number is 003.
- This repo is public on GitHub and depends on nothing outside it (`meta/002 D7`). The metadata values below name nothing outside this repository.

## Gap inventory

| Gap | Severity | Dimension |
| --- | --- | --- |
| The repo ships no license, so reuse rights are unstated | major | docs |
| The README states the owe-nothing promise but not the license that grants it | medium | docs |
| The GitHub landing page carries no description or topics | low | docs |

This entry closes all three.

## Decisions

1. **D1 — Adopt MIT for the whole repository.** The license covers every
   file in the tree: the contract text, the installer prompts, the two
   skills, the template, and the journal records. The copyright line is
   `Copyright (c) 2026 Dark Wagon Studio`. The choice was settled by the
   owner in the polish-pass session of 2026-10-04; this record restates it
   rather than quoting session words that named private workspace surfaces.
2. **D2 — The README gains a License section.** One section, placed between
   `## Versioning` and `## Provenance`, with the exact text:
   `MIT. See [LICENSE](./LICENSE).` Nothing else in the README changes.
3. **D3 — Forge metadata matches the README.** The GitHub repository gets
   description `Installer for the journal convention: a decision trail any
   repo can adopt.` and the topics `journal`, `decision-records`,
   `conventions`, `agent-skills`, `documentation`. No website, no avatar, no
   social preview; no assets exist for them.

## Execution phases

1. **License.** Write `LICENSE` with the standard MIT text and the D1
   copyright line. Done.
2. **README.** Insert the License section per D2. Done.
3. **Record.** Write this entry. Done.
4. **Verify.** Run the journal-craft lint on the tree. Done.
5. **Land.** Commit the three paths with a body citing this entry; push to
   `origin main`. Set the D3 metadata with `gh repo edit` and read it back.

## Verification

- `LICENSE` holds the standard MIT text with the exact copyright line.
- The README's License section sits between `## Versioning` and
  `## Provenance`; the link resolves to `LICENSE`.
- `python3 skills/journal-craft/journal-lint.py` exits with 0 errors.
- `git status --porcelain` shows exactly `LICENSE`, `README.md`, and this
  entry.
- `gh api repos/Dark-Wagon-Studio/journals` reports the D3 description, the
  five topics, and license `MIT`.
- The commit body cites `meta/003`.

## Files this entry will touch

- `LICENSE` — new.
- `README.md` — one License section.
- `journals/meta/003-mit-license.md` — this entry.

## Risk & rollback

Risk is low. The work adds one file and two README lines. A license grant is
irrevocable for copies already distributed, but the repository is public and
the owner settled the choice. Rollback deletes `LICENSE`, reverts the README,
and clears the forge metadata; no history rewrite.

## Non-goals

- No license change to any consuming repository. Their updates follow their
  own entries.
- No schema bump, no ledger change.
- No avatar, social preview, or homepage.
- No rewrite of historical entries. `meta/000` keeps its open license
  question as the record of its date.

## Execution log

- 2026-10-04. Wrote `LICENSE` (MIT, 2026, Dark Wagon Studio) and inserted
  the License section into `README.md` per D2. Wrote this entry.
- Verification: `python3 skills/journal-craft/journal-lint.py` reports
  0 errors, 0 notes. `git status --porcelain` shows exactly `LICENSE`,
  `README.md`, and this entry.
- Landed: one commit whose body cites `meta/003 D1 D2.`, pushed to
  `origin main`. Set the D3 description and topics with `gh repo edit`;
  read back description, topics, and license `MIT` with `gh api`.
