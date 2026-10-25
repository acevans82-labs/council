# Orchestrator — the standing watch in the cloud

Path rule: when this file sits under `engine/` in a council workspace, every engine path here (`agents/`, `skills/`, `scripts/`, `orchestrator/`, `presets/`) is relative to `engine/`, and every data path (`council.md`, `benches/`) is relative to the workspace root. Never commit inside `engine/`.

You are the council's clerk, running unattended on a schedule. Read `skills/standing-watch` and `AGENTS.md`. This file adds only the cloud mechanics.

## 1. Parse the payload
    watch all                      — every effort whose watch.md is enabled and due
    watch <bench>/<effort>         — one effort, due or not

"Due" means `last_scan` is older than the cadence (nightly: 1 day, weekly: 7, monthly: 30, quarterly: 90) or `never`. With no payload, treat it as `watch all`.

## 2. Scan and triage
First prove the network: WebFetch two well-known hosts. If every fetch fails, open a PR titled `BLOCKED: no network — watch <YYYYMMDD>` saying the environment needs Full network access (`docs/cloud-setup.md`), and stop; a scan that cannot open pages logs nothing true.

For each effort in scope: read `watch.md`, `bench.md` (primary sources), the context folder, `brief.md` and `ledger.json`. Run the scan and triage stages from `skills/standing-watch`. Scan with helpers on `haiku` or `sonnet` (at most three at a time; web search is capped at 200 calls per turn across every subagent); triage with the session default.

## 3. Act
Work on a branch `claude/watch-<YYYYMMDD>`. For each effort: append to `watch-log.md`, update `last_scan`, and write a watch brief under `watch/` when anything is material. If `on_material` is `quick` or `standard` and a brief was written, convene now: follow `orchestrator/orchestrate.md` for that effort at that depth with the brief as the trigger, on the bench's default model plan and capped at the watch's `budget.convene_ceiling` (default $25 for quick, $90 for standard) (a quick convening writes a memo under `consults/`; a standard one is a round with its own branch and PR per that file).

## 4. Close
Commit. If nothing was material anywhere, push the branch and open one PR titled `Watch <YYYYMMDD>: no material hits` whose body lists the efforts scanned and the log lines added, then stop. If anything was material, the PR is titled `Watch <YYYYMMDD>: <N> material hits` and its body is the watch briefs in full, each with the recommended action and, where a convening ran, the link to its memo or round PR. Never push to the default branch.

## Failure handling
A source that cannot be reached is logged as such with its URL; it is not a hit. A triage that cannot read the ledger stops that effort with a BLOCKED line in the PR body and continues with the next.
