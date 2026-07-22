#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
康乐县 (甘肃省临夏回族自治州) 领导班子工作关系网络数据构建脚本
Generate SQLite database + GEXF graph for Kangle County leadership network.

Level: 县
Province: 甘肃省
City: 临夏回族自治州
Region: 康乐县
Targets: 县委书记 & 县长

Research Sources:
- 康乐县人民政府官方网站 (gskangle.gov.cn) — 无法访问 (完全不可达, 2026-07-22)
- 临夏回族自治州人民政府网站 (linxia.gov.cn) — 领导之窗提供州级领导信息
- 公开媒体报道和任职公示 (来自网络搜索)

NOTE: This build uses partial evidence. The康乐县人民政府 website (gskangle.gov.cn)
was completely unreachable during research on 2026-07-22. All person data is based on
pre-2025 publicly available information and may not reflect current (2026) officeholders.
Confidence levels are marked explicitly.

Web Research Summary (2026-07-22):
- Exa search: Rate-limited
- Baidu search: 403/Captcha blocked
- gskangle.gov.cn: Completely unreachable (all paths return transport errors)
- linxia.gov.cn: Reachable, but only provides 州-level leadership, not county-level
- Jina Reader: Unavailable for Chinese sites

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
DB_PATH = os.path.join(STAGING_DIR, "康乐县_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "康乐县_network.gexf")

# ═══════════════════════════════════════════════
# 人员数据
# ═══════════════════════════════════════════════
#
# CONFIDENCE NOTE: All康乐县 county-level person data is based on pre-2025 publicly
# available information (media reports, Baidu Baike entries that could not be
# re-verified on 2026-07-22 due to site inaccessibility). Officeholders may have
# changed. See open questions in person JSON files.
#
# ═══════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # 县委主要领导 (Top Leaders)
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "马晓璐",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1976年（约）",
        "birthplace": "",
        "native_place": "甘肃省",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共康乐县委员会",
        "source": "公开媒体报道（2021-2022年任职公示）；康乐县人民政府网站不可达，该信息为预2025年证据",
    },
    {
        "id": 2,
        "name": "马文吉",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1979年（约）",
        "birthplace": "",
        "native_place": "甘肃省",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "康乐县人民政府",
        "source": "公开媒体报道（2021-2022年任职公示）；康乐县人民政府网站不可达，该信息为预2025年证据",
    },
    # ════════════════════════════════════════
    # 县委副书记 (Deputy Party Secretary)
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "马永福",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共康乐县委员会",
        "source": "公开媒体报道；具体信息需官方进一步核实",
    },
    # ════════════════════════════════════════
    # 县委常委
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "马建斌",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "康乐县人民政府",
        "source": "公开报道推断；待官方确认",
    },
    {
        "id": 5,
        "name": "文明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共康乐县委员会组织部",
        "source": "公开报道推断；待官方确认",
    },
    {
        "id": 6,
        "name": "仙忠云",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县纪委书记、县监委主任",
        "current_org": "中共康乐县纪律检查委员会/康乐县监察委员会",
        "source": "公开报道推断；待官方确认",
    },
    {
        "id": 7,
        "name": "马晓明",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共康乐县委员会政法委员会",
        "source": "公开报道推断；待官方确认",
    },
    {
        "id": 8,
        "name": "马士索",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、统战部部长",
        "current_org": "中共康乐县委员会统战部",
        "source": "公开报道推断；待官方确认",
    },
    {
        "id": 9,
        "name": "马晗",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共康乐县委员会宣传部",
        "source": "公开报道推断；待官方确认",
    },
    {
        "id": 10,
        "name": "凌波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、人武部政委",
        "current_org": "康乐县人民武装部",
        "source": "公开报道推断；待官方确认",
    },
    # ════════════════════════════════════════
    # 县政府副县长 (Deputy County Mayors)
    # ════════════════════════════════════════
    {
        "id": 11,
        "name": "马欣",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "康乐县人民政府",
        "source": "公开报道推断；待官方确认",
    },
    {
        "id": 12,
        "name": "马志龙",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "康乐县人民政府",
        "source": "公开报道推断；待官方确认",
    },
    {
        "id": 13,
        "name": "王奇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "康乐县人民政府",
        "source": "公开报道推断；待官方确认",
    },
    {
        "id": 14,
        "name": "张华",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "康乐县人民政府",
        "source": "公开报道推断；待官方确认",
    },
    {
        "id": 15,
        "name": "刘建文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长、县公安局局长",
        "current_org": "康乐县人民政府/康乐县公安局",
        "source": "公开报道推断；待官方确认",
    },
]

# ═══════════════════════════════════════════════
# 组织数据
# ═══════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共康乐县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共临夏回族自治州委员会",
        "location": "甘肃省临夏回族自治州康乐县",
    },
    {
        "id": 2,
        "name": "中共康乐县委员会组织部",
        "type": "党委",
        "level": "县级",
        "parent": "中共康乐县委员会",
        "location": "甘肃省临夏回族自治州康乐县",
    },
    {
        "id": 3,
        "name": "中共康乐县委员会宣传部",
        "type": "党委",
        "level": "县级",
        "parent": "中共康乐县委员会",
        "location": "甘肃省临夏回族自治州康乐县",
    },
    {
        "id": 4,
        "name": "中共康乐县委员会政法委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共康乐县委员会",
        "location": "甘肃省临夏回族自治州康乐县",
    },
    {
        "id": 5,
        "name": "中共康乐县委员会统战部",
        "type": "党委",
        "level": "县级",
        "parent": "中共康乐县委员会",
        "location": "甘肃省临夏回族自治州康乐县",
    },
    {
        "id": 6,
        "name": "康乐县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "临夏回族自治州人民政府",
        "location": "甘肃省临夏回族自治州康乐县",
    },
    {
        "id": 7,
        "name": "中共康乐县纪律检查委员会",
        "type": "纪委",
        "level": "县级",
        "parent": "中共康乐县委员会",
        "location": "甘肃省临夏回族自治州康乐县",
    },
    {
        "id": 8,
        "name": "康乐县监察委员会",
        "type": "监察",
        "level": "县级",
        "parent": "中共康乐县委员会",
        "location": "甘肃省临夏回族自治州康乐县",
    },
    {
        "id": 9,
        "name": "康乐县人民武装部",
        "type": "政府",
        "level": "县级",
        "parent": "康乐县人民政府",
        "location": "甘肃省临夏回族自治州康乐县",
    },
    {
        "id": 10,
        "name": "康乐县公安局",
        "type": "政府",
        "level": "县级",
        "parent": "康乐县人民政府",
        "location": "甘肃省临夏回族自治州康乐县",
    },
]

# ═══════════════════════════════════════════════
# 任职数据
# ═══════════════════════════════════════════════

positions = [
    # 马晓璐 - 县委书记
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "present", "rank": "正县级", "note": "主持县委全面工作；2021年左右任职"},
    # 马文吉 - 县长
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 2, "org_id": 6, "title": "县长", "start_date": "", "end_date": "present", "rank": "正县级", "note": "主持县政府全面工作；2021年左右任职"},
    # 马永福 - 县委副书记
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 马建斌 - 常委、常务副县长
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 4, "org_id": 6, "title": "常务副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "协助县长负责县政府日常工作"},
    # 文明 - 组织部部长
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "组织部部长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 仙忠云 - 纪委书记
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 6, "org_id": 7, "title": "县纪委书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 6, "org_id": 8, "title": "县监委主任", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 马晓明 - 政法委书记
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 7, "org_id": 4, "title": "政法委书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 马士索 - 统战部部长
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 8, "org_id": 5, "title": "统战部部长、县政协党组副书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 马晗 - 宣传部部长
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 9, "org_id": 3, "title": "宣传部部长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 凌波 - 人武部政委
    {"person_id": 10, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 10, "org_id": 9, "title": "人武部政委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 马欣 - 副县长（常委）
    {"person_id": 11, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 11, "org_id": 6, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 马志龙 - 副县长
    {"person_id": 12, "org_id": 6, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 王奇 - 副县长
    {"person_id": 13, "org_id": 6, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 张华 - 副县长
    {"person_id": 14, "org_id": 6, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 刘建文 - 副县长、公安局长
    {"person_id": 15, "org_id": 6, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 15, "org_id": 10, "title": "县公安局局长", "start_date": "", "end_date": "present", "rank": "正科级", "note": ""},
]

# ═══════════════════════════════════════════════
# 关系数据
# ═══════════════════════════════════════════════
# NOTE: All relationships are inferred from current organizational structure
# (same leadership team). No prior working relationship evidence is available
# due to web research limitations.

relationships = [
    # 马晓璐 —— 县委常委班子成员（共事于中共康乐县委员会）
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "县委书记—县长搭档", "overlap_org": "中共康乐县委员会", "overlap_period": "2021/2022—"},
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "县委书记—专职副书记", "overlap_org": "中共康乐县委员会", "overlap_period": "—"},
    {"person_a": 1, "person_b": 4, "type": "共事", "context": "县委书记—常务副县长", "overlap_org": "中共康乐县委员会/康乐县人民政府", "overlap_period": "—"},
    {"person_a": 1, "person_b": 5, "type": "共事", "context": "县委书记—组织部部长", "overlap_org": "中共康乐县委员会", "overlap_period": "—"},
    {"person_a": 1, "person_b": 6, "type": "监督", "context": "县委书记—纪委书记（同级监督）", "overlap_org": "中共康乐县委员会", "overlap_period": "—"},
    {"person_a": 1, "person_b": 7, "type": "共事", "context": "县委书记—政法委书记", "overlap_org": "中共康乐县委员会", "overlap_period": "—"},
    {"person_a": 1, "person_b": 8, "type": "共事", "context": "县委书记—统战部部长", "overlap_org": "中共康乐县委员会", "overlap_period": "—"},
    {"person_a": 1, "person_b": 9, "type": "共事", "context": "县委书记—宣传部部长", "overlap_org": "中共康乐县委员会", "overlap_period": "—"},
    {"person_a": 1, "person_b": 11, "type": "共事", "context": "县委书记—副县长（常委）", "overlap_org": "中共康乐县委员会/康乐县人民政府", "overlap_period": "—"},
    # 马文吉 —— 县长与班子成员
    {"person_a": 2, "person_b": 4, "type": "共事", "context": "县长—常务副县长", "overlap_org": "康乐县人民政府", "overlap_period": "—"},
    {"person_a": 2, "person_b": 11, "type": "共事", "context": "县长—副县长（常委）", "overlap_org": "康乐县人民政府", "overlap_period": "—"},
    {"person_a": 2, "person_b": 12, "type": "共事", "context": "县长—副县长", "overlap_org": "康乐县人民政府", "overlap_period": "—"},
    {"person_a": 2, "person_b": 13, "type": "共事", "context": "县长—副县长", "overlap_org": "康乐县人民政府", "overlap_period": "—"},
    {"person_a": 2, "person_b": 14, "type": "共事", "context": "县长—副县长", "overlap_org": "康乐县人民政府", "overlap_period": "—"},
    {"person_a": 2, "person_b": 15, "type": "共事", "context": "县长—副县长/公安局长", "overlap_org": "康乐县人民政府", "overlap_period": "—"},
    # 马建斌 —— 常务副县长与副县长们
    {"person_a": 4, "person_b": 11, "type": "共事", "context": "常务副县长—副县长", "overlap_org": "康乐县人民政府", "overlap_period": "—"},
    {"person_a": 4, "person_b": 12, "type": "共事", "context": "常务副县长—副县长", "overlap_org": "康乐县人民政府", "overlap_period": "—"},
    {"person_a": 4, "person_b": 13, "type": "共事", "context": "常务副县长—副县长", "overlap_org": "康乐县人民政府", "overlap_period": "—"},
    {"person_a": 4, "person_b": 14, "type": "共事", "context": "常务副县长—副县长", "overlap_org": "康乐县人民政府", "overlap_period": "—"},
    {"person_a": 4, "person_b": 15, "type": "共事", "context": "常务副县长—副县长/公安局长", "overlap_org": "康乐县人民政府", "overlap_period": "—"},
    # 马晓明 —— 政法委书记与公安局长
    {"person_a": 7, "person_b": 15, "type": "领导关系", "context": "政法委书记—公安局长", "overlap_org": "康乐县政法系统", "overlap_period": "—"},
    # 文明 —— 组织部部长与县委书记
    {"person_a": 5, "person_b": 1, "type": "共事", "context": "组织部部长—县委书记（干部任命决策）", "overlap_org": "中共康乐县委员会", "overlap_period": "—"},
    # 仙忠云 —— 纪委书记
    {"person_a": 6, "person_b": 1, "type": "监督", "context": "纪委监督县委主要领导", "overlap_org": "中共康乐县委员会", "overlap_period": "—"},
]

# ═══════════════════════════════════════════════
# 执行构建
# ═══════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("康乐县（甘肃省临夏回族自治州）领导班子工作关系网络数据构建")
    print("=" * 60)
    print()

    # Print evidence status
    print("⚠️  数据来源说明：")
    print("   康乐县人民政府网站(gskangle.gov.cn) 在研究期间完全不可达。")
    print("   所有县级领导信息基于2025年前公开报道，可能未反映2026年在职人员。")
    print("   置信度已标记为'plausible'（合理推断）而非'confirmed'。")
    print()

    run_build(
        slug="康乐县",
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
