---
slug: board-director
name: Board director
principal_role: Director, board chair or senior operator
organization: <fill in>
field: Any industry. The company the principal governs, runs or may join. <fill in the industry, the business model and the jurisdictions that matter>
noun: company
other_party: The company's management team
horizon: 3–5 years
preset: board-director
rebuttal: on
lookback_months: 24
created: 2026-10-20
---
# Bench — Board director

## The principal's seat
The principal is a director, board chair or senior operator assessing a company they govern, run or are considering joining. In this hat the principal can put items on the board agenda, ask management for information, vote on the matters reserved to the board (strategy, budget, capital, leadership, major transactions) and decide whether to join or stay. The principal cannot run the company day to day, cannot direct staff below the chief executive, and cannot act alone on matters reserved to the full board or to shareholders. The council addresses the principal in the third person, as "the principal", never "you"; every output should be forwardable to the rest of the board unedited.

## What this bench assesses
A company: an operating business with customers, a management team and a balance sheet, assessed as a whole. Typical efforts: an annual strategy review of a company the principal sits on; a board seat the principal has been offered; a company the principal runs, ahead of a plan refresh or a raise; a portfolio company under review. Two examples: a regional services company whose board the principal chairs, ahead of a three-year plan; a growth-stage software company that has offered the principal an independent director seat.

## The question the bench answers
score_label: Probability of value creation over 3–5 years

### Drivers
| key | driver | weight | 9–10 | 5–6 | 0–2 |
| --- | --- | --- | --- | --- | --- |
| standing | Industry standing | 20 | Top-three position in a growing segment; share gained over the last 24 months on third-party data; named rivals losing to it | Mid-pack in a flat or growing segment; share stable; rivals comparable in resources and momentum | Losing share; segment shrinking or consolidating against it; or no verifiable evidence of position at all |
| value_proposition | Competitive positioning and value proposition | 20 | Customers describe the differentiation in their own words and pay for it; documented wins against named rivals; substitutes priced out | Differentiation plausible but asserted mainly by the company; wins and losses mixed; price in line with rivals | Product interchangeable in the market's own comparisons; discounting or free pilots to close; a substitute does the job |
| operating | Operating strengths and execution | 15 | Delivery history meets plan; unit cost falling with scale; no single points of failure; service quality verified from outside | Plan credible but unproven; some fixed costs not scaling; known dependencies with a mitigation | Plan requires capabilities never demonstrated; SG&A growing faster than revenue; service failures visible publicly |
| runway | Financial runway and resilience | 15 | Self-funding or funded through the horizon; no customer, partner or contract above 25% of revenue; cash conversion healthy | Funded 18–24 months or dependent on a planned raise; one concentration above 25% with a mitigation | Funding need inside 12 months with no identified source; a concentration that could end the business; negative gross margin |
| regulatory | Regulatory position | 15 | Licences current and in the company's name; no revenue on a rule under review; clean enforcement history; compliance program tested | Perimeter mapped with one dependency on a rule in flux and a contingency for it | Core revenue rests on an exemption or flexibility with a sunset; enforcement history; licences in a predecessor's or an individual's name |
| capital | Capital and exit path | 15 | Several credible buyer types; recent precedents at supportive multiples; the exit story is the operating story | Buyer universe of two or three; comps from before a market reset; exit requires one more thing to be true | Buyer universe of one; exit depends on multiple expansion with no stated driver; financing closed for this asset type |

### Standards
Defaults per `skills/scoring`, plus: a score above 75 requires `runway` and `regulatory` both at 6 or higher.

## Assessment outline
Subject sections, in order: 1. Industry standing. 2. Competitive positioning and value proposition. 3. Operating strengths and weaknesses.
Stakeholder order: management, investor, customer-buyer, end-user, channel-partner, key-partner, supplier, employee, workforce-representative, regulator, policy-voice, legal-counsel.

## Roster
| seat | layer | default relevance | why it sits |
| --- | --- | --- | --- |
| financial | analyst | high | What the company earns, how repeatable it is, and the runway |
| market-competitive | analyst | high | The market it competes in, the rivals that matter, share won or lost |
| regulatory-policy | analyst | high | The licences and rules the revenue rests on, and what is changing |
| operating-model | analyst | high | How it delivers, what that costs, whether the plan is credible |
| product-positioning | analyst | high | What customers buy, in their words, against named rivals |
| valuation-precedent | analyst | high | What it could be worth in 3–5 years and to whom |
| management | stakeholder | high | Mirror of the people running it: their plan, and where the ledger disagrees |
| investor | stakeholder | high | The return on this equity over the horizon |
| customer-buyer | stakeholder | high | The one who pays: why they buy, why they would leave |
| end-user | stakeholder | moderate | The one on the receiving end, where that is not the buyer |
| employee | stakeholder | moderate | The workforce the plan depends on |
| channel-partner | stakeholder | moderate | The people who sell, recommend or refer it |
| key-partner | stakeholder | moderate | The platform or strategic partner it depends on: partner first, then threat |
| supplier | stakeholder | moderate | The inputs, capacity or network it cannot deliver without |
| regulator | stakeholder | moderate | The primary regulator or program official, from inside the agency |
| policy-voice | stakeholder | moderate | Where the legislature and administration are taking the rules |
| workforce-representative | stakeholder | low | Unions and professional bodies as a channel and as a barrier |
| legal-counsel | stakeholder | moderate | Litigation, contracts, IP, data and governance exposure |
| adversary | redteam | high | The best-placed rival with eighteen months to make the case fail |
| pre-mortem | redteam | high | The retrospective on how value was not created, written today |
| evidence-auditor | redteam | high | The chain behind every headline; never dropped |

(The seats/ folder is authoritative; this table is the readable index. `scripts/doctor.py` warns when they disagree.)

## Primary sources in this field
Field-free until the principal fills in the industry. Treat as T2 in any industry: the company registry and securities filings for the jurisdiction (SEC EDGAR, Companies House or the national equivalent); the register of whichever licences the business must hold; court dockets and regulator enforcement databases; official statistics for the segment; trade-association data; public procurement records; complaint datasets held by regulators or ombudsmen; patent and trademark registers. Add the industry's own list by extending `skills/exhaustive-retrieval/references/regulatory-sources.md` with a section for this field, and name the specific registers in each seat brief's Starting points.

## The other party
The company's management team. They may receive the question list and the briefing deck per `skills/briefing`: the method, the score, the insights, the data requests, the questions and next steps. They may not see driver rationales, individual findings, stakeholder views, the red team's work, or anything the principal supplied under board confidentiality.

## Confidentiality
Board packs, management accounts and anything else the principal supplies under board confidentiality go in the effort's `documents/` folder as T1 and are never quoted into another effort's ledger. Decide at setup whether `documents/` is committed or kept local; the default for board material is local. Where the principal is weighing a seat they have not yet taken, nothing supplied by the company during that process leaves the effort folder.
