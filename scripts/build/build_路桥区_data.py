#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 路桥区 (Luqiao District), 台州市, 浙江省.

Sources:
  - Official bio pages: https://www.luqiao.gov.cn/col/col1229303003/index.html
  - Community interaction: https://www.luqiao.gov.cn/col/col1229303206/index.html
  - Appointment notices: https://www.luqiao.gov.cn/col/col1229303238/index.html
"""

from __future__ import annotations

import os
import sys
import sqlite3
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parents[2]  # repo root when staging at data/tmp/zhejiang_路桥区/
sys.path.insert(0, str(BASE))

TMP = HERE
DB_PATH = str(TMP / "路桥区_network.db")
GEXF_PATH = str(TMP / "路桥区_network.gexf")

# ═══════════════════════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════════════════════

persons = [
    # ── 1. 中共路桥区委 ──
    {"id": 1, "name": "潘崇敏", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "路桥区委书记", "current_org": "中共路桥区委员会",
     "source": "https://www.baike.com/wiki/潘崇敏"},
    {"id": 2, "name": "牟傲野", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-01", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "路桥区委副书记、区长", "current_org": "路桥区人民政府",
     "source": "https://www.luqiao.gov.cn/col/col1229303003/index.html"},
    {"id": 3, "name": "庞鑫培", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "路桥区委副书记、社会工作部部长、政法委书记",
     "current_org": "中共路桥区委员会",
     "source": "https://www.luqiao.gov.cn/art/2025/6/30/art_1683576_58952643.html"},
    {"id": 4, "name": "王琛", "gender": "男", "ethnicity": "汉族",
     "birth": "1985-12", "birthplace": "", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "路桥区委常委、常务副区长（保留正县长级）",
     "current_org": "路桥区人民政府",
     "source": "https://www.luqiao.gov.cn/col/col1229750541/index.html"},
    {"id": 5, "name": "徐文华", "gender": "男", "ethnicity": "汉族",
     "birth": "1973-10", "birthplace": "", "education": "在职大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "路桥区委常委、副区长", "current_org": "路桥区人民政府",
     "source": "https://www.luqiao.gov.cn/col/col1229615140/index.html"},
    {"id": 6, "name": "陈文博", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "路桥区领导", "current_org": "中共路桥区委员会",
     "source": "https://www.luqiao.gov.cn/col/col1683482/art/2026/art_2384d2272edb469484aa836f41f4d2a2.html"},
    # ── 2. 路桥区人民政府 ──
    {"id": 7, "name": "尤燊", "gender": "男", "ethnicity": "汉族",
     "birth": "1983-11", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "路桥区副区长、党组成员", "current_org": "路桥区人民政府",
     "source": "https://www.luqiao.gov.cn/col/col1229750542/index.html"},
    {"id": 8, "name": "马青田", "gender": "男", "ethnicity": "汉族",
     "birth": "1974-06", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "路桥区副区长、党组成员", "current_org": "路桥区人民政府",
     "source": "https://www.luqiao.gov.cn/col/col1229781544/index.html"},
    {"id": 9, "name": "柯拓扬", "gender": "男", "ethnicity": "汉族",
     "birth": "1986-04", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "路桥区副区长、党组成员", "current_org": "路桥区人民政府",
     "source": "https://www.luqiao.gov.cn/col/col1229830876/index.html"},
    {"id": 10, "name": "罗朝辉", "gender": "男", "ethnicity": "汉族",
     "birth": "1979-05", "birthplace": "", "education": "在职大学/工程硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "路桥区副区长、党组成员，区公安分局局长",
     "current_org": "路桥区人民政府",
     "source": "https://www.luqiao.gov.cn/col/col1229881510/index.html"},
    {"id": 11, "name": "任超", "gender": "男", "ethnicity": "汉族",
     "birth": "1978-09", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "路桥区副区长、党组成员", "current_org": "路桥区人民政府",
     "source": "https://www.luqiao.gov.cn/col/col1229893208/index.html"},
    {"id": 12, "name": "蒋瑛", "gender": "女", "ethnicity": "汉族",
     "birth": "1985-11", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "路桥区副区长、党组成员", "current_org": "路桥区人民政府",
     "source": "https://www.luqiao.gov.cn/col/col1229303002/jy/index.html"},
]

organizations = [
    {"id": 1, "name": "中共路桥区委员会", "type": "党委", "level": "县处级",
     "parent": "中共台州市委员会", "location": "浙江省台州市路桥区"},
    {"id": 2, "name": "路桥区人民政府", "type": "政府", "level": "县处级",
     "parent": "台州市人民政府", "location": "浙江省台州市路桥区"},
    {"id": 3, "name": "台州市公安局路桥分局", "type": "政府", "level": "县处级",
     "parent": "台州市公安局", "location": "浙江省台州市路桥区"},
]

positions = [
    # 区委
    {"person_id": 1, "org_id": 1, "title": "路桥区委书记",
     "start": "2021-12", "end": "present", "rank": "县处级正职",
     "note": "2021年12月任路桥区委书记"},
    {"person_id": 2, "org_id": 1, "title": "路桥区委副书记（兼）",
     "start": "", "end": "present", "rank": "县处级正职", "note": "现任"},
    {"person_id": 2, "org_id": 2, "title": "路桥区区长",
     "start": "", "end": "present", "rank": "县处级正职", "note": "现任"},
    {"person_id": 3, "org_id": 1, "title": "路桥区委副书记（专职）",
     "start": "", "end": "present", "rank": "县处级副职", "note": "现任"},
    {"person_id": 3, "org_id": 1, "title": "路桥区社会工作部部长",
     "start": "", "end": "present", "rank": "", "note": "现任"},
    {"person_id": 3, "org_id": 1, "title": "路桥区委政法委书记",
     "start": "", "end": "present", "rank": "", "note": "现任"},
    {"person_id": 4, "org_id": 1, "title": "路桥区委常委",
     "start": "", "end": "present", "rank": "县处级副职", "note": "现任"},
    {"person_id": 4, "org_id": 2, "title": "常务副区长（保留正县长级）",
     "start": "", "end": "present", "rank": "县处级副职", "note": "现任"},
    {"person_id": 5, "org_id": 1, "title": "路桥区委常委",
     "start": "", "end": "present", "rank": "县处级副职", "note": "现任"},
    {"person_id": 5, "org_id": 2, "title": "副区长",
     "start": "", "end": "present", "rank": "县处级副职", "note": "现任"},
    # 区政府
    {"person_id": 7, "org_id": 2, "title": "副区长、党组成员",
     "start": "", "end": "present", "rank": "县处级副职", "note": "现任"},
    {"person_id": 8, "org_id": 2, "title": "副区长、党组成员",
     "start": "", "end": "present", "rank": "县处级副职", "note": "现任"},
    {"person_id": 9, "org_id": 2, "title": "副区长、党组成员",
     "start": "", "end": "present", "rank": "县处级副职", "note": "现任"},
    {"person_id": 10, "org_id": 2, "title": "副区长、党组成员",
     "start": "", "end": "present", "rank": "县处级副职", "note": "现任"},
    {"person_id": 10, "org_id": 3, "title": "区公安分局局长、党委书记",
     "start": "", "end": "present", "rank": "县处级副职", "note": "现任"},
    {"person_id": 11, "org_id": 2, "title": "副区长、党组成员",
     "start": "", "end": "present", "rank": "县处级副职", "note": "现任"},
    {"person_id": 12, "org_id": 2, "title": "副区长、党组成员",
     "start": "", "end": "present", "rank": "县处级副职", "note": "现任"},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "潘崇敏（区委书记）与牟傲野（区长）是路桥区党政一把手搭档关系",
     "overlap_org": "中共路桥区委员会/路桥区人民政府", "overlap_period": "2021-至今",
     "confidence": "confirmed"},
    {"person_a": 1, "person_b": 3, "type": "同僚",
     "context": "庞鑫培系区委专职副书记，配合潘崇敏处理区委日常工作；兼任政法委书记",
     "overlap_org": "中共路桥区委员会", "overlap_period": "",
     "confidence": "confirmed"},
    {"person_a": 2, "person_b": 3, "type": "同僚",
     "context": "牟傲野与庞鑫培同为路桥区委副书记",
     "overlap_org": "中共路桥区委员会", "overlap_period": "",
     "confidence": "confirmed"},
    {"person_a": 2, "person_b": 4, "type": "上下级",
     "context": "王琛（常务副区长）协助牟傲野处理区政府常务工作",
     "overlap_org": "路桥区人民政府", "overlap_period": "",
     "confidence": "confirmed"},
    {"person_a": 4, "person_b": 5, "type": "同僚",
     "context": "王琛与徐文华均为区委常委、副区长",
     "overlap_org": "中共路桥区委员会", "overlap_period": "",
     "confidence": "confirmed"},
    {"person_a": 1, "person_b": 4, "type": "上下级",
     "context": "王琛作为区委常委协助区委书记潘崇敏",
     "overlap_org": "中共路桥区委员会", "overlap_period": "",
     "confidence": "confirmed"},
    {"person_a": 1, "person_b": 5, "type": "上下级",
     "context": "徐文华作为区委常委协助区委书记潘崇敏",
     "overlap_org": "中共路桥区委员会", "overlap_period": "",
     "confidence": "confirmed"},
    {"person_a": 1, "person_b": 6, "type": "上下级",
     "context": "陈文博作为区领导陪同潘崇敏调研人工智能工作（2026年7月）",
     "overlap_org": "中共路桥区委员会", "overlap_period": "2026-07",
     "confidence": "confirmed"},
    {"person_a": 8, "person_b": 1, "type": "上下级",
     "context": "马青田副区长陪同潘崇敏调研商贸经济工作（2026年7月）",
     "overlap_org": "路桥区人民政府", "overlap_period": "2026-07",
     "confidence": "confirmed"},
    {"person_a": 11, "person_b": 1, "type": "上下级",
     "context": "任超副区长陪同潘崇敏调研人工智能发展工作（2026年7月）",
     "overlap_org": "路桥区人民政府", "overlap_period": "2026-07",
     "confidence": "confirmed"},
    {"person_a": 11, "person_b": 2, "type": "上下级",
     "context": "任超陪同牟傲野赴螺洋街道调研",
     "overlap_org": "路桥区人民政府", "overlap_period": "2026-07",
     "confidence": "confirmed"},
    {"person_a": 7, "person_b": 8, "type": "同僚",
     "context": "尤燊与马青田均为副区长，在区政府共事",
     "overlap_org": "路桥区人民政府", "overlap_period": "",
     "confidence": "confirmed"},
    {"person_a": 9, "person_b": 10, "type": "同僚",
     "context": "柯拓扬与罗朝辉均为副区长，在区政府共事",
     "overlap_org": "路桥区人民政府", "overlap_period": "",
     "confidence": "confirmed"},
    {"person_a": 11, "person_b": 12, "type": "同僚",
     "context": "任超与蒋瑛均为副区长，在区政府共事",
     "overlap_org": "路桥区人民政府", "overlap_period": "",
     "confidence": "confirmed"},
    {"person_a": 4, "person_b": 10, "type": "上下级",
     "context": "王琛（常务副区长）分管联系公安分局（罗朝辉任局长）",
     "overlap_org": "路桥区人民政府", "overlap_period": "",
     "confidence": "confirmed"},
    {"person_a": 4, "person_b": 11, "type": "上下级",
     "context": "王琛联系金融、科技领域（任超分管领域）",
     "overlap_org": "路桥区人民政府", "overlap_period": "",
     "confidence": "confirmed"},
]

# ═══════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    role = p["current_post"]
    if "区委书记" in role and "副书记" not in role:
        return "255,50,50"
    elif "区长" in role and "副书记" in role:
        return "50,100,255"
    elif "副书记" in role and ("社会工作" in role or "政法委" in role or "专职" in role):
        return "200,100,50"
    elif "常委" in role or "常务" in role:
        return "100,100,200"
    elif "副区长" in role:
        return "30,100,200"
    elif "纪委书记" in role or "纪检" in role:
        return "255,165,0"
    elif "人大" in role:
        return "200,255,255"
    elif "政协" in role:
        return "255,240,200"
    else:
        return "100,100,100"

def org_color(o):
    t = o["type"]
    palette = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "开发区": "200,255,200",
        "乡镇/街道": "255,255,200",
        "事业单位": "220,220,220",
        "群团": "255,220,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return palette.get(t, "200,200,200")

def person_size(p):
    role = p["current_post"]
    if "区委书记" in role and "副书记" not in role:
        return "20.0"
    elif "区长" in role:
        return "20.0"
    elif "副书记" in role:
        return "15.0"
    elif "常委" in role:
        return "14.0"
    elif "副区长" in role:
        return "12.0"
    else:
        return "10.0"


# ═══════════════════════════════════════════════════════════════════════
# BUILD DB
# ═══════════════════════════════════════════════════════════════════════

def build_db():
    os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
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
            person_a INTEGER, person_b INTEGER, type TEXT,
            context TEXT, overlap_org TEXT, overlap_period TEXT,
            confidence TEXT,
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
             p.get("birthplace", ""), p.get("education", ""),
             p["party_join"], p.get("work_start", ""),
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
             pos.get("start", ""), pos.get("end", ""),
             pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        c.execute("""INSERT INTO relationships
            (person_a, person_b, type, context, overlap_org, overlap_period, confidence)
            VALUES (?,?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"],
             r["context"], r["overlap_org"], r["overlap_period"], r.get("confidence", "confirmed")))

    conn.commit()
    conn.close()
    print(f"Database created: {DB_PATH}")


# ═══════════════════════════════════════════════════════════════════════
# BUILD GEXF
# ═══════════════════════════════════════════════════════════════════════

def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH) or ".", exist_ok=True)
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation Research Agent</creator>')
    lines.append('    <description>路桥区领导班子工作关系网络 - 浙江省台州市路桥区</description>')
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
        lines.append(f'          <attvalue for="2" value="{esc(pos.get("start",""))}~{esc(pos.get("end",""))}"/>')
        lines.append(f'          <attvalue for="3" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationships)
    for r in relationships:
        eid += 1
        w = "2.0" if r.get("confidence") == "confirmed" else "1.5"
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_period"])}"/>')
        lines.append(f'          <attvalue for="3" value="{r.get("confidence","confirmed")}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF created: {GEXF_PATH}")


# ═══════════════════════════════════════════════════════════════════════
# RUN
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    build_db()
    build_gexf()
    print(f"\nSummary:")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")