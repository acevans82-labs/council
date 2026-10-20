---
description: Check the council workspace and fix what can be fixed. Engine files, council.md, every bench and its seats, every effort's ledger, the roster tables, driver weights, and whether the cloud routine is recorded. Run it when something looks off or after editing files by hand.
argument-hint: [--quick]
---

Run `python3 scripts/doctor.py $ARGUMENTS` and read its report.

For each problem it names: fix it if the fix is mechanical and safe (a missing roster row, a weight table that does not sum to 100 where the intent is obvious, a seat whose persona is misspelled, a missing `index.md`), say what you changed, and re-run the doctor. For anything that needs the principal's judgment (a bench with no analysts, a custom seat with no charter, an effort with no brief), ask in one message.

Never touch a ledger's records; the doctor reports ledger problems and the fix is a new round, not an edit.
