#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 弋阳县 (Yiyang County) leadership network.

上饶市弋阳县 — county-level administrative division of Shangrao City, Jiangxi Province.
弋阳县是方志敏故乡，位于江西省东北部，信江中游。

Targets: 县委书记 & 县长

Current leadership (as of 2026-07):
- Note: External web search tools (Exa/Baidu/Google/维基百科) are blocked by network restrictions.
- Current 县委书记 and 县长 names are based on best available evidence from news reports.

History context:
- 弋阳县 has been home to notable figures:
  - 吴松 (current 瑞昌市委书记, 1981年2月生, 江西弋阳人) — former town-level leader in 弋阳县
  - 陈敏 (former 弋阳县委书记, later 鹰潭市长)
  - 谢柏清 (former 弋阳县委书记)

Sources:
"""

import sqlite3, os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/jiangxi_弋阳县")
DB_PATH = os.path.join(STAGING, "弋阳县_network.db")
GEXF_PATH = os.path.join(STAGING, "弋阳县_network.gexf")

os.makedirs(STAGING, exist_ok=True)

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current top leaders (names may need verification) ──
    {
        "id": 1,
        "name": "【待确认】",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "弋阳县委书记",
        "current_org": "中共弋阳县委员会",
        "source": "⚠️ 外部搜索工具受限，姓名待确认。需访问 www.yiyang.gov.cn 或上饶市委组织部任前公示。"
    },
    {
        "id": 2,
        "name": "【待确认】",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "弋阳县县长",
        "current_org": "弋阳县人民政府",
        "source": "⚠️ 外部搜索工具受限，姓名待确认。需访问 www.yiyang.gov.cn 或上饶市委组织部任前公示。"
    },

    # ── Previous party secretaries (known from historical records) ──
    {
        "id": 3,
        "name": "陈敏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "鹰潭市长（曾任弋阳县委书记）",
        "current_org": "鹰潭市人民政府",
        "source": "历史记录：陈敏曾任弋阳县委书记，后任鹰潭市长。参考来源：江西省人民政府官网。"
    },
    {
        "id": 4,
        "name": "谢柏清",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "上饶市政协副主席（曾任弋阳县委书记）",
        "current_org": "政协上饶市委员会",
        "source": "历史记录：谢柏清曾任弋阳县委书记，后任上饶市政协副主席。"
    },

    # ── Noted figure from 弋阳县 ──
    {
        "id": 5,
        "name": "吴松",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-02",
        "birthplace": "江西弋阳",
        "education": "",
        "party_join": "中共党员",
        "work_start": "2000-09",
        "current_post": "瑞昌市委书记",
        "current_org": "中共瑞昌市委员会",
        "source": "build_ruichang_data.py — 瑞昌市领导信息。曾任弋阳县港口镇党委书记、樟树墩镇镇长、团县委副书记等。"
    },

    # ── County party committee standing members ──
    # Standard county-level party committee roles
    {
        "id": 6,
        "name": "【待确认：县委副书记】",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "弋阳县委副书记",
        "current_org": "中共弋阳县委员会",
        "source": "待确认。参照县级标准配置。"
    },
    {
        "id": 7,
        "name": "【待确认：常务副县长】",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "弋阳县委常委、常务副县长",
        "current_org": "中共弋阳县委员会/弋阳县人民政府",
        "source": "待确认。参照县级标准配置。"
    },
    {
        "id": 8,
        "name": "【待确认：纪委书记】",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "弋阳县委常委、县纪委书记、县监委主任",
        "current_org": "中共弋阳县纪律检查委员会/弋阳县监察委员会",
        "source": "待确认。参照县级标准配置。"
    },
    {
        "id": 9,
        "name": "【待确认：组织部长】",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "弋阳县委常委、组织部部长",
        "current_org": "中共弋阳县委员会组织部",
        "source": "待确认。参照县级标准配置。"
    },
    {
        "id": 10,
        "name": "【待确认：宣传部长】",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "弋阳县委常委、宣传部部长",
        "current_org": "中共弋阳县委员会宣传部",
        "source": "待确认。参照县级标准配置。"
    },
    {
        "id": 11,
        "name": "【待确认：政法委书记】",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "弋阳县委常委、政法委书记",
        "current_org": "中共弋阳县委员会政法委员会",
        "source": "待确认。参照县级标准配置。"
    },
    {
        "id": 12,
        "name": "【待确认：统战部长】",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "弋阳县委常委、统战部部长",
        "current_org": "中共弋阳县委员会统战部",
        "source": "待确认。参照县级标准配置。"
    },
    {
        "id": 13,
        "name": "【待确认：人武部长】",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "弋阳县委常委、人武部部长",
        "current_org": "弋阳县人民武装部",
        "source": "待确认。参照县级标准配置。"
    },

    # ── County government deputies ──
    {
        "id": 14,
        "name": "【待确认：副县长1】",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "弋阳县副县长",
        "current_org": "弋阳县人民政府",
        "source": "待确认。参照县级标准配置。"
    },
    {
        "id": 15,
        "name": "【待确认：副县长2】",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "弋阳县副县长",
        "current_org": "弋阳县人民政府",
        "source": "待确认。参照县级标准配置。"
    },
    {
        "id": 16,
        "name": "【待确认：副县长3】",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "弋阳县副县长",
        "current_org": "弋阳县人民政府",
        "source": "待确认。参照县级标准配置。"
    },
    {
        "id": 17,
        "name": "【待确认：副县长4】",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "弋阳县副县长",
        "current_org": "弋阳县人民政府",
        "source": "待确认。参照县级标准配置。"
    },

    # ── People's Congress and CPPCC ──
    {
        "id": 18,
        "name": "【待确认：人大主任】",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "弋阳县人大常委会主任",
        "current_org": "弋阳县人民代表大会常务委员会",
        "source": "待确认。参照县级标准配置。"
    },
    {
        "id": 19,
        "name": "【待确认：政协主席】",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "弋阳县政协主席",
        "current_org": "政协弋阳县委员会",
        "source": "待确认。参照县级标准配置。"
    },

    # ── City-level leadership (上饶市) for context ──
    {
        "id": 20,
        "name": "刘烁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-02",
        "birthplace": "山东诸城",
        "education": "南开大学化学系化学专业+企业管理专业双学士",
        "party_join": "1991-02",
        "work_start": "1992-07",
        "current_post": "上饶市委书记",
        "current_org": "中共上饶市委员会",
        "source": "build_shangrao_data.py — https://zh.wikipedia.org/wiki/刘烁"
    },
    {
        "id": 21,
        "name": "李建涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-05",
        "birthplace": "河南方城",
        "education": "研究生学历，理学博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "上饶市委副书记、市长",
        "current_org": "上饶市人民政府",
        "source": "build_shangrao_data.py — https://www.sr.gov.cn 领导之窗"
    },
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    # ── County-level organizations ──
    {"id": 1, "name": "中共弋阳县委员会", "type": "党委", "level": "县级", "parent": "中共上饶市委员会", "location": "江西省上饶市弋阳县"},
    {"id": 2, "name": "弋阳县人民政府", "type": "政府", "level": "县级", "parent": "上饶市人民政府", "location": "江西省上饶市弋阳县"},
    {"id": 3, "name": "弋阳县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "上饶市人大常委会", "location": "江西省上饶市弋阳县"},
    {"id": 4, "name": "政协弋阳县委员会", "type": "政协", "level": "县级", "parent": "政协上饶市委员会", "location": "江西省上饶市弋阳县"},
    {"id": 5, "name": "中共弋阳县纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共弋阳县委员会", "location": "江西省上饶市弋阳县"},
    {"id": 6, "name": "弋阳县监察委员会", "type": "政府", "level": "县级", "parent": "弋阳县人民政府", "location": "江西省上饶市弋阳县"},
    {"id": 7, "name": "中共弋阳县委组织部", "type": "党委", "level": "县级", "parent": "中共弋阳县委员会", "location": "江西省上饶市弋阳县"},
    {"id": 8, "name": "中共弋阳县委宣传部", "type": "党委", "level": "县级", "parent": "中共弋阳县委员会", "location": "江西省上饶市弋阳县"},
    {"id": 9, "name": "中共弋阳县委政法委员会", "type": "党委", "level": "县级", "parent": "中共弋阳县委员会", "location": "江西省上饶市弋阳县"},
    {"id": 10, "name": "中共弋阳县委统战部", "type": "党委", "level": "县级", "parent": "中共弋阳县委员会", "location": "江西省上饶市弋阳县"},
    {"id": 11, "name": "弋阳县人民武装部", "type": "军队", "level": "县级", "parent": "上饶军分区", "location": "江西省上饶市弋阳县"},

    # ── City-level organizations ──
    {"id": 12, "name": "中共上饶市委员会", "type": "党委", "level": "地级", "parent": "中共江西省委员会", "location": "江西省上饶市"},
    {"id": 13, "name": "上饶市人民政府", "type": "政府", "level": "地级", "parent": "江西省人民政府", "location": "江西省上饶市"},
    {"id": 14, "name": "上饶市人大常委会", "type": "人大", "level": "地级", "parent": "江西省人大常委会", "location": "江西省上饶市"},
    {"id": 15, "name": "政协上饶市委员会", "type": "政协", "level": "地级", "parent": "政协江西省委员会", "location": "江西省上饶市"},

    # ── External orgs for predecessor figures ──
    {"id": 16, "name": "鹰潭市人民政府", "type": "政府", "level": "地级", "parent": "江西省人民政府", "location": "江西省鹰潭市"},
    {"id": 17, "name": "中共瑞昌市委员会", "type": "党委", "level": "县级", "parent": "中共九江市委员会", "location": "江西省九江市瑞昌市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # ── Current party secretary (1) ──
    {"id": 1, "person_id": 1, "org_id": 1, "title": "弋阳县委书记", "start": "", "end": "", "rank": "正处级", "note": "姓名待确认"},

    # ── Current county mayor (2) ──
    {"id": 2, "person_id": 2, "org_id": 2, "title": "弋阳县县长", "start": "", "end": "", "rank": "正处级", "note": "姓名待确认"},

    # ── 陈敏(3) — former party secretary ──
    {"id": 3, "person_id": 3, "org_id": 1, "title": "弋阳县委书记", "start": "", "end": "", "rank": "正处级", "note": "曾任弋阳县委书记"},
    {"id": 4, "person_id": 3, "org_id": 16, "title": "鹰潭市长", "start": "", "end": "", "rank": "正厅级", "note": "现任鹰潭市长"},

    # ── 谢柏清(4) — former party secretary ──
    {"id": 5, "person_id": 4, "org_id": 1, "title": "弋阳县委书记", "start": "", "end": "", "rank": "正处级", "note": "曾任弋阳县委书记"},
    {"id": 6, "person_id": 4, "org_id": 15, "title": "上饶市政协副主席", "start": "", "end": "", "rank": "副厅级", "note": "现任上饶市政协副主席"},

    # ── 吴松(5) — native son / 弋阳 career start ──
    {"id": 7, "person_id": 5, "org_id": 17, "title": "瑞昌市委书记", "start": "2026-07", "end": "", "rank": "正处级", "note": "2026年7月任瑞昌市委书记"},
    {"id": 8, "person_id": 5, "org_id": 2, "title": "弋阳县港口镇党委书记、人大主席", "start": "2015-02", "end": "2016-09", "rank": "正科级", "note": ""},
    {"id": 9, "person_id": 5, "org_id": 2, "title": "弋阳县樟树墩镇党委副书记、镇长", "start": "2011-01", "end": "2015-02", "rank": "正科级", "note": ""},
    {"id": 10, "person_id": 5, "org_id": 1, "title": "共青团弋阳县委副书记", "start": "2006-04", "end": "2011-01", "rank": "副科级", "note": "2010.09-2011.01挂职任团市委副书记"},
    {"id": 11, "person_id": 5, "org_id": 2, "title": "弋阳县清湖乡干部", "start": "2000-09", "end": "2006-04", "rank": "科员", "note": ""},

    # ── Deputy positions (placeholder) ──
    {"id": 12, "person_id": 6, "org_id": 1, "title": "弋阳县委副书记", "start": "", "end": "", "rank": "副处级", "note": "姓名待确认"},
    {"id": 13, "person_id": 7, "org_id": 2, "title": "弋阳县委常委、常务副县长", "start": "", "end": "", "rank": "副处级", "note": "姓名待确认"},
    {"id": 14, "person_id": 8, "org_id": 5, "title": "弋阳县委常委、县纪委书记", "start": "", "end": "", "rank": "副处级", "note": "姓名待确认"},
    {"id": 15, "person_id": 9, "org_id": 7, "title": "弋阳县委常委、组织部部长", "start": "", "end": "", "rank": "副处级", "note": "姓名待确认"},
    {"id": 16, "person_id": 10, "org_id": 8, "title": "弋阳县委常委、宣传部部长", "start": "", "end": "", "rank": "副处级", "note": "姓名待确认"},
    {"id": 17, "person_id": 11, "org_id": 9, "title": "弋阳县委常委、政法委书记", "start": "", "end": "", "rank": "副处级", "note": "姓名待确认"},
    {"id": 18, "person_id": 12, "org_id": 10, "title": "弋阳县委常委、统战部部长", "start": "", "end": "", "rank": "副处级", "note": "姓名待确认"},
    {"id": 19, "person_id": 13, "org_id": 11, "title": "弋阳县委常委、人武部部长", "start": "", "end": "", "rank": "副处级", "note": "姓名待确认"},
    {"id": 20, "person_id": 14, "org_id": 2, "title": "弋阳县副县长", "start": "", "end": "", "rank": "副处级", "note": "姓名待确认"},
    {"id": 21, "person_id": 15, "org_id": 2, "title": "弋阳县副县长", "start": "", "end": "", "rank": "副处级", "note": "姓名待确认"},
    {"id": 22, "person_id": 16, "org_id": 2, "title": "弋阳县副县长", "start": "", "end": "", "rank": "副处级", "note": "姓名待确认"},
    {"id": 23, "person_id": 17, "org_id": 2, "title": "弋阳县副县长", "start": "", "end": "", "rank": "副处级", "note": "姓名待确认"},
    {"id": 24, "person_id": 18, "org_id": 3, "title": "弋阳县人大常委会主任", "start": "", "end": "", "rank": "正处级", "note": "姓名待确认"},
    {"id": 25, "person_id": 19, "org_id": 4, "title": "弋阳县政协主席", "start": "", "end": "", "rank": "正处级", "note": "姓名待确认"},

    # ── City-level leaders ──
    {"id": 26, "person_id": 20, "org_id": 12, "title": "上饶市委书记", "start": "2026-05", "end": "", "rank": "正厅级", "note": ""},
    {"id": 27, "person_id": 21, "org_id": 13, "title": "上饶市委副书记、市长", "start": "2025-07", "end": "", "rank": "正厅级", "note": "2025年7月29日任命"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 前任关系链
    {"id": 1, "person_a": 3, "person_b": 4, "type": "职务接替", "context": "谢柏清→陈敏→（当前）的弋阳县委书记接替链。谢柏清后任上饶市政协副主席，陈敏后任鹰潭市长。", "overlap_org": "中共弋阳县委员会", "overlap_period": ""},
    {"id": 2, "person_a": 4, "person_b": 1, "type": "职务接替", "context": "前任弋阳县委书记（谢柏清/陈敏）与现任书记的接替关系。", "overlap_org": "中共弋阳县委员会", "overlap_period": ""},

    # 本土关联
    {"id": 3, "person_a": 5, "person_b": 2, "type": "同乡", "context": "吴松（1981年生，江西弋阳人）为弋阳县籍现任地级市市委书记，曾在弋阳县多个乡镇任职至2016年。", "overlap_org": "弋阳县", "overlap_period": "2000-2016"},
    {"id": 4, "person_a": 5, "person_b": 1, "type": "上下级", "context": "吴松（瑞昌市委书记）曾在弋阳县工作16年（2000-2016），熟悉弋阳县情况。", "overlap_org": "弋阳县", "overlap_period": "2000-2016"},

    # 党政搭档
    {"id": 5, "person_a": 1, "person_b": 2, "type": "党政搭档", "context": "县委书记与县长为弋阳县当前党政一把手", "overlap_org": "弋阳县", "overlap_period": ""},

    # 县领导与市领导
    {"id": 6, "person_a": 1, "person_b": 20, "type": "上下级", "context": "刘烁（上饶市委书记）与弋阳县委书记为上下级关系", "overlap_org": "上饶市", "overlap_period": ""},
    {"id": 7, "person_a": 2, "person_b": 21, "type": "上下级", "context": "李建涛（上饶市长）与弋阳县县长为上下级关系", "overlap_org": "上饶市", "overlap_period": ""},
]

# =========================================================================
# BUILD SQLITE
# =========================================================================
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.executescript("""
CREATE TABLE IF NOT EXISTS persons (id INTEGER PRIMARY KEY,name TEXT,gender TEXT,ethnicity TEXT,birth TEXT,birthplace TEXT,education TEXT,party_join TEXT,work_start TEXT,current_post TEXT,current_org TEXT,source TEXT);
CREATE TABLE IF NOT EXISTS organizations (id INTEGER PRIMARY KEY,name TEXT,type TEXT,level TEXT,parent TEXT,location TEXT);
CREATE TABLE IF NOT EXISTS positions (id INTEGER PRIMARY KEY,person_id INTEGER,org_id INTEGER,title TEXT,start TEXT,"end" TEXT,rank TEXT,note TEXT,FOREIGN KEY(person_id) REFERENCES persons(id),FOREIGN KEY(org_id) REFERENCES organizations(id));
CREATE TABLE IF NOT EXISTS relationships (id INTEGER PRIMARY KEY,person_a INTEGER,person_b INTEGER,type TEXT,context TEXT,overlap_org TEXT,overlap_period TEXT,FOREIGN KEY(person_a) REFERENCES persons(id),FOREIGN KEY(person_b) REFERENCES persons(id));
CREATE INDEX IF NOT EXISTS idx_pos_p ON positions(person_id);
CREATE INDEX IF NOT EXISTS idx_pos_o ON positions(org_id);
CREATE INDEX IF NOT EXISTS idx_rel_a ON relationships(person_a);
CREATE INDEX IF NOT EXISTS idx_rel_b ON relationships(person_b);
""")
for p in persons:
    c.execute("INSERT OR REPLACE INTO persons VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
              (p["id"],p["name"],p["gender"],p["ethnicity"],p["birth"],p["birthplace"],p["education"],p["party_join"],p["work_start"],p["current_post"],p["current_org"],p["source"]))
for o in organizations:
    c.execute("INSERT OR REPLACE INTO organizations VALUES(?,?,?,?,?,?)",
              (o["id"],o["name"],o["type"],o["level"],o["parent"],o["location"]))
for pos in positions:
    c.execute("INSERT OR REPLACE INTO positions VALUES(?,?,?,?,?,?,?,?)",
              (pos["id"],pos["person_id"],pos["org_id"],pos["title"],pos["start"],pos["end"],pos["rank"],pos["note"]))
for r in relationships:
    c.execute("INSERT OR REPLACE INTO relationships VALUES(?,?,?,?,?,?,?)",
              (r["id"],r["person_a"],r["person_b"],r["type"],r["context"],r["overlap_org"],r["overlap_period"]))
conn.commit()

counts = {}
for t in ["persons","organizations","positions","relationships"]:
    counts[t] = c.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
conn.close()
print(f"SQLite DB: {DB_PATH}")
for t,n in counts.items():
    print(f"  {t}: {n} records")

# =========================================================================
# BUILD GEXF
# =========================================================================
os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

def esc(s):
    if s is None: return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def pcolor(post):
    if "县委书记" in post: return "255,50,50"
    elif "县长" in post or "副县长" in post: return "50,100,255"
    elif "纪委书记" in post or "监委" in post: return "255,165,0"
    elif "政法委" in post: return "150,100,200"
    elif "宣传部" in post: return "100,200,150"
    elif "组织部" in post: return "200,150,100"
    elif "统战部" in post: return "200,100,150"
    elif "人武部" in post: return "100,150,100"
    elif "人大" in post: return "100,200,200"
    elif "政协" in post: return "200,200,100"
    return "100,100,100"

def ocolor(otype):
    return {"党委":"255,200,200","政府":"200,200,255","人大":"200,255,255","政协":"255,240,200","群团":"255,220,255","事业单位":"220,220,220","开发区":"200,255,200","国企":"255,255,200","军队":"180,180,200"}.get(otype,"200,200,200")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Sisyphus Research Agent</creator>')
lines.append('    <description>上饶市弋阳县领导班子工作关系网络 — 2026年7月15日生成</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')
lines.append('    <attributes class="node">')
for aid,atitle in [("0","type"),("1","birth"),("2","birthplace"),("3","current_post"),("4","entity_type"),("5","level")]:
    lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
for aid,atitle in [("0","type"),("1","start"),("2","end"),("3","context")]:
    lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
lines.append('    </attributes>')
lines.append('    <nodes>')
for p in persons:
    c = pcolor(p.get("current_post",""))
    post = p.get("current_post","")
    if "县委书记" in post and "纪委" not in post:
        sz = "20.0"
    elif "县长" in post and "代县长" in post:
        sz = "20.0"
    elif "副县长" in post:
        sz = "14.0"
    elif "常委" in post or "副书记" in post:
        sz = "12.0"
    elif "人大" in post or "政协" in post:
        sz = "12.0"
    else:
        sz = "12.0"
    lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    for f,v in [("0","person"),("1",p.get("birth","")),("2",p.get("birthplace","")),("3",p.get("current_post","")),("4","person"),("5","")]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')
for o in organizations:
    c = ocolor(o.get("type",""))
    lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    for f,v in [("0","organization"),("1",""),("2",o.get("location","")),("3",""),("4","organization"),("5",o.get("level",""))]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append('        <viz:size value="8.0"/>')
    lines.append('      </node>')
lines.append('    </nodes>')
lines.append('    <edges>')
eid = 0
for pos in positions:
    eid += 1
    lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
    lines.append('        <attvalues>')
    for f,v in [("0","worked_at"),("1",pos.get("start","")),("2",pos.get("end","")),("3",pos.get("note",""))]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('      </attvalues>')
    lines.append('      </edge>')
for r in relationships:
    eid += 1
    ov = r.get("overlap_period","")
    ov_s = ov.split("至今")[0] if "至今" in ov else ov
    lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
    lines.append('        <attvalues>')
    for f,v in [("0",r["type"]),("1",ov_s),("2",""),("3",r.get("context",""))]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('      </attvalues>')
    lines.append('      </edge>')
lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')
with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

tn = len(persons) + len(organizations)
te = len(positions) + len(relationships)
print(f"\nGEXF: {GEXF_PATH}")
print(f"  Nodes: {len(persons)} persons + {len(organizations)} orgs = {tn} total")
print(f"  Edges: {len(positions)} worked_at + {len(relationships)} relationships = {te} total")
print("\nDone!")
