# Releasing council updates

How a change reaches everyone who uses the council. The model follows NDLC's (`ndlc-v2/RELEASING.md`): this repository is the engine, every workspace mounts it as a git submodule pinned to a tag, and a release is a tag. The next thread anyone opens in a workspace offers the update with the notes (`scripts/check_update.py`).

## The ritual (every change that touches the engine)
1. Edit on a branch; open a PR to `main` (the repo is a template and public; `main` is what people copy).
2. Bump `version` in `.claude-plugin/plugin.json`: patch for fixes and wording, minor for a new capability or a change in how a round behaves, major for a change that breaks an existing bench or ledger.
3. Write the `CHANGELOG.md` entry: what shipped and why, in plain words, no em-dashes. The why is what other people inherit.
4. If `templates/workspace/CLAUDE.md` changed, update the version stamp in its first line; the doctor diffs every workspace's copy against it.
5. If the ledger schema changed, update `skills/evidence-ledger/references/schema.md`, `examples/sample-ledger.json`, and the doctor's checks, and say in the entry what an existing ledger needs (usually nothing; the engine never rewrites history).
6. If `orchestrator/*.md` changed materially, say so in the entry: cloud routine prompts only reference the file, so the change is live at the next fire, but anyone who pasted a copy needs to know.
7. Run `python3 scripts/doctor.py --presets` and the term scan (no company or person names from the private origin). Rebuild `examples/sample-council-ledger.html` if the template changed.
8. Squash-merge, tag `v<version>` (`git tag v<version> && git push origin v<version>`; the tag is what `check_update.py` looks for), and if the change is user-visible, add a GitHub release with the CHANGELOG entry as its notes.

Docs-only changes (README, ROADMAP, docs/) need no version bump.

## What people see
At thread open in a workspace: "Council engine X is available (you have Y)" with the release-note headings, and Update now / Skip / Remind me in 3 days. Update now checks out the tag in `engine/` and commits the pointer. A snooze is a promise: no prompt until it lapses, even if a newer release lands. Offline, silence. The doctor reports a snoozed update as a status line.

## Engine versus data
Engine (this repository): `agents/`, `skills/`, `commands/`, `scripts/`, `orchestrator/`, `presets/`, `docs/`, `templates/`, `CLAUDE.md`, `AGENTS.md`. Data (a workspace): `council.md`, `benches/`, plus its own `CLAUDE.md`, `AGENTS.md`, `README.md` born from `templates/workspace/`. A release never touches data. A preset change does not change any bench already copied from it.

## Workspace template
`acevans82-labs/council-workspace` is a separate, tiny, public template repository: the four files from `templates/workspace/` plus `.gitmodules` pointing at this engine. When those four files change here, copy them there in the same release.

## Onboarding a tester
1. `gh repo create my-council --template acevans82-labs/council-workspace --private --clone && cd my-council && git submodule update --init`, open it in Claude Code, say "set up my council".
2. They need Python 3.9+, `gh` authenticated, and for cloud rounds a Claude Code cloud environment with the GitHub app on their repo (`docs/cloud-setup.md`).
3. Point them at `docs/how-a-round-works.md` first and `ROADMAP.md` for what is coming.
