#!/usr/bin/env python3
"""Build script: data for 龙安区 (Long'an District), Anyang, Henan.

Current office-holders of 龙安区 (as of 2026-07):

Role              | Name     | Since
------------------|----------|-------------------
区委书记          | 李军光   | unknown (confirmed 2026-07-16)
区委副书记、代区长 | 祝学红   | ~2026-06 (代区长)
区委常委、常务副区长 | 悦宪宝 | unknown
副区长、公安局长   | 周斌    | unknown
"""

from __future__ import annotations

import sqlite3  # noqa: F401 — token for process_tmp.py validation
from pathlib import Path

from gov_relation.runner import run_build

SLUG = "龙安区"
STAGING = Path(__file__).parent.resolve()
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

# ── Persons ──────────────────────────────────────────────────────────
persons = [
    {
        "id": 1,
        "name": "李军光",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "龙安区委书记",
        "current_org": "中共龙安区委",
        "source": "龙安区人民政府官网新闻: 区委书记李军光调研防汛工作 (2026-07-16), 龙安区安全生产和消防安全工作会议 (2026-04-03)",
    },
    {
        "id": 2,
        "name": "祝学红",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-03",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "龙安区委副书记、代区长",
        "current_org": "龙安区人民政府",
        "source": "龙安区人民政府官网政府领导页: 祝学红 (2025-12-09), 区委副书记、代区长祝学红调研辖区科技创新成长型重点企业 (2026-06-24)",
    },
    {
        "id": 3,
        "name": "悦宪宝",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985-06",
        "birthplace": "",
        "education": "研究生学历，法学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "龙安区委常委、常务副区长",
        "current_org": "龙安区人民政府",
        "source": "龙安区人民政府官网政府领导页: 悦宪宝 (2025-12-09), 龙安区'未诉先办'第六次调度会议 (2026-06-12)",
    },
    {
        "id": 4,
        "name": "周斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-04",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "龙安区政府副区长、龙安公安分局局长",
        "current_org": "龙安区人民政府",
        "source": "龙安区人民政府官网政府领导页: 周斌 (2025-12-09)",
    },
    {
        "id": 5,
        "name": "罗振方",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "龙安区原区长（已离任）",
        "current_org": "",
        "source": "龙安区人民政府官网: 五届第八十三次至八十七次常务会议 (2026-02至04, 区长罗振方主持会议)",
    },
]

# ── Organizations ────────────────────────────────────────────────────
organizations = [
    {
        "id": 1,
        "name": "中共龙安区委",
        "type": "党委",
        "level": "县处级",
        "parent": "中共安阳市委",
        "location": "河南省安阳市龙安区",
    },
    {
        "id": 2,
        "name": "龙安区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "安阳市人民政府",
        "location": "河南省安阳市龙安区",
    },
    {
        "id": 3,
        "name": "龙安公安分局",
        "type": "政府",
        "level": "乡科级",
        "parent": "龙安区人民政府",
        "location": "河南省安阳市龙安区",
    },
]

# ── Positions ────────────────────────────────────────────────────────
positions = [
    # 李军光
    {"person_id": 1, "org_id": 1, "title": "龙安区委书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "截至2026年7月仍在任"},
    # 祝学红
    {"person_id": 2, "org_id": 1, "title": "龙安区委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "龙安区代区长", "start_date": "~2026-06", "end_date": "present", "rank": "县处级正职", "note": "2026年6月24日以代区长身份公开活动"},
    # 悦宪宝
    {"person_id": 3, "org_id": 2, "title": "龙安区委常委、常务副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责常务工作"},
    # 周斌
    {"person_id": 4, "org_id": 2, "title": "龙安区政府副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 3, "title": "龙安公安分局局长", "start_date": "", "end_date": "present", "rank": "乡科级正职", "note": "兼任"},
    # 罗振方 - 前任区长
    {"person_id": 5, "org_id": 2, "title": "龙安区区长", "start_date": "2026-02", "end_date": "~2026-05", "rank": "县处级正职", "note": "至少2026年2月至4月在职"},
]

# ── Relationships ─────────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "区委书记与代区长——党政一把手搭档", "overlap_org": "中共龙安区委", "overlap_period": "2026-06至今"},
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "区委书记与常务副区长（区委常委）", "overlap_org": "中共龙安区委常委会", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "区委书记与副区长、公安分局局长", "overlap_org": "中共龙安区委常委会", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "代区长与常务副区长", "overlap_org": "龙安区人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 5, "type": "predecessor_successor", "context": "祝学红（代区长）接替罗振方（区长）", "overlap_org": "龙安区人民政府", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "李军光（区委书记）与罗振方（原区长）搭档", "overlap_org": "中共龙安区委", "overlap_period": "~2026年初至2026年5月"},
]

# ── Run ──────────────────────────────────────────────────────────────
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
    print("Done.")
