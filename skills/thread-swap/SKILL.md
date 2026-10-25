---
name: thread-swap
description: "Hand the council's home thread to a fresh thread mid-flight, with the full live state, so nothing is lost and the old thread can be archived. Reads how full the thread's context window is at every safe moment and suggests a one-click swap at 60 percent, recommends it at 80 percent, and also watches for other signs of a full thread (compacted, slow, re-reading). Use when the principal says 'swap threads', 'new home thread', 'this thread is too long', 'start fresh on this', 'pass the baton', or when the thread itself notices it is full."
---

# thread-swap

The council's **home thread** is the local conversation where the principal plans runs, answers requests, fires cloud rounds and reads the results. A busy home thread fills up: it gets slow, it gets summarized, it starts re-reading what it already knew. This skill moves the same role to a brand-new thread without advancing the work: same bench, same effort, same round, same pending decisions, one fresh context window. Nothing merges and nothing is fired by the swap itself.

Mirrors NDLC's `ndlc-swap-thread`, cut down to what a council needs.

## When to suggest it
At every seam (below), the home thread reads how full its context window is. In Claude Desktop that is `get_usage` (session `self`): `context.percentUsed`, with `autoCompactsAtPercent` for where the app would start summarizing. Then:

| Context used | What the thread does |
| --- | --- |
| under 60% | nothing (unless a sign below applies) |
| 60% or more | **offers** the swap: one line ("This thread is 62% full; a fresh one would be faster") and two buttons, **Swap now** / **Keep going** |
| 80% or more | **recommends** it: **Swap now (Recommended)** / **Keep going**, and does not start a new round, plan or long answers session in this thread until the principal chooses |

Without a usage tool (another host, or the reading comes back unavailable), fall back to the signs. Either way, it also offers the swap when any of these is true:
- the conversation has already been summarized once to make room;
- it has carried two or more rounds, or one round plus a long planning or answers session;
- replies have become slow, or the thread catches itself re-reading files it read earlier for the same purpose;
- the principal says it feels long or slow.

Offer only at a seam: after a round closes, after a plan is approved and the routine fired, after the principal's answers are written into the brief, after a consult memo is delivered, and at the first turn of a thread that was resumed. Never in the middle of dispatching seats or merging a phase: finish the phase first. Offer at most once per seam. "Keep going" at the 60% offer is respected until the thread crosses 80%; "Keep going" at 80% is respected until the next seam, where it is recommended again.

## 1. Name the role
The successor carries exactly this thread's role, never the next one. Usually: "council home for <workspace>" with the active bench and effort. If the thread did several things, ask which role the successor carries.

## 2. Flush what lives only in this conversation
The successor wakes cold: it has the repository and nothing else. Before starting it, get every chat-only fact somewhere durable:
- Principal answers given in chat but not yet in `brief.md`: write them into the brief's "Round N answers" section now.
- A plan under discussion: write it into the brief as a draft `### Model plan` (no `approved:` line), or, if approved, make sure `approved:` is written.
- Decisions and rulings made in chat (a seat added for one convening, a depth changed, a scope cut): write them in the brief's `## Round parameters`.
- Uncommitted changes: commit and push on the workspace's default branch (data only, never inside `engine/`), or name them in the brief with the branch they sit on.
- Anything the principal asked for that has not been done: it goes in the brief as an open item.

Report what was flushed in one line; "nothing was pending" is a real answer.

## 3. Read the live state fresh
Read, do not remember:
- `council.md`: active bench, the routines and environment under `## Cloud`.
- For the active effort: the newest round ID and phase (`ledger.json` `phases`, `score-history.json`), whether a round branch exists (`git branch -r --list 'origin/claude/round-*'`) and its last commit, and any open PR for it (`gh pr list --search "<effort>"`).
- Open asks: the last round's requests list (Tier 0 first) and any `QUESTION.md` or `BLOCKED.md` waiting on the principal.
- Running cloud work: for each routine in `council.md`, `RemoteTrigger list_runs` (session id, status, last event time) and which round it is on. Name the round branch and the PR when there is one.
- Local subagents still running in this thread: a swap does not carry them. Wait for them to finish (or say which will be lost and re-dispatched) before the swap.
- Spend so far on the current run: `python3 scripts/cost_report.py --brief <brief>` for this thread, headline line only.

## 4. Write the handoff brief
The new thread's prompt is its whole inheritance. Plain sentences, self-contained:
- **Identity:** workspace path, engine version, the role it is taking.
- **Where the work is:** bench, effort, round ID, phase reached, branch, PR link.
- **Live state:** what is running in the cloud (routine id, run session id, started when, last seen when) and what the local thread was waiting for.
- **Open asks and pending decisions:** each with where it is written in the repository (brief section, requests file, QUESTION.md).
- **Decisions made here** that must not be reopened, with where each is recorded.
- **Its first acts, in order:** run `python3 engine/scripts/doctor.py --quick` (path from the workspace root); offer **Archive the old thread** as a button (the old thread is the session that started it; archive only that one, only on the principal's click); then say in three lines where things stand and what the principal's next action is.
- **The standing guard:** take over the role; do not re-fire a routine, re-run a phase or edit the ledger as a side effect of taking over.

## 5. Start the new thread
Use the app's session tool. In Claude Desktop: `start_session` with `context: "fresh"`, the brief as `prompt`, the workspace path, a short `title` naming the role ("Council home · <bench>/<effort>"), and `use_worktree: false` (the home thread works in the workspace checkout). When the principal asked for the swap in words, start it directly; when the thread suggested it, the **Swap now** click is the go. Where the tool is absent (a headless or cloud session), give one paste-ready line: open a new thread in the workspace and say "take over as council home; read the handoff in <path>", after writing the brief to `.council/handoff-<date>.md` in the workspace (gitignored).

## 6. Do not archive this thread
The successor offers the archive after it has taken over, and the principal approves it. This thread never archives itself, so a cancelled or ignored swap leaves it fully in charge with nothing to repair.

## Final message
> Ready to move to a fresh thread. <What was flushed, or "nothing was pending.">
> The new thread will offer to archive this one once it has taken over. Cancel it and nothing breaks; this thread stays in charge.
>
> **Next:** open the new **Council home** thread.

## Rules
- Same role, never the next one. A swap never fires a round, approves a plan, or merges a PR.
- Flush before starting, always.
- No archive without the principal's click.
- Plain English in everything the principal reads.
