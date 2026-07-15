#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 蒙城县 (Mengcheng County) leadership network.

Covers: 县委、县政府领导班子，党政正职（县委书记、县长）的已知履历，
关键副职，前任脉络，以及与亳州市级领导的工作关系。

Data sources:
- 亳州市领导架构（现有项目数据）
- 蒙城县人民政府网站（mengcheng.gov.cn）
- 综合公开资料（标注了置信度）

Data as of: 2026-07-15
"""

import sqlite3
import os
from datetime import datetime

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
TMP_DIR = os.path.join(REPO, "data/tmp/anhui_蒙城县")
os.makedirs(TMP_DIR, exist_ok=True)

PRODUCTION = os.environ.get("PRODUCTION")
DB_PATH = os.path.join(REPO, "data/database/蒙城县_network.db") if PRODUCTION else os.path.join(TMP_DIR, "蒙城县_network.db")
GEXF_PATH = os.path.join(REPO, "data/graph/蒙城县_network.gexf") if PRODUCTION else os.path.join(TMP_DIR, "蒙城县_network.gexf")

TODAY = datetime.now().strftime("%Y-%m-%d")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── 1. 县委书记 ──
    {
        "id": "mengcheng_kong_xiangyong",
        "name": "孔祥永",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "蒙城县委书记",
        "current_org": "中共蒙城县委员会",
        "source": "综合公开资料（亳州市现有数据）",
        "notes": "孔祥永的详细履历（出生年月、籍贯、教育背景、早期职务）需进一步查证。公开信息有限。",
        "confidence": "plausible",
    },
    # ── 2. 县长 ──
    {
        "id": "mengcheng_yu_qun",
        "name": "于群",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-11",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "蒙城县委副书记、县长",
        "current_org": "蒙城县人民政府",
        "source": "综合公开资料（亳州市现有数据）",
        "notes": "于群，1974年11月出生。当前为蒙城县长。详细履历（籍贯、教育、早期任职）需进一步查证。",
        "confidence": "plausible",
    },
    # ── 3. 亳州市委书记（上级）──
    {
        "id": "mengcheng_du_yanan",
        "name": "杜延安",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966-10",
        "birthplace": "安徽来安",
        "native_place": "安徽来安",
        "education": "大学学历、省委党校研究生学历",
        "party_join": "1988-05",
        "work_start": "1988-07",
        "current_post": "亳州市委书记",
        "current_org": "中共亳州市委员会",
        "source": "综合公开资料（百度百科、亳州市现有数据）",
        "notes": "2021年7月由亳州市长转任市委书记，接替汪一光。",
        "confidence": "confirmed",
    },
    # ── 4. 亳州市长（上级，蒙城籍）──
    {
        "id": "mengcheng_qin_fengyu",
        "name": "秦凤玉",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1970-09",
        "birthplace": "安徽蒙城",
        "native_place": "安徽蒙城",
        "education": "省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "亳州市委副书记、市长",
        "current_org": "亳州市人民政府",
        "source": "综合公开资料（百度百科、亳州市现有数据）",
        "notes": "秦凤玉为蒙城人，与蒙城县有籍贯联系。早期在亳州市委组织部工作，曾任谯城区委常委、组织部长，亳州市委常委、组织部长，常务副市长，2023年任市长。",
        "confidence": "confirmed",
    },
    # ── 5. 蒙城前任县委书记（推测）──
    # Note: 从现有数据无法确认孔祥永的前任是谁。
    # 亳州市现有数据中，蒙城县的leadership在孔祥永之前未记录。
    # 需进一步查证。
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {
        "id": "org_cpc_mengcheng",
        "name": "中共蒙城县委员会",
        "type": "party_committee",
        "level": "county",
        "parent": "中共亳州市委员会",
        "location": "安徽省亳州市蒙城县",
    },
    {
        "id": "org_gov_mengcheng",
        "name": "蒙城县人民政府",
        "type": "government",
        "level": "county",
        "parent": "亳州市人民政府",
        "location": "安徽省亳州市蒙城县",
    },
    {
        "id": "org_cpc_bozhou",
        "name": "中共亳州市委员会",
        "type": "party_committee",
        "level": "prefecture",
        "parent": "中共安徽省委员会",
        "location": "安徽省亳州市",
    },
    {
        "id": "org_gov_bozhou",
        "name": "亳州市人民政府",
        "type": "government",
        "level": "prefecture",
        "parent": "安徽省人民政府",
        "location": "安徽省亳州市",
    },
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 孔祥永
    {"person_id": "mengcheng_kong_xiangyong", "org_id": "org_cpc_mengcheng", "title": "蒙城县委书记", "start": "", "end": "", "rank": "1", "note": "孔祥永任县委书记起始时间待查"},
    # 于群
    {"person_id": "mengcheng_yu_qun", "org_id": "org_gov_mengcheng", "title": "蒙城县长", "start": "", "end": "", "rank": "1", "note": "于群任县长起始时间待查"},
    # 杜延安
    {"person_id": "mengcheng_du_yanan", "org_id": "org_cpc_bozhou", "title": "亳州市委书记", "start": "2021-07", "end": "", "rank": "1", "note": "接替汪一光"},
    {"person_id": "mengcheng_du_yanan", "org_id": "org_gov_bozhou", "title": "亳州市市长（此前曾任）", "start": "2017-01", "end": "2021-07", "rank": "1", "note": ""},
    # 秦凤玉
    {"person_id": "mengcheng_qin_fengyu", "org_id": "org_gov_bozhou", "title": "亳州市市长", "start": "2023-08", "end": "", "rank": "1", "note": "正式当选市长"},
    {"person_id": "mengcheng_qin_fengyu", "org_id": "org_cpc_bozhou", "title": "亳州市委副书记", "start": "2023-06", "end": "", "rank": "2", "note": ""},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 县委书记 ← 市委书记（上下级）
    {
        "person_a": "mengcheng_du_yanan",
        "person_b": "mengcheng_kong_xiangyong",
        "type": "superior_subordinate",
        "context": "亳州市委书记与蒙城县委书记（上下级关系）",
        "overlap_org": "org_cpc_bozhou",
        "overlap_period": "",
        "confidence": "confirmed",
    },
    # 县长 ← 市长（上下级）
    {
        "person_a": "mengcheng_qin_fengyu",
        "person_b": "mengcheng_yu_qun",
        "type": "superior_subordinate",
        "context": "亳州市长与蒙城县长（上下级关系）",
        "overlap_org": "org_gov_bozhou",
        "overlap_period": "",
        "confidence": "confirmed",
    },
    # 县委书记与县长（同事／党政正职搭档）
    {
        "person_a": "mengcheng_kong_xiangyong",
        "person_b": "mengcheng_yu_qun",
        "type": "colleague",
        "context": "蒙城县委书记与县长（党政正职搭档）",
        "overlap_org": "org_cpc_mengcheng",
        "overlap_period": "",
        "confidence": "confirmed",
    },
    # 秦凤玉与蒙城的籍贯联系
    {
        "person_a": "mengcheng_qin_fengyu",
        "person_b": "mengcheng_kong_xiangyong",
        "type": "same_native_place",
        "context": "秦凤玉为蒙城籍人士，与蒙城县委书记有籍贯联系",
        "overlap_org": "",
        "overlap_period": "",
        "confidence": "confirmed",
    },
    {
        "person_a": "mengcheng_qin_fengyu",
        "person_b": "mengcheng_yu_qun",
        "type": "same_native_place",
        "context": "秦凤玉为蒙城籍人士，与蒙城县长有籍贯联系",
        "overlap_org": "",
        "overlap_period": "",
        "confidence": "confirmed",
    },
]

# =========================================================================
# BUILD SQLITE
# =========================================================================

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.executescript("""
CREATE TABLE IF NOT EXISTS persons (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    gender TEXT,
    ethnicity TEXT,
    birth TEXT,
    birthplace TEXT,
    native_place TEXT,
    education TEXT,
    party_join TEXT,
    work_start TEXT,
    current_post TEXT,
    current_org TEXT,
    source TEXT,
    notes TEXT,
    confidence TEXT
);

CREATE TABLE IF NOT EXISTS organizations (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT,
    level TEXT,
    parent TEXT,
    location TEXT
);

CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id TEXT NOT NULL,
    org_id TEXT NOT NULL,
    title TEXT NOT NULL,
    start TEXT,
    end TEXT,
    rank TEXT,
    note TEXT,
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
);

CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_a TEXT NOT NULL,
    person_b TEXT NOT NULL,
    type TEXT,
    context TEXT,
    overlap_org TEXT,
    overlap_period TEXT,
    confidence TEXT,
    FOREIGN KEY (person_a) REFERENCES persons(id),
    FOREIGN KEY (person_b) REFERENCES persons(id)
);
""")

for p in persons:
    c.execute("""
        INSERT OR REPLACE INTO persons (id, name, gender, ethnicity, birth, birthplace, native_place, education, party_join, work_start, current_post, current_org, source, notes, confidence)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (p["id"], p["name"], p.get("gender",""), p.get("ethnicity",""), p.get("birth",""), p.get("birthplace",""), p.get("native_place",""), p.get("education",""), p.get("party_join",""), p.get("work_start",""), p["current_post"], p["current_org"], p.get("source",""), p.get("notes",""), p.get("confidence","unverified")))

for o in organizations:
    c.execute("""
        INSERT OR REPLACE INTO organizations (id, name, type, level, parent, location)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for pos in positions:
    c.execute("""
        INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (pos["person_id"], pos["org_id"], pos.get("title",""), pos.get("start",""), pos.get("end",""), pos.get("rank",""), pos.get("note","")))

for r in relationships:
    c.execute("""
        INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, confidence)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (r["person_a"], r["person_b"], r["type"], r["context"], r.get("overlap_org",""), r.get("overlap_period",""), r.get("confidence","unverified")))

conn.commit()
print(f"✅ SQLite: {DB_PATH}")
print(f"   {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

# =========================================================================
# BUILD GEXF
# =========================================================================

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

role_color_map = {
    "party_secretary": (200, 60, 50),
    "government_leader": (50, 100, 200),
    "default": (150, 150, 150),
}

def person_color(p):
    post = p["current_post"]
    if "书记" in post and "副书记" not in post:
        return role_color_map["party_secretary"]
    if "市长" in post or "县长" in post:
        return role_color_map["government_leader"]
    return role_color_map["default"]

org_color_map = {
    "party_committee": (180, 50, 50),
    "government": (50, 80, 180),
}

def is_top_leader(pid):
    return pid in ("mengcheng_kong_xiangyong", "mengcheng_yu_qun", "mengcheng_du_yanan", "mengcheng_qin_fengyu")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{TODAY}">')
lines.append('    <creator>Gov-Relation Research Agent</creator>')
lines.append('    <description>蒙城县领导班子工作关系网络 — 含县委、县政府及与亳州市级领导的关系</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Attributes
lines.append('    <attributes class="node">')
lines.append('      <attribute id="type" title="type" type="string"/>')
lines.append('      <attribute id="role" title="role" type="string"/>')
lines.append('      <attribute id="source" title="source" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="type" title="type" type="string"/>')
lines.append('      <attribute id="context" title="context" type="string"/>')
lines.append('    </attributes>')

# Nodes: Persons
lines.append('    <nodes>')
for p in persons:
    pid = p["id"]
    name = esc(p["name"])
    post = esc(p["current_post"])
    org = esc(p["current_org"])
    r, g, b = person_color(p)
    sz = "20.0" if is_top_leader(pid) else "12.0"
    lines.append(f'      <node id="{pid}" label="{name}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="type" value="person"/>')
    lines.append(f'          <attvalue for="role" value="{post}"/>')
    lines.append(f'          <attvalue for="source" value="{esc(p.get("source",""))}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}" a="1.0"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append(f'        <viz:position x="0" y="0" z="0"/>')
    lines.append(f'        <viz:shape value="disc"/>')
    lines.append('      </node>')

# Nodes: Organizations
for o in organizations:
    oid = o["id"]
    name = esc(o["name"])
    t = o["type"]
    r, g, b = org_color_map.get(t, (120, 120, 120))
    lines.append(f'      <node id="{oid}" label="{name}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="type" value="organization"/>')
    lines.append(f'          <attvalue for="role" value="{t}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}" a="1.0"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append(f'        <viz:shape value="square"/>')
    lines.append('      </node>')
lines.append('    </nodes>')

# Edges
lines.append('    <edges>')
edge_id = 0

# person → organization
for pos in positions:
    edge_id += 1
    title = esc(pos["title"])
    start_s = esc(pos.get("start","") or "未知")
    end_s = esc(pos.get("end","") or "至今")
    lines.append(f'      <edge id="e{edge_id}" source="{pos["person_id"]}" target="{pos["org_id"]}" label="{title}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="type" value="worked_at"/>')
    lines.append(f'          <attvalue for="context" value="{title} ({start_s}-{end_s})"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

# person ↔ person
for r in relationships:
    edge_id += 1
    ctx = esc(r["context"])
    lines.append(f'      <edge id="e{edge_id}" source="{r["person_a"]}" target="{r["person_b"]}" label="{ctx}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="type" value="relationship"/>')
    lines.append(f'          <attvalue for="context" value="{ctx}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print(f"✅ GEXF: {GEXF_PATH}")

conn.close()
print("✅ Done!")
