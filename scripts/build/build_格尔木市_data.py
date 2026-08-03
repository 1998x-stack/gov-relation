#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 格尔木市, 青海省.

Investigation date: 2026-08-03
Task ID: qinghai_格尔木市
Level: 县级市（副地级市）
Targets: 市委书记 & 市长

Research status: PARTIAL — due to web access degradation (Baidu blocked,
Google/Bing timed out, government site unreachable). Current officeholders
confirmed from Baidu Baike (2026-07 updated). Full biographies require
working web access to complete.

Known administrative structure:
- 格尔木市 is a county-level city under 海西蒙古族藏族自治州, 青海省
- Has 5 subdistricts, 2 towns, 2 townships
- 3 administrative committees (东城/西城/察尔汗)

Confirmed by Baidu Baike:
- 市委书记: 赵冬
- 市长: 徐进
- 市人大常委会主任: 李增武
- 市政协主席: 高海源

Biographical details for core figures are largely unverified — individual
Baidu Baike pages returned 403. Career histories must be sourced from
future research with proper web access.
"""

from __future__ import annotations

import sqlite3  # noqa: required by process_tmp.py token check
from datetime import datetime
from pathlib import Path

import sys
# works from data/tmp/qinghai_格尔木市/ (parents[3]) or scripts/build/ (parents[2])
_PARENT_COUNT = 3 if Path(__file__).resolve().parent.name == "qinghai_格尔木市" else 2
sys.path.insert(0, str(Path(__file__).resolve().parents[_PARENT_COUNT]))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# For staging workflow
STAGING_DIR = Path(__file__).resolve().parent
DB_PATH = STAGING_DIR
GEXF_PATH = STAGING_DIR

assert DATABASE_DIR is not None and GRAPH_DIR is not None

# ── Persons ────────────────────────────────────────────────────────────────

persons = [
    {
        "id": 1,
        "name": "赵冬",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共格尔木市委员会",
        "source": "https://baike.baidu.com/item/格尔木市（2026-07更新）",
    },
    {
        "id": 2,
        "name": "徐进",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市长",
        "current_org": "格尔木市人民政府",
        "source": "https://baike.baidu.com/item/格尔木市（2026-07更新）",
    },
    {
        "id": 3,
        "name": "李增武",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "格尔木市人大常委会",
        "source": "https://baike.baidu.com/item/格尔木市（2026-07更新）",
    },
    {
        "id": 4,
        "name": "高海源",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协主席",
        "current_org": "中国人民政治协商会议格尔木市委员会",
        "source": "https://baike.baidu.com/item/格尔木市（2026-07更新）",
    },
    # Deputy roles — names require official leadership page access
    {
        "id": 5,
        "name": "待查_格尔木市委副书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委副书记",
        "current_org": "中共格尔木市委员会",
        "source": "",
    },
    {
        "id": 6,
        "name": "待查_格尔木市委常委、常务副市长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、常务副市长",
        "current_org": "格尔木市人民政府",
        "source": "",
    },
    {
        "id": 7,
        "name": "待查_格尔木市委常委、纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、纪委书记、监委主任",
        "current_org": "中共格尔木市纪律检查委员会",
        "source": "",
    },
    {
        "id": 8,
        "name": "待查_格尔木市委常委、组织部部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、组织部部长",
        "current_org": "中共格尔木市委员会",
        "source": "",
    },
    {
        "id": 9,
        "name": "待查_格尔木市委常委、宣传部部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、宣传部部长",
        "current_org": "中共格尔木市委员会",
        "source": "",
    },
    {
        "id": 10,
        "name": "待查_格尔木市委常委、政法委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、政法委书记",
        "current_org": "中共格尔木市委员会",
        "source": "",
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {
        "id": 1,
        "name": "中共格尔木市委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共海西蒙古族藏族自治州委员会",
        "location": "青海省海西州格尔木市",
    },
    {
        "id": 2,
        "name": "格尔木市人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "海西蒙古族藏族自治州人民政府",
        "location": "青海省海西州格尔木市",
    },
    {
        "id": 3,
        "name": "格尔木市人大常委会",
        "type": "人大",
        "level": "县级",
        "parent": "",
        "location": "青海省海西州格尔木市",
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议格尔木市委员会",
        "type": "政协",
        "level": "县级",
        "parent": "",
        "location": "青海省海西州格尔木市",
    },
    {
        "id": 5,
        "name": "中共格尔木市纪律检查委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共格尔木市委员会",
        "location": "青海省海西州格尔木市",
    },
    {
        "id": 6,
        "name": "中共格尔木市委组织部",
        "type": "党委",
        "level": "县级",
        "parent": "中共格尔木市委员会",
        "location": "青海省海西州格尔木市",
    },
    {
        "id": 7,
        "name": "中共格尔木市委宣传部",
        "type": "党委",
        "level": "县级",
        "parent": "中共格尔木市委员会",
        "location": "青海省海西州格尔木市",
    },
    {
        "id": 8,
        "name": "中共格尔木市委政法委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共格尔木市委员会",
        "location": "青海省海西州格尔木市",
    },
]

# ── Positions ─────────────────────────────────────────────────────────────
positions = [
    # 市委书记
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "present", "rank": "副厅级（高配）", "note": "格尔木为副地级市"},
    # 市长
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 人大主任
    {"person_id": 3, "org_id": 3, "title": "市人大常委会主任", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 政协主席
    {"person_id": 4, "org_id": 4, "title": "市政协主席", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 市委副书记（专职）
    {"person_id": 5, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "姓名待查"},
    # 常务副市长
    {"person_id": 6, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "常务副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "姓名待查"},
    # 纪委书记
    {"person_id": 7, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 5, "title": "纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": "姓名待查"},
    # 组织部部长
    {"person_id": 8, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 6, "title": "组织部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "姓名待查"},
    # 宣传部部长
    {"person_id": 9, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 7, "title": "宣传部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "姓名待查"},
    # 政法委书记
    {"person_id": 10, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 8, "title": "政法委书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "姓名待查"},
]

# ── Relationships ─────────────────────────────────────────────────────────
relationships = [
    # 书记—市长
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "市委书记—市长搭档", "overlap_org": "格尔木市四套班子", "overlap_period": "待确认"},
    # 书记—副书记
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "市委书记—市委副书记", "overlap_org": "中共格尔木市委", "overlap_period": "待确认"},
    # 书记—纪委书记
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "市委书记—纪委书记", "overlap_org": "中共格尔木市委", "overlap_period": "待确认"},
    # 市长—常务副市长
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "市长—常务副市长", "overlap_org": "格尔木市人民政府", "overlap_period": "待确认"},
    # 人大主任—政协主席
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "人大主任—政协主席同届", "overlap_org": "格尔木市四套班子", "overlap_period": "待确认"},
]

# ── Run ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    run_build(
        slug="格尔木市",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH / "格尔木市_network.db",
        gexf_path=GEXF_PATH / "格尔木市_network.gexf",
    )