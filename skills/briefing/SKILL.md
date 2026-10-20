---
name: briefing
description: "Builds a briefing deck from a completed council round for the other party in the effort (a management team, a counterparty, a vendor, a partner): the council's method, the score, the key insights, the data requests and the questions. Rendered only from ledger.json. Use when the principal asks for a briefing deck, 'the deck', or a deck for the other side."
---

# briefing

A deck for **the other party** named in the effort brief, not for the principal. Its goals, in order: make the council's method credible, land the score without ambushing anyone, teach the handful of insights that matter, and convert the round's gaps into a specific ask for data. Tone: direct, respectful, numerate. The deck says hard things plainly and never gloats.

## Source rules
- Render **only from `ledger.json`** (plus `score-history.json` on later rounds). If a number is not in the ledger, it is not in the deck.
- Every insight slide's footer cites its finding IDs: `Findings F-011, F-012; ruling R-009`.
- Other-party translation is mandatory:
  - `gaps` and `open_questions` become **data requests** ("what would sharpen the analysis"), never accusations.
  - `open_questions` with `owner: other_party` become the **questions slide**, neutral, numbered.
  - Principal-only material stays out: no `judgment_calls`, no principal-requests list, no principal framing. Red-team content appears only as method (roster) and as insights already merged into findings.
- Confidence: state the band and where it comes from; the score slide always carries the disclaimer that this is a probability, not a valuation and not a verdict on the people, and that most of the band is data the other party holds (when true per the auditor's rationale).

## Format
- 16:9. Build with the session's native slides artifact type when available, titled "[Effort] Council assessment — Briefing"; otherwise the pptx skill; otherwise a standalone HTML deck. Same structure regardless.
- Title slide kicker: "[Bench name] council · Round N · [Month Year]". Title is a full assertion. Subtitle: "A briefing on the council's method, early results and the data we need from you". Footer: "Round [round_id] · Confidential: prepared for [other party]".
- Every content slide: section kicker ("1 · Method", "2 · Score", "3 · Key insights", "4 · Data that would sharpen the analysis", "Next steps"), an assertion-led full-sentence headline, and the page footer plus finding IDs where the slide makes claims.
- Numbers with units and dates. Stat tiles for counts, bars for scores and distributions, two-column cards for "supports vs. against" and "risk vs. fix".

## The structure (scale insights 3–5; keep everything else)
1. **Title**.
2. **Method — the council**: "A council of [N] independent seats, one shared evidence ledger." Stat tiles: analysts / stakeholder seats / red team / neutral chair. Inputs line: how many supplied documents over what period, plus primary sources; seats never see each other's reasoning, only the ledger.
3. **Method — the process**: the phases by name; "The record" tile (evidence records · findings · conflicts · rulings); evidence-tier note (T1/T2/T3, assertions count as unverified until corroborated); the headline rule and how many headlines the auditor demoted.
4. **Score mechanics**: the bench's drivers, weights, what earns a 9–10 and a 0–2. Formula line and what widens the band.
5. **The score**: "[score_label]: [score] out of 100, plus or minus [band]" (round 2+: "moved from …"). Big number + band + horizon; per-driver bars; one line naming the highest driver and why. Disclaimers per source rules.
6. **Insights divider**: the round's one-sentence thesis, plus "[N] insights follow, each tied to findings in the ledger."
7–11. **Insight slides** (3–5): numbered kicker, assertion headline, body shaped to the evidence (stat tiles, a bar list with side notes, a two-column evidenced-position vs. what-it's-up-against pair, a measure/figure/so-what table, a risk/fix quadrant). Footer cites findings.
12. **Priority data requests**: "[N] items would do the most to narrow the ±[band]." Table: request · why it matters · driver it moves.
13. **Further data**, grouped by what it tests. Closing line: sharing something that already exists is enough; the finding it touches is rechecked next round.
14. **Questions**: "[N] questions the council could not answer from the record." Numbered, neutral, answerable.
15. **Next steps**: three horizons (now → near gate → next round), what would move the score, when the council re-runs. Close with: "The score is built to move."

## Archive
Export or save a copy to `benches/<bench>/efforts/<effort>/briefings/<round_id>-briefing.<ext>` and note it in the round's last `phases` record so the ledger records that a briefing was issued.
