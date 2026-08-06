#!/usr/bin/env python3
"""Build script for 沈阳市大东区 government personnel network.

Confirmed core leadership (2026-07, degraded-web research):
  - 区委书记  王铁兵   (2026-05 任, 2026-07-30 当选)
  - 区长      魏鹏     (2022-至今)
  - 区委副书记/统战部长  庞挺
  - 副区长    陈兆春(常务)、曲飞、苏国峰、王跃
  - 原区委书记 王林祥
"""

import sqlite3
import sys
from datetime import datetime
from pathlib import Path

_here = Path(__file__).resolve()
_root_candidate = _here
while _root_candidate != _root_candidate.parent:
    if (_root_candidate / "gov_relation").is_dir():
        sys.path.insert(0, str(_root_candidate))
        break
    _root_candidate = _root_candidate.parent

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "大东区"
STAGING = Path("data/tmp/liaoning_大东区")

# Tokens required by process_tmp validation
DB_PATH = STAGING / "大东区_network.db"
GEXF_PATH = STAGING / "大东区_network.gexf"


# ── Persons ──────────────────────────────────────────────────────────────
persons = [
    # ── Party Secretary (区委书记) ──
    {
        "id": 1,
        "name": "王铁兵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-04",
        "birthplace": "待查",
        "education": "大学学历，硕士学位（沈阳师范大学毕业），中学一级教师",
        "party_join": "1998-12",
        "work_start": "1996-08",
        "current_post": "区委书记、区人武部党委第一书记",
        "current_org": "中共沈阳市大东区委员会",
        "source": "百度百科/东北新闻网/北斗融媒/浑南区人民政府（2026-07-30 当选）",
    },
    # ── District Mayor (区长) ──
    {
        "id": 2,
        "name": "魏鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-08",
        "birthplace": "待查",
        "education": "研究生学历，博士学位",
        "party_join": "2007-11",
        "work_start": "2009-07",
        "current_post": "区委副书记、区长，沈阳-欧盟经济开发区（沈阳汽车城开发建设）党工委副书记、管委会主任（兼）",
        "current_org": "大东区人民政府",
        "source": "沈阳市大东区人民政府官网（2026-07-27）/百度百科",
    },
    # ── Deputy Party Secretary / 统战部长 ──
    {
        "id": 3,
        "name": "庞挺",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1975-05",
        "birthplace": "待查",
        "education": "在职研究生学历，博士学位，副研究员",
        "party_join": "2000-12",
        "work_start": "1997-08",
        "current_post": "区委副书记、统战部部长",
        "current_org": "中共沈阳市大东区委员会",
        "source": "百度百科/沈阳市任前公示",
    },
    # ── Executive Deputy Mayor (区委常委、常务副区长) ──
    {
        "id": 4,
        "name": "陈兆春",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-02",
        "birthplace": "待查",
        "education": "研究生学历，硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委，区政府党组副书记、副区长（负责区政府常务工作）",
        "current_org": "大东区人民政府",
        "source": "沈阳市大东区人民政府官网/百度百科",
    },
    # ── Deputy Mayor (副区长/公安局长) ──
    {
        "id": 5,
        "name": "王跃",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-09",
        "birthplace": "待查",
        "education": "研究生学历，硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长，市公安局大东分局党组副书记、局长、督察长、一级高级警长",
        "current_org": "大东区人民政府/沈阳市公安局大东分局",
        "source": "沈阳市大东区人民政府官网（2026-04）",
    },
    # ── Deputy Mayor (副区长) ──
    {
        "id": 6,
        "name": "苏国峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986-06",
        "birthplace": "待查",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政府副区长、党组成员",
        "current_org": "大东区人民政府",
        "source": "沈阳市大东区人民政府官网（2025-08）/百度百科",
    },
    # ── Deputy Mayor (副区长) ──
    {
        "id": 7,
        "name": "曲飞",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1976-03",
        "birthplace": "山东黄县人",
        "education": "研究生学历（锦州师范学院中文系毕业）",
        "party_join": "1998-06",
        "work_start": "1998-08",
        "current_post": "区政府副区长、党组成员",
        "current_org": "大东区人民政府",
        "source": "沈阳市大东区人民政府官网/百度百科",
    },
    # ── Predecessor Party Secretary (原区委书记) ──
    {
        "id": 8,
        "name": "王林祥",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-09",
        "birthplace": "待查",
        "education": "大学学历，学士学位，高级工程师",
        "party_join": "2000-06",
        "work_start": "1992-08",
        "current_post": "原区委书记（已卸任）",
        "current_org": "",
        "source": "百度百科(辽宁省沈阳市大东区委原书记)",
    },
]


# ── Organizations ────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共沈阳市大东区委员会", "type": "党委", "level": "市辖区", "parent": "中共沈阳市委", "location": "沈阳市大东区"},
    {"id": 2, "name": "大东区人民政府", "type": "政府", "level": "市辖区", "parent": "沈阳市人民政府", "location": "沈阳市大东区"},
    {"id": 3, "name": "沈阳-欧盟经济开发区管委会（沈阳汽车城开发建设）", "type": "开发区", "level": "省级经开区", "parent": "大东区人民政府", "location": "沈阳市大东区"},
    {"id": 4, "name": "沈阳市公安局大东分局", "type": "政法", "level": "部门", "parent": "沈阳市委公安", "location": "沈阳市大东区"},
    {"id": 5, "name": "大东区人大常委会", "type": "人大", "level": "市辖区", "parent": "", "location": "沈阳市大东区"},
    {"id": 6, "name": "政协大东区委员会", "type": "政协", "level": "市辖区", "parent": "", "location": "沈阳市大东区"},
    # external (career-host) orgs
    {"id": 7, "name": "中共沈阳市浑南区委员会", "type": "党委", "level": "市辖区", "parent": "中共沈阳市委", "location": "沈阳市浑南区"},
    {"id": 8, "name": "浑南区人民政府", "type": "政府", "level": "市辖区", "parent": "沈阳市人民政府", "location": "沈阳市浑南区"},
    {"id": 9, "name": "沈阳燃气集团有限公司", "type": "事业单位", "level": "市属国企", "parent": "沈阳市人民政府", "location": "沈阳市"},
    {"id": 10, "name": "沈阳经济技术开发区管委会", "type": "开发区", "level": "国家级经开区", "parent": "沈阳市人民政府", "location": "沈阳市"},
]


# ── Positions ────────────────────────────────────────────────────────────
positions = [
    # 王铁兵
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "2026-05", "end_date": "至今", "rank": "副厅级", "note": "2026年7月30日在大东区第十四届党委一次全会当选；兼任大东区人武部党委第一书记"},
    {"person_id": 1, "org_id": 8, "title": "副区长", "start_date": "2020-05", "end_date": "", "rank": "", "note": "沈阳浑南区副区长"},
    {"person_id": 1, "org_id": 7, "title": "区委常委、区委办公室主任", "start_date": "", "end_date": "", "rank": "", "note": "曾任沈阳浑南区委常委、区委办主任"},
    {"person_id": 1, "org_id": 9, "title": "党委书记、董事长", "start_date": "", "end_date": "", "rank": "", "note": "曾任沈阳燃气集团党委书记、董事长"},
    # 魏鹏
    {"person_id": 2, "org_id": 2, "title": "区委副书记、区长", "start_date": "2022", "end_date": "至今", "rank": "副厅级", "note": "2024年3月14日曾拟任副省级城市县（市、区）委书记（任前公示）"},
    {"person_id": 2, "org_id": 3, "title": "管委会主任（兼）", "start_date": "", "end_date": "至今", "rank": "", "note": "沈阳-欧盟经济开发区管委会主任"},
    # 庞挺
    {"person_id": 3, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "至今", "rank": "副厅级", "note": "2026年4月拟任市政府直属事业单位正职"},
    {"person_id": 3, "org_id": 1, "title": "统战部部长", "start_date": "", "end_date": "至今", "rank": "", "note": "专职区委统战部长"},
    # 陈兆春
    {"person_id": 4, "org_id": 2, "title": "区委常委、常务副区长", "start_date": "2022", "end_date": "至今", "rank": "副厅级", "note": "负责区政府常务工作"},
    # 王跃
    {"person_id": 5, "org_id": 2, "title": "副区长（公安）", "start_date": "", "end_date": "至今", "rank": "副厅级", "note": "分管公安司法信访"},
    {"person_id": 5, "org_id": 4, "title": "区公安分局局长", "start_date": "", "end_date": "至今", "rank": "", "note": ""},
    # 苏国峰
    {"person_id": 6, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "至今", "rank": "正处级", "note": "分管市场监管、房屋征收、自然资源等"},
    # 曲飞
    {"person_id": 7, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "至今", "rank": "正处级", "note": ""},
    # 王林祥
    {"person_id": 8, "org_id": 1, "title": "区委书记", "start_date": "", "end_date": "", "rank": "副厅级", "note": "原区委书记，已卸任（2026年初离职）"},
    {"person_id": 8, "org_id": 10, "title": "沈阳经开区管委会副主任", "start_date": "2016", "end_date": "2019", "rank": "", "note": "兼中德沈阳高端装备产业园管委会副主任"},
]


# ── Relationships ────────────────────────────────────────────────────────
relationships = [
    # 王铁兵→魏鹏: 党政一把手
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "王铁兵任区委书记，魏鹏任区长，2026年搭班区委区政府", "overlap_org": "中共沈阳市大东区委/大东区人民政府", "overlap_period": "2026-至今"},
    # 王铁兵→庞挺: 班子
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "庞挺为区委副书记、统战部长，配合王铁兵工作", "overlap_org": "中共沈阳市大东区委员会", "overlap_period": "2026-至今"},
    # 魏鹏→陈兆春: 常务
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "陈兆春为常务副区长，协助魏鹏主持区政府常务工作", "overlap_org": "大东区人民政府", "overlap_period": "至今"},
    # 区委→政府副职
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "陈兆春为区委常委、常务副区长", "overlap_org": "大东区人民政府", "overlap_period": "至今"},
    # 区长→副区长
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "王跃为副区长兼公安局长，协助魏鹏工作", "overlap_org": "大东区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "苏国峰为副区长，协助魏鹏工作", "overlap_org": "大东区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "曲飞为副区长，协助魏鹏工作", "overlap_org": "大东区人民政府", "overlap_period": "至今"},
    # 前任→后任书记
    {"person_a": 1, "person_b": 8, "type": "前任-后任", "context": "王铁兵接替王林祥担任大东区委书记", "overlap_org": "中共沈阳市大东区委员会", "overlap_period": "2026交接"},
]


# ── Main ─────────────────────────────────────────────────────────────────
def main():
    db_path = STAGING / "大东区_network.db"
    gexf_path = STAGING / "大东区_network.gexf"

    print(f"==> Building: {SLUG}")
    print(f"    Persons: {len(persons)}")
    print(f"    Orgs:    {len(organizations)}")
    print(f"    Pos:     {len(positions)}")
    print(f"    Rel:     {len(relationships)}")

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

    # Verify
    conn = sqlite3.connect(str(DB_PATH))
    for table in ("persons", "organizations", "positions", "relationships"):
        count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"    DB {table}: {count} rows")
    conn.close()
    print(f"    GEXF: {GEXF_PATH.exists()}")
    print(f"    DB:   {DB_PATH.exists()}")
    print(f"==> Done: {SLUG}")


if __name__ == "__main__":
    main()