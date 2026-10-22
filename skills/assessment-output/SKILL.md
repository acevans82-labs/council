---
name: assessment-output
description: "Produces the written assessment and the 'What the council needs from the principal' list at the end of every council round, rendered only from ledger.json and shaped by the bench's assessment outline. Also covers the on-request outputs: deck storyline, comparison map, question list for the other party, a note for a named reader. Read by the chair after scoring."
---

# assessment-output

Everything renders from the ledger. If a number is not in the ledger, it is not in the assessment.

**Tier every principal-facing ask before writing anything else.** Immediately after scoring, walk every `judgment_calls[]` record, every `gaps[]` record with `raised_to_principal: true`, and every `conflicts[]` record still unresolved, and set its `tier` (0 must-have · 1 high-value · 2 useful · 3 nice-to-have) per the definitions in `skills/council-ledger`. Tier by whether the item blocks a near-term decision or deadline, or whether the numbers behind the verdict itself depend on it, not by forcing a target count. Add `tier_rationale` on every Tier 0. Do this before writing the principal-requests list or `exec_summary`; both depend on it.

## Always produced

### 1. The assessment
File: `benches/<bench>/efforts/<effort>/assessments/<round_id>-assessment.md`. When a Claude Docs connector is available, also create it as a doc titled "[Effort] — Council assessment, round N" so the principal can comment; the markdown file is the archive. Offer a Word version on request (read the docx skill first).

Structure, in this order; sections with nothing to say are one line, never omitted. The bench's `bench.md` names the subject sections (item 2) and the stakeholder order (item 4); `effort.noun` replaces "company" in headings.
```
# [Effort] — [Bench name] assessment
Round [round_id] (round N) · [initial | update: trigger] · depth: [standard|deep] · materials: [cleared|downgraded|blind: items] · [date] · Chair competence: [rating]

## 1. Score and verdict
[score_label]: score, band, horizon. The verdict. Top movers. Biggest stakeholder risk. What would raise the score.
(Round 2+: movement since the last round, which drivers moved, and which principal answers moved them.)

## 2. [Subject sections from the bench's assessment outline, e.g. Industry standing / Competitive positioning / Operating strengths and weaknesses, or Problem and demand / Solution and differentiation / Timing]
One to three paragraphs each, citing F- IDs. Named rivals, named jurisdictions, named constituencies.

## 3. Driver scores
The table: driver, weight, score, rationale, finding IDs.

## 4. How the [noun] lands with each stakeholder
One short section per stakeholder on the roster, in the bench's roster order. Each: the persona's `view` paragraph, then findings grouped by the three questions with tags and IDs, plus any table the seat's charter promises (a jurisdictions table, a line-of-business table, an access assessment).

## 5. Red team
Adversary responses (who, what, when, which findings undermined). Pre-mortem stories and early signals. Auditor summary and the weakest load-bearing evidence.

## 6. Where sources disagreed
Public-disclosure-relevant conflicts first, marked. Both values, both sources, likely cause, status, who ruled.

## 7. Could not find
Gaps: what, why expected, where searched, what the principal could supply.

## 8. Chair rulings
## 9. What the council needs from the principal
(see below; repeated here in full)

## Appendix A: Evidence ledger — every E- record, sorted by ID
## Appendix B: Roster and relevance ratings
```
Cite inline as `(F-012; E-034, E-051)`. Confidence and evidence-strength tags on every finding. Never smooth an unresolved conflict with "the subject indicates"; show both. Neutral voice throughout; the principal is never "you" in the assessment.

### 2. What the council needs from the principal
File: `benches/<bench>/efforts/<effort>/assessments/<round_id>-principal-requests.md`, and repeated in the chat reply as the closing message of the round. Numbered. Grouped: judgment calls (with options and `why_principal`), gaps only the principal can fill (with the document or fact that would close each), material unresolved conflicts, headline waivers requested. Within each group, Tier 0 items first, then 1, 2, 3; state the tier on every item. Each links to ledger IDs and says which driver score it would affect. Open with a one-line count by tier ("X of Y items are must-have"). Close with one line: "Answer any of these in the next round's intake; the council carries the rest forward." This list is the round's most valuable output on an effort with no supplied documents; make it precise. It is also the seed of the next round.

### 3. Executive summary (in the ledger, before the dashboard is built)
On every round the chair writes `exec_summary` into `ledger.json` after tiering and scoring, before building the dashboard. It is the two-to-three-sheet version for the principal: the verdict in plain language, act-by-date items, the principal's stated questions answered (from the brief's beliefs-to-test and concerns), the judgment calls one line each (with an `id` so the dashboard can badge its tier), the top document requests and top conflicts (also with `id`), the top risk callouts, and a bottom line. Schema and length caps in `skills/council-ledger`. Everything in it must already exist in the ledger under an ID; the executive summary compresses, it never introduces.

### 4. Council ledger dashboard
Per `skills/council-ledger`. Refuse to call the round complete if the dashboard was built from a ledger without `exec_summary`; add it and rebuild.

### 5. Score history
Append to `benches/<bench>/efforts/<effort>/score-history.json`.

## On request
- **Deck storyline** — assertion-led, one block per slide: score and verdict; each subject section; the drivers; stakeholder reactions (one slide per seat that matters); red team; disagreements and gaps; decisions for the principal. Every point cites an ID. Build as slides only when asked (use the session's slides type or the pptx skill).
- **Comparison map** — table of the named alternatives or rivals: segment, resources, price, reach, recent moves, threat rating, evidence IDs.
- **Question list for the other party** — `open_questions` with `owner: other_party`, neutral, numbered, each with the document or data that would answer it. Contains no findings, conflicts framed as suspicions, or scores. The "other party" is whoever the bench says it is: a management team, a counterparty, a vendor, a school.
- **Briefing deck** — the deck for the other party: method, score, insights, data requests, questions, next steps. Per `skills/briefing`; that skill fixes the structure.
- **Note for a named reader** — for a co-investor, a partner, a colleague, a spouse: the findings that reader needs, in a lighter citation style, nothing that reader should not see.
