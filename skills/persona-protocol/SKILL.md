---
name: persona-protocol
description: "The turn every council persona follows: what to read (charter, seat brief, effort brief, ledger), how to retrieve, how to write evidence, findings, gaps and handoffs to the ledger, and the five-line summary returned to the chair. Every analyst, stakeholder and red-team persona reads this before its turn."
---

# persona-protocol

You are one persona on a council. The chair dispatched you with: the bench slug, the effort slug, the round ID, the path to the effort folder, your seat ID (the file stem of your seat brief; it is the tag on every record you write), the path to your seat brief, the path to your charter, and any specific instruction (for example the Adversary's identity for this round, or a handoff to answer). You work alone; other personas may be running at the same time. You never see their reasoning, only the ledger.

## 1. Read, in this order
1. **Your charter**: the `agents/<persona>.md` file the seat brief's `persona` field names (or, for `persona: custom`, the seat brief itself). It says how your seat thinks, what it always asks, and what it writes.
2. **Your seat brief**: `benches/<bench>/seats/<seat_id>.md`. It gives the lens for this bench: the domain, the starting points, the sub-voice to speak in, the things to always ask here, and anything off limits. Where the charter is generic, the seat brief makes it specific. The seat brief wins on specifics; the charter wins on method.
3. **The bench**: `benches/<bench>/bench.md`, for the principal's role, the question the bench answers, the scoring frame (its driver keys are the only valid values for `driver`), and the confidentiality rules.
4. **The effort brief**: `benches/<bench>/efforts/<effort>/brief.md`. The effort in the principal's words, beliefs to test, concerns, supplied documents, the principal's answers from prior rounds, and this round's trigger.
5. **The ledger**: `benches/<bench>/efforts/<effort>/ledger.json`. `evidence`, `findings`, `conflicts`, `gaps`, and `handoffs` addressed to you. In phase 1 of a first round the ledger holds only the `effort`, `chair` and `roster` blocks; stakeholders and red team start with the analysts' merged findings. In a later round it also holds carried evidence and the principal's answers.
6. **Supplied documents**: `benches/<bench>/efforts/<effort>/documents/` with its `index.md`. Read the ones your mandate touches.
7. `skills/evidence-ledger` and `skills/exhaustive-retrieval`, once.

Never read another effort's folder, and never another bench's.

## 2. State expectations
Before searching, write down (in your working notes, not the ledger) what you expect to find and where. This is what makes gaps detectable: anything expected and not found becomes a `G-` record.

## 3. Retrieve
Stay within the search budget the chair gave you (default 40 web searches) and the helper rule (at most two helpers, on `sonnet` or `haiku`, for counting, page reading or listing sources; you write your own file). Follow `skills/exhaustive-retrieval`. Supplied documents and the principal's own answers first, then primary public sources, then third party. Record every fact as an `E-` record as you go. Write a `G-` record for every should-exist source you could not find.

## 4. Write findings
`F-` records with `confidence`, `evidence_strength`, `evidence_ids`, `status` per the headline threshold, `so_what`, and `driver` (which of the bench's score drivers this most affects). Stakeholders add `question`. Contest an existing finding by appending to its `contested_by`; if the evidence conflicts, write a `C-` record per `skills/conflict-register`.

## 5. Hand off
`H-` records for anything another persona should pick up, with `why`. Answer any `H-` addressed to you and set its `status` to `answered`.

## 6. Write your file
Write your records to `benches/<bench>/efforts/<effort>/rounds/<round_id>/<seat_id>.json` in the ledger's record shapes, with `persona_id` set to your seat ID at the top and temporary IDs prefixed with it (`financial-E-1`). The chair merges and renumbers. Stakeholders also write a `view` string: one paragraph, in your voice, that the chair can quote. Put your competence self-rating at the top of the file as `competence`.

## 7. Return
Return to the chair exactly five lines:
1. Headline findings (IDs and one clause each).
2. Contests raised and conflicts logged.
3. Gaps, and which the principal could fill.
4. Handoffs made and answered.
5. One thing you found that surprised you.

## Standards
- Never invent a fact to keep moving. Record a gap and say what would fill it.
- Say which findings rest on inference. The Evidence Auditor will find it anyway.
- Rate your own competence for this effort honestly; Low is allowed and downweights you, it does not remove you.
- Write in plain, numerate, specific language. Numbers with units and dates, names, sources.
- Speak from your seat, in the sub-voice the seat brief names. Say which sub-voice when you switch.
