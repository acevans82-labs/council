---
description: Consult the council on a question at a chosen depth. quick (default, 5–10 minutes) gives a cited memo from the seats that matter and writes no ledger; standard (30–60 minutes) and deep (hours) run a scored round. Say "promote" afterwards to turn a quick consult into the next round's trigger.
argument-hint: <question or effort> [quick|standard|deep] [bench/]
---

Consult the council: $ARGUMENTS

1. **Resolve.** Read `council.md` for the active bench (a `bench/` prefix overrides it). Decide the depth from the arguments; default `quick`. Decide the effort: an existing one the question belongs to, or a new effort with a two-line brief (name, the question). Read `skills/convening`.
2. **Materials gate.** Per `skills/intake`: cleared, downgraded or blind, in one line.
3. **quick.** Follow the quick consult procedure in `skills/convening`: frame, pick up to five seats (add a guest seat if needed), one sitting in parallel, the memo. Save it under `efforts/<effort>/consults/`, send the file, and close with the answer, its confidence, and the one-line promote offer.
4. **standard or deep.** This is a round. If the effort has no ledger, continue as `/council-run` at that depth; otherwise as `/council-round` at that depth. Say so in one line and proceed.
5. **promote** (a later message): register the memo's citations as `E-` records, set the memo's question as the next round's trigger in `brief.md`, and offer to start the round now.

Never write ledger records from a quick consult. Never let a quick answer skip the confidence line or the citations; "not checked" is the honest cell.
