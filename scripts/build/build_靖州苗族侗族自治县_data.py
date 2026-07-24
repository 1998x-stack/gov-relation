#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 靖州苗族侗族自治县 (Jingzhou Miao and Dong Autonomous County) leadership network."""

import sqlite3
import os
import sys
from pathlib import Path

# Add repo root to sys.path so gov_relation can be imported
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GOV_RELATION_DIR = os.path.join(BASE, "gov_relation")
if GOV_RELATION_DIR not in sys.path:
    sys.path.insert(0, GOV_RELATION_DIR)
if BASE not in sys.path:
    sys.path.insert(0, BASE)

from gov_relation.runner import run_build

SLUG = "靖州苗族侗族自治县"
STAGING_DIR = Path(__file__).resolve().parent
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"

# ── PERSONS ────────────────────────────────────────────────────────────
persons = [
    # ── Core leadership (县级领导) ──
    {"id": 1, "name": "张艳阳", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "靖州苗族侗族自治县委书记", "current_org": "中共靖州苗族侗族自治县委员会",
     "source": "https://www.jzx.gov.cn/jzx/c122051/xzf2020.shtml"},

    {"id": 2, "name": "滕海涛", "gender": "男", "ethnicity": "苗族",
     "birth": "1978-08", "birthplace": "", "education": "大学",
     "party_join": "", "work_start": "",
     "current_post": "靖州苗族侗族自治县委副书记、代理县长", "current_org": "靖州苗族侗族自治县人民政府",
     "source": "https://www.jzx.gov.cn/jzx/c122051/xzf2020.shtml"},

    # ── 四大班子正职 ──
    {"id": 3, "name": "杨景明", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "靖州苗族侗族自治县人大常委会主任", "current_org": "靖州苗族侗族自治县人大常委会",
     "source": "https://www.jzx.gov.cn/jzx/c116354/202607/612e29692f0449f183d38e0787727a8a.shtml"},

    {"id": 4, "name": "姜小华", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "靖州苗族侗族自治县政协主席", "current_org": "靖州苗族侗族自治县政协",
     "source": "https://www.jzx.gov.cn/jzx/c116354/202607/612e29692f0449f183d38e0787727a8a.shtml"},

    # ── 县委常委 ──
    {"id": 5, "name": "田锋", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "靖州苗族侗族自治县委常委", "current_org": "中共靖州苗族侗族自治县委员会",
     "source": "https://www.jzx.gov.cn/jzx/c116354/202607/612e29692f0449f183d38e0787727a8a.shtml"},

    {"id": 6, "name": "张长江", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "靖州苗族侗族自治县委常委", "current_org": "中共靖州苗族侗族自治县委员会",
     "source": "https://www.jzx.gov.cn/jzx/c116354/202607/612e29692f0449f183d38e0787727a8a.shtml"},

    {"id": 7, "name": "杨晓华", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "靖州苗族侗族自治县委常委", "current_org": "中共靖州苗族侗族自治县委员会",
     "source": "https://www.jzx.gov.cn/jzx/c116354/202607/612e29692f0449f183d38e0787727a8a.shtml"},

    {"id": 8, "name": "刘绍有", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "靖州苗族侗族自治县委常委", "current_org": "中共靖州苗族侗族自治县委员会",
     "source": "https://www.jzx.gov.cn/jzx/c116354/202607/612e29692f0449f183d38e0787727a8a.shtml"},

    {"id": 9, "name": "罗学贤", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "靖州苗族侗族自治县委常委、县委办主任", "current_org": "中共靖州苗族侗族自治县委员会",
     "source": "https://www.jzx.gov.cn/jzx/c116354/202606/77b60120b6f142d8a1243f7f7c43a1b7.shtml"},

    {"id": 10, "name": "周云", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "靖州苗族侗族自治县委常委、副县长", "current_org": "靖州苗族侗族自治县人民政府",
     "source": "https://www.jzx.gov.cn/jzx/c122051/xzf2020.shtml"},

    {"id": 11, "name": "许洪根", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "靖州苗族侗族自治县委常委", "current_org": "中共靖州苗族侗族自治县委员会",
     "source": "https://www.jzx.gov.cn/jzx/c116354/202607/612e29692f0449f183d38e0787727a8a.shtml"},

    # ── 副县长 ──
    {"id": 12, "name": "廉剑晖", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "靖州苗族侗族自治县副县长", "current_org": "靖州苗族侗族自治县人民政府",
     "source": "https://www.jzx.gov.cn/jzx/c122051/xzf2020.shtml"},

    {"id": 13, "name": "金波", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "靖州苗族侗族自治县副县长", "current_org": "靖州苗族侗族自治县人民政府",
     "source": "https://www.jzx.gov.cn/jzx/c122051/xzf2020.shtml"},

    {"id": 14, "name": "罗智敏", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "靖州苗族侗族自治县副县长", "current_org": "靖州苗族侗族自治县人民政府",
     "source": "https://www.jzx.gov.cn/jzx/c122051/xzf2020.shtml"},

    {"id": 15, "name": "蒋和平", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "靖州苗族侗族自治县副县长", "current_org": "靖州苗族侗族自治县人民政府",
     "source": "https://www.jzx.gov.cn/jzx/c122051/xzf2020.shtml"},

    {"id": 16, "name": "梁小彬", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "靖州苗族侗族自治县副县长", "current_org": "靖州苗族侗族自治县人民政府",
     "source": "https://www.jzx.gov.cn/jzx/c122051/xzf2020.shtml"},

    {"id": 17, "name": "任渔滨", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "靖州苗族侗族自治县副县长", "current_org": "靖州苗族侗族自治县人民政府",
     "source": "https://www.jzx.gov.cn/jzx/c122051/xzf2020.shtml"},
]

# ── ORGANIZATIONS ─────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共靖州苗族侗族自治县委员会", "type": "党委", "level": "县", "parent": "中共怀化市委", "location": "靖州苗族侗族自治县"},
    {"id": 2, "name": "靖州苗族侗族自治县人民政府", "type": "政府", "level": "县", "parent": "怀化市人民政府", "location": "靖州苗族侗族自治县"},
    {"id": 3, "name": "靖州苗族侗族自治县人大常委会", "type": "人大", "level": "县", "parent": "", "location": "靖州苗族侗族自治县"},
    {"id": 4, "name": "靖州苗族侗族自治县政协", "type": "政协", "level": "县", "parent": "", "location": "靖州苗族侗族自治县"},
]

# ── POSITIONS ─────────────────────────────────────────────────────────
positions = [
    # 张艳阳
    {"person_id": 1, "org_id": 1, "title": "靖州苗族侗族自治县委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "as of 2026-07-24 confirmed by official news"},

    # 滕海涛
    {"person_id": 2, "org_id": 1, "title": "靖州苗族侗族自治县委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "靖州苗族侗族自治县代理县长", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},

    # 四大班子
    {"person_id": 3, "org_id": 3, "title": "靖州苗族侗族自治县人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 4, "org_id": 4, "title": "靖州苗族侗族自治县政协主席", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},

    # 县委常委
    {"person_id": 5, "org_id": 1, "title": "靖州苗族侗族自治县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "靖州苗族侗族自治县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "靖州苗族侗族自治县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "靖州苗族侗族自治县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "靖州苗族侗族自治县委常委、县委办主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "靖州苗族侗族自治县委常委、副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 1, "title": "靖州苗族侗族自治县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},

    # 副县长
    {"person_id": 12, "org_id": 2, "title": "靖州苗族侗族自治县副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "靖州苗族侗族自治县副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "靖州苗族侗族自治县副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "靖州苗族侗族自治县副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "靖州苗族侗族自治县副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "靖州苗族侗族自治县副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
]

# ── RELATIONSHIPS ─────────────────────────────────────────────────────
relationships = [
    # 县委 — 政府 核心关系
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记—副书记/县长", "overlap_org": "中共靖州苗族侗族自治县委员会", "overlap_period": "2026~"},

    # 县委常委间共事关系
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "县委常委班子共事", "overlap_org": "中共靖州苗族侗族自治县委员会", "overlap_period": "2026~"},
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "县委常委班子共事", "overlap_org": "中共靖州苗族侗族自治县委员会", "overlap_period": "2026~"},
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "县委常委班子共事", "overlap_org": "中共靖州苗族侗族自治县委员会", "overlap_period": "2026~"},
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "县委常委班子共事", "overlap_org": "中共靖州苗族侗族自治县委员会", "overlap_period": "2026~"},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate", "context": "县委书记—县委办主任", "overlap_org": "中共靖州苗族侗族自治县委员会", "overlap_period": "2026~"},
    {"person_a": 1, "person_b": 10, "type": "overlap", "context": "县委常委班子共事", "overlap_org": "中共靖州苗族侗族自治县委员会", "overlap_period": "2026~"},
    {"person_a": 1, "person_b": 11, "type": "overlap", "context": "县委常委班子共事", "overlap_org": "中共靖州苗族侗族自治县委员会", "overlap_period": "2026~"},

    # 政府班子成员共事
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate", "context": "县长—副县长", "overlap_org": "靖州苗族侗族自治县人民政府", "overlap_period": "2026~"},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate", "context": "县长—副县长", "overlap_org": "靖州苗族侗族自治县人民政府", "overlap_period": "2026~"},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate", "context": "县长—副县长", "overlap_org": "靖州苗族侗族自治县人民政府", "overlap_period": "2026~"},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate", "context": "县长—副县长", "overlap_org": "靖州苗族侗族自治县人民政府", "overlap_period": "2026~"},
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate", "context": "县长—副县长", "overlap_org": "靖州苗族侗族自治县人民政府", "overlap_period": "2026~"},
    {"person_a": 2, "person_b": 16, "type": "superior_subordinate", "context": "县长—副县长", "overlap_org": "靖州苗族侗族自治县人民政府", "overlap_period": "2026~"},
    {"person_a": 2, "person_b": 17, "type": "superior_subordinate", "context": "县长—副县长", "overlap_org": "靖州苗族侗族自治县人民政府", "overlap_period": "2026~"},
]

# ── BUILD ─────────────────────────────────────────────────────────────
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
    print(f"Database: {DB_PATH}")
    print(f"GEXF:     {GEXF_PATH}")
    print(f"Persons:  {len(persons)}")
    print(f"Orgs:     {len(organizations)}")
    print(f"Positions:{len(positions)}")
    print(f"Relations:{len(relationships)}")
