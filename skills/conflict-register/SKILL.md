---
name: conflict-register
description: "Cross-source reconciliation for a council round. Compares what supplied material says against primary and third-party sources, logs every contradiction with both values and both sources, scores whether the conflict is real, and escalates conflicts between principal-supplied material and public statements. Run by the chair after each phase and by any persona that finds two evidence records that cannot both be true. Conflicts are never silently resolved."
---

# conflict-register

When two sources disagree, that disagreement is one of the most useful things the council can find. It is either a definitional difference the principal needs to understand, or a question someone needs to answer. Either way it goes into the assessment; never quietly to one side.

## When to run
- After each phase, before the chair synthesizes.
- Immediately when a persona notices two `E-` records that cannot both be true.
- Immediately when two personas cite different values for the same quantity.

## Procedure
1. **Pair the records.** Both `E-` IDs must exist. If one side is an unrecorded impression, record it first.
2. **Rule out non-conflicts.** Different periods, different definitions (gross vs. net, adjusted vs. reported, consolidated vs. segment, members vs. accounts), different scope, run-rate vs. actual, rounding, date. If one of these fully explains the difference, add a note to the evidence records and do not log a conflict.
3. **Log the conflict.** `C-` record with both values, both tiers, `confidence_real`, and `likely_cause`.
4. **Set `public_disclosure_relevant`.** True when one side is a public statement by the subject of the effort (filing, press release, regulator submission, published claim) and a principal-supplied document says something materially different. These are always headlines and always go to the principal.
5. **Hand off.** Route to the persona best placed to resolve it: the numbers analyst for figures, the rules analyst for rules and licenses, the market analyst for share and rival claims, the management mirror for the subject's own inconsistencies, the Evidence Auditor for source quality.

## Resolution
- A conflict resolves only three ways: the chair rules (`R-` record) with rationale the evidence supports; the principal rules (`J-` record); or it stays `unresolved` and goes into the assessment's open items.
- The chair may rule when the cause is clearly definitional or clearly a T3 error, or when one side's evidence is materially stronger. The chair may not rule when both sides are corroborated and the disagreement is about weighting, or on any `public_disclosure_relevant` conflict.
- "Resolved" never means one value was deleted. Both stay in the ledger.

## Output to the chair
Count of new conflicts; `public_disclosure_relevant` ones first; ones needing the principal; ones the chair can rule on.
