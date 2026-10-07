# Journal lint rules

Rule definitions for `journal-lint.py`, one section per rule in a fixed
template. The basis names the claim
the diagnostic may make: consistency states a mechanically established fact,
convention states a breach of a content contract, and heuristic offers an
observed feature as a conditional suggestion. A note never claims more than
its basis supports.

The lint reads the `journals/` tree and `journals/README.md`. It reports
claims that do not resolve. It never writes, scores, ranks, or gates.
Error findings print one per line as
`<path>:<line> <class> <code> <message>` by default; note findings print
only with `--notes`. Errors exit 1, the schema notice exits 2, notes exit 0.
Every finding on a legacy entry is a note. An entry resolves to a schema in
three steps. Step one: its own `Schema:` line, when it carries one. Step
two: the ledger line with the latest adoption date on or before the entry
date. Step three: legacy. `SCHEMA_MAX` is a constant in the script: the
highest schema this
lint understands, not the only one a repo may run.

## J01 — filenames and numbering

### What it checks

Each entry filename matches `<NNN>-<slug>.md` with three digits. In each
directory the lowest entry number is 000. After the first entry the numbers
run without gaps: a gap names the missing numbers and anchors at the file
that follows it. Two entries in one directory that share a number are a
duplicate: one note names the directory, the number, and the count, and
anchors at the second file in walk order.

### Basis

Convention. The diagnostic claims a breach of the naming and numbering
contract. The gap message states a fact the lint establishes by sort —
which numbers are absent — and reports it as a note.

### Why it matters

The number is the stable half of every citation. A wrong shape breaks
citation resolution, and a gap invites two files to claim one number later.
A duplicate is the gap realized: a short reference to a shared number
resolves to none of the entries, so the lint names the collision even
though the contract lets existing duplicates stay.

### Example

A file named `2-plan.md` in `journals/meta/`. Two entries in
`journals/combat/` numbered `002`: `002-heal-priority.md` and
`002-skill-audit.md`.

### Instead

The same file named `002-plan.md`. The duplicate stays, per the contract,
and a citation that means one of the two carries its slug:
`combat/002-heal-priority`.

### Exceptions

`README.md` and anything under a dot-directory is not an entry. A file that
declares a schema above `SCHEMA_MAX` keeps its place in the number sequence,
collects no J01 finding of its own, and never causes a sibling a false gap.
A filename mismatch is a note on a legacy entry, an error otherwise.

### Inputs

The entries discovered under `journals/`, grouped per directory.

### Configuration

None. Three digits, the 000 floor, and the gap report are fixed.

## J02 — heading

### What it checks

Line 1 parses as `# Journal <area>/<NNN> — <description>`, with the em dash.
The `<area>` equals the entry's directory under `journals/`, and `<NNN>`
equals the number in the filename. A heading that parses over a filename
without the `<NNN>-` prefix reports that shape breach on its own.

### Basis

Consistency. The diagnostic claims a mechanically established fact: the
heading does not parse, or the heading and the entry path disagree.

### Why it matters

The heading is the display form of the citation target. A heading that
disagrees with the path makes every reference to the entry ambiguous.

### Example

    # Journal meta/002 — the schema ledger

as line 1 of `journals/meta/003-schema-ledger.md`.

### Instead

    # Journal meta/003 — the schema ledger

### Exceptions

The description may hold any text; only the area and the number compare. An
unreadable file — not valid UTF-8, or unreadable at all — reports one J02
finding at line 1 and runs no further check.

### Inputs

Line 1 of the entry, and the entry path relative to `journals/`.

### Configuration

None.

## J03 — status grammar

### What it checks

The second non-empty line of the file is the status line. It parses as
`Status: <items>.` with the trailing period. The first item is the primary
state: Materialized, Decided, or Executed. Each later item is a modifier:
Provisional, On hold, a name declared in `journals/README.md`, or
`Superseded by <area>/<NNN>` whose target resolves to an entry. A
supersession target whose bare number names more than one entry in its
directory is ambiguous and reports; the target may carry `-<slug>` to name
one of them. A primary state in a later position reports.

### Basis

Convention. The diagnostic claims a breach of the status grammar. The
supersession finding states a fact: the target is absent from the entry
index.

### Why it matters

The status line is what the authority procedure reads first. An unknown
state or an unresolvable supersession target sends the reader to nothing.

### Example

    Status: Executed, Approved.

### Instead

    Status: Executed.

### Exceptions

An entry with fewer than two non-empty lines reports one missing-status
finding. An empty item between commas reports as a parse failure. The
supersession target must parse as `<area>/<NNN>`, with an optional
`-<slug>`; anything else reports as an unknown modifier.

### Inputs

The entry lines, the declared modifiers from `journals/README.md`, and the
entry index built from the `journals/` tree.

### Configuration

The `Modifiers:` line in `journals/README.md`. A column-zero line
`Modifiers: <name>, <name>.` declares extra legal modifiers for every
entry. An indented line is documentation, not a declaration.

## J04 — date and dependencies

### What it checks

A `Date:` line exists. It parses as
`Date: <YYYY-MM-DD>. Depends on: <targets>.` The date is a valid ISO 8601
calendar day. Each dependency is `<area>/<NNN>`, with an optional
`-<slug>`, and resolves to an entry, or the whole field reads `none`. A
dependency whose bare number names more than one entry in its directory is
ambiguous and reports.

### Basis

Consistency. The diagnostic claims mechanical facts: the line does not
parse, the date names no calendar day, or a dependency target is absent
from the tree.

### Why it matters

The date drives schema resolution and legacy status. A dependency edge that
resolves to nothing hides the entry's context.

### Example

    Date: 2026-13-01. Depends on: meta/001.

### Instead

    Date: 2026-01-13. Depends on: meta/001.

### Exceptions

`none` is the legal empty form. The first line that starts with `Date:` is
the date line; later ones go unread. A line that fails to parse reports
once, and the dependency checks do not run on it.

### Inputs

The `Date:` line, and the entry index built from the `journals/` tree. The
parsed date decides legacy status and schema resolution for the entry.

### Configuration

None.

## J05 — decision numbering

### What it checks

In the `## Decisions` section, every numbered item opens with
`N. **D<N> — <name>`. The check reads the head through the first
non-space of the name, so an unclosed bold phrase or a missing final
period does not report. Item numbers run from 1
with no skips, and item `N` defines decision `D<N>`. A line that opens a
bold phrase, with or without a bullet, but carries no item number is an
unnumbered decision item and reports.

### Basis

Convention. The diagnostic claims a breach of the decision-item grammar.
The sequence findings state mechanical facts about item order.

### Why it matters

Decision IDs are citation targets. A number out of sequence makes a
`D<k>` citation point at the wrong decision.

### Example

    2. **D3 — scope.** The lint owns the check.

### Instead

    2. **D2 — scope.** The lint owns the check.

### Exceptions

Blank lines never compare. On a legacy entry the unnumbered findings
collapse into one note on the first item. A bold phrase in ordinary prose
never reports; only a line that opens with one does.

### Inputs

The lines from the `## Decisions` heading to the next `## ` heading.

### Configuration

None.

## J06 — path depth

### What it checks

The entry path holds two or three components under `journals/`:
`<area>/<NNN>-<slug>.md`, or `<area>/<line>/<NNN>-<slug>.md`.

### Basis

Consistency. The diagnostic claims a mechanically established fact about
the path component count.

### Why it matters

One line level under an area keeps every `<area>/<NNN>` citation
resolvable from the directory layout alone.

### Example

    journals/meta/archive/2026/002-plan.md

### Instead

    journals/meta/archive/002-plan.md

### Exceptions

None. Any other depth reports once, at line 1.

### Inputs

The entry path relative to `journals/`.

### Configuration

None.

## J07 — dates in prose

### What it checks

Every date-shaped token outside the exemptions is a valid ISO 8601 date. A
`YYYY-MM-DD` token that names no calendar day reports. Non-ISO shapes
report: slash forms (`2026/1/5`, `1/5/2026`), dotted day.month.year forms,
and month-name forms (`Jan 5, 2026`).

### Basis

Consistency. The diagnostic claims a mechanically established fact about
the token.

### Why it matters

One date format sorts, diffs, and greps. A prose date reads differently in
every locale.

### Example

    Approved on 5 Jan 2026.

### Instead

    Approved on 2026-01-05.

### Exceptions

The `Date:` line is J04's; this check skips it. Quote lines never report:
they carry verbatim session speech, and a date inside one is evidence, not
a contract date. The dotted form bounds the day at 31 and the month at 12,
so a version-like token such as `3.14.1592` never matches.

### Inputs

The entry lines, minus the `Date:` line and the quote lines.

### Configuration

None.

## J08 — the schema ledger

### What it checks

`journals/README.md` exists, is readable, and holds at least one
`Schema: N. Adopted: YYYY-MM-DD.` line. Each adoption date is a valid ISO
8601 date. Versions ascend with no repeats, and adoption dates ascend
strictly: an equal or earlier date reports.

### Basis

Consistency. The diagnostic claims mechanical facts about the ledger
lines.

### Why it matters

The ledger is the resolution table for every entry. A repeated or
descending line makes schema resolution untrustworthy for the whole tree.

### Example

    Schema: 5. Adopted: 2026-09-27.
    Schema: 4. Adopted: 2026-09-30.

### Instead

    Schema: 4. Adopted: 2026-09-27.
    Schema: 5. Adopted: 2026-09-30.

### Exceptions

A missing or unreadable README reports once, at line 0. A file with no
ledger line reports once. A line whose date fails to parse reports and
stays out of the ascension chain. A ledger whose highest version exceeds
`SCHEMA_MAX` stops the run before any check: one notice line, exit 2.

### Inputs

`journals/README.md`.

### Configuration

None. The ledger is itself the repo's declaration; this check audits it.

## J09 — schema declaration

### What it checks

The front matter declares its schema once, as `Schema: <N>.` with `N` of 1
or higher, on the line directly after the `Date:` line. The declared
version does not exceed the highest adopted version in the ledger. Every
entry that resolves to schema 2 or higher declares one.

### Basis

Consistency. The diagnostic claims mechanical facts about the declaration
and the ledger. The requirement to declare at schema 2 and above is
contract; the rest is measurement.

### Why it matters

The declaration records the schema the author wrote under. A second
declaration, a wrong position, or a version the ledger never adopted makes
the record claim something the record cannot verify.

### Example

    Status: Materialized.
    Date: 2026-10-01. Depends on: none.

    Schema: 5.

### Instead

    Status: Materialized.
    Date: 2026-10-01. Depends on: none.
    Schema: 5.

### Exceptions

A declaration above `SCHEMA_MAX` produces one note, and the entry skips
every remaining check, including J01. An entry with no declaration resolves
through the ledger instead; only an entry that resolves to schema 2 or
higher without one reports. The declaration must sit in the front matter —
the lines before the first `## ` heading or the blank line that closes the
header. A malformed line already carries its own finding. The position
check still runs on it: a line that fails to parse also reports when it
does not sit directly after the Date line.

### Inputs

The front matter of the entry, the position of the `Date:` line, and the
ledger.

### Configuration

`SCHEMA_MAX`, a constant in the script: the highest schema this lint
understands. A repo declares adopted versions in the ledger, never here.

## J10 — citation resolution

### What it checks

Body citations resolve. `<area>/<NNN>` — optional `journals/` prefix, an
optional second area segment, optional `-slug`, optional `.md` — resolves
to an entry. A citation with no slug resolves only when the number names
one entry: a number that two entries in one directory share is ambiguous
and reports instead of resolving, while a slug that matches a claimant
resolves to that claimant. `<area>/<NNN> D<k>`
resolves to a decision defined in that entry. `<area>/<NNN> §<k>` resolves
to the entry; the section number is never checked, because sections are
named, not numbered. Citation areas are letter-led, so a count such as
`31/37` never reads as a citation. An external citation
`ext:<source>/<area>/<NNN>` is recognized: it claims its span, decoration
included, and never resolves.

### Basis

Consistency. The diagnostic claims a mechanical fact: the target is
present in the tree, or absent.

### Why it matters

A citation is a pointer a reader follows. An unresolved one sends the
reader to nothing and hides the entry's basis.

### Example

    Per meta/099, the lint owns the check.

### Instead

    Per meta/002, the lint owns the check.

### Exceptions

Quote lines never report. Decision definitions inside the `## Decisions`
section never report as citations. Text inside inline code spans never
reports, and the span state carries across lines. A declared `Citations:`
shape is recognized and never resolved. An external `ext:` citation never
reports either: the external pattern claims its span ahead of the local
grammar, so no tail of it resolves and its decoration never reads as a
bare decision ID. A bare `D<k>` reports one note when
the entry does not define that decision and the entry resolves to schema 4
or higher; below schema 4 it reports nothing. A miss is an error at schema
4 or higher and a note below. Each match resolves once; external citations
and declared shapes claim their spans first.

### Inputs

The body lines of the entry, external `ext:` citations included, the entry
and decision indexes built from the `journals/` tree, the declared shapes
from `journals/README.md`, and the entry's resolved schema.

### Configuration

The `Citations:` line in `journals/README.md`. A column-zero line
`Citations: <R<k>>, <R<k>>.` declares extra citation shapes; a declared
shape is shape-checked, not resolved, and a token without `<k>` declares
nothing. The schema-4 gate that sets the error class is fixed.
