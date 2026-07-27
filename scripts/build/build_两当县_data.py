#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
两当县 (甘肃省陇南市) 领导班子工作关系网络数据构建脚本
Generate SQLite database + GEXF graph for Liangdang County leadership network.

Level: 县
Province: 甘肃省
City: 陇南市
Region: 两当县
Targets: 县委书记 & 县长

Research Sources:
- 两当县人民政府官方网站 (liangdang.gov.cn) — 网站不可达（2026-07-22确认）
- 陇南市人民政府官方网站 (longnan.gov.cn) 领导之窗
- 该县数据存在大量待填充项，详见open_gaps.md

Research Date: 2026-07-22
"""

import os
import sys
from pathlib import Path

# Add project root to path for gov_relation imports
_REPO_ROOT = Path(__file__).resolve()
for _parent in [_REPO_ROOT] + list(_REPO_ROOT.parents):
    if (_parent / "gov_relation" / "__init__.py").exists():
        _REPO_ROOT = _parent
        break
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
import sqlite3  # used by the runner internally; kept here for process_tmp.py validation

STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, "两当县_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "两当县_network.gexf")

# ═══════════════════════════════════════════════
# 人员数据
# ═══════════════════════════════════════════════
#
# 注意：以下数据在 2026-07-22 调研时，两当县政府网站 (liangdang.gov.cn) 不可达，
# 陇南市层面亦无法查到完整的现任领导班子名单。
# 以下人员信息为基于公开渠道和已知事实的部分推断，需要实地或高级搜索验证。
# 所有缺失信息均标记为待查。
# ═══════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # 县委主要领导（身份待验证）
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共两当县委员会",
        "source": "待查 — 两当县政府网站不可达（liangdang.gov.cn）",
    },
    {
        "id": 2,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "两当县人民政府",
        "source": "待查 — 两当县政府网站不可达（liangdang.gov.cn）",
    },
    # ════════════════════════════════════════
    # 县委副书记
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共两当县委员会",
        "source": "待查",
    },
    # ════════════════════════════════════════
    # 县委常委
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "两当县人民政府",
        "source": "待查",
    },
    {
        "id": 5,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共两当县委员会组织部",
        "source": "待查",
    },
    {
        "id": 6,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县纪委书记、县监委主任",
        "current_org": "中共两当县纪律检查委员会/两当县监察委员会",
        "source": "待查",
    },
    {
        "id": 7,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共两当县委员会政法委员会",
        "source": "待查",
    },
    {
        "id": 8,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共两当县委员会宣传部",
        "source": "待查",
    },
    {
        "id": 9,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、统战部部长",
        "current_org": "中共两当县委员会统战部",
        "source": "待查",
    },
    {
        "id": 10,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、人武部政委",
        "current_org": "两当县人民武装部",
        "source": "待查",
    },
    # ════════════════════════════════════════
    # 县政府副县长
    # ════════════════════════════════════════
    {
        "id": 11,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长、县公安局局长",
        "current_org": "两当县人民政府/两当县公安局",
        "source": "待查",
    },
    {
        "id": 12,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "两当县人民政府",
        "source": "待查",
    },
    {
        "id": 13,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "两当县人民政府",
        "source": "待查",
    },
    {
        "id": 14,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "两当县人民政府",
        "source": "待查",
    },
    {
        "id": 15,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "两当县人民政府",
        "source": "待查",
    },
]

# ═══════════════════════════════════════════════
# 组织数据
# ═══════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共两当县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共陇南市委员会",
        "location": "甘肃省陇南市两当县",
    },
    {
        "id": 2,
        "name": "中共两当县委员会组织部",
        "type": "党委",
        "level": "县级",
        "parent": "中共两当县委员会",
        "location": "甘肃省陇南市两当县",
    },
    {
        "id": 3,
        "name": "中共两当县委员会宣传部",
        "type": "党委",
        "level": "县级",
        "parent": "中共两当县委员会",
        "location": "甘肃省陇南市两当县",
    },
    {
        "id": 4,
        "name": "中共两当县委员会政法委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共两当县委员会",
        "location": "甘肃省陇南市两当县",
    },
    {
        "id": 5,
        "name": "中共两当县委员会统战部",
        "type": "党委",
        "level": "县级",
        "parent": "中共两当县委员会",
        "location": "甘肃省陇南市两当县",
    },
    {
        "id": 6,
        "name": "两当县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "陇南市人民政府",
        "location": "甘肃省陇南市两当县",
    },
    {
        "id": 7,
        "name": "中共两当县纪律检查委员会",
        "type": "纪委",
        "level": "县级",
        "parent": "中共两当县委员会",
        "location": "甘肃省陇南市两当县",
    },
    {
        "id": 8,
        "name": "两当县监察委员会",
        "type": "监察",
        "level": "县级",
        "parent": "中共两当县委员会",
        "location": "甘肃省陇南市两当县",
    },
    {
        "id": 9,
        "name": "两当县人民武装部",
        "type": "政府",
        "level": "县级",
        "parent": "两当县人民政府",
        "location": "甘肃省陇南市两当县",
    },
    {
        "id": 10,
        "name": "两当县公安局",
        "type": "政府",
        "level": "县级",
        "parent": "两当县人民政府",
        "location": "甘肃省陇南市两当县",
    },
]

# ═══════════════════════════════════════════════
# 任职数据
# ═══════════════════════════════════════════════

positions = [
    # 县委书记
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "present", "rank": "正县级", "note": "主持县委全面工作"},
    # 县长
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 2, "org_id": 6, "title": "县长", "start_date": "", "end_date": "present", "rank": "正县级", "note": "主持县政府全面工作"},
    # 专职副书记
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 常务副县长
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 4, "org_id": 6, "title": "常务副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "协助县长负责县政府日常工作"},
    # 组织部部长
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "组织部部长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 纪委书记
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 6, "org_id": 7, "title": "县纪委书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 6, "org_id": 8, "title": "县监委主任", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 政法委书记
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 7, "org_id": 4, "title": "政法委书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 宣传部部长
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 8, "org_id": 3, "title": "宣传部部长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 统战部部长
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 9, "org_id": 5, "title": "统战部部长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 人武部政委
    {"person_id": 10, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 10, "org_id": 9, "title": "人武部政委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 副县长/公安局长
    {"person_id": 11, "org_id": 6, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 11, "org_id": 10, "title": "县公安局局长", "start_date": "", "end_date": "present", "rank": "正科级", "note": ""},
    # 副县长
    {"person_id": 12, "org_id": 6, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 13, "org_id": 6, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 14, "org_id": 6, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 15, "org_id": 6, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
]

# ═══════════════════════════════════════════════
# 关系数据
# ═══════════════════════════════════════════════
#
# 所有关系暂以县级领导班子结构推断，待确认具体人名后完善。
# ═══════════════════════════════════════════════

relationships = [
    # 县委书记 — 县委常委班子成员
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "县委书记—县长搭档", "overlap_org": "中共两当县委员会", "overlap_period": "待查—"},
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "县委书记—专职副书记", "overlap_org": "中共两当县委员会", "overlap_period": "待查—"},
    {"person_a": 1, "person_b": 4, "type": "共事", "context": "县委书记—常务副县长", "overlap_org": "中共两当县委员会/两当县人民政府", "overlap_period": "待查—"},
    {"person_a": 1, "person_b": 5, "type": "共事", "context": "县委书记—组织部部长", "overlap_org": "中共两当县委员会", "overlap_period": "待查—"},
    {"person_a": 1, "person_b": 6, "type": "监督", "context": "县委书记—纪委书记（同级监督）", "overlap_org": "中共两当县委员会", "overlap_period": "待查—"},
    {"person_a": 1, "person_b": 7, "type": "共事", "context": "县委书记—政法委书记", "overlap_org": "中共两当县委员会", "overlap_period": "待查—"},
    {"person_a": 1, "person_b": 8, "type": "共事", "context": "县委书记—宣传部部长", "overlap_org": "中共两当县委员会", "overlap_period": "待查—"},
    {"person_a": 1, "person_b": 9, "type": "共事", "context": "县委书记—统战部部长", "overlap_org": "中共两当县委员会", "overlap_period": "待查—"},
    # 县长与班子成员
    {"person_a": 2, "person_b": 4, "type": "共事", "context": "县长—常务副县长", "overlap_org": "两当县人民政府", "overlap_period": "待查—"},
    {"person_a": 2, "person_b": 11, "type": "共事", "context": "县长—副县长/公安局长", "overlap_org": "两当县人民政府", "overlap_period": "待查—"},
    {"person_a": 2, "person_b": 12, "type": "共事", "context": "县长—副县长", "overlap_org": "两当县人民政府", "overlap_period": "待查—"},
    {"person_a": 2, "person_b": 13, "type": "共事", "context": "县长—副县长", "overlap_org": "两当县人民政府", "overlap_period": "待查—"},
    {"person_a": 2, "person_b": 14, "type": "共事", "context": "县长—副县长", "overlap_org": "两当县人民政府", "overlap_period": "待查—"},
    {"person_a": 2, "person_b": 15, "type": "共事", "context": "县长—副县长", "overlap_org": "两当县人民政府", "overlap_period": "待查—"},
    # 常务副县长与副县长
    {"person_a": 4, "person_b": 11, "type": "共事", "context": "常务副县长—副县长/公安局长", "overlap_org": "两当县人民政府", "overlap_period": "待查—"},
    {"person_a": 4, "person_b": 12, "type": "共事", "context": "常务副县长—副县长", "overlap_org": "两当县人民政府", "overlap_period": "待查—"},
    {"person_a": 4, "person_b": 13, "type": "共事", "context": "常务副县长—副县长", "overlap_org": "两当县人民政府", "overlap_period": "待查—"},
    {"person_a": 4, "person_b": 14, "type": "共事", "context": "常务副县长—副县长", "overlap_org": "两当县人民政府", "overlap_period": "待查—"},
    {"person_a": 4, "person_b": 15, "type": "共事", "context": "常务副县长—副县长", "overlap_org": "两当县人民政府", "overlap_period": "待查—"},
    # 政法委书记与公安局长
    {"person_a": 7, "person_b": 11, "type": "领导关系", "context": "政法委书记—公安局长", "overlap_org": "两当县政法系统", "overlap_period": "待查—"},
    # 专职副书记与县委常委
    {"person_a": 3, "person_b": 4, "type": "共事", "context": "专职副书记—常务副县长", "overlap_org": "中共两当县委员会/两当县人民政府", "overlap_period": "待查—"},
    {"person_a": 3, "person_b": 5, "type": "共事", "context": "专职副书记—组织部部长", "overlap_org": "中共两当县委员会", "overlap_period": "待查—"},
]

# ═══════════════════════════════════════════════
# 执行构建
# ═══════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("两当县（甘肃省陇南市）领导班子工作关系网络数据构建")
    print("=" * 60)
    print()
    print("注意：2026-07-22 调研时两当县政府网站不可达 (liangdang.gov.cn)，")
    print("所有现任领导姓名均为待查，仅以县级标准编制模板填充。")
    print("详见 report/open_gaps.md 和 report/20260722-两当县领导班子调研报告.md")
    print()

    run_build(
        slug="两当县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    print()
    print("=" * 60)
    print(f"Database: {DB_PATH}")
    print(f"GEXF:     {GEXF_PATH}")
    print("=" * 60)
    print()
    print("⚠ 重要提示：本数据库中的15位人员姓名均为'（待查）'，")
    print("   待两当县政府网站恢复访问或通过其他渠道获取现任领导名单后，")
    print("   需要更新本脚本并重新生成数据库和图文件。")
