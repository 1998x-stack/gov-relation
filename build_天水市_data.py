#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 天水市 (Tianshui City, Gansu) leadership network.

天水市 — 甘肃省地级市, 省域副中心城市.
Covers current Party Secretary (杨金泉), Mayor (刘力江), their predecessors,
key Standing Committee members, and 4+1 county-level admin areas.
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/gansu_天水市")
os.makedirs(STAGING, exist_ok=True)

DB_PATH = os.path.join(STAGING, "天水市_network.db")
GEXF_PATH = os.path.join(STAGING, "天水市_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── A. Current city-level top leadership ──

    # 杨金泉 — 天水市委书记 (as of 2026.01)
    {"id": 1, "name": "杨金泉", "gender": "男", "ethnicity": "汉族",
     "birth": "1969-03", "birthplace": "甘肃玉门",
     "education": "省委党校研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "天水市委书记",
     "current_org": "中共天水市委员会",
     "source": "https://www.tianshui.gov.cn/info/4001/1230882.htm"},

    # 刘力江 — 天水市长 (as of 2024.08)
    {"id": 2, "name": "刘力江", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-05", "birthplace": "甘肃白银",
     "education": "省委党校研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "天水市委副书记、市长",
     "current_org": "天水市人民政府",
     "source": "https://www.tianshui.gov.cn/info/3991/1058562.htm"},

    # 张晓强 — 天水市委副书记（专职, 非兰州同名人）
    {"id": 3, "name": "张晓强", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "天水市委副书记",
     "current_org": "中共天水市委员会",
     "source": "https://www.tianshui.gov.cn/info/1141/1248782.htm"},

    # 贾义翔 — 天水市人大常委会主任 (as of ~2024)
    {"id": 4, "name": "贾义翔", "gender": "男", "ethnicity": "汉族",
     "birth": "1969-07", "birthplace": "",
     "education": "研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "天水市人大常委会党组书记、主任",
     "current_org": "天水市人大常委会",
     "source": "https://www.tianshui.gov.cn/info/5751/1012752.htm"},

    # 王燕 — 天水市政协主席 (as of 2021.12)
    {"id": 5, "name": "王燕", "gender": "女", "ethnicity": "汉族",
     "birth": "1968-09", "birthplace": "甘肃清水",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "天水市政协主席",
     "current_org": "天水市政协",
     "source": "https://www.tianshui.gov.cn/info/5761/604831.htm"},

    # ── B. Standing Committee members (市委常委) ──

    # 王文东 — 市委常委、宣传部部长
    {"id": 6, "name": "王文东", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "天水市委常委、宣传部部长",
     "current_org": "中共天水市委员会",
     "source": "https://www.tianshui.gov.cn/info/1151/2811.htm"},

    # 邵建斌 — 市委常委、政法委书记
    {"id": 7, "name": "邵建斌", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "天水市委常委、政法委书记",
     "current_org": "中共天水市委员会",
     "source": "https://www.tianshui.gov.cn/info/1151/2781.htm"},

    # 刘立桢 — 市委常委、秘书长
    {"id": 8, "name": "刘立桢", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "天水市委常委、秘书长",
     "current_org": "中共天水市委员会",
     "source": "https://www.tianshui.gov.cn/info/1151/1253752.htm"},

    # 孙亮 — 市委常委、副市长
    {"id": 9, "name": "孙亮", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "天水市委常委、副市长",
     "current_org": "天水市人民政府",
     "source": "https://www.tianshui.gov.cn/info/1151/1257842.htm"},

    # 储著贞 — 市委常委、常务副市长
    {"id": 10, "name": "储著贞", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "天水市委常委、常务副市长",
     "current_org": "天水市人民政府",
     "source": "https://www.tianshui.gov.cn/info/1151/1260732.htm"},

    # 康泰来 — 市委常委
    {"id": 11, "name": "康泰来", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "天水市委常委",
     "current_org": "中共天水市委员会",
     "source": "https://www.tianshui.gov.cn/info/1151/1069522.htm"},

    # 李炯芳 — 市委常委、纪委书记、监委主任
    {"id": 12, "name": "李炯芳", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "天水市委常委、纪委书记、监委主任",
     "current_org": "中共天水市纪律检查委员会",
     "source": "https://www.tianshui.gov.cn/info/1151/1069582.htm"},

    # 薛丞忠 — 市委常委
    {"id": 13, "name": "薛丞忠", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "天水市委常委",
     "current_org": "中共天水市委员会",
     "source": "https://www.tianshui.gov.cn/info/1151/1253792.htm"},

    # ── C. Deputy mayors (副市长) ──

    # 董小平 — 副市长
    {"id": 14, "name": "董小平", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "天水市副市长",
     "current_org": "天水市人民政府",
     "source": "https://www.tianshui.gov.cn/info/1181/2991.htm"},

    # 孟晓龙 — 副市长
    {"id": 15, "name": "孟晓龙", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "天水市副市长",
     "current_org": "天水市人民政府",
     "source": "https://www.tianshui.gov.cn/info/1181/1087312.htm"},

    # 马军胜 — 市政府秘书长
    {"id": 16, "name": "马军胜", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "天水市政府秘书长",
     "current_org": "天水市人民政府",
     "source": "https://www.tianshui.gov.cn/info/1191/1015552.htm"},

    # ── D. Predecessors ──

    # 冯文戈 — 前任天水市委书记 (2022.06-2026.01)
    {"id": 17, "name": "冯文戈", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原天水市委书记",
     "current_org": "",
     "source": "https://zh.wikipedia.org/wiki/天水市"},

    # 张永霞 — 前任天水市委书记 (2021.07-2022.06)
    {"id": 18, "name": "张永霞", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "甘肃省委常委、宣传部部长（原天水市委书记）",
     "current_org": "中共甘肃省委员会",
     "source": "https://zh.wikipedia.org/wiki/天水市"},

    # 王锐 — 前任天水市委书记 (2013.09-2021.07)
    {"id": 19, "name": "王锐", "gender": "男", "ethnicity": "汉族",
     "birth": "1963-10", "birthplace": "内蒙古",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "甘肃省政协副主席（原天水市委书记）",
     "current_org": "甘肃省政协",
     "source": "https://zh.wikipedia.org/wiki/天水市"},

    # 王国先 — 前任天水市长 (2021.01-2024.08)
    {"id": 20, "name": "王国先", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原天水市长",
     "current_org": "",
     "source": "https://zh.wikipedia.org/wiki/天水市"},

    # 杨维俊 — 前任天水市长 (2013.10-2017.04)
    {"id": 21, "name": "杨维俊", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原天水市长",
     "current_org": "",
     "source": "https://zh.wikipedia.org/wiki/天水市"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共天水市委员会", "type": "党委", "level": "地级", "parent": "中共甘肃省委员会", "location": "甘肃省天水市"},
    {"id": 2, "name": "天水市人民政府", "type": "政府", "level": "地级", "parent": "", "location": "甘肃省天水市"},
    {"id": 3, "name": "天水市人大常委会", "type": "人大", "level": "地级", "parent": "", "location": "甘肃省天水市"},
    {"id": 4, "name": "天水市政协", "type": "政协", "level": "地级", "parent": "", "location": "甘肃省天水市"},
    {"id": 5, "name": "中共天水市纪律检查委员会", "type": "党委", "level": "地级", "parent": "中共天水市委员会", "location": "甘肃省天水市"},
    {"id": 6, "name": "天水市监察委员会", "type": "党委", "level": "地级", "parent": "", "location": "甘肃省天水市"},
    {"id": 7, "name": "中共甘肃省委组织部", "type": "党委", "level": "省级", "parent": "中共甘肃省委员会", "location": "甘肃省兰州市"},
    {"id": 8, "name": "甘肃省人民政府", "type": "政府", "level": "省级", "parent": "", "location": "甘肃省兰州市"},
    {"id": 9, "name": "甘肃省政协", "type": "政协", "level": "省级", "parent": "", "location": "甘肃省兰州市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # Current top leaders
    {"person_id": 1, "org_id": 1, "title": "天水市委书记", "start": "2026-01", "end": "present", "rank": "正厅级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "天水市长", "start": "2024-08", "end": "present", "rank": "正厅级", "note": "同时担任市委副书记"},
    {"person_id": 2, "org_id": 1, "title": "天水市委副书记", "start": "2024-08", "end": "present", "rank": "正厅级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "天水市委副书记", "start": "", "end": "present", "rank": "副厅级", "note": "专职副书记"},
    {"person_id": 4, "org_id": 3, "title": "天水市人大常委会主任", "start": "", "end": "present", "rank": "正厅级", "note": ""},
    {"person_id": 5, "org_id": 4, "title": "天水市政协主席", "start": "2021-12", "end": "present", "rank": "正厅级", "note": ""},

    # Standing Committee positions
    {"person_id": 6, "org_id": 1, "title": "天水市委常委、宣传部部长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "天水市委常委、政法委书记", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "天水市委常委、秘书长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "天水市委常委、副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "天水市委常委、常务副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 11, "org_id": 1, "title": "天水市委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 12, "org_id": 5, "title": "天水市委常委、纪委书记、监委主任", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 13, "org_id": 1, "title": "天水市委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},

    # Deputy mayors
    {"person_id": 14, "org_id": 2, "title": "天水市副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "天水市副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "天水市政府秘书长", "start": "", "end": "present", "rank": "正处级", "note": ""},

    # Predecessors
    {"person_id": 17, "org_id": 1, "title": "天水市委书记", "start": "2022-06", "end": "2026-01", "rank": "正厅级", "note": ""},
    {"person_id": 18, "org_id": 1, "title": "天水市委书记", "start": "2021-07", "end": "2022-06", "rank": "正厅级", "note": ""},
    {"person_id": 19, "org_id": 1, "title": "天水市委书记", "start": "2013-09", "end": "2021-07", "rank": "正厅级", "note": ""},
    {"person_id": 20, "org_id": 2, "title": "天水市长", "start": "2021-01", "end": "2024-08", "rank": "正厅级", "note": ""},
    {"person_id": 21, "org_id": 2, "title": "天水市长", "start": "2013-10", "end": "2017-04", "rank": "正厅级", "note": ""},

    # Provincial roles
    {"person_id": 18, "org_id": 7, "title": "甘肃省委宣传部部长", "start": "2022", "end": "present", "rank": "副省级", "note": "现任"},
    {"person_id": 19, "org_id": 9, "title": "甘肃省政协副主席", "start": "", "end": "present", "rank": "副省级", "note": ""},

    # 杨金泉 previous roles
    {"person_id": 1, "org_id": 7, "title": "甘肃省委组织部副部长", "start": "", "end": "2026-01", "rank": "副厅级", "note": "据公开报道"},
    # TODO: 杨金泉此前已知担任甘肃省委组织部副部长，更早履历待填补
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 书记↔市长 工作搭档
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "市委班子搭档", "overlap_org": "中共天水市委员会", "overlap_period": "2026-至今"},
    # 书记↔前任书记 继任关系
    {"person_a": 1, "person_b": 17, "type": "predecessor_successor", "context": "市委书记继任", "overlap_org": "中共天水市委员会", "overlap_period": "2026"},
    {"person_a": 17, "person_b": 18, "type": "predecessor_successor", "context": "市委书记继任", "overlap_org": "中共天水市委员会", "overlap_period": "2021-2022"},
    {"person_a": 18, "person_b": 19, "type": "predecessor_successor", "context": "市委书记继任", "overlap_org": "中共天水市委员会", "overlap_period": "2013-2021"},
    # 市长↔前任市长 继任关系
    {"person_a": 2, "person_b": 20, "type": "predecessor_successor", "context": "市长继任", "overlap_org": "天水市人民政府", "overlap_period": "2024"},
    # 常委会成员 共事关系
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "市委常委班子", "overlap_org": "中共天水市委员会", "overlap_period": "2026-至今"},
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "市委常委班子", "overlap_org": "中共天水市委员会", "overlap_period": "2026-至今"},
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "市委常委班子", "overlap_org": "中共天水市委员会", "overlap_period": "2026-至今"},
    {"person_a": 1, "person_b": 9, "type": "overlap", "context": "市委常委班子", "overlap_org": "中共天水市委员会", "overlap_period": "2026-至今"},
    {"person_a": 1, "person_b": 10, "type": "overlap", "context": "市委常委班子", "overlap_org": "中共天水市委员会", "overlap_period": "2026-至今"},
    {"person_a": 1, "person_b": 11, "type": "overlap", "context": "市委常委班子", "overlap_org": "中共天水市委员会", "overlap_period": "2026-至今"},
    {"person_a": 1, "person_b": 12, "type": "overlap", "context": "市委常委班子", "overlap_org": "中共天水市委员会", "overlap_period": "2026-至今"},
    {"person_a": 1, "person_b": 13, "type": "overlap", "context": "市委常委班子", "overlap_org": "中共天水市委员会", "overlap_period": "2026-至今"},
    # 市长↔政府班子成员
    {"person_a": 2, "person_b": 9, "type": "overlap", "context": "市政府班子", "overlap_org": "天水市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 10, "type": "overlap", "context": "市政府班子", "overlap_org": "天水市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 14, "type": "overlap", "context": "市政府班子", "overlap_org": "天水市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 15, "type": "overlap", "context": "市政府班子", "overlap_org": "天水市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 16, "type": "overlap", "context": "市政府班子", "overlap_org": "天水市人民政府", "overlap_period": "至今"},
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

def color_for_role(title):
    t = title or ""
    if "书记" in t and "纪委" not in t and "副" not in t[:t.index("书记")] if "书记" in t else True:
        return "#E03C31"
    if "市长" in t or "县长" in t or "区长" in t:
        return "#4a7fc7"
    if "人大" in t:
        return "#5a7a9a"
    if "政协" in t:
        return "#7a5a9a"
    if "纪委" in t:
        return "#d4880f"
    if "副书记" in t:
        return "#E07A31"
    if "副市长" in t or "副县长" in t or "副区长" in t:
        return "#6a8fe7"
    return "#888888"

def org_color(org_type):
    return {"党委": "rgba(200,50,50,0.3)", "政府": "rgba(50,100,200,0.3)",
            "人大": "rgba(90,122,154,0.3)", "政协": "rgba(122,90,154,0.3)",
            "纪委": "rgba(200,150,20,0.3)"}.get(org_type, "rgba(200,200,200,0.3)")

gexf_parts = []
gexf_parts.append('<?xml version="1.0" encoding="UTF-8"?>')
gexf_parts.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
gexf_parts.append('<meta><creator>Gansu Tianshui Investigator</creator><description>天水市领导班子工作关系网络</description></meta>')
gexf_parts.append('<graph mode="static" defaultedgetype="undirected">')

# Nodes
gexf_parts.append('<nodes>')
for p in persons:
    slug_id = f"tianshui_{p['id']}"
    role_color = color_for_role(p["current_post"])
    is_top = "书记" in (p["current_post"] or "") and "纪委" not in (p["current_post"] or "") and "副" not in (p["current_post"] or "")
    is_gov = ("市长" in (p["current_post"] or "") and "副" not in (p["current_post"] or "")) or \
             ("县长" in (p["current_post"] or "") and "副" not in (p["current_post"] or "")) or \
             ("区长" in (p["current_post"] or "") and "副" not in (p["current_post"] or ""))
    size = 20.0 if is_top else 15.0 if is_gov else 12.0
    label = f"{p['name']} ({p['current_post'] or '?'})"
    gexf_parts.append(f'<node id="{slug_id}" label="{label}">')
    gexf_parts.append(f'<attvalues><attvalue for="role" value="{p["current_post"]}"/><attvalue for="org" value="{p["current_org"]}"/><attvalue for="birth" value="{p["birth"]}"/><attvalue for="birthplace" value="{p["birthplace"]}"/></attvalues>')
    gexf_parts.append(f'<viz:color r="{int(role_color[1:3],16)}" g="{int(role_color[3:5],16)}" b="{int(role_color[5:7],16)}"/>')
    gexf_parts.append(f'<viz:size value="{size}"/>')
    gexf_parts.append('</node>')

for o in organizations:
    oid = f"org_{o['id']}"
    oc = org_color(o["type"])
    oc_rgb = oc.replace("rgba(", "").rstrip(")").split(",")
    gexf_parts.append(f'<node id="{oid}" label="{o["name"]}">')
    gexf_parts.append(f'<attvalues><attvalue for="type" value="{o["type"]}"/><attvalue for="level" value="{o["level"]}"/></attvalues>')
    gexf_parts.append(f'<viz:color r="{int(oc_rgb[0])}" g="{int(oc_rgb[1])}" b="{int(oc_rgb[2])}"/>')
    gexf_parts.append(f'<viz:size value="8.0"/>')
    gexf_parts.append('</node>')
gexf_parts.append('</nodes>')

# Edges
gexf_parts.append('<edges>')
edge_id = 0
for po in positions:
    p = next(x for x in persons if x["id"] == po["person_id"])
    o = next(x for x in organizations if x["id"] == po["org_id"])
    edge_id += 1
    label = f"{p['name']} → {o['name']} ({po['title']})"
    gexf_parts.append(f'<edge id="e{edge_id}" source="tianshui_{p["id"]}" target="org_{o["id"]}" label="{label}" weight="1.0">')
    gexf_parts.append(f'<attvalues><attvalue for="type" value="worked_at"/><attvalue for="title" value="{po["title"]}"/><attvalue for="start" value="{po["start"]}"/><attvalue for="end" value="{po["end"]}"/></attvalues>')
    gexf_parts.append('</edge>')

for r in relationships:
    p_a = next(x for x in persons if x["id"] == r["person_a"])
    p_b = next(x for x in persons if x["id"] == r["person_b"])
    edge_id += 1
    gexf_parts.append(f'<edge id="e{edge_id}" source="tianshui_{p_a["id"]}" target="tianshui_{p_b["id"]}" label="{r["context"]}" weight="2.0">')
    gexf_parts.append(f'<attvalues><attvalue for="type" value="relationship"/><attvalue for="context" value="{r["context"]}"/></attvalues>')
    gexf_parts.append('</edge>')

gexf_parts.append('</edges>')
gexf_parts.append('</graph>')
gexf_parts.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(gexf_parts))

print(f"✅ GEXF 已创建: {GEXF_PATH}")
print(f"   节点: {len(persons) + len(organizations)} | 边: {edge_id}")

conn.close()
print("✅ 完成!")
