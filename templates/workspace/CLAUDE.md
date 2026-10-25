<!-- council-workspace block, engine template version 1.3.1. The doctor diffs this file against engine/templates/workspace/CLAUDE.md and offers the update. -->
# This is a council workspace

This repository holds one person's (or one team's) **council data**: `council.md` (who the principal is, the benches, the connections, the cloud routines) and `benches/` (each hat, its seats, its context, its efforts and rounds). The **engine** that runs it, the personas, skills, commands, scripts and orchestrators, lives in the `engine/` folder, a git submodule pinned to a released version of the public council engine (github.com/acevans82-labs/council). You never edit `engine/`; you update it.

**Read `engine/CLAUDE.md` now and follow it**, with this one path rule on top:
- A path in any engine file that starts with `agents/`, `skills/`, `commands/`, `scripts/`, `orchestrator/`, `presets/`, `docs/`, `examples/` or `templates/` is relative to `engine/`. So `skills/persona-protocol` means `engine/skills/persona-protocol`, and `python3 scripts/doctor.py` means `python3 engine/scripts/doctor.py`.
- A path that starts with `council.md` or `benches/` is relative to this workspace root.

If `engine/` is empty, the submodule has not been fetched: run `git submodule update --init` and read again.

## First turn of every new thread
Before any council work, run `python3 engine/scripts/doctor.py --quick` once. It is fast and silent when all is well.
- **`update available:`** (exit 3): a newer engine release exists. Tell the principal in two lines (the versions and the release-note headings it printed) and offer three buttons: **Update now** (`python3 engine/scripts/check_update.py --apply`, then `git add engine && git commit -m "engine <version>"` and push; if a marketplace plugin install also exists, chase it with `claude plugin update council@council`; then re-run the quick check, which may now say the templates below changed), **Skip** (nothing written; it asks again next thread), **Remind me in 3 days** (`python3 engine/scripts/check_update.py --snooze`). Never update over local changes in `engine/`. A live snooze prints only a status line; say nothing about it.
- **`CLAUDE.md` or `AGENTS.md` differs from the template:** after an update this is expected. Offer to copy `engine/templates/workspace/<file>` over (one button), then commit.
- **An ERROR line:** say it in one plain sentence and offer `/council-doctor` to fix it.
- Offline, the check is silent about updates, and so are you.

## The home thread
The local thread is where the principal plans runs, answers requests and reads results. Intake and run planning (budget, a model per seat, the estimate, a one-screen summary, the principal's go) always happen here, never in the cloud. When a fired cloud round lands, this thread sends the dashboard and the ledger; when one goes quiet, it reads the run log and says what stopped it. At every safe moment (a round closed, a plan approved and fired, answers written), read how full this thread's context is: at 60% offer a one-click swap to a fresh thread, at 80% recommend it (`skills/thread-swap`).

## Cloud rounds
`AGENTS.md` here tells a cloud session to fetch the submodule first and then follow `engine/orchestrator/orchestrate.md` (a round) or `engine/orchestrator/watch.md` (the standing watch). The engine version a cloud round uses is the one pinned here, so updating the pointer is what moves cloud rounds forward. Routines, their environment (Full network access) and their connectors are recorded under `## Cloud` in `council.md` and checked by `/council-doctor`.
