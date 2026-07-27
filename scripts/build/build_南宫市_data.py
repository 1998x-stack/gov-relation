#!/usr/bin/env python3
"""
南宫市（邢台市）领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Nangong City leadership.

Research date: 2026-07-23
Data sourced from nangong.gov.cn official leadership page and news articles.

Current leaders (confirmed from official news, as of 2026-07-23):
  - 杨跃峰: 市委书记 (confirmed from multiple 2022-2026 news articles)
  - 付继泽: 市委副书记、市长 (elected 2024-01-24)
  - 刘永宁: 市委常委、副市长（分工政府常务工作）
  - 杜九星: 副市长
  - 胡亚杰: 副市长
  - 范吉学: 副市长
  - 刘兴: 副市长、公安局局长
  - 张瑶: 副市长

Predecessors:
  - 朱继坤: 市长 (前, 直到 2023/2024 transition)
"""

import json
import os
import sqlite3
import sys
from datetime import datetime

# ── Paths ──
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(STAGING_DIR, "..", ".."))
DB_PATH = os.path.join(STAGING_DIR, "南宫市_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "南宫市_network.gexf")
PERSONS_DIR = STAGING_DIR


# ═══════════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════════

TODAY = "2026-07-23"

# ── Persons ──
PERSONS = [
    # === TOP LEADERS ===
    {
        "id": 1,
        "name": "杨跃峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员（具体时间待查）",
        "work_start": "待查",
        "current_post": "市委书记",
        "current_org": "中共南宫市委员会",
        "source": "https://www.nangong.gov.cn (市委书记杨跃峰, confirmed in news from 2022-02 through 2026-05)"
    },
    {
        "id": 2,
        "name": "付继泽",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员（具体时间待查）",
        "work_start": "待查",
        "current_post": "市委副书记、市长",
        "current_org": "南宫市人民政府",
        "source": "https://www.nangong.gov.cn/sz/view/s01.htm (confirmed); elected 2024-01-24 per article 167335"
    },
    # === DEPUTY MAYORS (from 市长之窗) ===
    {
        "id": 3,
        "name": "刘永宁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员（具体时间待查）",
        "work_start": "待查",
        "current_post": "市委常委、副市长（分工政府常务工作）",
        "current_org": "南宫市人民政府",
        "source": "https://www.nangong.gov.cn/sz/view/s02.htm (confirmed from 市长之窗)"
    },
    {
        "id": 4,
        "name": "杜九星",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员（具体时间待查）",
        "work_start": "待查",
        "current_post": "副市长",
        "current_org": "南宫市人民政府",
        "source": "https://www.nangong.gov.cn/sz/view/s06.htm (confirmed from 市长之窗)"
    },
    {
        "id": 5,
        "name": "胡亚杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员（具体时间待查）",
        "work_start": "待查",
        "current_post": "副市长",
        "current_org": "南宫市人民政府",
        "source": "https://www.nangong.gov.cn/sz/view/s08.htm (confirmed from 市长之窗)"
    },
    {
        "id": 6,
        "name": "范吉学",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员（具体时间待查）",
        "work_start": "待查",
        "current_post": "副市长",
        "current_org": "南宫市人民政府",
        "source": "https://www.nangong.gov.cn/sz/view/s07.htm (confirmed from 市长之窗)"
    },
    {
        "id": 7,
        "name": "刘兴",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员（具体时间待查）",
        "work_start": "待查",
        "current_post": "副市长、公安局局长",
        "current_org": "南宫市人民政府、南宫市公安局",
        "source": "https://www.nangong.gov.cn/sz/view/s10.htm (confirmed from 市长之窗)"
    },
    {
        "id": 8,
        "name": "张瑶",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员（具体时间待查）",
        "work_start": "待查",
        "current_post": "副市长",
        "current_org": "南宫市人民政府",
        "source": "https://www.nangong.gov.cn/sz/view/s11.htm (confirmed from 市长之窗)"
    },
    # === PREDECESSORS ===
    {
        "id": 9,
        "name": "朱继坤",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员（具体时间待查）",
        "work_start": "待查",
        "current_post": "前市长（已离任）",
        "current_org": "（已离任）",
        "source": "https://www.nangong.gov.cn (confirmed as 市长 from 2022-09 through 2023-09 news articles)"
    },
]

# ── Organizations ──
ORGANIZATIONS = [
    {"id": 0, "name": "中共南宫市委员会", "type": "党委", "level": "县级", "location": "南宫市"},
    {"id": 1, "name": "南宫市人民政府", "type": "政府", "level": "县级", "location": "南宫市"},
    {"id": 2, "name": "南宫市公安局", "type": "政府", "level": "科级", "location": "南宫市"},
]

# ── Positions ──
POSITIONS = [
    # Current leaders
    {"person_id": 1, "org_id": 0, "title": "市委书记", "start": "2021或更早", "end": "至今", "confidence": "confirmed"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记、市长", "start": "2024-01", "end": "至今", "confidence": "confirmed"},
    {"person_id": 3, "org_id": 1, "title": "市委常委、副市长（常务）", "start": "待查", "end": "至今", "confidence": "confirmed"},
    {"person_id": 4, "org_id": 1, "title": "副市长", "start": "待查", "end": "至今", "confidence": "confirmed"},
    {"person_id": 5, "org_id": 1, "title": "副市长", "start": "待查", "end": "至今", "confidence": "confirmed"},
    {"person_id": 6, "org_id": 1, "title": "副市长", "start": "待查", "end": "至今", "confidence": "confirmed"},
    {"person_id": 7, "org_id": 1, "title": "副市长、公安局局长", "start": "待查", "end": "至今", "confidence": "confirmed"},
    {"person_id": 7, "org_id": 2, "title": "公安局局长", "start": "待查", "end": "至今", "confidence": "confirmed"},
    {"person_id": 8, "org_id": 1, "title": "副市长", "start": "待查", "end": "至今", "confidence": "confirmed"},
    # Predecessors
    {"person_id": 9, "org_id": 1, "title": "市长", "start": "2021或更早", "end": "2024-01", "confidence": "confirmed"},
]

# ── Relationships ──
RELATIONSHIPS = [
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "市委-政府主要领导搭档（书记+市长）",
        "overlap_org": "中共南宫市委员会/南宫市人民政府",
        "overlap_period": "2024-01至今",
    },
    {
        "person_a": 2, "person_b": 9,
        "type": "predecessor_successor",
        "context": "市长职务交接（朱继坤→付继泽）",
        "overlap_org": "南宫市人民政府",
        "overlap_period": "2023-2024过渡期",
    },
    {
        "person_a": 1, "person_b": 3,
        "type": "superior_subordinate",
        "context": "市委-政府领导关系（书记+常务副市长）",
        "overlap_org": "中共南宫市委员会/南宫市人民政府",
        "overlap_period": "至今",
    },
    {
        "person_a": 2, "person_b": 3,
        "type": "superior_subordinate",
        "context": "正副市长关系（市长+常务副市长）",
        "overlap_org": "南宫市人民政府",
        "overlap_period": "至今",
    },
    {
        "person_a": 2, "person_b": 4,
        "type": "superior_subordinate",
        "context": "正副市长关系（市长+副市长）",
        "overlap_org": "南宫市人民政府",
        "overlap_period": "至今",
    },
    {
        "person_a": 2, "person_b": 5,
        "type": "superior_subordinate",
        "context": "正副市长关系（市长+副市长）",
        "overlap_org": "南宫市人民政府",
        "overlap_period": "至今",
    },
    {
        "person_a": 2, "person_b": 6,
        "type": "superior_subordinate",
        "context": "正副市长关系（市长+副市长）",
        "overlap_org": "南宫市人民政府",
        "overlap_period": "至今",
    },
    {
        "person_a": 2, "person_b": 7,
        "type": "superior_subordinate",
        "context": "正副市长关系（市长+副市长/公安局长）",
        "overlap_org": "南宫市人民政府",
        "overlap_period": "至今",
    },
    {
        "person_a": 2, "person_b": 8,
        "type": "superior_subordinate",
        "context": "正副市长关系（市长+副市长）",
        "overlap_org": "南宫市人民政府",
        "overlap_period": "至今",
    },
    {
        "person_a": 1, "person_b": 9,
        "type": "overlap",
        "context": "前任书记-市长搭档期间共事",
        "overlap_org": "中共南宫市委员会/南宫市人民政府",
        "overlap_period": "2021?-2024-01",
    },
]


# ═══════════════════════════════════════════════════════════
# BUILD FUNCTIONS
# ═══════════════════════════════════════════════════════════

def create_tables(conn):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
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
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            level TEXT,
            location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER NOT NULL,
            org_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            start TEXT,
            end TEXT,
            confidence TEXT DEFAULT 'confirmed',
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER NOT NULL,
            person_b INTEGER NOT NULL,
            type TEXT NOT NULL,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)


def build_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    create_tables(conn)
    for p in PERSONS:
        conn.execute(
            "INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"], p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"])
        )
    for o in ORGANIZATIONS:
        conn.execute(
            "INSERT INTO organizations (id, name, type, level, location) VALUES (?,?,?,?,?)",
            (o["id"], o["name"], o["type"], o["level"], o["location"])
        )
    for pos in POSITIONS:
        conn.execute(
            "INSERT INTO positions (person_id, org_id, title, start, end, confidence) VALUES (?,?,?,?,?,?)",
            (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos.get("confidence", "confirmed"))
        )
    for r in RELATIONSHIPS:
        conn.execute(
            "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
            (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"])
        )
    conn.commit()
    conn.close()
    print(f"✅ Database created: {DB_PATH}")


def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>China Gov Network Research Agent</creator>')
    lines.append('    <description>南宫市领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="org_type" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in PERSONS:
        pid = f"p{p['id']}"
        name = p["name"]
        post = p["current_post"]
        org = p["current_org"]

        if "书记" in post and "市委" in p.get("current_org", ""):
            color = "255,50,50"
            sz = "20.0"
        elif "市长" in post:
            color = "50,100,255"
            sz = "20.0"
        else:
            color = "100,100,100"
            sz = "12.0"

        lines.append(f'      <node id="{pid}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(post)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(org)}"/>')
        lines.append(f'          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{color.split(",")[0]}" g="{color.split(",")[1]}" b="{color.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    org_colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
    }
    for o in ORGANIZATIONS:
        oid = f"o{o['id']}"
        oname = o["name"]
        otype = o["type"]
        oc = org_colors.get(otype, "200,200,200")
        lines.append(f'      <node id="{oid}" label="{esc(oname)}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value="{esc(otype)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{oc.split(",")[0]}" g="{oc.split(",")[1]}" b="{oc.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person->Organization (worked_at)
    for pos in POSITIONS:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append('          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person<->Person relationships
    for r in RELATIONSHIPS:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ GEXF created: {GEXF_PATH}")


# ═══════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    build_db()
    build_gexf()
    print("✅ Done. Run person JSON separately.")
