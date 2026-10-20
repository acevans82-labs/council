---
name: rebuttal-round
description: "The stakeholder rebuttal phase of a council round. After the red team attacks, every rostered stakeholder gets one bounded pass to defend or revise its view, rebut other stakeholders by name, and respond to red-team challenges that touch its seat. Read by rebutting stakeholders after persona-protocol and stakeholder-protocol. A bench may switch this phase off in bench.md."
---

# rebuttal-round

Deliberation, not repetition. You have read the other seats' views and the red team's attack; now say where they are wrong, where they changed your mind, and what that does to your view. A rebuttal that restates your original findings is a wasted seat.

## Inputs
The merged ledger now contains every stakeholder's findings and `view`, the Adversary's attack and the Pre-mortem's failure stories. Read them all. You already know your own prior file.

## What you may do — one pass, no chains
1. **Defend or revise your view.** Write `view_revised`: one paragraph in your voice. If unchanged, say in one clause why the challenges do not move you.
2. **Rebut by name.** For each seat or red-team persona you engage, a `responds_to` entry: `{persona, finding_id, stance: support|rebut|revise, note}`. Engage the strongest opposing point that touches your seat, not the weakest. Do not pile on findings nobody contested.
3. **Contest on the record.** Evidence rules do not relax: contest a finding by appending to its `contested_by`; conflicting evidence is a `C-` record. A rebuttal claim needs an `E-` record like any other claim. Limited new retrieval is allowed only to source a rebuttal claim, per `skills/exhaustive-retrieval`.
4. **Change your mind honestly.** If a red-team challenge or another seat's evidence moves you, revise the relevant findings with `supersedes` set and say what changed. Do not converge to be agreeable; do not hold a position to look consistent.

## What you may not do
- No new lines of inquiry outside your seat's three questions.
- No rebuttals of rebuttals; the phase is one pass, and the analysts' answer pass and the Evidence Auditor come after you.
- Never edit another persona's file or records.

## Output
One file: `rounds/<round_id>/rebuttal-<persona_id>.json`, in the ledger's record shapes with temp IDs (`rebuttal-channel-partner-E-1`), containing: `view_revised`, `responds_to`, and any new or superseding `E-`/`F-`/`C-` records tagged with your persona. Then return the five-line summary of `skills/persona-protocol`, with line 5 replaced by: the one thing this phase changed your mind about, or "held everything" and the strongest challenge you survived.

## Chair's handling
Merge in dispatch order. `view_revised` replaces the roster `view` (the original stays in the persona's phase file). The rebuttal phase never restores anything the Evidence Auditor later demotes.
