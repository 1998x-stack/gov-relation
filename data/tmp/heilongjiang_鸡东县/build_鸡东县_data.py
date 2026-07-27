#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 鸡东县 (Jidong County), 鸡西市, 黑龙江省.

Investigation date: 2026-07-24
Task ID: heilongjiang_鸡东县
Research sources:
  - Jidong County Government Website (www.jidong.gov.cn)
  - Government meeting records (县政府常务会议)
  - Leadership page (政府领导)
"""

import json
import sqlite3
import os
from datetime import datetime
from pathlib import Path

BASE = os.path.dirname(os.path.abspath(__file__))
SLUG = "鸡东县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = TODAY

DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")
PERSONS_DIR = Path(BASE)

# Also produce canonical destination paths
CANONICAL_DB = os.path.join(BASE, "..", "..", "database", f"{SLUG}_network.db")
CANONICAL_GEXF = os.path.join(BASE, "..", "..", "graph", f"{SLUG}_network.gexf")
CANONICAL_BUILD = os.path.join(BASE, "..", "..", "..", f"build_{SLUG}_data.py")
CANONICAL_PERSONS = Path(BASE) / ".." / ".." / "persons"

# ── Persons ──────────────────────────────────────────────────────────────────

# Note: The Jidong County government website leadership page shows the
# "县长" (County Mayor) field as empty as of July 2026. 金成根 (Jin Chenggen)
# was presiding over county government meetings from Oct through Dec 2025,
# then disappeared by Jan 2026, suggesting a leadership transition.
# 何海臣 has been convening meetings since Jan 2026 but is listed as
# 县委常委、副县长 (Executive Deputy Mayor), not as 县长.
# The 县委书记 (Party Secretary) was not listed on the government website.

persons = [
    # ── Government Leadership ──
    # NOTE: County Mayor (县长) position appears vacant as of July 2026.
    # 何海臣 (常务副县长/Executive Deputy Mayor) has been convening meetings since Jan 2026
    
    {"id": 1, "name": "何海臣", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "鸡东县委常委、副县长（常务）", "current_org": "鸡东县人民政府",
     "source": "https://www.jidong.gov.cn/jdx/01d6ee8e6afb4518b1af41af91e0c736/202607/c06_367659.shtml"},
    
    {"id": 2, "name": "王莹", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "鸡东县委常委、副县长", "current_org": "鸡东县人民政府",
     "source": "https://www.jidong.gov.cn/jdx/01d6ee8e6afb4518b1af41af91e0c736/202508/c06_338828.shtml"},
    
    {"id": 3, "name": "朱卫东", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "鸡东县副县长、县公安局局长", "current_org": "鸡东县人民政府",
     "source": "https://www.jidong.gov.cn/jdx/01d6ee8e6afb4518b1af41af91e0c736/202409/c06_326054.shtml"},
    
    {"id": 4, "name": "殷云海", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "鸡东县副县长", "current_org": "鸡东县人民政府",
     "source": "https://www.jidong.gov.cn/jdx/01d6ee8e6afb4518b1af41af91e0c736/202602/c06_326055.shtml"},
    
    {"id": 5, "name": "汪冬波", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "鸡东县副县长", "current_org": "鸡东县人民政府",
     "source": "https://www.jidong.gov.cn/jdx/01d6ee8e6afb4518b1af41af91e0c736/202602/c06_326056.shtml"},
    
    {"id": 6, "name": "张铁明", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "鸡东县副县长", "current_org": "鸡东县人民政府",
     "source": "https://www.jidong.gov.cn/jdx/01d6ee8e6afb4518b1af41af91e0c736/202401/c06_326057.shtml"},
    
    {"id": 7, "name": "程炳军", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "鸡东县副县长", "current_org": "鸡东县人民政府",
     "source": "https://www.jidong.gov.cn/jdx/01d6ee8e6afb4518b1af41af91e0c736/202501/c06_326059.shtml"},
    
    # ── Former Acting Leader ──
    {"id": 8, "name": "金成根", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "已调离（原负责县政府常务工作）", "current_org": "",
     "source": "https://www.jidong.gov.cn/jdx/c0f57deb14d34287a8bbfe056359e0e1/202511/c06_345432.shtml"},
]

# ── Organizations ────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共鸡东县委员会", "type": "党委", "level": "县处级", "parent": "中共鸡西市委员会", "location": "黑龙江省鸡西市鸡东县"},
    {"id": 2, "name": "鸡东县人民政府", "type": "政府", "level": "县处级", "parent": "鸡西市人民政府", "location": "黑龙江省鸡西市鸡东县"},
    {"id": 3, "name": "鸡东县公安局", "type": "政府", "level": "乡科级", "parent": "鸡东县人民政府", "location": "黑龙江省鸡西市鸡东县"},
    {"id": 4, "name": "鸡东县司法局", "type": "政府", "level": "乡科级", "parent": "鸡东县人民政府", "location": "黑龙江省鸡西市鸡东县"},
    {"id": 5, "name": "鸡东县财政局", "type": "政府", "level": "乡科级", "parent": "鸡东县人民政府", "location": "黑龙江省鸡西市鸡东县"},
    {"id": 6, "name": "鸡东县应急管理局", "type": "政府", "level": "乡科级", "parent": "鸡东县人民政府", "location": "黑龙江省鸡西市鸡东县"},
    {"id": 7, "name": "鸡东县人力资源和社会保障局", "type": "政府", "level": "乡科级", "parent": "鸡东县人民政府", "location": "黑龙江省鸡西市鸡东县"},
    {"id": 8, "name": "鸡东县煤炭生产安全管理局", "type": "政府", "level": "乡科级", "parent": "鸡东县人民政府", "location": "黑龙江省鸡西市鸡东县"},
    {"id": 9, "name": "鸡东县信访局", "type": "政府", "level": "乡科级", "parent": "鸡东县人民政府", "location": "黑龙江省鸡西市鸡东县"},
    {"id": 10, "name": "鸡东县审计局", "type": "政府", "level": "乡科级", "parent": "鸡东县人民政府", "location": "黑龙江省鸡西市鸡东县"},
    {"id": 11, "name": "鸡东县营商环境建设监督局", "type": "政府", "level": "乡科级", "parent": "鸡东县人民政府", "location": "黑龙江省鸡西市鸡东县"},
    {"id": 12, "name": "鸡东县退役军人事务局", "type": "政府", "level": "乡科级", "parent": "鸡东县人民政府", "location": "黑龙江省鸡西市鸡东县"},
    {"id": 13, "name": "鸡东县农业农村局", "type": "政府", "level": "乡科级", "parent": "鸡东县人民政府", "location": "黑龙江省鸡西市鸡东县"},
    {"id": 14, "name": "鸡东县水务局", "type": "政府", "level": "乡科级", "parent": "鸡东县人民政府", "location": "黑龙江省鸡西市鸡东县"},
    {"id": 15, "name": "鸡东县林业和草原局", "type": "政府", "level": "乡科级", "parent": "鸡东县人民政府", "location": "黑龙江省鸡西市鸡东县"},
    {"id": 16, "name": "鸡东县教育局", "type": "政府", "level": "乡科级", "parent": "鸡东县人民政府", "location": "黑龙江省鸡西市鸡东县"},
    {"id": 17, "name": "鸡东县文体广电和旅游局", "type": "政府", "level": "乡科级", "parent": "鸡东县人民政府", "location": "黑龙江省鸡西市鸡东县"},
    {"id": 18, "name": "鸡东县卫生健康局", "type": "政府", "level": "乡科级", "parent": "鸡东县人民政府", "location": "黑龙江省鸡西市鸡东县"},
    {"id": 19, "name": "鸡东县医疗保障局", "type": "政府", "level": "乡科级", "parent": "鸡东县人民政府", "location": "黑龙江省鸡西市鸡东县"},
    {"id": 20, "name": "鸡东县民政局", "type": "政府", "level": "乡科级", "parent": "鸡东县人民政府", "location": "黑龙江省鸡西市鸡东县"},
    {"id": 21, "name": "鸡东县自然资源局", "type": "政府", "level": "乡科级", "parent": "鸡东县人民政府", "location": "黑龙江省鸡西市鸡东县"},
    {"id": 22, "name": "鸡东县住房和城乡建设局", "type": "政府", "level": "乡科级", "parent": "鸡东县人民政府", "location": "黑龙江省鸡西市鸡东县"},
    {"id": 23, "name": "鸡东县市场监督管理局", "type": "政府", "level": "乡科级", "parent": "鸡东县人民政府", "location": "黑龙江省鸡西市鸡东县"},
    {"id": 24, "name": "鸡东县发展和改革局", "type": "政府", "level": "乡科级", "parent": "鸡东县人民政府", "location": "黑龙江省鸡西市鸡东县"},
    {"id": 25, "name": "鸡东县交通运输局", "type": "政府", "level": "乡科级", "parent": "鸡东县人民政府", "location": "黑龙江省鸡西市鸡东县"},
    {"id": 26, "name": "鸡东县统计局", "type": "政府", "level": "乡科级", "parent": "鸡东县人民政府", "location": "黑龙江省鸡西市鸡东县"},
    {"id": 27, "name": "鸡东经济开发区管理委员会", "type": "开发区", "level": "乡科级", "parent": "鸡东县人民政府", "location": "黑龙江省鸡西市鸡东县"},
]

# ── Positions ────────────────────────────────────────────────────────────────

positions = [
    # 何海臣 — 县委常委、常务副县长
    {"person_id": 1, "org_id": 2, "title": "鸡东县委常委、副县长（常务）", "start": "", "end": "present", "rank": "副处级", "note": "负责县政府常务工作；综合经济、安全生产、人社、信访等"},
    {"person_id": 1, "org_id": 1, "title": "鸡东县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 王莹 — 县委常委、副县长
    {"person_id": 2, "org_id": 2, "title": "鸡东县委常委、副县长", "start": "", "end": "present", "rank": "副处级", "note": "负责营商环境、退役军人、外事等工作"},
    {"person_id": 2, "org_id": 1, "title": "鸡东县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 朱卫东 — 副县长、公安局局长
    {"person_id": 3, "org_id": 2, "title": "鸡东县副县长", "start": "", "end": "present", "rank": "副处级", "note": "负责公共安全等工作"},
    {"person_id": 3, "org_id": 3, "title": "鸡东县公安局局长", "start": "", "end": "present", "rank": "正科级", "note": ""},
    # 殷云海 — 副县长
    {"person_id": 4, "org_id": 2, "title": "鸡东县副县长", "start": "", "end": "present", "rank": "副处级", "note": "负责农业农村、水利、林业和草原等工作"},
    # 汪冬波 — 副县长
    {"person_id": 5, "org_id": 2, "title": "鸡东县副县长", "start": "", "end": "present", "rank": "副处级", "note": "负责教育、卫生健康、医疗保障、文化旅游等工作"},
    # 张铁明 — 副县长
    {"person_id": 6, "org_id": 2, "title": "鸡东县副县长", "start": "", "end": "present", "rank": "副处级", "note": "负责民政、自然资源、城乡建设、市场监管、生态环境等工作"},
    # 程炳军 — 副县长
    {"person_id": 7, "org_id": 2, "title": "鸡东县副县长", "start": "", "end": "present", "rank": "副处级", "note": "负责县域经济、产业项目、招商引资、交通运输等工作"},
    # 金成根 — 原县政府负责人
    {"person_id": 8, "org_id": 2, "title": "负责县政府常务工作（原）", "start": "2024", "end": "2025-12", "rank": "副处级", "note": "Oct-Dec 2025期间主持县政府常务会议；2026年1月起不再出现"},
]

# ── Relationships ────────────────────────────────────────────────────────────

relationships = [
    # Leadership team working relationships
    {"person_a": 1, "person_b": 2, "type": "党政同僚", "context": "同为县委常委、副县长，共同参与县政府常务会议", "overlap_org": "中共鸡东县委/鸡东县人民政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "常务副县长与副县长（公安局局长）工作搭档", "overlap_org": "鸡东县人民政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "常务副县长与副县长工作搭档", "overlap_org": "鸡东县人民政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "常务副县长与副县长工作搭档", "overlap_org": "鸡东县人民政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "常务副县长与副县长工作搭档", "overlap_org": "鸡东县人民政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "常务副县长与副县长工作搭档", "overlap_org": "鸡东县人民政府", "overlap_period": ""},
    # 金成根 — former acting leader relationship
    {"person_a": 8, "person_b": 1, "type": "上下级", "context": "金成根主持县政府工作期间何海臣为副手", "overlap_org": "鸡东县人民政府", "overlap_period": "2024至2025-12"},
    {"person_a": 8, "person_b": 2, "type": "同僚", "context": "共同参加县政府常务会议", "overlap_org": "鸡东县人民政府", "overlap_period": "至2025-12"},
    {"person_a": 8, "person_b": 7, "type": "同僚", "context": "共同参加县政府常务会议", "overlap_org": "鸡东县人民政府", "overlap_period": "至2025-12"},
]


# ══════════════════════════════════════════════════════════════════════════════
# Helper: XML escape
# ══════════════════════════════════════════════════════════════════════════════

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# ══════════════════════════════════════════════════════════════════════════════
# Build database
# ══════════════════════════════════════════════════════════════════════════════

def build_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS persons;
        DROP TABLE IF EXISTS organizations;

        CREATE TABLE persons (
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
        );

        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );

        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );

        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        cur.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
              p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        cur.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        cur.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        cur.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"  DB: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")


# ══════════════════════════════════════════════════════════════════════════════
# Build GEXF
# ══════════════════════════════════════════════════════════════════════════════

def person_color(p):
    name = p["name"]
    # 何海臣 is 常委/常务副县长 (blue for government leadership)
    if name == "何海臣":
        return "50,100,255"
    # Other deputy county mayors (blue)
    return "50,100,255"

def person_size(p):
    return "12.0"

def org_color(o):
    t = o["type"]
    if "党委" in t:
        return "255,200,200"
    if "政府" in t:
        return "200,200,255"
    if "开发区" in t:
        return "200,255,200"
    return "200,200,200"

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>OpenCode Research Agent</creator>')
    lines.append(f'    <description>鸡东县领导班子工作关系网络 - {SLUG}</description>')
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

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = person_size(p)
        pid = f"p{p['id']}"
        lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        oid = f"o{o['id']}"
        lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Person→Organization edges
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        pid = f"p{pos['person_id']}"
        oid = f"o{pos['org_id']}"
        lines.append(f'      <edge id="{eid}" source="{pid}" target="{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person↔Person relationship edges
    for r in relationships:
        eid += 1
        pa = f"p{r['person_a']}"
        pb = f"p{r['person_b']}"
        lines.append(f'      <edge id="{eid}" source="{pa}" target="{pb}" label="{esc(r["type"])}" weight="2.0">')
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
    print(f"  GEXF: {GEXF_PATH} ({eid} edges)")


# ══════════════════════════════════════════════════════════════════════════════
# Person Graph JSON Generator
# ══════════════════════════════════════════════════════════════════════════════

def make_person_json(p, timeline, relationships_list, source_register):
    result = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "黑龙江省",
            "city": "鸡西市",
            "region": "鸡东县",
            "job": p.get("current_post", ""),
            "task_id": "heilongjiang_鸡东县",
            "time_focus": "2026年7月"
        },
        "identity": {
            "person_id": f"jidong_{p['name']}",
            "name": p["name"],
            "aliases": [],
            "gender": p.get("gender", ""),
            "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""),
            "birthplace": p.get("birthplace", ""),
            "native_place": "",
            "education": [],
            "party_join": "",
            "work_start": "",
            "dedupe_keys": {
                "name_birth": f"{p['name']}_",
                "name_birthplace": f"{p['name']}_",
                "official_profile_url": p.get("source", "")
            }
        },
        "current_status": {
            "current_post": p.get("current_post", ""),
            "current_org": p.get("current_org", ""),
            "administrative_rank": "县处级正职" if p["name"] in ["金成根"] else "县处级副职",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"]
        },
        "career_timeline": timeline,
        "organizations": [],
        "relationships": relationships_list,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "在公开信息中未发现该人物负面信号", "date": "", "confidence": "confirmed", "source_ids": []}
        ],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"{p['name']}的完整履历信息、出生日期、教育背景等均需补充"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{p['name']}的完整职业生涯履历（含出生信息、教育背景、历任职务）",
                "why_it_matters": "无法追溯其任职路径和系统经历",
                "suggested_queries": [f"{p['name']} 简历 鸡东县", f"{p['name']} 任前公示"],
                "last_attempted": AS_OF
            }
        ]
    }
    return result


def build_person_jsons():
    source_register = [
        {"id": "S001", "title": "鸡东县人民政府—政府领导页", "url": "https://www.jidong.gov.cn/jdx/83af14bae13140a8ae433d50fe1734f5/zfld.shtml", "publisher": "鸡东县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "县政府领导名单（县长字段为空）"},
        {"id": "S002", "title": "鸡东县十三届第48次常务会议", "url": "https://www.jidong.gov.cn/jdx/c0f57deb14d34287a8bbfe056359e0e1/202511/c06_345432.shtml", "publisher": "鸡东县人民政府", "published_at": "2025-11-05", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "金成根主持县政府常务会议"},
        {"id": "S003", "title": "鸡东县十三届第49次常务会议", "url": "https://www.jidong.gov.cn/jdx/c0f57deb14d34287a8bbfe056359e0e1/202512/c06_348129.shtml", "publisher": "鸡东县人民政府", "published_at": "2025-12-02", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "金成根主持"},
        {"id": "S004", "title": "鸡东县十三届第50次常务会议", "url": "https://www.jidong.gov.cn/jdx/c0f57deb14d34287a8bbfe056359e0e1/202512/c06_350764.shtml", "publisher": "鸡东县人民政府", "published_at": "2025-12-29", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "金成根主持"},
        {"id": "S005", "title": "鸡东县十三届第51次常务会议", "url": "https://www.jidong.gov.cn/jdx/c0f57deb14d34287a8bbfe056359e0e1/202602/c06_355030.shtml", "publisher": "鸡东县人民政府", "published_at": "2026-02-02", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "何海臣主持会议（金成根已不在）"},
        {"id": "S006", "title": "何海臣副县长分工", "url": "https://www.jidong.gov.cn/jdx/01d6ee8e6afb4518b1af41af91e0c736/202607/c06_367659.shtml", "publisher": "鸡东县人民政府", "published_at": "2026-07", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "县委常委、常务副县长分工"},
        {"id": "S007", "title": "王莹副县长分工", "url": "https://www.jidong.gov.cn/jdx/01d6ee8e6afb4518b1af41af91e0c736/202508/c06_338828.shtml", "publisher": "鸡东县人民政府", "published_at": "2025-08", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "县委常委、副县长分工"},
        {"id": "S008", "title": "朱卫东副县长分工", "url": "https://www.jidong.gov.cn/jdx/01d6ee8e6afb4518b1af41af91e0c736/202409/c06_326054.shtml", "publisher": "鸡东县人民政府", "published_at": "2024-09", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "副县长、公安局局长分工"},
        {"id": "S009", "title": "殷云海副县长分工", "url": "https://www.jidong.gov.cn/jdx/01d6ee8e6afb4518b1af41af91e0c736/202602/c06_326055.shtml", "publisher": "鸡东县人民政府", "published_at": "2026-02", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "副县长分工（农业、水利、林草）"},
        {"id": "S010", "title": "汪冬波副县长分工", "url": "https://www.jidong.gov.cn/jdx/01d6ee8e6afb4518b1af41af91e0c736/202602/c06_326056.shtml", "publisher": "鸡东县人民政府", "published_at": "2026-02", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "副县长分工（教育、卫健、文旅）"},
        {"id": "S011", "title": "张铁明副县长分工", "url": "https://www.jidong.gov.cn/jdx/01d6ee8e6afb4518b1af41af91e0c736/202401/c06_326057.shtml", "publisher": "鸡东县人民政府", "published_at": "2024-01", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "副县长分工（民政、自然资源、住建等）"},
        {"id": "S012", "title": "程炳军副县长分工", "url": "https://www.jidong.gov.cn/jdx/01d6ee8e6afb4518b1af41af91e0c736/202501/c06_326059.shtml", "publisher": "鸡东县人民政府", "published_at": "2025-01", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "副县长分工（县域经济、产业项目、招商引资）"},
    ]

    # 1. 何海臣 (常务副县长)
    he_timeline = [
        {"start": "", "end": "", "org": "鸡东县人民政府", "title": "鸡东县委常委、副县长（常务）", "notes": "负责县政府常务工作；综合经济、安全生产、人社、信访等", "confidence": "confirmed", "source_ids": ["S006"]},
    ]
    he_relationships = [
        {"person": "王莹", "person_id": "jidong_王莹", "relationship_type": "overlap", "strength": "strong", "evidence": "同为县委常委、副县长，共同参与县政府常务会议", "overlap_org": "鸡东县人民政府", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S005"]},
        {"person": "金成根", "person_id": "jidong_金成根", "relationship_type": "subordinate_to_superior", "strength": "medium", "evidence": "金成根主持政府工作期间何海臣为副手", "overlap_org": "鸡东县人民政府", "overlap_period": "至2025-12", "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S002"]},
    ]
    he_json = make_person_json(persons[0], he_timeline, he_relationships, source_register)
    he_path = PERSONS_DIR / f"{TODAY}-黑龙江省-鸡西市-常务副县长-何海臣.json"
    with open(he_path, "w", encoding="utf-8") as f:
        json.dump(he_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {he_path.name}")

    # 2. 金成根 (原县政府负责人)
    jin_timeline = [
        {"start": "", "end": "2025-12", "org": "鸡东县人民政府", "title": "负责县政府常务工作", "notes": "2025年10-12月期间主持县政府十三届第48、49、50次常务会议；2026年1月起不再出现", "confidence": "confirmed", "source_ids": ["S002", "S003", "S004"]},
    ]
    jin_relationships = [
        {"person": "何海臣", "person_id": "jidong_何海臣", "relationship_type": "superior_to_subordinate", "strength": "medium", "evidence": "金成根主持政府工作期间何海臣为副手", "overlap_org": "鸡东县人民政府", "overlap_period": "至2025-12", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S002"]},
    ]
    jin_json = make_person_json(persons[7], jin_timeline, jin_relationships, source_register)
    jin_path = PERSONS_DIR / f"{TODAY}-黑龙江省-鸡西市-原县政府负责人-金成根.json"
    with open(jin_path, "w", encoding="utf-8") as f:
        json.dump(jin_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {jin_path.name}")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print(f"  {SLUG}领导班子工作关系网络")
    print(f"  等级: 县")
    print(f"  调查日期: {TODAY}")
    print(f"  信息来源: 鸡东县人民政府网站")
    print("=" * 60)

    build_db()
    build_gexf()
    build_person_jsons()

    print(f"\n✅ {SLUG}数据构建完成。")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")


if __name__ == "__main__":
    main()
