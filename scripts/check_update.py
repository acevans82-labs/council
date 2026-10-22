#!/usr/bin/env python3
"""Check whether a newer council engine release exists, honoring a snooze.

Usage (from a workspace whose engine is the git submodule at engine/, or from the
engine clone itself):
  check_update.py              # print status: current, latest, notes between, snoozed?
  check_update.py --snooze     # write a 3-day snooze for the latest version and exit
  check_update.py --apply      # check out the latest tag in the engine clone (ff only)

Exit codes: 0 up to date or snoozed, 3 update available, 1 error. Prints one JSON
line first (machine-readable), then a human summary. Silent and exit 0 when offline.
Stdlib only.
"""
import argparse
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path

SNOOZE = Path.home() / ".claude" / "council" / "update-snooze"


def sh(args, cwd):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=30)


def vtuple(v):
    return tuple(int(x) for x in re.findall(r"\d+", v)[:3]) or (0,)


def engine_dir():
    here = Path(__file__).resolve().parent.parent
    return here


def current_version(engine):
    try:
        return json.loads((engine / ".claude-plugin" / "plugin.json").read_text())["version"]
    except Exception:
        return None


def latest_tag(engine):
    r = sh(["git", "fetch", "--tags", "--quiet", "origin"], engine)
    if r.returncode != 0:
        return None, "offline"
    r = sh(["git", "tag", "--list", "v*"], engine)
    tags = sorted((t.strip() for t in r.stdout.splitlines() if t.strip()), key=vtuple)
    return (tags[-1] if tags else None), None


def notes_between(engine, cur, new):
    """CHANGELOG sections for versions > cur and <= new, from origin's copy of the latest tag."""
    r = sh(["git", "show", f"{new}:CHANGELOG.md"], engine)
    if r.returncode != 0:
        return ""
    out, keep = [], False
    for line in r.stdout.splitlines():
        m = re.match(r"^## (\d+\.\d+\.\d+)", line)
        if m:
            v = vtuple(m.group(1))
            keep = vtuple(cur) < v <= vtuple(new)
        if keep:
            out.append(line)
    return "\n".join(out).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--snooze", action="store_true")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--days", type=int, default=3)
    args = ap.parse_args()
    engine = engine_dir()
    cur = current_version(engine)
    if not cur:
        print(json.dumps({"status": "error", "reason": "no plugin.json"})); return 1
    latest, err = latest_tag(engine)
    if err == "offline" or not latest:
        print(json.dumps({"status": "offline", "current": cur})); return 0
    new = latest.lstrip("v")
    if vtuple(new) <= vtuple(cur):
        print(json.dumps({"status": "current", "current": cur, "latest": new})); print(f"council engine {cur} is current"); return 0
    if args.snooze:
        SNOOZE.parent.mkdir(parents=True, exist_ok=True)
        until = (dt.date.today() + dt.timedelta(days=args.days)).isoformat()
        SNOOZE.write_text(f"{until} {new}\n")
        print(json.dumps({"status": "snoozed", "until": until, "latest": new})); print(f"snoozed until {until}"); return 0
    if args.apply:
        if sh(["git", "status", "--porcelain"], engine).stdout.strip():
            print(json.dumps({"status": "error", "reason": "engine clone has local changes; not updating over a dirty tree"})); return 1
        r = sh(["git", "checkout", "--quiet", latest], engine)
        if r.returncode != 0:
            print(json.dumps({"status": "error", "reason": r.stderr.strip()})); return 1
        if SNOOZE.exists():
            SNOOZE.unlink()
        print(json.dumps({"status": "updated", "from": cur, "to": new}))
        print(f"council engine updated {cur} -> {new}. If this engine is a submodule, commit the pointer in the workspace: git add engine && git commit -m 'engine {new}'. If it is a plugin cache install, also run: claude plugin update council@council")
        return 0
    if SNOOZE.exists():
        try:
            until, _ = SNOOZE.read_text().split()
            if dt.date.fromisoformat(until) >= dt.date.today():
                print(json.dumps({"status": "snoozed", "current": cur, "latest": new, "until": until})); print(f"council engine {new} available (snoozed until {until})"); return 0
        except Exception:
            pass
    notes = notes_between(engine, cur, new)
    print(json.dumps({"status": "available", "current": cur, "latest": new}))
    print(f"Council engine {new} is available (you have {cur}).")
    if notes:
        print(notes)
    print("Options: update now (python3 engine/scripts/check_update.py --apply), skip, or remind me in 3 days (--snooze).")
    return 3


if __name__ == "__main__":
    sys.exit(main())
