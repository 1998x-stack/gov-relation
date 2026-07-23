#!/usr/bin/env python3
"""Build script for 容县 (Rong County, Yulin, Guangxi) leadership network.

Generated: 2026-07-23
Level: 县
Province: 广西壮族自治区
Parent City: 玉林市
Targets: 县委书记 & 县长

Research Notes:
  Current Party Secretary: 吴厚强 (来源: 百度百科容县词条, 2026年7月更新)
  Current Acting County Mayor: 李金星 (县政府党组书记、代理县长, 来源: 百度百科容县词条)
  Current 人大主任: 杨家贵 (来源: 百度百科容县词条)
  Current 政协主席: 刘崇泽 (来源: 百度百科容县词条)

  Previous Party Secretary: 甘文波 (2025前, 后调玉林市)
  Previous County Mayor: 吴厚强 (升任书记前)

  GAPS:
  - 吴厚强：完整简历（教育背景、出生年月、籍贯、早期履历）待查
  - 李金星：从何处调任/升任、完整履历待查
  - 杨家贵：完整履历待查
  - 刘崇泽：完整履历待查
  - 容县县委常委班子其他成员待查
  - 前任书记甘文波去向及容县具体任期待核实
  - 吴厚强任县长后何时、由谁接任县长至李金星代理的过渡期待查

Sources:
  - https://baike.baidu.com/item/容县 (容县百度百科词条，含2026年7月主要领导列表)
"""

import sqlite3  # noqa: used by gov_relation.runner

from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
from gov_relation.runner import run_build

# ═══════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════

# fmt: off
PERSONS = [
    # ── Core Leaders ──
    {
        "id": 1,
        "name": "吴厚强",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共容县委员会",
        "source": "https://baike.baidu.com/item/容县",
    },
    {
        "id": 2,
        "name": "李金星",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府党组书记、代理县长",
        "current_org": "容县人民政府",
        "source": "https://baike.baidu.com/item/容县",
    },
    {
        "id": 3,
        "name": "杨家贵",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "容县人大常委会",
        "source": "https://baike.baidu.com/item/容县",
    },
    {
        "id": 4,
        "name": "刘崇泽",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "中国人民政治协商会议容县委员会",
        "source": "https://baike.baidu.com/item/容县",
    },
    # ── Previous Leaders (limited info) ──
    {
        "id": 5,
        "name": "甘文波",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "https://baike.baidu.com/item/甘文波",
    },
]

ORGANIZATIONS = [
    {
        "id": 1,
        "name": "中国共产党容县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共玉林市委员会",
        "location": "容县",
    },
    {
        "id": 2,
        "name": "容县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "玉林市人民政府",
        "location": "容县",
    },
    {
        "id": 3,
        "name": "容县人大常委会",
        "type": "人大",
        "level": "县",
        "parent": "玉林市人大常委会",
        "location": "容县",
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议容县委员会",
        "type": "政协",
        "level": "县",
        "parent": "玉林市政协",
        "location": "容县",
    },
    {
        "id": 5,
        "name": "中共玉林市委员会",
        "type": "党委",
        "level": "地级",
        "parent": "中共广西壮族自治区委员会",
        "location": "玉林市",
    },
    {
        "id": 6,
        "name": "玉林市人民政府",
        "type": "政府",
        "level": "地级",
        "parent": "广西壮族自治区人民政府",
        "location": "玉林市",
    },
]

POSITIONS = [
    # 吴厚强
    {"person_id": 1, "org_id": 1, "title": "容县县委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "当前职务（2026年7月据百度百科确认在任）"},
    # 李金星
    {"person_id": 2, "org_id": 2, "title": "容县政府党组书记、代理县长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "代理县长，当前职务"},
    # 杨家贵
    {"person_id": 3, "org_id": 3, "title": "容县人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": "当前职务"},
    # 刘崇泽
    {"person_id": 4, "org_id": 4, "title": "容县政协主席", "start_date": "", "end_date": "present", "rank": "正处级", "note": "当前职务"},
]

RELATIONSHIPS = [
    # 吴厚强—李金星：书记-代县长搭档
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "县委书记与代县长党政一把手搭档", "overlap_org": "容县四家班子", "overlap_period": ""},
    # 吴厚强—杨家贵：书记-人大主任
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "县委与县人大领导共事", "overlap_org": "容县四家班子", "overlap_period": ""},
    # 吴厚强—刘崇泽：书记-政协主席
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "县委与县政协领导共事", "overlap_org": "容县四家班子", "overlap_period": ""},
]

# fmt: on

# ═══════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════

DB_PATH = DATABASE_DIR / "容县_network.db"
GEXF_PATH = GRAPH_DIR / "容县_network.gexf"


def main() -> None:
    run_build(
        slug="容县",
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )


if __name__ == "__main__":
    main()
