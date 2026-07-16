#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 秀屿区 (Xiuyu District), 莆田市, 福建省.

Level: 市辖区
Province: 福建省
Parent City: 莆田市
Targets: 区委书记 & 区长

Key findings (as of July 2026):
- 区委书记: 张伯松 (confirmed ~2021-2025 term; 2026 status needs verification)
- 区长: (current officeholder needs verification)
- 秀屿区是2002年2月1日经国务院批准设立，由原莆田县部分乡镇析置
- 区政府驻地：笏石镇

Sources:
- Xiuyu District Government official website (xiuyu.gov.cn - inaccessible from research environment)
- District news and meeting reports

Current as of: July 2026 (partial data - web research blocked)

IMPORTANT NOTE: Web research (government sites, Baidu, news) was blocked from
the research environment. Core facts rely on pre-existing knowledge with limited
current confirmation. All confidence levels are marked accordingly.
"""

import sqlite3, os, sys
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "秀屿区_network.db")
GEXF_PATH = os.path.join(BASE, "秀屿区_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ═════════════════════════════════════════════════════════════════════
    # Current top leadership
    # ═════════════════════════════════════════════════════════════════════

    # 张伯松 — 秀屿区委书记 (confirmed ~2021, needs 2026 verification)
    {"id":1,"name":"张伯松","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"秀屿区委书记","current_org":"中共莆田市秀屿区委员会",
     "source":"需从秀屿区政府官网领导之窗页面核实：http://www.xiuyu.gov.cn/zwgk/ldzc/"},

    # (区长 — 目前公开资料未确认现任区长人选。需从秀屿区政府官网核实)
    # 留空待以后核实后补充
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1,"name":"中共莆田市秀屿区委员会","type":"党委","level":"县处级","parent":"中共莆田市委员会","location":"莆田市秀屿区笏石镇"},
    {"id":2,"name":"莆田市秀屿区人民政府","type":"政府","level":"县处级","parent":"莆田市人民政府","location":"莆田市秀屿区笏石镇"},
    {"id":3,"name":"莆田市秀屿区人大常委会","type":"人大","level":"县处级","parent":"莆田市人大常委会","location":"莆田市秀屿区笏石镇"},
    {"id":4,"name":"中国人民政治协商会议莆田市秀屿区委员会","type":"政协","level":"县处级","parent":"政协莆田市委员会","location":"莆田市秀屿区笏石镇"},
    {"id":5,"name":"中共莆田市秀屿区纪律检查委员会","type":"党委","level":"县处级","parent":"中共莆田市纪律检查委员会","location":"莆田市秀屿区笏石镇"},
    {"id":6,"name":"中共莆田市秀屿区委组织部","type":"党委","level":"县处级","parent":"中共莆田市秀屿区委员会","location":"莆田市秀屿区笏石镇"},
    {"id":7,"name":"中共莆田市秀屿区委宣传部","type":"党委","level":"县处级","parent":"中共莆田市秀屿区委员会","location":"莆田市秀屿区笏石镇"},
    {"id":8,"name":"中共莆田市秀屿区委政法委员会","type":"党委","level":"县处级","parent":"中共莆田市秀屿区委员会","location":"莆田市秀屿区笏石镇"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 张伯松 — 区委书记
    {"id":1,"person_id":1,"org_id":1,"title":"秀屿区委书记","start":"~2021","end":"至今","rank":"县处级","note":"具体上任日期及连任情况需核实"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
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
        return "230,50,50"  # red for party secretary
    if "区长" in post or "代区长" in post:
        return "50,100,230"  # blue for district mayor
    if "副区长" in post:
        return "80,140,230"
    if "纪委书记" in post or "监委" in post:
        return "230,165,0"
    return "120,120,120"

def ocolor(otype):
    return {"党委":"255,200,200","政府":"200,200,255","事业单位":"220,220,220","人大":"200,255,255","政协":"255,240,200"}.get(otype,"200,200,200")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Sisyphus Research Agent</creator>')
lines.append('    <description>秀屿区（莆田市辖区）领导班子工作关系网络 — 2026年7月生成（部分数据需核实）</description>')
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
print("\nCRITICAL GAPS (research blocked - requires web access to fill):")
print("  1. Confirm current 区委书记 — 张伯松 was in office ~2021-2025, needs 2026 verification")
print("  2. CURRENT 区长 — not identified; most recent occupant needs verification")
print("  3. Full leadership roster (区委常委名单) not available")
print("  4. Key deputies: 常务副区长, 组织部, 纪委, 政法, 宣传")
print("  5. Predecessor/successor paths for both top leaders")
print("  6. Birth dates, education, full career timelines for all officials")
print("  7. Cross-region rotation and relationship evidence")
print("  8. Governance achievements and work style indicators")
print("\nRecommended URLs to check when web access is available:")
print("  - http://www.xiuyu.gov.cn/zwgk/ldzc/ (领导之窗)")
print("  - https://www.putian.gov.cn/zwgk/rsxx/ (人事信息)")
print("  - Baidu Baike: 秀屿区")
