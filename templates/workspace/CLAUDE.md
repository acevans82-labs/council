<!-- council-workspace block, engine template version 1.2.0. The doctor diffs this file against engine/templates/workspace/CLAUDE.md and offers the update. -->
# This is a council workspace

This repository holds one person's (or one team's) **council data**: `council.md` (who the principal is, the benches, the connections) and `benches/` (each hat, its seats, its context, its efforts and rounds). The **engine** that runs it, the personas, skills, commands, scripts and orchestrators, lives in the `engine/` folder, a git submodule pinned to a released version of the public council engine (github.com/acevans82-labs/council). You never edit `engine/`; you update it.

**Read `engine/CLAUDE.md` now and follow it**, with this one path rule on top:
- A path in any engine file that starts with `agents/`, `skills/`, `commands/`, `scripts/`, `orchestrator/`, `presets/`, `docs/`, `examples/` or `templates/` is relative to `engine/`. So `skills/persona-protocol` means `engine/skills/persona-protocol`, and `python3 scripts/doctor.py` means `python3 engine/scripts/doctor.py`.
- A path that starts with `council.md` or `benches/` is relative to this workspace root.

If `engine/` is empty, the submodule has not been fetched: run `git submodule update --init` and read again.

## Keeping the council current
At the start of a thread (once per thread, before any council work), run `python3 engine/scripts/check_update.py`. Exit 0: say nothing. Exit 3: an engine release is newer than the one pinned here. Tell the principal in two lines (the versions and the release-note headings the script printed) and offer three buttons: **Update now** (run it again with `--apply`, then `git add engine && git commit -m "engine <version>"` and push; if a marketplace plugin install also exists, chase it with `claude plugin update council@council`), **Skip** (nothing written; it asks again next thread), **Remind me in 3 days** (`--snooze`). Never update over local changes in `engine/`. Never ask while a snooze is live; the script handles that. Offline, the script is silent and so are you. `engine/scripts/doctor.py` runs the same check and reports a snoozed update as a status line without prompting.

## Cloud rounds
`AGENTS.md` here tells a cloud session to fetch the submodule first and then follow `engine/orchestrator/orchestrate.md` (a round) or `engine/orchestrator/watch.md` (the standing watch). The engine version a cloud round uses is the one pinned here, so updating the pointer is what moves cloud rounds forward.
