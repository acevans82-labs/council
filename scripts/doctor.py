#!/usr/bin/env python3
"""Council workspace doctor.

Usage: doctor.py [--quick] [--root DIR] [--presets]

Checks the engine version against the latest release, the engine files, the
workspace CLAUDE.md and AGENTS.md against templates/workspace, council.md
(including the ## Cloud records: routine, environment with Full network, GitHub
app, connectors), every bench (bench.md, seats/ and their frontmatter, roster
table, driver weights) and every effort (brief and its Model plan, ledger, score
history, waiting QUESTION/BLOCKED files). Prints one line per problem.

Exit 1 if any ERROR was found; else 3 if an engine update is available (the
'update available:' line and its notes are printed first); else 0. --quick checks
only the engine, the workspace templates and council.md: fast enough for the first
turn of every thread. The live cloud checks (routine enabled, environment, the
routine's connectors against the session's) need the RemoteTrigger tool and are
run by /council-doctor per skills/cloud-routines. Stdlib only.

Engine root is this script's grandparent. Workspace root is --root, else the
current directory when it holds council.md or benches/ or an engine/ submodule,
else the engine root (developing or trying the engine with data at its root).
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
    "orchestrator/orchestrate.md", "skills/run-planning/SKILL.md", "skills/round-close/SKILL.md",
    "skills/thread-swap/SKILL.md", "skills/cloud-routines/SKILL.md", "scripts/cost_report.py",
    "scripts/check_update.py", "templates/workspace/CLAUDE.md", "templates/workspace/AGENTS.md",
]
MODELS = {"fable", "opus", "sonnet", "haiku", "mythos"}
LAYERS = {"analyst", "stakeholder", "redteam"}
RELEVANCE = {"high", "moderate", "low"}
NOUNS = {"company", "idea", "deal", "decision", "initiative", "question"}

problems = []
update = {}


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
    try:
        import subprocess
        r = subprocess.run([sys.executable, str(root / "scripts" / "check_update.py")], capture_output=True, text=True, timeout=40)
        first = (r.stdout.splitlines() or [""])[0]
        info = json.loads(first) if first.startswith("{") else {}
        if info.get("status") == "available":
            update.update(info)
            notes = [ln for ln in r.stdout.splitlines()[1:] if ln.startswith("## ") or ln.startswith("- **")]
            print(f"update available: council engine {info.get('latest')} (you have {info.get('current')})")
            for ln in notes[:12]:
                print(f"  {ln}")
            print("  options: update now (check_update.py --apply), skip, or remind me in 3 days (check_update.py --snooze)")
        elif info.get("status") == "snoozed":
            print(f"note: engine {info.get('latest')} available, snoozed until {info.get('until')}")
    except Exception:
        pass
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


def check_workspace(ws, engine):
    if ws == engine:
        return
    sub = ws / "engine"
    if not sub.exists() or not (sub / ".claude-plugin" / "plugin.json").exists():
        err("workspace: engine/ submodule is missing or empty; run: git submodule update --init")
    tpl = engine / "templates" / "workspace" / "CLAUDE.md"
    own = ws / "CLAUDE.md"
    stamp = lambda t: (re.search(r"template version (\d+\.\d+\.\d+)", t) or [None, None])[1]
    if not own.exists():
        err("workspace: no CLAUDE.md; copy engine/templates/workspace/CLAUDE.md")
    elif tpl.exists():
        o, t = own.read_text(encoding="utf-8"), tpl.read_text(encoding="utf-8")
        if o.strip() != t.strip():
            so, st = stamp(o), stamp(t)
            if so and st and so != st:
                warn(f"workspace: CLAUDE.md is from template {so}; the engine's is {st}. Copy engine/templates/workspace/CLAUDE.md over to take the update")
            else:
                warn("workspace: CLAUDE.md differs from engine/templates/workspace/CLAUDE.md (a local edit?); copy it over to match the engine")
    tpa = engine / "templates" / "workspace" / "AGENTS.md"
    own_a = ws / "AGENTS.md"
    if not own_a.exists():
        warn("workspace: no AGENTS.md; cloud rounds will not know to fetch the submodule (copy engine/templates/workspace/AGENTS.md)")
    elif tpa.exists() and not own_a.read_text(encoding="utf-8").strip().startswith(tpa.read_text(encoding="utf-8").strip()):
        warn("workspace: AGENTS.md does not start with engine/templates/workspace/AGENTS.md (an older copy, or rules the engine now carries); copy the template over and keep workspace-only rules below its last line")


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
    check_cloud(body)
    return fm


def check_cloud(body):
    m = re.search(r"^##\s+Cloud\s*$(.*?)(?=^##\s|\Z)", body, re.M | re.S)
    if not m:
        warn("council.md: no '## Cloud' section; rounds will run in the local thread (run /council-setup step 4 to create the cloud routine)")
        return
    lines = {}
    for ln in m.group(1).splitlines():
        k = re.match(r"^\s*([a-z_]+):\s*(.*)$", ln)
        if k:
            lines[k.group(1)] = k.group(2).strip()
    routine = lines.get("routine", "")
    if not routine or routine.startswith("not set up"):
        print("note: no cloud routine recorded; rounds run in the local thread (/council-setup creates one)")
        return
    if not re.search(r"trig_\w+", routine):
        warn("council.md: the cloud routine has no trigger id (trig_...) recorded; /council-doctor can look it up")
    env = lines.get("environment", "")
    if not env or env.startswith("not"):
        warn("council.md: no cloud environment recorded; rounds need an environment with Full network access (skills/cloud-routines)")
    elif not re.search(r"network\s+full", env, re.I):
        warn(f"council.md: the cloud environment is not recorded as Full network ('{env}'); with Limited network every web page fetch fails")
    gh = lines.get("github_app", "")
    if not gh or gh.startswith("not"):
        warn("council.md: the Claude GitHub app on the workspace's owner is not recorded as checked (skills/cloud-routines, preflight)")
    con = lines.get("connectors", "")
    if not con or con.startswith("not"):
        print("note: the cloud routine's connectors have not been checked; run /council-doctor in a session with RemoteTrigger")
    elif re.search(r"missing:\s*(?!none)\S", con, re.I):
        warn(f"council.md: the cloud routine is missing connectors the local session has ({con.split('missing:')[1].strip()})")


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
        if not sf.read_text(encoding="utf-8").startswith("---"):
            err(f"{label}/seats/{sf.name}: no frontmatter (persona, layer, relevance between --- lines)")
            continue
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", sid):
            warn(f"{label}/seats/{sf.name}: seat ID '{sid}' should be lowercase with hyphens (it tags every record)")
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


def check_plan(elabel, brief):
    text = brief.read_text(encoding="utf-8")
    heads = list(re.finditer(r"^###\s+Model plan\b.*$", text, re.M))
    if not heads:
        return
    body = text[heads[-1].end():]
    nxt = re.search(r"^#{1,3}\s", body, re.M)
    body = body[: nxt.start()] if nxt else body
    header, rows = None, []
    for line in body.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
            continue
        if header is None:
            header = [c.lower() for c in cells]
        else:
            rows.append(dict(zip(header, cells)))
    if header is None:
        err(f"{elabel}/brief.md: '### Model plan' has no table")
        return
    if "est $" not in header or not re.search(r"ceiling:", body):
        warn(f"{elabel}/brief.md: the latest Model plan is in the old shape (no ceiling or 'est $' column); the next plan will be written in the skills/run-planning shape")
        return
    for r in rows:
        model = (r.get("model") or "").lower()
        if not any(k in model for k in MODELS) and not model.startswith("as "):
            warn(f"{elabel}/brief.md: Model plan row '{r.get('seats', '')[:40]}' names model '{r.get('model')}' (use fable, opus, sonnet or haiku)")
    est = re.search(r"estimate:\s*\$?([\d,.]+)", body)
    total = sum(float(re.sub(r"[^\d.]", "", r.get("est $", "")) or 0) for r in rows)
    if est and abs(float(est.group(1).replace(",", "")) - total) > max(5, 0.2 * total):
        print(f"note: {elabel}/brief.md: the plan's estimate ({est.group(1)}) and its rows (${total:.0f}) differ by more than the margin")
    if not re.search(r"approved:\s*\S", body):
        print(f"note: {elabel}/brief.md: the latest Model plan is a draft (no 'approved:' line); nothing will be dispatched until the principal says go")


def check_effort(label, ed):
    elabel = f"{label}/efforts/{ed.name}"
    if not (ed / "brief.md").exists():
        err(f"{elabel}: no brief.md (run intake)")
    else:
        check_plan(elabel, ed / "brief.md")
    rounds = sorted((ed / "rounds").glob("*/")) if (ed / "rounds").exists() else []
    if rounds:
        latest = rounds[-1]
        for name, what in (("QUESTION.md", "a question from the council"), ("BLOCKED.md", "a blocked round")):
            if (latest / name).exists():
                print(f"note: {elabel}/rounds/{latest.name}: {what} is waiting on the principal ({name})")
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
    engine = Path(__file__).resolve().parent.parent
    if args.root:
        root = Path(args.root).resolve()
    else:
        cwd = Path.cwd().resolve()
        root = cwd if any((cwd / x).exists() for x in ("council.md", "benches", "engine")) and cwd != engine else engine
    check_engine(engine)
    check_workspace(root, engine)
    check_council(root)
    if not args.quick:
        personas = {}
        for p in (engine / "agents").glob("*.md"):
            if p.name.startswith("_") or p.stem == "chair":
                continue
            fm, _ = frontmatter(p)
            d = (fm.get("description") or "").lower()
            layer = "analyst" if d.startswith("analyst") else "stakeholder" if d.startswith("stakeholder") else "redteam" if d.startswith("red-team") else ""
            personas[p.stem] = layer
        for bd in sorted((root / "benches").glob("*/")) if (root / "benches").exists() else []:
            if bd.is_dir():
                check_bench(root, bd, personas)
        if args.presets:
            for bd in sorted((engine / "presets").glob("*/")):
                if bd.is_dir():
                    check_bench(root, bd, personas, is_preset=True)
    errors = sum(1 for lvl, _ in problems if lvl == "ERROR")
    for lvl, msg in problems:
        print(f"{lvl}: {msg}")
    if not problems:
        print("ok: council workspace is healthy")
    else:
        print(f"{errors} error(s), {len(problems) - errors} warning(s)")
    return 1 if errors else 3 if update else 0


if __name__ == "__main__":
    sys.exit(main())
