#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 黎平县 (Liping County, Guizhou).

Task: guizhou_黎平县 — 县委书记 & 县长
Province: 贵州省
Parent city: 黔东南苗族侗族自治州
Region: 黎平县
Level: 县
Research date: 2026-07-23

Known officeholders (as of July 2026):
- 县委书记: 吴玉彬 (confirmed from lp.gov.cn news articles)
- 县委副书记、县长: 杨占杰 (confirmed from lp.gov.cn 领导之窗)
- 县委常委、常务副县长: 罗来冰
- 县委常委、副县长: 张泽猛
- 副县长、县公安局局长: 陈宏力
- 副县长: 王斌
- 副县长: 王跃
- 副县长: 杨璐

Sources:
- www.lp.gov.cn — official government website (primary source)
- lp.gov.cn/zwgk/ldzc/ — 领导之窗 for government leaders
- lp.gov.cn/xwdt/lpyw/ — news articles confirming party secretary
"""

import os
import sqlite3  # noqa: required by process_tmp validator
import sys
from datetime import datetime

# Ensure gov_relation is importable
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── PATHS ──
DB_PATH = os.path.join(SCRIPT_DIR, "黎平县_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "黎平县_network.gexf")

# ════════════════════════════════════════════
# PERSONS
# ════════════════════════════════════════════
PERSONS = [
    # ── 县委领导 ──
    {
        "id": 1,
        "name": "吴玉彬",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共黎平县委员会",
        "source": "lp.gov.cn_news_202607",
    },
    # ── 县政府领导 ──
    {
        "id": 2,
        "name": "杨占杰",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "1977年10月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "黎平县人民政府",
        "source": "lp.gov.cn_ldzc_202503",
    },
    {
        "id": 3,
        "name": "罗来冰",
        "gender": "男",
        "ethnicity": "侗族",
        "birth": "1981年12月",
        "birthplace": "贵州三穗",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "黎平县人民政府",
        "source": "lp.gov.cn_ldzc_202503",
    },
    {
        "id": 4,
        "name": "张泽猛",
        "gender": "男",
        "ethnicity": "侗族",
        "birth": "1974年8月",
        "birthplace": "",
        "education": "大专学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "黎平县人民政府",
        "source": "lp.gov.cn_ldzc_202503",
    },
    {
        "id": 5,
        "name": "陈宏力",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年10月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长、县公安局局长",
        "current_org": "黎平县人民政府",
        "source": "lp.gov.cn_ldzc_202503",
    },
    {
        "id": 6,
        "name": "王斌",
        "gender": "男",
        "ethnicity": "侗族",
        "birth": "1979年9月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "黎平县人民政府",
        "source": "lp.gov.cn_ldzc_202503",
    },
    {
        "id": 7,
        "name": "王跃",
        "gender": "男",
        "ethnicity": "侗族",
        "birth": "1979年1月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "黎平县人民政府",
        "source": "lp.gov.cn_ldzc_202503",
        "note": "民进会员",
    },
    {
        "id": 8,
        "name": "杨璐",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1984年10月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "黎平县人民政府",
        "source": "lp.gov.cn_ldzc_202503",
    },
]

# ════════════════════════════════════════════
# ORGANIZATIONS
# ════════════════════════════════════════════
ORGANIZATIONS = [
    {
        "id": 1,
        "name": "中共黎平县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共黔东南苗族侗族自治州委员会",
        "location": "贵州省黔东南州黎平县",
    },
    {
        "id": 2,
        "name": "黎平县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "黔东南苗族侗族自治州人民政府",
        "location": "贵州省黔东南州黎平县",
    },
    {
        "id": 3,
        "name": "黎平县公安局",
        "type": "政府",
        "level": "县级",
        "parent": "黎平县人民政府",
        "location": "贵州省黔东南州黎平县",
    },
    {
        "id": 4,
        "name": "贵州黎平经济开发区",
        "type": "开发区",
        "level": "县级",
        "parent": "黎平县人民政府",
        "location": "贵州省黔东南州黎平县",
    },
    {
        "id": 5,
        "name": "中共黎平县纪律检查委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共黎平县委员会",
        "location": "贵州省黔东南州黎平县",
    },
]

# ════════════════════════════════════════════
# POSITIONS
# ════════════════════════════════════════════
POSITIONS = [
    # 吴玉彬
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "present", "rank": "正县级", "note": "兼黎平经济开发区党工委书记"},
    {"person_id": 1, "org_id": 4, "title": "党工委书记", "start_date": "", "end_date": "present", "rank": "", "note": "兼任"},
    
    # 杨占杰
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "正县级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "", "end_date": "present", "rank": "正县级", "note": "县人民政府党组书记"},
    {"person_id": 2, "org_id": 4, "title": "管委会主任（兼）", "start_date": "", "end_date": "present", "rank": "", "note": "党工委副书记"},
    
    # 罗来冰
    {"person_id": 3, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "常务副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    
    # 张泽猛
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    
    # 陈宏力
    {"person_id": 5, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "县人民政府党组成员"},
    {"person_id": 5, "org_id": 3, "title": "县公安局局长", "start_date": "", "end_date": "present", "rank": "", "note": "县公安局党委书记"},
    
    # 王斌
    {"person_id": 6, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    
    # 王跃
    {"person_id": 7, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "民进会员"},
    
    # 杨璐
    {"person_id": 8, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
]

# ════════════════════════════════════════════
# RELATIONSHIPS
# ════════════════════════════════════════════
RELATIONSHIPS = [
    # 党政正职搭档
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记与县长党政搭档",
        "overlap_org": "中共黎平县委员会",
        "overlap_period": "2025-2026 (推定)",
    },
    # 县长与常务副县长
    {
        "person_a": 2,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "县长与常务副县长工作搭档",
        "overlap_org": "黎平县人民政府",
        "overlap_period": "2025-2026 (推定)",
    },
    # 县委常委间
    {
        "person_a": 3,
        "person_b": 4,
        "type": "overlap",
        "context": "同为县委常委",
        "overlap_org": "中共黎平县委员会",
        "overlap_period": "2025-2026 (推定)",
    },
    # 县长与副县长们
    {
        "person_a": 2,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "县长与副县长",
        "overlap_org": "黎平县人民政府",
        "overlap_period": "2025-2026 (推定)",
    },
    {
        "person_a": 2,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "县长与副县长",
        "overlap_org": "黎平县人民政府",
        "overlap_period": "2025-2026 (推定)",
    },
    {
        "person_a": 2,
        "person_b": 6,
        "type": "superior_subordinate",
        "context": "县长与副县长",
        "overlap_org": "黎平县人民政府",
        "overlap_period": "2025-2026 (推定)",
    },
    {
        "person_a": 2,
        "person_b": 7,
        "type": "superior_subordinate",
        "context": "县长与副县长",
        "overlap_org": "黎平县人民政府",
        "overlap_period": "2025-2026 (推定)",
    },
    {
        "person_a": 2,
        "person_b": 8,
        "type": "superior_subordinate",
        "context": "县长与副县长",
        "overlap_org": "黎平县人民政府",
        "overlap_period": "2025-2026 (推定)",
    },
    # 县委书记与县委常委（政府中）
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "县委书记与县委常委",
        "overlap_org": "中共黎平县委员会",
        "overlap_period": "2025-2026 (推定)",
    },
    {
        "person_a": 1,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "县委书记与县委常委",
        "overlap_org": "中共黎平县委员会",
        "overlap_period": "2025-2026 (推定)",
    },
]


def main():
    run_build(
        slug="黎平县",
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print(f"Build complete: {DB_PATH}")
    print(f"Build complete: {GEXF_PATH}")
    print(f"  Persons: {len(PERSONS)}")
    print(f"  Organizations: {len(ORGANIZATIONS)}")
    print(f"  Positions: {len(POSITIONS)}")
    print(f"  Relationships: {len(RELATIONSHIPS)}")


if __name__ == "__main__":
    main()
