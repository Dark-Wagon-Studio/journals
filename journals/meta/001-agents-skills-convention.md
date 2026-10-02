# Journal meta/001 — adopt the `.agents` convention

Status: Executed.
Date: 2026-10-02. Depends on: meta/000.
Schema: 5.

## Goal

Adopt the de-facto `.agents` convention in the direction each role demands.
A **publisher** authors its skills at root `skills/`. A **consumer**
receives them at `.agents/skills/`, committed. Scratch lives at
`.agents/work/`, gitignored. This repo is a publisher: its two skills stay
at root `skills/`. The change lands in the installer, which names root
`skills/<name>/` as the source in the journals tree and
`.agents/skills/<name>/` as the install target in the consuming repo. The
README install table, the contract, and the template describe that target
shape. References to a layer owned outside this repo come out.

Historical entries stay untouched. Their bare `skills/` paths are the
record of the state at their date.

## Current state (evidence, verified 2026-10-02)

The tree before this change:

- Root `skills/journal-craft/` and `skills/ste-writing/` held the two
  published skills, with their lints. They stay there.
- `.gitignore` carried two lines: `.agents/` and `**/.pi-subagents/*`. The
  blanket `.agents/` line gitignored the whole scratch tree.
- `.agents/` held `work/` (an untracked plan) and an untracked `.gitkeep`.
- The installer copied the skills into the target's root `skills/` and named
  root `skills/` as both the source and the installed location, so the
  publisher's role and the consumer's role read as the same path.

## Gap inventory

| Gap | Severity | Dimension |
| --- | --- | --- |
| The installer wrote installed skills into a consumer's root `skills/`, mixed with ordinary repo content | major | docs |
| The blanket `.agents/` ignore line blocked a committed `.agents/skills/` in a consumer | major | infra |
| The installer had no legacy handling for a target with a root `skills/` tree | medium | infra |
| The contract, template, and README install table named root `skills/` as the installed location | medium | docs |
| References to a layer owned outside this repo sat in the skills, the installer, and the README | low | docs |

This entry closes all five.

## Decisions

1. **D1 — Root `skills/` holds the published skills.** This repo authors
   `journal-craft` and `ste-writing`; they stay at `skills/<name>/`. A
   publisher's catalog is not an install.
2. **D2 — `.agents/skills/` is the install target.** A consumer repo
   receives skills at `.agents/skills/<name>/`, committed. The installer's
   target side uses that path: the install list, the probe, the stop, the
   verify, and the lint run all name it.
3. **D3 — The installer source is root `skills/`.** The journals tree is
   the source. Steps 3.3 and 3.4 copy `skills/<name>/` from the journals
   tree into `.agents/skills/<name>/` in the target.
4. **D4 — `.agents/work/` is scratch.** The blanket `.agents/` ignore line
   is replaced by `.agents/work/`. Scratch, tool artifacts, and subagent
   output are ignored; a consumer's committed `.agents/skills/` is not.
5. **D5 — The installer keeps legacy targets working.** It probes both
   `.agents/skills/<skill>` and root `skills/<skill>`, names both in the
   keep-or-replace stop, and offers to migrate a legacy tree to
   `.agents/skills/` (default: migrate). It never leaves both locations.
6. **D6 — Historical entries stay untouched.** `meta/000` keeps its bare
   `skills/...` paths; they record the state at 2026-10-01.
7. **D7 — Decoupling cleanup.** Remove every reference to a layer owned
   outside this repo — the orientation lint, the conventions lint, and the
   fixed lint template in `docs/markdown-conventions.md` — from the skills'
   reference docs, `journal-lint.py`, the installer, and the README.

## Execution phases

1. **Ignore rules.** Replace `.gitignore` with the scratch, tool, and
   subagent rules. Done.
2. **Installer target.** Point the install list, probe, stop, git hygiene,
   steps 3.3/3.4, and verify at `.agents/skills/<name>`; keep root
   `skills/` as the source. Add legacy handling for a target that keeps its
   skills at root `skills/`. Done.
3. **Text edits.** Update `AGENTS.md`, `README.md`, the contract
   `journals/README.md`, `templates/journals-README.md`, and the
   skill-internal run paths. Depends on 2. Done.
4. **Decoupling.** Remove the outside-layer references. Depends on 3. Done.
5. **Record.** Write this entry. Depends on 1 to 4. Done.
6. **Verify.** Run the journal-craft lint and the tree check. Depends on 5.

## Verification

- `python3 skills/journal-craft/journal-lint.py` exits with 0 errors
  against schema 5.
- Root `skills/journal-craft/` and `skills/ste-writing/` exist;
  `.agents/skills/` is gone; `.agents/work/` remains.
- `git status --porcelain` shows no skill move and no unrelated file.
- Every remaining `.agents/skills/` occurrence names the installer's
  target, a run path an installed skill's user follows, or a cross-skill
  reference resolved at run time. The one `skills/` scope note outside that
  set is `widen-entry-numbers.py`'s.
- `.agents/work/` is ignored.

## Files this entry will touch

- `.gitignore` — replaced.
- `AGENTS.md` — skills location, skill map row, scratch path.
- `README.md` — install table target paths.
- `journals/README.md`, `templates/journals-README.md` — contract and
  template target paths.
- `prompts/journals-init.md` — install list, target, source, and legacy
  handling.
- `skills/journal-craft/SKILL.md`,
  `skills/journal-craft/journal-lint.py`,
  `skills/journal-craft/widen-entry-numbers.py`,
  `skills/journal-craft/references/rules.md`,
  `skills/ste-writing/README.md`,
  `skills/ste-writing/references/rules.md` — run paths and decoupling.
- `journals/meta/001-agents-skills-convention.md` — this entry.

## Risk & rollback

Risk is low. The edits are path substitutions and doc prose. The one care
point is the blanket `.agents/` ignore line: leaving it would silently
gitignore a consumer's committed `.agents/skills/`, so the installer
replaces it. Rollback reverts the working tree with `git checkout` and
`git clean`; no external state changes.

## Non-goals

- No work outside this repository.
- No rewrite of historical entries. `meta/000` keeps its paths.
- No new lint rule or gate for the convention.
- No change to skill behavior. Only path strings and doc prose change.

## Execution log

- 2026-10-02. Replaced `.gitignore` with the scratch, tool, and subagent
  rules.
- Pointed the installer target at `.agents/skills/<name>` in the consuming
  repo and kept root `skills/<name>/` as the source in the journals tree.
- Updated `AGENTS.md`, `README.md`, `journals/README.md`,
  `templates/journals-README.md`, and the skill-internal run paths.
- Added legacy handling to `prompts/journals-init.md`: dual-path probe,
  keep-or-replace that names both paths, migrate-on-legacy default, the
  ignore-line replacement rule, and the `.agents/skills/` creation step.
- Kept the skills at root `skills/`. Left `journals/meta/000-succession.md`
  untouched.
- Decoupling: dropped the borrowed ignore paths and every reference to a
  concept owned outside this repo — from `.gitignore`, `README.md`,
  `journals/README.md`, `prompts/journals-init.md`, the two skills'
  `references/rules.md`, `journal-lint.py`, and the entry itself.
- Wrote this entry.
- Verification (conductor, 2026-10-02): `python3
  skills/journal-craft/journal-lint.py` reports 0 errors, 0 notes. Root
  `skills/journal-craft/` and `skills/ste-writing/` exist; `.agents/skills/`
  is gone; `.agents/work/` remains. `git status --porcelain` shows the
  edited files and this entry, and no unrelated file. `.agents/work/` is
  ignored.
