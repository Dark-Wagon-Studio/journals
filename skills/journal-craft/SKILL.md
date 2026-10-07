---
name: journal-craft
description: Write and check journal entries against schema 5 - the entry schema line, qualified decision IDs, status grammar, dependency and supersession edges, schema resolution, ruling receipts. Use when materializing a journal entry, editing one, checking entries with the lint, or citing a decision.
---

# journal-craft

Journal entries follow the schema in the repo's `journals/README.md`. This
skill writes entries that comply and checks entries that exist. The check is a
lint. It reports claims that do not resolve. It never rewrites, scores, or
gates.

## Writing rules (schema 5)

- Filename: `<NNN>-<slug>.md`. Numbering starts at `000` in each directory.
- Front matter, in order:
  1. `# Journal <area>/<NNN> — <one-line description>`
  2. `Status: <primary>[, <modifier>[, ...]].` Primary is one of Materialized,
     Decided, Executed. Modifiers come from the base set (Provisional,
     On hold, Superseded by `<area>/<NNN>`) or the repo's declared
     `Modifiers:` line in `journals/README.md`.
  3. `Date: <YYYY-MM-DD>. Depends on: <area>/<NNN>, <area>/<NNN>.` Use
     `Depends on: none.` when the entry stands alone.
  4. `Schema: <N>.` The schema you write the entry under, on the line
     directly after the `Date:` line. Read the highest adopted version from
     the ledger in `journals/README.md`. A new entry carries this line before
     it lands. An entry already in the record never gains one.
- Ruling receipts: when a section rests on what the user said in session,
  quote the words next to the claim. Quote the key part inline, in
  quotation marks, or set the whole ruling out as a quote line with its
  date. The form is the author's choice. The attribution names the
  speaker, by whatever name the author knows them. The git identity is
  one such name. `the user` stays the default form. Quote only words
  still present, verbatim, in the session context. Never reconstruct a
  quote. Capture receipts while you draft: the plan stage holds the words
  at their most recoverable, and materialization copies them in.
- Decisions: number every item in `## Decisions` as
  `1. **D1 — short name.** The decision sentence.` Numbers run from 1 inside
  the entry. Drop the section when no cross-cutting choice needs recording.
- Citation grammar: `<area>/<NNN> §<k>` for a section, `<area>/<NNN> D<k>` for a
  decision. Every citation must resolve: the entry, and the decision when the
  citation names one. Never cite a bare ID. The entry qualifies it. A bare ID
  in the entry that defines it reads as that entry's own decision; any other
  bare ID is a lint note. When a directory holds two entries with one number,
  a citation with no slug is ambiguous and reports as an error at schema
  4 or higher; carry the
  slug — `<area>/<NNN>-<slug>` — to name one of them. The `Citations:` line
  in `journals/README.md` declares extra citation shapes. Declared shapes
  are shape-checked, not resolved. An external citation
  `ext:<source>/<area>/<NNN>` is recognized and never resolved.

## Checking

Run `python3 .agents/skills/journal-craft/journal-lint.py` from the repo root before
landing an entry. The report prints error lines and a summary line carrying
both counts; `--notes` lists the note lines. Fix every error. Notes on legacy
entries are information, not work.

## Schema resolution

`journals/README.md` closes with a ledger, one line per adopted schema:

    Schema: 1. Adopted: 2026-09-18.
    Schema: 2. Adopted: 2026-09-20.
    Schema: 3. Adopted: 2026-09-24.
    Schema: 4. Adopted: 2026-09-25.
    Schema: 5. Adopted: 2026-09-27.

An entry resolves to a schema in three steps. First, its own `Schema:` line,
when it carries one. Second, the ledger line with the latest adoption date on
or before the entry date. Third, legacy.

The lint reports every finding on a legacy entry as a note. Never rewrite a
legacy entry to satisfy the schema. Never add a `Schema:` line to an entry
already in the record. The line records the schema the author wrote under.
Adding one later would make the record claim something that did not happen.
An entry you are drafting is not yet in the record: give it the line before
you land it, whatever the lint said about the file on disk.
