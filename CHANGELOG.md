# Changelog

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
