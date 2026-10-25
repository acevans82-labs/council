---
name: council-ledger
description: "Builds the council ledger dashboard for every council round: the minutes of the council (who found what, what was contested, where the chair ruled, where the principal was asked, how the effort lands with each stakeholder, the score and its drivers) as a standalone HTML file with an executive view, a narrative view for sharing and an audit view for tracing. Always produced at the end of a round. Also use when the principal asks how the council reasoned or wants to see the dashboard."
---

# council-ledger

Built from `ledger.json`; nothing is written by hand. A thin ledger makes a thin dashboard, and that is the honest outcome.

Three views, one file:
- **Executive summary** — the default view, two or three sheets at most, for the principal in two minutes: score and drivers, the verdict in plain language, **where to start** (every open item across the round, counted and colored by priority tier, with every Tier 0 shown in full), the principal's stated questions answered, act-by-date items, the decisions only the principal can make, the documents to supply first, the top conflicts in the data, and the risk callouts. Rendered from `exec_summary` in the ledger; if that block is missing the view is hidden and the build script warns. A round without it is incomplete.
- **Narrative** — for sharing with a board, a team, a partner: score and drivers, who sat, how the council ran, how the effort lands with each stakeholder, headline findings, disagreements, judgment, what remains open.
- **Audit** — for tracing: a **Principal's queue** tab (every judgment call, every gap raised to the principal, and every unresolved conflict, one filterable list, sorted by priority tier) first, then timeline by phase, personas, every finding with filters, conflicts, rulings and requests, every evidence record, gaps and open questions. Table headers stay pinned while a long table scrolls.

## Before building
Check the ledger is complete enough to render: each `phases` record has a `summary` that reads like minutes and `notable` moments; each `R-` has `rationale`; each `J-` has `why_principal` and a `tier`; each `gaps[]` record with `raised_to_principal: true` has a `tier`; each unresolved `conflicts[]` record has a `tier`; each stakeholder roster entry has a `view`; `assessment` has `label`, `score`, `band`, `drivers` and `verdict`; `effort.noun` is set; and `exec_summary` is present per `skills/assessment-output`. Fill any that are missing from the round's context before building.

## Priority tiers — the vital few, not a quota
Every `judgment_calls[]` record, every `gaps[]` record with `raised_to_principal: true`, and every `conflicts[]` record the chair has not resolved (`resolved_by` missing or `"unresolved"`) carries a `tier` (integer 0–3), assigned by the chair at synthesis:
- **0 — Must-have.** Blocks a near-term decision or deadline, or the numbers behind the verdict itself cannot be trusted without it.
- **1 — High-value.** Materially moves a scoring driver or de-risks a Tier 0 item, with no hard deadline of its own.
- **2 — Useful.** Corroborates or adds precision; the verdict would not change without it.
- **3 — Nice-to-have.** Narrow, cosmetic, or already deferred by the principal.

Tier by actual leverage against the round's decisions and deadlines, never by padding toward a target percentage. A good round typically lands with roughly a fifth of its open items at Tier 0 ("the 20% that gives 80% of the confidence"), but that is an observation about leverage being concentrated, not a quota. Add an optional `tier_rationale` (one sentence) on Tier 0 items; the dashboard shows it in the record drawer. `build_dashboard.py` warns if a principal-facing record has no tier.

## The evidence web — every ID is alive
Every `E-`, `F-`, `C-`, `R-`, `J-`, `G-`, `H-` and `Q-` token that appears anywhere in the rendered page is auto-detected and turned into a clickable cross-reference. No persona or chair ever writes a link.
- **Hover** an ID for a preview card: the record's statement, its "so what," confidence/evidence/tier tags, and (for findings) which evidence backs it.
- **Click** an ID to open it in a side drawer with every field the ledger has for that record, linkified too, with a breadcrumb trail and a Back button.
- **"Show in Audit"** in the drawer jumps to the Audit view, on the correct tab, scrolled to that row.
- **Phase stops** in the left-hand spine jump to that phase in the Audit Timeline tab.
- **Tier badges** in the executive summary jump to the Principal's queue, pre-filtered to that tier.

Nothing in `ledger.json` should contain a stray ID-shaped string that is not a real record; the linkifier will try to make it clickable.

`exec_summary` schema — every string is principal-grade prose, cites ledger IDs inline, and the whole block prints to two or three sheets:
```json
"exec_summary": {
  "verdict":       "3–6 sentences, plain language",
  "urgent":        [{"text": "…", "by": "10/9"}],
  "answers":       [{"q": "the principal's stated question", "a": "the council's answer"}],
  "decisions":     [{"id": "J-005", "text": "one line per judgment call"}],
  "decisions_note": "optional: where the rest of the list lives",
  "documents":     [{"id": "G-054", "text": "top document requests, five at most"}],
  "conflicts":     [{"id": "C-025", "text": "top conflicts in the data, five at most"}],
  "risks":         ["top risk callouts, five at most — prose only, not tied to a single ID"],
  "bottom_line":   "one closing paragraph"
}
```
`decisions`, `documents` and `conflicts` entries carry the `id` of the underlying record so the dashboard can show its tier badge. The "Where to start" section and the Principal's queue tab are computed directly from the raw arrays, so every principal-facing item appears somewhere even if it did not make the curated lists.

## Build
```bash
# round 1
python3 skills/council-ledger/scripts/build_dashboard.py benches/<bench>/efforts/<effort>/ledger.json benches/<bench>/efforts/<effort>/dashboards/<round_id>-council-ledger.html
# round 2 and later: pass the prior round's archived ledger so the dashboard can show what changed
python3 skills/council-ledger/scripts/build_dashboard.py benches/<bench>/efforts/<effort>/ledger.json benches/<bench>/efforts/<effort>/dashboards/<round_id>-council-ledger.html --prior benches/<bench>/efforts/<effort>/rounds/<prior_round_id>/ledger.json
# every round: refresh the effort's index of rounds
python3 scripts/build_effort_index.py benches/<bench>/efforts/<effort>
```
Standalone HTML, no dependencies beyond web fonts with system fallbacks. Send the round's dashboard to the principal; the index is the place to find every earlier one.

## Dashboards on demand: history and changes
Add `--artifact <path>` to also write the variant published as a claude.ai Artifact (no document wrapper, a specific title, phone-width layout, a scan for personal contact details; `--redact` removes them). `skills/round-close` publishes it at every close.

Every round keeps its own dashboard under `dashboards/`; nothing is overwritten. With `--prior`, the builder computes the change set and the dashboard gets:
- a **Changes** toggle in the header (on by default) that shows or hides everything below;
- a **What changed** block at the top of the executive and narrative views: score and band movement, drivers that moved, requests answered, gaps closed, conflicts resolved, headlines demoted, counts of new and changed records, and a link to the prior round's dashboard;
- **row marks** in every Audit table (green for new this round, amber for a carried record that changed) and a badge in the record drawer;
- the meta line shows the round's depth and, when not cleared, the materials-gate result.
`dashboards/index.html` (from `scripts/build_effort_index.py`) lists every round with score, movement and links, plus consults and watch briefs. The written assessment's redline is git's: `git log -p -- benches/<bench>/efforts/<effort>/assessments/`.

## What the principal should see in under a minute
- The score, its band, and the three things that moved it.
- Which of the round's open items are must-have and why.
- How the effort lands with each stakeholder.
- Where the chair stepped in and why.
- What the council needs from the principal.
- The conflicts, with public-disclosure ones marked.

If the narrative view does not answer those without scrolling, the ledger is missing something. Fix the ledger, not the template.

## Editing the template
`assets/dashboard-template.html` is plain HTML/CSS/JS with the ledger injected at `/*__LEDGER__*/`. For a different look, edit the template and rebuild; the schema does not change. The template reads `effort.noun` and `assessment.label` so the wording follows the bench.
