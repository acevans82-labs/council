---
name: seat-authoring
description: "How to add, remove or edit a seat on a bench, write a seat brief for a library persona, write a custom persona when no library charter fits, and contribute a persona back to the library. Read by /council-seat and by anyone editing seats/ by hand."
---

# seat-authoring

A **persona** is a charter in `agents/`: how a seat thinks, what it always asks, what it writes. It is generic and domain-free. A **seat** is that persona sitting on a particular bench, with a **seat brief** in `benches/<bench>/seats/<id>.md` that gives it the lens for that bench's field. Adding a seat is writing one short file. Removing a seat is deleting it.

## Add a seat from the library
1. Pick the persona: `ls agents/` and read the one-line `description` in each file's frontmatter. The library is grouped by layer: analysts establish facts, stakeholders react from a constituency, red team attacks.
2. Write `benches/<bench>/seats/<seat_id>.md`. **The file stem is the seat ID**: the tag every finding from this seat carries and the name the chair dispatches. Usually it equals the persona ID. Use a different stem when a bench needs the same persona twice with different lenses (`regulator-federal.md` and `regulator-state.md`, both `persona: regulator`; `domain-expert-clinician.md` and `domain-expert-educator.md`).
```
---
persona: <persona id from agents/>
layer: analyst | stakeholder | redteam
relevance: high | moderate | low
name: <optional display name override, e.g. "Pediatrician" for domain-expert>
---
# Seat brief — <name>

## Lens for this bench
Two to five sentences: what this seat is, in this field, on this bench. The sub-voice to speak in (a producing broker; a head of benefits; a school principal; a rival bidder's CFO).

## Starting points
Named rivals, regulators, registers, journals, forums, standards, datasets this seat should look at first. Places to start, not conclusions.

## Always asks here
Three to six questions this seat adds to its charter's list, specific to the field.

## Red flags here
Two to four field-specific signals.

## Off limits
Anything this seat must not do or read on this bench.
```
3. Add the row to the roster table in `bench.md`. Run `python3 scripts/doctor.py`.

## Remove a seat
Delete `benches/<bench>/seats/<id>.md`, remove the roster row, run the doctor. Never remove `evidence-auditor`; the chair may rate it but the bench keeps it.

## Edit a seat
Edit the seat brief. The charter in `agents/` is shared by every bench; change it only when the change is right for every bench, otherwise put the change in the seat brief.

## Write a custom persona
When no library charter fits (a seat the field needs that nothing in `agents/` covers), write the seat brief with `persona: custom` and give it the full charter inline, using `agents/_template.md` as the structure: identity, mandate, the three questions (stakeholders) or always-asks (analysts), red flags, sources, competence self-rating, what it writes. The chair dispatches it exactly like a library persona; the seat brief is its charter.

If the custom persona would serve other benches, promote it: copy the charter into `agents/<id>.md` with the frontmatter from `_template.md`, make it domain-free, and change the seat brief to `persona: <id>` with only the lens left behind. Contributions to the public library are welcome by pull request; keep them generic and give them a one-line `description` that says which layer and which constituency.

## Naming
Persona IDs and seat IDs are lowercase with hyphens. The seat ID (file stem) is the tag every finding carries (`persona: channel-partner`) and the `persona_id` in the roster. Keep them short and stable; renaming a seat invalidates the tags in every past ledger of that bench.
