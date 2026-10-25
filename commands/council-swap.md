---
description: Hand the council's home thread to a fresh thread with the full live state (active effort, round, phase, open asks, pending decisions, running cloud sessions), so nothing is lost and the old thread can be archived. Use when the thread is long, slow, or its context is filling.
argument-hint: [nothing]
---

Swap the council's home thread to a fresh one. Follow `skills/thread-swap` exactly: name the role, flush everything that lives only in this conversation into the repository, read the live state fresh (including running cloud rounds and their session ids), write the handoff brief, start the new thread with it, and never archive this thread yourself; the new thread offers that.
