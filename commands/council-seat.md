---
description: Add, remove, edit or list seats on a bench. Add from the persona library or write a custom persona; remove by deleting the seat file; edit the seat brief. Changes take one short file.
argument-hint: add <persona> [bench] | remove <seat> [bench] | edit <seat> [bench] | list [bench] | library
---

Seat operation requested: $ARGUMENTS

Read `council.md` for the active bench; a bench named in the arguments overrides it. Follow `skills/seat-authoring`.

- **library** — List every persona in `agents/` grouped by layer with its one-line description, and `_template.md` for custom ones. Nothing else.
- **list [bench]** — Show the bench's seats from `benches/<bench>/seats/`: seat ID, persona, layer, default relevance, one-line lens.
- **add <persona> [bench]** — If the persona exists in `agents/`, ask only what the seat brief needs (lens, sub-voice, starting points, anything off limits; three or four questions at most, in one message), then write `seats/<seat_id>.md`, add the roster row to `bench.md`, run `python3 scripts/doctor.py`. If no library persona fits, write a custom seat with `persona: custom` and the full charter inline, from `agents/_template.md`; offer to promote it to the library if it would serve other benches. The same persona can sit twice under different seat IDs.
- **remove <seat> [bench]** — Delete `seats/<seat_id>.md` and the roster row; run the doctor. Refuse to remove `evidence-auditor` and say why (the bench keeps its auditor; the chair may rate it Low). Past ledgers are untouched.
- **edit <seat> [bench]** — Ask what to change and edit the seat brief. If the change is about how the seat thinks rather than what it looks at in this field, say that belongs in the shared charter in `agents/` and would affect every bench, and ask before touching it.

Close every operation with the bench's updated roster in one compact table.
