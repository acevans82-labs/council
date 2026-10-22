# Running rounds in the cloud

A round can run in your Claude Code session (the chair dispatches every seat as a subagent, right here, and you wait) or as a **Claude Code cloud routine**: an unattended session that runs the whole round on its own, commits after every phase, and delivers the result as a pull request. Cloud is the better home for a council. Rounds take a while, several efforts can run at once, your laptop can close, and the orchestrator has a room of its own to send groups off and bring them back.

Intake never runs in the cloud. You and the session do intake in chat (`/council-run` or `/council-round`), the brief and documents are committed and pushed, and then the routine is fired with a one-line payload.

## What you need
- This repository on GitHub (private is fine; the template is public, your copy need not be).
- Claude Code cloud access on your account, with the GitHub app installed on the repository.
- `gh` logged in locally (`gh auth status`).

## Create the routine (once per repository)
1. Open the routines page in Claude Code (claude.ai/code/routines) and create a routine.
2. **Name:** `council-<repo>`.
3. **Repository:** this one. **Branch pushes:** leave restricted to the `claude/` prefix; the orchestrator works on `claude/round-<bench>-<effort>-<round_id>` and opens a PR.
4. **Trigger:** manual ("Run now") and the API trigger. No schedule; a council round fires when intake is done.
5. **Prompt:** paste exactly:
   ```
   Read orchestrator/orchestrate.md in this repository and follow it for this run. The payload is in the fire payload or the Run-now text.
   ```
6. **Environment:** the default cloud sandbox is enough. Personas use web search and the browser tools the session provides; no credentials are needed. If a bench's sources sit behind logins, that bench's seats record the gap rather than the fact.
7. Record it in `council.md` under `## Cloud` as `routine: council-<repo>` so `/council-run` knows to fire it rather than run here.

## Create the watch routine (once per repository, when any effort has a watch)
Same steps, with these differences: **Name** `council-watch-<repo>`; **Trigger** a schedule, nightly at a quiet hour (the shortest cadence any watch will use; `watch.md` decides per effort whether it is due); **Prompt**:
```
Read orchestrator/watch.md in this repository and follow it for this run. Payload: watch all
```
Record it in `council.md` under `## Cloud` as `watch_routine: council-watch-<repo>`. The watch opens one pull request per run; quiet runs say so in the title and can be merged or closed unread.

## Fire a round
After intake is committed and pushed, "Run now" with the payload:
```
round <bench>/<effort>
round <bench>/<effort>: <what prompted this round>
round <bench>/<effort> full
round <bench>/<effort> standard          — a condensed, scored round (default depth is deep)
```
`/council-run` and `/council-round` print the exact payload for the effort they just prepared. If your session has a routine-trigger tool, they fire it for you.

## Read the result
The routine opens a pull request titled `Council round: <bench>/<effort> <round_id> — score <score> (±<band>)`. The body has the verdict and the full "What the council needs from the principal" list. The assessment, the principal-requests file and the dashboard are in the branch. Merge the PR to accept the round into the record; answer the requests at the next round's intake.

## When it blocks
If the payload names an effort with no brief, or a supplied document contradicts the round's premise, the routine writes `rounds/<round_id>/BLOCKED.md`, commits, opens a PR titled `BLOCKED: …` and stops. Fix the cause in chat and fire again.

## Several groups, several routines
The default is one routine acting as the chair and dispatching every seat as a subagent. Because every persona writes exactly one file per phase and the chair merges with `scripts/merge_ledger.py`, splitting phases across separate routines later (one for analysts, one for stakeholders) is a configuration change, not a rebuild.
