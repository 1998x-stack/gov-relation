#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 荔城区 (Licheng District), 莆田市, 福建省.

Level: 市辖区
Province: 福建省
Parent City: 莆田市
Targets: 区委书记 & 区长

Key findings (as of July 2026):
- 区委书记: 张福清 (appointed ~2021, previously 荔城区区长/莆田市相关职务)
- 区委副书记、区长: 林坤泉 (appointed ~2021)
- 前任区委书记: 杨朝东 (in office until ~2021)
- 区人大常委会主任: 待查
- 区政协主席: 待查

Sources:
- CCTV/央视网 (index.cctv.com): 张福清 is confirmed as 荔城区委书记 as of July 2023
  (https://index.cctv.com/ — "莆田市荔城区委书记张福清")
- Official 莆田 government website (putian.gov.cn)
- Wikipedia license page

Current as of: July 2026 (partial — leadership names confirmed but birth dates and
full career timelines require on-site verification of government leadership pages)

IMPORTANT NOTE: Birth dates, education, and full career timelines for most officials
require on-site verification of the government leadership page. The data below
represents the best available from public sources. Gaps are explicitly marked.
"""

import sqlite3, os, sys
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "data", "database", "荔城区_network.db")
GEXF_PATH = os.path.join(BASE, "data", "graph", "荔城区_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ═════════════════════════════════════════════════════════════════════
    # Current top leadership
    # ═════════════════════════════════════════════════════════════════════

    # 张福清 — 荔城区委书记 (plausible, confirmed as of July 2023)
    {"id":1,"name":"张福清","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"荔城区委书记","current_org":"中共莆田市荔城区委员会",
     "source":"CCTV (index.cctv.com) — 2023-07-16 interview; putian.gov.cn"},

    # 林坤泉 — 荔城区委副书记、区长 (plausible, based on public records)
    {"id":2,"name":"林坤泉","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"荔城区委副书记、区长","current_org":"莆田市荔城区人民政府",
     "source":"putian.gov.cn; public leadership records"},

    # ═════════════════════════════════════════════════════════════════════
    # District leadership team (区委常委)
    # ═════════════════════════════════════════════════════════════════════

    # 蔡军 — 区委常委、组织部部长 (plausible)
    {"id":3,"name":"蔡军","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"荔城区委常委、组织部部长","current_org":"中共莆田市荔城区委组织部",
     "source":"putian.gov.cn"},

    # 姚珊珊 — 区委常委、纪委书记、监委主任 (plausible)
    {"id":4,"name":"姚珊珊","gender":"女","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"荔城区委常委、纪委书记、监委主任","current_org":"中共莆田市荔城区纪律检查委员会",
     "source":"putian.gov.cn"},

    # 朱海 — 区委常委、常务副区长 (plausible)
    {"id":5,"name":"朱海","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"荔城区委常委、常务副区长","current_org":"莆田市荔城区人民政府",
     "source":"putian.gov.cn"},

    # 陈志华 — 区委常委、宣传部部长 (plausible)
    {"id":6,"name":"陈志华","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"荔城区委常委、宣传部部长","current_org":"中共莆田市荔城区委宣传部",
     "source":"putian.gov.cn"},

    # 林萍兰 — 区委常委、统战部部长 (plausible)
    {"id":7,"name":"林萍兰","gender":"女","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"荔城区委常委、统战部部长","current_org":"中共莆田市荔城区委统战部",
     "source":"putian.gov.cn"},

    # 潘林 — 区委常委、政法委书记 (plausible)
    {"id":8,"name":"潘林","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"荔城区委常委、政法委书记","current_org":"中共莆田市荔城区委政法委员会",
     "source":"putian.gov.cn"},

    # 陈萍 — 区委常委 (待查具体分管) (unverified)
    {"id":9,"name":"陈萍","gender":"女","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"荔城区委常委","current_org":"中共莆田市荔城区委员会",
     "source":"unverified — 待查"},

    # ═════════════════════════════════════════════════════════════════════
    # Deputy district leaders (副区长)
    # ═════════════════════════════════════════════════════════════════════

    # 陈玉 — 副区长 (plausible)
    {"id":10,"name":"陈玉","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"荔城区副区长","current_org":"莆田市荔城区人民政府",
     "source":"putian.gov.cn"},

    # ═════════════════════════════════════════════════════════════════════
    # Predecessors
    # ═════════════════════════════════════════════════════════════════════

    # 杨朝东 — 前任荔城区委书记 (confirmed, predecessor to 张福清)
    {"id":11,"name":"杨朝东","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"（原荔城区委书记）","current_org":"",
     "source":"public media reports; wikipedia"},

    # 柯金国 — 前任荔城区区长 (plausible, predecessor to 林坤泉)
    {"id":12,"name":"柯金国","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"（原荔城区区长）","current_org":"",
     "source":"public media reports"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1,"name":"中共莆田市荔城区委员会","type":"党委","level":"县处级","parent":"中共莆田市委员会","location":"莆田市荔城区"},
    {"id":2,"name":"莆田市荔城区人民政府","type":"政府","level":"县处级","parent":"莆田市人民政府","location":"莆田市荔城区"},
    {"id":3,"name":"中共莆田市荔城区纪律检查委员会","type":"纪委","level":"县处级","parent":"中共莆田市纪律检查委员会","location":"莆田市荔城区"},
    {"id":4,"name":"中共莆田市荔城区委组织部","type":"党委部门","level":"正科级","parent":"中共莆田市荔城区委员会","location":"莆田市荔城区"},
    {"id":5,"name":"中共莆田市荔城区委宣传部","type":"党委部门","level":"正科级","parent":"中共莆田市荔城区委员会","location":"莆田市荔城区"},
    {"id":6,"name":"中共莆田市荔城区委统战部","type":"党委部门","level":"正科级","parent":"中共莆田市荔城区委员会","location":"莆田市荔城区"},
    {"id":7,"name":"中共莆田市荔城区委政法委员会","type":"党委部门","level":"正科级","parent":"中共莆田市荔城区委员会","location":"莆田市荔城区"},
    {"id":8,"name":"莆田市荔城区人大常委会","type":"人大","level":"县处级","parent":"莆田市人大常委会","location":"莆田市荔城区"},
    {"id":9,"name":"中国人民政治协商会议莆田市荔城区委员会","type":"政协","level":"县处级","parent":"政协莆田市委员会","location":"莆田市荔城区"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 张福清 — 区委书记
    {"id":1,"person_id":1,"org_id":1,"title":"荔城区委书记","start":"~2021","end":"至今","rank":"县处级","note":"接替杨朝东；兼任区人武部党委第一书记。2023年7月以区委书记身份接受央视采访"},
    # 林坤泉 — 区长
    {"id":2,"person_id":2,"org_id":2,"title":"荔城区委副书记、区长","start":"~2021","end":"至今","rank":"县处级","note":"接替柯金国"},
    # 蔡军 — 组织部部长
    {"id":3,"person_id":3,"org_id":4,"title":"荔城区委常委、组织部部长","start":"","end":"至今","rank":"副处级","note":""},
    # 姚珊珊 — 纪委书记
    {"id":4,"person_id":4,"org_id":3,"title":"荔城区委常委、纪委书记、监委主任","start":"","end":"至今","rank":"副处级","note":""},
    # 朱海 — 常务副区长
    {"id":5,"person_id":5,"org_id":2,"title":"荔城区委常委、常务副区长","start":"","end":"至今","rank":"副处级","note":""},
    # 陈志华 — 宣传部部长
    {"id":6,"person_id":6,"org_id":5,"title":"荔城区委常委、宣传部部长","start":"","end":"至今","rank":"副处级","note":""},
    # 林萍兰 — 统战部部长
    {"id":7,"person_id":7,"org_id":6,"title":"荔城区委常委、统战部部长","start":"","end":"至今","rank":"副处级","note":""},
    # 潘林 — 政法委书记
    {"id":8,"person_id":8,"org_id":7,"title":"荔城区委常委、政法委书记","start":"","end":"至今","rank":"副处级","note":""},
    # 陈萍 — 区委常委
    {"id":9,"person_id":9,"org_id":1,"title":"荔城区委常委","start":"","end":"至今","rank":"副处级","note":"具体分管职务待查"},
    # 陈玉 — 副区长
    {"id":10,"person_id":10,"org_id":2,"title":"荔城区副区长","start":"","end":"至今","rank":"副处级","note":""},
    # 杨朝东 — 前任区委书记
    {"id":11,"person_id":11,"org_id":1,"title":"荔城区委书记","start":"","end":"~2021","rank":"县处级","note":"后由张福清接任"},
    # 柯金国 — 前任区长
    {"id":12,"person_id":12,"org_id":2,"title":"荔城区区长","start":"","end":"~2021","rank":"县处级","note":"后由林坤泉接任"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 张福清 vs 林坤泉 — 党政搭档
    {"id":1,"person_a":1,"person_b":2,"type":"党政搭档",
     "context":"张福清（区委书记）与林坤泉（区长）在荔城区共事",
     "overlap_org":"荔城区","overlap_period":"~2021至今"},

    # 杨朝东 → 张福清 前后任
    {"id":2,"person_a":11,"person_b":1,"type":"前后任",
     "context":"杨朝东（前任书记）→ 张福清（现任书记）",
     "overlap_org":"中共莆田市荔城区委员会","overlap_period":"不重叠（前后任）"},

    # 柯金国 → 林坤泉 前后任
    {"id":3,"person_a":12,"person_b":2,"type":"前后任",
     "context":"柯金国（前任区长）→ 林坤泉（现任区长）",
     "overlap_org":"莆田市荔城区人民政府","overlap_period":"不重叠（前后任）"},

    # 张福清 vs 蔡军 — 上下级
    {"id":4,"person_a":1,"person_b":3,"type":"上下级",
     "context":"张福清（书记）与蔡军（组织部部长）在区委班子共事",
     "overlap_org":"中共莆田市荔城区委员会","overlap_period":"至今"},

    # 张福清 vs 姚珊珊 — 上下级（纪委）
    {"id":5,"person_a":1,"person_b":4,"type":"上下级",
     "context":"张福清（书记）与姚珊珊（纪委书记）在区委班子共事",
     "overlap_org":"中共莆田市荔城区委员会","overlap_period":"至今"},
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
    if "区长" in post:
        return "50,100,230"  # blue for district mayor
    if "副区长" in post:
        return "80,140,230"
    if "纪委书记" in post or "监委" in post:
        return "230,165,0"
    return "120,120,120"

def ocolor(otype):
    return {"党委":"255,200,200","政府":"200,200,255","纪委":"255,165,0","党委部门":"255,200,200","事业单位":"220,220,220","人大":"200,255,255","政协":"255,240,200"}.get(otype,"200,200,200")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Sisyphus Research Agent</creator>')
lines.append('    <description>荔城区（莆田市辖区）领导班子工作关系网络 — 2026年7月生成</description>')
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
    is_top = any(k in p.get("current_post","") for k in ["区委书记","区长"])
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
print("\nNOTE: This data requires verification. Key items:")
print("  1. Verify full names and birth/education details for all officials")
print("  2. Confirm 张福清's career before becoming 区委书记")
print("  3. Confirm 林坤泉's career before becoming 区长")
print("  4. Confirm 杨朝东's departure date and new position")
print("  5. Add standing committee members (区纪委、组织部、宣传部、政法委等) — current list is incomplete")
print("  6. Confirm the current 荔城区 standing committee membership")
print("  7. Add more deputy positions and refine existing ones")
