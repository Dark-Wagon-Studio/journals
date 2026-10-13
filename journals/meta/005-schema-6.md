# Journal meta/005 — schema 6: the Rulings kind, decision-level supersession, and cross-repo citation rules

Status: Materialized.
Date: 2026-10-13. Depends on: none.
Schema: 6.

## Goal

Adopt schema 6 in this repo. The bump names the decided/verdict entry kind,
gives partial supersession a grammar, pins the legacy class rule, and writes
the two cross-repo citation rules into the contract. The lint learns all of
it with byte-stable D-regexes, because a downstream indexer imports the
grammar.

Receipts: recorded as a restatement. The session's verbatim ask lives in the
siege scratch. The user ruled: the five harvest learnings land as schema 6,
the Rulings kind, the label-letter namespace, push all four repos, sync the
contract bodies, and the qudy citation repair rides the workshop phase. The
decisions below state the ruling.

## Current state (evidence, verified 2026-10-13)

- The contract sits at schema 5. The ledger holds two lines: 4 adopted
  2026-09-30, and 5 adopted 2026-10-01.
- `skills/journal-craft/journal-lint.py` holds `SCHEMA_MAX = 5`. The index
  walk reads `## Decisions` only.
- The schema-5 citation grammar is imported downstream. Monsoon's
  `corpus.py` reads the decision item regex, and this lint's own J10 reads
  group 4 of the decision citation regex. The bytes of every D-regex are the
  compatibility surface.
- Five repos paid for the same five missing concepts. The harvest digest in
  the siege scratch records each payment with its evidence.

## Gap inventory

| Gap | Severity | Dimension |
| --- | --- | --- |
| Rulings have no sanctioned section, so entries improvised headings. `ext:workshop/qudy/010` broke its own citations, and `ext:yard/yard/020`'s ruling items stay unindexed | major | contract |
| Partial supersession is unspeakable at the status line: `ext:yard/yard/006` and `ext:rook/meta/009` record it in body text, outside the lint's reach | major | contract |
| Legacy class policy is folklore. Infra notes every finding on a legacy entry. Monsoon's schema-1 entries drew 59 errors in one cleanup round | major | contract |
| `ext:rook/meta/002` claimed `ext:dark-wagon-studio/meta/004` as a commit authorizer, and no rule rejected it | medium | contract |
| `ext:dws/stack/001` rests on a retired foreign decision with no local re-decision rule | medium | contract |

## Decisions

Each item records a session ruling. The receipts block above states the
rulings as a restatement, not a quote.

1. **D1 — the Rulings kind, namespace by label letter.** An entry may carry
   a `## Rulings` section with items `1. **R1 — short name.**`, numbered
   from 1 inside the section. The item's own label letter names its
   namespace, wherever the item sits: a `**D4 —` item under Rulings stays a
   D-item. The heading is the sanctioned home for new R-items, never an
   override. Citations gain `<area>/<NNN> R<k>`, resolved against the
   rulings index. A bare `R<k>` stays unchecked.
2. **D2 — decision-level supersession.** The status modifier extends:
   `Superseded by <area>/<NNN> D<k>`, or `R<k>`, is legal, and the lint
   resolves the target item. The README notes that the superseding entry
   need not be Executed: a record-only entry that exists to supersede is
   legal. The note is contract text, not a new primary state.
3. **D3 — ruling receipts ratified by reference.** The README's Ruling
   receipts note already carries the form, `> "<words>" — the user, <date>`,
   and the restatement form for a ruling that verbatim quoting would
   breach. This entry ratifies the block by reference. The block itself does
   not change.
4. **D4 — the legacy class table pinned.** rules.md J08 and J09 and the lint
   docstring state the table. An entry predating the ledger's first adoption
   date is legacy. Every finding on a legacy entry is a note, never an
   error. An entry resolving to a declared schema uses that schema's
   classes. No one rewrites a landed entry to satisfy a schema.
5. **D5 — the two cross-repo citation rules.** The README's citation
   section states both. An external citation `ext:<source>/<area>/<NNN>` is
   provenance, never authorization: a commit's authorizing entry is local to
   the repo that commits. When another repo's record supersedes a decision
   this repo's work rests on, the dependent work re-decides locally before
   it executes. A foreign supersession never flips a local status line.

## Execution phases

1. **Lint.** Bump `SCHEMA_MAX` to 6. Update the docstring rule table and
   import list. Add the four regexes and the shared section walk. Extend
   J03, J05, and J10. Add `build_rulings_index()`. Done.
2. **rules.md.** J03, J05, J08/J09, J10. Done.
3. **SKILL.md.** The three bumps: the description, the writing-rules
   heading, the example ledger. Done.
4. **README.** The ruling citation and the label-letter rule. The two
   cross-repo rules. The `Superseded by` bullet. `## Rulings` in the entry
   format. The Notes bullet. The ledger append. Done.
5. **Template.** The README body with one placeholder ledger line. Done.
6. **This entry.**
7. **Validation.** The lint run, the template diff, the symbol grep.
8. **Land.** One commit cites this entry. Push to `origin main`.

## Verification

- `uv run skills/journal-craft/journal-lint.py` exits 0 on this tree.
- The four new symbols are present: `RULINGS_HEADING_RE`, `SCHEMA_MAX = 6`,
  `RULING_ITEM_RE`, `SUPERSEDED_DECISION_RE`.
- The template diff shows only the ledger block: the template holds
  `Schema: 6. Adopted: <YYYY-MM-DD>.` where the README holds the three
  adopted lines.
- No D-regex gains a byte: the diff touches no line that defines
  `DECISIONS_HEADING_RE`, `DECISION_ITEM_RE`, `CITATION_DECISION_RE`,
  `AREA_REF_RE`, `SUPERSEDED_RE`, `BARE_DECISION_RE`, or `entry_key()`.
- `git status` is clean after the commit.

## Files this entry will touch

- `skills/journal-craft/journal-lint.py` — the schema-6 grammar and checks.
- `skills/journal-craft/references/rules.md` — J03, J05, J08/J09, J10.
- `skills/journal-craft/SKILL.md` — the three bumps.
- `journals/README.md` — the contract text and the ledger.
- `templates/journals-README.md` — the body sync.
- `journals/meta/005-schema-6.md` — this entry.

## Risk & rollback

The risk is an unannounced importer of a new surface: a tool that reads a
capture group the R mirrors add. The additive design keeps every D-regex
byte-identical, so the known importer holds by construction. A `git revert`
of the landing commit restores schema 5. The ledger line leaves with it.

## Non-goals

- Schema-7 items: grammar-as-API versioning machinery, and the
  execution-permission gate text.
- Downstream repos. Yard, monsoon, and the workshop refresh their pins in
  their own entries.
- Migrating `ext:yard/yard/020`'s bold-lead improvisation. It stays
  unindexed, and the siege report names it.
- Rewriting any landed entry.

## Execution log

- 2026-10-13T08:22:21+00:00 gate: step "S1: upstream lint green on schema-6 tree" green — uv run skills/journal-craft/journal-lint.py (exit 0).

- 2026-10-13T08:22:26+00:00 gate: step "S1: template mirrors README except the ledger placeholder" green — bash -c diff templates/journals-README.md journals/README.md | grep -c "^[<>]" | grep -q "^4$" (exit 0).
