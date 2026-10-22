# Releasing council updates

How a change reaches everyone who uses the council. The model follows NDLC's (`ndlc-v2/RELEASING.md`): the engine is markdown and two scripts that load from disk, so a pull is a complete update. Until the engine/data split in `ROADMAP.md` item 2 ships, a copy made from the template updates by merging the engine paths from upstream; the doctor will offer that.

## The ritual (every change that touches the engine)
1. Edit on a branch; open a PR to `main` (the repo is a template and public; `main` is what people copy).
2. Bump `version` in `.claude-plugin/plugin.json`: patch for fixes and wording, minor for a new capability or a change in how a round behaves, major for a change that breaks an existing bench or ledger.
3. Write the `CHANGELOG.md` entry: what shipped and why, in plain words, no em-dashes. The why is what other people inherit.
4. If the ledger schema changed, update `skills/evidence-ledger/references/schema.md`, `examples/sample-ledger.json`, and the doctor's checks, and say in the entry what an existing ledger needs (usually nothing; the engine never rewrites history).
5. If `orchestrator/*.md` changed materially, say so in the entry: cloud routine prompts only reference the file, so the change is live at the next fire, but anyone who pasted a copy needs to know.
6. Run `python3 scripts/doctor.py --presets` and the term scan (no company or person names from the private origin). Rebuild `examples/sample-council-ledger.html` if the template changed.
7. Squash-merge, tag `v<version>`, and if the change is user-visible, add a GitHub release with the CHANGELOG entry as its notes.

Docs-only changes (README, ROADMAP, docs/) need no version bump.

## What people see
- Today: nothing automatic. Testers pull or merge upstream by hand; the CHANGELOG tells them what changed.
- After ROADMAP item 2: the update prompt at thread open, with the notes, pull / skip / remind in 3 days, exactly as NDLC does.

## Engine versus data
Engine: `agents/`, `skills/`, `commands/`, `scripts/`, `orchestrator/`, `presets/`, `CLAUDE.md`, `AGENTS.md`, `docs/`. Data: `council.md`, `benches/`. A release never touches data. A preset change does not change any bench already copied from it; the doctor may offer the diff.

## Onboarding a tester
1. They click "Use this template" (private copy) or clone, open it in Claude Code, and say "set up my council".
2. They need Python 3.9+, `gh` authenticated, and for cloud rounds a Claude Code cloud environment with the GitHub app on their repo (`docs/cloud-setup.md`).
3. Point them at `docs/how-a-round-works.md` first and `ROADMAP.md` for what is coming.
