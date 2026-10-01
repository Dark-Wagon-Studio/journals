#!/usr/bin/env python3
"""journal-lint.py — advisory lint for journal entries under schema 5.

Linter law: this tool reports claims that do not resolve. It never writes
files, generates content, scores, ranks, or gates. Findings print one per
line as `<path>:<line> <class> <code> <message>`, then a summary line.

Exit codes: 1 when errors exist, 2 on a schema-version notice, 0 otherwise.
Notes never fail the run.

Usage (from the repo root):

    python3 skills/journal-craft/journal-lint.py

Inputs: the `journals/` tree and `journals/README.md`. The README carries the
schema ledger (one `Schema: N. Adopted: <date>.` line per adopted schema,
ascending) and the optional `Modifiers:` and `Citations:` lines.

An entry resolves to a schema in three steps: its own `Schema: <N>.` line
when it carries one, otherwise the ledger line with the latest adoption date
on or before the entry date, otherwise legacy. Every check still runs on a
legacy entry, but each finding on it is a note, never an error. Without a
ledger nothing is legacy.

SCHEMA_MAX is the highest schema this lint understands, not the only one. A
schema-1 repo stays fully checked. A ledger above SCHEMA_MAX prints a notice
and exits 2 without running the checks, because no resolution would be
trustworthy. A single entry above SCHEMA_MAX produces one note and no other
finding: the entry skips every check, including the J01 numbering checks that
run outside lint_entry. The run continues and the entry never fails it.

Checks:
  J01  filenames (<NNN>-<slug>.md, three digits), lowest number is 000 per
       directory (error); numbering gaps after the first entry (note)
  J02  heading parses as "# Journal <area>/<NNN> — <description>" and the
       <area>/<NNN> matches the file's directory and filename number
  J03  status line is the second non-empty line; primary from the closed
       set; modifiers base or declared; supersession targets resolve
  J04  date/depends line present and parseable; date is ISO 8601; every
       dependency resolves to an entry; "none" is legal
  J05  every "## Decisions" item matches "N. **DN — name.**", sequential
       from 1; bulleted or bold-led items without that numbering are
       unnumbered decision prose (note on legacy entries)
  J06  entry path nests at most one line level under an area (two or
       three path components under journals/)
  J07  dates are ISO 8601 everywhere they appear (the Date line itself is
       J04's; J07 skips it; quote lines are exempt, because verbatim
       session speech may carry a date the contract did not write)
  J08  journals/README.md carries the schema ledger: at least one
       "Schema: N. Adopted: <date>." line, each with a valid date, versions
       and dates both ascending, no version repeated
  J09  the entry's "Schema: <N>." declaration: it parses, it is declared
       once, its version is 1 or higher, it sits on the line directly after
       the Date line, it does not exceed the highest adopted version, and it
       is present on every entry that resolves to schema 2 or higher. A
       declaration above SCHEMA_MAX is a note and skips the entry
  J10  citations in the entry body resolve: "<area>/<NNN>" (optional
       "journals/" prefix, "-slug", ".md") resolves to an entry and
       "<area>/<NNN> D<k>" to a decision in it; "§<k>" resolves the entry
       only, because sections are named, not numbered. Every citation area
       is letter-led: ratio tokens in evidence prose ("31/37") are counts,
       not citations. Quote lines, inline code spans, and decision
       definitions inside the Decisions section are exempt, and a declared
       "Citations:" shape is recognized but never resolved. An external
       citation "ext:<source>/<area>/<NNN>" (with the same decorations) is
       recognized, claimed ahead of the local grammar, and never resolved.
       A bare "D<k>"
       is a note unless the containing entry defines that decision, and
       reports nothing below schema 4. A miss is an error on schema 4 or
       higher, a note below schema 4. A relative filesystem path that ends
       like an entry citation ("dir/NNN-slug.md") still matches; no such
       token exists outside "journals/" today.

The citation grammar is importable: CITATION_ENTRY_RE, CITATION_DECISION_RE,
CITATION_SECTION_RE, BARE_DECISION_RE, CITATIONS_LINE_RE, and
EXT_CITATION_RE, the (entry, decision) indexes from build_indexes(), and
shape_to_regex() for a declared shape. An entry match captures (area, NNN,
slug); entry_key() reads the three from any citation or area match, and a
decision citation's D<k> is group 4. A downstream indexer imports the
grammar instead of re-deriving it. EXT_CITATION_RE recognizes the external
"ext:" form: it claims the span and resolves nothing.

Deterministic: two runs on the same tree print identical output. Python 3
standard library only; no network.
"""

import re
import sys
from datetime import date
from pathlib import Path

SCHEMA_MAX = 5

PRIMARY_STATES = ("Materialized", "Decided", "Executed")
BASE_MODIFIERS = ("Provisional", "On hold")

ENTRY_FILENAME_RE = re.compile(r"^(\d{3})-(.+)\.md$")
HEADING_RE = re.compile(r"^# Journal (.+)/(\d{3}) — (.+)$")
STATUS_RE = re.compile(r"^Status:\s*(.*?)\s*\.\s*$")
SUPERSEDED_RE = re.compile(r"^Superseded by (.+)$")
# The optional slug keeps a dependency or supersession target able to
# disambiguate a duplicated number; every target valid without one stays
# valid.
AREA_REF_RE = re.compile(
    r"^(.+)/(\d{3})(?:-([A-Za-z0-9][A-Za-z0-9_-]*))?$")
DATE_PREFIX_RE = re.compile(r"^Date:")
DATE_LINE_RE = re.compile(
    r"^Date:\s*(\d{4}-\d{2}-\d{2})\s*\.\s*Depends on:\s*(.*?)\s*\.\s*$")
FOOTER_RE = re.compile(
    r"^\s*Schema:\s*(\d+)\s*\.\s*Adopted:\s*(\d{4}-\d{2}-\d{2})\s*\.\s*$")
# An entry's own declaration. No "Adopted:" part: that belongs to the ledger.
ENTRY_SCHEMA_RE = re.compile(r"^Schema:\s*(\d+)\s*\.\s*$")
# Anchored at column zero: an indented Modifiers line in journals/README.md
# is a documentation example, not a declaration.
MODIFIERS_LINE_RE = re.compile(r"^Modifiers:\s*(.*?)\s*\.?\s*$")
SECTION_HEADING_RE = re.compile(r"^## ")
DECISIONS_HEADING_RE = re.compile(r"^## Decisions\s*$")
NUMBERED_ITEM_RE = re.compile(r"^\s*(\d+)[.)]\s+")
DECISION_ITEM_RE = re.compile(r"^(\d+)[.)]\s+\*\*D(\d+)\s+—\s+\S")
# A line that starts a bold-led item (optionally bulleted) attempts to be a
# decision item; without the "N. " number it is unnumbered decision prose.
# Mid-line "**D<k>" mentions (inline code, citations) are not item starts.
UNNUMBERED_ITEM_RE = re.compile(r"^(?:[-*+]\s+)?\*\*")
ISO_TOKEN_RE = re.compile(r"(?<!\d)(\d{4}-\d{2}-\d{2})(?!\d)")
# Dotted dates read day.month.year; the day and month bounds keep
# version-like tokens (3.14.1592) from matching.
NON_ISO_DATE_RE = re.compile(
    r"\b(\d{4}/\d{1,2}/\d{1,2}"
    r"|\d{1,2}/\d{1,2}/\d{4}"
    r"|(?:0?[1-9]|[12]\d|3[01])\.(?:0?[1-9]|1[0-2])\.\d{4}"
    r"|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.? \d{1,2},? \d{4})\b")

# Citation grammar (schema 4; width three since schema 5). Importable: a
# downstream indexer imports the
# grammar instead of re-deriving it. An entry citation is an optional
# journals/ prefix, one or two area segments, /<NNN>, an optional -slug and
# .md. Every citation area is letter-led: ratio tokens in evidence prose
# ("31/37") are counts, not citations. The lookbehind keeps a filesystem
# path from reading as a citation; the trailing guards keep a longer path or
# a non-.md extension from matching (guards reused from orientation-lint
# REF_RE).
_CITATION_HEAD = r"(?<![\w./-])(?:journals/)?"
_CITATION_AREA = r"([A-Za-z][A-Za-z0-9_-]*(?:/[A-Za-z0-9][A-Za-z0-9_-]*)?)"
_CITATION_ENTRY = r"/(\d{3})(?:-([A-Za-z0-9][A-Za-z0-9_-]*))?(?:\.md)?"
_CITATION_TAIL = r"(?![\w/-])(?!\.[A-Za-z0-9])"
CITATION_ENTRY_RE = re.compile(
    _CITATION_HEAD + _CITATION_AREA + _CITATION_ENTRY + _CITATION_TAIL)
# A decision citation is an entry citation followed on the same line by
# whitespace, then D<k> ("\s+D(\d+)"): a double space or tab still
# composes a decision citation. The entry's slug capture shifts the
# decision group to 4: (area, NNN, slug, k).
CITATION_DECISION_RE = re.compile(
    _CITATION_HEAD + _CITATION_AREA + _CITATION_ENTRY + r"\s+D(\d+)"
    + _CITATION_TAIL)
# A section citation resolves to the entry only: <k> is never validated,
# because sections are named, not numbered. The entry's slug capture
# shifts the section group to 4; no consumer reads it today.
#
# One key for every resolver: area, number, and slug from a citation or
# area-reference match. The slug is None when the reference carries none,
# which is the case that can be ambiguous.
CITATION_SECTION_RE = re.compile(
    _CITATION_HEAD + _CITATION_AREA + _CITATION_ENTRY + r" §(\d+)"
    + _CITATION_TAIL)
# An external citation ("ext:<source>/<area>/<NNN>") claims its whole span
# ahead of the declared shapes and the local grammar. The source name is
# letter-led; the rest is the local area/number/slug shape with its
# optional decorations, under the same tail guards, so a following
# decoration joins the claimed span. The decision decoration keeps the
# local grammar's "\s+"; the section decoration keeps its literal space.
# A claimed span is collected with kind "external" and resolves nothing.
EXT_CITATION_RE = re.compile(
    r"(?<![\w./-])ext:[A-Za-z][A-Za-z0-9_-]*"
    + "/" + _CITATION_AREA + _CITATION_ENTRY
    + r"(?:\s+D\d+| §\d+)?"
    + _CITATION_TAIL)
# A bare decision ID in prose, word-bounded. The lookbehind also excludes a
# bold lead, so a "**D1" definition head never matches; "D<k>" template text
# has a letter where a digit is required.
BARE_DECISION_RE = re.compile(r"(?<![\w*])D(\d+)(?!\w)")
# A column-zero "Citations:" line in journals/README.md, anchored exactly
# like MODIFIERS_LINE_RE: an indented line is documentation, not a
# declaration.
CITATIONS_LINE_RE = re.compile(r"^Citations:\s*(.*?)\s*\.?\s*$")


def entry_key(m):
    """Return (area, NNN, slug) from a citation or area-reference match.

    Reads the three groups every resolver needs: the area and number
    groups all the grammars share, and the slug group the entry and
    area-reference grammars capture. The slug is None when the reference
    carries none.
    """
    return m.group(1), m.group(2), m.group(3)

EXCERPT_MAX = 64


def excerpt(line):
    s = line.strip()
    if len(s) > EXCERPT_MAX:
        return s[:EXCERPT_MAX - 3] + "..."
    return s


def iso_date(s):
    """Return a datetime.date for a strict YYYY-MM-DD string, else None."""
    if not ISO_TOKEN_RE.fullmatch(s):
        return None
    try:
        return date(int(s[0:4]), int(s[5:7]), int(s[8:10]))
    except ValueError:
        return None


def display_dir(rel_dir_parts):
    return "journals/" + "/".join(rel_dir_parts) if rel_dir_parts else "journals"


def shape_to_regex(shape):
    """Compile one declared citation shape ("R<k>") to a bounded regex.

    Escapes the literal text and replaces <k> with \\d+. The citation
    boundary guards make the regex match a whole prose token, never a
    fragment of one.
    """
    body = re.escape(shape).replace(re.escape("<k>"), r"\d+")
    return re.compile(r"(?<![\w./-])" + body + r"(?![\w/-])(?!\.[A-Za-z0-9])")


def discover_entries(journals):
    if not journals.is_dir():
        return []
    entries = []
    for p in sorted(journals.rglob("*.md")):
        if p.name == "README.md" or not p.is_file():
            continue
        rel = p.relative_to(journals)
        if any(part.startswith(".") for part in rel.parts):
            continue
        entries.append((p, rel))
    return entries


def lint_readme(readme):
    """Parse journals/README.md.

    Returns (findings, declared, declared_shapes, ledger, notice). The
    ledger holds one (version, date, iso, lineno) tuple per adopted schema,
    in file order. Declared shapes are the "Citations:" tokens that contain
    "<k>"; a token without "<k>" declares nothing matchable and is ignored.
    The notice is set only when the ledger's highest version is newer than
    SCHEMA_MAX.
    """
    findings = []
    declared = []
    declared_shapes = []
    ledger = []
    notice = None

    def j08(lineno, msg):
        findings.append({"path": "journals/README.md", "line": lineno,
                         "code": "J08", "cls": "error", "msg": msg})

    if not readme.is_file():
        j08(0, "journals/README.md not found: no schema ledger "
               '("Schema: N. Adopted: YYYY-MM-DD."), adoption date, or '
               "declared modifiers")
        return findings, declared, declared_shapes, ledger, notice
    try:
        text = readme.read_text(encoding="utf-8")
    except OSError:
        j08(0, "journals/README.md cannot be read; schema ledger and "
               "declared modifiers unchecked")
        return findings, declared, declared_shapes, ledger, notice

    raw = []
    for lineno, line in enumerate(text.splitlines(), 1):
        fm = FOOTER_RE.match(line)
        if fm:
            raw.append((int(fm.group(1)), fm.group(2), lineno))
        mm = MODIFIERS_LINE_RE.match(line)
        if mm:
            for name in mm.group(1).split(","):
                name = name.strip()
                if name and name not in declared:
                    declared.append(name)
        cm = CITATIONS_LINE_RE.match(line)
        if cm:
            for shape in cm.group(1).split(","):
                shape = shape.strip()
                if shape and "<k>" in shape and shape not in declared_shapes:
                    declared_shapes.append(shape)

    if not raw:
        j08(0, 'schema ledger missing or malformed (expected at least one '
               '"Schema: N. Adopted: YYYY-MM-DD." line)')
        return findings, declared, declared_shapes, ledger, notice

    # A ledger this lint cannot read makes every resolution untrustworthy, so
    # the whole run stops. One entry above SCHEMA_MAX is a note on that entry.
    highest = max(v for v, _iso, _ln in raw)
    if highest > SCHEMA_MAX:
        lineno = next(ln for v, _iso, ln in raw if v == highest)
        notice = (f"notice: journals/README.md:{lineno} declares schema "
                  f"{highest}; this lint understands schema {SCHEMA_MAX}")
        return findings, declared, declared_shapes, ledger, notice

    prev = None
    for version, iso, lineno in raw:
        adopted = iso_date(iso)
        if adopted is None:
            j08(lineno, f"schema ledger adoption date is not a valid ISO 8601 "
                        f"date: {iso}")
            continue
        if prev is not None:
            prev_version, prev_date = prev
            if version == prev_version:
                j08(lineno, f"schema ledger repeats schema {version}")
            elif version < prev_version:
                j08(lineno, f"schema ledger versions do not ascend: "
                            f"{version} follows {prev_version}")
            if adopted <= prev_date:
                j08(lineno, f"schema ledger dates do not ascend: {iso} is not "
                            f"after {prev_date.isoformat()}")
        ledger.append((version, adopted, iso, lineno))
        prev = (version, adopted)
    return findings, declared, declared_shapes, ledger, notice


def front_matter_end(lines):
    """Return the index where the front-matter block ends and the body starts.

    The block ends at the first "## " heading or at the blank line that
    closes the header, whichever comes first. An entry with no section
    heading therefore cannot drag prose into the block.
    """
    in_block = False
    for i, line in enumerate(lines):
        if SECTION_HEADING_RE.match(line):
            return i
        if i > 0 and line.strip():
            in_block = True
        elif in_block and not line.strip():
            return i
    return len(lines)


def read_entry_schema(lines):
    """Read an entry's "Schema: <N>." declaration from its front matter.

    The front matter ends where front_matter_end says it ends. Returns
    (lineno, version, findings). The findings are (code, lineno, msg) tuples
    the caller emits once it knows whether the entry is legacy.
    """
    found = []
    for i, line in enumerate(lines[:front_matter_end(lines)]):
        if line.startswith("Schema:"):
            found.append((i + 1, line))
    if not found:
        return None, None, []
    findings = [("J09", lineno, "entry declares its schema more than once")
                for lineno, _line in found[1:]]
    lineno, line = found[0]
    m = ENTRY_SCHEMA_RE.match(line)
    if not m:
        findings.append(("J09", lineno,
                         'schema line does not parse as "Schema: <N>.": '
                         f"{excerpt(line)}"))
        return lineno, None, findings
    version = int(m.group(1))
    if version < 1:
        findings.append(("J09", lineno,
                         f"schema version must be 1 or higher: {version}"))
        return lineno, None, findings
    return lineno, version, findings


def resolve_schema(ledger, entry_date, entry_schema):
    """Resolve one entry to a schema. Returns (schema, legacy).

    Three steps: the entry's own declaration, then the ledger line with the
    latest adoption date on or before the entry date, then legacy. An
    undated entry and an empty ledger both resolve to (None, False): J04 and
    J08 already report those, and nothing is grandfathered on a guess.
    """
    if entry_schema is not None:
        return entry_schema, False
    if not ledger or entry_date is None:
        return None, False
    applicable = [(v, adopted) for v, adopted, _iso, _ln in ledger
                  if adopted <= entry_date]
    if applicable:
        return max(applicable, key=lambda va: va[1])[0], False
    return None, True


def collect_citations(line, in_code_span, declared_res):
    """Collect citation matches on one line, outside inline code spans.

    Each backtick on a scanned line toggles the span, whose state the
    caller carries across scanned lines; text inside a span is hidden,
    including whole lines of a
    multi-line span. Returns (start, end, kind, m) tuples with offsets into
    the line. One citation resolves once: a match overlapping an already
    claimed span is dropped. External citations claim first, then declared
    shapes, then decision, section, entry, and bare decision citations.
    """
    matches = []
    claimed = []

    def take(text, offset, regex, kind):
        for m in regex.finditer(text):
            s, e = offset + m.start(), offset + m.end()
            if any(s < ce and cs < e for cs, ce in claimed):
                continue
            claimed.append((s, e))
            matches.append((s, e, kind, m))

    pos = 0
    for j, part in enumerate(line.split("`")):
        if (j % 2 == 0) != in_code_span:
            take(part, pos, EXT_CITATION_RE, "external")
            for regex in declared_res:
                take(part, pos, regex, "declared")
            take(part, pos, CITATION_DECISION_RE, "decision")
            take(part, pos, CITATION_SECTION_RE, "section")
            take(part, pos, CITATION_ENTRY_RE, "entry")
            take(part, pos, BARE_DECISION_RE, "bare")
        pos += len(part) + 1
    return matches


def resolve_entry(key, entry_index):
    """Resolve one (area, NNN, slug) reference key against entry_index.

    Returns (path, reason). path is the entry Path when the reference
    resolves, None otherwise; reason then says why: "missing" when no
    entry carries the number, "slug" when the slug names none of the
    claimants, "ambiguous" when a bare number names more than one. The
    slug wins when it matches: the caller reports a bare number that
    names more than one, never a slug that names one.
    """
    area, nn, slug = key
    claimants = entry_index.get((area, nn), [])
    if not claimants:
        return None, "missing"
    if slug is not None:
        for s, q in claimants:
            if s == slug:
                return q, None
        return None, "slug"
    if len(claimants) == 1:
        return claimants[0][1], None
    return None, "ambiguous"


def lint_entry(p, rel, ledger, declared, declared_shapes, entry_index,
               decision_index):
    """Lint one entry file. Returns (findings, legacy, skipped).

    "skipped" is True when the entry declares a schema above SCHEMA_MAX. The
    caller must then suppress its J01 findings too: this lint cannot judge an
    entry written to a schema it does not know.
    """
    rel_dir_parts = rel.parts[:-1]
    rel_dir = "/".join(rel_dir_parts)
    findings = []
    legacy = False
    skipped = False

    def add(code, line, msg, cls="error"):
        if cls == "error" and legacy:
            cls = "note"
        findings.append({"path": p.as_posix(), "line": line, "code": code,
                         "cls": cls, "msg": msg})

    try:
        text = p.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        add("J02", 1, "entry file is not valid UTF-8; heading unreadable")
        return findings, legacy, False
    except OSError:
        add("J02", 1, "entry file cannot be read; checks skipped")
        return findings, legacy, False
    lines = text.splitlines()

    # J09 (part 1) — read the declaration before every other check. A
    # declaration above SCHEMA_MAX means this lint cannot judge the entry, so
    # it reports one note and leaves the entry alone.
    schema_lineno, entry_schema, schema_findings = read_entry_schema(lines)
    if entry_schema is not None and entry_schema > SCHEMA_MAX:
        findings.append({
            "path": p.as_posix(), "line": schema_lineno, "code": "J09",
            "cls": "note",
            "msg": f"entry declares schema {entry_schema}; this lint "
                   f"understands schema {SCHEMA_MAX}; remaining checks "
                   f"skipped",
        })
        return findings, legacy, True

    # J04 (part 1) — locate and parse the date line first: the entry date
    # decides legacy status, which downgrades later findings to notes.
    entry_date = None
    date_lineno = None
    date_line = None
    for i, line in enumerate(lines):
        if DATE_PREFIX_RE.match(line):
            date_lineno, date_line = i + 1, line
            break
    if date_line is None:
        add("J04", 0, 'date line missing (expected '
                      '"Date: <YYYY-MM-DD>. Depends on: <area>/<NNN>.")')
    else:
        dm = DATE_LINE_RE.match(date_line)
        if not dm:
            add("J04", date_lineno, f"date line does not parse: {excerpt(date_line)}")
        else:
            entry_date = iso_date(dm.group(1))
            if entry_date is None:
                add("J04", date_lineno,
                    f"date is not a valid ISO 8601 date: {dm.group(1)}")

    effective, legacy = resolve_schema(ledger, entry_date, entry_schema)

    # J09 (part 2) — held until legacy is known, so a legacy entry reports
    # notes like every other check.
    for code, lineno, msg in schema_findings:
        add(code, lineno, msg)
    if entry_schema is not None and ledger:
        highest = max(v for v, _a, _iso, _ln in ledger)
        if entry_schema > highest:
            add("J09", schema_lineno,
                f"entry declares schema {entry_schema}; the ledger in "
                f"journals/README.md adopts no schema above {highest}")
    if schema_lineno is not None and date_lineno is not None \
            and schema_lineno != date_lineno + 1:
        add("J09", schema_lineno,
            f"schema line must come directly after the Date line "
            f"(line {date_lineno + 1}), found it on line {schema_lineno}")
    # Gated on the line being absent, not on the version being unreadable: a
    # line that fails to parse already has its own finding, and an entry that
    # declares badly still declares.
    if schema_lineno is None and effective is not None and effective >= 2:
        add("J09", date_lineno or 1,
            f"entry resolves to schema {effective} and must declare it "
            f'("Schema: {effective}." after the Date line)')

    # J04 (part 2) — dependency targets.
    if date_line is not None:
        dm = DATE_LINE_RE.match(date_line)
        if dm:
            deps = dm.group(2).strip()
            if deps == "none":
                pass
            else:
                for item in (s.strip() for s in deps.split(",")):
                    if not item:
                        add("J04", date_lineno,
                            f"date line does not parse: {excerpt(date_line)}")
                        continue
                    am = AREA_REF_RE.match(item)
                    if not am:
                        add("J04", date_lineno,
                            f'dependency does not parse as "<area>/<NNN>": {item}')
                    else:
                        ep, reason = resolve_entry(entry_key(am), entry_index)
                        if reason == "ambiguous":
                            n = len(entry_index[(am.group(1), am.group(2))])
                            add("J04", date_lineno,
                                f"dependency is ambiguous: {item} names "
                                f"{n} entries")
                        elif ep is None:
                            add("J04", date_lineno,
                                f"dependency does not resolve: {item}")

    # J06 — one line level under an area: two components (area + file) or
    # three (area + line + file). One or four-plus components is an error.
    if len(rel.parts) not in (2, 3):
        add("J06", 1,
            f"entry path must nest at most one line level under an area "
            f"(two or three path components under journals/), found "
            f"{len(rel.parts)}")

    # J02 — heading parses and matches the file's path.
    heading = lines[0] if lines else ""
    hm = HEADING_RE.match(heading)
    if not hm:
        shown = excerpt(heading) if heading.strip() else "(missing)"
        add("J02", 1, 'heading does not parse as '
                      '"# Journal <area>/<NNN> — <description>": '
                      f"{shown}")
    else:
        heading_area, heading_nn = hm.group(1), hm.group(2)
        fnm = ENTRY_FILENAME_RE.match(p.name)
        if fnm is None:
            add("J02", 1, f'heading parses but the filename lacks the '
                          f'"<NNN>-" prefix ("<NNN>-<slug>.md"): {p.name}')
        elif heading_area != rel_dir or heading_nn != fnm.group(1):
            add("J02", 1, f"heading does not match entry path: expected "
                          f"{rel_dir}/{fnm.group(1)}, found "
                          f"{heading_area}/{heading_nn}")

    # J03 — status line is the second non-empty line.
    nonempty = [(i + 1, line) for i, line in enumerate(lines) if line.strip()]
    if len(nonempty) < 2:
        add("J03", nonempty[-1][0] if nonempty else max(len(lines), 1),
            'status line missing (the second non-empty line must be '
            '"Status: ...")')
    else:
        status_lineno, status_line = nonempty[1]
        sm = STATUS_RE.match(status_line)
        if not sm or not sm.group(1).strip():
            add("J03", status_lineno,
                f"status line does not parse: {excerpt(status_line)}")
        else:
            items = [it.strip() for it in sm.group(1).strip().split(",")]
            primary, modifiers = items[0], items[1:]
            if primary not in PRIMARY_STATES:
                add("J03", status_lineno,
                    f"unknown primary state: {primary} (expected one of "
                    f"{', '.join(PRIMARY_STATES)})")
            for it in modifiers:
                if not it:
                    add("J03", status_lineno,
                        f"status line does not parse: {excerpt(status_line)}")
                elif it in PRIMARY_STATES:
                    add("J03", status_lineno, f"primary state must come first: {it}")
                elif it in BASE_MODIFIERS or it in declared:
                    continue
                else:
                    um = SUPERSEDED_RE.match(it)
                    if not um:
                        add("J03", status_lineno, f"unknown status modifier: {it}")
                        continue
                    ref = um.group(1).strip()
                    am = AREA_REF_RE.match(ref)
                    if not am:
                        add("J03", status_lineno,
                            f'supersession target does not parse as '
                            f'"<area>/<NNN>": {ref}')
                    else:
                        ep, reason = resolve_entry(entry_key(am), entry_index)
                        if reason == "ambiguous":
                            n = len(entry_index[(am.group(1), am.group(2))])
                            add("J03", status_lineno,
                                f"supersession target is ambiguous: {ref} "
                                f"names {n} entries")
                        elif ep is None:
                            add("J03", status_lineno,
                                f"supersession target does not resolve: {ref}")

    # J05 — Decisions numbering. The section's span (dec_start..dec_end) is
    # shared with J10 below, so both checks mean the same lines by
    # "## Decisions".
    dec_start = None
    for i, line in enumerate(lines):
        if DECISIONS_HEADING_RE.match(line):
            dec_start = i
            break
    dec_end = None
    if dec_start is not None:
        section = []
        j = dec_start + 1
        while j < len(lines) and not SECTION_HEADING_RE.match(lines[j]):
            section.append((j + 1, lines[j]))
            j += 1
        dec_end = j
        seq = 0
        unnumbered = []
        for lineno, line in section:
            s = line.strip()
            if not s:
                continue
            nm = NUMBERED_ITEM_RE.match(line)
            if nm:
                seq += 1
                dm2 = DECISION_ITEM_RE.match(s)
                if not dm2:
                    add("J05", lineno, 'decision item does not match '
                                       '"N. **DN — name.**": '
                                       f"{excerpt(line)}")
                elif int(dm2.group(1)) != seq:
                    add("J05", lineno, f"decision numbering out of sequence: "
                                       f"expected {seq}, found {dm2.group(1)}")
                elif int(dm2.group(2)) != seq:
                    add("J05", lineno, f"decision number D{dm2.group(2)} does "
                                       f"not match item position {seq}")
            elif UNNUMBERED_ITEM_RE.match(s):
                unnumbered.append((lineno, s))
        if unnumbered:
            if legacy:
                add("J05", unnumbered[0][0],
                    "legacy entry: decisions unnumbered", cls="note")
            else:
                for lineno, s in unnumbered:
                    add("J05", lineno, f"decision item is unnumbered: {excerpt(s)}")

    # J07 — dates are ISO 8601 everywhere they appear. The Date line is
    # J04's; J07 skips it to avoid double-reporting. Quote lines are exempt:
    # they carry verbatim session speech, and a date inside one is evidence,
    # not a contract date.
    for i, line in enumerate(lines):
        if date_lineno is not None and i + 1 == date_lineno:
            continue
        if line.lstrip().startswith(">"):
            continue
        for m in ISO_TOKEN_RE.finditer(line):
            if iso_date(m.group(1)) is None:
                add("J07", i + 1,
                    f"date is not a valid ISO 8601 date: {m.group(1)}")
        for m in NON_ISO_DATE_RE.finditer(line):
            add("J07", i + 1,
                f"date not in ISO 8601 (YYYY-MM-DD): {m.group(1)}")

    # J10 — inline citation resolution. Scans the body only: the front matter
    # holds the Status and Depends on lines, J03/J04 territory. Quote lines
    # are exempt (verbatim session speech may cite anything) and decision
    # definitions are J05's, exempt only inside the Decisions section. The
    # code-span state carries across scanned lines and hides grammar
    # illustrations that cite entries of other repos. A declared shape and
    # an external "ext:" citation are recognized and never resolved; a bare
    # D<k> is exempt when this entry defines it. The class is computed
    # here: on schema 4 or higher a miss
    # is an error and a bare ID a note; below it a miss is a note and a
    # bare ID reports nothing.
    gate = effective is not None and effective >= 4
    miss_cls = "error" if gate else "note"
    fnm = ENTRY_FILENAME_RE.match(p.name)
    own = fnm.group(1) if fnm else None
    # The decision index maps (area, NN, k) to the set of entry paths that
    # define the decision; a bare D<k> counts as defined only when this
    # entry's own path is among them. Two entries that share a number do
    # not share decisions.
    own_decisions = {k for (a, n, k), paths in decision_index.items()
                     if a == rel_dir and n == own and p in paths}
    declared_res = [shape_to_regex(s) for s in declared_shapes]
    in_code_span = False
    body_start = front_matter_end(lines)
    for i, line in enumerate(lines):
        in_decisions = dec_start is not None and dec_start < i < dec_end
        if i >= body_start and not line.lstrip().startswith(">") \
                and not (in_decisions
                         and DECISION_ITEM_RE.match(line.strip())):
            for _s, _e, kind, m in collect_citations(
                    line, in_code_span, declared_res):
                if kind in ("declared", "external"):
                    continue
                if kind == "bare":
                    if int(m.group(1)) not in own_decisions and gate:
                        add("J10", i + 1,
                            f"bare decision ID; the entry qualifies it: "
                            f"D{m.group(1)}", cls="note")
                    continue
                area, nn, slug = entry_key(m)
                ep, reason = resolve_entry((area, nn, slug), entry_index)
                if ep is None:
                    if reason == "ambiguous":
                        n = len(entry_index[(area, nn)])
                        add("J10", i + 1,
                            f"citation is ambiguous: {m.group(0)} names "
                            f"{n} entries", cls=miss_cls)
                    else:
                        add("J10", i + 1,
                            f"citation does not resolve to an entry: "
                            f"{m.group(0)}", cls=miss_cls)
                elif kind == "decision" \
                        and ep not in decision_index.get(
                            (area, nn, int(m.group(4))), set()):
                    add("J10", i + 1,
                        f"decision citation does not resolve: "
                        f"{m.group(0)}", cls=miss_cls)
            if line.count("`") % 2:
                in_code_span = not in_code_span

    return findings, legacy, skipped


def lint_numbering(entries, legacy_by_path, skipped_paths):
    """J01 — filenames, lowest number 000 per directory, gap notes.

    An entry in skipped_paths declared a schema above SCHEMA_MAX. It keeps
    its place in the number sequence, so a sibling never reports a false gap,
    but it collects no finding of its own.
    """
    findings = []
    dirs = {}
    for p, rel in entries:
        dirs.setdefault(rel.parts[:-1], []).append((p, rel))
    for dir_parts in sorted(dirs):
        matches = []
        for p, rel in sorted(dirs[dir_parts], key=lambda t: t[0].name):
            fm = ENTRY_FILENAME_RE.match(p.name)
            if fm is None:
                if p.as_posix() in skipped_paths:
                    continue
                cls = "note" if legacy_by_path.get(p.as_posix(), False) else "error"
                findings.append({
                    "path": p.as_posix(), "line": 1, "code": "J01", "cls": cls,
                    "msg": f'filename does not match "<NNN>-<slug>.md": {p.name}',
                })
            else:
                matches.append((int(fm.group(1)), p, fm.group(1)))
        if not matches:
            continue
        matches.sort(key=lambda t: t[0])
        lowest_n, lowest_p, lowest_s = matches[0]
        if lowest_n != 0 and lowest_p.as_posix() not in skipped_paths:
            cls = ("note"
                   if legacy_by_path.get(lowest_p.as_posix(), False) else "error")
            findings.append({
                "path": lowest_p.as_posix(), "line": 1, "code": "J01", "cls": cls,
                "msg": f"lowest entry number in {display_dir(dir_parts)} is "
                       f"{lowest_s}, expected 000",
            })
        # A duplicate is not a gap (n == prev, and the gap test reads
        # n > prev + 1), so it gets its own sweep. One note per group of
        # entries that share a number, anchored at the second file of the
        # group in walk order: the first file a short reference can miss.
        # A skipped entry keeps its place in the group but collects no
        # finding of its own, so a note anchored on one is suppressed.
        prev = None
        dup_reported = False
        for n, p, nstr in matches:
            if prev is not None and n > prev + 1 and p.as_posix() not in skipped_paths:
                missing = ", ".join(f"{k:03d}" for k in range(prev + 1, n))
                findings.append({
                    "path": p.as_posix(), "line": 1, "code": "J01", "cls": "note",
                    "msg": f"numbering gap in {display_dir(dir_parts)}: "
                           f"{missing} missing",
                })
            if prev is not None and n == prev and not dup_reported:
                dup_reported = True
                if p.as_posix() not in skipped_paths:
                    count = sum(1 for k2, _q, _s in matches if k2 == n)
                    findings.append({
                        "path": p.as_posix(), "line": 1, "code": "J01",
                        "cls": "note",
                        "msg": f"duplicate entry number in "
                               f"{display_dir(dir_parts)}: {nstr} is shared "
                               f"by {count} entries; a short reference to "
                               f"it resolves to none of them",
                    })
            prev = n
    return findings


def build_indexes(journals):
    """Build the citation indexes for the journals tree.

    Returns (entry_index, decision_index). entry_index maps (area_dir, NNN)
    to a list of (slug, Path) pairs in walk order; two entries that share a
    number both land, and the resolvers judge. area_dir is the entry's
    directory under journals/ as a /-joined string. decision_index maps
    (area_dir, NN, k) to the set of entry Paths that define it, walked
    exactly as J05 walks the "## Decisions"
    section. The index records, it does not judge: numbering findings stay
    J05's.
    """
    entry_index = {}
    decision_index = {}
    for p, rel in discover_entries(journals):
        fm = ENTRY_FILENAME_RE.match(p.name)
        if not fm:
            continue
        area_dir = "/".join(rel.parts[:-1])
        nn = fm.group(1)
        entry_index.setdefault((area_dir, nn), []).append((fm.group(2), p))
        try:
            lines = p.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeDecodeError):
            continue
        dec_start = None
        for i, line in enumerate(lines):
            if DECISIONS_HEADING_RE.match(line):
                dec_start = i
                break
        if dec_start is None:
            continue
        j = dec_start + 1
        while j < len(lines) and not SECTION_HEADING_RE.match(lines[j]):
            if NUMBERED_ITEM_RE.match(lines[j]):
                dm = DECISION_ITEM_RE.match(lines[j].strip())
                if dm:
                    decision_index.setdefault(
                        (area_dir, nn, int(dm.group(2))), set()).add(p)
            j += 1
    return entry_index, decision_index


def lint_repo(root):
    journals = root / "journals"
    readme_findings, declared, declared_shapes, ledger, notice = \
        lint_readme(journals / "README.md")
    if notice is not None:
        return readme_findings, ledger, notice, {}, {}
    entries = discover_entries(journals)
    entry_index, decision_index = build_indexes(journals)
    findings = list(readme_findings)
    legacy_by_path = {}
    skipped_paths = set()
    for p, rel in entries:
        entry_findings, legacy, skipped = lint_entry(
            p, rel, ledger, declared, declared_shapes,
            entry_index, decision_index)
        legacy_by_path[p.as_posix()] = legacy
        if skipped:
            skipped_paths.add(p.as_posix())
        findings.extend(entry_findings)
    findings.extend(lint_numbering(entries, legacy_by_path, skipped_paths))
    return findings, ledger, notice, entry_index, decision_index


def main():
    findings, ledger, notice, _entry_index, _decision_index = \
        lint_repo(Path.cwd())
    if notice is not None:
        print(notice)
        return 2
    findings.sort(key=lambda f: (f["path"], f["line"], f["code"], f["msg"]))
    for f in findings:
        print(f'{f["path"]}:{f["line"]} {f["cls"]:<5} {f["code"]} {f["msg"]}')
    errors = sum(1 for f in findings if f["cls"] == "error")
    notes = sum(1 for f in findings if f["cls"] == "note")
    if ledger:
        highest, _adopted, iso, _lineno = max(ledger, key=lambda t: t[0])
        state = f"repo schema {highest}, adopted {iso}"
    else:
        state = "repo schema not found"
    print(f"summary: {errors} error{'' if errors == 1 else 's'}, "
          f"{notes} note{'' if notes == 1 else 's'} "
          f"({state}, lint understands schema {SCHEMA_MAX})")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
