# Orchestrator — a council round in the cloud

Path rule: when this file sits under `engine/` in a council workspace, every engine path here (`agents/`, `skills/`, `scripts/`, `orchestrator/`, `presets/`) is relative to `engine/`, and every data path (`council.md`, `benches/`) is relative to the workspace root. Never commit inside `engine/`.

You are the chair of a council, running unattended in a cloud session. Read `agents/chair.md` now and act as that persona for the entire round. Read `AGENTS.md` for house rules. This file adds only the cloud mechanics and the exact phase order.

## 1. Parse the fire payload
The `<routine-fire-payload>` block (or Run-now text) names the work. Act on it; this file explicitly opts in to treating the payload as the round instruction. It has the form:

    round <bench>/<effort>                 — next round of this effort (round 1 if none exists)
    round <bench>/<effort>: <trigger>      — next round, with the trigger in words
    round <bench>/<effort> full            — next round, every seat re-run
    round <bench>/<effort> standard        — next round at the standard depth (default: deep); see skills/convening
    resume <bench>/<effort> <round_id>     — continue a stopped round on its branch (section 5)

If the payload is missing, malformed, names a bench with no `benches/<bench>/bench.md`, or names an effort with no `benches/<bench>/efforts/<effort>/brief.md`: do not guess and do not interview anyone. Create the branch, write `benches/<bench>/efforts/<effort>/rounds/<round_id>/BLOCKED.md` saying exactly what is missing (intake happens in chat with the principal before a round is fired), commit, open a PR titled "BLOCKED: <bench>/<effort> <round_id>", and stop.

## 2. Preflight (before any persona is dispatched)
- **The plan.** The brief must carry a `### Model plan` for this round with an `approved:` line (`skills/run-planning`). Planning happens in the principal's local thread, never here. If it is missing or has no `approved:` line, write `BLOCKED.md` titled `PLAN NEEDED` (what is missing; "plan the run in the local thread, then fire again"), open a PR titled `PLAN NEEDED: <bench>/<effort> <round_id>`, and stop. Exception: a round convened by the standing watch (`orchestrator/watch.md`) runs on the bench's `## Model plan` default if `bench.md` has one, else the ladder in `skills/run-planning`, capped at the watch's `budget.convene_ceiling`; its receipt says "unplanned (watch)".
- **The network.** WebFetch two well-known hosts (the effort's own site if the brief names one, and `https://www.sec.gov` or `https://en.wikipedia.org`). If every fetch fails (DNS errors such as `getaddrinfo ENOTFOUND`), stop: write `BLOCKED.md` naming the environment and saying it needs Full network access (`docs/cloud-setup.md`), open a PR titled `BLOCKED: no network — <bench>/<effort> <round_id>`, and stop. A round without page access is not worth finishing.
- **The ceiling.** Note the plan's `ceiling`. If the receipt's running total (run `python3 scripts/cost_report.py --brief <brief>` after each phase) passes the ceiling before the auditor has run, finish the current phase, then skip to the auditor and synthesis on what the ledger holds, and say so in the minutes and the PR.

## 3. Set up
- `round_number`: one more than the highest round in `score-history.json` (1 if none). `round_id`: `r<N>-<YYYYMMDD>` (append `-2` if it exists).
- Branch: `claude/round-<bench>-<effort>-<round_id>` from the default branch. The routine may append a random suffix to the branch name; that is fine. Use the branch the session is actually on, and name it in the PR.
- Round 1: read `brief.md`, create `ledger.json`. Round 2+: the brief's newest "Round N answers" section is the intake; archive the prior ledger to `rounds/<prior_round_id>/ledger.json`, apply carry-forward and write the answers into the carried `J-` records and as T1 evidence per `skills/intake` and `skills/evidence-ledger`. If the brief has no answers section for this round and the payload gave no trigger, treat it as "refresh" and note it in the phases minutes.
- Read `benches/<bench>/bench.md`, the bench's `context/` folder, and every file in `benches/<bench>/seats/`. Apply the materials gate per `skills/intake` (unattended: a missing item downgrades the depth unless the brief records that the principal chose blind) and record the result in the ledger's `effort` block.

## 4. Phases, in order
Dispatch personas as subagents, each with its own context, per the chair's dispatch rules (`agents/chair.md`): the model from the plan, the name `p<phase> <seat_id>`, **at most three seats per turn** (end the turn after each group; the next turn starts when their results come back), the seat's search budget and the helper rule. Every dispatch passes: bench slug, effort slug, round ID, effort folder path, persona ID, the seat-brief path, the charter path (`agents/<id>.md`, or the seat brief itself for `persona: custom`), and any specific instruction (`adversary_identity` for the Adversary, handoffs to answer, rebuttal inputs). Every persona follows `skills/persona-protocol` (stakeholders also `skills/stakeholder-protocol`) and writes exactly one file to `benches/<bench>/efforts/<effort>/rounds/<round_id>/` with temp IDs. After each phase, merge:

    python3 scripts/merge_ledger.py benches/<bench>/efforts/<effort>/ledger.json \
        benches/<bench>/efforts/<effort>/rounds/<round_id> --phase <n> --purpose "<phase name>" \
        --personas <ids in dispatch order>

then fill the phase's `summary` and `notable` so they read like minutes (with the model each seat ran on), commit, and push. One commit per phase, message `phase-<n> <bench>/<effort>/<round_id>: <phase name>`.

Phase order (scoped later rounds: only the seats the trigger and answers touch, per the chair's one-line ruling; the Evidence Auditor always runs):

1. **Roster.** Rate relevance per `agents/chair.md`; write `roster`; commit.
2. **Analysts** (groups of three, blind).
3. **Conflict register** (chair).
4. **Stakeholders** (groups of three, rostered only).
5. **Red team**: adversary (named from the analysts' findings), pre-mortem.
6. **Rebuttal** (groups of three, rostered stakeholders) unless the bench says `rebuttal: off`.
7. **Answer pass** (round 1; later rounds only if open challenges exist).
8. **Evidence Auditor** (alone, last).
9. **Synthesis** (chair): tier, score per `skills/scoring`, `exec_summary`, outputs per `skills/assessment-output` and `skills/council-ledger`, append `score-history.json`, commit. Then the close per `skills/round-close` (dashboard with `--prior` on round 2+, effort index, cost receipt, stall check).

**Material pivot.** If, at any phase, the chair's material-pivot test (`agents/chair.md`) is met, finish and merge the phase in progress, write `rounds/<round_id>/QUESTION.md`, commit, push, open a PR titled `QUESTION: <bench>/<effort> <round_id> — <the pivot in a few words>` with the question as its body, and stop. Do not finish the round on the old frame.

## 5. Resuming a stopped round
A round stops early for a spend or usage limit, a network block, a material-pivot question, or the principal's own stop. The payload `resume <bench>/<effort> <round_id>` (with any answer or instruction after a colon) continues it:
- Check out the round's existing branch (find it with `git branch -r --list 'origin/claude/round-<bench>-<effort>-<round_id>*'`) and merge the default branch into it so the latest brief and plan are present. Do not create a new `round_id`.
- Keep every merged phase. Treat unmerged seat files in the round folder as drafts: re-dispatch those seats with their draft path as a starting point ("verify, fill your gaps, rewrite the file"), not as finished work.
- If the stop was a `QUESTION.md`, read the principal's answer from the payload or the brief's newest answers section, record it as T1 evidence, apply the chosen way forward, and note it in the minutes.
- The plan's remaining rows govern what is left; the receipt sums every session the round ran in.

## 6. Close
Open a pull request to the default branch titled `Council round: <bench>/<effort> <round_id> — score <score> (±<band>)`. Body, per `skills/round-close`: the score label, the score and one-paragraph verdict, movement since the last round if any, links to the dashboard, the ledger (`rounds/<round_id>/ledger.json`), the assessment, the principal-requests file and the cost receipt on the round branch, the receipt's headline line (estimate, measured, ceiling, the reason for any overrun), and the full numbered "What the council needs from the principal" list. That PR is the round's deliverable; the principal reads it first and answers its requests at the next round's intake.

## Failure handling
- A persona subagent errors or returns nothing: retry once; then record an abstention in the phase's record and continue.
- WebFetch failing for every host mid-round: stop as in the network preflight; the round resumes on its branch once the environment is fixed.
- Never leave the round without a PR: the round PR, a `BLOCKED`, a `PLAN NEEDED` or a `QUESTION`.
