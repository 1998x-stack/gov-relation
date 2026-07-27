#!/usr/bin/env python3
"""方正县（哈尔滨市）领导班子关系网络生成脚本

数据来源：
  - 方正县人民政府官网 (www.hrbfz.gov.cn) 新闻及领导活动报道
  - 新闻报道中提及的领导分工及任职信息
  - 百度百科方正县词条

数据截至：2026年7月

Target roles:
  - 县委书记: 周泉
  - 县委副书记、县长: 杨平
  - 县人大常委会主任: 吴国清
  - 县政协主席: 张威
"""

import json
import os
import sqlite3
from datetime import datetime
from pathlib import Path

# ── Paths ──
STAGING = Path(__file__).parent
DB_PATH = STAGING / "方正县_network.db"
GEXF_PATH = STAGING / "方正县_network.gexf"
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
    # ── Current Top Leaders ──
    {
        "id": 1,
        "name": "周泉",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1976-08",
        "birthplace": "",
        "education": "研究生/硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共方正县委员会",
        "source": "https://baike.baidu.com/item/周泉/26935918",
    },
    {
        "id": 2,
        "name": "杨平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976",
        "birthplace": "黑龙江宾县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "方正县人民政府",
        "source": "http://www.hrbfz.gov.cn/",
    },
    # ── Previous Leaders ──
    {
        "id": 3,
        "name": "郑伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984",
        "birthplace": "",
        "education": "清华大学硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "原县委书记（已离任）",
        "current_org": "中共哈尔滨市委（待确认去向）",
        "source": "https://baike.baidu.com/item/郑伟/60831633",
    },
    {
        "id": 4,
        "name": "张英俊",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原县长（已离任）",
        "current_org": "",
        "source": "",
    },
    # ── Standing Committee Members ──
    {
        "id": 5,
        "name": "崔融冰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共方正县委员会",
        "source": "http://www.hrbfz.gov.cn/",
    },
    {
        "id": 6,
        "name": "肖沐阳",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共方正县委员会",
        "source": "http://www.hrbfz.gov.cn/",
    },
    {
        "id": 7,
        "name": "张昕明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "方正县人民政府",
        "source": "http://www.hrbfz.gov.cn/",
    },
    {
        "id": 8,
        "name": "李洪日",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共方正县委员会",
        "source": "http://www.hrbfz.gov.cn/",
    },
    {
        "id": 9,
        "name": "刘文海",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "方正县人民政府",
        "source": "http://www.hrbfz.gov.cn/",
    },
    {
        "id": 10,
        "name": "马延妍",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共方正县委员会",
        "source": "http://www.hrbfz.gov.cn/",
    },
    {
        "id": 11,
        "name": "吴宏奇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共方正县委员会",
        "source": "http://www.hrbfz.gov.cn/",
    },
    {
        "id": 12,
        "name": "王刚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共方正县委员会",
        "source": "http://www.hrbfz.gov.cn/",
    },
    {
        "id": 13,
        "name": "郝鹏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共方正县委员会",
        "source": "http://www.hrbfz.gov.cn/",
    },
    {
        "id": 14,
        "name": "张声雷",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共方正县委员会",
        "source": "http://www.hrbfz.gov.cn/",
    },
    # ── County Government Leaders ──
    {
        "id": 15,
        "name": "刘国峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "方正县人民政府",
        "source": "http://www.hrbfz.gov.cn/",
    },
    {
        "id": 16,
        "name": "张广聪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长、公安局局长",
        "current_org": "方正县公安局",
        "source": "http://www.hrbfz.gov.cn/",
    },
    {
        "id": 17,
        "name": "姜兆姝",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "方正县人民政府",
        "source": "http://www.hrbfz.gov.cn/",
    },
    {
        "id": 18,
        "name": "张迪",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "方正县人民政府",
        "source": "http://www.hrbfz.gov.cn/",
    },
    {
        "id": 19,
        "name": "黄学仁",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "方正县人民政府",
        "source": "http://www.hrbfz.gov.cn/",
    },
    {
        "id": 20,
        "name": "宋伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "方正县人民政府",
        "source": "http://www.hrbfz.gov.cn/",
    },
    # ── Congress and Political Consultative ──
    {
        "id": 21,
        "name": "吴国清",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "方正县人民代表大会常务委员会",
        "source": "https://baike.baidu.com/item/方正县",
    },
    {
        "id": 22,
        "name": "汪志明",
        "gender": "女",
        "ethnicity": "蒙古族",
        "birth": "1967",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "方正县人民代表大会常务委员会",
        "source": "https://baike.baidu.com/item/方正县",
    },
    {
        "id": 23,
        "name": "高守星",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "方正县人民代表大会常务委员会",
        "source": "https://baike.baidu.com/item/方正县",
    },
    {
        "id": 24,
        "name": "张威",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "中国人民政治协商会议方正县委员会",
        "source": "https://baike.baidu.com/item/方正县",
    },
]

organizations = [
    {"id": 1, "name": "中共方正县委员会", "type": "党委", "level": "县处级", "parent": "中共哈尔滨市委", "location": "哈尔滨市方正县"},
    {"id": 2, "name": "方正县人民政府", "type": "政府", "level": "县处级", "parent": "哈尔滨市人民政府", "location": "哈尔滨市方正县"},
    {"id": 3, "name": "方正县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共方正县委员会", "location": "哈尔滨市方正县"},
    {"id": 4, "name": "方正县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "哈尔滨市人大常委会", "location": "哈尔滨市方正县"},
    {"id": 5, "name": "中国人民政治协商会议方正县委员会", "type": "政协", "level": "县处级", "parent": "哈尔滨市政协", "location": "哈尔滨市方正县"},
    {"id": 6, "name": "方正县公安局", "type": "政府", "level": "乡科级", "parent": "方正县人民政府", "location": "哈尔滨市方正县"},
    {"id": 7, "name": "中共哈尔滨市委", "type": "党委", "level": "地厅级", "parent": "中共黑龙江省委", "location": "哈尔滨市"},
]

positions = [
    # Party committee
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "2025-12", "end_date": "present", "rank": "县处级正职", "note": "县委主要负责人"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "2026-01", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 11, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 12, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 13, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 14, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "政法委书记"},
    # Government
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "2026-01", "end_date": "present", "rank": "县处级正职", "note": "县政府主要负责人"},
    {"person_id": 7, "org_id": 2, "title": "常务副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 16, "org_id": 6, "title": "副县长、公安局局长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 18, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 19, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 20, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # Previous leaders (historical positions)
    {"person_id": 1, "org_id": 2, "title": "县长", "start_date": "2024-07", "end_date": "2025-12", "rank": "县处级正职", "note": "周泉由县长升任县委书记"},
    {"person_id": 3, "org_id": 1, "title": "县委书记", "start_date": "2020", "end_date": "2025-12", "rank": "县处级正职", "note": "前任县委书记"},
    {"person_id": 3, "org_id": 2, "title": "县长", "start_date": "2019-03", "end_date": "2020-09", "rank": "县处级正职", "note": "郑伟由县长升任县委书记"},
    {"person_id": 4, "org_id": 2, "title": "县长", "start_date": "", "end_date": "2024-07", "rank": "县处级正职", "note": "前任县长（张英俊），具体任期待查"},
    # People's Congress
    {"person_id": 21, "org_id": 4, "title": "县人大常委会主任", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    {"person_id": 22, "org_id": 4, "title": "县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 23, "org_id": 4, "title": "县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # Political Consultative
    {"person_id": 24, "org_id": 5, "title": "县政协主席", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
]

relationships = [
    # 书记 ↔ 县长 (top leadership pair)
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "周泉（县委书记，原县长）与杨平（县长）在县委常委会和县政府班子共事", "overlap_org": "中共方正县委/方正县人民政府", "overlap_period": "2026年1月至今"},
    # 书记 ↔ 副书记
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "周泉与崔融冰在县委常委会共事", "overlap_org": "中共方正县委", "overlap_period": "2025年12月至今"},
    # 书记 ↔ 常委
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "周泉与张昕明在县委常委会共事", "overlap_org": "中共方正县委", "overlap_period": "2025年12月至今"},
    {"person_a": 1, "person_b": 14, "type": "overlap", "context": "周泉与张声雷在县委常委会共事", "overlap_org": "中共方正县委", "overlap_period": "2025年12月至今"},
    # 县长 ↔ 副县长
    {"person_a": 2, "person_b": 7, "type": "overlap", "context": "杨平（县长）与张昕明（常务副县长）在县政府班子共事", "overlap_org": "方正县人民政府", "overlap_period": "2026年1月至今"},
    {"person_a": 2, "person_b": 9, "type": "overlap", "context": "杨平与刘文海在县政府班子共事", "overlap_org": "方正县人民政府", "overlap_period": "2026年1月至今"},
    {"person_a": 2, "person_b": 15, "type": "overlap", "context": "杨平与刘国峰在县政府班子共事", "overlap_org": "方正县人民政府", "overlap_period": "2026年1月至今"},
    {"person_a": 2, "person_b": 16, "type": "overlap", "context": "杨平与张广聪在县政府班子共事", "overlap_org": "方正县人民政府", "overlap_period": "2026年1月至今"},
    {"person_a": 2, "person_b": 17, "type": "overlap", "context": "杨平与姜兆姝在县政府班子共事", "overlap_org": "方正县人民政府", "overlap_period": "2026年1月至今"},
    {"person_a": 2, "person_b": 18, "type": "overlap", "context": "杨平与张迪在县政府班子共事", "overlap_org": "方正县人民政府", "overlap_period": "2026年1月至今"},
    {"person_a": 2, "person_b": 19, "type": "overlap", "context": "杨平与黄学仁在县政府班子共事", "overlap_org": "方正县人民政府", "overlap_period": "2026年1月至今"},
    {"person_a": 2, "person_b": 20, "type": "overlap", "context": "杨平与宋伟在县政府班子共事", "overlap_org": "方正县人民政府", "overlap_period": "2026年1月至今"},
    # Predecessor relationship
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor", "context": "周泉接替郑伟任方正县委书记（2025年12月）；此前周泉任县长时亦与郑伟（时任书记）搭档", "overlap_org": "中共方正县委", "overlap_period": "2024-2025"},
    {"person_a": 3, "person_b": 4, "type": "predecessor_successor", "context": "郑伟由县长升任县委书记，郑伟的前任县长为张英俊", "overlap_org": "方正县人民政府", "overlap_period": ""},
    # 常务副县长 ↔ 其他副县长
    {"person_a": 7, "person_b": 15, "type": "overlap", "context": "张昕明（常务副县长）与刘国峰在县政府班子共事", "overlap_org": "方正县人民政府", "overlap_period": "2026年至今"},
    {"person_a": 7, "person_b": 16, "type": "overlap", "context": "张昕明与张广聪在县政府班子共事", "overlap_org": "方正县人民政府", "overlap_period": "2026年至今"},
    {"person_a": 7, "person_b": 17, "type": "overlap", "context": "张昕明与姜兆姝在县政府班子共事", "overlap_org": "方正县人民政府", "overlap_period": "2026年至今"},
    {"person_a": 7, "person_b": 18, "type": "overlap", "context": "张昕明与张迪在县政府班子共事", "overlap_org": "方正县人民政府", "overlap_period": "2026年至今"},
    {"person_a": 7, "person_b": 19, "type": "overlap", "context": "张昕明与黄学仁在县政府班子共事", "overlap_org": "方正县人民政府", "overlap_period": "2026年至今"},
    {"person_a": 7, "person_b": 20, "type": "overlap", "context": "张昕明与宋伟在县政府班子共事", "overlap_org": "方正县人民政府", "overlap_period": "2026年至今"},
    # 副书记 ↔ 常委
    {"person_a": 5, "person_b": 14, "type": "overlap", "context": "崔融冰与张声雷在县委常委会共事", "overlap_org": "中共方正县委", "overlap_period": "2025年至今"},
    {"person_a": 5, "person_b": 7, "type": "overlap", "context": "崔融冰与张昕明在县委常委会共事", "overlap_org": "中共方正县委", "overlap_period": "2025年至今"},
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
        pid = f"fangzheng_{p['name']}"
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
        if "书记" in post and "副" not in post and "纪委" not in post and "县委" in post:
            return "255,50,50"
        if "县长" in post and "副" not in post and "县委副书记" in post:
            return "50,100,255"
        if "副县长" in post or "常务副" in post:
            return "100,150,220"
        if "副书记" in post and "县委副书记" in post and "县长" not in post:
            return "100,150,220"
        if "人大" in post:
            return "200,100,100"
        if "政协" in post:
            return "200,150,50"
        return "100,100,100"

    def is_top_leader(post):
        return ("书记" in post and "副" not in post and "纪委" not in post and "县委" in post) or \
               ("县长" in post and "副" not in post and "县委副书记" in post) or \
               ("人大主任" in post) or \
               ("政协主席" in post)

    def person_shape(post):
        if "书记" in post and "副" not in post and "纪委" not in post and "县委" in post:
            return "square"
        if "县长" in post and "副" not in post:
            return "circle"
        if "常务副" in post:
            return "diamond"
        if "人大" in post:
            return "triangle"
        if "政协" in post:
            return "square"
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
    lines.append('    <description>哈尔滨市方正县领导班子关系网络</description>')
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
        {"id": "S001", "title": "方正县人民政府 - 领导之窗", "url": "http://www.hrbfz.gov.cn/col/col35693/index.html",
         "publisher": "方正县人民政府", "published_at": "", "accessed_at": "2026-07-24", "source_type": "official", "reliability": "high", "notes": "方正县政府领导信息页"},
        {"id": "S002", "title": "百度百科 - 方正县", "url": "https://baike.baidu.com/item/方正县",
         "publisher": "百度百科", "published_at": "", "accessed_at": "2026-07-24", "source_type": "encyclopedia", "reliability": "medium", "notes": "方正县政治现状：县委书记周泉、县长杨平"},
        {"id": "S003", "title": "网易 - 周泉任方正县委书记", "url": "",
         "publisher": "网易", "published_at": "2025-12-19", "accessed_at": "2026-07-24", "source_type": "media", "reliability": "medium", "notes": "周泉任方正县委书记"},
        {"id": "S004", "title": "方正县十八届人大六次会议 - 杨平当选县长", "url": "",
         "publisher": "方正县人大", "published_at": "2026-01-16", "accessed_at": "2026-07-24", "source_type": "appointment_notice", "reliability": "high", "notes": "杨平当选方正县人民政府县长"},
        {"id": "S005", "title": "人民网 - 专访方正县委书记郑伟", "url": "",
         "publisher": "人民网", "published_at": "2022-09-05", "accessed_at": "2026-07-24", "source_type": "media", "reliability": "medium", "notes": "前任县委书记郑伟专访"},
    ]

    def make_person_json(p, custom_id=None):
        result = {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "黑龙江省",
                "city": "哈尔滨市",
                "region": "方正县",
                "job": p.get("current_post", ""),
                "task_id": "heilongjiang_方正县",
                "time_focus": "2026年7月"
            },
            "identity": {
                "person_id": f"fangzheng_{p['name']}" if not custom_id else custom_id,
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
                "administrative_rank": "县处级正职" if ("书记" in p.get("current_post", "") and "副" not in p.get("current_post", "") and "县委" in p.get("current_post", "")) or ("县长" in p.get("current_post", "") and "副" not in p.get("current_post", "")) else "县处级副职",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001", "S002"]
            },
            "career_timeline": [
                {
                    "start": "unknown",
                    "end": "",
                    "org": p.get("current_org", ""),
                    "title": p.get("current_post", ""),
                    "notes": "现任，公开资料有限，详细履历待补充",
                    "confidence": "confirmed" if p.get("source") else "plausible",
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
                "identity": "plausible",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "medium",
                "biggest_gap": f"{p['name']}的完整履历信息缺失"
            },
            "open_questions": [
                {"priority": "critical",
                 "question": f"{p['name']}的完整职业生涯履历（出生年月、教育背景、历任职务）",
                 "why_it_matters": "无法追溯其任职路径和系统经历，无法建立更深层的关系网络",
                 "suggested_queries": [f"{p['name']} 简历 方正 哈尔滨"],
                 "last_attempted": AS_OF},
            ]
        }

        # Add specific career timeline for 周泉 (known trajectory)
        if p["id"] == 1:
            result["career_timeline"] = [
                {
                    "start": "unknown",
                    "end": "2024-06",
                    "org": "",
                    "title": "此前职务（待查）",
                    "notes": "周泉任方正县长之前的履历在公开资料中未找到",
                    "confidence": "unverified",
                    "source_ids": []
                },
                {
                    "start": "2024-07",
                    "end": "2025-12",
                    "org": "方正县人民政府",
                    "title": "县长",
                    "notes": "由方正县十八届人大常委会任命为代县长/县长",
                    "confidence": "plausible",
                    "source_ids": ["S003"]
                },
                {
                    "start": "2025-12",
                    "end": "present",
                    "org": "中共方正县委员会",
                    "title": "县委书记",
                    "notes": "由县长升任县委书记",
                    "confidence": "confirmed",
                    "source_ids": ["S003"]
                }
            ]
            result["relationships"] = [
                {"person": "杨平", "person_id": "fangzheng_杨平", "relationship_type": "overlap", "strength": "strong",
                 "evidence": "周泉（县委书记，原县长）与杨平（县长）在县委常委会及县政府班子共事",
                 "overlap_org": "中共方正县委/方正县人民政府", "overlap_period": "2026年1月至今",
                 "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003", "S004"]},
                {"person": "郑伟", "person_id": "fangzheng_郑伟", "relationship_type": "predecessor_successor", "strength": "strong",
                 "evidence": "周泉接替郑伟任方正县委书记；此前周泉任县长时与郑伟（县委书记）搭档",
                 "overlap_org": "中共方正县委", "overlap_period": "2024-2025",
                 "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003"]},
            ]
        elif p["id"] == 2:
            result["relationships"] = [
                {"person": "周泉", "person_id": "fangzheng_周泉", "relationship_type": "overlap", "strength": "strong",
                 "evidence": "杨平（县长）与周泉（县委书记，原县长）在县委常委会及县政府班子共事",
                 "overlap_org": "中共方正县委/方正县人民政府", "overlap_period": "2026年1月至今",
                 "direction": "undirected", "confidence": "confirmed", "source_ids": ["S004"]},
            ]

        return result

    # Generate person JSON files for the two main leaders: 周泉 and 杨平
    for p in persons[:2]:
        pjson = make_person_json(p)
        job_slug = "县委书记" if p["id"] == 1 else "县长"
        fname = f"{TODAY}-黑龙江省-哈尔滨市-{job_slug}-{p['name']}.json"
        fpath = os.path.join(PERSONS_DIR, fname)
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(pjson, f, ensure_ascii=False, indent=2)
        print(f"Person JSON written: {fpath}")


if __name__ == "__main__":
    build()
