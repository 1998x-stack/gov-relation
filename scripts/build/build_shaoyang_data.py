#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 邵阳市 (Shaoyang City, Hunan) leadership network."""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/shaoyang_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/shaoyang_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── A. City-level leadership ──
    {"id": 1, "name": "程蓓", "gender": "女", "ethnicity": "汉族",
     "birth": "1972-08", "birthplace": "安徽省淮南市", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "邵阳市委书记、市长", "current_org": "中共邵阳市委/邵阳市人民政府",
     "source": "https://zh.wikipedia.org/wiki/邵阳市"},
    {"id": 2, "name": "严华", "gender": "男", "ethnicity": "汉族",
     "birth": "1968-08", "birthplace": "湖南省常德市澧县", "education": "湖南师范大学思想政治教育专业",
     "party_join": "1987", "work_start": "1991",
     "current_post": "原邵阳市委书记（2026.05卸任，另有任用）", "current_org": "",
     "source": "https://zh.wikipedia.org/wiki/严华_(1968年)"},
    {"id": 3, "name": "周迎春", "gender": "女", "ethnicity": "汉族",
     "birth": "1969-01", "birthplace": "湖南省安仁县", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "邵阳市人大常委会主任", "current_org": "邵阳市人大常委会",
     "source": "https://zh.wikipedia.org/wiki/邵阳市"},
    {"id": 4, "name": "周文", "gender": "男", "ethnicity": "汉族",
     "birth": "1968-09", "birthplace": "湖南省武冈市", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "邵阳市政协主席", "current_org": "邵阳市政协",
     "source": "https://zh.wikipedia.org/wiki/邵阳市"},
    # ── B. County-level (confirmed from Wikipedia) ──
    {"id": 5, "name": "袁胜良", "gender": "男", "ethnicity": "汉族",
     "birth": "1971-08", "birthplace": "湖南省隆回县", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "邵阳县委书记", "current_org": "中共邵阳县委员会",
     "source": "https://zh.wikipedia.org/wiki/邵阳县"},
    {"id": 6, "name": "周玉祥", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-11", "birthplace": "湖南省新邵县", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "邵阳县县长", "current_org": "邵阳县人民政府",
     "source": "https://zh.wikipedia.org/wiki/邵阳县"},
    {"id": 7, "name": "黄海蓉", "gender": "女", "ethnicity": "汉族",
     "birth": "1973-04", "birthplace": "湖南省邵阳市", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "新邵县委书记", "current_org": "中共新邵县委员会",
     "source": "https://zh.wikipedia.org/wiki/新邵县"},
    {"id": 8, "name": "谢小军", "gender": "男", "ethnicity": "汉族",
     "birth": "1978-09", "birthplace": "湖南省邵东市", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "新邵县县长", "current_org": "新邵县人民政府",
     "source": "https://zh.wikipedia.org/wiki/新邵县"},
    {"id": 9, "name": "刘厚见", "gender": "男", "ethnicity": "汉族",
     "birth": "1973-11", "birthplace": "湖南省邵东市", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "隆回县委书记", "current_org": "中共隆回县委员会",
     "source": "https://zh.wikipedia.org/wiki/隆回县"},
    {"id": 10, "name": "杨韶辉", "gender": "男", "ethnicity": "瑶族",
     "birth": "1974-02", "birthplace": "湖南省洞口县", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "隆回县县长", "current_org": "隆回县人民政府",
     "source": "https://zh.wikipedia.org/wiki/隆回县"},
    {"id": 11, "name": "彭茂华", "gender": "男", "ethnicity": "汉族",
     "birth": "1973-04", "birthplace": "湖南省武冈市", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "邵阳县人大常委会主任", "current_org": "邵阳县人大常委会",
     "source": "https://zh.wikipedia.org/wiki/邵阳县"},
    {"id": 12, "name": "唐军良", "gender": "男", "ethnicity": "汉族",
     "birth": "1967-03", "birthplace": "湖南省邵阳县", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "邵阳县政协主席", "current_org": "邵阳县政协",
     "source": "https://zh.wikipedia.org/wiki/邵阳县"},
    {"id": 13, "name": "刘长峰", "gender": "男", "ethnicity": "汉族",
     "birth": "1971-01", "birthplace": "湖南省隆回县", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "新邵县人大常委会主任", "current_org": "新邵县人大常委会",
     "source": "https://zh.wikipedia.org/wiki/新邵县"},
    {"id": 14, "name": "邹功树", "gender": "男", "ethnicity": "汉族",
     "birth": "1968-09", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "新邵县政协主席", "current_org": "新邵县政协",
     "source": "https://zh.wikipedia.org/wiki/新邵县"},
    {"id": 15, "name": "曾梅林", "gender": "男", "ethnicity": "汉族",
     "birth": "1968-09", "birthplace": "湖南省隆回县", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "隆回县人大常委会主任", "current_org": "隆回县人大常委会",
     "source": "https://zh.wikipedia.org/wiki/隆回县"},
    {"id": 16, "name": "奉锡样", "gender": "男", "ethnicity": "瑶族",
     "birth": "1972-01", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "隆回县政协主席", "current_org": "隆回县政协",
     "source": "https://zh.wikipedia.org/wiki/隆回县"},
]

organizations = [
    {"id": 1, "name": "中共邵阳市委", "type": "党委", "level": "地级", "parent": "", "location": "邵阳市"},
    {"id": 2, "name": "邵阳市人民政府", "type": "政府", "level": "地级", "parent": "", "location": "邵阳市"},
    {"id": 3, "name": "邵阳市人大常委会", "type": "人大", "level": "地级", "parent": "", "location": "邵阳市"},
    {"id": 4, "name": "邵阳市政协", "type": "政协", "level": "地级", "parent": "", "location": "邵阳市"},
    {"id": 5, "name": "中共邵阳县委员会", "type": "党委", "level": "县级", "parent": "中共邵阳市委", "location": "邵阳县"},
    {"id": 6, "name": "邵阳县人民政府", "type": "政府", "level": "县级", "parent": "邵阳市人民政府", "location": "邵阳县"},
    {"id": 7, "name": "邵阳县人大常委会", "type": "人大", "level": "县级", "parent": "", "location": "邵阳县"},
    {"id": 8, "name": "邵阳县政协", "type": "政协", "level": "县级", "parent": "", "location": "邵阳县"},
    {"id": 9, "name": "中共新邵县委员会", "type": "党委", "level": "县级", "parent": "中共邵阳市委", "location": "新邵县"},
    {"id": 10, "name": "新邵县人民政府", "type": "政府", "level": "县级", "parent": "邵阳市人民政府", "location": "新邵县"},
    {"id": 11, "name": "新邵县人大常委会", "type": "人大", "level": "县级", "parent": "", "location": "新邵县"},
    {"id": 12, "name": "新邵县政协", "type": "政协", "level": "县级", "parent": "", "location": "新邵县"},
    {"id": 13, "name": "中共隆回县委员会", "type": "党委", "level": "县级", "parent": "中共邵阳市委", "location": "隆回县"},
    {"id": 14, "name": "隆回县人民政府", "type": "政府", "level": "县级", "parent": "邵阳市人民政府", "location": "隆回县"},
    {"id": 15, "name": "隆回县人大常委会", "type": "人大", "level": "县级", "parent": "", "location": "隆回县"},
    {"id": 16, "name": "隆回县政协", "type": "政协", "level": "县级", "parent": "", "location": "隆回县"},
]

positions = [
    # City-level positions
    {"person_id": 1, "org_id": 1, "title": "邵阳市委书记", "start": "2026-05", "end": "", "rank": "正厅", "note": ""},
    {"person_id": 1, "org_id": 2, "title": "邵阳市市长", "start": "2024-09", "end": "", "rank": "正厅", "note": "一肩挑书记+市长"},
    {"person_id": 2, "org_id": 1, "title": "邵阳市委书记", "start": "2021-08", "end": "2026-05", "rank": "正厅", "note": ""},
    {"person_id": 3, "org_id": 3, "title": "邵阳市人大常委会主任", "start": "2022-01", "end": "", "rank": "正厅", "note": ""},
    {"person_id": 4, "org_id": 4, "title": "邵阳市政协主席", "start": "2022-01", "end": "", "rank": "正厅", "note": ""},
    # Shaoyang County
    {"person_id": 5, "org_id": 5, "title": "邵阳县委书记", "start": "2021-06", "end": "", "rank": "正处", "note": ""},
    {"person_id": 6, "org_id": 6, "title": "邵阳县县长", "start": "2021-10", "end": "", "rank": "正处", "note": ""},
    {"person_id": 11, "org_id": 7, "title": "邵阳县人大常委会主任", "start": "2024-05", "end": "", "rank": "正处", "note": ""},
    {"person_id": 12, "org_id": 8, "title": "邵阳县政协主席", "start": "2021-10", "end": "", "rank": "正处", "note": ""},
    # Xinshao County
    {"person_id": 7, "org_id": 9, "title": "新邵县委书记", "start": "2023-09", "end": "", "rank": "正处", "note": ""},
    {"person_id": 8, "org_id": 10, "title": "新邵县县长", "start": "2023-10", "end": "", "rank": "正处", "note": ""},
    {"person_id": 13, "org_id": 11, "title": "新邵县人大常委会主任", "start": "2022-07", "end": "", "rank": "正处", "note": ""},
    {"person_id": 14, "org_id": 12, "title": "新邵县政协主席", "start": "2021-10", "end": "", "rank": "正处", "note": ""},
    # Longhui County
    {"person_id": 9, "org_id": 13, "title": "隆回县委书记", "start": "2024-05", "end": "", "rank": "正处", "note": ""},
    {"person_id": 10, "org_id": 14, "title": "隆回县县长", "start": "2021-10", "end": "", "rank": "正处", "note": ""},
    {"person_id": 15, "org_id": 15, "title": "隆回县人大常委会主任", "start": "2021-10", "end": "", "rank": "正处", "note": ""},
    {"person_id": 16, "org_id": 16, "title": "隆回县政协主席", "start": "2021-10", "end": "", "rank": "正处", "note": ""},
]

relationships = [
    # Work together in same city
    {"person_a": 1, "person_b": 3, "type": "党政同僚", "context": "邵阳市委书记与人大主任", "overlap_org": "邵阳市", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 4, "type": "党政同僚", "context": "邵阳市委书记与政协主席", "overlap_org": "邵阳市", "overlap_period": "2026-"},
    # Succession: Yan Hua → Cheng Bei
    {"person_a": 2, "person_b": 1, "type": "前后任", "context": "严华→程蓓 邵阳市委书记交接", "overlap_org": "中共邵阳市委", "overlap_period": "2026-05"},
    # Cross-county connections (birthplace-based)
    {"person_a": 6, "person_b": 13, "type": "同乡（新邵）", "context": "周玉祥(新邵人/邵阳县县长)与刘长峰(隆回人)", "overlap_org": "", "overlap_period": ""},
    {"person_a": 8, "person_b": 9, "type": "同乡（邵东）", "context": "谢小军(邵东人/新邵县长)与刘厚见(邵东人/隆回书记)", "overlap_org": "", "overlap_period": ""},
    {"person_a": 5, "person_b": 13, "type": "同乡（隆回）", "context": "袁胜良(隆回人/邵阳县委书记)与刘长峰(隆回人)", "overlap_org": "", "overlap_period": ""},
    {"person_a": 4, "person_b": 5, "type": "同乡（隆回）", "context": "周文武冈人/政协主席 vs 袁胜良隆回人", "overlap_org": "", "overlap_period": ""},
]

# ── BUILD DATABASE ──────────────────────────────────────────────────

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
CREATE TABLE IF NOT EXISTS persons (
    id INTEGER PRIMARY KEY,
    name TEXT, gender TEXT, ethnicity TEXT,
    birth TEXT, birthplace TEXT, education TEXT,
    party_join TEXT, work_start TEXT,
    current_post TEXT, current_org TEXT, source TEXT
);
CREATE TABLE IF NOT EXISTS organizations (
    id INTEGER PRIMARY KEY,
    name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
);
CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER, org_id INTEGER,
    title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT,
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
);
CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_a INTEGER, person_b INTEGER,
    type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT,
    FOREIGN KEY (person_a) REFERENCES persons(id),
    FOREIGN KEY (person_b) REFERENCES persons(id)
);
""")

for p in persons:
    cur.execute("INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                (p["id"], p["name"], p["gender"], p["ethnicity"],
                 p["birth"], p["birthplace"], p["education"],
                 p["party_join"], p["work_start"],
                 p["current_post"], p["current_org"], p["source"]))

for o in organizations:
    cur.execute("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)",
                (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for po in positions:
    cur.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)",
                (po["person_id"], po["org_id"], po["title"], po["start"], po["end"], po["rank"], po["note"]))

for r in relationships:
    cur.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
                (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

conn.commit()

# ── Print summary ──
cur.execute("SELECT COUNT(*) FROM persons")
person_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM organizations")
org_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM positions")
pos_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM relationships")
rel_count = cur.fetchone()[0]

print(f"✅ 数据库已创建: {DB_PATH}")
print(f"   人物: {person_count} | 机构: {org_count} | 任职: {pos_count} | 关系: {rel_count}")

# ── BUILD GEXF ──────────────────────────────────────────────────────

def color_for_role(title):
    t = title or ""
    if "书记" in t and "纪委" not in t:
        return "#E03C31"
    if "市长" in t or "县长" in t or "区长" in t:
        return "#4a7fc7"
    if "人大" in t:
        return "#5a7a9a"
    if "政协" in t:
        return "#7a5a9a"
    if "纪委" in t:
        return "#d4880f"
    return "#888888"

def org_color(org_type):
    return {"党委": "rgba(200,50,50,0.3)", "政府": "rgba(50,100,200,0.3)",
            "人大": "rgba(90,122,154,0.3)", "政协": "rgba(122,90,154,0.3)",
            "纪委": "rgba(200,150,20,0.3)"}.get(org_type, "rgba(200,200,200,0.3)")

gexf_parts = []
gexf_parts.append('<?xml version="1.0" encoding="UTF-8"?>')
gexf_parts.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
gexf_parts.append('<meta><creator>Shaoyang Investigator</creator><description>邵阳市领导班子工作关系网络</description></meta>')
gexf_parts.append('<graph mode="static" defaultedgetype="undirected">')

# Nodes
gexf_parts.append('<nodes>')
for p in persons:
    rid = f"shaoyang_{p['name']}"
    role_color = color_for_role(p["current_post"])
    size = 20.0 if "书记" in (p["current_post"] or "") and "纪委" not in (p["current_post"] or "") else 15.0 if "市长" in (p["current_post"] or "") or "县长" in (p["current_post"] or "") else 12.0
    label = f"{p['name']} ({p['current_post'] or '?'})"
    gexf_parts.append(f'<node id="{rid}" label="{label}">')
    gexf_parts.append(f'<attvalues><attvalue for="role" value="{p["current_post"]}"/><attvalue for="org" value="{p["current_org"]}"/><attvalue for="birth" value="{p["birth"]}"/><attvalue for="birthplace" value="{p["birthplace"]}"/></attvalues>')
    gexf_parts.append(f'<viz:color r="{int(role_color[1:3],16)}" g="{int(role_color[3:5],16)}" b="{int(role_color[5:7],16)}"/>')
    gexf_parts.append(f'<viz:size value="{size}"/>')
    gexf_parts.append('</node>')

for o in organizations:
    oid = f"org_{o['name']}"
    oc = org_color(o["type"])
    oc_rgb = oc.replace("rgba(", "").rstrip(")").split(",")
    gexf_parts.append(f'<node id="{oid}" label="{o["name"]}">')
    gexf_parts.append(f'<attvalues><attvalue for="type" value="{o["type"]}"/><attvalue for="level" value="{o["level"]}"/></attvalues>')
    gexf_parts.append(f'<viz:color r="{int(oc_rgb[0])}" g="{int(oc_rgb[1])}" b="{int(oc_rgb[2])}"/>')
    gexf_parts.append(f'<viz:size value="8.0"/>')
    gexf_parts.append('</node>')
gexf_parts.append('</nodes>')

# Edges
gexf_parts.append('<edges>')
edge_id = 0
for po in positions:
    p = next(x for x in persons if x["id"] == po["person_id"])
    o = next(x for x in organizations if x["id"] == po["org_id"])
    edge_id += 1
    label = f"{p['name']} → {o['name']} ({po['title']})"
    gexf_parts.append(f'<edge id="e{edge_id}" source="shaoyang_{p["name"]}" target="org_{o["name"]}" label="{label}" weight="1.0">')
    gexf_parts.append(f'<attvalues><attvalue for="type" value="worked_at"/><attvalue for="title" value="{po["title"]}"/><attvalue for="start" value="{po["start"]}"/><attvalue for="end" value="{po["end"]}"/></attvalues>')
    gexf_parts.append('</edge>')

for r in relationships:
    p_a = next(x for x in persons if x["id"] == r["person_a"])
    p_b = next(x for x in persons if x["id"] == r["person_b"])
    edge_id += 1
    gexf_parts.append(f'<edge id="e{edge_id}" source="shaoyang_{p_a["name"]}" target="shaoyang_{p_b["name"]}" label="{r["context"]}" weight="2.0">')
    gexf_parts.append(f'<attvalues><attvalue for="type" value="relationship"/><attvalue for="context" value="{r["context"]}"/></attvalues>')
    gexf_parts.append('</edge>')

gexf_parts.append('</edges>')
gexf_parts.append('</graph>')
gexf_parts.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(gexf_parts))

print(f"✅ GEXF 已创建: {GEXF_PATH}")
print(f"   节点: {len(persons) + len(organizations)} | 边: {edge_id}")

conn.close()
print("✅ 完成!")
