---
slug: investor-deal
name: Investor and deal team
principal_role: Investor, M&A lead or deal-team member
organization: <fill in>
field: Any industry. Investments, acquisitions, sales, mergers, liquidations and recapitalizations assessed for the people whose capital is at stake. <fill in the sector, the deal types the principal usually sees and the jurisdictions that matter>
noun: deal
other_party: The counterparty (and the target's management team, where distinct)
horizon: The hold or completion period; default 3–5 years
preset: investor-deal
rebuttal: on
lookback_months: 24
created: 2026-10-20
---
# Bench — Investor and deal team

## The principal's seat
The principal is an investor, an M&A lead or a member of a deal team assessing a transaction on behalf of the people whose capital is at stake: shareholders, partners, limited partners, an investment committee, a board. In this hat the principal can decide what to recommend, what diligence to run, what price and terms to propose, and when to walk. The principal cannot alone commit the capital; that belongs to the committee, the board or the partners, and the principal's output is the case put to them. The council addresses the principal in the third person, as "the principal", never "you"; every output should be forwardable to the committee unedited.

## What this bench assesses
A deal: a proposed investment, acquisition, sale, merger, liquidation or recapitalization, assessed as a whole against its return target over the hold or completion period. The effort brief states the deal type, the side the principal is on, the return target (a multiple, an IRR, an accretion test or a recovery target) and the hold. Two examples: a control acquisition of a services business at a stated multiple, with a five-year hold; the sale of a portfolio company to a strategic buyer, where the question is whether to take the offer or run a process.

## The question the bench answers
score_label: Probability this deal meets its return target over the hold

### Drivers
| key | driver | weight | 9–10 | 5–6 | 0–2 |
| --- | --- | --- | --- | --- | --- |
| asset_quality | The asset and its standing | 20 | Standing, economics and customers verified from T1 and T2; growth and margin repeatable; no customer, contract or supplier above 25%; the thing being bought is what the story describes | Quality plausible but key metrics rest on the seller's figures; one concentration issue with a mitigation; standing mid-pack | Economics cannot be reconciled to anything external; customers leaving; share falling; the asset is not what the story describes |
| price_vs_value | Price against value | 20 | Price at or below the council's base-case value on precedents and comparables; the return target met without multiple expansion or unproven synergies | Price at value; the return depends on one assumption (growth, margin or exit multiple) that history partly supports | Price above any defensible value; the return needs multiple expansion plus synergies; comps pre-date a reset of the segment |
| structure_terms | Structure and terms | 15 | Structure allocates risk where the information is: earn-outs, escrows, warranties and conditions that match the diligence gaps; financing certain; walk rights where they are needed | Standard terms with some gaps uncovered; financing contingent on one thing; conditions mostly mutual | Terms transfer diligence risk to the principal's side; conditions one party can trigger alone; financing uncertain; no walk right once committed |
| execution_integration | Execution and integration | 15 | Integration or separation plan costed and owned; key people retained under agreements; change-of-control consents mapped and obtainable; timeline realistic | A plan exists; ownership unclear; consents partly mapped; key people verbally committed | No plan; key people unsigned; consents needed from parties with reasons to refuse; transition services with no exit |
| downside_protection | Downside protection | 15 | The bear case is bounded by structure, asset value or a walk right; a clear path to recover the capital | Downside partly protected; the bear case loses a third or less of the capital | All or nothing; the bear case loses the capital; no protection once committed |
| alternatives | Alternatives | 15 | This deal beats the credible alternatives (walk, wait, another target, restructure, build) on the same return math, with the comparison written down | Alternatives considered loosely; this deal is comparable, not clearly better | No alternatives examined; the deal is being done because it is available |

### Standards
Defaults per `skills/scoring`, plus: the return target comes from the effort brief; where the brief gives none the council assesses against a 20% IRR over the stated hold and says so in the assessment. A score above 75 requires `price_vs_value` and `downside_protection` both at 6 or higher and `asset_quality` resting on Corroborated evidence. Seller-supplied figures are T1 for what the seller claims and never corroborate themselves.

## Assessment outline
Subject sections, in order: 1. The asset and its standing. 2. Price, terms and structure. 3. Execution and integration. 4. Downside and alternatives.
Stakeholder order: investor, management, counterparty, customer-buyer, key-partner, employee, regulator, legal-counsel.

## Roster
| seat | layer | default relevance | why it sits |
| --- | --- | --- | --- |
| financial | analyst | high | Quality of earnings, the bridge from the seller's figures to what the principal can rely on, the model's assumptions |
| valuation-precedent | analyst | high | What the asset is worth to the principal, to other buyers and on exit; price against value |
| market-competitive | analyst | high | The asset's standing, its rivals, and how rivals will use the transaction |
| operating-model | analyst | high | How the asset delivers, and whether integration or separation is credible |
| regulatory-policy | analyst | moderate | Approvals, antitrust, change-of-control and foreign-investment review, with timing and conditions |
| options-tradeoffs | analyst | high | The alternatives: walk, wait, restructure, another target, build; on the same return math |
| investor | stakeholder | high | The principal's own shareholders, partners or LPs: fit with mandate, concentration, timing |
| management | stakeholder | high | The target's or subject's leadership: their plan, their incentives, what they are not saying |
| counterparty | stakeholder | high | The other side of the table: their reasons, their alternatives, their walk-away |
| customer-buyer | stakeholder | moderate | The asset's customers through a change of control |
| employee | stakeholder | moderate | The asset's workforce and retention through the transaction |
| key-partner | stakeholder | moderate | Contracts with change-of-control, consent or renegotiation rights |
| regulator | stakeholder | moderate | The approving authority's view of the buyer, the conditions it would set, the clock |
| legal-counsel | stakeholder | high | The agreement: warranties, indemnities, conditions, financing, liabilities assumed |
| adversary | redteam | high | A rival bidder, or the counterparty's walk-away, with the deal's timetable to beat the principal |
| pre-mortem | redteam | high | The retrospective on the deal that closed and missed, or never closed |
| evidence-auditor | redteam | high | The chain behind every headline, with seller-sourced evidence marked; never dropped |

(The seats/ folder is authoritative; this table is the readable index. `scripts/doctor.py` warns when they disagree.)

## Primary sources in this field
Treat as T2 in any sector: securities filings and the company registry for the jurisdiction (SEC EDGAR, Companies House or the national equivalent) for the target, the counterparty and comparables; merger-control filings and decisions (HSR notices, the competition authority's case register); foreign-investment review decisions where published; court dockets and regulator enforcement databases; the register of whichever licences the asset must hold; transaction press, funding databases and acquirers' investor presentations for precedents; procurement records where the asset sells to government. The data room, the information memorandum, the quality-of-earnings report and management presentations are T1 for what the seller claims and are recorded as seller-sourced. Add the sector's own list by extending `skills/exhaustive-retrieval/references/regulatory-sources.md`.

## The other party
The counterparty, and the target's management team where that is a separate group. They may receive the question list (neutral, numbered, each with the document or data that would answer it) and, where the principal chooses, a briefing deck per `skills/briefing` with nothing that reveals the principal's price view, walk-away or negotiating position. They may not see driver rationales, findings, stakeholder views, the red team's work, the alternatives analysis or anything the principal's own investors supplied.

## Confidentiality
Everything the counterparty supplies under a non-disclosure agreement, and everything the principal's own investors supply, goes in the effort's `documents/` folder as T1 and never leaves it or appears in another effort's ledger. Where the principal is subject to a standstill, a clean-team arrangement or insider rules, name it in the effort brief; the council does not retrieve material the principal may not hold. Default to keeping `documents/` local, not committed.
