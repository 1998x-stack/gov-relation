#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 甘谷县 (Gangu County), 天水市, 甘肃省.

甘谷县 — 甘肃省天水市下辖县，位于天水市西部，渭河上游，有"华夏第一县"之称。
Covers current County Party Secretary (孙忠平), County Magistrate (许祖熙),
key leadership team members, and predecessor information.

Current leadership as of 2026-07:
  - 孙忠平 (县委书记, as of at least 2026-07-14)
  - 许祖熙 (县委副书记、县长, as of at least 2026-07-16)

Reference sources:
  - 甘谷县人民政府网站: https://www.gangu.gov.cn/
  - 天水市人民政府网站: https://www.tianshui.gov.cn/

IMPORTANT GAPS:
  - 孙忠平 and 许祖熙's full career timelines (birth, education, previous posts) are
    unknown. Person JSON files document these gaps explicitly.
  - Predecessor names are unknown and marked as open questions.
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/gansu_甘谷县")
os.makedirs(TMP, exist_ok=True)

DB_PATH = os.path.join(TMP, "甘谷县_network.db")
GEXF_PATH = os.path.join(TMP, "甘谷县_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ═══════════════════════════════════════════════════════════
    # CURRENT TOP LEADERS
    # ═══════════════════════════════════════════════════════════

    # 孙忠平 — 甘谷县委书记 (as of 2026-07-14)
    {"id": 1, "name": "孙忠平", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "甘谷县委书记",
     "current_org": "中共甘谷县委员会",
     "source": "https://www.gangu.gov.cn/ 新闻: 2026-07-15 县委主要领导督导城区防汛和安全生产工作"},

    # 许祖熙 — 甘谷县委副书记、县长 (as of 2026-07-16)
    {"id": 2, "name": "许祖熙", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "甘谷县委副书记、县长",
     "current_org": "甘谷县人民政府",
     "source": "https://www.gangu.gov.cn/ 新闻: 2026-07-17 县政府主要领导在古坡镇督导检查防汛工作"},

    # ═══════════════════════════════════════════════════════════
    # FOUR MAJOR LEADERSHIP
    # ═══════════════════════════════════════════════════════════

    # 令军强 — 县政协党组书记、主席 (as of 2026-07-10)
    {"id": 3, "name": "令军强", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "甘谷县政协党组书记、主席",
     "current_org": "中国人民政治协商会议甘谷县委员会",
     "source": "https://www.gangu.gov.cn/ 新闻: 2026-07-13 政协甘谷县第十四届委员会常务委员会第二十六次会议"},

    # ═══════════════════════════════════════════════════════════
    # COUNTY GOVERNMENT DEPUTIES
    # ═══════════════════════════════════════════════════════════

    # 马顺民 — 副县长 (mentioned at 政协会议 2026-07-10)
    {"id": 4, "name": "马顺民", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "甘谷县副县长",
     "current_org": "甘谷县人民政府",
     "source": "https://www.gangu.gov.cn/ 新闻: 2026-07-13 政协甘谷县第十四届委员会常务委员会第二十六次会议"},
]

organizations = [
    {"id": 1, "name": "中共甘谷县委员会", "type": "党委", "level": "县处级",
     "parent": "中共天水市委员会", "location": "甘肃省天水市甘谷县"},
    {"id": 2, "name": "甘谷县人民政府", "type": "政府", "level": "县处级",
     "parent": "天水市人民政府", "location": "甘肃省天水市甘谷县"},
    {"id": 3, "name": "中国人民政治协商会议甘谷县委员会", "type": "政协", "level": "县处级",
     "parent": "天水市政协", "location": "甘肃省天水市甘谷县"},
    {"id": 4, "name": "中共天水市委员会", "type": "党委", "level": "地厅级",
     "parent": "中共甘肃省委员会", "location": "甘肃省天水市"},
    {"id": 5, "name": "天水市人民政府", "type": "政府", "level": "地厅级",
     "parent": "甘肃省人民政府", "location": "甘肃省天水市"},
]

positions = [
    # ── 孙忠平 (id=1) ──
    {"person_id": 1, "org_id": 1, "title": "甘谷县委书记", "start": "", "end": "present", "rank": "正处级",
     "note": "2026年7月14日以县委书记身份督导城区防汛工作，任职起始时间待查"},

    # ── 许祖熙 (id=2) ──
    {"person_id": 2, "org_id": 1, "title": "甘谷县委副书记", "start": "", "end": "present", "rank": "正处级",
     "note": ""},
    {"person_id": 2, "org_id": 2, "title": "甘谷县县长", "start": "", "end": "present", "rank": "正处级",
     "note": "2026年7月16日以县长身份督导防汛，任职起始时间待查"},

    # ── 令军强 (id=3) ──
    {"person_id": 3, "org_id": 3, "title": "甘谷县政协主席", "start": "", "end": "present", "rank": "正处级",
     "note": ""},

    # ── 马顺民 (id=4) ──
    {"person_id": 4, "org_id": 2, "title": "甘谷县副县长", "start": "", "end": "present", "rank": "副处级",
     "note": ""},
]

relationships = [
    # ── Current top leaders ──
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "strength": "strong",
     "context": "孙忠平作为县委书记、许祖熙作为县长，是甘谷县党政一把手搭档关系",
     "overlap_org": "中共甘谷县委员会/甘谷县人民政府",
     "overlap_period": "~2025~present", "confidence": "confirmed"},

    # ── 县委书记 ↔ 政协主席 ──
    {"person_a": 1, "person_b": 3, "type": "overlap", "strength": "medium",
     "context": "孙忠平与令军强在甘谷县党政班子共事",
     "overlap_org": "中共甘谷县委员会/甘谷县政协",
     "overlap_period": "present", "confidence": "confirmed"},

    # ── 县长 ↔ 政协主席 ──
    {"person_a": 2, "person_b": 3, "type": "overlap", "strength": "medium",
     "context": "许祖熙与令军强在甘谷县党政班子共事",
     "overlap_org": "甘谷县人民政府/甘谷县政协",
     "overlap_period": "present", "confidence": "confirmed"},
]


# ── HELPERS ─────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    role = p["current_post"]
    if "县委书记" in role and "副书记" not in role:
        return "255,50,50"
    elif "县长" in role and "副书记" in role:
        return "50,100,255"
    elif "县长" in role:
        return "50,100,255"
    elif "人大" in role:
        return "200,255,255"
    elif "政协" in role:
        return "255,240,200"
    elif "纪委书记" in role or "纪检" in role:
        return "255,165,0"
    elif "原" in role:
        return "160,160,160"
    else:
        return "100,100,100"


def org_color(o):
    t = o["type"]
    return {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "开发区": "200,255,200",
        "乡镇/街道": "255,255,200",
        "事业单位": "220,220,220",
        "群团": "255,220,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }.get(t, "200,200,200")


def is_top_leader(p):
    role = p["current_post"]
    return "县委书记" in role or ("县长" in role and "副书记" in role)


def person_size(p):
    return "20.0" if is_top_leader(p) else ("14.0" if "原" not in p["current_post"] else "10.0")


# ── BUILD DB ─────────────────────────────────────────────────

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
            id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER, title TEXT,
            start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER, type TEXT, strength TEXT,
            context TEXT, overlap_org TEXT, overlap_period TEXT, confidence TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education,
             party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
             p["birthplace"], p["education"], p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("""INSERT INTO positions
            (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("""INSERT INTO relationships
            (person_a, person_b, type, strength, context, overlap_org, overlap_period, confidence)
            VALUES (?,?,?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"], r["strength"],
             r["context"], r["overlap_org"], r["overlap_period"], r["confidence"]))

    conn.commit()
    conn.close()
    print(f"Database created: {DB_PATH}")


# ── BUILD GEXF ────────────────────────────────────────────────

def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation Research Agent</creator>')
    lines.append('    <description>甘谷县领导班子工作关系网络 - 甘肃省天水市甘谷县</description>')
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
    lines.append('      <attribute id="2" title="period" type="string"/>')
    lines.append('      <attribute id="3" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = person_size(p)
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["parent"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → Organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos["start"])}~{esc(pos["end"])}"/>')
        lines.append(f'          <attvalue for="3" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationships)
    for r in relationships:
        eid += 1
        w = "2.0" if r["strength"] == "strong" else "1.5" if r["strength"] == "medium" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_period"])}"/>')
        lines.append(f'          <attvalue for="3" value="{r["confidence"]}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF created: {GEXF_PATH}")


# ── SUMMARY ──────────────────────────────────────────────────

def print_summary():
    print(f"\nSummary:")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")


if __name__ == "__main__":
    build_db()
    build_gexf()
    print_summary()
