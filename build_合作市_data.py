#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
合作市 (甘肃省甘南藏族自治州) 领导班子工作关系网络数据构建脚本
Generate SQLite database + GEXF graph for Hezuo City leadership network.

Level: 县级市
Province: 甘肃省
City: 甘南藏族自治州
Region: 合作市
Targets: 市委书记 & 市长

Research Sources:
- 合作市人民政府官方网站 (hezuo.gov.cn) — 访问超时，2026-07-22无法连接
- zh.wikipedia.org/wiki/合作市 — 行政区划信息，2026年7月22日确认
- zh.wikipedia.org/wiki/甘南藏族自治州 — 州级领导信息，2026年7月22日确认
- 合作市为甘南藏族自治州州府所在地，县级市建制
- 现任市委书记、市长姓名暂未从公开可访问渠道获取

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
DB_PATH = os.path.join(STAGING_DIR, "合作市_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "合作市_network.gexf")

# ═══════════════════════════════════════════════
# 人员数据
# ═══════════════════════════════════════════════
#
# 以下数据基于合作市作为甘南藏族自治州州府的结构确认。
# 由于 hezuo.gov.cn 超时、百度百科403、Exa搜索限流，
# 现任领导姓名无法从公开可访问来源获取。
# 详见 report/open_gaps.md
# ═══════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # 市委主要领导
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
        "current_post": "市委书记",
        "current_org": "中共合作市委员会",
        "source": "待查 — hezuo.gov.cn 无法访问",
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
        "current_post": "市委副书记、市长",
        "current_org": "合作市人民政府",
        "source": "待查 — hezuo.gov.cn 无法访问",
    },
    # ════════════════════════════════════════
    # 市委副书记（专职）
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
        "current_post": "市委副书记（专职）",
        "current_org": "中共合作市委员会",
        "source": "待查",
    },
    # ════════════════════════════════════════
    # 市委常委
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
        "current_post": "市委常委、常务副市长",
        "current_org": "合作市人民政府",
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
        "current_post": "市委常委、组织部部长",
        "current_org": "中共合作市委员会组织部",
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
        "current_post": "市委常委、市纪委书记、市监委主任",
        "current_org": "中共合作市纪律检查委员会/合作市监察委员会",
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
        "current_post": "市委常委、政法委书记",
        "current_org": "中共合作市委员会政法委员会",
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
        "current_post": "市委常委、宣传部部长",
        "current_org": "中共合作市委员会宣传部",
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
        "current_post": "市委常委、统战部部长",
        "current_org": "中共合作市委员会统战部",
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
        "current_post": "市委常委、人武部政委",
        "current_org": "合作市人民武装部",
        "source": "待查",
    },
    # ════════════════════════════════════════
    # 市政府副市长
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
        "current_post": "副市长、市公安局局长",
        "current_org": "合作市人民政府/合作市公安局",
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
        "current_post": "副市长",
        "current_org": "合作市人民政府",
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
        "current_post": "副市长",
        "current_org": "合作市人民政府",
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
        "current_post": "副市长",
        "current_org": "合作市人民政府",
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
        "current_post": "副市长",
        "current_org": "合作市人民政府",
        "source": "待查",
    },
]

# ═══════════════════════════════════════════════
# 组织数据
# ═══════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共合作市委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共甘南藏族自治州委员会",
        "location": "甘肃省甘南藏族自治州合作市",
    },
    {
        "id": 2,
        "name": "中共合作市委员会组织部",
        "type": "党委",
        "level": "县级",
        "parent": "中共合作市委员会",
        "location": "甘肃省甘南藏族自治州合作市",
    },
    {
        "id": 3,
        "name": "中共合作市委员会宣传部",
        "type": "党委",
        "level": "县级",
        "parent": "中共合作市委员会",
        "location": "甘肃省甘南藏族自治州合作市",
    },
    {
        "id": 4,
        "name": "中共合作市委员会政法委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共合作市委员会",
        "location": "甘肃省甘南藏族自治州合作市",
    },
    {
        "id": 5,
        "name": "中共合作市委员会统战部",
        "type": "党委",
        "level": "县级",
        "parent": "中共合作市委员会",
        "location": "甘肃省甘南藏族自治州合作市",
    },
    {
        "id": 6,
        "name": "合作市人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "甘南藏族自治州人民政府",
        "location": "甘肃省甘南藏族自治州合作市",
    },
    {
        "id": 7,
        "name": "中共合作市纪律检查委员会",
        "type": "纪委",
        "level": "县级",
        "parent": "中共合作市委员会",
        "location": "甘肃省甘南藏族自治州合作市",
    },
    {
        "id": 8,
        "name": "合作市监察委员会",
        "type": "监察",
        "level": "县级",
        "parent": "中共合作市委员会",
        "location": "甘肃省甘南藏族自治州合作市",
    },
    {
        "id": 9,
        "name": "合作市人民武装部",
        "type": "政府",
        "level": "县级",
        "parent": "合作市人民政府",
        "location": "甘肃省甘南藏族自治州合作市",
    },
    {
        "id": 10,
        "name": "合作市公安局",
        "type": "政府",
        "level": "县级",
        "parent": "合作市人民政府",
        "location": "甘肃省甘南藏族自治州合作市",
    },
]

# ═══════════════════════════════════════════════
# 任职数据
# ═══════════════════════════════════════════════

positions = [
    # 市委书记
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "present", "rank": "正县级", "note": "主持市委全面工作"},
    # 市长
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 2, "org_id": 6, "title": "市长", "start_date": "", "end_date": "present", "rank": "正县级", "note": "主持市政府全面工作"},
    # 专职副书记
    {"person_id": 3, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 常务副市长
    {"person_id": 4, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 4, "org_id": 6, "title": "常务副市长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "协助市长负责市政府日常工作"},
    # 组织部部长
    {"person_id": 5, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "组织部部长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 纪委书记
    {"person_id": 6, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 6, "org_id": 7, "title": "市纪委书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 6, "org_id": 8, "title": "市监委主任", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 政法委书记
    {"person_id": 7, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 7, "org_id": 4, "title": "政法委书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 宣传部部长
    {"person_id": 8, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 8, "org_id": 3, "title": "宣传部部长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 统战部部长
    {"person_id": 9, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 9, "org_id": 5, "title": "统战部部长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 人武部政委
    {"person_id": 10, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 10, "org_id": 9, "title": "人武部政委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 副市长/公安局长
    {"person_id": 11, "org_id": 6, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 11, "org_id": 10, "title": "市公安局局长", "start_date": "", "end_date": "present", "rank": "正科级", "note": ""},
    # 副市长
    {"person_id": 12, "org_id": 6, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 13, "org_id": 6, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 14, "org_id": 6, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 15, "org_id": 6, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
]

# ═══════════════════════════════════════════════
# 关系数据
# ═══════════════════════════════════════════════
#
# 所有具体人名均为（待查），关系数据以市级领导班子结构推断。
# 待获取领导姓名后完善。
# ═══════════════════════════════════════════════

relationships = [
    # 市委书记 — 市长（confirmed搭档）
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "市委书记—市长搭档", "overlap_org": "中共合作市委员会/合作市人民政府", "overlap_period": "—"},
    # 市委书记 — 市委常委班子成员
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "市委书记—专职副书记", "overlap_org": "中共合作市委员会", "overlap_period": "—"},
    {"person_a": 1, "person_b": 4, "type": "共事", "context": "市委书记—常务副市长", "overlap_org": "中共合作市委员会/合作市人民政府", "overlap_period": "—"},
    {"person_a": 1, "person_b": 5, "type": "共事", "context": "市委书记—组织部部长", "overlap_org": "中共合作市委员会", "overlap_period": "—"},
    {"person_a": 1, "person_b": 6, "type": "监督", "context": "市委书记—纪委书记（同级监督）", "overlap_org": "中共合作市委员会", "overlap_period": "—"},
    {"person_a": 1, "person_b": 7, "type": "共事", "context": "市委书记—政法委书记", "overlap_org": "中共合作市委员会", "overlap_period": "—"},
    {"person_a": 1, "person_b": 8, "type": "共事", "context": "市委书记—宣传部部长", "overlap_org": "中共合作市委员会", "overlap_period": "—"},
    {"person_a": 1, "person_b": 9, "type": "共事", "context": "市委书记—统战部部长", "overlap_org": "中共合作市委员会", "overlap_period": "—"},
    # 市长与班子成员
    {"person_a": 2, "person_b": 4, "type": "共事", "context": "市长—常务副市长", "overlap_org": "合作市人民政府", "overlap_period": "—"},
    {"person_a": 2, "person_b": 11, "type": "共事", "context": "市长—副市长/公安局长", "overlap_org": "合作市人民政府", "overlap_period": "—"},
    {"person_a": 2, "person_b": 12, "type": "共事", "context": "市长—副市长", "overlap_org": "合作市人民政府", "overlap_period": "—"},
    {"person_a": 2, "person_b": 13, "type": "共事", "context": "市长—副市长", "overlap_org": "合作市人民政府", "overlap_period": "—"},
    {"person_a": 2, "person_b": 14, "type": "共事", "context": "市长—副市长", "overlap_org": "合作市人民政府", "overlap_period": "—"},
    {"person_a": 2, "person_b": 15, "type": "共事", "context": "市长—副市长", "overlap_org": "合作市人民政府", "overlap_period": "—"},
    # 常务副市长与副市长
    {"person_a": 4, "person_b": 11, "type": "共事", "context": "常务副市长—副市长/公安局长", "overlap_org": "合作市人民政府", "overlap_period": "—"},
    {"person_a": 4, "person_b": 12, "type": "共事", "context": "常务副市长—副市长", "overlap_org": "合作市人民政府", "overlap_period": "—"},
    {"person_a": 4, "person_b": 13, "type": "共事", "context": "常务副市长—副市长", "overlap_org": "合作市人民政府", "overlap_period": "—"},
    {"person_a": 4, "person_b": 14, "type": "共事", "context": "常务副市长—副市长", "overlap_org": "合作市人民政府", "overlap_period": "—"},
    {"person_a": 4, "person_b": 15, "type": "共事", "context": "常务副市长—副市长", "overlap_org": "合作市人民政府", "overlap_period": "—"},
    # 政法委书记与公安局长
    {"person_a": 7, "person_b": 11, "type": "领导关系", "context": "政法委书记—公安局长", "overlap_org": "合作市政法系统", "overlap_period": "—"},
    # 专职副书记与市委常委
    {"person_a": 3, "person_b": 4, "type": "共事", "context": "专职副书记—常务副市长", "overlap_org": "中共合作市委员会/合作市人民政府", "overlap_period": "—"},
    {"person_a": 3, "person_b": 5, "type": "共事", "context": "专职副书记—组织部部长", "overlap_org": "中共合作市委员会", "overlap_period": "—"},
]

# ═══════════════════════════════════════════════
# 执行构建
# ═══════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("合作市（甘肃省甘南藏族自治州）领导班子工作关系网络数据构建")
    print("=" * 60)
    print()
    print("调研日期：2026-07-22")
    print("信息来源：zh.wikipedia.org/wiki/合作市（行政区划信息），hezuo.gov.cn 无法连接")
    print()
    print("注意：因 hezuo.gov.cn 访问超时、百度百科403、Exa搜索限流，")
    print("现任市委、市政府领导姓名均为（待查），")
    print("共计15位人员信息待补充。详见 report/open_gaps.md")
    print()

    run_build(
        slug="合作市",
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
    print("⚠ 重要提示：本数据库中的15位人员姓名为'（待查）'，")
    print("   需要从合作市人民政府网站的领导之窗页面或通过甘南州委组织部任前公示等渠道")
    print("   获取现任领导班子完整名单后更新本脚本并重新生成。")
