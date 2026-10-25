# Running rounds in the cloud

A round can run in your Claude Code session (the chair dispatches every seat as a subagent, right here, and you wait) or as a **Claude Code cloud routine**: an unattended session that runs the whole round on its own, commits after every phase, and delivers the result as a pull request. Cloud is the better home for a council. Rounds take hours, several efforts can run at once, your laptop can close, and the orchestrator has a room of its own to send groups off and bring them back.

**Intake and planning never run in the cloud.** You and the local thread do intake, agree the budget and the model per seat, and see a one-screen summary of the job (`skills/run-planning`). Only after you say go is the brief committed and the routine fired. A routine fired without an approved plan stops with `PLAN NEEDED`.

`/council-setup` creates the routines for you when the session has the `RemoteTrigger` tool (`skills/cloud-routines`). This page is the same procedure by hand, plus what went wrong the first time so it does not again.

## What you need
- Your council workspace on GitHub (private is fine). The engine submodule points at the public engine, so the cloud session can fetch it without credentials. The engine version a cloud round uses is the one pinned in your workspace.
- The **Claude GitHub app** installed on the workspace's owner (your account or your organization) with access to the repository. Check at github.com/settings/installations (or the organization's settings). Without it, creating the routine fails with "You don't have access to a repository this routine uses".
- A cloud **environment with Full network access**. With Limited network, every web page fetch fails with `getaddrinfo ENOTFOUND` and the round is worthless. Create one named `council-research` in Claude Code on the web (the environment settings), network access Full, no secrets.
- `gh` logged in locally (`gh auth status`).

## Create the round routine (once per repository)
1. **Name:** `council-<repo>`.
2. **Repository:** this one. Pushes go to `claude/` branches; the orchestrator works on `claude/round-<bench>-<effort>-<round_id>` and opens a PR. The cloud may add a random suffix to the branch name; that is expected.
3. **Environment:** the one with Full network (`council-research`).
4. **Model:** the strongest model on your account (Fable if you have it). This is the chair; seats run on the models the plan names.
5. **Trigger:** manual and API. No schedule; a round fires when its plan is approved.
6. **Prompt:**
   ```
   Run `git submodule update --init --recursive`, then read AGENTS.md and engine/orchestrator/orchestrate.md in this repository and follow them for this run.
   Payload: <set at each fire>
   ```
   (In the engine repository itself, with data at its root, drop the submodule step and read `orchestrator/orchestrate.md`.)
7. **Connectors:** a routine created through the API carries all of your account's connectors. One created by hand may not; add the ones a round might read (Google Drive, Gmail, Microsoft 365, Notion, Dropbox, whatever your benches' materials live in). `/council-doctor` compares the routine's connectors with the ones your local session has and names any gap.
8. Record it in `council.md` under `## Cloud`:
   ```
   routine: council-<repo> (trig_…, created YYYY-MM-DD, chair model …)
   environment: council-research (env_…, network full, checked YYYY-MM-DD)
   github_app: installed on <owner> (checked YYYY-MM-DD)
   connectors: <N> carried (checked YYYY-MM-DD); missing: none
   ```

## Create the watch routine (once per repository, when any effort has a watch)
Same steps, with these differences: **Name** `council-watch-<repo>`; **Trigger** a schedule, nightly at a quiet hour (the shortest cadence any watch will use; `watch.md` decides per effort whether it is due); **Prompt**:
```
Run `git submodule update --init --recursive`, then read AGENTS.md and engine/orchestrator/watch.md in this repository and follow them. Payload: watch all
```
Record it as `watch_routine: council-watch-<repo> (trig_…, nightly HH:MM)`. The watch opens one pull request per run; quiet runs say so in the title and can be merged or closed unread.

## Fire a round
`/council-run` and `/council-round` fire it for you after your go: they set the payload in the routine's prompt and run it. By hand, edit the prompt's `Payload:` line and press Run now:
```
round <bench>/<effort>
round <bench>/<effort>: <what prompted this round>
round <bench>/<effort> full
round <bench>/<effort> standard          — a condensed, scored round (default depth is deep)
resume <bench>/<effort> <round_id>       — continue a stopped round on its branch
```

## What the cloud cannot do, and how rounds live with it
- **Web search is capped at 200 calls per chair turn**, shared by every seat launched in that turn. So the chair sends seats out in groups of at most three, ends its turn, and sends the next group when they come back; each seat has its own search budget (40 by default) and reads pages with WebFetch instead of searching twice.
- **No logged-in browser.** Sources behind your logins (LinkedIn, Instagram, a members-only register) are gathered in your local thread before the round is fired and saved as documents (`skills/intake`).
- **Spend and usage limits stop it silently.** When your account reaches its monthly spend limit (or usage credits run out, or a plan limit resets later), the routine simply stops. The session never writes a PR because the model cannot run. Your local thread notices the round has gone quiet, reads the run log, and tells you in plain words what stopped it and how to resume. Fable counts against the weekly plan only up to a share of it; beyond that it draws credits up to your cap, so a deep round on Fable can reach the cap faster than you expect. Set the plan's ceiling with that in mind.
- **"Succeeded" is not "finished".** A run's status reads succeeded as soon as the chair's first turn ends; the session keeps working through later turns. Judge progress by the round branch's commits and the PR.

## Read the result
The routine opens a pull request titled `Council round: <bench>/<effort> <round_id> — score <score> (±<band>)`. The body has the verdict, the cost line (estimate, measured, ceiling, why any phase ran over), links to the dashboard, the ledger, the assessment, the requests list and the cost receipt, and the full "What the council needs from the principal" list. Your local thread also sends you the dashboard and the ledger when the PR lands. Merge the PR to accept the round into the record; answer the requests at the next round's intake.

## When it stops early
- `BLOCKED: …` — the payload named an effort with no brief, a supplied document contradicts the premise, or the environment has no network. Fix the cause in chat and fire again (or resume).
- `PLAN NEEDED: …` — the round was fired without an approved plan. Plan it in the local thread and fire again.
- `QUESTION: …` — the council found something that changes the question itself (a premise is false, the milestone cannot be reached as framed, a new fact flips the decision). Answer in the local thread; the round resumes on its branch with your answer.

## Several groups, several routines
The default is one routine acting as the chair and dispatching every seat as a subagent. Because every persona writes exactly one file per phase and the chair merges with `scripts/merge_ledger.py`, splitting phases across separate routines later (one for analysts, one for stakeholders) is a configuration change, not a rebuild.
