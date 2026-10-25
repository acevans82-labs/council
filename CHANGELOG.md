# Changelog

## 1.3.0 — 2026-10-24
Lessons from the first cloud rounds, built into the engine.
- **Budget first.** Every standard or deep run (and any consult with more than three seats) is planned with the principal before anything is spent: a dollar ceiling, the seats, a model per seat with one line of why, an estimate from measured costs, and a one-screen summary of the job and what it delivers. Nothing is dispatched until the principal says go (`skills/run-planning`). The plan is written into the brief as a `### Model plan` table, and the chair sends each seat out on the model it names. Why: a deep round can cost $90 or $500 depending on the models, and the principal should choose that, not discover it.
- **Cost receipts.** `scripts/cost_report.py` reads the session's own transcripts, prices every message per model, and compares the result with the plan, phase by phase. Every round's close includes the receipt, with a reason for any phase that went over. Why: the next plan starts from real numbers.
- **Plain words when a run stalls.** The receipt and the home thread detect a monthly spend limit, used-up credits, a plan limit or a network failure, and say what stopped the run and how to resume it. Why: a cloud round that hit the spend cap stopped silently, with no PR and no message.
- **Three seats per turn.** Web search is capped at 200 calls per chair turn across every subagent, so the chair now sends seats out in groups of at most three, each with its own search budget. Why: ten analysts launched at once shared one allowance and ran dry.
- **Network check.** A cloud round proves it can open web pages before dispatching anyone, and stops with a BLOCKED pull request if it cannot. Why: an environment with Limited network made every page fetch fail and the round produced drafts from search snippets.
- **Resuming a stopped round.** `resume <bench>/<effort> <round_id>` continues on the round's branch, keeps every merged phase, and treats unmerged seat files as drafts to verify.
- **Every round delivers the dashboard and the ledger.** The close (`skills/round-close`) builds them, sends them to the principal (SendUserFile where available) and links them in the PR. Why: the dashboard is the thing people read, and it was sometimes left in the branch.
- **Questions on material pivots, and only then.** When a premise turns out false, the milestone cannot be reached as framed, or a new fact flips the question, the chair stops and asks (locally a question; in the cloud a `QUESTION.md` and a PR titled `QUESTION: …`) instead of finishing on the old frame. Ordinary findings never stop a round.
- **Plan locally, then fire.** Intake and planning always happen in the local thread. A cloud round fired without an approved plan stops with `PLAN NEEDED`.
- **Local browser for the principal's side.** In the local thread the council may use the built-in browser, or Claude in Chrome for logged-in sources such as LinkedIn, to gather principal-side evidence before a round, saved as documents. Facts about people stay within their public and professional capacity.
- **Thread swap.** `/council-swap` (`skills/thread-swap`) hands a long home thread to a fresh one with the full live state (effort, round, phase, open asks, pending decisions, running cloud sessions), and the old thread can then be archived. The home thread offers it when it gets long.
- **Cloud routines at setup.** `/council-setup` now creates the round routine (and the watch routine when needed) through `RemoteTrigger`, on an environment with Full network access, after checking the Claude GitHub app, and records the routine, environment and connectors in `council.md` (`skills/cloud-routines`). `docs/cloud-setup.md` explains the search cap, the network requirement, the spend cap, branch-name suffixes and why a run marked "succeeded" may still be working.
- **Doctor.** Checks the engine version against the latest release on every thread's first turn (with Update now, Skip, Remind me in 3 days), the workspace `CLAUDE.md` and `AGENTS.md` against the template, the `## Cloud` records, the shape of each brief's model plan, seat frontmatter, and waiting QUESTION or BLOCKED files. `/council-doctor` adds live checks of each routine: it exists, is enabled, runs on the recorded Full-network environment, and carries the connectors the local session has. Exit code 3 now means an update is available.
- **Workspace template 1.3.0.** `CLAUDE.md` runs the doctor's quick check on the first turn of every new thread and describes the home thread; `AGENTS.md` points at the engine's rules. What a workspace needs: update the engine pointer, copy both template files over (the doctor offers it), and add `environment:`, `github_app:` and `connectors:` lines under `## Cloud` in `council.md` (`/council-doctor` fills them). Existing ledgers and benches need nothing.
- `orchestrator/orchestrate.md` and `orchestrator/watch.md` changed materially (plan check, network check, groups of three, resume, question, close). Routine prompts that reference the files pick this up at the next fire; anyone who pasted a copy into a routine should re-paste it.

## 1.2.2 — 2026-10-22
- The update prompt now shows the release notes between your version and the latest; it was reading the changelog from the wrong ref.

## 1.2.1 — 2026-10-22
- `check_update.py --apply` no longer refuses over untracked files in the engine clone; only tracked changes count as a dirty tree.

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
