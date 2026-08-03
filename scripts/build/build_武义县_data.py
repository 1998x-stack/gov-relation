#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 武义县 (Wuyi County, Zhejiang) leadership network.

归口地区: 浙江省金华市武义县
"""

import sqlite3
import os
import sys
from datetime import datetime, date

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, REPO_ROOT

SLUG = "武义县"
PROVINCE = "浙江省"
PARENT_CITY = "金华市"
TODAY = "2026-08-03"

# Use staging directory
STAGING = REPO_ROOT / "data/tmp/zhejiang_武义县"
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

# ═══════════════════════════════════════════════════════════════════════════
# DATA — hardcoded research data
# Sources: 武义县人民政府网站 (www.zjwy.gov.cn) news reports
# Confirmed as of 2026-08-03
# ═══════════════════════════════════════════════════════════════════════════

persons = [
    {
        "id": 1,
        "name": "陈洪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "武义县委书记",
        "current_org": "中共武义县委员会",
    },
    {
        "id": 2,
        "name": "李强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "武义县委副书记、县长",
        "current_org": "武义县人民政府",
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共武义县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共金华市委员会",
        "location": "浙江省金华市武义县",
    },
    {
        "id": 2,
        "name": "武义县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "金华市人民政府",
        "location": "浙江省金华市武义县",
    },
]

positions = [
    {
        "id": 1,
        "person_id": 1,
        "org_id": 1,
        "title": "武义县委书记",
        "start": "待查",
        "end": "present",
        "rank": "正处级",
        "note": "Confirmed on official government website as of 2026-08-03",
    },
    {
        "id": 2,
        "person_id": 2,
        "org_id": 2,
        "title": "武义县委副书记、县长",
        "start": "待查",
        "end": "present",
        "rank": "正处级",
        "note": "Confirmed on official government website as of 2026-08-03",
    },
]

relationships = [
    {
        "id": 1,
        "person_a": 1,
        "person_b": 2,
        "type": "党政正职搭档",
        "context": "县委书记与县长，为武义县党政领导核心搭档",
        "overlap_org": "武义县",
        "overlap_period": "至2026年8月在任",
    },
]

# ═══════════════════════════════════════════════════════════════════════════
# GEXF node colors
# ═══════════════════════════════════════════════════════════════════════════

COLORS = {
    "party_secretary": "255,50,50",   # Red — 县委书记
    "mayor": "50,100,255",             # Blue — 县长/县长
    "other_person": "100,100,100",     # Grey
    "org_dangwei": "255,200,200",     # Pink — 党委
    "org_gov": "200,200,255",         # Light blue — 政府
    "org_devzone": "200,255,200",     # Light green
    "org_town": "255,255,200",        # Light yellow
    "org_institution": "220,220,220", # Light grey
    "org_default": "200,200,200",
}

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def build_gexf(output_path):
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append(f'    <description>武义县领导工作关系网络 — 浙江省金华市武义县, as of {TODAY}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')
    for p in persons:
        pid = p["id"]
        name = p["name"]
        if pid == 1:
            color = COLORS["party_secretary"]
            sz = "20.0"
            role = "县委书记"
        elif pid == 2:
            color = COLORS["mayor"]
            sz = "20.0"
            role = "县长"
        else:
            color = COLORS["other_person"]
            sz = "12.0"
            role = ""
        c = color.split(",")
        lines.append(f'      <node id="p{pid}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="a0" value="person"/>')
        lines.append(f'          <attvalue for="a1" value="{esc(role)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for org in organizations:
        oid = org["id"]
        oname = org["name"]
        otype = org["type"]
        if otype == "党委":
            color = COLORS["org_dangwei"]
        elif otype == "政府":
            color = COLORS["org_gov"]
        else:
            color = COLORS["org_unit"]
        c = color.split(",")
        lines.append(f'      <node id="o{oid}" label="{esc(oname)}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="a0" value="organization"/>')
        lines.append(f'          <attvalue for="a1" value="{esc(otype)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <v:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person -> organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person <-> person (relationship)
    for rel in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{rel["person_a"]}" target="p{rel["person_b"]}" label="{esc(rel["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(rel["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

def main():
    print(f"Building {SLUG} network...")
    print(f"  DB path: {DB_PATH}")
    print(f"  GEXF path: {GEXF_PATH}")

    # Build using runner
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    # Override GEXF with custom version
    print("  Writing custom GEXF with viz attributes...")
    gexf_path = GEXF_PATH
    if "tmp" in os.path.dirname(str(gexf_path)):
        gexf_path = GEXF_PATH
    build_gexf(GEXF_PATH)

    # Verify
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM persons")
    p_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM organizations")
    o_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM positions")
    pos_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM relationships")
    r_count = cur.fetchone()[0]
    conn.close()

    print(f"\n  Summary: {p_count} persons, {o_count} organizations, {pos_count} positions, {r_count} relationships")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print("Done.")


if __name__ == "__main__":
    main()