---
name: round-close
description: "How every round, and every consult that writes ledger records, closes: build the dashboard and the effort index, write the cost receipt (estimate against measured, by phase, with the reason for any overrun), check for a spend-limit or network stall and say so in plain words, deliver the dashboard (as a file and as a published claude.ai Artifact) and the ledger to the principal, and link them in the pull request. Read by the chair at phase 9 and by the cloud orchestrator at its close."
---

# round-close

A round is not finished until the principal has the dashboard and the ledger in hand and knows what the run cost. This skill is the last thing the chair does, locally or in the cloud. A quick consult writes no ledger, so it delivers its memo only (and its receipt when a plan was made).

## 1. Build
After synthesis (`agents/chair.md` phase 9, `skills/assessment-output`):
```bash
python3 skills/council-ledger/scripts/build_dashboard.py benches/<bench>/efforts/<effort>/ledger.json \
    benches/<bench>/efforts/<effort>/dashboards/<round_id>-council-ledger.html [--prior benches/<bench>/efforts/<effort>/rounds/<prior_round_id>/ledger.json] \
    --artifact benches/<bench>/efforts/<effort>/dashboards/<round_id>-artifact.html
python3 scripts/build_effort_index.py benches/<bench>/efforts/<effort>
```
`--artifact` writes the page variant for publishing (no document wrapper, titled "<Effort> Round <N> Ledger", phone-width layout) and scans it for personal contact details. If it lists any (exit 2), check each: business contacts (a company switchboard, a sales address) are fine; anything personal (a private mobile, a personal email) means rerun with `--redact`. Never publish a variant with a personal detail left in.

Copy the round's final ledger to `rounds/<round_id>/ledger.json` as well, so the delivered file is the round's own and does not change when the next round opens.

## 2. Cost receipt
```bash
python3 scripts/cost_report.py --brief benches/<bench>/efforts/<effort>/brief.md \
    --label "<bench>/<effort> <round_id>" \
    --out benches/<bench>/efforts/<effort>/assessments/<round_id>-cost.md \
    --json benches/<bench>/efforts/<effort>/rounds/<round_id>/cost.json
```
It reads this session's transcripts (in the cloud, the routine's session; locally, the thread, counted from the plan's `approved:` time) and prices every message per model. Then the chair fills the one placeholder per overrun: **"Reason:"**, one sentence on why that phase cost more than planned (a seat went deep on a rule change, a phase was re-run after a stall, the answer pass touched more analysts than planned). A phase over by more than 25 percent and $2 is an overrun; say so even when the total is within the ceiling.

A resumed round sums every session it ran in: pass each with `--session`. If no transcript is reachable (some cloud setups), write the receipt with the estimate only and say "measured cost not available in this environment".

Put the receipt's headline line (estimate, measured, over or under) in the PR body and in the local close.

## 3. Stalls, in plain words
`cost_report.py` exits 2 when it finds a stall in the transcripts. Report each in one plain sentence, never as an error code:
- **Spend limit:** "The run stopped at 21:26 UTC because the account reached its monthly spend limit. Raise the limit or wait for it to reset, then say 'resume the round'."
- **Out of credits / plan limit:** the same shape, with the reset time when the message gave one.
- **Network:** "Web pages could not be opened from the cloud environment. It needs Full network access."

A run that stalls usually cannot write its own close, because the stall stops the model. So the **local thread** checks: when a fired routine has gone quiet (no new commits on the round branch for 30 minutes and no PR), read the run with `RemoteTrigger list_runs` and `get_run_log`, look for the limit or network messages, and tell the principal in plain words what stopped it and what one action restarts it. Do not report a quiet run as a failure until the log says so: a routine's status reads "succeeded" when its first turn ends, while the session keeps working on later turns.

## 4. Deliver
Every time, both forms of the dashboard:
- **Published page.** Publish `dashboards/<round_id>-artifact.html` with the `Artifact` tool: icon `chart`, a one-sentence description ("Council ledger for <effort>, round <N>: score <score>, <one-clause verdict>"). The first publish for an effort creates the page; later rounds of the same effort publish to a new page (each round keeps its own link). Put the link in the close message and in the PR body (edit the PR body if the PR is already open: `gh pr edit <n> --body-file`). Record the link in `dashboards/index.md` beside the round.
- **File.** The dashboard HTML as an attachment (below).

Then send the principal, in this order, in one message:
1. The dashboard (`dashboards/<round_id>-council-ledger.html`), with the published link beside it.
2. The ledger (`rounds/<round_id>/ledger.json`).
3. The assessment (`assessments/<round_id>-assessment.md`) and the requests list (`assessments/<round_id>-principal-requests.md`).
4. The cost receipt.

Locally, use `SendUserFile` when the session has it (status `normal` when the principal is in the conversation, `proactive` when the round finished while they were away; `display: attach` for the dashboard and the ledger, since the published page is the one to view). Without it, give the paths as clickable links. In the cloud, the PR carries them: the body links each file on the round branch (`https://github.com/<owner>/<repo>/blob/<branch>/<path>`), and the dashboard link also gives the raw-HTML preview route when the repository is public (`https://htmlpreview.github.io/?<raw url>`). The cloud usually has no `Artifact` tool: then the PR body says "the published dashboard follows from the local thread", and when the local home thread sees the round's PR land, it fetches the branch, publishes `dashboards/<round_id>-artifact.html` (scan and redact as above), adds the link to the PR body and `dashboards/index.md`, and sends the dashboard file and the ledger with `SendUserFile`, so they reach the principal's phone.

## 5. The close message
Plain English, short, no ledger jargon in the first screen:
- the score label, score and one-paragraph verdict;
- what moved since the last round (round 2+);
- the published dashboard link and the four delivered files;
- the cost line ("$203 against an estimate of $185 and a ceiling of $250; phase 2 ran over because ...");
- any stall, in one sentence;
- the numbered "What the council needs from the principal" list, Tier 0 first;
- one line: how to answer ("answer any of these with /council-round <slug>").
