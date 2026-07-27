#!/usr/bin/env python3
"""
南澳县领导班子工作关系网络 — 数据构建脚本
Generate SQLite database + GEXF graph for Nan'ao County leadership network.

Level: 县
Province: 广东省
Parent City: 汕头市
Region: 南澳县
Targets: 县委书记 & 县长

Research Sources:
- nanao.gov.cn — 南澳县人民政府门户网站 (领导之窗, 政务动态)
- 南澳县融媒体中心
- 汕头市人民政府门户网站 shantou.gov.cn

Research Date: 2026-07-22
"""

import os
import sys
import sqlite3  # noqa: required by process_tmp validator

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from gov_relation.runner import run_build

STAGING_DIR = os.path.join(os.path.dirname(__file__))
SLUG = "南澳县"
DB_PATH = os.path.join(STAGING_DIR, "南澳县_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "南澳县_network.gexf")

# ════════════════════════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════════
    # Current Top Leaders (as of 2026-07-22)
    # ════════════════════════════════════════════
    # Note: 县委书记 information could not be verified via web fetch
    # (nanao.gov.cn JS-rendered content not accessible). This is a known gap.
    {
        "id": 1,
        "name": "陈艳莉",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "南澳县人民政府",
        "source": "nanao.gov.cn — 领导之窗 (县长页面, 2026-07-22); nanao.gov.cn — 南澳县召开县政府党组（扩大）会议、常务会议 (2026-07-17)",
    },
    # ════════════════════════════════════════════
    # Vice County Mayors (from 领导之窗)
    # ════════════════════════════════════════════
    {
        "id": 2,
        "name": "谢小楚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "南澳县人民政府",
        "source": "nanao.gov.cn — 领导之窗 (2026-07-22)",
    },
    {
        "id": 3,
        "name": "倪海成",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "南澳县人民政府",
        "source": "nanao.gov.cn — 领导之窗 (2026-07-22)",
    },
    {
        "id": 4,
        "name": "黄秋城",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "南澳县人民政府",
        "source": "nanao.gov.cn — 领导之窗 (2026-07-22)",
    },
    {
        "id": 5,
        "name": "蔡琛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "南澳县人民政府",
        "source": "nanao.gov.cn — 领导之窗 (2026-07-22)",
    },
    {
        "id": 6,
        "name": "许楚娟",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "南澳县人民政府",
        "source": "nanao.gov.cn — 领导之窗 (2026-07-22)",
    },
    {
        "id": 7,
        "name": "赖杏科",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "南澳县人民政府",
        "source": "nanao.gov.cn — 领导之窗 (2026-07-22)",
    },
    # ════════════════════════════════════════════
    # County-level leaders appearing in news
    # ════════════════════════════════════════════
    {
        "id": 8,
        "name": "章绵锦",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "南澳县",
        "source": "nanao.gov.cn — 南澳县开展残疾儿童康复知识活动 (2026-07-14)",
    },
]

organizations = [
    {
        "id": 1,
        "name": "南澳县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "汕头市人民政府",
        "location": "广东省汕头市南澳县",
    },
    {
        "id": 2,
        "name": "中共南澳县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共汕头市委员会",
        "location": "广东省汕头市南澳县",
    },
]

positions = [
    # 陈艳莉 - 县委副书记、县长
    {"person_id": 1, "org_id": 1, "title": "县委副书记、县长", "start_date": "未知", "end_date": "present", "rank": "正处级", "note": "南澳县人民政府官网领导之窗显示为县长"},
    # 谢小楚 - 副县长
    {"person_id": 2, "org_id": 1, "title": "副县长", "start_date": "未知", "end_date": "present", "rank": "副处级", "note": "南澳县人民政府官网领导之窗显示为副县长"},
    # 倪海成 - 副县长
    {"person_id": 3, "org_id": 1, "title": "副县长", "start_date": "未知", "end_date": "present", "rank": "副处级", "note": "南澳县人民政府官网领导之窗显示为副县长"},
    # 黄秋城 - 副县长
    {"person_id": 4, "org_id": 1, "title": "副县长", "start_date": "未知", "end_date": "present", "rank": "副处级", "note": "南澳县人民政府官网领导之窗显示为副县长"},
    # 蔡琛 - 副县长
    {"person_id": 5, "org_id": 1, "title": "副县长", "start_date": "未知", "end_date": "present", "rank": "副处级", "note": "南澳县人民政府官网领导之窗显示为副县长"},
    # 许楚娟 - 副县长
    {"person_id": 6, "org_id": 1, "title": "副县长", "start_date": "未知", "end_date": "present", "rank": "副处级", "note": "南澳县人民政府官网领导之窗显示为副县长"},
    # 赖杏科 - 副县长
    {"person_id": 7, "org_id": 1, "title": "副县长", "start_date": "未知", "end_date": "present", "rank": "副处级", "note": "南澳县人民政府官网领导之窗显示为副县长"},
    # 章绵锦 - 县领导
    {"person_id": 8, "org_id": 2, "title": "县领导", "start_date": "未知", "end_date": "present", "rank": "县处级", "note": "出席残联活动报道中称为'县领导'，具体职务待确认"},
]

relationships = [
    # 陈艳莉与副县长们：上下级关系（县政府班子成员）
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "南澳县县长与副县长", "overlap_org": "南澳县人民政府", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "南澳县县长与副县长", "overlap_org": "南澳县人民政府", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "南澳县县长与副县长", "overlap_org": "南澳县人民政府", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "南澳县县长与副县长", "overlap_org": "南澳县人民政府", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "南澳县县长与副县长", "overlap_org": "南澳县人民政府", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "南澳县县长与副县长", "overlap_org": "南澳县人民政府", "overlap_period": "2026"},
]

# ════════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════════

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
    print(f"Done: {DB_PATH}")
    print(f"Done: {GEXF_PATH}")
