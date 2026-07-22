#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
玛曲县 (甘肃省甘南藏族自治州) 领导班子工作关系网络数据构建脚本
Generate SQLite database + GEXF graph for Maqu County leadership network.

Level: 县
Province: 甘肃省
City: 甘南藏族自治州
Region: 玛曲县
Targets: 县委书记 & 县长

Research Sources:
- 玛曲县人民政府官方网站 (maqu.gov.cn) — 2026-07-22访问超时，未能获取领导信息
- 甘南藏族自治州人民政府网站 (gnzrmzf.gov.cn) — 2026-07-22访问超时
- 维基百科玛曲县页面 — 仅有地理信息，无现任领导列表
- 外部搜索工具（Exa）rate-limited
- 百度搜索、Jina Reader等工具均因网络限制未能返回有效信息

Confidence:
- 截至2026年7月22日，未能通过公开网络渠道获取玛曲县现任县委书记和县长的姓名
- 所有领导信息标记为"（待查）"，需通过其他渠道补充
- 组织结构基于甘南州县级领导班子的标准配置推测

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
DB_PATH = os.path.join(STAGING_DIR, "玛曲县_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "玛曲县_network.gexf")

# ═══════════════════════════════════════════════
# 人员数据
# ═══════════════════════════════════════════════
#
# ⚠ 重要提示：以下领导姓名因公开网络渠道访问受限，均为"（待查）"状态。
# 2026-07-22尝试访问 maqu.gov.cn、gnzrmzf.gov.cn 均超时，
# 百度搜索受403限制，Exa搜索达到免费调用上限。
# 需要从以下渠道补充：
# 1. 玛曲县人民政府网站 领导之窗页面（https://www.maqu.gov.cn/zjqm/ldzc/）
# 2. 甘南州委组织部任前公示
# 3. 人民网地方领导资料库（ldzl.people.com.cn）
# 4. 中国知网或新闻报道数据库检索
# ═══════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # 县委主要领导
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
        "current_org": "中共玛曲县委员会",
        "source": "待查 — maqu.gov.cn无法访问（2026-07-22），无法确认现任县委书记姓名",
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
        "current_org": "玛曲县人民政府",
        "source": "待查 — maqu.gov.cn无法访问（2026-07-22），无法确认现任县长姓名",
    },
    # ════════════════════════════════════════
    # 县委副书记（专职）
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
        "current_post": "县委副书记（专职）",
        "current_org": "中共玛曲县委员会",
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
        "current_org": "玛曲县人民政府",
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
        "current_org": "中共玛曲县委员会组织部",
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
        "current_org": "中共玛曲县纪律检查委员会/玛曲县监察委员会",
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
        "current_org": "中共玛曲县委员会政法委员会",
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
        "current_org": "中共玛曲县委员会宣传部",
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
        "current_org": "中共玛曲县委员会统战部",
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
        "current_org": "玛曲县人民武装部",
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
        "current_org": "玛曲县人民政府/玛曲县公安局",
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
        "current_org": "玛曲县人民政府",
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
        "current_org": "玛曲县人民政府",
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
        "current_org": "玛曲县人民政府",
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
        "current_org": "玛曲县人民政府",
        "source": "待查",
    },
]

# ═══════════════════════════════════════════════
# 组织数据
# ═══════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共玛曲县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共甘南藏族自治州委员会",
        "location": "甘肃省甘南藏族自治州玛曲县",
    },
    {
        "id": 2,
        "name": "中共玛曲县委员会组织部",
        "type": "党委",
        "level": "县级",
        "parent": "中共玛曲县委员会",
        "location": "甘肃省甘南藏族自治州玛曲县",
    },
    {
        "id": 3,
        "name": "中共玛曲县委员会宣传部",
        "type": "党委",
        "level": "县级",
        "parent": "中共玛曲县委员会",
        "location": "甘肃省甘南藏族自治州玛曲县",
    },
    {
        "id": 4,
        "name": "中共玛曲县委员会政法委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共玛曲县委员会",
        "location": "甘肃省甘南藏族自治州玛曲县",
    },
    {
        "id": 5,
        "name": "中共玛曲县委员会统战部",
        "type": "党委",
        "level": "县级",
        "parent": "中共玛曲县委员会",
        "location": "甘肃省甘南藏族自治州玛曲县",
    },
    {
        "id": 6,
        "name": "玛曲县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "甘南藏族自治州人民政府",
        "location": "甘肃省甘南藏族自治州玛曲县",
    },
    {
        "id": 7,
        "name": "中共玛曲县纪律检查委员会",
        "type": "纪委",
        "level": "县级",
        "parent": "中共玛曲县委员会",
        "location": "甘肃省甘南藏族自治州玛曲县",
    },
    {
        "id": 8,
        "name": "玛曲县监察委员会",
        "type": "监察",
        "level": "县级",
        "parent": "中共玛曲县委员会",
        "location": "甘肃省甘南藏族自治州玛曲县",
    },
    {
        "id": 9,
        "name": "玛曲县人民武装部",
        "type": "政府",
        "level": "县级",
        "parent": "玛曲县人民政府",
        "location": "甘肃省甘南藏族自治州玛曲县",
    },
    {
        "id": 10,
        "name": "玛曲县公安局",
        "type": "政府",
        "level": "县级",
        "parent": "玛曲县人民政府",
        "location": "甘肃省甘南藏族自治州玛曲县",
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
# ⚠ 因所有领导姓名均未确认，以下关系基于县级领导班子结构推断。
# 确认具体人名后需更新。
# ═══════════════════════════════════════════════

relationships = [
    # 县委书记 — 县长（基于班子结构推测）
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "县委书记—县长搭档（结构推断）", "overlap_org": "中共玛曲县委员会/玛曲县人民政府", "overlap_period": "待查—"},
    # 县委书记 — 县委常委班子成员
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "县委书记—专职副书记", "overlap_org": "中共玛曲县委员会", "overlap_period": "待查—"},
    {"person_a": 1, "person_b": 4, "type": "共事", "context": "县委书记—常务副县长", "overlap_org": "中共玛曲县委员会/玛曲县人民政府", "overlap_period": "待查—"},
    {"person_a": 1, "person_b": 5, "type": "共事", "context": "县委书记—组织部部长", "overlap_org": "中共玛曲县委员会", "overlap_period": "待查—"},
    {"person_a": 1, "person_b": 6, "type": "监督", "context": "县委书记—纪委书记（同级监督）", "overlap_org": "中共玛曲县委员会", "overlap_period": "待查—"},
    {"person_a": 1, "person_b": 7, "type": "共事", "context": "县委书记—政法委书记", "overlap_org": "中共玛曲县委员会", "overlap_period": "待查—"},
    {"person_a": 1, "person_b": 8, "type": "共事", "context": "县委书记—宣传部部长", "overlap_org": "中共玛曲县委员会", "overlap_period": "待查—"},
    {"person_a": 1, "person_b": 9, "type": "共事", "context": "县委书记—统战部部长", "overlap_org": "中共玛曲县委员会", "overlap_period": "待查—"},
    # 县长与班子成员
    {"person_a": 2, "person_b": 4, "type": "共事", "context": "县长—常务副县长", "overlap_org": "玛曲县人民政府", "overlap_period": "待查—"},
    {"person_a": 2, "person_b": 11, "type": "共事", "context": "县长—副县长/公安局长", "overlap_org": "玛曲县人民政府", "overlap_period": "待查—"},
    {"person_a": 2, "person_b": 12, "type": "共事", "context": "县长—副县长", "overlap_org": "玛曲县人民政府", "overlap_period": "待查—"},
    {"person_a": 2, "person_b": 13, "type": "共事", "context": "县长—副县长", "overlap_org": "玛曲县人民政府", "overlap_period": "待查—"},
    {"person_a": 2, "person_b": 14, "type": "共事", "context": "县长—副县长", "overlap_org": "玛曲县人民政府", "overlap_period": "待查—"},
    {"person_a": 2, "person_b": 15, "type": "共事", "context": "县长—副县长", "overlap_org": "玛曲县人民政府", "overlap_period": "待查—"},
    # 常务副县长与副县长
    {"person_a": 4, "person_b": 11, "type": "共事", "context": "常务副县长—副县长/公安局长", "overlap_org": "玛曲县人民政府", "overlap_period": "待查—"},
    {"person_a": 4, "person_b": 12, "type": "共事", "context": "常务副县长—副县长", "overlap_org": "玛曲县人民政府", "overlap_period": "待查—"},
    {"person_a": 4, "person_b": 13, "type": "共事", "context": "常务副县长—副县长", "overlap_org": "玛曲县人民政府", "overlap_period": "待查—"},
    {"person_a": 4, "person_b": 14, "type": "共事", "context": "常务副县长—副县长", "overlap_org": "玛曲县人民政府", "overlap_period": "待查—"},
    {"person_a": 4, "person_b": 15, "type": "共事", "context": "常务副县长—副县长", "overlap_org": "玛曲县人民政府", "overlap_period": "待查—"},
    # 政法委书记与公安局长
    {"person_a": 7, "person_b": 11, "type": "领导关系", "context": "政法委书记—公安局长", "overlap_org": "玛曲县政法系统", "overlap_period": "待查—"},
    # 专职副书记与县委常委
    {"person_a": 3, "person_b": 4, "type": "共事", "context": "专职副书记—常务副县长", "overlap_org": "中共玛曲县委员会/玛曲县人民政府", "overlap_period": "待查—"},
    {"person_a": 3, "person_b": 5, "type": "共事", "context": "专职副书记—组织部部长", "overlap_org": "中共玛曲县委员会", "overlap_period": "待查—"},
]

# ═══════════════════════════════════════════════
# 执行构建
# ═══════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("玛曲县（甘肃省甘南藏族自治州）领导班子工作关系网络数据构建")
    print("=" * 60)
    print()
    print("调研日期：2026-07-22")
    print("信息来源：maqu.gov.cn（无法访问）、gnzrmzf.gov.cn（无法访问）")
    print()
    print("⚠ 重要：截至2026年7月22日，所有公开网络渠道均无法获取")
    print("   玛曲县现任领导班子成员姓名。以下所有人员均标注为（待查）。")
    print()
    print("尝试过的渠道：")
    print("  - maqu.gov.cn — 连接超时（HTTPS和HTTP均尝试）")
    print("  - maqu.gov.cn/zjqm/ldzc/ — 连接超时")
    print("  - maqu.gov.cn/zwgk/ldxx/ — 连接超时")
    print("  - gnzrmzf.gov.cn — 连接超时")
    print("  - 百度百科 — 403拒绝访问")
    print("  - Exa搜索引擎 — 免费API调用上限")
    print("  - Jina Reader — 连接超时/传输错误")
    print()
    print("建议渠道：")
    print("  1. maqu.gov.cn 领导之窗（需在能访问政府网站的网络环境下打开）")
    print("  2. 甘南州委组织部任前公示")
    print("  3. 人民网地方领导资料库 ldzl.people.com.cn")
    print("  4. 通过VPN或国内服务器访问政府网站")
    print()

    run_build(
        slug="玛曲县",
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
    print("⚠ 重要提示：全部15位人员的姓名为'（待查）'，")
    print("   需要通过以下渠道获取现任领导班子完整名单后更新本脚本：")
    print("   1. 玛曲县人民政府网站 领导之窗页面")
    print("   2. 甘南州委组织部任前公示")
    print("   3. 人民网地方领导资料库")
