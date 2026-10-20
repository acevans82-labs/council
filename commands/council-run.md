---
description: Start round 1 on a new effort (a company, idea, deal, decision, initiative or question) on the active bench. Runs intake in chat, then either runs the full council here or fires the cloud routine. If the effort already has a round, points you to /council-round.
argument-hint: <effort name> [notes] — or <bench>/<effort name> to target another bench
---

Start a council round 1 for: $ARGUMENTS

Steps, in order:

1. **Resolve bench and effort.** Read `council.md` for the active bench (a `bench/` prefix in the arguments overrides it). If no bench exists, run `/council-setup`. Derive a short slug for the effort. If `benches/<bench>/efforts/<slug>/ledger.json` or `score-history.json` exists, say a prior round exists and hand off to `/council-round` unless the principal insists on a fresh start (then archive the old effort folder as `<slug>-archived-<date>` first).
2. **Intake.** Read `benches/<bench>/bench.md`, then `skills/intake`, and run the round-1 batch in one message. Register attached documents in `documents/index.md`. Write `brief.md`. Say intake is complete in one line.
3. **Where to run.** If `council.md` records a cloud routine for this repo: commit the effort folder, push, and fire the routine with the payload `round <bench>/<slug>` (use a routine-trigger tool if this session has one; otherwise give the principal the payload to paste into "Run now" and stop). Tell them the result arrives as a pull request. If there is no cloud routine, run here: say it will take a while and the session stays open, then continue.
4. **Run here.** Read `agents/chair.md` and act as the chair for the rest of the round: roster and relevance ratings (tell the principal, do not wait), dispatch the analysts in parallel as subagents, each with the bench slug, effort slug, round ID, effort folder path, seat ID, seat-brief path, charter path and any specific instruction; merge with `scripts/merge_ledger.py`; conflict register; stakeholders; red team; rebuttal (unless the bench says off); answer pass; Evidence Auditor; synthesis per `skills/scoring`, `skills/assessment-output` and `skills/council-ledger`.
5. **Run to completion.** Pause mid-round only when the effort is ambiguous or a supplied document contradicts the round's premise. Batch everything else into "What the council needs from the principal."
6. **Close** with: the score label, the score and one-paragraph verdict; the assessment and dashboard files; and the numbered principal-requests list, Tier 0 first. Then one line: "Answer any of these with /council-round <slug> when you are ready; the council carries the rest forward."
