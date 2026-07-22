#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 三元区 (Sanyuan District), 三明市, 福建省.

Level: 市辖区
Province: 福建省
Parent City: 三明市
Targets: 区委书记 & 区长

Key findings (as of July 2026):
- 区委书记: 温毅 (confirmed per Wikipedia)
- 区委副书记、区长: 肖世龙 (confirmed in office through 2025 at least)
- Note: 肖世龙 was relieved of concurrent role as 三元经济开发区管理委员会主任 in Dec 2025

Sources:
- Chinese Wikipedia: 三元区 entry (zh.wikipedia.org)
- Sanming City Government website (www.smsy.gov.cn)
- District personnel appointment/removal notices

Current as of: July 2026

Gaps:
- Birth dates, education, and full career timelines for most officials
- Current 区长 status after 肖世龙's December 2025 adjustment
- Full district leadership roster beyond the top two
"""

import sqlite3, os, sys
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "三元区_network.db")
GEXF_PATH = os.path.join(BASE, "三元区_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ═════════════════════════════════════════════════════════════════════
    # Current top leadership
    # ═════════════════════════════════════════════════════════════════════

    # 温毅 — 三元区委书记 (confirmed per Wikipedia)
    {"id":1,"name":"温毅","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"三元区委书记","current_org":"中共三明市三元区委员会",
     "source":"https://zh.wikipedia.org/wiki/%E4%B8%89%E5%85%83%E5%8C%BA"},

    # 肖世龙 — 三元区委副书记、区长 (confirmed from official appointment/removal notices 2021-2025)
    {"id":2,"name":"肖世龙","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"三元区委副书记、区长","current_org":"三明市三元区人民政府",
     "source":"https://www.smsy.gov.cn/zwgk/rsxx/rsrm_26829/202601/t20260104_2181482.htm"},

    # ═════════════════════════════════════════════════════════════════════
    # Other known district leaders (from official news/appointments)
    # ═════════════════════════════════════════════════════════════════════

    # 彭琴莲 — 三元经济开发区管理委员会第一副主任 (appointed Oct 2021)
    {"id":3,"name":"彭琴莲","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"三元经济开发区管理委员会第一副主任","current_org":"福建三元经济开发区管理委员会",
     "source":"https://www.smsy.gov.cn/zwgk/rsxx/rsrm_26829/202112/t20211207_1734787.htm"},

    # ═════════════════════════════════════════════════════════════════════
    # Predecessors - 区委书记
    # ═════════════════════════════════════════════════════════════════════

    # 前任区委书记 information not yet verified from official sources
    # Note: 三元区 was formed in 2021 by merging old 三元区和梅列区
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1,"name":"中共三明市三元区委员会","type":"党委","level":"县处级","parent":"中共三明市委员会","location":"三明市三元区"},
    {"id":2,"name":"三明市三元区人民政府","type":"政府","level":"县处级","parent":"三明市人民政府","location":"三明市三元区"},
    {"id":3,"name":"福建三元经济开发区管理委员会","type":"开发区","level":"县处级","parent":"三明市三元区人民政府","location":"三明市三元区"},
    {"id":4,"name":"三明市三元区人民代表大会常务委员会","type":"人大","level":"县处级","parent":"三明市人大常委会","location":"三明市三元区"},
    {"id":5,"name":"中国人民政治协商会议三明市三元区委员会","type":"政协","level":"县处级","parent":"政协三明市委员会","location":"三明市三元区"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 温毅 — 区委书记
    {"id":1,"person_id":1,"org_id":1,"title":"三元区委书记","start":"","end":"至今","rank":"县处级","note":"现任区委书记"},
    # 肖世龙 — 区长
    {"id":2,"person_id":2,"org_id":2,"title":"三元区委副书记、区长","start":"","end":"至今","rank":"县处级","note":"区长，曾兼任三元经济开发区管理委员会主任至2025年12月"},
    {"id":3,"person_id":2,"org_id":3,"title":"三元经济开发区管理委员会主任（兼）","start":"2021-10","end":"2025-12","rank":"县处级","note":"2025年12月免去兼任职务"},
    # 彭琴莲 — 开发区副主任
    {"id":4,"person_id":3,"org_id":3,"title":"三元经济开发区管理委员会第一副主任（兼）","start":"2021-10","end":"至今","rank":"副处级","note":""},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 温毅 vs 肖世龙 — 党政搭档
    {"id":1,"person_a":1,"person_b":2,"type":"党政搭档",
     "context":"温毅（区委书记）与肖世龙（区长）在三元区共事",
     "overlap_org":"三元区","overlap_period":"至今"},
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
    if "区委书记" in post:
        return "230,50,50"
    if "区长" in post or "代区长" in post:
        return "50,100,230"
    if "副区长" in post:
        return "80,140,230"
    if "纪委书记" in post or "监委" in post:
        return "230,165,0"
    return "120,120,120"

def ocolor(otype):
    return {"党委":"255,200,200","政府":"200,200,255","开发区":"200,255,200","人大":"200,255,255","政协":"255,240,200"}.get(otype,"200,200,200")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Sisyphus Research Agent</creator>')
lines.append('    <description>三元区（三明市辖区）领导班子工作关系网络 — 2026年7月生成</description>')
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
    is_top = any(k in p.get("current_post","") for k in ["区委书记","区长","代区长"])
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
    lines.append('      </edge>')
for r in relationships:
    eid += 1
    ov = r.get("overlap_period","")
    ov_s = ov.split("至今")[0] if "至今" in ov else ov
    lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
    lines.append('        <attvalues>')
    for f,v in [("0",r["type"]),("1",ov_s),("2",""),("3",r.get("context",""))]:
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
print("\nNOTE: This data requires verification. Key items:")
print("  1. Verify full names, birth, and education details for all officials")
print("  2. Confirm 温毅's full career timeline")
print("  3. Confirm 肖世龙's current status (区长 role continues or changed after Dec 2025)")
print("  4. Add full standing committee members (区纪委、组织部、宣传部、政法委等)")
print("  5. Add predecessor 区委书记 (三元区 was created in 2021)")
print("  6. Add deputy positions")
