# AGENTS.md — house rules for every cloud run in this council workspace

This repository is a council workspace: data only. The engine is the git submodule at `engine/`, pinned to a released version. Before anything else in a cloud session:

    git submodule update --init --recursive

If that fails (no network, or the pointer is gone), write `BLOCKED.md` at the repository root saying so, commit on a `claude/` branch, open a PR titled `BLOCKED: engine submodule`, and stop.

Then read `engine/AGENTS.md` and follow it, with the path rule from `CLAUDE.md`: engine paths (`agents/`, `skills/`, `commands/`, `scripts/`, `orchestrator/`, `presets/`, `docs/`) are relative to `engine/`; data paths (`council.md`, `benches/`) are relative to this root. A round follows `engine/orchestrator/orchestrate.md`; the standing watch follows `engine/orchestrator/watch.md`. Never commit changes inside `engine/`.

`engine/AGENTS.md` carries the rules every round lives by: the approved model plan from the brief, three seats per turn with a search budget each, the network check, resuming a stopped round, stopping with a question only on a material pivot, and the close with its cost receipt. Rules for this workspace alone go below this line.
