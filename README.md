# Council

**A swarm with seats.** A council of AI personas (analysts, stakeholders, a red team and a neutral chair) that deliberates on whatever you bring it, round after round, with every claim traced to an evidence ledger. Runs inside Claude Code, locally or as an unattended cloud routine.

You wear several hats. Each hat gets a **bench**: a board member's bench, a founder's bench, a head-of-regulatory bench, a parent's bench. Each bench has the seats that hat needs and a question it answers with a score. Each thing a bench works on is an **effort**. Each pass of the council on an effort is a **round**, and round N picks up exactly where round N-1 left off: the council tells you what it needs from you, you answer what you can, and it carries the rest forward.

## Install in five minutes

1. **Make your own copy.** Click **Use this template** on GitHub (private is fine), then clone it:
   ```bash
   gh repo create my-council --template acevans82-labs/council --private --clone
   ```
   Or just `git clone` this repository.
2. **Open it in Claude Code** and say "set up my council". There is nothing to install: `CLAUDE.md` routes plain words to the commands. (If you prefer slash commands, install it as a plugin: `claude plugin marketplace add acevans82-labs/council` then `claude plugin install council@council`.)
3. **Answer the setup questions**: who you are, which hats you wear, which one to bench first. Setup offers a preset that matches and adjusts it with you.
4. **Bring the first effort**: "run the council on Acme" or "vet this idea". Intake is one batch of questions; then the council runs. For a quick answer, "consult the council on X" gives a cited memo in minutes.

Python 3.9+ is the only requirement; the two scripts use the standard library.

## What a round produces
- **A score** (0–100 with a confidence band) against the question your bench asks, with the three findings that moved it.
- **An assessment** in a neutral voice you could forward unedited.
- **A dashboard**: one HTML file with an executive view, a narrative view and an audit view where every ID clicks through to its evidence.
- **What the council needs from you**: numbered, tiered 0–3, the seed of the next round.

`docs/how-a-round-works.md` walks through the ten steps in plain language.

## How deep
"Consult the council" is one verb with three depths. **Quick** (5 to 10 minutes) picks the seats that matter, sits once, and writes a cited memo with no ledger. **Standard** (30 to 60 minutes) runs the full roster through condensed phases and scores. **Deep** (hours, cloud by default) is the full nine phases. The levers behind each profile (seats, phases, retrieval, models, sittings, budget) are explicit in `skills/convening`, and a bench can override them. The chair can add a guest seat for one convening when the question needs an expert the bench lacks.

Every convening passes the **materials gate**: the bench's ladder says what supplied material each depth needs, and the council says cleared, downgraded or blind before it starts. Each bench also has a `context/` folder, read first at every depth, which is how the business or the situation gets trained in.

## Standing research
"Watch Acme for me" turns on a scheduled scan of the bench's sources for the effort's terms, a triage pass against what the council already found, and an action: log it, queue it for the next round, or convene at quick or standard depth. Cadence is nightly, weekly, monthly or quarterly per effort; one scheduled cloud routine serves every watch in the repo. The results arrive as a pull request with a watch brief.

## Dashboards on demand
Every round keeps its own dashboard. From round 2 the dashboard carries a **Changes** toggle: what moved since the prior round (score, drivers, requests answered, gaps closed, headlines demoted), marks on every new or changed row, and a link to the prior version. `dashboards/index.html` lists every round with its score and movement, the consults and the watch briefs. The written assessment's redline is git's.

## Presets
Ready-made benches under `presets/`. Setup copies one and adjusts it; you can also copy by hand.

| Preset | Hat | Assesses | Question |
| --- | --- | --- | --- |
| `board-director` | director, chair, operator | a company | probability of value creation over 3–5 years |
| `board-director-healthcare` | the same, for US healthcare services and benefits | a company | the same, with program-rule and access exposure sharpened |
| `founder-venture` | founder, entrepreneur | an idea or venture | probability it reaches its next milestone |
| `investor-deal` | investor, M&A or deal team | a deal | probability it meets its return target |
| `functional-leader` | head of a function (regulatory, R&D, product, sales, ops) | an initiative | likelihood it delivers its objective by its date |
| `personal-decision` | parent, partner, individual | a decision | likelihood the choice serves the stated goal |
| `research-question` | anyone with an open question | a question | confidence that the evidence supports the answer |

More presets are welcome by pull request. A preset is a `bench.md` and a folder of seat briefs; see `skills/bench-design`.

## Seats and personas
`agents/` is the persona library: generic charters that say how a seat thinks. A **seat** is a persona on a bench with a short **seat brief** giving it the lens for that field. Adding a seat is one file; removing one is deleting it; the same persona can sit twice under different seat IDs. When no charter fits, write a custom one from `agents/_template.md`. Say "add a seat" or "what personas are there" and the session does it. The library today:

- **Analysts** establish facts: `financial`, `market-competitive`, `regulatory-policy`, `operating-model`, `product-positioning`, `valuation-precedent`, `technical-feasibility`, `research-evidence`, `options-tradeoffs`.
- **Stakeholders** react from a seat: `management`, `investor`, `customer-buyer`, `end-user`, `employee`, `channel-partner`, `key-partner`, `supplier`, `regulator`, `policy-voice`, `workforce-representative`, `legal-counsel`, `domain-expert`, `values-ethics`, `counterparty`, `co-decider`, `community-public`.
- **Red team** attacks: `adversary`, `pre-mortem`, `evidence-auditor`.

## Commands
| Command | Does |
| --- | --- |
| `/council-setup` | first run: who you are, your hats, the first bench, cloud or not |
| `/council-bench new \| switch \| list \| edit` | one bench per hat |
| `/council-seat add \| remove \| edit \| list \| library` | one file per seat |
| `/council-consult <question> [quick\|standard\|deep]` | a cited memo in minutes, or a scored round at the deeper settings |
| `/council-run <effort> [standard\|deep]` | round 1 on a new effort |
| `/council-round <effort> [standard\|deep]` | the next round: answers, what changed, what moved |
| `/council-watch on\|off\|edit\|status\|brief <effort>` | standing research between rounds |
| `/council-status` | every bench and effort, open requests first |
| `/council-doctor` | checks the workspace and fixes what it can |

## Local or cloud
Locally, the chair dispatches every seat as a subagent in your session and you wait. In the cloud, a Claude Code routine runs the whole round unattended and opens a pull request with the score, the verdict and the requests list. Cloud is the better home for a council once you have more than one effort going; `docs/cloud-setup.md` takes about ten minutes.

## How it is built
```
council.md                    you and your benches (created by setup)
benches/<bench>/              bench.md, seats/, context/, efforts/<effort>/{brief.md, documents/, ledger.json, rounds/, consults/, watch.md, assessments/, dashboards/}
presets/<preset>/             bench.md + seats/
agents/                       persona charters, _template.md
skills/                       the rules: protocols, evidence ledger, retrieval, conflicts, rebuttal, scoring, outputs, dashboard, intake, bench design, seat authoring, convening (depth), standing watch
commands/                     the slash commands
orchestrator/                 orchestrate.md (a round in the cloud), watch.md (the scheduled watch)
scripts/                      merge_ledger.py (deterministic merge of seat files into the ledger), doctor.py, build_effort_index.py
docs/suite-integration.md     how the council will plug into BDLC and NDLC (planned, not wired)
skills/council-ledger/        build_dashboard.py and the HTML template
```
The engine is deliberately small: two scripts and a template. Everything else is markdown that Claude reads, which is why anyone can change it.

## Confidentiality
Each effort's documents live in its own folder and are read only during that effort's rounds. Keep your copy private if your efforts are. To keep supplied documents out of git entirely, uncomment the last line of `.gitignore`.

## Lineage
Council generalizes a private board-director's council built for US healthcare-services companies in 2026. That council's method (evidence tiers, the headline threshold, the conflict register, the rebuttal round, the evidence auditor, priority tiers on every ask) is kept whole; its field lives on as the `board-director-healthcare` preset.

## The suite
Council is one of three: NDLC builds software, BDLC runs a venture, the council deliberates. `docs/suite-integration.md` is the plan for how they will hand work to each other.

MIT licensed.
