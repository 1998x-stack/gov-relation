#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 灞桥区, 西安市, 陕西省.

Investigation date: 2026-07-25
Task ID: shaanxi_灞桥区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - 灞桥区人民政府官方网站 (www.baqiao.gov.cn) — confirmed current leadership resumes
  - News articles from the official website (various dates through 2026-07-24)

Confidence notes:
  - 区政府领导（6人）姓名、职务、分工、简历全部在政府网站确认
  - 区委书记一职在公开信息中空缺（苏晓梅虽主持区委全面工作，但正式职务仅为区委副书记、区长）
  - 李连永（区委副书记、政法委书记）、柴艳荣（区委常委、组织部长）、马学智（区委常委、宣传部长兼统战部长）、周开来（区委常委）、刘志光（区委常委，可能为人武部长）确认出席区委会议
  - 王伟（区委常委、区纪委书记、区监委主任）通过区纪委全会确认
"""

import json
import os
import sqlite3  # noqa: F401
import sys
from datetime import datetime
from pathlib import Path

BASE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE, "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "灞桥区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

STAGING_DIR = Path(BASE)
DB_PATH = str(STAGING_DIR / f"{SLUG}_network.db")
GEXF_PATH = str(STAGING_DIR / f"{SLUG}_network.gexf")

# ═══════════════════════════════════════════════════════════════════════════════
# Data
# ═══════════════════════════════════════════════════════════════════════════════

persons_data = [
    # ══════════════════════════════════════════════════════════════════════════
    # Party Committee (区委) Leadership
    # ══════════════════════════════════════════════════════════════════════════

    # 区委书记 — 空缺（苏晓梅实际主持区委工作但未正式任命为书记）
    {
        "id": 1,
        "name": "（区委书记空缺）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委书记（空缺）",
        "current_org": "中共西安市灞桥区委员会",
        "source": "区政府官网未公示区委书记，苏晓梅实际主持区委常委会工作"
    },
    # 苏晓梅 — 区委副书记、区长
    {
        "id": 2,
        "name": "苏晓梅",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1969年11月",
        "birthplace": "陕西泾阳",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "1986年12月",
        "current_post": "区委副书记、区政府党组书记、区长",
        "current_org": "西安市灞桥区人民政府",
        "source": "https://www.baqiao.gov.cn/zwgk/zfld/zxg/1.html"
    },
    # 李连永 — 区委副书记、政法委书记
    {
        "id": 3,
        "name": "李连永",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、政法委书记",
        "current_org": "中共西安市灞桥区委员会",
        "source": "https://www.baqiao.gov.cn/xwzx/bqyw/2059895610730373122.html"
    },
    # 王伟 — 区委常委、区纪委书记、区监委主任
    {
        "id": 4,
        "name": "王伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区纪委书记、区监委主任",
        "current_org": "中共西安市灞桥区纪律检查委员会",
        "source": "https://www.baqiao.gov.cn/zwgk/zfld/ldhd/1894922534315896834.html"
    },
    # 柴艳荣 — 区委常委、组织部部长
    {
        "id": 5,
        "name": "柴艳荣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、组织部部长",
        "current_org": "中共西安市灞桥区委员会",
        "source": "https://www.baqiao.gov.cn/zwgk/zfld/ldhd/1901556249256853505.html"
    },
    # 马学智 — 区委常委、宣传部部长、统战部部长
    {
        "id": 6,
        "name": "马学智",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、宣传部部长、统战部部长",
        "current_org": "中共西安市灞桥区委员会",
        "source": "https://www.baqiao.gov.cn/zwgk/zfld/ldhd/1901556249256853505.html"
    },
    # 周开来 — 区委常委（具体职务待确认）
    {
        "id": 7,
        "name": "周开来",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共西安市灞桥区委员会",
        "source": "https://www.baqiao.gov.cn/zwgk/zfld/ldhd/1894922534315896834.html"
    },
    # 刘志光 — 区委常委（可能为人武部长）
    {
        "id": 8,
        "name": "刘志光",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共西安市灞桥区委员会",
        "source": "https://www.baqiao.gov.cn/zwgk/zfld/ldhd/1894922534315896834.html"
    },
    # 柳春林 — 区委常委、常务副区长
    {
        "id": 9,
        "name": "柳春林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年12月",
        "birthplace": "黑龙江五常",
        "education": "研究生学历，工学博士",
        "party_join": "中共党员",
        "work_start": "2000年7月",
        "current_post": "区委常委、常务副区长",
        "current_org": "西安市灞桥区人民政府",
        "source": "https://www.baqiao.gov.cn/zwgk/zfld/lcl/1.html"
    },
    # 李刚毅 — 区委常委、副区长
    {
        "id": 10,
        "name": "李刚毅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年1月",
        "birthplace": "陕西西安",
        "education": "大学本科",
        "party_join": "中共党员",
        "work_start": "1997年12月",
        "current_post": "区委常委、副区长",
        "current_org": "西安市灞桥区人民政府",
        "source": "https://www.baqiao.gov.cn/zwgk/zfld/lgy/1.html"
    },

    # ══════════════════════════════════════════════════════════════════════════
    # Government (区政府) Leadership
    # ══════════════════════════════════════════════════════════════════════════

    # 刘强 — 副区长
    {
        "id": 11,
        "name": "刘强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年3月",
        "birthplace": "陕西西安",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "1997年8月",
        "current_post": "副区长",
        "current_org": "西安市灞桥区人民政府",
        "source": "https://www.baqiao.gov.cn/zwgk/zfld/lq/1.html"
    },
    # 王亚军 — 副区长、公安分局局长
    {
        "id": 12,
        "name": "王亚军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年5月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长、公安灞桥分局党委书记、局长兼督察长",
        "current_org": "西安市公安局灞桥分局",
        "source": "https://www.baqiao.gov.cn/zwgk/zfld/wyj/1.html"
    },
    # 王丽琼 — 副区长
    {
        "id": 13,
        "name": "王丽琼",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1981年11月",
        "birthplace": "甘肃张掖",
        "education": "教育学硕士研究生",
        "party_join": "中共党员",
        "work_start": "2002年7月",
        "current_post": "副区长",
        "current_org": "西安市灞桥区人民政府",
        "source": "https://www.baqiao.gov.cn/zwgk/zfld/wlq/1.html"
    },

    # ══════════════════════════════════════════════════════════════════════════
    # 人大、政协
    # ══════════════════════════════════════════════════════════════════════════

    # 郭向卫 — 区人大常委会主任
    {
        "id": 14,
        "name": "郭向卫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "西安市灞桥区人民代表大会常务委员会",
        "source": "https://www.baqiao.gov.cn/xwzx/bqyw/2058814155827281921.html"
    },
    # 杨联合 — 区政协主席
    {
        "id": 15,
        "name": "杨联合",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "中国人民政治协商会议西安市灞桥区委员会",
        "source": "https://www.baqiao.gov.cn/xwzx/bqyw/2058814155827281921.html"
    },
    # 王志强 — 区人大常委会副主任
    {
        "id": 16,
        "name": "王志强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会副主任",
        "current_org": "西安市灞桥区人民代表大会常务委员会",
        "source": "https://www.baqiao.gov.cn/xwzx/bqyw/2035914891903164418.html"
    },
    # 袁焱 — 区人大常委会副主任
    {
        "id": 17,
        "name": "袁焱",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会副主任",
        "current_org": "西安市灞桥区人民代表大会常务委员会",
        "source": "https://www.baqiao.gov.cn/xwzx/bqyw/2058814155827281921.html"
    },
    # 孟新力 — 区政协副主席
    {
        "id": 18,
        "name": "孟新力",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协副主席",
        "current_org": "中国人民政治协商会议西安市灞桥区委员会",
        "source": "https://www.baqiao.gov.cn/xwzx/bqyw/2035914891903164418.html"
    },
]

organizations_data = [
    {
        "id": 1,
        "name": "中共西安市灞桥区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共西安市委员会",
        "location": "西安市灞桥区"
    },
    {
        "id": 2,
        "name": "西安市灞桥区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "西安市人民政府",
        "location": "西安市灞桥区"
    },
    {
        "id": 3,
        "name": "西安市灞桥区人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "西安市人民代表大会常务委员会",
        "location": "西安市灞桥区"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议西安市灞桥区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协西安市委员会",
        "location": "西安市灞桥区"
    },
    {
        "id": 5,
        "name": "中共西安市灞桥区纪律检查委员会",
        "type": "纪委",
        "level": "县处级",
        "parent": "中共西安市纪律检查委员会",
        "location": "西安市灞桥区"
    },
    {
        "id": 6,
        "name": "西安市公安局灞桥分局",
        "type": "政府",
        "level": "县处级",
        "parent": "西安市公安局",
        "location": "西安市灞桥区"
    },
]

positions_data = [
    # 区委（党委系统）
    {"person_id": 1, "org_id": 1, "title": "区委书记（空缺）", "start_date": "", "end_date": "present", "rank": "正处级", "note": "区委书记一职公开信息空缺"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "2022-03", "end_date": "present", "rank": "正处级", "note": "confirmed"},
    {"person_id": 3, "org_id": 1, "title": "区委副书记、政法委书记", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "confirmed via multiple news articles"},
    {"person_id": 4, "org_id": 5, "title": "区委常委、区纪委书记、区监委主任", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "confirmed via 区纪委全会"},
    {"person_id": 5, "org_id": 1, "title": "区委常委、组织部部长", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "confirmed via 区委工作会议"},
    {"person_id": 6, "org_id": 1, "title": "区委常委、宣传部部长、统战部部长", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "confirmed via 区委工作会议"},
    {"person_id": 7, "org_id": 1, "title": "区委常委", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "具体职务待确认"},
    {"person_id": 8, "org_id": 1, "title": "区委常委", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "可能为人武部长"},
    {"person_id": 9, "org_id": 2, "title": "区委常委、常务副区长", "start_date": "2022-03", "end_date": "present", "rank": "正处级", "note": "confirmed via government resume"},
    {"person_id": 10, "org_id": 2, "title": "区委常委、副区长", "start_date": "2023-12", "end_date": "present", "rank": "正处级", "note": "confirmed via government resume"},

    # 区政府
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "2022-03", "end_date": "present", "rank": "正处级", "note": "confirmed"},
    {"person_id": 11, "org_id": 2, "title": "副区长", "start_date": "2023-12", "end_date": "present", "rank": "副处级", "note": "confirmed via government resume"},
    {"person_id": 12, "org_id": 6, "title": "副区长、公安分局局长", "start_date": "2025-03", "end_date": "present", "rank": "副处级", "note": "confirmed via government resume"},
    {"person_id": 12, "org_id": 2, "title": "副区长", "start_date": "2025-03", "end_date": "present", "rank": "副处级", "note": "confirmed"},
    {"person_id": 13, "org_id": 2, "title": "副区长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "confirmed via government resume"},

    # 人大
    {"person_id": 14, "org_id": 3, "title": "区人大常委会主任", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 16, "org_id": 3, "title": "区人大常委会副主任", "start_date": "2026-03", "end_date": "present", "rank": "副处级", "note": "2026年3月两会当选"},
    {"person_id": 17, "org_id": 3, "title": "区人大常委会副主任", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": ""},

    # 政协
    {"person_id": 15, "org_id": 4, "title": "区政协主席", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 18, "org_id": 4, "title": "区政协副主席", "start_date": "2026-03", "end_date": "present", "rank": "副处级", "note": "2026年3月两会当选"},
]

relationships_data = [
    # 党政主要领导搭档
    {"person_a": 2, "person_b": 3, "type": "党政搭档", "context": "区委副书记（区长）与专职副书记、政法委书记工作关系", "overlap_org": "中共灞桥区委", "overlap_period": "unknown-present"},

    # 区委常委之间的工作关系
    {"person_a": 5, "person_b": 6, "type": "工作关系", "context": "组织部长与宣传部长（统战部长）同为区委职能部门负责人", "overlap_org": "中共灞桥区委", "overlap_period": "unknown-present"},
    {"person_a": 9, "person_b": 10, "type": "工作关系", "context": "常务副区长与副区长同为政府班子成员", "overlap_org": "灞桥区人民政府", "overlap_period": "2023-12-present"},
    {"person_a": 2, "person_b": 9, "type": "党政搭档", "context": "区长—常务副区长工作关系", "overlap_org": "灞桥区人民政府", "overlap_period": "2022-03-present"},
    {"person_a": 2, "person_b": 10, "type": "党政搭档", "context": "区长—副区长工作关系", "overlap_org": "灞桥区人民政府", "overlap_period": "2023-12-present"},
    {"person_a": 2, "person_b": 11, "type": "党政搭档", "context": "区长—副区长工作关系", "overlap_org": "灞桥区人民政府", "overlap_period": "2023-12-present"},
    {"person_a": 2, "person_b": 13, "type": "党政搭档", "context": "区长—副区长工作关系", "overlap_org": "灞桥区人民政府", "overlap_period": "unknown-present"},
    {"person_a": 2, "person_b": 4, "type": "工作关系", "context": "区委副书记（区长）与纪委书记工作关系", "overlap_org": "中共灞桥区委", "overlap_period": "unknown-present"},

    # 纪委与巡察
    {"person_a": 4, "person_b": 6, "type": "工作关系", "context": "纪委书记与区委常委马学智在巡察工作中配合", "overlap_org": "中共灞桥区委", "overlap_period": "unknown-present"},

    # 政法委与公安
    {"person_a": 3, "person_b": 12, "type": "工作关系", "context": "政法委书记与副区长兼公安分局局长工作关系", "overlap_org": "灞桥区政法系统", "overlap_period": "2025-03-present"},
]

# ═══════════════════════════════════════════════════════════════════════════════
# Person JSON generation template
# ═══════════════════════════════════════════════════════════════════════════════

PERSON_JSON_TEMPLATE = {
    "苏晓梅": {
        "filename": f"{TODAY}-陕西省-西安市-灞桥区-区长-苏晓梅.json",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "陕西省",
                "city": "西安市",
                "region": "灞桥区",
                "job": "区长",
                "task_id": "shaanxi_灞桥区",
                "time_focus": "2026"
            },
            "identity": {
                "person_id": "baqiao_su_xiaomei",
                "name": "苏晓梅",
                "aliases": [],
                "gender": "女",
                "ethnicity": "汉族",
                "birth": "1969年11月",
                "birthplace": "陕西泾阳",
                "native_place": "陕西泾阳",
                "education": ["在职研究生"],
                "party_join": "中共党员",
                "work_start": "1986年12月",
                "dedupe_keys": {
                    "name_birth": "苏晓梅_1969年11月",
                    "name_birthplace": "苏晓梅_陕西泾阳",
                    "official_profile_url": "https://www.baqiao.gov.cn/zwgk/zfld/zxg/1.html"
                }
            },
            "current_status": {
                "current_post": "区委副书记、区政府党组书记、区长",
                "current_org": "西安市灞桥区人民政府",
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001"]
            },
            "career_timeline": [
                {"start": "", "end": "", "org": "彬县", "title": "县委常委、宣传部长", "level": "县处级", "location": "陕西咸阳", "system": "party", "rank": "副处级", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "", "end": "", "org": "咸阳市委", "title": "副秘书长", "level": "地厅级", "location": "陕西咸阳", "system": "party", "rank": "正处级", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "", "end": "", "org": "兴平市", "title": "市委副书记、市长", "level": "县处级", "location": "陕西咸阳", "system": "government", "rank": "正处级", "is_key_promotion": True, "notes": "县级市市长", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "", "end": "", "org": "永寿县", "title": "县委书记", "level": "县处级", "location": "陕西咸阳", "system": "party", "rank": "正处级", "is_key_promotion": True, "notes": "县委书记（一把手）", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "", "end": "2022-03", "org": "省委老干局", "title": "副局长", "level": "省直", "location": "陕西西安", "system": "party", "rank": "副厅级", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "2022-03", "end": "present", "org": "西安市灞桥区人民政府", "title": "区委副书记、区长", "level": "县处级", "location": "陕西西安", "system": "government", "rank": "正处级", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
            ],
            "organizations": [],
            "relationships": [
                {"person": "李连永", "person_id": "baqiao_li_lianyong", "relationship_type": "overlap", "strength": "strong", "evidence": "区委副书记（区长）与专职副书记、政法委书记工作搭档", "overlap_org": "中共灞桥区委", "overlap_period": "unknown-present", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
                {"person": "柳春林", "person_id": "baqiao_liu_chunlin", "relationship_type": "overlap", "strength": "strong", "evidence": "区长—常务副区长工作搭档", "overlap_org": "灞桥区人民政府", "overlap_period": "2022-03-present", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
                {"person": "李刚毅", "person_id": "baqiao_li_gangyi", "relationship_type": "overlap", "strength": "strong", "evidence": "区长—副区长工作搭档", "overlap_org": "灞桥区人民政府", "overlap_period": "2023-12-present", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": ["县域治理", "宣传思想文化"],
                "secondary_specializations": ["老干部工作"],
                "career_pattern": "从县区宣传系统起步，历经县市长、县委书记、省直机关副局长、区长的多岗位历练",
                "systems_experience": ["party", "government"],
                "geographic_pattern": ["陕西泾阳→彬县→兴平→永寿→西安"],
                "promotion_velocity": {"summary": "从彬县宣传部长逐步晋升至县委书记，后调任省直机关副局长再转任灞桥区区长，跨系统调动较多", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {"public_style_indicators": [], "speech_themes": [], "management_signals": [], "caveat": "Work style is inferred from public records, not private psychological assessment."},
            "network_metrics": {},
            "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现公开的纪律处分、审计问题或负面报道", "date": "", "confidence": "unverified", "source_ids": []}],
            "source_register": [{"id": "S001", "title": "灞桥区人民政府—苏晓梅简历", "url": "https://www.baqiao.gov.cn/zwgk/zfld/zxg/1.html", "publisher": "灞桥区人民政府", "published_at": "2026-04-20", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "confirmed区长简历"}],
            "confidence_summary": {"identity": "confirmed", "current_role": "confirmed", "career_completeness": "high", "relationship_confidence": "high", "biggest_gap": "具体任职起止时间（如彬县宣传部长具体年份）"},
            "open_questions": [{"priority": "high", "question": "苏晓梅在彬县、兴平、永寿等职位的具体起止时间", "why_it_matters": "精确时间线对关系网络分析重要", "suggested_queries": ["苏晓梅 履历 彬县", "苏晓梅 兴平市长 任职时间"], "last_attempted": AS_OF}]
        }
    },
    "柳春林": {
        "filename": f"{TODAY}-陕西省-西安市-灞桥区-常务副区长-柳春林.json",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {"province": "陕西省", "city": "西安市", "region": "灞桥区", "job": "常务副区长", "task_id": "shaanxi_灞桥区", "time_focus": "2026"},
            "identity": {
                "person_id": "baqiao_liu_chunlin",
                "name": "柳春林",
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "1978年12月",
                "birthplace": "黑龙江五常",
                "native_place": "黑龙江五常",
                "education": ["研究生学历", "工学博士"],
                "party_join": "中共党员",
                "work_start": "2000年7月",
                "dedupe_keys": {"name_birth": "柳春林_1978年12月", "name_birthplace": "柳春林_黑龙江五常", "official_profile_url": "https://www.baqiao.gov.cn/zwgk/zfld/lcl/1.html"}
            },
            "current_status": {"current_post": "区委常委、常务副区长", "current_org": "西安市灞桥区人民政府", "administrative_rank": "正处级", "as_of": AS_OF, "is_current_confirmed": True, "source_ids": ["S001"]},
            "career_timeline": [
                {"start": "unknown", "end": "", "org": "西安石油大学石油工程学院", "title": "学生管理办公室副主任、团委书记", "level": "高校", "location": "陕西西安", "system": "education", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "", "end": "", "org": "西安石油大学党委组织部", "title": "正科级组织员、副部长", "level": "高校", "location": "陕西西安", "system": "education", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "", "end": "", "org": "西安市人社局", "title": "专业技术人员管理处副处长（正处级）、就业促进处处长", "level": "地厅级", "location": "陕西西安", "system": "government", "rank": "正处级", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "", "end": "2022-03", "org": "西安市碑林区委", "title": "区委常委、宣传部长", "level": "县处级", "location": "陕西西安", "system": "party", "rank": "正处级", "is_key_promotion": True, "notes": "挂职:杭州上城区区长助理、泰州文旅集团副总经理、中央党校学习", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "2022-03", "end": "present", "org": "西安市灞桥区人民政府", "title": "区委常委、常务副区长", "level": "县处级", "location": "陕西西安", "system": "government", "rank": "正处级", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
            ],
            "relationships": [{"person": "苏晓梅", "person_id": "baqiao_su_xiaomei", "relationship_type": "overlap", "strength": "strong", "evidence": "区长—常务副区长党政搭档", "overlap_org": "灞桥区人民政府", "overlap_period": "2022-03-present", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]}],
            "governance_record": [], "professional_profile": {"primary_specializations": ["高校管理", "人社工作", "宣传思想文化"], "secondary_specializations": [], "career_pattern": "高校→政府→区委→区政府", "systems_experience": ["education", "government", "party"], "geographic_pattern": ["黑龙江五常→西安"], "promotion_velocity": {"summary": "从高校处级干部转型为政府官员，碑林区委宣传部长后到灞桥区任常务副区长", "notable_fast_promotions": []}},
            "work_style_and_personality": {"public_style_indicators": [], "speech_themes": [], "management_signals": [], "caveat": ""},
            "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现公开的纪律处分", "date": "", "confidence": "unverified", "source_ids": []}],
            "source_register": [{"id": "S001", "title": "灞桥区人民政府—柳春林简历", "url": "https://www.baqiao.gov.cn/zwgk/zfld/lcl/1.html", "publisher": "灞桥区人民政府", "published_at": "2026-04-20", "accessed_at": AS_OF, "source_type": "official", "reliability": "high"}],
            "confidence_summary": {"identity": "confirmed", "current_role": "confirmed", "career_completeness": "high", "relationship_confidence": "high", "biggest_gap": "西安石油大学具体年份"},
            "open_questions": [{"priority": "medium", "question": "柳春林在碑林区的具体工作时间及前期经历细节", "why_it_matters": "完善履历时间线", "suggested_queries": ["柳春林 碑林区 任职时间"], "last_attempted": AS_OF}]
        }
    },
    "李刚毅": {
        "filename": f"{TODAY}-陕西省-西安市-灞桥区-副区长-李刚毅.json",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {"province": "陕西省", "city": "西安市", "region": "灞桥区", "job": "副区长", "task_id": "shaanxi_灞桥区", "time_focus": "2026"},
            "identity": {
                "person_id": "baqiao_li_gangyi",
                "name": "李刚毅",
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "1977年1月",
                "birthplace": "陕西西安",
                "native_place": "陕西西安",
                "education": ["大学本科"],
                "party_join": "中共党员",
                "work_start": "1997年12月",
                "dedupe_keys": {"name_birth": "李刚毅_1977年1月", "name_birthplace": "李刚毅_陕西西安", "official_profile_url": "https://www.baqiao.gov.cn/zwgk/zfld/lgy/1.html"}
            },
            "current_status": {"current_post": "区委常委、副区长", "current_org": "西安市灞桥区人民政府", "administrative_rank": "正处级", "as_of": AS_OF, "is_current_confirmed": True, "source_ids": ["S001"]},
            "career_timeline": [
                {"start": "", "end": "", "org": "长安区子午街道办事处", "title": "副主任", "level": "乡科级", "location": "陕西西安", "system": "government", "rank": "副科级", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "", "end": "", "org": "长安区子午街道党工委", "title": "副书记", "level": "乡科级", "location": "陕西西安", "system": "party", "rank": "正科级", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "", "end": "", "org": "长安区王曲街道办事处", "title": "主任", "level": "乡科级", "location": "陕西西安", "system": "government", "rank": "正科级", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "", "end": "", "org": "长安区王曲街道党工委", "title": "书记", "level": "乡科级", "location": "陕西西安", "system": "party", "rank": "正科级", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "", "end": "", "org": "长安区韦曲街道党工委", "title": "书记", "level": "乡科级", "location": "陕西西安", "system": "party", "rank": "正科级", "is_key_promotion": True, "notes": "长安区核心街道", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "", "end": "2023-12", "org": "西安市灞桥区人民政府", "title": "副区长", "level": "县处级", "location": "陕西西安", "system": "government", "rank": "副处级", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "2023-12", "end": "present", "org": "西安市灞桥区人民政府", "title": "区委常委、副区长", "level": "县处级", "location": "陕西西安", "system": "government", "rank": "正处级", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
            ],
            "relationships": [{"person": "苏晓梅", "person_id": "baqiao_su_xiaomei", "relationship_type": "overlap", "strength": "strong", "evidence": "区长—副区长工作搭档", "overlap_org": "灞桥区人民政府", "overlap_period": "2023-12-present", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]}],
            "governance_record": [], "professional_profile": {"primary_specializations": ["基层治理", "街道管理"], "secondary_specializations": [], "career_pattern": "从长安区街道基层逐级晋升至区领导", "systems_experience": ["party", "government"], "geographic_pattern": ["陕西西安→长安区→灞桥区"], "promotion_velocity": {"summary": "从街道副主任到区委常委、副区长，典型的基层逐级晋升路径", "notable_fast_promotions": []}},
            "work_style_and_personality": {"public_style_indicators": [{"trait": "military_civilian_focused", "evidence": "2026年带队慰问省军区干休所", "confidence": "plausible", "source_ids": ["S001"]}], "speech_themes": [], "management_signals": [], "caveat": ""},
            "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现公开的纪律处分", "date": "", "confidence": "unverified", "source_ids": []}],
            "source_register": [{"id": "S001", "title": "灞桥区人民政府—李刚毅简历", "url": "https://www.baqiao.gov.cn/zwgk/zfld/lgy/1.html", "publisher": "灞桥区人民政府", "published_at": "2026-04-20", "accessed_at": AS_OF, "source_type": "official", "reliability": "high"}],
            "confidence_summary": {"identity": "confirmed", "current_role": "confirmed", "career_completeness": "high", "relationship_confidence": "high", "biggest_gap": "各街道任职具体年份"},
            "open_questions": [{"priority": "medium", "question": "李刚毅在长安区各街道任职的具体起止时间", "why_it_matters": "完善履历时间线", "suggested_queries": ["李刚毅 长安区 任职"], "last_attempted": AS_OF}]
        }
    }
}

# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════

def write_person_json(data: dict, filename: str) -> Path:
    path = STAGING_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Wrote {path}")
    return path

def main():
    print(f"Building network for {SLUG}...")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print()

    run_build(
        slug=SLUG,
        persons=persons_data,
        organizations=organizations_data,
        positions=positions_data,
        relationships=relationships_data,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print()

    print("Writing person JSON files...")
    for key, entry in PERSON_JSON_TEMPLATE.items():
        write_person_json(entry["data"], entry["filename"])

    print()
    print("=" * 60)
    print(f"Build complete for {SLUG}")
    print(f"  {len(persons_data)} persons")
    print(f"  {len(organizations_data)} organizations")
    print(f"  {len(positions_data)} positions")
    print(f"  {len(relationships_data)} relationships")
    print(f"  {len(PERSON_JSON_TEMPLATE)} person JSONs")
    print("=" * 60)

if __name__ == "__main__":
    main()
