#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 盐城市 (Yancheng City) leadership network.

Covers: City-level leadership (市委书记, 市长),
9 district/county-level sub-divisions: 亭湖区, 盐都区, 大丰区,
响水县, 滨海县, 阜宁县, 射阳县, 建湖县, 东台市.
"""

import sqlite3, os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/yancheng_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/yancheng_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── City-level leadership ──
    # 1. 严汉平 — 盐城市委书记 (1974-11, 陕西西安, 2026.07任)
    {"id":1,"name":"严汉平","gender":"男","ethnicity":"汉族","birth":"1974-11","birthplace":"陕西西安","education":"","party_join":"","work_start":"","current_post":"盐城市委书记","current_org":"中共盐城市委员会","source":""},
    # 2. 吴炜 — 盐城市长 (1972-12, 江苏如东, 2025.07任)
    {"id":2,"name":"吴炜","gender":"男","ethnicity":"汉族","birth":"1972-12","birthplace":"江苏如东","education":"","party_join":"","work_start":"","current_post":"盐城市市长","current_org":"盐城市人民政府","source":""},

    # ── 亭湖区 ──
    # 3. 田海波 — 亭湖区委书记
    {"id":3,"name":"田海波","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"亭湖区委书记","current_org":"中共亭湖区委员会","source":""},
    # 4. 董玲玲 — 亭湖区代区长 (女)
    {"id":4,"name":"董玲玲","gender":"女","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"亭湖区代区长","current_org":"亭湖区人民政府","source":""},

    # ── Placeholder entries for missing data (待查) ──
    # 盐都区委书记
    {"id":5,"name":"盐都区委书记","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"盐都区委书记","current_org":"中共盐都区委员会","source":""},
    # 盐都区长
    {"id":6,"name":"盐都区长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"盐都区长","current_org":"盐都区人民政府","source":""},
    # 大丰区委书记
    {"id":7,"name":"大丰区委书记","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"大丰区委书记","current_org":"中共大丰区委员会","source":""},
    # 大丰区长
    {"id":8,"name":"大丰区长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"大丰区长","current_org":"大丰区人民政府","source":""},
    # 响水县委书记
    {"id":9,"name":"响水县委书记","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"响水县委书记","current_org":"中共响水县委员会","source":""},
    # 响水县长
    {"id":10,"name":"响水县长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"响水县长","current_org":"响水县人民政府","source":""},
    # 滨海县委书记
    {"id":11,"name":"滨海县委书记","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"滨海县委书记","current_org":"中共滨海县委员会","source":""},
    # 滨海县长
    {"id":12,"name":"滨海县长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"滨海县长","current_org":"滨海县人民政府","source":""},
    # 阜宁县委书记
    {"id":13,"name":"阜宁县委书记","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"阜宁县委书记","current_org":"中共阜宁县委员会","source":""},
    # 阜宁县长
    {"id":14,"name":"阜宁县长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"阜宁县长","current_org":"阜宁县人民政府","source":""},
    # 射阳县委书记
    {"id":15,"name":"射阳县委书记","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"射阳县委书记","current_org":"中共射阳县委员会","source":""},
    # 射阳县长
    {"id":16,"name":"射阳县长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"射阳县长","current_org":"射阳县人民政府","source":""},
    # 建湖县委书记
    {"id":17,"name":"建湖县委书记","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"建湖县委书记","current_org":"中共建湖县委员会","source":""},
    # 建湖县长
    {"id":18,"name":"建湖县长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"建湖县长","current_org":"建湖县人民政府","source":""},
    # 东台市委书记
    {"id":19,"name":"东台市委书记","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"东台市委书记","current_org":"中共东台市委员会","source":""},
    # 东台市长
    {"id":20,"name":"东台市长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"东台市长","current_org":"东台市人民政府","source":""},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    # ── Yancheng city-level core ──
    {"id":1,"name":"中共盐城市委员会","type":"党委","level":"地级","parent":"中共江苏省委员会","location":"江苏省盐城市"},
    {"id":2,"name":"盐城市人民政府","type":"政府","level":"地级","parent":"江苏省人民政府","location":"江苏省盐城市"},
    {"id":3,"name":"盐城市人大常委会","type":"人大","level":"地级","parent":"","location":"江苏省盐城市"},
    {"id":4,"name":"政协盐城市委员会","type":"政协","level":"地级","parent":"","location":"江苏省盐城市"},
    {"id":5,"name":"中共盐城市纪律检查委员会","type":"党委","level":"地级","parent":"中共盐城市委员会","location":"江苏省盐城市"},

    # ── 3 Districts — Party committees ──
    {"id":6,"name":"中共亭湖区委员会","type":"党委","level":"县级","parent":"中共盐城市委员会","location":"江苏省盐城市亭湖区"},
    {"id":7,"name":"中共盐都区委员会","type":"党委","level":"县级","parent":"中共盐城市委员会","location":"江苏省盐城市盐都区"},
    {"id":8,"name":"中共大丰区委员会","type":"党委","level":"县级","parent":"中共盐城市委员会","location":"江苏省盐城市大丰区"},

    # ── 5 Counties — Party committees ──
    {"id":9,"name":"中共响水县委员会","type":"党委","level":"县级","parent":"中共盐城市委员会","location":"江苏省盐城市响水县"},
    {"id":10,"name":"中共滨海县委员会","type":"党委","level":"县级","parent":"中共盐城市委员会","location":"江苏省盐城市滨海县"},
    {"id":11,"name":"中共阜宁县委员会","type":"党委","level":"县级","parent":"中共盐城市委员会","location":"江苏省盐城市阜宁县"},
    {"id":12,"name":"中共射阳县委员会","type":"党委","level":"县级","parent":"中共盐城市委员会","location":"江苏省盐城市射阳县"},
    {"id":13,"name":"中共建湖县委员会","type":"党委","level":"县级","parent":"中共盐城市委员会","location":"江苏省盐城市建湖县"},

    # ── 1 County-level city — Party committee ──
    {"id":14,"name":"中共东台市委员会","type":"党委","level":"县级","parent":"中共盐城市委员会","location":"江苏省盐城市东台市"},

    # ── 3 Districts — Governments ──
    {"id":15,"name":"亭湖区人民政府","type":"政府","level":"县级","parent":"盐城市人民政府","location":"江苏省盐城市亭湖区"},
    {"id":16,"name":"盐都区人民政府","type":"政府","level":"县级","parent":"盐城市人民政府","location":"江苏省盐城市盐都区"},
    {"id":17,"name":"大丰区人民政府","type":"政府","level":"县级","parent":"盐城市人民政府","location":"江苏省盐城市大丰区"},

    # ── 5 Counties — Governments ──
    {"id":18,"name":"响水县人民政府","type":"政府","level":"县级","parent":"盐城市人民政府","location":"江苏省盐城市响水县"},
    {"id":19,"name":"滨海县人民政府","type":"政府","level":"县级","parent":"盐城市人民政府","location":"江苏省盐城市滨海县"},
    {"id":20,"name":"阜宁县人民政府","type":"政府","level":"县级","parent":"盐城市人民政府","location":"江苏省盐城市阜宁县"},
    {"id":21,"name":"射阳县人民政府","type":"政府","level":"县级","parent":"盐城市人民政府","location":"江苏省盐城市射阳县"},
    {"id":22,"name":"建湖县人民政府","type":"政府","level":"县级","parent":"盐城市人民政府","location":"江苏省盐城市建湖县"},

    # ── 1 County-level city — Government ──
    {"id":23,"name":"东台市人民政府","type":"政府","level":"县级","parent":"盐城市人民政府","location":"江苏省盐城市东台市"},

    # ── External / higher-level orgs ──
    {"id":24,"name":"中共江苏省委员会","type":"党委","level":"省级","parent":"","location":"江苏省南京市"},
    {"id":25,"name":"江苏省人民政府","type":"政府","level":"省级","parent":"","location":"江苏省南京市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # ── 严汉平 (盐城市委书记) ──
    {"id":1,"person_id":1,"org_id":1,"title":"盐城市委书记","start":"2026-07","end":"","rank":"副部级","note":"1974年生，陕西西安人，2026.07任"},
    {"id":2,"person_id":1,"org_id":1,"title":"盐城市委副书记","start":"2026-07","end":"","rank":"副部级","note":""},

    # ── 吴炜 (盐城市市长) ──
    {"id":3,"person_id":2,"org_id":2,"title":"盐城市市长","start":"2025-07","end":"","rank":"副部级","note":"1972-12，江苏如东人"},
    {"id":4,"person_id":2,"org_id":1,"title":"盐城市委副书记","start":"2025-07","end":"","rank":"副部级","note":""},

    # ── 田海波 (亭湖区委书记) ──
    {"id":5,"person_id":3,"org_id":6,"title":"亭湖区委书记","start":"","end":"","rank":"副厅级","note":""},

    # ── 董玲玲 (亭湖区代区长, 女) ──
    {"id":6,"person_id":4,"org_id":15,"title":"亭湖区代区长","start":"","end":"","rank":"正处级","note":"女"},

    # ── Placeholder positions ──
    {"id":7,"person_id":5,"org_id":7,"title":"盐都区委书记","start":"","end":"","rank":"副厅级","note":"信息待查"},
    {"id":8,"person_id":6,"org_id":16,"title":"盐都区长","start":"","end":"","rank":"正处级","note":"信息待查"},
    {"id":9,"person_id":7,"org_id":8,"title":"大丰区委书记","start":"","end":"","rank":"副厅级","note":"信息待查"},
    {"id":10,"person_id":8,"org_id":17,"title":"大丰区长","start":"","end":"","rank":"正处级","note":"信息待查"},
    {"id":11,"person_id":9,"org_id":9,"title":"响水县委书记","start":"","end":"","rank":"副厅级","note":"信息待查"},
    {"id":12,"person_id":10,"org_id":18,"title":"响水县长","start":"","end":"","rank":"正处级","note":"信息待查"},
    {"id":13,"person_id":11,"org_id":10,"title":"滨海县委书记","start":"","end":"","rank":"副厅级","note":"信息待查"},
    {"id":14,"person_id":12,"org_id":19,"title":"滨海县长","start":"","end":"","rank":"正处级","note":"信息待查"},
    {"id":15,"person_id":13,"org_id":11,"title":"阜宁县委书记","start":"","end":"","rank":"副厅级","note":"信息待查"},
    {"id":16,"person_id":14,"org_id":20,"title":"阜宁县长","start":"","end":"","rank":"正处级","note":"信息待查"},
    {"id":17,"person_id":15,"org_id":12,"title":"射阳县委书记","start":"","end":"","rank":"副厅级","note":"信息待查"},
    {"id":18,"person_id":16,"org_id":21,"title":"射阳县长","start":"","end":"","rank":"正处级","note":"信息待查"},
    {"id":19,"person_id":17,"org_id":13,"title":"建湖县委书记","start":"","end":"","rank":"副厅级","note":"信息待查"},
    {"id":20,"person_id":18,"org_id":22,"title":"建湖县长","start":"","end":"","rank":"正处级","note":"信息待查"},
    {"id":21,"person_id":19,"org_id":14,"title":"东台市委书记","start":"","end":"","rank":"副厅级","note":"信息待查"},
    {"id":22,"person_id":20,"org_id":23,"title":"东台市长","start":"","end":"","rank":"正处级","note":"信息待查"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # ── 严汉平 ↔ 吴炜（党政搭档）──
    {"id":1,"person_a":1,"person_b":2,"type":"党政搭档","context":"严汉平（盐城市委书记）与吴炜（市长）为盐城市党政一把手搭档","overlap_org":"盐城市","overlap_period":"2026-07至今"},

    # ── 各区委/县委书记与区长/县长（党政搭档）──
    # 亭湖区
    {"id":2,"person_a":3,"person_b":4,"type":"党政搭档","context":"田海波（亭湖区委书记）与董玲玲（亭湖区代区长）党政搭档","overlap_org":"亭湖区","overlap_period":""},
    # 盐都区
    {"id":3,"person_a":5,"person_b":6,"type":"党政搭档","context":"盐都区委书记与盐都区长党政搭档","overlap_org":"盐都区","overlap_period":""},
    # 大丰区
    {"id":4,"person_a":7,"person_b":8,"type":"党政搭档","context":"大丰区委书记与大丰区长党政搭档","overlap_org":"大丰区","overlap_period":""},
    # 响水县
    {"id":5,"person_a":9,"person_b":10,"type":"党政搭档","context":"响水县委书记与响水县长党政搭档","overlap_org":"响水县","overlap_period":""},
    # 滨海县
    {"id":6,"person_a":11,"person_b":12,"type":"党政搭档","context":"滨海县委书记与滨海县长党政搭档","overlap_org":"滨海县","overlap_period":""},
    # 阜宁县
    {"id":7,"person_a":13,"person_b":14,"type":"党政搭档","context":"阜宁县委书记与阜宁县长党政搭档","overlap_org":"阜宁县","overlap_period":""},
    # 射阳县
    {"id":8,"person_a":15,"person_b":16,"type":"党政搭档","context":"射阳县委书记与射阳县长党政搭档","overlap_org":"射阳县","overlap_period":""},
    # 建湖县
    {"id":9,"person_a":17,"person_b":18,"type":"党政搭档","context":"建湖县委书记与建湖县长党政搭档","overlap_org":"建湖县","overlap_period":""},
    # 东台市
    {"id":10,"person_a":19,"person_b":20,"type":"党政搭档","context":"东台市委书记与东台市长党政搭档","overlap_org":"东台市","overlap_period":""},

    # ── 市区联系：各区委/县委书记向市委书记汇报 ──
    {"id":11,"person_a":1,"person_b":3,"type":"隶属关系","context":"严汉平（市委书记）领导田海波（亭湖区委书记）","overlap_org":"盐城市","overlap_period":""},
    {"id":12,"person_a":1,"person_b":5,"type":"隶属关系","context":"严汉平（市委书记）领导盐都区委书记","overlap_org":"盐城市","overlap_period":""},
    {"id":13,"person_a":1,"person_b":7,"type":"隶属关系","context":"严汉平（市委书记）领导大丰区委书记","overlap_org":"盐城市","overlap_period":""},
    {"id":14,"person_a":1,"person_b":9,"type":"隶属关系","context":"严汉平（市委书记）领导响水县委书记","overlap_org":"盐城市","overlap_period":""},
    {"id":15,"person_a":1,"person_b":11,"type":"隶属关系","context":"严汉平（市委书记）领导滨海县委书记","overlap_org":"盐城市","overlap_period":""},
    {"id":16,"person_a":1,"person_b":13,"type":"隶属关系","context":"严汉平（市委书记）领导阜宁县委书记","overlap_org":"盐城市","overlap_period":""},
    {"id":17,"person_a":1,"person_b":15,"type":"隶属关系","context":"严汉平（市委书记）领导射阳县委书记","overlap_org":"盐城市","overlap_period":""},
    {"id":18,"person_a":1,"person_b":17,"type":"隶属关系","context":"严汉平（市委书记）领导建湖县委书记","overlap_org":"盐城市","overlap_period":""},
    {"id":19,"person_a":1,"person_b":19,"type":"隶属关系","context":"严汉平（市委书记）领导东台市委书记","overlap_org":"盐城市","overlap_period":""},
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
lines.append('    <description>盐城市（地级市）领导班子 + 9区市县工作关系网络 — 2026年7月14日生成</description>')
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
