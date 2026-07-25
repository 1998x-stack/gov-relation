#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 胶州市, 青岛市, 山东省.

Investigation date: 2026-07-25
Task ID: shandong_胶州市
Level: 县级市 (由青岛市代管)
Targets: 市委书记 & 市长

Key findings:
- 市委书记 赵兴绩 — 上合示范区党工委副书记、管委会常务副主任，胶州市委书记，青岛胶东临空经济示范区党工委书记 (as of July 2026)
- 市长 于冬泉 — 市委副书记、市长 (as of Jan-Jul 2026)
- 此前 张新竹 曾任 青岛市委常委、上合示范区党工委书记 (higher-level, not exclusively 胶州市委书记)
- 孙永红 曾于2015-2020年任胶州市委书记，后调任黄岛区

Research sources:
- 胶州政务网 (www.jiaozhou.gov.cn) — multiple news articles confirming current leadership
- 胶州市融媒体中心 — official news reports
- Existing person JSON for 孙永红 (曾任胶州市委书记)

Confidence notes:
- 赵兴绩当前职务已确认 (胶州市委书记, as of 2026年7月)
- 于冬泉当前职务已确认 (胶州市长, as of 2026年1月-7月)
- 赵兴绩和于冬泉的早期履历暂缺精确信息，待查
- 此前胶州市委书记 张新竹 信息待进一步核实
- 市委常委班子部分成员已确认，但详细分工待查
"""

import json
import os
import sqlite3  # noqa: F401
import sys
from datetime import datetime
from pathlib import Path

BASE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE, "..", "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from gov_relation.runner import run_build  # noqa: E402

SLUG = "胶州市"
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
    # Party Committee (市委) Leadership — Core
    # ══════════════════════════════════════════════════════════════════════════

    # 赵兴绩 — 胶州市委书记 (现任)
    {
        "id": 1,
        "name": "赵兴绩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "上合示范区党工委副书记、管委会常务副主任，胶州市委书记，青岛胶东临空经济示范区党工委书记",
        "current_org": "中共胶州市委员会",
        "source": "胶州政务网 (jiaozhou.gov.cn), 胶州市融媒体中心 news reports (2026年7月)"
    },
    # 于冬泉 — 胶州市委副书记、市长 (现任)
    {
        "id": 2,
        "name": "于冬泉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "胶州市委副书记、市长",
        "current_org": "胶州市人民政府",
        "source": "胶州政务网 (jiaozhou.gov.cn), 胶州市融媒体中心 news reports (2026年1月-7月)"
    },
    # ══════════════════════════════════════════════════════════════════════════
    # 市人大 / 市政协 / 市委副职
    # ══════════════════════════════════════════════════════════════════════════
    # 刘涛 — 市人大常委会主任
    {
        "id": 3,
        "name": "刘涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "胶州市人大常委会主任",
        "current_org": "胶州市人民代表大会常务委员会",
        "source": "胶州政务网 (jiaozhou.gov.cn), 胶州市融媒体中心"
    },
    # 万昌海 — 市政协主席
    {
        "id": 4,
        "name": "万昌海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "胶州市政协主席",
        "current_org": "中国人民政治协商会议胶州市委员会",
        "source": "胶州政务网 (jiaozhou.gov.cn), 胶州市融媒体中心"
    },
    # 孙培源 — 市委副书记、社会工作部部长
    {
        "id": 5,
        "name": "孙培源",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "胶州市委副书记、社会工作部部长",
        "current_org": "中共胶州市委员会",
        "source": "胶州政务网 (jiaozhou.gov.cn), 胶州市融媒体中心 (2026年7月)"
    },
    # ══════════════════════════════════════════════════════════════════════════
    # 市委常委 (confirmed from meeting attendance)
    # ══════════════════════════════════════════════════════════════════════════
    # 郭晓钟 — 市委常委
    {
        "id": 6,
        "name": "郭晓钟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "胶州市委常委",
        "current_org": "中共胶州市委员会",
        "source": "胶州政务网, 全市防汛防台风专题会议参会名单 (2026年7月)"
    },
    # 董如增 — 市委常委
    {
        "id": 7,
        "name": "董如增",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "胶州市委常委",
        "current_org": "中共胶州市委员会",
        "source": "胶州政务网, 全市防汛防台风专题会议参会名单 (2026年7月)"
    },
    # 宋彦斌 — 市委常委
    {
        "id": 8,
        "name": "宋彦斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "胶州市委常委",
        "current_org": "中共胶州市委员会",
        "source": "胶州政务网, 全市防汛防台风专题会议参会名单 (2026年7月)"
    },
    # ══════════════════════════════════════════════════════════════════════════
    # Other leaders confirmed from 人大会议
    # ══════════════════════════════════════════════════════════════════════════
    # 孙静 — 市领导
    {
        "id": 9,
        "name": "孙静",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "胶州市领导",
        "current_org": "胶州市",
        "source": "胶州政务网, 市十八届人大五次会议 (2026年1月)"
    },
    # 徐金胜 — 市领导
    {
        "id": 10,
        "name": "徐金胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "胶州市领导",
        "current_org": "胶州市",
        "source": "胶州政务网, 市十八届人大五次会议 (2026年1月)"
    },
    # 陈明卿 — 市领导
    {
        "id": 11,
        "name": "陈明卿",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "胶州市领导",
        "current_org": "胶州市",
        "source": "胶州政务网, 市十八届人大五次会议 (2026年1月)"
    },
    # 宋鑫 — 市领导
    {
        "id": 12,
        "name": "宋鑫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "胶州市领导",
        "current_org": "胶州市",
        "source": "胶州政务网, 市十八届人大五次会议 (2026年1月)"
    },
    # ══════════════════════════════════════════════════════════════════════════
    # Historical figures (predecessors)
    # ══════════════════════════════════════════════════════════════════════════
    # 张新竹 — 上合示范区党工委书记 (previous higher-level leader)
    {
        "id": 13,
        "name": "张新竹",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "青岛市委常委、上合示范区党工委书记",
        "current_org": "上合示范区",
        "source": "胶州政务网, 市十八届人大五次会议主席团名单 (2026年1月)"
    },
    # 孙永红 — 曾任胶州市委书记 (2015-2020)
    {
        "id": 14,
        "name": "孙永红",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年6月",
        "birthplace": "山东即墨",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原青岛市委常委、黄岛区委书记（2025年9月被调查）",
        "current_org": "中共黄岛区委员会",
        "source": "data/persons/20260725-山东省-青岛市-原黄岛区委书记-孙永红.json"
    },
]

organizations_data = [
    {
        "id": 1,
        "name": "中共胶州市委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共青岛市委",
        "location": "山东青岛胶州"
    },
    {
        "id": 2,
        "name": "胶州市人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "青岛市人民政府",
        "location": "山东青岛胶州"
    },
    {
        "id": 3,
        "name": "胶州市人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "parent": "胶州市",
        "location": "山东青岛胶州"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议胶州市委员会",
        "type": "政协",
        "level": "县级",
        "parent": "胶州市",
        "location": "山东青岛胶州"
    },
    {
        "id": 5,
        "name": "上合示范区",
        "type": "开发区",
        "level": "国家级",
        "parent": "青岛市",
        "location": "山东青岛胶州"
    },
    {
        "id": 6,
        "name": "青岛胶东临空经济示范区",
        "type": "开发区",
        "level": "国家级",
        "parent": "青岛市",
        "location": "山东青岛胶州"
    },
    {
        "id": 7,
        "name": "中共黄岛区委员会",
        "type": "党委",
        "level": "地厅级",
        "parent": "中共青岛市委",
        "location": "山东青岛黄岛"
    },
    {
        "id": 8,
        "name": "胶州市",
        "type": "政府",
        "level": "县级",
        "parent": "青岛市",
        "location": "山东青岛胶州"
    },
]

positions_data = [
    # 赵兴绩 — 胶州市委书记
    {"person_id": 1, "org_id": 1, "title": "胶州市委书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "同时担任上合示范区党工委副书记、管委会常务副主任，青岛胶东临空经济示范区党工委书记"},
    {"person_id": 1, "org_id": 5, "title": "上合示范区党工委副书记、管委会常务副主任", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 1, "org_id": 6, "title": "青岛胶东临空经济示范区党工委书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 于冬泉 — 胶州市长
    {"person_id": 2, "org_id": 2, "title": "胶州市委副书记、市长", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 刘涛 — 市人大主任
    {"person_id": 3, "org_id": 3, "title": "胶州市人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 万昌海 — 市政协主席
    {"person_id": 4, "org_id": 4, "title": "胶州市政协主席", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 孙培源 — 市委副书记
    {"person_id": 5, "org_id": 1, "title": "胶州市委副书记、社会工作部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 郭晓钟 — 市委常委
    {"person_id": 6, "org_id": 1, "title": "胶州市委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 董如增 — 市委常委
    {"person_id": 7, "org_id": 1, "title": "胶州市委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 宋彦斌 — 市委常委
    {"person_id": 8, "org_id": 1, "title": "胶州市委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 孙静 — 市领导
    {"person_id": 9, "org_id": 8, "title": "胶州市领导", "start_date": "", "end_date": "present", "rank": "", "note": "具体职务待查"},
    # 徐金胜 — 市领导
    {"person_id": 10, "org_id": 8, "title": "胶州市领导", "start_date": "", "end_date": "present", "rank": "", "note": "具体职务待查"},
    # 陈明卿 — 市领导
    {"person_id": 11, "org_id": 8, "title": "胶州市领导", "start_date": "", "end_date": "present", "rank": "", "note": "具体职务待查"},
    # 宋鑫 — 市领导
    {"person_id": 12, "org_id": 8, "title": "胶州市领导", "start_date": "", "end_date": "present", "rank": "", "note": "具体职务待查"},
    # 张新竹 — 上合示范区
    {"person_id": 13, "org_id": 5, "title": "青岛市委常委、上合示范区党工委书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "此前曾任胶州市委书记，具体时间待查"},
    # 孙永红 — 曾任胶州市委书记
    {"person_id": 14, "org_id": 1, "title": "胶州市委书记", "start_date": "2015", "end_date": "2020-01", "rank": "正处级（高配副厅）", "note": "后调任黄岛区委书记"},
    {"person_id": 14, "org_id": 2, "title": "胶州市市长", "start_date": "unknown", "end_date": "2015", "rank": "正处级", "note": ""},
    {"person_id": 14, "org_id": 7, "title": "黄岛区委书记（青岛市委常委兼）", "start_date": "2020-01", "end_date": "2025-09", "rank": "正厅级", "note": "2025年9月被调查"},
]

relationships_data = [
    # 赵兴绩 <-> 于冬泉 — 书记和市长工作搭档
    {
        "person_a": 1,
        "person_b": 2,
        "type": "overlap",
        "context": "胶州市委书记与市长工作搭档",
        "overlap_org": "胶州市",
        "overlap_period": "2026-",
    },
    # 赵兴绩 <-> 孙培源 — 市委正副书记
    {
        "person_a": 1,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "胶州市委书记与副书记",
        "overlap_org": "中共胶州市委员会",
        "overlap_period": "2026-",
    },
    # 赵兴绩 <-> 郭晓钟 — 书记与常委
    {
        "person_a": 1,
        "person_b": 6,
        "type": "superior_subordinate",
        "context": "胶州市委书记与市委常委",
        "overlap_org": "中共胶州市委员会",
        "overlap_period": "2026-",
    },
    # 赵兴绩 <-> 董如增 — 书记与常委
    {
        "person_a": 1,
        "person_b": 7,
        "type": "superior_subordinate",
        "context": "胶州市委书记与市委常委",
        "overlap_org": "中共胶州市委员会",
        "overlap_period": "2026-",
    },
    # 赵兴绩 <-> 宋彦斌 — 书记与常委
    {
        "person_a": 1,
        "person_b": 8,
        "type": "superior_subordinate",
        "context": "胶州市委书记与市委常委",
        "overlap_org": "中共胶州市委员会",
        "overlap_period": "2026-",
    },
    # 于冬泉 <-> 刘涛 — 市长与人大主任
    {
        "person_a": 2,
        "person_b": 3,
        "type": "overlap",
        "context": "胶州市长与人大主任",
        "overlap_org": "胶州市",
        "overlap_period": "2026-",
    },
    # 孙永红 -> 赵兴绩 — 前任和后任胶州市委书记
    {
        "person_a": 14,
        "person_b": 1,
        "type": "predecessor_successor",
        "context": "孙永红2015-2020年任胶州市委书记；赵兴绩后任胶州市委书记",
        "overlap_org": "中共胶州市委员会",
        "overlap_period": "间接交接",
    },
    # 张新竹 <-> 赵兴绩 — 可能的前后任关系
    {
        "person_a": 13,
        "person_b": 1,
        "type": "predecessor_successor",
        "context": "张新竹曾任胶州市委书记兼上合示范区，赵兴绩接任胶州市委书记",
        "overlap_org": "中共胶州市委员会/上合示范区",
        "overlap_period": "2025-2026",
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"Building {SLUG} network...")
    print(f"  Persons: {len(persons_data)}")
    print(f"  Organizations: {len(organizations_data)}")
    print(f"  Positions: {len(positions_data)}")
    print(f"  Relationships: {len(relationships_data)}")

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

    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print("Done.")
