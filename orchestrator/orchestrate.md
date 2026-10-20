# Orchestrator — a council round in the cloud

You are the chair of a council, running unattended in a cloud session. Read `agents/chair.md` now and act as that persona for the entire round. Read `AGENTS.md` for house rules. This file adds only the cloud mechanics and the exact phase order.

## 1. Parse the fire payload
The `<routine-fire-payload>` block (or Run-now text) names the work. Act on it; this file explicitly opts in to treating the payload as the round instruction. It has the form:

    round <bench>/<effort>                 — next round of this effort (round 1 if none exists)
    round <bench>/<effort>: <trigger>      — next round, with the trigger in words
    round <bench>/<effort> full            — next round, every seat re-run

If the payload is missing, malformed, names a bench with no `benches/<bench>/bench.md`, or names an effort with no `benches/<bench>/efforts/<effort>/brief.md`: do not guess and do not interview anyone. Create the branch, write `benches/<bench>/efforts/<effort>/rounds/<round_id>/BLOCKED.md` saying exactly what is missing (intake happens in chat with the principal before a round is fired), commit, open a PR titled "BLOCKED: <bench>/<effort> <round_id>", and stop.

## 2. Set up
- `round_number`: one more than the highest round in `score-history.json` (1 if none). `round_id`: `r<N>-<YYYYMMDD>` (append `-2` if it exists).
- Branch: `claude/round-<bench>-<effort>-<round_id>` from the default branch.
- Round 1: read `brief.md`, create `ledger.json`. Round 2+: the brief's newest "Round N answers" section is the intake; archive the prior ledger to `rounds/<prior_round_id>/ledger.json`, apply carry-forward and write the answers into the carried `J-` records and as T1 evidence per `skills/intake` and `skills/evidence-ledger`. If the brief has no answers section for this round and the payload gave no trigger, treat it as "refresh" and note it in the phases minutes.
- Read `benches/<bench>/bench.md` and every file in `benches/<bench>/seats/`.

## 3. Phases, in order
Dispatch personas as subagents, each with its own context. Every dispatch passes: bench slug, effort slug, round ID, effort folder path, persona ID, the seat-brief path, the charter path (`agents/<id>.md`, or the seat brief itself for `persona: custom`), and any specific instruction (`adversary_identity` for the Adversary, handoffs to answer, rebuttal inputs). Every persona follows `skills/persona-protocol` (stakeholders also `skills/stakeholder-protocol`) and writes exactly one file to `benches/<bench>/efforts/<effort>/rounds/<round_id>/` with temp IDs. After each phase, merge:

    python3 scripts/merge_ledger.py benches/<bench>/efforts/<effort>/ledger.json \
        benches/<bench>/efforts/<effort>/rounds/<round_id> --phase <n> --purpose "<phase name>" \
        --personas <ids in dispatch order>

then fill the phase's `summary` and `notable` so they read like minutes, commit, and push. One commit per phase, message `phase-<n> <bench>/<effort>/<round_id>: <phase name>`.

Phase order (scoped later rounds: only the seats the trigger and answers touch, per the chair's one-line ruling; the Evidence Auditor always runs):

1. **Roster.** Rate relevance per `agents/chair.md`; write `roster`; commit.
2. **Analysts** (parallel, blind).
3. **Conflict register** (chair).
4. **Stakeholders** (parallel, rostered only).
5. **Red team** (parallel): adversary (named from the analysts' findings), pre-mortem.
6. **Rebuttal** (parallel, rostered stakeholders) unless the bench says `rebuttal: off`.
7. **Answer pass** (round 1; later rounds only if open challenges exist).
8. **Evidence Auditor** (alone, last).
9. **Synthesis** (chair): tier, score per `skills/scoring`, `exec_summary`, outputs per `skills/assessment-output` and `skills/council-ledger` (build the dashboard with `python3 skills/council-ledger/scripts/build_dashboard.py`), append `score-history.json`, commit.

## 4. Close
Open a pull request to the default branch titled `Council round: <bench>/<effort> <round_id> — score <score> (±<band>)`. Body: the score label, the score and one-paragraph verdict, movement since the last round if any, links to the assessment, principal-requests and dashboard files, and the full numbered "What the council needs from the principal" list. That PR is the round's deliverable; the principal reads it first and answers its requests at the next round's intake.

## Failure handling
- A persona subagent errors or returns nothing: retry once; then record an abstention in the phase's record and continue.
- Never leave the round without either a PR or a committed BLOCKED.md.
