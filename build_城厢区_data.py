#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 城厢区 (Chengxiang District), 莆田市, 福建省.

Level: 市辖区
Province: 福建省
Parent City: 莆田市
Targets: 区委书记 & 区长

Key findings (as of July 2026):
- 区委书记: 王文晖 (formerly 区长, promoted ~July 13, 2026)
- 区委副书记、代区长: 黄建恩 (appointed ~July 14, 2026)
- 前任区委书记: 郑松青 (in office as of June 9, 2026, succeeded by 王文晖)
- 副区长: 赖宇贞 (confirmed from online interview), 陈旭清, 苏顺琪
- 区领导: 黄智光, 胡彬伟, 程启琦, 陈美钗

Sources:
- Chengxiang District Government official website (chengxiang.gov.cn)
- District news and meeting reports

Current as of: July 2026

Note: Birth dates, education, and full career timelines for most officials
require on-site verification of the government leadership page.
"""

import sqlite3, os, sys
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "城厢区_network.db")
GEXF_PATH = os.path.join(BASE, "城厢区_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ═════════════════════════════════════════════════════════════════════
    # Current top leadership
    # ═════════════════════════════════════════════════════════════════════

    # 王文晖 — 城厢区委书记 (confirmed, July 2026)
    {"id":1,"name":"王文晖","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"城厢区委书记","current_org":"中共莆田市城厢区委员会",
     "source":"https://www.chengxiang.gov.cn/zwgk/cxdt/cxyw/202607/t20260716_2225972.htm"},

    # 黄建恩 — 城厢区委副书记、代区长 (confirmed, July 2026)
    {"id":2,"name":"黄建恩","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"城厢区委副书记、代区长","current_org":"莆田市城厢区人民政府",
     "source":"https://www.chengxiang.gov.cn/zwgk/cxdt/cxyw/202607/t20260715_2225681.htm"},

    # ═════════════════════════════════════════════════════════════════════
    # Confirmed district leaders (区领导 mentioned in official news)
    # ═════════════════════════════════════════════════════════════════════

    # 赖宇贞 — 副区长 (confirmed from online interview, June 2026)
    {"id":3,"name":"赖宇贞","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"城厢区副区长","current_org":"莆田市城厢区人民政府",
     "source":"https://www.chengxiang.gov.cn/gzcy/zxft/202606/t20260626_2222534.htm"},

    # 陈旭清 — 区领导 (mentioned in July 2026 news)
    {"id":4,"name":"陈旭清","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"城厢区领导","current_org":"莆田市城厢区人民政府",
     "source":"https://www.chengxiang.gov.cn/zwgk/cxdt/cxyw/202607/t20260715_2225681.htm"},

    # 苏顺琪 — 区领导 (mentioned in June/July 2026 news)
    {"id":5,"name":"苏顺琪","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"城厢区领导","current_org":"莆田市城厢区人民政府",
     "source":"https://www.chengxiang.gov.cn/zwgk/cxdt/cxyw/202607/t20260715_2225681.htm"},

    # 黄智光 — 区领导 (mentioned in July 2026 news)
    {"id":6,"name":"黄智光","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"城厢区领导","current_org":"莆田市城厢区人民政府",
     "source":"https://www.chengxiang.gov.cn/zwgk/cxdt/cxyw/202607/t20260716_2225972.htm"},

    # 胡彬伟 — 区领导 (mentioned in July 2026 news)
    {"id":7,"name":"胡彬伟","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"城厢区领导","current_org":"莆田市城厢区人民政府",
     "source":"https://www.chengxiang.gov.cn/zwgk/cxdt/cxyw/202607/t20260716_2225972.htm"},

    # 程启琦 — 区领导 (mentioned in July 2026 news)
    {"id":8,"name":"程启琦","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"城厢区领导","current_org":"莆田市城厢区人民政府",
     "source":"https://www.chengxiang.gov.cn/zwgk/cxdt/cxyw/202607/t20260716_2225972.htm"},

    # 陈美钗 — 区领导 (mentioned in June 2026 news)
    {"id":9,"name":"陈美钗","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"城厢区领导","current_org":"莆田市城厢区人民政府",
     "source":"https://www.chengxiang.gov.cn/zwgk/cxdt/cxyw/202606/t20260610_2219902.htm"},

    # ═════════════════════════════════════════════════════════════════════
    # Predecessors
    # ═════════════════════════════════════════════════════════════════════

    # 郑松青 — 前任城厢区委书记 (confirmed through June 9, 2026)
    {"id":10,"name":"郑松青","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"（原城厢区委书记）","current_org":"",
     "source":"https://www.chengxiang.gov.cn/zwgk/cxdt/cxyw/202606/t20260610_2219902.htm"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1,"name":"中共莆田市城厢区委员会","type":"党委","level":"县处级","parent":"中共莆田市委员会","location":"莆田市城厢区"},
    {"id":2,"name":"莆田市城厢区人民政府","type":"政府","level":"县处级","parent":"莆田市人民政府","location":"莆田市城厢区"},
    {"id":3,"name":"莆田市城厢区人民武装部","type":"事业单位","level":"县处级","parent":"莆田军分区","location":"莆田市城厢区"},
    {"id":4,"name":"莆田市城厢区人大常委会","type":"人大","level":"县处级","parent":"莆田市人大常委会","location":"莆田市城厢区"},
    {"id":5,"name":"中国人民政治协商会议莆田市城厢区委员会","type":"政协","level":"县处级","parent":"政协莆田市委员会","location":"莆田市城厢区"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 王文晖 — 区委书记
    {"id":1,"person_id":1,"org_id":1,"title":"城厢区委书记","start":"2026-07","end":"至今","rank":"县处级","note":"接替郑松青；同时兼任区人武部党委第一书记"},
    {"id":2,"person_id":1,"org_id":3,"title":"区人武部党委第一书记","start":"2026-07","end":"至今","rank":"县处级","note":"兼任"},
    # 王文晖 — 前任区长
    {"id":3,"person_id":1,"org_id":2,"title":"城厢区委副书记、区长","start":"","end":"2026-07","rank":"县处级","note":"此前任职，后升任区委书记"},
    # 黄建恩 — 代区长
    {"id":4,"person_id":2,"org_id":2,"title":"城厢区委副书记、代区长","start":"2026-07","end":"至今","rank":"县处级","note":"新任代区长"},
    # 赖宇贞 — 副区长
    {"id":5,"person_id":3,"org_id":2,"title":"城厢区副区长","start":"","end":"至今","rank":"副处级","note":""},
    # 陈旭清 — 区领导
    {"id":6,"person_id":4,"org_id":2,"title":"城厢区领导","start":"","end":"至今","rank":"副处级","note":""},
    # 苏顺琪 — 区领导
    {"id":7,"person_id":5,"org_id":2,"title":"城厢区领导","start":"","end":"至今","rank":"副处级","note":""},
    # 黄智光 — 区领导
    {"id":8,"person_id":6,"org_id":2,"title":"城厢区领导","start":"","end":"至今","rank":"副处级","note":""},
    # 胡彬伟 — 区领导
    {"id":9,"person_id":7,"org_id":2,"title":"城厢区领导","start":"","end":"至今","rank":"副处级","note":""},
    # 程启琦 — 区领导
    {"id":10,"person_id":8,"org_id":2,"title":"城厢区领导","start":"","end":"至今","rank":"副处级","note":""},
    # 陈美钗 — 区领导
    {"id":11,"person_id":9,"org_id":1,"title":"城厢区领导","start":"","end":"至今","rank":"副处级","note":""},
    # 郑松青 — 前任区委书记
    {"id":12,"person_id":10,"org_id":1,"title":"城厢区委书记","start":"","end":"2026-07","rank":"县处级","note":"后由王文晖接任"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 王文晖 vs 黄建恩 — 党政搭档
    {"id":1,"person_a":1,"person_b":2,"type":"党政搭档",
     "context":"王文晖（区委书记）与黄建恩（代区长）在城厢区共事",
     "overlap_org":"城厢区","overlap_period":"2026-07至今"},

    # 郑松青 → 王文晖 前后任
    {"id":2,"person_a":10,"person_b":1,"type":"前后任",
     "context":"郑松青（前任书记）→ 王文晖（现任书记）",
     "overlap_org":"中共莆田市城厢区委员会","overlap_period":"不重叠（前后任）"},

    # 王文晖 → 黄建恩 前后任（区长交接）
    {"id":3,"person_a":1,"person_b":2,"type":"前后任",
     "context":"王文晖升任区委书记后，黄建恩接任代区长",
     "overlap_org":"莆田市城厢区人民政府","overlap_period":"不重叠（前后任）"},
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
lines.append('    <description>城厢区（莆田市辖区）领导班子工作关系网络 — 2026年7月生成</description>')
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
print("\nNOTE: This data requires verification. Key items:")
print("  1. Verify full names and birth/education details for all officials")
print("  2. Confirm 王文晖's career before becoming 区长")
print("  3. Confirm 黄建恩's career before becoming 代区长")
print("  4. Confirm 郑松青's departure date and new position")
print("  5. Add standing committee members (区纪委、组织部、宣传部、政法委等)")
print("  6. Add more deputy positions and refine existing ones")
