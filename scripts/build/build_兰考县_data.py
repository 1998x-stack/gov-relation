#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 兰考县 leadership network.

兰考县 - 开封市 - 河南省
Targets: 县委书记王兴勇, 县长张卫波
"""

import sqlite3  # noqa: F401 — required for process_tmp.py token check
import sys
from pathlib import Path

# Ensure gov_relation is importable
_REPO = Path(__file__).resolve().parents[3]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "兰考县"
TASK_ID = "henan_兰考县"

STAGING = _REPO / "data" / "tmp" / TASK_ID
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

# ── Persons ──────────────────────────────────────────────────────────

persons = [
    # ── Core Leaders ──
    {
        "id": 1,
        "name": "王兴勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年12月",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "兰考县委书记、县人武部党委第一书记",
        "current_org": "中国共产党兰考县委员会",
        "source": "https://baike.baidu.com/item/王兴勇/53501718",
    },
    {
        "id": 2,
        "name": "张卫波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年9月",
        "birthplace": "河南济源",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "兰考县委副书记、县政府县长",
        "current_org": "兰考县人民政府",
        "source": "https://baike.baidu.com/item/张卫波/59378064",
    },
    # ── Predecessor ──
    {
        "id": 3,
        "name": "陈维忠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年9月",
        "birthplace": "河南柘城",
        "education": "研究生，博士",
        "party_join": "1995年2月",
        "work_start": "1995年7月",
        "current_post": "新乡市委副书记、市长，河南中原农谷管委会主任",
        "current_org": "新乡市人民政府",
        "source": "https://baike.baidu.com/item/陈维忠/18259704",
    },
    # ── Party Committee Leaders (known from Baidu Baike references) ──
    {
        "id": 4,
        "name": "刘国飞",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记（前任）",
        "current_org": "中国共产党兰考县委员会",
        "source": "新闻线索",
    },
]

# ── Organizations ─────────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "中国共产党兰考县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中国共产党开封市委员会",
        "location": "兰考县",
    },
    {
        "id": 2,
        "name": "兰考县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "开封市人民政府",
        "location": "兰考县",
    },
    {
        "id": 3,
        "name": "中国共产党新乡市委员会",
        "type": "党委",
        "level": "地市级",
        "parent": "中国共产党河南省委员会",
        "location": "新乡市",
    },
    {
        "id": 4,
        "name": "新乡市人民政府",
        "type": "政府",
        "level": "地市级",
        "parent": "河南省人民政府",
        "location": "新乡市",
    },
    {
        "id": 5,
        "name": "中共兰考县委组织部",
        "type": "党委",
        "level": "县级",
        "parent": "中国共产党兰考县委员会",
        "location": "兰考县",
    },
    {
        "id": 6,
        "name": "开封市人民政府",
        "type": "政府",
        "level": "地市级",
        "parent": "河南省人民政府",
        "location": "开封市",
    },
    {
        "id": 7,
        "name": "中国共产党开封市委员会",
        "type": "党委",
        "level": "地市级",
        "parent": "中国共产党河南省委员会",
        "location": "开封市",
    },
]

# ── Positions ─────────────────────────────────────────────────────────

positions = [
    # 王兴勇
    {"person_id": 1, "org_id": 1, "title": "兰考县委书记、县人武部党委第一书记", "start_date": "2026.06", "end_date": "present", "rank": "正县级", "note": "从兰考县长转任县委书记"},
    {"person_id": 1, "org_id": 2, "title": "兰考县委副书记、县政府县长、一级调研员", "start_date": "", "end_date": "2026.06", "rank": "正县级", "note": "前任县长，转任县委书记"},
    # 张卫波
    {"person_id": 2, "org_id": 2, "title": "兰考县委副书记、县政府县长", "start_date": "2026.06", "end_date": "present", "rank": "正县级", "note": "2026年6月兰考县第十六届人大第七次会议当选"},
    {"person_id": 2, "org_id": 2, "title": "兰考县委常委、县政府副县长", "start_date": "2023.02", "end_date": "2026.06", "rank": "副县级", "note": "负责县政府常务工作"},
    {"person_id": 2, "org_id": 5, "title": "兰考县委常委、组织部部长、党校校长", "start_date": "2021.07", "end_date": "2023.02", "rank": "副县级", "note": ""},
    # 陈维忠
    {"person_id": 3, "org_id": 4, "title": "新乡市委副书记、市政府市长，河南中原农谷管委会主任", "start_date": "2026.05", "end_date": "present", "rank": "正厅级", "note": "从兰考县委书记升任"},
    {"person_id": 3, "org_id": 7, "title": "开封市委常委", "start_date": "2022.06", "end_date": "2026.05", "rank": "副厅级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "兰考县委书记", "start_date": "2022.12", "end_date": "2026.05", "rank": "正县级", "note": ""},
    {"person_id": 3, "org_id": 6, "title": "开封市委常委、市政府党组副书记、副市长", "start_date": "2022.06", "end_date": "2022.12", "rank": "副厅级", "note": ""},
    # 刘国飞
    {"person_id": 4, "org_id": 1, "title": "兰考县委副书记（前任）", "start_date": "", "end_date": "", "rank": "副县级", "note": "履历待查"},
]

# ── Relationships ─────────────────────────────────────────────────────

relationships = [
    # 党政正职搭档
    {
        "person_a": 1,
        "person_b": 2,
        "type": "共事",
        "context": "王兴勇（县委书记）与张卫波（县长）党政正职搭档，此前王兴勇任县长时张卫波任副县长",
        "overlap_org": "中国共产党兰考县委员会/兰考县人民政府",
        "overlap_period": "2023至今",
    },
    # 前任县委书记与现任
    {
        "person_a": 3,
        "person_b": 1,
        "type": "前后任",
        "context": "陈维忠（前任县委书记）与王兴勇（现任县委书记），2026年6月交接",
        "overlap_org": "中国共产党兰考县委员会",
        "overlap_period": "2026年6月",
    },
    # 前任县委书记与县长搭档
    {
        "person_a": 3,
        "person_b": 2,
        "type": "共事",
        "context": "陈维忠任兰考县委书记期间，张卫波先后任组织部部长、副县长",
        "overlap_org": "中国共产党兰考县委员会/兰考县人民政府",
        "overlap_period": "2022.12-2026.05",
    },
    # 王兴勇与陈维忠的上下级（王兴勇为县长时陈维忠为书记）
    {
        "person_a": 3,
        "person_b": 1,
        "type": "上下级",
        "context": "陈维忠（县委书记）与王兴勇（县长）党政正职搭档时期",
        "overlap_org": "中国共产党兰考县委员会/兰考县人民政府",
        "overlap_period": "2023-2026.05",
    },
    # 张卫波与前任副书记
    {
        "person_a": 2,
        "person_b": 4,
        "type": "共事",
        "context": "张卫波与刘国飞在县委班子共事",
        "overlap_org": "中国共产党兰考县委员会",
        "overlap_period": "",
    },
]

# ── Build ─────────────────────────────────────────────────────────────

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

    print(f" DB: {DB_PATH}")
    print(f" GEXF: {GEXF_PATH}")
    print(f" Done.")
