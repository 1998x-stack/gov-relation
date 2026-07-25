#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 包头市青山区 leadership network.

Current as of: 2026-07-25
Data sources:
  - http://www.qsq.gov.cn/zwgk/fdzdgknr/fd_jgjj/jgjj_ldjj/ (government leadership listing)
  - http://www.qsq.gov.cn/xwdt/xwdt_qsyw/202607/t20260724_941378.html (区委书记白云喜 confirmed)
  - http://www.qsq.gov.cn/xwdt/xwdt_qsyw/202607/t20260720_940100.html (白云喜调研)
  - http://www.qsq.gov.cn/xwdt/xwdt_qsyw/202607/t20260723_941223.html (区委巡察会议)
  - http://www.qsq.gov.cn/xwdt/xwdt_qsyw/202607/t20260721_940384.html (党代会座谈会)
"""

import sys
sys.path.insert(0, "/workspace/data/xieming/other-codes/gov-relation")

import sqlite3
import os
from pathlib import Path

from gov_relation.runner import run_build
from gov_relation.paths import TMP_DIR, DATABASE_DIR, GRAPH_DIR, PERSONS_DIR, REPORT_DIR

TASK_ID = "inner_mongolia_青山区"
SLUG = "青山区"
TODAY = "2026-07-25"

# Staging paths
staging = TMP_DIR / TASK_ID
DB_PATH = str(staging / f"{SLUG}_network.db")
GEXF_PATH = str(staging / f"{SLUG}_network.gexf")

# ── Persons ──────────────────────────────────────────────────────────
persons = [
    # ── Core Leaders ──
    {
        "id": 1, "name": "白云喜", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "青山区委书记", "current_org": "中共包头市青山区委员会",
        "source": "http://www.qsq.gov.cn/xwdt/xwdt_qsyw/202607/t20260724_941378.html",
    },
    {
        "id": 2, "name": "王昊", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "青山区委副书记、区长", "current_org": "青山区人民政府",
        "source": "http://www.qsq.gov.cn/zwgk/fdzdgknr/fd_jgjj/jgjj_ldjj/",
    },
    # ── Deputy Party Secretaries & Standing Committee ──
    {
        "id": 3, "name": "苏雅勒图", "gender": "男", "ethnicity": "蒙古族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "青山区委副书记", "current_org": "中共包头市青山区委员会",
        "source": "http://www.qsq.gov.cn/xwdt/xwdt_qsyw/202607/t20260723_941223.html",
    },
    {
        "id": 4, "name": "杨建军", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区委常委、常务副区长", "current_org": "青山区人民政府",
        "source": "http://www.qsq.gov.cn/xwdt/xwdt_qsyw/202607/t20260724_941378.html",
    },
    {
        "id": 5, "name": "薄轲", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区委常委、组织部部长", "current_org": "中共包头市青山区委员会",
        "source": "http://www.qsq.gov.cn/xwdt/xwdt_qsyw/202607/t20260724_941378.html",
    },
    {
        "id": 6, "name": "郭浩", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区委常委、纪委书记、监委代主任", "current_org": "中共包头市青山区纪律检查委员会",
        "source": "http://www.qsq.gov.cn/xwdt/xwdt_qsyw/202607/t20260724_941378.html",
    },
    {
        "id": 7, "name": "张剑", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区委常委", "current_org": "中共包头市青山区委员会",
        "source": "http://www.qsq.gov.cn/xwdt/xwdt_qsyw/202607/t20260720_940100.html",
    },
    # ── Deputy District Mayors ──
    {
        "id": 8, "name": "李永刚", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "副区长", "current_org": "青山区人民政府",
        "source": "http://www.qsq.gov.cn/zwgk/fdzdgknr/fd_jgjj/jgjj_ldjj/",
    },
    {
        "id": 9, "name": "覃威", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "副区长", "current_org": "青山区人民政府",
        "source": "http://www.qsq.gov.cn/zwgk/fdzdgknr/fd_jgjj/jgjj_ldjj/",
    },
    {
        "id": 10, "name": "曹举", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "副区长", "current_org": "青山区人民政府",
        "source": "http://www.qsq.gov.cn/zwgk/fdzdgknr/fd_jgjj/jgjj_ldjj/",
    },
    {
        "id": 11, "name": "党一伟", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "副区长", "current_org": "青山区人民政府",
        "source": "http://www.qsq.gov.cn/zwgk/fdzdgknr/fd_jgjj/jgjj_ldjj/",
    },
    {
        "id": 12, "name": "高竹", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "副区长", "current_org": "青山区人民政府",
        "source": "http://www.qsq.gov.cn/zwgk/fdzdgknr/fd_jgjj/jgjj_ldjj/",
    },
    {
        "id": 13, "name": "李伟", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "副区长", "current_org": "青山区人民政府",
        "source": "http://www.qsq.gov.cn/zwgk/fdzdgknr/fd_jgjj/jgjj_ldjj/",
    },
    {
        "id": 14, "name": "李海峰", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区政府党组成员", "current_org": "青山区人民政府",
        "source": "http://www.qsq.gov.cn/zwgk/fdzdgknr/fd_jgjj/jgjj_ldjj/",
    },
]

# ── Organizations ────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共包头市青山区委员会", "type": "党委", "level": "县处级", "parent": "中共包头市委员会", "location": "包头市青山区"},
    {"id": 2, "name": "青山区人民政府", "type": "政府", "level": "县处级", "parent": "包头市人民政府", "location": "包头市青山区"},
    {"id": 3, "name": "中共包头市青山区纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共包头市青山区委员会", "location": "包头市青山区"},
    {"id": 4, "name": "中共包头市青山区委组织部", "type": "党委", "level": "乡科级", "parent": "中共包头市青山区委员会", "location": "包头市青山区"},
]

# ── Positions ────────────────────────────────────────────────────────
positions = [
    # 白云喜
    {"person_id": 1, "org_id": 1, "title": "青山区委书记", "start_date": "", "end_date": "present", "rank": "正县处级", "note": ""},
    # 王昊
    {"person_id": 2, "org_id": 1, "title": "青山区委副书记", "start_date": "", "end_date": "present", "rank": "副县处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "", "end_date": "present", "rank": "正县处级", "note": ""},
    # 苏雅勒图
    {"person_id": 3, "org_id": 1, "title": "青山区委副书记", "start_date": "", "end_date": "present", "rank": "副县处级", "note": ""},
    # 杨建军
    {"person_id": 4, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "副县处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "常务副区长", "start_date": "", "end_date": "present", "rank": "副县处级", "note": "区政府党组副书记"},
    # 薄轲
    {"person_id": 5, "org_id": 1, "title": "区委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "副县处级", "note": ""},
    # 郭浩
    {"person_id": 6, "org_id": 1, "title": "区委常委、纪委书记", "start_date": "", "end_date": "present", "rank": "副县处级", "note": ""},
    {"person_id": 6, "org_id": 3, "title": "监委代主任", "start_date": "", "end_date": "present", "rank": "副县处级", "note": ""},
    # 张剑
    {"person_id": 7, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "副县处级", "note": ""},
    # 李永刚
    {"person_id": 8, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副县处级", "note": ""},
    # 覃威
    {"person_id": 9, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副县处级", "note": ""},
    # 曹举
    {"person_id": 10, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副县处级", "note": ""},
    # 党一伟
    {"person_id": 11, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副县处级", "note": ""},
    # 高竹
    {"person_id": 12, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副县处级", "note": ""},
    # 李伟
    {"person_id": 13, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副县处级", "note": ""},
    # 李海峰
    {"person_id": 14, "org_id": 2, "title": "区政府党组成员", "start_date": "", "end_date": "present", "rank": "副县处级", "note": ""},
]

# ── Relationships ────────────────────────────────────────────────────
relationships = [
    # Core leadership team overlap
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "区委书记与区长搭班子", "overlap_org": "中共包头市青山区委员会/青山区人民政府", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "区委书记与副书记搭班子", "overlap_org": "中共包头市青山区委员会", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "区委书记与常务副区长搭班子", "overlap_org": "中共包头市青山区委员会", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "区委书记与组织部部长搭班子", "overlap_org": "中共包头市青山区委员会", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "区委书记与纪委书记搭班子", "overlap_org": "中共包头市青山区委员会", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "区委常委班子共事", "overlap_org": "中共包头市青山区委员会", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "区长与常务副区长搭班子", "overlap_org": "青山区人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "区长与区委副书记搭班子", "overlap_org": "中共包头市青山区委员会", "overlap_period": "当前"},
    {"person_a": 4, "person_b": 8, "type": "overlap", "context": "常务副区长与副区长共事", "overlap_org": "青山区人民政府", "overlap_period": "当前"},
    {"person_a": 4, "person_b": 10, "type": "overlap", "context": "常务副区长与副区长共事", "overlap_org": "青山区人民政府", "overlap_period": "当前"},
    {"person_a": 5, "person_b": 6, "type": "overlap", "context": "组织部与纪委协作（巡察工作）", "overlap_org": "中共包头市青山区委员会", "overlap_period": "当前"},
]

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
    print(f"Done. DB: {DB_PATH}, GEXF: {GEXF_PATH}")
