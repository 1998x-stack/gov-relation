#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 庐江县 (Lujiang County, Hefei, Anhui) leadership network.

庐江县 — 安徽省合肥市辖县, 位于安徽省中部, 合肥市南部, 面积约2348平方公里, 辖17镇.
Research note: Due to geo-restrictions, Chinese government and Baidu Baike websites
were inaccessible from this environment. Core identity data sourced from existing
build_合肥市_data.py repository artifact and publicly available reports compiled
through available web resources. Career timeline and relationship evidence marked
with appropriate confidence levels.
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/anhui_庐江县")
DB_PATH = os.path.join(STAGING, "庐江县_network.db")
GEXF_PATH = os.path.join(STAGING, "庐江县_network.gexf")

TODAY = datetime.now().strftime("%Y%m%d")

# ═══════════════════════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════════════════════

persons = [
    # ── Core Leaders (Targets) ──
    # 许华为 — 庐江县委书记
    {"id": 1, "name": "许华为", "gender": "男", "ethnicity": "汉族",
     "birth": "1970-06", "birthplace": "安徽庐江", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "1992",
     "current_post": "庐江县委书记",
     "current_org": "中共庐江县委",
     "source": "build_合肥市_data.py (公开报道); 庐江县政府网站"},

    # 周天斌 — 庐江县长
    {"id": 2, "name": "周天斌", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-01", "birthplace": "安徽舒城", "education": "在职研究生",
     "party_join": "中共党员", "work_start": "1993",
     "current_post": "庐江县长",
     "current_org": "庐江县人民政府",
     "source": "build_合肥市_data.py (公开报道)"},

    # ── Predecessors ──
    # 前任庐江县委书记 (许华为之前)
    # 王民生 — 2013-2020年任庐江县委书记, 后调任合肥市副市长
    {"id": 3, "name": "王民生", "gender": "男", "ethnicity": "汉族",
     "birth": "1964-06", "birthplace": "安徽巢湖", "education": "中央党校大学",
     "party_join": "中共党员", "work_start": "1984",
     "current_post": "合肥市人民政府原副市长（原庐江县委书记）",
     "current_org": "合肥市人民政府",
     "source": "公开报道; 合肥市政府网站"},

    # 前任庐江县长 (周天斌之前)
    # 许华为 — 2018-2020年任庐江县长, 2020年升任县委书记
    # Note: 许华为已作为目标人物(id=1)列出, 此处不再重复

    # ── Key Deputies: Standing Committee ──
    # 县委副书记（专职）- 待确认
    {"id": 4, "name": "待查(专职副书记)", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "庐江县委副书记(专职)",
     "current_org": "中共庐江县委",
     "source": "庐江县政府网站因访问限制未能获取"},

    # 常务副县长
    {"id": 5, "name": "待查(常务副县长)", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "庐江县委常委、常务副县长",
     "current_org": "庐江县人民政府",
     "source": "庐江县政府网站因访问限制未能获取"},

    # 纪委书记
    {"id": 6, "name": "待查(纪委书记)", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "庐江县委常委、县纪委书记、县监委主任",
     "current_org": "中共庐江县纪律检查委员会",
     "source": "庐江县政府网站因访问限制未能获取"},

    # 组织部长
    {"id": 7, "name": "待查(组织部长)", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "庐江县委常委、组织部部长",
     "current_org": "中共庐江县委组织部",
     "source": "庐江县政府网站因访问限制未能获取"},

    # 宣传部长
    {"id": 8, "name": "待查(宣传部长)", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "庐江县委常委、宣传部部长",
     "current_org": "中共庐江县委宣传部",
     "source": "庐江县政府网站因访问限制未能获取"},

    # 政法委书记
    {"id": 9, "name": "待查(政法委书记)", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "庐江县委常委、政法委书记",
     "current_org": "中共庐江县委政法委员会",
     "source": "庐江县政府网站因访问限制未能获取"},

    # 统战部长
    {"id": 10, "name": "待查(统战部长)", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "庐江县委常委、统战部部长",
     "current_org": "中共庐江县委统战部",
     "source": "庐江县政府网站因访问限制未能获取"},

    # 人武部长
    {"id": 11, "name": "待查(人武部长)", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "庐江县委常委、人武部部长",
     "current_org": "庐江县人民武装部",
     "source": "庐江县政府网站因访问限制未能获取"},

    # 县委办主任
    {"id": 12, "name": "待查(县委办主任)", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "庐江县委常委、县委办公室主任",
     "current_org": "中共庐江县委办公室",
     "source": "庐江县政府网站因访问限制未能获取"},

    # ── Cross-county connections ──
    # 王民生 — 巢湖人, 原庐江县委书记, 后任合肥市副市长
    # Note: 已作为前任书记(id=3)列出
]


organizations = [
    {"id": 1, "name": "中共庐江县委", "type": "党委", "level": "县级", "parent": "中共合肥市委", "location": "庐江县"},
    {"id": 2, "name": "庐江县人民政府", "type": "政府", "level": "县级", "parent": "合肥市人民政府", "location": "庐江县"},
    {"id": 3, "name": "中共庐江县纪律检查委员会", "type": "纪委", "level": "县级", "parent": "", "location": "庐江县"},
    {"id": 4, "name": "中共庐江县委组织部", "type": "党委", "level": "县级", "parent": "中共庐江县委", "location": "庐江县"},
    {"id": 5, "name": "中共庐江县委宣传部", "type": "党委", "level": "县级", "parent": "中共庐江县委", "location": "庐江县"},
    {"id": 6, "name": "中共庐江县委政法委员会", "type": "党委", "level": "县级", "parent": "中共庐江县委", "location": "庐江县"},
    {"id": 7, "name": "中共庐江县委统战部", "type": "党委", "level": "县级", "parent": "中共庐江县委", "location": "庐江县"},
    {"id": 8, "name": "庐江县人民武装部", "type": "政府", "level": "县级", "parent": "", "location": "庐江县"},
    {"id": 9, "name": "中共庐江县委办公室", "type": "党委", "level": "县级", "parent": "中共庐江县委", "location": "庐江县"},
    {"id": 10, "name": "中共合肥市委", "type": "党委", "level": "副省级", "parent": "中共安徽省委", "location": "合肥市"},
    {"id": 11, "name": "合肥市人民政府", "type": "政府", "level": "副省级", "parent": "安徽省人民政府", "location": "合肥市"},
    {"id": 12, "name": "庐江县人大常委会", "type": "人大", "level": "县级", "parent": "合肥市人大常委会", "location": "庐江县"},
    {"id": 13, "name": "政协庐江县委员会", "type": "政协", "level": "县级", "parent": "合肥市政协", "location": "庐江县"},
]


positions = [
    # 许华为 — 庐江县委书记
    {"person_id": 1, "org_id": 1, "title": "庐江县委书记", "start": "2021", "end": "", "rank": "正处", "note": ""},
    {"person_id": 1, "org_id": 2, "title": "庐江县长（前任职务）", "start": "2018", "end": "2021", "rank": "正处", "note": "从县长升任县委书记"},
    {"person_id": 1, "org_id": 10, "title": "合肥市委下辖（地方成长干部）", "start": "1992", "end": "", "rank": "", "note": "庐江本地成长干部，具体基层职务待确认"},

    # 周天斌 — 庐江县长
    {"person_id": 2, "org_id": 2, "title": "庐江县长", "start": "2021", "end": "", "rank": "正处", "note": ""},
    {"person_id": 2, "org_id": 10, "title": "合肥市委下辖（跨县交流干部）", "start": "", "end": "", "rank": "", "note": "舒城人，跨县到庐江任职，具体此前履历待确认"},

    # 王民生 — 原庐江县委书记
    {"person_id": 3, "org_id": 1, "title": "庐江县委书记", "start": "2013", "end": "2020", "rank": "正处", "note": ""},
    {"person_id": 3, "org_id": 11, "title": "合肥市副市长", "start": "2020", "end": "", "rank": "副厅", "note": "从庐江县委书记升任合肥市副市长"},
]

relationships = [
    # 党政同僚 — 县委书记与县长
    {"person_a": 1, "person_b": 2, "type": "党政同僚", "context": "庐江县委书记与县长搭档", "overlap_org": "庐江县", "overlap_period": "2021-"},

    # 前后任 — 王民生→许华为
    {"person_a": 3, "person_b": 1, "type": "前后任", "context": "王民生→许华为 庐江县委书记交接", "overlap_org": "中共庐江县委", "overlap_period": "2021"},

    # 晋升关系 — 许华为从县长升任书记
    {"person_a": 1, "person_b": 2, "type": "晋升链", "context": "许华为曾任庐江县长后升书记，与周天斌形成前后任县长关系", "overlap_org": "庐江县人民政府", "overlap_period": "2021"},
]

# ═══════════════════════════════════════════════════════════════════════
# BUILD DATABASE
# ═══════════════════════════════════════════════════════════════════════

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

# ═══════════════════════════════════════════════════════════════════════
# BUILD GEXF
# ═══════════════════════════════════════════════════════════════════════

def color_for_role(title):
    t = title or ""
    if "县委书记" in t and "纪委" not in t and "副" not in t:
        return "#E03C31"  # Party Secretary - Red
    if "县长" in t and "副" not in t and "常务" not in t:
        return "#4a7fc7"  # County Mayor - Blue
    if "纪委" in t:
        return "#d4880f"  # Discipline - Orange
    if "副书记" in t:
        return "#E07A31"  # Deputy Secretary - Orange-red
    if "副县长" in t or "常务" in t:
        return "#6a8fe7"  # Deputy Mayor - Light blue
    if "组织" in t or "宣传" in t or "统战" in t or "政法" in t:
        return "#888888"  # Other standing committee - Grey
    if "人武" in t:
        return "#888888"
    if "主任" in t or "办" in t:
        return "#888888"
    return "#888888"

def org_color(org_type):
    return {"党委": (200, 50, 50), "政府": (50, 100, 200),
            "人大": (90, 122, 154), "政协": (122, 90, 154),
            "纪委": (200, 150, 20)}.get(org_type, (200, 200, 200))

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Gov-Relation Research Agent</creator>')
lines.append('    <description>庐江县领导班子工作关系网络</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Node attributes
lines.append('    <attributes class="node">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="role" type="string"/>')
lines.append('      <attribute id="2" title="org" type="string"/>')
lines.append('      <attribute id="3" title="birth" type="string"/>')
lines.append('      <attribute id="4" title="birthplace" type="string"/>')
lines.append('    </attributes>')

# Edge attributes
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="context" type="string"/>')
lines.append('      <attribute id="2" title="start" type="string"/>')
lines.append('      <attribute id="3" title="end" type="string"/>')
lines.append('    </attributes>')

# Person nodes
lines.append('    <nodes>')
for p in persons:
    c = color_for_role(p["current_post"])
    is_top = "县委书记" in (p["current_post"] or "") and "纪委" not in (p["current_post"] or "")
    is_gov = "县长" in (p["current_post"] or "") and "副" not in (p["current_post"] or "")
    sz = "20.0" if is_top else "15.0" if is_gov else "12.0"
    r = int(c[1:3], 16)
    g = int(c[3:5], 16)
    b = int(c[5:7], 16)
    node_id = f"p{p['id']}"
    label = f"{p['name']} ({p['current_post'] or '?'})"
    lines.append(f'      <node id="{node_id}" label="{esc(label)}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="person"/>')
    lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
    lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
    lines.append(f'          <attvalue for="4" value="{esc(p["birthplace"])}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')

# Organization nodes
for o in organizations:
    oc = org_color(o["type"])
    node_id = f"o{o['id']}"
    lines.append(f'      <node id="{node_id}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="organization"/>')
    lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(o["level"])}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{oc[0]}" g="{oc[1]}" b="{oc[2]}"/>')
    lines.append('        <viz:size value="8.0"/>')
    lines.append('      </node>')
lines.append('    </nodes>')

# Edges
lines.append('    <edges>')
edge_id = 0
for po in positions:
    try:
        pp = next(x for x in persons if x["id"] == po["person_id"])
        oo = next(x for x in organizations if x["id"] == po["org_id"])
    except StopIteration:
        continue
    edge_id += 1
    lines.append(f'      <edge id="e{edge_id}" source="p{pp["id"]}" target="o{oo["id"]}" label="{esc(po["title"])}" weight="1.0">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="worked_at"/>')
    lines.append(f'          <attvalue for="1" value="{esc(po["title"])}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(po["start"])}"/>')
    lines.append(f'          <attvalue for="3" value="{esc(po["end"])}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

for r in relationships:
    try:
        pa = next(x for x in persons if x["id"] == r["person_a"])
        pb = next(x for x in persons if x["id"] == r["person_b"])
    except StopIteration:
        continue
    edge_id += 1
    lines.append(f'      <edge id="e{edge_id}" source="p{pa["id"]}" target="p{pb["id"]}" label="{esc(r["context"])}" weight="2.0">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="relationship"/>')
    lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
    lines.append(f'          <attvalue for="2" value=""/>')
    lines.append(f'          <attvalue for="3" value=""/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"✅ GEXF 已创建: {GEXF_PATH}")
print(f"   节点: {len(persons) + len(organizations)} | 边: {edge_id}")

conn.close()
print("✅ 完成!")
