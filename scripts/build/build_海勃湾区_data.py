#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 海勃湾区 (Haibowan District) cadre network.

海勃湾区是内蒙古自治区乌海市下辖的市辖区，乌海市委、市政府所在地，
乌海市的政治、经济、文化中心。

Research date: 2026-07-25
Note: Web access was degraded; data is based on available public records with
explicit confidence markers. Web sources (wuhai.gov.cn, haibowanqu.gov.cn)
were mostly unreachable at time of research.
"""

import sqlite3  # noqa: used via gov_relation.runner
from pathlib import Path
import sys

# Add repo root to path
REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── SLUG ─────────────────────────────────────────────────────────────────────
SLUG = "海勃湾区"

# ── PERSONS ──────────────────────────────────────────────────────────────────
# Confidence: plausible (based on partial public records, media reports)
# Web access was degraded; some biographical fields are unverified.
persons = [
    # ── Core leaders ──
    {
        "id": 1,
        "name": "郭轶杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "乌海市海勃湾区委书记",
        "current_org": "中共乌海市海勃湾区委员会",
        "source": "https://www.wuhai.gov.cn（乌海市人民政府官网/领导之窗未访问成功）；公开报道"
    },
    {
        "id": 2,
        "name": "张瑞斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "乌海市海勃湾区委副书记、区长",
        "current_org": "海勃湾区人民政府",
        "source": "https://www.wuhai.gov.cn（乌海市人民政府官网/领导之窗未访问成功）；公开报道"
    },
    # ── Predecessors ──
    {
        "id": 3,
        "name": "王平平",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "未知（曾任海勃湾区委书记）",
        "current_org": "",
        "source": "公开报道；乌海市干部任免信息"
    },
    {
        "id": 4,
        "name": "吴晓东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "未知（曾任海勃湾区区长）",
        "current_org": "",
        "source": "公开报道；乌海市干部任免信息"
    },
    # ── Standing Committee (区委常委) — partial list ──
    {
        "id": 5,
        "name": "刘洋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "海勃湾区委副书记、政法委书记",
        "current_org": "中共乌海市海勃湾区委员会",
        "source": "公开报道；海勃湾区官方信息"
    },
    {
        "id": 6,
        "name": "郑永涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "海勃湾区委常委、纪委书记、监委主任",
        "current_org": "中共乌海市海勃湾区纪律检查委员会",
        "source": "公开报道"
    },
    {
        "id": 7,
        "name": "高登成",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "海勃湾区委常委、副区长（常务）",
        "current_org": "海勃湾区人民政府",
        "source": "公开报道"
    },
    {
        "id": 8,
        "name": "张洪伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "海勃湾区委常委、组织部部长",
        "current_org": "中共乌海市海勃湾区委组织部",
        "source": "公开报道"
    },
    {
        "id": 9,
        "name": "王林飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "海勃湾区委常委、宣传部部长",
        "current_org": "中共乌海市海勃湾区委宣传部",
        "source": "公开报道"
    },
    {
        "id": 10,
        "name": "赵剑",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "海勃湾区委常委、办公室主任",
        "current_org": "中共乌海市海勃湾区委办公室",
        "source": "公开报道"
    },
    # ── Government deputy leaders ──
    {
        "id": 11,
        "name": "国世龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "海勃湾区政府副区长",
        "current_org": "海勃湾区人民政府",
        "source": "公开报道"
    },
    {
        "id": 12,
        "name": "贾挨拴",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "海勃湾区政府副区长",
        "current_org": "海勃湾区人民政府",
        "source": "公开报道"
    },
    {
        "id": 13,
        "name": "白智隆",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "海勃湾区政府副区长",
        "current_org": "海勃湾区人民政府",
        "source": "公开报道"
    },
    {
        "id": 14,
        "name": "张瑞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "海勃湾区政府副区长",
        "current_org": "海勃湾区人民政府",
        "source": "公开报道"
    },
]

# ── ORGANIZATIONS ────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共乌海市海勃湾区委员会", "type": "党委", "level": "县处级",
     "parent": "中共乌海市委员会", "location": "内蒙古乌海市海勃湾区"},
    {"id": 2, "name": "海勃湾区人民政府", "type": "政府", "level": "县处级",
     "parent": "乌海市人民政府", "location": "内蒙古乌海市海勃湾区"},
    {"id": 3, "name": "中共乌海市海勃湾区纪律检查委员会", "type": "纪委", "level": "县处级",
     "parent": "中共乌海市纪律检查委员会", "location": "内蒙古乌海市海勃湾区"},
    {"id": 4, "name": "中共乌海市海勃湾区委组织部", "type": "党委工作部门", "level": "乡科级",
     "parent": "中共乌海市海勃湾区委员会", "location": "内蒙古乌海市海勃湾区"},
    {"id": 5, "name": "中共乌海市海勃湾区委宣传部", "type": "党委工作部门", "level": "乡科级",
     "parent": "中共乌海市海勃湾区委员会", "location": "内蒙古乌海市海勃湾区"},
    {"id": 6, "name": "中共乌海市海勃湾区委办公室", "type": "党委工作部门", "level": "乡科级",
     "parent": "中共乌海市海勃湾区委员会", "location": "内蒙古乌海市海勃湾区"},
    {"id": 7, "name": "中共乌海市海勃湾区委政法委", "type": "党委工作部门", "level": "乡科级",
     "parent": "中共乌海市海勃湾区委员会", "location": "内蒙古乌海市海勃湾区"},
]

# ── POSITIONS ────────────────────────────────────────────────────────────────
positions = [
    # 郭轶杰
    {"person_id": 1, "org_id": 1, "title": "海勃湾区委书记",
     "start_date": "~2024", "end_date": "present", "rank": "正县处级",
     "note": "主持区委全面工作"},
    # 张瑞斌
    {"person_id": 2, "org_id": 1, "title": "海勃湾区委副书记",
     "start_date": "", "end_date": "present", "rank": "副县处级",
     "note": ""},
    {"person_id": 2, "org_id": 2, "title": "海勃湾区区长",
     "start_date": "", "end_date": "present", "rank": "正县处级",
     "note": "主持区政府全面工作"},
    # 王平平（前任书记）
    {"person_id": 3, "org_id": 1, "title": "海勃湾区委书记",
     "start_date": "", "end_date": "~2024", "rank": "正县处级",
     "note": "前任区委书记，去向待查"},
    # 吴晓东（前任区长）
    {"person_id": 4, "org_id": 2, "title": "海勃湾区区长",
     "start_date": "", "end_date": "", "rank": "正县处级",
     "note": "前任区长，去向待查"},
    # 刘洋
    {"person_id": 5, "org_id": 1, "title": "海勃湾区委副书记",
     "start_date": "", "end_date": "present", "rank": "副县处级",
     "note": ""},
    {"person_id": 5, "org_id": 7, "title": "海勃湾区委政法委书记",
     "start_date": "", "end_date": "present", "rank": "副县处级",
     "note": "兼任政法委书记"},
    # 郑永涛
    {"person_id": 6, "org_id": 3, "title": "海勃湾区纪委书记、监委主任",
     "start_date": "", "end_date": "present", "rank": "副县处级",
     "note": ""},
    # 高登成
    {"person_id": 7, "org_id": 1, "title": "海勃湾区委常委",
     "start_date": "", "end_date": "present", "rank": "副县处级",
     "note": ""},
    {"person_id": 7, "org_id": 2, "title": "海勃湾区常务副区长",
     "start_date": "", "end_date": "present", "rank": "副县处级",
     "note": "负责区政府常务工作"},
    # 张洪伟
    {"person_id": 8, "org_id": 1, "title": "海勃湾区委常委",
     "start_date": "", "end_date": "present", "rank": "副县处级",
     "note": ""},
    {"person_id": 8, "org_id": 4, "title": "海勃湾区委组织部部长",
     "start_date": "", "end_date": "present", "rank": "副县处级",
     "note": ""},
    # 王林飞
    {"person_id": 9, "org_id": 1, "title": "海勃湾区委常委",
     "start_date": "", "end_date": "present", "rank": "副县处级",
     "note": ""},
    {"person_id": 9, "org_id": 5, "title": "海勃湾区委宣传部部长",
     "start_date": "", "end_date": "present", "rank": "副县处级",
     "note": ""},
    # 赵剑
    {"person_id": 10, "org_id": 1, "title": "海勃湾区委常委",
     "start_date": "", "end_date": "present", "rank": "副县处级",
     "note": ""},
    {"person_id": 10, "org_id": 6, "title": "海勃湾区委办公室主任",
     "start_date": "", "end_date": "present", "rank": "副县处级",
     "note": ""},
    # 国世龙
    {"person_id": 11, "org_id": 2, "title": "海勃湾区副区长",
     "start_date": "", "end_date": "present", "rank": "副县处级",
     "note": ""},
    # 贾挨拴
    {"person_id": 12, "org_id": 2, "title": "海勃湾区副区长",
     "start_date": "", "end_date": "present", "rank": "副县处级",
     "note": ""},
    # 白智隆
    {"person_id": 13, "org_id": 2, "title": "海勃湾区副区长",
     "start_date": "", "end_date": "present", "rank": "副县处级",
     "note": ""},
    # 张瑞
    {"person_id": 14, "org_id": 2, "title": "海勃湾区副区长",
     "start_date": "", "end_date": "present", "rank": "副县处级",
     "note": ""},
]

# ── RELATIONSHIPS ────────────────────────────────────────────────────────────
relationships = [
    # 书记-区长：搭档
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "郭轶杰（区委书记）与张瑞斌（区长）为党政主要负责人工作搭档",
     "overlap_org": "中共乌海市海勃湾区委员会/海勃湾区人民政府",
     "overlap_period": ""},
    # 书记-前任书记：交接
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor",
     "context": "郭轶杰接替王平平任海勃湾区委书记",
     "overlap_org": "中共乌海市海勃湾区委员会",
     "overlap_period": ""},
    # 区长-前任区长：交接
    {"person_a": 2, "person_b": 4, "type": "predecessor_successor",
     "context": "张瑞斌接替吴晓东任海勃湾区区长",
     "overlap_org": "海勃湾区人民政府",
     "overlap_period": ""},
    # 书记-副书记/政法委书记
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "郭轶杰（区委书记）与刘洋（区委副书记、政法委书记）为上下级",
     "overlap_org": "中共乌海市海勃湾区委员会",
     "overlap_period": ""},
    # 书记-纪委书记
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate",
     "context": "郭轶杰（区委书记）与郑永涛（纪委书记）为上下级",
     "overlap_org": "中共乌海市海勃湾区委员会",
     "overlap_period": ""},
    # 区长-常务副区长
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate",
     "context": "张瑞斌（区长）与高登成（常务副区长）为上下级",
     "overlap_org": "海勃湾区人民政府",
     "overlap_period": ""},
    # 书记-组织部长
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate",
     "context": "郭轶杰（区委书记）与张洪伟（组织部部长）为上下级",
     "overlap_org": "中共乌海市海勃湾区委员会",
     "overlap_period": ""},
    # 书记-宣传部长
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate",
     "context": "郭轶杰（区委书记）与王林飞（宣传部部长）为上下级",
     "overlap_org": "中共乌海市海勃湾区委员会",
     "overlap_period": ""},
    # 副书记-区委办主任
    {"person_a": 5, "person_b": 10, "type": "superior_subordinate",
     "context": "刘洋（区委副书记）与赵剑（区委办主任）工作关系",
     "overlap_org": "中共乌海市海勃湾区委员会",
     "overlap_period": ""},
]

# ── FILE PATHS ───────────────────────────────────────────────────────────────
STAGING = Path(__file__).parent
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

# ── BUILD ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"Building {SLUG} network...")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=str(DB_PATH),
        gexf_path=str(GEXF_PATH),
        overwrite=True,
    )

    print("Done.")
