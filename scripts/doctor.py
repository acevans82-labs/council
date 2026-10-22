#!/usr/bin/env python3
"""Council workspace doctor.

Usage: doctor.py [--quick] [--root DIR]

Checks the engine files, council.md, every bench (bench.md, seats/, roster table,
driver weights) and every effort (brief, ledger, score history). Prints one line
per problem and exits 1 if any ERROR was found, 0 otherwise. --quick checks only
the engine and council.md. Stdlib only.
"""
import argparse
import json
import re
import sys
from pathlib import Path

ENGINE = [
    "agents/chair.md", "agents/_template.md", "agents/evidence-auditor.md",
    "scripts/merge_ledger.py", "skills/council-ledger/scripts/build_dashboard.py",
    "skills/council-ledger/assets/dashboard-template.html",
    "skills/persona-protocol/SKILL.md", "skills/stakeholder-protocol/SKILL.md",
    "skills/evidence-ledger/SKILL.md", "skills/scoring/SKILL.md",
    "skills/assessment-output/SKILL.md", "skills/intake/SKILL.md",
    "skills/bench-design/SKILL.md", "skills/seat-authoring/SKILL.md",
    "orchestrator/orchestrate.md",
]
LAYERS = {"analyst", "stakeholder", "redteam"}
RELEVANCE = {"high", "moderate", "low"}
NOUNS = {"company", "idea", "deal", "decision", "initiative", "question"}

problems = []


def err(msg):
    problems.append(("ERROR", msg))


def warn(msg):
    problems.append(("WARN", msg))


def frontmatter(path):
    """Minimal YAML-ish frontmatter: scalars and '- item' lists only."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end < 0:
        return {}, text
    block, body = text[3:end], text[end + 4:]
    data, key = {}, None
    for line in block.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if m:
            key, val = m.group(1), m.group(2).strip()
            data[key] = val.strip('"').strip("'") if val else []
        elif key is not None and line.lstrip().startswith("- "):
            if not isinstance(data[key], list):
                data[key] = [data[key]] if data[key] else []
            data[key].append(line.strip()[2:].strip())
    return data, body


def md_tables(body, heading_pat):
    """Rows of the first markdown table under a heading matching heading_pat."""
    m = re.search(heading_pat, body)
    if not m:
        return None
    rows, header_seen = [], False
    for line in body[m.end():].splitlines()[1:]:
        s = line.strip()
        if s.startswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                continue
            if not header_seen:
                header_seen = True  # the header row
                continue
            rows.append(cells)
        elif rows or header_seen:
            break
        elif s.startswith("#"):
            break
    return rows


def check_engine(root):
    for rel in ENGINE:
        if not (root / rel).exists():
            err(f"engine file missing: {rel}")
    if sys.version_info < (3, 9):
        warn(f"python {sys.version.split()[0]} found; 3.9+ recommended")
    agents = root / "agents"
    if agents.exists():
        for p in sorted(agents.glob("*.md")):
            if p.name.startswith("_"):
                continue
            fm, _ = frontmatter(p)
            if fm.get("name") != p.stem:
                warn(f"agents/{p.name}: frontmatter name '{fm.get('name')}' != file stem")
            if not fm.get("description"):
                warn(f"agents/{p.name}: no description")


def check_council(root):
    c = root / "council.md"
    if not c.exists():
        warn("council.md not found: run /council-setup (fine on a fresh template)")
        return None
    fm, body = frontmatter(c)
    if not fm.get("principal"):
        err("council.md: no 'principal' in frontmatter")
    active = fm.get("active_bench")
    if active and not (root / "benches" / active / "bench.md").exists():
        err(f"council.md: active_bench '{active}' has no benches/{active}/bench.md")
    rows = md_tables(body, r"##\s+Benches")
    if rows is not None:
        listed = {r[0].strip("`") for r in rows if r}
        actual = {p.parent.name for p in (root / "benches").glob("*/bench.md")}
        for s in sorted(actual - listed):
            warn(f"council.md: bench '{s}' exists but is not in the Benches table")
        for s in sorted(listed - actual):
            warn(f"council.md: Benches table lists '{s}' but benches/{s}/bench.md is missing")
    return fm


def check_bench(root, bench_dir, personas, is_preset=False):
    label = ("presets/" if is_preset else "benches/") + bench_dir.name
    bm = bench_dir / "bench.md"
    if not bm.exists():
        err(f"{label}: no bench.md")
        return
    fm, body = frontmatter(bm)
    for key in ("slug", "name", "noun", "horizon"):
        if not fm.get(key):
            err(f"{label}/bench.md: frontmatter missing '{key}'")
    if fm.get("slug") and fm["slug"] != bench_dir.name:
        warn(f"{label}/bench.md: slug '{fm['slug']}' != folder name")
    if fm.get("noun") and fm["noun"] not in NOUNS:
        warn(f"{label}/bench.md: noun '{fm['noun']}' is custom (fine; outputs will use it as written)")
    if not re.search(r"score_label\s*:", body):
        err(f"{label}/bench.md: no 'score_label:' line (skills/scoring needs it)")
    drivers = md_tables(body, r"###\s+Drivers")
    if drivers is None:
        err(f"{label}/bench.md: no '### Drivers' table")
    else:
        total, keys = 0, []
        for r in drivers:
            if len(r) < 3:
                err(f"{label}/bench.md: driver row has fewer than 3 cells: {r}")
                continue
            keys.append(r[0].strip("`"))
            try:
                total += int(re.sub(r"[^\d]", "", r[2]) or 0)
            except ValueError:
                err(f"{label}/bench.md: driver '{r[0]}' weight '{r[2]}' is not a number")
        if total != 100:
            err(f"{label}/bench.md: driver weights sum to {total}, not 100")
        if not (4 <= len(drivers) <= 8):
            warn(f"{label}/bench.md: {len(drivers)} drivers (4–8 recommended)")
        for k in keys:
            if not re.fullmatch(r"[a-z][a-z0-9_]*", k):
                warn(f"{label}/bench.md: driver key '{k}' should be snake_case (it is the finding.driver tag)")
    seats_dir = bench_dir / "seats"
    seat_files = sorted(seats_dir.glob("*.md")) if seats_dir.exists() else []
    if not seat_files:
        err(f"{label}: no seats/ folder or no seat files")
        return
    layers, seat_ids = {}, set()
    for sf in seat_files:
        sid = sf.stem
        seat_ids.add(sid)
        sfm, sbody = frontmatter(sf)
        persona = sfm.get("persona")
        layer = sfm.get("layer")
        rel = (sfm.get("relevance") or "").lower()
        if not persona:
            err(f"{label}/seats/{sf.name}: no 'persona'")
        elif persona != "custom" and persona not in personas:
            err(f"{label}/seats/{sf.name}: persona '{persona}' not found in agents/")
        if layer not in LAYERS:
            err(f"{label}/seats/{sf.name}: layer '{layer}' must be one of {sorted(LAYERS)}")
        elif persona in personas and personas[persona] and personas[persona] != layer:
            warn(f"{label}/seats/{sf.name}: layer '{layer}' but agents/{persona}.md says '{personas[persona]}'")
        if rel not in RELEVANCE:
            warn(f"{label}/seats/{sf.name}: relevance '{sfm.get('relevance')}' should be high/moderate/low")
        if persona == "custom" and not re.search(r"##\s+(Identity|Mandate)", sbody):
            err(f"{label}/seats/{sf.name}: custom persona needs a full charter (Identity, Mandate…) inline")
        if not re.search(r"##\s+Lens", sbody):
            warn(f"{label}/seats/{sf.name}: no '## Lens for this bench' section")
        layers[sid] = layer
    if "evidence-auditor" not in seat_ids:
        err(f"{label}: no evidence-auditor seat (every bench keeps its auditor)")
    for want in ("adversary", "pre-mortem"):
        if want not in seat_ids:
            warn(f"{label}: no {want} seat (red team is usually all three)")
    if not any(v == "analyst" for v in layers.values()):
        err(f"{label}: no analyst seats")
    if not any(v == "stakeholder" for v in layers.values()):
        warn(f"{label}: no stakeholder seats")
    roster = md_tables(body, r"##\s+Roster")
    if roster is None:
        warn(f"{label}/bench.md: no '## Roster' table (seats/ is authoritative; the table is the readable index)")
    else:
        listed = {r[0].strip("`") for r in roster if r}
        for s in sorted(seat_ids - listed):
            warn(f"{label}/bench.md: seat '{s}' exists but is not in the Roster table")
        for s in sorted(listed - seat_ids):
            warn(f"{label}/bench.md: Roster table lists '{s}' but seats/{s}.md is missing")
    if not re.search(r"##\s+Materials ladder", body):
        warn(f"{label}/bench.md: no '## Materials ladder' section; the materials gate will treat every depth as cleared")
    ctx = bench_dir / "context"
    if not ctx.exists():
        warn(f"{label}: no context/ folder (every convening reads it first; create it with a README.md)")
    elif not is_preset and not any(p.suffix == ".md" and p.name != "README.md" for p in ctx.iterdir()):
        warn(f"{label}/context: only a README; add an overview so convenings start with the basics")
    if not is_preset:
        for ed in sorted((bench_dir / "efforts").glob("*/")) if (bench_dir / "efforts").exists() else []:
            check_effort(label, ed)


def check_effort(label, ed):
    elabel = f"{label}/efforts/{ed.name}"
    if not (ed / "brief.md").exists():
        err(f"{elabel}: no brief.md (run intake)")
    docs = ed / "documents"
    if docs.exists() and any(p.is_file() and p.name != "index.md" for p in docs.iterdir()) and not (docs / "index.md").exists():
        warn(f"{elabel}: documents/ has files but no index.md")
    lp = ed / "ledger.json"
    if lp.exists():
        try:
            ledger = json.loads(lp.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            err(f"{elabel}/ledger.json: invalid JSON ({e})")
            return
        for key in ("effort", "roster", "phases", "evidence", "findings"):
            if key not in ledger:
                warn(f"{elabel}/ledger.json: missing '{key}' (old schema? 'company'/'rounds' became 'effort'/'phases')")
        eff = ledger.get("effort", {})
        if not eff.get("noun"):
            warn(f"{elabel}/ledger.json: effort.noun not set; outputs will say 'effort'")
        a = ledger.get("assessment", {})
        if a and a.get("score") is not None and not a.get("label"):
            warn(f"{elabel}/ledger.json: assessment has a score but no label")
    wp = ed / "watch.md"
    if wp.exists():
        wfm, _ = frontmatter(wp)
        if wfm.get("cadence") not in ("nightly", "weekly", "monthly", "quarterly"):
            err(f"{elabel}/watch.md: cadence must be nightly, weekly, monthly or quarterly")
        if not wfm.get("terms"):
            err(f"{elabel}/watch.md: no terms to watch for")
        if wfm.get("on_material") not in (None, "", "queue", "quick", "standard"):
            err(f"{elabel}/watch.md: on_material must be queue, quick or standard (never deep)")
    sh = ed / "score-history.json"
    if sh.exists():
        try:
            hist = json.loads(sh.read_text(encoding="utf-8"))
            if not isinstance(hist, list):
                err(f"{elabel}/score-history.json: must be a list")
        except json.JSONDecodeError as e:
            err(f"{elabel}/score-history.json: invalid JSON ({e})")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--root", default=None)
    ap.add_argument("--presets", action="store_true", help="also check presets/")
    args = ap.parse_args()
    root = Path(args.root) if args.root else Path(__file__).resolve().parent.parent
    check_engine(root)
    check_council(root)
    if not args.quick:
        personas = {}
        for p in (root / "agents").glob("*.md"):
            if p.name.startswith("_") or p.stem == "chair":
                continue
            fm, _ = frontmatter(p)
            d = (fm.get("description") or "").lower()
            layer = "analyst" if d.startswith("analyst") else "stakeholder" if d.startswith("stakeholder") else "redteam" if d.startswith("red-team") else ""
            personas[p.stem] = layer
        for bd in sorted((root / "benches").glob("*/")):
            if bd.is_dir():
                check_bench(root, bd, personas)
        if args.presets:
            for bd in sorted((root / "presets").glob("*/")):
                if bd.is_dir():
                    check_bench(root, bd, personas, is_preset=True)
    errors = sum(1 for lvl, _ in problems if lvl == "ERROR")
    for lvl, msg in problems:
        print(f"{lvl}: {msg}")
    if not problems:
        print("ok: council workspace is healthy")
    else:
        print(f"{errors} error(s), {len(problems) - errors} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
