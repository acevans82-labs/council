# Roadmap

What comes next for the council, in order. Each item says why it matters, what done looks like, and what is still an open question. Items move to `CHANGELOG.md` when they ship. Smaller things live in GitHub issues.

Current release: 1.1 (depth profiles, materials gate, context folder, dashboard history, standing watch). Nothing below is started.

## 0. Shake-out (before anything else)
The 1.1 prompts have never run live. One quick consult, one standard round, one round 2 with answers, and one watch brief, each on a real effort, with every ambiguity fixed in the skills as it appears.
**Done:** a `SHAKEOUT.md` listing what broke and what changed, and a tagged 1.1.x.

## 1. Sources of truth: evidence connections and the doctor
The council is only as good as what it can read. Most of a principal's evidence does not live in a repo: OneDrive and SharePoint, Google Drive, Microsoft 365 and Gmail, calendars, contacts, messages, the CRM, the books. Today the council reads what is dropped into `documents/` and `context/`; everything else it must be told.
**Build:**
- **Connections in `council.md`.** A `## Connections` section listing the connectors the principal has authorized (Microsoft 365, Google Workspace, email, calendar, contacts, messages, CRM, accounting, Notion, Dropbox), what each is allowed to serve, and which benches may read it. A personal bench never reads a company connector and vice versa unless the principal says so.
- **The doctor probes them.** Setup and `/council-doctor` discover the MCP connectors present in the session (one live call each, the way ndlc-setup does), ask for the ones that are missing and would matter for this bench's ladder, and drive the browser to the connector page so the principal only presses the consent button.
- **Retrieval reads them.** `skills/exhaustive-retrieval` step 1 (T1) searches the authorized connectors before the web. Evidence records cite connector locators (file path and page, message ID and date, event ID). Nothing is copied into the repo unless the principal says to register it as a document.
- **The ladder can name a connector.** A materials ladder line may say "the board pack folder on SharePoint" and the gate clears when the connector reaches it.
- **Watch scans connectors too.** A standing watch may include an inbox, a shared folder or a calendar as a source.
**Done:** a bench whose ladder points at a SharePoint folder clears the gate without anyone uploading a file, and a round's evidence cites that folder by locator.
**Open:** which connectors are reachable from a cloud routine versus only in an interactive session (cloud rounds may need the material registered first); how to log what a round read for audit.

## 2. Keeping every copy current (auto-update) — shipped in 1.2.0, see CHANGELOG
Kept here for the reasoning. Remaining: a marketplace plugin install alongside the submodule (slash commands) should be chased by `claude plugin update council@council` after a pointer move; the doctor should notice when the two disagree.
When this public repo improves, every tester's copy should offer the update the next time they open a thread, with the release notes, and let them pull, skip or snooze. Copy NDLC's mechanism exactly (`ndlc-v2/RELEASING.md`, "How updates propagate", and the CLAUDE block's "Keeping NDLC current"): fetch in the plugin clone, compare `plugin.json` versions, show the CHANGELOG entries between them, offer "pull now" or "remind me in 3 days", snooze file at `~/.claude/council/update-snooze`, never prompt offline, never break a snooze for a newer release.
**Prerequisite: the engine/data split.** NDLC's model works because the plugin is a git clone that only Anthropic-side code lives in, and the project is a separate repo. The council today is one template that bundles engine (agents, skills, commands, scripts, orchestrator, presets) with data (council.md, benches). A template copy cannot `git pull` upstream without merging the owner's data. So:
- The engine becomes the plugin install (a clone of this repo in a visible home folder, registered as a marketplace, exactly as NDLC does), and a principal's council repo holds only `council.md`, `benches/`, `CLAUDE.md` and the cloud files.
- Cloud routines need the engine too: setup commits a pinned copy of the orchestrator and scripts into the council repo, and the doctor diffs that copy against the installed version and offers a sync PR, the way ndlc-doctor checks the committed skills.
- Interim for copies made from the template before the split: the doctor adds an `upstream` remote and offers a PR that updates only the engine paths.
**Done:** a tester on 1.1 opens a thread after 1.2 ships, sees "Council 1.2 is available" with the notes, pulls, and their benches are untouched.

## 3. Several people on one bench
One request is certain: a bench shared by a team, several people working the same effort. The access unit is the repository, so the answer is a **bench repo**: a repository whose root is one bench (`bench.md`, `seats/`, `context/`, `efforts/`), with the engine coming from the plugin (item 2). GitHub collaborators control who can read and convene. A personal council keeps personal benches in the personal repo and mounts shared bench repos beside it (`council.md` lists them with their paths; a submodule where people want one checkout).
**Build:**
- `council.md` lists people per bench: principals (convene at any depth, answer requests, change seats) and contributors (add material, run quick consults, read everything).
- Rounds already run on their own branch and land as a PR, so two people convening on different efforts never collide; two rounds on the same effort serialize on merge order, and the chair refuses to start a round while another round's PR on that effort is open.
- Requests to the principal name which principal when a bench has several; answers record who answered.
- A bench export ("share this bench without its efforts") produces a preset-shaped folder from a live bench.
**Done:** two GitHub accounts convene on the same effort in a shared bench repo, each from their own machine, and the second round carries the first person's answers.
**Open:** whether a cloud routine for a shared bench runs on one person's account or the organization's.

## 4. The suite talking to itself (BDLC and NDLC)
`docs/suite-integration.md` is the contract. Wire it: "convene the council on A-07" from a BDLC session writes the brief, runs or fires the convening at a chosen depth, and copies the assessment's findings back into the assumptions register as evidence, never as a verdict. Align BDLC's six Board seats with the council's charters by the mapping table so improvements flow both ways on purpose. NDLC gets a documented hand-carry only. Total Recall later: the context folder read from it, assessments written back to it as memories.
**Done:** a BDLC escalation resolved by a council round with the register row citing council IDs.

## 5. Extensible everywhere (adapters)
The council assumes GitHub for the repo and PRs, files for the dashboard, and nothing for tracking. Others will have Azure DevOps or GitLab, Linear or ADO boards or Jira, and want a Notion front end. Componentize behind four adapter seams, each with a file-based default so nothing is required:
- **source of record** (where benches live and rounds land): GitHub today; GitLab, ADO repos next.
- **tracker** (where open requests and watch briefs surface for humans): none today; Linear, ADO boards, Jira.
- **front end** (where people read): the HTML dashboards today; a Notion mirror of efforts, scores and open requests.
- **evidence connectors** (item 1).
`council.md` names the adapter per seam; the doctor verifies each is reachable and configured, and setup walks through the missing ones with the same tool ladder as ndlc-setup (MCP call, CLI, API, browser with the human on the consent button only).
**Done:** a tester on ADO with Jira runs a round and sees the requests list in Jira without editing a skill.

## Smaller items, any time
- Ledger compaction for efforts past ten rounds (archive stale carried evidence; keep IDs stable).
- A scheduled refresh round (cadence in `watch.md`, `on_schedule: standard`), distinct from the watch.
- A `calc` renderer in the dashboard drawer.
- Per-layer model names in a depth profile, honored by the chair's dispatch.
- Preset contributions: a template PR checklist and a doctor pass for presets.
