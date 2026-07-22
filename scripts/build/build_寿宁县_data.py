#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 寿宁县 (Shouning County, Ningde, Fujian).

Task: fujian_寿宁县 — 县委书记 & 县长
Province: 福建省
City: 宁德市
Region: 寿宁县
Level: 县
Research date: 2026-07-17

Confirmed officeholders (as of 2026-07-17):
- 县委书记: 张永森 (confirmed from 今日寿宁 news article 2026-01-01 "县委书记张永森开展节前安全生产调研")
- 代县长: 林晓晞 (confirmed from 观八闽 article 2026-03-19 "福建省委组织部公示后，林晓晞任代县长（附简历）")

Sources:
- baike.baidu.com (寿宁县 overview)
- 今日寿宁 news article (2026-01-01, "县委书记张永森")
- 观八闽 news article (2026-03-19, "林晓晞任代县长")
- zh.wikipedia.org (寿宁县 background)
- Official government site www.fjndsn.gov.cn (unreachable from research environment)

Confidence: Current core leadership confirmed from Baidu Baike search result entries.
Career details are incomplete — government website was unreachable, so full career histories
and complete leadership roster are not yet available. Marked gaps explicitly.
"""

import json
import os
import sqlite3
from datetime import datetime

# ── paths ──────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GOV_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(SCRIPT_DIR))) \
    if "data/tmp" in SCRIPT_DIR else os.path.dirname(SCRIPT_DIR)
if "data/tmp" in SCRIPT_DIR:
    STAGING = SCRIPT_DIR
else:
    STAGING = os.path.join(GOV_ROOT, "data", "tmp", "fujian_寿宁县")
DB_PATH = os.path.join(STAGING, "寿宁县_network.db")
GEXF_PATH = os.path.join(STAGING, "寿宁县_network.gexf")

TODAY = datetime.now().strftime("%Y-%m-%d")


# ── research data ──────────────────────────────────────────────────────

persons = [
    # ══════════════ Core Leaders ══════════════

    # 县委书记 — 张永森
    {
        "id": "shouning_zhang_yongsen",
        "name": "张永森",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "寿宁县委书记",
        "current_org": "中共寿宁县委员会",
        "source": "今日寿宁 (2026-01-01 安全生产调研), 百度百科寿宁县词条",
        "notes": "2026年1月已任寿宁县委书记（见2026-01-01'县委书记张永森开展节前安全生产调研'报道）。"
             "履历（出生年月、籍贯、教育背景、此前职务）尚未查到公开详情。"
             "政府官网www.fjndsn.gov.cn在调研环境下无法访问。",
        "confidence": "confirmed",
    },

    # 代县长 — 林晓晞
    {
        "id": "shouning_lin_xiaoxi",
        "name": "林晓晞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "寿宁县委副书记、代县长",
        "current_org": "寿宁县人民政府",
        "source": "观八闽 (2026-03-19 任前公示), 百度百科寿宁县词条",
        "notes": "2026年3月19日，福建省委组织部公示后任寿宁县代县长（见'福建省委组织部公示后，林晓晞任代县长（附简历）'）。"
             "履历（出生年月、籍贯、教育背景、此前职务）尚未查到公开详情。"
             "政府官网www.fjndsn.gov.cn在调研环境下无法访问。",
        "confidence": "confirmed",
    },
]

organizations = [
    {"id": "cpc_shouning", "name": "中共寿宁县委员会", "type": "党委", "level": "县",
     "parent": "中共宁德市委员会", "location": "福建省宁德市寿宁县"},
    {"id": "gov_shouning", "name": "寿宁县人民政府", "type": "政府", "level": "县",
     "parent": "宁德市人民政府", "location": "福建省宁德市寿宁县"},
]

positions = [
    # 张永森
    {"person_id": "shouning_zhang_yongsen", "org_id": "cpc_shouning",
     "title": "寿宁县委书记", "start": "unknown", "end": "present",
     "rank": "正处级", "note": "2026年1月已任现职"},

    # 林晓晞
    {"person_id": "shouning_lin_xiaoxi", "org_id": "cpc_shouning",
     "title": "寿宁县委副书记", "start": "2026-03", "end": "present",
     "rank": "副处级", "note": ""},
    {"person_id": "shouning_lin_xiaoxi", "org_id": "gov_shouning",
     "title": "寿宁县代县长", "start": "2026-03", "end": "present",
     "rank": "正处级", "note": "县政府党组书记"},
]

relationships = [
    # 张永森 ↔ 林晓晞 (书记↔代县长，党政一把手搭档)
    {"person_a": "shouning_zhang_yongsen", "person_b": "shouning_lin_xiaoxi",
     "type": "superior_subordinate", "strength": "strong",
     "context": "党政一把手搭档，张永森主持县委全面工作，林晓晞主持县政府全面工作",
     "overlap_org": "中共寿宁县委员会/寿宁县人民政府",
     "overlap_period": "2026年3月起", "confidence": "confirmed"},
]


# ── BUILD ────────────────────────────────────────────────────────────

def build():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("PRAGMA foreign_keys = ON;")

    c.execute("""
        CREATE TABLE IF NOT EXISTS persons (
            id TEXT PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT,
            birth TEXT, birthplace TEXT, native_place TEXT,
            education TEXT,
            party_join TEXT, work_start TEXT,
            current_post TEXT, current_org TEXT,
            source TEXT,
            notes TEXT, confidence TEXT
        );
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id TEXT PRIMARY KEY,
            name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        );
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT, org_id TEXT,
            title TEXT, start TEXT, end TEXT,
            rank TEXT, note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT, person_b TEXT,
            type TEXT, context TEXT,
            overlap_org TEXT, overlap_period TEXT,
            strength TEXT, confidence TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, native_place,
             education, party_join, work_start,
             current_post, current_org, source,
             notes, confidence)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"],
             p["birth"], p.get("birthplace", ""), p.get("native_place", ""),
             p.get("education", ""), p["party_join"], p.get("work_start", ""),
             p["current_post"], p["current_org"], p["source"],
             p.get("notes", ""), p["confidence"]))

    for o in organizations:
        c.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"],
             o["parent"], o["location"]))

    for pos in positions:
        c.execute("""INSERT INTO positions
            (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos["start"], pos["end"], pos["rank"], pos["note"]))

    for rel in relationships:
        c.execute("""INSERT INTO relationships
            (person_a, person_b, type, context, overlap_org, overlap_period,
             strength, confidence)
            VALUES (?,?,?,?,?,?,?,?)""",
            (rel["person_a"], rel["person_b"], rel["type"],
             rel["context"], rel["overlap_org"], rel["overlap_period"],
             rel["strength"], rel["confidence"]))

    conn.commit()
    conn.close()
    print(f"[DB] Wrote {DB_PATH}")


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    current = p.get("current_post", "")
    if "县委书记" in current:
        return "255,50,50"
    if "县长" in current or "副县长" in current or "常务副" in current:
        return "50,100,255"
    if "纪委书记" in current or "监委" in current:
        return "255,165,0"
    return "100,100,100"


def is_top_leader(p):
    current = p.get("current_post", "")
    return "县委书记" in current or "县长" in current


def org_color(o):
    t = o.get("type", "")
    if "党委" in t:
        return "255,200,200"
    if "政府" in t:
        return "200,200,255"
    if "人大" in t:
        return "200,255,255"
    if "政协" in t:
        return "255,240,200"
    if "乡镇" in t:
        return "255,255,200"
    if "事业单位" in t:
        return "220,220,220"
    return "200,200,200"


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append('    <description>寿宁县领导班子工作关系网络 — 中共寿宁县委员会、寿宁县人民政府</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="org_type" type="string"/>')
    lines.append('      <attribute id="2" title="birth" type="string"/>')
    lines.append('      <attribute id="3" title="title" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="strength" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="{esc(p["id"])}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("current_post",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="{esc(o["id"])}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 1
    for pos in positions:
        lines.append(f'      <edge id="e{eid}" source="{esc(pos["person_id"])}" target="{esc(pos["org_id"])}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    for rel in relationships:
        w = "2.0" if rel.get("strength") == "strong" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="{esc(rel["person_a"])}" target="{esc(rel["person_b"])}" label="{esc(rel["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(rel.get("context",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(rel.get("strength",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[GEXF] Wrote {GEXF_PATH}")


if __name__ == "__main__":
    build()
    build_gexf()

    # Summary
    print(f"\nSummary:")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
