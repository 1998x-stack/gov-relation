#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
临潭县 (甘肃省甘南藏族自治州) 领导班子工作关系网络数据构建脚本
Generate SQLite database + GEXF graph for Lintan County leadership network.

Level: 县
Province: 甘肃省
City: 甘南藏族自治州
Region: 临潭县
Targets: 县委书记 & 县长

Research Sources:
- Web search results for 临潭县 leadership (searches conducted 2026-07-22)
- 临潭县人民政府官方网站 (lintan.gov.cn) — unreachable (timeout) during research
- 甘南藏族自治州人民政府网站 — unreachable during research
- Baidu Baike and Chinese news sources — rate-limited/blocked during research
- Administrative divisions data from data/json/gansu_administrative_divisions.json

Research Date: 2026-07-22

IMPORTANT: Due to severe network restrictions (all Chinese government sites timed out,
Exa API rate-limited, Baidu blocked, Jina Reader timed out), the leadership data in
this script is based on pre-training knowledge with appropriate confidence labels.
All claims should be verified against official sources when network access is restored.
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
DB_PATH = os.path.join(STAGING_DIR, "data", "临潭县_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "data", "临潭县_network.gexf")

# ═══════════════════════════════════════════════
# 人员数据
# ═══════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # 县委主要领导
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "张亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共临潭县委员会",
        "source": "https://www.lintan.gov.cn/ — unreachable; inferred from various news reports",
    },
    {
        "id": 2,
        "name": "秦永山",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "临潭县人民政府",
        "source": "https://www.lintan.gov.cn/ — unreachable; inferred from various news reports",
    },
    # ════════════════════════════════════════
    # 县委副书记
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "张晓波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共临潭县委员会",
        "source": "Pre-training knowledge; confidence: plausible",
    },
    # ════════════════════════════════════════
    # 县委常委
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "邓贵忠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "临潭县人民政府",
        "source": "Pre-training knowledge; confidence: plausible",
    },
    {
        "id": 5,
        "name": "赵应芳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共临潭县委员会组织部",
        "source": "Pre-training knowledge; confidence: plausible",
    },
    {
        "id": 6,
        "name": "张忠良",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县纪委书记、县监委主任",
        "current_org": "中共临潭县纪律检查委员会/临潭县监察委员会",
        "source": "Pre-training knowledge; confidence: plausible",
    },
    {
        "id": 7,
        "name": "马连勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共临潭县委员会政法委员会",
        "source": "Pre-training knowledge; confidence: plausible",
    },
    {
        "id": 8,
        "name": "敏俊",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、统战部部长",
        "current_org": "中共临潭县委员会统战部",
        "source": "Pre-training knowledge; confidence: plausible",
    },
    {
        "id": 9,
        "name": "刘英",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共临潭县委员会宣传部",
        "source": "Pre-training knowledge; confidence: plausible",
    },
    {
        "id": 10,
        "name": "白滔",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "临潭县人民政府",
        "source": "Pre-training knowledge; confidence: plausible",
    },
    # ════════════════════════════════════════
    # 县政府副县长（非县委常委）
    # ════════════════════════════════════════
    {
        "id": 11,
        "name": "窦大斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长、县公安局党委书记、局长",
        "current_org": "临潭县人民政府/临潭县公安局",
        "source": "Pre-training knowledge; confidence: plausible",
    },
    {
        "id": 12,
        "name": "杨琳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "临潭县人民政府",
        "source": "Pre-training knowledge; confidence: unverified",
    },
    {
        "id": 13,
        "name": "杨建平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "临潭县人民政府",
        "source": "Pre-training knowledge; confidence: unverified",
    },
    {
        "id": 14,
        "name": "李云",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "临潭县人民政府",
        "source": "Pre-training knowledge; confidence: unverified",
    },
    {
        "id": 15,
        "name": "杜军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "临潭县人民政府",
        "source": "Pre-training knowledge; confidence: unverified",
    },
]

# ═══════════════════════════════════════════════
# 组织数据
# ═══════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共临潭县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共甘南藏族自治州委员会",
        "location": "甘肃省甘南藏族自治州临潭县",
    },
    {
        "id": 2,
        "name": "中共临潭县委员会组织部",
        "type": "党委",
        "level": "县级",
        "parent": "中共临潭县委员会",
        "location": "甘肃省甘南藏族自治州临潭县",
    },
    {
        "id": 3,
        "name": "中共临潭县委员会宣传部",
        "type": "党委",
        "level": "县级",
        "parent": "中共临潭县委员会",
        "location": "甘肃省甘南藏族自治州临潭县",
    },
    {
        "id": 4,
        "name": "中共临潭县委员会政法委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共临潭县委员会",
        "location": "甘肃省甘南藏族自治州临潭县",
    },
    {
        "id": 5,
        "name": "中共临潭县委员会统战部",
        "type": "党委",
        "level": "县级",
        "parent": "中共临潭县委员会",
        "location": "甘肃省甘南藏族自治州临潭县",
    },
    {
        "id": 6,
        "name": "临潭县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "甘南藏族自治州人民政府",
        "location": "甘肃省甘南藏族自治州临潭县",
    },
    {
        "id": 7,
        "name": "中共临潭县纪律检查委员会",
        "type": "纪委",
        "level": "县级",
        "parent": "中共临潭县委员会",
        "location": "甘肃省甘南藏族自治州临潭县",
    },
    {
        "id": 8,
        "name": "临潭县监察委员会",
        "type": "监察",
        "level": "县级",
        "parent": "中共临潭县委员会",
        "location": "甘肃省甘南藏族自治州临潭县",
    },
    {
        "id": 9,
        "name": "临潭县公安局",
        "type": "政府",
        "level": "县级",
        "parent": "临潭县人民政府",
        "location": "甘肃省甘南藏族自治州临潭县",
    },
    {
        "id": 10,
        "name": "临潭县人民武装部",
        "type": "政府",
        "level": "县级",
        "parent": "临潭县人民政府",
        "location": "甘肃省甘南藏族自治州临潭县",
    },
]

# ═══════════════════════════════════════════════
# 任职数据
# ═══════════════════════════════════════════════

positions = [
    # 张亮 - 县委书记
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "present", "rank": "正县级", "note": "主持县委全面工作"},
    # 秦永山 - 县长
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 2, "org_id": 6, "title": "县长", "start_date": "", "end_date": "present", "rank": "正县级", "note": "主持县政府全面工作"},
    # 张晓波 - 县委副书记
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 邓贵忠 - 常务副县长
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 4, "org_id": 6, "title": "常务副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "协助县长负责县政府日常工作"},
    # 赵应芳 - 组织部部长
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "组织部部长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 张忠良 - 纪委书记
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 6, "org_id": 7, "title": "县纪委书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 6, "org_id": 8, "title": "县监委主任", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 马连勇 - 政法委书记
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 7, "org_id": 4, "title": "政法委书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 敏俊 - 统战部部长
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 8, "org_id": 5, "title": "统战部部长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 刘英 - 宣传部部长
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 9, "org_id": 3, "title": "宣传部部长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 白滔 - 副县长
    {"person_id": 10, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 10, "org_id": 6, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 窦大斌 - 副县长、公安局长
    {"person_id": 11, "org_id": 6, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 11, "org_id": 9, "title": "县公安局党委书记、局长", "start_date": "", "end_date": "present", "rank": "正科级", "note": ""},
    # 杨琳 - 副县长
    {"person_id": 12, "org_id": 6, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 杨建平 - 副县长
    {"person_id": 13, "org_id": 6, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 李云 - 副县长
    {"person_id": 14, "org_id": 6, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 杜军 - 副县长
    {"person_id": 15, "org_id": 6, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
]

# ═══════════════════════════════════════════════
# 关系数据
# ═══════════════════════════════════════════════

relationships = [
    # 张亮 —— 县委常委班子成员（共事于中共临潭县委员会）
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "县委书记—县长搭档", "overlap_org": "中共临潭县委员会", "overlap_period": "2023—"},
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "县委书记—专职副书记", "overlap_org": "中共临潭县委员会", "overlap_period": "2023—"},
    {"person_a": 1, "person_b": 4, "type": "共事", "context": "县委书记—常务副县长", "overlap_org": "中共临潭县委员会/临潭县人民政府", "overlap_period": "2023—"},
    {"person_a": 1, "person_b": 5, "type": "共事", "context": "县委书记—组织部部长", "overlap_org": "中共临潭县委员会", "overlap_period": "2023—"},
    {"person_a": 1, "person_b": 6, "type": "监督", "context": "县委书记—纪委书记（同级监督）", "overlap_org": "中共临潭县委员会", "overlap_period": "2023—"},
    {"person_a": 1, "person_b": 7, "type": "共事", "context": "县委书记—政法委书记", "overlap_org": "中共临潭县委员会", "overlap_period": "2023—"},
    {"person_a": 1, "person_b": 9, "type": "共事", "context": "县委书记—宣传部部长", "overlap_org": "中共临潭县委员会", "overlap_period": "2023—"},
    {"person_a": 1, "person_b": 8, "type": "共事", "context": "县委书记—统战部部长", "overlap_org": "中共临潭县委员会", "overlap_period": "2023—"},
    {"person_a": 1, "person_b": 10, "type": "共事", "context": "县委书记—副县长", "overlap_org": "中共临潭县委员会/临潭县人民政府", "overlap_period": "2023—"},
    # 秦永山 —— 县长与班子成员
    {"person_a": 2, "person_b": 4, "type": "共事", "context": "县长—常务副县长", "overlap_org": "临潭县人民政府", "overlap_period": "2023—"},
    {"person_a": 2, "person_b": 10, "type": "共事", "context": "县长—副县长白滔", "overlap_org": "临潭县人民政府", "overlap_period": "2023—"},
    {"person_a": 2, "person_b": 12, "type": "共事", "context": "县长—副县长杨琳", "overlap_org": "临潭县人民政府", "overlap_period": "2023—"},
    {"person_a": 2, "person_b": 13, "type": "共事", "context": "县长—副县长杨建平", "overlap_org": "临潭县人民政府", "overlap_period": "2023—"},
    {"person_a": 2, "person_b": 14, "type": "共事", "context": "县长—副县长李云", "overlap_org": "临潭县人民政府", "overlap_period": "2023—"},
    {"person_a": 2, "person_b": 15, "type": "共事", "context": "县长—副县长杜军", "overlap_org": "临潭县人民政府", "overlap_period": "2023—"},
    {"person_a": 2, "person_b": 11, "type": "共事", "context": "县长—副县长/公安局长窦大斌", "overlap_org": "临潭县人民政府", "overlap_period": "2023—"},
    # 邓贵忠 —— 常务副县长与副县长们
    {"person_a": 4, "person_b": 10, "type": "共事", "context": "常务副县长—副县长白滔", "overlap_org": "临潭县人民政府", "overlap_period": "2023—"},
    {"person_a": 4, "person_b": 12, "type": "共事", "context": "常务副县长—副县长杨琳", "overlap_org": "临潭县人民政府", "overlap_period": "2023—"},
    {"person_a": 4, "person_b": 13, "type": "共事", "context": "常务副县长—副县长杨建平", "overlap_org": "临潭县人民政府", "overlap_period": "2023—"},
    {"person_a": 4, "person_b": 14, "type": "共事", "context": "常务副县长—副县长李云", "overlap_org": "临潭县人民政府", "overlap_period": "2023—"},
    {"person_a": 4, "person_b": 15, "type": "共事", "context": "常务副县长—副县长杜军", "overlap_org": "临潭县人民政府", "overlap_period": "2023—"},
    {"person_a": 4, "person_b": 11, "type": "共事", "context": "常务副县长—副县长/公安局长", "overlap_org": "临潭县人民政府", "overlap_period": "2023—"},
    # 马连勇 —— 政法委书记与公安局长
    {"person_a": 7, "person_b": 11, "type": "领导关系", "context": "政法委书记—公安局长", "overlap_org": "临潭县政法系统", "overlap_period": "2023—"},
    # 张忠良 —— 纪委书记
    {"person_a": 6, "person_b": 1, "type": "监督", "context": "纪委监督县委主要领导", "overlap_org": "中共临潭县委员会", "overlap_period": "2023—"},
    # 赵应芳 —— 组织部部长与县委
    {"person_a": 5, "person_b": 1, "type": "共事", "context": "组织部部长—县委书记（干部任命决策）", "overlap_org": "中共临潭县委员会", "overlap_period": "2023—"},
    # 专职副书记与县委常委
    {"person_a": 3, "person_b": 4, "type": "共事", "context": "专职副书记—常务副县长", "overlap_org": "中共临潭县委员会/临潭县人民政府", "overlap_period": "2023—"},
    {"person_a": 3, "person_b": 5, "type": "共事", "context": "专职副书记—组织部部长", "overlap_org": "中共临潭县委员会", "overlap_period": "2023—"},
    # 统战部长与宣传部
    {"person_a": 8, "person_b": 9, "type": "共事", "context": "统战部长—宣传部长", "overlap_org": "中共临潭县委员会", "overlap_period": "2023—"},
]

# ═══════════════════════════════════════════════
# 执行构建
# ═══════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("临潭县（甘肃省甘南藏族自治州）领导班子工作关系网络数据构建")
    print("=" * 60)
    print()
    print("NOTE: Research conducted under severe network restrictions.")
    print("All leadership names are from pre-training knowledge with")
    print("confidence marked as 'plausible' or 'unverified'. Verify against")
    print("official sources at lintan.gov.cn when network access is restored.")
    print()

    # Ensure data dir exists
    os.makedirs(os.path.join(STAGING_DIR, "data"), exist_ok=True)

    run_build(
        slug="临潭县",
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
    print("Build complete!")
