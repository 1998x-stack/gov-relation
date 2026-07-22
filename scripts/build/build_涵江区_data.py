#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 涵江区 (Hanjiang District), 莆田市, 福建省.

Level: 市辖区
Province: 福建省
Parent City: 莆田市
Targets: 区委书记 & 区长

Key findings (as of July 2026):
- 区委书记: 郑群星 (born 1969.10, appointed ~September 2025, formerly 区长 2021-2025)
- 区委副书记、区长: 陈俊杰 (born 1978.11, appointed ~October 2025 as acting/区长)
- 前任区委书记: 连向红 (promoted to 莆田市政协副主席)
- 前任区长: 郑群星 (promoted to 区委书记)
- 副区长: 林梓雄 (confirmed from education research news, 2025)

Sources:
- 莆田市涵江区人民政府官网 (pthj.gov.cn) — official government website (primary)
- Baidu Baike / Baidu search — leadership roster and career timelines
- 人民网 — appointment notices and career summaries
- 福建省委组织部 — pre-appointment public notices

Current as of: July 2026

Note: Birth dates, education, and full career timelines for most officials
require further on-site verification. Some deputy positions may have gaps.
"""

import sqlite3, os, sys
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "涵江区_network.db")
GEXF_PATH = os.path.join(BASE, "涵江区_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ═════════════════════════════════════════════════════════════════════
    # Current top leadership
    # ═════════════════════════════════════════════════════════════════════

    # 郑群星 — 涵江区委书记 (confirmed, ~September 2025)
    {"id":1,"name":"郑群星","gender":"男","ethnicity":"汉族",
     "birth":"1969年10月","birthplace":"福建仙游（待确认）",
     "education":"中央党校大学（本科学历）",
     "party_join":"中共党员","work_start":"",
     "current_post":"涵江区委书记","current_org":"中共莆田市涵江区委员会",
     "source":"人民网;福建省委组织部公示;涵江时讯"},

    # 陈俊杰 — 涵江区委副书记、区长 (confirmed, ~October 2025)
    {"id":2,"name":"陈俊杰","gender":"男","ethnicity":"汉族",
     "birth":"1978年11月","birthplace":"福建（待确认）",
     "education":"大学本科",
     "party_join":"中共党员","work_start":"",
     "current_post":"涵江区委副书记、区长","current_org":"莆田市涵江区人民政府",
     "source":"人民网;福建省委组织部公示;涵江时讯"},

    # ═════════════════════════════════════════════════════════════════════
    # District leaders mentioned in official news (2025-2026)
    # ═════════════════════════════════════════════════════════════════════

    # 林梓雄 — 副区长 (confirmed from education research news, March 2025)
    {"id":3,"name":"林梓雄","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"涵江区副区长","current_org":"莆田市涵江区人民政府",
     "source":"涵江区政府官网;微信公众平台"},

    # ═════════════════════════════════════════════════════════════════════
    # Predecessors
    # ═════════════════════════════════════════════════════════════════════

    # 连向红 — 前任涵江区委书记 (now 莆田市政协副主席)
    {"id":4,"name":"连向红","gender":"女","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"莆田市政协副主席（原涵江区委书记）","current_org":"政协莆田市委员会",
     "source":"人民网;网易新闻;涵江时讯"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1,"name":"中共莆田市涵江区委员会","type":"党委","level":"县处级","parent":"中共莆田市委员会","location":"莆田市涵江区"},
    {"id":2,"name":"莆田市涵江区人民政府","type":"政府","level":"县处级","parent":"莆田市人民政府","location":"莆田市涵江区"},
    {"id":3,"name":"莆田市涵江区人民武装部","type":"事业单位","level":"县处级","parent":"莆田军分区","location":"莆田市涵江区"},
    {"id":4,"name":"莆田市涵江区人大常委会","type":"人大","level":"县处级","parent":"莆田市人大常委会","location":"莆田市涵江区"},
    {"id":5,"name":"中国人民政治协商会议莆田市涵江区委员会","type":"政协","level":"县处级","parent":"政协莆田市委员会","location":"莆田市涵江区"},
    # 前任关联机构
    {"id":6,"name":"政协莆田市委员会","type":"政协","level":"地厅级","parent":"福建省政协","location":"福建省莆田市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 郑群星 — 区委书记
    {"id":1,"person_id":1,"org_id":1,"title":"涵江区委书记","start":"2025-09","end":"至今","rank":"县处级","note":"兼任区人武部党委第一书记；前任：连向红"},
    {"id":2,"person_id":1,"org_id":3,"title":"区人武部党委第一书记","start":"2025-09","end":"至今","rank":"县处级","note":"兼任"},
    # 郑群星 — 前任区长
    {"id":3,"person_id":1,"org_id":2,"title":"涵江区委副书记、区长","start":"2021-06","end":"2025-09","rank":"县处级","note":"2021年6月任代区长，后当选区长；由陈俊杰接任"},
    # 郑群星 — 荔城区
    {"id":4,"person_id":1,"org_id":0,"title":"荔城区副区长","start":"","end":"","rank":"副处级","note":"莆田市荔城区人民政府任职"},
    {"id":5,"person_id":1,"org_id":0,"title":"荔城区委常委","start":"","end":"","rank":"副处级","note":""},
    {"id":6,"person_id":1,"org_id":0,"title":"荔城区委常委、副区长","start":"","end":"","rank":"副处级","note":""},

    # 陈俊杰 — 区长
    {"id":7,"person_id":2,"org_id":2,"title":"涵江区委副书记、区长","start":"2025-10","end":"至今","rank":"县处级","note":"2025年10月任副区长、代理区长，后当选区长；前任：郑群星"},
    # 陈俊杰 — 此前任职
    {"id":8,"person_id":2,"org_id":0,"title":"莆田市工信局党组成员、副局长","start":"","end":"","rank":"副处级","note":""},
    {"id":9,"person_id":2,"org_id":0,"title":"莆田市二轻联社党组成员、副主任（主持日常工作）","start":"","end":"","rank":"副处级","note":""},
    {"id":10,"person_id":2,"org_id":0,"title":"莆田市二轻联社党组书记、主任，市工信局党组副书记","start":"","end":"","rank":"正处级","note":""},
    {"id":11,"person_id":2,"org_id":1,"title":"涵江区委副书记（正处长级）","start":"2025-09","end":"2025-10","rank":"正处级","note":"2025年9月任涵江区委副书记，为区长人选"},

    # 林梓雄 — 副区长
    {"id":12,"person_id":3,"org_id":2,"title":"涵江区副区长","start":"","end":"至今","rank":"副处级","note":""},

    # 连向红 — 前任区委书记
    {"id":13,"person_id":4,"org_id":1,"title":"涵江区委书记","start":"","end":"2025-09","rank":"县处级","note":"后由郑群星接任"},
    {"id":14,"person_id":4,"org_id":6,"title":"莆田市政协副主席","start":"2025-09","end":"至今","rank":"副厅级","note":"现任"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 郑群星 vs 陈俊杰 — 党政搭档
    {"id":1,"person_a":1,"person_b":2,"type":"党政搭档",
     "context":"郑群星（区委书记）与陈俊杰（区长）在涵江区共事",
     "overlap_org":"涵江区","overlap_period":"2025-10至今"},

    # 连向红 → 郑群星 前后任（区委书记）
    {"id":2,"person_a":4,"person_b":1,"type":"前后任",
     "context":"连向红（前任书记）→ 郑群星（现任书记）",
     "overlap_org":"中共莆田市涵江区委员会","overlap_period":"不重叠（前后任）"},

    # 郑群星 → 陈俊杰 前后任（区长交接）
    {"id":3,"person_a":1,"person_b":2,"type":"前后任",
     "context":"郑群星升任区委书记后，陈俊杰接任区长",
     "overlap_org":"莆田市涵江区人民政府","overlap_period":"不重叠（前后任）"},

    # 郑群星 vs 连向红 — 前后任（区长-书记时期可能有重叠）
    {"id":4,"person_a":1,"person_b":4,"type":"superior_subordinate",
     "context":"郑群星任区长期间，连向红任区委书记（上下级关系）",
     "overlap_org":"涵江区","overlap_period":"2021-06至2025-09"},
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
    if o["id"] == 0:
        continue  # placeholder for unknown orgs, skip
    c.execute("INSERT OR REPLACE INTO organizations VALUES(?,?,?,?,?,?)",
              (o["id"],o["name"],o["type"],o["level"],o["parent"],o["location"]))
for pos in positions:
    if pos["org_id"] == 0:
        continue  # placeholder org, skip
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
    if "政协" in post:
        return "255,240,200"
    return "120,120,120"

def ocolor(otype):
    return {"党委":"255,200,200","政府":"200,200,255","事业单位":"220,220,220","人大":"200,255,255","政协":"255,240,200"}.get(otype,"200,200,200")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Sisyphus Research Agent</creator>')
lines.append('    <description>涵江区（莆田市辖区）领导班子工作关系网络 — 2026年7月生成</description>')
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
    if o["id"] == 0:
        continue
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
    if pos["org_id"] == 0:
        continue
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
    lines.append('      </edge>')
lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

tn = len(persons) + len([o for o in organizations if o["id"] != 0])
te = len([pos for pos in positions if pos["org_id"] != 0]) + len(relationships)
print(f"\nGEXF: {GEXF_PATH}")
print(f"  Nodes: {len(persons)} persons + {len([o for o in organizations if o['id'] != 0])} orgs = {tn} total")
print(f"  Edges: {len([pos for pos in positions if pos['org_id'] != 0])} worked_at + {len(relationships)} relationships = {te} total")
print("\nDone!")
print("\nNOTE: This data requires verification. Key items:")
print("  1. Verify birthplaces and full birth/education details for all officials")
print("  2. Verify 郑群星's complete career before 荔城区 (early career)")
print("  3. Verify 陈俊杰's complete career before 市工信局 (early career)")
print("  4. Confirm 连向红's full career timeline")
print("  5. Add standing committee members (区纪委、组织部、宣传部、政法委等)")
print("  6. Add more deputy positions (副区长 list) and refine existing ones")
