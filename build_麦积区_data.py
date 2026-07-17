#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 麦积区 (Maiji District, Tianshui, Gansu) leadership network.

麦积区 — 甘肃省天水市市辖区, 市委市政府驻地之一 (部分).
Covers current Party Secretary (赵虎生), District Mayor (石生勃),
their predecessors, Standing Committee members, and deputy mayors.
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/gansu_麦积区")
os.makedirs(STAGING, exist_ok=True)

DB_PATH = os.path.join(STAGING, "麦积区_network.db")
GEXF_PATH = os.path.join(STAGING, "麦积区_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── A. Current top leadership ──

    # 赵虎生 — 麦积区委书记 (as of 2026.07)
    {"id": 1, "name": "赵虎生", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-12", "birthplace": "",
     "education": "研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "麦积区委书记、麦积山大景区党工委书记",
     "current_org": "中共天水市麦积区委员会",
     "source": "https://www.maiji.gov.cn/info/1091/488422.htm"},

    # 石生勃 — 麦积区委副书记、区长 (as of 2025.03)
    {"id": 2, "name": "石生勃", "gender": "男", "ethnicity": "汉族",
     "birth": "1984-01", "birthplace": "",
     "education": "本科学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "麦积区委副书记、区长",
     "current_org": "麦积区人民政府",
     "source": "https://www.maiji.gov.cn/info/1141/506172.htm"},

    # 王军龙 — 区委常委、常务副区长 (as of 2026.02)
    {"id": 3, "name": "王军龙", "gender": "男", "ethnicity": "汉族",
     "birth": "1984-12", "birthplace": "",
     "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "麦积区委常委、常务副区长",
     "current_org": "麦积区人民政府",
     "source": "https://www.maiji.gov.cn/info/1111/350562.htm"},

    # 刘洋 — 区委常委、副区长（挂职）
    {"id": 4, "name": "刘洋", "gender": "男", "ethnicity": "汉族",
     "birth": "1984-02", "birthplace": "",
     "education": "研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "麦积区委常委、副区长（挂职）",
     "current_org": "麦积区人民政府",
     "source": "https://www.maiji.gov.cn/info/1111/545542.htm"},

    # 汪萍 — 区委常委
    {"id": 5, "name": "汪萍", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "麦积区委常委",
     "current_org": "中共天水市麦积区委员会",
     "source": "https://www.maiji.gov.cn/ldzc.htm"},

    # 张天龙 — 区委常委
    {"id": 6, "name": "张天龙", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "麦积区委常委",
     "current_org": "中共天水市麦积区委员会",
     "source": "https://www.maiji.gov.cn/ldzc.htm"},

    # 强永斌 — 区委常委
    {"id": 7, "name": "强永斌", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "麦积区委常委、副区长",
     "current_org": "麦积区人民政府",
     "source": "https://www.maiji.gov.cn/ldzc.htm"},

    # 龚开明 — 区委常委
    {"id": 8, "name": "龚开明", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "麦积区委常委",
     "current_org": "中共天水市麦积区委员会",
     "source": "https://www.maiji.gov.cn/ldzc.htm"},

    # 田强 — 区委常委
    {"id": 9, "name": "田强", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "麦积区委常委",
     "current_org": "中共天水市麦积区委员会",
     "source": "https://www.maiji.gov.cn/ldzc.htm"},

    # 刘灿 — 区委常委、副区长
    {"id": 10, "name": "刘灿", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "麦积区委常委、副区长",
     "current_org": "麦积区人民政府",
     "source": "https://www.maiji.gov.cn/ldzc.htm"},

    # 董文海 — 区委常委
    {"id": 11, "name": "董文海", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "麦积区委常委",
     "current_org": "中共天水市麦积区委员会",
     "source": "https://www.maiji.gov.cn/ldzc.htm"},

    # 宋昌华 — 区委常委
    {"id": 12, "name": "宋昌华", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "麦积区委常委",
     "current_org": "中共天水市麦积区委员会",
     "source": "https://www.maiji.gov.cn/ldzc.htm"},

    # ── B. Deputy mayors (副区长, not in standing committee) ──

    # 马玮 — 副区长
    {"id": 13, "name": "马玮", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "麦积区副区长",
     "current_org": "麦积区人民政府",
     "source": "https://www.maiji.gov.cn/ldzc.htm"},

    # 赵锦鹏 — 副区长
    {"id": 14, "name": "赵锦鹏", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "麦积区副区长",
     "current_org": "麦积区人民政府",
     "source": "https://www.maiji.gov.cn/ldzc.htm"},

    # 李翔 — 副区长
    {"id": 15, "name": "李翔", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "麦积区副区长",
     "current_org": "麦积区人民政府",
     "source": "https://www.maiji.gov.cn/ldzc.htm"},

    # 马晶 — 副区长
    {"id": 16, "name": "马晶", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "麦积区副区长",
     "current_org": "麦积区人民政府",
     "source": "https://www.maiji.gov.cn/ldzc.htm"},

    # ── C. 人大领导 ──

    # 赵继文 — 区人大常委会主任
    {"id": 17, "name": "赵继文", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "麦积区人大常委会主任",
     "current_org": "麦积区人大常委会",
     "source": "https://www.maiji.gov.cn/ldzc.htm"},

    # ── D. 政协领导 ──

    # 高志强 — 区政协主席
    {"id": 18, "name": "高志强", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "麦积区政协主席",
     "current_org": "麦积区政协",
     "source": "https://www.maiji.gov.cn/ldzc.htm"},

    # ── E. Predecessors ──

    # 康泰来 — 前任麦积区委书记 (2021-09 ~ 2023-06), 后任天水市副市长、秦州区委书记
    {"id": 19, "name": "康泰来", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-03", "birthplace": "甘肃武山",
     "education": "大学学历，教育硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "天水市委常委、秦州区委书记",
     "current_org": "中共天水市秦州区委员会",
     "source": "data/persons/20260717-甘肃省-天水市-区委书记-康泰来.json"},

    # 成少平 — 前任麦积区长（推测，待确认）
    {"id": 20, "name": "成少平", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原麦积区长",
     "current_org": "",
     "source": "https://www.maiji.gov.cn/zfxxgk/fdzdgknr1/rsxx.htm"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共天水市麦积区委员会", "type": "党委", "level": "县级", "parent": "中共天水市委员会", "location": "甘肃省天水市麦积区"},
    {"id": 2, "name": "麦积区人民政府", "type": "政府", "level": "县级", "parent": "天水市人民政府", "location": "甘肃省天水市麦积区"},
    {"id": 3, "name": "麦积区人大常委会", "type": "人大", "level": "县级", "parent": "天水市人大常委会", "location": "甘肃省天水市麦积区"},
    {"id": 4, "name": "麦积区政协", "type": "政协", "level": "县级", "parent": "天水市政协", "location": "甘肃省天水市麦积区"},
    {"id": 5, "name": "麦积山大景区管理委员会", "type": "事业单位", "level": "县级", "parent": "", "location": "甘肃省天水市麦积区"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # Current top leaders
    {"person_id": 1, "org_id": 1, "title": "麦积区委书记", "start": "", "end": "present", "rank": "正县级", "note": "兼任麦积山大景区党工委书记"},
    {"person_id": 1, "org_id": 5, "title": "麦积山大景区党工委书记", "start": "", "end": "present", "rank": "正县级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "麦积区长", "start": "", "end": "present", "rank": "正县级", "note": "同时担任区委副书记"},
    {"person_id": 2, "org_id": 1, "title": "麦积区委副书记", "start": "", "end": "present", "rank": "正县级", "note": ""},

    # Standing Committee members
    {"person_id": 3, "org_id": 1, "title": "麦积区委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "麦积区常务副区长", "start": "", "end": "present", "rank": "副县级", "note": "区政府党组副书记"},
    {"person_id": 4, "org_id": 1, "title": "麦积区委常委", "start": "", "end": "present", "rank": "副县级", "note": "挂职"},
    {"person_id": 4, "org_id": 2, "title": "麦积区副区长（挂职）", "start": "", "end": "present", "rank": "副县级", "note": "挂职"},
    {"person_id": 5, "org_id": 1, "title": "麦积区委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "麦积区委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "麦积区委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "麦积区副区长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "麦积区委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "麦积区委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "麦积区委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "麦积区副区长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 11, "org_id": 1, "title": "麦积区委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 12, "org_id": 1, "title": "麦积区委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},

    # Deputy mayors not in standing committee
    {"person_id": 13, "org_id": 2, "title": "麦积区副区长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "麦积区副区长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "麦积区副区长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "麦积区副区长", "start": "", "end": "present", "rank": "副县级", "note": ""},

    # 人大
    {"person_id": 17, "org_id": 3, "title": "麦积区人大常委会主任", "start": "", "end": "present", "rank": "正县级", "note": ""},

    # 政协
    {"person_id": 18, "org_id": 4, "title": "麦积区政协主席", "start": "", "end": "present", "rank": "正县级", "note": ""},

    # Predecessors
    {"person_id": 19, "org_id": 1, "title": "麦积区委书记", "start": "2021-09", "end": "2023-06", "rank": "正县级", "note": "后任天水市副市长、秦州区委书记"},
    {"person_id": 19, "org_id": 2, "title": "天水市副市长", "start": "2023-06", "end": "2026-07", "rank": "副厅级", "note": "兼任麦积区委书记至202306"},
    {"person_id": 19, "org_id": 1, "title": "秦州区委书记", "start": "2026-07", "end": "present", "rank": "副厅级", "note": "担任天水市委常委、秦州区委书记"},
    {"person_id": 20, "org_id": 2, "title": "麦积区长", "start": "", "end": "", "rank": "正县级", "note": "前任区长，具体任期待确认"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 书记 ↔ 区长 工作搭档
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "区委班子搭档:书记+区长", "overlap_org": "中共天水市麦积区委员会", "overlap_period": "至今"},

    # 书记 ↔ 前任书记 继任关系
    {"person_a": 1, "person_b": 19, "type": "predecessor_successor", "context": "麦积区委书记继任", "overlap_org": "中共天水市麦积区委员会", "overlap_period": "约2023"},

    # 书记 ↔ 常委会成员 共事关系
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "区委常委班子", "overlap_org": "中共天水市麦积区委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "区委常委班子", "overlap_org": "中共天水市麦积区委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "区委常委班子", "overlap_org": "中共天水市麦积区委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "区委常委班子", "overlap_org": "中共天水市麦积区委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "区委常委班子", "overlap_org": "中共天水市麦积区委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "区委常委班子", "overlap_org": "中共天水市麦积区委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 9, "type": "overlap", "context": "区委常委班子", "overlap_org": "中共天水市麦积区委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 10, "type": "overlap", "context": "区委常委班子", "overlap_org": "中共天水市麦积区委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 11, "type": "overlap", "context": "区委常委班子", "overlap_org": "中共天水市麦积区委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 12, "type": "overlap", "context": "区委常委班子", "overlap_org": "中共天水市麦积区委员会", "overlap_period": "至今"},

    # 区长 ↔ 政府班子成员
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "区政府班子", "overlap_org": "麦积区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "区政府班子", "overlap_org": "麦积区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 7, "type": "overlap", "context": "区政府班子", "overlap_org": "麦积区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 10, "type": "overlap", "context": "区政府班子", "overlap_org": "麦积区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 13, "type": "overlap", "context": "区政府班子", "overlap_org": "麦积区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 14, "type": "overlap", "context": "区政府班子", "overlap_org": "麦积区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 15, "type": "overlap", "context": "区政府班子", "overlap_org": "麦积区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 16, "type": "overlap", "context": "区政府班子", "overlap_org": "麦积区人民政府", "overlap_period": "至今"},
]

# =========================================================================
# BUILD SQLITE DATABASE
# =========================================================================

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS persons")
cur.execute("DROP TABLE IF EXISTS organizations")
cur.execute("DROP TABLE IF EXISTS positions")
cur.execute("DROP TABLE IF EXISTS relationships")

cur.execute("""CREATE TABLE persons (
    id INTEGER PRIMARY KEY,
    name TEXT,
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
)""")

cur.execute("""CREATE TABLE organizations (
    id INTEGER PRIMARY KEY,
    name TEXT,
    type TEXT,
    level TEXT,
    parent TEXT,
    location TEXT
)""")

cur.execute("""CREATE TABLE positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER,
    org_id INTEGER,
    title TEXT,
    start TEXT,
    "end" TEXT,
    rank TEXT,
    note TEXT
)""")

cur.execute("""CREATE TABLE relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_a INTEGER,
    person_b INTEGER,
    type TEXT,
    context TEXT,
    overlap_org TEXT,
    overlap_period TEXT
)""")

for p in persons:
    cur.execute("INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                 p["birthplace"], p["education"], p["party_join"],
                 p["work_start"], p["current_post"], p["current_org"],
                 p["source"]))

for o in organizations:
    cur.execute("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)",
                (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for po in positions:
    cur.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)",
                (po["person_id"], po["org_id"], po["title"], po["start"], po["end"], po["rank"], po["note"]))

for r in relationships:
    cur.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
                (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

conn.commit()

# Print summary
cur.execute("SELECT COUNT(*) FROM persons")
person_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM organizations")
org_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM positions")
pos_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM relationships")
rel_count = cur.fetchone()[0]

print(f"✅ 数据库已创建: {DB_PATH}")
print(f"   人物: {person_count} | 机构: {org_count} | 任职: {pos_count} | 关系: {rel_count}")

# =========================================================================
# BUILD GEXF
# =========================================================================

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(title):
    t = title or ""
    if "书记" in t and "纪委" not in t and ("副" not in t[:t.index("书记")+2] if "书记" in t else True):
        return (255, 50, 50)
    if "区长" in t and "副" not in t[:t.index("区长")+2] if "区长" in t else False:
        return (50, 100, 255)
    if "人大" in t:
        return (150, 180, 200)
    if "政协" in t:
        return (180, 150, 200)
    if "纪委" in t:
        return (255, 165, 0)
    if "副区长" in t or "副书记" in t:
        return (80, 130, 230)
    return (100, 100, 100)

def org_color(org_type):
    t = org_type or ""
    if "党委" in t:
        return (255, 200, 200)
    if "政府" in t:
        return (200, 200, 255)
    if "人大" in t:
        return (200, 255, 255)
    if "政协" in t:
        return (255, 240, 200)
    if "事业单位" in t:
        return (220, 220, 220)
    return (200, 200, 200)

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>China Gov Network Investigator</creator>')
lines.append('    <description>麦积区领导班子工作关系网络 - 甘肃省天水市麦积区</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Attributes
lines.append('    <attributes class="node">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="role" type="string"/>')
lines.append('      <attribute id="2" title="org" type="string"/>')
lines.append('      <attribute id="3" title="birth" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="label" type="string"/>')
lines.append('    </attributes>')

# Nodes: persons
lines.append('    <nodes>')
for p in persons:
    slug_id = f"maiji_p{p['id']}"
    c = person_color(p["current_post"])
    is_top = "书记" in (p["current_post"] or "") and "纪委" not in (p["current_post"] or "") and "副" not in (p["current_post"] or "")
    is_mayor = "区长" in (p["current_post"] or "") and "副" not in (p["current_post"] or "")
    sz = "20.0" if is_top else "15.0" if is_mayor else "12.0"
    label = f"{p['name']} ({p['current_post'] or '?'})"
    lines.append(f'      <node id="{slug_id}" label="{esc(label)}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="person"/>')
    lines.append(f'          <attvalue for="1" value="{esc(p["current_post"] or "")}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(p["current_org"] or "")}"/>')
    lines.append(f'          <attvalue for="3" value="{esc(p["birth"] or "")}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')

# Nodes: organizations
for o in organizations:
    oid = f"maiji_o{o['id']}"
    c = org_color(o["type"])
    lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="organization"/>')
    lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
    lines.append('        <viz:size value="8.0"/>')
    lines.append('      </node>')
lines.append('    </nodes>')

# Edges
lines.append('    <edges>')
edge_id = 0

# Person→Organization (worked_at)
for po in positions:
    p = next(x for x in persons if x["id"] == po["person_id"])
    o = next(x for x in organizations if x["id"] == po["org_id"])
    edge_id += 1
    lines.append(f'      <edge id="e{edge_id}" source="maiji_p{p["id"]}" target="maiji_o{o["id"]}" label="{esc(po["title"])}" weight="1.0">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="worked_at"/>')
    lines.append(f'          <attvalue for="1" value="{esc(po["title"])}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

# Person↔Person (relationships)
for r in relationships:
    p_a = next(x for x in persons if x["id"] == r["person_a"])
    p_b = next(x for x in persons if x["id"] == r["person_b"])
    edge_id += 1
    lines.append(f'      <edge id="e{edge_id}" source="maiji_p{p_a["id"]}" target="maiji_p{p_b["id"]}" label="{esc(r["context"])}" weight="2.0">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="relationship"/>')
    lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"✅ GEXF 已创建: {GEXF_PATH}")
print(f"   节点: {len(persons) + len(organizations)} | 边: {edge_id}")

conn.close()
print("✅ 完成!")
