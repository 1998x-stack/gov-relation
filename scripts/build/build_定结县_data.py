#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 定结县 (Dinggyê County), 日喀则市, 西藏自治区.

Current officeholders as of 2026-07:
  - Party Secretary (县委书记): 陶明君 (also 日喀则市政协副主席, 副厅级)
  - County Mayor (县长): 次琼 (县委副书记)
  - Standing Committee (县委常委): includes 陶明君, 次琼, 李刚, 杨红, 普布次仁, 赵晨曦, 莫向波

Source: 定结县人民政府官网 (http://www.djx.gov.cn/), Baidu Baike, 县人大公告 (2026-07)
"""

import sqlite3, os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TASK_ID = "xizang_定结县"
STAGING = os.path.join(BASE, "data/tmp", TASK_ID)
DB_PATH = os.path.join(STAGING, "定结县_network.db")
GEXF_PATH = os.path.join(STAGING, "定结县_network.gexf")

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
    # ── Top leadership ──
    # 陶明君 — 定结县委书记（兼日喀则市政协副主席，副厅级）
    {
        "id": 1,
        "name": "陶明君",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-10",
        "birthplace": "重庆市",
        "education": "自治区党委党校研究生",
        "party_join": "2000-03",
        "work_start": "1998-07",
        "current_post": "定结县委书记、日喀则市政协副主席",
        "current_org": "中共定结县委员会",
        "source": "https://baike.baidu.com/item/%E9%99%B6%E6%98%8E%E5%90%9B/59354518"
    },
    # 次琼 — 定结县委副书记、县长
    {
        "id": 2,
        "name": "次琼",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "定结县委副书记、县长",
        "current_org": "定结县人民政府",
        "source": "http://www.djx.gov.cn/goverment-leaders.thtml?id=12150"
    },
    # 李刚 — 常务副县长（吉林长春援藏干部）
    {
        "id": 3,
        "name": "李刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "定结县委常委、常务副县长",
        "current_org": "定结县人民政府",
        "source": "http://www.djx.gov.cn/goverment-leaders.thtml?id=12150"
    },
    # 杨红 — 县委常委、组织部部长
    {
        "id": 4,
        "name": "杨红",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "定结县委常委、组织部部长",
        "current_org": "中共定结县委组织部",
        "source": "http://www.djx.gov.cn/"
    },
    # ── 副县长（县委常委兼任）──
    # 普布次仁 — 县委常委、副县长
    {
        "id": 5,
        "name": "普布次仁",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "定结县委常委、副县长",
        "current_org": "定结县人民政府",
        "source": "http://www.djx.gov.cn/goverment-leaders.thtml?id=12150"
    },
    # 赵晨曦 — 县委常委、副县长（吉林长春援藏干部）
    {
        "id": 6,
        "name": "赵晨曦",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "定结县委常委、副县长",
        "current_org": "定结县人民政府",
        "source": "http://www.djx.gov.cn/goverment-leaders.thtml?id=12150"
    },
    # 莫向波 — 县委常委、副县长
    {
        "id": 7,
        "name": "莫向波",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "定结县委常委、副县长",
        "current_org": "定结县人民政府",
        "source": "http://www.djx.gov.cn/goverment-leaders.thtml?id=12150"
    },
    # ── 副县长（非常委）──
    {
        "id": 8,
        "name": "尼琼",
        "gender": "女",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "定结县副县长",
        "current_org": "定结县人民政府",
        "source": "http://www.djx.gov.cn/goverment-leaders.thtml?id=12150"
    },
    {
        "id": 9,
        "name": "次仁顿珠",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "定结县副县长",
        "current_org": "定结县人民政府",
        "source": "http://www.djx.gov.cn/goverment-leaders.thtml?id=12150"
    },
    {
        "id": 10,
        "name": "索朗旺堆",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "定结县副县长",
        "current_org": "定结县人民政府",
        "source": "http://www.djx.gov.cn/goverment-leaders.thtml?id=12150"
    },
    {
        "id": 11,
        "name": "胡锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "定结县副县长",
        "current_org": "定结县人民政府",
        "source": "http://www.djx.gov.cn/goverment-leaders.thtml?id=12150"
    },
    {
        "id": 12,
        "name": "汪吉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "定结县副县长",
        "current_org": "定结县人民政府",
        "source": "http://www.djx.gov.cn/goverment-leaders.thtml?id=12150"
    },
    {
        "id": 13,
        "name": "李霞",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "定结县副县长",
        "current_org": "定结县人民政府",
        "source": "http://www.djx.gov.cn/goverment-leaders.thtml?id=12150"
    },
    # ── 人大常委会 ──
    {
        "id": 14,
        "name": "李辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "定结县人大常委会主任",
        "current_org": "定结县人大常委会",
        "source": "http://www.djx.gov.cn/（县人大公告2026-07-06）"
    },
    {
        "id": 15,
        "name": "巴桑",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "定结县人大常委会副主任",
        "current_org": "定结县人大常委会",
        "source": "http://www.djx.gov.cn/（县人大公告2026-07-06）"
    },
    {
        "id": 16,
        "name": "赵俊峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "定结县人大常委会副主任",
        "current_org": "定结县人大常委会",
        "source": "http://www.djx.gov.cn/（县人大公告2026-07-06）"
    },
    {
        "id": 17,
        "name": "格桑扎西",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "定结县人大常委会副主任",
        "current_org": "定结县人大常委会",
        "source": "http://www.djx.gov.cn/（县人大公告2026-07-06）"
    },
    {
        "id": 18,
        "name": "达顿",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "定结县人大常委会副主任",
        "current_org": "定结县人大常委会",
        "source": "http://www.djx.gov.cn/（县人大公告2026-07-06）"
    },
    # ── 监察委、法院、检察院 ──
    {
        "id": 19,
        "name": "李洪涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "定结县监察委员会主任",
        "current_org": "定结县监察委员会",
        "source": "http://www.djx.gov.cn/（定结县人民当公告2026-07-06）"
    },
    {
        "id": 20,
        "name": "拉加",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "定结县人民法院院长",
        "current_org": "定结县人民法院",
        "source": "http://www.djx.gov.cn/（定结县人民当公告2026-07-06）"
    },
    {
        "id": 21,
        "name": "祁海燕",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "定结县人民检察院检察长",
        "current_org": "定结县人民检察院",
        "source": "http://www.djx.gov.cn/（定结县人民:公告2026-07-06）"
    },
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共定结县委员会", "type": "党委", "level": "县级", "parent": "中共日喀则市委", "location": "西藏自治区日喀则市定结县"},
    {"id": 2, "name": "定结县人民政府", "type": "政府", "level": "县级", "parent": "日喀则市人民政府", "location": "西藏自治区日喀则市定结县"},
    {"id": 3, "name": "定结县人大常委会", "type": "人大", "level": "县级", "parent": "定结县", "location": "西藏自治区日喀则市定结县"},
    {"id": 4, "name": "政协定结县委员会", "type": "政协", "level": "县级", "parent": "定结县", "location": "西藏自治区日喀则市定结县"},
    {"id": 5, "name": "中共定结县纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共定结县委员会", "location": "西藏自治区日喀则市定结县"},
    {"id": 6, "name": "定结县监察委员会", "type": "政府", "level": "县级", "parent": "定结县", "location": "西藏自治区日喀则市定结县"},
    {"id": 7, "name": "定结县人民法院", "type": "政府", "level": "县级", "parent": "定结县", "location": "西藏自治区日喀则市定结县"},
    {"id": 8, "name": "定结县人民检察院", "type": "政府", "level": "县级", "parent": "定结县", "location": "西藏自治区日喀则市定结县"},
    {"id": 9, "name": "中共定结县委组织部", "type": "党委", "level": "县级", "parent": "中共定结县委员会", "location": "西藏自治区日喀则市定结县"},
    {"id": 10, "name": "日喀则市政协", "type": "政协", "level": "地级", "parent": "日喀则市", "location": "西藏自治区日喀则市"},
    {"id": 11, "name": "岗巴县委组织部", "type": "党委", "level": "县级", "parent": "中共岗巴县委", "location": "西藏自治区日喀则市岗巴县"},
    {"id": 12, "name": "江孜县委组织部", "type": "党委", "level": "县级", "parent": "中共江孜县委", "location": "西藏自治区日喀则市江孜县"},
    {"id": 13, "name": "日喀则市文化局", "type": "政府", "level": "地级", "parent": "日喀则市人民政府", "location": "西藏自治区日喀则市"},
    {"id": 14, "name": "中共日喀则市委宣传部", "type": "党委", "level": "地级", "parent": "中共日喀则市委", "location": "西藏自治区日喀则市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 陶明君
    {"person_id": 1, "org_id": 1, "title": "定结县委书记", "start_date": "2021-06", "end_date": "present", "rank": "正县", "note": ""},
    {"person_id": 1, "org_id": 10, "title": "日喀则市政协副主席", "start_date": "2026-01", "end_date": "present", "rank": "副厅级", "note": "兼任"},
    {"person_id": 1, "org_id": 11, "title": "岗巴县委常委、组织部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": "早期职务"},
    {"person_id": 1, "org_id": 12, "title": "江孜县委副书记、组织部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 13, "title": "日喀则地区文化局党组副书记、副局长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 14, "title": "日喀则市委宣传部副部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 13, "title": "日喀则市文化局党组书记、副局长", "start_date": "", "end_date": "2021-06", "rank": "正处级", "note": ""},

    # 次琼 — 县长
    {"person_id": 2, "org_id": 2, "title": "定结县县长", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "定结县委副书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},

    # 李刚 — 常务副县长
    {"person_id": 3, "org_id": 2, "title": "定结县委常委、常务副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "吉林省长春市第九批援藏干部"},

    # 杨红 — 组织部部长
    {"person_id": 4, "org_id": 9, "title": "定结县委组织部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "定结县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},

    # 普布次仁 — 常委副县长
    {"person_id": 5, "org_id": 2, "title": "定结县委常委、副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},

    # 赵晨曦 — 常委副县长
    {"person_id": 6, "org_id": 2, "title": "定结县委常委、副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "吉林省长春市第九批援藏干部"},

    # 莫向波 — 常委副县长
    {"person_id": 7, "org_id": 2, "title": "定结县委常委、副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},

    # 非常委副县长
    {"person_id": 8, "org_id": 2, "title": "定结县副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "定结县副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "定结县副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "定结县副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "定结县副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "定结县副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},

    # 人大常委会
    {"person_id": 14, "org_id": 3, "title": "定结县人大常委会主任", "start_date": "2026-07", "end_date": "present", "rank": "正处级", "note": "2026年7月县人大换届当选"},
    {"person_id": 15, "org_id": 3, "title": "定结县人大常委会副主任", "start_date": "2026-07", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 16, "org_id": 3, "title": "定结县人大常委会副主任", "start_date": "2026-07", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 17, "org_id": 3, "title": "定结县人大常委会副主任", "start_date": "2026-07", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 18, "org_id": 3, "title": "定结县人大常委会副主任", "start_date": "2026-07", "end_date": "present", "rank": "副处级", "note": ""},

    # 监察委法院检察院
    {"person_id": 19, "org_id": 6, "title": "定结县监察委员会主任", "start_date": "2026-07", "end_date": "present", "rank": "副处级", "note": "县人大2026-07-06选举"},
    {"person_id": 20, "org_id": 7, "title": "定结县人民法院院长", "start_date": "2026-07", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 21, "org_id": 8, "title": "定结县人民检察院检察长", "start_date": "2026-07", "end_date": "present", "rank": "副处级", "note": ""},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 书记—县长（当前搭档）
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "陶明君（书记）与次琼（县长）搭班子", "overlap_org": "中共定结县委员会/定结县人民政府", "overlap_period": "至今"},

    # 书记—常务副县长（援藏干部）
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "陶明君（书记）与李刚（常务副县长援藏干部）共事", "overlap_org": "中共定结县委员会", "overlap_period": "至今"},

    # 书记—组织部长
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "陶明君（书记）与杨红（组织部长）——组织人事归口", "overlap_org": "中共定结县常务委员会", "overlap_period": "至今"},

    # 县长—常务副县长
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "次琼（县长）与李刚（常务副县长）直接上下级", "overlap_org": "定结县人民政府", "overlap_period": "至今"},

    # 县长—常务委员（共同服务）
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "同为县委常委", "overlap_org": "中共定结县常务委员会", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 6, "type": "overlap", "context": "同为县委常委", "overlap_org": "中共定结县常务委员会", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 7, "type": "overlap", "context": "同为县委常委", "overlap_org": "中共定结县常务委员会", "overlap_period": "至今"},

    # 书记—人大主任
    {"person_a": 1, "person_b": 14, "type": "overlap", "context": "县委与人大主要领导", "overlap_org": "定结县", "overlap_period": "至今"},

    # 杨红（组织部长）—常委会集体
    {"person_a": 4, "person_b": 5, "type": "overlap", "context": "同为县委常委", "overlap_org": "中共定结县常务委员会", "overlap_period": "至今"},
    {"person_a": 4, "person_b": 6, "type": "overlap", "context": "同为县委常委", "overlap_org": "中共定结县常务委员会", "overlap_period": "至今"},
    {"person_a": 4, "person_b": 7, "type": "overlap", "context": "同为县委常委", "overlap_org": "中共定结县常务委员会", "overlap_period": "至今"},

    # 陶明君—前任相关（早期组织系统工作交集）
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "陶明君曾任县委组织部长，熟悉干部管理系统", "overlap_org": "西藏自治区组织系统", "overlap_period": ""},
]

# =========================================================================
# GENERATION
# =========================================================================
def esc(s):
    if s is None: return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def person_color(p):
    title = p.get("current_post","")
    if "书记" in title and "纪委" not in title and "统战" not in title:
        return "255,50,50"
    if "县长" in title or "市长" in title:
        return "50,100,255"
    if "纪委书记" in title or "监察" in title:
        return "255,165,0"
    if "人大" in title:
        return "200,255,255"
    if "政协" in title:
        return "255,240,200"
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
    return "书记" in title or "县长" in title

def generate_gexf(persons, orgs, positions, edges, output_path):
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>gov-relation Research Agent</creator>')
    lines.append(f'    <description>定结县领导班子工作关系网络 — {len(persons)} persons, {len(orgs)} orgs, {len(edges)} edges</description>')
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
    lines.append('      <attribute type="string" id="0" title="type"/>')
    lines.append('      <attribute type="string" id="1" title="context"/>')
    lines.append('      <attribute type="string" id="2" title="period"/>')
    lines.append('    </attributes>')
    lines.append('    <nodes>')
    for p in persons:
        sz = "20.0" if is_top_leader(p) else "12.0"
        c = person_color(p).split(",")
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
        lines.append(f'        <viz:size value="8.0"/>')
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
        lines.append(f'      <edge id="e{eid}" source="p{rel["person_a"]}" target="p{rel["person_b"]}" label="{esc(rel.get("type",""))}" type="2.0" weight="2.0">')
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
    print(f"Building 定结县 network data...")
    print(f"  Persons: {len(persons)}")
    print(f"  Orgs: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

    # Build SQLite DB
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("DROP TABLE IF EXISTS relationships")
    conn.execute("DROP TABLE IF EXISTS positions")
    conn.execute("DROP TABLE IF EXISTS organizations")
    conn.execute("DROP TABLE IF EXISTS persons")
    for ddl in (CREATE_PERSONS, CREATE_ORGANIZATIONS, CREATE_POSITIONS, CREATE_RELATIONSHIPS):
        conn.execute(ddl)

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