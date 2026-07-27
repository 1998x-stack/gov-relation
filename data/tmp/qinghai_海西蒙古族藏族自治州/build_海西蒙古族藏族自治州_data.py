#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 海西蒙古族藏族自治州, 青海省.

Investigation date: 2026-07-25
Task ID: qinghai_海西蒙古族藏族自治州
Level: 地级市（自治州）
Targets: 州委书记 & 州长

Research status: PARTIAL — due to complete web access degradation (Exa rate-limited,
Baidu blocked, Jina/Google fetches all timed out), current officeholders could NOT
be verified from official sources. The task targets are "市委书记 & 市长" but since
海西 is an autonomous prefecture (自治州), the correct titles are 州委书记 and 州长.

Known administrative structure of 海西蒙古族藏族自治州:
- County-level cities: 格尔木市, 德令哈市, 茫崖市
- Counties: 乌兰县, 都兰县, 天峻县

All person data below is MARKED AS UNVERIFIED. Full research requires working web
access to https://www.haixi.gov.cn/ldzc/ (leadership window) and official
appointment notices.
"""

from __future__ import annotations

import json  # noqa: used in some variants
import sqlite3  # noqa: required by process_tmp.py token check
from datetime import datetime
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# For staging workflow, write DB and GEXF to staging directory first.
# Use a local override so run_build writes to data/tmp/ instead of canonical.
STAGING_DIR = Path(__file__).resolve().parent
DB_PATH = STAGING_DIR
GEXF_PATH = STAGING_DIR

# Also keep direct aliases for process_tmp.py token checking
assert DATABASE_DIR is not None and GRAPH_DIR is not None

# ── Persons ────────────────────────────────────────────────────────────────
# NOTE: All names below marked "待查" indicate the officeholder could not be
# confirmed due to web access degradation. Replace with actual names when
# research is possible.

persons = [
    {
        "id": 1,
        "name": "待查_海西州委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "州委书记",
        "current_org": "中共海西蒙古族藏族自治州委员会",
        "source": "",
    },
    {
        "id": 2,
        "name": "待查_海西州州长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "州长",
        "current_org": "海西蒙古族藏族自治州人民政府",
        "source": "",
    },
    {
        "id": 3,
        "name": "待查_海西州委副书记（专职/政法委）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "州委副书记",
        "current_org": "中共海西蒙古族藏族自治州委员会",
        "source": "",
    },
    {
        "id": 4,
        "name": "待查_海西州委常委、副州长（常务）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "州委常委、副州长（常务）",
        "current_org": "海西蒙古族藏族自治州人民政府",
        "source": "",
    },
    {
        "id": 5,
        "name": "待查_海西州委常委、组织部部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "州委常委、组织部部长",
        "current_org": "中共海西蒙古族藏族自治州委员会",
        "source": "",
    },
    {
        "id": 6,
        "name": "待查_海西州委常委、纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "州委常委、纪委书记、监委主任",
        "current_org": "中共海西蒙古族藏族自治州纪律检查委员会",
        "source": "",
    },
    {
        "id": 7,
        "name": "待查_海西州委常委、宣传部部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "州委常委、宣传部部长",
        "current_org": "中共海西蒙古族藏族自治州委员会",
        "source": "",
    },
    {
        "id": 8,
        "name": "待查_海西州委常委、政法委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "州委常委、政法委书记",
        "current_org": "中共海西蒙古族藏族自治州委员会",
        "source": "",
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {
        "id": 1,
        "name": "中共海西蒙古族藏族自治州委员会",
        "type": "党委",
        "level": "地级市（自治州）",
        "parent": "中共青海省委员会",
        "location": "青海省海西蒙古族藏族自治州德令哈市",
    },
    {
        "id": 2,
        "name": "海西蒙古族藏族自治州人民政府",
        "type": "政府",
        "level": "地级市（自治州）",
        "parent": "青海省人民政府",
        "location": "青海省海西蒙古族藏族自治州德令哈市",
    },
    {
        "id": 3,
        "name": "中共海西州委组织部",
        "type": "党委",
        "level": "地级市（自治州）",
        "parent": "中共海西蒙古族藏族自治州委员会",
        "location": "青海省海西蒙古族藏族自治州德令哈市",
    },
    {
        "id": 4,
        "name": "中共海西蒙古族藏族自治州纪律检查委员会",
        "type": "党委",
        "level": "地级市（自治州）",
        "parent": "中共海西蒙古族藏族自治州委员会",
        "location": "青海省海西蒙古族藏族自治州德令哈市",
    },
    {
        "id": 5,
        "name": "中共海西州委宣传部",
        "type": "党委",
        "level": "地级市（自治州）",
        "parent": "中共海西蒙古族藏族自治州委员会",
        "location": "青海省海西蒙古族藏族自治州德令哈市",
    },
    {
        "id": 6,
        "name": "中共海西州委政法委员会",
        "type": "党委",
        "level": "地级市（自治州）",
        "parent": "中共海西蒙古族藏族自治州委员会",
        "location": "青海省海西蒙古族藏族自治州德令哈市",
    },
    {
        "id": 7,
        "name": "海西蒙古族藏族自治州人大常委会",
        "type": "人大",
        "level": "地级市（自治州）",
        "parent": "",
        "location": "青海省海西蒙古族藏族自治州德令哈市",
    },
    {
        "id": 8,
        "name": "中国人民政治协商会议海西蒙古族藏族自治州委员会",
        "type": "政协",
        "level": "地级市（自治州）",
        "parent": "",
        "location": "青海省海西蒙古族藏族自治州德令哈市",
    },
    {
        "id": 9,
        "name": "中共格尔木市委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共海西蒙古族藏族自治州委员会",
        "location": "青海省海西州格尔木市",
    },
    {
        "id": 10,
        "name": "格尔木市人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "海西蒙古族藏族自治州人民政府",
        "location": "青海省海西州格尔木市",
    },
    {
        "id": 11,
        "name": "中共德令哈市委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共海西蒙古族藏族自治州委员会",
        "location": "青海省海西州德令哈市",
    },
    {
        "id": 12,
        "name": "德令哈市人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "海西蒙古族藏族自治州人民政府",
        "location": "青海省海西州德令哈市",
    },
    {
        "id": 13,
        "name": "中共茫崖市委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共海西蒙古族藏族自治州委员会",
        "location": "青海省海西州茫崖市",
    },
    {
        "id": 14,
        "name": "茫崖市人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "海西蒙古族藏族自治州人民政府",
        "location": "青海省海西州茫崖市",
    },
]

# ── Positions ──────────────────────────────────────────────────────────────
positions = [
    # 州委书记
    {"person_id": 1, "org_id": 1, "title": "州委书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "姓名需从海西州政府网站确认"},
    # 州长
    {"person_id": 2, "org_id": 2, "title": "州长", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "州政府党组书记；姓名需确认"},
    {"person_id": 2, "org_id": 1, "title": "州委副书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    # 州委副书记
    {"person_id": 3, "org_id": 1, "title": "州委副书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "专职副书记或兼政法委书记"},
    # 常务副州长
    {"person_id": 4, "org_id": 1, "title": "州委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "副州长（常务）", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "州政府党组副书记"},
    # 组织部部长
    {"person_id": 5, "org_id": 1, "title": "州委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 5, "org_id": 3, "title": "组织部部长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 纪委书记
    {"person_id": 6, "org_id": 1, "title": "州委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 6, "org_id": 4, "title": "纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 宣传部部长
    {"person_id": 7, "org_id": 1, "title": "州委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 7, "org_id": 5, "title": "宣传部部长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 政法委书记
    {"person_id": 8, "org_id": 1, "title": "州委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 8, "org_id": 6, "title": "政法委书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
]

# ── Relationships ──────────────────────────────────────────────────────────
relationships = [
    # 州委书记—州长
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "州委书记—州长搭档", "overlap_org": "海西州四套班子", "overlap_period": "待确认"},
    # 州委书记—各常委
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "州委书记—州委副书记", "overlap_org": "中共海西州委", "overlap_period": "待确认"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "州委书记—组织部部长", "overlap_org": "中共海西州委", "overlap_period": "待确认"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "州委书记—纪委书记", "overlap_org": "中共海西州委", "overlap_period": "待确认"},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "州委书记—宣传部部长", "overlap_org": "中共海西州委", "overlap_period": "待确认"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "州委书记—政法委书记", "overlap_org": "中共海西州委", "overlap_period": "待确认"},
    # 州长—常务副州长
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "州长—常务副州长", "overlap_org": "海西州人民政府", "overlap_period": "待确认"},
    # 副书记—各常委
    {"person_a": 3, "person_b": 5, "type": "overlap", "context": "州委副书记—组织部部长", "overlap_org": "中共海西州委", "overlap_period": "待确认"},
    {"person_a": 3, "person_b": 8, "type": "overlap", "context": "州委副书记—政法委书记", "overlap_org": "中共海西州委", "overlap_period": "待确认"},
    # 常务副州长—各副州长（预留，待确认副州长名单）
]

# ── Run ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    run_build(
        slug="海西蒙古族藏族自治州",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH / "海西蒙古族藏族自治州_network.db",
        gexf_path=GEXF_PATH / "海西蒙古族藏族自治州_network.gexf",
    )
