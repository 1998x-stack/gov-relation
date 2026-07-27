#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 廉江市 (Lianjiang City), 湛江市, 广东省.

Covers: city-level leaders (市委书记, 市长), key standing committee members,
and organizational relationships.

Sources:
- 廉江市人民政府 official site: www.lianjiang.gov.cn (领导信息 page — confirmed)
- 湛江市人民政府: www.zhanjiang.gov.cn

Current as of: July 2026

Key findings:
- 市委书记: 曾平治 (confirmed via 廉江市政府网站 领导信息栏目, 2026-07-22)
- 市长: 柯俊 (confirmed via 廉江市政府网站 领导信息栏目, 2026-07-22)
- Full leadership roster confirmed via official leadership page
"""

import sqlite3, os, sys
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "廉江市_network.db")
GEXF_PATH = os.path.join(BASE, "廉江市_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================

persons = [
    # ═════════════════════════════════════════════════════════════════════
    # Current leadership — 市委
    # ═════════════════════════════════════════════════════════════════════

    # 曾平治 — 廉江市委书记
    {"id": 1, "name": "曾平治", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "廉江市委书记", "current_org": "中共廉江市委员会",
     "source": "廉江市人民政府网站 — 领导信息栏目（2026-07-22确认）"},

    # 柯俊 — 廉江市委副书记、市长
    {"id": 2, "name": "柯俊", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "廉江市委副书记、市长", "current_org": "廉江市人民政府",
     "source": "廉江市人民政府网站 — 领导信息栏目（2026-07-22确认）"},

    # 李雪 — 廉江市委副书记
    {"id": 3, "name": "李雪", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "廉江市委副书记", "current_org": "中共廉江市委员会",
     "source": "廉江市人民政府网站 — 领导信息栏目（2026-07-22确认）"},

    # 陶加辉 — 廉江市委副书记
    {"id": 4, "name": "陶加辉", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "廉江市委副书记", "current_org": "中共廉江市委员会",
     "source": "廉江市人民政府网站 — 领导信息栏目（2026-07-22确认）"},

    # ═════════════════════════════════════════════════════════════════════
    # 市委常委
    # ═════════════════════════════════════════════════════════════════════

    # 李玉辉 — 市委常委、副市长
    {"id": 5, "name": "李玉辉", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "廉江市委常委、副市长", "current_org": "中共廉江市委员会/廉江市人民政府",
     "source": "廉江市人民政府网站 — 领导信息栏目（2026-07-22确认）"},

    # 陈荣 — 市委常委
    {"id": 6, "name": "陈荣", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "廉江市委常委", "current_org": "中共廉江市委员会",
     "source": "廉江市人民政府网站 — 领导信息栏目（2026-07-22确认）"},

    # 何荣拔 — 市委常委
    {"id": 7, "name": "何荣拔", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "廉江市委常委", "current_org": "中共廉江市委员会",
     "source": "廉江市人民政府网站 — 领导信息栏目（2026-07-22确认）"},

    # 王艳 — 市委常委
    {"id": 8, "name": "王艳", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "廉江市委常委", "current_org": "中共廉江市委员会",
     "source": "廉江市人民政府网站 — 领导信息栏目（2026-07-22确认）"},

    # 王丰 — 市委常委
    {"id": 9, "name": "王丰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "廉江市委常委", "current_org": "中共廉江市委员会",
     "source": "廉江市人民政府网站 — 领导信息栏目（2026-07-22确认）"},

    # 黄伟 — 市委常委、副市长
    {"id": 10, "name": "黄伟", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "廉江市委常委、副市长", "current_org": "中共廉江市委员会/廉江市人民政府",
     "source": "廉江市人民政府网站 — 领导信息栏目（2026-07-22确认）"},

    # 陈武略 — 市委常委、市纪委书记
    {"id": 11, "name": "陈武略", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "廉江市委常委、市纪委书记", "current_org": "中共廉江市纪律检查委员会",
     "source": "廉江市人民政府网站 — 领导信息栏目（2026-07-22确认）"},

    # ═════════════════════════════════════════════════════════════════════
    # 市政府副市长（非市委常委）
    # ═════════════════════════════════════════════════════════════════════

    # 郑王建 — 副市长
    {"id": 12, "name": "郑王建", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "廉江市副市长", "current_org": "廉江市人民政府",
     "source": "廉江市人民政府网站 — 领导信息栏目（2026-07-22确认）"},

    # 吴福东 — 副市长
    {"id": 13, "name": "吴福东", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "廉江市副市长", "current_org": "廉江市人民政府",
     "source": "廉江市人民政府网站 — 领导信息栏目（2026-07-22确认）"},

    # 王骁 — 副市长
    {"id": 14, "name": "王骁", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "廉江市副市长", "current_org": "廉江市人民政府",
     "source": "廉江市人民政府网站 — 领导信息栏目（2026-07-22确认）"},

    # 谢伟清 — 副市长
    {"id": 15, "name": "谢伟清", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "廉江市副市长", "current_org": "廉江市人民政府",
     "source": "廉江市人民政府网站 — 领导信息栏目（2026-07-22确认）"},

    # 梁伟霞 — 副市长
    {"id": 16, "name": "梁伟霞", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "廉江市副市长", "current_org": "廉江市人民政府",
     "source": "廉江市人民政府网站 — 领导信息栏目（2026-07-22确认）"},

    # ═════════════════════════════════════════════════════════════════════
    # 市人大
    # ═════════════════════════════════════════════════════════════════════

    # 李小军 — 市人大常委会主任候选人
    {"id": 17, "name": "李小军", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "廉江市人大常委会主任候选人", "current_org": "廉江市人民代表大会常务委员会",
     "source": "廉江市人民政府网站 — 领导信息栏目（2026-07-22确认）"},

    # 黄大庆 — 市政协主席
    {"id": 18, "name": "黄大庆", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "廉江市政协主席", "current_org": "中国人民政治协商会议廉江市委员会",
     "source": "廉江市人民政府网站 — 领导信息栏目（2026-07-22确认）"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共廉江市委员会", "type": "党委", "level": "县处级", "parent": "中共湛江市委员会", "location": "湛江市廉江市"},
    {"id": 2, "name": "廉江市人民政府", "type": "政府", "level": "县处级", "parent": "湛江市人民政府", "location": "湛江市廉江市"},
    {"id": 3, "name": "廉江市人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "湛江市人民代表大会常务委员会", "location": "湛江市廉江市"},
    {"id": 4, "name": "中国人民政治协商会议廉江市委员会", "type": "政协", "level": "县处级", "parent": "中国人民政治协商会议湛江市委员会", "location": "湛江市廉江市"},
    {"id": 5, "name": "中共廉江市纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共湛江市纪律检查委员会", "location": "湛江市廉江市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 曾平治
    {"id": 1, "person_id": 1, "org_id": 1, "title": "廉江市委书记", "start": "", "end": "", "rank": "县处级", "note": "当前在任，confirmed as of 2026-07-22"},
    # 柯俊
    {"id": 2, "person_id": 2, "org_id": 2, "title": "廉江市市长", "start": "", "end": "", "rank": "县处级", "note": "当前在任，confirmed as of 2026-07-22"},
    {"id": 3, "person_id": 2, "org_id": 1, "title": "廉江市委副书记", "start": "", "end": "", "rank": "县处级", "note": "兼任市委副书记"},
    # 李雪
    {"id": 4, "person_id": 3, "org_id": 1, "title": "廉江市委副书记", "start": "", "end": "", "rank": "县处级", "note": "当前在任"},
    # 陶加辉
    {"id": 5, "person_id": 4, "org_id": 1, "title": "廉江市委副书记", "start": "", "end": "", "rank": "县处级", "note": "当前在任"},
    # 李玉辉
    {"id": 6, "person_id": 5, "org_id": 1, "title": "廉江市委常委", "start": "", "end": "", "rank": "县处级", "note": "当前在任"},
    {"id": 7, "person_id": 5, "org_id": 2, "title": "廉江市副市长", "start": "", "end": "", "rank": "县处级", "note": "兼任副市长"},
    # 陈荣
    {"id": 8, "person_id": 6, "org_id": 1, "title": "廉江市委常委", "start": "", "end": "", "rank": "县处级", "note": "当前在任"},
    # 何荣拔
    {"id": 9, "person_id": 7, "org_id": 1, "title": "廉江市委常委", "start": "", "end": "", "rank": "县处级", "note": "当前在任"},
    # 王艳
    {"id": 10, "person_id": 8, "org_id": 1, "title": "廉江市委常委", "start": "", "end": "", "rank": "县处级", "note": "当前在任"},
    # 王丰
    {"id": 11, "person_id": 9, "org_id": 1, "title": "廉江市委常委", "start": "", "end": "", "rank": "县处级", "note": "当前在任"},
    # 黄伟
    {"id": 12, "person_id": 10, "org_id": 1, "title": "廉江市委常委", "start": "", "end": "", "rank": "县处级", "note": "当前在任"},
    {"id": 13, "person_id": 10, "org_id": 2, "title": "廉江市副市长", "start": "", "end": "", "rank": "县处级", "note": "兼任副市长"},
    # 陈武略
    {"id": 14, "person_id": 11, "org_id": 5, "title": "廉江市纪委书记", "start": "", "end": "", "rank": "县处级", "note": "当前在任"},
    {"id": 15, "person_id": 11, "org_id": 1, "title": "廉江市委常委", "start": "", "end": "", "rank": "县处级", "note": "兼任市委常委"},
    # 郑王建
    {"id": 16, "person_id": 12, "org_id": 2, "title": "廉江市副市长", "start": "", "end": "", "rank": "县处级", "note": "当前在任"},
    # 吴福东
    {"id": 17, "person_id": 13, "org_id": 2, "title": "廉江市副市长", "start": "", "end": "", "rank": "县处级", "note": "当前在任"},
    # 王骁
    {"id": 18, "person_id": 14, "org_id": 2, "title": "廉江市副市长", "start": "", "end": "", "rank": "县处级", "note": "当前在任"},
    # 谢伟清
    {"id": 19, "person_id": 15, "org_id": 2, "title": "廉江市副市长", "start": "", "end": "", "rank": "县处级", "note": "当前在任"},
    # 梁伟霞
    {"id": 20, "person_id": 16, "org_id": 2, "title": "廉江市副市长", "start": "", "end": "", "rank": "县处级", "note": "当前在任"},
    # 李小军
    {"id": 21, "person_id": 17, "org_id": 3, "title": "廉江市人大常委会主任候选人", "start": "", "end": "", "rank": "县处级", "note": "已公示为主任候选人"},
    # 黄大庆
    {"id": 22, "person_id": 18, "org_id": 4, "title": "廉江市政协主席", "start": "", "end": "", "rank": "县处级", "note": "当前在任"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 曾平治 vs 柯俊 — 党政搭档
    {"id": 1, "person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "曾平治（市委书记）与柯俊（市长）是廉江市核心党政搭档",
     "overlap_org": "廉江市", "overlap_period": "2026"},

    # 曾平治 vs 李雪 — 市委班子
    {"id": 2, "person_a": 1, "person_b": 3, "type": "上下级",
     "context": "曾平治（市委书记）与李雪（市委副书记）在市委班子中共事",
     "overlap_org": "中共廉江市委员会", "overlap_period": "2026"},

    # 曾平治 vs 陶加辉 — 市委班子
    {"id": 3, "person_a": 1, "person_b": 4, "type": "上下级",
     "context": "曾平治（市委书记）与陶加辉（市委副书记）在市委班子中共事",
     "overlap_org": "中共廉江市委员会", "overlap_period": "2026"},

    # 柯俊 vs 李玉辉 — 市长与副市长
    {"id": 4, "person_a": 2, "person_b": 5, "type": "上下级",
     "context": "柯俊（市长）与李玉辉（市委常委、副市长）在市政府班子中配合",
     "overlap_org": "廉江市人民政府", "overlap_period": "2026"},

    # 柯俊 vs 黄伟 — 市长与副市长
    {"id": 5, "person_a": 2, "person_b": 10, "type": "上下级",
     "context": "柯俊（市长）与黄伟（市委常委、副市长）在市政府班子中配合",
     "overlap_org": "廉江市人民政府", "overlap_period": "2026"},

    # 柯俊 vs 黄大庆 — 政府与政协
    {"id": 6, "person_a": 2, "person_b": 18, "type": "党政关系",
     "context": "柯俊（市长）与黄大庆（市政协主席）在人大政协活动中配合",
     "overlap_org": "廉江市", "overlap_period": "2026"},

    # 曾平治 vs 陈武略 — 书记与纪委书记
    {"id": 7, "person_a": 1, "person_b": 11, "type": "上下级",
     "context": "曾平治（市委书记）与陈武略（市纪委书记）在党风廉政建设中配合",
     "overlap_org": "中共廉江市委员会", "overlap_period": "2026"},

    # 陈武略 vs 柯俊 — 纪委与政府
    {"id": 8, "person_a": 11, "person_b": 2, "type": "党政关系",
     "context": "陈武略（市纪委书记）与柯俊（市长）在廉政建设中配合",
     "overlap_org": "廉江市", "overlap_period": "2026"},
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
lines.append('    <description>廉江市（湛江市代管县级市）领导班子工作关系网络 — 2026年7月生成</description>')
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
print("  1. 廉江市人民政府 — 领导信息栏目（2026-07-22确认）")
print("  2. 廉江市人民政府 — 新闻会议报道（曾平治、柯俊）")
print("\nOpen gaps:")
print("  1. All birth dates, education backgrounds, and career timelines for all persons")
print("  2. 曾平治's complete career timeline")
print("  3. 柯俊's complete career timeline")
print("  4. Predecessor/successor chain with exact dates")
print("  5. Standing committee members' specific portfolios (组织, 宣传, 政法, 统战等)")
print("  6. 陈恩才 — former Wikipedia-listed 市委书记, needs confirmation on status")
