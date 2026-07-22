#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 泰州市 (Taizhou City) leadership network.

Covers: City-level leadership (市委书记, 市长),
6 district/county-level sub-divisions: 海陵区, 高港区, 姜堰区,
兴化市, 靖江市, 泰兴市.
"""

import sqlite3, os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/taizhou_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/taizhou_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── City-level leadership ──
    # 1. 姜冬冬 — 泰州市委书记 (1976-10, 安徽利辛, 2024.10任)
    {"id":1,"name":"姜冬冬","gender":"男","ethnicity":"汉族","birth":"1976-10","birthplace":"安徽利辛","education":"","party_join":"","work_start":"","current_post":"泰州市委书记","current_org":"中共泰州市委员会","source":""},
    # 2. 李晖 — 泰州市长 (1970-11, 江西新余, 2026.06任)
    {"id":2,"name":"李晖","gender":"男","ethnicity":"汉族","birth":"1970-11","birthplace":"江西新余","education":"","party_join":"","work_start":"","current_post":"泰州市市长","current_org":"泰州市人民政府","source":""},

    # ── Known subs ──
    # 3. 顾萍 — 高港区委书记
    {"id":3,"name":"顾萍","gender":"女","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"高港区委书记","current_org":"中共高港区委员会","source":""},
    # 4. 方针 — 姜堰区委书记
    {"id":4,"name":"方针","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"姜堰区委书记","current_org":"中共姜堰区委员会","source":""},
    # 5. 陈锋剑 — 兴化市委书记
    {"id":5,"name":"陈锋剑","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"兴化市委书记","current_org":"中共兴化市委员会","source":""},
    # 6. 申强 — 靖江市委书记
    {"id":6,"name":"申强","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"靖江市委书记","current_org":"中共靖江市委员会","source":""},
    # 7. 刘文荣 — 泰兴市委书记
    {"id":7,"name":"刘文荣","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"泰兴市委书记","current_org":"中共泰兴市委员会","source":""},
    # 8. 牛世杰 — 泰兴市长
    {"id":8,"name":"牛世杰","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"泰兴市长","current_org":"泰兴市人民政府","source":""},

    # ── Placeholder entries for missing data (待查) ──
    # 海陵区委书记
    {"id":9,"name":"海陵区委书记","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"海陵区委书记","current_org":"中共海陵区委员会","source":""},
    # 海陵区长
    {"id":10,"name":"海陵区长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"海陵区长","current_org":"海陵区人民政府","source":""},
    # 高港区长
    {"id":11,"name":"高港区长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"高港区长","current_org":"高港区人民政府","source":""},
    # 姜堰区长
    {"id":12,"name":"姜堰区长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"姜堰区长","current_org":"姜堰区人民政府","source":""},
    # 兴化市长
    {"id":13,"name":"兴化市长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"兴化市长","current_org":"兴化市人民政府","source":""},
    # 靖江市长
    {"id":14,"name":"靖江市长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"靖江市长","current_org":"靖江市人民政府","source":""},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    # ── Taizhou city-level core ──
    {"id":1,"name":"中共泰州市委员会","type":"党委","level":"地级","parent":"中共江苏省委员会","location":"江苏省泰州市"},
    {"id":2,"name":"泰州市人民政府","type":"政府","level":"地级","parent":"江苏省人民政府","location":"江苏省泰州市"},
    {"id":3,"name":"泰州市人大常委会","type":"人大","level":"地级","parent":"","location":"江苏省泰州市"},
    {"id":4,"name":"政协泰州市委员会","type":"政协","level":"地级","parent":"","location":"江苏省泰州市"},
    {"id":5,"name":"中共泰州市纪律检查委员会","type":"党委","level":"地级","parent":"中共泰州市委员会","location":"江苏省泰州市"},

    # ── 3 Districts — Party committees ──
    {"id":6,"name":"中共海陵区委员会","type":"党委","level":"县级","parent":"中共泰州市委员会","location":"江苏省泰州市海陵区"},
    {"id":7,"name":"中共高港区委员会","type":"党委","level":"县级","parent":"中共泰州市委员会","location":"江苏省泰州市高港区"},
    {"id":8,"name":"中共姜堰区委员会","type":"党委","level":"县级","parent":"中共泰州市委员会","location":"江苏省泰州市姜堰区"},

    # ── 3 County-level cities — Party committees ──
    {"id":9,"name":"中共兴化市委员会","type":"党委","level":"县级","parent":"中共泰州市委员会","location":"江苏省泰州市兴化市"},
    {"id":10,"name":"中共靖江市委员会","type":"党委","level":"县级","parent":"中共泰州市委员会","location":"江苏省泰州市靖江市"},
    {"id":11,"name":"中共泰兴市委员会","type":"党委","level":"县级","parent":"中共泰州市委员会","location":"江苏省泰州市泰兴市"},

    # ── 3 Districts — Governments ──
    {"id":12,"name":"海陵区人民政府","type":"政府","level":"县级","parent":"泰州市人民政府","location":"江苏省泰州市海陵区"},
    {"id":13,"name":"高港区人民政府","type":"政府","level":"县级","parent":"泰州市人民政府","location":"江苏省泰州市高港区"},
    {"id":14,"name":"姜堰区人民政府","type":"政府","level":"县级","parent":"泰州市人民政府","location":"江苏省泰州市姜堰区"},

    # ── 3 County-level cities — Governments ──
    {"id":15,"name":"兴化市人民政府","type":"政府","level":"县级","parent":"泰州市人民政府","location":"江苏省泰州市兴化市"},
    {"id":16,"name":"靖江市人民政府","type":"政府","level":"县级","parent":"泰州市人民政府","location":"江苏省泰州市靖江市"},
    {"id":17,"name":"泰兴市人民政府","type":"政府","level":"县级","parent":"泰州市人民政府","location":"江苏省泰州市泰兴市"},

    # ── External / higher-level orgs ──
    {"id":18,"name":"中共江苏省委员会","type":"党委","level":"省级","parent":"","location":"江苏省南京市"},
    {"id":19,"name":"江苏省人民政府","type":"政府","level":"省级","parent":"","location":"江苏省南京市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # ── 姜冬冬 (泰州市委书记) ──
    {"id":1,"person_id":1,"org_id":1,"title":"泰州市委书记","start":"2024-10","end":"","rank":"副部级","note":"1976年生，安徽利辛人，2024.10任"},
    {"id":2,"person_id":1,"org_id":1,"title":"泰州市委副书记","start":"2024-10","end":"","rank":"副部级","note":""},

    # ── 李晖 (泰州市市长) ──
    {"id":3,"person_id":2,"org_id":2,"title":"泰州市市长","start":"2026-06","end":"","rank":"副部级","note":"1970-11，江西新余人，2026.06任"},
    {"id":4,"person_id":2,"org_id":1,"title":"泰州市委副书记","start":"2026-06","end":"","rank":"副部级","note":""},

    # ── 顾萍 (高港区委书记, 女) ──
    {"id":5,"person_id":3,"org_id":7,"title":"高港区委书记","start":"","end":"","rank":"副厅级","note":"女"},

    # ── 方针 (姜堰区委书记) ──
    {"id":6,"person_id":4,"org_id":8,"title":"姜堰区委书记","start":"","end":"","rank":"副厅级","note":""},

    # ── 陈锋剑 (兴化市委书记) ──
    {"id":7,"person_id":5,"org_id":9,"title":"兴化市委书记","start":"","end":"","rank":"副厅级","note":""},

    # ── 申强 (靖江市委书记) ──
    {"id":8,"person_id":6,"org_id":10,"title":"靖江市委书记","start":"","end":"","rank":"副厅级","note":""},

    # ── 刘文荣 (泰兴市委书记) ──
    {"id":9,"person_id":7,"org_id":11,"title":"泰兴市委书记","start":"","end":"","rank":"副厅级","note":""},

    # ── 牛世杰 (泰兴市长) ──
    {"id":10,"person_id":8,"org_id":17,"title":"泰兴市长","start":"","end":"","rank":"正处级","note":""},

    # ── Placeholder positions ──
    {"id":11,"person_id":9,"org_id":6,"title":"海陵区委书记","start":"","end":"","rank":"副厅级","note":"信息待查"},
    {"id":12,"person_id":10,"org_id":12,"title":"海陵区长","start":"","end":"","rank":"正处级","note":"信息待查"},
    {"id":13,"person_id":11,"org_id":13,"title":"高港区长","start":"","end":"","rank":"正处级","note":"信息待查"},
    {"id":14,"person_id":12,"org_id":14,"title":"姜堰区长","start":"","end":"","rank":"正处级","note":"信息待查"},
    {"id":15,"person_id":13,"org_id":15,"title":"兴化市长","start":"","end":"","rank":"正处级","note":"信息待查"},
    {"id":16,"person_id":14,"org_id":16,"title":"靖江市长","start":"","end":"","rank":"正处级","note":"信息待查"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # ── 姜冬冬 ↔ 李晖（党政搭档）──
    {"id":1,"person_a":1,"person_b":2,"type":"党政搭档","context":"姜冬冬（泰州市委书记）与李晖（市长）为泰州市党政一把手搭档","overlap_org":"泰州市","overlap_period":"2026-06至今"},

    # ── 各区委/市委书记与区长/市长（党政搭档）──
    # 海陵区
    {"id":2,"person_a":9,"person_b":10,"type":"党政搭档","context":"海陵区委书记与海陵区长党政搭档","overlap_org":"海陵区","overlap_period":""},
    # 高港区
    {"id":3,"person_a":3,"person_b":11,"type":"党政搭档","context":"顾萍（高港区委书记）与高港区长党政搭档","overlap_org":"高港区","overlap_period":""},
    # 姜堰区
    {"id":4,"person_a":4,"person_b":12,"type":"党政搭档","context":"方针（姜堰区委书记）与姜堰区长党政搭档","overlap_org":"姜堰区","overlap_period":""},
    # 兴化市
    {"id":5,"person_a":5,"person_b":13,"type":"党政搭档","context":"陈锋剑（兴化市委书记）与兴化市长党政搭档","overlap_org":"兴化市","overlap_period":""},
    # 靖江市
    {"id":6,"person_a":6,"person_b":14,"type":"党政搭档","context":"申强（靖江市委书记）与靖江市长党政搭档","overlap_org":"靖江市","overlap_period":""},
    # 泰兴市
    {"id":7,"person_a":7,"person_b":8,"type":"党政搭档","context":"刘文荣（泰兴市委书记）与牛世杰（泰兴市长）党政搭档","overlap_org":"泰兴市","overlap_period":""},

    # ── 市区联系：各区委/市委书记向市委书记汇报 ──
    {"id":8,"person_a":1,"person_b":9,"type":"隶属关系","context":"姜冬冬（市委书记）领导海陵区委书记","overlap_org":"泰州市","overlap_period":""},
    {"id":9,"person_a":1,"person_b":3,"type":"隶属关系","context":"姜冬冬（市委书记）领导顾萍（高港区委书记）","overlap_org":"泰州市","overlap_period":""},
    {"id":10,"person_a":1,"person_b":4,"type":"隶属关系","context":"姜冬冬（市委书记）领导方针（姜堰区委书记）","overlap_org":"泰州市","overlap_period":""},
    {"id":11,"person_a":1,"person_b":5,"type":"隶属关系","context":"姜冬冬（市委书记）领导陈锋剑（兴化市委书记）","overlap_org":"泰州市","overlap_period":""},
    {"id":12,"person_a":1,"person_b":6,"type":"隶属关系","context":"姜冬冬（市委书记）领导申强（靖江市委书记）","overlap_org":"泰州市","overlap_period":""},
    {"id":13,"person_a":1,"person_b":7,"type":"隶属关系","context":"姜冬冬（市委书记）领导刘文荣（泰兴市委书记）","overlap_org":"泰州市","overlap_period":""},
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
        return "200,30,30"
    if "市长" in post or "区长" in post or "县长" in post:
        return "30,80,200"
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
lines.append('    <description>泰州市（地级市）领导班子 + 6区市工作关系网络 — 2026年7月14日生成</description>')
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
