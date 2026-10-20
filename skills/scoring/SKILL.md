---
name: scoring
description: "How the chair scores a council round: the bench's weighted drivers scored 0–10 from cited findings, a 0–100 score, a confidence band from the Evidence Auditor's report, and the narrative verdict. The drivers, weights and anchors come from the bench's scoring frame in bench.md, so the same procedure scores a company, an idea, a deal, a decision or a research question. Read by the chair at synthesis."
---

# scoring

The score is a structured judgment, not a model output. Every driver score cites the findings that set it, so the principal can trace the number back to evidence and disagree with a specific step.

## The frame comes from the bench
`benches/<bench>/bench.md` carries the scoring frame:
- `score_label`: what the number means, in words ("Probability of value creation over 3–5 years", "Likelihood this initiative delivers its objective by Q3", "Confidence that the evidence supports the answer"). It is written on every output.
- `horizon`: the period the judgment covers.
- the **drivers table**: four to eight rows of `key | driver | weight | what earns 9–10 | what earns 5–6 | what earns 0–2`, weights summing to 100.
- optional **standards**: thresholds such as "a score above 75 requires at least half the drivers at 7 or higher with Corroborated evidence".

Weights may change for one effort only if the principal said so at intake; record any change in the assessment. If the bench has no frame (a seat-only bench made by hand), use the default frame in `skills/bench-design` and say so in the assessment.

## Procedure
1. For each driver, list the headline and supporting findings tagged with that driver (`finding.driver`). Weigh stakeholder findings alongside analyst findings; a constituency's stated intent to walk, block or build its own is evidence.
2. Score 0–10 with a two-sentence rationale citing finding IDs. Say what would move it one point either way.
3. Raw score = Σ(weight × score) / 10, rounded to an integer.
4. Confidence band: start at ±5. Add ±3 if more than half the headline findings rest on T3 evidence; add ±3 if the Evidence Auditor demoted any headline; add ±4 if a load-bearing gap is open; add ±3 if a driver has fewer than two findings. Cap at ±25. Record the rationale.
5. Verdict: two to four paragraphs in the chair's neutral voice, following the bench's assessment outline section by section (standing, positioning, execution for a company; problem, solution, timing for an idea; fit, evidence, cost, reversibility for a decision). The probability judgment and what it rests on. No hedging clichés; name the trade-offs.
6. Fill `top_movers` (three findings that moved the score most), `biggest_stakeholder_risk` (the seat whose reaction is the largest downside), `what_would_raise` (three specific things, at least one of which the principal could supply or do).
7. Write `assessment.label` from `score_label`, append to `score_history`, and on a later round state the movement and which drivers moved.

## Standards
- Apply the bench's standards. Where the bench is silent: a score above 75 requires at least half the drivers at 7 or higher with Corroborated evidence; a band wider than ±15 leads with what would narrow it.
- Never let a driver score rest on a single Inferred finding; score it at the evidence's level and say so.
- A driver with no findings scores at 5 with the band widened per step 4, and the assessment says the council could not assess it.
