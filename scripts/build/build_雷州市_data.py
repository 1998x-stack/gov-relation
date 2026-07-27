#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 雷州市 (Leizhou City), 湛江市, 广东省.

Covers: city-level leaders (市委书记, 市长), key standing committee members,
and organizational relationships.

Sources:
- 雷州市人民政府 official site: www.leizhou.gov.cn (via HTTP — confirmed)
- 湛江市人民政府: www.zhanjiang.gov.cn
- 雷州市政府网站 领导之窗栏目 (ldzc/)

Current as of: July 2026

Key findings:
- 市委书记: 吴松江 (confirmed via 雷州市政府网站 新闻报道, 2026-07-09)
- 市长: 闫嘉伟 (confirmed via 雷州市政府网站 常务会议报道, 2026-05-19)
- Government leadership page confirms leadership structure
"""

import os, sqlite3, sys
from datetime import datetime

STAGING = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING, "雷州市_network.db")
GEXF_PATH = os.path.join(STAGING, "雷州市_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================

persons = [
    # ═════════════════════════════════════════════════════════════════════
    # Current leadership — 市委
    # ═════════════════════════════════════════════════════════════════════

    # 吴松江 — 雷州市委书记
    {"id": 1, "name": "吴松江", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "雷州市委书记", "current_org": "中共雷州市委员会",
     "source": "雷州市人民政府网站 — 新闻报道'吴松江率队到白沙镇开展平安夜访活动'（2026-07-09确认）"},

    # 闫嘉伟 — 雷州市委副书记、市长
    {"id": 2, "name": "闫嘉伟", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "雷州市委副书记、市长", "current_org": "雷州市人民政府",
     "source": "雷州市人民政府网站 — 常务会议报道'闫嘉伟市长主持召开市政府第十七届133次常务会议'（2026-07-22确认）"},

    # ═════════════════════════════════════════════════════════════════════
    # 市委常委 (identified from news reports)
    # ═════════════════════════════════════════════════════════════════════

    # 市委副书记（专职）- Not yet identified by name
    {"id": 3, "name": "待查（市委副书记）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "雷州市委副书记", "current_org": "中共雷州市委员会",
     "source": "暂未从公开报道中确认专职副书记姓名"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共雷州市委员会", "type": "党委", "level": "县处级", "parent": "中共湛江市委员会", "location": "湛江市雷州市"},
    {"id": 2, "name": "雷州市人民政府", "type": "政府", "level": "县处级", "parent": "湛江市人民政府", "location": "湛江市雷州市"},
    {"id": 3, "name": "雷州市人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "湛江市人民代表大会常务委员会", "location": "湛江市雷州市"},
    {"id": 4, "name": "中国人民政治协商会议雷州市委员会", "type": "政协", "level": "县处级", "parent": "中国人民政治协商会议湛江市委员会", "location": "湛江市雷州市"},
    {"id": 5, "name": "中共雷州市纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共湛江市纪律检查委员会", "location": "湛江市雷州市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 吴松江
    {"id": 1, "person_id": 1, "org_id": 1, "title": "雷州市委书记", "start": "", "end": "", "rank": "县处级", "note": "当前在任，confirmed as of 2026-07-22"},
    # 闫嘉伟
    {"id": 2, "person_id": 2, "org_id": 2, "title": "雷州市市长", "start": "", "end": "", "rank": "县处级", "note": "当前在任，confirmed as of 2026-07-22"},
    {"id": 3, "person_id": 2, "org_id": 1, "title": "雷州市委副书记", "start": "", "end": "", "rank": "县处级", "note": "兼任市委副书记"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 吴松江 vs 闫嘉伟 — 党政搭档
    {"id": 1, "person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "吴松江（市委书记）与闫嘉伟（市长）是雷州市核心党政搭档",
     "overlap_org": "雷州市", "overlap_period": "2026"},
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
    if "书记" in post and "纪委" not in post:
        return "230,50,50"  # red for party secretary
    if "市长" in post:
        return "50,100,230"  # blue for mayor
    if "副市长" in post:
        return "80,140,230"
    if "人大常委会" in post or "人大" in post:
        return "200,255,255"  # cyan for 人大
    if "政协" in post:
        return "255,240,200"  # cream for 政协
    if "纪委" in post:
        return "255,165,0"  # orange for discipline
    return "120,120,120"

def ocolor(otype):
    return {"党委":"255,200,200","政府":"200,200,255","人大":"200,255,255","政协":"255,240,200"}.get(otype,"200,200,200")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Sisyphus Research Agent</creator>')
lines.append('    <description>雷州市（湛江市代管县级市）领导班子工作关系网络 — 2026年7月生成</description>')
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
    c = pcolor(p.get("current_post",""))
    is_top = any(k in p.get("current_post","") for k in ["市委书记","市长","副书记"])
    sz = "20.0" if is_top else "12.0"
    lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    for f,v in [("0","person"),("1",p.get("birth","")),("2",p.get("birthplace","")),("3",p.get("current_post","")),("4","person"),("5","")]:
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
    lines.append('        </attvalues>')
    lines.append('      </edge>')
for r in relationships:
    eid += 1
    ov = r.get("overlap_period","")
    lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
    lines.append('        <attvalues>')
    for f,v in [("0",r["type"]),("1",ov),("2",""),("3",r.get("context",""))]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
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
print("\nSources:")
print("  1. 雷州市人民政府门户网站 — www.leizhou.gov.cn（2026-07-22确认）")
print("  2. 雷州市政府网站 领导之窗栏目 (ldzc/)")
print("\nOpen gaps:")
print("  1. All birth dates, education backgrounds, and career timelines for all persons")
print("  2. 吴松江's complete career timeline (previous roles, party membership details)")
print("  3. 闫嘉伟's complete career timeline (previous roles, party membership details)")
print("  4. Predecessor/successor chain with exact dates")
print("  5. Full standing committee roster with specific portfolios")
print("  6. Previous party secretary (吴松江's predecessor)")
print("  7. Previous mayor (闫嘉伟's predecessor)")
