---
name: standing-watch
description: "Standing research on an effort between rounds: a scheduled scan of the bench's sources for the effort's watch terms, a triage pass that checks each hit against the ledger's headline findings and open items, and an action (log, queue for the next round, or convene at a chosen depth). Defines watch.md, the watch log and the watch brief. Read by /council-watch and by orchestrator/watch.md."
---

# standing-watch

A round is a sitting; a watch is the clerk who reads the papers every morning and knocks on the door only when something changes. It never deliberates and never scores. It scans, triages against what the council already found, and either logs, queues, or convenes.

## watch.md (in the effort folder)
```
---
enabled: true
cadence: nightly | weekly | monthly | quarterly
created: YYYY-MM-DD
last_scan: YYYY-MM-DD | never
terms:
  - <names, rules, rivals, topics, exact phrases>
sources:
  - bench primary sources            # the bench.md "Primary sources in this field" list
  - <extra URLs, feeds, registers, journals>
lookback_days: 8                     # how far back each scan looks; a little more than the cadence
material_if:
  - touches a headline finding       # the defaults; edit freely
  - closes or reopens an open gap
  - answers or changes an open request to the principal
  - names a rival move, a rule change or a transaction in the effort's arena
on_material: queue | quick | standard   # queue = log and wait for the next round; quick/standard = convene now
notify: pr                            # the watch brief arrives as a pull request; add "sms:<number>" or "linear" if the routine's environment supports it
budget:
  scan_model: cheap                   # a cheaper model for the scan is fine; triage uses the session default
  max_hits_per_scan: 25
---
```

## The three stages
1. **Scan.** For each term across each source, within `lookback_days`, collect hits: title, source, date, URL, one-line excerpt. Deduplicate. Cap at `max_hits_per_scan`, keeping the most recent. A scan that finds nothing writes one log line and stops.
2. **Triage.** Read the effort's `ledger.json`: headline findings, open gaps, open requests, unresolved conflicts, and the pre-mortem's early signals. For each hit decide `ignore` (no bearing), `log` (bears on the effort but changes nothing yet), or `material` (meets a `material_if` rule; name which finding, gap, request or signal it touches, by ID). Triage reads the ledger; it never writes records.
3. **Act.** Append every non-ignored hit to `watch-log.md` (date, verdict, the IDs touched, locator). If any hit is `material`: write a **watch brief** (`watch/<YYYYMMDD>-brief.md`: the material hits with the IDs they touch, why they matter in two sentences each, and the recommended action) and then follow `on_material`: `queue` leaves the brief as the trigger for the next round and tells the principal; `quick` or `standard` convenes now with the brief as the trigger, per `skills/convening`, and the round's intake registers the brief's hits as `E-` records.

## What runs it
A scheduled Claude Code cloud routine, `council-watch-<repo>`, firing with the payload `watch all` (every enabled watch whose cadence is due) or `watch <bench>/<effort>`. Procedure in `orchestrator/watch.md`. One routine serves every bench and effort in the repo; the cadence lives in each `watch.md`, and the routine's schedule only needs to be at least as frequent as the shortest cadence (nightly covers everything). `/council-watch brief` runs one scan by hand when the principal cannot wait.

## Standards
- A hit is evidence only when a round registers it. The log is a lead list, not a ledger.
- Triage cites the ledger ID it is matching against; "feels relevant" is `ignore`.
- A watch never convenes at `deep`; a deep round is the principal's call.
- Scans are cheap and boring by design. The cost is in convenings, and `on_material: queue` keeps that at zero until the principal says otherwise.
