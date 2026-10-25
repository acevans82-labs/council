# AGENTS.md — house rules for every council cloud run

This repository is a council: a swarm of AI personas with seats, chaired by a neutral chair, that deliberates on the efforts its principal brings. The files in `agents/`, `skills/` and `commands/` are the source of truth for what every persona does. Nothing in this file overrides them.

## What runs here
A council round executes as one cloud session (the routine). The session acts as the **chair** (`agents/chair.md`) and dispatches every other seat as a subagent with its own context. Personas never see each other's reasoning, only the merged ledger. The full procedure for a cloud session is `orchestrator/orchestrate.md`.

## Source of truth
- Git is authoritative. Every persona file, merged ledger, assessment and dashboard is committed. Nothing authoritative lives only in session output.
- One file per persona per phase: `benches/<bench>/efforts/<effort>/rounds/<round_id>/` per `skills/persona-protocol`. Never co-write a file. The chair merges with `scripts/merge_ledger.py` and commits after every phase.
- Work happens on a branch named `claude/round-<bench>-<effort>-<round_id>`. The round ends with a pull request to the default branch. Never push directly to the default branch.

## Unattended discipline
- There is no human mid-round. Follow the chair's autonomy rule: run to completion, batch every question into "What the council needs from the principal". Pause (write `BLOCKED.md`, commit, open the PR early) only when the effort or entity is ambiguous or a supplied document contradicts the round's premise. Stop with a `QUESTION.md` and a PR titled `QUESTION: …` only on a material pivot as `agents/chair.md` defines it (a premise is false, the milestone is unreachable as framed, a new fact flips the question); ordinary findings never stop a round.
- If a persona subagent fails or stalls, record it as an abstention in the ledger's `phases` record and continue. A partial council beats a hung one.
- Log one `phases` entry per phase with a summary that reads like minutes.

## Model plan
Every round runs on the approved `### Model plan` in the effort's `brief.md` (`skills/run-planning`), made with the principal in the local thread. No approved plan: stop with `PLAN NEEDED` (`orchestrator/orchestrate.md`). The chair dispatches each seat on the model the plan names (the Agent tool's `model` parameter: `fable`, `opus`, `sonnet`, `haiku`), names each dispatch `p<phase> <seat_id>`, passes the helper rule (at most two helpers per seat, on `sonnet` or `haiku`; the seat writes its own file), and records the model each seat actually ran on in the phase minutes. Seats the plan does not name run on the chair's model.

## Search budget and dispatch groups
Web search is capped at 200 calls per chair turn, shared by every subagent launched in that turn. Never launch a whole phase at once. Dispatch seats in groups of at most three, end the turn after each group (say which seats are out), and launch the next group when their results bring you back, so every group gets a fresh allowance. Tell every seat its budget: at most 40 web searches (20 for a bounded seat, 10 for a rebuttal); read sources with WebFetch rather than searching again; if search runs out, keep fetching known URLs and log the rest as gaps.

## Network
Prove the network before the first dispatch: WebFetch two well-known hosts. If WebFetch fails for every host, stop: write `BLOCKED.md` naming the environment (it needs Full network access, `docs/cloud-setup.md`) and open the BLOCKED pull request. A round without page access is not worth finishing.

## Resuming a stopped round
A `resume <bench>/<effort> <round_id>` payload continues a round on its existing branch (find it by prefix; the cloud adds a random suffix): merge the default branch in, keep the round ID and every merged phase, and treat unmerged seat files in the round folder as drafts. Re-dispatch those seats with their draft path as a starting point ("verify, fill your gaps, rewrite the file"), not as finished work. Full procedure: `orchestrator/orchestrate.md` section 5.

## Close and cost
Every round closes per `skills/round-close`: the dashboard and the effort index built, the ledger copied into the round folder, the cost receipt written (`scripts/cost_report.py`: estimate against measured by phase, with a one-sentence reason for each overrun), and the PR body linking the dashboard, the ledger, the assessment, the requests and the receipt.

## Confidentiality
- One effort per round. Never read another effort's folder, on this bench or any other (`skills/evidence-ledger`, effort isolation rule).
- Documents under `efforts/<effort>/documents/` are principal-supplied T1 material. They never leave this repository and are never quoted into another effort's ledger.
- No secrets in the repo. Tokens and credentials live in the routine's environment, never in a committed file.
