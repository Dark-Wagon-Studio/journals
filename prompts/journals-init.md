# Initialize the journal convention

These instructions run inside a repository that needs the journal
convention. The journals tree (this repo, cloned to a temporary directory)
is the source for the template and the skills. Reference that clone root as
the journals tree.

This prompt installs the journal convention only: the contract, two skills,
and the git hygiene. It does not install a repo standard — no `AGENTS.md`
planning sections, no docs contract, no orientation, no conventions lint.
Those belong to a wider layer, and a separate installer brings them.

The install always writes:

- `journals/README.md` — the planning contract (layout, commits, status
  grammar, workflow, entry format).
- `skills/journal-craft/` — copied from the journals tree.
- `skills/ste-writing/` — copied from the journals tree.
- `.gitignore` coverage for `.agents/` and `**/.pi-subagents/*`, and a
  `.agents/` scratch directory with `.gitkeep` in it.

Record the install at:

- `journals/<area>/<NNN>-journals-install.md` — written after the work with
  `Status: Executed.` Records the install and any decision or fallback
  taken. The area is the target's choice — see the Phase 2 record-area
  gate. A new area starts at `000`. An existing area takes its next free
  number.

## Authorization and scope

The user's invocation of the installer is the explicit instruction to
execute the install. The no-same-session-execution gate does not block this
install. The record entry is written after the work as a record, not before
it as a plan. The invocation authorizes the install and nothing else — no
code changes, no commits, no other files.

Write every generated file in the ste-writing style: active voice, short
sentences, one name for one thing.

## Phase 1 — Probe

Gather these facts in one pass before writing anything:

- Is this a git work tree? (`git rev-parse --is-inside-work-tree`)
- Does `journals/` exist?
- Does `journals/README.md` carry a `Schema:` ledger line or a
  `Modifiers:` line? (A convention may already be installed — Phase 2 stop
  conditions already govern this. Step 3.1 branches on this fact: it never
  copies the template over a file that has either line.)
- The last date in any `Schema:` ledger the file carries. Step 3.1 dates
  its adoption after it.
- The newest `Date:` among entries that carry no `Schema:` line. Step 3.1
  dates its adoption after it too.
- The `journals/` area directories.
- Any prior journals install or reconcile entry, with its path. The
  record-area gate drafts its default from it.
- Do `AGENTS.md` or `CLAUDE.md` exist? Do they reference a planning or
  journaling workflow? (Read-only fact. This install never edits them.)
- Does `.gitignore` exist? Does it cover `.agents/` and
  `**/.pi-subagents/*`?
- Does `skills/` exist? Do `skills/ste-writing` or `skills/journal-craft`
  exist?
- Today's date.

## Phase 2 — Stop conditions, then state and proceed

Stop and ask before writing anything if:

1. `journals/` exists — a convention may already be installed.
2. An existing `AGENTS.md` or `CLAUDE.md` defines a planning or journaling
   workflow — do not overwrite a convention. Ask whether to proceed with
   the file set above, since this install does not edit those files.
3. This is not a git work tree — ask whether to proceed without the git
   hygiene steps.
4. `skills/ste-writing` or `skills/journal-craft` already exists — ask
   whether to keep or replace it.

### Record-area gate

The install record lands under a journal area the target owns, not a fixed
one. At this confirm point ask one bounded question, unless the invocation
already decided it:

Record the install under which journal area? Default: <draft>.

The draft rule: the area of a prior journals install entry when one exists,
else `meta`. The answer names an area, one path component — not a line. An
unclear answer takes the default. Carry the choice to Phase 4. A new area
starts at `000`. An existing area takes its next free number.

If a stop condition above holds, fold this question into that stop.

If no stop condition holds, state the file list in one short block and
proceed in the same turn. The invocation is the confirmation. Do not wait
for another.

## Phase 3 — Install

### 3.1 Write `journals/README.md`

**Check the probe first.** When `journals/README.md` does not exist, copy
`templates/journals-README.md` from the journals tree to
`journals/README.md` and fill the ledger placeholder `<YYYY-MM-DD>` with
the adoption date computed below.

When `journals/README.md` already exists and the probe found a `Schema:`
ledger line or a `Modifiers:` line in it, **do not copy the template over
it.** Stop. This installer carries no upgrade path. Losing the ledger makes
the entire existing corpus legacy, so every error-level finding on it
silently becomes an advisory note and the lint starts exiting 0. Losing the
`Modifiers:` line invalidates every status line that used a declared
modifier. Both losses are invisible in the lint output.

When `journals/README.md` exists with neither line, it predates the schema.
Copy the template over it, and say in the final summary that you replaced a
pre-schema contract file.

The adoption date grandfathers any pre-existing corpus. Take the latest of
three dates: today, one day after the newest entry that carries no
`Schema:` line, and one day after the last date in any ledger the probe
found. The second rule stops the date from landing on an entry already in
the record, which would demand a `Schema:` line that nobody may add. The
third keeps the ledger ascending, which the lint requires.

### 3.2 Git hygiene

Make `.gitignore` cover `.agents/` and `**/.pi-subagents/*`. Create
`.gitignore` if it does not exist. When it exists without the lines, append
them. Create `.agents/` with an empty `.gitkeep` in it.

### 3.3 Install the journal-craft skill

Copy `skills/journal-craft/` from the journals tree into
`skills/journal-craft/`. Drop any `__pycache__` in the copy. If `skills/`
already holds other skills, leave them alone. If the skill is missing from
the journals tree, report it and continue.

### 3.4 Install the ste-writing skill

Copy `skills/ste-writing/` from the journals tree into
`skills/ste-writing/`. If `skills/` already holds other skills, leave them
alone. If the skill is missing from the journals tree, report it and
continue — the contract's _Style_ section already carries the by-hand rule.

## Phase 4 — Record

Write `journals/<area>/<NNN>-journals-install.md` now, after the work. Use
the area and the number the Phase 2 record-area gate chose. Use the entry
format from the README you just wrote, including the `Schema:` line. Read
the version from the ledger in the README you just wrote.
`Status: Executed.` — bare, no date in the status line. Fill every section
from the probe and the install that just ran. Adjust the gap rows to what
the probe actually found. Drop the _Decisions_ section unless a real choice
was made: the record-area choice, a keep-or-replace resolution, or a
fallback taken. The execution log names what landed, any fallbacks, and the
verification results.

Also record the schema adoption date from step 3.1 and why that date was
chosen when it is not today.

## Phase 5 — Verify and present

Check, then report:

- `journals/README.md` exists and carries the two-tier status grammar.
- `.gitignore` covers both patterns. `.agents/.gitkeep` exists.
- `skills/journal-craft/SKILL.md` exists, with `journal-lint.py`.
- `skills/ste-writing/SKILL.md` exists.
- The install record exists at the chosen path with `Status: Executed.` and
  a `Schema:` line that matches the contract's ledger.
- `python3 skills/journal-craft/journal-lint.py` exits with 0 errors.

Do not commit. The install stays in the working tree. The user commits.
