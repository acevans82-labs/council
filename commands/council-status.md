---
description: Show the state of every bench and effort, or one of them. Latest score and band, movement, last round and trigger, open requests to the principal, open gaps, unresolved conflicts. Read-only.
argument-hint: [bench, bench/effort, or blank for everything]
---

Report council status for: $ARGUMENTS (everything if blank).

Read `council.md`. For each bench (or the one named), and each effort under it (or the one named), read `ledger.json` and `score-history.json` and produce one compact table row: bench, effort, latest score ± band with the score label, movement since the prior round, last round ID and date, trigger, count of open requests to the principal, count of open gaps raised to the principal, count of unresolved conflicts. Below the table, for each effort list the open requests by ID, tier and question, one line each, Tier 0 first.

Mark the active bench. Benches with no efforts show "no efforts yet"; efforts with no ledger show "intake only".

Do not dispatch any persona, retrieve anything, or change any file.
