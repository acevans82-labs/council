#!/usr/bin/env python3
"""Build dashboards/index.html for one effort: every round with its score, band and
movement, links to each round's dashboard, assessment and principal-requests file,
plus the consults and watch briefs on record.

Usage: build_effort_index.py <effort_dir>
"""
import html
import json
import sys
from pathlib import Path

STYLE = """body{margin:0;background:#EDEFF1;color:#182029;font-family:"Source Serif 4",Georgia,serif;font-size:17px;line-height:1.5}
main{max-width:980px;margin:0 auto;padding:40px 24px}h1{font-size:30px;margin:0 0 4px}.meta{color:#5B6570;font-family:system-ui,sans-serif;font-size:14px;margin-bottom:28px}
table{width:100%;border-collapse:collapse;background:#F7F8F9;font-family:system-ui,sans-serif;font-size:14px;margin:12px 0 32px}th,td{text-align:left;padding:8px 10px;border-bottom:1px solid #C9CED4;vertical-align:top}th{color:#5B6570;font-weight:600}
.up{color:#3E6B4A}.down{color:#8A2D2D}a{color:#2B4C7E}h2{font-size:20px;margin:28px 0 6px}.muted{color:#5B6570}"""


def e(x):
    return html.escape(str(x if x is not None else ""))


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    ed = Path(sys.argv[1])
    hist = json.loads((ed / "score-history.json").read_text()) if (ed / "score-history.json").exists() else []
    ledger = json.loads((ed / "ledger.json").read_text()) if (ed / "ledger.json").exists() else {}
    eff = ledger.get("effort", {})
    name = eff.get("name") or ed.name
    rows, prev = [], None
    for h in hist:
        rid = h.get("round_id", "")
        dash = ed / "dashboards" / f"{rid}-council-ledger.html"
        asm = ed / "assessments" / f"{rid}-assessment.md"
        req = ed / "assessments" / f"{rid}-principal-requests.md"
        mv = ""
        if prev is not None and h.get("score") is not None and prev.get("score") is not None:
            d = h["score"] - prev["score"]
            mv = f'<span class="up">&#9650; {d}</span>' if d > 0 else f'<span class="down">&#9660; {-d}</span>' if d < 0 else '<span class="muted">0</span>'
        links = []
        if dash.exists():
            links.append(f'<a href="{e(dash.name)}">dashboard</a>')
        if asm.exists():
            links.append(f'<a href="../assessments/{e(asm.name)}">assessment</a>')
        if req.exists():
            links.append(f'<a href="../assessments/{e(req.name)}">requests</a>')
        rows.append(f"<tr><td>{e(rid)}</td><td>{e(h.get('date'))}</td><td><b>{e(h.get('score'))}</b> ±{e(h.get('band'))}</td><td>{mv}</td><td>{e(h.get('note'))}</td><td>{' · '.join(links) or '<span class=muted>files not found</span>'}</td></tr>")
        prev = h
    consults = (ed / "consults" / "index.md").read_text() if (ed / "consults" / "index.md").exists() else ""
    briefs = sorted((ed / "watch").glob("*-brief.md")) if (ed / "watch").exists() else []
    out = [f"<!doctype html><html lang=en><head><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'><title>{e(name)} — rounds</title><style>{STYLE}</style></head><body><main>",
           f"<h1>{e(name)} — every round</h1><div class=meta>{e(eff.get('bench_name') or '')}{' · ' if eff.get('bench_name') else ''}{e(eff.get('description') or '')}{' · ' if ledger.get('assessment', {}).get('label') else ''}{e(ledger.get('assessment', {}).get('label') or '')}</div>",
           "<table><thead><tr><th>Round</th><th>Date</th><th>Score</th><th>Moved</th><th>Trigger</th><th>Open</th></tr></thead><tbody>",
           "".join(rows) or "<tr><td colspan=6 class=muted>No rounds yet.</td></tr>", "</tbody></table>",
           "<p class=muted>Each dashboard carries a Changes toggle that marks what moved since the round before it. The assessment's redline is <code>git log -p</code> on the assessments folder.</p>"]
    if consults.strip():
        out.append("<h2>Consults</h2><pre style='white-space:pre-wrap;font-family:system-ui,sans-serif;font-size:14px'>" + e(consults) + "</pre>")
    if briefs:
        out.append("<h2>Watch briefs</h2><ul>" + "".join(f"<li><a href='../watch/{e(b.name)}'>{e(b.name)}</a></li>" for b in briefs) + "</ul>")
    out.append("</main></body></html>")
    dest = ed / "dashboards" / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text("\n".join(out))
    print(f"wrote {dest} ({len(rows)} rounds)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
