---
name: convening
description: "How deep the council goes when it is convened: the three depth profiles (quick, standard, deep), the levers behind them (seats, phases, retrieval, models, sittings, budget), how a bench overrides them, how the chair adds a guest seat for one convening, and the quick-consult procedure that produces a memo instead of a round. Read by /council-consult, /council-run, /council-round and the chair before any convening."
---

# convening

"Consult the council" is one verb. What changes between a ten-minute consult and an all-day deep dive is not who you ask but how far they go: how many seats sit, which phases run, how hard they retrieve, which models think, how many times they convene, and how much time and budget they burn. Those are the levers. A **depth profile** fixes them.

## The three profiles

| Lever | quick | standard | deep |
| --- | --- | --- | --- |
| Time box | 5–10 minutes | 30–60 minutes | hours; cloud by default |
| Budget | about $3–25 | about $60–120 | about $150–220 on the ladder; set by the principal in the plan |
| Seats | the chair picks up to 5 from the roster for this question | every rostered seat at Moderate relevance or better | every rostered seat, plus guest seats if the question needs one |
| Phases | one sitting: chosen seats in parallel, chair synthesis | roster · analysts · conflict register · stakeholders · red team (adversary, pre-mortem) · auditor · synthesis | all nine, including rebuttal and the answer pass; optionally a second sitting |
| Retrieval | supplied material, the context folder and the ledger; one shallow web pass per seat | the full source order, 12-month lookback unless the bench says otherwise | the full `skills/exhaustive-retrieval` doctrine, bench lookback, browser where needed |
| Auditor | spot-check: the chair's headline claims only | audits headlines and Low-rated seats | full audit including rebuttals |
| Models | the ladder in `skills/run-planning` (plan needed only above three seats) | per the approved plan (`skills/run-planning`) | per the approved plan; chair and auditor on the strongest model |
| Sittings | 1 | 1 | 1, or 2 when the first sitting leaves Tier 0 conflicts the chair can resolve with one more pass |
| Output | a consult memo, no score | a scored round (condensed) | a scored round (full) |
| Writes | `consults/<consult_id>-memo.md` | a round: ledger, assessment, requests, dashboard | a round: ledger, assessment, requests, dashboard |
| Counts as a round | no | yes | yes |

Before any standard or deep convening, `skills/run-planning` runs in the local thread: a dollar ceiling, a model per seat, an estimate, a one-screen summary, and the principal's go. A convening at `standard` or `deep` **is a round** and follows `agents/chair.md` with the phases the profile names. A convening at `quick` is a **consult**: it reads the ledger and writes a memo, never ledger records, so it costs nothing to ask and promises nothing it did not check.

Defaults: `/council-consult` is quick; `/council-run` and `/council-round` are deep. Any of them takes `quick`, `standard` or `deep` as a word in the arguments. The cloud payload carries it the same way (`round <bench>/<effort> standard`).

## Bench overrides
A bench may carry a `## Depth profiles` section in `bench.md` that changes any cell for that bench, for example a research bench that wants `standard` to keep the 120-month lookback, or a company-harnessed bench that caps every convening at `standard` and names the model per layer. Write only the cells that differ, as `profile.lever: value` lines. A convening may override one lever in the arguments ("deep, but skip rebuttal"); the chair records the profile actually used in `effort.depth` and the phases minutes.

## Guest seats
When the question needs an expert the bench does not seat (a question about a tariff on a bench with no trade seat), the chair adds a **guest seat** for this convening: a seat brief written per `skills/seat-authoring`, usually `domain-expert` or `regulator` with a lens, saved to `seats/` and flagged `guest: true` in its frontmatter. The guest sits with full standing. After the convening the chair says in the close which guests were added; the principal keeps them (remove the flag) or drops them (delete the file). A bench of twenty seats is normal; the chair's relevance rating is what keeps a sitting small.

## Quick consult procedure
1. **Frame.** Restate the question in one line and name the effort it belongs to (an existing effort, or a new one created with a two-line brief). Read `bench.md`, the context folder, the effort brief, and the ledger if there is one.
2. **Materials.** Apply the materials gate from `skills/intake`: say in one line what the bench's ladder expects at this depth and what is present.
3. **Pick seats.** Up to five, by relevance to the question, named with one clause each. Add a guest seat if nothing on the bench covers the question.
4. **One sitting.** Dispatch the chosen seats (at most three per turn; a fourth and fifth go in a second group) with the question, the paths, and the `quick` profile. Each returns five lines per `skills/persona-protocol`: what it can say from the ledger and supplied material, what it found in its one shallow pass (with locator and date), its confidence, what it could not check, and what it would need. Seats cite ledger IDs where they exist; new facts are cited inline with tier and reliability but are not written to the ledger.
5. **Synthesize.** The chair writes the memo:
   ```
   # Consult — <question>   (<bench>/<effort>, <consult_id>, quick)
   ## Answer   (3–6 sentences, confidence High/Moderate/Low with the reason)
   ## What it rests on   (ledger IDs and inline citations; "not checked" is a valid entry)
   ## Where the seats disagreed
   ## What a round would add   (the seats, phases and material that would change the confidence)
   ## Promote?   one line: "say 'promote' to make this the next round's trigger"
   ```
   Save to `efforts/<effort>/consults/<consult_id>-memo.md` (`consult_id` = `k<N>-<YYYYMMDD>`) and append a line to `consults/index.md`.
6. **Promote.** If the principal says promote, the memo's question becomes the next round's trigger and its inline citations are registered as `E-` records at that round's intake. Nothing else carries.

## Standards at every depth
- Confidence and citations are never thinner at quick; the memo says "not checked" instead of guessing.
- The materials gate applies at every depth; a deep convening on thin material runs blind and says so.
- The profile used is written on every output (memo header, assessment header, dashboard meta line).
