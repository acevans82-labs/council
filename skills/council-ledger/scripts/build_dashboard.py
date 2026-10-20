#!/usr/bin/env python3
"""Build the council ledger dashboard from ledger.json.

Usage: build_dashboard.py <ledger.json> <output.html>

Reads the ledger, validates the fields the dashboard depends on, injects the JSON
into the template at the /*__LEDGER__*/ marker, and writes a standalone HTML file.
"""
import json
import sys
from pathlib import Path

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
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    ledger = json.loads(src.read_text())
    validate(ledger)
    template = TEMPLATE.read_text()
    if "/*__LEDGER__*/" not in template:
        print("error: template missing /*__LEDGER__*/ marker", file=sys.stderr)
        return 1
    payload = json.dumps(ledger, ensure_ascii=False).replace("</", "<\\/")
    html = template.replace("/*__LEDGER__*/", f"const LEDGER = {payload};")
    out.write_text(html)
    print(f"wrote {out} ({len(html)//1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
