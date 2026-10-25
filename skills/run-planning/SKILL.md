---
name: run-planning
description: "Plan every council run with the principal before anything is dispatched: a dollar ceiling, the phases, research tracks and seats, a model per seat with one line of why, a cost estimate from measured per-seat figures, a one-screen summary of the job and its deliverables, and the principal's go. Writes the '### Model plan' table into the effort brief, which the chair and the cloud orchestrator dispatch from. Read by /council-run, /council-round and /council-consult (standard and deep, and any quick consult that dispatches more than three seats) right after intake, always in the local thread."
---

# run-planning

A council run spends real money. The principal decides how much before it starts, sees what the money buys, and says go. Nothing is dispatched, locally or in the cloud, until then.

Planning always happens **in the local thread**, right after intake, with the principal present. The cloud routine never plans; it reads the plan from the brief. An unplanned cloud round stops with `PLAN NEEDED` (see `orchestrator/orchestrate.md`).

## When it runs
- Every standard or deep convening (`/council-run`, `/council-round`, `/council-consult standard|deep`).
- A quick consult that dispatches more than three seats, or any seat on the strongest model. A quick consult of three seats or fewer on the default ladder needs no plan; say "quick, three seats, about $3 to $8" in one line and go.
- A resumed round: re-plan only what is left (the remaining phases), and keep what was spent as a line in the receipt.

## The questions, in one message
Skip any the conversation already answered; say what you assumed.
1. **Ceiling.** What is the dollar ceiling for this run (and for the next round, if known)?
2. **Milestone.** What exactly is being scored this time, and what is out of scope?
3. **Tracks.** Which research tracks matter most, in order? Anything that can run lighter or sit out?
4. **Seats.** Any guest seat to add, or seats that can sit out?
5. **Models.** Any model off the table? (Default: none; the plan optimises value per dollar.)
6. **Where.** Here in this thread, or the cloud routine? (Cloud is the default for a round when `council.md` records a routine.)

## The model ladder
| Use | Model | Why |
| --- | --- | --- |
| Chair: intake, rulings, scoring, synthesis | the strongest model the account has (`fable`, else `opus`) | judgment, legal exposure and valuation live here |
| Evidence auditor | the strongest model | a wrong fact costs the most at verification |
| Research-heavy analysts, the adversary, seats carrying legal exposure, the buyer, the founder's mirror | `opus` | multi-source digging and reasoning |
| Bounded analysts, narrow stakeholders, the pre-mortem, every rebuttal | `sonnet` | re-reading a ledger that already holds the facts |
| Helpers a seat spawns to count, read pages or list sources | `sonnet` or `haiku`, at most two per seat | cheap, disposable, no judgment needed |

Rules the plan applies without asking:
- A seat may spawn at most two helpers and writes its own file itself.
- Never lower the chair or the auditor to save money. Cut helpers, narrow seats and the second sitting first; then drop to standard depth; then drop Low-relevance stakeholders.
- If the principal planned on the strongest model throughout, do not argue the plan, only the arithmetic.

## Estimating
Use measured figures. Per seat run, at API prices (October 2026; `scripts/cost_report.py` holds the price table):

| Seat run | Typical | Heavy research seat |
| --- | --- | --- |
| `haiku` helper | $0.05 to $0.20 | $0.30 |
| `sonnet` | about $1 | $2 |
| `opus` | $2 to $4 | $6 |
| `fable` | $6 to $10 | $15 |
| chair, per phase it runs (`fable`) | $3 to $8 | $12 at synthesis |

Whole runs, measured: a standard round with every seat on `opus` about $90; a deep round on the ladder $150 to $220; a deep round all on `fable` $350 to $500; a quick consult with three research seats about $25.

Before estimating, read the effort's last `assessments/<round_id>-cost.md` if one exists and correct the per-seat figures with what that round actually measured. Say so ("estimates use r1's measured costs").

Add a 15 percent margin and round to the nearest $5. If the estimate exceeds the ceiling, say by how much and propose cuts in the order above until it fits; never silently trim.

Subscriptions are not metered per token; these figures are what the same work costs at pay-per-token rates. Web-search fees and the app's own summarising are not included.

## Headroom on the account
Before showing the summary, read the account's limits. In Claude Desktop that is `get_usage`: `plan.windows` (the 5-hour, weekly and per-model weekly limits, percent used and reset time) and `plan.extraUsage` (whether extra usage is on, `spent` and `monthlyLimit`). What it means for the plan:
- **A model's weekly allowance at or near 100%** (often the strongest model): seats on that model draw extra usage, which is billed in dollars. Treat the plan's estimate for those seats as real money.
- **Extra usage headroom** is `monthlyLimit - spent`. If the plan's estimate for seats that would draw extra usage exceeds the headroom, the run will stop at the limit partway through. Say so, and offer the choices: raise the monthly limit (claude.ai/settings/usage), move seats to a model with weekly allowance left, run at a lower depth, or wait for the reset date.
- **Extra usage off** and the strongest model's weekly allowance used up: those seats cannot run until the reset; plan them on the next model down or wait.
If the reading is unavailable (an API key, another host), say "account limits not read" and continue.

## Search budget
Web search is capped at 200 calls per chair turn, shared by every subagent launched in that turn. So the plan dispatches **in groups of at most three seats per turn**, and gives every seat a search budget: 40 web searches by default (a bounded seat 20, a rebuttal 10), read sources with WebFetch rather than searching again, and log the rest as gaps if search runs out. Write the group order into the plan.

## What goes into the brief
Under the round's `## Round parameters`, exactly this shape (the chair, the orchestrator, the doctor and `scripts/cost_report.py` all parse it):

```
### Model plan
ceiling: $250 · estimate: $185 · depth: deep · where: cloud · approved: 2026-10-24 by the principal
| phase | seats | model | est $ | why |
| --- | --- | --- | --- | --- |
| chair | intake, rulings, scoring, synthesis | fable | 35 | judgment and valuation |
| 2 | market-competitive, financial, technical-feasibility | opus | 12 | deep research |
| 2 | product-positioning, options-tradeoffs | sonnet | 2 | bounded questions |
| 4 | management, customer-buyer, legal-counsel | opus | 10 | move the score or carry exposure |
| 4 | end-user, channel-partner | sonnet | 2 | narrow lenses |
| 5 | adversary | opus | 4 | must out-think the plan |
| 5 | pre-mortem | sonnet | 1 | pattern work |
| 6 | all rostered stakeholders | sonnet | 6 | one bounded pass |
| 7 | answering analysts | opus | 8 | close the challenges |
| 8 | evidence-auditor | fable | 10 | verification |
Groups: at most three seats per turn, in the order listed. Search: 40 per seat (bounded seats 20, rebuttals 10).
Helpers: at most two per seat, on sonnet or haiku; the seat writes its own file.
```

- `phase` is the phase number from `agents/chair.md` (`chair` for the chair's own work across phases).
- `est $` is the estimate for that whole row; the rows sum to the `estimate`.
- `approved:` is written only after the principal says go, with the date. No `approved:` line means the plan is a draft and nothing is dispatched.
- Seats the table does not name run on the chair's model and are reported as unplanned in the receipt.

## The one-screen summary (the gate)
Before asking for go, show one screen, plain English, no jargon:

```
**The job:** <the question this run answers, one sentence>
**Depth and where:** deep, in the cloud (about 3 to 5 hours; the result arrives as a pull request)
**Seats:** 14 of 18 (dropped: <names and why>); guest: <name, if any>
**Models:** chair and auditor on Fable; 7 research seats on Opus; 6 bounded seats on Sonnet
**Cost:** about $185 against a $250 ceiling (estimate from <source>)
**Account:** Fable weekly allowance used up (resets <date>), so about $120 of this draws extra usage; $600 left of the $2,000 monthly limit
**You will get:** the assessment, the dashboard, the ledger, the requests list for next round, and a cost receipt
**What it will not cover:** <out of scope, one line>
```

Then ask with buttons: **Go**, **Change the plan**, **Cancel**. On Go, write `approved:` into the plan, commit the brief, and only then dispatch or fire the routine. On Change, edit and show the screen again. A change to the ceiling, depth or models after approval is a new approval.

## Recording what was used
The chair records the model actually used per seat in the phase minutes (`phases[].summary`), names each dispatch `p<phase> <seat_id>` (so `cost_report.py` can map spend to phases), and passes every seat its search budget and the helper rule. At the close, `skills/round-close` writes the cost receipt against this plan.
