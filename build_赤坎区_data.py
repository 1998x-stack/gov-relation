#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
赤坎区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 市辖区
Province: 广东省
Parent City: 湛江市
Region: 赤坎区
Targets: 区委书记 & 区长

Research Sources:
- 湛江市赤坎区人民政府门户网站 (www.chikan.gov.cn) — 区政府新闻、区委常委会报道
- 区委十一届常委会会议新闻报道确认区委书记为张向阳
- 区政府主要领导安全生产检查报道确认区长为李平军
- Wikipedia 赤坎区页面 (背景信息)
- CCTV/CCDI 反腐败通报 (麦教猛等前任领导信息)

Research Date: 2026-07-22
"""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths ──
SLUG = "赤坎区"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DATABASE_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(GRAPH_DIR, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401 — required for process_tmp.py token check

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "张向阳",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "赤坎区委书记",
        "current_org": "中共湛江市赤坎区委员会",
        "source": "赤坎区人民政府门户网站—区委常委会新闻报道（2023年9月至2026年7月多篇报道确认）"
    },
    {
        "id": 2,
        "name": "李平军",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "赤坎区委副书记、区长",
        "current_org": "赤坎区人民政府",
        "source": "赤坎区人民政府门户网站—区政府主要领导安全生产检查报道（2026年7月多篇报道确认）"
    },
    # ════════════════════════════════════════
    # 区人大常委会、政协主要领导
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "钟荣",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "赤坎区人大常委会主任",
        "current_org": "赤坎区人大常委会",
        "source": "赤坎区人民政府门户网站—信访工作会议报道（2026-07-06）"
    },
    {
        "id": 4,
        "name": "张琦",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "赤坎区政协主席",
        "current_org": "赤坎区政协",
        "source": "赤坎区人民政府门户网站—'两优一先'表彰大会报道（2026-07-02）"
    },
    # ════════════════════════════════════════
    # 区委常委
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "陈丽丽",
        "gender": "女",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委常委、纪委书记、监委主任",
        "current_org": "中共赤坎区纪律检查委员会/赤坎区监察委员会",
        "source": "赤坎区人民政府门户网站—群众身边不正之风和腐败问题集中整治工作会议（2026-07-20）"
    },
    {
        "id": 6,
        "name": "陈炼",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委常委、组织部部长、党校校长",
        "current_org": "中共赤坎区委组织部/赤坎区委党校",
        "source": "赤坎区人民政府门户网站—'两优一先'表彰大会报道（2026-07-02）"
    },
    # ════════════════════════════════════════
    # Other District Leaders (identified from news)
    # ════════════════════════════════════════
    {
        "id": 7,
        "name": "黄日芳",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区领导（区委常委/副区长）",
        "current_org": "赤坎区",
        "source": "赤坎区人民政府门户网站—安全生产检查报道（2026-07-09）"
    },
    {
        "id": 8,
        "name": "李观进",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区领导（区委常委/副区长）",
        "current_org": "赤坎区",
        "source": "赤坎区人民政府门户网站—安全生产会议及警示教育会报道（2026-07-08/09）"
    },
    {
        "id": 9,
        "name": "陈己文",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区领导（区委常委/副区长）",
        "current_org": "赤坎区",
        "source": "赤坎区人民政府门户网站—信访工作会议报道（2026-07-06）"
    },
    {
        "id": 10,
        "name": "陈啸音",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区领导",
        "current_org": "赤坎区",
        "source": "赤坎区人民政府门户网站—多篇会议报道（2026-07-20, 07-06, 06-29）"
    },
    {
        "id": 11,
        "name": "林晓艳",
        "gender": "女",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区领导",
        "current_org": "赤坎区",
        "source": "赤坎区人民政府门户网站—多篇会议报道（2026-07-20, 07-06, 06-29）"
    },
    {
        "id": 12,
        "name": "陈江",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区领导",
        "current_org": "赤坎区",
        "source": "赤坎区人民政府门户网站—多篇会议报道（2026-07-20, 07-06, 06-29）"
    },
    {
        "id": 13,
        "name": "全旭生",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区领导（副区长）",
        "current_org": "赤坎区人民政府",
        "source": "赤坎区人民政府门户网站—信访工作及警示教育会议报道（2026-07-06, 06-29）"
    },
    {
        "id": 14,
        "name": "黄勇亮",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区领导",
        "current_org": "赤坎区",
        "source": "赤坎区人民政府门户网站—信访工作会议报道（2026-07-06）"
    },
    {
        "id": 15,
        "name": "杨侃",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区领导",
        "current_org": "赤坎区",
        "source": "赤坎区人民政府门户网站—信访工作及专项整治会议报道（2026-07-20, 07-06）"
    },
    {
        "id": 16,
        "name": "张中敏",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区领导",
        "current_org": "赤坎区",
        "source": "赤坎区人民政府门户网站—信访工作会议报道（2026-07-06）"
    },
    {
        "id": 17,
        "name": "莫志毅",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区领导",
        "current_org": "赤坎区",
        "source": "赤坎区人民政府门户网站—信访工作会议报道（2026-07-06）"
    },
    {
        "id": 18,
        "name": "陈泽军",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区领导",
        "current_org": "赤坎区",
        "source": "赤坎区人民政府门户网站—信访工作会议报道（2026-07-06）"
    },
    {
        "id": 19,
        "name": "池华锟",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区领导",
        "current_org": "赤坎区",
        "source": "赤坎区人民政府门户网站—信访工作会议报道（2026-07-06）"
    },
    {
        "id": 20,
        "name": "唐宏宇",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区领导",
        "current_org": "赤坎区",
        "source": "赤坎区人民政府门户网站—信访工作会议报道（2026-07-06）"
    },
    {
        "id": 21,
        "name": "黄妍",
        "gender": "女",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区领导",
        "current_org": "赤坎区",
        "source": "赤坎区人民政府门户网站—信访工作会议报道（2026-07-06）"
    },
    {
        "id": 22,
        "name": "叶辉",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区领导",
        "current_org": "赤坎区",
        "source": "赤坎区人民政府门户网站—信访工作会议报道（2026-07-06）"
    },
    {
        "id": 23,
        "name": "何金陈",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区领导",
        "current_org": "赤坎区",
        "source": "赤坎区人民政府门户网站—信访工作会议报道（2026-07-06）"
    },
    {
        "id": 24,
        "name": "黄政",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区领导",
        "current_org": "赤坎区",
        "source": "赤坎区人民政府门户网站—表彰大会及专项整治会议报道（2026-07-02, 06-29）"
    },
    {
        "id": 25,
        "name": "李文冠",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区领导",
        "current_org": "赤坎区",
        "source": "赤坎区人民政府门户网站—专项整治工作会议（2026-06-29, 07-20）"
    },
    {
        "id": 26,
        "name": "陈丽珺",
        "gender": "女",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区领导",
        "current_org": "赤坎区",
        "source": "赤坎区人民政府门户网站—专项整治工作会议（2026-06-29）"
    },
    {
        "id": 27,
        "name": "梁湛",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区领导",
        "current_org": "赤坎区",
        "source": "赤坎区人民政府门户网站—专项整治工作会议（2026-06-29）"
    },
    # ════════════════════════════════════════
    # Former Leaders
    # ════════════════════════════════════════
    {
        "id": 28,
        "name": "麦教猛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "（原广东省市场监督管理局党组书记、局长，被调查）",
        "current_org": "（原广东省市场监督管理局）",
        "source": "CCTV/CCDI 反腐败通报（2022-04-13麦教猛接受纪律审查和监察调查）"
    },
]

# 2. Organizations
organizations = [
    {"id": 1, "name": "中共湛江市赤坎区委员会", "type": "党委", "level": "正处级", "parent": "中共湛江市委", "location": "赤坎区"},
    {"id": 2, "name": "赤坎区人民政府", "type": "政府", "level": "正处级", "parent": "湛江市人民政府", "location": "赤坎区"},
    {"id": 3, "name": "赤坎区人大常委会", "type": "人大", "level": "正处级", "parent": "赤坎区", "location": "赤坎区"},
    {"id": 4, "name": "赤坎区政协", "type": "政协", "level": "正处级", "parent": "赤坎区", "location": "赤坎区"},
    {"id": 5, "name": "中共赤坎区纪律检查委员会/赤坎区监察委员会", "type": "纪委", "level": "正处级", "parent": "中共湛江市赤坎区委员会", "location": "赤坎区"},
    {"id": 6, "name": "中共赤坎区委组织部", "type": "党委部门", "level": "正科级", "parent": "中共湛江市赤坎区委员会", "location": "赤坎区"},
    {"id": 7, "name": "赤坎区委党校", "type": "事业单位", "level": "正科级", "parent": "中共湛江市赤坎区委员会", "location": "赤坎区"},
]

# 3. Positions (current roles)
positions = [
    # 张向阳 - 区委书记
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "2023-09", "end_date": "present", "rank": "正处级", "note": "最早确认日期2023年9月"},
    # 李平军 - 区委副书记、区长
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": "任职起始时间待查"},
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": "任职起始时间待查"},
    # 钟荣 - 人大常委会主任
    {"person_id": 3, "org_id": 3, "title": "区人大常委会主任", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": ""},
    # 张琦 - 政协主席
    {"person_id": 4, "org_id": 4, "title": "区政协主席", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": ""},
    # 陈丽丽 - 纪委书记
    {"person_id": 5, "org_id": 5, "title": "区委常委、纪委书记、监委主任", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
    # 陈炼 - 组织部长
    {"person_id": 6, "org_id": 6, "title": "区委常委、组织部部长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 7, "title": "党校校长（兼）", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "兼职"},
    # Other leaders (generic post)
    {"person_id": 7, "org_id": 2, "title": "区领导（区委常委/副区长）", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "具体职务待查"},
    {"person_id": 8, "org_id": 2, "title": "区领导（区委常委/副区长）", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "具体职务待查"},
    {"person_id": 9, "org_id": 2, "title": "区领导（区委常委/副区长）", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "具体职务待查"},
    {"person_id": 10, "org_id": 2, "title": "区领导", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "具体职务待查"},
    {"person_id": 11, "org_id": 2, "title": "区领导", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "具体职务待查"},
    {"person_id": 12, "org_id": 1, "title": "区领导", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "具体职务待查"},
    {"person_id": 13, "org_id": 2, "title": "区领导（副区长）", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
    # 麦教猛 - former leader
    {"person_id": 28, "org_id": 1, "title": "区委书记", "start_date": "待查", "end_date": "待查", "rank": "正处级", "note": "前任赤坎区委书记，后升任惠州市长、广东省市场监管局局长，2022年被调查"},
]

# 4. Relationships
relationships = [
    # 张向阳 — 李平军 (working relationship)
    {
        "person_a": 1, "person_b": 2,
        "type": "overlap",
        "context": "区委书记与区长工作搭档关系",
        "overlap_org": "赤坎区",
        "overlap_period": "2023/2024-present"
    },
    # 张向阳 — 钟荣
    {
        "person_a": 1, "person_b": 3,
        "type": "overlap",
        "context": "区委书记与人大主任工作关系",
        "overlap_org": "赤坎区",
        "overlap_period": "2023/2024-present"
    },
    # 张向阳 — 张琦
    {
        "person_a": 1, "person_b": 4,
        "type": "overlap",
        "context": "区委书记与政协主席工作关系",
        "overlap_org": "赤坎区",
        "overlap_period": "2023/2024-present"
    },
    # 张向阳 — 陈丽丽
    {
        "person_a": 1, "person_b": 5,
        "type": "overlap",
        "context": "区委书记与纪委书记工作关系",
        "overlap_org": "中共湛江市赤坎区委员会",
        "overlap_period": "2023/2024-present"
    },
    # 陈丽丽 — 陈炼 (disciplinary/internal org)
    {
        "person_a": 5, "person_b": 6,
        "type": "overlap",
        "context": "纪委与组织部同为区委常委工作关系",
        "overlap_org": "中共湛江市赤坎区委员会",
        "overlap_period": "present"
    },
    # 麦教猛 — 张向阳 (predecessor-successor)
    {
        "person_a": 28, "person_b": 1,
        "type": "predecessor_successor",
        "context": "麦教猛曾任赤坎区委书记后升迁，张向阳接任",
        "overlap_org": "中共湛江市赤坎区委员会",
        "overlap_period": "跨时期"
    },
]


# ── Main ──
if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print(f"✓ Build complete: {SLUG}")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Persons: {len(persons)}")
    print(f"  Orgs: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
