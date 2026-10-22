#!/usr/bin/env python3
"""Build the council ledger dashboard from ledger.json.

Usage: build_dashboard.py <ledger.json> <output.html> [--prior <prior-ledger.json>]

Reads the ledger, validates the fields the dashboard depends on, injects the JSON
into the template at the /*__LEDGER__*/ marker, and writes a standalone HTML file.
With --prior, also computes what changed since the prior round (score and driver
deltas, requests answered, gaps closed, conflicts resolved, carried records that
changed, and what is new) and injects it as CHANGES so the dashboard can show,
hide and link the differences.
"""
import argparse
import json
import sys
from pathlib import Path

VOLATILE = {"carried_from", "reverified", "id"}
ARRAYS = ["evidence", "findings", "conflicts", "rulings", "judgment_calls", "handoffs", "gaps", "open_questions"]


def strip_p(rid: str) -> str:
    return rid[2:] if isinstance(rid, str) and rid.startswith("P/") else rid


def changes(cur: dict, prior: dict) -> dict:
    pr_index = {}
    for key in ARRAYS:
        for rec in prior.get(key, []):
            pr_index[strip_p(str(rec.get("id", "")))] = (key, rec)
    records, counts = {}, {"new": 0, "changed": 0, "carried": 0}
    answered, closed_gaps, resolved_conflicts, demoted = [], [], [], []
    for key in ARRAYS:
        for rec in cur.get(key, []):
            rid = str(rec.get("id", ""))
            base = strip_p(rid)
            if rid.startswith("P/") and base in pr_index:
                old = pr_index[base][1]
                a = {k: v for k, v in rec.items() if k not in VOLATILE}
                o = {k: v for k, v in old.items() if k not in VOLATILE}
                if a != o:
                    diff = sorted(k for k in set(a) | set(o) if a.get(k) != o.get(k))
                    records[rid] = {"kind": "changed", "fields": diff}
                    counts["changed"] += 1
                    if key == "judgment_calls" and rec.get("answer") and not old.get("answer"):
                        answered.append(rid)
                    if key == "gaps" and old.get("status") == "not_found" and rec.get("status") != "not_found":
                        closed_gaps.append(rid)
                    if key == "conflicts" and (not old.get("resolved_by") or old.get("resolved_by") == "unresolved") \
                            and rec.get("resolved_by") not in (None, "", "unresolved"):
                        resolved_conflicts.append(rid)
                    if key == "findings" and old.get("status") == "headline" and rec.get("status") != "headline":
                        demoted.append(rid)
                else:
                    records[rid] = {"kind": "carried"}
                    counts["carried"] += 1
            else:
                records[rid] = {"kind": "new"}
                counts["new"] += 1
    pa, ca = prior.get("assessment", {}), cur.get("assessment", {})
    pd = {d.get("key"): d for d in pa.get("drivers", [])}
    drivers = []
    for d in ca.get("drivers", []):
        o = pd.get(d.get("key"), {})
        if o.get("score") != d.get("score"):
            drivers.append({"key": d.get("key"), "name": d.get("name"), "from": o.get("score"), "to": d.get("score")})
    pe, ce = prior.get("effort", {}), cur.get("effort", {})
    return {
        "prior_round_id": pe.get("round_id"), "round_id": ce.get("round_id"),
        "prior_dashboard": f"{pe.get('round_id')}-council-ledger.html" if pe.get("round_id") else None,
        "score": {"from": pa.get("score"), "to": ca.get("score"), "band_from": pa.get("band"), "band_to": ca.get("band")},
        "drivers": drivers, "records": records, "counts": counts,
        "answered": answered, "closed_gaps": closed_gaps, "resolved_conflicts": resolved_conflicts, "demoted": demoted,
        "new_headlines": [f.get("id") for f in cur.get("findings", []) if f.get("status") == "headline"],
        "prior_headline_count": sum(1 for f in prior.get("findings", []) if f.get("status") == "headline"),
    }

TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "dashboard-template.html"

REQUIRED_TOP = ["effort", "roster", "phases", "evidence", "findings", "conflicts",
                "rulings", "judgment_calls", "handoffs", "gaps", "open_questions",
                "assessment", "score_history"]


def warn(msg: str) -> None:
    print(f"warning: {msg}", file=sys.stderr)


def validate(ledger: dict) -> None:
    for key in REQUIRED_TOP:
        if key not in ledger:
            warn(f"ledger missing top-level '{key}'; dashboard will show it as empty")
            ledger[key] = {} if key in ("effort", "assessment") else []
    for r in ledger.get("phases", []):
        if not r.get("summary"):
            warn(f"phase {r.get('n')} has no summary; narrative view will be thin")
    for r in ledger.get("rulings", []):
        if not r.get("rationale"):
            warn(f"ruling {r.get('id')} has no rationale")
    for j in ledger.get("judgment_calls", []):
        if not j.get("why_principal"):
            warn(f"judgment call {j.get('id')} has no why_principal")
        if j.get("tier") not in (0, 1, 2, 3):
            warn(f"judgment call {j.get('id')} has no priority tier; it will show no badge and sort last")
    for g in ledger.get("gaps", []):
        if g.get("raised_to_principal") and g.get("tier") not in (0, 1, 2, 3):
            warn(f"gap {g.get('id')} is raised to the principal but has no priority tier")
    for c in ledger.get("conflicts", []):
        unresolved = not c.get("resolved_by") or c.get("resolved_by") == "unresolved"
        if unresolved and c.get("tier") not in (0, 1, 2, 3):
            warn(f"conflict {c.get('id')} is unresolved but has no priority tier")
    a = ledger.get("assessment", {})
    if a.get("score") is None:
        warn("assessment has no score; dashboard lead will be empty")
    if not a.get("label"):
        warn("assessment has no label (the bench's score label, e.g. 'Probability of value creation over 3–5 years'); the dashboard will say 'Score'")
    xs = ledger.get("exec_summary")
    if not xs:
        warn("ledger has no exec_summary; the Executive summary view will be hidden — "
             "every round must carry one (see skills/assessment-output)")
    else:
        for key in ("verdict", "answers", "urgent", "decisions", "documents", "conflicts", "risks"):
            if not xs.get(key):
                warn(f"exec_summary missing '{key}'; that block will not render")
        for key in ("decisions", "documents", "conflicts"):
            for entry in xs.get(key, []):
                if not isinstance(entry, dict) or "id" not in entry:
                    warn(f"exec_summary.{key} has a plain-string entry; give it {{'id': ..., 'text': ...}} "
                         f"so the dashboard can show its priority tier")
    heads = [f for f in ledger.get("findings", []) if f.get("status") == "headline"]
    for f in heads:
        if not f.get("so_what"):
            warn(f"headline {f.get('id')} has no so_what")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ledger")
    ap.add_argument("output")
    ap.add_argument("--prior", help="the prior round's ledger.json, to compute what changed")
    args = ap.parse_args()
    src, out = Path(args.ledger), Path(args.output)
    ledger = json.loads(src.read_text())
    validate(ledger)
    template = TEMPLATE.read_text()
    if "/*__LEDGER__*/" not in template:
        print("error: template missing /*__LEDGER__*/ marker", file=sys.stderr)
        return 1
    chg = None
    if args.prior:
        prior = json.loads(Path(args.prior).read_text())
        chg = changes(ledger, prior)
        c = chg["counts"]
        print(f"changes vs {chg['prior_round_id']}: {c['new']} new, {c['changed']} changed, {c['carried']} carried unchanged; "
              f"{len(chg['answered'])} requests answered, {len(chg['closed_gaps'])} gaps closed, {len(chg['resolved_conflicts'])} conflicts resolved")
    elif ledger.get("effort", {}).get("prior_round", {}).get("round_id"):
        warn("ledger names a prior round but --prior was not given; the dashboard will not show what changed")
    payload = json.dumps(ledger, ensure_ascii=False).replace("</", "<\\/")
    cpayload = json.dumps(chg, ensure_ascii=False).replace("</", "<\\/") if chg else "null"
    html = template.replace("/*__LEDGER__*/", f"const LEDGER = {payload};\nconst CHANGES = {cpayload};")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    print(f"wrote {out} ({len(html)//1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
