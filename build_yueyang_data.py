#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Yueyang City leadership network."""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/yueyang_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/yueyang_network.gexf")

# ── DATA ──

persons = [
    # ===== City-level =====
    {"id": 1, "name": "谢卫江", "gender": "男", "ethnicity": "汉族",
     "birth": "1973-01", "birthplace": "河南扶沟", "education": "硕士（东南大学热能工程）",
     "party_join": "中共党员", "work_start": "1997-04",
     "current_post": "中共湖南省委副书记、岳阳市委书记", "current_org": "中共岳阳市委员会",
     "source": "https://zh.wikipedia.org/wiki/%E8%B0%A2%E5%8D%AB%E6%B1%9F"},
    {"id": 2, "name": "李挚", "gender": "男", "ethnicity": "汉族",
     "birth": "1969-01", "birthplace": "湖南浏阳", "education": "大学（湖南科技大学中文系）",
     "party_join": "1991-03", "work_start": "1991",
     "current_post": "岳阳市人民政府市长", "current_org": "岳阳市人民政府",
     "source": "https://zh.wikipedia.org/wiki/%E6%9D%8E%E6%8C%9A"},
    {"id": 3, "name": "曹普华", "gender": "男", "ethnicity": "汉族",
     "birth": "1966-09", "birthplace": "湖南衡山", "education": "大学（湖南师范大学/中国人民大学）",
     "party_join": "1987-06", "work_start": "1988",
     "current_post": "中共湖南省委副秘书长、办公厅主任", "current_org": "中共湖南省委办公厅",
     "source": "https://zh.wikipedia.org/wiki/%E6%9B%B9%E6%99%AE%E5%8D%8E"},
    {"id": 4, "name": "马娜", "gender": "女", "ethnicity": "汉族",
     "birth": "1969-03", "birthplace": "湖南临澧", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "岳阳市人大常委会主任", "current_org": "岳阳市人大常委会",
     "source": "https://zh.wikipedia.org/wiki/%E5%B2%B3%E9%98%B3%E5%B8%82"},
    {"id": 5, "name": "汪涛", "gender": "男", "ethnicity": "汉族",
     "birth": "1968-01", "birthplace": "湖南湘阴", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "岳阳市政协主席", "current_org": "政协岳阳市委员会",
     "source": "https://zh.wikipedia.org/wiki/%E5%B2%B3%E9%98%B3%E5%B8%82"},

    # ===== 岳阳楼区 =====
    {"id": 6, "name": "曾平原", "gender": "男", "ethnicity": "汉族",
     "birth": "1971-09", "birthplace": "湖南", "education": "硕士研究生",
     "party_join": "中共党员", "work_start": "1989-07",
     "current_post": "岳阳楼区委书记", "current_org": "中共岳阳市岳阳楼区委员会",
     "source": "https://www.baidu.com/s?wd=%E5%B2%B3%E9%98%B3%E6%A5%BC%E5%8C%BA+%E5%8C%BA%E5%A7%94%E4%B9%A6%E8%AE%B0"},
    {"id": 7, "name": "杨钦涵", "gender": "男", "ethnicity": "汉族",
     "birth": "1983-02", "birthplace": "湖南", "education": "研究生，法学硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "岳阳楼区委副书记、代区长", "current_org": "岳阳市岳阳楼区人民政府",
     "source": "https://www.yylq.gov.cn"},

    # ===== 云溪区 =====
    {"id": 8, "name": "蒋春艳", "gender": "女", "ethnicity": "汉族",
     "birth": "1980-04", "birthplace": "湖北随州", "education": "研究生工学博士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "云溪区委书记、区长（兼任岳阳绿色化工高新区党工委书记）", "current_org": "中共岳阳市云溪区委员会",
     "source": "https://www.163.com/dy/article/JDSCCSUK0514R9P4.html"},

    # ===== 君山区 =====
    {"id": 9, "name": "雷欣", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "湖南", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "君山区委书记", "current_org": "中共岳阳市君山区委员会",
     "source": "https://www.rednet.cn"},
    {"id": 10, "name": "陈淼", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "湖南", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "君山区人民政府区长", "current_org": "岳阳市君山区人民政府",
     "source": "https://www.junshan.gov.cn"},

    # ===== 岳阳县 =====
    {"id": 11, "name": "肖湘晖", "gender": "男", "ethnicity": "汉族",
     "birth": "1974-05", "birthplace": "湖南洞口", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "岳阳县委书记", "current_org": "中共岳阳县委员会",
     "source": "https://zh.wikipedia.org/wiki/%E5%B2%B3%E9%98%B3%E5%8E%BF"},
    {"id": 12, "name": "吴光文", "gender": "男", "ethnicity": "汉族",
     "birth": "1974-01", "birthplace": "湖南汨罗", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "岳阳县人民政府县长", "current_org": "岳阳县人民政府",
     "source": "https://zh.wikipedia.org/wiki/%E5%B2%B3%E9%98%B3%E5%8E%BF"},

    # ===== 华容县 =====
    {"id": 13, "name": "陶伟军", "gender": "男", "ethnicity": "汉族",
     "birth": "1970-10", "birthplace": "湖南宁乡", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "华容县委书记", "current_org": "中共华容县委员会",
     "source": "https://zh.wikipedia.org/wiki/%E5%8D%8E%E5%AE%B9%E5%8E%BF"},
    {"id": 14, "name": "周鹏", "gender": "男", "ethnicity": "汉族",
     "birth": "1978-01", "birthplace": "湖南湘阴", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "华容县人民政府县长", "current_org": "华容县人民政府",
     "source": "https://zh.wikipedia.org/wiki/%E5%8D%8E%E5%AE%B9%E5%8E%BF"},

    # ===== 湘阴县 =====
    {"id": 15, "name": "刘世奇", "gender": "男", "ethnicity": "汉族",
     "birth": "1980-10", "birthplace": "河南郾城", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "湘阴县委书记（兼县长）", "current_org": "中共湘阴县委员会",
     "source": "https://zh.wikipedia.org/wiki/%E6%B9%98%E9%98%B4%E5%8E%BF"},

    # ===== 平江县 =====
    {"id": 16, "name": "李勇", "gender": "男", "ethnicity": "汉族",
     "birth": "1969-03", "birthplace": "湖南汨罗", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "平江县委书记", "current_org": "中共平江县委员会",
     "source": "https://zh.wikipedia.org/wiki/%E5%B9%B3%E6%B1%9F%E5%8E%BF"},
    {"id": 17, "name": "彭方建", "gender": "男", "ethnicity": "汉族",
     "birth": "1970-11", "birthplace": "湖南汨罗", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "平江县人民政府县长", "current_org": "平江县人民政府",
     "source": "https://zh.wikipedia.org/wiki/%E5%B9%B3%E6%B1%9F%E5%8E%BF"},

    # ===== 临湘市 =====
    {"id": 18, "name": "王文华", "gender": "男", "ethnicity": "汉族",
     "birth": "1969-01", "birthplace": "湖南华容", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "临湘市委书记", "current_org": "中共临湘市委员会",
     "source": "https://zh.wikipedia.org/wiki/%E4%B8%B4%E6%B9%98%E5%B8%82"},
    {"id": 19, "name": "刘琦", "gender": "男", "ethnicity": "汉族",
     "birth": "1969-10", "birthplace": "湖南", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "临湘市人民政府市长", "current_org": "临湘市人民政府",
     "source": "https://zh.wikipedia.org/wiki/%E4%B8%B4%E6%B9%98%E5%B8%82"},

    # ===== 汨罗市 =====
    {"id": 20, "name": "朱平波", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "湖南", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "汨罗市委书记", "current_org": "中共汨罗市委员会",
     "source": "https://www.miluo.gov.cn"},
    {"id": 21, "name": "林恒求", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "湖南", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "汨罗市人民政府市长", "current_org": "汨罗市人民政府",
     "source": "https://www.miluo.gov.cn"},
]

organizations = [
    {"id": 1, "name": "中共岳阳市委员会", "type": "党委", "level": "地级",
     "parent": "中共湖南省委员会", "location": "湖南省岳阳市"},
    {"id": 2, "name": "岳阳市人民政府", "type": "政府", "level": "地级",
     "parent": "湖南省人民政府", "location": "湖南省岳阳市"},
    {"id": 3, "name": "岳阳市人大常委会", "type": "人大", "level": "地级",
     "parent": "湖南省人大常委会", "location": "湖南省岳阳市"},
    {"id": 4, "name": "政协岳阳市委员会", "type": "政协", "level": "地级",
     "parent": "政协湖南省委员会", "location": "湖南省岳阳市"},
    {"id": 5, "name": "中共湖南省委办公厅", "type": "党委", "level": "省级",
     "parent": "中共湖南省委员会", "location": "湖南省长沙市"},
    {"id": 6, "name": "中共岳阳市岳阳楼区委员会", "type": "党委", "level": "县级",
     "parent": "中共岳阳市委员会", "location": "湖南省岳阳市岳阳楼区"},
    {"id": 7, "name": "岳阳市岳阳楼区人民政府", "type": "政府", "level": "县级",
     "parent": "岳阳市人民政府", "location": "湖南省岳阳市岳阳楼区"},
    {"id": 8, "name": "中共岳阳市云溪区委员会", "type": "党委", "level": "县级",
     "parent": "中共岳阳市委员会", "location": "湖南省岳阳市云溪区"},
    {"id": 9, "name": "岳阳市云溪区人民政府", "type": "政府", "level": "县级",
     "parent": "岳阳市人民政府", "location": "湖南省岳阳市云溪区"},
    {"id": 10, "name": "中共岳阳市君山区委员会", "type": "党委", "level": "县级",
     "parent": "中共岳阳市委员会", "location": "湖南省岳阳市君山区"},
    {"id": 11, "name": "岳阳市君山区人民政府", "type": "政府", "level": "县级",
     "parent": "岳阳市人民政府", "location": "湖南省岳阳市君山区"},
    {"id": 12, "name": "中共岳阳县委员会", "type": "党委", "level": "县级",
     "parent": "中共岳阳市委员会", "location": "湖南省岳阳市岳阳县"},
    {"id": 13, "name": "岳阳县人民政府", "type": "政府", "level": "县级",
     "parent": "岳阳市人民政府", "location": "湖南省岳阳市岳阳县"},
    {"id": 14, "name": "中共华容县委员会", "type": "党委", "level": "县级",
     "parent": "中共岳阳市委员会", "location": "湖南省岳阳市华容县"},
    {"id": 15, "name": "华容县人民政府", "type": "政府", "level": "县级",
     "parent": "岳阳市人民政府", "location": "湖南省岳阳市华容县"},
    {"id": 16, "name": "中共湘阴县委员会", "type": "党委", "level": "县级",
     "parent": "中共岳阳市委员会", "location": "湖南省岳阳市湘阴县"},
    {"id": 17, "name": "湘阴县人民政府", "type": "政府", "level": "县级",
     "parent": "岳阳市人民政府", "location": "湖南省岳阳市湘阴县"},
    {"id": 18, "name": "中共平江县委员会", "type": "党委", "level": "县级",
     "parent": "中共岳阳市委员会", "location": "湖南省岳阳市平江县"},
    {"id": 19, "name": "平江县人民政府", "type": "政府", "level": "县级",
     "parent": "岳阳市人民政府", "location": "湖南省岳阳市平江县"},
    {"id": 20, "name": "中共汨罗市委员会", "type": "党委", "level": "县级",
     "parent": "中共岳阳市委员会", "location": "湖南省岳阳市汨罗市"},
    {"id": 21, "name": "汨罗市人民政府", "type": "政府", "level": "县级",
     "parent": "岳阳市人民政府", "location": "湖南省岳阳市汨罗市"},
    {"id": 22, "name": "中共临湘市委员会", "type": "党委", "level": "县级",
     "parent": "中共岳阳市委员会", "location": "湖南省岳阳市临湘市"},
    {"id": 23, "name": "临湘市人民政府", "type": "政府", "level": "县级",
     "parent": "岳阳市人民政府", "location": "湖南省岳阳市临湘市"},
]

positions = [
    # City-level
    {"person_id": 1, "org_id": 1, "title": "中共湖南省委副书记、岳阳市委书记", "start": "2023-12", "end": "", "rank": "副省级", "note": "2025.07起兼任湖南省委副书记"},
    {"person_id": 2, "org_id": 2, "title": "岳阳市人民政府市长", "start": "2022-04", "end": "", "rank": "正厅级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "岳阳市委书记（前任）", "start": "2022-01", "end": "2023-12", "rank": "正厅级", "note": "现任省委副秘书长"},
    {"person_id": 3, "org_id": 5, "title": "中共湖南省委副秘书长、办公厅主任", "start": "2024", "end": "", "rank": "正厅级", "note": ""},
    {"person_id": 4, "org_id": 3, "title": "岳阳市人大常委会主任", "start": "2022-01", "end": "", "rank": "正厅级", "note": ""},
    {"person_id": 5, "org_id": 4, "title": "岳阳市政协主席", "start": "2025-11", "end": "", "rank": "正厅级", "note": ""},

    # District/county level
    {"person_id": 6, "org_id": 6, "title": "岳阳楼区委书记", "start": "", "end": "", "rank": "正县级", "note": ""},
    {"person_id": 7, "org_id": 7, "title": "岳阳楼区委副书记、代区长", "start": "2026-03", "end": "", "rank": "正县级", "note": "代区长"},
    {"person_id": 8, "org_id": 8, "title": "云溪区委书记、区长", "start": "2025-06", "end": "", "rank": "正县级", "note": "兼任岳阳绿色化工高新区党工委书记"},
    {"person_id": 9, "org_id": 10, "title": "君山区委书记", "start": "", "end": "", "rank": "正县级", "note": ""},
    {"person_id": 10, "org_id": 11, "title": "君山区人民政府区长", "start": "", "end": "", "rank": "正县级", "note": ""},
    {"person_id": 11, "org_id": 12, "title": "岳阳县委书记", "start": "2021-07", "end": "", "rank": "正县级", "note": ""},
    {"person_id": 12, "org_id": 13, "title": "岳阳县人民政府县长", "start": "2021-10", "end": "", "rank": "正县级", "note": ""},
    {"person_id": 13, "org_id": 14, "title": "华容县委书记", "start": "2020-06", "end": "", "rank": "正县级", "note": ""},
    {"person_id": 14, "org_id": 15, "title": "华容县人民政府县长", "start": "2021-10", "end": "", "rank": "正县级", "note": ""},
    {"person_id": 15, "org_id": 16, "title": "湘阴县委书记（兼县长）", "start": "2024-05", "end": "", "rank": "正县级", "note": "书记县长一肩挑"},
    {"person_id": 16, "org_id": 18, "title": "平江县委书记", "start": "2021-07", "end": "", "rank": "正县级", "note": ""},
    {"person_id": 17, "org_id": 19, "title": "平江县人民政府县长", "start": "2021-10", "end": "", "rank": "正县级", "note": ""},
    {"person_id": 18, "org_id": 22, "title": "临湘市委书记", "start": "2021-07", "end": "", "rank": "正县级", "note": ""},
    {"person_id": 19, "org_id": 23, "title": "临湘市人民政府市长", "start": "2021-10", "end": "", "rank": "正县级", "note": ""},
    {"person_id": 20, "org_id": 20, "title": "汨罗市委书记", "start": "", "end": "", "rank": "正县级", "note": ""},
    {"person_id": 21, "org_id": 21, "title": "汨罗市人民政府市长", "start": "", "end": "", "rank": "正县级", "note": ""},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "岳阳市委书记+市长党政搭档", "overlap_org": "岳阳市", "overlap_period": "2023.12—至今"},
    {"person_a": 3, "person_b": 1, "type": "职务接替", "context": "曹普华→谢卫江，前后任岳阳市委书记", "overlap_org": "中共岳阳市委员会", "overlap_period": "2023.12"},
    {"person_a": 1, "person_b": 4, "type": "党政搭档", "context": "谢卫江（书记）与马娜（人大主任）", "overlap_org": "岳阳市", "overlap_period": "2023.12—至今"},
    {"person_a": 1, "person_b": 5, "type": "党政搭档", "context": "谢卫江（书记）与汪涛（政协主席）", "overlap_org": "岳阳市", "overlap_period": "2023.12—至今"},
    # Known cross-county connections - 汨罗 connections (李勇平江书记, 彭方建平江县长, 吴光光岳阳县县长 are all 汨罗人)
    {"person_a": 16, "person_b": 12, "type": "同乡关系", "context": "李勇（平江书记）与吴光文（岳阳县县长）同籍汨罗", "overlap_org": "", "overlap_period": ""},
    {"person_a": 16, "person_b": 17, "type": "党政搭档", "context": "李勇（平江书记）与彭方建（平江县长）党政搭档", "overlap_org": "平江县", "overlap_period": "2021—至今"},
]

# ── BUILD DATABASE ──────────────────────────────────────────────────

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
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
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER,
    org_id INTEGER,
    title TEXT,
    start TEXT,
    end TEXT,
    rank TEXT,
    note TEXT,
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
);

CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_a INTEGER,
    person_b INTEGER,
    type TEXT,
    context TEXT,
    overlap_org TEXT,
    overlap_period TEXT,
    FOREIGN KEY (person_a) REFERENCES persons(id),
    FOREIGN KEY (person_b) REFERENCES persons(id)
);
""")

for p in persons:
    cur.execute("""INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"], p["education"],
         p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"]))

for o in organizations:
    cur.execute("""INSERT INTO organizations (id, name, type, level, parent, location)
        VALUES (?, ?, ?, ?, ?, ?)""", (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for po in positions:
    cur.execute("""INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
        VALUES (?, ?, ?, ?, ?, ?, ?)""", (po["person_id"], po["org_id"], po["title"], po["start"], po["end"], po["rank"], po["note"]))

for r in relationships:
    cur.execute("""INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
        VALUES (?, ?, ?, ?, ?, ?)""", (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

conn.commit()
conn.close()
print(f"✅ SQLite database created: {DB_PATH}")

# ── BUILD GEXF ──────────────────────────────────────────────────────

os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

def esc(text):
    """Escape XML special characters."""
    if text is None:
        return ""
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&apos;")

def get_color(post):
    if "书记" in post and "市委" in post and "省委" not in post:
        return "#E03C31"  # red for party secretary
    if "市长" in post and ("副市长" not in post):
        return "#4a7fc7"  # blue for mayor
    if "区长" in post or "县长" in post:
        return "#4a7fc7"
    if "人大" in post:
        return "#5a7a9a"
    if "政协" in post:
        return "#7a5a9a"
    return "#6a6a6a"

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# --- Attributes ---
lines.append('    <attributes class="node">')
lines.append('      <attribute id="role" title="Role" type="string"/>')
lines.append('      <attribute id="birth" title="Birth" type="string"/>')
lines.append('      <attribute id="birthplace" title="Birthplace" type="string"/>')
lines.append('      <attribute id="org_type" title="Org Type" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="type" title="Type" type="string"/>')
lines.append('      <attribute id="period" title="Period" type="string"/>')
lines.append('      <attribute id="context" title="Context" type="string"/>')
lines.append('    </attributes>')

# --- Nodes: Persons ---
lines.append('    <nodes>')
for p in persons:
    pid = f"p{p['id']}"
    role = "市委/区委书记" if ("书记" in p["current_post"] and "副书记" not in p["current_post"]) else "市长/区长/县长" if ("市长" in p["current_post"] or "区长" in p["current_post"] or "县长" in p["current_post"]) else "其他"
    c = get_color(p["current_post"])
    sz = 20.0 if ("书记" in p["current_post"] and "副书记" not in p["current_post"] and "省委" not in p["current_post"]) else 15.0 if ("市长" in p["current_post"] or "区长" in p["current_post"] or "县长" in p["current_post"]) else 12.0
    lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="role" value="{esc(role)}"/>')
    lines.append(f'          <attvalue for="birth" value="{esc(p["birth"])}"/>')
    lines.append(f'          <attvalue for="birthplace" value="{esc(p["birthplace"])}"/>')
    lines.append(f'          <attvalue for="org_type" value="person"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="{int(c[1:3],16)}" g="{int(c[3:5],16)}" b="{int(c[5:7],16)}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append(f'      </node>')
lines.append('    </nodes>')

# --- Nodes: Organizations ---
lines.append('    <nodes>')
for o in organizations:
    oid = f"o{o['id']}"
    lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="role" value="organization"/>')
    lines.append(f'          <attvalue for="org_type" value="{esc(o["type"])}"/>')
    lines.append(f'        </attvalues>')
    if o["type"] == "党委":
        lines.append('        <viz:color r="200" g="60" b="49"/>')
    elif o["type"] == "政府":
        lines.append('        <viz:color r="74" g="127" b="199"/>')
    else:
        lines.append('        <viz:color r="90" g="90" b="90"/>')
    lines.append('        <viz:size value="8.0"/>')
    lines.append('      </node>')
lines.append('    </nodes>')

# --- Edges: person→org (worked_at) ---
lines.append('    <edges>')
eid = 1
for po in positions:
    src = f"p{po['person_id']}"
    tgt = f"o{po['org_id']}"
    lines.append(f'      <edge id="e{eid}" source="{src}" target="{tgt}" label="worked_at">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="worked_at"/>')
    lines.append(f'          <attvalue for="period" value="{esc(po["start"])}—{esc(po["end"])}"/>')
    lines.append(f'          <attvalue for="context" value="{esc(po["title"])}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="180" g="180" b="180"/>')
    lines.append(f'        <viz:thickness value="1.0"/>')
    lines.append(f'      </edge>')
    eid += 1

# --- Edges: person↔person (relationship) ---
for r in relationships:
    src = f"p{r['person_a']}"
    tgt = f"p{r['person_b']}"
    lines.append(f'      <edge id="e{eid}" source="{src}" target="{tgt}" label="{esc(r["type"])}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="{esc(r["type"])}"/>')
    lines.append(f'          <attvalue for="period" value="{esc(r["overlap_period"])}"/>')
    lines.append(f'          <attvalue for="context" value="{esc(r["context"])}"/>')
    lines.append(f'        </attvalues>')
    if r["type"] in ("党政搭档", "职务接替"):
        lines.append('        <viz:color r="201" g="169" b="78"/>')
        lines.append('        <viz:thickness value="2.5"/>')
    else:
        lines.append('        <viz:color r="100" g="150" b="200"/>')
        lines.append('        <viz:thickness value="1.5"/>')
    lines.append(f'      </edge>')
    eid += 1

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"✅ GEXF graph created: {GEXF_PATH}")
print(f"📊 Summary: {len(persons)} persons, {len(organizations)} organizations, {len(positions)} positions, {len(relationships)} relationships")
