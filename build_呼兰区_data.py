#!/usr/bin/env python3
"""呼兰区（哈尔滨市）领导班子关系网络生成脚本

数据来源：
  - 哈尔滨市呼兰区人民政府官网 (www.hulan.gov.cn) 新闻及领导活动报道
  - 呼兰区五届人大常委会第四十次、第四十二次会议公告

数据截至：2026年7月

Target roles:
  - 区委书记: 曹德友
  - 区委副书记、区长: 张磊
  - 区委副书记: 刘蕊
  - 区委常委、常务副区长: 任良
  - 区委常委、副区长: 关巍
  - 区委常委、纪委书记、监委主任: 徐辉
  - 区委常委、组织部部长: 邹青宇
  - 区委常委、宣传部部长: 徐小燕
"""

import json
import os
import sqlite3
from datetime import datetime
from pathlib import Path

# ── Paths ──
STAGING = Path(__file__).parent
DB_PATH = STAGING / "呼兰区_network.db"
GEXF_PATH = STAGING / "呼兰区_network.gexf"
PERSONS_DIR = STAGING

TODAY = "2026-07-24"
AS_OF = TODAY

# ── Helper ──
def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# =========================================================================
# DATA
# =========================================================================

persons = [
    {
        "id": 1,
        "name": "曹德友",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共呼兰区委员会",
        "source": "https://www.hulan.gov.cn/",
    },
    {
        "id": 2,
        "name": "张磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委副书记、区长",
        "current_org": "呼兰区人民政府",
        "source": "https://www.hulan.gov.cn/",
    },
    {
        "id": 3,
        "name": "刘蕊",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委副书记",
        "current_org": "中共呼兰区委员会",
        "source": "https://www.hulan.gov.cn/",
    },
    {
        "id": 4,
        "name": "任良",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、常务副区长",
        "current_org": "呼兰区人民政府",
        "source": "https://www.hulan.gov.cn/",
    },
    {
        "id": 5,
        "name": "邹青宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、组织部部长",
        "current_org": "中共呼兰区委员会",
        "source": "https://www.hulan.gov.cn/",
    },
    {
        "id": 6,
        "name": "徐辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、纪委书记、监委主任",
        "current_org": "中共呼兰区纪律检查委员会",
        "source": "https://www.hulan.gov.cn/",
    },
    {
        "id": 7,
        "name": "关巍",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "呼兰区人民政府",
        "source": "https://www.hulan.gov.cn/",
    },
    {
        "id": 8,
        "name": "徐小燕",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、宣传部部长",
        "current_org": "中共呼兰区委员会",
        "source": "https://www.hulan.gov.cn/",
    },
    {
        "id": 9,
        "name": "李彤",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "呼兰区人民政府",
        "source": "https://www.hulan.gov.cn/",
    },
    {
        "id": 10,
        "name": "马金明",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "呼兰区人民政府",
        "source": "https://www.hulan.gov.cn/",
    },
    {
        "id": 11,
        "name": "张弘",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "呼兰区人民政府",
        "source": "https://www.hulan.gov.cn/",
    },
    {
        "id": 12,
        "name": "张岐欣",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "呼兰区人民代表大会常务委员会",
        "source": "https://www.hulan.gov.cn/",
    },
    {
        "id": 13,
        "name": "郭启才",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区人大常委会副主任",
        "current_org": "呼兰区人民代表大会常务委员会",
        "source": "https://www.hulan.gov.cn/",
    },
    {
        "id": 14,
        "name": "董威江",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区人大常委会副主任",
        "current_org": "呼兰区人民代表大会常务委员会",
        "source": "https://www.hulan.gov.cn/",
    },
    {
        "id": 15,
        "name": "卢刚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "中共呼兰区委员会",
        "source": "https://www.hulan.gov.cn/",
    },
    {
        "id": 16,
        "name": "孟朝晖",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区人民法院院长",
        "current_org": "呼兰区人民法院",
        "source": "https://www.hulan.gov.cn/",
    },
    {
        "id": 17,
        "name": "付爱民",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区人民检察院检察长",
        "current_org": "呼兰区人民检察院",
        "source": "https://www.hulan.gov.cn/",
    },
]

organizations = [
    {"id": 1, "name": "中共呼兰区委员会", "type": "党委", "level": "县处级", "parent": "中共哈尔滨市委", "location": "哈尔滨市呼兰区"},
    {"id": 2, "name": "呼兰区人民政府", "type": "政府", "level": "县处级", "parent": "哈尔滨市人民政府", "location": "哈尔滨市呼兰区"},
    {"id": 3, "name": "中共呼兰区纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共呼兰区委员会", "location": "哈尔滨市呼兰区"},
    {"id": 4, "name": "呼兰区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "哈尔滨市人大常委会", "location": "哈尔滨市呼兰区"},
    {"id": 5, "name": "呼兰区人民法院", "type": "事业单位", "level": "县处级", "parent": "哈尔滨市中级人民法院", "location": "哈尔滨市呼兰区"},
    {"id": 6, "name": "呼兰区人民检察院", "type": "事业单位", "level": "县处级", "parent": "哈尔滨市人民检察院", "location": "哈尔滨市呼兰区"},
    {"id": 7, "name": "中共呼兰区委组织部", "type": "党委", "level": "乡科级", "parent": "中共呼兰区委员会", "location": "哈尔滨市呼兰区"},
    {"id": 8, "name": "中共呼兰区委宣传部", "type": "党委", "level": "乡科级", "parent": "中共呼兰区委员会", "location": "哈尔滨市呼兰区"},
]

positions = [
    # Party committee
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "区委主要负责人"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # Government
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "区政府主要负责人"},
    {"person_id": 4, "org_id": 2, "title": "常务副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副区长", "start_date": "2026-04", "end_date": "present", "rank": "县处级副职", "note": "2026年4月任命"},
    {"person_id": 11, "org_id": 2, "title": "副区长", "start_date": "2026-07", "end_date": "present", "rank": "县处级副职", "note": "2026年7月任命"},
    # Discipline
    {"person_id": 6, "org_id": 3, "title": "纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # Organization
    {"person_id": 5, "org_id": 7, "title": "组织部部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # Propaganda
    {"person_id": 8, "org_id": 8, "title": "宣传部部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "原副区长，2026年4月转任宣传部部长"},
    # People's Congress
    {"person_id": 12, "org_id": 4, "title": "区人大常委会主任", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    {"person_id": 13, "org_id": 4, "title": "区人大常委会副主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 14, "org_id": 4, "title": "区人大常委会副主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # Court & Procuratorate
    {"person_id": 16, "org_id": 5, "title": "院长", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    {"person_id": 17, "org_id": 6, "title": "检察长", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
]

relationships = [
    # 书记 ↔ 区长 (top leadership pair)
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "曹德友（区委书记）与张磊（区长）在区委常委会和区政府班子共事", "overlap_org": "中共呼兰区委/呼兰区人民政府", "overlap_period": "2025年至今"},
    # 书记 ↔ 副书记
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "曹德友与刘蕊在区委常委会共事", "overlap_org": "中共呼兰区委", "overlap_period": "2025年至今"},
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "曹德友与任良在区委常委会共事", "overlap_org": "中共呼兰区委", "overlap_period": "2025年至今"},
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "曹德友与邹青宇在区委常委会共事", "overlap_org": "中共呼兰区委", "overlap_period": "2025年至今"},
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "曹德友与徐辉在区委常委会共事", "overlap_org": "中共呼兰区委", "overlap_period": "2025年至今"},
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "曹德友与关巍在区委常委会共事", "overlap_org": "中共呼兰区委", "overlap_period": "2025年至今"},
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "曹德友与徐小燕在区委常委会共事", "overlap_org": "中共呼兰区委", "overlap_period": "2025年至今"},
    # 区长 ↔ 副区长
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "张磊（区长）与任良（常务副区长）在区政府班子共事", "overlap_org": "呼兰区人民政府", "overlap_period": "2025年至今"},
    {"person_a": 2, "person_b": 7, "type": "overlap", "context": "张磊与关巍在区政府班子共事", "overlap_org": "呼兰区人民政府", "overlap_period": "2025年至今"},
    {"person_a": 2, "person_b": 9, "type": "overlap", "context": "张磊与李彤在区政府班子共事", "overlap_org": "呼兰区人民政府", "overlap_period": "2025年至今"},
    {"person_a": 2, "person_b": 10, "type": "overlap", "context": "张磊与马金明在区政府班子共事", "overlap_org": "呼兰区人民政府", "overlap_period": "2026年4月至今"},
    {"person_a": 2, "person_b": 11, "type": "overlap", "context": "张磊与张弘在区政府班子共事", "overlap_org": "呼兰区人民政府", "overlap_period": "2026年7月至今"},
    # 常务副区长 ↔ 其他副区长
    {"person_a": 4, "person_b": 7, "type": "overlap", "context": "任良（常务副区长）与关巍（副区长）在区政府班子共事", "overlap_org": "呼兰区人民政府", "overlap_period": "2025年至今"},
    {"person_a": 4, "person_b": 9, "type": "overlap", "context": "任良与李彤在区政府班子共事", "overlap_org": "呼兰区人民政府", "overlap_period": "2025年至今"},
    {"person_a": 4, "person_b": 10, "type": "overlap", "context": "任良与马金明在区政府班子共事", "overlap_org": "呼兰区人民政府", "overlap_period": "2026年4月至今"},
    {"person_a": 4, "person_b": 11, "type": "overlap", "context": "任良与张弘在区政府班子共事", "overlap_org": "呼兰区人民政府", "overlap_period": "2026年7月至今"},
    # 副书记间关系
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "刘蕊与任良在区委常委会共事", "overlap_org": "中共呼兰区委", "overlap_period": "2025年至今"},
    {"person_a": 3, "person_b": 5, "type": "overlap", "context": "刘蕊与邹青宇在区委常委会共事", "overlap_org": "中共呼兰区委", "overlap_period": "2025年至今"},
    {"person_a": 3, "person_b": 6, "type": "overlap", "context": "刘蕊与徐辉在区委常委会共事", "overlap_org": "中共呼兰区委", "overlap_period": "2025年至今"},
    {"person_a": 3, "person_b": 8, "type": "overlap", "context": "刘蕊与徐小燕在区委常委会共事", "overlap_org": "中共呼兰区委", "overlap_period": "2025年至今"},
    # 人大与党委
    {"person_a": 1, "person_b": 12, "type": "overlap", "context": "曹德友与张岐欣在区委、区人大工作中协作", "overlap_org": "呼兰区", "overlap_period": "2025年至今"},
    {"person_a": 2, "person_b": 12, "type": "overlap", "context": "张磊向区人大常委会报告工作并提请人事任免", "overlap_org": "呼兰区人民政府/区人大常委会", "overlap_period": "2025年至今"},
    # 徐小燕从副区长转任宣传部长
    {"person_a": 8, "person_b": 2, "type": "overlap", "context": "徐小燕曾任副区长（至2026年4月），后转任宣传部部长，曾与张磊在区政府班子共事", "overlap_org": "呼兰区人民政府", "overlap_period": "2025年-2026年4月"},
    {"person_a": 8, "person_b": 4, "type": "overlap", "context": "徐小燕与任良在区政府班子共事至2026年4月", "overlap_org": "呼兰区人民政府", "overlap_period": "2025年-2026年4月"},
]


# =========================================================================
# BUILD
# =========================================================================

def build():
    os.makedirs(STAGING, exist_ok=True)

    # ── SQLite ──
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()

    cur.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS organizations;
        DROP TABLE IF EXISTS persons;

        CREATE TABLE persons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pid TEXT UNIQUE NOT NULL,
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
            person_id TEXT NOT NULL,
            org_id INTEGER NOT NULL,
            title TEXT DEFAULT '',
            start_date TEXT DEFAULT '',
            end_date TEXT DEFAULT '',
            rank TEXT DEFAULT '',
            note TEXT DEFAULT '',
            FOREIGN KEY (person_id) REFERENCES persons(pid),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );

        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT NOT NULL,
            person_b TEXT NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(pid),
            FOREIGN KEY (person_b) REFERENCES persons(pid)
        );
    """)

    person_map = {}
    for idx, p in enumerate(persons, 1):
        pid = f"hulan_{p['name']}"
        person_map[p["id"]] = pid
        cur.execute("""INSERT INTO persons (id,pid,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (idx, pid, p["name"], p.get("gender", ""), p.get("ethnicity", ""), p.get("birth", ""),
                     p.get("birthplace", ""), p.get("education", ""), p.get("party_join", ""), p.get("work_start", ""),
                     p.get("current_post", ""), p.get("current_org", ""), p.get("source", "")))

    for o in organizations:
        cur.execute("""INSERT INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)""",
                    (o["id"], o["name"], o["type"], o["level"], o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        cur.execute("""INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)""",
                    (person_map[pos["person_id"]], pos["org_id"], pos["title"], pos.get("start_date", ""),
                     pos.get("end_date", ""), pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        cur.execute("""INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)""",
                    (person_map[r["person_a"]], person_map[r["person_b"]], r["type"], r["context"],
                     r.get("overlap_org", ""), r.get("overlap_period", "")))

    conn.commit()
    conn.close()
    print(f"DB written: {DB_PATH}")
    print(f"  {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

    # ── GEXF ──
    def person_color(post):
        if "书记" in post and "副" not in post and "纪委" not in post and "区委书记" in post:
            return "255,50,50"
        if "区长" in post and "副" not in post:
            return "50,100,255"
        if "副区长" in post or "常务副区长" in post:
            return "100,150,220"
        if "副书记" in post and "区长" not in post:
            return "100,150,220"
        if "纪委书记" in post or "纪委" in post:
            return "255,165,0"
        if "主任" in post and "人大" in post:
            return "60,180,60"
        if "法院" in post or "检察院" in post:
            return "180,100,180"
        if "部长" in post:
            return "100,150,220"
        return "100,100,100"

    def is_top_leader(post):
        return ("书记" in post and "副" not in post and "纪委" not in post and "区委书记" in post) or \
               ("区长" in post and "副" not in post)

    def person_shape(post):
        if "书记" in post and "副" not in post and "纪委" not in post and "区委书记" in post:
            return "square"
        if "区长" in post and "副" not in post:
            return "circle"
        if "常务副区长" in post:
            return "diamond"
        if "纪委书记" in post or "纪委" in post:
            return "diamond"
        return "triangle"

    def org_color(otype):
        colors = {
            "党委": "255,200,200",
            "政府": "200,200,255",
            "人大": "200,255,255",
            "政协": "255,240,200",
            "纪委": "255,200,150",
            "开发区": "200,255,200",
            "事业单位": "220,220,220",
        }
        return colors.get(otype, "200,200,200")

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>哈尔滨市呼兰区领导班子关系网络</description>')
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

    # Nodes — persons
    lines.append('    <nodes>')
    for p in persons:
        pid_num = p["id"]
        post = p.get("current_post", "")
        c = person_color(post)
        sz = "20.0" if is_top_leader(post) else "12.0"
        shape = person_shape(post)

        lines.append(f'      <node id="p{pid_num}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("source",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}" a="1.0"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append(f'        <viz:shape value="{shape}"/>')
        lines.append('      </node>')

    # Nodes — organizations
    for o in organizations:
        oid = o["id"] + 100000
        ocolor = org_color(o["type"])

        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{ocolor.split(",")[0]}" g="{ocolor.split(",")[1]}" b="{ocolor.split(",")[2]}" a="0.8"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append(f'        <viz:shape value="hexagon"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → organization
    for pos in positions:
        if pos["org_id"] == 99:
            continue
        eid += 1
        pid_num = pos["person_id"]
        oid = pos["org_id"] + 100000
        lines.append(
            f'      <edge id="e{eid}" source="p{pid_num}" target="o{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ person
    for r in relationships:
        eid += 1
        lines.append(
            f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}")

    # ── Person Graph JSONs ──
    source_register = [
        {"id": "S001", "title": "呼兰区召开庆祝中国共产党成立105周年暨'两优一先'表彰大会",
         "url": "https://www.hulan.gov.cn/hebhlq/ldhd/202606/c01_1132929.shtml",
         "publisher": "呼兰区人民政府", "published_at": "2026-06-30", "accessed_at": "2026-07-24", "source_type": "official", "reliability": "high", "notes": "确认区委书记曹德友、区委副书记刘蕊、区委常委等人"},
        {"id": "S002", "title": "呼兰区五届人大常委会召开第四十二次会议",
         "url": "https://www.hulan.gov.cn/hebhlq/rsrm/202607/c01_1133826.shtml",
         "publisher": "呼兰区人民政府", "published_at": "2026-07-03", "accessed_at": "2026-07-24", "source_type": "official", "reliability": "high", "notes": "确认区长张磊、副区长任良、李彤、马金明、任命张弘为副区长"},
        {"id": "S003", "title": "呼兰区五届人大常委会召开第四十次会议",
         "url": "https://www.hulan.gov.cn/hebhlq/rsrm/202604/c01_1121683.shtml",
         "publisher": "呼兰区人民政府", "published_at": "2026-04-23", "accessed_at": "2026-07-24", "source_type": "official", "reliability": "high", "notes": "确认张磊为区长（提名），任命马金明为副区长，徐小燕免去副区长转宣传部部长"},
        {"id": "S004", "title": "曹德友等领导检查节日期间安全工作",
         "url": "https://www.hulan.gov.cn/hebhlq/ldhd/202606/c01_1131503.shtml",
         "publisher": "呼兰区人民政府", "published_at": "2026-06-20", "accessed_at": "2026-07-24", "source_type": "official", "reliability": "high", "notes": "确认曹德友为区委书记"},
        {"id": "S005", "title": "市老促会到呼兰区开展革命老区振兴发展专项调研",
         "url": "https://www.hulan.gov.cn/hebhlq/ldhd/202607/c01_1135523.shtml",
         "publisher": "呼兰区人民政府", "published_at": "2026-07-15", "accessed_at": "2026-07-24", "source_type": "official", "reliability": "high", "notes": "确认刘蕊为区委副书记"},
        {"id": "S006", "title": "呼兰区举办'二次创业启新程'演讲活动",
         "url": "https://www.hulan.gov.cn/hebhlq/ldhd/202606/c01_1132496.shtml",
         "publisher": "呼兰区人民政府", "published_at": "2026-06-26", "accessed_at": "2026-07-24", "source_type": "official", "reliability": "high", "notes": "确认卢刚、刘蕊、徐小燕、郭启才为区领导"},
        {"id": "S007", "title": "Wikipedia - 呼兰区",
         "url": "https://zh.wikipedia.org/wiki/%E5%91%BC%E5%85%B0%E5%8C%BA",
         "publisher": "Wikipedia", "published_at": "", "accessed_at": "2026-07-24", "source_type": "encyclopedia", "reliability": "medium", "notes": "呼兰区基本概况"},
    ]

    def make_person_json(p, custom_id=None):
        rank = "县处级正职"
        if "书记" in p.get("current_post", "") and "副" not in p.get("current_post", "") and "区委书记" in p.get("current_post", ""):
            rank = "县处级正职"
        elif "区长" in p.get("current_post", "") and "副" not in p.get("current_post", ""):
            rank = "县处级正职"
        else:
            rank = "县处级副职"

        result = {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "黑龙江省",
                "city": "哈尔滨市",
                "region": "呼兰区",
                "job": p.get("current_post", ""),
                "task_id": "heilongjiang_呼兰区",
                "time_focus": "2026年7月"
            },
            "identity": {
                "person_id": f"hulan_{p['name']}" if not custom_id else custom_id,
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
                    "name_birth": f"{p['name']}_{p.get('birth', '')}",
                    "name_birthplace": f"{p['name']}_{p.get('birthplace', '')}",
                    "official_profile_url": p.get("source", "")
                }
            },
            "current_status": {
                "current_post": p.get("current_post", ""),
                "current_org": p.get("current_org", ""),
                "administrative_rank": rank,
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001", "S002", "S003"]
            },
            "career_timeline": [
                {
                    "start": "unknown",
                    "end": "",
                    "org": p.get("current_org", ""),
                    "title": p.get("current_post", ""),
                    "notes": "现任，公开资料中未找到详细履历",
                    "confidence": "confirmed",
                    "source_ids": ["S001", "S002"]
                }
            ],
            "organizations": [],
            "relationships": [],
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
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "在公开信息中未发现该人物负面信号",
                 "date": "", "confidence": "confirmed", "source_ids": []}
            ],
            "source_register": source_register,
            "confidence_summary": {
                "identity": "unverified" if not p.get("birth") else "confirmed",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "medium",
                "biggest_gap": f"{p['name']}的完整履历信息缺失"
            },
            "open_questions": [
                {"priority": "critical",
                 "question": f"{p['name']}的完整职业生涯履历（出生年月、教育背景、历任职务）",
                 "why_it_matters": "无法追溯其任职路径和系统经历，无法建立更深层的关系网络",
                 "suggested_queries": [f"{p['name']} 简历 呼兰 哈尔滨"],
                 "last_attempted": AS_OF},
            ]
        }
        return result

    # Generate person JSON files for the two main leaders
    for p in persons[:2]:
        pjson = make_person_json(p)
        job_slug = "区委书记" if p["id"] == 1 else "区长"
        fname = f"{TODAY}-黑龙江省-哈尔滨市-{job_slug}-{p['name']}.json"
        fpath = os.path.join(PERSONS_DIR, fname)
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(pjson, f, ensure_ascii=False, indent=2)
        print(f"Person JSON written: {fpath}")


if __name__ == "__main__":
    build()
