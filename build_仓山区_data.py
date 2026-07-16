#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 仓山区 (Cangshan District), 福州市, 福建省.

Covers: district-level leaders (party secretary, district mayor, standing committee,
vice mayors), plus predecessor chain and key connections.

Sources:
- Cangshan District Government official website (fzcangshan.gov.cn) — news and leadership mentions
- Fuzhou Daily / mainstream media reports
- Official government meeting/news pages

Current as of: July 2026

Key findings:
- 区委书记: 施家雄 (succeeded 魏邦仲 who was in office as of Aug 2025)
- 区委副书记、区长: 林国晃 (born 1977-09, male, Han, university education, CCP member)

Note: Birth dates, education, and full career timelines for most officials
require on-site verification of the government leadership page.
"""

import sqlite3, os, sys
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "仓山区_network.db")
GEXF_PATH = os.path.join(BASE, "仓山区_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ═════════════════════════════════════════════════════════════════════
    # Current top leadership
    # ═════════════════════════════════════════════════════════════════════

    # 施家雄 — 仓山区委书记 (confirmed from district news, July 2026)
    {"id":1,"name":"施家雄","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"仓山区委书记","current_org":"中共福州市仓山区委员会",
     "source":"https://www.fzcangshan.gov.cn/xjwz/xxgk/gzdt/csxw/202607/t20260716_5347204.htm"},

    # 林国晃 — 仓山区委副书记、区长 (confirmed from official leadership page)
    {"id":2,"name":"林国晃","gender":"男","ethnicity":"汉族",
     "birth":"1977-09","birthplace":"",
     "education":"大学",
     "party_join":"中共党员","work_start":"",
     "current_post":"仓山区委副书记、区政府党组书记、区长","current_org":"福州市仓山区人民政府",
     "source":"https://www.fzcangshan.gov.cn/xjwz/xxgk/ldzc/lgh/"},

    # ═════════════════════════════════════════════════════════════════════
    # Current government leadership team (区政府领导)
    # ═════════════════════════════════════════════════════════════════════

    # 余垂霄 — 区政府党组副书记、副区长
    {"id":3,"name":"余垂霄","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"仓山区政府党组副书记、副区长","current_org":"福州市仓山区人民政府",
     "source":"https://www.fzcangshan.gov.cn/xjwz/xxgk/ldzc/"},

    # 赵旭宇 — 区政府党组成员
    {"id":4,"name":"赵旭宇","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"仓山区政府党组成员","current_org":"福州市仓山区人民政府",
     "source":"https://www.fzcangshan.gov.cn/xjwz/xxgk/ldzc/"},

    # 高晓健 — 区政府党组成员、副区长
    {"id":5,"name":"高晓健","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"仓山区政府党组成员、副区长","current_org":"福州市仓山区人民政府",
     "source":"https://www.fzcangshan.gov.cn/xjwz/xxgk/ldzc/"},

    # 钟治民 — 区政府党组成员、副区长
    {"id":6,"name":"钟治民","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"仓山区政府党组成员、副区长","current_org":"福州市仓山区人民政府",
     "source":"https://www.fzcangshan.gov.cn/xjwz/xxgk/ldzc/"},

    # 叶晓瑜 — 区政府党组成员、副区长
    {"id":7,"name":"叶晓瑜","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"仓山区政府党组成员、副区长","current_org":"福州市仓山区人民政府",
     "source":"https://www.fzcangshan.gov.cn/xjwz/xxgk/ldzc/"},

    # 连锦 — 区政府党组成员、副区长
    {"id":8,"name":"连锦","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"仓山区政府党组成员、副区长","current_org":"福州市仓山区人民政府",
     "source":"https://www.fzcangshan.gov.cn/xjwz/xxgk/ldzc/"},

    # 郑金保 — 区政府副区长（挂职）
    {"id":9,"name":"郑金保","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"仓山区政府副区长（挂职）","current_org":"福州市仓山区人民政府",
     "source":"https://www.fzcangshan.gov.cn/xjwz/xxgk/ldzc/"},

    # 林斌 — 区政府副区长
    {"id":10,"name":"林斌","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"仓山区政府副区长","current_org":"福州市仓山区人民政府",
     "source":"https://www.fzcangshan.gov.cn/xjwz/xxgk/ldzc/"},

    # 江必达 — 区政府党组成员、副区长
    {"id":11,"name":"江必达","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"仓山区政府党组成员、副区长","current_org":"福州市仓山区人民政府",
     "source":"https://www.fzcangshan.gov.cn/xjwz/xxgk/ldzc/"},

    # 黄朝锋 — 区政府党组成员、副区长
    {"id":12,"name":"黄朝锋","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"仓山区政府党组成员、副区长","current_org":"福州市仓山区人民政府",
     "source":"https://www.fzcangshan.gov.cn/xjwz/xxgk/ldzc/"},

    # 胡斌 — 区政府党组成员
    {"id":13,"name":"胡斌","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"仓山区政府党组成员","current_org":"福州市仓山区人民政府",
     "source":"https://www.fzcangshan.gov.cn/xjwz/xxgk/ldzc/"},

    # ═════════════════════════════════════════════════════════════════════
    # Predecessors
    # ═════════════════════════════════════════════════════════════════════

    # 魏邦仲 — 前任仓山区委书记 (confirmed through Aug 2025, succeeded by 施家雄)
    {"id":14,"name":"魏邦仲","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"（原仓山区委书记）","current_org":"",
     "source":"https://www.fzcangshan.gov.cn/xjwz/xxgk/gzdt/csxw/202508/t20250825_5065872.htm"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1,"name":"中共福州市仓山区委员会","type":"党委","level":"县处级","parent":"中共福州市委员会","location":"福州市仓山区"},
    {"id":2,"name":"福州市仓山区人民政府","type":"政府","level":"县处级","parent":"福州市人民政府","location":"福州市仓山区"},
    {"id":3,"name":"福州新区仓山功能区管委会","type":"新区","level":"县处级","parent":"福州市人民政府","location":"福州市仓山区"},
    {"id":4,"name":"福建自贸区福州片区管委会","type":"政府","level":"副厅级","parent":"福州市人民政府","location":"福州市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 施家雄 — 区委书记
    {"id":1,"person_id":1,"org_id":1,"title":"仓山区委书记","start":"2025/2026?","end":"至今","rank":"县处级","note":"接替魏邦仲；上任时间待确认"},
    # 林国晃 — 区长
    {"id":2,"person_id":2,"org_id":2,"title":"仓山区委副书记、区政府党组书记、区长","start":"","end":"至今","rank":"县处级","note":"兼任福建自贸区福州片区管委会副主任、福州新区仓山功能区管委会主任"},
    {"id":3,"person_id":2,"org_id":3,"title":"福州新区仓山功能区管委会主任","start":"","end":"至今","rank":"县处级","note":"兼任"},
    {"id":4,"person_id":2,"org_id":4,"title":"福建自贸区福州片区管委会（福州保税港区管委会）副主任","start":"","end":"至今","rank":"","note":"兼任"},
    # 余垂霄 — 副区长
    {"id":5,"person_id":3,"org_id":2,"title":"区政府党组副书记、副区长","start":"","end":"至今","rank":"副处级","note":""},
    # 赵旭宇 — 党组成员
    {"id":6,"person_id":4,"org_id":2,"title":"区政府党组成员","start":"","end":"至今","rank":"副处级","note":""},
    # 高晓健 — 副区长
    {"id":7,"person_id":5,"org_id":2,"title":"区政府党组成员、副区长","start":"","end":"至今","rank":"副处级","note":""},
    # 钟治民 — 副区长
    {"id":8,"person_id":6,"org_id":2,"title":"区政府党组成员、副区长","start":"","end":"至今","rank":"副处级","note":""},
    # 叶晓瑜 — 副区长
    {"id":9,"person_id":7,"org_id":2,"title":"区政府党组成员、副区长","start":"","end":"至今","rank":"副处级","note":""},
    # 连锦 — 副区长
    {"id":10,"person_id":8,"org_id":2,"title":"区政府党组成员、副区长","start":"","end":"至今","rank":"副处级","note":""},
    # 郑金保 — 挂职副区长
    {"id":11,"person_id":9,"org_id":2,"title":"区政府副区长（挂职）","start":"","end":"至今","rank":"副处级","note":"挂职"},
    # 林斌 — 副区长
    {"id":12,"person_id":10,"org_id":2,"title":"区政府副区长","start":"","end":"至今","rank":"副处级","note":""},
    # 江必达 — 副区长
    {"id":13,"person_id":11,"org_id":2,"title":"区政府党组成员、副区长","start":"","end":"至今","rank":"副处级","note":""},
    # 黄朝锋 — 副区长
    {"id":14,"person_id":12,"org_id":2,"title":"区政府党组成员、副区长","start":"","end":"至今","rank":"副处级","note":""},
    # 胡斌 — 党组成员
    {"id":15,"person_id":13,"org_id":2,"title":"区政府党组成员","start":"","end":"至今","rank":"副处级","note":""},
    # 魏邦仲 — 前任区委书记
    {"id":16,"person_id":14,"org_id":1,"title":"仓山区委书记","start":"","end":"约2025/2026","rank":"县处级","note":"后由施家雄接任"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 施家雄 vs 林国晃 — 党政搭档
    {"id":1,"person_a":1,"person_b":2,"type":"党政搭档",
     "context":"施家雄（区委书记）与林国晃（区长）在仓山区共事",
     "overlap_org":"仓山区","overlap_period":"2025/2026至今"},

    # 魏邦仲 → 施家雄 前后任
    {"id":2,"person_a":14,"person_b":1,"type":"前后任",
     "context":"魏邦仲（前任书记）→ 施家雄（现任书记）",
     "overlap_org":"中共福州市仓山区委员会","overlap_period":"不重叠（前后任）"},
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
    if "书记" in post and "区委" in post:
        return "230,50,50"  # red for party secretary
    if "区长" in post:
        return "50,100,230"  # blue for district mayor
    if "副区长" in post:
        return "80,140,230"
    if "纪委书记" in post or "监委" in post:
        return "230,165,0"
    return "120,120,120"

def ocolor(otype):
    return {"党委":"255,200,200","政府":"200,200,255","新区":"200,255,200"}.get(otype,"200,200,200")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Sisyphus Research Agent</creator>')
lines.append('    <description>仓山区（福州市辖区）领导班子工作关系网络 — 2026年7月生成</description>')
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
print("\n⚠️ NOTE: This data requires verification. Key items:")
print("  1. Verify 施家雄's full name and birth/education details")
print("  2. Verify predecessor 魏邦仲's successor timeline")
print("  3. Complete career timelines for all officials")
print("  4. Add standing committee members (区纪委、组织部、宣传部、政法委等)")
