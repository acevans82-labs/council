# The council in the suite: NDLC, BDLC, Council, Total Recall

Status: **planned, not wired.** This file is the contract the council will honor when the handoffs are built. Nothing in it changes how the council runs today. It mirrors BDLC's `references/ndlc-integration.md` in shape.

## Which framework
- **NDLC** builds software: discovery, phases, epics, a critic that gates code, a builder, hardening, acceptance. One repo per product.
- **BDLC** runs a venture: canon, a critic that gates commitments, a six-seat Board convened inside every critic pass, `bdlc-validate` for assumptions, typed epics executed by people, readouts and funded gates. Notion is its human surface.
- **Council** deliberates: a bench per hat, a question answered with a score and an evidence ledger, round after round, at a chosen depth. No lifecycle, no gate, no verdict on anyone's plan. The home for the ad hoc, the off-plan, the deep dive, and the hats that are not ventures.
- **Total Recall** (later) is the memory: the second brain the other three read from and write to.

Rule of thumb: if the question is "is this plan ready", it is NDLC's or BDLC's critic. If the question is "what is true, how sure are we, and what would change it", it is the council.

## The one touch point with BDLC (planned)
A BDLC venture may **convene the council** from exactly two places:
1. **An escalated assumption.** `bdlc-critic` Check 2 escalates what `bdlc-validate` could not settle (REFUTED with a canon-level fix, or UNTESTABLE). The mentor may send it to the council instead of, or before, a field test.
2. **A Research epic** larger than an afternoon of desk work.

The handoff is a brief, like the Build-epic brief to NDLC: the question, the assumption IDs it carries, the venture's canon files to read as context, the depth (`quick`, `standard`, `deep`), and the bench to use (a venture's own bench, created once from `founder-venture` or `board-director` with the venture canon copied into `context/`).

The return is **evidence, never a verdict**: the council's assessment and ledger IDs land in `docs/canon/assumptions.md` as the evidence column of the assumption rows, and in `docs/validation/` as a dated report. The BDLC critic reads them on its next pass and decides. The council never sets a BDLC state, never writes a critic pass, never touches Notion.

Mechanics when built: a `convene the council on A-07` phrase in a BDLC session writes the brief into the council repo's effort folder (or the venture repo's own `council/` folder if the two live together), runs or fires the convening, and copies the result back. Until then, the mentor does this by hand: paste the brief as the effort's intake, run the round, paste the assessment's findings into the register.

## Persona alignment (planned)
BDLC's Board has six named seats. They map onto council personas; when one side improves a charter the other is updated on purpose, not by accident.

| BDLC Board seat | Council persona | Note |
| --- | --- | --- |
| Customer | `customer-buyer` (+ `end-user` when buyer and user differ) | |
| Competitor | `adversary` | the council's is named per round from the market findings |
| Regulator | `regulator` (+ `regulatory-policy` for the facts) | |
| CFO | `financial` | |
| Skeptical Investor | `investor` with the red-team posture of `pre-mortem` | |
| Operator's Advocate | `management` (mirror) + `employee` | BDLC's seat argues for the operator's time; the council splits it |

`bdlc-validate` corresponds to the council's analyst layer and its verdict scale (CONFIRMED / NARROWED / REFUTED / UNTESTABLE) maps onto evidence strength (Strong or Corroborated / Single-source / contradicted by a conflict record / a gap record with a field test designed by `options-tradeoffs`).

## NDLC
No touch point is planned. A council effort about a product decision produces a document a human can carry into NDLC discovery; nothing automates that.

## Total Recall (later)
When Total Recall exists, two flows: the council reads a bench's `context/` from it instead of from files, and the council writes each round's assessment and principal-requests back as memories tagged by bench and effort, so the next hat the principal wears can see what the last one concluded.

## What stays true regardless
- Each framework keeps its own repo, plugin and conventions. Shared ideas (chips, thread naming, doctors, cloud routines, plain-English references) are copied with attribution, not imported.
- The council stays public and dependency-free; the integrations live on the private side (BDLC) and call into it.
