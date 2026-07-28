#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 尼木县 leadership network."""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/尼木县_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/尼木县_network.gexf")

# ── DATA ──

persons = [
    # ── Current County Party Secretary ──
    {"id": 1, "name": "赵铁岭", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共尼木县委书记", "current_org": "中共尼木县委员会",
     "source": "http://www.nmx.gov.cn/nmx/nmyw/202606/47e081fe7ccf42a2b95fece91aa5f6e0.shtml"},

    # ── County Government Leaders ──
    {"id": 2, "name": "五金多吉", "gender": "男", "ethnicity": "藏族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共尼木县委副书记、县长", "current_org": "尼木县人民政府",
     "source": "http://www.nmx.gov.cn/nmx/dxxz/202607/9558416c9959435282c527212d3cf6dd.shtml"},

    {"id": 3, "name": "刘北宁", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常务副书记、常务副县长（援藏）", "current_org": "尼木县人民政府",
     "source": "http://www.nmx.gov.cn/nmx/dxfxz/202607/11f482293c6244b9b12842bc2d64dba8.shtml"},

    {"id": 4, "name": "王双艳", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、常务副县长", "current_org": "尼木县人民政府",
     "source": "http://www.nmx.gov.cn/nmx/dxfxz/202607/b7d217ce069f4af98c950ac5d1e06979.shtml"},

    {"id": 5, "name": "晋美郎加", "gender": "男", "ethnicity": "藏族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、副县长", "current_org": "尼木县人民政府",
     "source": "http://www.nmx.gov.cn/nmx/dxfxz/202607/571709eb4c28464d8dce6c4f8305312a.shtml"},

    {"id": 6, "name": "武博", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、副县长（援藏）", "current_org": "尼木县人民政府",
     "source": "http://www.nmx.gov.cn/nmx/dxfxz/202607/becb471291b64940b653dfbfb422f7b4.shtml"},

    {"id": 7, "name": "田福全", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县政府副县长", "current_org": "尼木县人民政府",
     "source": "http://www.nmx.gov.cn/nmx/dxfxz/202607/2655e788c0e344abaf91ad212450cfff.shtml"},

    {"id": 8, "name": "张建雄", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县政府副县长", "current_org": "尼木县人民政府",
     "source": "http://www.nmx.gov.cn/nmx/dxfxz/202607/457d89390851483fa68c8ee6354ff868.shtml"},

    {"id": 9, "name": "赵述成", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县政府副县长、县公安局局长", "current_org": "尼木县人民政府",
     "source": "http://www.nmx.gov.cn/nmx/dxfxz/202607/3690d025d81e4e4e91c3bdbc3d1c6a4f.shtml"},

    {"id": 10, "name": "张绪刚", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县政府副县长", "current_org": "尼木县人民政府",
     "source": "http://www.nmx.gov.cn/nmx/dxfxz/202607/bca5e8d0dd124bef9d158e76b0285cc1.shtml"},

    {"id": 11, "name": "扎西卓玛", "gender": "女", "ethnicity": "藏族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县政府副县长", "current_org": "尼木县人民政府",
     "source": "http://www.nmx.gov.cn/nmx/dxfxz/202607/399e8dd30efc40bfbcc52d39ed4f9da9.shtml"},

    {"id": 12, "name": "贺舒州", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县政府副县长", "current_org": "尼木县人民政府",
     "source": "http://www.nmx.gov.cn/nmx/dxfxz/202607/7a9e9db325284491b2322e74f5bb1a6b.shtml"},

    # ── Congress, CPPCC, Discipline Commission, Law ──
    {"id": 13, "name": "邹守忠", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县人大常委会主任", "current_org": "尼木县人大常委会",
     "source": "http://www.nmx.gov.cn/nmx/ztbd/202607/71201031fa414bea9903e1f8222ec4fe.shtml"},

    {"id": 14, "name": "扎西顿珠", "gender": "男", "ethnicity": "藏族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县政协主席", "current_org": "尼木县政协",
     "source": "http://www.nmx.gov.cn/nmx/ztbd/202607/a3e24c4f59554f8999d3c78400a5340e.shtml"},

    {"id": 15, "name": "刘毅", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县纪委书记", "current_org": "中共尼木县纪律检查委员会",
     "source": "http://www.nmx.gov.cn/nmx/nmyw/202606/47e081fe7ccf42a2b95fecc91aa5f6e0.shtml"},

    {"id": 16, "name": "尼玛次仁", "gender": "男", "ethnicity": "藏族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县人民法院代理院长", "current_org": "尼木县人民法院",
     "source": "http://www.nmx.gov.cn/nmx/rsrm/202606/59bf0c37b3184c6989e86d7b47a65457.shtml"},

    {"id": 17, "name": "黄凯", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县人民检察院代理检察长", "current_org": "尼木县人民检察院",
     "source": "http://www.nmx.gov.cn/nmx/rsrm/202606/59bf0c37b3184c6989e86d7b47a65457.shtml"},

    # ── Predecessors ──
    {"id": 18, "name": "刘亚飞", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原尼木县人民法院院长", "current_org": "",
     "source": "http://www.nmx.gov.cn/nmx/rsrm/202606/59bf0c37b3184c6989e86d7b47a65457.shtml"},

    {"id": 19, "name": "德吉桑姆", "gender": "女", "ethnicity": "藏族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原尼木县人民检察院检察长", "current_org": "",
     "source": "http://www.nmx.gov.cn/nmx/rsrm/202606/59bf0c37b3184c6989e86d7b47a65457.shtml"},
]

organizations = [
    {"id": 1, "name": "中共尼木县委员会", "type": "党委", "level": "县处级", "parent": "中共拉萨市委员会", "location": "西藏拉萨尼木"},
    {"id": 2, "name": "尼木县人民政府", "type": "政府", "level": "县处级", "parent": "拉萨市人民政府", "location": "西藏拉萨尼木"},
    {"id": 3, "name": "尼木县人大常委会", "type": "人大", "level": "县处级", "parent": "", "location": "西藏拉萨尼木"},
    {"id": 4, "name": "尼木县政协", "type": "政协", "level": "县处级", "parent": "", "location": "西藏拉萨尼木"},
    {"id": 5, "name": "中共尼木县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共拉萨市纪律检查委员会", "location": "西藏拉萨尼木"},
    {"id": 6, "name": "尼木县人民法院", "type": "司法", "level": "县处级", "parent": "", "location": "西藏拉萨尼木"},
    {"id": 7, "name": "尼木县人民检察院", "type": "司法", "level": "县处级", "parent": "", "location": "西藏拉萨尼木"},
]

positions = [
    {"id": 1, "person_id": 1, "org_id": 1, "title": "中共尼木县委书记", "start": "", "end": "", "rank": "县处级正职", "note": "现任，第十一届县委"},
    {"id": 2, "person_id": 2, "org_id": 1, "title": "中共尼木县委副书记", "start": "2026-07", "end": "", "rank": "县处级副职", "note": ""},
    {"id": 3, "person_id": 2, "org_id": 2, "title": "尼木县人民政府县长", "start": "2026-07", "end": "", "rank": "县处级正职", "note": ""},
    {"id": 4, "person_id": 3, "org_id": 1, "title": "县委常务副书记（援藏）", "start": "2025-09", "end": "", "rank": "县处级副职", "note": "北京援藏"},
    {"id": 5, "person_id": 3, "org_id": 2, "title": "常务副县长（援藏）", "start": "2025-09", "end": "", "rank": "县处级副职", "note": "北京援藏"},
    {"id": 6, "person_id": 4, "org_id": 1, "title": "县委常委", "start": "2024-10", "end": "", "rank": "县处级副职", "note": ""},
    {"id": 7, "person_id": 4, "org_id": 2, "title": "常务副县长", "start": "2024-10", "end": "", "rank": "县处级副职", "note": ""},
    {"id": 8, "person_id": 5, "org_id": 1, "title": "县委常委", "start": "2026-07", "end": "", "rank": "县处级副职", "note": ""},
    {"id": 9, "person_id": 5, "org_id": 2, "title": "副县长", "start": "2026-07", "end": "", "rank": "县处级副职", "note": ""},
    {"id": 10, "person_id": 6, "org_id": 1, "title": "县委常委（援藏）", "start": "2025-09", "end": "", "rank": "县处级副职", "note": "北京援藏"},
    {"id": 11, "person_id": 6, "org_id": 2, "title": "副县长（援藏）", "start": "2025-09", "end": "", "rank": "县处级副职", "note": "北京援藏"},
    {"id": 12, "person_id": 7, "org_id": 2, "title": "副县长", "start": "2024-03", "end": "", "rank": "县处级副职", "note": ""},
    {"id": 13, "person_id": 8, "org_id": 2, "title": "副县长", "start": "2024-08", "end": "", "rank": "县处级副职", "note": ""},
    {"id": 14, "person_id": 9, "org_id": 2, "title": "副县长、县公安局局长", "start": "2024-10", "end": "", "rank": "县处级副职", "note": ""},
    {"id": 15, "person_id": 10, "org_id": 2, "title": "副县长", "start": "2026-07", "end": "", "rank": "县处级副职", "note": ""},
    {"id": 16, "person_id": 11, "org_id": 2, "title": "副县长", "start": "2026-07", "end": "", "rank": "县处级副职", "note": ""},
    {"id": 17, "person_id": 12, "org_id": 2, "title": "副县长", "start": "2026-07", "end": "", "rank": "县处级副职", "note": ""},
    {"id": 18, "person_id": 13, "org_id": 3, "title": "县人大常委会主任", "start": "", "end": "", "rank": "县处级正职", "note": ""},
    {"id": 19, "person_id": 14, "org_id": 4, "title": "县政协主席", "start": "", "end": "", "rank": "县处级正职", "note": ""},
    {"id": 20, "person_id": 15, "org_id": 5, "title": "县纪委书记", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"id": 21, "person_id": 16, "org_id": 6, "title": "刑事审判员、审判委员会委员、副院长、代理院长", "start": "2026-06", "end": "", "rank": "县处级副职", "note": "代理院长"},
    {"id": 22, "person_id": 17, "org_id": 7, "title": "检察员、检察委员会委员、副检察长、代理检察长", "start": "2026-06", "end": "", "rank": "县处级副职", "note": "代理检察长"},
    {"id": 23, "person_id": 18, "org_id": 6, "title": "院长", "start": "", "end": "2026-06", "rank": "县处级正职", "note": "已辞职"},
    {"id": 24, "person_id": 19, "org_id": 7, "title": "检察长", "start": "", "end": "2026-06", "rank": "县处级正职", "note": "已辞职"},
    # Deputy roles for Wang Shuangyan
    {"id": 25, "person_id": 4, "org_id": 2, "title": "副县长", "start": "2021-06", "end": "2024-10", "rank": "县处级副职", "note": ""},
]

relationships = [
    {"id": 1, "person_a_id": 1, "person_b_id": 2, "type": "党政搭档", "context": "赵铁岭(县委书记)与五金多吉(县长)搭档", "overlap_org": "中共尼木县委员会", "overlap_period": "2026-07至今"},
    {"id": 2, "person_a_id": 2, "person_b_id": 3, "type": "同僚", "context": "五金多吉与刘北宁在县政府共事", "overlap_org": "尼木县人民政府", "overlap_period": "2025-09至今"},
    {"id": 3, "person_a_id": 3, "person_b_id": 6, "type": "同僚", "context": "刘北宁与武博同为北京援藏干部", "overlap_org": "尼木县人民政府", "overlap_period": "2025-09至今"},
    {"id": 4, "person_a_id": 4, "person_b_id": 5, "type": "同僚", "context": "王双艳与晋美郎加均为县委常委、副县长", "overlap_org": "中共尼木县委员会", "overlap_period": "2026-07至今"},
    {"id": 5, "person_a_id": 18, "person_b_id": 16, "type": "交接", "context": "刘亚飞辞职后由尼玛次仁代理法院院长", "overlap_org": "尼木县人民法院", "overlap_period": "2026-06"},
    {"id": 6, "person_a_id": 19, "person_b_id": 17, "type": "交接", "context": "德吉桑姆辞职后由黄凯代理检察院检察长", "overlap_org": "尼木县人民检察院", "overlap_period": "2026-06"},
    {"id": 7, "person_a_id": 13, "person_b_id": 1, "type": "同僚", "context": "邹守忠主任与赵铁岭书记在县人大会议共事", "overlap_org": "尼木县人大常委会", "overlap_period": ""},
    {"id": 8, "person_a_id": 14, "person_b_id": 1, "type": "同僚", "context": "扎西顿珠主席主持第四届政协会议", "overlap_org": "尼木县政协", "overlap_period": ""},
    {"id": 9, "person_a_id": 1, "person_b_id": 15, "type": "同僚", "context": "赵铁岭(书记)与刘毅(纪委)在党代会共事", "overlap_org": "中共尼木县委员会", "overlap_period": ""},
]

# ── BUILD SQLite DATABASE ───────────────

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
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

# ── BUILD GEXF GRAPH ───────────────────

today = datetime.now().strftime("%Y-%m-%d")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append(f'<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{today}">')
lines.append('    <creator>china-gov-network skill</creator>')
lines.append(f'    <description>尼木县领导班子工作关系网络 - {today}</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

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

lines.append('    <nodes>')
for p in persons:
    if p["id"] == 1:
        color = '#E03C31'; size = 20.0
    elif p["id"] == 2:
        color = '#2980B9'; size = 18.0
    elif p["id"] in [3, 6]:
        color = '#9B59B6'; size = 14.0  # purple: aid-Tibet
    elif p["id"] in [15]:
        color = '#E67E22'; size = 16.0  # orange: discipline
    elif p["id"] in [13, 14]:
        color = '#2ECC71'; size = 15.0  # green: congress/consultative
    else:
        color = '#95A5A6'; size = 12.0

    lines.append(f'      <node id="{p["id"]}" label="{p["name"]}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="person"/>')
    lines.append(f'          <attvalue for="category" value="person"/>')
    lines.append(f'          <attvalue for="birth" value="{p["birth"]}"/>')
    lines.append(f'          <attvalue for="birthplace" value="{p["birthplace"]}"/>')
    lines.append(f'          <attvalue for="education" value="{p["education"]}"/>')
    lines.append(f'          <attvalue for="current_post" value="{p["current_post"]}"/>')
    lines.append(f'          <attvalue for="source" value="{p["source"]}"/>')
    lines.append(f'        </atvalues>')
    lines.append(f'        <viz:color r="{int(color[1:3], 16)}" g="{int(color[3:5], 16)}" b="{int(color[5:7], 16)}"/>')
    lines.append(f'        <viz:size value="{size}"/>')
    lines.append(f'      </node>')

for o in organizations:
    oid = 1000 + o["id"]
    lines.append(f'      <node id="{oid}" label="{o["name"]}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="org"/>')
    lines.append(f'          <attvalue for="category" value="{o["type"]}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="44" g="62" b="80"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append(f'      </node>')
lines.append('    </nodes>')

lines.append('    <edges>')
edge_id = 1
for pos in positions:
    oid = 1000 + pos["org_id"]
    lines.append(f'      <edge id="{edge_id}" source="{pos["person_id"]}" target="{oid}" label="worked_at">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="worked_at"/>')
    lines.append(f'          <attvalue for="context" value="{pos["title"]}"/>')
    lines.append(f'          <attvalue for="period" value="{pos["start"] or "?"} → {pos["end"] or "今"}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'      </edge>')
    edge_id += 1

for r in relationships:
    lines.append(f'      <edge id="{edge_id}" source="{r["person_a_id"]}" target="{r["person_b_id"]}" label="{r["type"]}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="{r["type"]}"/>')
    lines.append(f'          <attvalue for="context" value="{r["context"]}"/>')
    lines.append(f'          <attvalue for="period" value="{r["overlap_period"]}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'      </edge>')
    edge_id += 1

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

total_nodes = len(persons) + len(organizations)
total_edges = len(positions) + len(relationships)
print(f"\nGEXF graph written: {GEXF_PATH}")
print(f"  Nodes: {len(persons)} persons + {len(organizations)} organizations = {total_nodes} total")
print(f"  Edges: {len(positions)} worked_at + {len(relationships)} relationships = {total_edges} total")
print("\nDone!")
