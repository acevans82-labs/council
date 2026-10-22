# Council — how to work in this repository

This repository is a **council**: a swarm of AI personas with seats, chaired by a neutral chair, that deliberates on whatever its principal brings it (a company, an idea, a deal, a decision, an initiative, a question), round after round, with every claim traced to an evidence ledger. The person talking to you is **the principal**. One principal can wear several hats; each hat is a **bench** with its own roster and scoring frame; each thing a bench works on is an **effort**; each pass of the council on an effort is a **round**.

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
| "check the setup", "something looks off", "doctor" | `commands/council-doctor.md` |

If `council.md` does not exist yet, every path starts with setup.

## Where things live
```
council.md                    the principal and the bench index (created by setup)
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
```

## Rules that always hold
- **Never read across efforts.** A round reads and writes only its own effort folder. Supplied documents are confidential to that effort.
- **Nothing reaches an output without a ledger ID.** Evidence, findings, conflicts, rulings, requests, gaps, handoffs. See `skills/evidence-ledger`.
- **The chair never reads a persona's reasoning**, only its five-line summary and the merged ledger. Dispatch personas as subagents with their own context, each told its seat ID, seat brief path and charter path.
- **Outputs never say "you".** The principal's asks go in "What the council needs from the principal", tiered 0–3.
- **Run to completion.** Pause mid-round only when the effort is ambiguous or a supplied document contradicts the premise. Batch everything else into the requests list.
- **Depth is a budget, not a roster.** Every convening is quick, standard or deep (`skills/convening`). Quick writes a memo and no ledger; standard and deep are rounds. The materials gate runs at every depth and says cleared, downgraded or blind.
- **Round N picks up where round N-1 stopped.** The requests list is the seed of the next round; answers come in at intake and become T1 evidence.
- **Benches are cheap, seats are one file.** Make a bench per hat. Add a seat by writing `seats/<id>.md`; remove it by deleting the file. Run `python3 scripts/doctor.py` after hand edits.
- **No secrets in the repo.** Tokens live in the routine's environment.

## Engine commands
```bash
python3 scripts/doctor.py                  # check the workspace (add --presets to check presets too)
python3 scripts/merge_ledger.py <ledger.json> <round_dir> --phase N --purpose "<name>" --personas <seat ids>
python3 skills/council-ledger/scripts/build_dashboard.py <ledger.json> <out.html>
```
