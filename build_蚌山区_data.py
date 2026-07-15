#!/usr/bin/env python3
"""Build 蚌山区 (Bengshan District, Bengbu, Anhui) leadership network data: SQLite DB + GEXF graph.

Research date: 2026-07-15
Task: anhui_蚌山区
Province: 安徽省
City: 蚌埠市
Region: 蚌山区
Level: 市辖区

Current leaders (confirmed from official Bengshan district government news, July 2026):
  - 区委书记: 王志 (confirmed 2026-06-23 from 5th Party Congress report)
  - 区委副书记/区长: 张圣辉 (confirmed 2026-07-14 from fire safety meeting)
  - 区委副书记: 潘成佳 (confirmed from "两优一先" meeting 2026-07-02)

Sources:
  - https://www.bengshan.gov.cn/ (official district government website)
  - Multiple news articles accessed 2026-07-15

Confidence:
  - Current roles: confirmed from multiple official Bengshan government news articles (July 2026)
  - Biographical details: partial — Baidu Baike blocked by geo-restrictions
"""

import json
import os
import sqlite3
from datetime import datetime

# ── paths ────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# When deployed to repo root, paths change; for tmp staging we write locally
IS_STAGING = "data/tmp" in SCRIPT_DIR

if IS_STAGING:
    DB_PATH = os.path.join(SCRIPT_DIR, "蚌山区_network.db")
    GEXF_PATH = os.path.join(SCRIPT_DIR, "蚌山区_network.gexf")
else:
    BASE = os.path.dirname(SCRIPT_DIR)  # repo root
    DB_PATH = os.path.join(BASE, "data/database/蚌山区_network.db")
    GEXF_PATH = os.path.join(BASE, "data/graph/蚌山区_network.gexf")

TODAY = datetime.now().strftime("%Y-%m-%d")

# ── research data ────────────────────────────────────────────────────────

persons = [
    {
        "id": 1,
        "name": "王志",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "蚌山区委书记",
        "current_org": "中共蚌埠市蚌山区委员会",
        "source": "https://www.bengshan.gov.cn/ywdt/bsyw/5094269.html"
    },
    {
        "id": 2,
        "name": "张圣辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "蚌山区委副书记、区长",
        "current_org": "蚌埠市蚌山区人民政府",
        "source": "https://www.bengshan.gov.cn/ywdt/bsyw/5095001.html"
    },
    {
        "id": 3,
        "name": "潘成佳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "蚌山区委副书记",
        "current_org": "中共蚌埠市蚌山区委员会",
        "source": "https://www.bengshan.gov.cn/ywdt/bsyw/5094597.html"
    },
    {
        "id": 4,
        "name": "闫小京",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "蚌山区领导（常委/副区长级）",
        "current_org": "蚌埠市蚌山区",
        "source": "https://www.bengshan.gov.cn/ywdt/bsyw/5095001.html"
    },
    {
        "id": 5,
        "name": "陈光华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "蚌山区领导（常委/副区长级）",
        "current_org": "蚌埠市蚌山区",
        "source": "https://www.bengshan.gov.cn/ywdt/bsyw/5093891.html"
    },
    {
        "id": 6,
        "name": "潘俞伊",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "蚌山区领导（常委/副区长级）",
        "current_org": "蚌埠市蚌山区",
        "source": "https://www.bengshan.gov.cn/ywdt/bsyw/5094630.html"
    },
    {
        "id": 7,
        "name": "邵兵",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "蚌山区领导（常委/副区长级）",
        "current_org": "蚌埠市蚌山区",
        "source": "https://www.bengshan.gov.cn/ywdt/bsyw/5094630.html"
    },
    {
        "id": 8,
        "name": "单桂云",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "蚌山区领导（常委/副区长级）",
        "current_org": "蚌埠市蚌山区",
        "source": "https://www.bengshan.gov.cn/ywdt/bsyw/5095001.html"
    },
    {
        "id": 9,
        "name": "谢庆元",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "蚌山区领导",
        "current_org": "蚌埠市蚌山区",
        "source": "https://www.bengshan.gov.cn/ywdt/bsyw/5095001.html"
    }
]

organizations = [
    {
        "id": 1,
        "name": "中共蚌埠市蚌山区委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共蚌埠市委",
        "location": "蚌埠市蚌山区"
    },
    {
        "id": 2,
        "name": "蚌埠市蚌山区人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "蚌埠市人民政府",
        "location": "蚌埠市蚌山区"
    },
    {
        "id": 3,
        "name": "蚌埠市蚌山区",
        "type": "行政区域",
        "level": "县级",
        "parent": "蚌埠市",
        "location": "蚌埠市"
    }
]

positions = [
    # 王志 - 区委书记
    {"id": 1, "person_id": 1, "org_id": 1, "title": "蚌山区委书记",
     "start": "未知", "end": "present", "rank": "正处级",
     "note": "以区委书记身份作区第五次党代会报告 (2026-06-23)"},
    # 张圣辉 - 区长
    {"id": 2, "person_id": 2, "org_id": 2, "title": "蚌山区委副书记、区长",
     "start": "未知", "end": "present", "rank": "正处级",
     "note": "以区委副书记、区长身份主持消防专项整治会 (2026-07-14)"},
    {"id": 3, "person_id": 2, "org_id": 1, "title": "蚌山区委副书记",
     "start": "未知", "end": "present", "rank": "正处级",
     "note": "区委副书记兼区长"},
    # 潘成佳 - 区委副书记
    {"id": 4, "person_id": 3, "org_id": 1, "title": "蚌山区委副书记",
     "start": "未知", "end": "present", "rank": "副处级/正处级",
     "note": "主持'两优一先'表彰大会 (2026-07-02)"},
    # 其他领导 (区域领导身份)
    {"id": 5, "person_id": 4, "org_id": 3, "title": "区领导",
     "start": "未知", "end": "present", "rank": "",
     "note": "出席区消防专项整治会 (2026-07-14)及多次会议"},
    {"id": 6, "person_id": 5, "org_id": 3, "title": "区领导",
     "start": "未知", "end": "present", "rank": "",
     "note": "出席全区安全生产会 (2026-06-06)"},
    {"id": 7, "person_id": 6, "org_id": 3, "title": "区领导",
     "start": "未知", "end": "present", "rank": "",
     "note": "出席二季度安委会 (2026-07-03)及台风防范会 (2026-07-12)"},
    {"id": 8, "person_id": 7, "org_id": 3, "title": "区领导",
     "start": "未知", "end": "present", "rank": "",
     "note": "出席二季度安委会 (2026-07-03)"},
    {"id": 9, "person_id": 8, "org_id": 3, "title": "区领导",
     "start": "未知", "end": "present", "rank": "",
     "note": "出席消防专项整治会 (2026-07-14)及台风防范会 (2026-07-12)"},
    {"id": 10, "person_id": 9, "org_id": 3, "title": "区领导",
     "start": "未知", "end": "present", "rank": "",
     "note": "出席消防专项整治会 (2026-07-14)"}
]

relationships = [
    {
        "id": 1,
        "person_a": 1, "person_b": 2,
        "type": "overlap",
        "context": "王志（区委书记）与张圣辉（区长）为蚌山区党政搭档",
        "overlap_org": "蚌山区",
        "overlap_period": "2026"
    },
    {
        "id": 2,
        "person_a": 1, "person_b": 3,
        "type": "overlap",
        "context": "王志（区委书记）与潘成佳（区委副书记）同为蚌山区委领导班子成员",
        "overlap_org": "中共蚌埠市蚌山区委员会",
        "overlap_period": "2026"
    },
    {
        "id": 3,
        "person_a": 2, "person_b": 3,
        "type": "overlap",
        "context": "张圣辉（区委副书记/区长）与潘成佳（专职副书记）同为蚌山区委副书记",
        "overlap_org": "中共蚌埠市蚌山区委员会",
        "overlap_period": "2026"
    },
    {
        "id": 4,
        "person_a": 2, "person_b": 4,
        "type": "overlap",
        "context": "张圣辉（区长）与闫小京（区领导）同届在蚌山区工作",
        "overlap_org": "蚌山区",
        "overlap_period": "2026"
    },
    {
        "id": 5,
        "person_a": 1, "person_b": 4,
        "type": "overlap",
        "context": "王志（区委书记）与闫小京同届在蚌山区工作",
        "overlap_org": "蚌山区",
        "overlap_period": "2026"
    },
    {
        "id": 6,
        "person_a": 2, "person_b": 6,
        "type": "overlap",
        "context": "张圣辉（区长）与潘俞伊（区领导）共同出席安委会和台风防范会议",
        "overlap_org": "蚌山区人民政府",
        "overlap_period": "2026-07"
    },
    {
        "id": 7,
        "person_a": 2, "person_b": 8,
        "type": "overlap",
        "context": "张圣辉（区长）与单桂云（区领导）共同出席消防专项整治会和安委会",
        "overlap_org": "蚌山区人民政府",
        "overlap_period": "2026-07"
    }
]

# ── helpers ──────────────────────────────────────────────────────────────

def is_top_leader(p):
    """Return True for the party secretary (top leader)."""
    return "书记" in p["current_post"] and "副书记" not in p["current_post"]


def person_color(p):
    """Return 'r,g,b' string for a person node."""
    post = p.get("current_post", "")
    if "书记" in post and "副书记" not in post:
        return "255,50,50"      # Red — Party Secretary
    if "区长" in post or "市长" in post:
        return "50,100,255"     # Blue — Mayor/区长
    if "副书记" in post:
        return "200,50,200"     # Purple — Deputy Secretary
    return "100,100,100"        # Grey — Others


def org_color(o):
    """Return 'r,g,b' string for an org node."""
    t = o.get("type", "")
    if t == "党委":
        return "255,200,200"
    if t == "政府":
        return "200,200,255"
    if t == "行政区域":
        return "200,255,200"
    return "200,200,200"


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# ── BUILD SQLite ────────────────────────────────────────────────────────

def build_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY,
            person_id INTEGER, org_id INTEGER, title TEXT,
            start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY,
            person_a INTEGER, person_b INTEGER, type TEXT,
            context TEXT, overlap_org TEXT, overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                   p["birthplace"], p["education"], p["party_join"],
                   p["work_start"], p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("INSERT OR REPLACE INTO positions VALUES (?,?,?,?,?,?,?,?)",
                  (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
                   pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("INSERT OR REPLACE INTO relationships VALUES (?,?,?,?,?,?,?)",
                  (r["id"], r["person_a"], r["person_b"], r["type"],
                   r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"✅ SQLite DB written: {DB_PATH}")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")


# ── BUILD GEXF ──────────────────────────────────────────────────────────

def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>蚌山区（安徽省蚌埠市）领导关系网络 — 区委书记、区长及领导班子</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # ── Nodes ──
    lines.append('    <nodes>')

    # Person nodes
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else ("16.0" if "区长" in p["current_post"] else ("14.0" if "副书记" in p["current_post"] else "12.0"))
        role = p.get("current_post", "")
        org = p.get("current_org", "")
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(role)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(org)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # ── Edges ──
    lines.append('    <edges>')

    eid = 0

    # Person → Org (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationships)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"✅ GEXF graph written: {GEXF_PATH}")


# ── MAIN ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("  蚌山区（Bengshan District）领导关系网络数据库构建")
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    build_db()
    build_gexf()
    print("\n[DONE] Build complete.")
