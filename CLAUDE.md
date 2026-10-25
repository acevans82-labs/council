# Council — how to work with the engine

**Engine or workspace?** This file belongs to the council **engine**: the personas, skills, commands, scripts and orchestrators. A person's data (their `council.md` and `benches/`) lives in a **workspace** repository that mounts this engine as the git submodule `engine/` (template: github.com/acevans82-labs/council-workspace). When you are in a workspace, its own `CLAUDE.md` sends you here and adds one path rule: engine paths are relative to `engine/`, data paths to the workspace root. When you are in the engine repository itself, you are either developing the engine (edit on a branch, follow `RELEASING.md`) or trying it out: data may live at this root too, and every path below works unchanged.

This engine runs a **council**: a swarm of AI personas with seats, chaired by a neutral chair, that deliberates on whatever its principal brings it (a company, an idea, a deal, a decision, an initiative, a question), round after round, with every claim traced to an evidence ledger. The person talking to you is **the principal**. One principal can wear several hats; each hat is a **bench** with its own roster and scoring frame; each thing a bench works on is an **effort**; each pass of the council on an effort is a **round**.

## Zero-install routing
The slash commands in `commands/` work when this repo is installed as a plugin, but nothing requires that. When the principal asks in plain words, read the matching command file and follow it exactly as if they had typed the slash command:

| They say something like | Read and follow |
| --- | --- |
| "set up", "get started", "who am I to this thing", first message in a fresh clone | `commands/council-setup.md` |
| "new bench", "switch to my founder hat", "list benches", "edit the bench" | `commands/council-bench.md` |
| "add a seat", "remove the union seat", "what personas are there", "edit the regulator's brief" | `commands/council-seat.md` |
| "consult the council on X", "quick question for the council", "what does the bench think about X" | `commands/council-consult.md` (quick by default; "standard" or "deep" in the ask changes it) |
| "run the council on X", "assess X", "start an effort", "vet this idea" | `commands/council-run.md` |
| "next round on X", "round 2", "here are my answers", "update X, a new deck arrived" | `commands/council-round.md` |
| "watch X for me", "keep an eye on X", "turn off the watch", "what has the watch found" | `commands/council-watch.md` |
| "status", "where are we", "what's open" | `commands/council-status.md` |
| "check the setup", "something looks off", "doctor", "is there an update" | `commands/council-doctor.md` |
| "what will this cost", "plan the run", "change the budget", "use Sonnet for that seat" | `skills/run-planning/SKILL.md` |
| "what did that cost", "cost receipt", "why did it go over" | `skills/round-close/SKILL.md` (section 2) |
| "swap threads", "this thread is too long", "new home thread", "pass the baton" | `commands/council-swap.md` |
| "set up the cloud", "create the routine", "is the routine healthy", "the cloud round went quiet" | `skills/cloud-routines/SKILL.md` |

If `council.md` does not exist yet, every path starts with setup.

## Where things live
```
council.md                    the principal and the bench index (created by setup)   [workspace]
benches/                      the data                                                [workspace]
benches/<bench>/bench.md      one hat: role, field, question, scoring frame, roster index
benches/<bench>/seats/*.md    the roster: one seat brief per persona (file stem = seat ID)
benches/<bench>/context/      standing material every convening reads first (the bench's "training")
benches/<bench>/efforts/<effort>/   brief, documents, ledger.json, rounds/, consults/, watch.md, assessments/, dashboards/
presets/<preset>/             ready-made benches to copy and adjust
agents/                       the persona library (generic charters) and _template.md
skills/                       the rules of the council: protocols, ledger, scoring, outputs, design
commands/                     the slash commands above
orchestrator/orchestrate.md   how a cloud routine runs a round unattended; orchestrator/watch.md runs the standing watch
scripts/                      merge_ledger.py, doctor.py; the dashboard builder is under skills/council-ledger
docs/                         cloud setup, how a round works
scripts/cost_report.py        the cost receipt: real token usage from the session transcripts, priced per model, against the plan
```

## Rules that always hold
- **Never read across efforts.** A round reads and writes only its own effort folder. Supplied documents are confidential to that effort.
- **Nothing reaches an output without a ledger ID.** Evidence, findings, conflicts, rulings, requests, gaps, handoffs. See `skills/evidence-ledger`.
- **The chair never reads a persona's reasoning**, only its five-line summary and the merged ledger. Dispatch personas as subagents with their own context, each told its seat ID, seat brief path and charter path.
- **Outputs never say "you".** The principal's asks go in "What the council needs from the principal", tiered 0–3.
- **Run to completion.** Pause mid-round only when the effort is ambiguous or a supplied document contradicts the premise. Batch everything else into the requests list.
- **Depth is a budget, not a roster.** Every convening is quick, standard or deep (`skills/convening`). Quick writes a memo and no ledger; standard and deep are rounds. The materials gate runs at every depth and says cleared, downgraded or blind.
- **Plan locally, then spend.** Intake and run planning (`skills/run-planning`: a dollar ceiling, a model per seat, an estimate, a one-screen summary) happen in the local thread with the principal, and nothing is dispatched or fired before the principal's go. The cloud never plans.
- **Three seats per turn.** Web search is capped at 200 calls per chair turn across every subagent, so seats go out in groups of at most three, each with a search budget.
- **Every round delivers.** The close (`skills/round-close`) builds the dashboard, writes the cost receipt, and sends the principal the dashboard and the ledger (SendUserFile where available), linked in the PR too.
- **Ask on a material pivot, and only then.** A false premise, an unreachable milestone, or a fact that flips the question stops the round with a question to the principal (`agents/chair.md`). Everything else is a finding.
- **Local browser for the principal's side.** In the local thread, the built-in browser or Claude in Chrome may gather principal-side evidence (logged-in sources too), saved as documents; facts about people stay within their public and professional capacity (`skills/intake`).
- **Round N picks up where round N-1 stopped.** The requests list is the seed of the next round; answers come in at intake and become T1 evidence.
- **Benches are cheap, seats are one file.** Make a bench per hat. Add a seat by writing `seats/<id>.md`; remove it by deleting the file. Run `python3 scripts/doctor.py` after hand edits.
- **No secrets in the repo.** Tokens live in the routine's environment.
- **Never edit `engine/` from a workspace.** Engine changes are releases; a workspace updates its pointer (`scripts/check_update.py`).

## Engine commands
```bash
python3 scripts/doctor.py                  # check the workspace (add --presets to check presets too); finds the workspace from the current directory
python3 scripts/check_update.py            # is a newer engine release available? (--apply to take it, --snooze for 3 days)
python3 scripts/merge_ledger.py <ledger.json> <round_dir> --phase N --purpose "<name>" --personas <seat ids>
python3 skills/council-ledger/scripts/build_dashboard.py <ledger.json> <out.html>
python3 scripts/cost_report.py --brief <brief.md> --label "<bench>/<effort> <round_id>" --out <receipt.md>   # exit 2 = a spend limit or network stall was found
```
