#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 竹山县 (Zhushan County), 十堰市, 湖北省.

Level: 县
Province: 湖北省
Parent city: 十堰市
Targets: 县委书记 (Party Secretary), 县长 (County Magistrate)
Task ID: hubei_竹山县

Research date: 2026-07-24
Official source: http://www.zhushan.gov.cn/ (竹山县人民政府) — confirmed accessible via HTTP

Current status (as of 2026-07-24):
- 县委书记: 曾祥成 (confirmed via official县委 leadership page + news articles)
- 县长: 王丽媛 (confirmed via official县政府 leadership page)

Roster sources:
  县委领导: http://www.zhushan.gov.cn/xxgkxi/fdzdgk/zfld/zsxw/
  县政府领导: http://www.zhushan.gov.cn/xzf_0/
  县人大: http://www.zhushan.gov.cn/xxgkxi/fdzdgk/zfld/zsxrd/

Confidence notes:
  - Current roles for all县委, 县政府, 县人大 members: confirmed via official government website
  - Career histories for all leaders: unverified — only current positions confirmed from official sources
  - Birth details, education, party join dates: unverified
  - Exa search was rate-limited; Baidu returned 403; Google/Bing/DuckDuckGo timed out
  - Some personal details (gender, ethnicity) may be inferred from official context where reasonable
"""
# process_tmp.py tokens: sqlite3, DB_PATH, GEXF_PATH
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
BASE = STAGING_DIR.parents[2]  # repo root
SLUG = "竹山县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# Staging paths
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING_DIR

# Canonical paths (after promotion)
CANONICAL_DB = BASE / "data" / "database" / f"{SLUG}_network.db"
CANONICAL_GEXF = BASE / "data" / "graph" / f"{SLUG}_network.gexf"
CANONICAL_BUILD = BASE / f"build_{SLUG}_data.py"
CANONICAL_PERSONS = BASE / "data" / "persons"

# ── Persons ─────────────────────────────────────────────────────────────────
persons = [
    # ═══════ Core Leadership ═══════
    {
        "id": 1,
        "name": "曾祥成",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共竹山县委员会",
        "source": "http://www.zhushan.gov.cn/xxgkxi/fdzdgk/zfld/zsxw/"
    },
    {
        "id": 2,
        "name": "王丽媛",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县长",
        "current_org": "竹山县人民政府",
        "source": "http://www.zhushan.gov.cn/xxgkxi/fdzdgk/zfld/zsxxzf/wly_0001/"
    },
    # ═══════ 县委领导 ═══════
    {
        "id": 3,
        "name": "明昌艳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、政法委书记",
        "current_org": "中共竹山县委员会",
        "source": "http://www.zhushan.gov.cn/xxgkxi/fdzdgk/zfld/zsxw/"
    },
    {
        "id": 4,
        "name": "余启波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、纪委书记、监委主任",
        "current_org": "中共竹山县纪律检查委员会",
        "source": "http://www.zhushan.gov.cn/xxgkxi/fdzdgk/zfld/zsxw/"
    },
    {
        "id": 5,
        "name": "范奇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "竹山县人民政府",
        "source": "http://www.zhushan.gov.cn/xxgkxi/fdzdgk/zfld/zsxw/"
    },
    {
        "id": 6,
        "name": "张涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县人武部政委",
        "current_org": "竹山县人民武装部",
        "source": "http://www.zhushan.gov.cn/xxgkxi/fdzdgk/zfld/zsxw/"
    },
    {
        "id": 7,
        "name": "熊应标",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县委办主任，县委直属机关工委书记",
        "current_org": "中共竹山县委员会办公室",
        "source": "http://www.zhushan.gov.cn/xxgkxi/fdzdgk/zfld/zsxw/"
    },
    {
        "id": 8,
        "name": "成刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长，县行政学校校长",
        "current_org": "竹山县人民政府",
        "source": "http://www.zhushan.gov.cn/xxgkxi/fdzdgk/zfld/zsxw/"
    },
    {
        "id": 9,
        "name": "李攀",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共竹山县委组织部",
        "source": "http://www.zhushan.gov.cn/xxgkxi/fdzdgk/zfld/zsxw/"
    },
    {
        "id": 10,
        "name": "李金柱",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共竹山县委宣传部",
        "source": "http://www.zhushan.gov.cn/xxgkxi/fdzdgk/zfld/zsxw/"
    },
    {
        "id": 11,
        "name": "孟繁野",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "竹山县人民政府",
        "source": "http://www.zhushan.gov.cn/xxgkxi/fdzdgk/zfld/zsxw/"
    },
    {
        "id": 12,
        "name": "边宏伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "竹山县人民政府",
        "source": "http://www.zhushan.gov.cn/xxgkxi/fdzdgk/zfld/zsxw/"
    },
    # ═══════ 县政府其他领导 ═══════
    {
        "id": 13,
        "name": "刘丽",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "竹山县人民政府",
        "source": "http://www.zhushan.gov.cn/xzf_0/"
    },
    {
        "id": 14,
        "name": "王金柱",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "竹山县人民政府",
        "source": "http://www.zhushan.gov.cn/xzf_0/"
    },
    {
        "id": 15,
        "name": "高明勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "竹山县人民政府",
        "source": "http://www.zhushan.gov.cn/xzf_0/"
    },
    {
        "id": 16,
        "name": "朱彦霖",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "竹山县人民政府",
        "source": "http://www.zhushan.gov.cn/xzf_0/"
    },
    {
        "id": 17,
        "name": "耿恒举",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "竹山县人民政府",
        "source": "http://www.zhushan.gov.cn/xzf_0/"
    },
    {
        "id": 18,
        "name": "刘子龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "竹山县人民政府",
        "source": "http://www.zhushan.gov.cn/xzf_0/"
    },
    # ═══════ 县人大领导 ═══════
    {
        "id": 19,
        "name": "毛昌盛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会党组书记、主任",
        "current_org": "竹山县人大常委会",
        "source": "http://www.zhushan.gov.cn/xxgkxi/fdzdgk/zfld/zsxrd/"
    },
    {
        "id": 20,
        "name": "朱德彬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会党组副书记、副主任",
        "current_org": "竹山县人大常委会",
        "source": "http://www.zhushan.gov.cn/xxgkxi/fdzdgk/zfld/zsxrd/"
    },
    {
        "id": 21,
        "name": "周清荣",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会副主任，县残联理事长",
        "current_org": "竹山县人大常委会",
        "source": "http://www.zhushan.gov.cn/xxgkxi/fdzdgk/zfld/zsxrd/"
    },
    {
        "id": 22,
        "name": "杨德远",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会党组成员、副主任",
        "current_org": "竹山县人大常委会",
        "source": "http://www.zhushan.gov.cn/xxgkxi/fdzdgk/zfld/zsxrd/"
    },
    {
        "id": 23,
        "name": "刘甲华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会党组成员、副主任",
        "current_org": "竹山县人大常委会",
        "source": "http://www.zhushan.gov.cn/xxgkxi/fdzdgk/zfld/zsxrd/"
    },
    {
        "id": 24,
        "name": "刘锐",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会党组成员、副主任",
        "current_org": "竹山县人大常委会",
        "source": "http://www.zhushan.gov.cn/xxgkxi/fdzdgk/zfld/zsxrd/"
    },
    {
        "id": 25,
        "name": "冯波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会党组成员、副主任",
        "current_org": "竹山县人大常委会",
        "source": "http://www.zhushan.gov.cn/xxgkxi/fdzdgk/zfld/zsxrd/"
    },
    # ═══════ 其他相关官员 ═══════
    {
        "id": 26,
        "name": "杨明章",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "竹山县",
        "source": "http://www.zhushan.gov.cn/xwzx/zsxw/202607/t20260724_4974476.shtml"
    },
    {
        "id": 27,
        "name": "李璐",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "竹山县",
        "source": "http://www.zhushan.gov.cn/xwzx/zsxw/202607/t20260723_4973146.shtml"
    },
]

# ── Organizations ───────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共竹山县委员会", "type": "党委", "level": "县级", "parent": "中共十堰市委员会", "location": "湖北省十堰市竹山县"},
    {"id": 2, "name": "竹山县人民政府", "type": "政府", "level": "县级", "parent": "十堰市人民政府", "location": "湖北省十堰市竹山县"},
    {"id": 3, "name": "中共竹山县纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共十堰市纪律检查委员会", "location": "湖北省十堰市竹山县"},
    {"id": 4, "name": "竹山县人民武装部", "type": "政府", "level": "县级", "parent": "十堰市军分区", "location": "湖北省十堰市竹山县"},
    {"id": 5, "name": "中共竹山县委员会办公室", "type": "党委", "level": "县级", "parent": "中共竹山县委员会", "location": "湖北省十堰市竹山县"},
    {"id": 6, "name": "中共竹山县委组织部", "type": "党委", "level": "县级", "parent": "中共竹山县委员会", "location": "湖北省十堰市竹山县"},
    {"id": 7, "name": "中共竹山县委宣传部", "type": "党委", "level": "县级", "parent": "中共竹山县委员会", "location": "湖北省十堰市竹山县"},
    {"id": 8, "name": "中共竹山县委政法委员会", "type": "党委", "level": "县级", "parent": "中共竹山县委员会", "location": "湖北省十堰市竹山县"},
    {"id": 9, "name": "竹山县人大常委会", "type": "人大", "level": "县级", "parent": "十堰市人大常委会", "location": "湖北省十堰市竹山县"},
    {"id": 10, "name": "竹山县监察委员会", "type": "党委", "level": "县级", "parent": "十堰市监察委员会", "location": "湖北省十堰市竹山县"},
]

# ── Positions ───────────────────────────────────────────────────────────────
positions = [
    # Core leadership
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "", "end": "present", "rank": "正县级", "note": "Confirmed as of 2026-07-24"},
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "", "end": "present", "rank": "正县级", "note": "Confirmed as of 2026-07-24"},
    # 县委领导
    {"person_id": 3, "org_id": 1, "title": "县委副书记、政法委书记", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 4, "org_id": 3, "title": "县委常委、纪委书记、监委主任", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "县委常委、副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 6, "org_id": 4, "title": "县委常委、县人武部政委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 7, "org_id": 5, "title": "县委常委、县委办主任，县委直属机关工委书记", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "县委常委、常务副县长，县行政学校校长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 9, "org_id": 6, "title": "县委常委、组织部部长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 10, "org_id": 7, "title": "县委常委、宣传部部长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "县委常委、副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "县委常委、副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 县政府其他领导
    {"person_id": 13, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 18, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 县人大
    {"person_id": 19, "org_id": 9, "title": "县人大常委会党组书记、主任", "start": "", "end": "present", "rank": "正县级", "note": ""},
    {"person_id": 20, "org_id": 9, "title": "县人大常委会党组副书记、副主任", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 21, "org_id": 9, "title": "县人大常委会副主任，县残联理事长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 22, "org_id": 9, "title": "县人大常委会党组成员、副主任", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 23, "org_id": 9, "title": "县人大常委会党组成员、副主任", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 24, "org_id": 9, "title": "县人大常委会党组成员、副主任", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 25, "org_id": 9, "title": "县人大常委会党组成员、副主任", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # Other
    {"person_id": 26, "org_id": 1, "title": "县领导", "start": "", "end": "present", "rank": "", "note": "Mentioned in news article as attending party branch event"},
    {"person_id": 27, "org_id": 2, "title": "县领导", "start": "", "end": "present", "rank": "", "note": "Reported inspecting key projects and flood control"},
]

# ── Relationships ───────────────────────────────────────────────────────────
relationships = [
    # Top leadership tandem
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记与县长党政主要领导搭档", "overlap_org": "竹山县", "overlap_period": "current"},
    # 县委常委会核心成员之间的关系
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "县委书记与副书记", "overlap_org": "中共竹山县委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "县委书记与纪委书记", "overlap_org": "中共竹山县委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "县委书记与常务副县长", "overlap_org": "中共竹山县委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate", "context": "县委书记与组织部部长", "overlap_org": "中共竹山县委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "县委书记与县委办主任", "overlap_org": "中共竹山县委员会", "overlap_period": "current"},
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate", "context": "县委书记与宣传部部长", "overlap_org": "中共竹山县委员会", "overlap_period": "current"},
    # 县长与副县长
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "县长与常务副县长", "overlap_org": "竹山县人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "竹山县人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "竹山县人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "竹山县人民政府", "overlap_period": "current"},
    # 人大主任关系
    {"person_a": 1, "person_b": 19, "type": "overlap", "context": "县委书记与人大主任党政配合", "overlap_org": "竹山县", "overlap_period": "current"},
    # 政法委书记与纪委书记（政法+纪委联动）
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "政法委书记与纪委书记工作联动", "overlap_org": "竹山县", "overlap_period": "current"},
]

try:
    import sqlite3  # noqa: F811

    # ── Inject repo path ────────────────────────────────────────────────────
    sys.path.insert(0, str(BASE))

    from gov_relation.runner import run_build

    print(f"=== Building {SLUG} network ===")
    print(f"  Persons: {len(persons)}")
    print(f"  Orgs: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    print(f"\nDB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print("=== Done ===")

except ImportError as e:
    print(f"ERROR importing gov_relation modules: {e}")
    print("Falling back to standalone mode...")
    # ── Standalone fallback ──────────────────────────────────────────────
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    GEXF_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
            birth TEXT, birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER, title TEXT,
            start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER, type TEXT,
            context TEXT, overlap_org TEXT, overlap_period TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        conn.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace,
                education, party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
              p["birthplace"], p["education"], p["party_join"], p["work_start"],
              p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        conn.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        conn.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["person_id"], pos["org_id"], pos["title"], pos["start"],
              pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        conn.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (r["person_a"], r["person_b"], r["type"], r["context"],
              r.get("overlap_org", ""), r.get("overlap_period", "")))

    conn.commit()
    conn.close()
    print(f"Standalone DB written: {DB_PATH}")

    # ── Build GEXF ──────────────────────────────────────────────────────
    def esc(s):
        if s is None: return ""
        return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">',
        f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">',
        '    <creator>Research Agent</creator>',
        f'    <description>{SLUG} leadership network</description>',
        '  </meta>',
        '  <graph mode="static" defaultedgetype="undirected">',
        '    <attributes class="node">',
        '      <attribute id="0" title="type" type="string"/>',
        '      <attribute id="1" title="role" type="string"/>',
        '      <attribute id="2" title="org" type="string"/>',
        '    </attributes>',
        '    <attributes class="edge">',
        '      <attribute id="0" title="type" type="string"/>',
        '      <attribute id="1" title="context" type="string"/>',
        '    </attributes>',
    ]

    def is_top_leader(p):
        return "县委书记" in p["current_post"] or p["current_post"] == "县长"

    def person_color(p):
        if "县委书记" in p.get("current_post", ""):
            return "255,50,50"
        if p.get("current_post") == "县长":
            return "50,100,255"
        if "纪委书记" in p.get("current_post", ""):
            return "255,165,0"
        return "100,100,100"

    def org_color(o):
        colors = {
            "党委": "255,200,200",
            "政府": "200,200,255",
            "人大": "200,255,255",
        }
        return colors.get(o.get("type", ""), "200,200,200")

    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p).split(",")
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color(o).split(",")
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type", ""))}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        context = r.get("context", r.get("type", ""))
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(context)}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(context)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Standalone GEXF written: {GEXF_PATH}")
