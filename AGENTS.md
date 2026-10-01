# AGENTS.md

Entry point for AI work in this repo. Read this first. The contract is
`journals/README.md` — it governs every rule summarized here.

## Planning workflow

Every line of work runs: plan, materialize, execute. Work the problem in
conversation or in `.agents/` (gitignored scratch), write the plan to
`journals/<area>/<NNN>-<slug>.md` per `journals/README.md`, then — only on
the user's instruction — execute it and append the outcome to the entry's
_Execution log_. Do not execute an entry in the session that wrote it,
unless the user explicitly says to implement it or has granted autonomy for
the line of work. Default to stopping after materialization.

## Confirm before acting

Before acting on anything that is not a direct instruction, state a default
and let the user override it, or stop and ask. Do not decide in silence.

## Skills

| Skill           | Use |
| --------------- | --- |
| `journal-craft` | Write and check journal entries against the schema ledger. Mandated when materializing or editing a journal entry. |
| `ste-writing`   | ASD-STE100 style for prose. Mandated for journal entries and for docs prose. |

## Repository map

| Path | Holds |
| --- | --- |
| `journals/meta/` | Convention records and install records. |
