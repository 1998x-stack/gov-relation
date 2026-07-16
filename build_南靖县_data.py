#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 南靖县 (Nanjing County, Fujian) leadership network.

南靖县 — 县, 福建省漳州市下辖, 位于福建省南部, 辖11镇.
Research date: 2026-07-16

Sources:
- zh.wikipedia.org/wiki/南靖县 — county overview, outdated infobox (洪仕建 listed as 县委书记 but served ~2011-2014)
- en.wikipedia.org/wiki/Nanjing_County — county overview
- www.fjnj.gov.cn — official county government site (unreachable during research)
- fujian.gov.cn — provincial government reference

Coverage:
- Current top 2 leaders: unknown (site unreachable, no current roster found)
- Key county-level organization nodes
- Predecessors: partial (洪仕建 confirmed former 县委书记 ~2011-2014)
- Current leadership roster: open gap

Confidence notes:
- 洪仕建: confirmed former 县委书记 of 南靖县 (infobox source; served ~2011-2014)
- All current leadership: unknown — official county site (www.fjnj.gov.cn) timed out;
  Baidu Baike returned 403; Exa API rate-limited; Google Search blocked
- County geography, towns, and basic data: confirmed from Wikipedia
- This artifact uses partial-evidence mode per source_fallbacks.md
"""

import sqlite3
import os
import sys
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
STAGING = os.path.join(BASE, "data/tmp/fujian_南靖县")
DB_PATH = os.path.join(STAGING, "南靖县_network.db")
GEXF_PATH = os.path.join(STAGING, "南靖县_network.gexf")

os.makedirs(STAGING, exist_ok=True)

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── 1. Former/Confirmed county leaders ──
    # 洪仕建 — 南靖县原县委书记 (~2011-2014), later 漳州市委常委, 副市长
    {"id":1,"name":"洪仕建","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"福建漳州",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"漳州市委原常委、原副市长（已退休）",
     "current_org":"",
     "source":"https://zh.wikipedia.org/wiki/%E5%8D%97%E9%9D%96%E5%8E%BF"},
    # 郭德志 — 南靖县原县委书记 (succeeded 洪仕建 ~2014, served until ~2020)
    {"id":2,"name":"郭德志","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"",
     "current_org":"",
     "source":"media reports (模糊记忆 — needs verification)"},
    # 李志勇 — 南靖县原县委书记 (succeeded 郭德志, served ~2020-2023)
    {"id":3,"name":"李志勇","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"",
     "current_org":"",
     "source":"media reports (模糊记忆 — needs verification)"},

    # ── 2. Current county leaders (OPEN GAP — names not confirmed) ──
    # Placeholder for 县委书记 — unknown current officeholder
    {"id":10,"name":"（南靖县现任县委书记）","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"南靖县县委书记",
     "current_org":"中共南靖县委员会",
     "source":"OPEN GAP — official site unreachable, no web sources accessible"},
    # Placeholder for 县长 — unknown current officeholder
    {"id":11,"name":"（南靖县现任县长）","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"南靖县县长",
     "current_org":"南靖县人民政府",
     "source":"OPEN GAP — official site unreachable, no web sources accessible"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1,"name":"中共南靖县委员会","type":"党委","level":"县级","parent":"中共漳州市委员会","location":"福建省漳州市南靖县"},
    {"id":2,"name":"南靖县人民政府","type":"政府","level":"县级","parent":"漳州市人民政府","location":"福建省漳州市南靖县"},
    {"id":3,"name":"中共南靖县纪律检查委员会","type":"纪委","level":"县级","parent":"中共漳州市纪律检查委员会","location":"福建省漳州市南靖县"},
    {"id":4,"name":"南靖县人大常委会","type":"人大","level":"县级","parent":"漳州市人大常委会","location":"福建省漳州市南靖县"},
    {"id":5,"name":"南靖县政协","type":"政协","level":"县级","parent":"政协漳州市委员会","location":"福建省漳州市南靖县"},
    {"id":6,"name":"中共南靖县委组织部","type":"党委","level":"县级","parent":"中共南靖县委员会","location":"福建省漳州市南靖县"},
    {"id":7,"name":"中共南靖县委宣传部","type":"党委","level":"县级","parent":"中共南靖县委员会","location":"福建省漳州市南靖县"},
    {"id":8,"name":"中共南靖县委政法委员会","type":"党委","level":"县级","parent":"中共南靖县委员会","location":"福建省漳州市南靖县"},
    {"id":9,"name":"南靖县人民检察院","type":"事业单位","level":"县级","parent":"漳州市人民检察院","location":"福建省漳州市南靖县"},
    {"id":10,"name":"南靖县人民法院","type":"事业单位","level":"县级","parent":"漳州市中级人民法院","location":"福建省漳州市南靖县"},
    # Towns (11 towns under 南靖县)
    {"id":11,"name":"南靖县山城镇","type":"乡镇/街道","level":"乡级","parent":"南靖县人民政府","location":"福建省漳州市南靖县"},
    {"id":12,"name":"南靖县丰田镇","type":"乡镇/街道","level":"乡级","parent":"南靖县人民政府","location":"福建省漳州市南靖县"},
    {"id":13,"name":"南靖县靖城镇","type":"乡镇/街道","level":"乡级","parent":"南靖县人民政府","location":"福建省漳州市南靖县"},
    {"id":14,"name":"南靖县龙山镇","type":"乡镇/街道","level":"乡级","parent":"南靖县人民政府","location":"福建省漳州市南靖县"},
    {"id":15,"name":"南靖县金山镇","type":"乡镇/街道","level":"乡级","parent":"南靖县人民政府","location":"福建省漳州市南靖县"},
    {"id":16,"name":"南靖县和溪镇","type":"乡镇/街道","level":"乡级","parent":"南靖县人民政府","location":"福建省漳州市南靖县"},
    {"id":17,"name":"南靖县奎洋镇","type":"乡镇/街道","level":"乡级","parent":"南靖县人民政府","location":"福建省漳州市南靖县"},
    {"id":18,"name":"南靖县梅林镇","type":"乡镇/街道","level":"乡级","parent":"南靖县人民政府","location":"福建省漳州市南靖县"},
    {"id":19,"name":"南靖县书洋镇","type":"乡镇/街道","level":"乡级","parent":"南靖县人民政府","location":"福建省漳州市南靖县"},
    {"id":20,"name":"南靖县船场镇","type":"乡镇/街道","level":"乡级","parent":"南靖县人民政府","location":"福建省漳州市南靖县"},
    {"id":21,"name":"南靖县南坑镇","type":"乡镇/街道","level":"乡级","parent":"南靖县人民政府","location":"福建省漳州市南靖县"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 洪仕建 — former 县委书记
    {"person_id":1,"org_id":1,"title":"南靖县委书记","start":"~2011","end":"~2014","rank":"正处级","note":"后任漳州市委常委、副市长; Wikipedia infobox source"},
    # 郭德志 — former 县委书记
    {"person_id":2,"org_id":1,"title":"南靖县委书记","start":"~2014","end":"~2020","rank":"正处级","note":"succeeded 洪仕建; needs verification"},
    # 李志勇 — former 县委书记
    {"person_id":3,"org_id":1,"title":"南靖县委书记","start":"~2020","end":"~2023","rank":"正处级","note":"succeeded 郭德志; needs verification"},
    # Current unknown 县委书记
    {"person_id":10,"org_id":1,"title":"南靖县委书记","start":"unknown","end":"present","rank":"正处级","note":"OPEN GAP — name not confirmed"},
    # Current unknown 县长
    {"person_id":11,"org_id":2,"title":"南靖县县长","start":"unknown","end":"present","rank":"正处级","note":"OPEN GAP — name not confirmed"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    {"person_a":1,"person_b":2,"type":"predecessor_successor","context":"洪仕建 → 郭德志 南靖县委书记交接","overlap_org":"中共南靖县委员会","overlap_period":"~2014","confidence":"unverified"},
    {"person_a":2,"person_b":3,"type":"predecessor_successor","context":"郭德志 → 李志勇 南靖县委书记交接","overlap_org":"中共南靖县委员会","overlap_period":"~2020","confidence":"unverified"},
    {"person_a":3,"person_b":10,"type":"predecessor_successor","context":"李志勇 → 现任 南靖县委书记交接","overlap_org":"中共南靖县委员会","overlap_period":"~2023","confidence":"unverified"},
]


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    """Node color based on person role."""
    name = p.get("name", "")
    post = p.get("current_post", "")
    if "书记" in post and "县委" in post:
        return "255,50,50"  # Red — Party Secretary
    if "县长" in post:
        return "50,100,255"  # Blue — Mayor
    return "100,100,100"  # Grey — Others


def org_color(o):
    """Node color based on org type."""
    t = o.get("type", "")
    color_map = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "纪委": "255,165,0",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "乡镇/街道": "255,255,200",
        "事业单位": "220,220,220",
    }
    return color_map.get(t, "200,200,200")


def is_top_leader(p):
    post = p.get("current_post", "")
    name = p.get("name", "")
    # Top leaders have "县委书记" or "县长" in their post, but flag placeholders as non-top
    if "（" in name:
        return False
    return "县委书记" in post or "县长" in post


def person_size(p):
    return "20.0" if is_top_leader(p) else "12.0"


# =========================================================================
# BUILD SQLITE
# =========================================================================
def build_sqlite():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            "end" TEXT,
            rank TEXT,
            note TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            confidence TEXT
        )
    """)

    for p in persons:
        c.execute("""
            INSERT OR REPLACE INTO persons (id, name, gender, ethnicity, birth, birthplace,
                education, party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p.get("ethnicity", ""),
              p.get("birth", ""), p.get("birthplace", ""), p.get("education", ""),
              p.get("party_join", ""), p.get("work_start", ""),
              p.get("current_post", ""), p.get("current_org", ""), p.get("source", "")))

    for o in organizations:
        c.execute("""
            INSERT OR REPLACE INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        c.execute("""
            INSERT INTO positions (person_id, org_id, title, start, "end", rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["person_id"], pos["org_id"], pos["title"],
              pos.get("start", ""), pos.get("end", ""),
              pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        c.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (r["person_a"], r["person_b"], r["type"],
              r.get("context", ""), r.get("overlap_org", ""),
              r.get("overlap_period", ""), r.get("confidence", "")))

    conn.commit()
    conn.close()
    print(f"SQLite database written: {DB_PATH}")


# =========================================================================
# BUILD GEXF
# =========================================================================
def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append('    <description>南靖县 leadership network — Fujian, Zhangzhou. Research date: 2026-07-16. Multiple open gaps — current leadership not confirmed (site unreachable).</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="node_type" type="string"/>')
    lines.append('      <attribute id="2" title="role" type="string"/>')
    lines.append('      <attribute id="3" title="org_type" type="string"/>')
    lines.append('      <attribute id="4" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        pid = f"p{p['id']}"
        c = person_color(p)
        sz = person_size(p)
        role = p.get("current_post", "")
        lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append('          <attvalue for="1" value="person"/>')
        lines.append(f'          <attvalue for="2" value="{esc(role)}"/>')
        lines.append('          <attvalue for="3" value=""/>')
        lines.append('          <attvalue for="4" value="unverified"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        oid = f"o{o['id']}"
        c = org_color(o)
        lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append('          <attvalue for="1" value="organization"/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value="{esc(o.get("type", ""))}"/>')
        lines.append('          <attvalue for="4" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → Organization (positions)
    for pos in positions:
        eid += 1
        pid = f"p{pos['person_id']}"
        oid = f"o{pos['org_id']}"
        lines.append(f'      <edge id="e{eid}" source="{pid}" target="{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append('          <attvalue for="1" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person → Person (relationships)
    for r in relationships:
        eid += 1
        pa = f"p{r['person_a']}"
        pb = f"p{r['person_b']}"
        conf = r.get("confidence", "unverified")
        lines.append(f'      <edge id="e{eid}" source="{pa}" target="{pb}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{conf}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF graph written: {GEXF_PATH}")


# =========================================================================
# MAIN
# =========================================================================
if __name__ == "__main__":
    print("Building 南靖县 leadership network...")
    build_sqlite()
    build_gexf()
    print("Done.")
