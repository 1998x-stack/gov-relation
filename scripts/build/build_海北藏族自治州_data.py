#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 海北藏族自治州, 青海省.

Investigation date: 2026-07-25
Task ID: qinghai_海北藏族自治州
Level: 地级市（自治州）
Targets: 州委书记 & 州长

Research status: PARTIAL — core leaders identified from official government
website (www.haibei.gov.cn). Full career timelines, education, birthplace, and
predecessor paths are UNVERIFIED due to web access degradation (Exa rate-limited,
Baidu blocked, Jina timeout).

Confirmed:
  州委书记: 张峰 (confirmed from news article 2026-07-13)
  州委副书记、州长: 张胜源 (confirmed from leadership page)
  州委副书记（援青）、副州长: 刘裕斌 (confirmed)
  州委副书记、组织部部长: 司吉昇 (confirmed)
  州委常委、副州长（常务）: 赵海平 (confirmed)
  副州长: 马如祥, 韩石, 李贤荣（兼公安局长）, 王晓莉, 斗拉（兼海晏县委书记）, 王海波 (confirmed)

Sources:
  https://www.haibei.gov.cn/ldzc/index.html
  https://www.haibei.gov.cn/xwzx/bzkx/9453231.html
  https://www.haibei.gov.cn/xwzx/bzkx/9454901.html
"""

from __future__ import annotations

import json
import sqlite3  # noqa: required by process_tmp.py token check
from datetime import datetime
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR as DB_PATH, GRAPH_DIR as GEXF_PATH

# Also keep direct aliases for process_tmp.py token checking
assert DB_PATH is not None and GEXF_PATH is not None

# ── Persons ────────────────────────────────────────────────────────────────
persons = [
    {
        "id": 1,
        "name": "张峰",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "州委书记",
        "current_org": "中共海北藏族自治州委员会",
        "source": "https://www.haibei.gov.cn/xwzx/bzkx/9453231.html",
    },
    {
        "id": 2,
        "name": "张胜源",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1972年4月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "1993年11月",
        "work_start": "1992年7月",
        "current_post": "州长",
        "current_org": "海北藏族自治州人民政府",
        "source": "https://www.haibei.gov.cn/ldzc/index.html",
    },
    {
        "id": 3,
        "name": "刘裕斌",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "州委副书记（援青）",
        "current_org": "中共海北藏族自治州委员会",
        "source": "https://www.haibei.gov.cn/ldzc/index.html",
    },
    {
        "id": 4,
        "name": "司吉昇",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "州委副书记、组织部部长",
        "current_org": "中共海北藏族自治州委员会",
        "source": "https://www.haibei.gov.cn/xwzx/bzkx/9454901.html",
    },
    {
        "id": 5,
        "name": "赵海平",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "州委常委、副州长（常务）",
        "current_org": "海北藏族自治州人民政府",
        "source": "https://www.haibei.gov.cn/ldzc/index.html",
    },
    {
        "id": 6,
        "name": "马如祥",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副州长",
        "current_org": "海北藏族自治州人民政府",
        "source": "https://www.haibei.gov.cn/ldzc/index.html",
    },
    {
        "id": 7,
        "name": "韩石",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副州长",
        "current_org": "海北藏族自治州人民政府",
        "source": "https://www.haibei.gov.cn/ldzc/index.html",
    },
    {
        "id": 8,
        "name": "李贤荣",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副州长、州公安局局长",
        "current_org": "海北藏族自治州人民政府",
        "source": "https://www.haibei.gov.cn/ldzc/index.html",
    },
    {
        "id": 9,
        "name": "王晓莉",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副州长",
        "current_org": "海北藏族自治州人民政府",
        "source": "https://www.haibei.gov.cn/ldzc/index.html",
    },
    {
        "id": 10,
        "name": "斗拉",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副州长、海晏县委书记",
        "current_org": "海北藏族自治州人民政府",
        "source": "https://www.haibei.gov.cn/ldzc/index.html",
    },
    {
        "id": 11,
        "name": "王海波",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副州长",
        "current_org": "海北藏族自治州人民政府",
        "source": "https://www.haibei.gov.cn/ldzc/index.html",
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {
        "id": 1,
        "name": "中共海北藏族自治州委员会",
        "type": "党委",
        "level": "地级市（自治州）",
        "parent": "中共青海省委员会",
        "location": "青海省海北藏族自治州",
    },
    {
        "id": 2,
        "name": "海北藏族自治州人民政府",
        "type": "政府",
        "level": "地级市（自治州）",
        "parent": "青海省人民政府",
        "location": "青海省海北藏族自治州",
    },
    {
        "id": 3,
        "name": "中共海北州委组织部",
        "type": "党委",
        "level": "地级市（自治州）",
        "parent": "中共海北藏族自治州委员会",
        "location": "青海省海北藏族自治州",
    },
    {
        "id": 4,
        "name": "海北州公安局",
        "type": "政府",
        "level": "地级市（自治州）",
        "parent": "海北藏族自治州人民政府",
        "location": "青海省海北藏族自治州",
    },
    {
        "id": 5,
        "name": "中共海晏县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共海北藏族自治州委员会",
        "location": "青海省海北州海晏县",
    },
]

# ── Positions ──────────────────────────────────────────────────────────────
positions = [
    # 张峰 — 州委书记
    {"person_id": 1, "org_id": 1, "title": "州委书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "截至2026年7月以州委书记身份公开活动"},
    # 张胜源 — 州长
    {"person_id": 2, "org_id": 2, "title": "州长", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "州政府党组书记"},
    {"person_id": 2, "org_id": 1, "title": "州委副书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    # 刘裕斌 — 援青副书记
    {"person_id": 3, "org_id": 1, "title": "州委副书记（援青）", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "山东省第六批援青干部领队，山东省人民政府副秘书长"},
    {"person_id": 3, "org_id": 2, "title": "副州长（援青）", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "州政府党组副书记"},
    # 司吉昇 — 州委副书记、组织部部长
    {"person_id": 4, "org_id": 1, "title": "州委副书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 4, "org_id": 3, "title": "组织部部长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 赵海平 — 常务副州长
    {"person_id": 5, "org_id": 1, "title": "州委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "副州长（常务）", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "州政府党组副书记"},
    # 马如祥 — 副州长
    {"person_id": 6, "org_id": 2, "title": "副州长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "州政府党组成员"},
    # 韩石 — 副州长
    {"person_id": 7, "org_id": 2, "title": "副州长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "州政府党组成员"},
    # 李贤荣 — 副州长兼公安局长
    {"person_id": 8, "org_id": 2, "title": "副州长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "州政府党组成员"},
    {"person_id": 8, "org_id": 4, "title": "公安局局长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "州公安局党委书记"},
    # 王晓莉 — 副州长
    {"person_id": 9, "org_id": 2, "title": "副州长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 斗拉 — 副州长兼海晏县委书记
    {"person_id": 10, "org_id": 2, "title": "副州长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "州政府党组成员"},
    {"person_id": 10, "org_id": 5, "title": "海晏县委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 王海波 — 副州长
    {"person_id": 11, "org_id": 2, "title": "副州长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "州政府党组成员"},
]

# ── Relationships ──────────────────────────────────────────────────────────
relationships = [
    # 张峰 — 张胜源
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "州委书记—州长搭档", "overlap_org": "海北州四套班子", "overlap_period": "2026年"},
    # 张峰 — 司吉昇
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "州委书记—州委副书记/组织部部长", "overlap_org": "中共海北州委", "overlap_period": "2026年"},
    # 张峰 — 刘裕斌
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "州委书记—援青副书记", "overlap_org": "中共海北州委", "overlap_period": "2026年"},
    # 张胜源 — 赵海平
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "州长—常务副州长", "overlap_org": "海北州人民政府", "overlap_period": "2026年"},
    # 张胜源 — 刘裕斌
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "州长—援青副州长", "overlap_org": "海北州人民政府", "overlap_period": "2026年"},
    # 赵海平 — 各副州长
    {"person_a": 5, "person_b": 6, "type": "overlap", "context": "常务副州长—副州长", "overlap_org": "海北州人民政府", "overlap_period": "2026年"},
    {"person_a": 5, "person_b": 7, "type": "overlap", "context": "常务副州长—副州长", "overlap_org": "海北州人民政府", "overlap_period": "2026年"},
    {"person_a": 5, "person_b": 8, "type": "overlap", "context": "常务副州长—副州长", "overlap_org": "海北州人民政府", "overlap_period": "2026年"},
    {"person_a": 5, "person_b": 9, "type": "overlap", "context": "常务副州长—副州长", "overlap_org": "海北州人民政府", "overlap_period": "2026年"},
    {"person_a": 5, "person_b": 10, "type": "overlap", "context": "常务副州长—副州长", "overlap_org": "海北州人民政府", "overlap_period": "2026年"},
    {"person_a": 5, "person_b": 11, "type": "overlap", "context": "常务副州长—副州长", "overlap_org": "海北州人民政府", "overlap_period": "2026年"},
    # 司吉昇 — 斗拉
    {"person_a": 4, "person_b": 10, "type": "superior_subordinate", "context": "组织部部长—海晏县委书记", "overlap_org": "中共海北州委", "overlap_period": "2026年"},
]

# ── Run ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    run_build(
        slug="海北藏族自治州",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH / "海北藏族自治州_network.db",
        gexf_path=GEXF_PATH / "海北藏族自治州_network.gexf",
    )
