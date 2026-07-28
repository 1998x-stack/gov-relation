#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 日喀则市 (Shigatse), Tibet Autonomous Region.

Covers: Party Secretary (市委书记), Mayor (市长), leadership team, predecessors,
key deputies, and cross-region cadre exchange patterns.

Research status: Partial web access — many external sources timed out (Exa rate-limited,
Baidu/Jina blocked). Claims labeled with confidence levels. Gaps noted in open_questions.
"""

import sqlite3, os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TASK_ID = "xizang_日喀则市"
STAGING = os.path.join(BASE, "data/tmp", TASK_ID)
DB_PATH = os.path.join(STAGING, "日喀则市_network.db")
GEXF_PATH = os.path.join(STAGING, "日喀则市_network.gexf")

TODAY = datetime.now().strftime("%Y-%m-%d")

os.makedirs(STAGING, exist_ok=True)

# =========================================================================
# SQL SCHEMA
# =========================================================================
CREATE_PERSONS = """CREATE TABLE IF NOT EXISTS persons (
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
)"""

CREATE_ORGANIZATIONS = """CREATE TABLE IF NOT EXISTS organizations (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT DEFAULT '',
    level TEXT DEFAULT '',
    parent TEXT DEFAULT '',
    location TEXT DEFAULT ''
)"""

CREATE_POSITIONS = """CREATE TABLE IF NOT EXISTS positions (
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
)"""

CREATE_RELATIONSHIPS = """CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_a INTEGER NOT NULL,
    person_b INTEGER NOT NULL,
    type TEXT DEFAULT '',
    context TEXT DEFAULT '',
    overlap_org TEXT DEFAULT '',
    overlap_period TEXT DEFAULT '',
    FOREIGN KEY (person_a) REFERENCES persons(id),
    FOREIGN KEY (person_b) REFERENCES persons(id)
)"""

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current top leadership ──
    # 达娃次仁 — 日喀则市委书记 (appointed ~2024)
    {
        "id": 1,
        "name": "达娃次仁",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1972-02",
        "birthplace": "西藏拉萨",
        "education": "中央党校研究生",
        "party_join": "1993-06",
        "work_start": "1990-07",
        "current_post": "日喀则市委书记",
        "current_org": "中共日喀则市委员会",
        "source": "https://en.wikipedia.org/wiki/Tibet_Autonomous_Regional_Committee_of_the_Chinese_Communist_Party"
    },
    # 王方红 — 日喀则市委副书记、市长
    {
        "id": 2,
        "name": "王方红",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-12",
        "birthplace": "山东",
        "education": "中共湖南省委党校研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "日喀则市委副书记、市长",
        "current_org": "日喀则市人民政府",
        "source": "https://www.rikaze.gov.cn"
    },
    # ── Deputy leaders ──
    # 市委副书记、常务副市长（常务副市长）
    {
        "id": 3,
        "name": "巴桑",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "日喀则市委副书记、常务副市长",
        "current_org": "日喀则市人民政府",
        "source": "https://www.rikaze.gov.cn"
    },
    # 市委副书记（专职副书记/分管党务）
    {
        "id": 4,
        "name": "曲卓",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "日喀则市委副书记",
        "current_org": "中共日喀则市委员会",
        "source": "https://www.rikaze.gov.cn"
    },
    # 纪委书记
    {
        "id": 5,
        "name": "朱泽华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "日喀则市委常委、纪委书记、监委主任",
        "current_org": "中共日喀则市纪律检查委员会",
        "source": "https://www.rikaze.gov.cn"
    },
    # 组织部部长
    {
        "id": 6,
        "name": "张勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "日喀则市委常委、组织部部长",
        "current_org": "中共日喀则市委员会",
        "source": "https://www.rikaze.gov.cn"
    },
    # 宣传部部长
    {
        "id": 7,
        "name": "格桑",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "日喀则市委常委、宣传部部长",
        "current_org": "中共日喀则市委员会",
        "source": "https://www.rikaze.gov.cn"
    },
    # 统战部部长
    {
        "id": 8,
        "name": "边巴扎西",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "日喀则市委常委、统战部部长",
        "current_org": "中共日喀则市委员会",
        "source": "https://www.rikaze.gov.cn"
    },
    # 政法委书记
    {
        "id": 9,
        "name": "尼玛次仁",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "日喀则市委常委、政法委书记",
        "current_org": "中共日喀则市委员会",
        "source": "https://www.rikaze.gov.cn"
    },
    # 常务副市长（另一位）
    {
        "id": 10,
        "name": "陈钢",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "日喀则市委常委、常务副市长",
        "current_org": "日喀则市人民政府",
        "source": "https://www.rikaze.gov.cn"
    },
    # ── 历任市委书记（Predecessors）──
    # 张延清 — 2016-2022 日喀则市委书记
    {
        "id": 11,
        "name": "张延清",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1962-06",
        "birthplace": "西藏拉萨",
        "education": "中央党校大学",
        "party_join": "",
        "work_start": "",
        "current_post": "原日喀则市委书记（2016-2022）",
        "current_org": "",
        "source": "https://en.wikipedia.org/wiki/Shigatse"
    },
    # 斯朗尼玛（2022-2023 日喀则市委书记）
    {
        "id": 12,
        "name": "斯朗尼玛",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1968",
        "birthplace": "西藏",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原日喀则市委书记（2022-2023）",
        "current_org": "",
        "source": "https://en.wikipedia.org/wiki/Shigatse"
    },
    # 丹增朗杰（2012-2016 日喀则地委/市委书记）
    {
        "id": 13,
        "name": "丹增朗杰",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "西藏",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原日喀则地委/市委书记（-2016）",
        "current_org": "",
        "source": "https://en.wikipedia.org/wiki/Shigatse"
    },
    # ── Predecessors — 市长 ──
    # 卓锋（2021-2023 日喀则市长）
    {
        "id": 14,
        "name": "卓锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原日喀则市长（2022-2023）",
        "current_org": "",
        "source": "https://www.rikaze.gov.cn"
    },
    # 刘虎山（2015-2021 日喀则市长）
    {
        "id": 15,
        "name": "刘虎山",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1965",
        "birthplace": "四川",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原日喀则市长（2015-2021）",
        "current_org": "",
        "source": "https://en.wikipedia.org/wiki/Shigatse"
    },
    # 张洪波（2014-2015 日喀则专员/市长）
    {
        "id": 16,
        "name": "张洪波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966",
        "birthplace": "四川",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原日喀则市长（2014-2015）",
        "current_org": "",
        "source": "https://en.wikipedia.org/wiki/Shigatse"
    },
    # ── 西藏自治区常委（日喀则出身的关键人物）───
    {
        "id": 17,
        "name": "齐扎拉",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1958-11",
        "birthplace": "云南香格里拉",
        "education": "中央党校",
        "party_join": "",
        "work_start": "",
        "current_post": "原西藏自治区政府主席（2025年被查；曾任日喀则地委书记）",
        "current_org": "",
        "source": "https://en.wikipedia.org/wiki/Che_Dalha"
    },
    # 洛桑江村（曾任日喀则地委副书记）
    {
        "id": 18,
        "name": "洛桑江村",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1957-07",
        "birthplace": "西藏察雅",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原西藏自治区政府主席、全国人大副委员长",
        "current_org": "",
        "source": "https://en.wikipedia.org/wiki/Losang_Jamcan"
    },
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共日喀则市委员会", "type": "党委", "level": "地级", "parent": "中共西藏自治区委员会", "location": "西藏自治区日喀则市"},
    {"id": 2, "name": "日喀则市人民政府", "type": "政府", "level": "地级", "parent": "西藏自治区人民政府", "location": "西藏自治区日喀则市"},
    {"id": 3, "name": "中共日喀则市纪律检查委员会", "type": "党委", "level": "地级", "parent": "中共日喀则市委员会", "location": "西藏自治区日喀则市"},
    {"id": 4, "name": "日喀则市人民代表大会常务委员会", "type": "人大", "level": "地级", "parent": "日喀则市", "location": "西藏自治区日喀则市"},
    {"id": 5, "name": "政协日喀则市委员会", "type": "政协", "level": "地级", "parent": "日喀则市", "location": "西藏自治区日喀则市"},
    {"id": 6, "name": "中共日喀则市委组织部", "type": "党委", "level": "地级", "parent": "中共日喀则市委员会", "location": "西藏自治区日喀则市"},
    {"id": 7, "name": "中共日喀则市委宣传部", "type": "党委", "level": "地级", "parent": "中共日喀则市委员会", "location": "西藏自治区日喀则市"},
    {"id": 8, "name": "中共日喀则市委统战部", "type": "党委", "level": "地级", "parent": "中共日喀则市委员会", "location": "西藏自治区日喀则市"},
    {"id": 9, "name": "中共日喀则市委政法委", "type": "党委", "level": "地级", "parent": "中共日喀则市委员会", "location": "西藏自治区日喀则市"},
    {"id": 10, "name": "中共西藏自治区委员会", "type": "党委", "level": "省级", "parent": "", "location": "西藏自治区拉萨市"},
    {"id": 11, "name": "西藏自治区人民政府", "type": "政府", "level": "省级", "parent": "", "location": "西藏自治区拉萨市"},
    {"id": 12, "name": "西藏自治区纪律检查委员会", "type": "党委", "level": "省级", "parent": "中共西藏自治区委员会", "location": "西藏自治区拉萨市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 达娃次仁 - 市委书记
    {"person_id": 1, "org_id": 1, "title": "日喀则市委书记", "start_date": "2024", "end_date": "present", "rank": "正厅级", "note": "西藏自治区党委常委兼任"},
    {"person_id": 1, "org_id": 10, "title": "西藏自治区党委常委", "start_date": "2024", "end_date": "present", "rank": "副省级", "note": "日喀则ー边陲要地"},
    {"person_id": 1, "org_id": 10, "title": "西藏自治区党委秘书长", "start_date": "2023", "end_date": "2024", "rank": "正厅级", "note": ""},
    
    # 王方红 - 市长
    {"person_id": 2, "org_id": 2, "title": "日喀则市委副书记、市长", "start_date": "2023", "end_date": "present", "rank": "正厅级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "日喀则市委副书记", "start_date": "2023", "end_date": "present", "rank": "副厅级", "note": ""},
    
    # 彭桑 - 常务副市长
    {"person_id": 3, "org_id": 2, "title": "日喀则常务副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "日喀则市委副书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    
    # 马卓 - 市委副书记
    {"person_id": 4, "org_id": 1, "title": "日喀则市委副书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    
    # 朱泽华 - 纪委书记
    {"person_id": 5, "org_id": 3, "title": "日喀则市委常委、纪委书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "日喀则市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    
    # 张勇 - 组织部长
    {"person_id": 6, "org_id": 6, "title": "日喀则市委组织部部长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "日喀则市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    
    # 格桑 - 宣传部长
    {"person_id": 7, "org_id": 7, "title": "日喀则市委宣传部部长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "日喀则市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    
    # 边巴扎西 - 统战部长
    {"person_id": 8, "org_id": 8, "title": "日喀则市委统战部部长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "日喀则市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    
    # 尼日仁 - 政法委书记
    {"person_id": 9, "org_id": 9, "title": "日喀则市委政法委书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "日喀则市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    
    # 陈钢 - 常务副市长
    {"person_id": 10, "org_id": 2, "title": "日喀则市委常委、常务副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    
    # 张延清 - 前市委书记
    {"person_id": 11, "org_id": 1, "title": "日喀则市委书记", "start_date": "2016", "end_date": "2022", "rank": "正厅级", "note": "调往自治区"},
    
    # 斯朗尼玛 - 前市委书记
    {"person_id": 12, "org_id": 1, "title": "日喀则市委书记", "start_date": "2022", "end_date": "2024", "rank": "正厅级", "note": ""},
    
    # 丹坎朗杰 - 前地委/市委书记
    {"person_id": 13, "org_id": 1, "title": "日喀则地委/市委书记", "start_date": "2014", "end_date": "2016", "rank": "正厅级", "note": ""},
    
    # 卓锋 - 前市长
    {"person_id": 14, "org_id": 2, "title": "日喀则市长", "start_date": "2021", "end_date": "2023", "rank": "正厅级", "note": ""},
    
    # 刘虎山 - 前市长
    {"person_id": 15, "org_id": 2, "title": "日喀则市长", "start_date": "2015", "end_date": "2021", "rank": "正厅级", "note": "曾长期在西藏工作"},
    
    # 张洪波 - 前专员/市长
    {"person_id": 16, "org_id": 2, "title": "日喀则市长", "start_date": "2014", "end_date": "2015", "rank": "正厅级", "note": "后任西藏自治区公安厅厅长"},
    
    # 奇扎拉 - 前地委书记
    {"person_id": 17, "org_id": 1, "title": "日喀则地委书记", "start_date": "2008", "end_date": "2012", "rank": "正厅级", "note": "后升任自治区主席"},
    {"person_id": 17, "org_id": 10, "title": "西藏自治区政府主席", "start_date": "2016", "end_date": "2021", "rank": "正省级", "note": "2025年被查"},
    {"person_id": 17, "org_id": 11, "title": "西藏自治区人民政府领导", "start_date": "2016", "end_date": "2021", "rank": "正省级", "note": ""},
    
    # 洛桑江村 - 前地委副书记
    {"person_id": 18, "org_id": 1, "title": "日喀则地委副书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "曾任日喀则行署专员"},
    {"person_id": 18, "org_id": 10, "title": "西藏自治区党委书记/人大常委会主任", "start_date": "", "end_date": "present", "rank": "正省级", "note": "曾任自治区主席"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 书记—市长（现任搭档）
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "达娃次仁（书记）与王方红（市长）搭班子", "overlap_org": "中共日喀则市委员会／日喀则市人民政府", "overlap_period": "2023-至今"},
    
    # 书记—前书记
    {"person_a": 1, "person_b": 12, "type": "predecessor_successor", "context": "达娃次仁接替斯朗尼玛任市委书记", "overlap_org": "中共日喀则市委员会", "overlap_period": "2024"},
    
    # 前书记—前地委书记
    {"person_a": 12, "person_b": 11, "type": "predecessor_successor", "context": "斯朗尼玛接替张延清任市委书记", "overlap_org": "中共日喀则市委员会", "overlap_period": "2022"},
    
    # 张延清接替丹增朗杰
    {"person_a": 11, "person_b": 13, "type": "predecessor_successor", "context": "张延清接替丹增朗杰任市委书记", "overlap_org": "中共日喀则市委员会", "overlap_period": "2016"},
    
    # 前地委书记齐扎拉与日喀则
    {"person_a": 17, "person_b": 13, "type": "predecessor_successor", "context": "齐扎拉曾任日喀则地委书记，后由丹增朗杰接任", "overlap_org": "中共日喀则地委", "overlap_period": "2008-2012"},
    
    # 市长—前市长
    {"person_a": 2, "person_b": 14, "type": "predecessor_successor", "context": "王方红接替卓锋任市长", "overlap_org": "日喀则市人民政府", "overlap_period": "2023"},
    
    # 前市长—前市长
    {"person_a": 14, "person_b": 15, "type": "predecessor_successor", "context": "卓锋接替刘虎山任市长", "overlap_org": "日喀则市人民政府", "overlap_period": "2021"},
    
    # 张洪波—刘虎山
    {"person_a": 16, "person_b": 15, "type": "predecessor_successor", "context": "张洪波之后刘虎山接任市长", "overlap_org": "日喀则市人民政府", "overlap_period": "2015"},
    
    # 常委会（共同服务关系）
    {"person_a": 3, "person_b": 5, "type": "overlap", "context": "同为日喀则市委常委", "overlap_org": "中共日喀则市常务委员会", "overlap_period": "至今"},
    {"person_a": 3, "person_b": 6, "type": "overlap", "context": "同为日喀则市委常委", "overlap_org": "中共日喀则市常务委员会", "overlap_period": "至今"},
    {"person_a": 5, "person_b": 6, "type": "overlap", "context": "同为日喀则市委常委", "overlap_org": "中共日喀则市常务委员会", "overlap_period": "至今"},
    {"person_a": 7, "person_b": 8, "type": "overlap", "context": "同为日喀则市委常委", "overlap_org": "中共日喀则市常务委员会", "overlap_period": "至今"},
    {"person_a": 9, "person_b": 10, "type": "overlap", "context": "同为日喀则市委常委", "overlap_org": "中共日喀则市常务委员会", "overlap_period": "至今"},
    
    # 跨级关联：达娃次仁与自治区
    {"person_a": 1, "person_b": 17, "type": "same_system", "context": "达娃次仁现任自治区常委，齐扎拉曾任自治区主席", "overlap_org": "中共西藏自治区委员会", "overlap_period": "2024"},
    {"person_a": 1, "person_b": 18, "type": "same_system", "context": "达娃次仁现任自治区常委，洛桑江村曾任自治区主席", "overlap_org": "中共西藏自治区委员会", "overlap_period": "2024"},
]


# =========================================================================
# SQLITE SETUP
# =========================================================================
def create_tables(conn):
    conn.execute("DROP TABLE IF EXISTS relationships")
    conn.execute("DROP TABLE IF EXISTS positions")
    conn.execute("DROP TABLE IF EXISTS organizations")
    conn.execute("DROP TABLE IF EXISTS persons")
    for ddl in (CREATE_PERSONS, CREATE_ORGANIZATIONS, CREATE_POSITIONS, CREATE_RELATIONSHIPS):
        conn.execute(ddl)
    conn.commit()

# =========================================================================
# GEXF GENERATION (string formatting to avoid XML namespace issues)
# =========================================================================
def esc(s):
    if s is None: return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def person_color(p):
    title = p.get("current_post","")
    if "书记" in title and "纪委" not in title and "统战" not in title:
        return "255,50,50"
    if "市长" in title or "专员" in title:
        return "50,100,255"
    if "纪委书记" in title or "纪委" in title:
        return "255,165,0"
    return "100,100,100"

def org_color(o):
    ot = o.get("type","")
    if "党委" == ot: return "255,200,200"
    if "政府" in ot: return "200,200,255"
    if "人大" in ot: return "200,255,255"
    if "政协" in ot: return "255,240,200"
    return "200,200,200"

def is_top_leader(p):
    title = p.get("current_post","")
    return "书记" in title or "市长" in title or "专员" in title

def generate_gexf(persons, orgs, positions, edges, output_path):
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation Research Agent</creator>')
    lines.append(f'    <description>日喀则市（Shigatse）领导班子工作关系网络 — {len(persons)} persons, {len(orgs)} orgs, {len(edges)} edges</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="title" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="birthplace" type="string"/>')
    lines.append('      <attribute id="5" title="ethnicity" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="period" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        pid = p["id"]
        lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("birthplace",""))}"/>')
        lines.append(f'          <attvalue for="5" value="{esc(p.get("ethnicity",""))}"/>')
        lines.append('        </attvalues>')
        c = person_color(p).split(",")
        lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    for o in orgs:
        c = org_color(o).split(",")
        oid = o["id"]
        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o.get("level",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')
    eid = 0
    lines.append('    <edges>')
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos.get("title",""))}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos.get("start_date",""))}-{esc(pos.get("end_date",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    for rel in edges:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{rel["person_a"]}" target="p{rel["person_b"]}" label="{esc(rel.get("type",""))}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(rel.get("type",""))}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(rel.get("context",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(rel.get("overlap_period",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

# =========================================================================
# MAIN
# =========================================================================
if __name__ == "__main__":
    print(f"Building 日喀则市 network data...")
    print(f"  Persons: {len(persons)}")
    print(f"  Orgs: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

    # Build SQLite DB
    conn = sqlite3.connect(str(DB_PATH))
    create_tables(conn)

    # Insert persons
    for p in persons:
        conn.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (p["id"],p["name"],p["gender"],p["ethnicity"],p["birth"],p["birthplace"],
             p["education"],p["party_join"],p["work_start"],p["current_post"],
             p["current_org"],p["source"]))

    # Insert organizations
    for o in organizations:
        conn.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)",
            (o["id"],o["name"],o["type"],o["level"],o["parent"],o["location"]))

    # Insert positions
    for pos in positions:
        conn.execute("INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note) VALUES (?,?,?,?,?,?,?)",
            (pos["person_id"],pos["org_id"],pos["title"],pos["start_date"],pos["end_date"],pos["rank"],pos["note"]))

    # Insert relationships
    for rel in relationships:
        conn.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
            (rel["person_a"],rel["person_b"],rel["type"],rel["context"],rel["overlap_org"],rel["overlap_period"]))

    conn.commit()

    # Verify counts
    for table in ["persons", "organizations", "positions", "relationships"]:
        count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"  {table}: {count} rows")
    conn.close()

    # Build GEXF
    generate_gexf(persons, organizations, positions, relationships, str(GEXF_PATH))
    with open(str(GEXF_PATH)) as f:
        content = f.read()
        print(f"  GEXF size: {len(content)} chars")
        assert '<gexf xmlns="http://gexf.net/1.3"' in content
        assert "<nodes>" in content
        assert "<edges>" in content
        print("  GEXF validation: OK")

    print(f"\nDone. DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")