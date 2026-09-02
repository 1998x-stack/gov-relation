#!/usr/bin/env python3
"""Reusable helper: list + dispatch pending TODO regions for china-gov-network investigations.

Usage:
  python3 scripts/data/dispatch_batch.py --list                # print next N pending tasks
  python3 scripts/data/dispatch_batch.py --count N          # how many pending
Supports the goal-driven batch pipeline: reads data/TODO.json and reveals the next
batch of pending (undone) region tasks so the orchestrator can dispatch subagents.

Also normalizes person-label coverage so genuinely-covered regions are not re-investigated.
"""
from __future__ import annotations
import json, re, glob, os, sys, argparse
from collections import defaultdict
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

def coverage_sets():
    graph_names = {os.path.basename(f).replace("_network.gexf","") for f in glob.glob("data/graph/*.gexf")}
    person_labels=set()
    for f in glob.glob("data/persons/*.json")+glob.glob("data/provinces/*/persons/*.json"):
        for p in re.split(r"-", os.path.basename(f).replace(".json",""))[1:]:
            person_labels.add(p)
    return graph_names, person_labels

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--list", action="store_true", help="print next N pending tasks")
    ap.add_argument("--n", type=int, default=10, help="number of pending tasks to print (default 10)")
    ap.add_argument("--province", help="filter to a province substring")
    ap.add_argument("--count", action="store_true", help="print total pending count by province")
    a=ap.parse_args()
    d=json.load(open("data/TODO.json"))
    if a.count:
        for p in d["provinces"]:
            pend=[t for t in p["tasks"] if not t["done"]]
            if pend:
                print(f"{p['province']:12s} {len(pend)}")
        return
    if a.list:
        shown=0
        for p in d["provinces"]:
            if a.province and a.province not in p["province"]:
                continue
            for t in p["tasks"]:
                if not t["done"]:
                    roles="+".join(x["role"] for x in t["targets"])
                    print(f"{t['region']}	{p['province']}	{t['parent_city']}	{t['level']}	{roles}")
                    shown+=1
                    if shown>=a.n:
                        return
    else:
        ap.print_help()

if __name__=="__main__":
    main()
