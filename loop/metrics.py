#!/usr/bin/env python3
"""
metrics.py — Sovereign Token Usage Viewer

Reads memory/metrics.jsonl and prints a summary of local executor usage.
Usage:
    python3 metrics.py              # summary by agent
    python3 metrics.py --session X  # filter to a session
    python3 metrics.py --tail 20    # last N tasks
    python3 metrics.py --full       # all rows
"""

import argparse, json, os
from collections import defaultdict

SOVEREIGN    = os.environ.get("SOVEREIGN", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
METRICS_FILE = f"{SOVEREIGN}/memory/metrics.jsonl"

def load(session=None, tail=None):
    if not os.path.exists(METRICS_FILE):
        return []
    with open(METRICS_FILE) as f:
        rows = [json.loads(l) for l in f if l.strip()]
    if session:
        rows = [r for r in rows if r.get("session") == session]
    if tail:
        rows = rows[-tail:]
    return rows

def summary(rows):
    by_agent = defaultdict(lambda: {"tasks": 0, "tokens_in": 0, "tokens_out": 0, "elapsed": 0.0, "failures": 0})
    for r in rows:
        a = by_agent[r.get("agent", "?")]
        a["tasks"]      += 1
        a["tokens_in"]  += r.get("tokens_in", 0)
        a["tokens_out"] += r.get("tokens_out", 0)
        a["elapsed"]    += r.get("elapsed_s", 0)
        if not r.get("success", True):
            a["failures"] += 1

    total_in  = sum(v["tokens_in"]  for v in by_agent.values())
    total_out = sum(v["tokens_out"] for v in by_agent.values())
    total_t   = sum(v["elapsed"]    for v in by_agent.values())
    total_tasks = sum(v["tasks"]    for v in by_agent.values())

    print(f"\n{'Agent':<12} {'Model':<24} {'Tasks':>6} {'In':>8} {'Out':>8} {'Total':>8} {'Elapsed':>9} {'tok/s':>7} {'Fail':>5}")
    print("─" * 95)

    from sovereign_loop_dispatch_agents import AGENTS  # lazy import for model names
    # Fallback: just use agent name
    for agent, v in sorted(by_agent.items(), key=lambda x: -x[1]["tokens_out"]):
        model = AGENTS.get(agent, "?") if False else "—"
        tps   = round(v["tokens_out"] / v["elapsed"], 1) if v["elapsed"] > 0 else 0
        total = v["tokens_in"] + v["tokens_out"]
        print(f"{agent:<12} {model:<24} {v['tasks']:>6} {v['tokens_in']:>8} {v['tokens_out']:>8} {total:>8} {v['elapsed']:>8.1f}s {tps:>7} {v['failures']:>5}")

    print("─" * 95)
    tps_total = round(total_out / total_t, 1) if total_t > 0 else 0
    print(f"{'TOTAL':<12} {'':24} {total_tasks:>6} {total_in:>8} {total_out:>8} {total_in+total_out:>8} {total_t:>8.1f}s {tps_total:>7}")
    print()

def full_table(rows):
    print(f"\n{'Timestamp':<22} {'Session':<20} {'Agent':<12} {'In':>6} {'Out':>6} {'s':>6} {'t/s':>6} {'OK':>4}")
    print("─" * 85)
    for r in rows:
        ts   = r.get("ts", "")[:19]
        sess = r.get("session", "")[:20]
        ag   = r.get("agent", "?")
        ti   = r.get("tokens_in", 0)
        to   = r.get("tokens_out", 0)
        el   = r.get("elapsed_s", 0)
        tps  = r.get("tok_per_s", 0)
        ok   = "✓" if r.get("success", True) else "✗"
        print(f"{ts:<22} {sess:<20} {ag:<12} {ti:>6} {to:>6} {el:>6.1f} {tps:>6} {ok:>4}")
    print()


# ── Patch summary to skip bad import ─────────────────────────────────────
def summary_fixed(rows):
    by_agent = defaultdict(lambda: {"model": "—", "tasks": 0, "tokens_in": 0, "tokens_out": 0, "elapsed": 0.0, "failures": 0})
    for r in rows:
        a = by_agent[r.get("agent", "?")]
        a["model"]      = r.get("model", "—")
        a["tasks"]      += 1
        a["tokens_in"]  += r.get("tokens_in", 0)
        a["tokens_out"] += r.get("tokens_out", 0)
        a["elapsed"]    += r.get("elapsed_s", 0)
        if not r.get("success", True):
            a["failures"] += 1

    total_in    = sum(v["tokens_in"]  for v in by_agent.values())
    total_out   = sum(v["tokens_out"] for v in by_agent.values())
    total_t     = sum(v["elapsed"]    for v in by_agent.values())
    total_tasks = sum(v["tasks"]      for v in by_agent.values())

    print(f"\n{'Agent':<12} {'Model':<26} {'Tasks':>6} {'In':>8} {'Out':>8} {'Total':>8} {'Elapsed':>9} {'tok/s':>7} {'Fail':>5}")
    print("─" * 98)
    for agent, v in sorted(by_agent.items(), key=lambda x: -x[1]["tokens_out"]):
        tps   = round(v["tokens_out"] / v["elapsed"], 1) if v["elapsed"] > 0 else 0
        total = v["tokens_in"] + v["tokens_out"]
        print(f"{agent:<12} {v['model']:<26} {v['tasks']:>6} {v['tokens_in']:>8} {v['tokens_out']:>8} {total:>8} {v['elapsed']:>8.1f}s {tps:>7} {v['failures']:>5}")

    print("─" * 98)
    tps_total = round(total_out / total_t, 1) if total_t > 0 else 0
    print(f"{'TOTAL':<12} {'':26} {total_tasks:>6} {total_in:>8} {total_out:>8} {total_in+total_out:>8} {total_t:>8.1f}s {tps_total:>7}")
    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sovereign token usage viewer")
    parser.add_argument("--session", default=None, help="Filter to a session slug")
    parser.add_argument("--tail",    type=int, default=None, help="Last N task rows")
    parser.add_argument("--full",    action="store_true", help="Show all rows")
    args = parser.parse_args()

    rows = load(session=args.session, tail=args.tail)

    if not rows:
        print("No metrics recorded yet. Run dispatch.py to generate data.")
    elif args.full:
        full_table(rows)
        summary_fixed(rows)
    else:
        summary_fixed(rows)
        if rows:
            print(f"  ({len(rows)} task{'s' if len(rows)!=1 else ''} total — use --full for row detail)")
