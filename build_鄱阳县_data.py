#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 鄱阳县 (Poyang County) leadership network.

上饶市鄱阳县 — county-level administrative division of Shangrao City, Jiangxi Province.
鄱阳县是江西省第一人口大县、第二地域大县，省直管县体制改革试点。
古称番邑、饶州，鄱阳湖因县而得名。

Targets: 县委书记 & 县长

Current leadership (as of 2026-07, sourced from Baidu Baike):
- 县委书记: 李小平
- 县委副书记、县长候选人: 徐光
- 县人大常委会主任: 汤丁山
- 县政协主席: 江俊

⚠️ 网络环境限制：大部分外部网站（百度百科人物页、政府网站、新闻网站）不可达。
   当前姓名来自鄱阳县百度百科词条（2026-07-15可访问）。
   详细履历需在上饶市委组织部任前公示或鄱阳县政府官网领导之窗可访问时补充。

Research date: 2026-07-15
"""

import sqlite3, os, sys
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/jiangxi_鄱阳县")
DB_PATH = os.path.join(STAGING, "鄱阳县_network.db")
GEXF_PATH = os.path.join(STAGING, "鄱阳县_network.gexf")

os.makedirs(STAGING, exist_ok=True)

# The training_dir variable is used for process_tmp validation
training_dir = STAGING

# =========================================================================
# PERSONS
# =========================================================================

persons = [
    # ── Current party secretary (县委书记) ──
    {
        "id": 1,
        "name": "李小平",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "鄱阳县委书记",
        "current_org": "中共鄱阳县委员会",
        "source": "Baidu Baike — 鄱阳县词条（2026-07-15访问）。确认李小平为现任鄱阳县委书记。详细履历待查。"
    },

    # ── Current county mayor candidate (县长候选人) ──
    {
        "id": 2,
        "name": "徐光",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "鄱阳县委副书记、县长候选人",
        "current_org": "鄱阳县人民政府",
        "source": "Baidu Baike — 鄱阳县词条（2026-07-15访问）。标注为'县委副书记、县长候选人'，可能为代县长或已当选。"
    },

    # ── County People's Congress Director (县人大常委会主任) ──
    {
        "id": 3,
        "name": "汤丁山",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "鄱阳县人大常委会主任",
        "current_org": "鄱阳县人民代表大会常务委员会",
        "source": "Baidu Baike — 鄱阳县词条（2026-07-15访问）。"
    },

    # ── County CPPCC Chair (县政协主席) ──
    {
        "id": 4,
        "name": "江俊",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "鄱阳县政协主席",
        "current_org": "政协鄱阳县委员会",
        "source": "Baidu Baike — 鄱阳县词条（2026-07-15访问）。"
    },

    # ── Previous party secretary (predecessor, inferred from historical data) ──
    # Note: 鄱阳县前任县委书记姓名暂未确认
    {
        "id": 5,
        "name": "（待确认）前任鄱阳县委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（待核实）",
        "current_org": "（待核实）",
        "source": "待确认 — 李小平的前任。需通过上饶市人大常委会公告、鄱阳县委宣传部历史新闻或江西省组织部任前公示核实。"
    },
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================

organizations = [
    # ── 鄱阳县核心机构 ──
    {"id": 1, "name": "中共鄱阳县委员会", "type": "党委", "level": "县级",
     "parent": "中共上饶市委员会", "location": "江西省上饶市鄱阳县"},
    {"id": 2, "name": "鄱阳县人民政府", "type": "政府", "level": "县级",
     "parent": "上饶市人民政府", "location": "江西省上饶市鄱阳县"},
    {"id": 3, "name": "鄱阳县人民代表大会常务委员会", "type": "人大", "level": "县级",
     "parent": "上饶市人大常委会", "location": "江西省上饶市鄱阳县"},
    {"id": 4, "name": "政协鄱阳县委员会", "type": "政协", "level": "县级",
     "parent": "政协上饶市委员会", "location": "江西省上饶市鄱阳县"},
    {"id": 5, "name": "中共鄱阳县纪律检查委员会", "type": "党委", "level": "县级",
     "parent": "中共鄱阳县委员会", "location": "江西省上饶市鄱阳县"},
    {"id": 6, "name": "中共鄱阳县委组织部", "type": "党委", "level": "县级",
     "parent": "中共鄱阳县委员会", "location": "江西省上饶市鄱阳县"},
    {"id": 7, "name": "中共鄱阳县委宣传部", "type": "党委", "level": "县级",
     "parent": "中共鄱阳县委员会", "location": "江西省上饶市鄱阳县"},
    {"id": 8, "name": "中共鄱阳县委政法委员会", "type": "党委", "level": "县级",
     "parent": "中共鄱阳县委员会", "location": "江西省上饶市鄱阳县"},

    # ── 上饶市（上级） ──
    {"id": 9, "name": "中共上饶市委员会", "type": "党委", "level": "地市级",
     "parent": "中共江西省委员会", "location": "江西省上饶市"},
    {"id": 10, "name": "上饶市人民政府", "type": "政府", "level": "地市级",
     "parent": "江西省人民政府", "location": "江西省上饶市"},
]

# =========================================================================
# POSITIONS (current known roles)
# =========================================================================

positions = [
    # 李小平 — current roles
    {"id": 1, "person_id": 1, "org_id": 1,
     "title": "鄱阳县委书记", "start": "（待核实）", "end": "",
     "rank": "正处级", "note": "现任鄱阳县委书记。到任时间及此前任职待查。"},

    # 徐光 — current roles
    {"id": 2, "person_id": 2, "org_id": 1,
     "title": "鄱阳县委副书记", "start": "（待核实）", "end": "",
     "rank": "正处级", "note": "现任鄱阳县委副书记。"},
    {"id": 3, "person_id": 2, "org_id": 2,
     "title": "县长候选人", "start": "（待核实）", "end": "",
     "rank": "正处级", "note": "县长候选人，推测为代县长或已当选县长。到任时间待查。"},

    # 汤丁山
    {"id": 4, "person_id": 3, "org_id": 3,
     "title": "鄱阳县人大常委会主任", "start": "（待核实）", "end": "",
     "rank": "正处级", "note": ""},

    # 江俊
    {"id": 5, "person_id": 4, "org_id": 4,
     "title": "鄱阳县政协主席", "start": "（待核实）", "end": "",
     "rank": "正处级", "note": ""},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================

relationships = [
    # 李小平 ↔ 徐光（党政搭档）
    {"id": 1, "person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "李小平（县委书记）与徐光（县长候选人）为鄱阳县党政一把手搭档关系",
     "overlap_org": "鄱阳县", "overlap_period": "至今"},

    # 李小平 → 前任（职务接替）
    {"id": 2, "person_a": 5, "person_b": 1, "type": "职务接替",
     "context": "前任鄱阳县委书记（姓名待确认）→ 李小平接任。具体交接时间待核实",
     "overlap_org": "中共鄱阳县委员会", "overlap_period": "不重叠（前后任）"},
]

# =========================================================================
# BUILD SQLITE
# =========================================================================

if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

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
    id INTEGER PRIMARY KEY, person_id INTEGER, org_id INTEGER,
    title TEXT, start TEXT, "end" TEXT, rank TEXT, note TEXT,
    FOREIGN KEY(person_id) REFERENCES persons(id),
    FOREIGN KEY(org_id) REFERENCES organizations(id)
);
CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY, person_a INTEGER, person_b INTEGER,
    type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT,
    FOREIGN KEY(person_a) REFERENCES persons(id),
    FOREIGN KEY(person_b) REFERENCES persons(id)
);
CREATE INDEX IF NOT EXISTS idx_pos_p ON positions(person_id);
CREATE INDEX IF NOT EXISTS idx_pos_o ON positions(org_id);
CREATE INDEX IF NOT EXISTS idx_rel_a ON relationships(person_a);
CREATE INDEX IF NOT EXISTS idx_rel_b ON relationships(person_b);
""")

for p in persons:
    c.execute("INSERT OR REPLACE INTO persons VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
              (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
               p["birthplace"], p["education"], p["party_join"],
               p["work_start"], p["current_post"], p["current_org"], p["source"]))
for o in organizations:
    c.execute("INSERT OR REPLACE INTO organizations VALUES(?,?,?,?,?,?)",
              (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))
for pos in positions:
    c.execute("INSERT OR REPLACE INTO positions VALUES(?,?,?,?,?,?,?,?)",
              (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
               pos["start"], pos["end"], pos["rank"], pos["note"]))
for r in relationships:
    c.execute("INSERT OR REPLACE INTO relationships VALUES(?,?,?,?,?,?,?)",
              (r["id"], r["person_a"], r["person_b"], r["type"],
               r["context"], r["overlap_org"], r["overlap_period"]))
conn.commit()

counts = {}
for t in ["persons", "organizations", "positions", "relationships"]:
    counts[t] = c.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
conn.close()
print(f"SQLite DB: {DB_PATH}")
for t, n in counts.items():
    print(f"  {t}: {n} records")

# =========================================================================
# BUILD GEXF
# =========================================================================

def esc(s):
    if s is None: return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def pcolor(post):
    if "县委书记" in post and "纪委" not in post: return "255,50,50"
    elif "县长" in post or "副县长" in post or "县长候选人" in post: return "50,100,255"
    elif "纪委书记" in post or "监委" in post: return "255,165,0"
    elif "政法委" in post: return "150,100,200"
    elif "宣传部" in post: return "100,200,150"
    elif "组织部" in post: return "200,150,100"
    elif "统战部" in post: return "200,100,150"
    elif "人武部" in post: return "100,150,100"
    elif "人大" in post: return "100,200,200"
    elif "政协" in post: return "200,200,100"
    return "100,100,100"

def ocolor(otype):
    return {"党委":"255,200,200","政府":"200,200,255","人大":"200,255,255",
            "政协":"255,240,200","群团":"255,220,255","事业单位":"220,220,220",
            "开发区":"200,255,200","国企":"255,255,200","军队":"180,180,200"}.get(otype,"200,200,200")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Sisyphus Research Agent</creator>')
lines.append('    <description>江西省上饶市鄱阳县领导班子工作关系网络 — 2026年7月15日生成</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')
lines.append('    <attributes class="node">')
for aid, atitle in [("0","type"),("1","birth"),("2","birthplace"),("3","current_post"),("4","entity_type"),("5","level")]:
    lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
for aid, atitle in [("0","type"),("1","start"),("2","end"),("3","context")]:
    lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
lines.append('    </attributes>')
lines.append('    <nodes>')
for p in persons:
    c = pcolor(p.get("current_post",""))
    post = p.get("current_post","")
    if "县委书记" in post and "纪委" not in post:
        sz = "20.0"
    elif "县长" in post or "县长候选人" in post:
        sz = "20.0"
    elif "副县长" in post:
        sz = "14.0"
    elif "常委" in post or "副书记" in post:
        sz = "12.0"
    elif "人大" in post or "政协" in post:
        sz = "12.0"
    else:
        sz = "12.0"
    lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    for f,v in [("0","person"),("1",p.get("birth","")),("2",p.get("birthplace","")),
                ("3",p.get("current_post","")),("4","person"),("5","")]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')
for o in organizations:
    c = ocolor(o.get("type",""))
    lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    for f,v in [("0","organization"),("1",""),("2",o.get("location","")),("3",""),("4","organization"),("5",o.get("level",""))]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append('      </node>')
lines.append('    </nodes>')
lines.append('    <edges>')
eid = 0
for pos in positions:
    eid += 1
    lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
    lines.append('        <attvalues>')
    for f,v in [("0","worked_at"),("1",pos.get("start","")),("2",pos.get("end","")),("3",pos.get("note",""))]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('      </attvalues>')
    lines.append('      </edge>')
for r in relationships:
    eid += 1
    ov = r.get("overlap_period","")
    ov_s = ov.split("至今")[0] if "至今" in ov else ov
    lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
    lines.append('        <attvalues>')
    for f,v in [("0",r["type"]),("1",ov_s),("2",""),("3",r.get("context",""))]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('      </attvalues>')
    lines.append('      </edge>')
lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')
with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

tn = len(persons) + len(organizations)
te = len(positions) + len(relationships)
print(f"\nGEXF: {GEXF_PATH}")
print(f"  Nodes: {len(persons)} persons + {len(organizations)} orgs = {tn} total")
print(f"  Edges: {len(positions)} worked_at + {len(relationships)} relationships = {te} total")
print("\nDone! ✅ Core leaders identified (李小平/徐光) from Baidu Baike. Detailed biographies need web access to fill.")
