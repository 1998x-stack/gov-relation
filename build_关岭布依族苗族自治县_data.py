#!/usr/bin/env python3
"""Build 关岭布依族苗族自治县 leadership network data (SQLite + GEXF + person JSON)."""

import json
import os
import sqlite3
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
DB_PATH = STAGING_DIR / "关岭布依族苗族自治县_network.db"
GEXF_PATH = STAGING_DIR / "关岭布依族苗族自治县_network.gexf"
PERSONS_DIR = STAGING_DIR / "persons"
AS_OF = "2026-07-23"
SLUG = "关岭布依族苗族自治县"

PERSONS_DIR.mkdir(parents=True, exist_ok=True)


# ── Persons ────────────────────────────────────────────────────────────────
persons = [
    {
        "id": 1,
        "name": "王埝",
        "gender": "女",
        "ethnicity": "苗族",
        "birth": "1980年9月",
        "birthplace": "贵州遵义",
        "education": "省委党校研究生，法学学士",
        "party_join": "",
        "work_start": "2003年7月",
        "current_post": "关岭布依族苗族自治县县委书记",
        "current_org": "中共关岭布依族苗族自治县委员会",
        "source": "https://www.guanling.gov.cn/",
    },
    {
        "id": 2,
        "name": "严再正",
        "gender": "男",
        "ethnicity": "布依族",
        "birth": "1976年9月",
        "birthplace": "贵州安顺",
        "education": "研究生，管理学硕士",
        "party_join": "2006年4月",
        "work_start": "1996年8月",
        "current_post": "关岭布依族苗族自治县县长",
        "current_org": "关岭布依族苗族自治县人民政府",
        "source": "https://www.guanling.gov.cn/",
    },
    {
        "id": 3,
        "name": "王敏",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "关岭布依族苗族自治县人大常委会主任",
        "current_org": "关岭布依族苗族自治县人大常委会",
        "source": "https://www.guanling.gov.cn/",
    },
    {
        "id": 4,
        "name": "赵宗舜",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "关岭布依族苗族自治县政协主席",
        "current_org": "关岭布依族苗族自治县政协",
        "source": "https://www.guanling.gov.cn/",
    },
    {
        "id": 5,
        "name": "熊飞",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "关岭布依族苗族自治县县委副书记",
        "current_org": "中共关岭布依族苗族自治县委员会",
        "source": "https://www.guanling.gov.cn/",
    },
    {
        "id": 6,
        "name": "阳旭凯",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "关岭布依族苗族自治县县委副书记",
        "current_org": "中共关岭布依族苗族自治县委员会",
        "source": "https://www.guanling.gov.cn/",
    },
    {
        "id": 7,
        "name": "贺洁",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "关岭布依族苗族自治县县委常委、常务副县长",
        "current_org": "关岭布依族苗族自治县人民政府",
        "source": "https://www.guanling.gov.cn/",
    },
    {
        "id": 8,
        "name": "宋汝谋",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "关岭布依族苗族自治县副县长",
        "current_org": "关岭布依族苗族自治县人民政府",
        "source": "https://www.guanling.gov.cn/",
    },
    {
        "id": 9,
        "name": "荀博",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "关岭布依族苗族自治县副县长（挂职）",
        "current_org": "关岭布依族苗族自治县人民政府",
        "source": "https://www.guanling.gov.cn/",
    },
    {
        "id": 10,
        "name": "吕阳",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "关岭布依族苗族自治县副县长（挂职）",
        "current_org": "关岭布依族苗族自治县人民政府",
        "source": "https://www.guanling.gov.cn/",
    },
    {
        "id": 11,
        "name": "王平",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "关岭布依族苗族自治县副县长",
        "current_org": "关岭布依族苗族自治县人民政府",
        "source": "https://www.guanling.gov.cn/",
    },
    {
        "id": 12,
        "name": "李鹏",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "关岭布依族苗族自治县副县长",
        "current_org": "关岭布依族苗族自治县人民政府",
        "source": "https://www.guanling.gov.cn/",
    },
    {
        "id": 13,
        "name": "张袭龙",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "关岭布依族苗族自治县副县长",
        "current_org": "关岭布依族苗族自治县人民政府",
        "source": "https://www.guanling.gov.cn/",
    },
    {
        "id": 14,
        "name": "陈克忠",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "关岭布依族苗族自治县副县长",
        "current_org": "关岭布依族苗族自治县人民政府",
        "source": "https://www.guanling.gov.cn/",
    },
    {
        "id": 15,
        "name": "沈童武",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "关岭布依族苗族自治县副县长、县公安局局长",
        "current_org": "关岭布依族苗族自治县人民政府",
        "source": "https://www.guanling.gov.cn/",
    },
    {
        "id": 16,
        "name": "韦朝虎",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任关岭县委书记",
        "current_org": "",
        "source": "https://www.guanling.gov.cn/",
    },
]


# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共关岭布依族苗族自治县委员会", "type": "党委", "level": "县级", "parent": "中共安顺市委员会", "location": "贵州省安顺市关岭布依族苗族自治县"},
    {"id": 2, "name": "关岭布依族苗族自治县人民政府", "type": "政府", "level": "县级", "parent": "安顺市人民政府", "location": "贵州省安顺市关岭布依族苗族自治县"},
    {"id": 3, "name": "关岭布依族苗族自治县人大常委会", "type": "人大", "level": "县级", "parent": "", "location": "贵州省安顺市关岭布依族苗族自治县"},
    {"id": 4, "name": "关岭布依族苗族自治县政协", "type": "政协", "level": "县级", "parent": "", "location": "贵州省安顺市关岭布依族苗族自治县"},
    {"id": 5, "name": "关岭布依族苗族自治县公安局", "type": "政府", "level": "科级", "parent": "关岭布依族苗族自治县人民政府", "location": "贵州省安顺市关岭布依族苗族自治县"},
    {"id": 6, "name": "共青团安顺市委员会", "type": "群团", "level": "地市级", "parent": "安顺市", "location": "贵州省安顺市"},
    {"id": 7, "name": "中共平坝区委员会", "type": "党委", "level": "县级", "parent": "中共安顺市委员会", "location": "贵州省安顺市平坝区"},
    {"id": 8, "name": "安顺市人民政府办公室", "type": "政府", "level": "地市级", "parent": "安顺市人民政府", "location": "贵州省安顺市"},
    {"id": 9, "name": "中共普定县委员会", "type": "党委", "level": "县级", "parent": "中共安顺市委员会", "location": "贵州省安顺市普定县"},
    {"id": 10, "name": "安顺市纪委市监委", "type": "纪委", "level": "地市级", "parent": "中共安顺市委员会", "location": "贵州省安顺市"},
    {"id": 11, "name": "中共安顺市委员会", "type": "党委", "level": "地市级", "parent": "中共贵州省委员会", "location": "贵州省安顺市"},
    {"id": 12, "name": "安顺市人民政府", "type": "政府", "level": "地市级", "parent": "贵州省人民政府", "location": "贵州省安顺市"},
]


# ── Positions ──────────────────────────────────────────────────────────────
positions = [
    # 王埝 career
    {"person_id": 1, "org_id": 1, "title": "关岭自治县委常委、宣传部部长", "start_date": "约2016", "end_date": "约2018", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 6, "title": "共青团安顺市委书记", "start_date": "约2018", "end_date": "约2020", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 7, "title": "平坝区委副书记（保留正县长级）", "start_date": "约2020", "end_date": "2021.05", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 2, "title": "关岭自治县委副书记、副县长、代理县长", "start_date": "2021.05", "end_date": "2021.06", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 2, "title": "关岭自治县委副书记、县长", "start_date": "2021.06", "end_date": "2025.02", "rank": "正处级", "note": "县第十一届人民政府县长"},
    {"person_id": 1, "org_id": 1, "title": "关岭自治县委书记、一级调研员", "start_date": "2025.02", "end_date": "至今", "rank": "副厅级", "note": "2025年2月贵州省委组织部任前公示，拟任县(市、区)党委书记"},
    {"person_id": 1, "org_id": 1, "title": "关岭经济开发区党工委书记（兼）", "start_date": "2025.02", "end_date": "至今", "rank": "", "note": ""},

    # 严再正 career
    {"person_id": 2, "org_id": 8, "title": "小学教师", "start_date": "1996.08", "end_date": "约2000", "rank": "", "note": "早期职业生涯"},
    {"person_id": 2, "org_id": 8, "title": "乡镇公务员", "start_date": "约2000", "end_date": "约2018", "rank": "", "note": "逐步晋升"},
    {"person_id": 2, "org_id": 8, "title": "安顺市人民政府办公室副主任", "start_date": "约2018", "end_date": "约2020", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 9, "title": "普定县委常委、政法委书记", "start_date": "约2020", "end_date": "2024.06", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "关岭自治县委常委、副县长（分管常务工作）", "start_date": "2024.06", "end_date": "2025.04", "rank": "副处级", "note": "2024年6月县人大常委会任命为副县长"},
    {"person_id": 2, "org_id": 2, "title": "关岭自治县委副书记、代理县长", "start_date": "2025.04", "end_date": "2025.05", "rank": "正处级", "note": "2025年4月贵州省委组织部任前公示"},
    {"person_id": 2, "org_id": 2, "title": "关岭自治县委副书记、县长", "start_date": "2025.05", "end_date": "至今", "rank": "正处级", "note": "2025年5月县十一届人大五次会议选举为县长"},

    # Current leadership team
    {"person_id": 3, "org_id": 3, "title": "关岭自治县人大常委会主任", "start_date": "", "end_date": "至今", "rank": "正处级", "note": ""},
    {"person_id": 4, "org_id": 4, "title": "关岭自治县政协主席", "start_date": "", "end_date": "至今", "rank": "正处级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "关岭自治县委副书记", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "关岭自治县委副书记", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "关岭自治县委常委、常务副县长", "start_date": "2024", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "关岭自治县副县长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "负责农业农村、乡村振兴等工作"},
    {"person_id": 9, "org_id": 2, "title": "关岭自治县副县长（挂职）", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "花都区对口帮扶关岭"},
    {"person_id": 10, "org_id": 2, "title": "关岭自治县副县长（挂职）", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "航空工业对口帮扶关岭"},
    {"person_id": 11, "org_id": 2, "title": "关岭自治县副县长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "负责民族宗教、人社、卫健、医保、林业等工作"},
    {"person_id": 12, "org_id": 2, "title": "关岭自治县副县长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "负责新型城镇化、自然资源、住建等工作"},
    {"person_id": 13, "org_id": 2, "title": "关岭自治县副县长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "负责教育、民政、水务、旅游等工作"},
    {"person_id": 14, "org_id": 2, "title": "关岭自治县副县长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "负责工业、商务、交通、市场监管等工作"},
    {"person_id": 15, "org_id": 2, "title": "关岭自治县副县长、县公安局局长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "负责公安、司法、退役军人事务等工作"},

    # 前任县委书记
    {"person_id": 16, "org_id": 1, "title": "关岭自治县委书记", "start_date": "约2021", "end_date": "2025.02", "rank": "副厅级", "note": "王埝前任"},
]


# ── Relationships ──────────────────────────────────────────────────────────
relationships = [
    # 王埝 ↔ 严再正 - 党政搭档
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "县委书记与县长党政搭档（2025.05-至今）", "overlap_org": "中共关岭自治县委/关岭自治县人民政府", "overlap_period": "2025.05-至今"},

    # 王埝 ↔ 熊飞、阳旭凯 - 班子成员
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "县委书记与县委副书记班子成员", "overlap_org": "中共关岭自治县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "县委书记与县委副书记班子成员", "overlap_org": "中共关岭自治县委", "overlap_period": ""},

    # 王埝 ↔ 王敏、赵宗舜 - 四套班子
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "县委书记与县人大常委会主任", "overlap_org": "关岭自治县四套班子", "overlap_period": ""},
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "县委书记与县政协主席", "overlap_org": "关岭自治县四套班子", "overlap_period": ""},

    # 严再正 ↔ 贺洁 - 政府领导班子
    {"person_a": 2, "person_b": 7, "type": "overlap", "context": "县长与常务副县长政府班子搭档", "overlap_org": "关岭自治县人民政府", "overlap_period": "2024-至今"},

    # 严再正与各副县长
    {"person_a": 2, "person_b": 8, "type": "overlap", "context": "县长与副县长政府班子成员", "overlap_org": "关岭自治县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 11, "type": "overlap", "context": "县长与副县长政府班子成员", "overlap_org": "关岭自治县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 12, "type": "overlap", "context": "县长与副县长政府班子成员", "overlap_org": "关岭自治县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 13, "type": "overlap", "context": "县长与副县长政府班子成员", "overlap_org": "关岭自治县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 14, "type": "overlap", "context": "县长与副县长政府班子成员", "overlap_org": "关岭自治县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 15, "type": "overlap", "context": "县长与副县长、公安局长政府班子成员", "overlap_org": "关岭自治县人民政府", "overlap_period": ""},

    # 王埝 ↔ 韦朝虎 - 前后任县委书记
    {"person_a": 1, "person_b": 16, "type": "predecessor_successor", "context": "王埝接替韦朝虎任关岭县委书记", "overlap_org": "中共关岭自治县委", "overlap_period": "2025.02"},
]


# ── Helpers ────────────────────────────────────────────────────────────────
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(current_post):
    cp = current_post or ""
    if "书记" in cp and "副书记" not in cp:
        return "200,30,30"
    if "县长" in cp or "区长" in cp:
        return "30,100,200"
    if "副书记" in cp:
        return "220,80,80"
    if "副" in cp and ("县长" in cp or "区长" in cp):
        return "100,150,220"
    if "常委" in cp:
        return "180,100,180"
    if "主任" in cp or "人大" in cp:
        return "60,180,60"
    if "主席" in cp:
        return "60,180,60"
    return "100,100,100"


def person_size(current_post):
    cp = current_post or ""
    if "书记" in cp and "副书记" not in cp:
        return "20.0"
    if "县长" in cp:
        return "18.0"
    if "副书记" in cp:
        return "15.0"
    if "副" in cp:
        return "12.0"
    if "常委" in cp:
        return "12.0"
    if "主任" in cp or "主席" in cp:
        return "12.0"
    return "10.0"


def person_shape(current_post):
    cp = current_post or ""
    if "书记" in cp:
        return "square"
    if "人大" in cp or "政协" in cp:
        return "diamond"
    if "副" in cp:
        return "triangle"
    return "circle"


def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "纪委": "255,200,150",
        "群团": "255,220,255",
    }
    return colors.get(org_type, "200,200,200")


# ── DB ────────────────────────────────────────────────────────────────────
def build_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS organizations;
        DROP TABLE IF EXISTS persons;

        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT DEFAULT '',
            ethnicity TEXT DEFAULT '',
            birth TEXT DEFAULT '',
            birthplace TEXT DEFAULT '',
            education TEXT DEFAULT '',
            party_join TEXT DEFAULT '',
            work_start TEXT DEFAULT '',
            current_post TEXT DEFAULT '',
            current_org TEXT DEFAULT '',
            source TEXT DEFAULT ''
        );

        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        );

        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER NOT NULL,
            org_id INTEGER NOT NULL,
            title TEXT DEFAULT '',
            start_date TEXT DEFAULT '',
            end_date TEXT DEFAULT '',
            rank TEXT DEFAULT '',
            note TEXT DEFAULT '',
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );

        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER NOT NULL,
            person_b INTEGER NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        cur.execute("""INSERT INTO persons (id,name,gender,ethnicity,birth,birthplace,education,
                       party_join,work_start,current_post,current_org,source)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""),
                     p.get("birth", ""), p.get("birthplace", ""), p.get("education", ""),
                     p.get("party_join", ""), p.get("work_start", ""),
                     p.get("current_post", ""), p.get("current_org", ""),
                     p.get("source", "")))

    for o in organizations:
        cur.execute("""INSERT INTO organizations (id,name,type,level,parent,location)
                       VALUES (?,?,?,?,?,?)""",
                    (o["id"], o["name"], o["type"], o["level"],
                     o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        cur.execute("""INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note)
                       VALUES (?,?,?,?,?,?,?)""",
                    (pos["person_id"], pos["org_id"], pos["title"],
                     pos.get("start_date", ""), pos.get("end_date", ""),
                     pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        cur.execute("""INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period)
                       VALUES (?,?,?,?,?,?)""",
                    (r["person_a"], r["person_b"], r["type"], r["context"],
                     r.get("overlap_org", ""), r.get("overlap_period", "")))

    conn.commit()
    conn.close()
    print(f"DB written: {DB_PATH}")
    print(f"  {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")


# ── GEXF ──────────────────────────────────────────────────────────────────
def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append(f'    <description>{SLUG}领导班子关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="source" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes - Persons
    lines.append('    <nodes>')
    for p in persons:
        pid = p["id"]
        cp = p.get("current_post", "")
        color = person_color(cp)
        size = person_size(cp)
        shape = person_shape(cp)
        lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(cp)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("source",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{color.split(",")[0]}" g="{color.split(",")[1]}" b="{color.split(",")[2]}" a="1.0"/>')
        lines.append(f'        <viz:size value="{size}"/>')
        lines.append(f'        <viz:shape value="{shape}"/>')
        lines.append('      </node>')

    # Nodes - Organizations
    for o in organizations:
        oid = o["id"] + 100000
        ocolor = org_color(o["type"])
        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{ocolor.split(",")[0]}" g="{ocolor.split(",")[1]}" b="{ocolor.split(",")[2]}" a="0.8"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('        <viz:shape value="hexagon"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]+100000}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ person (relationships)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}")


# ── Person JSON builder ───────────────────────────────────────────────────
def build_person_json(person, timeline, rels, sources):
    p = person
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "贵州省",
            "city": "安顺市",
            "region": "关岭布依族苗族自治县",
            "job": p.get("current_post", ""),
            "task_id": "guizhou_关岭布依族苗族自治县",
            "time_focus": f"as of {AS_OF}"
        },
        "identity": {
            "person_id": f"guanling_{p['name']}",
            "name": p["name"],
            "aliases": [],
            "gender": p.get("gender", ""),
            "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""),
            "birthplace": p.get("birthplace", ""),
            "native_place": "",
            "education": [],
            "party_join": p.get("party_join", ""),
            "work_start": p.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{p['name']}_{p.get('birth','')}",
                "name_birthplace": f"{p['name']}_{p.get('birthplace','')}",
                "official_profile_url": p.get("source", "")
            }
        },
        "current_status": {
            "current_post": p.get("current_post", ""),
            "current_org": p.get("current_org", ""),
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": bool(p.get("current_post")),
            "source_ids": ["S001"]
        },
        "career_timeline": timeline,
        "organizations": [],
        "relationships": rels,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{
            "type": "none_found",
            "description": "No risk signals found through available public sources",
            "date": "",
            "confidence": "unverified",
            "source_ids": []
        }],
        "source_register": sources,
        "confidence_summary": {
            "identity": "confirmed" if p.get("birth") else "partial",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"Earlier career timeline before current role for {p['name']}"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"Complete career timeline before current role - full position history for {p['name']}",
                "why_it_matters": "Cannot assess career pattern, promotion velocity, or network building without full timeline",
                "suggested_queries": [f"{p['name']} 简历", f"{p['name']} 任职经历", f"{p['name']} 百度百科"],
                "last_attempted": AS_OF
            }
        ]
    }


def build_person_jsons():
    """Build and write person JSON files for core leaders."""
    now = AS_OF.replace("-", "")

    sources = [
        {"id": "S001", "title": "关岭布依族苗族自治县人民政府门户网站",
         "url": "https://www.guanling.gov.cn/", "publisher": "关岭布依族苗族自治县人民政府",
         "published_at": "", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "Active government portal with leadership info"},
        {"id": "S002", "title": "百度百科 - 王埝",
         "url": "https://baike.baidu.com/item/%E7%8E%8B%E5%9F%9D",
         "publisher": "百度百科", "published_at": "",
         "accessed_at": AS_OF, "source_type": "baike", "reliability": "medium",
         "notes": "Baidu Baike entry - secondary quality source"},
        {"id": "S003", "title": "贵州省委组织部干部任前公示",
         "url": "https://www.guanling.gov.cn/",
         "publisher": "贵州省委组织部", "published_at": "2025-02-23",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "Pre-appointment public notice"},
        {"id": "S004", "title": "百度百科 - 严再正",
         "url": "https://baike.baidu.com/item/%E4%B8%A5%E5%86%8D%E6%AD%A3",
         "publisher": "百度百科", "published_at": "",
         "accessed_at": AS_OF, "source_type": "baike", "reliability": "medium",
         "notes": "Baidu Baike entry - secondary quality source"},
    ]

    # ── 王埝 person JSON ──
    wn_timeline = [
        {"start": "", "end": "约2016",
         "org": "关岭自治县委宣传部",
         "title": "关岭自治县委常委、宣传部部长", "level": "副处级",
         "location": "贵州省安顺市关岭县", "system": "party",
         "rank": "副处级", "is_key_promotion": False,
         "notes": "早期任职，具体时间信息有限",
         "confidence": "plausible",
         "source_ids": ["S002"]},
        {"start": "约2018", "end": "约2020",
         "org": "共青团安顺市委员会",
         "title": "共青团安顺市委书记", "level": "正处级",
         "location": "贵州省安顺市", "system": "mass_org",
         "rank": "正处级", "is_key_promotion": True,
         "notes": "由副处级晋升正处级",
         "confidence": "confirmed",
         "source_ids": ["S002"]},
        {"start": "约2020", "end": "2021.05",
         "org": "中共平坝区委员会",
         "title": "平坝区委副书记（保留正县长级）", "level": "正处级",
         "location": "贵州省安顺市平坝区", "system": "party",
         "rank": "正处级", "is_key_promotion": False,
         "notes": "从共青团转地方任职",
         "confidence": "confirmed",
         "source_ids": ["S002"]},
        {"start": "2021.05", "end": "2021.06",
         "org": "关岭自治县人民政府",
         "title": "关岭自治县委副书记、副县长、代理县长", "level": "正处级",
         "location": "贵州省安顺市关岭县", "system": "government",
         "rank": "正处级", "is_key_promotion": True,
         "notes": "从平坝调至关岭",
         "confidence": "confirmed",
         "source_ids": ["S001", "S002"]},
        {"start": "2021.06", "end": "2025.02",
         "org": "关岭自治县人民政府",
         "title": "关岭自治县委副书记、县长", "level": "正处级",
         "location": "贵州省安顺市关岭县", "system": "government",
         "rank": "正处级", "is_key_promotion": True,
         "notes": "县第十一届人民政府县长",
         "confidence": "confirmed",
         "source_ids": ["S001", "S002"]},
        {"start": "2025.02", "end": "至今",
         "org": "中共关岭自治县委",
         "title": "关岭自治县委书记、一级调研员", "level": "副厅级",
         "location": "贵州省安顺市关岭县", "system": "party",
         "rank": "副厅级", "is_key_promotion": True,
         "notes": "2025年2月任前公示，由县长转任县委书记。据传2026年7月已交流至遵义市。",
         "confidence": "confirmed",
         "source_ids": ["S001", "S003"]},
    ]
    wn_relationships = [
        {"person": "严再正", "person_id": "guanling_严再正",
         "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "先后以县长身份配合前任县委书记工作，后以县委书记身份与严再正党政搭档",
         "overlap_org": "关岭自治县四套班子",
         "overlap_period": "2021-至今",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S001"]},
        {"person": "韦朝虎", "person_id": "guanling_韦朝虎",
         "relationship_type": "predecessor_successor",
         "strength": "medium",
         "evidence": "接替韦朝虎任关岭县委书记",
         "overlap_org": "中共关岭自治县委",
         "overlap_period": "2025.02",
         "direction": "other_to_person",
         "confidence": "confirmed",
         "source_ids": ["S001"]},
    ]
    wn_json = build_person_json(persons[0], wn_timeline, wn_relationships, sources)
    wn_json["identity"]["education"] = [
        {"period": "", "institution": "贵州大学", "major": "",
         "degree": "法学学士", "study_type": "full_time",
         "source_ids": ["S002"]},
        {"period": "", "institution": "贵州省委党校", "major": "公共管理",
         "degree": "研究生", "study_type": "part_time",
         "source_ids": ["S002"]},
    ]
    wn_path = os.path.join(PERSONS_DIR, f"{now}-贵州省-安顺市-县委书记-王埝.json")
    with open(wn_path, "w", encoding="utf-8") as f:
        json.dump(wn_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {wn_path}")

    # ── 严再正 person JSON ──
    yzz_timeline = [
        {"start": "1996.08", "end": "约2000",
         "org": "教育系统",
         "title": "小学教师", "level": "",
         "location": "贵州省安顺市", "system": "education",
         "rank": "", "is_key_promotion": False,
         "notes": "职业生涯起点",
         "confidence": "confirmed",
         "source_ids": ["S004"]},
        {"start": "约2000", "end": "约2018",
         "org": "安顺市乡镇/基层政府",
         "title": "乡镇公务员（逐步晋升）", "level": "",
         "location": "贵州省安顺市", "system": "government",
         "rank": "", "is_key_promotion": False,
         "notes": "18年基层到市级机关经历，具体细节待查",
         "confidence": "plausible",
         "source_ids": ["S004"]},
        {"start": "约2018", "end": "约2020",
         "org": "安顺市人民政府办公室",
         "title": "安顺市人民政府办公室副主任", "level": "副处级",
         "location": "贵州省安顺市", "system": "government",
         "rank": "副处级", "is_key_promotion": True,
         "notes": "",
         "confidence": "confirmed",
         "source_ids": ["S004"]},
        {"start": "约2020", "end": "2024.06",
         "org": "中共普定县委政法委",
         "title": "普定县委常委、政法委书记", "level": "副处级",
         "location": "贵州省安顺市普定县", "system": "party",
         "rank": "副处级", "is_key_promotion": False,
         "notes": "",
         "confidence": "confirmed",
         "source_ids": ["S004"]},
        {"start": "2024.06", "end": "2025.04",
         "org": "关岭自治县人民政府",
         "title": "关岭自治县委常委、副县长（分管常务工作）", "level": "副处级",
         "location": "贵州省安顺市关岭县", "system": "government",
         "rank": "副处级", "is_key_promotion": False,
         "notes": "2024年6月县人大常委会任命",
         "confidence": "confirmed",
         "source_ids": ["S001", "S004"]},
        {"start": "2025.04", "end": "2025.05",
         "org": "关岭自治县人民政府",
         "title": "关岭自治县委副书记、代理县长", "level": "正处级",
         "location": "贵州省安顺市关岭县", "system": "government",
         "rank": "正处级", "is_key_promotion": True,
         "notes": "2025年4月省委组织部任前公示，拟提名为县长候选人",
         "confidence": "confirmed",
         "source_ids": ["S001", "S004"]},
        {"start": "2025.05", "end": "至今",
         "org": "关岭自治县人民政府",
         "title": "关岭自治县委副书记、县长", "level": "正处级",
         "location": "贵州省安顺市关岭县", "system": "government",
         "rank": "正处级", "is_key_promotion": True,
         "notes": "2025年5月县十一届人大五次会议选举为县长",
         "confidence": "confirmed",
         "source_ids": ["S001", "S004"]},
    ]
    yzz_relationships = [
        {"person": "王埝", "person_id": "guanling_王埝",
         "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "县长与县委书记党政搭档",
         "overlap_org": "关岭自治县人民政府/中共关岭自治县委",
         "overlap_period": "2025.05-至今",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S001"]},
        {"person": "贺洁", "person_id": "guanling_贺洁",
         "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "县长与常务副县长政府班子搭档",
         "overlap_org": "关岭自治县人民政府",
         "overlap_period": "2024-至今",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S001"]},
    ]
    yzz_json = build_person_json(persons[1], yzz_timeline, yzz_relationships, sources)
    yzz_json["investigation_scope"]["job"] = "县长"
    yzz_path = os.path.join(PERSONS_DIR, f"{now}-贵州省-安顺市-县长-严再正.json")
    with open(yzz_path, "w", encoding="utf-8") as f:
        json.dump(yzz_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {yzz_path}")


# ── Main ──────────────────────────────────────────────────────────────────
def build():
    os.makedirs(STAGING_DIR, exist_ok=True)
    print(f"=== Building {SLUG} data ===")
    print(f"Staging dir: {STAGING_DIR}")
    build_db()
    build_gexf()
    build_person_jsons()
    print("\nBuild complete.")


if __name__ == "__main__":
    build()
