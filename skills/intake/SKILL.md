---
name: intake
description: "Intake for a council round. On round 1 of an effort, interviews the principal in one batch about the effort, the beliefs to test, the concerns, the other party and the supplied documents, and writes brief.md. On round 2 and later, collects the principal's answers to the last round's requests first, then the trigger, new documents and scope, and applies carry-forward. Runs before the chair; never forms views."
---

# intake

The principal is busy. Ask in one batch, skip what is already answered in the conversation or the effort folder, and say what you are assuming. Intake always happens in chat with the principal; a cloud round never interviews anyone.

## The effort folder
`benches/<bench>/efforts/<effort>/` holds everything for one effort:
```
brief.md                intake output, updated each round (answers accumulate in it)
documents/              supplied T1 material, with index.md (name, type, date received, pages)
ledger.json             current round's ledger (prior rounds archived under rounds/)
rounds/<round_id>/      per-persona files and the archived ledger for that round
score-history.json      one line per round
assessments/            assessment and principal-requests markdown per round
dashboards/             council-ledger HTML per round
briefings/              decks for the other party, when produced
```
Create the folder on first use. Slugs are short and lowercase (`acme`, `series-b`, `school-choice`). Round IDs are `r<N>-<YYYYMMDD>`.

## The materials gate (every convening, every depth)
Read the bench's `## Materials ladder` (see `skills/bench-design`): what supplied material each depth expects. Compare it with `documents/index.md` and the bench's `context/` folder. Then say, in one line, one of:
- **cleared**: the material the ladder names for this depth is present;
- **downgraded**: material for the requested depth is missing, so the convening runs one depth lower (say which items would restore it);
- **blind**: the principal asked to proceed anyway; the convening runs at the requested depth, the band widens per `skills/scoring`, every missing item becomes a Tier 0 request, and every output header carries "blind: <items>".
The principal chooses between downgraded and blind; the default is downgraded. A bench may make the gate hard (`materials_gate: hard` in its frontmatter), in which case blind is not offered and the convening stops until the material arrives.

## Depth
Every convening has a depth, `quick`, `standard` or `deep`, per `skills/convening`. Record it in `effort.depth` for a round and in the memo header for a consult. Ask only if neither the command's default nor the arguments settled it.

## Round 1: the batch
Read the bench first (`benches/<bench>/bench.md`) so the questions use its words: its noun, its other party, its horizon. Read `benches/<bench>/context/` too; anything already answered there is not re-asked. Then ask together, one message:
1. The effort in the principal's words: what it is, for whom, how it works today; the exact thing to assess (the legal entity, the specific idea, the decision as a yes/no, the question as a sentence).
2. The principal's role in it and what T1 material can be supplied now.
3. The case for it, as its proponents state it, in two or three sentences (management's strategy, the founder's pitch, the plan's objective, the argument for the choice).
4. What the principal believes is true that the council should test rather than assume.
5. What the principal is most concerned about.
6. Any seat to emphasize or leave off this round; any rival, jurisdiction, alternative or expert view to make sure the council covers.
7. Documents: attach now, or say what will come later. Each is registered in `documents/index.md`. Name the ladder items for the requested depth so the principal knows what the gate wants.
8. Horizon and weights: confirm the bench's defaults or change them for this effort only.
9. Standing watch: whether this effort should be watched between rounds (`skills/standing-watch`); if yes, the terms and cadence.

If the principal has already covered items in the conversation, do not re-ask; list the assumptions in the brief.

## Round 2 and later: the batch
If a promoted consult memo or a watch brief triggered this round, read it first; its question is the trigger and its citations are registered as `E-` records before anything else.
Open by listing the open requests from the last round (`judgment_calls` without `answer`, gaps with `raised_to_principal: true` and status `not_found`, unresolved conflicts), by ID, Tier 0 first. Then ask together:
1. Answers to any of those, by ID. Partial is fine; the council carries the rest forward.
2. What prompted this round (a document arrived, something moved, a deadline is near, time has passed, or "refresh").
3. New documents to register.
4. Full re-run of every seat, or only the seats the trigger and the answers touch (default: scoped; the chair decides which and says so).

Then:
- Write each answer into the carried `J-` record (`answer`, `answered_at`, `answered_in_round`) and as a new T1 `E-` record with locator "principal answer, round N".
- Archive the prior ledger to `rounds/<prior_round_id>/ledger.json`.
- Apply carry-forward per `skills/evidence-ledger`: evidence, conflicts, gaps and judgment calls carry; findings, rulings and the prior assessment do not; evidence older than 90 days is re-verified; score history carries whole.
- Update `brief.md`: append a "Round N answers" section and the new trigger.

## Confidentiality
Documents and facts supplied for one effort are stored in that effort's folder and are never read during another effort's round. If a supplied document contains personal identifiers, note it in the index and instruct personas to use aggregate figures only. Benches may add rules of their own.

## Output: brief.md
```
# Brief — [Effort name]
Bench: [bench name] · Noun: [noun] · Other party: [who]
## Identity
What it is, who it is for, the exact thing to assess, the principal's role, slug
## The case as its proponents state it
## Beliefs to test
## Stated concerns
## Roster notes
Seats emphasized or excluded; rivals, jurisdictions, alternatives or experts to cover
## Supplied documents
From documents/index.md
## Round parameters
round_number, round_id, date, depth, materials gate result, trigger, prior-round mode, horizon and weight changes
## Round N answers   (one section per later round, newest last)
J-012: [answer] · G-004: [answer] · …
```
Then tell the principal intake is complete in one line and hand off to the chair, or to the cloud routine when the round runs there.
