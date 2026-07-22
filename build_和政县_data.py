#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
和政县 (甘肃省临夏回族自治州) 领导班子工作关系网络数据构建脚本
Generate SQLite database + GEXF graph for Hezheng County leadership network.

Level: 县
Province: 甘肃省
City: 临夏回族自治州
Region: 和政县
Targets: 县委书记 & 县长

Research Sources:
- 和政县人民政府官方网站 (www.hezheng.gov.cn) — 可访问 (2026-07-22)
- 网站政务要闻、工作动态、人事信息栏目
- 公开媒体报道

Research Notes:
- 和政县人民政府网站可正常访问，提供了大量2026年政务活动信息
- 领导之窗(ldzc)页面路径不可达，主要领导人信息通过新闻活动报道确认
- 县委书记冯祥安、县长赵斌的职务通过多篇正式新闻报道交叉确认
- 两位核心领导的完整个人简历(出生年月、教育背景、早期工作经历)未能从公开渠道获取
- 其他县委常委及副县长的名单通过人事任免通知和政务活动报道推断

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
DB_PATH = os.path.join(STAGING_DIR, "和政县_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "和政县_network.gexf")

# ═══════════════════════════════════════════════
# 人员数据
# ═══════════════════════════════════════════════
#
# CONFIDENCE NOTE:
# 县委书记冯祥安、县长赵斌职务已通过官方政务新闻交叉确认。
# 其他领导成员主要根据政务活动中出现频率推断，部分人员职务和分管领域待官方确认。
# 所有人员的出生年月、教育背景、早期履历均未能从公开渠道获取完整信息。
#
# ═══════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # 县委主要领导 (Top Leaders)
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "冯祥安",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共和政县委员会",
        "source": "和政县人民政府官方网站政务要闻确认；冯祥安多次主持召开县委常委会会议（2026年7月）",
    },
    {
        "id": 2,
        "name": "赵斌",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "和政县人民政府",
        "source": "和政县人民政府官方网站确认；赵斌以县委副书记、县长身份主持召开县政府常务会议（2026年7月）",
    },
    # ════════════════════════════════════════
    # 县委副书记 (Deputy Party Secretary)
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "（副书记待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记（专职）",
        "current_org": "中共和政县委员会",
        "source": "公开信息未明确；和政县新闻中专职副书记信息不足",
    },
    # ════════════════════════════════════════
    # 县委常委 (Standing Committee Members)
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "（常务副县长待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "和政县人民政府",
        "source": "公开信息未明确；待官方领导分工栏目确认",
    },
    {
        "id": 5,
        "name": "（纪委书记待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县纪委书记",
        "current_org": "中共和政县纪律检查委员会",
        "source": "公开信息未明确；待官方确认",
    },
    {
        "id": 6,
        "name": "（组织部长待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共和政县委员会组织部",
        "source": "公开信息未明确；待官方确认",
    },
    {
        "id": 7,
        "name": "（宣传部长待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共和政县委员会宣传部",
        "source": "公开信息未明确；待官方确认",
    },
    {
        "id": 8,
        "name": "（统战部长待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、统战部部长",
        "current_org": "中共和政县委员会统战部",
        "source": "公开信息未明确；待官方确认",
    },
    {
        "id": 9,
        "name": "（政法委书记待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共和政县委员会政法委员会",
        "source": "公开信息未明确；待官方确认",
    },
    # ════════════════════════════════════════
    # 副县长 (Deputy County Mayors)
    # ════════════════════════════════════════
    {
        "id": 10,
        "name": "马丽琼",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "和政县人民政府",
        "source": "和政府人〔2026〕21号；2026年6月县人大常委会第三十八次会议任命",
    },
    {
        "id": 11,
        "name": "（副县长待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "和政县人民政府",
        "source": "公开信息未明确；待官方确认",
    },
    {
        "id": 12,
        "name": "（副县长待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "和政县人民政府",
        "source": "公开信息未明确；待官方确认",
    },
    {
        "id": 13,
        "name": "（副县长待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "和政县人民政府",
        "source": "公开信息未明确；待官方确认",
    },
    # ════════════════════════════════════════
    # 前任领导 (Predecessors)
    # ════════════════════════════════════════
    {
        "id": 14,
        "name": "（前任县委书记待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任县委书记",
        "current_org": "中共和政县委员会",
        "source": "公开信息不足；冯祥安的任职时间尚不明确",
    },
    {
        "id": 15,
        "name": "（前任县长待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任县长",
        "current_org": "和政县人民政府",
        "source": "公开信息不足；赵斌的任职时间尚不明确",
    },
]

# ═══════════════════════════════════════════════
# 组织数据
# ═══════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共和政县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共临夏回族自治州委员会",
        "location": "甘肃省临夏回族自治州和政县",
    },
    {
        "id": 2,
        "name": "中共和政县委员会组织部",
        "type": "党委",
        "level": "县级",
        "parent": "中共和政县委员会",
        "location": "甘肃省临夏回族自治州和政县",
    },
    {
        "id": 3,
        "name": "中共和政县委员会宣传部",
        "type": "党委",
        "level": "县级",
        "parent": "中共和政县委员会",
        "location": "甘肃省临夏回族自治州和政县",
    },
    {
        "id": 4,
        "name": "中共和政县委员会政法委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共和政县委员会",
        "location": "甘肃省临夏回族自治州和政县",
    },
    {
        "id": 5,
        "name": "中共和政县委员会统战部",
        "type": "党委",
        "level": "县级",
        "parent": "中共和政县委员会",
        "location": "甘肃省临夏回族自治州和政县",
    },
    {
        "id": 6,
        "name": "和政县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "临夏回族自治州人民政府",
        "location": "甘肃省临夏回族自治州和政县",
    },
    {
        "id": 7,
        "name": "中共和政县纪律检查委员会",
        "type": "纪委",
        "level": "县级",
        "parent": "中共和政县委员会",
        "location": "甘肃省临夏回族自治州和政县",
    },
    {
        "id": 8,
        "name": "和政县监察委员会",
        "type": "监察",
        "level": "县级",
        "parent": "中共和政县委员会",
        "location": "甘肃省临夏回族自治州和政县",
    },
    {
        "id": 9,
        "name": "和政县人民武装部",
        "type": "政府",
        "level": "县级",
        "parent": "和政县人民政府",
        "location": "甘肃省临夏回族自治州和政县",
    },
    {
        "id": 10,
        "name": "和政县人大常委会",
        "type": "人大",
        "level": "县级",
        "parent": "和政县",
        "location": "甘肃省临夏回族自治州和政县",
    },
    {
        "id": 11,
        "name": "政协和政县委员会",
        "type": "政协",
        "level": "县级",
        "parent": "和政县",
        "location": "甘肃省临夏回族自治州和政县",
    },
]

# ═══════════════════════════════════════════════
# 任职数据
# ═══════════════════════════════════════════════

positions = [
    # 冯祥安 - 县委书记
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "present", "rank": "正县级", "note": "主持县委全面工作；2026年多次主持召开县委常委会（2026年7月）"},
    # 赵斌 - 县长
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 2, "org_id": 6, "title": "县长", "start_date": "", "end_date": "present", "rank": "正县级", "note": "主持县政府全面工作；主持召开第70次县政府常务会议（2026年7月）"},
    # 专职副书记 - 待确认
    {"person_id": 3, "org_id": 1, "title": "县委副书记（专职）", "start_date": "", "end_date": "present", "rank": "副县级", "note": "待确认"},
    # 常务副县长 - 待确认
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 4, "org_id": 6, "title": "常务副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "协助县长负责县政府日常工作；待确认"},
    # 纪委书记 - 待确认
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 5, "org_id": 7, "title": "县纪委书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 5, "org_id": 8, "title": "县监委主任", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 组织部长 - 待确认
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "组织部部长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 宣传部长 - 待确认
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 7, "org_id": 3, "title": "宣传部部长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 统战部长 - 待确认
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 8, "org_id": 5, "title": "统战部部长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 政法委书记 - 待确认
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 9, "org_id": 4, "title": "政法委书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 马丽琼 - 副县长
    {"person_id": 10, "org_id": 6, "title": "副县长", "start_date": "2026-06", "end_date": "present", "rank": "副县级", "note": "2026年6月15日经县人大常委会第三十八次会议任命"},
    # 副县长 - 待确认（党文发已免职）
    {"person_id": 11, "org_id": 6, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 12, "org_id": 6, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 13, "org_id": 6, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
]

# ═══════════════════════════════════════════════
# 关系数据
# ═══════════════════════════════════════════════
# NOTE: 基于当前县级领导班子结构推断，未有直接共事前的工作关系证据

relationships = [
    # 冯祥安 —— 县委常委班子成员
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "县委书记—县长搭档", "overlap_org": "中共和政县委员会", "overlap_period": "2026—"},
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "县委书记—专职副书记", "overlap_org": "中共和政县委员会", "overlap_period": "—"},
    {"person_a": 1, "person_b": 4, "type": "共事", "context": "县委书记—常务副县长", "overlap_org": "中共和政县委员会/和政县人民政府", "overlap_period": "—"},
    {"person_a": 1, "person_b": 5, "type": "监督", "context": "县委书记—纪委书记（同级监督）", "overlap_org": "中共和政县委员会", "overlap_period": "—"},
    {"person_a": 1, "person_b": 6, "type": "共事", "context": "县委书记—组织部部长", "overlap_org": "中共和政县委员会", "overlap_period": "—"},
    {"person_a": 1, "person_b": 7, "type": "共事", "context": "县委书记—宣传部部长", "overlap_org": "中共和政县委员会", "overlap_period": "—"},
    {"person_a": 1, "person_b": 8, "type": "共事", "context": "县委书记—统战部部长", "overlap_org": "中共和政县委员会", "overlap_period": "—"},
    {"person_a": 1, "person_b": 9, "type": "共事", "context": "县委书记—政法委书记", "overlap_org": "中共和政县委员会", "overlap_period": "—"},
    # 赵斌 —— 县长与班子成员
    {"person_a": 2, "person_b": 4, "type": "共事", "context": "县长—常务副县长", "overlap_org": "和政县人民政府", "overlap_period": "—"},
    {"person_a": 2, "person_b": 10, "type": "共事", "context": "县长—副县长", "overlap_org": "和政县人民政府", "overlap_period": "2026—"},
    {"person_a": 2, "person_b": 11, "type": "共事", "context": "县长—副县长", "overlap_org": "和政县人民政府", "overlap_period": "—"},
    {"person_a": 2, "person_b": 12, "type": "共事", "context": "县长—副县长", "overlap_org": "和政县人民政府", "overlap_period": "—"},
    {"person_a": 2, "person_b": 13, "type": "共事", "context": "县长—副县长", "overlap_org": "和政县人民政府", "overlap_period": "—"},
]

# ═══════════════════════════════════════════════
# 执行构建
# ═══════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("和政县（甘肃省临夏回族自治州）领导班子工作关系网络数据构建")
    print("=" * 60)
    print()

    # Print evidence status
    print("✅ 和政县人民政府网站(www.hezheng.gov.cn)可正常访问。")
    print("✅ 县委书记冯祥安、县长赵斌职务已通过官方政务新闻确认。")
    print("⚠️  领导之窗(ldzc)页面路径不可达，领导详细简历信息无法获取。")
    print("⚠️  县委常委、副县长的完整名单及分管领域待官方确认。")
    print("⚠️  冯祥安和赵斌的出生年月、教育背景、早期履历均无法从公开渠道获取。")
    print("⚠️  前任领导信息不足，无法确认。")
    print()

    run_build(
        slug="和政县",
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
    print("Build complete! (partial evidence mode)")
