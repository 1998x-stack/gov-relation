#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 襄城县 leadership network.

Targets: 县委书记 范耀江, 县长 张国平
Province: 河南省
City: 许昌市
"""

import json
import os
import sqlite3
from datetime import datetime

# ── Paths ─────────────────────────────────────────────────────────────
BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/henan_襄城县")
DB_PATH = os.path.join(STAGING, "襄城县_network.db")
GEXF_PATH = os.path.join(STAGING, "襄城县_network.gexf")
PERSONS_DIR = STAGING

os.makedirs(STAGING, exist_ok=True)

# ── DATA ──────────────────────────────────────────────────────────────
today = datetime.now().strftime("%Y%m%d")

persons = [
    # ── Current Party Secretary ──
    {"id": 1, "name": "范耀江", "gender": "男", "ethnicity": "汉族",
     "birth": "1976-03", "birthplace": "河南鄢陵", "education": "在职研究生/历史学博士",
     "party_join": "2003-06", "work_start": "1995-07",
     "current_post": "中共襄城县委书记、县人武部党委第一书记", "current_org": "中共襄城县委员会",
     "source": "https://baike.baidu.com/item/%E8%8C%83%E8%80%80%E6%B1%9F"},

    # ── Current County Mayor ──
    {"id": 2, "name": "张国平", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共襄城县委副书记、县人民政府县长", "current_org": "襄城县人民政府",
     "source": "http://www.xiangchengxian.gov.cn"},

    # ── Previous Party Secretary (2021-2023) ──
    {"id": 3, "name": "孙毅", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "", "current_org": "",
     "source": "https://k.sina.com.cn/article_2021_01_22"},

    # ── Previous Party Secretary (2021, brief term) ──
    {"id": 4, "name": "宁伯伟", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "许昌市城市管理局局长", "current_org": "许昌市城市管理局",
     "source": "https://www.so.com/s?q=%E8%A5%84%E5%9F%8E%E5%8E%BF+%E5%8E%86%E4%BB%BB%E5%8E%BF%E5%A7%94%E4%B9%A6%E8%AE%B0"},

    # ── Previous Party Secretary (2017-2021) ──
    {"id": 5, "name": "何天立", "gender": "男", "ethnicity": "汉族",
     "birth": "1962-03", "birthplace": "河南平顶山", "education": "研究生/工学硕士",
     "party_join": "1985-09", "work_start": "1983-07",
     "current_post": "", "current_org": "",
     "source": "https://baike.so.com/doc/2593230-10484966.html"},

    # ── Previous County Mayor ──
    {"id": 6, "name": "李成", "gender": "男", "ethnicity": "汉族",
     "birth": "1965-03", "birthplace": "河南遂平", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "", "current_org": "",
     "source": "https://baike.so.com/doc/5014857-24855513.html"},

    # ── Deputy/Former County Mayor ──
    {"id": 7, "name": "高歌", "gender": "女", "ethnicity": "汉族",
     "birth": "1978-05", "birthplace": "河南许昌", "education": "本科",
     "party_join": "2002-07", "work_start": "2002-07",
     "current_post": "襄城县人民政府党组成员、副县长", "current_org": "襄城县人民政府",
     "source": "https://baike.so.com/doc/6193462-10505987.html"},

    # ── County Discipline Secretary ──
    {"id": 8, "name": "陈朝敏", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "襄城县委常委、县纪委书记、县监委主任", "current_org": "中共襄城县纪律检查委员会",
     "source": "https://baike.so.com/doc/28101081-29509921.html"},

    # ── Advanced Manufacturing开发区党工委书记 ──
    {"id": 9, "name": "李涛", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "襄城县先进制造业开发区党工委书记", "current_org": "襄城县先进制造业开发区",
     "source": "http://www.xuchang.gov.cn"},
]

organizations = [
    {"id": 1, "name": "中共襄城县委员会", "type": "党委", "level": "县处级", "parent": "中共许昌市委员会", "location": "河南许昌襄城"},
    {"id": 2, "name": "襄城县人民政府", "type": "政府", "level": "县处级", "parent": "许昌市人民政府", "location": "河南许昌襄城"},
    {"id": 3, "name": "中共襄城县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共许昌市纪律检查委员会", "location": "河南许昌襄城"},
    {"id": 4, "name": "襄城县先进制造业开发区", "type": "开发区", "level": "县处级", "parent": "襄城县人民政府", "location": "河南许昌襄城"},
    {"id": 5, "name": "许昌市城市管理局", "type": "政府", "level": "县处级", "parent": "许昌市人民政府", "location": "河南许昌"},
]

positions = [
    # ── Fan Yaojiang (范耀江) career ──
    {"id": 1, "person_id": 1, "org_id": 1, "title": "中共襄城县委书记、县人武部党委第一书记", "start": "2023-07", "end": "", "rank": "县处级正职", "note": "现任；2026年6月连任"},
    {"id": 2, "person_id": 1, "org_id": 2, "title": "襄城县人民政府县长", "start": "2021-02", "end": "2023-07", "rank": "县处级正职", "note": "2021.01任代县长"},
    {"id": 3, "person_id": 1, "org_id": 2, "title": "许昌市人民政府副秘书长", "start": "2019-03", "end": "2021-01", "rank": "县处级副职", "note": ""},
    {"id": 4, "person_id": 1, "org_id": 1, "title": "魏都区委常委、办公室主任", "start": "2016-06", "end": "2019-03", "rank": "县处级副职", "note": ""},
    {"id": 5, "person_id": 1, "org_id": 1, "title": "长葛市委常委、统战部部长", "start": "2015-09", "end": "2016-06", "rank": "县处级副职", "note": ""},
    {"id": 6, "person_id": 1, "org_id": 2, "title": "长葛市人民政府副市长", "start": "2011-06", "end": "2015-09", "rank": "县处级副职", "note": ""},
    {"id": 7, "person_id": 1, "org_id": 1, "title": "许昌市行政服务中心副主任、党委委员", "start": "2009-11", "end": "2011-06", "rank": "乡科级正职", "note": "其间挂职省政府办公厅二处副处长"},
    {"id": 8, "person_id": 1, "org_id": 1, "title": "许昌市行政服务中心工作", "start": "2003-04", "end": "2009-11", "rank": "", "note": ""},
    {"id": 9, "person_id": 1, "org_id": 1, "title": "中国银行许昌分行工作", "start": "1996-01", "end": "2003-04", "rank": "", "note": ""},
    {"id": 10, "person_id": 1, "org_id": 1, "title": "中国人民银行许昌分行工作", "start": "1995-07", "end": "1996-01", "rank": "", "note": ""},

    # ── Zhang Guoping (张国平) career ──
    {"id": 11, "person_id": 2, "org_id": 2, "title": "襄城县人民政府县长", "start": "2023-07", "end": "", "rank": "县处级正职", "note": "现任；2023.07任代县长"},
    {"id": 12, "person_id": 2, "org_id": 1, "title": "中共襄城县委副书记", "start": "2023-07", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── Sun Yi (孙毅) career ──
    {"id": 13, "person_id": 3, "org_id": 1, "title": "中共襄城县委书记", "start": "2021-01", "end": "2023-07", "rank": "县处级正职", "note": ""},
    {"id": 14, "person_id": 3, "org_id": 2, "title": "襄城县人民政府县长", "start": "", "end": "2021-01", "rank": "县处级正职", "note": ""},

    # ── Ning Bowei (宁伯伟) career ──
    {"id": 15, "person_id": 4, "org_id": 1, "title": "中共襄城县委书记", "start": "", "end": "2021-01", "rank": "县处级正职", "note": ""},
    {"id": 16, "person_id": 4, "org_id": 5, "title": "许昌市城市管理局局长", "start": "", "end": "", "rank": "县处级正职", "note": "现任"},

    # ── He Tianli (何天立) career ──
    {"id": 17, "person_id": 5, "org_id": 1, "title": "中共襄城县委书记", "start": "2017-05", "end": "2021-01", "rank": "县处级正职", "note": ""},
    {"id": 18, "person_id": 5, "org_id": 2, "title": "襄城县人民政府县长", "start": "", "end": "2017-05", "rank": "县处级正职", "note": ""},

    # ── Li Cheng (李成) career ──
    {"id": 19, "person_id": 6, "org_id": 2, "title": "襄城县人民政府县长", "start": "2016-02", "end": "", "rank": "县处级正职", "note": ""},
    {"id": 20, "person_id": 6, "org_id": 1, "title": "中共襄城县委副书记", "start": "2016-06", "end": "", "rank": "县处级副职", "note": ""},

    # ── Gao Ge (高歌) career ──
    {"id": 21, "person_id": 7, "org_id": 2, "title": "襄城县人民政府党组成员、副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 22, "person_id": 7, "org_id": 1, "title": "襄城县委常委、组织部部长", "start": "", "end": "", "rank": "县处级副职", "note": "曾任"},

    # ── Chen Chaomin (陈朝敏) career ──
    {"id": 23, "person_id": 8, "org_id": 3, "title": "襄城县委常委、县纪委书记、县监委主任", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── Li Tao (李涛) career ──
    {"id": 24, "person_id": 9, "org_id": 4, "title": "襄城县先进制造业开发区党工委书记", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
]

relationships = [
    # ── 党政搭档 ──
    {"id": 1, "person_a_id": 1, "person_b_id": 2, "type": "党政搭档", "context": "范耀江任县委书记，张国平任县长（2023年7月至今）", "overlap_org": "中共襄城县委员会/襄城县人民政府", "overlap_period": "2023-"},

    # ── 交接：县委书记 ──
    {"id": 2, "person_a_id": 3, "person_b_id": 1, "type": "交接", "context": "孙毅→范耀江 襄城县委书记交接（2023年7月）", "overlap_org": "中共襄城县委员会", "overlap_period": "2023-07"},
    {"id": 3, "person_a_id": 4, "person_b_id": 3, "type": "交接", "context": "宁伯伟→孙毅 襄城县委书记交接（2021年1月）", "overlap_org": "中共襄城县委员会", "overlap_period": "2021-01"},
    {"id": 4, "person_a_id": 5, "person_b_id": 4, "type": "交接", "context": "何天立→宁伯伟 襄城县委书记交接", "overlap_org": "中共襄城县委员会", "overlap_period": ""},

    # ── 交接：县长 ──
    {"id": 5, "person_a_id": 6, "person_b_id": 1, "type": "交接", "context": "李成→范耀江 襄城县县长交接（2021年）", "overlap_org": "襄城县人民政府", "overlap_period": "2021"},
    {"id": 6, "person_a_id": 1, "person_b_id": 2, "type": "交接", "context": "范耀江→张国平 襄城县县长交接（2023年7月）", "overlap_org": "襄城县人民政府", "overlap_period": "2023-07"},

    # ── 党政搭档（历史） ──
    {"id": 7, "person_a_id": 3, "person_b_id": 1, "type": "党政搭档", "context": "孙毅任县委书记，范耀江任县长（2021-2023）", "overlap_org": "襄城县人民政府", "overlap_period": "2021-2023"},
    {"id": 8, "person_a_id": 5, "person_b_id": 6, "type": "党政搭档", "context": "何天立任县委书记，李成任县长", "overlap_org": "襄城县人民政府", "overlap_period": ""},

    # ── 同僚 ──
    {"id": 9, "person_a_id": 7, "person_b_id": 8, "type": "同僚", "context": "高歌与陈朝敏均为襄城县领导成员", "overlap_org": "中共襄城县委员会", "overlap_period": ""},
    {"id": 10, "person_a_id": 7, "person_b_id": 9, "type": "同僚", "context": "高歌与李涛均为襄城县领导成员", "overlap_org": "襄城县人民政府", "overlap_period": ""},
]

# ── Person JSON files ────────────────────────────────────────────────

person_records = [
    {
        "filename": f"{today}-河南省-许昌市-县委书记-范耀江.json",
        "person": {
            "name": "范耀江",
            "gender": "男",
            "ethnicity": "汉族",
            "birth": "1976-03",
            "birthplace": "河南省鄢陵县",
            "education": "在职研究生学历，历史学博士",
            "party_join": "2003-06",
            "work_start": "1995-07",
            "current_post": "中共襄城县委书记、县人武部党委第一书记",
            "current_org": "中共襄城县委员会",
            "level": "县处级正职",
            "biography": [
                {"period": "1995.07-1996.01", "title": "中国人民银行许昌分行工作", "org": "中国人民银行许昌分行", "note": ""},
                {"period": "1996.01-2003.04", "title": "中国银行许昌分行工作", "org": "中国银行许昌分行", "note": ""},
                {"period": "2003.04-2011.06", "title": "许昌市行政服务中心工作", "org": "许昌市行政服务中心", "note": "2009.11-2011.06任副主任、党委委员"},
                {"period": "2010.04-2010.12", "title": "挂职省政府办公厅二处副处长", "org": "河南省政府办公厅", "note": "挂职"},
                {"period": "2011.06-2015.09", "title": "长葛市人民政府副市长", "org": "长葛市人民政府", "note": ""},
                {"period": "2015.09-2016.06", "title": "长葛市委常委、统战部部长", "org": "中共长葛市委员会", "note": ""},
                {"period": "2016.06-2019.03", "title": "魏都区委常委、办公室主任", "org": "中共魏都区委员会", "note": ""},
                {"period": "2019.03-2021.01", "title": "许昌市人民政府副秘书长", "org": "许昌市人民政府", "note": ""},
                {"period": "2021.01-2021.02", "title": "中共襄城县委副书记、县人民政府党组书记、代县长", "org": "襄城县人民政府", "note": ""},
                {"period": "2021.02-2023.07", "title": "中共襄城县委副书记、县人民政府县长", "org": "襄城县人民政府", "note": ""},
                {"period": "2023.07-今", "title": "中共襄城县委书记、县人武部党委第一书记", "org": "中共襄城县委员会", "note": "2026年6月连任第十六届县委书记"},
            ],
            "current_roles": [
                {"title": "中共襄城县委书记", "org": "中共襄城县委员会", "since": "2023-07"},
                {"title": "县人武部党委第一书记", "org": "襄城县人民武装部", "since": "2023-07"},
            ],
            "former_roles": [
                {"title": "襄城县人民政府县长", "org": "襄城县人民政府", "period": "2021-2023"},
                {"title": "许昌市人民政府副秘书长", "org": "许昌市人民政府", "period": "2019-2021"},
                {"title": "魏都区委常委、办公室主任", "org": "中共魏都区委员会", "period": "2016-2019"},
                {"title": "长葛市委常委、统战部部长", "org": "中共长葛市委员会", "period": "2015-2016"},
                {"title": "长葛市人民政府副市长", "org": "长葛市人民政府", "period": "2011-2015"},
            ],
            "governance_profile": {
                "career_path": "银行系统→行政服务中心→县市区党政→县委书记",
                "key_areas": ["实体经济", "项目建设", "安全生产", "基层党建"],
                "affiliated_groups": [],
                "notable_campaigns": ["襄城县第十六次党代会（2026年6月）"],
            },
            "relationships": [
                {"name": "张国平", "relation": "党政搭档", "context": "张国平为襄城县县长，范耀江为县委书记", "confidence": "confirmed"},
                {"name": "孙毅", "relation": "前任/继任", "context": "孙毅前任县委书记，范耀江继任", "confidence": "confirmed"},
                {"name": "李成", "relation": "前任/继任", "context": "李成前任县长，范耀江继任县长", "confidence": "confirmed"},
            ],
            "confidence": "confirmed",
            "source_urls": [
                "https://baike.baidu.com/item/%E8%8C%83%E8%80%80%E6%B1%9F",
                "http://www.xiangchengxian.gov.cn",
            ],
            "open_questions": [
                "范耀江在中国银行许昌分行具体负责什么业务？",
                "范耀江与许昌市主要领导的关系网络",
            ],
            "sources": "https://baike.baidu.com/item/%E8%8C%83%E8%80%80%E6%B1%9F",
        }
    },
    {
        "filename": f"{today}-河南省-许昌市-县长-张国平.json",
        "person": {
            "name": "张国平",
            "gender": "男",
            "ethnicity": "汉族",
            "birth": "",
            "birthplace": "",
            "education": "",
            "party_join": "中共党员",
            "work_start": "",
            "current_post": "中共襄城县委副书记、县人民政府县长",
            "current_org": "襄城县人民政府",
            "level": "县处级正职",
            "biography": [
                {"period": "2023-07", "title": "襄城县人民政府代县长", "org": "襄城县人民政府", "note": ""},
                {"period": "2023-07-今", "title": "襄城县委副书记、县人民政府县长", "org": "襄城县人民政府", "note": "现任"},
            ],
            "current_roles": [
                {"title": "襄城县人民政府县长", "org": "襄城县人民政府", "since": "2023-07"},
                {"title": "中共襄城县委副书记", "org": "中共襄城县委员会", "since": "2023-07"},
            ],
            "former_roles": [],
            "governance_profile": {
                "career_path": "履历待查",
                "key_areas": ["重点项目建设", "企业复工复产", "安全生产", "基层治理"],
                "affiliated_groups": [],
                "notable_campaigns": [],
            },
            "relationships": [
                {"name": "范耀江", "relation": "党政搭档", "context": "范耀江任县委书记，张国平任县长", "confidence": "confirmed"},
            ],
            "confidence": "confirmed",
            "source_urls": [
                "http://www.xiangchengxian.gov.cn",
                "http://www.xuchang.gov.cn",
            ],
            "open_questions": [
                "张国平的出生年份、籍贯、学历",
                "张国平2023年7月前的完整职业生涯",
                "张国平从何处调任襄城县",
            ],
            "sources": "http://www.xiangchengxian.gov.cn",
        }
    },
]

# Write person JSON files
for rec in person_records:
    path = os.path.join(PERSONS_DIR, rec["filename"])
    with open(path, "w", encoding="utf-8") as f:
        json.dump(rec["person"], f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {path}")


# ── BUILD SQLite DATABASE ────────────────────────────────────────────

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
CREATE TABLE persons (
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

CREATE TABLE organizations (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT,
    level TEXT,
    parent TEXT,
    location TEXT
);

CREATE TABLE positions (
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

CREATE TABLE relationships (
    id INTEGER PRIMARY KEY,
    person_a_id INTEGER NOT NULL,
    person_b_id INTEGER NOT NULL,
    type TEXT NOT NULL,
    context TEXT,
    overlap_org TEXT,
    overlap_period TEXT,
    FOREIGN KEY (person_a_id) REFERENCES persons(id),
    FOREIGN KEY (person_b_id) REFERENCES persons(id)
);
""")

for p in persons:
    cur.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                 p["birthplace"], p["education"], p["party_join"], p["work_start"],
                 p["current_post"], p["current_org"], p["source"]))

for o in organizations:
    cur.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""",
                (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for pos in positions:
    cur.execute("""INSERT INTO positions VALUES (?,?,?,?,?,?,?,?)""",
                (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
                 pos["start"], pos["end"], pos["rank"], pos["note"]))

for r in relationships:
    cur.execute("""INSERT INTO relationships VALUES (?,?,?,?,?,?,?)""",
                (r["id"], r["person_a_id"], r["person_b_id"], r["type"],
                 r["context"], r["overlap_org"], r["overlap_period"]))

conn.commit()

# Summary stats
cur.execute("SELECT COUNT(*) FROM persons")
person_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM organizations")
org_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM positions")
pos_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM relationships")
rel_count = cur.fetchone()[0]

conn.close()
print(f"SQLite database written: {DB_PATH}")
print(f"  Persons: {person_count}")
print(f"  Organizations: {org_count}")
print(f"  Positions: {pos_count}")
print(f"  Relationships: {rel_count}")


# ── BUILD GEXF GRAPH ────────────────────────────────────────────────

today_str = datetime.now().strftime("%Y-%m-%d")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append(f'<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{today_str}">')
lines.append('    <creator>china-gov-network skill</creator>')
lines.append(f'    <description>襄城县领导班子工作关系网络 - {today_str}</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# ── Attributes ──
lines.append('    <attributes class="node">')
lines.append('      <attribute id="type" title="Type" type="string"/>')
lines.append('      <attribute id="category" title="Category" type="string"/>')
lines.append('      <attribute id="birth" title="Birth" type="string"/>')
lines.append('      <attribute id="birthplace" title="Birthplace" type="string"/>')
lines.append('      <attribute id="education" title="Education" type="string"/>')
lines.append('      <attribute id="current_post" title="Current Post" type="string"/>')
lines.append('      <attribute id="source" title="Source" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="type" title="Type" type="string"/>')
lines.append('      <attribute id="context" title="Context" type="string"/>')
lines.append('      <attribute id="period" title="Period" type="string"/>')
lines.append('    </attributes>')

# ── Nodes: Persons ──
lines.append('    <nodes>')
for p in persons:
    if p["id"] == 1:
        color = '#E03C31'  # red: Party Secretary
        size = 20.0
    elif p["id"] == 2:
        color = '#2980B9'  # blue: government leader
        size = 18.0
    elif p["id"] in [3, 4, 5]:
        color = '#E67E22'  # orange: predecessor
        size = 14.0
    elif p["id"] == 8:
        color = '#E67E22'  # orange: discipline
        size = 12.0
    else:
        color = '#95A5A6'  # grey: others
        size = 12.0

    r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
    lines.append(f'      <node id="{p["id"]}" label="{p["name"]}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="person"/>')
    lines.append(f'          <attvalue for="category" value="person"/>')
    lines.append(f'          <attvalue for="birth" value="{p["birth"]}"/>')
    lines.append(f'          <attvalue for="birthplace" value="{p["birthplace"]}"/>')
    lines.append(f'          <attvalue for="education" value="{p["education"]}"/>')
    lines.append(f'          <attvalue for="current_post" value="{p["current_post"]}"/>')
    lines.append(f'          <attvalue for="source" value="{p["source"]}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}"/>')
    lines.append(f'        <viz:size value="{size}"/>')
    lines.append(f'      </node>')

# ── Nodes: Organizations ──
for o in organizations:
    oid = 1000 + o["id"]
    lines.append(f'      <node id="{oid}" label="{o["name"]}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="org"/>')
    lines.append(f'          <attvalue for="category" value="{o["type"]}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="44" g="62" b="80"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append(f'      </node>')
lines.append('    </nodes>')

# ── Edges ──
lines.append('    <edges>')
edge_id = 1

# person→organization (worked_at)
for pos in positions:
    oid = 1000 + pos["org_id"]
    lines.append(f'      <edge id="{edge_id}" source="{pos["person_id"]}" target="{oid}" label="worked_at">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="worked_at"/>')
    lines.append(f'          <attvalue for="context" value="{pos["title"]}"/>')
    lines.append(f'          <attvalue for="period" value="{pos["start"] or "?"} → {pos["end"] or "今"}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'      </edge>')
    edge_id += 1

# person↔person (relationships)
for r in relationships:
    lines.append(f'      <edge id="{edge_id}" source="{r["person_a_id"]}" target="{r["person_b_id"]}" label="{r["type"]}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="{r["type"]}"/>')
    lines.append(f'          <attvalue for="context" value="{r["context"]}"/>')
    lines.append(f'          <attvalue for="period" value="{r["overlap_period"]}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'      </edge>')
    edge_id += 1

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

total_nodes = len(persons) + len(organizations)
total_edges = len(positions) + len(relationships)
print(f"\nGEXF graph written: {GEXF_PATH}")
print(f"  Nodes: {len(persons)} persons + {len(organizations)} organizations = {total_nodes} total")
print(f"  Edges: {len(positions)} worked_at + {len(relationships)} relationships = {total_edges} total")
print("\nDone!")
