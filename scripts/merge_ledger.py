#!/usr/bin/env python3
"""Deterministic merge of persona phase files into an effort's ledger.

Usage:
  merge_ledger.py <ledger.json> <round_dir> --phase N --purpose "..." \
      --personas id1 id2 ... [--files f1.json f2.json ...]

Implements skills/evidence-ledger "Writing to the file": each persona writes
records with temp IDs prefixed by its persona id (financial-E-1, or
rebuttal-financial-E-1 in the rebuttal phase). This script merges them into
ledger.json in persona order, renumbers IDs sequentially per record type, and
rewrites every cross-reference to a temp ID anywhere in the merged records.

- Append-only: existing ledger records are never modified, except that a
  persona's `contest` entries append to an existing finding's contested_by,
  a persona's `handoff_answers` set an existing H- record's status, and a
  stakeholder's view/view_revised and competence update its roster entry.
- Idempotent: merged files are recorded in <round_dir>/merge-log.json and
  skipped on re-run.
- A phases entry is appended with summary "PENDING" for the chair to fill.
"""
import argparse
import json
import re
import sys
from pathlib import Path

TYPE_KEYS = {  # record-type prefix -> ledger array
    "E": "evidence", "F": "findings", "C": "conflicts", "G": "gaps",
    "H": "handoffs", "Q": "open_questions",
}
ARRAYS = ["evidence", "findings", "conflicts", "rulings", "judgment_calls",
          "handoffs", "gaps", "open_questions"]
TEMP_ID = re.compile(r"\b((?:rebuttal-)?[a-z][a-z0-9-]*?)-([EFCGHQ])-(\d+)\b")


def load(path, default):
    p = Path(path)
    if p.exists():
        return json.loads(p.read_text())
    return default


def next_num(ledger, prefix):
    key = TYPE_KEYS[prefix]
    mx = 0
    for rec in ledger.get(key, []):
        m = re.match(rf"^(?:P/)?{prefix}-(\d+)$", str(rec.get("id", "")))
        if m:
            mx = max(mx, int(m.group(1)))
    return mx + 1


def rewrite(obj, idmap):
    """Recursively replace temp IDs in every string field."""
    if isinstance(obj, str):
        return TEMP_ID.sub(lambda m: idmap.get(m.group(0), m.group(0)), obj)
    if isinstance(obj, list):
        return [rewrite(x, idmap) for x in obj]
    if isinstance(obj, dict):
        return {k: rewrite(v, idmap) for k, v in obj.items()}
    return obj


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ledger")
    ap.add_argument("round_dir")
    ap.add_argument("--phase", type=int, required=True)
    ap.add_argument("--purpose", required=True)
    ap.add_argument("--personas", nargs="+", required=True,
                    help="persona ids in dispatch order")
    ap.add_argument("--files", nargs="*", default=None,
                    help="explicit files; default <persona>.json (or "
                         "rebuttal-<persona>.json when they exist and "
                         "<persona>.json was already merged)")
    args = ap.parse_args()

    ledger_path = Path(args.ledger)
    round_dir = Path(args.round_dir)
    ledger = load(ledger_path, None)
    if ledger is None:
        print(f"error: {ledger_path} does not exist", file=sys.stderr)
        return 2
    for key in ARRAYS:
        ledger.setdefault(key, [])
    ledger.setdefault("roster", [])
    ledger.setdefault("phases", [])

    log_path = round_dir / "merge-log.json"
    mlog = load(log_path, {"merged_files": []})

    # Resolve the file list.
    files = []
    if args.files:
        files = [round_dir / f for f in args.files]
    else:
        for pid in args.personas:
            reb = round_dir / f"rebuttal-{pid}.json"
            plain = round_dir / f"{pid}.json"
            if reb.exists() and reb.name not in mlog["merged_files"]:
                files.append(reb)
            elif plain.exists() and plain.name not in mlog["merged_files"]:
                files.append(plain)
            else:
                print(f"note: no unmerged file for persona '{pid}' "
                      f"(abstention or already merged)")

    counters = {p: next_num(ledger, p) for p in TYPE_KEYS}
    idmap = {}
    staged = []          # (array_key, record) in persona order
    roster_updates = []  # (persona_id, fields)
    contests = []        # (target_finding_id, {persona, note})
    handoff_answers = [] # (target_handoff_id, status)
    abstained = []
    merged_now = []

    for f in files:
        if not f.exists():
            abstained.append(f.stem)
            continue
        try:
            data = json.loads(f.read_text())
        except json.JSONDecodeError as e:
            print(f"error: {f.name} is not valid JSON ({e}); treating as "
                  f"abstention", file=sys.stderr)
            abstained.append(f.stem)
            continue
        pid = data.get("persona_id") or f.stem.removeprefix("rebuttal-")

        # First pass: assign final IDs for this persona's new records.
        for key_prefix, array in TYPE_KEYS.items():
            for rec in data.get(array, []):
                tmp = str(rec.get("id", ""))
                final = f"{key_prefix}-{counters[key_prefix]:03d}"
                counters[key_prefix] += 1
                if tmp:
                    idmap[tmp] = final
                rec["id"] = final
                rec.setdefault("recorded_by" if array == "evidence"
                               else "persona", pid)
                staged.append((array, rec))

        rf = {"competence": data.get("competence"),
              "view": data.get("view_revised") or data.get("view")}
        rf = {k: v for k, v in rf.items() if v}
        if rf:
            roster_updates.append((pid, rf))
        for c in data.get("contests", []):
            contests.append((c.get("finding_id"),
                             {"persona": pid, "note": c.get("note", "")}))
        for h in data.get("handoff_answers", []):
            handoff_answers.append((h.get("handoff_id"),
                                    h.get("status", "answered")))
        merged_now.append(f.name)

    # Second pass: rewrite temp-ID references everywhere in staged records.
    for array, rec in staged:
        ledger[array].append(rewrite(rec, idmap))

    for pid, fields in roster_updates:
        for entry in ledger["roster"]:
            if entry.get("persona_id") == pid:
                entry.update(fields)
                break
    for fid, note in contests:
        fid = idmap.get(fid, fid)
        for fnd in ledger["findings"]:
            if fnd.get("id") == fid:
                fnd.setdefault("contested_by", []).append(note)
                break
        else:
            print(f"warning: contest targets unknown finding {fid}",
                  file=sys.stderr)
    for hid, status in handoff_answers:
        hid = idmap.get(hid, hid)
        for h in ledger["handoffs"]:
            if h.get("id") == hid:
                h["status"] = status
                break

    ledger["phases"].append({
        "n": args.phase, "purpose": args.purpose,
        "personas": args.personas, "abstained": abstained,
        "summary": "PENDING — chair fills this so it reads like minutes",
        "notable": [],
    })

    ledger_path.write_text(json.dumps(ledger, indent=2) + "\n")
    mlog["merged_files"].extend(merged_now)
    log_path.write_text(json.dumps(mlog, indent=2) + "\n")
    n_new = len(staged)
    print(f"merged {len(merged_now)} file(s), {n_new} record(s); "
          f"abstained: {abstained or 'none'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
