#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 凤凰县 leadership network."""

import sqlite3
import os
import sys
from datetime import datetime

# ── Paths ─────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
# If running from staging, the db/gexf should go to staging
# We detect if we're in data/tmp/xxx or in repo root
if "/data/tmp/" in BASE:
    # Running from staging directory
    pass
else:
    BASE = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE, "凤凰县_network.db")
GEXF_PATH = os.path.join(BASE, "凤凰县_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Top Leader: 县委书记 ──
    {
        "id": 1,
        "name": "樊忠清",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "1975-10",
        "birthplace": "湖南省花垣县",
        "education": "中央党校函授学院本科班法律专业",
        "party_join": "1997-12",
        "work_start": "1996-09",
        "current_post": "凤凰县委书记",
        "current_org": "中共凤凰县委员会",
        "source": "https://baike.baidu.com/item/%E6%A8%8A%E5%BF%A0%E6%B8%85/14075483"
    },
    # ── Former Top Leader: 原县委书记（另有任用）──
    {
        "id": 2,
        "name": "毛家",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1973-10",
        "birthplace": "湖南省永顺县",
        "education": "中南林学院林学专业",
        "party_join": "1996-04",
        "work_start": "1996-07",
        "current_post": "凤凰县委原书记（另有任用）",
        "current_org": "中共凤凰县委员会",
        "source": "https://baike.baidu.com/item/%E6%AF%9B%E5%AE%B6/9526626"
    },
    # ── 县人大常委会主任 ──
    {
        "id": 3,
        "name": "龙金明",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "1966-03",
        "birthplace": "湖南省凤凰县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "凤凰县人大常委会主任",
        "current_org": "凤凰县人民代表大会常务委员会",
        "source": "https://zh.wikipedia.org/wiki/%E5%87%A4%E5%87%B0%E5%8E%BF"
    },
    # ── 县政协主席 ──
    {
        "id": 4,
        "name": "田儒勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968-10",
        "birthplace": "湖南省凤凰县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "凤凰县政协主席",
        "current_org": "中国人民政治协商会议凤凰县委员会",
        "source": "https://zh.wikipedia.org/wiki/%E5%87%A4%E5%87%B0%E5%8E%BF"
    },
    # ── Predecessor: 毛家的前任县委书记（2016-2021）──
    {
        "id": 5,
        "name": "颜长文",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "曾任凤凰县委书记（2016-2021）",
        "current_org": "中共凤凰县委员会",
        "source": ""
    },
    # ── 常务副县长（待补充）──
    {
        "id": 6,
        "name": "田建新",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "凤凰县委常委、常务副县长",
        "current_org": "凤凰县人民政府",
        "source": ""
    },
    # ── 县纪委书记 ──
    {
        "id": 7,
        "name": "谢军",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "凤凰县委常委、县纪委书记",
        "current_org": "中共凤凰县纪律检查委员会",
        "source": ""
    },
    # ── 县委副书记（协助党建）──
    {
        "id": 8,
        "name": "贾明俊",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "凤凰县委副书记",
        "current_org": "中共凤凰县委员会",
        "source": ""
    },
    # ── 县委政法委书记 ──
    {
        "id": 9,
        "name": "龙志勇",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "凤凰县委常委、政法委书记",
        "current_org": "中共凤凰县委员会",
        "source": ""
    },
    # ── 县委组织部部长 ──
    {
        "id": 10,
        "name": "林艳",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "凤凰县委常委、组织部部长",
        "current_org": "中共凤凰县委员会",
        "source": ""
    },
    # ── 县委宣传部部长 ──
    {
        "id": 11,
        "name": "龙仙会",
        "gender": "女",
        "ethnicity": "苗族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "凤凰县委常委、宣传部部长",
        "current_org": "中共凤凰县委员会",
        "source": ""
    },
    # ── 县委统战部部长 ──
    {
        "id": 12,
        "name": "黄武才",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "凤凰县委常委、统战部部长",
        "current_org": "中共凤凰县委员会",
        "source": ""
    },
    # ── 县委办主任 ──
    {
        "id": 13,
        "name": "杨波",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "凤凰县委常委、县委办公室主任",
        "current_org": "中共凤凰县委员会",
        "source": ""
    },
]

organizations = [
    {"id": 1, "name": "中共凤凰县委员会", "type": "county_party", "level": "county", "parent": "中共湘西土家族苗族自治州委员会", "location": "凤凰县"},
    {"id": 2, "name": "凤凰县人民政府", "type": "county_gov", "level": "county", "parent": "湘西土家族苗族自治州人民政府", "location": "凤凰县"},
    {"id": 3, "name": "凤凰县人民代表大会常务委员会", "type": "npc", "level": "county", "parent": "湘西土家族苗族自治州人大常委会", "location": "凤凰县"},
    {"id": 4, "name": "中国人民政治协商会议凤凰县委员会", "type": "cppcc", "level": "county", "parent": "政协湘西土家族苗族自治州委员会", "location": "凤凰县"},
    {"id": 5, "name": "中共凤凰县纪律检查委员会", "type": "discipline", "level": "county", "parent": "中共湘西土家族苗族自治州纪律检查委员会", "location": "凤凰县"},
    {"id": 6, "name": "中共凤凰县委政法委员会", "type": "party", "level": "county", "parent": "中共凤凰县委员会", "location": "凤凰县"},
    {"id": 7, "name": "中共凤凰县委组织部", "type": "party", "level": "county", "parent": "中共凤凰县委员会", "location": "凤凰县"},
    {"id": 8, "name": "中共凤凰县委宣传部", "type": "party", "level": "county", "parent": "中共凤凰县委员会", "location": "凤凰县"},
    {"id": 9, "name": "中共凤凰县委统战部", "type": "party", "level": "county", "parent": "中共凤凰县委员会", "location": "凤凰县"},
    {"id": 10, "name": "中共凤凰县委办公室", "type": "party", "level": "county", "parent": "中共凤凰县委员会", "location": "凤凰县"},
    {"id": 11, "name": "共青团湘西土家族苗族自治州委员会", "type": "mass_org", "level": "prefecture", "parent": "湘西土家族苗族自治州", "location": "湘西州"},
    {"id": 12, "name": "湘西土家族苗族自治州总工会", "type": "mass_org", "level": "prefecture", "parent": "湘西土家族苗族自治州", "location": "湘西州"},
    {"id": 13, "name": "湘西州生态环境局", "type": "gov_dept", "level": "prefecture", "parent": "湘西土家族苗族自治州人民政府", "location": "湘西州"},
    {"id": 14, "name": "泸溪县人民政府", "type": "county_gov", "level": "county", "parent": "湘西土家族苗族自治州人民政府", "location": "泸溪县"},
    {"id": 15, "name": "古丈县人民政府", "type": "county_gov", "level": "county", "parent": "湘西土家族苗族自治州人民政府", "location": "古丈县"},
    {"id": 16, "name": "花垣县人民政府", "type": "county_gov", "level": "county", "parent": "湘西土家族苗族自治州人民政府", "location": "花垣县"},
    {"id": 17, "name": "中共花垣县委员会", "type": "county_party", "level": "county", "parent": "中共湘西土家族苗族自治州委员会", "location": "花垣县"},
    {"id": 18, "name": "花垣县道二乡人民政府", "type": "township", "level": "township", "parent": "花垣县人民政府", "location": "花垣县"},
    {"id": 19, "name": "花垣县大河坪乡人民政府", "type": "township", "level": "township", "parent": "花垣县人民政府", "location": "花垣县"},
    {"id": 20, "name": "花垣县吉卫镇人民政府", "type": "township", "level": "township", "parent": "花垣县人民政府", "location": "花垣县"},
    {"id": 21, "name": "古丈县高望界林场", "type": "institution", "level": "county", "parent": "古丈县人民政府", "location": "古丈县"},
    {"id": 22, "name": "中共古丈县委员会", "type": "county_party", "level": "county", "parent": "中共湘西土家族苗族自治州委员会", "location": "古丈县"},
    {"id": 23, "name": "中共花垣县委办公室", "type": "party", "level": "county", "parent": "中共花垣县委员会", "location": "花垣县"},
]

positions = [
    # ── 樊忠清 ──
    {"person_id": 1, "org_id": 1, "title": "凤凰县委书记", "start": "2026-07", "end": "present", "rank": "正处级", "note": "2026年7月2日任凤凰县委书记"},
    {"person_id": 1, "org_id": 2, "title": "凤凰县人民政府县长", "start": "2022-03", "end": "2026-07", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 2, "title": "凤凰县委副书记、代理县长", "start": "2022-02", "end": "2022-03", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 2, "title": "湘西州政府办党组成员、三级调研员", "start": "2021-09", "end": "2022-02", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 22, "title": "古丈县委副书记、三级调研员", "start": "2020-05", "end": "2021-09", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 22, "title": "古丈县委副书记", "start": "2016-09", "end": "2020-05", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 15, "title": "古丈县委常委、常务副县长", "start": "2013-07", "end": "2016-09", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 5, "title": "泸溪县委常委、县纪委书记", "start": "2010-04", "end": "2013-07", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 5, "title": "湘西州纪委行政效能监察室主任", "start": "2006-12", "end": "2010-04", "rank": "正科级", "note": ""},
    {"person_id": 1, "org_id": 5, "title": "湘西州纪委正科级干部", "start": "2006-06", "end": "2006-12", "rank": "正科级", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "花垣县委办公室副主任（正科级）", "start": "2006-04", "end": "2006-06", "rank": "正科级", "note": ""},
    {"person_id": 1, "org_id": 20, "title": "花垣县吉卫镇党委书记", "start": "2004-05", "end": "2006-04", "rank": "正科级", "note": ""},
    {"person_id": 1, "org_id": 19, "title": "花垣县大河坪乡党委书记", "start": "2001-02", "end": "2004-05", "rank": "正科级", "note": ""},
    {"person_id": 1, "org_id": 23, "title": "花垣县委办公室副主任科员", "start": "2000-02", "end": "2001-02", "rank": "副科级", "note": ""},
    {"person_id": 1, "org_id": 23, "title": "花垣县委办公室干部", "start": "1999-06", "end": "2000-02", "rank": "科员", "note": ""},
    {"person_id": 1, "org_id": 17, "title": "花垣县委机要科干部", "start": "1998-04", "end": "1999-06", "rank": "科员", "note": ""},
    {"person_id": 1, "org_id": 18, "title": "花垣县道二乡农经站干部", "start": "1996-09", "end": "1998-04", "rank": "科员", "note": ""},
    # ── 毛家 ──
    {"person_id": 2, "org_id": 1, "title": "凤凰县委书记", "start": "2022-01", "end": "2026-07", "rank": "正处级", "note": "2026年7月2日免职，另有任用"},
    {"person_id": 2, "org_id": 13, "title": "湘西州生态环境局党组书记、局长", "start": "2020-04", "end": "2022-01", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 14, "title": "泸溪县委常委、常务副县长", "start": "2013-08", "end": "2020-04", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 14, "title": "泸溪县委常委、副县长、统战部部长", "start": "2011-06", "end": "2013-08", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 14, "title": "泸溪县委常委、副县长", "start": "2010-07", "end": "2011-06", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 12, "title": "湘西州总工会副主席、党组成员", "start": "2006-12", "end": "2010-07", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 12, "title": "湘西州总工会办公室主任", "start": "2006-03", "end": "2006-12", "rank": "正科级", "note": ""},
    {"person_id": 2, "org_id": 11, "title": "团湘西州委青工青农部部长", "start": "2000-09", "end": "2006-03", "rank": "正科级", "note": ""},
    {"person_id": 2, "org_id": 11, "title": "团湘西州委青工青农部副部长", "start": "1999-11", "end": "2000-09", "rank": "副科级", "note": ""},
    {"person_id": 2, "org_id": 22, "title": "古丈团县委副书记", "start": "1998-04", "end": "1999-11", "rank": "副科级", "note": ""},
    {"person_id": 2, "org_id": 21, "title": "古丈县高望界林场工作", "start": "1996-07", "end": "1998-04", "rank": "科员", "note": ""},
    # ── 龙金明 ──
    {"person_id": 3, "org_id": 3, "title": "凤凰县人大常委会主任", "start": "2024-02", "end": "present", "rank": "正处级", "note": ""},
    # ── 田儒勇 ──
    {"person_id": 4, "org_id": 4, "title": "凤凰县政协主席", "start": "2021-10", "end": "present", "rank": "正处级", "note": ""},
    # ── 颜长文 ──
    {"person_id": 5, "org_id": 1, "title": "凤凰县委书记", "start": "2016", "end": "2021-12", "rank": "正处级", "note": "毛家的前任"},
    # ── 田建新 ──
    {"person_id": 6, "org_id": 2, "title": "凤凰县委常委、常务副县长", "start": "", "end": "", "rank": "副处级", "note": "待补充详细履历"},
    # ── 谢军 ──
    {"person_id": 7, "org_id": 5, "title": "凤凰县委常委、县纪委书记", "start": "", "end": "", "rank": "副处级", "note": "待补充详细履历"},
    # ── 贾明俊 ──
    {"person_id": 8, "org_id": 1, "title": "凤凰县委副书记", "start": "", "end": "", "rank": "副处级", "note": "待补充详细履历"},
    # ── 龙志勇 ──
    {"person_id": 9, "org_id": 6, "title": "凤凰县委常委、政法委书记", "start": "", "end": "", "rank": "副处级", "note": "待补充详细履历"},
    # ── 林艳 ──
    {"person_id": 10, "org_id": 7, "title": "凤凰县委常委、组织部部长", "start": "", "end": "", "rank": "副处级", "note": "待补充详细履历"},
    # ── 龙仙会 ──
    {"person_id": 11, "org_id": 8, "title": "凤凰县委常委、宣传部部长", "start": "", "end": "", "rank": "副处级", "note": "待补充详细履历"},
    # ── 黄武才 ──
    {"person_id": 12, "org_id": 9, "title": "凤凰县委常委、统战部部长", "start": "", "end": "", "rank": "副处级", "note": "待补充详细履历"},
    # ── 杨波 ──
    {"person_id": 13, "org_id": 10, "title": "凤凰县委常委、县委办公室主任", "start": "", "end": "", "rank": "副处级", "note": "待补充详细履历"},
]

relationships = [
    # ── 樊忠清 ↔ 毛家（前后任书记）──
    {"id": 1, "person_a": 1, "person_b": 2, "type": "predecessor_successor",
     "context": "樊忠清接替毛家任凤凰县委书记，毛家另有任用",
     "overlap_org": "中共凤凰县委员会",
     "overlap_period": "2022.01-2022.02（短暂交接期）"},
    # ── 樊忠清 ↔ 毛家（搭班合作）──
    {"id": 2, "person_a": 1, "person_b": 2, "type": "colleague",
     "context": "樊忠清任凤凰县长期间与毛家（县委书记）搭班约4年5个月",
     "overlap_org": "凤凰县",
     "overlap_period": "2022.03-2026.07"},
    # ── 樊忠清 ↔ 龙金明 ──
    {"id": 3, "person_a": 1, "person_b": 3, "type": "colleague",
     "context": "县四套班子主要领导",
     "overlap_org": "凤凰县",
     "overlap_period": "2022.03-present"},
    # ── 樊忠清 ↔ 田儒勇 ──
    {"id": 4, "person_a": 1, "person_b": 4, "type": "colleague",
     "context": "县四套班子主要领导",
     "overlap_org": "凤凰县",
     "overlap_period": "2022.03-present"},
    # ── 毛家 ↔ 颜长文（前后任书记）──
    {"id": 5, "person_a": 2, "person_b": 5, "type": "predecessor_successor",
     "context": "毛家接替颜长文任凤凰县委书记",
     "overlap_org": "中共凤凰县委员会",
     "overlap_period": "2022.01"},
    # ── 樊忠清 ↔ 龙志勇（委政法委）──
    {"id": 6, "person_a": 1, "person_b": 9, "type": "colleague",
     "context": "县委常委班子",
     "overlap_org": "中共凤凰县委员会",
     "overlap_period": ""},
    # ── 毛家 ↔ 龙志勇 ──
    {"id": 7, "person_a": 2, "person_b": 9, "type": "colleague",
     "context": "县委常委班子",
     "overlap_org": "中共凤凰县委员会",
     "overlap_period": "2022.01-2026.07"},
    # ── 樊忠清 ↔ 田建新（县政府班子）──
    {"id": 8, "person_a": 1, "person_b": 6, "type": "superior_subordinate",
     "context": "樊忠清（原县长）与常务副县长搭班",
     "overlap_org": "凤凰县人民政府",
     "overlap_period": "2022.03-2026.07"},
]

# ── SQLITE BUILD ──────────────────────────────────────────────────────

def build_db():
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
            id INTEGER PRIMARY KEY,
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
        cur.execute(
            "INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
             p["birthplace"], p["education"], p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"])
        )

    for o in organizations:
        cur.execute(
            "INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"])
        )

    for pos in positions:
        cur.execute(
            "INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)",
            (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"])
        )

    for r in relationships:
        cur.execute(
            "INSERT OR REPLACE INTO relationships VALUES (?,?,?,?,?,?,?)",
            (r["id"], r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"])
        )

    conn.commit()
    conn.close()
    print(f"✅ Database created: {DB_PATH}")


# ── GEXF BUILD ────────────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Return r,g,b string based on role."""
    role = p.get("current_post", "")
    if "县委书记" in role:
        if "原" in role:
            return "200,50,50"   # Darker red for former
        return "255,50,50"       # Red for party secretary
    if "县长" in role or "副县长" in role:
        return "50,100,255"      # Blue for government
    if "纪委书记" in role or "纪委" in role:
        return "255,165,0"       # Orange for discipline
    if "人大常委会主任" in role:
        return "200,255,255"     # Cyan for NPC
    if "政协主席" in role:
        return "255,240,200"     # Cream for CPPCC
    return "100,100,100"         # Grey for others

def is_top_leader(p):
    role = p.get("current_post", "")
    return "县委书记" in role and "原" not in role

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>China Gov Network Research Agent</creator>')
    lines.append('    <description>凤凰县领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="birthplace" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')

    # Person nodes
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("birthplace",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    org_colors = {
        "county_party": "255,200,200",
        "county_gov": "200,200,255",
        "npc": "200,255,255",
        "cppcc": "255,240,200",
        "discipline": "255,220,200",
        "party": "255,230,230",
        "mass_org": "255,220,255",
        "township": "255,255,200",
        "institution": "220,220,220",
        "gov_dept": "200,200,255",
    }
    for o in organizations:
        c = org_colors.get(o["type"], "200,200,200")
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o.get("level",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → Organization (worked_at) for current positions
    current_positions = [pos for pos in positions if pos["end"] in ("present", "")]
    for pos in current_positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationship)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ GEXF created: {GEXF_PATH}")


# ── MAIN ──────────────────────────────────────────────────────────────

def print_stats():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    tables = ["persons", "organizations", "positions", "relationships"]
    for t in tables:
        cur.execute(f"SELECT COUNT(*) FROM {t}")
        cnt = cur.fetchone()[0]
        print(f"  {t}: {cnt}")
    conn.close()


if __name__ == "__main__":
    build_db()
    build_gexf()
    print("\n📊 Database summary:")
    print_stats()
    print("\nDone.")
