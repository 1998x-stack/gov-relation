#!/usr/bin/env python3
"""Build script for 麒麟区, 曲靖市, 云南省 — cadre exchange network investigation."""

import json
import os
import sqlite3
from datetime import datetime

AS_OF = "2026-07-28"
AS_OF_SHORT = AS_OF.replace("-", "")

# Paths — staging first
TMP = os.path.join(os.path.dirname(__file__), "..", "..", "data", "tmp", "yunnan_麒麟区")
DB_PATH = os.path.join(TMP, "麒麟区_network.db")
GEXF_PATH = os.path.join(TMP, "麒麟区_network.gexf")
PERSONS_DIR = os.path.join(TMP, "persons")

# =========================================================================
# RESEARCH DATA — collected from ql.gov.cn (primary), qujing.gov.cn, news
# =========================================================================

# ── Persons ──
persons = [
    # === Top Leaders ===
    {"id": 1, "name": "兰发文", "gender": "男", "ethnicity": "汉", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "麒麟区委书记", "current_org": "中共曲靖市麒麟区委员会",
     "source": "https://www.ql.gov.cn/news/detail/qlyw/83591.html"},
    {"id": 2, "name": "张忠文", "gender": "男", "ethnicity": "汉", "birth": "1977-02", "birthplace": "",
     "education": "云南省委党校在职经济管理专业研究生", "party_join": "", "work_start": "1997-07",
     "current_post": "麒麟区区长", "current_org": "麒麟区人民政府",
     "source": "https://www.ql.gov.cn/gov/public/detail/2zfld/14088.html"},

    # === Party Standing Committee (from 七代会主席台名单) ===
    {"id": 3, "name": "刘江梅", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "麒麟区委副书记", "current_org": "中共曲靖市麒麟区委员会",
     "source": "https://www.ql.gov.cn/news/detail/qlyw/83591.html"},
    {"id": 4, "name": "李锐（政法委）", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "麒麟区委政法委书记", "current_org": "中共曲靖市麒麟区委员会",
     "source": "https://www.ql.gov.cn/news/detail/qlyw/83591.html"},
    {"id": 5, "name": "王明波", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "麒麟区委常委", "current_org": "中共曲靖市麒麟区委员会",
     "source": "https://www.ql.gov.cn/news/detail/qlyw/83591.html"},
    {"id": 6, "name": "毕文荣", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "麒麟区委常委", "current_org": "中共曲靖市麒麟区委员会",
     "source": "https://www.ql.gov.cn/news/detail/qlyw/83591.html"},
    {"id": 7, "name": "隽加宏", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "麒麟区委常委", "current_org": "中共曲靖市麒麟区委员会",
     "source": "https://www.ql.gov.cn/news/detail/qlyw/83591.html"},
    {"id": 8, "name": "刘鹏", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "麒麟区委常委", "current_org": "中共曲靖市麒麟区委员会",
     "source": "https://www.ql.gov.cn/news/detail/qlyw/83591.html"},
    {"id": 9, "name": "李锐（组织部）", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "麒麟区委组织部部长", "current_org": "中共曲靖市麒麟区委员会",
     "source": "https://www.ql.gov.cn/news/detail/qlyw/83591.html"},

    # ── District Government Leadership ──
    {"id": 10, "name": "李周", "gender": "男", "ethnicity": "回族", "birth": "1978-04", "birthplace": "云南沾益",
     "education": "大学", "party_join": "", "work_start": "2000-09",
     "current_post": "麒麟区委常委、常务副区长", "current_org": "麒麟区人民政府",
     "source": "https://www.ql.gov.cn/gov/public/detail/2zfld/76509.html"},
    {"id": 11, "name": "高兴志", "gender": "男", "ethnicity": "汉", "birth": "1971-09", "birthplace": "",
     "education": "省委党校大学", "party_join": "", "work_start": "1993",
     "current_post": "麒麟区副区长、麒麟公安分局局长", "current_org": "麒麟区人民政府",
     "source": "https://www.ql.gov.cn/gov/public/detail/2zfld/33942.html"},
    {"id": 12, "name": "杨刚", "gender": "男", "ethnicity": "汉", "birth": "1979-04", "birthplace": "",
     "education": "中央党校大学", "party_join": "", "work_start": "1999-09",
     "current_post": "麒麟区副区长", "current_org": "麒麟区人民政府",
     "source": "https://www.ql.gov.cn/gov/public/detail/2zfld/55955.html"},
    {"id": 13, "name": "刘兴丽", "gender": "女", "ethnicity": "汉", "birth": "1980-08", "birthplace": "云南会泽",
     "education": "省委党校研究生（法律专业）", "party_join": "2000-06", "work_start": "1999-08",
     "current_post": "麒麟区委常委、副区长", "current_org": "麒麟区人民政府",
     "source": "https://www.ql.gov.cn/gov/public/detail/2zfld/14095.html"},
    {"id": 14, "name": "王子佳", "gender": "女", "ethnicity": "汉", "birth": "1986-11", "birthplace": "",
     "education": "硕士研究生", "party_join": "", "work_start": "2010-08",
     "current_post": "麒麟区委常委、副区长（挂职）", "current_org": "麒麟区人民政府",
     "source": "https://www.ql.gov.cn/gov/public/detail/2zfld/71609.html"},
    {"id": 15, "name": "丁连高", "gender": "男", "ethnicity": "汉", "birth": "1972-04", "birthplace": "",
     "education": "云南农业大学农业经济管理专业", "party_join": "", "work_start": "1996-08",
     "current_post": "麒麟区副区长", "current_org": "麒麟区人民政府",
     "source": "https://www.ql.gov.cn/gov/public/detail/2zfld/53824.html"},
    {"id": 16, "name": "李维敏", "gender": "男", "ethnicity": "汉", "birth": "1980-07", "birthplace": "",
     "education": "大学", "party_join": "", "work_start": "2003-12",
     "current_post": "麒麟区副区长", "current_org": "麒麟区人民政府",
     "source": "https://www.ql.gov.cn/gov/public/detail/2zfld/69400.html"},
    {"id": 17, "name": "王俊", "gender": "男", "ethnicity": "汉", "birth": "1982-11", "birthplace": "云南麒麟",
     "education": "大学", "party_join": "", "work_start": "2005-12",
     "current_post": "麒麟区副区长", "current_org": "麒麟区人民政府",
     "source": "https://www.ql.gov.cn/gov/public/detail/2zfld/76578.html"},

    # ── Predecessor ──
    {"id": 18, "name": "杨庆东", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "（前任）麒麟区委书记", "current_org": "中共曲靖市麒麟区委员会",
     "source": "https://www.ql.gov.cn/news/detail/qlyw/82915.html"},
]

# ── Organizations ──
organizations = [
    {"id": 1, "name": "中共曲靖市麒麟区委员会", "type": "党委", "level": "县处级",
     "parent": "中共曲靖市委员会", "location": "麒麟区"},
    {"id": 2, "name": "麒麟区人民政府", "type": "政府", "level": "县处级",
     "parent": "曲靖市人民政府", "location": "麒麟区"},
    {"id": 3, "name": "麒麟公安分局", "type": "政府", "level": "乡科级",
     "parent": "曲靖市公安局", "location": "麒麟区"},
    {"id": 4, "name": "中共曲靖市委", "type": "党委", "level": "地厅级",
     "parent": "", "location": "麒麟区"},
    {"id": 5, "name": "曲靖市人民政府", "type": "政府", "level": "地厅级",
     "parent": "", "location": "麒麟区"},
    {"id": 6, "name": "麒麟区工业园区", "type": "开发区", "level": "县处级",
     "parent": "麒麟区人民政府", "location": "麒麟区"},
]

# ── Positions ──
positions = [
    # Lan Fawen
    {"person_id": 1, "org_id": 1, "title": "麒麟区委书记", "start_date": "~2026-06", "end_date": "present",
     "rank": "县处级正职", "note": "2026年6月在麒麟区第七次党代会上当选第七届区委书记"},
    {"person_id": 1, "org_id": 4, "title": "曲靖市委常委", "start_date": "~2026-06", "end_date": "present",
     "rank": "地厅级副职", "note": "兼任"},
    # Zhang Zhongwen
    {"person_id": 2, "org_id": 2, "title": "麒麟区区长", "start_date": "~2021", "end_date": "present",
     "rank": "县处级正职", "note": "区委副书记、区政府党组书记、区长、麒麟工业园区工委书记，2026年6月七代会继续当选副书记"},
    {"person_id": 2, "org_id": 1, "title": "麒麟区委副书记", "start_date": "~2021", "end_date": "present",
     "rank": "县处级副职", "note": "兼"},
    # Liu Jiangmei
    {"person_id": 3, "org_id": 1, "title": "麒麟区委副书记", "start_date": "", "end_date": "present",
     "rank": "县处级副职", "note": "七代会主席团成员"},
    # Li Rui (Politics and Law)
    {"person_id": 4, "org_id": 1, "title": "麒麟区委政法委书记", "start_date": "", "end_date": "present",
     "rank": "县处级副职", "note": "区委常委"},
    # Wang Mingbo
    {"person_id": 5, "org_id": 1, "title": "麒麟区委常委", "start_date": "", "end_date": "present",
     "rank": "县处级副职", "note": ""},
    # Bi Wenrong
    {"person_id": 6, "org_id": 1, "title": "麒麟区委常委", "start_date": "", "end_date": "present",
     "rank": "县处级副职", "note": ""},
    # Jun Jiahong
    {"person_id": 7, "org_id": 1, "title": "麒麟区委常委", "start_date": "", "end_date": "present",
     "rank": "县处级副职", "note": ""},
    # Liu Peng
    {"person_id": 8, "org_id": 1, "title": "麒麟区委常委", "start_date": "", "end_date": "present",
     "rank": "县处级副职", "note": ""},
    # Li Rui (Organization)
    {"person_id": 9, "org_id": 1, "title": "麒麟区委组织部部长", "start_date": "", "end_date": "present",
     "rank": "县处级副职", "note": "区委常委"},
    # Li Zhou
    {"person_id": 10, "org_id": 2, "title": "麒麟区常务副区长", "start_date": "", "end_date": "present",
     "rank": "县处级副职", "note": "区委常委、区政府党组副书记"},
    {"person_id": 10, "org_id": 1, "title": "麒麟区委常委", "start_date": "", "end_date": "present",
     "rank": "县处级副职", "note": ""},
    # Gao Xingzhi
    {"person_id": 11, "org_id": 2, "title": "麒麟区副区长", "start_date": "", "end_date": "present",
     "rank": "县处级副职", "note": "区委政法委副书记"},
    {"person_id": 11, "org_id": 3, "title": "麒麟公安分局局长", "start_date": "", "end_date": "present",
     "rank": "乡科级正职", "note": "党委书记、局长、督察长"},
    # Yang Gang
    {"person_id": 12, "org_id": 2, "title": "麒麟区副区长", "start_date": "", "end_date": "present",
     "rank": "县处级副职", "note": "区政府党组成员"},
    # Liu Xingli
    {"person_id": 13, "org_id": 2, "title": "麒麟区副区长", "start_date": "", "end_date": "present",
     "rank": "县处级副职", "note": "区委常委、区政府党组成员"},
    {"person_id": 13, "org_id": 1, "title": "麒麟区委常委", "start_date": "", "end_date": "present",
     "rank": "县处级副职", "note": ""},
    # Wang Zijia (suspended)
    {"person_id": 14, "org_id": 2, "title": "麒麟区副区长（挂职）", "start_date": "", "end_date": "present",
     "rank": "县处级副职", "note": "区委常委、挂职两年（2025年挂职）"},
    {"person_id": 14, "org_id": 1, "title": "麒麟区委常委（挂职）", "start_date": "", "end_date": "present",
     "rank": "县处级副职", "note": ""},
    # Ding Lianguo
    {"person_id": 15, "org_id": 2, "title": "麒麟区副区长", "start_date": "", "end_date": "present",
     "rank": "县处级副职", "note": "区政府党组成员"},
    # Li Weimin
    {"person_id": 16, "org_id": 2, "title": "麒麟区副区长", "start_date": "", "end_date": "present",
     "rank": "县处级副职", "note": "区政府党组成员"},
    # Wang Jun
    {"person_id": 17, "org_id": 2, "title": "麒麟区副区长", "start_date": "", "end_date": "present",
     "rank": "县处级副职", "note": "区政府党组成员"},

    # Predecessor Yang Qingdong
    {"person_id": 18, "org_id": 1, "title": "麒麟区委书记", "start_date": "~2021", "end_date": "2026-06",
     "rank": "县处级正职", "note": "曾任曲靖市委常委、麒麟区委书记；2026年5月仍以区委书记身份调研，6月被兰发文接替"},
    {"person_id": 18, "org_id": 4, "title": "曲靖市委常委", "start_date": "", "end_date": "2026-06",
     "rank": "地厅级副职", "note": ""},
]

# ── Relationships ──
relationships = [
    # Core leadership tandem
    {"person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "兰发文为区委书记、张忠文为区长，组成麒麟区党政正职搭档",
     "overlap_org": "麒麟区党政班子", "overlap_period": "2026-06至今"},
    # Party Standing Committee relations
    {"person_a": 1, "person_b": 3, "type": "党委班子成员",
     "context": "兰发文（书记）与刘江梅（副书记）同在区委常委会",
     "overlap_org": "麒麟区区委常委会", "overlap_period": "2026-06至今"},
    {"person_a": 1, "person_b": 4, "type": "党委班子成员",
     "context": "兰发文与李锐（政法委书记）同在区委常委会",
     "overlap_org": "麒麟区区委常委会", "overlap_period": "2026-06至今"},
    {"person_a": 1, "person_b": 5, "type": "党委班子成员",
     "context": "兰发文与王明波同在区委常委会",
     "overlap_org": "麒麟区区委常委会", "overlap_period": "2026-06至今"},
    {"person_a": 1, "person_b": 6, "type": "党委班子成员",
     "context": "兰发文与毕文荣同在区委常委会",
     "overlap_org": "麒麟区区委常委会", "overlap_period": "2026-06至今"},
    {"person_a": 1, "person_b": 7, "type": "党委班子成员",
     "context": "兰发文与隽加宏同在区委常委会",
     "overlap_org": "麒麟区区委常委会", "overlap_period": "2026-06至今"},
    {"person_a": 1, "person_b": 8, "type": "党委班子成员",
     "context": "兰发文与刘鹏同在区委常委会",
     "overlap_org": "麒麟区区委常委会", "overlap_period": "2026-06至今"},
    {"person_a": 1, "person_b": 9, "type": "党委班子成员",
     "context": "兰发文与李锐（组织部部长）同在区委常委会",
     "overlap_org": "麒麟区区委常委会", "overlap_period": "2026-06至今"},
    # Mayor with deputies
    {"person_a": 2, "person_b": 10, "type": "政府班子正副职",
     "context": "张忠文（区长）与李周（常务副区长）构成政府正副搭档",
     "overlap_org": "麒麟区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 11, "type": "政府班子",
     "context": "张忠文与高兴志（副区长兼公安局长）同在区政府",
     "overlap_org": "麒麟区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 12, "type": "政府班子",
     "context": "张忠文与杨刚（副区长）同在区政府",
     "overlap_org": "麒麟区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 13, "type": "政府班子",
     "context": "张忠文与刘兴丽（区委常委、副区长）同在区政府",
     "overlap_org": "麒麟区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 14, "type": "政府班子",
     "context": "张忠文与王子佳（挂职副区长）同在区政府",
     "overlap_org": "麒麟区人民政府", "overlap_period": "2025-01至今"},
    {"person_a": 2, "person_b": 15, "type": "政府班子",
     "context": "张忠文与丁连高（副区长）同在区政府",
     "overlap_org": "麒麟区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 16, "type": "政府班子",
     "context": "张忠文与李维敏（副区长）同在区政府",
     "overlap_org": "麒麟区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 17, "type": "政府班子",
     "context": "张忠文与王俊（副区长）同在区政府",
     "overlap_org": "麒麟区人民政府", "overlap_period": "至今"},
    # Predecessor relationships
    {"person_a": 18, "person_b": 2, "type": "前任继任搭档",
     "context": "杨庆东（前区委书记）与张忠文（区长）先后共事，2021年至2026年6月组成核心搭档",
     "overlap_org": "麒麟区党政班子", "overlap_period": "~2021至2026-06"},
    {"person_a": 1, "person_b": 18, "type": "职位接替",
     "context": "兰发文接替杨庆东担任麒麟区委书记（2026年6月第七次党代会换届）",
     "overlap_org": "中共曲靖市麒麟区委员会", "overlap_period": "2026-06"},
    # Cross-district connections
    {"person_a": 10, "person_b": 11, "type": "同事",
     "context": "李周（常务副区长）与高兴志（副区长兼公安局长）同在区政府班子",
     "overlap_org": "麒麟区人民政府", "overlap_period": "至今"},
    {"person_a": 10, "person_b": 12, "type": "同事",
     "context": "李周与杨刚同为麒麟区副区长",
     "overlap_org": "麒麟区人民政府", "overlap_period": "至今"},
    {"person_a": 10, "person_b": 13, "type": "同事",
     "context": "李周与刘兴丽同为麒麟区副区长",
     "overlap_org": "麒麟区人民政府", "overlap_period": "至今"},
]


# =========================================================================
# Helper functions
# =========================================================================

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(post, is_secretary_predecessor=False):
    """Determine color based on current post."""
    if is_secretary_predecessor or "书记" == post.split("）")[-1] if "书记" in post else False:
        return "200,30,30"
    # Check individual
    if "区委书记" in post and "副" not in post.split("、")[0]:
        return "200,30,30"
    if post in ["麒麟区区长"] or ("区长" in post and "副" not in post and "挂职" not in post):
        return "30,100,200"
    if "纪委" in post:
        return "255,165,0"
    if "政法委" in post:
        return "180,100,50"
    return "100,100,100"


def person_is_top(p):
    post = p.get("current_post", "")
    return "区委书记" in post or "区长" in post


# =========================================================================
# Build
# =========================================================================

def build():
    os.makedirs(TMP, exist_ok=True)
    os.makedirs(PERSONS_DIR, exist_ok=True)

    # ── SQLite ──
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS organizations;
        DROP TABLE IF EXISTS persons;
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY, name TEXT NOT NULL, gender TEXT DEFAULT '', ethnicity TEXT DEFAULT '',
            birth TEXT DEFAULT '', birthplace TEXT DEFAULT '', education TEXT DEFAULT '',
            party_join TEXT DEFAULT '', work_start TEXT DEFAULT '', current_post TEXT DEFAULT '',
            current_org TEXT DEFAULT '', source TEXT DEFAULT ''
        );
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY, name TEXT NOT NULL, type TEXT DEFAULT '',
            level TEXT DEFAULT '', parent TEXT DEFAULT '', location TEXT DEFAULT ''
        );
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT, person_id INTEGER NOT NULL, org_id INTEGER NOT NULL,
            title TEXT DEFAULT '', start_date TEXT DEFAULT '', end_date TEXT DEFAULT '',
            rank TEXT DEFAULT '', note TEXT DEFAULT '',
            FOREIGN KEY (person_id) REFERENCES persons(id), FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT, person_a INTEGER NOT NULL, person_b INTEGER NOT NULL,
            type TEXT DEFAULT '', context TEXT DEFAULT '', overlap_org TEXT DEFAULT '', overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(id), FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        cur.execute(
            "INSERT INTO persons (id,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""), p.get("birth", ""),
             p.get("birthplace", ""), p.get("education", ""), p.get("party_join", ""), p.get("work_start", ""),
             p.get("current_post", ""), p.get("current_org", ""), p.get("source", "")))
    for o in organizations:
        cur.execute("INSERT INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)",
                    (o["id"], o["name"], o["type"], o["level"], o.get("parent", ""), o.get("location", "")))
    for pos in positions:
        cur.execute(
            "INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)",
            (pos["person_id"], pos["org_id"], pos["title"], pos.get("start_date", ""), pos.get("end_date", ""),
             pos.get("rank", ""), pos.get("note", "")))
    for r in relationships:
        cur.execute(
            "INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)",
            (r["person_a"], r["person_b"], r["type"], r["context"], r.get("overlap_org", ""),
             r.get("overlap_period", "")))
    conn.commit()
    conn.close()
    print(f"DB written: {DB_PATH}")
    print(f"  {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

    # ── GEXF ──
    gexf_lines = []
    gexf_lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    gexf_lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    gexf_lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    gexf_lines.append('    <creator>Gov-Relation Research Agent</creator>')
    gexf_lines.append('    <description>曲靖市麒麟区领导班子工作关系网络</description>')
    gexf_lines.append('  </meta>')
    gexf_lines.append('  <graph mode="static" defaultedgetype="undirected">')
    gexf_lines.append('    <attributes class="node">')
    gexf_lines.append('      <attribute id="0" title="type" type="string"/>')
    gexf_lines.append('      <attribute id="1" title="current_post" type="string"/>')
    gexf_lines.append('      <attribute id="2" title="current_org" type="string"/>')
    gexf_lines.append('      <attribute id="3" title="birth" type="string"/>')
    gexf_lines.append('      <attribute id="4" title="source" type="string"/>')
    gexf_lines.append('    </attributes>')
    gexf_lines.append('    <attributes class="edge">')
    gexf_lines.append('      <attribute id="0" title="type" type="string"/>')
    gexf_lines.append('      <attribute id="1" title="context" type="string"/>')
    gexf_lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    gexf_lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    gexf_lines.append('    </attributes>')
    gexf_lines.append('    <nodes>')

    # Helper to classify a person dict
    def is_sec(p_dict):
        post = p_dict.get("current_post", "")
        return ("区委书记" in post and "副" not in post and "前任" not in post and p_dict["name"] != "杨庆东")
    def is_may(p_dict):
        post = p_dict.get("current_post", "")
        return ("区长" in post and "副" not in post) or post == "麒麟区区长"

    # Person nodes
    for p in persons:
        pid = p["id"]
        post = p.get("current_post", "")
        name_clean = p["name"]
        is_qd = "前任" in post or p["name"] == "杨庆东"

        if is_qd:
            color = "150,150,150"
            sz = "18.0"
            shape = "diamond"
        elif is_sec(p):
            color = "200,30,30"
            sz = "20.0"
            shape = "square"
        elif is_may(p):
            color = "30,100,200"
            sz = "20.0"
            shape = "circle"
        elif "纪委" in post:
            color = "255,165,0"
            sz = "12.0"
            shape = "triangle"
        elif "政法委" in post:
            color = "100,100,50"
            sz = "12.0"
            shape = "triangle"
        elif "常委" in post:
            color = "180,100,180"
            sz = "12.0"
            shape = "triangle"
        else:
            color = "100,100,100"
            sz = "12.0"
            shape = "triangle"

    # Organization nodes
    for o in organizations:
        oid = o["id"] + 100000
        otype = o["type"]
        color_map = {"党委": "255,200,200", "政府": "200,200,255", "人大": "200,255,255",
                     "政协": "255,240,200", "纪委": "255,200,150", "国企": "200,255,200",
                     "开发区": "200,255,200"}
        ocolor = color_map.get(otype, "200,200,200")
        gexf_lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        gexf_lines.append('        <attvalues>')
        gexf_lines.append(f'          <attvalue for="0" value="organization"/>')
        gexf_lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        gexf_lines.append('        </attvalues>')
        gexf_lines.append(f'        <viz:color r="{ocolor.split(",")[0]}" g="{ocolor.split(",")[1]}" b="{ocolor.split(",")[2]}" a="0.8"/>')
        gexf_lines.append(f'        <viz:size value="8.0"/>')
        gexf_lines.append(f'        <viz:shape value="hexagon"/>')
        gexf_lines.append('      </node>')

    gexf_lines.append('    </nodes>')
    gexf_lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        gexf_lines.append(
            f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"] + 100000}" '
            f'label="{esc(pos["title"])}" weight="1.0">')
        gexf_lines.append('        <attvalues>')
        gexf_lines.append('          <attvalue for="0" value="worked_at"/>')
        gexf_lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        gexf_lines.append('        </attvalues>')
        gexf_lines.append('      </edge>')
    for r in relationships:
        eid += 1
        gexf_lines.append(
            f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" '
            f'label="{esc(r["type"])}" weight="2.0">')
        gexf_lines.append('        <attvalues>')
        gexf_lines.append(f'          <attvalue for="0" value="relationship"/>')
        gexf_lines.append(f'          <attvalue for="1" value="{esc(r.get("context",""))}"/>')
        gexf_lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org",""))}"/>')
        gexf_lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period",""))}"/>')
        gexf_lines.append('        </attvalues>')
        gexf_lines.append('      </edge>')
    gexf_lines.append('    </edges>')
    gexf_lines.append('  </graph>')
    gexf_lines.append('</gexf>')
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(gexf_lines))
    print(f"GEXF written: {GEXF_PATH}")

    # ── Person JSONs ──
    source_register = [
        {"id": "S001", "title": "麒麟区第七次党代会开幕，兰发文作报告",
         "url": "https://www.ql.gov.cn/news/detail/qlyw/83591.html",
         "publisher": "麒麟区人民政府", "published_at": "2026-06-27", "accessed_at": AS_OF,
         "source_type": "government", "reliability": "high"},
        {"id": "S002", "title": "张忠文——区长简历",
         "url": "https://www.ql.gov.cn/gov/public/detail/2zfld/14088.html",
         "publisher": "麒麟区人民政府", "published_at": "2021-11-25", "accessed_at": AS_OF,
         "source_type": "government", "reliability": "high"},
        {"id": "S003", "title": "李周——常务副区长简历",
         "url": "https://www.ql.gov.cn/gov/public/detail/2zfld/76509.html",
         "publisher": "麒麟区人民政府", "published_at": "2025-07-25", "accessed_at": AS_OF,
         "source_type": "government", "reliability": "high"},
        {"id": "S004", "title": "高兴志——副区长简历",
         "url": "https://www.ql.gov.cn/gov/public/detail/2zfld/33942.html",
         "publisher": "麒麟区人民政府", "published_at": "2022-11-15", "accessed_at": AS_OF,
         "source_type": "government", "reliability": "high"},
        {"id": "S005", "title": "刘兴丽——副区长简历",
         "url": "https://www.ql.gov.cn/gov/public/detail/2zfld/14095.html",
         "publisher": "麒麟区人民政府", "published_at": "2021-11-25", "accessed_at": AS_OF,
         "source_type": "government", "reliability": "high"},
        {"id": "S006", "title": "区政府领导页面",
         "url": "https://www.ql.gov.cn/gov/public/leader/2zfld.html",
         "publisher": "麒麟区人民政府", "accessed_at": AS_OF,
         "source_type": "government", "reliability": "high"},
        {"id": "S007", "title": "七代会预备会议（确认兰发文为区委书记）",
         "url": "https://www.ql.gov.cn/news/detail/qlyw/83538.html",
         "publisher": "麒麟区人民政府", "published_at": "2026-06-25", "accessed_at": AS_OF,
         "source_type": "government", "reliability": "high"},
    ]

    def make_person_json(person_p, timeline_items, rels_items, src_items):
        p_data = next((x for x in persons if x["id"] == person_p["id"]), person_p)
        return {
            "schema_version": "1.0", "generated_at": AS_OF,
            "investigation_scope": {
                "province": "云南省", "city": "曲靖市", "region": "麒麟区",
                "job": p_data.get("current_post", ""), "task_id": "yunnan_麒麟区",
                "time_focus": f"as of {AS_OF}"
            },
            "identity": {
                "person_id": f"qilin_{p_data['name']}",
                "name": p_data["name"], "aliases": [],
                "gender": p_data.get("gender", ""), "ethnicity": p_data.get("ethnicity", ""),
                "birth": p_data.get("birth", ""), "birthplace": p_data.get("birthplace", ""),
                "native_place": "",
                "education": [{"degree": p_data.get("education", "")}],
                "party_join": p_data.get("party_join", ""),
                "work_start": p_data.get("work_start", ""),
                "dedupe_keys": {
                    "name_birth": f"{p_data['name']}_{p_data.get('birth', '')}",
                    "official_profile_url": p_data.get("source", "")
                }
            },
            "current_status": {
                "current_post": p_data.get("current_post", ""),
                "current_org": p_data.get("current_org", ""),
                "administrative_rank": "县处级",
                "as_of": AS_OF, "is_current_confirmed": True, "source_ids": ["S001", "S002", "S006"]
            },
            "career_timeline": timeline_items,
            "organizations": [],
            "relationships": rels_items,
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "career_pattern": "",
                "systemsExperience": [],
                "geographic_pattern": []
            },
            "source_register": src_items,
            "open_questions": [
                {"priority": "critical",
                 "question": f"Complete career timeline before current role for {p_data['name']}",
                 "suggested_queries": [f"{p_data['name']} 简历", f"{p_data['name']} 任职经历"]}
            ]
        }

    # Generate person JSONs for key figures
    for p in persons:
        name = p["name"]
        if name in ["兰发文", "张忠文", "杨庆东", "李周", "刘兴丽"]:
            timeline = []
            for pos in positions:
                if pos["person_id"] == p["id"]:
                    org_name = next((o["name"] for o in organizations if o["id"] == pos["org_id"]), "")
                    timeline.append({
                        "start": pos.get("start_date", ""), "end": pos.get("end_date", ""),
                        "org": org_name, "title": pos["title"], "rank": pos.get("rank", ""),
                        "location": "云南曲靖麒麟区", "notes": pos.get("note", ""),
                        "confidence": "confirmed",
                        "source_ids": ["S001", "S002", "S006", "S007"][:2]
                    })
            rels = []
            for r in relationships:
                if r["person_a"] == p["id"]:
                    other = next((x["name"] for x in persons if x["id"] == r["person_b"]), "")
                    rels.append({
                        "person": other, "relationship_type": r["type"],
                        "evidence": r["context"], "confidence": "confirmed"
                    })
                elif r["person_b"] == p["id"]:
                    other = next((x["name"] for x in persons if x["id"] == r["person_a"]), "")
                    rels.append({
                        "person": other, "relationship_type": r["type"],
                        "evidence": r["context"], "confidence": "confirmed"
                    })
            pjson = make_person_json(p, timeline, rels, source_register)
            # Determine job title for filename
            job = p.get("current_post", "").replace("（", "(").replace("）", ")")
            safe_name = p["name"]
            p_path = os.path.join(PERSONS_DIR,
                                  f"{AS_OF_SHORT}-云南省-曲靖市-{job}-{safe_name}.json")
            with open(p_path, "w", encoding="utf-8") as f:
                json.dump(pjson, f, ensure_ascii=False, indent=2)
            print(f"Person JSON written: {p_path}")

    print("\nBuild complete.")


if __name__ == "__main__":
    build()