#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 马尾区 (Mawei District), 福州市, 福建省.

Covers: district-level leaders (party secretary, district mayor, standing committee,
vice mayors), plus predecessor chain and key connections.

Sources:
- Mawei District Government official website (mawei.gov.cn) — news and leadership mentions
- Mawei News (mwnews.cn)
- Official government meeting/news pages

Current as of: July 2026

Key findings:
- 区委书记: 张锋 (confirmed from July 2026 news articles)
- 区委副书记、代区长: 郑浩 (区政府党组书记、代区长, confirmed from July 2026 news)
- 陈健海 was removed as 副区长 in June 2026 (11th NPC Standing Committee 53rd session)

Note: Birth dates, education, and full career timelines for most officials
require on-site verification of the government leadership page.
"""

import sqlite3, os, sys
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "马尾区_network.db")
GEXF_PATH = os.path.join(BASE, "马尾区_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ═════════════════════════════════════════════════════════════════════
    # Current top leadership
    # ═════════════════════════════════════════════════════════════════════

    # 张锋 — 马尾区委书记 (confirmed from district news, July 2026)
    {"id":1,"name":"张锋","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"马尾区委书记","current_org":"中共福州市马尾区委员会",
     "source":"https://www.mawei.gov.cn/xjwz/zwgk/gzdt/mwyw/202607/t20260716_5347166.htm"},

    # 郑浩 — 马尾区委副书记、代区长 (confirmed from official news, July 2026)
    {"id":2,"name":"郑浩","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"马尾区委副书记、区政府党组书记、代区长","current_org":"福州市马尾区人民政府",
     "source":"https://www.mawei.gov.cn/xjwz/zwgk/gzdt/mwyw/202607/t20260715_5346751.htm"},

    # ═════════════════════════════════════════════════════════════════════
    # Current government leadership team (区政府领导)
    # ═════════════════════════════════════════════════════════════════════

    # 江典顺 — 区领导（区委常委、副区长级）
    {"id":3,"name":"江典顺","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"马尾区委常委、副区长（或常务副区长）","current_org":"福州市马尾区人民政府",
     "source":"https://www.mawei.gov.cn/xjwz/zwgk/gzdt/mwyw/202607/t20260710_5344984.htm"},

    # 王栋梁 — 区领导
    {"id":4,"name":"王栋梁","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"马尾区领导","current_org":"福州市马尾区人民政府",
     "source":"https://www.mawei.gov.cn/xjwz/zwgk/gzdt/mwyw/202607/t20260710_5344984.htm"},

    # 林建豪 — 区领导
    {"id":5,"name":"林建豪","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"马尾区领导","current_org":"福州市马尾区人民政府",
     "source":"https://www.mawei.gov.cn/xjwz/zwgk/gzdt/mwyw/202607/t20260710_5344980.htm"},

    # 张琴 — 区领导 (参与船政文化景区建设工作)
    {"id":6,"name":"张琴","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"马尾区领导","current_org":"福州市马尾区人民政府",
     "source":"https://www.mwnews.cn/html/2/20260707/6a4c4b2f00dc0.shtml"},

    # 林隽 — 区领导 (参与船政文化景区建设工作)
    {"id":7,"name":"林隽","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"马尾区领导","current_org":"福州市马尾区人民政府",
     "source":"https://www.mwnews.cn/html/2/20260707/6a4c4b2f00dc0.shtml"},

    # 徐国珍 — 区领导 (参与船政文化景区建设工作)
    {"id":8,"name":"徐国珍","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"马尾区领导","current_org":"福州市马尾区人民政府",
     "source":"https://www.mwnews.cn/html/2/20260707/6a4c4b2f00dc0.shtml"},

    # 金剑钊 — 区政协党组成员、副主席，区工信局党组书记、局长
    {"id":9,"name":"金剑钊","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"马尾区政协党组成员、副主席，区工信局党组书记、局长","current_org":"中国人民政治协商会议福州市马尾区委员会",
     "source":"https://www.mawei.gov.cn/xjwz/hdjl/zxft/wqft/202606/t20260604_5330331.htm"},

    # ═════════════════════════════════════════════════════════════════════
    # Other key officials
    # ═════════════════════════════════════════════════════════════════════

    # 陈巍 — 区人大常委会主任
    {"id":10,"name":"陈巍","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"马尾区人大常委会主任","current_org":"福州市马尾区人民代表大会常务委员会",
     "source":"https://www.mwnews.cn/html/2/20260709/6a4f02d8b9312.shtml"},

    # 陈健海 — 原副区长（2026年6月被免职）
    {"id":11,"name":"陈健海","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"原马尾区副区长（2026年6月被免职）","current_org":"福州市马尾区人民政府",
     "source":"https://www.mawei.gov.cn/xjwz/zwgk/rsxx/rsrm/202606/t20260618_5335991.htm"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1,"name":"中共福州市马尾区委员会","type":"党委","level":"县处级","parent":"中共福州市委员会","location":"福州市马尾区"},
    {"id":2,"name":"福州市马尾区人民政府","type":"政府","level":"县处级","parent":"福州市人民政府","location":"福州市马尾区"},
    {"id":3,"name":"福州市马尾区人民代表大会常务委员会","type":"人大","level":"县处级","parent":"福州市人民代表大会常务委员会","location":"福州市马尾区"},
    {"id":4,"name":"中国人民政治协商会议福州市马尾区委员会","type":"政协","level":"县处级","parent":"中国人民政治协商会议福州市委员会","location":"福州市马尾区"},
    {"id":5,"name":"福州经济技术开发区管理委员会","type":"开发区","level":"国家级","parent":"福州市人民政府","location":"福州市马尾区"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 张锋
    {"id":1,"person_id":1,"org_id":1,"title":"马尾区委书记","start":"","end":"","rank":"县处级","note":"现任，2026年7月在任"},
    # 郑浩
    {"id":2,"person_id":2,"org_id":2,"title":"马尾区委副书记、区政府党组书记、代区长","start":"","end":"","rank":"县处级","note":"现任，2026年7月在任"},
    # 江典顺
    {"id":3,"person_id":3,"org_id":2,"title":"区委常委、副区长（或常务副区长）","start":"","end":"","rank":"县处级","note":"2026年7月在任"},
    # 王栋梁
    {"id":4,"person_id":4,"org_id":2,"title":"马尾区领导","start":"","end":"","rank":"县处级","note":"2026年7月在任"},
    # 林建豪
    {"id":5,"person_id":5,"org_id":2,"title":"马尾区领导","start":"","end":"","rank":"县处级","note":"2026年7月在任"},
    # 张琴
    {"id":6,"person_id":6,"org_id":2,"title":"马尾区领导","start":"","end":"","rank":"县处级","note":"2026年7月在任"},
    # 林隽
    {"id":7,"person_id":7,"org_id":2,"title":"马尾区领导","start":"","end":"","rank":"县处级","note":"2026年7月在任"},
    # 徐国珍
    {"id":8,"person_id":8,"org_id":2,"title":"马尾区领导","start":"","end":"","rank":"县处级","note":"2026年7月在任"},
    # 金剑钊
    {"id":9,"person_id":9,"org_id":4,"title":"区政协党组成员、副主席","start":"","end":"","rank":"县处级","note":"2026年在任"},
    {"id":10,"person_id":9,"org_id":2,"title":"区工信局党组书记、局长","start":"","end":"","rank":"正科级","note":"2026年在任"},
    # 陈巍
    {"id":11,"person_id":10,"org_id":3,"title":"区人大常委会主任","start":"","end":"","rank":"县处级","note":"2026年7月在任"},
    # 陈健海
    {"id":12,"person_id":11,"org_id":2,"title":"副区长","start":"","end":"2026-06","rank":"县处级","note":"2026年6月17日被区人大常委会免职"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 张锋 vs 郑浩 — 党政搭档
    {"id":1,"person_a":1,"person_b":2,"type":"党政搭档",
     "context":"张锋（区委书记）与郑浩（代区长）在马尾区共事",
     "overlap_org":"马尾区","overlap_period":"2026至今"},

    # 张锋 vs 江典顺 — 上下级
    {"id":2,"person_a":1,"person_b":3,"type":"上下级",
     "context":"张锋（区委书记）与江典顺（区委常委）在马尾区委共事",
     "overlap_org":"中共福州市马尾区委员会","overlap_period":"2026至今"},

    # 郑浩 vs 江典顺 — 政府班子搭档
    {"id":3,"person_a":2,"person_b":3,"type":"政府班子",
     "context":"郑浩（代区长）与江典顺（副区长）在马尾区政府共事",
     "overlap_org":"福州市马尾区人民政府","overlap_period":"2026至今"},

    # 郑浩 vs 陈巍 — 党政+人大
    {"id":4,"person_a":2,"person_b":10,"type":"党政+人大",
     "context":"郑浩与陈巍（区人大主任）工作交集",
     "overlap_org":"福州市马尾区","overlap_period":"2026至今"},
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
    if "人大常委会" in post or "人大" in post:
        return "200,255,255"  # cyan for 人大
    if "政协" in post:
        return "255,240,200"  # cream for 政协
    return "120,120,120"

def ocolor(otype):
    return {"党委":"255,200,200","政府":"200,200,255","开发区":"200,255,200","人大":"200,255,255","政协":"255,240,200"}.get(otype,"200,200,200")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Sisyphus Research Agent</creator>')
lines.append('    <description>马尾区（福州市辖区）领导班子工作关系网络 — 2026年7月生成</description>')
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
print("  1. Verify 张锋's full name and birth/education details")
print("  2. Verify 郑浩's full name and birth/education details")
print("  3. Find predecessor of 张锋 (previous party secretary)")
print("  4. Complete career timelines for all officials")
print("  5. Add standing committee members (区纪委、组织部、宣传部、政法委等)")
print("  6. Verify exact official titles for 江典顺, 王栋梁, 林建豪, 张琴, 林隽, 徐国珍")
