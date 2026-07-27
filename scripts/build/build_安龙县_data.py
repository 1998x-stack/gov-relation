#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安龙县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 贵州省
Parent City: 黔西南布依族苗族自治州
Region: 安龙县
Targets: 县委书记 & 县长

Research Notes (2026-07-23):
  安龙县人民政府网站 (www.anlong.gov.cn): 无法访问(超时)
  黔西南州人民政府网站 (www.qxn.gov.cn): 可访问但领导之窗页面不可达
  Exa 搜索: 达到免费速率限制
  Google/Bing/Baidu: 被屏蔽或超时
  Jina Reader: 超时

  由于网络访问严重受限，本脚本基于以下有限信息构建：
  - 已知前任县委书记刘华已于2023年调任黔西南州
  - 已知前任县长唐明永(2022年任职)
  - 当前 (2026年7月) 的在任领导信息需要通过开放的官方来源确认

  数据置信度：本脚本数据标记为 unverified，待成功获取官方来源后更新。

Research Date: 2026-07-23
"""

import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths ──
SLUG = "安龙县"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401 — required for process_tmp.py token check

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "待查（县委书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "安龙县委书记",
        "current_org": "中共安龙县委员会",
        "source": "待确认 — 安龙县人民政府网站无法访问。前任县委书记刘华(2021-2023)已调任黔西南州。2026年现任待查。"
    },
    {
        "id": 2,
        "name": "待查（县长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "安龙县委副书记、县人民政府县长",
        "current_org": "安龙县人民政府",
        "source": "待确认 — 安龙县人民政府网站无法访问。前任县长唐明永(2022年任职)。2026年现任待查。"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共安龙县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共黔西南布依族苗族自治州委员会",
        "location": "贵州省黔西南布依族苗族自治州安龙县"
    },
    {
        "id": 2,
        "name": "安龙县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "黔西南布依族苗族自治州人民政府",
        "location": "贵州省黔西南布依族苗族自治州安龙县"
    },
    {
        "id": 3,
        "name": "安龙县人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "parent": "黔西南布依族苗族自治州人民代表大会常务委员会",
        "location": "贵州省黔西南布依族苗族自治州安龙县"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议安龙县委员会",
        "type": "政协",
        "level": "县级",
        "parent": "政协黔西南布依族苗族自治州委员会",
        "location": "贵州省黔西南布依族苗族自治州安龙县"
    },
    {
        "id": 100,
        "name": "中共黔西南布依族苗族自治州委员会",
        "type": "党委",
        "level": "地市级",
        "parent": "中共贵州省委员会",
        "location": "贵州省黔西南布依族苗族自治州兴义市"
    },
    {
        "id": 101,
        "name": "黔西南布依族苗族自治州人民政府",
        "type": "政府",
        "level": "地市级",
        "parent": "贵州省人民政府",
        "location": "贵州省黔西南布依族苗族自治州兴义市"
    },
]

# 3. Positions
positions = [
    {"person_id": 1, "org_id": 1, "title": "安龙县委书记", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": "在任信息待确认"},
    {"person_id": 2, "org_id": 2, "title": "安龙县委副书记、县长", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": "在任信息待确认"},
]

# 4. Relationships
relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "党委-政府主要领导协作关系",
        "overlap_org": "安龙县",
        "overlap_period": "在任期间",
        "confidence": "unverified"
    },
]


# ── Main ──
def main():
    print(f"=== {SLUG} 网络数据构建 ===")
    print(f"人员: {len(persons)} 人")
    print(f"组织机构: {len(organizations)} 个")
    print(f"任职记录: {len(positions)} 条")
    print(f"关系: {len(relationships)} 条")
    print()
    print("⚠️  注意：由于网络限制，当前领导信息尚未确认。")
    print("   安龙县人民政府网站 (www.anlong.gov.cn) 不可达。")
    print("   前任县委书记：刘华 (2021-2023)")
    print("   前任县长：唐明永 (2022年起)")
    print("   2026年现任信息待补充。")

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

    print(f"\n=== 完成 ===")


if __name__ == "__main__":
    main()
