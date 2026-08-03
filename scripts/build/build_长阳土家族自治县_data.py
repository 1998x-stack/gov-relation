#!/usr/bin/env python3
"""Build script for 长阳土家族自治县 (Changyang Tujia Autonomous County, Yichang, Hubei).

Sources:
- Official government website: www.changyang.gov.cn (news articles July 2026)
- 长阳土家族自治县人民政府 news archive (content-5084-*)
"""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

_STAGING_DIR = Path(__file__).resolve().parent
# data/tmp/hubei_长阳土家族自治县/ -> data/ -> repo root
_REPO_ROOT = (_STAGING_DIR / ".." / ".." / "..").resolve()
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "长阳土家族自治县"
PROVINCE = "湖北省"
CITY = "宜昌市"
DATE = "2026-08-03"

DB_PATH = DATABASE_DIR / f"{SLUG}_network.db"
GEXF_PATH = GRAPH_DIR / f"{SLUG}_network.gexf"

# ── Persons ──────────────────────────────────────────────────────────

persons = [
    {
        "id": 1,
        "name": "郑书香",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共长阳土家族自治县委书记",
        "current_org": "中共长阳土家族自治县委员会",
        "source": "http://www.changyang.gov.cn/content-5084-542391-1.html",
    },
    {
        "id": 2,
        "name": "张学书",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "长阳土家族自治县委副书记、县长",
        "current_org": "长阳土家族自治县人民政府",
        "source": "http://www.changyang.gov.cn/content-5084-542272-1.html",
    },
    {
        "id": 3,
        "name": "余红",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共长阳土家族自治县委员会",
        "source": "http://www.changyang.gov.cn/content-5084-542232-1.html",
    },
    {
        "id": 4,
        "name": "覃宏明",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "长阳土家族自治县人大常委会",
        "source": "http://www.changyang.gov.cn/content-5084-542344-1.html",
    },
    {
        "id": 5,
        "name": "覃高轩",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "政协长阳土家族自治县委员会",
        "source": "http://www.changyang.gov.cn/content-5084-542292-1.html",
    },
    {
        "id": 6,
        "name": "周近群",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共长阳土家族自治县委员会",
        "source": "http://www.changyang.gov.cn/content-5084-542335-1.html",
    },
    {
        "id": 7,
        "name": "王梁",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "长阳土家族自治县人民政府",
        "source": "http://www.changyang.gov.cn/content-5084-542265-1.html",
    },
    {
        "id": 8,
        "name": "程刚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "长阳土家族自治县人民政府",
        "source": "http://www.changyang.gov.cn/content-5084-542301-1.html",
    },
    {
        "id": 9,
        "name": "章玉莲",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "长阳土家族自治县",
        "source": "http://www.changyang.gov.cn/content-5084-542335-1.html",
    },
    {
        "id": 10,
        "name": "李钦",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "长阳土家族自治县",
        "source": "http://www.changyang.gov.cn/content-5084-542232-1.html",
    },
    {
        "id": 11,
        "name": "夏云辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "长阳土家族自治县",
        "source": "http://www.changyang.gov.cn/content-5084-542335-1.html",
    },
    {
        "id": 12,
        "name": "魏海",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "长阳土家族自治县人民政府",
        "source": "http://www.changyang.gov.cn/content-5084-542292-1.html",
    },
    {
        "id": 13,
        "name": "李杨",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "长阳土家族自治县",
        "source": "http://www.changyang.gov.cn/content-5084-542232-1.html",
    },
    {
        "id": 14,
        "name": "林刚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "长阳土家族自治县",
        "source": "http://www.changyang.gov.cn/content-5084-542232-1.html",
    },
    {
        "id": 15,
        "name": "冯胜多",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "长阳土家族自治县",
        "source": "http://www.changyang.gov.cn/content-5084-542232-1.html",
    },
    {
        "id": 16,
        "name": "胡永庆",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "长阳土家族自治县",
        "source": "http://www.changyang.gov.cn/content-5084-542232-1.html",
    },
    {
        "id": 17,
        "name": "万丹",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "长阳土家族自治县",
        "source": "http://www.changyang.gov.cn/content-5084-542290-1.html",
    },
    {
        "id": 18,
        "name": "饶会群",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "长阳土家族自治县",
        "source": "http://www.changyang.gov.cn/content-5084-542290-1.html",
    },
    {
        "id": 19,
        "name": "李德兵",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "长阳土家族自治县",
        "source": "http://www.changyang.gov.cn/content-5084-542202-1.html",
    },
    {
        "id": 20,
        "name": "朱晓亮",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "长阳土家族自治县",
        "source": "http://www.changyang.gov.cn/content-5084-542202-1.html",
    },
]

# ── Organizations ────────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "中共长阳土家族自治县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共宜昌市委员会",
        "location": "长阳土家族自治县",
    },
    {
        "id": 2,
        "name": "长阳土家族自治县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "宜昌市人民政府",
        "location": "长阳土家族自治县",
    },
    {
        "id": 3,
        "name": "长阳土家族自治县人大常委会",
        "type": "人大",
        "level": "县级",
        "parent": "宜昌市人大常委会",
        "location": "长阳土家族自治县",
    },
    {
        "id": 4,
        "name": "政协长阳土家族自治县委员会",
        "type": "政协",
        "level": "县级",
        "parent": "政协宜昌市委员会",
        "location": "长阳土家族自治县",
    },
]

# ── Positions ────────────────────────────────────────────────────────

positions = [
    # 郑书香
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "confirmed as of July 2026"},
    # 张学书
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "confirmed as of July 2026"},
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "confirmed as of July 2026"},
    # 余红
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "confirmed as of July 2026"},
    # 覃宏明
    {"person_id": 4, "org_id": 3, "title": "县人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": "confirmed as of July 2026"},
    # 覃高轩
    {"person_id": 5, "org_id": 4, "title": "县政协主席", "start_date": "", "end_date": "present", "rank": "正处级", "note": "confirmed as of July 2026"},
    # 周近群
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "confirmed as of July 2026"},
    # 王梁
    {"person_id": 7, "org_id": 2, "title": "县领导", "start_date": "", "end_date": "present", "rank": "副处级", "note": "confirmed as of July 2026"},
    # 程刚
    {"person_id": 8, "org_id": 2, "title": "县领导", "start_date": "", "end_date": "present", "rank": "副处级", "note": "confirmed as of July 2026"},
    # 章玉莲
    {"person_id": 9, "org_id": 2, "title": "县领导", "start_date": "", "end_date": "present", "rank": "副处级", "note": "confirmed as of July 2026"},
    # 李钦
    {"person_id": 10, "org_id": 2, "title": "县领导", "start_date": "", "end_date": "present", "rank": "副处级", "note": "confirmed as of July 2026"},
    # 夏云辉
    {"person_id": 11, "org_id": 2, "title": "县领导", "start_date": "", "end_date": "present", "rank": "副处级", "note": "confirmed as of July 2026"},
    # 魏海
    {"person_id": 12, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "confirmed as of July 2026"},
    # 李杨
    {"person_id": 13, "org_id": 2, "title": "县领导", "start_date": "", "end_date": "present", "rank": "副处级", "note": "confirmed as of July 2026"},
    # 林刚
    {"person_id": 14, "org_id": 2, "title": "县领导", "start_date": "", "end_date": "present", "rank": "副处级", "note": "confirmed as of July 2026"},
    # 冯胜多
    {"person_id": 15, "org_id": 2, "title": "县领导", "start_date": "", "end_date": "present", "rank": "副处级", "note": "confirmed as of July 2026"},
    # 胡永庆
    {"person_id": 16, "org_id": 2, "title": "县领导", "start_date": "", "end_date": "present", "rank": "副处级", "note": "confirmed as of July 2026"},
    # 万丹
    {"person_id": 17, "org_id": 2, "title": "县领导", "start_date": "", "end_date": "present", "rank": "副处级", "note": "confirmed as of July 2026"},
    # 饶会群
    {"person_id": 18, "org_id": 2, "title": "县领导", "start_date": "", "end_date": "present", "rank": "副处级", "note": "confirmed as of July 2026"},
    # 李德兵
    {"person_id": 19, "org_id": 2, "title": "县领导", "start_date": "", "end_date": "present", "rank": "副处级", "note": "confirmed as of July 2026"},
    # 朱晓亮
    {"person_id": 20, "org_id": 2, "title": "县领导", "start_date": "", "end_date": "present", "rank": "副处级", "note": "confirmed as of July 2026"},
]

# ── Relationships ────────────────────────────────────────────────────

relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "colleague",
        "context": "县委书记与县长搭班子（2026年7月）",
        "overlap_org": "长阳土家族自治县",
        "overlap_period": "2026-",
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "colleague",
        "context": "县委书记与县委副书记搭班子",
        "overlap_org": "中共长阳土家族自治县委员会",
        "overlap_period": "2026-",
    },
    {
        "person_a": 1,
        "person_b": 4,
        "type": "colleague",
        "context": "县委书记与人大主任同县班子",
        "overlap_org": "长阳土家族自治县",
        "overlap_period": "2026-",
    },
    {
        "person_a": 1,
        "person_b": 5,
        "type": "colleague",
        "context": "县委书记与政协主席同县班子",
        "overlap_org": "长阳土家族自治县",
        "overlap_period": "2026-",
    },
    {
        "person_a": 1,
        "person_b": 6,
        "type": "colleague",
        "context": "县委书记与县委常委同县班子",
        "overlap_org": "中共长阳土家族自治县委员会",
        "overlap_period": "2026-",
    },
    {
        "person_a": 2,
        "person_b": 12,
        "type": "colleague",
        "context": "县长与副县长",
        "overlap_org": "长阳土家族自治县人民政府",
        "overlap_period": "2026-",
    },
]

# ── Main ─────────────────────────────────────────────────────────────

def main():
    db_path = DB_PATH
    gexf_path = GEXF_PATH

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=db_path,
        gexf_path=gexf_path,
        overwrite=True,
    )

    print(f"Done. {len(persons)} persons, {len(organizations)} orgs, "
          f"{len(positions)} positions, {len(relationships)} relationships.")

if __name__ == "__main__":
    main()