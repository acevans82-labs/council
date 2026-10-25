---
description: Check the council workspace and fix what can be fixed. Engine version against the latest release (with update and snooze), engine files, workspace CLAUDE.md and AGENTS.md against the template, council.md, every bench and its seats, every effort's brief, model plan and ledger, and the cloud routines (exists, enabled, Full network, connectors present). Run it when something looks off or after editing files by hand.
argument-hint: [--quick]
---

Run `python3 scripts/doctor.py $ARGUMENTS` and read its report.

1. **Update.** If it prints `update available:`, say so in two lines (the versions and the release-note headings it printed) and offer three buttons: **Update now** (`python3 scripts/check_update.py --apply`, then in a workspace `git add engine && git commit -m "engine <version>"` and push, then re-run the doctor), **Skip**, **Remind me in 3 days** (`python3 scripts/check_update.py --snooze`). A snoozed update is a status line, never a prompt.
2. **Templates.** If it reports the workspace `CLAUDE.md` or `AGENTS.md` differs from `templates/workspace/`, show the difference in one line and offer to copy the template over (a local edit the principal wants to keep is their call).
3. **Mechanical fixes.** For each problem that is mechanical and safe (a missing roster row, a weight table that does not sum to 100 where the intent is obvious, a seat whose persona is misspelled, a seat brief missing its frontmatter field, a missing `index.md`), fix it, say what you changed, and re-run the doctor. For anything that needs the principal's judgment (a bench with no analysts, a custom seat with no charter, an effort with no brief), ask in one message.
4. **Cloud (full run only, not `--quick`).** If `council.md` records routines, run the live checks in `skills/cloud-routines` section 6 with `RemoteTrigger`: each routine exists and is enabled, its environment matches the recorded one and has Full network, and its connectors cover the ones this session has. Report gaps in plain words and offer the fix as a button (it changes the account). No `RemoteTrigger` tool: say the cloud checks need a session that has it.

Never touch a ledger's records; the doctor reports ledger problems and the fix is a new round, not an edit. Close with one line per area: engine, workspace, benches, efforts, cloud, each "ok" or what is open.
