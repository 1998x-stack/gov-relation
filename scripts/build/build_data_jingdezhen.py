#!/usr/bin/env python3
"""
Build SQLite database + GEXF graph for Jingdezhen cadre exchange network.
"""

import sqlite3
import os

DB_PATH = "data/database/jingdezhen_network.db"
GEXF_PATH = "data/graph/jingdezhen_network.gexf"

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# ── Schema ──────────────────────────────────────────────────────────────
cur.executescript("""
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS persons (
    id          INTEGER PRIMARY KEY,
    name        TEXT NOT NULL,
    gender      TEXT,
    ethnicity   TEXT,
    birth       TEXT,
    birthplace  TEXT,
    education   TEXT,
    party_join  TEXT,
    work_start  TEXT,
    current_post    TEXT,
    current_org     TEXT,
    source      TEXT
);

CREATE TABLE IF NOT EXISTS organizations (
    id          INTEGER PRIMARY KEY,
    name        TEXT NOT NULL,
    type        TEXT,
    level       TEXT,
    parent      TEXT,
    location    TEXT
);

CREATE TABLE IF NOT EXISTS positions (
    id          INTEGER PRIMARY KEY,
    person_id   INTEGER NOT NULL,
    org_id      INTEGER NOT NULL,
    title       TEXT NOT NULL,
    start_date  TEXT,
    end_date    TEXT,
    rank        TEXT,
    note        TEXT,
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
);

CREATE TABLE IF NOT EXISTS relationships (
    id          INTEGER PRIMARY KEY,
    person_a    INTEGER NOT NULL,
    person_b    INTEGER NOT NULL,
    type        TEXT,
    context     TEXT,
    overlap_org TEXT,
    overlap_period TEXT,
    FOREIGN KEY (person_a) REFERENCES persons(id),
    FOREIGN KEY (person_b) REFERENCES persons(id)
);
""")

# ── Organizations ───────────────────────────────────────────────────────
orgs = [
    (1, "景德镇市委", "党委", "地级市", "江西省委", "景德镇"),
    (2, "景德镇市政府", "政府", "地级市", "江西省政府", "景德镇"),
    (3, "景德镇市人大常委会", "人大", "地级市", "景德镇市", "景德镇"),
    (4, "景德镇市政协", "政协", "地级市", "景德镇市", "景德镇"),
    (5, "景德镇市纪委监委", "纪委", "地级市", "江西省纪委监委", "景德镇"),
    (6, "江西省委宣传部", "党委部门", "省级", "江西省委", "南昌"),
    (7, "江西省人社厅", "政府部门", "省级", "江西省政府", "南昌"),
    (8, "工信部原材料工业司", "中央部委司局", "司局级", "工信部", "北京"),
    (9, "鹰潭市委", "党委", "地级市", "江西省委", "鹰潭"),
    (10, "鹰潭市政府", "政府", "地级市", "江西省政府", "鹰潭"),
    (11, "鹰潭市纪委监委", "纪委", "地级市", "江西省纪委监委", "鹰潭"),
    (12, "九江市政府", "政府", "地级市", "江西省政府", "九江"),
    (13, "九江市委", "党委", "地级市", "江西省委", "九江"),
    (14, "共青团江西省委", "群团", "省级", "江西省委", "南昌"),
    (15, "景德镇市委政法委", "党委部门", "地级市", "景德镇市委", "景德镇"),
]

cur.executemany("INSERT INTO organizations VALUES (?,?,?,?,?,?)", orgs)

# ── Persons ─────────────────────────────────────────────────────────────
persons = [
    (1, "陈克龙", "男", "汉族", "1976-12", "江西抚州", "工学硕士", None, None,
     "景德镇市委书记", "景德镇市委",
     "https://district.ce.cn/newarea/sddy/202604/t20260427_2932496.shtml"),

    (2, "胡雪梅", "女", "汉族", None, None, None, None, None,
     "江西省委宣传部副部长", "江西省委宣传部",
     "南方都市报 2026-05-05"),

    (3, "刘锋", "男", "汉族", None, None, None, None, None,
     "待查", None,
     "维基百科"),

    (4, "钟志生", "男", "汉族", "1963-06", "江西分宜", "在职研究生/EMBA硕士", "1985-09", "1982-08",
     "被开除党籍/公职", None,
     "https://www.163.com/dy/article/GDHN8K3K0514R9P4.html"),

    (5, "鄢华", "男", "汉族", "1969-10", "安徽无为", "大学", None, None,
     "景德镇市人大常委会主任", "景德镇市人大常委会",
     "http://district.ce.cn/newarea/sddy/202601/t20260124_2724032.shtml"),

    (6, "俞小平", "男", "汉族", "1967-08", None, None, None, None,
     "景德镇市政协主席", "景德镇市政协",
     "维基百科"),

    (7, "曹雄泰", "男", "汉族", None, None, None, None, None,
     "原景德镇市人大常委会主任", None,
     "维基百科"),

    (8, "肖斐杰", "男", "汉族", None, None, None, None, None,
     "景德镇市委常委、政法委书记", "景德镇市委政法委",
     "极目新闻 2025-09-26"),

    (9, "董梅生", "男", "汉族", None, None, None, None, None,
     "景德镇市委常委、纪委书记", "景德镇市纪委监委",
     "江西新闻联播 2025-03-26"),

    (10, "盛璟晶", "女", "汉族", "1970-09", None, "省委党校研究生", None, None,
     "景德镇市人大常委会副主任", "景德镇市人大常委会",
     "http://district.ce.cn/newarea/sddy/202601/t20260124_2724032.shtml"),
]

cur.executemany("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", persons)

# ── Positions ──────────────────────────────────────────────────────────
positions = [
    # 陈克龙
    (1, 1, 8, "工信部原材料工业司司长", "~2021", "~2024", "司局级", "中央部委空降至地方"),
    (2, 1, 2, "景德镇市市长", "~2024", "2026-04", "正厅级", "中央→地方空降"),
    (3, 1, 1, "景德镇市委书记", "2026-04", None, "正厅级", "现任，由市长升任"),

    # 胡雪梅
    (4, 2, 2, "景德镇市市长", "~2021", "2024-09", "正厅级", "任市长约3年"),
    (5, 2, 1, "景德镇市委书记", "2024-09", "2026-04", "正厅级", "由市长升任书记"),
    (6, 2, 6, "江西省委宣传部副部长", "2026-05", None, "正厅级", "卸任市委书记后调任"),

    # 钟志生
    (7, 4, 14, "共青团江西省委书记", "2003-05", "2008-03", "正厅级", ""),
    (8, 4, 10, "鹰潭市代市长、市长", "2008-03", "2013-09", "正厅级", "鹰潭→"),
    (9, 4, 12, "九江市代市长、市长", "2013-09", "2015-08", "正厅级", "→九江→"),
    (10, 4, 1, "景德镇市委书记", "2015-08", "2021-03", "正厅级", "→景德镇"),
    (11, 4, 7, "江西省人社厅党组书记", "2021-03", "2024", "正厅级", "调任省厅"),

    # 鄢华
    (12, 5, 11, "鹰潭市委常委、市纪委书记、市监委主任", None, "2025-12", "副厅级", "从鹰潭调任"),
    (13, 5, 3, "景德镇市人大常委会主任", "2026-01", None, "正厅级", "跨市提拔"),

    # 俞小平
    (14, 6, 4, "景德镇市政协主席", "2021-11", None, "正厅级", "现任"),

    # 曹雄泰
    (15, 7, 3, "景德镇市人大常委会主任", None, "2026-01", "正厅级", "前任"),

    # 肖斐杰
    (16, 8, 15, "景德镇市委常委、市委政法委书记", "2025-09", None, "副厅级", ""),

    # 董梅生
    (17, 9, 5, "景德镇市委常委、市纪委书记", "2025-03", None, "副厅级", ""),

    # 盛璟晶
    (18, 10, 3, "景德镇市人大常委会副主任", "2026-01", None, "副厅级", "本地提拔"),
]

cur.executemany("INSERT INTO positions VALUES (?,?,?,?,?,?,?,?)", positions)

# ── Relationships ───────────────────────────────────────────────────────
relationships = [
    (1, 1, 6, "前后任", "陈克龙接替胡雪梅任景德镇市委书记", "景德镇市委", "2026-04"),
    (2, 2, 3, "前后任", "胡雪梅接替刘锋任景德镇市委书记", "景德镇市委", "2024-09"),
    (3, 2, 4, "前后任", "胡雪梅接替钟志生任景德镇市长（？待核实）", "景德镇市政府", "~2021"),
    (4, 3, 4, "前后任", "刘锋接替钟志生任景德镇市委书记", "景德镇市委", "2021-03"),
    (5, 2, 1, "党政搭档", "胡雪梅（书记）与陈克龙（市长）为党政搭档", "景德镇市", "~2024—2026-04"),
    (6, 4, 9, "前后任", "钟志生继任者鄢华从鹰潭调入景德镇（不同届）", "鹰潭-景德镇", "2008-2026"),
    (7, 5, 7, "前后任", "鄢华接替曹雄泰任人大常委会主任", "景德镇市人大常委会", "2026-01"),
    (8, 4, 8, "前后任", "无直接关系", "江西省", "跨市链：鹰潭→九江→景德镇"),
]

cur.executemany("INSERT INTO relationships VALUES (?,?,?,?,?,?,?)", relationships)

conn.commit()

# ── Summary ─────────────────────────────────────────────────────────────
cur.execute("SELECT COUNT(*) FROM persons")
pc = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM organizations")
oc = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM positions")
psc = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM relationships")
rc = cur.fetchone()[0]
print(f"✅ DB: {pc} persons, {oc} orgs, {psc} positions, {rc} relationships")
conn.close()

# ═══════════════════════════════════════════════════════════════════════
# GEXF
# ═══════════════════════════════════════════════════════════════════════
persons_list = [
    (1, "陈克龙", "市委书记", "red"),
    (2, "胡雪梅", "宣传部副部长（原书记）", "orange"),
    (3, "刘锋", "前市委书记（去向待查）", "grey"),
    (4, "钟志生", "前市委书记（被双开）", "grey"),
    (5, "鄢华", "人大常委会主任", "blue"),
    (6, "俞小平", "政协主席", "grey"),
    (7, "曹雄泰", "原人大常委会主任", "grey"),
    (8, "肖斐杰", "政法委书记", "orange"),
    (9, "董梅生", "纪委书记", "orange"),
    (10, "盛璟晶", "人大常委会副主任", "grey"),
]

orgs_list = [
    (101, "景德镇市委", "党委"),
    (102, "景德镇市政府", "政府"),
    (103, "景德镇市人大常委会", "人大"),
    (104, "景德镇市政协", "政协"),
    (105, "景德镇市纪委监委", "纪委"),
    (106, "江西省委宣传部", "党委部门"),
    (107, "江西省人社厅", "政府部门"),
    (108, "工信部原材料工业司", "中央部委"),
    (109, "鹰潭市纪委监委", "纪委"),
    (110, "鹰潭市政府", "政府"),
    (111, "九江市政府", "政府"),
    (112, "共青团江西省委", "群团"),
    (113, "景德镇市委政法委", "党委部门"),
]

edges = [
    (1, 102, "worked_at", "市长"),
    (1, 101, "worked_at", "市委书记"),
    (1, 108, "worked_at", "工信部原材料司司长"),

    (2, 102, "worked_at", "市长"),
    (2, 101, "worked_at", "市委书记"),
    (2, 106, "worked_at", "省委宣传部副部长"),

    (3, 101, "worked_at", "市委书记"),

    (4, 112, "worked_at", "共青团江西省委书记"),
    (4, 110, "worked_at", "鹰潭市长"),
    (4, 111, "worked_at", "九江市长"),
    (4, 101, "worked_at", "景德镇市委书记"),
    (4, 107, "worked_at", "省人社厅党组书记"),

    (5, 109, "worked_at", "鹰潭市纪委书记"),
    (5, 103, "worked_at", "市人大常委会主任"),

    (6, 104, "worked_at", "市政协主席"),
    (7, 103, "worked_at", "原市人大常委会主任"),
    (8, 113, "worked_at", "市委政法委书记"),
    (9, 105, "worked_at", "市纪委书记"),
    (10, 103, "worked_at", "市人大常委会副主任"),

    # person↔person edges
    (1, 2, "relationship", "前后任/党政搭档"),
    (2, 3, "relationship", "前后任"),
    (2, 4, "relationship", "前后任"),
    (3, 4, "relationship", "前后任"),
    (5, 7, "relationship", "前后任"),
]

# Build GEXF
lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Attributes
lines.append('    <attributes class="node">')
lines.append('      <attribute id="type" title="Type" type="string"/>')
lines.append('      <attribute id="role" title="Role" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="type" title="Edge Type" type="string"/>')
lines.append('      <attribute id="label" title="Label" type="string"/>')
lines.append('    </attributes>')

# Nodes
lines.append('    <nodes>')
for pid, name, role, color in persons_list:
    color_map = {"red": "#E03C31", "orange": "#E8762D", "blue": "#3B6DB5", "grey": "#888888"}
    c = color_map.get(color, "#888888")
    lines.append(f'      <node id="p{pid}" label="{name}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="person"/>')
    lines.append(f'          <attvalue for="role" value="{role}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="{int(c[1:3],16)}" g="{int(c[3:5],16)}" b="{int(c[5:7],16)}"/>')
    lines.append(f'        <viz:size value="20.0"/>')
    lines.append(f'      </node>')

for oid, oname, otype in orgs_list:
    lines.append(f'      <node id="o{oid}" label="{oname}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="organization"/>')
    lines.append(f'          <attvalue for="role" value="{otype}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="100" g="100" b="100"/>')
    lines.append(f'        <viz:size value="10.0"/>')
    lines.append(f'      </node>')

lines.append('    </nodes>')

# Edges
lines.append('    <edges>')
eid = 0
for src, tgt, etype, label in edges:
    eid += 1
    vid1 = f"p{src}"
    vid2 = f"o{tgt}" if etype == "worked_at" else f"p{tgt}"
    color = '"200" g="180" b="50"' if etype == "relationship" else '"150" g="150" b="150"'
    thickness = '3.0' if etype == "relationship" else '1.0'
    lines.append(f'      <edge id="e{eid}" source="{vid1}" target="{vid2}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="{etype}"/>')
    lines.append(f'          <attvalue for="label" value="{label}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r={color}/>')
    lines.append(f'        <viz:thickness value="{thickness}"/>')
    lines.append(f'      </edge>')

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

import os
gbytes = os.path.getsize(GEXF_PATH)
print(f"✅ GEXF: {GEXF_PATH} ({gbytes} bytes)")
print(f"\n📊 Summary: {len(persons_list)} person nodes, {len(orgs_list)} org nodes, {eid} edges")
