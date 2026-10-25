---
name: exhaustive-retrieval
description: "Search doctrine for council personas: supplied documents and principal answers first, then primary public sources, then third party; 24-month lookback by default; wrong-entity stop; should-exist-but-missing sources become gap records. Read before the first retrieval of a round."
---

# exhaustive-retrieval

"Couldn't find it quickly" is not an end state. Search until the fact is corroborated or the trail is exhausted, then record either evidence or a gap.

## Source order
1. **Supplied documents and principal answers (T1).** Always first. Read the effort folder's `documents/index.md` and the brief's answers section. Cite by document name and page or section, or "principal answer, round N".
2. **Primary public sources (T2).** Filings, registers, regulators, statutes and rules, court records, official statistics, peer-reviewed research, standards bodies, procurement records. The bench's `bench.md` and your seat brief name the ones that matter in this field; `references/regulatory-sources.md` is a starter list by business type that any bench can extend.
3. **Third party (T3).** Press, analyst and vendor reports, comparison and review sites, funding databases, conference material, job postings, websites (use archived versions to see change over time), forums and communities. Use to corroborate or where T1/T2 are silent.

## Lookback
24 months standard. Go further when a persona states why (a rule change, a transaction, a restatement, a long-running study base). A bench may set a different default in `bench.md`.

## Wrong-entity stop
If you believe an entity is registered, licensed, listed or published and cannot locate it after a reasonable search, stop. Write a `G-` record, flag that the legal entity, name or identifier may differ, and continue with what you have. The chair will raise it to the principal.

## Regulated or documented domains
If the nature of the effort implies that official documents exist (licenses, filings, registrations, approvals, published guidelines, trial registrations, accreditation), find them or record the gap. Never assume a document exists because it should.

## Search budget
Web search is capped at 200 calls per chair turn, shared by every seat launched in that turn, so every seat has a budget (the chair passes it: 40 by default, 20 for a bounded seat, 10 for a rebuttal). Search to find sources; read them with WebFetch rather than searching again. When search runs out, keep fetching URLs you already have and record the rest as gaps with where you would have looked.

## Browser
When search cannot reach a source (form-based databases, portals behind selectors, PDF-only registers), use the browser tools available in the session. Record the URL you landed on as the locator. A cloud round has no logged-in browser: sources behind a login (LinkedIn, Instagram, a members-only register) are gathered in the principal's local thread before the round is fired (`skills/intake`, principal-side evidence) or recorded as gaps with `principal_could_supply: true`. Facts about named people stay within their public and professional capacity.

## Gaps
A gap is a source you had good reason to expect and could not find. Write `G-` with what you expected, why, where you looked, and `principal_could_supply` if the principal plausibly has it. Set `raised_to_principal: true` when the gap would change a finding's strength. Never downgrade a gap to "probably fine."

## What every retrieval writes
An `E-` record with tier, reliability, locator, timestamp and recorder, or a `G-` record. Nothing else counts.
