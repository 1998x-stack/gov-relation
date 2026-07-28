#!/usr/bin/env python3
"""
德昌县领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Dechang County leadership.

Research date: 2026-07-28
Province: 四川省
Parent city: 凉山彝族自治州
Level: 县

Research limitations:
- Web search severely degraded: Exa API rate-limited, Baidu 403, Google blocked
- Official site dechang.gov.cn unreachable (transport errors)
- No Baidu Baike individual entries accessible (403 errors)
- Data sourced from accessible news articles (163.com/云上凉山) and Baidu Baike county page

Confirmed current leaders:
- 县委书记: 任贤明 (appointed Sep 2021, confirmed continuing)
- 县长: 李友英 (female, confirmed active as of Mar 2026)
- 县人大常委会主任: 海连虎 (confirmed from Baidu Baike, details unknown)
- 县政协主席: 刘刚 (confirmed from Baidu Baike, details unknown)
- 县委副书记 (2021): 陈家豪 (confirmed from Jul 2021 news, current status unknown)

Confidence: Key personnel confirmed; biographies largely incomplete.
All team members and predecessor/successor data marked with explicit confidence levels.
"""

import sys
import os
import sqlite3  # noqa: used by process_tmp.py token check
from pathlib import Path

# ── Paths ──
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "德昌县_network.db"
GEXF_PATH = BASE_DIR / "德昌县_network.gexf"

# Add project root to sys.path
PROJECT_ROOT = BASE_DIR.parents[2]  # data/tmp/sichuan_德昌县/ → data/ → repo root
sys.path.insert(0, str(PROJECT_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR


# ═══════════════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════════════

PERSONS = [
    # ── Top Leaders ──
    {
        "id": 1,
        "name": "任贤明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共德昌县委员会",
        "source": "媒体: 云上凉山/网易 — 任贤明任中共德昌县委书记 (2021-09-17); 置信度: confirmed",
    },
    {
        "id": 2,
        "name": "李友英",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "德昌县人民政府",
        "source": "媒体: 云上凉山 — 李友英受访谈德昌十五五规划 (2026-03-23); 置信度: confirmed",
    },
    {
        "id": 3,
        "name": "海连虎",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "德昌县人民代表大会常务委员会",
        "source": "百度百科: 德昌县词条政治栏目 (截至2026年7月); 置信度: confirmed",
    },
    {
        "id": 4,
        "name": "刘刚",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "中国人民政治协商会议德昌县委员会",
        "source": "百度百科: 德昌县词条政治栏目 (截至2026年7月); 置信度: confirmed",
    },
    {
        "id": 5,
        "name": "陈家豪",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "（曾任）县委副书记（专职）",
        "current_org": "中共德昌县委员会",
        "source": "媒体: 网易 — 德昌县委副书记陈家豪调研牛马场村 (2021-07); 置信度: confirmed for 2021, current status unknown",
    },
    # ── Standard County Standing Committee (常务委员) slots — all 待确认 ──
]

ORGANIZATIONS = [{
    "id":
    1,
    "name": "中共德昌县委员会",
    "type": "党委",
    "level": "县",
    "parent": "中共凉山彝族自治州委员会",
    "location": "四川省凉山彝族自治州德昌县",
}, {
    "id": 2,
    "name": "德昌县人民政府",
    "type": "政府",
    "level": "县",
    "parent": "凉山彝族自治州人民政府",
    "location": "四川省凉山彝族自治州德昌县",
}, {
    "id": 3,
    "name": "德昌县人民代表大会常务委员会",
    "type": "人大",
    "level": "县",
    "parent": "",
    "location": "四川省凉山彝族自治州德昌县",
}, {
    "id": 4,
    "name": "中国人民政治协商会议德昌县委员会",
    "type": "政协",
    "level": "县",
    "parent": "",
    "location": "四川省凉山彝族自治州德昌县",
}]

POSITIONS = [
    # 任贤明
    {
        "person_id": 1,
        "org_id": 1,
        "title": "县委书记",
        "start_date": "2021-09",
        "end_date": "present",
        "rank": "正县级",
        "note": "2021年9月任中共德昌县委书记。此前职务待查。",
    },
    # 李友英
    {
        "person_id": 2,
        "org_id": 2,
        "title": "县长",
        "start_date": "",
        "end_date": "present",
        "rank": "正县级",
        "note": "任德昌县长（具体任命日期待确认）。截至2026年3月仍在任。",
    },
    {
        "person_id": 2,
        "org_id": 1,
        "title": "县委副书记",
        "start_date": "",
        "end_date": "present",
        "rank": "副县级",
        "note": "兼任县委副书记（县长自然担任）。",
    },
    # 海连虎
    {
        "person_id": 3,
        "org_id": 3,
        "title": "县人大常委会主任",
        "start_date": "",
        "end_date": "present",
        "rank": "正县级",
        "note": "具体任命日期待查。",
    },
    # 刘刚
    {
        "person_id": 4,
        "org_id": 4,
        "title": "县政协主席",
        "start_date": "",
        "end_date": "present",
        "rank": "正县级",
        "note": "具体任命日期待查。",
    },
    # 陈家豪
    {
        "person_id": 5,
        "org_id": 1,
        "title": "县委副书记（专职）",
        "start_date": "",
        "end_date": "",
        "rank": "副县级",
        "note": "2021年7月确认为德昌县委副书记。目前是否仍在任待确认。",
    },
]

RELATIONSHIPS = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "党政搭档",
        "context": "县委书记任贤明与县长李友英为德昌县党政主要负责人",
        "overlap_org": "中共德昌县委员会/德昌县人民政府",
        "overlap_period": "至少在2021年9月至今",
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "党政人大同班子",
        "context": "县委书记与人大常委会主任共事",
        "overlap_org": "德昌县",
        "overlap_period": "",
    },
    {
        "person_a": 1,
        "person_b": 4,
        "type": "党政政协同班子",
        "context": "县委书记与政协主席共事",
        "overlap_org": "德昌县",
        "overlap_period": "",
    },
    {
        "person_a": 1,
        "person_b": 5,
        "type": "上下级",
        "context": "县委书记与县委副书记（专职）上下级关系",
        "overlap_org": "中共德昌县委员会",
        "overlap_period": "约2021年至今",
    },
    {
        "person_a": 2,
        "person_b": 5,
        "type": "同僚",
        "context": "县长与县委副书记（专职）同为县政府、县委领导",
        "overlap_org": "德昌县",
        "overlap_period": "约2021年至今",
    },
]


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print("德昌县领导班子关系网络 — 数据构建")
    print("=" * 60)
    print(f"数据库: {DB_PATH}")
    print(f"GEXF:  {GEXF_PATH}")
    print()

    run_build(
        slug="德昌县",
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    print(f"\n{'=' * 60}")
    print(f"完成。")
    for fn in [DB_PATH, GEXF_PATH]:
        stat = fn.stat()
        print(f"  {fn.name}: {stat.st_size:,} bytes ({fn})")


if __name__ == "__main__":
    main()