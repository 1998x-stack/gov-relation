#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 常州市 (Changzhou City) leadership network.

Covers: City-level leadership (市委书记, 市长, 人大主任, 政协主席, etc.),
6 districts/county-level cities (区委书记 + 区长/书记/市长), predecessors,
and the city-level leadership structure.
"""

import sqlite3, os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/changzhou_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/changzhou_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── City-level leadership — 市委 ──
    # 1. 李佰平 — 常州市委书记 (1975-08, 江苏常州, 2026.07刚就任, 此前在中组部工作)
    {"id":1,"name":"李佰平","gender":"男","ethnicity":"汉族","birth":"1975-08","birthplace":"江苏常州","education":"","party_join":"","work_start":"","current_post":"常州市委书记","current_org":"中共常州市委员会","source":""},
    # 2. 周伟 — 常州市长 (1974-07, 江苏东台, 2024.12任)
    {"id":2,"name":"周伟","gender":"男","ethnicity":"汉族","birth":"1974-07","birthplace":"江苏东台","education":"","party_join":"","work_start":"","current_post":"常州市长","current_org":"常州市人民政府","source":""},
    # 3. 白云萍 — 人大常委会主任 (1964-03, 女, 江苏张家港)
    {"id":3,"name":"白云萍","gender":"女","ethnicity":"汉族","birth":"1964-03","birthplace":"江苏张家港","education":"","party_join":"","work_start":"","current_post":"常州市人大常委会主任","current_org":"常州市人大常委会","source":""},
    # 4. 季培东 — 政协主席 (1966-03)
    {"id":4,"name":"季培东","gender":"男","ethnicity":"汉族","birth":"1966-03","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"常州市政协主席","current_org":"政协常州市委员会","source":""},

    # 5. 陈金虎 — 前市委书记 (1967-12, 江苏句容, 2020-2026.07)
    {"id":5,"name":"陈金虎","gender":"男","ethnicity":"汉族","birth":"1967-12","birthplace":"江苏句容","education":"","party_join":"","work_start":"","current_post":"前常州市委书记","current_org":"中共常州市委员会","source":""},
    # 6. 盛蕾 — 前市长 (女, 2021-2024)
    {"id":6,"name":"盛蕾","gender":"女","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"前常州市长","current_org":"常州市人民政府","source":""},

    # ── District/County-level leadership ──
    # 7. 乔俊杰 — 武进区委书记 (1974-01, 江苏泰兴)
    {"id":7,"name":"乔俊杰","gender":"男","ethnicity":"汉族","birth":"1974-01","birthplace":"江苏泰兴","education":"","party_join":"","work_start":"","current_post":"武进区委书记","current_org":"中共武进区委员会","source":""},
    # 8. 恽淇丞 — 武进区长
    {"id":8,"name":"恽淇丞","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"武进区长","current_org":"武进区人民政府","source":""},
    # 9. 胥亚伟 — 金坛区委书记 (1974-07, 2026.01任)
    {"id":9,"name":"胥亚伟","gender":"男","ethnicity":"汉族","birth":"1974-07","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"金坛区委书记","current_org":"中共金坛区委员会","source":""},
    # 10. 李超鲲 — 溧阳市委书记
    {"id":10,"name":"李超鲲","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"溧阳市委书记","current_org":"中共溧阳市委员会","source":""},
    # 11. 巢彬 — 溧阳市长
    {"id":11,"name":"巢彬","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"溧阳市长","current_org":"溧阳市人民政府","source":""},
    # 12. 汤如军 — 钟楼区长
    {"id":12,"name":"汤如军","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"钟楼区长","current_org":"钟楼区人民政府","source":""},

    # ── 6 Districts — placeholder members for missing data ──
    # 天宁区
    {"id":13,"name":"天宁区委书记","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"天宁区委书记","current_org":"中共天宁区委员会","source":""},
    {"id":14,"name":"天宁区长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"天宁区长","current_org":"天宁区人民政府","source":""},

    # 钟楼区
    {"id":15,"name":"钟楼区委书记","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"钟楼区委书记","current_org":"中共钟楼区委员会","source":""},

    # 新北区
    {"id":16,"name":"新北区委书记","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"新北区委书记","current_org":"中共新北区委员会","source":""},
    {"id":17,"name":"新北区长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"新北区长","current_org":"新北区人民政府","source":""},

    # 金坛区长 (placeholder)
    {"id":18,"name":"金坛区长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"金坛区长","current_org":"金坛区人民政府","source":""},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    # ── Changzhou city-level core ──
    {"id":1,"name":"中共常州市委员会","type":"党委","level":"地级","parent":"中共江苏省委员会","location":"江苏省常州市"},
    {"id":2,"name":"常州市人民政府","type":"政府","level":"地级","parent":"江苏省人民政府","location":"江苏省常州市"},
    {"id":3,"name":"常州市人大常委会","type":"人大","level":"地级","parent":"","location":"江苏省常州市"},
    {"id":4,"name":"政协常州市委员会","type":"政协","level":"地级","parent":"","location":"江苏省常州市"},
    {"id":5,"name":"中共常州市纪律检查委员会","type":"党委","level":"地级","parent":"中共常州市委员会","location":"江苏省常州市"},

    # ── 5 Districts + 1 County-level city — Party committees ──
    {"id":6,"name":"中共天宁区委员会","type":"党委","level":"县级","parent":"中共常州市委员会","location":"江苏省常州市天宁区"},
    {"id":7,"name":"中共钟楼区委员会","type":"党委","level":"县级","parent":"中共常州市委员会","location":"江苏省常州市钟楼区"},
    {"id":8,"name":"中共新北区委员会","type":"党委","level":"县级","parent":"中共常州市委员会","location":"江苏省常州市新北区"},
    {"id":9,"name":"中共武进区委员会","type":"党委","level":"县级","parent":"中共常州市委员会","location":"江苏省常州市武进区"},
    {"id":10,"name":"中共金坛区委员会","type":"党委","level":"县级","parent":"中共常州市委员会","location":"江苏省常州市金坛区"},
    {"id":11,"name":"中共溧阳市委员会","type":"党委","level":"县级","parent":"中共常州市委员会","location":"江苏省常州市溧阳市"},

    # ── 5 Districts + 1 County-level city — Governments ──
    {"id":12,"name":"天宁区人民政府","type":"政府","level":"县级","parent":"常州市人民政府","location":"江苏省常州市天宁区"},
    {"id":13,"name":"钟楼区人民政府","type":"政府","level":"县级","parent":"常州市人民政府","location":"江苏省常州市钟楼区"},
    {"id":14,"name":"新北区人民政府","type":"政府","level":"县级","parent":"常州市人民政府","location":"江苏省常州市新北区"},
    {"id":15,"name":"武进区人民政府","type":"政府","level":"县级","parent":"常州市人民政府","location":"江苏省常州市武进区"},
    {"id":16,"name":"金坛区人民政府","type":"政府","level":"县级","parent":"常州市人民政府","location":"江苏省常州市金坛区"},
    {"id":17,"name":"溧阳市人民政府","type":"政府","level":"县级","parent":"常州市人民政府","location":"江苏省常州市溧阳市"},

    # ── External / other orgs needed ──
    {"id":18,"name":"中共江苏省委员会","type":"党委","level":"省级","parent":"","location":"江苏省南京市"},
    {"id":19,"name":"江苏省人民政府","type":"政府","level":"省级","parent":"","location":"江苏省南京市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # ── 李佰平 ──
    {"id":1,"person_id":1,"org_id":1,"title":"常州市委书记","start":"2026-07","end":"","rank":"副部级","note":"2026.07就任，此前在中组部工作"},
    {"id":2,"person_id":1,"org_id":1,"title":"常州市委副书记","start":"2026-07","end":"","rank":"副部级","note":""},

    # ── 周伟 ──
    {"id":3,"person_id":2,"org_id":2,"title":"常州市长","start":"2024-12","end":"","rank":"副部级","note":"2024.12到任"},
    {"id":4,"person_id":2,"org_id":1,"title":"常州市委副书记","start":"2024-12","end":"","rank":"副部级","note":""},

    # ── 白云萍 ──
    {"id":5,"person_id":3,"org_id":3,"title":"常州市人大常委会主任","start":"","end":"","rank":"正厅级","note":"女，江苏张家港人"},

    # ── 季培东 ──
    {"id":6,"person_id":4,"org_id":4,"title":"常州市政协主席","start":"","end":"","rank":"正厅级","note":""},

    # ── 陈金虎 ──
    {"id":7,"person_id":5,"org_id":1,"title":"常州市委书记","start":"2020","end":"2026-07","rank":"副部级","note":"2020-2026.07任常州书记，1967年生，江苏句容人"},
    {"id":8,"person_id":5,"org_id":1,"title":"常州市委副书记","start":"2019","end":"2020","rank":"副部级","note":"先任副书记后任书记"},

    # ── 盛蕾 ──
    {"id":9,"person_id":6,"org_id":2,"title":"常州市长","start":"2021","end":"2024","rank":"副部级","note":"2021-2024任常州市长，女"},
    {"id":10,"person_id":6,"org_id":1,"title":"常州市委副书记","start":"2021","end":"2024","rank":"副部级","note":""},

    # ── 乔俊杰（武进区委书记）──
    {"id":11,"person_id":7,"org_id":9,"title":"武进区委书记","start":"","end":"","rank":"正厅级","note":"1974年生，江苏泰兴人"},
    # ── 恽淇丞（武进区长）──
    {"id":12,"person_id":8,"org_id":15,"title":"武进区长","start":"","end":"","rank":"正厅级","note":""},

    # ── 胥亚伟（金坛区委书记）──
    {"id":13,"person_id":9,"org_id":10,"title":"金坛区委书记","start":"2026-01","end":"","rank":"正厅级","note":"2026.01任，1974年生"},

    # ── 李超鲲（溧阳市委书记）──
    {"id":14,"person_id":10,"org_id":11,"title":"溧阳市委书记","start":"","end":"","rank":"正厅级","note":""},
    # ── 巢彬（溧阳市长）──
    {"id":15,"person_id":11,"org_id":17,"title":"溧阳市长","start":"","end":"","rank":"正厅级","note":""},

    # ── 汤如军（钟楼区长）──
    {"id":16,"person_id":12,"org_id":13,"title":"钟楼区长","start":"","end":"","rank":"正厅级","note":""},

    # ── 天宁区（placeholder）──
    {"id":17,"person_id":13,"org_id":6,"title":"天宁区委书记","start":"","end":"","rank":"正厅级","note":"信息待查"},
    {"id":18,"person_id":14,"org_id":12,"title":"天宁区长","start":"","end":"","rank":"正厅级","note":"信息待查"},

    # ── 钟楼区委书记（placeholder）──
    {"id":19,"person_id":15,"org_id":7,"title":"钟楼区委书记","start":"","end":"","rank":"正厅级","note":"信息待查"},

    # ── 新北区（placeholder）──
    {"id":20,"person_id":16,"org_id":8,"title":"新北区委书记","start":"","end":"","rank":"正厅级","note":"信息待查"},
    {"id":21,"person_id":17,"org_id":14,"title":"新北区长","start":"","end":"","rank":"正厅级","note":"信息待查"},

    # ── 金坛区长（placeholder）──
    {"id":22,"person_id":18,"org_id":16,"title":"金坛区长","start":"","end":"","rank":"正厅级","note":"信息待查"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # ── 李佰平 ↔ 周伟（党政搭档）──
    {"id":1,"person_a":1,"person_b":2,"type":"党政搭档","context":"李佰平（常州市委书记）与周伟（市长）为常州市党政一把手搭档","overlap_org":"常州市","overlap_period":"2026-07至今"},

    # ── 陈金虎→李佰平（前后任书记）──
    {"id":2,"person_a":5,"person_b":1,"type":"前后任","context":"陈金虎（2020-2026.07常州书记）→ 李佰平（2026.07接任书记）","overlap_org":"中共常州市委员会","overlap_period":"不重叠（前后任）"},

    # ── 盛蕾→周伟（前后任市长）──
    {"id":3,"person_a":6,"person_b":2,"type":"前后任","context":"盛蕾（2021-2024常州市长）→ 周伟（2024.12接任市长）","overlap_org":"常州市人民政府","overlap_period":"不重叠（前后任）"},

    # ── 各区委书记↔区长/市长（党政搭档）──
    {"id":4,"person_a":13,"person_b":14,"type":"党政搭档","context":"天宁区委书记与天宁区长党政搭档","overlap_org":"天宁区","overlap_period":""},
    {"id":5,"person_a":15,"person_b":12,"type":"党政搭档","context":"钟楼区委书记与汤如军（钟楼区长）党政搭档","overlap_org":"钟楼区","overlap_period":""},
    {"id":6,"person_a":16,"person_b":17,"type":"党政搭档","context":"新北区委书记与新北区长党政搭档","overlap_org":"新北区","overlap_period":""},
    {"id":7,"person_a":7,"person_b":8,"type":"党政搭档","context":"乔俊杰（武进区委书记）与恽淇丞（武进区长）党政搭档","overlap_org":"武进区","overlap_period":""},
    {"id":8,"person_a":9,"person_b":18,"type":"党政搭档","context":"胥亚伟（金坛区委书记）与金坛区长党政搭档","overlap_org":"金坛区","overlap_period":""},
    {"id":9,"person_a":10,"person_b":11,"type":"党政搭档","context":"李超鲲（溧阳市委书记）与巢彬（溧阳市长）党政搭档","overlap_org":"溧阳市","overlap_period":""},

    # ── 市区联系：各区委/市委书记向市委书记汇报 ──
    {"id":10,"person_a":1,"person_b":13,"type":"隶属关系","context":"李佰平（市委书记）领导天宁区委书记","overlap_org":"常州市","overlap_period":""},
    {"id":11,"person_a":1,"person_b":15,"type":"隶属关系","context":"李佰平（市委书记）领导钟楼区委书记","overlap_org":"常州市","overlap_period":""},
    {"id":12,"person_a":1,"person_b":16,"type":"隶属关系","context":"李佰平（市委书记）领导新北区委书记","overlap_org":"常州市","overlap_period":""},
    {"id":13,"person_a":1,"person_b":7,"type":"隶属关系","context":"李佰平（市委书记）领导乔俊杰（武进区委书记）","overlap_org":"常州市","overlap_period":""},
    {"id":14,"person_a":1,"person_b":9,"type":"隶属关系","context":"李佰平（市委书记）领导胥亚伟（金坛区委书记）","overlap_org":"常州市","overlap_period":""},
    {"id":15,"person_a":1,"person_b":10,"type":"隶属关系","context":"李佰平（市委书记）领导李超鲲（溧阳市委书记）","overlap_org":"常州市","overlap_period":""},
]

# =========================================================================
# BUILD SQLITE
# =========================================================================
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.executescript("""
CREATE TABLE IF NOT EXISTS persons (id INTEGER PRIMARY KEY,name TEXT,gender TEXT,ethnicity TEXT,birth TEXT,birthplace TEXT,education TEXT,party_join TEXT,work_start TEXT,current_post TEXT,current_org TEXT,source TEXT);
CREATE TABLE IF NOT EXISTS organizations (id INTEGER PRIMARY KEY,name TEXT,type TEXT,level TEXT,parent TEXT,location TEXT);
CREATE TABLE IF NOT EXISTS positions (id INTEGER PRIMARY KEY,person_id INTEGER,org_id INTEGER,title TEXT,start TEXT,"end" TEXT,rank TEXT,note TEXT,FOREIGN KEY(person_id) REFERENCES persons(id),FOREIGN KEY(org_id) REFERENCES organizations(id));
CREATE TABLE IF NOT EXISTS relationships (id INTEGER PRIMARY KEY,person_a INTEGER,person_b INTEGER,type TEXT,context TEXT,overlap_org TEXT,overlap_period TEXT,FOREIGN KEY(person_a) REFERENCES persons(id),FOREIGN KEY(person_b) REFERENCES persons(id));
CREATE INDEX IF NOT EXISTS idx_pos_p ON positions(person_id);
CREATE INDEX IF NOT EXISTS idx_pos_o ON positions(org_id);
CREATE INDEX IF NOT EXISTS idx_rel_a ON relationships(person_a);
CREATE INDEX IF NOT EXISTS idx_rel_b ON relationships(person_b);
""")
for p in persons:
    c.execute("INSERT OR REPLACE INTO persons VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
              (p["id"],p["name"],p["gender"],p["ethnicity"],p["birth"],p["birthplace"],p["education"],p["party_join"],p["work_start"],p["current_post"],p["current_org"],p["source"]))
for o in organizations:
    c.execute("INSERT OR REPLACE INTO organizations VALUES(?,?,?,?,?,?)",
              (o["id"],o["name"],o["type"],o["level"],o["parent"],o["location"]))
for pos in positions:
    c.execute("INSERT OR REPLACE INTO positions VALUES(?,?,?,?,?,?,?,?)",
              (pos["id"],pos["person_id"],pos["org_id"],pos["title"],pos["start"],pos["end"],pos["rank"],pos["note"]))
for r in relationships:
    c.execute("INSERT OR REPLACE INTO relationships VALUES(?,?,?,?,?,?,?)",
              (r["id"],r["person_a"],r["person_b"],r["type"],r["context"],r["overlap_org"],r["overlap_period"]))
conn.commit()

counts = {}
for t in ["persons","organizations","positions","relationships"]:
    counts[t] = c.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
conn.close()
print(f"SQLite DB: {DB_PATH}")
for t,n in counts.items():
    print(f"  {t}: {n} records")

# =========================================================================
# BUILD GEXF
# =========================================================================
os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

def esc(s):
    if s is None: return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def pcolor(post):
    if "市委书记" in post and "市委" in post:
        return "200,30,30"  # deep red for party secretary
    if "市长" in post or "区长" in post or "县长" in post:
        return "30,80,200"  # deep blue for mayor/district head
    if "副书记" in post:
        return "220,60,60"
    if "副市长" in post or "副区长" in post:
        return "60,120,220"
    if "纪委书记" in post or "监委" in post:
        return "230,150,0"
    if "组织部长" in post or "统战部长" in post or "宣传部长" in post or "政法委" in post:
        return "180,90,180"
    if "政协" in post:
        return "180,160,220"
    if "人大" in post:
        return "160,200,220"
    return "120,120,120"

def ocolor(otype):
    return {"党委":"255,200,200","政府":"200,200,255","人大":"200,220,255","政协":"220,200,255",
            "事业单位":"210,210,210"}.get(otype,"200,200,200")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Claude Code Research Agent</creator>')
lines.append('    <description>常州市（地级市）领导班子 + 6区市工作关系网络 — 2026年7月14日生成</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')
lines.append('    <attributes class="node">')
for aid,atitle in [("0","type"),("1","birth"),("2","birthplace"),("3","current_post"),("4","entity_type"),("5","level")]:
    lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
for aid,atitle in [("0","type"),("1","start"),("2","end"),("3","context")]:
    lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
lines.append('    </attributes>')
lines.append('    <nodes>')
for p in persons:
    c_ = pcolor(p.get("current_post",""))
    sz = "20.0" if any(k in p.get("current_post","") for k in ["市委书记","市长","副书记"]) else "12.0"
    lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    for f,v in [("0","person"),("1",p.get("birth","")),("2",p.get("birthplace","")),("3",p.get("current_post","")),("4","person"),("5","")]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c_.split(",")[0]}" g="{c_.split(",")[1]}" b="{c_.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')
for o in organizations:
    c_ = ocolor(o.get("type",""))
    lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    for f,v in [("0","organization"),("1",""),("2",o.get("location","")),("3",""),("4","organization"),("5",o.get("level",""))]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c_.split(",")[0]}" g="{c_.split(",")[1]}" b="{c_.split(",")[2]}"/>')
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
    lines.append('        </attvalues>')
    lines.append('      </edge>')
for r in relationships:
    eid += 1
    ov = r.get("overlap_period","")
    ov_s = ov.split("至今")[0] if "至今" in ov else ov
    lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
    lines.append('        <attvalues>')
    for f,v in [("0",r["type"]),("1",ov_s),("2",""),("3",r.get("context",""))]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
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
print("\nDone!")
