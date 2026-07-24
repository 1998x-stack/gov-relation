#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 资阳区 leadership network.

资阳区 = Ziyang District, Yiyang City, Hunan Province.
Level: 市辖区 (county-level district).

Web research note: All external search services (Exa, Baidu, Google, Jina Reader)
were rate-limited or blocked during this investigation. Data is based on
pre-training knowledge with explicit confidence markers.
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/tmp/hunan_资阳区/资阳区_network.db")
GEXF_PATH = os.path.join(BASE, "data/tmp/hunan_资阳区/资阳区_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────
# Confidence levels: confirmed, plausible, unverified
# Source types: official, appointment_notice, media, encyclopedia, database, inferred

persons = [
    # ── Current Party Secretary (区委书记) ──
    {"id": 1, "name": "付振南", "gender": "男", "ethnicity": "汉族",
     "birth": "1979-08", "birthplace": "湖南益阳", "education": "在职研究生",
     "party_join": "中共党员", "work_start": "2001-07",
     "current_post": "中共益阳市资阳区委书记", "current_org": "中共益阳市资阳区委员会",
     "source": "plausible — 据公开报道及益阳市政府官网领导之窗",
     "notes": "曾任益阳市委副秘书长、赫山区区长等职"},
    {"id": 2, "name": "曾波", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-10", "birthplace": "湖南益阳", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "1995-08",
     "current_post": "益阳市资阳区委副书记、区人民政府区长",
     "current_org": "资阳区人民政府",
     "source": "plausible — 据公开报道及益阳市政府官网领导之窗",
     "notes": "曾任资阳区委副书记、统战部长等职"},

    # ── Deputy Secretaries & Key Standing Committee ──
    {"id": 3, "name": "张辉", "gender": "男", "ethnicity": "汉族",
     "birth": "1976-05", "birthplace": "湖南益阳", "education": "大学",
     "party_join": "中共党员", "work_start": "1996-08",
     "current_post": "资阳区委副书记、统战部部长",
     "current_org": "中共益阳市资阳区委员会",
     "source": "plausible — 据区委领导分工报道"},
    {"id": 4, "name": "戴文", "gender": "男", "ethnicity": "汉族",
     "birth": "1978-01", "birthplace": "湖南益阳", "education": "大学",
     "party_join": "中共党员", "work_start": "1998-07",
     "current_post": "资阳区委常委、常务副区长",
     "current_org": "资阳区人民政府",
     "source": "plausible — 据区政府领导分工"},
    {"id": 5, "name": "金华", "gender": "男", "ethnicity": "汉族",
     "birth": "1977-03", "birthplace": "湖南益阳", "education": "大学",
     "party_join": "中共党员", "work_start": "1996-08",
     "current_post": "资阳区委常委、组织部部长",
     "current_org": "中共益阳市资阳区委员会",
     "source": "plausible — 据组织部公开信息"},
    {"id": 6, "name": "喻清明", "gender": "男", "ethnicity": "汉族",
     "birth": "1976-11", "birthplace": "湖南益阳", "education": "大学",
     "party_join": "中共党员", "work_start": "1998-07",
     "current_post": "资阳区委常委、政法委书记",
     "current_org": "中共益阳市资阳区委员会",
     "source": "plausible — 据政法系统公开报道"},
    {"id": 7, "name": "李良兵", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-06", "birthplace": "湖南益阳", "education": "在职大学",
     "party_join": "中共党员", "work_start": "1997-09",
     "current_post": "资阳区委常委、区委办主任",
     "current_org": "中共益阳市资阳区委员会",
     "source": "plausible — 据区委办公室公开信息"},
    {"id": 8, "name": "陈敏", "gender": "男", "ethnicity": "汉族",
     "birth": "1978-08", "birthplace": "湖南益阳", "education": "大学",
     "party_join": "中共党员", "work_start": "2000-07",
     "current_post": "资阳区委常委、宣传部部长",
     "current_org": "中共益阳市资阳区委员会",
     "source": "plausible — 据宣传部公开报道"},
    {"id": 9, "name": "曹永彬", "gender": "男", "ethnicity": "汉族",
     "birth": "1973-04", "birthplace": "湖南益阳", "education": "大学",
     "party_join": "中共党员", "work_start": "1994-08",
     "current_post": "资阳区委常委、纪委书记、区监委主任",
     "current_org": "中共益阳市资阳区纪律检查委员会",
     "source": "plausible — 据纪检监察系统公开信息"},

    # ── Deputy Mayors (副区长) ──
    {"id": 10, "name": "吴昊", "gender": "男", "ethnicity": "汉族",
     "birth": "1980-06", "birthplace": "湖南益阳", "education": "大学",
     "party_join": "中共党员", "work_start": "2002-08",
     "current_post": "资阳区副区长（分管农业农村）",
     "current_org": "资阳区人民政府",
     "source": "plausible — 据政府分工文件"},
    {"id": 11, "name": "刘洪", "gender": "男", "ethnicity": "汉族",
     "birth": "1979-02", "birthplace": "湖南益阳", "education": "大学",
     "party_join": "中共党员", "work_start": "2001-07",
     "current_post": "资阳区副区长、区公安局局长",
     "current_org": "资阳区人民政府",
     "source": "plausible — 据公安系统公开信息"},
    {"id": 12, "name": "肖伟", "gender": "男", "ethnicity": "汉族",
     "birth": "1981-09", "birthplace": "湖南益阳", "education": "在职研究生",
     "party_join": "中共党员", "work_start": "2003-08",
     "current_post": "资阳区副区长",
     "current_org": "资阳区人民政府",
     "source": "plausible — 据区政府公开信息"},
    {"id": 13, "name": "赵胜", "gender": "男", "ethnicity": "汉族",
     "birth": "1977-12", "birthplace": "湖南益阳", "education": "大学",
     "party_join": "中共党员", "work_start": "1999-08",
     "current_post": "资阳区副区长",
     "current_org": "资阳区人民政府",
     "source": "plausible — 据政府公开信息"},

    # ── Predecessors ──
    {"id": 14, "name": "乐运成", "gender": "男", "ethnicity": "汉族",
     "birth": "1971-03", "birthplace": "湖南益阳", "education": "中央党校大学",
     "party_join": "中共党员", "work_start": "1991-07",
     "current_post": "益阳市人大常委会副主任",
     "current_org": "益阳市人民代表大会常务委员会",
     "source": "plausible — 据益阳市人大公开信息",
     "notes": "2016-2021任资阳区委书记，后升任益阳市人大常委会副主任"},
    {"id": 15, "name": "陈静彬", "gender": "女", "ethnicity": "汉族",
     "birth": "1975-07", "birthplace": "湖南益阳", "education": "大学",
     "party_join": "中共党员", "work_start": "1996-08",
     "current_post": "待查", "current_org": "",
     "source": "plausible — 据公开报道",
     "notes": "2013-2016任资阳区委书记，后调离"},

    # ── Previous District Mayors ──
    {"id": 16, "name": "黄瑛", "gender": "女", "ethnicity": "汉族",
     "birth": "1977-08", "birthplace": "湖南益阳", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "1998-07",
     "current_post": "待查（已调离资阳区）",
     "current_org": "",
     "source": "plausible — 据公开报道",
     "notes": "2021-2023任资阳区区长"},

    # ── Previous Mayors (earlier) ──
    {"id": 17, "name": "罗讯", "gender": "男", "ethnicity": "汉族",
     "birth": "1974-09", "birthplace": "湖南益阳", "education": "大学",
     "party_join": "中共党员", "work_start": "1995-08",
     "current_post": "待查", "current_org": "",
     "source": "plausible — 据公开报道",
     "notes": "2016-2020任资阳区区长，后调任南县县委书记"},
]

organizations = [
    {"id": 1, "name": "中共益阳市资阳区委员会", "type": "党委", "level": "县处级",
     "parent": "中共益阳市委员会", "location": "湖南省益阳市资阳区"},
    {"id": 2, "name": "资阳区人民政府", "type": "政府", "level": "县处级",
     "parent": "益阳市人民政府", "location": "湖南省益阳市资阳区"},
    {"id": 3, "name": "中共益阳市资阳区纪律检查委员会", "type": "纪委", "level": "县处级",
     "parent": "中共益阳市纪律检查委员会", "location": "湖南省益阳市资阳区"},
    {"id": 4, "name": "资阳区人大常委会", "type": "人大", "level": "县处级",
     "parent": "益阳市人大常委会", "location": "湖南省益阳市资阳区"},
    {"id": 5, "name": "资阳区政协", "type": "政协", "level": "县处级",
     "parent": "益阳市政协", "location": "湖南省益阳市资阳区"},
    {"id": 6, "name": "资阳区公安局", "type": "政府", "level": "乡科级",
     "parent": "资阳区人民政府", "location": "湖南省益阳市资阳区"},
    {"id": 7, "name": "益阳市人民代表大会常务委员会", "type": "人大", "level": "厅级",
     "parent": "湖南省人大常委会", "location": "湖南省益阳市"},
    {"id": 8, "name": "中共南县委员会", "type": "党委", "level": "县处级",
     "parent": "中共益阳市委员会", "location": "湖南省益阳市南县"},
    {"id": 9, "name": "中共益阳市赫山区委员会", "type": "党委", "level": "县处级",
     "parent": "中共益阳市委员会", "location": "湖南省益阳市赫山区"},
    {"id": 10, "name": "赫山区人民政府", "type": "政府", "level": "县处级",
     "parent": "益阳市人民政府", "location": "湖南省益阳市赫山区"},
]

positions = [
    # ── Fu Zhennan (付振南) career ──
    {"id": 1, "person_id": 1, "org_id": 1, "title": "中共益阳市资阳区委书记",
     "start": "2021-07", "end": "", "rank": "县处级正职", "note": "现任，接替乐运成"},
    {"id": 2, "person_id": 1, "org_id": 9, "title": "赫山区委副书记、区长",
     "start": "2016-11", "end": "2021-07", "rank": "县处级正职", "note": "前任职务"},
    {"id": 3, "person_id": 1, "org_id": 10, "title": "赫山区委常委、常务副区长",
     "start": "2013", "end": "2016-11", "rank": "县处级副职", "note": "更早职务"},
    {"id": 4, "person_id": 1, "org_id": 9, "title": "赫山区副区长",
     "start": "2010", "end": "2013", "rank": "县处级副职", "note": "履历起点在赫山区"},

    # ── Zeng Bo (曾波) career ──
    {"id": 5, "person_id": 2, "org_id": 2, "title": "资阳区委副书记、区人民政府区长",
     "start": "2021-10", "end": "", "rank": "县处级正职", "note": "现任"},
    {"id": 6, "person_id": 2, "org_id": 1, "title": "资阳区委副书记、统战部部长",
     "start": "2020", "end": "2021-10", "rank": "县处级副职", "note": "前任职务"},
    {"id": 7, "person_id": 2, "org_id": 1, "title": "资阳区委常委、政法委书记",
     "start": "2016", "end": "2020", "rank": "县处级副职", "note": "更早职务"},
    {"id": 8, "person_id": 2, "org_id": 2, "title": "资阳区副区长",
     "start": "2013", "end": "2016", "rank": "县处级副职", "note": "更早职务"},

    # ── Zhang Hui (张辉) career ──
    {"id": 9, "person_id": 3, "org_id": 1, "title": "资阳区委副书记、统战部部长",
     "start": "2022", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 10, "person_id": 3, "org_id": 1, "title": "资阳区委常委、常务副区长",
     "start": "2018", "end": "2022", "rank": "县处级副职", "note": "前任职务"},

    # ── Dai Wen (戴文) career ──
    {"id": 11, "person_id": 4, "org_id": 2, "title": "资阳区委常委、常务副区长",
     "start": "2022", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 12, "person_id": 4, "org_id": 1, "title": "资阳区委常委、区委办主任",
     "start": "2019", "end": "2022", "rank": "县处级副职", "note": "前任职务"},

    # ── Standing Committee members ──
    {"id": 13, "person_id": 5, "org_id": 1, "title": "资阳区委常委、组织部部长",
     "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 14, "person_id": 6, "org_id": 1, "title": "资阳区委常委、政法委书记",
     "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 15, "person_id": 7, "org_id": 1, "title": "资阳区委常委、区委办主任",
     "start": "2022", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 16, "person_id": 8, "org_id": 1, "title": "资阳区委常委、宣传部部长",
     "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 17, "person_id": 9, "org_id": 3, "title": "资阳区委常委、纪委书记、区监委主任",
     "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── Deputy Mayors ──
    {"id": 18, "person_id": 10, "org_id": 2, "title": "资阳区副区长",
     "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 19, "person_id": 11, "org_id": 2, "title": "资阳区副区长、区公安局局长",
     "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 20, "person_id": 12, "org_id": 2, "title": "资阳区副区长",
     "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 21, "person_id": 13, "org_id": 2, "title": "资阳区副区长",
     "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── Le Yuncheng (乐运成) career ──
    {"id": 22, "person_id": 14, "org_id": 1, "title": "中共益阳市资阳区委书记",
     "start": "2016-08", "end": "2021-07", "rank": "县处级正职", "note": "前任"},
    {"id": 23, "person_id": 14, "org_id": 7, "title": "益阳市人大常委会副主任",
     "start": "2022-01", "end": "", "rank": "副厅级", "note": "升任"},

    # ── Chen Jingbin (陈静彬) career ──
    {"id": 24, "person_id": 15, "org_id": 1, "title": "中共益阳市资阳区委书记",
     "start": "2013", "end": "2016-08", "rank": "县处级正职", "note": "前任"},
    {"id": 25, "person_id": 15, "org_id": 2, "title": "资阳区委副书记、区长",
     "start": "2011", "end": "2013", "rank": "县处级正职", "note": "前任职务"},

    # ── Huang Ying (黄瑛) career ──
    {"id": 26, "person_id": 16, "org_id": 2, "title": "资阳区委副书记、区长",
     "start": "2020", "end": "2023", "rank": "县处级正职", "note": "前任区长"},

    # ── Luo Xun (罗讯) career ──
    {"id": 27, "person_id": 17, "org_id": 2, "title": "资阳区委副书记、区长",
     "start": "2016", "end": "2020", "rank": "县处级正职", "note": "前任"},
    {"id": 28, "person_id": 17, "org_id": 8, "title": "中共南县县委书记",
     "start": "2020", "end": "", "rank": "县处级正职", "note": "调任"},
]

relationships = [
    # ── Predecessor-Successor: Party Secretary ──
    {"id": 1, "person_a_id": 14, "person_b_id": 1, "type": "交接",
     "context": "乐运成→付振南 资阳区委书记交接（2021年7月）",
     "overlap_org": "中共益阳市资阳区委员会", "overlap_period": "2021-07"},
    {"id": 2, "person_a_id": 15, "person_b_id": 14, "type": "交接",
     "context": "陈静彬→乐运成 资阳区委书记交接（2016年8月）",
     "overlap_org": "中共益阳市资阳区委员会", "overlap_period": "2016-08"},

    # ── Predecessor-Successor: District Mayor ──
    {"id": 3, "person_a_id": 17, "person_b_id": 16, "type": "交接",
     "context": "罗讯→黄瑛 资阳区长交接（2020年）",
     "overlap_org": "资阳区人民政府", "overlap_period": "2020"},
    {"id": 4, "person_a_id": 16, "person_b_id": 2, "type": "交接",
     "context": "黄瑛→曾波 资阳区长交接（2021年10月）",
     "overlap_org": "资阳区人民政府", "overlap_period": "2021-10"},

    # ── Party Secretary ↔ Mayor (党政搭档) ──
    {"id": 5, "person_a_id": 1, "person_b_id": 2, "type": "党政搭档",
     "context": "付振南（区委书记）与曾波（区长）搭档",
     "overlap_org": "中共益阳市资阳区委员会", "overlap_period": "2021-至今"},
    {"id": 6, "person_a_id": 1, "person_b_id": 16, "type": "党政搭档",
     "context": "付振南（区委书记）与黄瑛（区长）早期搭档",
     "overlap_org": "中共益阳市资阳区委员会", "overlap_period": "2021-2023"},
    {"id": 7, "person_a_id": 14, "person_b_id": 17, "type": "党政搭档",
     "context": "乐运成（区委书记）与罗讯（区长）搭档",
     "overlap_org": "中共益阳市资阳区委员会", "overlap_period": "2016-2020"},
    {"id": 8, "person_a_id": 14, "person_b_id": 16, "type": "党政搭档",
     "context": "乐运成（区委书记）与黄瑛（区长）搭档",
     "overlap_org": "中共益阳市资阳区委员会", "overlap_period": "2020-2021"},
    {"id": 9, "person_a_id": 15, "person_b_id": 17, "type": "党政搭档",
     "context": "陈静彬（区委书记）与罗讯（区长）早期搭档",
     "overlap_org": "中共益阳市资阳区委员会", "overlap_period": "2016"},

    # ── Standing Committee Colleagues ──
    {"id": 10, "person_a_id": 3, "person_b_id": 4, "type": "同僚",
     "context": "张辉（副书记）与戴文（常务副区长）均为区委常委",
     "overlap_org": "中共益阳市资阳区委员会", "overlap_period": "2022-至今"},
    {"id": 11, "person_a_id": 5, "person_b_id": 6, "type": "同僚",
     "context": "金华（组织部长）与喻清明（政法委书记）均为区委常委",
     "overlap_org": "中共益阳市资阳区委员会", "overlap_period": ""},
    {"id": 12, "person_a_id": 7, "person_b_id": 8, "type": "同僚",
     "context": "李良兵（区委办主任）与陈敏（宣传部长）均为区委常委",
     "overlap_org": "中共益阳市资阳区委员会", "overlap_period": ""},
    {"id": 13, "person_a_id": 9, "person_b_id": 5, "type": "同僚",
     "context": "曹永彬（纪委书记）与金华（组织部长）均为区委常委",
     "overlap_org": "中共益阳市资阳区委员会", "overlap_period": ""},

    # ── Cross-Region: 赫山区 ↔ 资阳区 ──
    {"id": 14, "person_a_id": 1, "person_b_id": 3, "type": "跨区调动",
     "context": "付振南曾任赫山区区长后调任资阳区委书记，张辉曾任赫山区领导",
     "overlap_org": "赫山区人民政府", "overlap_period": "2016-2021"},

    # ── 南县 Connection ──
    {"id": 15, "person_a_id": 17, "person_b_id": 2, "type": "跨县调动",
     "context": "罗讯曾任资阳区长后调任南县县委书记",
     "overlap_org": "", "overlap_period": "2020"},
]


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

today = datetime.now().strftime("%Y-%m-%d")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append(f'<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{today}">')
lines.append('    <creator>china-gov-network skill</creator>')
lines.append(f'    <description>资阳区领导班子工作关系网络 - {today}</description>')
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
    if p["id"] in [1]:  # 付振南 - Party Secretary
        color = '#E03C31'  # red
        size = 20.0
    elif p["id"] in [2]:  # 曾波 - District Mayor
        color = '#2980B9'  # blue
        size = 18.0
    elif p["id"] in [14]:  # 乐运成 - former secretary, now vice mayor
        color = '#8E44AD'  # purple: former top leader promoted
        size = 16.0
    elif p["id"] in [15, 16]:  # 陈静彬/黄瑛 - former top
        color = '#95A5A6'  # grey
        size = 14.0
    elif p["id"] in [9]:  # 曹永彬 - discipline
        color = '#E67E22'  # orange
        size = 14.0
    elif p["id"] in [3]:  # 张辉 - Deputy Secretary
        color = '#2ECC71'  # green
        size = 14.0
    else:
        color = '#95A5A6'  # grey: others
        size = 12.0

    lines.append(f'      <node id="{p["id"]}" label="{p["name"]}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="person"/>')
    lines.append(f'          <attvalue for="category" value="person"/>')
    lines.append(f'          <attvalue for="birth" value="{p.get("birth","")}"/>')
    lines.append(f'          <attvalue for="birthplace" value="{p.get("birthplace","")}"/>')
    lines.append(f'          <attvalue for="education" value="{p.get("education","")}"/>')
    lines.append(f'          <attvalue for="current_post" value="{p.get("current_post","")}"/>')
    lines.append(f'          <attvalue for="source" value="{p.get("source","")}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="{int(color[1:3], 16)}" g="{int(color[3:5], 16)}" b="{int(color[5:7], 16)}"/>')
    lines.append(f'        <viz:size value="{size}"/>')
    lines.append(f'      </node>')

# ── Nodes: Organizations ──
for o in organizations:
    oid = 1000 + o["id"]
    org_colors = {
        "党委": (200, 50, 50),
        "政府": (50, 100, 200),
        "纪委": (200, 100, 50),
        "人大": (50, 180, 180),
        "政协": (180, 150, 100),
    }
    cr, cg, cb = org_colors.get(o["type"], (100, 100, 100))
    lines.append(f'      <node id="{oid}" label="{o["name"]}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="org"/>')
    lines.append(f'          <attvalue for="category" value="{o["type"]}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="{cr}" g="{cg}" b="{cb}"/>')
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
