# Changelog

## 1.2.0 — 2026-10-22
- **Engine and workspace are separate.** This repository is now the engine only; data lives in a workspace made from the `council-workspace` template with the engine mounted as a git submodule pinned to a release. Why: a template copy could never pull upstream without merging the owner's benches, so no update could ever be offered. Now the engine is read-only for everyone but its maintainers and every workspace updates by moving one pointer.
- **Update check.** `scripts/check_update.py` compares the pinned engine to the latest tag, prints the release notes between, and supports `--apply` and a 3-day `--snooze` (`~/.claude/council/update-snooze`). The workspace `CLAUDE.md` runs it once per thread and offers Update now / Skip / Remind me in 3 days, mirroring NDLC.
- **Doctor** finds the workspace from the current directory, checks the submodule, diffs the workspace `CLAUDE.md` against the engine template, and reports an available or snoozed update.
- `templates/workspace/` holds the files a workspace is born with. Cloud routine prompts now fetch the submodule first.

## 1.1.0 — 2026-10-21
- **Depth profiles.** "Consult the council" at quick, standard or deep (`skills/convening`, `/council-consult`); quick writes a cited memo and no ledger; guest seats for one convening.
- **Materials gate and context folder.** Each bench declares what material each depth needs; every convening says cleared, downgraded or blind. `context/` is read first at every depth.
- **Dashboards on demand.** `--prior` on the builder computes what changed; the dashboard gets a Changes toggle, row marks and a link to the prior version; `build_effort_index.py` lists every round.
- **Standing watch.** `watch.md` per effort, a scheduled cloud routine (`orchestrator/watch.md`), triage against the ledger, log / queue / convene.
- **Show the math.** `calc` on derived evidence records.
- **Suite integration plan** for BDLC, NDLC and Total Recall (`docs/suite-integration.md`), written, not wired.

## 1.0.0 — 2026-10-20
First public release. Generalized from a private board-director's council for US healthcare services.
- Benches (one per hat), seats (one file each), efforts and rounds; round N opens by collecting answers to round N-1's requests.
- Persona library of 29 generic charters plus a template; seven presets.
- Engine: evidence ledger with tiers and the headline threshold, conflict register, rebuttal phase, evidence auditor, priority tiers, scoring against the bench's frame, assessment, principal-requests list, and the council-ledger dashboard.
- Commands: setup, bench, seat, run, round, status, doctor. Zero-install routing through CLAUDE.md; plugin manifest for marketplace install.
- Cloud orchestrator for unattended rounds delivered as pull requests.
