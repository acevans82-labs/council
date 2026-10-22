---
description: Run the next round on an existing effort. Opens with the council's open requests from the last round so the principal can answer them, takes new documents and what changed, carries evidence forward, re-runs the seats the round touches, and reports what moved. This is how an ongoing effort continues, round after round.
argument-hint: <effort> [what's new, or answers] [standard|deep] — or <bench>/<effort>
---

Start the next council round for: $ARGUMENTS

Steps, in order:

1. **Resolve.** Read `council.md` for the active bench (a `bench/` prefix overrides it). Confirm `benches/<bench>/efforts/<effort>/ledger.json` exists; if not, say there is no prior round and offer `/council-run`. Compute the next round number from `score-history.json` and the round ID `r<N>-<YYYYMMDD>`.
2. **Depth and gate.** Depth is `deep` unless the arguments say `standard`; apply the materials gate per `skills/intake`. If a promoted consult or a watch brief is the trigger, read it first.
3. **Open requests first.** List the last round's open items by ID, Tier 0 first: judgment calls without answers, gaps raised to the principal and still not found, unresolved conflicts, any headline waiver requested. Then run the later-round intake batch from `skills/intake` in one message: answers by ID (partial is fine), what prompted this round, new documents, scope (scoped by default, full on request). Anything already in the arguments counts as answered.
4. **Carry forward.** Per `skills/intake` and `skills/evidence-ledger`: write answers into the carried `J-` records and as new T1 evidence; archive the prior ledger to `rounds/<prior_round_id>/ledger.json`; carry evidence, conflicts, gaps and judgment calls; re-verify evidence older than 90 days; carry score history whole. Append a "Round N answers" section to `brief.md`.
5. **Where to run.** Same choice as `/council-run` step 3: cloud routine with payload `round <bench>/<effort>: <trigger>` (add ` full` for a full re-run), or here.
6. **Run here.** Read `agents/chair.md` and act as the chair. Decide which seats the trigger and the answers touch and say so in one line (an answer about the numbers touches the financial analyst and the investor at minimum; a rival's move touches market-competitive, product-positioning, channel-partner, key-partner and the adversary; a rule change touches regulatory-policy and every regulator and policy seat; "refresh" or "full" re-runs everything). The Evidence Auditor always runs. Dispatch, merge, reconcile, score.
7. **Close** with: what changed since the last round and which principal answers drove it; the new score with movement and which drivers moved; the assessment and dashboard files; and the principal-requests list for the next round, Tier 0 first.
