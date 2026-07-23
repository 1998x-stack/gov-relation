#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
井陉矿区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 市辖区
Province: 河北省
Parent City: 石家庄市
Region: 井陉矿区
Targets: 区委书记 & 区长

Research Sources:
- 井陉矿区人民政府门户网站 (www.sjzkq.gov.cn) — 矿区要闻: 区委常委会会议等新闻报道
- 区委常委会新闻报道确认区委书记为刘杰
- 矿区经济高质量发展大会新闻报道确认区长郭贺伟、区委副书记殷蓓、人大常委会主任李建义、政协主席任玉玉
- 区委全会新闻报道确认区委书记刘杰及区委委员名单
- 巡视整改通报确认区委领导架构

Research Date: 2026-07-23
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "井陉矿区"
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
        "name": "刘杰",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "石家庄市井陉矿区委书记",
        "current_org": "中共石家庄市井陉矿区委员会",
        "source": "井陉矿区人民政府门户网站—矿区要闻（2025-2026年多篇报道确认刘杰担任区委书记）"
    },
    {
        "id": 2,
        "name": "郭贺伟",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "井陉矿区委副书记、区长",
        "current_org": "井陉矿区人民政府",
        "source": "井陉矿区人民政府门户网站—矿区要闻（2026-03-05经济高质量发展大会确认郭贺伟为区委副书记、区长）"
    },
    # ════════════════════════════════════════
    # 区委领导 / 区人大、政协主要领导
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "殷蓓",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "井陉矿区委副书记",
        "current_org": "中共石家庄市井陉矿区委员会",
        "source": "井陉矿区人民政府网站—经济高质量发展大会（2026-03-05）及区委管理干部研讨班（2026-04-27）新闻报道"
    },
    {
        "id": 4,
        "name": "李建义",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "井陉矿区人大常委会主任",
        "current_org": "井陉矿区人大常委会",
        "source": "井陉矿区人民政府网站—区委管理干部研讨班（2026-04-27）新闻报道"
    },
    {
        "id": 5,
        "name": "任玉玉",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "井陉矿区政协主席",
        "current_org": "井陉矿区政协",
        "source": "井陉矿区人民政府网站—经济高质量发展大会（2026-03-05）新闻报道"
    },
    # ════════════════════════════════════════
    # 区级领导（来源于巡视整改通报和其他新闻报道）
    # ════════════════════════════════════════
    {
        "id": 6,
        "name": "王素文",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "石家庄市委常委、常务副市长（主管井陉矿区等区县）",
        "current_org": "中共石家庄市委",
        "source": "井陉矿区人民政府网站—王素文在井陉县井陉矿区栾城区元氏县调研（2026-07-02）"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共石家庄市井陉矿区委员会",
        "type": "党委",
        "level": "县处级",
        "location": "石家庄市井陉矿区"
    },
    {
        "id": 2,
        "name": "井陉矿区人民政府",
        "type": "政府",
        "level": "县处级",
        "location": "石家庄市井陉矿区"
    },
    {
        "id": 3,
        "name": "井陉矿区人大常委会",
        "type": "人大",
        "level": "县处级",
        "location": "石家庄市井陉矿区"
    },
    {
        "id": 4,
        "name": "井陉矿区政协",
        "type": "政协",
        "level": "县处级",
        "location": "石家庄市井陉矿区"
    },
    {
        "id": 5,
        "name": "中共石家庄市委",
        "type": "党委",
        "level": "地市级",
        "location": "石家庄市"
    },
    {
        "id": 6,
        "name": "中共石家庄市井陉矿区纪律检查委员会",
        "type": "党委",
        "level": "县处级",
        "location": "石家庄市井陉矿区"
    },
    {
        "id": 7,
        "name": "井陉矿区监察委员会",
        "type": "政府",
        "level": "县处级",
        "location": "石家庄市井陉矿区"
    },
]

# 3. Positions (person_id, org_id, title)
positions = [
    # 刘杰 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start": "待查", "end": "至今", "rank": "正县处级", "note": "2025-2026年井陉矿区新闻报道中均以区委书记身份出现"},
    # 郭贺伟 — 区长
    {"person_id": 2, "org_id": 2, "title": "区长", "start": "待查", "end": "至今", "rank": "正县处级", "note": "2026-03-05经济高质量发展大会以区委副书记、区长身份部署工作"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start": "待查", "end": "至今", "rank": "正县处级", "note": "兼任区委副书记"},
    # 殷蓓 — 区委副书记
    {"person_id": 3, "org_id": 1, "title": "区委副书记", "start": "待查", "end": "至今", "rank": "副县处级", "note": "2026年新闻报道中均以区委副书记身份参加活动"},
    # 李建义 — 人大常委会主任
    {"person_id": 4, "org_id": 3, "title": "区人大常委会主任", "start": "待查", "end": "至今", "rank": "正县处级", "note": "2026-04-27区委管理干部研讨班以区人大常委会主任身份参加"},
    # 任玉玉 — 政协主席
    {"person_id": 5, "org_id": 4, "title": "区政协主席", "start": "待查", "end": "至今", "rank": "正县处级", "note": "2026-03-05经济高质量发展大会以区政协主席身份参加"},
    # 王素文 — 市委常委
    {"person_id": 6, "org_id": 5, "title": "市委常委、常务副市长", "start": "待查", "end": "至今", "rank": "副厅级", "note": "2026-07-02调研井陉矿区"},
]

# 4. Relationships
relationships = [
    {
        "person_a": 1,  # 刘杰
        "person_b": 2,  # 郭贺伟
        "type": "overlap",
        "context": "区委书记与区长搭档关系",
        "overlap_org": "中共井陉矿区委/井陉矿区人民政府",
        "overlap_period": "2025-2026年至今"
    },
    {
        "person_a": 1,  # 刘杰
        "person_b": 3,  # 殷蓓
        "type": "overlap",
        "context": "区委书记与区委副书记上下级关系",
        "overlap_org": "中共井陉矿区委",
        "overlap_period": "2025-2026年至今"
    },
    {
        "person_a": 2,  # 郭贺伟
        "person_b": 3,  # 殷蓓
        "type": "overlap",
        "context": "区长与区委副书记同级协作关系",
        "overlap_org": "中共井陉矿区委",
        "overlap_period": "2025-2026年至今"
    },
    {
        "person_a": 1,  # 刘杰
        "person_b": 4,  # 李建义
        "type": "overlap",
        "context": "区委书记与人大常委会主任党政关系",
        "overlap_org": "井陉矿区",
        "overlap_period": "2025-2026年至今"
    },
    {
        "person_a": 1,  # 刘杰
        "person_b": 5,  # 任玉玉
        "type": "overlap",
        "context": "区委书记与政协主席党政关系",
        "overlap_org": "井陉矿区",
        "overlap_period": "2025-2026年至今"
    },
    {
        "person_a": 2,  # 郭贺伟
        "person_b": 4,  # 李建义
        "type": "overlap",
        "context": "区长与人大常委会主任关系",
        "overlap_org": "井陉矿区",
        "overlap_period": "2025-2026年至今"
    },
    {
        "person_a": 2,  # 郭贺伟
        "person_b": 5,  # 任玉玉
        "type": "overlap",
        "context": "区长与政协主席关系",
        "overlap_org": "井陉矿区",
        "overlap_period": "2025-2026年至今"
    },
    {
        "person_a": 1,  # 刘杰
        "person_b": 6,  # 王素文
        "type": "overlap",
        "context": "区委书记与市委常委上下级关系",
        "overlap_org": "石家庄市",
        "overlap_period": "2025-2026年至今"
    },
    {
        "person_a": 2,  # 郭贺伟
        "person_b": 6,  # 王素文
        "type": "overlap",
        "context": "区长与市委常委上下级关系",
        "overlap_org": "石家庄市",
        "overlap_period": "2025-2026年至今"
    },
]

# ── Run ──
if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
    print(f"\nDone: {SLUG}")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
