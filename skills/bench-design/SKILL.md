---
name: bench-design
description: "How to design a bench: the interview that turns a person's role, field and question into a configured council (bench.md plus a seats/ folder), either from a preset or from scratch. Covers the roster method (who decides whether the effort succeeds; what must be true), the scoring frame (drivers, weights, anchors, label), the assessment outline, and the default frames per kind of effort. Read by /council-setup and /council-bench, and by anyone editing a bench by hand."
---

# bench-design

A bench is one hat the principal wears: a role, a field, the kind of thing it assesses, the question it answers, and the seats that answer it. One person holds many benches (board member, founder, head of a function, parent). A bench is a folder:

```
benches/<slug>/
  bench.md          the hat, the question, the scoring frame, the roster index, the materials ladder
  seats/<id>.md     one seat brief per persona on the bench (the roster is this folder)
  context/          standing material every convening reads: the business or situation in brief,
                    glossary, strategy, org and people, prior decisions, house rules (see below)
  efforts/          one folder per thing the bench works on
```

Benches are cheap. Make one per hat, not one giant bench. Switching hats is switching the active bench.

## The interview (one batch, skip what is known)
1. **The hat.** Your role title in this hat, and the organization or "personal". What you can decide alone in this role, and what you cannot.
2. **The field.** The industry, discipline or domain, in a sentence. The jurisdictions that matter.
3. **What the bench assesses.** Pick a noun: company, idea, deal, decision, initiative, question, or your own. Give two example efforts.
4. **The question.** In one sentence, what the council should answer about each effort, with a horizon ("probability of value creation over 3–5 years", "should we proceed, and what has to be true", "likelihood this delivers its objective by Q3", "which option best serves [goal] over the next two years").
5. **Who decides whether an effort succeeds.** The people and bodies whose reaction matters: customers, users, partners, regulators, investors, staff, family, a counterparty. Each becomes a stakeholder seat.
6. **What must be true.** The facts that have to hold: the numbers, the market, the rules, the feasibility, the evidence base. Each becomes an analyst seat.
7. **The other party.** Who receives a briefing after a round (a management team, a counterparty, a vendor, nobody).
8. **Confidentiality.** Anything that never leaves the effort folder; whether documents should be committed or kept local.
9. **Context.** What every convening should already know before it starts: a page on the organization or situation, a glossary, the current strategy or plan, who is who, decisions already made, rules of the house. Collect what exists now into `context/`; list what to add later in `context/README.md`.
10. **Materials.** What material a serious assessment needs on this bench (a board deck, financials, a plan, a study, a budget) and what a lighter one can do without. This becomes the materials ladder.
11. **Preset.** Offer the presets whose noun and role match (`presets/*/bench.md`, read their frontmatter). The principal picks one to adjust, or builds from scratch.

## Roster method
- **Analysts** (phase 2) establish facts. Four to eight. Always include whichever of `financial`, `market-competitive`, `regulatory-policy`, `operating-model`, `research-evidence`, `options-tradeoffs`, `technical-feasibility`, `product-positioning`, `valuation-precedent` the "what must be true" answer implies.
- **Stakeholders** (phase 4) react from a seat. Four to twelve. One per constituency from "who decides". Map each to a library persona (`agents/`) and write a seat brief that names the sub-voice; if none fits, write a custom seat per `skills/seat-authoring`.
- **Red team** (phase 5): always `adversary` (the best-placed rival, opponent or skeptic), `pre-mortem`, and `evidence-auditor`. Never drop the auditor.
- The chair is always present and is not a seat file.
- Give each seat a default `relevance` (high / moderate / low). The chair re-rates per effort and drops Low stakeholders.

## Scoring frame
Four to eight drivers, weights summing to 100, each with anchors for 9–10, 5–6 and 0–2. Derive them from the question: what would have to be strong for the answer to be yes. Name the `score_label` in words. Add standards (thresholds) if the field needs them. Default frames by noun are below; adjust, do not copy blindly.

### Default frames
**company** (label: Probability of value creation over [horizon]): standing 20 · value_proposition 20 · operating 15 · runway 15 · regulatory 15 · capital 15.
**idea** (label: Probability this venture reaches [milestone] by [horizon]): problem_demand 20 · solution_differentiation 20 · market_timing 15 · economics 15 · team_execution 15 · capital_risk 15.
**deal** (label: Probability this deal returns [target] over [horizon]): asset_quality 20 · price_vs_value 20 · structure_terms 15 · execution_integration 15 · downside_protection 15 · alternatives 15.
**decision** (label: Likelihood this choice serves [goal] over [horizon]): fit_with_goals 20 · evidence_it_works 20 · cost_affordability 15 · reversibility_risk 15 · effect_on_people 15 · timing 15.
**initiative** (label: Likelihood this initiative delivers its objective by [date]): objective_value 20 · feasibility 20 · resourcing 15 · risk_compliance 15 · buy_in 15 · timing 15.
**question** (label: Confidence that the evidence supports the council's answer): evidence_quality 25 · consensus 20 · mechanism 20 · applicability 20 · counter_evidence 15.

## The context folder
`context/` is how the bench is "trained in" the business or the situation. Every convening reads it first, at every depth, and personas cite it as T1 ("context: strategy.md, section 2"). Keep it to what is stable across efforts; effort-specific material goes in the effort's `documents/`. Typical files: `overview.md`, `glossary.md`, `strategy.md`, `people.md`, `decisions.md`, `house-rules.md`. A `README.md` lists what is there and what is still wanted. A tighter harness (a company deployment) is a bench with a locked context folder, a locked source list and a depth cap in `## Depth profiles`.

## The materials ladder
Three lines in `bench.md` under `## Materials ladder`, one per depth, naming what the gate in `skills/intake` expects:
```
quick: nothing beyond the context folder
standard: <e.g. a management summary or plan, and the latest numbers>
deep: <e.g. the board deck, financial statements, contracts or the study base>
```
Add `materials_gate: hard` to the frontmatter when a convening must not proceed blind.

## Depth profiles
Defaults live in `skills/convening`. A bench that needs different cells writes only those under `## Depth profiles` as `profile.lever: value` lines (for example `standard.lookback_months: 120`, `deep.max_depth: standard`, `deep.chair_model: <id>`).

## Assessment outline
Name the subject sections the assessment writes after the score (three to five), in order, and the stakeholder order. For a company: industry standing; competitive positioning and value proposition; operating strengths and weaknesses. For an idea: problem and demand; solution and differentiation; timing and economics. For a decision: the options; the evidence; the costs and reversibility; the people affected.

## bench.md
```
---
slug: <slug>
name: <display name of the hat>
principal_role: <role title>
organization: <org or personal>
field: <one line>
noun: company | idea | deal | decision | initiative | question | <own>
other_party: <who gets the briefing, or none>
horizon: <period>
preset: <preset slug or custom>
rebuttal: on
lookback_months: 24
created: YYYY-MM-DD
---
# Bench — <name>

## The principal's seat
One paragraph: who the principal is in this hat, what they can decide, what they cannot, how the council should address them (never "you" in outputs).

## What this bench assesses
The noun, the typical efforts, two examples.

## The question the bench answers
score_label: <words>

### Drivers
| key | driver | weight | 9–10 | 5–6 | 0–2 |
| --- | --- | --- | --- | --- | --- |

### Standards
Thresholds, or "defaults per skills/scoring".

## Assessment outline
Subject sections in order; stakeholder order.

## Roster
| seat | layer | default relevance | why it sits |
| --- | --- | --- | --- |
(The seats/ folder is authoritative; this table is the readable index. `scripts/doctor.py` warns when they disagree.)

## Materials ladder
quick: …
standard: …
deep: …

## Depth profiles
(optional; only the cells that differ from skills/convening)

## Primary sources in this field
What counts as T2 here; the registers, regulators, journals and databases a persona should check first.

## The other party
Who they are, what they may see, what they may not.

## Confidentiality
```

## After writing
Create `context/README.md`. Run `python3 scripts/doctor.py` and fix what it reports. Add the bench to the index in `council.md`. Tell the principal the roster in one compact table and the question in one line, and offer to start the first effort.
