---
slug: functional-leader
name: Functional leader assessing an initiative
principal_role: <fill in: head of the function, e.g. Head of Regulatory and Compliance, VP of AI R&D, Director of Product, Head of Operations>
organization: <fill in>
field: <fill in: the function and the company in one line, e.g. "regulatory and compliance at a conversational-AI company" or "AI R&D at a mid-size logistics firm"; the jurisdictions that matter>
noun: initiative
other_party: the executive sponsor or steering group
horizon: the initiative's target date, default 6–18 months
preset: functional-leader
rebuttal: on
lookback_months: 24
created: 2026-10-20
---
# Bench — Functional leader assessing an initiative

This preset is meant to be copied once per function and the `field` line filled in. The seats read the field and speak in that lane: the regulator seat for a compliance function is a different regulator from the one an HR function faces; the end-user of a product initiative is a customer, the end-user of a finance initiative is a budget holder. A principal who leads several functions, or who wears the hat for several companies, makes several benches rather than one broad one.

## The principal's seat
The principal leads a function inside an organization and is assessing an initiative, a plan or a decision inside that lane: a new process, a program, a tool or platform adoption, a reorganization, a policy, a research direction, a go-to-market change. The principal can decide alone within the function's budget and mandate, can propose beyond it, and cannot decide what the executive sponsor, peer functions, the budget committee or the external customer will do. The council addresses the principal in the third person as "the principal" or by role title, never "you". The principal may be the initiative's proposer or its reviewer; say which at intake, since it changes what the `management` seat mirrors.

## What this bench assesses
An initiative: a bounded piece of work with an objective, an owner, a budget and a target date. Examples: standing up a model-evaluation program before a regulatory deadline; moving the function's core workflow to a new platform by the end of the fiscal year.

## The question the bench answers
score_label: Likelihood this initiative delivers its objective by its target date

The objective and the date are named at intake. If the objective is stated as an activity ("implement the tool") rather than an outcome, the council restates it as the outcome the sponsor would accept and says so.

### Drivers
| key | driver | weight | 9–10 | 5–6 | 0–2 |
| --- | --- | --- | --- | --- | --- |
| objective_value | The objective and what it is worth | 20 | The objective is stated as a measurable outcome the sponsor has signed, its value is quantified against a baseline, and the function's own numbers support it | The objective is clear but its value is asserted rather than measured; the baseline is approximate; the sponsor agrees in principle | The objective is an activity, a slogan or a mandate from above with no stated benefit; nobody can say what "done" looks like |
| feasibility | Can it be done as planned | 20 | The approach has been done before in a comparable organization, the dependencies are known and in hand, and the hard part has been tried in a pilot | The approach is sound, one or two dependencies are unconfirmed, and the hard part is understood but untested here | The approach has not worked elsewhere, or depends on a capability the organization does not have and has no plan to acquire |
| resourcing | People, money and time | 15 | Budget is approved, named people are assigned at the stated share of their time, and the plan has slack | Budget is likely but not approved; people are named but still fully committed elsewhere; no slack | No budget line; the team is "to be identified"; the plan assumes overtime or a vendor that has not been engaged |
| risk_compliance | Risk and compliance exposure | 15 | Legal, regulatory, security and ethical reviews are done or scheduled with owners; the residual risks are named and accepted by someone with authority | Reviews are planned but unscheduled; risks are listed without owners; one material exposure is unresolved | No review planned; a rule, contract or policy the initiative touches has not been read; a risk is known and undocumented |
| buy_in | Organizational buy-in | 15 | The sponsor, the delivering team and the internal users have said yes in writing or in action, and the peer functions that could block it have been consulted | The sponsor is supportive, the team is willing, the users and peers have not yet been asked | The sponsor is lukewarm or has changed, the delivering team has pushed back, or a peer function has a competing initiative |
| timing | Timing and the target date | 15 | The date is derived from the plan rather than imposed; the plan has a critical path with slack; the external deadline (if any) is confirmed | The date is imposed but reachable if nothing slips; no slack; the external deadline is assumed | The date predates the dependencies it needs; the plan has no critical path; a similar initiative here slipped by more than half its length |

### Standards
Defaults per skills/scoring. In addition: a score above 70 requires buy_in at 6 or higher, since an initiative the delivering team has not accepted does not deliver on time regardless of its merits.

## Assessment outline
Subject sections, in order: the objective and its value; feasibility and resourcing; risk and compliance; organizational buy-in and timing.

Stakeholder order: management (the sponsor and leadership), employee (the delivering team), end-user, customer-buyer, key-partner, legal-counsel, regulator, values-ethics.

## Roster
| seat | layer | default relevance | why it sits |
| --- | --- | --- | --- |
| options-tradeoffs | analyst | high | The real options including doing nothing, the smaller version and the rival approach; the cheapest test between them |
| operating-model | analyst | high | Execution: the plan, the critical path, the dependencies, the capacity of the team that delivers |
| financial | analyst | high | Budget, cost to deliver, cost to run, and the value against the baseline |
| technical-feasibility | analyst | high | Whether the approach, tool or capability can be built or adopted here by the date |
| regulatory-policy | analyst | high | The rules, standards and internal policies the initiative must satisfy, and the ones it changes |
| research-evidence | analyst | high | What the literature, benchmarks and case evidence say about whether this kind of initiative works |
| market-competitive | analyst | moderate | What peer organizations and vendors do, and how this initiative compares |
| management | stakeholder | high | The executive sponsor and leadership: what they expect, what they will fund, what they will drop |
| end-user | stakeholder | high | The internal users or the customers the initiative touches; decides whether it is adopted |
| employee | stakeholder | high | The team that has to deliver it; decides whether the plan is real |
| customer-buyer | stakeholder | moderate | The external customer where the initiative reaches them; moderate by default, raised when it does |
| legal-counsel | stakeholder | high | Contracts, liability, employment and data terms the initiative creates or breaks |
| regulator | stakeholder | moderate | The primary regulator or program official for this function; raised to high in regulated lanes |
| key-partner | stakeholder | moderate | The vendor or platform the initiative depends on; raised when the initiative is an adoption |
| values-ethics | stakeholder | moderate | Whether the initiative is one the organization would defend in public; raised for AI, data, workforce and safety initiatives |
| adversary | redteam | high | The strongest case for the status quo or for the rival approach |
| pre-mortem | redteam | high | The initiative missed its date; the stories and the early signals |
| evidence-auditor | redteam | high | Grades the plan's claims, the value case and the buy-in evidence |
(The seats/ folder is authoritative; this table is the readable index. `scripts/doctor.py` warns when they disagree.)

## Primary sources in this field
T1 is what the principal supplies: the initiative charter, the plan, the budget request, the sponsor's brief, prior status reports, internal policies, vendor proposals. T2 in this field: the function's primary regulator or standards body and its guidance; statutes and rules the initiative touches; peer-reviewed and official research on the approach; industry standards; the organization's own audited numbers where supplied. T3: vendor material, analyst reports, conference talks, peer case studies, practitioner forums. Replace the fill-in prompts in the seat briefs with the regulator, standards and vendors of the actual function.

## The other party
The executive sponsor or steering group. They may see the question list, the briefing per skills/briefing and the assessment if the principal chooses to share it. They may not see the principal's intake notes, the principal's beliefs-to-test, or any document the principal marked as held back at intake. The `management` seat mirrors their position as the council understands it; it is not a channel to them.

## Confidentiality
Internal documents, budgets, personnel names and vendor proposals stay in the effort folder and are never quoted into another effort, including another effort on another of the principal's benches. The council reads what the principal supplies and what is public; it does not contact vendors, regulators or colleagues. Keep documents uncommitted by uncommenting the `documents/` line in `.gitignore` if the repository is shared.
