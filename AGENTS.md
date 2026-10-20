# AGENTS.md — house rules for every council cloud run

This repository is a council: a swarm of AI personas with seats, chaired by a neutral chair, that deliberates on the efforts its principal brings. The files in `agents/`, `skills/` and `commands/` are the source of truth for what every persona does. Nothing in this file overrides them.

## What runs here
A council round executes as one cloud session (the routine). The session acts as the **chair** (`agents/chair.md`) and dispatches every other seat as a subagent with its own context. Personas never see each other's reasoning, only the merged ledger. The full procedure for a cloud session is `orchestrator/orchestrate.md`.

## Source of truth
- Git is authoritative. Every persona file, merged ledger, assessment and dashboard is committed. Nothing authoritative lives only in session output.
- One file per persona per phase: `benches/<bench>/efforts/<effort>/rounds/<round_id>/` per `skills/persona-protocol`. Never co-write a file. The chair merges with `scripts/merge_ledger.py` and commits after every phase.
- Work happens on a branch named `claude/round-<bench>-<effort>-<round_id>`. The round ends with a pull request to the default branch. Never push directly to the default branch.

## Unattended discipline
- There is no human mid-round. Follow the chair's autonomy rule: run to completion, batch every question into "What the council needs from the principal". Pause (write `BLOCKED.md`, commit, open the PR early) only when the effort or entity is ambiguous or a supplied document contradicts the round's premise.
- If a persona subagent fails or stalls, record it as an abstention in the ledger's `phases` record and continue. A partial council beats a hung one.
- Log one `phases` entry per phase with a summary that reads like minutes.

## Confidentiality
- One effort per round. Never read another effort's folder, on this bench or any other (`skills/evidence-ledger`, effort isolation rule).
- Documents under `efforts/<effort>/documents/` are principal-supplied T1 material. They never leave this repository and are never quoted into another effort's ledger.
- No secrets in the repo. Tokens and credentials live in the routine's environment, never in a committed file.
