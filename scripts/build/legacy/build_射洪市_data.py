#!/usr/bin/env python3
"""射洪市 领导班子工作关系网络 — 数据构建脚本 (v3, 2026-07-27 updated with 文加武 confirmed)"""

import sqlite3
import os
from datetime import datetime

SLUG = "射洪市"
BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "data", "database", f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, "data", "graph", f"{SLUG}_network.gexf")

ORGANIZATIONS = [
    (1, "中共射洪市委员会", "党委", "县级市", "中共遂宁市委", "遂宁市射洪市"),
    (2, "射洪市人民政府", "政府", "县级市", "遂宁市人民政府", "遂宁市射洪市"),
    (3, "射洪市人大常委会", "人大", "县级市", "遂宁市人大常委会", "遂宁市射洪市"),
    (4, "射洪市政协委员会", "政协", "县级市", "遂宁市政协", "遂宁市射洪市"),
    (5, "射洪市公安局", "政府", "市级", "射洪市人民政府", "遂宁市射洪市"),
    (6, "中共遂宁市委", "党委", "地级市", "中共四川省委", "遂宁市"),
    (7, "四川沱牌绿色生态食品产业园", "政府", "产业园", "射洪市人民政府", "遂宁市射洪市"),
    (8, "遂宁国家农业科技园区", "政府", "园区", "射洪市人民政府", "遂宁市射洪市"),
    (9, "中共射洪市委政法委员会", "党委", "市级", "中共射洪市委", "遂宁市射洪市"),
]

PERSONS = [
    (1,  "皮国平",       "男", "汉族",   None, None, None, None, None,
     "中共射洪市委书记", "中共射洪市委", None),
    (2,  "王能",         "男", "汉族",   "1974年1月", "四川蓬溪", "硕士研究生", "1997年10月", "1994年7月",
     "射洪市委副书记、市长、市政府党组书记", "射洪市人民政府", None),
    (3,  "荣泽黎",       "男", "汉族",   "1986年9月", "四川蓬溪", "党校研究生", "2008年10月", "2007年7月",
     "射洪市委常委、常务副市长、统战部部长，市政府党组副书记", "射洪市人民政府", None),
    (4,  "周昊",         "男", "汉族",   "1981年3月", "四川通江", "党校研究生", "2004年4月", "2001年9月",
     "射洪市委常委、副市长（挂职）", "射洪市人民政府", None),
    (5,  "唐锐",         "男", "汉族",   "1979年12月", "四川遂宁", "西南大学农业推广研究生", "2004年6月", "2001年5月",
     "射洪市副市长、市公安局局长", "射洪市公安局", None),
    (6,  "钱洪杰",       "女", "汉族",   "1985年12月", "四川大英", "大学", "民革党员", "2005年12月",
     "射洪市副市长", "射洪市人民政府", None),
    (7,  "努尔江·布拉别克", "男", "哈萨克族", "1989年7月", "新疆特克斯", "研究生", "2010年11月", "2015年11月",
     "射洪市副市长", "射洪市人民政府", None),
    (8,  "刘睿江",       "男", "汉族",   "1984年5月", "四川大英", "研究生", "2011年6月", "2008年12月",
     "射洪市副市长", "射洪市人民政府", None),
    (9,  "唐昆仑",       "男", "汉族",   "1971年12月", "四川安居", "大学", "1994年1月", "1994年8月",
     "射洪市政府党组成员、遂宁国家农业科技园区党工委书记", "射洪市人民政府", None),
    (10, "张俊懿",       "男", "汉族",   None, None, None, None, None,
     "前任市委书记", "中共射洪市委", None),
    (11, "文加武",       "男", "汉族",   None, None, None, None, None,
     "射洪市委常委、政法委书记", "中共射洪市委政法委员会", None),
    (12, "夏礼",         "男", "汉族",   None, None, None, None, None,
     "射洪市领导（职务待确认）", "射洪市人民政府", None),
    (13, "管行",         "男", "汉族",   None, None, None, None, None,
     "射洪市领导（职务待确认）", "射洪市人民政府", None),
    (14, "周素全",       "男", "汉族",   None, None, None, None, None,
     "射洪市人民法院院长", "射洪市人民法院", None),
    (15, "程龙",         "男", "汉族",   None, None, None, None, None,
     "射洪市人民检察院检察长", "射洪市人民检察院", None),
]

POSITIONS = [
    (1,  1, "中共射洪市委书记", "2026-07", None, "正县级"),
    (10, 1, "遂宁市委常委、射洪市委书记（前任）", None, "2026-07", "副厅级"),
    (2,  2, "射洪市委副书记、市长、市政府党组书记", None, None, "正县级"),
    (3,  2, "射洪市委常委、常务副市长、统战部部长", None, None, "副县级"),
    (4,  2, "射洪市委常委、副市长（挂职）", None, None, "挂职"),
    (5,  5, "射洪市副市长、市公安局局长", None, None, "副县级"),
    (6,  2, "射洪市副市长", None, None, "副县级"),
    (7,  2, "射洪市副市长", None, None, "副县级"),
    (8,  2, "射洪市副市长", None, None, "副县级"),
    (9,  8, "射洪市政府党组成员、遂宁国家农业科技园区党工委书记", None, None, "副县级"),
    (11, 9, "射洪市委常委、政法委书记", None, None, "副县级"),
    (12, 2, "射洪市领导（职务待确认）", None, None, None),
    (13, 2, "射洪市领导（职务待确认）", None, None, None),
    (14, 1, "射洪市人民法院院长", None, None, "副县级"),
    (15, 1, "射洪市人民检察院检察长", None, None, "副县级"),
]

PAIRS = [
    (1, 2, "党政搭档", "市委书记+市长搭班子", "射洪市委/市政府", "2026年7月至今"),
    (1, 3, "上下级", "市委书记+常务副市长", "射洪市委/市政府", "2026年7月至今"),
    (1, 10, "前后任", "皮国平接替张俊懿", "中共射洪市委", "2026年7月"),
    (1, 11, "上下级", "市委书记+政法委书记", "中共射洪市委", "2026年7月至今"),
    (10, 2, "前任搭档", "前任书记与市长", "射洪市委/市政府", "至2026年7月"),
    (2, 3, "上下级+同乡", "市长+常务副市长（均蓬溪籍）", "射洪市政府", "至今"),
    (2, 4, "上下级", "市长+挂职副市长", "射洪市政府", "至今"),
    (2, 8, "上下级", "市长+副市长刘睿江", "射洪市政府", "至今"),
    (3, 4, "同僚", "常务副市长+挂职副市长", "射洪市政府", "至今"),
    (11, 5, "政法系统上下级", "政法委书记+公安局长", "射洪政法系统", "至今"),
    (11, 14, "政法系统", "政法委书记+法院院长", "射洪政法系统", "至今"),
    (11, 15, "政法系统", "政法委书记+检察院检察长", "射洪政法系统", "至今"),
    (2, 3, "同乡", "蓬溪同乡", "四川蓬溪", "出生地"),
]

def create_tables(conn):
    conn.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS persons;
        DROP TABLE IF EXISTS organizations;
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT,
            source TEXT
        );
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        );
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER, title TEXT,
            start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER, type TEXT,
            context TEXT, overlap_org TEXT, overlap_period TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

def insert_data(conn):
    for row in PERSONS:
        conn.execute("INSERT INTO persons (id,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", row)
    for row in ORGANIZATIONS:
        conn.execute("INSERT INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)", row)
    for row in POSITIONS:
        conn.execute("INSERT INTO positions (person_id,org_id,title,start,end,rank) VALUES (?,?,?,?,?,?)", row)
    for row in PAIRS:
        conn.execute("INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)", row)
    conn.commit()

def esc(s):
    """XML-escape a string."""
    if s is None: return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append('    <description>射洪市领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="post" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('      <attribute id="3" title="gender" type="string"/>')
    lines.append('      <attribute id="4" title="ethnicity" type="string"/>')
    lines.append('      <attribute id="5" title="birth" type="string"/>')
    lines.append('    </attributes>')
    # Colors
    CM = {"皮国平":"255,50,50","张俊懿":"200,80,80","王能":"50,100,255","荣泽黎":"50,150,220","文加武":"210,130,30"}
    # Nodes
    lines.append('    <nodes>')
    for p in PERSONS:
        pid,name = str(p[0]),str(p[1])
        c = CM.get(name,"160,160,160")
        sz = "20.0" if name in ("皮国平","王能") else "14.0" if name in ("荣泽黎","文加武") else "12.0"
        lines.append(f'      <node id="{pid}" label="{esc(name)}">')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p[9] or "")}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p[10] or "")}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p[2] or "")}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p[3] or "")}"/>')
        lines.append(f'          <attvalue for="5" value="{esc(p[4] or "")}"/>')
        lines.append('        </attvalues>')
        lines.append('      </node>')
    for o in ORGANIZATIONS:
        oid = f"org_{o[0]}"
        lines.append(f'      <node id="{oid}" label="{esc(o[1])}">')
        lines.append('        <viz:color r="180" g="180" b="180"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="org"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o[1])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o[2])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </node>')
    lines.append('    </nodes>')
    # Edges
    lines.append('    <edges>')
    eid = 0
    for pos in POSITIONS:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="{pos[0]}" target="org_{pos[1]}" label="{esc(pos[3] or "worked_at")}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    for pair in PAIRS:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="{pair[0]}" target="{pair[1]}" label="{esc(pair[2])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(pair[2])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pair[3])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pair[4])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(pair[5] or "")}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')
    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')
    lines.append('  </graph>')
    lines.append('</gexf>')
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

if __name__=="__main__":
    os.makedirs(os.path.dirname(DB_PATH),exist_ok=True)
    conn=sqlite3.connect(DB_PATH)
    try: create_tables(conn); insert_data(conn)
    finally: conn.close()
    print(f"  DB: {DB_PATH}\n    persons={len(PERSONS)} orgs={len(ORGANIZATIONS)} positions={len(POSITIONS)} relationships={len(set((a,b) for a,b,_,_,_,_ in PAIRS))}")
    build_gexf(); print(f"  GEXF: {GEXF_PATH} written")
