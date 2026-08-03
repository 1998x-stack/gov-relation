#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 堆龙德庆区 (Duilong Deqing District) leadership network.

堆龙德庆区 is a district of 拉萨市, 西藏自治区.
Current as of: 2026-08-03

Key personnel:
- 石运本: 区委书记 (2021.04-2026.04) → moved to 拉萨市民委党组书记
- 方文伟: 区委副书记、区长 (since 2026.07)
- 普布国庆: 前区长 (until ~2026.05)
- 陈献森: 援藏县委书记 (2013-2016, from Beijing)

Data sources:
  - http://www.dldqq.gov.cn/dldqqrmzf/ldxx/ldzc.shtml (government leadership)
  - http://www.dldqq.gov.cn/dldqqrmzf/dldqxz/202607/ce5a37bfc3c94613... (方文伟 resume)
  - http://mzsw.lasa.gov.cn/mzsw/shuji/201909/2f3c85a8aa1f289e6ca... (石运本 resume)
  - Baidu Baike
"""

import sqlite3
import os
from datetime import datetime

STAGING = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING, "堆龙德庆区_network.db")
GEXF_PATH = os.path.join(STAGING, "堆龙德庆区_network.gexf")

# ── Metadata ────────────────────────────────────────────────────────
SLUG = "堆龙德庆区"
TODAY = "2026-08-03"

# ── Persons ─────────────────────────────────────────────────────────
persons = [
    # === Core leaders ===
    # Current 区长
    {"id": 1, "name": "方文伟", "gender": "男", "ethnicity": "汉族",
     "birth": "1977-09", "birthplace": "",
     "education": "本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "堆龙德庆区委副书记、政府党组书记、区长", "current_org": "堆龙德庆区人民政府",
     "source": "http://www.dldqq.gov.cn/dldqqrmzf/dldqxz/202607/e5a37bfa3c946139153eeeefe59789ac.shtml"},
    # Former区委书记 (2021.04-2026.04)
    {"id": 2, "name": "石运本", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "西藏农牧学院林学系",
     "party_join": "中共党员", "work_start": "2000-07",
     "current_post": "拉萨市民族事务委员会党组书记、副主任", "current_org": "拉萨市民族事务委员会",
     "source": "http://msww.lasa.gov.cn/mzsw/shuji/201909/2f3c85a8aa2440f28939e5aaaac7ca54be8f6.shtml"},
    # 前任区长
    {"id": 3, "name": "普布国庆", "gender": "男", "ethnicity": "藏族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "", "current_org": "",
     "source": "http://www.dldg.gov.cn/ljqqrmzf/ldxx/202603/2c9643d86446689ec99784957166c95dcba.shtml"},
    # 区委常务副书记、常务副区长
    {"id": 4, "name": "李洋", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "堆龙德庆区委常务副书记、政府党组副书记、常务副区长", "current_org": "堆龙德庆区人民政府",
     "source": "http://www.dldg.gov.cn/ljqqzf/ldxx/lds.sh"},
    {"id": 5, "name": "丹增强嘎", "gender": "男", "ethnicity": "藏族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "堆龙德庆区委常委、政府党组副书记、副区长", "current_org": "堆龙德庆区人民政府",
     "source": "http://www.dldg.gov.cn/ljqqzf/ldxx/ldz.shtml"},
    {"id": 6, "name": "耿超", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "堆龙德庆区委常委、政府党组副书记、副区长", "current_org": "堆龙德庆区人民政府",
     "source": "http://www.dldg.gov.cn/ljqqzf/ldxx/ldz.shtml"},
    {"id": 7, "name": "杨开颜", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "堆龙德庆区委常委、政府党组副书记、副区长", "current_org": "堆龙德庆区人民政府",
     "source": "http://www.dldg.gov.cn/ljqqzf/ldxx/ldz.shtml"},
    {"id": 8, "name": "向秋多吉", "gender": "男", "ethnicity": "藏族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "堆龙德庆区政府党组成员、副区长", "current_org": "堆龙德庆区人民政府",
     "source": "http://www.dldg.gov.cn/ljqqzf/ldxx/ldz.shtml"},
    {"id": 9, "name": "邹世金", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "堆龙德庆区政府党组成员、副区长", "current_org": "堆龙德庆区人民政府",
     "source": "http://www.dldg.gov.cn/ljqqzf/ldxx/ldz.shtml"},
    {"id": 10, "name": "马立玲", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "堆龙德庆区政府党组成员、副区长", "current_org": "堆龙德庆区人民政府",
     "source": "http://www.dldg.gov.cn/ljqqzf/ldxx/ldz.shtml"},
    {"id": 11, "name": "庹超", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "堆龙德庆区政府党组成员、副区长", "current_org": "堆龙德庆区人民政府",
     "source": "http://www.dldg.gov.cn/ljqqzf/ldxx/ldz.shtml"},
    {"id": 12, "name": "李明", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "堆龙德庆区政府党组成员、副区长", "current_org": "堆龙德庆区人民政府",
     "source": "http://www.dldg.gov.cn/ljqqzf/ldxx/ldz.shtml"},
    {"id": 13, "name": "丹镇旺姆", "gender": "女", "ethnicity": "藏族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "堆龙德庆区政府党组成员、副区长", "current_org": "堆龙德庆区人民政府",
     "source": "http://www.dldg.gov.cn/ljqqzf/ldxx/ldz.shtml"},
    {"id": 14, "name": "平措朗杰", "gender": "男", "ethnicity": "藏族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "堆龙德庆区政府党组成员、副区长", "current_org": "堆龙德庆区人民政府",
     "source": "http://www.dldg.gov.cn/ljqqzf/ldxx/ldz.shtml"},
    # Historical: 援藏县委书记 by Beijing cadre
    {"id": 15, "name": "陈献森", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-09", "birthplace": "北京市",
     "education": "北京大学公共管理硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "北京市东城区区长", "current_org": "东城区人民政府",
     "source": "data/persons/20260716-北京市-东城区-区长-陈献珍.json"},
]

# ── Organizations ───────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共拉萨市堆龙德庆区委员会", "type": "党委", "level": "县级", "parent": "中共拉萨市委员会", "location": "西藏自治区拉萨市堆龙德庆区"},
    {"id": 2, "name": "堆龙德庆区人民政府", "type": "政府", "level": "县级", "parent": "拉萨市人民政府", "location": "西藏自治区拉萨市堆龙德庆区"},
    {"id": 3, "name": "堆龙德庆县委员会", "type": "党委", "level": "县级", "parent": "中共拉萨市委员会", "location": "西藏自治区拉萨市（2015年撤县设区）"},
    {"id": 4, "name": "拉萨市民族宗教事务委员会", "type": "政府", "level": "正处级", "parent": "拉萨市人民政府", "location": "西藏自治区拉萨市"},
]

# ── Positions ──────────────────────────────────────────────────────
positions = [
    # 方文伟 - current 区长
    {"person_id": 1, "org_id": 1, "title": "区委副书记", "start_date": "2026-06", "end_date": "present", "rank": "正处级", "note": "堆龙德庆区"},
    {"person_id": 1, "org_id": 2, "title": "区长", "start_date": "2026-07", "end_date": "present", "rank": "正处级", "note": "2026.06代理区长，2026.07正式当选"},
    {"person_id": 1, "org_id": 2, "title": "区政府党组书记", "start_date": "2026-06", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "区政府党组书记", "start_date": "2026-06", "end_date": "present", "rank": "正处级", "note": ""},
    # 方文伟 - earlier career (云南寻甸)
    {"person_id": 1, "org_id": 2, "title": "云南省寻甸县柯渡镇人民政府科员", "start_date": "2000", "end_date": "2003", "rank": "科员", "note": "云南昆明寻甸县"},
    {"person_id": 1, "org_id": 2, "title": "云南省寻甸县共青团委书记", "start_date": "2003", "end_date": "2005", "rank": "正科级", "note": "寻甸县"},
    {"person_id": 1, "org_id": 2, "title": "云南省寻甸县仁德镇党委副书记、副镇长", "start_date": "2005", "end_date": "2007", "rank": "正科级", "note": "寻甸县"},
    {"person_id": 1, "org_id": 2, "title": "云南省寻甸县七星镇党委副书记、镇长", "start_date": "2007", "end_date": "2009", "rank": "正科级", "note": "寻甸县"},
    {"person_id": 1, "org_id": 2, "title": "云南省寻甸县七星镇党委书记", "start_date": "2009", "end_date": "2012", "rank": "正科级", "note": "寻甸县"},
    # 方文伟 - 进藏
    {"person_id": 1, "org_id": 2, "title": "拉萨市林周县委常委、副县长", "start_date": "2012", "end_date": "2015", "rank": "副处级", "note": "林周县"},
    {"person_id": 1, "org_id": 1, "title": "林周县委副书记", "start_date": "2015", "end_date": "2020", "rank": "正处级", "note": "林周县（拉萨市）"},
    {"person_id": 1, "org_id": 2, "title": "拉萨市城市管理局党组书记、副局长", "start_date": "2020", "end_date": "2022", "rank": "正处级", "note": "拉萨市"},
    {"person_id": 1, "org_id": 2, "title": "拉萨市城市管理和综合执法局党组副书记、局长", "start_date": "2022", "end_date": "2026-06", "rank": "正处级", "note": "拉萨市"},
    # 石运本
    {"person_id": 2, "org_id": 1, "title": "堆龙德庆区委书记", "start_date": "2021-04", "end_date": "2026-04", "rank": "正处级", "note": "一级调研员"},
    {"person_id": 2, "org_id": 2, "title": "区政府党组书记", "start_date": "2020-10", "end_date": "2021-04", "rank": "一级调研员", "note": "堆龙德庆区"},
    {"person_id": 2, "org_id": 4, "title": "拉萨市民族宗教事务委员会党组书记、副主任", "start_date": "2026-04", "end_date": "present", "rank": "正处级", "note": ""},
    # 石运本 - earlier career
    {"person_id": 2, "org_id": 2, "title": "西藏农牧学院林学系学生", "start_date": "1997-09", "end_date": "2000-07", "rank": "", "note": "果林专业"},
    {"person_id": 2, "org_id": 2, "title": "察隅县委办科员", "start_date": "2000-07", "end_date": "2003-06", "rank": "科员", "note": "林芝市察隅县"},
    {"person_id": 2, "org_id": 2, "title": "察隅县委办副主任科员", "start_date": "2003-06", "end_date": "2004-04", "rank": "副科级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "察隅县委办副主任", "start_date": "2004-04", "end_date": "2004-10", "rank": "副科级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "察隅县古玉乡党委副书记", "start_date": "2004-10", "end_date": "2005-06", "rank": "副科级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "察隅县古玉乡党委书记、人大主席", "start_date": "2005-06", "end_date": "2010-04", "rank": "正科级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "朗县县委常委、组织部部长", "start_date": "2010-04", "end_date": "2013-11", "rank": "副处级", "note": "林芝市朗县"},
    {"person_id": 2, "org_id": 2, "title": "米林县委副书记、常务副县长", "start_date": "2013-11", "end_date": "2016-01", "rank": "副处级", "note": "米林县"},
    {"person_id": 2, "org_id": 1, "title": "工布江达县委常务副书记", "start_date": "2016-01", "end_date": "2016-07", "rank": "正处级", "note": "林芝市工布江达县"},
    {"person_id": 2, "org_id": 2, "title": "工布江达县委副书记、县长", "start_date": "2016-07", "end_date": "2020-10", "rank": "正处级", "note": "2019.12晋升一级调研员"},
    # 普布国庆 - existing data
    {"person_id": 3, "org_id": 1, "title": "区委副书记", "start_date": "2020", "end_date": "2026-05", "rank": "正处级", "note": "堆龙德庆区"},
    {"person_id": 3, "org_id": 2, "title": "区长", "start_date": "2021", "end_date": "2026-05", "rank": "正处级", "note": ""},
    # 李洋 - 常务副区
    {"person_id": 4, "org_id": 1, "title": "区委常务副书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "堆龙德庆区"},
    {"person_id": 4, "org_id": 2, "title": "常务副区长", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # Deputy mayors
    {"person_id": 5, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "区委常委"},
    {"person_id": 6, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "区委常委"},
    {"person_id": 7, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "区委常委"},
    {"person_id": 8, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 陈献森 - historical援藏县委书记
    {"person_id": 15, "org_id": 3, "title": "援藏：堆龙德庆县委书记", "start_date": "2013-07", "end_date": "2016-04", "rank": "正处级", "note": "北京市对口支援指挥部"},
]

# ── Relationships ───────────────────────────────────────────────────
relationships = [
    # 党政主要领导 work pair
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "方文伟（区长）与石运本（区委书记）2020-2021年曾在堆龙德庆区搭档（石运本任区长时），2025-2026年石运本任区委书记时方文伟还未到任", "overlap_org": "堆龙德庆区", "overlap_period": "2020-2021"},
    # 方文伟 and the current leadership team
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "区长与常务副区长工作搭档", "overlap_org": "堆龙德庆区人民政府", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "堆龙德庆区人民政府", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "堆龙德庆区人民政府", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "堆龙德庆区人民政府", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "堆龙德庆区人民政府", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "堆龙德庆区人民政府", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "堆龙德庆区人民政府", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 11, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "堆龙德庆区人民政府", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 12, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "堆龙德庆区人民政府", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 13, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "堆龙德庆区人民政府", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 14, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "堆龙德庆区人民政府", "overlap_period": "2026"},
    # Prior-successor chain: 石运本 → (unknown) → 方文伟 (区长), 普布国庆 → 方文伟
    {"person_a": 2, "person_b": 3, "type": "predecessor_successor", "context": "石运本任区委书记期间普布国庆任区长，形成党政搭档", "overlap_org": "堆龙德庆区", "overlap_period": "2021-2026"},
    {"person_a": 3, "person_b": 1, "type": "predecessor_successor", "context": "普布国庆卸任区长后由方文伟接任", "overlap_org": "堆龙德庆区人民政府", "overlap_period": "2026"},
    # 援藏 connection
    {"person_a": 15, "person_b": 2, "type": "overlap", "context": "陈献森为北京市援藏干部（2013-2016堆龙德庆县委书记），石运本后来成为原地区区委书记", "overlap_org": "堆龙德庆县/堆龙德庆区", "overlap_period": "2013-2026"},
    # Deputy group overlaps
    {"person_a": 4, "person_b": 5, "type": "overlap", "context": "区政府领导班子同事", "overlap_org": "堆龙德庆区人民政府", "overlap_period": "present"},
    {"person_a": 4, "person_b": 6, "type": "overlap", "context": "区政府领导班子同事", "overlap_org": "堆龙德庆区人民政府", "overlap_period": "present"},
    {"person_a": 5, "person_b": 6, "type": "overlap", "context": "区政府领导班子同事", "overlap_org": "堆龙德庆区人民政府", "overlap_period": "present"},
    {"person_a": 6, "person_b": 7, "type": "overlap", "context": "区政府领导班子同事", "overlap_org": "堆龙德庆区人民政府", "overlap_period": "present"},
    {"person_a": 8, "person_b": 9, "type": "overlap", "context": "区政府领导班子同事", "overlap_org": "堆龙德庆区人民政府", "overlap_period": "present"},
    {"person_a": 10, "person_b": 11, "type": "overlap", "context": "区政府领导班子成员", "overlap_org": "堆龙德庆区人民政府", "overlap_period": "present"},
    {"person_a": 12, "person_b": 13, "type": "overlap", "context": "区政府领导班子成员", "overlap_org": "堆龙德庆区人民政府", "overlap_period": "present"},
    {"person_a": 13, "person_b": 14, "type": "overlap", "context": "区政府领导班子成员（同为藏族干部）", "overlap_org": "堆龙德庆区人民政府", "overlap_period": "present"},
]

# ── SQLite ─────────────────────────────────────────────────────────
def create_tables(conn):
    conn.execute("""CREATE TABLE IF NOT EXISTS persons (
        id INTEGER PRIMARY KEY, name TEXT NOT NULL, gender TEXT DEFAULT '',
        ethnicity TEXT DEFAULT '', birth TEXT DEFAULT '', birthplace TEXT DEFAULT '',
        education TEXT DEFAULT '', party_join TEXT DEFAULT '', work_start TEXT DEFAULT '',
        current_post TEXT DEFAULT '', current_org TEXT DEFAULT '', source TEXT DEFAULT '')""")
    conn.execute("""CREATE TABLE IF NOT EXISTS organizations (
        id INTEGER PRIMARY KEY, name TEXT NOT NULL, type TEXT DEFAULT '',
        level TEXT DEFAULT '', parent TEXT DEFAULT '', location TEXT DEFAULT '')""")
    conn.execute("""CREATE TABLE IF NOT EXISTS positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT, person_id INTEGER NOT NULL,
        org_id INTEGER NOT NULL, title TEXT DEFAULT '', start_date TEXT DEFAULT '',
        end_date TEXT DEFAULT '', rank TEXT DEFAULT '', note TEXT DEFAULT '')""")
    conn.execute("""CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT, person_a INTEGER NOT NULL,
        person_b INTEGER NOT NULL, type TEXT DEFAULT '', context TEXT DEFAULT '',
        overlap_org TEXT DEFAULT '', overlap_period TEXT DEFAULT '')""")


def insert_data(conn):
    for p in persons:
        conn.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                     [p.get(k, "") for k in ["id","name","gender","ethnicity","birth","birthplace",
                                             "education","party_join","work_start","current_post",
                                             "current_org","source"]])
    for o in organizations:
        conn.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)",
                     [o.get(k, "") for k in ["id","name","type","level","parent","location"]])
    for pos in positions:
        conn.execute("INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)",
                     [pos.get(k, "") for k in ["person_id","org_id","title","start_date","end_date","rank","note"]])
    for r in relationships:
        conn.execute("INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)",
                     [r.get(k, "") for k in ["person_a","person_b","type","context","overlap_org","overlap_period"]])
    conn.commit()


# ── GEXF ───────────────────────────────────────────────────────────
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")


def person_color(p):
    if p["id"] in (1, 2):
        return "50,100,255"   # District mayor - blue
    elif p["id"] == 3:
        return "100,100,100"  # Previous mayor - grey
    elif p["id"] in (4,):
        return "255,165,0"    # Executive deputy - orange
    elif p["id"] == 15:
        return "255,50,50"    # Historical party secretary (援藏) - red
    else:
        return "100,100,100"


def org_color(o):
    t = o.get("type", "")
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
    }
    return colors.get(t, "200,200,200")


def is_top_leader(p):
    return p["id"] in (1, 2, 3)


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>Government Personnel Network Investigator</creator>')
    lines.append(f'    <description>{SLUG} leadership network</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('    </attributes>')
    # Nodes: persons
    lines.append('    <nodes>')
    for p in persons:
        sz = "20.0" if is_top_leader(p) else ("15.0" if p["id"] in (4, 15) else "12.0")
        c = person_color(p)
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    # Nodes: organizations
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')
    # Edges
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1
    for r in relationships:
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    try:
        create_tables(conn)
        insert_data(conn)
    finally:
        conn.close()
    build_gexf()
    print(f"Done. DB: {DB_PATH}")
    print(f"Done. GEXF: {GEXF_PATH}")
    print(f"Summary: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")