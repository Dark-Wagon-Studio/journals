# ste-lint categories

Rule definitions for `ste-lint.py`, one section per counted category in the
fixed template from `docs/markdown-conventions.md` §8. The basis names the
claim the diagnostic may make: consistency states a mechanically
established fact, convention states a breach of a content contract, and
heuristic offers an observed feature as a conditional suggestion. A note
never claims more than its basis supports.

The lint counts, it never passes or fails. It reads Markdown from the files
named on the command line, or from stdin when none are. It strips fenced
blocks and inline code spans, and splits what remains into sentences.
Eleven categories count their matches; the score is total violations per
100 words, and the signal is the delta between two drafts, not any single
number. Two more figures print in the stdin/JSON path only, without
counting toward the score: the count of em and en dashes in the raw text,
and the longest sentence in words. File-argument mode prints a one-line
summary per file and omits the longest sentence. Word-list
matching ignores case.

Every category here is heuristic. The count is a mechanical fact; the
reading — this line carries slop — is a conditional suggestion, and the
README says so plainly: a banned-words list is the least reliable fix.

## long_sentence(>20w)

### What it checks

A sentence of more than 20 words counts one. Heading markers and list
markers come off before the count.

### Basis

Heuristic. The count is mechanical; the suggestion is that the sentence
carries slack.

### Why it matters

STE wants one instruction per sentence, under 20 words. Length is where
padding hides.

### Example

    The tool provides a comprehensive set of capabilities that will allow you to easily manage all of the various different aspects of your configuration files across all of your projects.

### Instead

    The tool manages configuration files across projects.

### Exceptions

None. The count is exact after code stripping.

### Inputs

The sentence list, after fenced blocks and inline code spans are stripped.

### Configuration

None. The threshold of 20 is a constant in the script.

## semicolon

### What it checks

Each semicolon in the stripped text counts one.

### Basis

Heuristic. The count is mechanical; the suggestion is that one line
carries two claims that want separation.

### Why it matters

STE avoids the semicolon. Two sentences read faster than one joined pair.

### Example

    Run the lint; fix the findings.

### Instead

    Run the lint. Fix the findings.

### Exceptions

Semicolons inside fenced blocks and inline code spans never count.

### Inputs

The stripped text, at character level.

### Configuration

None.

## contraction

### What it checks

Each contraction counts one: a word ending in an apostrophe, straight or
curly, plus t, re, ve, ll, d, s, or m.

### Basis

Heuristic. The count is mechanical; the suggestion is informality.

### Why it matters

STE writes verbs out. "Don't" becomes "do not", which reads as an
instruction.

### Example

    The lint won't rewrite the file.

### Instead

    The lint does not rewrite the file.

### Exceptions

A possessive such as `repo's` matches the `s` branch and counts. The lint
accepts that cost.

### Inputs

The stripped text.

### Configuration

None. The suffix list is a constant in the script.

## passive_voice

### What it checks

A be-verb — am, is, are, was, were, be, been, being — followed by a word
ending in `ed`, or by one of the listed irregular participles (done, made,
sent, read, built, kept, held, set, put, run, written, shown, given,
taken, found, got, gotten, seen, known, thrown, drawn), counts one.
Matching ignores case.

### Basis

Heuristic. A be-verb plus a participle is an observed feature; some
matches are not passive, and review decides.

### Why it matters

STE names the actor. "The file was written by the tool" becomes "The tool
writes the file."

### Example

    The file was written by the installer.

### Instead

    The installer writes the file.

### Exceptions

The pattern is shape-based. A word that merely ends in `ed`, such as
`speed`, matches.

### Inputs

The stripped text.

### Configuration

None. The be-verb list and the irregular-participle list are constants in
the script.

## ing_main_verb

### What it checks

A be-verb followed by a word ending in `ing` counts one. Matching ignores
case.

### Basis

Heuristic. The progressive shape is an observed feature; STE prefers the
simple present.

### Why it matters

"The tool is running" names a state. "The tool runs" names the behavior
the reader needs.

### Example

    The linter is checking the tree.

### Instead

    The linter checks the tree.

### Exceptions

The shape also matches a gerund use, such as "the goal is keeping costs
low". The lint accepts that cost.

### Inputs

The stripped text.

### Configuration

None.

## nominalization

### What it checks

Two shapes count. One: a padding verb — perform, conduct, provide, carry
out, make use of — with the inflected forms the list carries. Two: a stem
of four or more letters ending in tion, ment, ance, or ence, followed by
`of`. The whole word runs eight letters or more. Matching
ignores case.

### Basis

Heuristic. Both shapes are observed features that suggest a heavy noun
where a verb belongs.

### Why it matters

"Perform an initialization of" is four words where "initialize" is one.
The noun pile hides the action.

### Example

    Perform an initialization of the database.

### Instead

    Initialize the database.

### Exceptions

The verb list is closed. A padding verb outside the list never reports.

### Inputs

The stripped text.

### Configuration

None. The verb list and the suffix list are constants in the script.

## phrasal_verb

### What it checks

A listed phrase counts one: spin up, spin down, reach out, dive into,
dives into, diving into, kick off, kicks off, roll out, rolls out, tear
down, ramp up, circle back, drill down, spun up, reaching out. Matching
ignores case and bounds each phrase on letters.

### Basis

Heuristic. A listed phrase is an observed feature; STE prefers a single
verb.

### Why it matters

A phrasal verb buries the action in a particle. "Spin up a VM" becomes
"Start a VM."

### Example

    Spin up a container before you run the tests.

### Instead

    Start a container before you run the tests.

### Exceptions

Only listed phrases report. An inflection outside the list, such as
"spinning up", never reports.

### Inputs

The stripped text.

### Configuration

None. The list is a constant in the script.

## banned_word

### What it checks

A word or phrase from the banned list counts one. The list holds the
padding vocabulary — begin, commence, initiate, originate, utilize,
leverage, facilitate, ensure, obtain, acquire, demonstrate, additionally,
furthermore, moreover, comprehensive, utilization, aforementioned,
henceforth, therein, whilst, amongst, numerous, myriad, plethora — and the
phrase forms prior to, subsequent to, in order to, a variety of, in the
event that, due to the fact that, it is important to note, with the
inflected forms the list carries. Matching ignores case and bounds each
phrase on letters.

### Basis

Heuristic. The count is a signal, not a verdict; the skill's README calls
the banned-words list the least reliable fix.

### Why it matters

These words pad and hedge. Most have a shorter, plainer replacement.

### Example

    In order to commence, ensure that you initiate the daemon.

### Instead

    Start the daemon.

### Exceptions

Only list entries report. An inflection outside the list, such as
`ensured`, never reports. The phrase "it is important to note" sits in
this list and in the modal-hedge list; one occurrence counts in both
categories.

### Inputs

The stripped text.

### Configuration

None. The list is a constant in the script.

## marketing_adjective

### What it checks

A term from the marketing list counts one: seamless, robust, powerful,
cutting-edge, effortless, world-class, next-generation, revolutionary,
blazing, lightning-fast, elegant, delightful, turnkey, best-in-class,
state-of-the-art, game-changing, first-class, battle-tested,
enterprise-grade, supercharge, unlock, unleash, empower, with the
inflected forms the list carries. Matching ignores case.

### Basis

Heuristic. The term is an observed feature; the count feeds the score, and
the sample list names what matched.

### Why it matters

Marketing adjectives claim without evidence. STE replaces the claim with a
verifiable fact.

### Example

    This blazing, battle-tested tool provides seamless integration.

### Instead

    This tool imports the configuration in one step.

### Exceptions

Only list terms report. In the stdin/JSON path, the first six distinct
matches print as `sample_marketing`; the count is unaffected.

### Inputs

The stripped text.

### Configuration

None. The list is a constant in the script.

## modal_hedge

### What it checks

A hedge phrase counts one: it is important to note, it should be noted, it
is worth noting, please note that, as mentioned, as noted above. Matching
ignores case.

### Basis

Heuristic. The phrase is an observed feature of narration around the point
instead of the point.

### Why it matters

A hedge tells the reader to pay attention without saying anything. Delete
it, and the sentence stands.

### Example

    It is important to note that the lint never gates.

### Instead

    The lint never gates.

### Exceptions

The list is closed. The overlap with the banned list on "it is important
to note" counts once in each category.

### Inputs

The stripped text.

### Configuration

None. The list is a constant in the script.

## long_paragraph(>6s)

### What it checks

A paragraph — the text between blank lines in the raw file — whose
code-stripped sentence count passes six counts one.

### Basis

Heuristic. The count is mechanical; the suggestion is that the paragraph
holds more than one idea.

### Why it matters

STE keeps paragraphs short. A long paragraph buries the instruction its
first sentence promised.

### Example

A procedure paragraph of eight sentences.

### Instead

One paragraph per step, three sentences or fewer each.

### Exceptions

The sentence count strips code first, so a code-heavy paragraph never
reports on fence content alone.

### Inputs

The raw text, split on blank lines; the sentence count per paragraph runs
on stripped text.

### Configuration

None. The threshold of six is a constant in the script.
