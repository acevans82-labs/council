---
description: Standing research on an effort between rounds. Turn a watch on or off, set its terms, sources, cadence (nightly, weekly, monthly, quarterly) and the depth it convenes at when something material lands, or show what the watch has logged. The scan itself runs as a scheduled cloud routine.
argument-hint: on <effort> | off <effort> | edit <effort> | status [effort] | brief <effort>
---

Standing watch operation: $ARGUMENTS

Read `council.md` for the active bench (a `bench/` prefix overrides it) and `skills/standing-watch`.

- **on <effort>** — Ask in one message: what to watch for (terms, names, rules, rivals, topics), where (the bench's primary sources by default, plus anything the principal names), how often (nightly / weekly / monthly / quarterly), what counts as material (default: anything that touches a headline finding, an open gap or an open request), and what to do when it is (default: log and queue for the next round; or convene at `quick` / `standard`). Write `efforts/<effort>/watch.md`. Then say what makes it run: the `council-watch-<repo>` routine on the chosen schedule (`docs/cloud-setup.md`), and whether that routine exists per `council.md`'s `## Cloud` section. If it does not, walk the principal through creating it now or record it as pending.
- **off <effort>** — Set `enabled: false` in `watch.md`; keep the log.
- **edit <effort>** — Change any field; re-print the watch in one compact block.
- **status [effort]** — For each watched effort: cadence, last scan date, hits logged since the last round, convenings fired. Read-only.
- **brief <effort>** — Run one scan and triage pass here, now, instead of waiting for the schedule, following `orchestrator/watch.md` steps 2–4 without the commit-and-PR close; show the watch brief in chat.
