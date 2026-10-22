# My council

A council workspace. The data (`council.md`, `benches/`) is mine; the engine that runs it is the public council engine mounted at `engine/`, pinned to a release.

## First time on a machine
```bash
git clone <this repo> && cd <this repo>
git submodule update --init
```
Open the folder in Claude Code and say **"set up my council"**. Python 3.9+ is the only requirement. Slash commands are optional: `claude plugin marketplace add acevans82-labs/council` then `claude plugin install council@council`.

## Every day
- "consult the council on …" for a quick cited memo; "run the council on …" for a full round; "next round on …" to continue.
- "watch … for me" for standing research; "status" for every bench and effort.
- Cloud rounds: `engine/docs/cloud-setup.md`.

## Updating the engine
Threads offer updates when a new engine release exists. By hand: `python3 engine/scripts/check_update.py --apply`, then commit the `engine` pointer.

## Privacy
Effort documents live under `benches/<bench>/efforts/<effort>/documents/`. Keep this repository private if your efforts are. To keep documents out of git entirely, uncomment the last line of `.gitignore`.
