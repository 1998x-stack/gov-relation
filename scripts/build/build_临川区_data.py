#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 临川区 (抚州市, 江西省) leadership network.

临川区概况: 临川区是江西省抚州市下辖的市辖区, 抚州市政府所在地,
抚州市的政治、经济、文化中心。原为临川县, 1995年撤县设市,
2000年抚州撤地设市时改为临川区。

数据说明: 由于网络搜索工具受到限制, 本脚本中的数据部分来自现有的
抚州市级资料和公开信息, 部分信息标记为待核实。所有数据以2026年7月
15日调查时为基准。

IMPORTANT: Web search and government site access was severely rate-limited during
research (Exa API rate limit reached, Baidu/Google blocking automated requests).
Data is sourced from existing repository artifacts and prior knowledge, with
confidence levels explicitly marked.
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/jiangxi_临川区")
DB_PATH = os.path.join(STAGING, "临川区_network.db")
GEXF_PATH = os.path.join(STAGING, "临川区_network.gexf")

os.makedirs(STAGING, exist_ok=True)

TODAY = datetime.now().strftime("%Y-%m-%d")

# =========================================================================
# PERSONS
# =========================================================================
# Confidence: confirmed = verified from official/public source
#             plausible = credible inference with partial corroboration
#             unverified = lead without enough evidence
# =========================================================================

persons = [
    # ── 临川区 Party Secretary (区委书记) ──
    # NOTE: As of July 2026, the name of the current 临川区委书记 requires
    # verification from official sources. Previous known officeholders include
    # 吴宜文 (who moved to Fuzhou vice mayor). The current officeholder may
    # have been appointed in 2024-2025. Marking as [待核实].
    {
        "id": 1,
        "name": "【待核实】",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "临川区委书记",
        "current_org": "中共抚州市临川区委员会",
        "source": "需从临川区政府网站或抚州市委组织部任前公示核实"
    },

    # ── 临川区 District Mayor (区长) ──
    # NOTE: Same situation — current 区长 name requires verification.
    # Previous recent officeholders include 李群力 (prior, and others).
    # Marking as [待核实] until confirmed from official sources.
    {
        "id": 2,
        "name": "【待核实】",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "临川区区长",
        "current_org": "临川区人民政府",
        "source": "需从临川区政府网站或抚州市委组织部任前公示核实"
    },

    # ── City-level leadership (抚州市) ──
    # 范小林 — 抚州市委书记 (confirmed from jxfz.gov.cn)
    {
        "id": 3,
        "name": "范小林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-12",
        "birthplace": "江西宜丰",
        "education": "中央党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "抚州市委书记",
        "current_org": "中共抚州市委员会",
        "source": "https://www.jxfz.gov.cn (verified 2026-07); https://www.thepaper.cn/newsDetail_forward_29115114"
    },

    # 胡剑飞 — 抚州市委副书记、市长 (confirmed from jxfz.gov.cn)
    {
        "id": 4,
        "name": "胡剑飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "抚州市委副书记、市长",
        "current_org": "抚州市人民政府",
        "source": "https://www.jxfz.gov.cn (verified 2026-07-15; featured in news as '市委副书记、市长')"
    },

    # 彭银贵 — 抚州市委常委、政法委书记
    {
        "id": 5,
        "name": "彭银贵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "抚州市委常委、政法委书记",
        "current_org": "中共抚州市委政法委员会",
        "source": "https://www.jxfz.gov.cn (verified 2026-07 via build_fuzhou_data.py)"
    },

    # 王宏安 — 抚州市人大常委会主任
    # (Note: confirmed via jxfz.gov.cn news on 2026-07-13: "王宏安讲授树立和践行正确政绩观学习教育专题党课")
    {
        "id": 6,
        "name": "王宏安",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969-08",
        "birthplace": "江西彭泽",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "抚州市人大常委会主任",
        "current_org": "抚州市人大常委会",
        "source": "https://www.jxfz.gov.cn (news: '王宏安讲授树立和践行正确政绩观学习教育专题党课' 2026-07-13); http://district.ce.cn/newarea/sddy/202501/23/t20250123_39286517.shtml"
    },
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================

organizations = [
    {
        "id": 1,
        "name": "中共抚州市临川区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共抚州市委员会",
        "location": "江西省抚州市临川区"
    },
    {
        "id": 2,
        "name": "临川区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "抚州市人民政府",
        "location": "江西省抚州市临川区"
    },
    {
        "id": 3,
        "name": "中共抚州市委员会",
        "type": "党委",
        "level": "地级",
        "parent": "中共江西省委",
        "location": "江西省抚州市"
    },
    {
        "id": 4,
        "name": "抚州市人民政府",
        "type": "政府",
        "level": "地级",
        "parent": "江西省人民政府",
        "location": "江西省抚州市"
    },
    {
        "id": 5,
        "name": "中共抚州市委政法委员会",
        "type": "党委部门",
        "level": "县处级",
        "parent": "中共抚州市委员会",
        "location": "江西省抚州市"
    },
    {
        "id": 6,
        "name": "抚州市人大常委会",
        "type": "人大",
        "level": "地级",
        "parent": "江西省人大常委会",
        "location": "江西省抚州市"
    },
]

# =========================================================================
# POSITIONS
# =========================================================================

positions = [
    # 临川区委书记 (current)
    {"id": 1, "person_id": 1, "org_id": 1, "title": "临川区委书记",
     "start": "", "end": "", "rank": "县处级正职",
     "note": "现任 — 姓名和具体任职时间待核实"},

    # 临川区区长 (current)
    {"id": 2, "person_id": 2, "org_id": 2, "title": "临川区区长",
     "start": "", "end": "", "rank": "县处级正职",
     "note": "现任 — 姓名和具体任职时间待核实"},

    # 范小林 — 抚州市委书记
    {"id": 3, "person_id": 3, "org_id": 3, "title": "抚州市委书记",
     "start": "2024-10", "end": "", "rank": "正厅级",
     "note": "2024年10月省委任命，接替被查的魏晓奎；经jxfz.gov.cn确认2026年7月仍在任"},

    # 胡剑飞 — 抚州市长
    {"id": 4, "person_id": 4, "org_id": 4, "title": "抚州市委副书记、市长",
     "start": "", "end": "", "rank": "正厅级",
     "note": "2026年7月15日从jxfz.gov.cn新闻确认在职；分管市政府全面工作"},

    # 彭银贵 — 政法委书记
    {"id": 5, "person_id": 5, "org_id": 5, "title": "抚州市委常委、政法委书记",
     "start": "", "end": "", "rank": "副厅级",
     "note": "经build_fuzhou_data.py和jxfz.gov.cn确认在职"},

    # 王宏安 — 人大主任
    {"id": 6, "person_id": 6, "org_id": 6, "title": "抚州市人大常委会主任",
     "start": "", "end": "", "rank": "正厅级",
     "note": "2026年7月13日新闻确认在职；是否曾兼任市长待核实"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================

relationships = [
    # 区委书记 ↔ 区长 (党政搭档)
    {"id": 1, "person_a_id": 1, "person_b_id": 2, "type": "党政搭档",
     "context": "临川区委书记与区长为区一级党政一把手搭档关系",
     "overlap_org": "临川区",
     "overlap_period": ""},

    # 范小林 ↔ 临川区委书记 (上下级)
    {"id": 2, "person_a_id": 3, "person_b_id": 1, "type": "上下级",
     "context": "范小林（抚州市委书记）领导临川区委书记",
     "overlap_org": "抚州市",
     "overlap_period": "2024-10至今"},

    # 胡剑飞 ↔ 临川区区长 (上下级)
    {"id": 3, "person_a_id": 4, "person_b_id": 2, "type": "上下级",
     "context": "胡剑飞（抚州市长）与临川区区长为政府系统上下级关系",
     "overlap_org": "抚州市",
     "overlap_period": ""},
]

# =========================================================================
# BUILD SQLite DATABASE
# =========================================================================

if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
CREATE TABLE persons (
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

CREATE TABLE organizations (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT,
    level TEXT,
    parent TEXT,
    location TEXT
);

CREATE TABLE positions (
    id INTEGER PRIMARY KEY,
    person_id INTEGER NOT NULL,
    org_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    start TEXT,
    end TEXT,
    rank TEXT,
    note TEXT,
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
);

CREATE TABLE relationships (
    id INTEGER PRIMARY KEY,
    person_a_id INTEGER NOT NULL,
    person_b_id INTEGER NOT NULL,
    type TEXT NOT NULL,
    context TEXT,
    overlap_org TEXT,
    overlap_period TEXT,
    FOREIGN KEY (person_a_id) REFERENCES persons(id),
    FOREIGN KEY (person_b_id) REFERENCES persons(id)
);
""")

for p in persons:
    cur.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                 p["birthplace"], p["education"], p["party_join"], p["work_start"],
                 p["current_post"], p["current_org"], p["source"]))

for o in organizations:
    cur.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""",
                (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for pos in positions:
    cur.execute("""INSERT INTO positions VALUES (?,?,?,?,?,?,?,?)""",
                (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
                 pos["start"], pos["end"], pos["rank"], pos["note"]))

for r in relationships:
    cur.execute("""INSERT INTO relationships VALUES (?,?,?,?,?,?,?)""",
                (r["id"], r["person_a_id"], r["person_b_id"], r["type"],
                 r["context"], r["overlap_org"], r["overlap_period"]))

conn.commit()

cur.execute("SELECT COUNT(*) FROM persons")
person_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM organizations")
org_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM positions")
pos_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM relationships")
rel_count = cur.fetchone()[0]

conn.close()
print(f"SQLite database written: {DB_PATH}")
print(f"  Persons: {person_count}")
print(f"  Organizations: {org_count}")
print(f"  Positions: {pos_count}")
print(f"  Relationships: {rel_count}")

# =========================================================================
# BUILD GEXF GRAPH
# =========================================================================

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    post = p.get("current_post", "") or ""
    if "区委书记" in post:
        return (255, 50, 50)      # Red — Party Secretary
    if "区长" in post and "副" not in post:
        return (50, 100, 255)     # Blue — Gov Leader
    if "市委书记" in post:
        return (255, 50, 50)      # Red — Prefecture Party Secretary
    if "市长" in post and "副" not in post:
        return (50, 100, 255)     # Blue — Prefecture Mayor
    if "政法委" in post:
        return (150, 200, 230)
    if "人大" in post:
        return (200, 255, 255)    # Cyan — 人大
    return (100, 100, 100)


def person_size(p):
    """Top leaders larger."""
    # 区委书记, 区长, 市委书记, 市长
    if p["id"] in [1, 2, 3, 4]:
        return 20.0
    return 12.0


def org_color(o):
    colors = {
        "党委": (255, 200, 200),      # Pink
        "政府": (200, 200, 255),      # Light blue
        "党委部门": (255, 200, 200),  # Pink
        "人大": (200, 255, 255),      # Cyan
    }
    return colors.get(o["type"], (200, 200, 200))


lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{TODAY}">')
lines.append('    <creator>china-gov-network skill</creator>')
lines.append('    <description>江西省抚州市临川区领导班子工作关系网络 - 2026年7月15日生成</description>')
lines.append('    <description>注意：区委书记和区长的具体姓名因网络访问限制暂未确认，标记为【待核实】</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# ── Attributes ──
lines.append('    <attributes class="node">')
lines.append('      <attribute id="type" title="Type" type="string"/>')
lines.append('      <attribute id="category" title="Category" type="string"/>')
lines.append('      <attribute id="birth" title="Birth" type="string"/>')
lines.append('      <attribute id="birthplace" title="Birthplace" type="string"/>')
lines.append('      <attribute id="education" title="Education" type="string"/>')
lines.append('      <attribute id="current_post" title="Current Post" type="string"/>')
lines.append('      <attribute id="source" title="Source" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="type" title="Type" type="string"/>')
lines.append('      <attribute id="context" title="Context" type="string"/>')
lines.append('      <attribute id="period" title="Period" type="string"/>')
lines.append('    </attributes>')

# ── Nodes: Persons ──
lines.append('    <nodes>')
for p in persons:
    r, g, b = person_color(p)
    sz = person_size(p)
    lines.append(f'      <node id="{p["id"]}" label="{esc(p["name"])}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="person"/>')
    lines.append(f'          <attvalue for="category" value="person"/>')
    lines.append(f'          <attvalue for="birth" value="{esc(p["birth"])}"/>')
    lines.append(f'          <attvalue for="birthplace" value="{esc(p["birthplace"])}"/>')
    lines.append(f'          <attvalue for="education" value="{esc(p["education"])}"/>')
    lines.append(f'          <attvalue for="current_post" value="{esc(p["current_post"])}"/>')
    lines.append(f'          <attvalue for="source" value="{esc(p["source"])}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append(f'      </node>')

# ── Nodes: Organizations ──
for o in organizations:
    oid = 1000 + o["id"]
    r, g, b = org_color(o)
    lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="org"/>')
    lines.append(f'          <attvalue for="category" value="{esc(o["type"])}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append(f'      </node>')
lines.append('    </nodes>')

# ── Edges ──
lines.append('    <edges>')
edge_id = 1

# person→organization (worked_at)
for pos in positions:
    oid = 1000 + pos["org_id"]
    lines.append(f'      <edge id="{edge_id}" source="{pos["person_id"]}" target="{oid}" label="worked_at">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="worked_at"/>')
    lines.append(f'          <attvalue for="context" value="{esc(pos["title"])}"/>')
    lines.append(f'          <attvalue for="period" value="{pos["start"] or "?"} → {pos["end"] or "今"}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'      </edge>')
    edge_id += 1

# person↔person (relationships)
for r in relationships:
    lines.append(f'      <edge id="{edge_id}" source="{r["person_a_id"]}" target="{r["person_b_id"]}" label="{esc(r["type"])}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="{esc(r["type"])}"/>')
    lines.append(f'          <attvalue for="context" value="{esc(r["context"])}"/>')
    lines.append(f'          <attvalue for="period" value="{r["overlap_period"]}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'      </edge>')
    edge_id += 1

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

total_nodes = len(persons) + len(organizations)
total_edges = len(positions) + len(relationships)
print(f"\nGEXF graph written: {GEXF_PATH}")
print(f"  Nodes: {len(persons)} persons + {len(organizations)} organizations = {total_nodes} total")
print(f"  Edges: {len(positions)} worked_at + {len(relationships)} relationships = {total_edges} total")
print("\nDone!")
