---
description: Create, switch, list or edit a bench (one hat the principal wears, with its own roster and scoring frame). New benches come from a preset or from the bench-design interview. Switching sets the active bench every other command defaults to.
argument-hint: new [preset] | switch <slug> | list | edit <slug>
---

Bench operation requested: $ARGUMENTS

Read `council.md` first. If it does not exist, say so and run `/council-setup` instead.

- **new [preset]** — Run the bench-design interview from `skills/bench-design` (one batch; skip what the conversation already covers). If a preset was named, or the interview matches one, copy `presets/<preset>/` to `benches/<slug>/` and adjust it to the answers: rename seats, drop the ones that do not apply, add any the interview surfaced (per `skills/seat-authoring`), rewrite the field-specific "Starting points" prompts into real names, set the principal's seat paragraph and the organization. From scratch: write `bench.md` and `seats/` directly. Then run `python3 scripts/doctor.py`, add the row to `council.md`, set it as `active_bench`, and show the roster table and the question.
- **switch <slug>** — Set `active_bench` in `council.md`. Confirm in one line with the bench's name and its efforts.
- **list** — Show the bench index from `council.md` with, for each bench, its efforts and each effort's latest round, score and open-request count (read `score-history.json` and `ledger.json`; never dispatch anything).
- **edit <slug>** — Ask what to change: the principal's seat, the field, the question or drivers, the horizon, the other party, confidentiality, or seats (hand seats to `/council-seat`). Edit `bench.md`, run the doctor, and say in one line what changed. Changing drivers or weights after a round has run makes later scores non-comparable; say so and record it in the bench.
- **delete <slug>** — Only on an explicit request. Confirm the effort count, then remove the folder and the index row.

If the argument is blank, show the list and ask which operation.
