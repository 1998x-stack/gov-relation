#!/usr/bin/env python3
"""Build 集安市 leadership network database and GEXF graph.

Data sources:
- 集安市人民政府网站 (jilinja.gov.cn) — official leader bios
- 通化市人民政府网站 (tonghua.gov.cn) — appointment news
- 集安市融媒体中心 articles
"""

import sys
from pathlib import Path
import sqlite3  # noqa: F401 — used by gov_relation.runner; kept for process_tmp.py validation

_HERE = Path(__file__).resolve().parent
_REPO = _HERE.parents[2]
sys.path.insert(0, str(_REPO))

from gov_relation.runner import run_build

SLUG = "集安市"
DB_PATH = _HERE / "集安市_network.db"
GEXF_PATH = _HERE / "集安市_network.gexf"

# ── Persons ─────────────────────────────────────────────────────────
# IDs: 1-9 for current leadership
PERSONS = [
    # === Core Leaders ===
    {
        "id": 1,
        "name": "吴红亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "集安市委书记",
        "current_org": "中共集安市委",
        "source": "集安市人民政府网站，市委常委会会议报道 (2026-05,06,07)",
    },
    {
        "id": 2,
        "name": "高霞",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1980-10",
        "birthplace": "",
        "education": "研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "集安市委副书记、市长",
        "current_org": "集安市人民政府",
        "source": "集安市人民政府网站领导之窗",
    },
    # === Government Leadership Team ===
    {
        "id": 3,
        "name": "王玉文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-06",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "集安市委常委、副市长",
        "current_org": "集安市人民政府",
        "source": "集安市人民政府网站领导之窗",
    },
    {
        "id": 4,
        "name": "吕伟鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983-11",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "集安市委常委、副市长（挂职）",
        "current_org": "集安市人民政府",
        "source": "集安市人民政府网站领导之窗",
    },
    {
        "id": 5,
        "name": "吴玲斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-08",
        "birthplace": "",
        "education": "研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "集安市委常委、副市长（挂职）",
        "current_org": "集安市人民政府",
        "source": "集安市人民政府网站领导之窗",
    },
    {
        "id": 6,
        "name": "张立军",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "1972-05",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "集安市副市长、市公安局党委书记、局长、督察长",
        "current_org": "集安市公安局",
        "source": "集安市人民政府网站领导之窗",
    },
    {
        "id": 7,
        "name": "隗英辉",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1984-04",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "集安市政府副市长",
        "current_org": "集安市人民政府",
        "source": "集安市人民政府网站领导之窗",
    },
    {
        "id": 8,
        "name": "徐薇翔",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1989-12",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "集安市政府副市长",
        "current_org": "集安市人民政府",
        "source": "集安市人民政府网站领导之窗",
    },
    {
        "id": 9,
        "name": "王超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986-11",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "集安市政府副市长",
        "current_org": "集安市人民政府",
        "source": "集安市人民政府网站领导之窗",
    },
    {
        "id": 10,
        "name": "魏国勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-12",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "集安市政府副市长、市住房和城乡建设局党组书记、局长",
        "current_org": "集安市住房和城乡建设局",
        "source": "集安市人民政府网站领导之窗",
    },
]

# ── Organizations ───────────────────────────────────────────────────
ORGANIZATIONS = [
    {"id": 1, "name": "中共集安市委", "type": "党委", "level": "县级", "parent": "中共通化市委", "location": "集安市"},
    {"id": 2, "name": "集安市人民政府", "type": "政府", "level": "县级", "parent": "通化市人民政府", "location": "集安市"},
    {"id": 3, "name": "集安市公安局", "type": "政府", "level": "正科级", "parent": "集安市人民政府", "location": "集安市"},
    {"id": 4, "name": "集安市住房和城乡建设局", "type": "政府", "level": "正科级", "parent": "集安市人民政府", "location": "集安市"},
    {"id": 5, "name": "中共通化市委", "type": "党委", "level": "地市级", "parent": "中共吉林省委", "location": "通化市"},
    {"id": 6, "name": "通化市人民政府", "type": "政府", "level": "地市级", "parent": "吉林省人民政府", "location": "通化市"},
]

# ── Positions ───────────────────────────────────────────────────────
POSITIONS = [
    # 吴红亮
    {"person_id": 1, "org_id": 1, "title": "集安市委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 高霞
    {"person_id": 2, "org_id": 1, "title": "集安市委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "集安市人民政府党组书记、市长", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 王玉文
    {"person_id": 3, "org_id": 1, "title": "集安市委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "集安市副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 吕伟鹏（挂职）
    {"person_id": 4, "org_id": 1, "title": "集安市委常委（挂职）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "挂职"},
    {"person_id": 4, "org_id": 2, "title": "集安市副市长（挂职）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "挂职"},
    # 吴玲斌（挂职）
    {"person_id": 5, "org_id": 1, "title": "集安市委常委（挂职）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "挂职"},
    {"person_id": 5, "org_id": 2, "title": "集安市副市长（挂职）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "挂职"},
    # 张立军
    {"person_id": 6, "org_id": 3, "title": "集安市公安局党委书记、局长、督察长", "start_date": "", "end_date": "present", "rank": "正科级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "集安市副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 隗英辉
    {"person_id": 7, "org_id": 2, "title": "集安市政府副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 徐薇翔
    {"person_id": 8, "org_id": 2, "title": "集安市政府副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 王超
    {"person_id": 9, "org_id": 2, "title": "集安市政府副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 魏国勇
    {"person_id": 10, "org_id": 2, "title": "集安市政府副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 4, "title": "集安市住房和城乡建设局党组书记、局长", "start_date": "", "end_date": "present", "rank": "正科级", "note": ""},
]

# ── Relationships ────────────────────────────────────────────────────
# Edges represent confirmed work relationships from government leadership structure
RELATIONSHIPS = [
    # 吴红亮 ↔ 高霞（党政一把手）
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "集安市委书记与市长", "overlap_org": "中共集安市委/集安市人民政府", "overlap_period": "2024-2026"},
    # 吴红亮 ↔ 王玉文（常委副市长）
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "市委书记与市委常委、副市长", "overlap_org": "中共集安市委", "overlap_period": ""},
    # 吴红亮 ↔ 吕伟鹏（挂职常委）
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "市委书记与挂职常委", "overlap_org": "中共集安市委", "overlap_period": ""},
    # 吴红亮 ↔ 吴玲斌（挂职常委）
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "市委书记与挂职常委", "overlap_org": "中共集安市委", "overlap_period": ""},
    # 高霞 ↔ 王玉文（市长与常务口副市长）
    {"person_a": 2, "person_b": 3, "type": "上下级", "context": "市长与市委常委、副市长（常务）", "overlap_org": "集安市人民政府", "overlap_period": ""},
    # 高霞 ↔ 吕伟鹏
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "市长与挂职副市长", "overlap_org": "集安市人民政府", "overlap_period": ""},
    # 高霞 ↔ 吴玲斌
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "市长与挂职副市长", "overlap_org": "集安市人民政府", "overlap_period": ""},
    # 高霞 ↔ 张立军
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "市长与副市长、公安局长", "overlap_org": "集安市人民政府", "overlap_period": ""},
    # 高霞 ↔ 隗英辉
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "市长与副市长", "overlap_org": "集安市人民政府", "overlap_period": ""},
    # 高霞 ↔ 徐薇翔
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "市长与副市长", "overlap_org": "集安市人民政府", "overlap_period": ""},
    # 高霞 ↔ 王超
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "市长与副市长", "overlap_org": "集安市人民政府", "overlap_period": ""},
    # 高霞 ↔ 魏国勇
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "市长与副市长", "overlap_org": "集安市人民政府", "overlap_period": ""},
    # 王玉文 ↔ 吴玲斌（对口合作协管关系）
    {"person_a": 3, "person_b": 5, "type": "协作", "context": "吴玲斌协助王玉文负责对口合作工作", "overlap_org": "集安市人民政府", "overlap_period": ""},
    # 王超 ↔ 吴玲斌（边境村建设协管关系）
    {"person_a": 9, "person_b": 5, "type": "协作", "context": "吴玲斌协助王超负责边境村建设工作", "overlap_org": "集安市人民政府", "overlap_period": ""},
]


def main() -> None:
    run_build(
        slug=SLUG,
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print("✅ 集安市 network build complete.")
    print(f"   DB:   {DB_PATH}")
    print(f"   GEXF: {GEXF_PATH}")


if __name__ == "__main__":
    main()
