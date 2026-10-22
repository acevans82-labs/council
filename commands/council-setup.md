---
description: First-run setup for the council. Checks the tools, learns who the principal is and which hats they wear, writes council.md, builds the first bench from a preset or from scratch, and offers to wire the cloud routine. Safe to re-run; it never overwrites a bench.
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
   ```
3. **The first bench.** Pick the hat they want first and run the bench-design interview from `skills/bench-design` (offer the matching presets from `presets/`; a preset is copied to `benches/<slug>/` and then adjusted). Write `bench.md`, `seats/` and `context/` (ask for whatever already exists that every convening should know: an overview, a strategy, a glossary; drop it in and list the rest in `context/README.md`), add the row to `council.md`, set `active_bench`. Run `python3 scripts/doctor.py` and fix what it reports.
4. **Cloud mode.** Explain in three lines: a round can run here in this session (fine for a first effort; takes a while and the laptop stays open) or as a cloud routine that runs unattended and delivers a pull request. If they want cloud, follow `docs/cloud-setup.md` with them now and record `routine: council-<repo>` under `## Cloud` in `council.md`; otherwise leave `routine: not set up` and move on.
5. **Close.** Tell them the roster of the first bench in one compact table and the question it answers in one line. Then offer: "Start the first effort with /council-run <name of the thing>", "Add another bench with /council-bench new", or "Change a seat with /council-seat".

Never invent a hat, a field or a seat the principal did not describe. Never overwrite an existing bench; `/council-bench edit` does that on purpose.
