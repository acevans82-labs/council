---
description: First-run setup for the council. Checks the tools, learns who the principal is and which hats they wear, writes council.md, builds the first bench from a preset or from scratch, and creates the cloud routine (on an environment with Full network, with the GitHub app and the account's connectors) by default. Safe to re-run; it never overwrites a bench or a routine.
argument-hint: [nothing, or a few words about who you are]
---

Set up this council for the person in front of you. Notes from them, if any: $ARGUMENTS

Work through these in order. Skip anything that is already done; say so in a line.

1. **Preflight.** Run `python3 scripts/doctor.py --quick`. It checks that python3 is present, the engine files are intact, and reports whether `council.md` exists. If `council.md` already exists, say so, show the bench index, and skip to step 4.
2. **The principal.** Ask, in one message: their name; how they want to be referred to in outputs (default: "the principal"; outputs never say "you"); the hats they wear that they might bring to a council (one line each, e.g. "board member at two companies", "founder vetting ideas", "head of regulatory at my company", "parent"). Then write `council.md`:
   ```
   ---
   principal: <name>
   address_as: the principal
   active_bench: <set in step 3>
   created: <today>
   ---
   # Council — <name>
   ## Benches
   | slug | name | role | noun | efforts | last round |
   | --- | --- | --- | --- | --- | --- |
   ## Hats not yet benched
   - <each remaining hat from the interview, so /council-bench can pick them up later>
   ## Cloud
   routine: not set up
   watch_routine: not set up
   environment: not set up
   github_app: not checked
   connectors: not checked
   ```
3. **The first bench.** Pick the hat they want first and run the bench-design interview from `skills/bench-design` (offer the matching presets from `presets/`; a preset is copied to `benches/<slug>/` and then adjusted). Write `bench.md`, `seats/` and `context/` (ask for whatever already exists that every convening should know: an overview, a strategy, a glossary; drop it in and list the rest in `context/README.md`), add the row to `council.md`, set `active_bench`. Run `python3 scripts/doctor.py` and fix what it reports.
4. **Cloud routines (the default).** Say in two lines: rounds run best as a cloud routine that works unattended for hours and delivers a pull request; planning and intake always stay here in this thread. Then follow `skills/cloud-routines` with them: preflight (workspace on GitHub, the Claude GitHub app on its owner, an environment with **Full** network access, created or chosen, browser-assisted where a page must be filled), create the round routine through `RemoteTrigger`, and the watch routine too if any effort will be watched. Each account change is a button the principal clicks. Then check the routine carries the connectors this session has and report any gap in plain words. Record `routine:`, `watch_routine:`, `environment:`, `github_app:` and `connectors:` under `## Cloud` in `council.md`. If the session has no `RemoteTrigger` tool, walk the principal through `docs/cloud-setup.md` instead. If they decline cloud, leave `routine: not set up`; rounds will run here.
5. **Close.** Tell them the roster of the first bench in one compact table and the question it answers in one line. Then offer: "Start the first effort with /council-run <name of the thing>", "Add another bench with /council-bench new", or "Change a seat with /council-seat".

Never invent a hat, a field or a seat the principal did not describe. Never overwrite an existing bench; `/council-bench edit` does that on purpose.
