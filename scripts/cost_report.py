#!/usr/bin/env python3
"""Cost receipt for a council run: real token usage from the session transcripts,
priced per model, set against the brief's Model plan.

Usage:
  cost_report.py [--brief brief.md] [--session ID_OR_PATH ...] [--project-dir DIR]
                 [--since ISO] [--until ISO] [--label TEXT] [--out receipt.md] [--json out.json]

Where the numbers come from: Claude Code writes every session to
~/.claude/projects/<cwd with non-alphanumerics as '-'>/<session>.jsonl, and every
subagent to <session>/subagents/agent-<id>.jsonl with a .meta.json holding its
description and parent. Each assistant message carries its model and usage
(input, output, cache reads, 5-minute and 1-hour cache writes). This script
de-duplicates by message id, prices each message, and maps subagents to phases:
a dispatch described "p<phase> <seat_id>" maps directly; a helper inherits its
parent's phase; otherwise the seat IDs in the plan are matched against the
description. The session's own messages are the chair.

With no --session it takes the most recently modified session for the current
directory. With no --since it uses the plan's `approved:` timestamp when that
carries a time, so a long local thread only counts this run.

It also scans for stalls: a spend or usage limit, and web fetches that failed
for lack of network. Exit 0, or 2 when a stall was found. Stdlib only.
"""
import argparse
import glob
import json
import os
import re
import sys
from pathlib import Path

# $ per million tokens: input, output, cache read. Cache writes: 5m = 1.25x input, 1h = 2x input.
# First matching key wins, so specific versions come before family fallbacks.
PRICES = [
    ("fable", (10.0, 50.0, 0.25)),
    ("mythos", (10.0, 50.0, 0.25)),
    ("opus-5-5", (4.0, 20.0, 0.20)),
    ("opus", (5.0, 25.0, 0.50)),
    ("sonnet-5", (2.0, 10.0, 0.20)),
    ("sonnet", (3.0, 15.0, 0.30)),
    ("haiku-5-5", (0.10, 0.50, 0.01)),
    ("haiku", (1.0, 5.0, 0.10)),
]
STALL_PATTERNS = [  # matched only on the app's own API error messages, never on what a model wrote
    ("spend limit", re.compile(r"monthly spend limit|spend(ing)? (limit|cap)", re.I)),
    ("out of credits", re.compile(r"out of (usage )?credits|credit balance is too low", re.I)),
    ("plan limit", re.compile(r"hit your (weekly|daily|session|5-hour|usage) limit|usage limit (reached|exceeded)", re.I)),
    ("rate limit", re.compile(r"exceed your account's rate limit", re.I)),
]
NET_PATTERN = re.compile(r"getaddrinfo ENOTFOUND|ENOTFOUND|EAI_AGAIN|network is unreachable", re.I)


def rate(model):
    m = (model or "").lower()
    if not m or "synthetic" in m:
        return None
    for key, p in PRICES:
        if key in m:
            return p
    return None


def short(model):
    m = (model or "").lower()
    for k in ("fable", "mythos", "opus", "sonnet", "haiku"):
        if k in m:
            return k
    return m or "?"


def msg_cost(r):
    p = rate(r["model"])
    if not p:
        return 0.0
    i, o, c = p
    return (r["inp"] * i + r["out"] * o + r["cr"] * c + r["w5"] * i * 1.25 + r["w1"] * i * 2) / 1e6


def scan(path, since=None, until=None):
    """Priced rows for one transcript, plus stall and network hits."""
    seen, stalls, net = {}, [], 0
    try:
        fh = open(path, encoding="utf-8", errors="replace")
    except OSError:
        return [], [], 0
    with fh:
        for line in fh:
            try:
                o = json.loads(line)
            except ValueError:
                continue
            ts = o.get("timestamp") or ""
            if (since and ts and ts < since) or (until and ts and ts > until):
                continue
            if o.get("isApiErrorMessage"):
                text = _snippet(o)
                for label, pat in STALL_PATTERNS:
                    if pat.search(text):
                        stalls.append((ts, label, text))
                        break
            if o.get("type") == "user" and isinstance(o.get("message"), dict):
                for b in o["message"].get("content") or []:
                    if isinstance(b, dict) and b.get("type") == "tool_result":
                        c = b.get("content")
                        c = c if isinstance(c, str) else " ".join(x.get("text", "") for x in (c or []) if isinstance(x, dict))
                        if len(c) < 2000 and NET_PATTERN.search(c):
                            net += 1
            m = o.get("message")
            if o.get("type") != "assistant" or not isinstance(m, dict):
                continue
            u, mid = m.get("usage"), m.get("id")
            if not u or not mid:
                continue
            seen[mid] = (m.get("model"), u, ts)  # the last write per id carries the final usage
    rows = []
    for model, u, ts in seen.values():
        cc = u.get("cache_creation") or {}
        w5, w1 = cc.get("ephemeral_5m_input_tokens"), cc.get("ephemeral_1h_input_tokens")
        if w5 is None and w1 is None:
            w5, w1 = u.get("cache_creation_input_tokens", 0), 0
        rows.append(dict(model=model, ts=ts, inp=u.get("input_tokens", 0) or 0, out=u.get("output_tokens", 0) or 0,
                         cr=u.get("cache_read_input_tokens", 0) or 0, w5=w5 or 0, w1=w1 or 0))
    return rows, stalls, net


def _snippet(o):
    m = o.get("message")
    text = ""
    if isinstance(m, dict):
        c = m.get("content")
        if isinstance(c, str):
            text = c
        elif isinstance(c, list):
            text = " ".join(b.get("text", "") for b in c if isinstance(b, dict))
    text = text or o.get("content") or ""
    return re.sub(r"\s+", " ", str(text))[:160]


def project_dir_for(cwd):
    slug = re.sub(r"[^A-Za-z0-9]", "-", str(cwd))
    return Path.home() / ".claude" / "projects" / slug


def resolve_sessions(args):
    pdir = Path(args.project_dir) if args.project_dir else project_dir_for(Path.cwd().resolve())
    out = []
    for s in args.session or []:
        p = Path(s)
        if p.suffix == ".jsonl" and p.exists():
            out.append(p)
        elif (pdir / f"{s}.jsonl").exists():
            out.append(pdir / f"{s}.jsonl")
        else:
            print(f"warning: session {s} not found under {pdir}", file=sys.stderr)
    if not args.session:
        cands = sorted(pdir.glob("*.jsonl"), key=lambda p: p.stat().st_mtime) if pdir.exists() else []
        if cands:
            out.append(cands[-1])
    return out, pdir


def parse_plan(brief_path):
    """The brief's ### Model plan: header fields and rows (phase, seats, model, est)."""
    plan = dict(ceiling=None, estimate=None, approved=None, rows=[])
    if not brief_path or not Path(brief_path).exists():
        return plan
    text = Path(brief_path).read_text(encoding="utf-8")
    blocks = list(re.finditer(r"^###\s+Model plan\b.*$", text, re.M))
    if not blocks:
        return plan
    body = text[blocks[-1].end():]
    nxt = re.search(r"^#{1,3}\s", body, re.M)
    body = body[: nxt.start()] if nxt else body
    m = re.search(r"ceiling:\s*\$?([\d,.]+)", body)
    plan["ceiling"] = float(m.group(1).replace(",", "")) if m else None
    m = re.search(r"estimate:\s*\$?([\d,.]+)", body)
    plan["estimate"] = float(m.group(1).replace(",", "")) if m else None
    m = re.search(r"approved:\s*(\S+)", body)
    plan["approved"] = m.group(1) if m else None
    header = None
    for line in body.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
            continue
        if header is None:
            header = [c.lower() for c in cells]
            continue
        row = dict(zip(header, cells))
        est = re.sub(r"[^\d.]", "", row.get("est $", row.get("est", "")) or "")
        seats = [x.strip() for x in re.split(r"[,;]", row.get("seats", "")) if x.strip()]
        plan["rows"].append(dict(phase=_phase_key(row.get("phase", "")), seats=seats,
                                 model=(row.get("model") or "").lower(), est=float(est) if est else 0.0))
    if plan["estimate"] is None and plan["rows"]:
        plan["estimate"] = sum(r["est"] for r in plan["rows"])
    return plan


def _phase_key(cell):
    m = re.match(r"\s*(\d+)", cell or "")
    return m.group(1) if m else ("chair" if "chair" in (cell or "").lower() else (cell or "?").strip().lower())


def collect(sessions, since, until, plan):
    agents, stalls, net = [], [], 0
    chair_rows = []
    for sp in sessions:
        rows, st, n = scan(sp, since, until)
        chair_rows += rows
        stalls += st
        net += n
        sub = sp.with_suffix("") / "subagents"
        for f in sorted(glob.glob(str(sub / "agent-*.jsonl"))):
            aid = os.path.basename(f)[6:-6]
            meta = {}
            mp = f[:-6] + ".meta.json"
            if os.path.exists(mp):
                try:
                    meta = json.load(open(mp, encoding="utf-8"))
                except ValueError:
                    meta = {}
            rows, st, n = scan(f, since, until)
            stalls += st
            net += n
            if not rows:
                continue
            agents.append(dict(id=aid, desc=meta.get("description") or "", parent=meta.get("parentAgentId"),
                               models=sorted({short(r["model"]) for r in rows if rate(r["model"])}),
                               cost=sum(msg_cost(r) for r in rows),
                               tokens=sum(r["inp"] + r["out"] + r["cr"] + r["w5"] + r["w1"] for r in rows)))
    byid = {a["id"]: a for a in agents}
    seat_index = [(s.lower(), r["phase"]) for r in plan["rows"] for s in r["seats"]]

    def place(a, depth=0):
        if "phase" in a:
            return a["phase"], a["seat"]
        m = re.match(r"\s*p(\d+)\s+([\w.-]+)", a["desc"], re.I)
        if m:
            ph, seat = m.group(1), m.group(2)
        elif a["parent"] and a["parent"] in byid and depth < 6:
            ph, seat = place(byid[a["parent"]], depth + 1)
            a["helper"] = True
        else:
            d = a["desc"].lower()
            hit = next(((s, p) for s, p in sorted(seat_index, key=lambda x: -len(x[0])) if s and s in d), None)
            ph, seat = (hit[1], hit[0]) if hit else ("unplanned", a["desc"][:40] or a["id"])
        a["phase"], a["seat"] = ph, seat
        return ph, seat

    for a in agents:
        place(a)
    chair = dict(cost=sum(msg_cost(r) for r in chair_rows),
                 models=sorted({short(r["model"]) for r in chair_rows if rate(r["model"])}))
    return agents, chair, stalls, net


def phase_order(k):
    return (0, 0) if k == "chair" else (1, int(k)) if str(k).isdigit() else (2, 0)


def build(plan, agents, chair, stalls, net, label, sessions):
    est = {}
    plan_models = {}
    for r in plan["rows"]:
        est[r["phase"]] = est.get(r["phase"], 0.0) + r["est"]
        plan_models.setdefault(r["phase"], set()).add(r["model"])
    meas = {"chair": chair["cost"]}
    seats = {}
    for a in agents:
        meas[a["phase"]] = meas.get(a["phase"], 0.0) + a["cost"]
        key = (a["phase"], a["seat"])
        s = seats.setdefault(key, dict(cost=0.0, helpers=0, models=set()))
        s["cost"] += a["cost"]
        s["models"].update(a["models"])
        if a.get("helper"):
            s["helpers"] += 1
    total = sum(meas.values())
    phases = sorted(set(est) | set(meas), key=phase_order)
    rows, overruns = [], []
    for ph in phases:
        e, m = est.get(ph), meas.get(ph, 0.0)
        n_seats = len({k[1] for k in seats if k[0] == ph}) if ph != "chair" else 1
        note = []
        if ph != "chair":
            ran = set().union(*[v["models"] for k, v in seats.items() if k[0] == ph]) if any(k[0] == ph for k in seats) else set()
            planned = {short(x) for x in plan_models.get(ph, set())}
            off = sorted(ran - planned) if planned else []
            if off:
                note.append(f"ran on {', '.join(off)}; plan said {', '.join(sorted(planned))}")
        if ph == "unplanned" and m:
            note.append("seats the plan did not name")
        if e is not None and m > e * 1.25 and m - e > 2:
            note.append("over")
            overruns.append(ph)
        rows.append(dict(phase=ph, est=e, measured=round(m, 2), seats=n_seats, note="; ".join(note)))
    why = []
    for ph in overruns:
        top = sorted(((k[1], v) for k, v in seats.items() if k[0] == ph), key=lambda x: -x[1]["cost"])[:3]
        parts = [f"{s} ${v['cost']:.2f} on {'/'.join(sorted(v['models'])) or '?'}" + (f" with {v['helpers']} helper(s)" if v["helpers"] else "") for s, v in top]
        if ph == "chair":
            parts = [f"the chair's own turns ${chair['cost']:.2f} on {'/'.join(chair['models']) or '?'}"]
        why.append(dict(phase=ph, over=round(meas.get(ph, 0) - (est.get(ph) or 0), 2), top=parts))
    return dict(label=label, ceiling=plan["ceiling"], estimate=plan["estimate"], measured=round(total, 2),
                rows=rows, why=why, stalls=stalls, net_failures=net, agents=len(agents),
                sessions=[str(s) for s in sessions])


def plain_stalls(rep):
    out = []
    seen = set()
    for ts, label, snip in rep["stalls"]:
        if label in seen:
            continue
        seen.add(label)
        when = ts[:16].replace("T", " ") + " UTC" if ts else "an unknown time"
        reset = re.search(r"resets? ([^.,]+(\([^)]*\))?)", snip or "")
        if label == "spend limit":
            out.append(f"The run stopped at {when} because the account reached its monthly spend limit. Raise the limit (claude.ai/settings/usage) or wait for it to reset, then resume the round; it picks up where it stopped.")
        elif label == "out of credits":
            out.append(f"The run stopped at {when} because the account ran out of usage credits. Add credits (claude.ai/settings/usage), then resume the round.")
        elif label == "plan limit":
            out.append(f"The run stopped at {when} because the plan's usage limit was reached" + (f" (it {reset.group(0)})" if reset else "") + ". Resume the round after the reset.")
        else:
            out.append(f"The run slowed at {when} on the account's rate limit; it retries on its own. If it stopped, resume the round.")
    if rep["net_failures"]:
        out.append(f"{rep['net_failures']} web page fetch(es) failed because the environment could not reach the internet. Cloud rounds need an environment with Full network access (engine docs/cloud-setup.md).")
    return out


def money(x):
    return "n/a" if x is None else f"${x:,.2f}"


def markdown(rep):
    e, m, c = rep["estimate"], rep["measured"], rep["ceiling"]
    head = f"Estimate {money(e)}" + (f" (ceiling {money(c)})" if c else "") + f" · Measured {money(m)}"
    if e:
        pct = (m - e) / e * 100
        verdict = f"{abs(pct):.0f}% {'over' if pct > 0 else 'under'} the estimate"
        if c:
            verdict += ", within the ceiling" if m <= c else f", {money(m - c)} over the ceiling"
        head += f" · {verdict}"
    lines = [f"# Cost receipt — {rep['label']}", "", head, "",
             "| phase | estimate | measured | difference | seats | note |", "| --- | --- | --- | --- | --- | --- |"]
    for r in rep["rows"]:
        diff = "" if r["est"] is None else f"{'+' if r['measured'] - r['est'] >= 0 else '-'}${abs(r['measured'] - r['est']):,.2f}"
        lines.append(f"| {r['phase']} | {money(r['est'])} | {money(r['measured'])} | {diff} | {r['seats']} | {r['note']} |")
    lines.append("")
    if rep["why"]:
        lines += ["## Where it went over", ""]
        for w in rep["why"]:
            lines.append(f"- Phase {w['phase']}, {money(w['over'])} over: " + "; ".join(w["top"]) + ". Reason: <the chair says why in one sentence>")
        lines.append("")
    st = plain_stalls(rep)
    lines += ["## Stalls", ""] + ([f"- {s}" for s in st] if st else ["- None."]) + [""]
    lines.append(f"Measured from {rep['agents']} subagent transcript(s) and the chair's own messages at API prices (the table in scripts/cost_report.py). Subscriptions are not metered per token; this is what the same work costs at pay-per-token rates. Web-search fees are not included.")
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--brief")
    ap.add_argument("--session", action="append")
    ap.add_argument("--project-dir")
    ap.add_argument("--since")
    ap.add_argument("--until")
    ap.add_argument("--label", default="council run")
    ap.add_argument("--out")
    ap.add_argument("--json")
    args = ap.parse_args()
    plan = parse_plan(args.brief)
    since = args.since
    if not since and plan["approved"] and "T" in plan["approved"]:
        since = plan["approved"]
    sessions, pdir = resolve_sessions(args)
    if not sessions:
        print(f"no session transcript found under {pdir}; the receipt shows the estimate only", file=sys.stderr)
    agents, chair, stalls, net = collect(sessions, since, args.until, plan)
    rep = build(plan, agents, chair, stalls, net, args.label, sessions)
    md = markdown(rep)
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(md, encoding="utf-8")
    if args.json:
        Path(args.json).write_text(json.dumps(rep, indent=2, default=list), encoding="utf-8")
    print(md)
    return 2 if (stalls or net) else 0


if __name__ == "__main__":
    sys.exit(main())
