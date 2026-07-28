#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 椒江区 (Jiaojiang District), 台州市, 浙江省.

Covers: district-level leaders (party secretary, district mayor, standing committee,
vice district mayors), predecessor chain, and key connections.

Sources:
- Jiaojiang District Government official website (jj.gov.cn) — news, leadership division, appointments
- Taizhou City Government (zjtz.gov.cn)
- Official appointment notices

Current as of: July 2026

⚠️ NOTE: Biographical details (birth dates, education, birthplace) for most officials
could not be confirmed from open web sources due to Baidu Baike blocking and search
engine rate limits. This data should be supplemented with on-site government website
verification.
"""

import sqlite3, os, sys
from datetime import datetime

STAGING = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(STAGING, "..", "..", "scripts", "build")
DB_PATH = os.path.join(STAGING, "椒江区_network.db")
GEXF_PATH = os.path.join(STAGING, "椒江区_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ═════════════════════════════════════════════════════════════════════
    # Current top leadership (confirmed from official news, July 2026)
    # ═════════════════════════════════════════════════════════════════════
    {"id":1,"name":"林强","gender":"","ethnicity":"","birth":"","birthplace":"",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"椒江区委书记","current_org":"中共台州市椒江区委员会",
     "source":"http://www.jj.gov.cn/col/col1311043/art/2026/art_36ab5686e52641deb625ae62410080f0.html — 区委书记林强主持召开会议"},

    {"id":2,"name":"陈永兵","gender":"","ethnicity":"","birth":"","birthplace":"",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"椒江区委副书记、区长","current_org":"椒江区人民政府",
     "source":"http://www.jj.gov.cn/col/col1311043/art/2026/art_1bba0058e7254650abcc9777361d2c1a.html — 区长陈永兵主持会议"},

    # ═════════════════════════════════════════════════════════════════════
    # Deputy district mayors (confirmed from government work division notice, May 2026)
    # ═════════════════════════════════════════════════════════════════════

    # 谢海君 — 常务副区长
    {"id":3,"name":"谢海君","gender":"","ethnicity":"","birth":"","birthplace":"",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"椒江区委常委、常务副区长","current_org":"椒江区人民政府",
     "source":"http://www.jj.gov.cn/col/col1229458117/art/2026/art_e505f7b34a5442ca9bf4e55e1aa14d0f.html — 政府领导班子分工通知"},

    # 张升 — 副区长
    {"id":4,"name":"张升","gender":"","ethnicity":"","birth":"","birthplace":"",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"椒江区副区长（主持椒江经济开发区）","current_org":"椒江区人民政府",
     "source":"http://www.jj.gov.cn/col/col1229458117/art/2026/art_e5f7b344a5442ca9bf4e55e1aa14d0f.html"},

    # 金霄翔 — 副区长（挂职色达）
    {"id":5,"name":"金霄翔","gender":"","ethnicity":"","birth":"","birthplace":"",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"椒江区副区长（挂职四川色达）","current_org":"椒江区人民政府",
     "source":"同上"},

    # 王巍 — 副区长
    {"id":6,"name":"王巍","gender":"","ethnicity":"","birth":"","birthplace":"",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"椒江区副区长","current_org":"椒江区人民政府",
     "source":"同上"},

    # 蒋吉清 — 副区长
    {"id":7,"name":"蒋吉清","gender":"","ethnicity":"","birth":"","birthplace":"",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"椒江区副区长","current_org":"椒江区人民政府",
     "source":"同上"},

    # 董世虎 — 副区长（公安）
    {"id":8,"name":"董世虎","gender":"","ethnicity":"","birth":"","birthplace":"",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"椒江区副区长、区公安分局局长","current_org":"椒江区人民政府",
     "source":"同上"},

    # 曾程耀 — 副区长
    {"id":9,"name":"曾程耀","gender":"","ethnicity":"","birth":"","birthplace":"",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"椒江区副区长","current_org":"椒江区人民政府",
     "source":"同上"},

    # 杨宇 — 副区长
    {"id":10,"name":"杨宇","gender":"","ethnicity":"","birth":"","birthplace":"",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"椒江区副区长","current_org":"椒江区人民政府",
     "source":"同上"},

    # 丁海顺 — 副区长
    {"id":11,"name":"丁海顺","gender":"","ethnicity":"","birth":"","birthplace":"",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"椒江区副区长","current_org":"椒江区人民政府",
     "source":"同上"},

    # 孙天波 — 副区长（政府工作报告列明）
    {"id":12,"name":"孙天波","gender":"","ethnicity":"","birth":"","birthplace":"",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"椒江区副区长","current_org":"椒江区人民政府",
     "source":"http://www.jj.gov.cn/col/col1229458124/art/2026/art_7958521bb5d9466db529ea5a26db4888.html — 政府工作报告"},

    # 盛光义 — 区领导（列席三大牵引性抓手例会）
    {"id":13,"name":"盛光义","gender":"","ethnicity":"","birth":"","birthplace":"",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"椒江区领导","current_org":"中共椒江区委员会",
     "source":"http://www.jj.gov.cn/col/col1311043/art/2026/art_36ab5686e52641deb625ae62410080f0.html"},

    # 倪国正 — 大陈镇/区领导
    {"id":14,"name":"倪国正","gender":"","ethnicity":"","birth":"","birthplace":"",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"大陈岛开发建设管委会负责人","current_org":"大陈岛开发建设管委会",
     "source":"政府工作报告责任分解"},

    # ═════════════════════════════════════════════════════════════════════
    # Predecessors (limited information from available sources)
    # ═════════════════════════════════════════════════════════════════════

    # 前任区委书记 — 据分析林强可能是在2024-2025年接任此前一任书记
    # NOTE: 林强的具体接任时间和前任信息未能从公开网络确认
    {"id":15,"name":"（前任区委书记待确认）","gender":"","ethnicity":"","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"椒江区委书记（前任）","current_org":"中共椒江区委员会",
     "source":"待补充——需查阅台州市委组织部任前公示和椒江区领导之窗历史页面"},

    # 前任区长 — 未知
    {"id":16,"name":"（前任区长待确认）","gender":"","ethnicity":"","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"椒江区区长（前任）","current_org":"椒江区人民政府",
     "source":"待补充——需查阅历史新闻和任免文件"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1,"name":"中共台州市椒江区委员会","type":"党委","level":"县处级","parent":"中共台州市委员会","location":"台州市椒江区"},
    {"id":2,"name":"椒江区人民政府","type":"政府","level":"县处级","parent":"台州市人民政府","location":"台州市椒江区"},
    {"id":3,"name":"椒江区人大常委会","type":"人大","level":"县处级","parent":"台州市人民代表大会常务委员会","location":"台州市椒江区"},
    {"id":4,"name":"椒江区政协","type":"政协","level":"县处级","parent":"台州市政协","location":"台州市椒江区"},
    {"id":5,"name":"椒江区纪律检查委员会","type":"纪委","level":"副县处级","parent":"中共台州市纪律检查委员会","location":"台州市椒江区"},
    {"id":6,"name":"椒江经济开发区管委会","type":"开发区","level":"副县处级","parent":"椒江区人民政府","location":"台州市椒江区"},
    {"id":7,"name":"大陈岛开发建设管委会","type":"事业单位","level":"副县处级","parent":"椒江区人民政府","location":"椒江区大陈镇"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 林强 — 区委书记
    {"id":1,"person_id":1,"org_id":1,"title":"椒江区委书记","start":"","end":"至今","rank":"正处级","note":"主持会议2026年7月"},
    # 陈永兵 — 区长
    {"id":2,"person_id":2,"org_id":1,"title":"椒江区委副书记","start":"","end":"至今","rank":"正处级","note":"见2026年政府工作报告"},
    {"id":3,"person_id":2,"org_id":2,"title":"椒江区区长","start":"","end":"至今","rank":"正处级","note":"主持区政府全面工作"},

    # 谢海君 — 常务副区长
    {"id":4,"person_id":3,"org_id":2,"title":"常务副区长","start":"","end":"至今","rank":"副处级","note":"分管发改、财税、审计等"},
    # 张升
    {"id":5,"person_id":4,"org_id":2,"title":"副区长","start":"","end":"至今","rank":"副处级","note":"主持椒江经济开发区工作"},
    {"id":6,"person_id":4,"org_id":6,"title":"椒江经济开发区负责人","start":"","end":"至今","rank":"","note":""},
    # 金霄翔
    {"id":7,"person_id":5,"org_id":2,"title":"副区长（挂职）","start":"","end":"至今","rank":"副处级","note":"选四川色达县挂职"},
    # 王巍
    {"id":8,"person_id":6,"org_id":2,"title":"副区长","start":"","end":"至今","rank":"副处级","note":"分管教育、环保、民政、卫健等"},
    # 蒋吉清
    {"id":9,"person_id":7,"org_id":2,"title":"副区长","start":"","end":"至今","rank":"副处级","note":"分管科技文广体旅、行政服务等"},
    # 董世虎
    {"id":10,"person_id":8,"org_id":2,"title":"副区长","start":"","end":"至今","rank":"副处级","note":"主持区公安分局"},
    # 曾程耀
    {"id":11,"person_id":9,"org_id":2,"title":"副区长","start":"","end":"至今","rank":"副处级","note":"分管交通、农业农村、水利等"},
    # 杨宇
    {"id":12,"person_id":10,"org_id":2,"title":"副区长","start":"","end":"至今","rank":"副处级","note":"分管商务、市场监管、金融等"},
    # 丁海顺
    {"id":13,"person_id":11,"org_id":2,"title":"副区长","start":"","end":"至今","rank":"副处级","note":"分管住建、综合执法、一江两岸等"},
    # 孙天波
    {"id":14,"person_id":12,"org_id":2,"title":"副区长","start":"","end":"至今","rank":"副处级","note":"分管住建相关工作在政府报告列出"},
    # 盛光义
    {"id":15,"person_id":13,"org_id":1,"title":"椒江区领导","start":"","end":"至今","rank":"","note":"在三大牵引性抓手例会参会"},
    # 倪国正 — 大陈岛
    {"id":16,"person_id":14,"org_id":7,"title":"大陈岛开发建设管委会负责人","start":"","end":"至今","rank":"","note":""},

    # 前任区委书记
    {"id":17,"person_id":15,"org_id":1,"title":"椒江区委书记（前任）","start":"","end":"","rank":"正处级","note":"姓名不详，需进一步确认"},

    # 前任区长
    {"id":18,"person_id":16,"org_id":2,"title":"椒江区区长（前任）","start":"","end":"","rank":"正处级","note":"姓名不详，需进一步确认"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 林强 ↔ 陈永兵 — 党政搭档
    {"id":1,"person_a":1,"person_b":2,"type":"党政搭档",
     "context":"林强（区委书记）与陈永兵（区长、副书记）在椒江区党政领导班子组成工作搭档",
     "overlap_org":"中共椒江区委员会","overlap_period":"2025至今"},

    # 林强 ↔ 前区委书记 — 前后任
    {"id":2,"person_a":15,"person_b":1,"type":"前后任",
     "context":"前任椒江区委书记（待确认）与林强在区委书记职务上前后续接",
     "overlap_org":"中共椒江区委员会","overlap_period":"不重叠"},

    # 陈永兵 ↔ 前任区长
    {"id":3,"person_a":16,"person_b":2,"type":"前后任",
     "context":"前任椒江区区长（待确认）与陈永兵在区长职务上前后续接",
     "overlap_org":"椒江区人民政府","overlap_period":"不重叠"},

    # 谢海君 ↔ 陈永兵 — 上下级
    {"id":4,"person_a":3,"person_b":2,"type":"上下级",
     "context":"常务副区长谢海君辅助区长陈永兵分管常务工作",
     "overlap_org":"椒江区人民政府","overlap_period":"2026年至今"},

    # 张升 ↔ 陈永兵 — 上下级
    {"id":5,"person_a":4,"person_b":2,"type":"上下级",
     "context":"副区长张升向区长陈永兵汇报经济开发区工作",
     "overlap_org":"椒江区人民政府","overlap_period":"2026年至今"},

    # 区政府班子成员 — 共同任职
    {"id":6,"person_a":3,"person_b":4,"type":"共同任职",
     "context":"谢海君与张升同为椒江区副区长在区政府共事",
     "overlap_org":"椒江区人民政府","overlap_period":"2026年至今"},

    # 集体 — 区委常委会
    {"id":7,"person_a":1,"person_b":3,"type":"上下级",
     "context":"区委书记林强对常务副区长谢海君的工作有领导关系",
     "overlap_org":"中共椒江区委员会","overlap_period":"2026年至今"},
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
    if "区委书记" in post and "区委副书记" not in post:
        return "230,50,50"
    if "区委副书记" in post or "区长" in post:
        return "50,100,230"
    if "常务副" in post:
        return "80,130,230"
    if "副区长" in post:
        return "90,150,230"
    if "人大" in post:
        return "180,200,255"
    if "政协" in post:
        return "200,255,200"
    if "纪委书记" in post:
        return "255,165,0"
    return "120,120,120"

def ocolor(otype):
    colors = {
        "党委":"255,200,200",
        "政府":"200,200,255",
        "人大":"200,230,255",
        "政协":"200,255,200",
        "纪委":"255,220,180",
        "事业单位":"220,220,220",
    }
    return colors.get(otype, "200,200,200")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Sisyphus Research Agent</creator>')
lines.append('    <description>台州市椒江区（市辖区）领导班子工作关系网络 — 2026年7月生成</description>')
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
    sz = "20.0" if any(k in p.get("current_post","") for k in ["区委书记","区长","区委副书记"]) else "12.0"
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
    for k,v in [("0","organization"),("1",""),("2",o.get("location","")),("3",""),("4","organization"),("5",o.get("level",""))]:
        lines.append(f'          <attvalue for="{k}" value="{esc(v)}"/>')
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
    for k,v in [("0","worked_at"),("1",pos.get("start","")),("2",pos.get("end","")),("3",pos.get("note",""))]:
        lines.append(f'          <attvalue for="{k}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')
for r in relationships:
    eid += 1
    ov = r.get("overlap_period","")
    lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
    lines.append('        <attvalues>')
    for k,v in [("0",r["type"]),("1",ov),("2",""),("3",r.get("context",""))]:
        lines.append(f'          <attvalue for="{k}" value="{esc(v)}"/>')
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
print("\n⚠️ NOTE: This data requires supplementation. Key gaps:")
print("  1. Fill in biographical details (birth dates, education, birthplace) for all officials")
print("  2. Identify full standing committee members (organization dept, propaganda, united front) when leadership page becomes accessible")
print("  3. Confirm previous party secretary and mayor names and their current positions")
print("  4. Add cross-county cadre exchange patterns with other Taizhou districts (Huangyan, Luqiao)")