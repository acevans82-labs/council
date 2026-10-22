---
name: evidence-ledger
description: "The shared fact ledger for a council round, stored in the effort folder as ledger.json. Every fact, finding, conflict, ruling, request to the principal, handoff and gap gets an ID and a source. Read before writing to the ledger for the first time in a round. Nothing reaches the assessment, dashboard or any output without a ledger ID."
---

# evidence-ledger

`benches/<bench>/efforts/<effort>/ledger.json` is the single source of truth for a round. Personas write to it; the chair reads from it; outputs render from it. The full schema is in `references/schema.md`.

## Rules

**Every fact gets an evidence record before it is used.** Write the `E-` record with source, tier, reliability, locator and timestamp, then cite it in the finding. No orphan claims.

**Source tier is fixed at record time.**
- `T1` principal-supplied: documents the principal provides (decks, plans, financials, contracts, notes, prior analyses), the bench's `context/` folder, facts the principal confirms at intake, and the principal's written answers between rounds. Locator is the document name and page or section, "context: <file>, <section>", "intake, confirmed by principal", or "principal answer, round N".
- `T2` primary public sources: regulators and registers, filings, court records, statutes and rules, official statistics, peer-reviewed research, standards bodies, procurement records.
- `T3` third party: press, analyst and vendor reports, comparison sites, websites, reviews, job postings, funding databases, conference material, forums.

The bench's `bench.md` may name which sources count as T2 in its field. When it is silent, use the definitions above.

**Reliability grade** is separate from tier: `A` primary document, `B` reputable secondary, `C` single unverified source, `D` inferred or modeled. An assertion in a supplied deck is T1 but `C` until corroborated.

**Show the math.** A figure the persona computed or modeled (reliability `D`, or any derived number) carries a `calc` field: the inputs by evidence ID, the formula in words or symbols, and the assumptions, so a reader can redo it. No `calc`, no derived number.

**Locator and timestamp are mandatory.** URL for web, filing type and date for registers, document name and page for supplied files. If you cannot say where it came from, do not record it.

**Findings carry two tags.** `confidence` (High / Moderate / Low, the persona's own confidence) and `evidence_strength` (Strong: multiple T1/T2 A-grade · Corroborated: two independent sources · Single-source · Inferred).

**Headline threshold.** A finding is a `headline` only at Moderate confidence or better and Corroborated evidence or better. Otherwise `supporting` or `open`. The chair cannot waive this; only the principal can, through a judgment-call record.

**Persona attribution is immutable.** Disagreement is a `contested_by` entry and, if evidence conflicts, a conflict record. Never an edit.

**Requests to the principal are records.** Before the chair asks the principal anything, it writes a `J-` record with the question, options and `why_principal`. Answers are written back when they arrive, usually at the next round's intake.

**Every principal-facing ask gets a priority tier.** Every `J-` record, every `G-` record with `raised_to_principal: true`, and every unresolved `C-` record carries a `tier` (0 must-have, 1 high-value, 2 useful, 3 nice-to-have) set by the chair at synthesis. Tier by leverage against this round's actual decisions and deadlines, never to hit a target count. Full definitions in `skills/council-ledger`.

**Effort isolation.** A round reads and writes only its own effort folder. Never cite an evidence record from another effort's ledger, on this bench or any other. Public facts that apply to more than one effort are retrieved and recorded again in each.

## Consults do not write here
A quick consult (`skills/convening`) reads the ledger and writes a memo. Its inline citations enter the ledger only when the consult is promoted into a round, at that round's intake.

## Carry-forward on a later round

Copy `evidence`, `conflicts`, `gaps` and `judgment_calls` from the prior ledger with `carried_from: <round_id>` on each record. Do not copy `findings`, `rulings` or `assessment`; conclusions anchor, evidence does not. Re-verify any carried evidence record older than 90 days before a persona cites it and set `reverified`. Copy `score_history` whole and append the new round's score at the end.

Principal answers collected at intake are written into the carried `J-` records (`answer`, `answered_at`, `answered_in_round`) and each answer also becomes a new T1 `E-` record so findings can cite it.

## ID conventions

`E-` evidence · `F-` finding · `C-` conflict · `R-` ruling · `J-` request to the principal · `G-` gap · `H-` handoff · `Q-` open question. Sequential within a round. Carried records keep their ID with a `P/` prefix.

## Writing to the file

Append, never rewrite history. Corrections are new records with `supersedes` set. Personas write in small batches as they finish so an interrupted round loses one persona's work, not a phase's. When personas run in parallel, each writes its records to `rounds/<round_id>/<persona>.json` and the chair merges them into `ledger.json` at the end of the phase with `scripts/merge_ledger.py`, renumbering IDs in persona order and rewriting cross-references.
