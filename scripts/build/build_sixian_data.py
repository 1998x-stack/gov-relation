#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 泗县 leadership network."""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/sixian_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/sixian_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    {"id": 1, "name": "杨松涛", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-03", "birthplace": "未知", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泗县县委书记、一级调研员", "current_org": "中共泗县委员会",
     "source": "https://www.sixian.gov.cn/content/column/11465673?liId=16661"},
    {"id": 2, "name": "谢颖锋", "gender": "男", "ethnicity": "汉族",
     "birth": "1981-09", "birthplace": "未知", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泗县县委副书记、县长", "current_org": "泗县人民政府",
     "source": "https://www.sixian.gov.cn/content/column/11465673?liId=16631"},
    {"id": 3, "name": "邱磊", "gender": "男", "ethnicity": "汉族",
     "birth": "1978-06", "birthplace": "未知", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泗县县委副书记", "current_org": "中共泗县委员会",
     "source": "https://www.sixian.gov.cn/content/column/11465673?liId=16151"},
    {"id": 4, "name": "冉昊", "gender": "男", "ethnicity": "汉族",
     "birth": "1977-02", "birthplace": "未知", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泗县县委常委、常务副县长", "current_org": "泗县人民政府",
     "source": "https://www.sixian.gov.cn/content/column/11465673?liId=16161"},
    {"id": 5, "name": "桂连成", "gender": "男", "ethnicity": "汉族",
     "birth": "未知", "birthplace": "未知", "education": "未知",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泗县县委常委、县人武部部长", "current_org": "泗县人民武装部",
     "source": "https://www.sixian.gov.cn/ldzc/index.html"},
    {"id": 6, "name": "刘朋", "gender": "男", "ethnicity": "回族",
     "birth": "1983-09", "birthplace": "未知", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泗县县委常委、组织部部长", "current_org": "中共泗县委员会",
     "source": "https://www.sixian.gov.cn/content/column/11465673?liId=16011"},
    {"id": 7, "name": "周志", "gender": "男", "ethnicity": "汉族",
     "birth": "1988-10", "birthplace": "未知", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泗县县委常委、宣传部部长", "current_org": "中共泗县委员会",
     "source": "https://www.sixian.gov.cn/content/column/11465673?liId=16601"},
    {"id": 8, "name": "杜煜", "gender": "男", "ethnicity": "汉族",
     "birth": "1982-04", "birthplace": "未知", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泗县县委常委、纪委书记、监委主任", "current_org": "中共泗县纪律检查委员会",
     "source": "https://www.sixian.gov.cn/content/column/11465673?liId=16531"},
    {"id": 9, "name": "史肖生", "gender": "男", "ethnicity": "汉族",
     "birth": "1983-02", "birthplace": "未知", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泗县县委常委、社工部部长、政法委书记，县政府副县长", "current_org": "中共泗县委员会",
     "source": "https://www.sixian.gov.cn/content/column/11465673?liId=16721"},
    {"id": 10, "name": "江利景", "gender": "男", "ethnicity": "汉族",
     "birth": "1991-07", "birthplace": "未知", "education": "研究生、管理学博士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泗县县委常委、县政府副县长人选", "current_org": "泗县人民政府",
     "source": "https://www.sixian.gov.cn/content/column/11465673?liId=16381"},
    {"id": 11, "name": "刘琪", "gender": "女", "ethnicity": "汉族",
     "birth": "1985-10", "birthplace": "未知", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泗县县委常委、统战部部长、大庄镇党委书记", "current_org": "中共泗县委员会",
     "source": "https://www.sixian.gov.cn/content/column/11465673?liId=16731"},
    {"id": 12, "name": "刘培培", "gender": "女", "ethnicity": "汉族",
     "birth": "1984-03", "birthplace": "未知", "education": "研究生",
     "party_join": "致公党党员", "work_start": "",
     "current_post": "泗县副县长", "current_org": "泗县人民政府",
     "source": "https://www.sixian.gov.cn/content/column/11465673?liId=15741"},
    {"id": 13, "name": "余浩", "gender": "男", "ethnicity": "汉族",
     "birth": "1978-03", "birthplace": "未知", "education": "大专",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泗县副县长、县公安局党委书记、局长", "current_org": "泗县人民政府",
     "source": "https://www.sixian.gov.cn/content/column/11465673?liId=16131"},
    {"id": 14, "name": "骆松", "gender": "男", "ethnicity": "汉族",
     "birth": "1977-12", "birthplace": "未知", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泗县副县长", "current_org": "泗县人民政府",
     "source": "https://www.sixian.gov.cn/content/column/11465673?liId=16441"},
    {"id": 15, "name": "雷广州", "gender": "男", "ethnicity": "汉族",
     "birth": "1985-05", "birthplace": "未知", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泗县副县长（挂职）", "current_org": "泗县人民政府",
     "source": "https://www.sixian.gov.cn/content/column/11465673?liId=16331"},
    {"id": 16, "name": "祖巍", "gender": "男", "ethnicity": "汉族",
     "birth": "未知", "birthplace": "未知", "education": "未知",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泗县政协主席", "current_org": "政协泗县委员会",
     "source": "https://www.sixian.gov.cn/xwzx/zwyw/163908581.html"},
    {"id": 17, "name": "惠友华", "gender": "男", "ethnicity": "汉族",
     "birth": "未知", "birthplace": "未知", "education": "未知",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泗县人大常委会副主任", "current_org": "泗县人民代表大会常务委员会",
     "source": "https://www.sixian.gov.cn/public/25072/163926711.html"},
    {"id": 18, "name": "王毅", "gender": "男", "ethnicity": "汉族",
     "birth": "未知", "birthplace": "未知", "education": "未知",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泗县政协副主席、县水利局局长", "current_org": "政协泗县委员会",
     "source": "https://www.sixian.gov.cn/public/25072/163926711.html"},
    {"id": 19, "name": "杨振洲", "gender": "男", "ethnicity": "汉族",
     "birth": "未知", "birthplace": "未知", "education": "未知",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泗县县领导（具体职务待查）", "current_org": "泗县人民政府",
     "source": "https://www.sixian.gov.cn/xwzx/zwyw/163911321.html"},
]

organizations = [
    {"id": 1, "name": "中共泗县委员会", "type": "党委", "level": "县级",
     "parent": "中共宿州市委员会", "location": "安徽省宿州市泗县"},
    {"id": 2, "name": "泗县人民政府", "type": "政府", "level": "县级",
     "parent": "宿州市人民政府", "location": "安徽省宿州市泗县"},
    {"id": 3, "name": "中共泗县纪律检查委员会", "type": "党委", "level": "县级",
     "parent": "中共宿州市纪律检查委员会", "location": "安徽省宿州市泗县"},
    {"id": 4, "name": "政协泗县委员会", "type": "政协", "level": "县级",
     "parent": "政协宿州市委员会", "location": "安徽省宿州市泗县"},
    {"id": 5, "name": "泗县人民代表大会常务委员会", "type": "人大", "level": "县级",
     "parent": "宿州市人民代表大会常务委员会", "location": "安徽省宿州市泗县"},
    {"id": 6, "name": "泗县人民武装部", "type": "政府", "level": "县级",
     "parent": "宿州军分区", "location": "安徽省宿州市泗县"},
]

positions = [
    {"id": 1, "person_id": 1, "org_id": 1, "title": "泗县县委书记、一级调研员",
     "start": "", "end": "", "rank": "正处级", "note": "主持县委全面工作"},
    {"id": 2, "person_id": 2, "org_id": 2, "title": "泗县县委副书记、县长",
     "start": "", "end": "", "rank": "正处级", "note": "领导县政府全面工作"},
    {"id": 3, "person_id": 2, "org_id": 1, "title": "泗县县委副书记",
     "start": "", "end": "", "rank": "正处级", "note": "县委副书记兼任县长"},
    {"id": 4, "person_id": 3, "org_id": 1, "title": "泗县县委副书记",
     "start": "", "end": "", "rank": "副处级", "note": "协助杨松涛抓党的建设工作"},
    {"id": 5, "person_id": 4, "org_id": 1, "title": "泗县县委常委",
     "start": "", "end": "", "rank": "副处级", "note": ""},
    {"id": 6, "person_id": 4, "org_id": 2, "title": "泗县常务副县长",
     "start": "", "end": "", "rank": "副处级", "note": "负责财政、国资、金融、税务等"},
    {"id": 7, "person_id": 5, "org_id": 1, "title": "泗县县委常委",
     "start": "", "end": "", "rank": "副处级", "note": ""},
    {"id": 8, "person_id": 5, "org_id": 6, "title": "泗县人武部部长",
     "start": "", "end": "", "rank": "副处级", "note": ""},
    {"id": 9, "person_id": 6, "org_id": 1, "title": "泗县县委常委、组织部部长",
     "start": "", "end": "", "rank": "副处级", "note": ""},
    {"id": 10, "person_id": 7, "org_id": 1, "title": "泗县县委常委、宣传部部长",
     "start": "", "end": "", "rank": "副处级", "note": ""},
    {"id": 11, "person_id": 8, "org_id": 1, "title": "泗县县委常委、纪委书记",
     "start": "", "end": "", "rank": "副处级", "note": ""},
    {"id": 12, "person_id": 8, "org_id": 3, "title": "泗县监委主任",
     "start": "", "end": "", "rank": "副处级", "note": ""},
    {"id": 13, "person_id": 9, "org_id": 1, "title": "泗县县委常委、社工部部长、政法委书记",
     "start": "", "end": "", "rank": "副处级", "note": "负责政法、信访、社会稳定"},
    {"id": 14, "person_id": 9, "org_id": 2, "title": "泗县副县长",
     "start": "", "end": "", "rank": "副处级", "note": "自然资源、住建、城管等"},
    {"id": 15, "person_id": 10, "org_id": 1, "title": "泗县县委常委",
     "start": "", "end": "", "rank": "副处级", "note": ""},
    {"id": 16, "person_id": 10, "org_id": 2, "title": "泗县副县长人选",
     "start": "", "end": "", "rank": "副处级", "note": "发改、工信、招商、开发区等"},
    {"id": 17, "person_id": 11, "org_id": 1, "title": "泗县县委常委、统战部部长",
     "start": "", "end": "", "rank": "副处级", "note": "主持大庄镇党委全面工作"},
    {"id": 18, "person_id": 12, "org_id": 2, "title": "泗县副县长",
     "start": "", "end": "", "rank": "副处级", "note": "人社、市场监管、教育、文旅等"},
    {"id": 19, "person_id": 13, "org_id": 2, "title": "泗县副县长",
     "start": "", "end": "", "rank": "副处级", "note": "公安、司法、退役军人事务等"},
    {"id": 20, "person_id": 14, "org_id": 2, "title": "泗县副县长",
     "start": "", "end": "", "rank": "副处级", "note": "交通、民政、数据资源等"},
    {"id": 21, "person_id": 15, "org_id": 2, "title": "泗县副县长（挂职）",
     "start": "", "end": "", "rank": "副处级", "note": "协助工信、科技、商务等"},
    {"id": 22, "person_id": 16, "org_id": 4, "title": "泗县政协主席",
     "start": "", "end": "", "rank": "正处级", "note": ""},
    {"id": 23, "person_id": 17, "org_id": 5, "title": "泗县人大常委会副主任",
     "start": "", "end": "", "rank": "副处级", "note": ""},
    {"id": 24, "person_id": 18, "org_id": 4, "title": "泗县政协副主席、县水利局局长",
     "start": "", "end": "", "rank": "副处级", "note": ""},
    {"id": 25, "person_id": 19, "org_id": 2, "title": "泗县县领导（待查）",
     "start": "", "end": "", "rank": "未知", "note": "具体职务待补充"},
]

relationships = [
    {"id": 1, "person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "杨松涛（县委书记）与谢颖锋（县长）搭班子，泗县核心党政领导",
     "overlap_org": "中共泗县委员会/泗县人民政府",
     "overlap_period": "现任"},
    {"id": 2, "person_a": 1, "person_b": 3, "type": "上下级",
     "context": "杨松涛（县委书记）与邱磊（专职副书记），邱磊协助杨松涛抓党建工作",
     "overlap_org": "中共泗县委员会",
     "overlap_period": "现任"},
    {"id": 3, "person_a": 2, "person_b": 4, "type": "上下级",
     "context": "谢颖锋（县长）与冉昊（常务副县长），冉昊协助县长分管审计局",
     "overlap_org": "泗县人民政府",
     "overlap_period": "现任"},
    {"id": 4, "person_a": 1, "person_b": 9, "type": "工作交集",
     "context": "杨松涛调研房屋建筑安全等工作，史肖生陪同参加",
     "overlap_org": "泗县",
     "overlap_period": "2026-07"},
    {"id": 5, "person_a": 2, "person_b": 4, "type": "政府班子",
     "context": "谢颖锋、冉昊同属泗县政府领导班子",
     "overlap_org": "泗县人民政府",
     "overlap_period": "现任"},
    {"id": 6, "person_a": 3, "person_b": 6, "type": "县委班子",
     "context": "邱磊与刘朋同属泗县县委领导班子",
     "overlap_org": "中共泗县委员会",
     "overlap_period": "现任"},
    {"id": 7, "person_a": 6, "person_b": 7, "type": "县委班子",
     "context": "刘朋（组织部长）与周志（宣传部长）同属县委班子成员",
     "overlap_org": "中共泗县委员会",
     "overlap_period": "现任"},
    {"id": 8, "person_a": 8, "person_b": 1, "type": "监督关系",
     "context": "杜煜（纪委书记）监督杨松涛（书记）",
     "overlap_org": "中共泗县委员会",
     "overlap_period": "现任"},
    {"id": 9, "person_a": 2, "person_b": 9, "type": "政府班子",
     "context": "谢颖锋与史肖生同属县政府领导班子",
     "overlap_org": "泗县人民政府",
     "overlap_period": "现任"},
]

# ── BUILD SQLite ────────────────────────────────────────────────────

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.executescript("""
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS persons (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    gender TEXT,
    ethnicity TEXT,
    birth TEXT,
    birthplace TEXT,
    education TEXT,
    party_join TEXT,
    work_start TEXT,
    current_post TEXT,
    current_org TEXT,
    source TEXT
);

CREATE TABLE IF NOT EXISTS organizations (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT,
    level TEXT,
    parent TEXT,
    location TEXT
);

CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY,
    person_id INTEGER NOT NULL,
    org_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    start TEXT,
    end TEXT,
    rank TEXT,
    note TEXT,
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
);

CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY,
    person_a INTEGER NOT NULL,
    person_b INTEGER NOT NULL,
    type TEXT,
    context TEXT,
    overlap_org TEXT,
    overlap_period TEXT,
    FOREIGN KEY (person_a) REFERENCES persons(id),
    FOREIGN KEY (person_b) REFERENCES persons(id)
);
""")

for p in persons:
    c.execute("INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
              (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
               p["birthplace"], p["education"], p["party_join"], p["work_start"],
               p["current_post"], p["current_org"], p["source"]))

for o in organizations:
    c.execute("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)",
              (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for pos in positions:
    c.execute("INSERT OR REPLACE INTO positions VALUES (?,?,?,?,?,?,?,?)",
              (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
               pos["start"], pos["end"], pos["rank"], pos["note"]))

for r in relationships:
    c.execute("INSERT OR REPLACE INTO relationships VALUES (?,?,?,?,?,?,?)",
              (r["id"], r["person_a"], r["person_b"], r["type"],
               r["context"], r["overlap_org"], r["overlap_period"]))

conn.commit()
conn.close()

print(f"✅ SQLite DB: {DB_PATH}")
print(f"   Persons: {len(persons)}")
print(f"   Organizations: {len(organizations)}")
print(f"   Positions: {len(positions)}")
print(f"   Relationships: {len(relationships)}")

# ── BUILD GEXF ──────────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Color by role."""
    post = p.get("current_post", "")
    if "县委书记" in post:
        return "255,50,50"
    elif "县长" in post and "副书记" in post:
        return "50,100,255"
    elif "副书记" in post:
        return "100,100,200"
    elif "纪委书记" in post or "监委" in post:
        return "255,165,0"
    elif "部长" in post or "统战" in post:
        return "100,180,100"
    elif "副县长" in post or "常务" in post:
        return "100,150,255"
    elif "政协" in post:
        return "255,200,100"
    elif "人大" in post:
        return "100,200,200"
    elif "人武部" in post:
        return "150,150,150"
    else:
        return "100,100,100"

def person_size(p):
    post = p.get("current_post", "")
    if "县委书记" in post:
        return "20.0"
    elif "县长" in post:
        return "20.0"
    elif "政协主席" in post:
        return "16.0"
    else:
        return "12.0"

def org_color(o):
    t = o.get("type", "")
    colors = {"党委": "255,200,200", "政府": "200,200,255", "人大": "200,255,255",
              "政协": "255,240,200", "开发区": "200,255,200", "乡镇": "255,255,200",
              "事业单位": "220,220,220", "群团": "255,220,255"}
    return colors.get(t, "200,200,200")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>OpenCode Research Agent</creator>')
lines.append('    <description>泗县领导班子工作关系网络 — 含19人、6机构、25任职、9关系</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Node attributes
lines.append('    <attributes class="node">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="role" type="string"/>')
lines.append('      <attribute id="2" title="birth" type="string"/>')
lines.append('      <attribute id="3" title="education" type="string"/>')
lines.append('    </attributes>')

# Edge attributes
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="context" type="string"/>')
lines.append('    </attributes>')

# Nodes
lines.append('    <nodes>')
for p in persons:
    c = person_color(p)
    sz = person_size(p)
    lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="person"/>')
    post = esc(p.get("current_post", ""))
    lines.append(f'          <attvalue for="1" value="{post}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(p.get("birth", ""))}"/>')
    lines.append(f'          <attvalue for="3" value="{esc(p.get("education", ""))}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')

for o in organizations:
    c = org_color(o)
    lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="organization"/>')
    lines.append(f'          <attvalue for="1" value="{esc(o.get("type", ""))}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append('        <viz:size value="8.0"/>')
    lines.append('      </node>')
lines.append('    </nodes>')

# Edges
lines.append('    <edges>')
eid = 0
# person→org edges
for pos in positions:
    eid += 1
    lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="worked_at"/>')
    lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

# person↔person edges
for r in relationships:
    eid += 1
    lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="relationship"/>')
    lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"✅ GEXF graph: {GEXF_PATH}")
print(f"   Person nodes: {len(persons)}")
print(f"   Org nodes: {len(organizations)}")
print(f"   Edges: {eid}")
print("\nAll done!")
