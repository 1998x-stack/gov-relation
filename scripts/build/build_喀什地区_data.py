#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 喀什地区 leadership network.

喀什地区 = Kashgar Prefecture, Xinjiang Uyghur Autonomous Region.
This is a prefecture-level division (地级行政区), not to be confused with
喀什市 (Kashgar City), a county-level city within the prefecture.

The top party position is 喀什地区党委书记 (Prefecture Party Secretary),
and the top government position is 喀什地区行署专员 (Administrative Commissioner).

Targets: 地委书记 (Party Secretary) & 行署专员 (Commissioner)
"""

import sys
import os
import sqlite3
from pathlib import Path

# Ensure gov_relation is importable
# The script lives at data/tmp/xinjiang_喀什地区/build_xxx.py
# Repo root is 4 directories up from the script
_script_path = Path(__file__).resolve()
_gov_relation_marker = _script_path.parents[3]
REPO_ROOT = _gov_relation_marker
sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

STAGING_DIR = REPO_ROOT / "data/tmp/xinjiang_喀什地区"
DB_PATH = STAGING_DIR / "喀什地区_network.db"
GEXF_PATH = STAGING_DIR / "喀什地区_network.gexf"

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Top Leaders ──
    {
        "id": 1,
        "name": "聂壮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-03",
        "birthplace": "江西丰城",
        "education": "在职大学（新疆经济管理干部学院国际商务专业）",
        "party_join": "1996-06",
        "work_start": "1992-08",
        "current_post": "新疆维吾尔自治区人民政府副主席、喀什地委书记、兵团第三师党委第一书记、第一政委",
        "current_org": "中共喀什地区委员会",
        "source": "https://baike.baidu.com/item/%E8%81%82%E5%A3%AE",
    },
    {
        "id": 2,
        "name": "尼加提·尼亚孜",
        "gender": "男",
        "ethnicity": "维吾尔族",
        "birth": "1975-03",
        "birthplace": "新疆哈密",
        "education": "大学本科",
        "party_join": "中共党员",
        "work_start": "1998-08",
        "current_post": "喀什地委副书记、行署党组书记、专员",
        "current_org": "喀什地区行政公署",
        "source": "https://www.kashi.gov.cn/ksdqxzgs/c108131/202110/4a3122335b304a1ba90ebb0968aa83c2.shtml",
    },
    # ── Deputy Commissioners (行署副专员) ──
    {
        "id": 3,
        "name": "吴晓斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-04",
        "birthplace": "甘肃静宁",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "1992-09",
        "current_post": "喀什地委委员、行署党组副书记、常务副专员",
        "current_org": "喀什地区行政公署",
        "source": "https://www.kashi.gov.cn/ksdqxzgs/c108131/202308/a640decba63d4482834f4a55526c27f4.shtml",
    },
    {
        "id": 4,
        "name": "刘四宏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-01",
        "birthplace": "河南周口",
        "education": "",
        "party_join": "中共党员",
        "work_start": "1993-08",
        "current_post": "喀什地区行政公署党组成员、副专员",
        "current_org": "喀什地区行政公署",
        "source": "https://www.kashi.gov.cn/ksdqxzgs/c108131/202504/d748a1374205410cb023e49071cbda9e.shtml",
    },
    {
        "id": 5,
        "name": "祖力甫哈尔·阿布都热甫",
        "gender": "男",
        "ethnicity": "维吾尔族",
        "birth": "1973-01",
        "birthplace": "新疆伊宁",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "1995-07",
        "current_post": "喀什地区行政公署党组成员、副专员",
        "current_org": "喀什地区行政公署",
        "source": "https://www.kashi.gov.cn/ksdqxzxgs/c108131/202110/4abc5dc7564a4bfe9cc147a65801ffe5.shtml",
    },
    {
        "id": 6,
        "name": "马继明",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1979-10",
        "birthplace": "甘肃兰州",
        "education": "工学博士",
        "party_join": "中共党员",
        "work_start": "2005-07",
        "current_post": "喀什地区行政公署党组成员、副专员",
        "current_org": "喀什地区行政公署",
        "source": "https://www.kashi.gov.cn/ksdqxzxgs/c108131/202405/7b1a9a1f4df54ce0916f741298496365.shtml",
    },
    {
        "id": 7,
        "name": "扎帕尔·阿塔吾拉",
        "gender": "男",
        "ethnicity": "塔吉克族",
        "birth": "1972-11",
        "birthplace": "新疆塔什库尔干",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "1996-07",
        "current_post": "喀什地区行政公署党组成员、副专员",
        "current_org": "喀什地区行政公署",
        "source": "https://www.kashi.gov.cn/ksdqxzxgs/c108131/202506/f161dda710bf482c4bb1c65791a711b32.shtml",
    },
    # ── Predecessors ──
    {
        "id": 8,
        "name": "李宁平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "https://baike.baidu.com/item/%E5%96%80%E4%BB%80%E5%9C%B0%E5%8C%BA",
    },
    {
        "id": 9,
        "name": "帕尔哈提·肉孜",
        "gender": "男",
        "ethnicity": "维吾尔族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "https://baike.baidu.com/item/%E5%96%80%E4%BB%80%E5%9C%B0%E5%8C%BA",
    },
    # ── Cross-region / Additional ──
    {
        "id": 10,
        "name": "陈旭光",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "",
    },
]

organizations = [
    {"id": 1, "name": "中共喀什地区委员会（喀什地委）", "type": "党委", "level": "地厅级",
     "parent": "中共新疆维吾尔自治区委员会", "location": "新疆喀什"},
    {"id": 2, "name": "喀什地区行政公署", "type": "政府", "level": "地厅级",
     "parent": "新疆维吾尔自治区人民政府", "location": "新疆喀什"},
    {"id": 3, "name": "喀什地区纪委监委", "type": "纪委", "level": "地厅级",
     "parent": "中共新疆维吾尔自治区纪律检查委员会", "location": "新疆喀什"},
    {"id": 4, "name": "新疆维吾尔自治区人民政府", "type": "政府", "level": "副省级",
     "parent": "", "location": "新疆乌鲁木齐"},
    {"id": 5, "name": "新疆生产建设兵团第三师", "type": "兵团", "level": "地厅级",
     "parent": "新疆生产建设兵团", "location": "新疆图木舒克"},
    {"id": 6, "name": "博尔塔拉蒙古自治州党委", "type": "党委", "level": "地厅级",
     "parent": "中共新疆维吾尔自治区委员会", "location": "新疆博乐"},
    {"id": 7, "name": "阿拉山口市委", "type": "党委", "level": "县处级",
     "parent": "博尔塔拉蒙古自治州党委", "location": "新疆阿拉山口"},
    {"id": 8, "name": "新疆维吾尔自治区公安厅", "type": "政府", "level": "厅级",
     "parent": "新疆维吾尔自治区人民政府", "location": "新疆乌鲁木齐"},
    {"id": 9, "name": "博乐市委", "type": "党委", "level": "县处级",
     "parent": "博尔塔拉蒙古自治州党委", "location": "新疆博乐"},
]

positions = [
    # ── 聂壮 career (confirmed from Baidu Baike) ──
    {"person_id": 1, "org_id": 1, "title": "喀什地委书记",
     "start_date": "2022-06", "end_date": "", "rank": "地厅级正职",
     "note": "2025年2月起兼任自治区副主席"},
    {"person_id": 1, "org_id": 4, "title": "新疆维吾尔自治区人民政府副主席",
     "start_date": "2025-02", "end_date": "", "rank": "副省级",
     "note": ""},
    {"person_id": 1, "org_id": 5, "title": "兵团第三师党委第一书记、第一政委",
     "start_date": "2022-06", "end_date": "", "rank": "地厅级",
     "note": "兼任"},
    {"person_id": 1, "org_id": 8, "title": "新疆维吾尔自治区公安厅党委副书记、常务副厅长、政治部主任",
     "start_date": "2018-06", "end_date": "2022-06", "rank": "厅级",
     "note": ""},
    {"person_id": 1, "org_id": 9, "title": "博尔塔拉蒙古zu自l治州党委常委、博乐市委书记",
     "start_date": "2016-08", "end_date": "2018-06", "rank": "地厅级副职",
     "note": ""},
    {"person_id": 1, "org_id": 6, "title": "博尔塔拉蒙古自治州党委常委，副州长、政府党组成员",
     "start_date": "2016-07", "end_date": "2016-08", "rank": "地厅级副职",
     "note": ""},
    {"person_id": 1, "org_id": 6, "title": "博尔塔拉蒙古自治州人民政府党组成员、副州长人选",
     "start_date": "2016-06", "end_date": "2016-07", "rank": "地厅级副职",
     "note": ""},
    {"person_id": 1, "org_id": 7, "title": "阿拉山口市委书记、阿拉山口综合保税区管委会主任",
     "start_date": "2013-06", "end_date": "2016-06", "rank": "县处级正职",
     "note": ""},
    {"person_id": 1, "org_id": 6, "title": "温泉县委书记",
     "start_date": "2011-07", "end_date": "2013-06", "rank": "县处级正职",
     "note": ""},
    {"person_id": 1, "org_id": 6, "title": "温泉县委常委、副县长（正县级）",
     "start_date": "2007-10", "end_date": "2011-07", "rank": "县处级正职",
     "note": ""},
    {"person_id": 1, "org_id": 6, "title": "挂职任温泉县党委常委、副县长",
     "start_date": "2005-12", "end_date": "2007-10", "rank": "县处级副职",
     "note": ""},

    # ── 尼加提·尼亚孜 (limited bio) ──
    {"person_id": 2, "org_id": 1, "title": "喀什地委副书记",
     "start_date": "", "end_date": "", "rank": "地厅级副职",
     "note": "现任"},
    {"person_id": 2, "org_id": 2, "title": "喀什地区行政公署党组书记、专员",
     "start_date": "", "end_date": "", "rank": "地厅级",
     "note": "现任, 全面履历缺失"},

    # ── 吴晓斌 ──
    {"person_id": 3, "org_id": 1, "title": "喀什地委委员",
     "start_date": "", "end_date": "", "rank": "地厅级副职",
     "note": ""},
    {"person_id": 3, "org_id": 2, "title": "行署党组副书记、常务副专员",
     "start_date": "", "end_date": "", "rank": "地厅级副职",
     "note": "现任"},

    # ── 刘四宏 ──
    {"person_id": 4, "org_id": 2, "title": "喀什行署党组成员、副专员",
     "start_date": "", "end_date": "", "rank": "地厅级副职",
     "note": "现任"},

    # ── 祖力甫哈尔·阿布都热甫 ──
    {"person_id": 5, "org_id": 2, "title": "喀什行署党组成员、副专员",
     "start_date": "", "end_date": "", "rank": "地厅级副职",
     "note": "现任"},

    # ── 马继明 ──
    {"person_id": 6, "org_id": 2, "title": "喀什行署党组成员、副专员",
     "start_date": "", "end_date": "", "rank": "地厅级副职",
     "note": "现任"},

    # ── 扎甫哈尔·阿塔吾拉 ──
    {"person_id": 7, "org_id": 2, "title": "喀什行署党组成员、副专员",
     "start_date": "", "end_date": "", "rank": "地厅级副职",
     "note": "现任"},

    # ── Predecessor positions ──
    {"person_id": 8, "org_id": 1, "title": "喀什地委书记",
     "start_date": "", "end_date": "2022-06", "rank": "地厅级正职",
     "note": "前任, 聂壮接任"},
    {"person_id": 9, "org_id": 2, "title": "喀什地区行署专员",
     "start_date": "", "end_date": "", "rank": "地厅级",
     "note": "前任专员"},
]

relationships = [
    # ── Predecessor-Successor ──
    {"person_a": 8, "person_b": 1, "type": "交接",
     "context": "李宁平→聂壮 喀什地委书记交接（2022年6月）",
     "overlap_org": "中共喀什地区委员会", "overlap_period": "2022-06"},
    {"person_a": 2, "person_b": 9, "type": "交接",
     "context": "尼加提·尼亚孜接任行署专员，前任为帕尔哈提·肉孜",
     "overlap_org": "喀什地区行政公署", "overlap_period": ""},

    # ── Party-Government Working Pair ──
    {"person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "聂壮（地委书记）+ 尼加提·尼亚孜（行署专员）党政搭档",
     "overlap_org": "中共喀什地区委员会", "overlap_period": "2021-"},

    # ── 聂壮's network connections ──
    {"person_a": 1, "person_b": 8, "type": "前任继任",
     "context": "聂雵接替李宁平任喀什地委书记",
     "overlap_org": "中共喀什地区委员会", "overlap_period": "2022-06"},
]

# ── BUILD ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"\nBuilding 喀什地区 leadership network...")
    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")

    # Create staging dir
    os.makedirs(str(STAGING_DIR), exist_ok=True)

    run_build(
        slug="喀什地区",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=str(DB_PATH),
        gexf_path=str(GEXF_PATH),
        overwrite=True,
    )

    print("\n✅ Build complete!")
    print(f"   Persons:       {len(persons)}")
    print(f"   Organizations: {len(organizations)}")
    print(f"   Positions:     {len(positions)}")
    print(f"   Relationships: {len(relationships)}")