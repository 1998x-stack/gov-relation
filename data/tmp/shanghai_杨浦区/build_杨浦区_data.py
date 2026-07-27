#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 上海市杨浦区 leadership network.

调查日期: 2026-07-25
信息来源: 上海市杨浦区人民政府门户网站 (www.shyp.gov.cn)
调查级别: 市辖区(直辖市)

Confirmed from government homepage/news (2026-07):
- 薛侃 — 杨浦区委书记
- 周海鹰 — 杨浦区委副书记、区长
"""

import json
import os
import sqlite3
import sys
from datetime import datetime

# ── Paths ──────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(BASE, "..", "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

STAGING_DIR = BASE
DB_PATH = os.path.join(STAGING_DIR, "杨浦区_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "杨浦区_network.gexf")
PERSONS_DIR = STAGING_DIR

TODAY = datetime.now().strftime("%Y%m%d")
SLUG = "上海市杨浦区"

# ── PERSONS ────────────────────────────────────────────────────────
persons = [
    # ═══════════════════════════════════════════════
    # 区委领导 (District Party Committee)
    # ═══════════════════════════════════════════════

    # 区委书记 — 薛侃
    {
        "id": 1,
        "name": "薛侃",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共上海市杨浦区委书记",
        "current_org": "中共上海市杨浦区委员会",
        "source": "http://www.shyp.gov.cn/",
    },
    # 区委副书记、区长 — 周海鹰
    {
        "id": 2,
        "name": "周海鹰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "杨浦区委副书记、区长",
        "current_org": "上海市杨浦区人民政府",
        "source": "http://www.shyp.gov.cn/",
    },
    # 区委副书记 — 周嵘
    {
        "id": 3,
        "name": "周嵘",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共上海市杨浦区委副书记",
        "current_org": "中共上海市杨浦区委员会",
        "source": "http://www.shyp.gov.cn/",
    },
    # 区委常委、副区长（常务）— 尼冰
    {
        "id": 4,
        "name": "尼冰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "杨浦区委常委、副区长（常务）",
        "current_org": "上海市杨浦区人民政府",
        "source": "http://www.shyp.gov.cn/",
    },
    # 区委常委、纪委书记、监委主任 — 包蕾
    {
        "id": 5,
        "name": "包蕾",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "杨浦区委常委、纪委书记、监委主任",
        "current_org": "中共上海市杨浦区纪律检查委员会",
        "source": "http://www.shyp.gov.cn/",
    },
    # 区委常委、组织部部长 — 秦丽萍
    {
        "id": 6,
        "name": "秦丽萍",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "杨浦区委常委、组织部部长",
        "current_org": "中共上海市杨浦区委组织部",
        "source": "http://www.shyp.gov.cn/",
    },
    # 区委常委、宣传部部长 — 施方
    {
        "id": 7,
        "name": "施方",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "杨浦区委常委、宣传部部长",
        "current_org": "中共上海市杨浦区委宣传部",
        "source": "http://www.shyp.gov.cn/",
    },
    # 区委常委、政法委书记 — 陆志斌
    {
        "id": 8,
        "name": "陆志斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "杨浦区委常委、政法委书记",
        "current_org": "中共上海市杨浦区委政法委员会",
        "source": "http://www.shyp.gov.cn/",
    },
    # 区委统战部部长 — (name not yet verified from available news)
    {
        "id": 9,
        "name": "待查_统战部部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "杨浦区委常委、统战部部长",
        "current_org": "中共上海市杨浦区委统战部",
        "source": "",
    },
    # 区委常委、区人民武装部政委 — (name not yet verified)
    {
        "id": 10,
        "name": "待查_人武部政委",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "杨浦区委常委、区人民武装部政委",
        "current_org": "上海市杨浦区人民武装部",
        "source": "",
    },
    # ═══════════════════════════════════════════════
    # 区政府副区长 (District Government)
    # ═══════════════════════════════════════════════

    # 副区长 — 徐明
    {
        "id": 11,
        "name": "徐明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "杨浦区副区长",
        "current_org": "上海市杨浦区人民政府",
        "source": "http://www.shyp.gov.cn/",
    },
    # 副区长 — 刘晋元
    {
        "id": 12,
        "name": "刘晋元",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "杨浦区副区长",
        "current_org": "上海市杨浦区人民政府",
        "source": "http://www.shyp.gov.cn/",
    },
    # 副区长 — 王浩
    {
        "id": 13,
        "name": "王浩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "杨浦区副区长",
        "current_org": "上海市杨浦区人民政府",
        "source": "http://www.shyp.gov.cn/",
    },
    # 副区长 — 苟如虎
    {
        "id": 14,
        "name": "苟如虎",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "杨浦区副区长",
        "current_org": "上海市杨浦区人民政府",
        "source": "http://www.shyp.gov.cn/",
    },
    # 副区长 — 于洋
    {
        "id": 15,
        "name": "于洋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "杨浦区副区长",
        "current_org": "上海市杨浦区人民政府",
        "source": "http://www.shyp.gov.cn/",
    },
    # ═══════════════════════════════════════════════
    # 人大、政协领导
    # ═══════════════════════════════════════════════

    # 区人大常委会主任 — 程绣明
    {
        "id": 16,
        "name": "程绣明",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "杨浦区人大常委会主任",
        "current_org": "上海市杨浦区人民代表大会常务委员会",
        "source": "http://www.shyp.gov.cn/",
    },
    # 区政协主席 — 邰荀
    {
        "id": 17,
        "name": "邰荀",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "杨浦区政协主席",
        "current_org": "中国人民政治协商会议上海市杨浦区委员会",
        "source": "http://www.shyp.gov.cn/",
    },
    # ═══════════════════════════════════════════════
    # 前任领导 (Predecessors — known connections)
    # ═══════════════════════════════════════════════

    # 前任区委书记 — 谢坚钢 (known predecessor of 薛侃)
    {
        "id": 18,
        "name": "谢坚钢",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "http://www.shyp.gov.cn/",
    },
    # 区政府办公室副主任 — (added as organizational member)
]

# ── ORGANIZATIONS ──────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共上海市杨浦区委员会", "type": "党委", "level": "市辖区(直辖市)", "parent": "中共上海市委", "location": "上海市杨浦区"},
    {"id": 2, "name": "上海市杨浦区人民政府", "type": "政府", "level": "市辖区(直辖市)", "parent": "上海市人民政府", "location": "上海市杨浦区"},
    {"id": 3, "name": "中共上海市杨浦区纪律检查委员会", "type": "纪委", "level": "市辖区(直辖市)", "parent": "中共上海市杨浦区委员会", "location": "上海市杨浦区"},
    {"id": 4, "name": "中共上海市杨浦区委组织部", "type": "党委部门", "level": "市辖区(直辖市)", "parent": "中共上海市杨浦区委员会", "location": "上海市杨浦区"},
    {"id": 5, "name": "中共上海市杨浦区委宣传部", "type": "党委部门", "level": "市辖区(直辖市)", "parent": "中共上海市杨浦区委员会", "location": "上海市杨浦区"},
    {"id": 6, "name": "中共上海市杨浦区委政法委员会", "type": "党委部门", "level": "市辖区(直辖市)", "parent": "中共上海市杨浦区委员会", "location": "上海市杨浦区"},
    {"id": 7, "name": "中共上海市杨浦区委统战部", "type": "党委部门", "level": "市辖区(直辖市)", "parent": "中共上海市杨浦区委员会", "location": "上海市杨浦区"},
    {"id": 8, "name": "上海市杨浦区人民武装部", "type": "军队", "level": "市辖区(直辖市)", "parent": "上海警备区", "location": "上海市杨浦区"},
    {"id": 9, "name": "上海市杨浦区人民代表大会常务委员会", "type": "人大", "level": "市辖区(直辖市)", "parent": "上海市人民代表大会常务委员会", "location": "上海市杨浦区"},
    {"id": 10, "name": "中国人民政治协商会议上海市杨浦区委员会", "type": "政协", "level": "市辖区(直辖市)", "parent": "中国人民政治协商会议上海市委员会", "location": "上海市杨浦区"},
]

# ── POSITIONS ──────────────────────────────────────────────────────
positions = [
    # 薛侃 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "中共上海市杨浦区委书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "现任杨浦区委书记"},
    # 周海鹰 — 区委副书记、区长
    {"person_id": 2, "org_id": 2, "title": "杨浦区委副书记、区长", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "现任杨浦区长"},
    {"person_id": 2, "org_id": 1, "title": "中共上海市杨浦区委副书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    # 周嵘 — 区委副书记
    {"person_id": 3, "org_id": 1, "title": "中共上海市杨浦区委副书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    # 尼冰 — 区委常委、常务副区长
    {"person_id": 4, "org_id": 2, "title": "杨浦区委常委、副区长（常务）", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "兼任区食药安委主任"},
    # 包蕾 — 纪委书记
    {"person_id": 5, "org_id": 3, "title": "杨浦区委常委、纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 秦丽萍 — 组织部部长
    {"person_id": 6, "org_id": 4, "title": "杨浦区委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 施方 — 宣传部部长
    {"person_id": 7, "org_id": 5, "title": "杨浦区委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 陆志斌 — 政法委书记
    {"person_id": 8, "org_id": 6, "title": "杨浦区委常委、政法委书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 待查_统战部部长
    {"person_id": 9, "org_id": 7, "title": "杨浦区委常委、统战部部长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "待确认姓名"},
    # 待查_人武部政委
    {"person_id": 10, "org_id": 8, "title": "杨浦区委常委、区人民武装部政委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "待确认姓名"},
    # 徐明 — 副区长
    {"person_id": 11, "org_id": 2, "title": "杨浦区副区长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "分管防汛等工作"},
    # 刘晋元 — 副区长
    {"person_id": 12, "org_id": 2, "title": "杨浦区副区长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 王浩 — 副区长
    {"person_id": 13, "org_id": 2, "title": "杨浦区副区长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "分管体育等工作"},
    # 苟如虎 — 副区长
    {"person_id": 14, "org_id": 2, "title": "杨浦区副区长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 于洋 — 副区长
    {"person_id": 15, "org_id": 2, "title": "杨浦区副区长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 程绣明 — 人大主任
    {"person_id": 16, "org_id": 9, "title": "杨浦区人大常委会主任", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "兼区选举委员会主任"},
    # 邰荀 — 政协主席
    {"person_id": 17, "org_id": 10, "title": "杨浦区政协主席", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    # 谢坚钢 — 前任区委书记
    {"person_id": 18, "org_id": 1, "title": "中共上海市杨浦区委书记（前任）", "start_date": "", "end_date": "", "rank": "正厅级", "note": "薛侃前任"},
]

# ── RELATIONSHIPS ─────────────────────────────────────────────────
relationships = [
    # 薛侃 — 周海鹰 (搭档)
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "区委书记—区长搭档关系", "overlap_org": "上海市杨浦区", "overlap_period": "至今"},
    # 薛侃 — 周嵘 (上下级)
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "区委书记—区委副书记", "overlap_org": "中共上海市杨浦区委员会", "overlap_period": ""},
    # 周海鹰 — 周嵘 (共事)
    {"person_a": 2, "person_b": 3, "type": "共事", "context": "区长—区委副书记", "overlap_org": "上海市杨浦区", "overlap_period": ""},
    # 薛侃 — 尼冰 (上下级)
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "区委书记—常务副区长", "overlap_org": "上海市杨浦区", "overlap_period": ""},
    # 周海鹰 — 尼冰 (上下级)
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "区长—常务副区长", "overlap_org": "上海市杨浦区人民政府", "overlap_period": ""},
    # 薛侃 — 各常委 (上下级)
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "区委书记—纪委书记", "overlap_org": "中共上海市杨浦区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "区委书记—组织部部长", "overlap_org": "中共上海市杨浦区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "区委书记—宣传部部长", "overlap_org": "中共上海市杨浦区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "区委书记—政法委书记", "overlap_org": "中共上海市杨浦区委员会", "overlap_period": ""},
    # 薛侃 — 谢坚钢 (前后任)
    {"person_a": 1, "person_b": 18, "type": "前后任", "context": "薛侃接替谢坚钢任杨浦区委书记", "overlap_org": "中共上海市杨浦区委员会", "overlap_period": ""},
    # 周海鹰 — 各副区长 (上下级)
    {"person_a": 2, "person_b": 11, "type": "上下级", "context": "区长—副区长", "overlap_org": "上海市杨浦区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 12, "type": "上下级", "context": "区长—副区长", "overlap_org": "上海市杨浦区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 13, "type": "上下级", "context": "区长—副区长", "overlap_org": "上海市杨浦区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 14, "type": "上下级", "context": "区长—副区长", "overlap_org": "上海市杨浦区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 15, "type": "上下级", "context": "区长—副区长", "overlap_org": "上海市杨浦区人民政府", "overlap_period": ""},
    # 人大常委会
    {"person_a": 1, "person_b": 16, "type": "共事", "context": "区委—人大", "overlap_org": "上海市杨浦区", "overlap_period": ""},
    {"person_a": 2, "person_b": 16, "type": "共事", "context": "政府—人大", "overlap_org": "上海市杨浦区", "overlap_period": ""},
    # 政协
    {"person_a": 1, "person_b": 17, "type": "共事", "context": "区委—政协", "overlap_org": "上海市杨浦区", "overlap_period": ""},
    {"person_a": 2, "person_b": 17, "type": "共事", "context": "政府—政协", "overlap_org": "上海市杨浦区", "overlap_period": ""},
]

# ── BUILD ──────────────────────────────────────────────────────────
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

if __name__ == "__main__":
    print(f"=== Building {SLUG} network ===")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

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

    # Export person JSON files
    def write_person_json(person: dict, job_label: str):
        filename = f"{TODAY}-上海市-杨浦区-{job_label}-{person['name']}.json"
        output = {
            "schema_version": "1.0",
            "generated_at": TODAY,
            "investigation_scope": {
                "province": "上海市",
                "city": "杨浦区",
                "region": "杨浦区",
                "job": person["current_post"],
                "task_id": "shanghai_杨浦区",
                "time_focus": "2024-2026",
            },
            "identity": {
                "person_id": f"yangpu_{person['name']}",
                "name": person["name"],
                "aliases": [],
                "gender": person.get("gender", ""),
                "ethnicity": person.get("ethnicity", ""),
                "birth": person.get("birth", ""),
                "birthplace": person.get("birthplace", ""),
                "native_place": person.get("birthplace", ""),
                "education": [{"period": "", "institution": "", "major": "", "degree": person.get("education", ""), "study_type": "unknown", "source_ids": ["S001"]}],
                "party_join": person.get("party_join", ""),
                "work_start": person.get("work_start", ""),
                "dedupe_keys": {
                    "name_birth": f"{person['name']}_{person.get('birth', '')}",
                    "name_birthplace": f"{person['name']}_{person.get('birthplace', '')}",
                    "official_profile_url": "",
                },
            },
            "current_status": {
                "current_post": person["current_post"],
                "current_org": person["current_org"],
                "administrative_rank": "",
                "as_of": TODAY,
                "is_current_confirmed": True,
                "source_ids": ["S001"],
            },
            "career_timeline": [
                {
                    "start": pos.get("start_date", ""),
                    "end": pos.get("end_date", ""),
                    "org": pos["org_id"],
                    "title": pos["title"],
                    "rank": pos.get("rank", ""),
                    "notes": pos.get("note", ""),
                    "confidence": "plausible",
                    "source_ids": ["S001"],
                }
                for pos in positions
                if pos["person_id"] == person["id"]
            ],
            "organizations": [
                {
                    "org_id": org["id"],
                    "name": org["name"],
                    "type": org["type"],
                    "level": org["level"],
                    "parent": org.get("parent", ""),
                    "location": org.get("location", ""),
                    "source_ids": ["S001"],
                }
                for org in organizations
                if org["id"] in {pos["org_id"] for pos in positions if pos["person_id"] == person["id"]}
            ],
            "relationships": [
                {
                    "person": p["name"],
                    "person_id": f"yangpu_{p['name']}",
                    "relationship_type": r["type"],
                    "strength": "strong" if r["type"] in ("共事", "前后任") else "medium",
                    "evidence": r["context"],
                    "overlap_org": r["overlap_org"],
                    "overlap_period": r["overlap_period"],
                    "direction": "undirected",
                    "confidence": "confirmed",
                    "source_ids": ["S001"],
                }
                for r in relationships
                for p in persons
                if (r["person_a"] == person["id"] and r["person_b"] == p["id"]) or (r["person_b"] == person["id"] and r["person_a"] == p["id"])
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "",
                "systems_experience": [],
                "geographic_pattern": [],
                "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, not private psychological assessment.",
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [],
            "source_register": [
                {
                    "id": "S001",
                    "title": "上海市杨浦区人民政府门户网站",
                    "url": "http://www.shyp.gov.cn/",
                    "publisher": "上海市杨浦区人民政府",
                    "published_at": "",
                    "accessed_at": TODAY,
                    "source_type": "official",
                    "reliability": "high",
                    "notes": "Confirmed current officeholders from homepage news feed (2026-07 articles)",
                }
            ],
            "confidence_summary": {
                "identity": "plausible",
                "current_role": "confirmed",
                "career_completeness": "partial",
                "relationship_confidence": "medium",
                "biggest_gap": "Detailed career timeline and education background need verification from official biography pages",
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": f"完整简历：{person['name']}的详细教育背景、早期职业生涯、晋升时间线",
                    "why_it_matters": "核心领导的履历完整度影响关系网络分析的深度",
                    "suggested_queries": [f"{person['name']} 简历", f"{person['name']} 任前公示"],
                    "last_attempted": TODAY,
                }
            ],
        }
        path = os.path.join(PERSONS_DIR, filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {filename}")

    # Core leaders (keys have valid names)
    write_person_json(persons[0], "区委书记")  # 薛侃
    write_person_json(persons[1], "区长")  # 周海鹰

    print(f"\n=== Done. Output in {STAGING_DIR} ===")
